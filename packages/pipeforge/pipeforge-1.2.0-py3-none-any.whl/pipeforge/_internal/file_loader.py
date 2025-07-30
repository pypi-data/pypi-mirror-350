# vim: colorcolumn=101 textwidth=100

import os
import re
import json
import copy

import toml  # Not included in python's standard lib (ie. need to be "pip install"ed)

from .utils import log # Local module



####################################################################################################
# Auxiliary functions
####################################################################################################

def _find_line(file_path, regex):
    """
    Find the first line in a file that matches the provided regular expression.

    @param file_path: Path to the file to search
    @param regex    : Regular expression to search for. Note that if "regex" is a list, the function
                      will search for the first line that matches the first regex, then the next
                      line (starting from the just found line) that matches the second regex, and so
                      on. The return value will be the line number where the last regex was found.

    @return: The line number where the first match was found. If no match was found, return -1
    """

    if not isinstance(regex, list):
        regex = [regex]

    with open(file_path) as f:
        n = 0
        for line_number, line in enumerate(f):
            if re.search(regex[n], line):
                if n == len(regex) - 1:
                    return line_number+1
                else:
                    n += 1
        else:
            return -1



####################################################################################################
# API
####################################################################################################

class FileLoader:

    def __init__(self, path_to_file, validation_mode=False):

        self._validation_mode = validation_mode

        extension = os.path.splitext(path_to_file)[1]

        log("DEBUG",  "")
        log("DEBUG", f"Pipeline file read from disk ({path_to_file}):")
        log("DEBUG", open(path_to_file).readlines())

        if extension == ".json":
            self._pipeline_data = json.load(open(path_to_file))

        elif extension == ".toml":
            self._pipeline_data = toml.load(path_to_file)

        else:
            # Try to figure out whether this is json or toml
            try:
                self._pipeline_data = json.load(open(path_to_file))
            except Exception as e1:
                try:
                    self._pipeline_data = toml.load(path_to_file)
                except Exception as e2:
                    log("ERROR", "")
                    log("ERROR", f"The provided file ({path_to_file}) does not seem to contain valid JSON nor TOML data!")
                    log("ERROR", "")
                    log("ERROR", f"json loader: {e1}")
                    log("ERROR", "")
                    log("ERROR", f"toml loader: {e2}")
                    log("ERROR", "")
                    raise ValueError("Invalid file format")

        log("DEBUG", "")
        log("DEBUG", "Pipeline data once parsed into memory structures:")
        log("DEBUG", self._pipeline_data)

        self._file = path_to_file

        if validation_mode:
            self._file_str = ""
        else:
            self._file_str = f" ({self._file})"

        self._expand_syntactic_sugar() # This will also fill "self._dependencies"
        self._validate()


    def _calculate_dependencies(self, pipeline_name):

        for p in self._pipeline_data["pipelines"]:
            if p["name"] == pipeline_name:
                pipeline = p
                break
        else:
            log("ERROR", "")
            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, re.escape(pipeline_name))})")
            log("ERROR", f"Pipeline {pipeline_name} does not exist!")
            log("ERROR", "")
            raise ValueError("Malformed pipeline definition file")

        job_pointers      = {}  # Direct access to each job object by name
        job_dependencies  = {}  # List of other jobs a particular job depends on

        for job in pipeline["jobs"]:
            if job["name"] in job_pointers.keys():
                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'name.*' + re.escape(job['name'])])}")
                log("ERROR", f"Job <{job['name']}> is defined more than once in pipeline <{pipeline_name}>")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file")

            job_pointers    [job["name"]] = job
            job_dependencies[job["name"]] = []

        for job in pipeline["jobs"]:
            if "input" in job.keys():
                for param, value in job["input"].items():
                    if not isinstance(value, str):
                        continue
                    for ref in re.findall("@{.*?}", value):
                        if "::" in ref[2:-1]:
                            # Reference to a parameter from another job
                            #
                            job_ref, param_ref = ref[2:-1].split("::")

                            if job_ref not in job_pointers.keys():
                                log("ERROR", "")
                                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'input',re.escape(job_ref)])}")
                                log("ERROR", f"Job <{job['name']}> is referencing a non existing job (<{job_ref}>) in its input parameters section")
                                log("ERROR", "")
                                raise ValueError("Malformed pipeline definition file")

                            if "output" not in job_pointers[job_ref] or \
                                param_ref not in job_pointers[job_ref]["output"].keys():

                                log("ERROR", "")
                                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'input',re.escape(job_ref)+'::'+re.escape(param_ref)])}")
                                log("ERROR", f"Job <{job['name']}> is referencing a non existing parameter (<{param_ref}>) from job <{job_ref}>")
                                log("ERROR", "")
                                raise ValueError("Malformed pipeline definition file")
                        else:
                            # Reference to the job itself (this is used to indicate that the current
                            # job must not start until the referenced one has finished)
                            #
                            job_ref = ref[2:-1]

                        if job_ref not in job_pointers.keys():
                            log("ERROR", "")
                            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'input',re.escape(job_ref)])}")
                            log("ERROR", f"Job <{job['name']}> is referencing a non existing job (<{job_ref}>) in its input parameters section")
                            log("ERROR", "")
                            raise ValueError("Malformed pipeline definition file")

                        if job_ref not in job_dependencies[job["name"]]:
                            job_dependencies[job["name"]].append(job_ref)

                            # Check for circular dependency
                            #
                            if job_ref in job_dependencies.keys() and \
                               job["name"] in job_dependencies[job_ref]:
                                log("ERROR", "")
                                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'input',re.escape(job_ref)])}")
                                log("ERROR", f"Job <{job['name']}> depends on job <{job_ref}> which in turn depends on job <{job['name']}> (circular dependency)")
                                log("ERROR", "")
                                raise ValueError("Malformed pipeline definition file")


        return job_dependencies


    def _expand_syntactic_sugar(self):

        # If there is no "pipelines" entry, create one with name = "main" and add all jobs to it
        #
        if "pipelines" not in self._pipeline_data:
            if "jobs" not in self._pipeline_data:
                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str}")
                log("ERROR",  "No jobs defined")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file")

            self._pipeline_data["pipelines"] = [{
                                                 "name" : "main",
                                                 "jobs" : copy.deepcopy(self._pipeline_data["jobs"])
                                               }]
            del self._pipeline_data["jobs"]


        # Make sure all pipelines have a name and a jobs list
        #
        for pipeline in self._pipeline_data["pipelines"]:
            if "name" not in pipeline or "jobs" not in pipeline:
                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str}")
                log("ERROR",  "All pipelines must have a name and a list of jobs")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file ")

            if type(pipeline["jobs"]) is not list:
                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(pipeline['name']),'jobs'])}")
                log("ERROR",  "The jobs entry of a pipeline must be a list")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file")


        # Replace "${PIPEFORGE__...}" references with values extracted from the environment
        #
        if self._validation_mode:
            # In validation mode we don't care about environment variables. No need to process them.
            #
            pass

        else:
            try:
                if "meta" in self._pipeline_data:
                    raw_meta = json.dumps(self._pipeline_data["meta"])
                    
                    for ref in re.findall(r"\${PIPEFORGE__.*?}", raw_meta):
                        resolved_ref = os.getenv(ref[2:-1])

                        if not resolved_ref:
                            log("ERROR", "")
                            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['meta',re.escape(ref)])}")
                            log("ERROR", f"'meta' section is referencing a non existing pipeline manager variable (<{ref}>)")
                            log("ERROR", "")
                            raise ValueError("Malformed pipeline definition file")

                        raw_meta = raw_meta.replace(ref, os.getenv(ref[2:-1]))

                    self._pipeline_data["meta"] = json.loads(raw_meta)
            except Exception:
                # We don't really care about the "meta" section
                pass

            for pipeline in self._pipeline_data["pipelines"]:
                for job in pipeline["jobs"]:
                    if "input" in job.keys():
                        for param, value in job["input"].items():
                            for ref in re.findall(r"\${PIPEFORGE__.*?}", value):
                                resolved_ref = os.getenv(ref[2:-1])

                                if not resolved_ref:
                                    log("ERROR", "")
                                    log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'input',re.escape(ref)])}")
                                    log("ERROR", f"Job <{job['name']}> is referencing a non existing pipeline manager variable (<{ref}>) in its input parameters section")
                                    log("ERROR", "")
                                    raise ValueError("Malformed pipeline definition file")

                                job["input"][param] = job["input"][param].replace(ref, resolved_ref)

            log("DEBUG", "")
            log("DEBUG", "Pipeline data after \"PIPEFORGE__...\" environment variables substitution:")
            log("DEBUG", self._pipeline_data)


        # Inject global parameters into each of the jobs
        #
        def _add_not_already_present_dictionary_entries(source, target):
            #
            # Insert (key,values) from dictionary "source" into dictionary "target", but only those
            # which do not already exist in target.
            #
            # Some of the keys of "source" can contain nested dictionaried (of arbitrary depth). In
            # these cases, if the key already exists in "target", this function will "descend" into
            # the new dictionaries and start the process all over.

            for param, value in source.items():

                if param not in target.keys():
                    target[param] = copy.deepcopy(value)
                    continue

                if isinstance(value, str) and isinstance(target[param], str):
                    # Don't update an already existing value
                    continue

                if isinstance(value, dict) and isinstance(target[param], dict):
                    _add_not_already_present_dictionary_entries(value, target[param])
                    continue

                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str}")
                log("ERROR", f"Incompatible types when applying global substitution on parameter {param}:")
                log("ERROR", f"{type(value)} != {type(target[param])}")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file")

        if "global" in self._pipeline_data:
            for pipeline in self._pipeline_data["pipelines"]:
                for job in pipeline["jobs"]:
                    _add_not_already_present_dictionary_entries(self._pipeline_data["global"], job)

            del self._pipeline_data["global"]

        log("DEBUG", "")
        log("DEBUG", "Pipeline data after globals injection:")
        log("DEBUG", self._pipeline_data)


        # Process the "run_always" "fake" parameter
        #
        if "config" in self._pipeline_data and "run_always" in self._pipeline_data["config"]:

            jobs_always = re.findall("@{.*?}", self._pipeline_data["config"]["run_always"])
            jobs_always = [x[2:-1] for x in jobs_always]

            for pipeline in self._pipeline_data["pipelines"]:
                if set([x["name"] for x in pipeline["jobs"]]) & set(jobs_always):
                    # There is at least one job that must always run thus:
                    #
                    #   1. Change the "on_failure" property of all jobs in this pipeline to
                    #      "continue"
                    #
                    #   2. Change the "on_input_err" property of all jobs in this pipeline:
                    #      ...to "skip" for jobs not in the jobs_always list
                    #      ...to "run"  for jobs not in     jobs_always list

                    for job in pipeline["jobs"]:
                        job["on_failure"]   = "continue"
                        job["on_input_err"] = "skip"

                        if job["name"] in jobs_always:
                            job["on_input_err"] = "run"

            log("DEBUG", "")
            log("DEBUG", "Pipeline data after 'run_always' expansion:")
            log("DEBUG", self._pipeline_data)


        # Resolve dependencies
        #
        self._dependencies = {}
        for pipeline in self._pipeline_data["pipelines"]:
            self._dependencies[pipeline["name"]] = self._calculate_dependencies(pipeline["name"])


        # Create new pipelines for "retrigger without" on_failure conditions.
        #
        auto_pipeline = ["auto_pipeline_", 0]
        for pipeline in self._pipeline_data["pipelines"]:
            for job in pipeline["jobs"]:
                if "on_failure" not in job.keys():
                    log("ERROR", "")
                    log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name'])])}")
                    log("ERROR", f"Job <{job['name']}> does not have an <on_failure> property")
                    log("ERROR", "")
                    raise ValueError("Malformed pipeline definition file")

                if job["on_failure"].startswith("retrigger without"):

                    # Create new pipeline for when this job fails

                    auto_pipeline = [auto_pipeline[0], auto_pipeline[1] + 1]
                    new_pipeline  = {
                                      "name" : auto_pipeline[0] + str(auto_pipeline[1]),
                                      "jobs" : []
                                    }

                    self._dependencies[new_pipeline["name"]] = self._dependencies[pipeline["name"]]

                    skipped_jobs = re.findall("@{([^}]*)}", job["on_failure"])

                    job["on_failure"] = f"trigger pipeline : {new_pipeline['name']}"

                    # Add to the new pipeline a copy of all the jobs in the current pipeline that do
                    # not appear in the skipped_jobs list:
                    #
                    for job2 in pipeline["jobs"]:
                        if job2["name"] not in skipped_jobs:
                            new_job = copy.deepcopy(job2)

                            # If one of the jobs to add depends on a skipped_job, replace the input
                            # parameter value for a reference to the status of the jobs the
                            # skipped_job depends on.
                            #
                            if "input" in new_job.keys():
                                for input_param, input_value in new_job["input"].items():
                                    for skipped in skipped_jobs:

                                        def scan_dependencies(replacement, deps):
                                            for dep in deps:
                                                if dep not in skipped:
                                                    replacement.append("@{" + dep + "}")
                                                else:
                                                    scan_dependencies(
                                                          replacement,
                                                          self._dependencies[pipeline["name"]][dep])

                                        replacement = []
                                        scan_dependencies(
                                                      replacement,
                                                      self._dependencies[pipeline["name"]][skipped])

                                        for x in re.findall(
                                                     "(@{"+re.escape(skipped)+" *(::)*[^}]*})",
                                                     input_value):

                                            input_value = input_value.replace(
                                                              x[0],
                                                              "!!" + "+".join(replacement) + "!!")

                                    new_job["input"][input_param] = input_value

                            new_pipeline["jobs"].append(new_job)

                    self._pipeline_data["pipelines"].append(new_pipeline)

        log("DEBUG", "")
        log("DEBUG", "Pipeline data after implicit pipelines creation:")
        log("DEBUG", self._pipeline_data)


        # Resolve dependencies of newly created pipelines
        #
        for i in range(auto_pipeline[1]):
            new_pipeline_name = auto_pipeline[0] + str(i+1)
            self._dependencies[new_pipeline_name] = self._calculate_dependencies(new_pipeline_name)


    def _validate(self):

        # Make sure there is a pipeline called "main"
        #
        if "pipelines" not in self._pipeline_data or \
           "main"      not in [pipeline["name"] for pipeline in self._pipeline_data["pipelines"]]:
            log("ERROR", "")
            log("ERROR", f"Malformed pipeline definition file{self._file_str}")
            log("ERROR",  "Could not find a pipeline with name = 'main'")
            log("ERROR", "")
            raise ValueError("Malformed pipeline definition file")


        # Make sure the name of pipelines is unique
        #
        all_pipeline_names = [pipeline["name"] for pipeline in self._pipeline_data["pipelines"]]
        if len(all_pipeline_names) != len(set(all_pipeline_names)):
            repeated = list(set([x for x in all_pipeline_names if all_pipeline_names.count(x) > 1]))[0]
            log("ERROR", "")
            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(repeated),'name.*' + re.escape(repeated)])}")
            log("ERROR",  "Pipeline names must be unique")
            log("ERROR", "")
            raise ValueError("Malformed pipeline definition file")


        # Make sure the name of jobs is unique within a pipeline
        #
        for pipeline in self._pipeline_data["pipelines"]:
            all_pipeline_jobs_names = [job["name"] for job in pipeline["jobs"]]
            if len(all_pipeline_jobs_names) != len(set(all_pipeline_jobs_names)):
                repeated = list(set([x for x in all_pipeline_jobs_names if all_pipeline_jobs_names.count(x) > 1]))[0]
                log("ERROR", "")
                log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(pipeline['name']),'name.*' + re.escape(repeated),'name.*' + re.escape(repeated)])}")
                log("ERROR", f"Job names within pipeline <{pipeline['name']}> must be unique")
                log("ERROR", "")
                raise ValueError("Malformed pipeline definition file")


        # Make sure jobs only include mandatory fields and that their value is a string.
        #
        for pipeline in self._pipeline_data["pipelines"]:
            for job in pipeline["jobs"]:
                for field in job.keys():
                    if field in ["input", "output"]:
                        pass
                    elif field in ["name", "script", "runner", "detached", "timeout", "retries", "on_failure", "on_input_err"]:
                        if not isinstance(job[field],str):
                            log("ERROR", "")
                            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),re.escape(field)])}")
                            log("ERROR", f"Job <{job['name']}> is not defining field <{field}> as a string")
                            log("ERROR", "")
                            raise ValueError("Malformed pipeline definition file")
                    else:
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),re.escape(field)])}")
                        log("ERROR", f"Job <{job['name']}> is defining an invalid field: <{field}>")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")


        # Make sure all input and output job parameters (if present) are strings.
        # Make sure all output job parameters (if present) are set to "?"
        #
        for pipeline in self._pipeline_data["pipelines"]:
            for job in pipeline["jobs"]:
                if "input" in job.keys():
                    for param, value in job["input"].items():
                        if not isinstance(value, str):
                            log("ERROR", "")
                            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),re.escape(param)])}")
                            log("ERROR", f"Job <{job['name']}> is providing a non-string value to input parameter <{param}>")
                            log("ERROR", "")
                            raise ValueError("Malformed pipeline definition file")
                if "output" in job.keys():
                    for param, value in job["output"].items():
                        if not isinstance(value, str) or value != "?":
                            log("ERROR", "")
                            log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),re.escape(param)])}")
                            log("ERROR", f"Job <{job['name']}> output parameter <{param}> must be set to special string \"?\" (question mark). This is true for all output parameters.")
                            log("ERROR", "")
                            raise ValueError("Malformed pipeline definition file")


        # Make sure all output job parameters (if present) are being used as input parameters
        # somewhere. This is not an error, just a warning.
        #
        for pipeline in self._pipeline_data["pipelines"]:
            for job in pipeline["jobs"]:
                if "output" in job.keys():
                    for param, value in job["output"].items():
                        if not any([f"@{{{job['name']}::{param}}}" in y for x in pipeline["jobs"] for y in x["input"].values()]):

                            if self._validation_mode:
                                loglevel = "NORMAL"
                            else:
                                loglevel = "DEBUG"

                            log(loglevel,  "WARNING:")
                            log(loglevel, f"WARNING: Possibly malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),re.escape(param)])}")
                            log(loglevel, f"WARNING: Job <{job['name']}> output parameter <{param}> is not being used as input parameter in any other job")
                            log(loglevel,  "WARNING:")

                else:
                    # Check for direct references to the job status.
                    #
                    if not any([f"@{{{job['name']}}}" in y for x in pipeline["jobs"] for y in x["input"].values()]):

                        if self._validation_mode:
                            loglevel = "NORMAL"
                        else:
                            loglevel = "DEBUG"

                        log(loglevel,  "WARNING:")
                        log(loglevel, f"WARNING: Possibly malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name'])])}")
                        log(loglevel, f"WARNING: Job <{job['name']}> is not being used as input for any other job")
                        log(loglevel,  "WARNING:")


        # Make sure that "detached" is either "true" or "false".
        # In the former case, make sure "timeout", "retries" and "on_failure" are all set to special
        # string "N/A".
        # In the latter case, make sure one of the other valid values are being used.
        #
        for pipeline in self._pipeline_data["pipelines"]:
            for job in pipeline["jobs"]:

                if job["detached"] == "true":
                    if job["timeout"] != "N/A" or job["retries"] != "N/A" or job["on_failure"] != "N/A":
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'detached'])}")
                        log("ERROR", f"Job <{job['name']}> has property <detached> set to \"true\". When this happens, properties <timeout>, <retries> and <on_failure> *must* be set to special string \"N/A\".")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")

                elif job["detached"] == "false":

                    # Check <timeout> property
                    #
                    error = False

                    if not error:
                        try:
                            number, word = job["timeout"].split()
                        except Exception:
                            error = True

                    if not error:
                        try:
                            _ = int(number)
                        except Exception:
                            error = True

                    if not error:
                        if word not in ["hour", "hours", "minute", "minutes", "second", "seconds"]:
                            error = True

                    if error:
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'timeout'])}")
                        log("ERROR", f"Job <{job['name']}> property <timeout> value is not valid ({job['timeout']}). It must be a number followed by either \"second\", \"seconds\", \"minute\", \"minutes\", \"hour\" or \"hours\" (examples: \"5 minutes\", \"1 hour\", ...)")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")

                    # Check <retries> property
                    #
                    try:
                        _ = int(job["retries"])
                    except Exception:
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'retries'])}")
                        log("ERROR", f"Job <{job['name']}> property <retries> value is not valid ({job['retries']}). It must be a string containing a valid integer number")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")

                    # Check <on_failure> property
                    #
                    if job["on_failure"] in ["stop pipeline", "continue", "restart pipeline"]:
                        pass
                    elif job["on_failure"].startswith("restart from") and \
                         job["on_failure"].split(":")[1].strip() in [x["name"] for x in
                                                                     self.pipeline["jobs"]]:
                        pass
                    elif job["on_failure"].startswith("trigger pipeline") and \
                         job["on_failure"].split(":")[1].strip() in [x["name"] for x in
                                                                  self._pipeline_data["pipelines"]]:
                        pass
                    elif job["on_failure"].startswith("retrigger without"):
                        pass
                    else:
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'on_failure'])}")
                        log("ERROR", f"Job <{job['name']}> property <on_failure> value is not valid ({job['on_failure']}). It must one of these strings: \"stop pipeline\", \"continue\", \"restart pipeline\", \"restart from : <job name>\", \"trigger pipeline : <pipeline name>\", \"retrigger without : <job_1>, <job_2>, ...\"")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")

                    # Check <on_input_err> property
                    #
                    if job["on_input_err"] in ["run", "fail", "succeed", "skip"]:
                        pass
                    else:
                        log("ERROR", "")
                        log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'on_input_err'])}")
                        log("ERROR", f"Job <{job['name']}> property <on_input_err> value is not valid ({job['on_input_err']}). It must one of these strings: \"run\", \"fail\", \"succeed\", \"skip\"")
                        log("ERROR", "")
                        raise ValueError("Malformed pipeline definition file")

                else:
                    log("ERROR", "")
                    log("ERROR", f"Malformed pipeline definition file{self._file_str} @ line {_find_line(self._file, ['name.*' + re.escape(job['name']),'detached'])}")
                    log("ERROR", f"Job <{job['name']}> must set param <detached> to string \"true\" or \"false\". Other values are not valid.")
                    log("ERROR", "")
                    raise ValueError("Malformed pipeline definition file")


    def get_pipeline(self):
        return self._pipeline_data

    def get_dependencies(self):
        return self._dependencies

