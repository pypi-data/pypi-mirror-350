# vim: colorcolumn=101 textwidth=100

import re
import sys
import signal
import datetime
import threading

from .utils  import log, topological_sort  # Local module



####################################################################################################
# Globals
####################################################################################################

external_interrupt_received = False
sleep_event                 = threading.Event()



####################################################################################################
# Auxiliary functions
####################################################################################################

def _time_now(real_time, cycle):
    """
    Return a datetime.datetime() object representing the time when this function was called.

    @param real_time: if True, this function returns the current UTC time, which is what you want
        99% of the times.
        If False, the returned object represents a fixed date in the past *plus* some minutes (the
        amount specified in @ref cycle). This is useful when running in "simulation" mode, for
        example in unit tests.

    @param cycle: Number of minutes to add to the datetime.datetime() object that is going to be
        returned when @ref real_time is False. This parameter is ignored when @ref real_time is
        True.

    @return a datetime.datetime() object that can represent either the current UTC time or a fixed
        date in the past plus some minutes.

    NOTE: The "fixed time in the past" is not really relevant, as in simulation mode we are only
    interested in time deltas, but if case you are wondering, it's the 1st of July of 1961 at 19:45.
    I will let you try to figure out what happened at that time :)
    """

    if real_time:
        return datetime.datetime.utcnow()
    else:
        return datetime.datetime(1961, 7, 1, 19, 45) + datetime.timedelta(minutes=cycle)


def _timeout_expired(start, stop, timeout):
    """
    Check if the time ellapsed from "start" to "stop" is bigger than "timeout"

    @param start: datetime.datetime() object representing the period start point

    @param stop: datetime.datetime() object representing the period end point

    @param timeout: a string representing an amount of time in "natural language". Examples: "5
        seconds", "2 minutes", etc...

    @return True if the [start,stop] period is bigger than "timeout"
    """

    if timeout == "N/A":
        return False  # Special case

    window_length_in_seconds = (stop-start).days * 24 * 60 * 60 + (stop-start).seconds

    if timeout.split(" ")[1].startswith("second"):
        timeout_in_seconds = int(timeout.split(" ")[0]) * 1

    elif timeout.split(" ")[1].startswith("minute"):
        timeout_in_seconds = int(timeout.split(" ")[0]) * 60

    elif timeout.split(" ")[1].startswith("hour"):
        timeout_in_seconds = int(timeout.split(" ")[0]) * 60 * 60

    if window_length_in_seconds > timeout_in_seconds:
        return True
    else:
        return False


def _external_interrupt_handler(sig, frame):
    global external_interrupt_received
    global sleep_event

    external_interrupt_received = True
    sleep_event.set()



####################################################################################################
# API
####################################################################################################

def run_pipeline(db_proxy, script_manager, heartbeat):
    """
    Run all the jobs that make up a pipeline in order, respecting their dependencies.

    @param db_proxy: object of type "database.DBProxy()" previously initialized to hold references
        to the pipeline we want to run and its associated jobs.

    @param script_manager: object of type "script.ScriptManager()" previously initialized that will
        be used to start, query and stop a job script.

    @param heartbeat: number of seconds between each "poll cycle", where the status of currently
        running jobs is checked to decided whether the pipeline should be terminated and/or new jobs
        triggered.

    @return "SUCCESS" if all jobs (excluding those with the "detached" property set) finished
        executing and reported no error. Otherwise:

          - If no jobs failed, return "CANCELED".

          - Otherwise:

            - If one of the jobs that failed triggered a new pipeline (by using the "on_failure"
              property), return "TRIGGER:<name_of_the_pipeline_to_trigger>" (example:
              "TRIGGER:secondary")

            - Otherwise, return "FAILURE"
    """

    # Install the handler for when the user wants to externally cancel the pipeline execution.
    #
    #   - SIGINT is received when typing Ctrl+C on the terminal pipeforge is running on.
    #   - SIGTERM is not as common, but can be used in some scenarios (for example when pipeforge is
    #     running as a Jenkins job and the user clicks on the "X" button to cancel the job
    #     execution)
    #
    global external_interrupt_received

    signal.signal(signal.SIGINT,  _external_interrupt_handler)
    signal.signal(signal.SIGTERM, _external_interrupt_handler)


    # Print a topological sorting of jobs based on their dependencies (just for fun)
    #
    log("DEBUG", "")
    log("DEBUG", "Topological sorting of jobs that make up the pipeline:")
    for x in topological_sort(db_proxy.job_dependencies):
        log("DEBUG", f"  - {x}")


    # Find out the longest job name (so that later we use this value to generate pretty/aligned) log
    # messages.
    #
    max_job_name_length = max([len(job_db.name) for job_db in db_proxy.jobs]) + 2


    # Convenience variables
    #
    keep_going = True
    cycle      = 0


    # Update/set pipeline start time
    #
    now = _time_now(heartbeat>0, cycle)

    db_proxy.pipeline.metadata.current_state = "RUNNING"
    db_proxy.pipeline.metadata.start_time    = now
    db_proxy.pipeline.save()


    # Start the loop that will eventually execute all jobs in the pipeline
    #
    cycle            = -1
    trigger_pipeline = None

    log("NORMAL",  "")

    while keep_going:

        cycle      += 1
        before      = now
        now         = _time_now(heartbeat>0, cycle)
        normal_logs = 0

        log("DEBUG",  "")
        log("DEBUG",  "")
        log("DEBUG",  "")
        log("DEBUG", f"Polling cycle #{cycle} starts")


        # Update the status of running jobs (in case any of them has finished or timed out)
        #
        log("DEBUG", "")
        log("DEBUG", "  - Checking status of running jobs...")

        for job_db in db_proxy.jobs:

            if job_db.metadata.current_state in ["QUEUED", "RUNNING"] or \
               job_db.metadata.current_state.startswith("RUNNING:"):

                if job_db.metadata.current_state == "RUNNING" and \
                   _timeout_expired(job_db.metadata.start2_times[-1], now, job_db.timeout):
                        script_manager.stop(job_db.metadata.executions_id[-1])
                        new_state = "FAILURE"
                        extra     = " (timeout)"

                elif job_db.metadata.current_state == "RUNNING:TO_FAILURE":
                    new_state = "FAILURE"
                    extra     = ""

                    # Forcefully exhaust all retries
                    job_db.retries = "0"

                elif job_db.metadata.current_state == "RUNNING:TO_SUCCESS":
                    new_state = "SUCCESS"
                    extra     = ""

                elif job_db.metadata.current_state == "RUNNING:TO_SKIPPED":
                    new_state = "SKIPPED"
                    extra     = ""

                else:
                    new_state = script_manager.query(job_db.metadata.executions_id[-1])
                    extra     = ""

                    if new_state == "NOT FOUND":
                        #
                        # This indicates a fatal error. Let's act as if the job was canceled

                        new_state = "CANCELED"
                        extra     = "executor not found!"

                log("DEBUG", f"    - Job {'<'+job_db.name+'>':{max_job_name_length}} : {new_state:8}{extra} {'(detached)' if job_db.detached == 'true' else ''}")

                if job_db.metadata.current_state == new_state:
                    # Job still queued/running
                    continue

                log("NORMAL", f"Job {'<'+job_db.name+'>':{max_job_name_length}} : {job_db.metadata.current_state:8} --> {new_state:8}{extra} {'(detached)' if job_db.detached == 'true' else ''} {script_manager.exe_uri(job_db.metadata.executions_id[-1])}")
                normal_logs += 1

                if job_db.metadata.current_state == "QUEUED" or \
                   job_db.metadata.current_state.startswith("RUNNING:"):

                    job_db.metadata.start2_times.append(before)

                job_db.metadata.current_state      = new_state
                job_db.metadata.executions_uri[-1] = script_manager.exe_uri(job_db.metadata.executions_id[-1])
                job_db.save()

                if new_state == "FAILURE":
                    if job_db.detached == "false":
                        log("DEBUG", f"      - Decrementing number of retries. New value = <{job_db.retries}>")
                        if job_db.on_failure == "continue":
                            log("NORMAL", f"`--> Retries left = {job_db.retries} (that's ok, when this job fails we have been told to ignore it)")
                            normal_logs += 1
                        else:
                            log("NORMAL", f"`--> Retries left = {job_db.retries}")
                            normal_logs += 1
                        job_db.retries = str(int(job_db.retries) - 1)

                    job_db.metadata.stop_times.append(now)
                    job_db.metadata.results.append("FAILURE")

                    job_db.save()

                elif new_state in ["SUCCESS", "SKIPPED"]:
                    job_db.metadata.stop_times.append(now)
                    job_db.metadata.results.append(new_state)

                    job_db.save()

                    if job_db.detached == "false":
                        log("DEBUG", "      - Checking output parameters:")

                        if job_db.output:
                            max_param_out_length = max([len(k) for k in job_db.output.keys()])

                            job_db.reload()

                            for k,v in job_db.output.items():
                                message = f"        - {k:{max_param_out_length}} = {v}"
                                if v == "?":
                                    message += f" => Parameter <{k}> was not set by job <{job_db.name}> script (<{job_db.script}>)"
                                log("DEBUG", message)


        # Check if the whole pipeline needs to be stopped because of a failed job
        #
        log("DEBUG", "")
        log("DEBUG", "  - Checking for pipeline stop/restart conditions...")

        for job_db in db_proxy.jobs:

            if job_db.metadata.current_state == "CANCELED" or external_interrupt_received is True:

                # When a job is canceled, we assume the whole pipeline must be stopped
                # Stop all running (even detached!) jobs
                #
                for job_db2 in db_proxy.jobs:
                    if job_db2.metadata.current_state == "WAITING":

                        log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is WAITING. We are going to change its state to CANCELED.")

                        job_db2.metadata.executions_id.append("<None>")
                        job_db2.metadata.executions_uri.append("<None>")

                        job_db2.metadata.stop_times.append(now)
                        job_db2.metadata.current_state = "CANCELED"
                        job_db2.metadata.results.append("CANCELED")
                        job_db2.save()

                    elif job_db2.metadata.current_state in ["QUEUED", "RUNNING"]:

                        log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is {job_db2.metadata.current_state}. Killing it...")

                        script_manager.stop(job_db2.metadata.executions_id[-1])

                        job_db2.metadata.stop_times.append(now)
                        job_db2.metadata.current_state = "CANCELED"
                        job_db2.metadata.results.append("CANCELED")
                        job_db2.save()

                keep_going = False
                break

            if job_db.metadata.current_state != "FAILURE": continue
            if job_db.detached               == "true"   : continue  # Detached jobs can fail
            if int(job_db.retries)           >= 0        : continue  # No retries left

            log("DEBUG", f"    - Job {'<'+job_db.name+'>':{max_job_name_length}} has exhausted its retries.")

            if job_db.on_failure == "continue":
                log("DEBUG", "      - Its \"on_failure\" property is set to \"continue\". Nothing to do...")
                continue

            if job_db.on_failure == "stop pipeline" or \
               job_db.on_failure.startswith("trigger pipeline"):
                log("DEBUG", f"      - Its \"on_failure\" property is set to \"{job_db.on_failure}\". Let's kill all other RUNNING jobs (excluding 'detached' ones):")
                log("NORMAL", f"Job {'<'+job_db.name+'>'} has exhausted its retries. This is critial. Stop pipeline.")
                normal_logs += 1

                # Stop all running (and not detached) jobs
                #
                for job_db2 in db_proxy.jobs:
                    if job_db2.metadata.current_state == "WAITING":

                        log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is WAITING. We are going to change its state to CANCELED.")

                        job_db2.metadata.executions_id.append("<None>")
                        job_db2.metadata.executions_uri.append("<None>")

                        job_db2.metadata.stop_times.append(now)
                        job_db2.metadata.current_state = "CANCELED"
                        job_db2.metadata.results.append("CANCELED")
                        job_db2.save()

                    elif job_db2.metadata.current_state in ["QUEUED", "RUNNING"]:

                        if job_db2.detached == "true":
                            log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is {job_db2.metadata.current_state} *but* its \"detached\" property is set to \"true\". Do not kill this job.")
                        else:
                            log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is {job_db2.metadata.current_state}. Killing it...")

                            script_manager.stop(job_db2.metadata.executions_id[-1])

                            job_db2.metadata.stop_times.append(now)
                            job_db2.metadata.current_state = "CANCELED"
                            job_db2.metadata.results.append("CANCELED")
                            job_db2.save()


                if job_db.on_failure.startswith("trigger pipeline"):
                    trigger_pipeline = job_db.on_failure.split(":")[1].strip()

                keep_going = False
                break

            elif job_db.on_failure == "restart pipeline":
                log("DEBUG", "      - Its \"on_failure\" property is set to \"restart pipeline\". Let's kill all other RUNNING/QUEUED jobs (including 'detached' ones):")

                # Stop all running jobs, including detached ones!
                #
                for job_db2 in db_proxy.jobs:

                    if job_db2.metadata.current_state == "WAITING":

                        job_db2.metadata.executions_id.append("<None>")
                        job_db2.metadata.executions_uri.append("<None>")
                        job_db2.metadata.stop_times.append(now)

                    elif job_db2.metadata.current_state in ["QUEUED", "RUNNING"]:

                        log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is RUNNING. Killing it...")

                        script_manager.stop(job_db2.metadata.executions_id[-1])
                        job_db2.metadata.stop_times.append(now)

                    job_db2.metadata.current_state = "WAITING" # This will make the whole pipeline
                    job_db2.save()                             # start from the beginning

                    # TODO: Restore original values of DBProxy entries, add new start/stop
                    #       timestamp to the pipeline object

                break

            elif job_db.on_failure.startswith("restart from"):
                log("DEBUG", f"      - Its \"on_failure\" property is set to \"{job_db.on_failure}\". Let's kill all other RUNNING jobs that depend on it (excluding 'detached' ones):")

                # If we get here we want to restart from job X

                # Stop all running jobs "downstream" the provided one, including detached ones!
                #
                start_from_job = job_db.on_failure.split(":")[1].strip()

                def recursive_deps(node):
                    my_deps = []
                    for dep in db_proxy.job_dependencies[node]:
                        my_deps += [dep]
                        my_deps += recursive_deps(dep)
                    return my_deps

                for job_db2 in db_proxy.jobs:
                    # Only change to "WATING" downstream jobs (and the just failed job too)
                    #
                    if job_db2.name == start_from_job or \
                       start_from_job in recursive_deps(job_db2.name):

                        if job_db2.metadata.current_state in ["QUEUED", "RUNNING"]:

                            log("DEBUG", f"        - Job {'<'+job_db2.name+'>':{max_job_name_length}} is RUNNING, not detached and depends (directly or indirectly) on <{start_from_job}>. Killing it...")

                            script_manager.stop(job_db2.metadata.executions_id[-1])

                        job_db2.metadata.current_state = "WAITING"
                        job_db2.save()

                        # TODO: Restore original values of DBProxy entries, add new start/stop
                        #       timestamp to the pipeline object

                break


        if not keep_going:
            continue


        # Check if any of the waiting (or failed) jobs can be started (or restarted)
        #
        log("DEBUG", "")
        log("DEBUG", "  - Checking for new job candidates to be started...")

        for job_db in db_proxy.jobs:

            if job_db.metadata.current_state == "WAITING"        or \
                    (job_db.metadata.current_state == "FAILURE" and \
                     job_db.detached               == "false"   and \
                     int(job_db.retries)           >= 0):

                log("DEBUG", f"    - Job {'<'+job_db.name+'>':{max_job_name_length}} is waiting to be started. Let's check its dependencies:")

                # Check dependencies and run script
                #
                all_deps_ready = True

                for dep in db_proxy.job_dependencies[job_db.name]:

                    status = [x for x in db_proxy.jobs if x.name == dep][0].metadata.current_state

                    log("DEBUG", f"      - Dependency {'<'+dep+'>':{max_job_name_length}} status is {status}.")

                    if status in [ "WAITING", "RUNNING", "QUEUED" ] or \
                       status.startswith("RUNNING:"):

                        all_deps_ready = False

                if all_deps_ready:
                    log("DEBUG", f"      - All dependencies are done! We can start job <{job_db.name}>")
                    log("DEBUG",  "      - ...but first, let's update its input parameters:")

                    # Update input parameters with new values (ie. obtained from previously executed
                    # job output parameters)
                    #
                    max_param_in_length = max([len(k) for k in job_db.input.keys()] or [0])

                    one_question_mark_input = False

                    original_input = {}
                    for input_param, old_value in job_db.input.items():
                        original_input[input_param] = old_value

                    new_input = {}
                    for input_param, old_value in original_input.items():
                        new_value = old_value

                        for ref in re.findall("@{.*?}", old_value):
                            if "::" in ref[2:-1]:
                                job_ref, param_ref = ref[2:-1].split("::")
                            else:
                                job_ref   = ref[2:-1]
                                param_ref = "<implicit_status>"

                            for job_db2 in db_proxy.jobs:
                                if job_db2.name == job_ref:
                                    job_db2.reload()

                                    if param_ref == "<implicit_status>":
                                        # Resolve to the status of the referenced job
                                        #
                                        new_value = new_value.replace(
                                                        ref,
                                                        job_db2.metadata.current_state)

                                        if job_db2.metadata.current_state != "SUCCESS":
                                            # If the job did not succeed, we will behave in the same
                                            # way as if this output parameter was not set, so that
                                            # the "on_input_err" property of the next job kicks in.
                                            one_question_mark_input = True

                                    else:
                                        # Resolve to the referenced output parameter of the
                                        # referenced job
                                        #
                                        new_value = new_value.replace(
                                                        ref,
                                                        job_db2.output[param_ref])

                                        if job_db2.output[param_ref] == "?":
                                            one_question_mark_input = True
                                    break

                        if new_value != old_value:
                            log("DEBUG", f"        > {input_param:{max_param_in_length}} = {old_value} = {new_value}")
                        else:
                            log("DEBUG", f"        > {input_param:{max_param_in_length}} = {old_value}")

                        new_input[input_param] = new_value

                    job_db.update(set__input=new_input)

                    if one_question_mark_input is False or job_db.on_input_err == "run":

                        try:
                            execution_id = script_manager.run(job_db.name,
                                                              job_db.script,
                                                              job_db.runner,
                                                              db_proxy.database_url + \
                                                                  "#" + str(job_db.id))
                        except Exception as e:
                            log("ERROR", "")
                            log("ERROR", f"Error while trying to run script <{job_db.script}> from job <{job_db.name}>.")
                            log("ERROR", f"Exception: {e}")
                            log("ERROR", "")

                            import traceback
                            traceback.print_exc()

                            sys.exit(-1)

                        log("NORMAL", f"Job {'<'+job_db.name+'>':{max_job_name_length}} : {job_db.metadata.current_state:8} --> {'QUEUED':8} {'(detached)' if job_db.detached == 'true' else ''}")
                        normal_logs += 1

                        job_db.metadata.executions_id.append(execution_id)
                        job_db.metadata.executions_uri.append(script_manager.exe_uri(execution_id))
                        job_db.metadata.current_state = "QUEUED"
                        job_db.metadata.start_times.append(_time_now(heartbeat>0, cycle))

                    elif job_db.on_input_err == "fail":
                        job_db.metadata.executions_id.append("<None>")
                        job_db.metadata.executions_uri.append("<None>")
                        job_db.metadata.current_state = "RUNNING:TO_FAILURE"
                        job_db.metadata.start_times.append(_time_now(heartbeat>0, cycle))

                    elif job_db.on_input_err == "succeed":
                        job_db.metadata.executions_id.append("<None>")
                        job_db.metadata.executions_uri.append("<None>")
                        job_db.metadata.current_state = "RUNNING:TO_SUCCESS"
                        job_db.metadata.start_times.append(_time_now(heartbeat>0, cycle))

                    elif job_db.on_input_err == "skip":
                        job_db.metadata.executions_id.append("<None>")
                        job_db.metadata.executions_uri.append("<None>")
                        job_db.metadata.current_state = "RUNNING:TO_SKIPPED"
                        job_db.metadata.start_times.append(_time_now(heartbeat>0, cycle))

                    else:
                        log("ERROR", "")
                        log("ERROR", f"Invalid value for 'on_input_err': {job_db.on_input_err}")
                        log("ERROR", "")

                    job_db.save()

                else:
                    log("DEBUG", "      - At least one dependency from above is not ready. We need to keep waiting.")


        # Check if we are done
        #

        log("DEBUG", "")
        log("DEBUG", "  - Checking if we are done...")

        keep_going           = False
        jobs_running_queued  = []

        for job_db in db_proxy.jobs:

            if job_db.metadata.current_state == "WAITING":
                log("DEBUG", f"    - Job {'<'+job_db.name+'>':{max_job_name_length}} status is {'<'+job_db.metadata.current_state+'>':10} {'(detached)' if job_db.detached == 'true' else ''} ")
            else:
                log("DEBUG", f"    - Job {'<'+job_db.name+'>':{max_job_name_length}} status is {'<'+job_db.metadata.current_state+'>':10} {'(detached)' if job_db.detached == 'true' else ''} {script_manager.exe_uri(job_db.metadata.executions_id[-1])}")

            if job_db.metadata.current_state == "WAITING"           or \
               job_db.metadata.current_state.startswith("RUNNING:") or \
              (job_db.metadata.current_state in ["RUNNING", "QUEUED"] and \
                                                                      job_db.detached == "false"):
                keep_going = True

            if job_db.metadata.current_state.startswith("RUNNING:") or \
              (job_db.metadata.current_state in ["RUNNING", "QUEUED"] and \
                                                                      job_db.detached == "false"):
                  jobs_running_queued.append(job_db.name)

        if not keep_going:
            log("DEBUG", "    - Nothing else remaining! Exiting the polling loop...")

        if normal_logs > 0:
            if len(jobs_running_queued) > 0:
                aux = ', '.join(jobs_running_queued)
                if len(aux) > 80:
                    aux = aux[:77] + "..."
                log("NORMAL", f"{len(jobs_running_queued)} job(s) currently running/queued: {aux}")
                normal_logs += 1


        # Sleep
        #
        if heartbeat > 0:
            sleep_event.wait(heartbeat) # Interruptible sleep
            sleep_event.clear()
            if normal_logs > 0:
                log("NORMAL", "")


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # This is where we exit the while loop.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Update/set pipeline start time
    #
    db_proxy.pipeline.metadata.stop_time = _time_now(heartbeat>0, cycle)
    db_proxy.pipeline.save()


    # Decide what to return
    #
    log("DEBUG", "")
    log("DEBUG", "")
    log("DEBUG+NORMAL", "")
    log("DEBUG+NORMAL", "Polling finished. Checking jobs status...")

    total_failed   = 0
    total_canceled = 0
    total_skipped  = 0

    for job_db in db_proxy.jobs:
        log("DEBUG+NORMAL", f"  - Job {'<'+job_db.name+'>':{max_job_name_length}} : {job_db.metadata.current_state:8} {'(detached)' if job_db.detached == 'true' else ''} {script_manager.exe_uri(job_db.metadata.executions_id[-1])}")

        if job_db.detached == "false":
            if job_db.metadata.current_state == "FAILURE"               : total_failed   += 1
            if job_db.metadata.current_state == "CANCELED"              : total_canceled += 1
            if job_db.metadata.current_state == "CANCELED_WHILE_WAITING": total_canceled += 1
            if job_db.metadata.current_state == "SKIPPED"               : total_skipped  += 1

    log("DEBUG+NORMAL", "")
    log("DEBUG", f"  - total_failed   = {total_failed}")
    log("DEBUG", f"  - total_canceled = {total_canceled}")
    log("DEBUG", f"  - total_skipped  = {total_skipped}")

    return_value = "UNKNOWN"

    if   trigger_pipeline    : return_value = f"TRIGGER:{trigger_pipeline}"
    elif total_failed   > 0  : return_value =  "FAILURE"
    elif total_canceled > 0  : return_value =  "CANCELED"
    else                     : return_value =  "SUCCESS"

    log("DEBUG", "")
    log("DEBUG", f"  - return_value   = {return_value}")

    db_proxy.pipeline.metadata.current_state = return_value
    db_proxy.pipeline.save()

    if trigger_pipeline:
        log("DEBUG+NORMAL", f"Triggering new pipeline: {trigger_pipeline}")

    signal.signal(signal.SIGINT,  signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)

    return return_value

