# vim: colorcolumn=101 textwidth=100

from . import core_loop  # Local module
from . import database   # Local module
from . import drawing    # Local module

from .utils import log   # Local module


####################################################################################################
# API
####################################################################################################

class Pipeline:

    def __init__(self, param_1, param_2 = None):
        """
        You can create an object of this class in two different ways:

        Option #1 (to create a new entry in the supporting database):

        @param param_1: URL of the supporting database that we will use to create and save a new
            pipeline as defined in param_2. Example:

                mongodb://localhost:27017/pipelines

        @param param_2: Path to a json/toml file containing a pipeline definition. Examples:

                some/path/to/my/file/pipeline.json
                some/path/to/my/file/pipeline.toml

            If the pipeline file contains more that one pipeline, the pipeline called "main" will
            be chosen by default. If you want a different one, the name of the file needs to be
            followed by ":" plus the name of the pileline. Examples:

                some/path/to/my/file/pipeline.json::second
                some/path/to/my/file/pipeline.toml::failure_fallback

            If the pipeline is being triggered from another one you should specify its ID (as
            returned from Pipeline.uri() or Pipeline.run()). Examples:

                some/path/to/my/file/pipeline.json::second::<id>
                some/path/to/my/file/pipeline.toml::failure_fallback::<id>

        Option #2 (to obtain a reference to an already existing entry in the supporting database):

        @param param_1: One of the IDs returned by a previous call to "Pipeline.run()" or
            "Pipeline.uri()"

        @param param_2: Leave it empty!
        """

        if param_2 is None:
            self._database_url  = param_1.split("#")[0]
            self._file          = None

            pipeline_id         = param_1.split("#")[1]

        else:
            tokens = param_2.split("::")

            if len(tokens) == 1:
                file_name, pipeline_name, parent_pipeline_id = tokens[0], "main", ""

            elif len(tokens) == 2:
                file_name, pipeline_name, parent_pipeline_id = tokens[0], tokens[1], ""

            else:
                file_name, pipeline_name = tokens[0], tokens[1]

                if param_1 != tokens[2].split("#")[0]:
                    # The parent *must* be in the same database instance in order to be referenced!
                    #
                    log("DEBUG+NORMAL", "WARNING: Ignoring cross-database parent/child relationship")
                    parent_pipeline_id = ""
                else:
                    parent_pipeline_id = tokens[2].split("#")[1]

            self._database_url = param_1
            self._file         = file_name

            pipeline_id        = f"{file_name}::{pipeline_name}::{parent_pipeline_id}"


        self._db_proxy = database.DBProxy(self._database_url, pipeline_id)


    @property
    def uri(self):
        """
        Return an ID token that unequivocally identifies this pipeline.
        """
        return self._database_url + "#" + str(self._db_proxy.pipeline.id)


    def run(self, script_manager, polling_period):
        """
        Run all the jobs that make up the pipeline in order (ie. respecting their dependencies) and
        wait for them to finish.

        This is a blocking function. It will not return until the pipeline is done executing.

        Note that one pipeline can finish with a "request to trigger another pipeline", which itself
        can end with another similar request and so on... This function will only return until all
        the "chained" pipelines have finished.

        @param polling_period: Number of seconds between each polling cycle of the pipeline manager.
            The lower this number, the sooner jobs will be start/stopped, but also more pressure on
            the supporting database. If your jobs typically last more than 5 minutes, setting this
            to 60 is more than enough.

        @param script_manager: object that implements the "pipeforge.Script" interface (ie. an
            object on which we can call "run()", "query()" and "stop()").

        @return a list of tuples of two elements:

            - The first one is the pipeline exit status: "FAILURE", "CANCELED", "SUCCESS" or
              "TRIGGER:<name_of_new_pipeline>".

            - The second one is an ID token that unequivocally identifies this pipeline.

            Elements in the list are returned in order of execution. This means that if there are
            more than one elements, the first N-1 one will always have status == "TRIGGER:..." and
            the last one will always have a status of "FAILURE", "CANCELED" or "SUCCESS".
        """

        ret = []

        # Start the core loop that triggers each of the job scripts in turn and waits for them to
        # finish
        #
        result = core_loop.run_pipeline(self._db_proxy,
                                        script_manager,
                                        polling_period)

        ret.append((result,
                    self._database_url + "#" + str(self._db_proxy.pipeline.id)))

        # If the pipeline returned "TRIGGERED:<new_pipeline_name>", then create a new Pipeline
        # object and run it with the same script_manager and polling_period
        #
        while result.startswith("TRIGGER:"):

            new_pipeline_name = result.split(":")[1]

            if self._file:
                # Load the new Pipeline from the same file that was used to create the current
                # Pipeline
                #
                new_pipeline_id = f"{self._file}::{new_pipeline_name}::{ret[-1][1]}"

            else:
                # The current pipeline was not loaded from disk but directly from the DB. This
                # means we are "replaying" a previously executed pipeline.
                #
                # When it was first executed it might or might not have requested a secondary
                # pipeline execution, which means that "new_pipeline_name" might or might not be in
                # the DB.
                #
                # TODO: Options we have here:
                #
                #       A) Return an error. Tell the user replayed pipelines are not allowed to
                #          trigger other pipelines.
                #
                #       B) When a pipeline is saved to the DB, save also the TOML/JSON data with it,
                #          so that we can load it back here and use it to create new_pipeline_name.
                #
                new_pipeline_id = "TODO"
                raise("Not implemented: triggering a pipeline from a replayed pipeline")

            new_pipeline = Pipeline(self._database_url, new_pipeline_id)

            result = core_loop.run_pipeline(new_pipeline._db_proxy,
                                            script_manager,
                                            polling_period)

            ret.append((result,
                        new_pipeline._database_url + "#" + str(new_pipeline._db_proxy.pipeline.id)))

        return ret


    def draw_timeline(self, mode):
        """
        Draw all pipeline jobs over a timeline taking into consideration their start and stop times.

        @param mode: Defines how to "draw" the timeline. Supported values are:

            - "ascii:<width>:<where>:<scale>": Print to <where> using ASCII characters. Each line
              can be up to <width> columns long. <where> can be one of these:

                  - "stdout"                : print to the current stdout
                  - "buffer"                : print to a buffer and return it to the caller
                  - "file@path/to/file.txt" : print to the specified file (ex:
                                              "file@/tmp/timeline.txt")

              <scale> can be either "minutes", "hours" or "auto" and affects the precission of the
              timestamps printed in the horizontal axis.

              Exampe: "ascii:150:stdout:auto"

            - "unicode:<width>:<where>:<scale>": Same as the previous mode, but use unicode
              characters instead of ASCII. This makes the time line prettier but might not be
              supported in all terminals.

            - "png": <NOT YET SUPPORTED>

        @return None or other values depending on the selected @ref mode.
        """

        return drawing.draw_timeline(self._db_proxy, mode)

