# vim: colorcolumn=101 textwidth=100

import os
import sys
import json
import socket

import mongoengine    # Not included in python's standard lib (ie. need to be "pip install"ed)

from .utils import log          # Local module
from .      import file_loader  # Local module



####################################################################################################
# Job database schema
####################################################################################################

# The pipeline manager depends on an external MongoDB server where we will be storing information
# about the pipeline we run.
#
# More specifically, two "collections" will be created in a database (typically called "pipelines")
# inside the MongoDB server:
#
#   - The "pipeline" collection will contain "pipeline objects" represented by the "Pipeline" python
#     class.
#     Each of them stores the time the pipeline was started/stopped and pointers to other pipelines
#     that were executed as "retriggers" of the current one.
#
#   - The "job" collection will contain "job objects" represented by the "Job" python class.
#     Each of them stores information associated to one job (aka. "step") of a given pipeline, such
#     as the script to execute, the number of retries, what to do with the pipeline if the job
#     fails, input and output parameters, etc...
#
# When a pipeline is run for the first time from a *.{json,toml} specification file, this is what
# happens:
#
#   1. A Pipeline() object is created
#
#   2. For each job definition found in the *.{json,toml} file, a Job() object is created and linked
#      to the Pipeline() object created in the previous step:
#
#                         .--- Job()
#                         |
#          Pipeline() <---+--- Job()
#                         |
#                         '--- Job()
#
#
# When we want to retrigger a previously executed pipeline, this is what happens:
#
#   1. A *new* Pipeline() object is created and linked to the original Pipeline()
#
#   2. For all Job()s that need to be retriggered (for example #1 and #2), new Job() entries are
#      created and linked to the new Pipeline():
#
#                         .--- Job()
#                         |
#          Pipeline() <---+--- Job()
#          *original*     |
#                         '--- Job()
#
#                         .--- Job() *copy*
#                         |
#          Pipeline() <---+--- Job() *copy*
#          *new*
#
#   3. For all Job()s that don't need to be retriggered (for example #3) a new link is
#      added from the original Job() to the new Pipeline():
#
#                         .--- Job()
#                         |
#          Pipeline() <---+--- Job()
#          *original*     |
#                         '--- Job() ----->------.
#                                                |
#                         .--- Job() *copy*      |
#                         |                      |
#          Pipeline() <---+--- Job() *copy*      |
#          *new*          |                      |
#                         '-------------<--------'
#
#
#      NOTE: When does this happen? When re-triggering a pipeline from the middle. For example if
#      one of the latest jobs failed (for example due to external circumnstances) and we want to
#      retrigger the pipeline from that point because we know it is not needed to go through the
#      whole process again.
#
#
# Internally, MongoDB stores JSON objects inside "collections". We could work with our python
# "Pipeline" and "Job" classes and every time we want to update the database, first serialize the
# class instance into a JSON string and then use the "pymongo" library to send these strings to the
# server... *or*, we could use a higher level library such as "mongoengine", which automatically
# maps python classes into MongoDB objects. Example:
#
#   class Book(mongoengine.Document):
#       title  = mongoengine.StringField()
#       author = mongoengine.StringField()
#
#   bible = Book()
#   bible.title  = "The Bible"
#   bible.author = "Many people"
#   bible.save()   <---------- This creates a JSON entry in the "Book" collection in the remote
#                              MongoDB server
#
# Following this strategy, we are going two create two "mongoengine" classes ("Pipeline" and "Job")
# for the two collections we will be using.
#
#   NOTE: There are also two auxiliary classes ("PipelineMetadata" and "JobMetadata") that are only
#   used for the purpose of embedding a dictionary in the original class (this makes it possible to
#   have a "hierarchy" in the final JSON object stored in MongoDB)


class PipelineMetadata(mongoengine.EmbeddedDocument):
    name          = mongoengine.StringField()

    current_state = mongoengine.StringField()  # "WAITING", "RUNNING", etc..

    start_time    = mongoengine.DateTimeField()
    stop_time     = mongoengine.DateTimeField()

    parent        = mongoengine.ReferenceField("Pipeline")
      #
      # Reference to the parent Pipeline from which the current one was executed. If this is the
      # first time the pipeline is run this variable will be empty.
      # Notice I had to use "Pipeline" (in quotes) because the actual Pipeline class is defined
      # later. Fortunately "mongoengine" allows you to use this trick to work around this
      # limitation.

    fluff         = mongoengine.StringField()
      #
      # JSON string containing the data from the [meta] section (if any) of the *.{json,toml} file
      # that was used to create this Pipeline object.
      # This information is only stored here for user convenience, as pipeforge does not need it for
      # anything.
      # Note that "fluff" will be empty for all pipelines expect the "top level" one (i.e. the one
      # without a "parent")

    db_uri        = mongoengine.StringField()
      #
      # URI of the database that contained this Pipeline object when it was created

    exe_uri       = mongoengine.StringField()
      #
      # This is a reference to the "environment" where the pipeline was executed.
      # In the typical case (you are running pipeforge on the terminal) it will include the hostname
      # and process ID)... but there are other possibilities: if, for example, pipeforge detects
      # that it is being run as a Jenkins job, it will contain the URL to an HTTP page containing
      # the job output.


class Pipeline(mongoengine.Document):
    file_path = mongoengine.StringField()

    metadata  = mongoengine.EmbeddedDocumentField(PipelineMetadata)

    def to_dict(self):
        return {
            "id"        : str(self.id),
            "file_path" : self.file_path,
            "metadata"  : {
                "name"          : str(self.metadata.name),
                "current_state" : str(self.metadata.current_state),
                "start_time"    : str(self.metadata.start_time),
                "stop_time"     : str(self.metadata.stop_time),
                "parent"        : str(self.metadata.parent),
                "fluff"         : str(self.metadata.fluff),
                "db_uri"        : str(self.metadata.db_uri),
                "exe_uri"       : str(self.metadata.exe_uri)
            }
        }


class JobMetadata(mongoengine.EmbeddedDocument):
    pipeline         = mongoengine.ReferenceField(Pipeline)

    dependencies     = mongoengine.ListField(mongoengine.StringField())

    original_retries = mongoengine.StringField()  # "retries", "input" and "output" are modified
    original_input   = mongoengine.DictField()    # while the pipeline is running. We need to save
    original_output  = mongoengine.DictField()    # here the original values in case we later want
                                                  # to restart the pipeline (fully or partially)

    current_state    = mongoengine.StringField()  # "WAITING", "RUNNING", etc..

    executions_id    = mongoengine.ListField(mongoengine.StringField())   # For each execution
    executions_uri   = mongoengine.ListField(mongoengine.StringField())   # (which can be more than
    start_times      = mongoengine.ListField(mongoengine.DateTimeField()) # one if retries>0) we
    start2_times     = mongoengine.ListField(mongoengine.DateTimeField()) # save these items.
    stop_times       = mongoengine.ListField(mongoengine.DateTimeField()) # NOTE: "start2" is when
    results          = mongoengine.ListField(mongoengine.StringField())   # the job *really* starts
                                                                          # executing (after waiting
                                                                          # in queue, if applicable)


class Job(mongoengine.Document):
    name         = mongoengine.StringField()
    script       = mongoengine.StringField()
    runner       = mongoengine.StringField()
    detached     = mongoengine.StringField()
    timeout      = mongoengine.StringField()
    retries      = mongoengine.StringField()
    on_failure   = mongoengine.StringField()
    on_input_err = mongoengine.StringField()

    input      = mongoengine.DictField()
    output     = mongoengine.DictField()

    metadata   = mongoengine.EmbeddedDocumentField(JobMetadata)

    def to_dict(self):
        return {
            "id"           : str(self.id),
            "name"         : self.name,
            "script"       : self.script,
            "runner"       : self.runner,
            "detached"     : self.detached,
            "timeout"      : self.timeout,
            "retries"      : self.retries,
            "on_failure"   : self.on_failure,
            "on_input_err" : self.on_input_err,
            "input"        : self.input,
            "output"       : self.output,
            "metadata"     : {
                "pipeline"         : str(self.metadata.pipeline.id),
                "dependencies"     : self.metadata.dependencies,
                "original_retries" : self.metadata.original_retries,
                "original_input"   : self.metadata.original_input,
                "original_output"  : self.metadata.original_output,
                "current_state"    : self.metadata.current_state,
                "executions_id"    : self.metadata.executions_id,
                "executions_uri"   : self.metadata.executions_uri,
                "start_times"      : [str(x) for x in self.metadata.start_times],
                "start2_times"     : [str(x) for x in self.metadata.start2_times],
                "stop_times"       : [str(x) for x in self.metadata.stop_times],
                "results"          : self.metadata.results
            }
        }



####################################################################################################
# API
####################################################################################################

class DBProxy():
    """
    Proxy object that establishes a mapping with pipeline data stored in a remote database.

    One instance of this class represents *one* full pipeline, which includes:

      - One Pipeline() object, which can be obtained by calling "pipeline()" on the instance
      - Several Job() objects, which can be ontained by calling "jobs()" on the instance
    """

    def __init__(self, database_url, pipeline_id):
        """
        @param database_url: URL of the database where pipeline data can be found. Example:

            mongodb://localhost:27017/pipelines

        @param pipeline_id: Identifier of the pipeline that we want to work with. It can take two
            different types of values:

            - A path to a json/toml file containing a pipeline definition, followed by "::",
              followed by the name of the pipeline inside the file (usually "main"), followd by
              "::", followed by the nothing or ID of an already existing pipeline in @ref
              database_url.

              In this case a new pipeline object will be created in @ref database_url and its parent
              will be set to the provided ID after the second "::" (if any). Examples:

                  some/path/to/my/file/pipeline.json::main::
                  some/path/to/my/file/pipeline.toml::failure_fallback::701ab7e09abe5e7261092834

            - The ID of an already existing pipeline in @ref database_url. Example:

                  64512b58dd70fd2adba57103
        """

        log("DEBUG+NORMAL", "")
        log("DEBUG+NORMAL", "Connecting to external database...")

        try:
            mongoengine.connect(host=database_url)

            log("DEBUG", "  - Connection successful")
        except Exception:
            log("ERROR", "  - Connection to external database failed. Aborting")
            sys.exit(-1)

        self._database_url     = database_url
        self._pipeline_db      = None
        self._jobs_db          = []
        self._job_dependencies = {}


        # Obtain a reference to the pipeline object (first creating and inserting new entries in the
        # remote database if needed):
        #
        if "::" in pipeline_id:
            self._pipeline_db = self._load_from_disk(pipeline_id.split("::")[0],
                                                     pipeline_id.split("::")[1],
                                                     pipeline_id.split("::")[2])
        else:
            self._pipeline_db = self._load_from_db(pipeline_id)

        log("DEBUG", "")
        log("DEBUG", "pipeline_db object:")
        log("DEBUG", self._pipeline_db.to_dict())

        log("DEBUG", "")
        log("DEBUG", "job_db objects associated to the previous pipeline_db object:")
        for i, job_db in enumerate(Job.objects(metadata__pipeline=self._pipeline_db)):
            log("DEBUG", f"#{i}:")
            log("DEBUG", job_db.to_dict())


        # Obtain a list of references to all the job objects that are part of the pipeline
        #
        self._jobs_db = Job.objects(metadata__pipeline=self._pipeline_db)


        # Create a dependencies dictionary where each entry key is a job name and its value the list
        # of job names it depends on
        #
        for job_db in Job.objects(metadata__pipeline=self._pipeline_db):
            self._job_dependencies[job_db.name] = job_db.metadata.dependencies

        log("DEBUG", "")
        log("DEBUG", "Pipeline dependencies structure:")
        log("DEBUG", self._job_dependencies)


    def _load_from_disk(self, pipeline_file_path, pipeline_name, parent_pipeline_id=""):
        """
        Load a new pipeline from a JSON/TOML file, create new objects in the remote database that
        represent it (and its associated jobs) and save a reference to the Pipeline() object in
        self._pipeline_db

        @param pipeline_file_path: path to the JSON/TOML file containing the pipeline specification

        @param pipeline_name: name of the pipeline to load from all the ones contained in the file.
            For single pipeline files this will always be "main"

        @param parent_db_id: ID of the Pipeline object in the DB which will be set as the "parent"
        of the new Pipeline object we are about to create. It can be left empty for "no parent".
        """

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Load pipeline data from disk
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        fl            = file_loader.FileLoader(pipeline_file_path)
        pipeline_data = fl.get_pipeline()

        pipeline      = [x for x in pipeline_data["pipelines"] if x["name"] == pipeline_name][0]
        pipeline_deps = fl.get_dependencies()[pipeline["name"]]

        log("DEBUG", "")
        log("DEBUG", "Pipeline data as loaded from disk:")
        log("DEBUG", pipeline)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Insert pipeline/job entries into the database
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        pipeline_db = Pipeline(file_path = pipeline_file_path,
                               metadata  = PipelineMetadata()   # Initially empty
        )

        pipeline_db.metadata.name = pipeline["name"]

        if parent_pipeline_id:
            pipeline_db.metadata.parent = Pipeline.objects.get(id=parent_pipeline_id)
        else:
            if "meta" in pipeline_data:
                pipeline_db.metadata.fluff = json.dumps(pipeline_data["meta"])

        pipeline_db.metadata.db_uri = self._database_url

        if os.getenv("JENKINS_URL") and os.getenv("BUILD_URL"):
            # It looks like the pipeline is being executed in a Jenkins instance. We can access its
            # ouput of the URL contains in environment variable BUILD_URL
            #
            pipeline_db.metadata.exe_uri = os.getenv("BUILD_URL") + "console"
        else:
            # Use hostname + PID
            #
            pipeline_db.metadata.exe_uri = f"{socket.gethostname()}, PID={os.getpid()}"

        pipeline_db.save()

        log("DEBUG", "")
        log("DEBUG", f"New pipeline object added to database (id={pipeline_db.id})")


        # Insert all job objects into the "job collection"
        #
        for job in pipeline["jobs"]:

            j_db = Job(**job)

            j_db.metadata = JobMetadata(
                              pipeline         = pipeline_db,
                              dependencies     = pipeline_deps[job["name"]],
                              original_retries = job["retries"],
                              current_state    = "WAITING",
                              executions_id    = [],
                              executions_uri   = [],
                              start_times      = [],
                              stop_times       = [],
                              results          = []
            )

            if "input"  in job.keys(): j_db.metadata["original_input"]  = job["input"]
            if "output" in job.keys(): j_db.metadata["original_output"] = job["output"]

            j_db.save()

        return pipeline_db


    def _load_from_db(self, pipeline_id):
        """
        Retrieve a given pipeline object from the remote database and save a reference to the
        associated local Pipeline() object in self._pipeline_db.
        """

        log("DEBUG", "")
        log("DEBUG", f"Reusing a previously existing pipeline object (id={pipeline_id})")

        pipeline_db = Pipeline.objects.get(id=pipeline_id)

        return pipeline_db


    ################################################################################################
    # External API
    ################################################################################################

    @property
    def database_url(self):
        """
        Return the database URL originally provided when creating the DBProxy() object.
        """
        return self._database_url


    @property
    def job_dependencies(self):
        """
        Return a dictionary of dependencies where each entry has this format:
          - key  : job name from the current pipeline
          - value: list of other job names it depends on

        Example:

            >>> db_proxy = DBProxy("pipelines/example.toml")
            >>> print(db_proxy.job_dependencies)
            {'Test 1': ['Build'], 'Test 2': ['Build'], 'Build': ['Download'], 'Send email': ['Test 1', 'Test 2']}
        """
        return self._job_dependencies


    @property
    def pipeline(self):
        """
        Return the Pipeline() object that is associated to the current DBProxy handler.
        The JSON data associated to this Pipeline() object can be queried using "dot notation".

        Example:

            >>> db_proxy = DBProxy("pipelines/example.toml")
            >>> print(db_proxy.pipeline.file_path)
            pipelines/example.toml

        In addition, two methods can be called on the returned object:

          - obj.save() will push the value of *modified* fields to the database (ie. the whole
            remote object is not overwriten, thus you don't have to worry about other fields)

          - obj.reload() will replace the whole local object (ie. "all fields") with a copy of the
            data stored in the database.
        """
        return self._pipeline_db


    @property
    def jobs(self):
        """
        Return the list of Job() objects that make up the Pipeline() associated to the current
        DBProxy handler.

        The JSON data associated to these Job() objects can be queries using "dot notation".

        Example:

            >>> db_proxy = DBProxy("pipelines/example.toml")
            >>> for job_db in db_proxy.jobs: print(job_db.name)
            Test 1
            Test 2
            Build
            Send email

        In addition, two methods can be called on the returned object:

          - obj.save() will push the value of *modified* fields to the database (ie. the whole
            remote object is not overwriten, thus you don't have to worry about other fields)

          - obj.reload() will replace the whole local object (ie. "all fields") with a copy of the
            data stored in the database.
        """
        return self._jobs_db

