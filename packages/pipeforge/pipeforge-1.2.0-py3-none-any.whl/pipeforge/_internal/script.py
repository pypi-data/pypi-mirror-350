# vim: colorcolumn=101 textwidth=100

import os
import sys
import uuid
import time
import shutil
import random
import subprocess
import datetime

from .params import JobParams  # Local module
from .utils  import log        # Local module



####################################################################################################
# Virtual interface for the "ScriptManager" class
####################################################################################################

class ScriptManager():
    """
    A ScriptManager object is the one in charge of starting, querying and stopping job scripts.

    This class is meant to be used as a base clase of a more specialized one which actually
    implements the methods below.

    Example:

        class MyScript(pipeforge.ScriptManager):
            def run(self, description, script_name, modifiers, db_job_id):
                ...
            def query(self, execution_id):
                ...
            def stop(self, execution_id):
                ...

    Then you are meant to provide an instance of this specialized class to
    "pipeforge.Pipeline.run()", like this:

        import pipeforge

        p = pipeline.Pipeline(...)
        p.run(script_manager = MyScript(...))
    """

    def run(self, description, script_name, modifiers, db_job_id):
        """
        Start running a script and return an ID associated to its execution.

        @param description: short description of the job (for human consumption)

        @param script_name: name of the script to run, as provided in the "script" field of the
            associated job in the *.toml pipeline definition. It will have different meaning to
            different subclasses of ScriptManager(). Some examples:

              - The path to a script in the local file system
              - The URL of a REST API endpoint to trigger the job in a remote Jenkins instance
              - The key of a dictionary of pre-defined scripts
              - Etc...

        @param modifiers: additional restrictions considerations regarding where/how the script
            should be run, as provided in the "runner" field of the associated job in the *.toml
            pipeline definition. It will have different meaning to different subclasses of
            ScriptManager(). Some examples:

              - The name of a specific remote machine
              - A comma separated list of tags a Jenkins agent must contain when considering which
                one to use
              - The name a docker image
              - Etc...

            Check the documentation of each subclass for details.

        @param db_job_id: this is the "token" that the script manager will make available "somehow"
            to the script so that it can use as a parameter to JobParams() which it needs to read
            input parameters and set output parameters. The way this "token" is made available to
            the script depends on the specific subclass of ScriptManager(). Some examples:

              - As an environment variable
              - As an input argument to the script
              - As the contents of a predefined file in the file system
              - Etc...

            The "token" itself should be treated as an opaque type: the script manager should not do
            anything with it except for passing it to the script.

        @return execution_id, which can be used by the rest of methods of this class to query/stop
            the script that we just started here.
        """

        raise NotImplementedError("method 'run()' not yet implemented")


    def query(self, execution_id):
        """
        Return the current status of the script that was started by "run()"

        @param execution_id: handler returned by the call to "run()" that started the script whose
           status we want to query.

        @return one of these:

           - "NOT FOUND" : The provided execution_id is incorrect.
           - "QUEUED"    : The script is waiting to be started, which will eventually happen.
           - "RUNNING"   : The script is currently running.
           - "SUCCESS"   : The script has finished executing and returned OK.
           - "FAILURE"   : The script has finished executing and returned KO.
           - "CANCELED"  : The script has been externally canceled (by calling stop()), either while
                           "RUNNING" or while "QUEUED"
        """

        raise NotImplementedError("method 'query()' not yet implemented")


    def stop(self, execution_id):
        """
        Stop a running (or queued) script previously started with "run()".

        @param execution_id: handler returned by the call to "run()" that started the script whose
           status we want to stop.
        """

        raise NotImplementedError("method 'query()' not yet implemented")


    def exe_uri(self, execution_id):
        """
        Return a reference to "some object" with more information about the job execution.

        @param execution_id: handler returned by the call to "run()" that started the script whose
           status we want to stop.

        @return a string that contains some type of reference (a URL, a path in the local file
            system, etc...) containing more information about the requested execution.
            Check the specific subclass documentation for more details.
        """

        raise NotImplementedError("method 'query()' not yet implemented")


####################################################################################################
# "Dummy" script manager
####################################################################################################

class DummyScriptManager(ScriptManager):
    """
    This runner ignores the provided script name and instead pretends it is waiting on queue for X
    seconds and then pretends it is running Y more seconds.

    Once it finishes the required output parameters will automatically be set to a random value
    different from "?" to trick the pipeline manager into thinking execution took place as expected.

    Notice that you can run *any* pipeline with this class, as it does not require any particular
    input parameter to be present on any of the jobs. In other words, you can use DummyScript() to
    "simulate" the execution of one real pipeline (even if the timings will obviously not be the
    same).

    NOTE:
        Contrary to what is recommended in the documentation of the "pipeforge.ScriptManager.run()"
        function, this specialized class *will* use the "db_job_id" "token" to simulate what a real
        script would do.
        This is obviously a hack due to the nature of this specialized subclass: a real subclass
        implementation would never do this and always treat "db_job_id" as an opaque type.
    """

    def __init__(self):
        self._processes_table = {}
        self._min_queue   = 0
        self._max_queue   = 5
        self._min_run     = 3
        self._max_run     = 9


    def run(self, description, script_name, modifiers, db_job_id):
        """
        See ScriptManager.run() and then read this:

        @param modifiers is ignored in this subclass
        """

        job_params   = JobParams(db_job_id)
        execution_id = uuid.uuid4().hex


        self._processes_table[execution_id] = (
            int(time.time()),                                 # Start timestamp
            random.randint(self._min_queue, self._max_queue), # Time in queue (seconds)
            random.randint(self._min_run,   self._max_run),   # Time running  (seconds)
            job_params
        )

        return execution_id


    def query(self, execution_id):

        if execution_id not in self._processes_table:
            return "CANCELED"

        start_time    = self._processes_table[execution_id][0]
        time_in_queue = self._processes_table[execution_id][1]
        time_running  = self._processes_table[execution_id][2]
        job_params    = self._processes_table[execution_id][3]

        current_time = int(time.time())

        if current_time > start_time + time_in_queue + time_running:
            # Hack: the real script would have set the expected output parameters while running.
            # In this dummy implementation (which simply runs "sleep") we need to do it here, when
            # the pipeline manager queries the state and we figure out that the script has already
            # finished executing.

            fake_output = {}
            i           = 0

            for output_param in job_params.get_output_parameters():
                fake_output[output_param] = f"Fake param #{i}"
                i += 1

            job_params.set_output_parameters_and_values(fake_output)

            return "SUCCESS"

        elif current_time > start_time + time_in_queue:

            return "RUNNING"

        else:

            return "QUEUED"


    def stop(self, execution_id):
        self._processes_table[execution_id].kill()
        del self._processes_table[execution_id]


    def exe_uri(self, execution_id):
        return ""


####################################################################################################
# "Test" script manager (for unit tests)
####################################################################################################

class TestScriptManager(ScriptManager):
    """
    This runner ignores the provided script name and instead simulates that it is running for some
    time. More specifically, once you call "run()" on this object...

      - The next "x-1" calls you make to "query()" will always return "RUNNING"
      - Call "x" to "query()" will return the value provided in input argument "return_code"

    ...where "x" is the number provided in input argument "run_time"

    This makes execution time independent from the POLL INTERVAL that the pipeline manager is using,
    which makes it convenient to obtain deterministic results.

    The last call to "query()" (ie. the one that no longer returns "RUNNING") will also set output
    parameters to a random value different from "?" to trick the pipeline manager into thinking
    execution took place as expected. The only exception to this is that if there is an output
    parameter called "output" it will be set to the value of input parameter "output_value".

    Notice that you can only use this runner with a special type of pipelines. In particular, all
    jobs defined in the pipeline must have "run_time", "return_code" and (optionally) "output_value"
    as input parameters. This means you can not use it with a real pipeline. The benefit is that you
    get more control over those two parameters, making this type or runner ideal for testing the
    pipeline manager itself.

    If a job is configured to have retries, you can specify:
      - ...a different "run_time" on each of them by using a "+" separator, like this:
        run_time = 2+4+1
      - ...a different "return_code" on each of them by using a "+" separator, like this:
        return_code = "FAILURE+FAILURE+SUCCESS"
      - ...a different "output_value" on each of them by using a "+" separator, like this:
        output_value = "cocacola+fanta+pepsi"

    NOTE:
        Contrary to what is recommended in the documentation of the "pipeforge.ScriptManager.run()"
        function, this specialized class *will* use the "db_job_id" "token" to simulate what a real
        script would do and also return different values depending on the number of pending retries.
        This is obviously a hack due to the nature of this specialized subclass: a real subclass
        implementation would never do this and always treat "db_job_id" as an opaque type.
    """

    def __init__(self):
        self._processes_table = {}


    def run(self, description,  script_name, modifiers, db_job_id):
        """
        See ScriptManager.run() and then read this:

        @param modifiers is ignored in this subclass
        """

        job_params   = JobParams(db_job_id)
        execution_id = uuid.uuid4().hex

        input_params = job_params.get_input_parameters_and_values()

        if "run_time" not in input_params or "return_code" not in input_params:
            raise ValueError("In order to use the \"TestScriptManager\" all jobs defined in the pipeline must have these two input parameters defined: \"run_time\" and \"return_code\"")

        retries_count = int(input_params["__job_attempt"])

        queue_cycles  = input_params["queue_time"].split("+")
        run_cycles    = input_params["run_time"].split("+")
        return_code   = input_params["return_code"].split("+")

        queue_cycles  = int(queue_cycles[retries_count%len(queue_cycles)])
        run_cycles    = int(run_cycles[retries_count%len(run_cycles)])
        return_code   = return_code[retries_count%len(return_code)]

        self._processes_table[execution_id] = [queue_cycles,
                                               run_cycles,
                                               return_code,
                                               job_params]
        return execution_id


    def query(self, execution_id):
        queue_cycles  = self._processes_table[execution_id][0]
        run_cycles    = self._processes_table[execution_id][1]
        return_code   = self._processes_table[execution_id][2]
        job_params    = self._processes_table[execution_id][3]

        if run_cycles == -99:
            return "CANCELED"

        if queue_cycles > 0:
            self._processes_table[execution_id][0] = queue_cycles - 1
            return "QUEUED"

        if run_cycles > 1:
            self._processes_table[execution_id][1] = run_cycles - 1
            return "RUNNING"

        else:
            # Hack: the real script would have set the expected output parameters while running. In
            # this dummy implementation we need to do it here, when the pipeline manager queries the
            # state and we figure out that the script has already finished executing.

            fake_output = {}
            i           = 0

            for output_param in job_params.get_output_parameters():
                if output_param == "output":
                    fake_output["output"] = job_params.get_input_parameters_and_values()["output_value"]
                else:
                    fake_output[output_param] = f"Fake param #{i}"
                i += 1

            job_params.set_output_parameters_and_values(fake_output)

            self._processes_table[execution_id][1] = 1 # In case we query again in the future (which
                                                       # we shouldn't, but if we do, return the
                                                       # same thing
            return return_code


    def stop(self, execution_id):
        self._processes_table[execution_id][0] = -99 # Special indicator for "CANCELED"


    def exe_uri(self, execution_id):
        return ""



####################################################################################################
# "Local" script manager
####################################################################################################

class LocalScriptManager(ScriptManager):
    """
    This runner executes the provided script in the local system, ignoring the "modifiers" argument
    that run() receives.

    Scripts must already be present in the local system and, for convenience, it is recomended to
    provide the full path when calling run()
    """

    def __init__(self):
        self._processes_table = {}


    def run(self, description, script_name, modifiers, db_job_id):
        """
        See ScriptManager.run() and then read this:

        @param modifiers is ignored in this subclass
        """

        if not os.path.exists(script_name):
            # Search in PATH
            #
            new_script_name = shutil.which(script_name)

            if new_script_name is None:
                log("ERROR", f"script <{script_name}> could not be found...")
                sys.exit(-1)
            else:
                script_name = new_script_name

        # Create files to store process STDOUT, STDERR
        #
        template = f"/tmp/pipeforge__{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_" + \
                   f"{os.path.basename(script_name)}"

        fstdout = open(template + ".stdout.txt", mode="w+")
        fstderr = open(template + ".stderr.txt", mode="w+")

        log("DEBUG", f"      - Logging STDOUT to file {fstdout.name}")
        log("DEBUG", f"      - Logging STDERR to file {fstderr.name}")

        p = subprocess.Popen(
                script_name,
                shell  = True,
                env    = os.environ | {"JOB_ID": db_job_id}, # Copy of the current environment plus
                stdout = fstdout,                            # an extra new variable (JOB_ID)
                stderr = fstderr,
                start_new_session=True)

        self._processes_table[str(p.pid)] = [p, fstdout, fstderr]

        return str(p.pid)


    def _final_log(self, execution_id):
        """
        Print log messages indicating process has finished
        """

        #out, err = p.communicate()

        p, fstdout, fstderr = self._processes_table[execution_id]

        log("DEBUG", f"    - script <{p.pid}> has finished executing...")
        log("DEBUG", f"      - STDOUT has been saved to file {fstdout.name}")
        fstdout.close()
        for line in open(fstdout.name).readlines():          # Uncomment for quicker
            log("DEBUG", f"          > {line.rstrip()}")     # debug


        log("DEBUG", f"      - STDERR has been saved to file {fstderr.name}")
        fstderr.close()
        for line in open(fstderr.name).readlines():          # Uncomment for quicker
            log("DEBUG", f"          > {line.rstrip()}")     # debug


    def query(self, execution_id):

        if execution_id not in self._processes_table.keys():
            return "NOT FOUND"

        p = self._processes_table[execution_id][0]

        if p == "CANCELED":
            return "CANCELED"

        if p.poll() is None:
            return "RUNNING"

        # If we reach this point, the process has finished executing.

        self._final_log(execution_id)

        if p.returncode != 0:
            return "FAILURE"

        return "SUCCESS"


    def stop(self, execution_id):
        if execution_id in self._processes_table.keys():

            p = self._processes_table[execution_id]
            p[0].kill()

            p[0] = "CANCELED"  # We don't remove it from the table, instead we set the entry
                               # to "CANCELED" so that query() can figure out this process was
                               # canceled


    def exe_uri(self, execution_id):
        """
        Return the local path to the files where stdout and stderr are being / have been saved.

        When the process is still running you should be able to "tail -f ..." these file to get
        realtime feedback.

        When the process has finished these files will contain the whole STDOUT/STDERR produced.
        """
        if execution_id == "<None>":
            return "(did not start)"

        return f"stdout:{self._processes_table[execution_id][1].name}; stderr:{self._processes_table[execution_id][2].name}"



####################################################################################################
# "Jenkins" script manager
####################################################################################################

class JenkinsScriptManager(ScriptManager):
    """
    This runner executes the provided script on a remote Jenkins instance.

    In order to use this ScriptManager type you need to first set and export an environment variable
    called "PIPEFORGESCRIPT_JENKINS_ENDPOINT" which takes this format:

        <Jenkins instance URL>:::<username>:::<password>:::<job_name>

    Example:

        export PIPEFORGESCRIPT_JENKINS_ENDPOINT='https://jenkins.example.com:::john:::cobra123:::Run_script'

    Note that if the Jenkins instance does not require authentication, you can leave <username> and
    <password> empty, like this:

        export PIPEFORGESCRIPT_JENKINS_ENDPOINT='https://jenkins.example.com::::::Run_script'

    Hint: Don't forget to use sinque quotes (') or bash will complain about ":::"

    <job_name> ("Run_script") in the example above is a regular Jenkins job that you will first have
    to create following these instructions:

      1. Name it as <job_name> (ex: "Run_script" or something like that)

      2. In the "Configure" tab, select the "This project is parameterized" checkbox and add these
         entries:

         - Type: Label
           Name: SLAVE
           Description:
               List of tags (separated by a space) the selected slave to run this job must have.

               Check [1] for valid syntax.

               [1] "label expression", as defined in
               https://kb.novaordis.com/index.php/Jenkins_Job_Label_Expression

         - Type: Multi-string
           Name: ENVIRONMENT
           Description: List <variable>=<value> lines of environment variables to set

      3. Select the "Execute concurrent builds if necessary" checkbox.

      4. In "Build Steps" add this entry:

         - Type: Execute shell
         - Command: /path/to/your/entry_point/run.sh

      "pipeforge" with remotely trigger this job using Jenkins REST API, providing these arguments:

        - SLAVE = <whatever has been specified in the 'runner' field in the pipeline TOML file>
        - ENVIRONMENT = ...
            JOB_DESCRIPTION=<value specified in the 'name' field in the pipeline TOML file>
            JOB_SCRIPT=<value specified in the 'script' field in the pipeline TOML file>
            JOB_ID=<the token to access input and output parameters for the "pipeforge" job >

          NOTE: When pipeforge itself is also running as a Jenkins job, the ENVIRONMENT field will
          contain an extra variable called "JENKINS_PARENT" which points to the URL of the Jenkins
          job running the pipeline, so that children can (if they want) access it.

      "run.sh" is a script *you provide*, preinstalled on each Jenkins slave (or downloaded as part
      of the Jenkins job "command"), responsible for:

        1. Read environment variable "ENVIRONMENT" and "export" all its entries so that they are
           available as environment variables by its children.
           In other words, if "ENVIRONMENT" contains a line that reads "DEBUG_MODE=yes", then
           environment variable "DEBUG_MODE" must exist for all processes started by
           "run.sh".

               NOTE: In addition to "JOB_SCRIPT" and "JOB_ID", the argument "ENVIRONMENT" that is
               sent to Jenkins will also contain all the environment variables that start with
               "PIPEFORGESCRIPT_JENKINS_OPT__". For example, if the following environment variables
               exists:

                   PIPEFORGESCRIPT_JENKINS_OPT__COLOR=blue
                   PIPEFORGESCRIPT_JENKINS_OPT__AGE=33

               The "ENVIRONMENT" will contain these extra entries:

                   COLOR=blue
                   AGE=33

               This feature makes it possible to run jobs in a special/debug mode when needed by
               simply setting variables before running pipeforge.

        2. Run the script referenced by "JOB_SCRIPT" (which could be a full path, a "key" of a table
           that is translated into a set of actions, etc...).
           Each Jenkins slave must obviously have all that is needed to "run" "JOB_SCRIPT" (ie. in
           "Build Steps" you might have to add an extra one that downloads the repository where all
           your "pipeforge" scripts are located).

       This is an example of a simple "run.sh" (in bash) that assumes "JOB_SCRIPT" refers to a
       binary that is on $PATH and can be executed without any special setup:

       > if ! [ -z "$ENVIRONMENT" ]; then
       >
       >     eval $(
       >         while IFS= read -r line
       >         do
       >             echo "export $line"
       >         done < <(printf '%s\n' "$ENVIRONMENT")
       >     )
       > fi
       >
       > $JOB_SCRIPT

      "$JOB_SCRIPT" is a regular "pipeforge" job script, which means it must call
      pipeforge.JobParam(os.getenv("JOB_ID")) to read input parameters and set output parameters in
      the pipeline job.
    """

    def __init__(self):

        import jenkins  # Only needed for this type of script manager, that's why we import it here
                        # (Note: This module is installed with "pip install python-jenkins")

        self._triggered_jobs = {}  
                        #
                        # There will be one entry for each triggered job.
                        #
                        # The <key> is the original "queue" number that is returned by Jenkins when
                        # a job is triggered (this is a monotonic number guaranteed to be unique).
                        #
                        # The <value> is a list of three elements:
                        #   - The first indicates the last known state of the job. It can be
                        #     "QUEUED", "CANCELED", "RUNNING", "SUCCESS" or "FAILURE".
                        #   - The second one is a string containing "more information" about the
                        #     job. It can be be either the string "(queued)" or an URL pointing to a
                        #     to a Jenkins page with more information about the job (ie. its output
                        #     log)
                        #   - The third element can be None or the execution id (a number) that the
                        #     job receives once it is no longer in queue.
                        #   - The fourth element can be "?", None or the queue id (a number) of the
                        #     "semaphore" entry a job (that has already received an execution id)
                        #     has to wait for before *really* start running (note: only special
                        #     Jenkins jobs make use of this "second queue" feature)

        jenkins_server = None

        # Parse environment variable PIPEFORGESCRIPT_JENKINS_ENDPOINT and create jenkins object
        #
        jenkins_info = os.getenv("PIPEFORGESCRIPT_JENKINS_ENDPOINT", "")

        if jenkins_info != "":
            try:
                url, user, passw, job = jenkins_info.split(":::")

                if user == "" and passw == "":
                    jenkins_server = jenkins.Jenkins(url)
                else:
                    jenkins_server = jenkins.Jenkins(url, user, passw)

            except Exception:
                pass

        if jenkins_server is None:
            log("ERROR", "In order to use the 'JenkinsScriptManager' you need to export an environment variable")
            log("ERROR", "called 'PIPEFORGESCRIPT_JENKINS_ENDPOINT' with information regarding the Jenkins endpoint")
            log("ERROR", "capable of running jobs.")
            log("ERROR", "")
            log("ERROR", "For more details run this from the python interpreter:")
            log("ERROR", "")
            log("ERROR", "  import pipeforge")
            log("ERROR", "  help(pipeforge._internal.script.JenkinsScriptManager)")
            log("ERROR", "")
            sys.exit(-1)

        # Make sure the provided Jenkins URL is reachable and contains an actual Jenkins instance
        #
        try:
            jenkins_server.get_version()
        except Exception as e:
            log("ERROR", f"The provided Jenkins url ({url}) does not seem to point to an actual Jenkins instance!")
            log("ERROR", f"Exception: {e}")
            sys.exit(-1)

        # Obtain the offset (in seconds) between the Jenkins server clock and the computer where
        # this script is running.
        #
        try:
            server_time = int(jenkins_server.run_script("println(System.currentTimeMillis())"))//1000
            pc_time     = int(time.time())
        except Exception as e:
            log("ERROR", f"Could not obtain Jenkins' clock current time on {url}")
            log("ERROR", f"Exception: {e}")
            sys.exit(-1)

        self._clock_offset = pc_time - server_time

        # Make sure the provided job exists
        #
        def recursive_search(x, key, matches):
            if isinstance(x, list):
                for i in x:
                    recursive_search(i, key, matches)
            elif isinstance(x, dict):
                for k,v in x.items():
                    if k == key:
                        matches.append(v)
                    elif isinstance(v, dict) or isinstance(v, list):
                        recursive_search(v, key, matches)

        matches = []
        recursive_search(jenkins_server.get_all_jobs(), "fullname", matches)

        if job not in matches:
            log("ERROR", f"The provided Jenkins job ({job}) does not seem to")
            log("ERROR", f"exist in {url}")
            sys.exit(-1)

        # Save data for later use
        #
        self._jenkins_server = jenkins_server
        self._jenkins_job    = job


    def run(self, description, script_name, modifiers, db_job_id):
        """
        See ScriptManager.run() and then read this:

        @param script_name is the name of the script to run. Jenkins' job must have previously been
            configured to "know" where to look for this script (maybe it is in $PATH, or maybe there
            is a hardcoded path in the job configuration)

        @param modifiers must be a string string containing a "Jenkins job label expression", as
            defined in [1]. This is used to restrict on which slaves the job can run. Example:
            "LINUX and FAST"

            [1] https://kb.novaordis.com/index.php/Jenkins_Job_Label_Expression
        """

        slave       = modifiers  # In which node should the scrip run
        environment = {
            "JOB_DESCRIPTION" : f"{description}", # Short job description
            "JOB_SCRIPT"      : f"{script_name}", # Script to run in Jenkins
            "JOB_ID"          : f"{db_job_id}",   # Pipeline job reference (to query for input
                                                  # parameters and set output parameters)

            "JENKINS_PARENT"  : f"{os.getenv('BUILD_URL', '') if os.getenv('JENKINS_URL') else ''}"
                                    #
                                    # When using Jenkins, it is not strange to also have pipeforge
                                    # itself running as a Jenkins job.
                                    # When that happens, environment variable "BUILD_URL" points to
                                    # the URL of that job (otherwise it will be empty).
                                    # We will send its value to the triggered job so that it knows
                                    # which its "parent" Jenkins job is.
                                    # Why? Several reasons... for example, to let the Jenkins child
                                    # execution change the name of the Jenkins parent execution.
        }

        for extra_env in os.environ.keys():
            if extra_env.startswith("PIPEFORGESCRIPT_JENKINS_OPT__"):
                param = extra_env[len("PIPEFORGESCRIPT_JENKINS_OPT__"):]
                value = os.getenv(extra_env)
                environment[param] = value

        attempts = 0
        while True:
            log("DEBUG", f"      - Triggering {script_name} in Jenkins@{self._jenkins_job}:")
            log("DEBUG", f"        - SLAVE       = {slave}")
            log("DEBUG", f"        - ENVIRONMENT = {environment}")

            try:
                queue_item = self._jenkins_server.build_job(
                    self._jenkins_job,
                    {
                        "SLAVE"       : slave,
                        "ENVIRONMENT" : "\n".join([f"{k}=\"{v}\"" for k,v in environment.items()])
                    }
                )
                break

            except Exception as e:
                log("DEBUG", f"Error when triggering Jenkins job: {e}")
                if attempts > 3:
                    log("ERROR", "Desisting after several attempts...")
                    raise e
                else:
                    attempts += 1
                    log("DEBUG", "      - Retrying...")
                    time.sleep(2)

        queue_item = str(queue_item)
        self._triggered_jobs[queue_item] = ["QUEUED", "(queued)", None, "?"]

        return queue_item


    def query(self, execution_id):

        if execution_id not in self._triggered_jobs.keys():
            return "NOT FOUND"

        if self._triggered_jobs[execution_id][0] in ["SUCCESS", "FAILURE", "CANCELED"]:
            return self._triggered_jobs[execution_id][0]

        elif self._triggered_jobs[execution_id][0] == "QUEUED":

            if self._triggered_jobs[execution_id][2] is None:
                # While in the queue, the job never received an execution number. We need to keep
                # querying the queue API.
                #
                try:
                    response = self._jenkins_server.get_queue_item(int(execution_id))
                    self._triggered_jobs[execution_id][2] = response["executable"]["number"]
                except Exception:
                    return "QUEUED"
            else:
                # We are still in the queue despite having received an execution number in the past.
                # This can only mean that we are in the "secondary queue" (one that Jenkins uses
                # in jobs of type "Pipeline" where the agent is dynamically decided inside the
                # Jenkinsfile groovy script).
                # We don't need to do anything special here. The code below will take care of this
                # case.
                #
                pass

        # If we reach this point, it means the job is already running...

        real_execution_id = self._triggered_jobs[execution_id][2]

        attempts = 0
        while True:
            try:
                build_info_response = \
                        self._jenkins_server.get_build_info(self._jenkins_job, real_execution_id)
                break

            except Exception as e:
                log("DEBUG", f"Error when retrieving Jenkins job details: {e}")
                if attempts > 3:
                    log("ERROR", "Desisting after several attempts...")
                    return "NOT FOUND"
                else:
                    attempts += 1
                    time.sleep(2)

        # ...or maybe not! As explained before, for jobs of type "Pipeline" with dynamic agent
        # assignment, there is a "secondary queue": the job appears as running (ie. it has a real
        # execution id) but it is actually waiting for *a new element* (with a different queue ID!)
        # to be removed from the queue before resuming its work.
        #
        # The only way to deal with this case that I could find is to do this:
        #
        # 1. If the job has been running for just a few seconds, consider it "QUEUED" (this is to
        #    avoid a race condition where the job is already running but the "secondary queue" entry
        #    has not yet been created) and try again later.
        #
        # 2. If the job has been running for more time then:
        #    - The first time we get to this point query all queued items with an ID higher than the
        #      original queue ID and check whether they reference our "already running" job. If one
        #      is found, save it (this is the "secondary queue" entry).
        #    - All other times query the queue API for the saved element until it dissappears.
        #
        current_execution_time = \
                int(time.time()) - (build_info_response["timestamp"]//1000 + self._clock_offset)

        if current_execution_time < 30:
            return "QUEUED"

        elif self._triggered_jobs[execution_id][3] == "?":
            # This is the first time a job with an execution ID reaches this far.
            # We need to check for a "secondary queue" entry, in case this is a job of type
            # "Pipeline" with dynamic agent assignment.
            #
            response = self._jenkins_server.get_queue_info()

            for element in response:
                if int(element["id"]) > int(real_execution_id):
                    response = self._jenkins_server.get_queue_item(int(element["id"]), depth=2)

                    if response["task"]["url"].endswith(
                                   f"{self._jenkins_job}/{real_execution_id}/"):

                        # "Secondary queue" entry found. Save it to query for it from now on
                        #
                        self._triggered_jobs[execution_id][3] = element["id"]
                        return "QUEUED"

            # The job was never added to the "secondary queue"
            #
            self._triggered_jobs[execution_id][3] = None

        elif self._triggered_jobs[execution_id][3] is not None:
            # The job is waiting on the "secondary queue". Query the queue API.
            #
            response = self._jenkins_server.get_queue_info()

            if self._triggered_jobs[execution_id][3] in [x["id"] for x in response]:
                return "QUEUED"
            else:
                # The job is no longer in the "secondary" queue.
                #
                self._triggered_jobs[execution_id][3] = None

        # Finally, if we reach this point we can be 100% sure we are no longer in any queue!

        if self._triggered_jobs[execution_id][1] == "(queued)":
            self._triggered_jobs[execution_id][1] = build_info_response["url"]

        if "result" in build_info_response:

            if build_info_response["inProgress"]:
                self._triggered_jobs[execution_id][0] = "RUNNING"

            elif build_info_response["result"] == "SUCCESS": 
                self._triggered_jobs[execution_id][0] = "SUCCESS"

            elif build_info_response["result"] == "FAILURE": 
                self._triggered_jobs[execution_id][0] = "FAILURE"

            elif build_info_response["result"] == "ABORTED":
                self._triggered_jobs[execution_id][0] = "CANCELED"

            elif build_info_response["result"] is None:
                self._triggered_jobs[execution_id][0] = "RUNNING"

            return self._triggered_jobs[execution_id][0]

        return "NOT FOUND"


    def stop(self, execution_id):
        log("DEBUG", f"          - Stopping Jenkins@{self._jenkins_job} build #{execution_id}")

        if execution_id not in self._triggered_jobs.keys():
            log("DEBUG",  "            - build not found")
            return

        if self._triggered_jobs[execution_id][0] == "CANCELED":
            log("DEBUG",  "            - build was already canceled")
            return

        if self._triggered_jobs[execution_id][0] == "QUEUED":
            log("DEBUG",  "            - build is still queued")
            # Job still in queue. Query queue

            for i in range(2):
                #
                # We try to stop the job twice due to Jenkins race conditions (?) where sometimes a
                # job is no longer in a queue but Jenkins still reports that is the case.

                queue_id = None  # ID to cancel job from queue
                other_id = None  # ID to cancel job from any other place

                try:
                    response = self._jenkins_server.get_queue_item(int(execution_id))
                    other_id = response["executable"]["number"]  # Job no longer in queue.
                                                                 # Update it's ID
                    log("DEBUG", f"            - build was actually running. Its real execution id is {other_id}")
                except Exception:
                    queue_id = execution_id                      # Job is still in queue.

                if queue_id:
                    try:
                        self._jenkins_server.cancel_queue(queue_id)
                    except Exception as e:
                        if i == 0:
                            log("ERROR", f"{queue_id} : {e}")
                            return
                else:
                    try:
                        self._jenkins_server.stop_build(self._jenkins_job, other_id)
                    except Exception as e:
                        if i == 0:
                            log("ERROR", f"{self._jenkins_job}/{other_id} : {e}")
                            return

                time.sleep(1)

        else: # the job was already running
            log("DEBUG", f"            - build is currently running with a real execution id of {self._triggered_jobs[execution_id][2]}")

            try:
                self._jenkins_server.stop_build(self._jenkins_job,
                                                self._triggered_jobs[execution_id][2])
            except Exception as e:
                log("ERROR", f"{self._jenkins_job}/{self._triggered_jobs[execution_id][2]} : {e}")
                return

        log("DEBUG",  "            - build successfully canceled")

        self._triggered_jobs[execution_id][0] = "CANCELED"  # We don't remove it from the table,
                                                            # instead we set the entry to "CANCELED"
                                                            # so that query() can figure out this
                                                            # process was canceled

    def exe_uri(self, execution_id):
        """
        Return a link to the Jenkins page associated to the job execution.

        In that link the user can check STDOUT, artifacts, status, etc...
        """
        if execution_id == "<None>":
            return "(did not start)"

        return self._triggered_jobs[execution_id][1]
