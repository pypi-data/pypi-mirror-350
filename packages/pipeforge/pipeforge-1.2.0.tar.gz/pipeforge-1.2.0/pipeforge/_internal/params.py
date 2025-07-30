# vim: colorcolumn=101 textwidth=100

import mongoengine  # Not included in python's standard lib (ie. need to be "pip install"ed)

from .database import Job



####################################################################################################
# API
####################################################################################################

class JobParams():

    def __init__(self, db_job_id):
        """
        This class represents a job running inside a pipeline.

        @param db_job_id: Job identification token. Scripts running inside a pipeline will typically
            receive this token as an environment variable. You don't need to know its format
            (instead, just use its opaque value), but for the shake of completeness it is a string
            with two tokens separated by a "#":

             - The first token is the database URL. Example:

                   mongodb://localhost:27017/pipelines

             - The second token is the Job() document ID inside that database whose input and output
               parameters we want to access. It looks like this:

                   644969f17dc00d3911e77df7

             Thus, the full "db_job_id" looks like this:

                   mongodb://localhost:27017/pipelines#644969f17dc00d3911e77df7
        """
        database_url, job_id = db_job_id.split("#")

        mongoengine.connect(host = database_url)

        self._job = Job.objects.get(id=job_id)


    def get_input_parameters_and_values(self):
        """
        Return a dictionary containing the job input parameters where, for each entry:

          - The key is a string with the name of the input parameter.
          - The value is a string with its value.

        The returned dictionary will also contains these extra/secret entries:

          - "__pipeline_id" contains an ID string that identifies the pipeline object (in a
            database) this job belongs to. This is only useful for reporting purposes, as no other
            API from this class uses this value.

          - "__pipeline_stdout" contains a string that "hints" on how to access stdout from the
            pipeline engine itself. This could be a path to a file, a hostname + PID, a URL to a
            Jenkins execution, etc...

          - "__job_attempt" contains how many times this job has been reatempted. In other words:
            the first time a job is executed this parameter will be set to "0", the second one it
            will be set to "1", etc...  Notice that a job is only ever reattempted if its "retries"
            property is > 0.

        Example:

           >>> jp = JobParams(...)
           >>> jp.get_input_parameters_and_values()
           { "flavor"            : "vanilla",
             "price"             : "5 euro",
             "__pipeline_id"     : "6483328783e96bafb389535c",
             "__pipeline_stdout" : "http://jenkins.example.com/job/Job_runner/1232/",
             "__job_attempt"     : "0"}

        Note that you are expected to only *read* this dictionary values and *not* modify them.
        """

        aux = self._job.input.copy()
        aux["__pipeline_id"]     = str(self._job.metadata.pipeline.metadata.db_uri) + "#" + \
                                   str(self._job.metadata.pipeline.id)
        aux["__pipeline_stdout"] = str(self._job.metadata.pipeline.metadata.exe_uri)

        if self._job.metadata.original_retries == "N/A": # this happens on detached jobs
            aux["__job_attempt"] = "0"
        else:
            aux["__job_attempt"]     = str(int(self._job.metadata.original_retries) - \
                                           int(self._job.retries))

        return aux


    def get_output_parameters(self):
        """
        Return a list of all the output parameters that you are expected to later set in one single
        call to "set_output_parameters_and_values()".

        Each element of the returned list is a string containing the name of the parameter.

        Example:

           >>> jp = JobParams(...)
           >>> jp.get_output_parameters()
           [ "result", "executed_tests" ]
        """

        return list(self._job.output.keys())


    def set_output_parameters_and_values(self, new_output_dictionary):
        """
        Set the dictionary containing the job output parameters where, for each entry:

          - The key is a string with the name of the output parameter.
          - The value is a string with its value.

        Typically the list of keys of "new_output_dictionary" will exactly match the list of strings
        returned by "get_output_parameters()". In other words: you will only need to call this
        function once, at the end of your job, with all the values for all output parameters:

        Example:

           >>> jp = JobParams(...)
           >>> jp.set_output_parameters_and_values({"result" : "OK", "executed_tests" : "11"})

        However, it is also possible to call it several times, providing only a subset of all the
        (key, value) pairs each time.

           >>> jp = JobParams(...)
           >>> jp.set_output_parameters_and_values({"result" : "OK"})
           >>> ...
           >>> jp.set_output_parameters_and_values({"executed_tests" : "11"})

        In case of one value being provided in more than one call, the last one will prevail:

           >>> jp = JobParams(...)
           >>> jp.set_output_parameters_and_values({"result" : "OK"})
           >>> ...
           >>> jp.set_output_parameters_and_values({"executed_tests" : "11"})
           >>> ...
           >>> jp.set_output_parameters_and_values({"result" : "KO"})  <---------- This is the "good" one now.
        """

        aux = self._job.output.copy()
        aux.update(new_output_dictionary)

        self._job.update(set__output=aux)
        self._job.reload()

