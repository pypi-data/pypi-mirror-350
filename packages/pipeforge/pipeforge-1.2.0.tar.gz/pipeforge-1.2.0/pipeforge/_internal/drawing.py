# vim: colorcolumn=101 textwidth=100

import datetime

from . import utils  # Local module



####################################################################################################
# Auxiliary functions
####################################################################################################

def _job_fits(job, jobs):
    """
    Given a job definition (with start and stop timestamps) return whether it "fits" in a list of
    jobs without overlapping with any of them.

    @param job: a tuple whose second and third elements contain the start and stop timestamps.

    @param jobs: a list of jobs (each one with the same properties as @ref job)

    @return True if @ref job does not overlap with any of the @ref jobs. False otherwise
    """

    for start, stop in [(x[1], x[3]) for x in jobs]:
        if (job[1]  > start and job[1]  < stop) or \
           (job[3]  > start and job[3]  < stop) or \
           (job[1] <= start and job[3] >= stop):
            return False

    return True


def _print_ascii(stacks, secs_per_unit, scale, output_width=100, unicode_supported=True,
                 stdout="stdout"):
    """
    Print an ASCII timeline containing all provided jobs (contained in a list of @ref stacks)

    @param stacks: list of "stacks" of jobs. Each stack contains non-overlapping (in execution time)
        jobs, meaning they can be printed in the same row.
        Each job on each stack is represented by a list of 6 elements:

          - [0] (string) Job name
          - [1] (int) Start  time (from 0 to 100)
          - [2] (int) Start2 time (from 0 to 100). This is when the job *really* started executing.
                Before that it was waiting in queue.
          - [3] (int) Stop time (from 0 to 100)
          - [4] (string) Job status
          - [5] (string) "True" or "False" depending on whether this is a detached job (ie. one
                which does not require monitoring)

        Example:

            stacks = [
                [["A",  0, 0, 20, "SUCCESS", "False"], ["C", 20, 25, 60, "SUCCESS", "False"], ["D", 90, 90, 100, "SUCCESS", "False"]],
                [["B", 10, 80, 90, "SUCCESS", "False"], ["E", 90, 90, 95, "SUCCESS", "False"]]
            ]

            ...which would generate something like this:

           |---A---|...--C------|         |-D-|
              |..............B....--------|E|

           |----------------------------------> t

    @param secs_per_unit: Number of seconds each of the 100 normalized units represents. If set to
        0, the translation from units to time will not be done and the final representation will
        include normalized units instead.

    @param scale: Can be "minutes" or "hours". In the first case, each timestamp on the horizontal
    axis will be printed in Xm:YYs format (ex: "8m:09s"). In the second case, each timestamp will
    look like Xh:YYm (ex: "2h:39m").
    If can also take the value "auto". In that case the format will be automatically selected for
    you depending on the total time spawn to be printed.

    @param output_width: Number of columns to use to represent the timeline

    @param unicode_supported: Set to True if the output can use unicode characters. Set to False if
        you only want regular ASCII characters (which is less "pretty" but works fine also)

    @param stdout: Where to send the resulting timeline. Can take any of these values:

        - "stdout" : print to stdout
        - "buffer" : print to a buffer and *return* it to the caller of this function
        - "file@/path/to/file.txt" : print to the provided file (warning! contents will be
          overwritten)

    @return a test buffer with the resulting timeline representation if @ref stdout was set to
    "buffer". Return None otherwise.
    """
    #print(stacks) #DEBUG

    output_buffer = []

    tokens       = "ABCDEFGIJKLMNOPQRTUVWabcdefghijklmnopqrstuvw" * 10
    tokens_super = "ᴬᴮꟲᴰᴱꟳᴳᴵᴶᴷᴸᴹᴺᴼᴾꟴᴿᵀᵁⱽᵂᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𐞥ʳˢᵗᵘᵛʷ" * 10
        # Note: there are missing letters because not all of them have a unicode "superscript"
        # version

    if unicode_supported:
        symbols = {
            "SUCCESS"             : [("│","-","│"), ("│","│"), ("╫")],  # │-------│  ├┤  ╫
            "FAILURE"             : [("│","═","│"), ("╞","╡"), ("╬")],  # │═══════│  ╞╡  ╬
            "RUNNING"             : [("│","᠁","᠁"), ("│","᠁"), ("᠁")],  # │᠁᠁᠁᠁᠁᠁᠁᠁  │᠁  ᠁
            "RUNNING:TO_FAILURE"  : [("│","᠁","᠁"), ("│","᠁"), ("᠁")],  # │᠁᠁᠁᠁᠁᠁᠁᠁  │᠁  ᠁  Same as RUNNING
            "RUNNING:TO_SUCCESS"  : [("│","᠁","᠁"), ("│","᠁"), ("᠁")],  # │᠁᠁᠁᠁᠁᠁᠁᠁  │᠁  ᠁  Same as RUNNING
            "RUNNING:TO_SKIPPED"  : [("│","᠁","᠁"), ("│","᠁"), ("᠁")],  # │᠁᠁᠁᠁᠁᠁᠁᠁  │᠁  ᠁  Same as RUNNING
            "CANCELED"            : [("│","᠁","᠁"), ("│","᠁"), ("᠁")],  # │᠁᠁᠁᠁᠁᠁᠁᠁  │᠁  ᠁  Same as RUNNING
            "SKIPPED"             : [("│","≫","|"), ("│","≫"), ("≫")]   # │≫≫≫≫≫≫≫|  |≫  ≫
        }
    else:
        symbols = {
            "SUCCESS"            : [("|","-","|"), ("|","|"), ("H")],  # |-------|  ||  H
            "FAILURE"            : [("|","=","|"), ("X","X"), ("#")],  # |=======|  XX  #
            "RUNNING"            : [("|","~","~"), ("|","~"), ("~")],  # |~~~~~~~~  |~  ~
            "RUNNING:TO_FAILURE" : [("|","~","~"), ("|","~"), ("~")],  # |~~~~~~~~  |~  ~  Same as RUNNING
            "RUNNING:TO_SUCCESS" : [("|","~","~"), ("|","~"), ("~")],  # |~~~~~~~~  |~  ~  Same as RUNNING
            "RUNNING:TO_SKIPPED" : [("|","~","~"), ("|","~"), ("~")],  # |~~~~~~~~  |~  ~  Same as RUNNING
            "CANCELED"           : [("|","~","~"), ("|","~"), ("~")],  # |~~~~~~~~  |~  ~  Same as RUNNING
            "SKIPPED"            : [("|",">","|"), ("|",">"), (">")]   # |>>>>>>>|  |>  >
        }

        tokens_super = tokens

    timeline = [None]*output_width  # store all instants where jobs start and stop

    output_buffer.append("")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Sort from first to last (to have some ordering when assigning legend aliases)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    names_sorted = [(x[0],x[1]) for element in stacks for x in element]
    names_sorted.sort(key = lambda x:x[1])

    legend         = {}
    reverse_legend = {}
    token_index    = 0

    for job_name, _ in names_sorted:
        if job_name in legend.values():
            continue

        if token_index >= len(tokens):
            reverse_legend[job_name] = (".", "˙") 
            continue

        if tokens[token_index] in legend.keys():
            legend[tokens[token_index]].append(job_name)
        else:
            legend[tokens[token_index]] = [job_name]

        reverse_legend[job_name] = (tokens[token_index], tokens_super[token_index])
        token_index += 1

    # If the name of all jobs is just once character, use it instead of a legend.
    #
    if max([len(x) for jobs_names in legend.values() for x in jobs_names]) == 1:
        legend = {}


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print each stack on its own line
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for stack in stacks:

        line     = [" "] *output_width  # main line for each stack
        extra    = [" "] *output_width  # auxiliary per stack line if superscripts are needed

        # We want to use one single line to print all segments, like this:
        #
        #     |---A---|-----C------|         |-D-|
        #
        # ...but this might not always be possible. In particular, where would we print the "token"
        # ("A", "B", ...) when the segment is two short?
        #
        #   - 3 columns segment --> no problem -->  |A|
        #   - 2 columns segment --> ? ------------> ||
        #   - 1 column segment ---> ? ------------> ‖
        #
        # For both the 2 columns and 1 column cases we will add an extra line below with the token
        # character (in superscript form), like this:
        #
        #     ||   ‖
        #     ᴬ    ᴮ
        #
        # Note that this extra line will only be needed if for the current stack there is at least
        # one "very small" segment, otherwise we won't print it.

        for job in stack:
            start    = int(job[1] / 100 * (output_width-1))
            start2   = int(job[2] / 100 * (output_width-1))
            stop     = int(job[3] / 100 * (output_width-1))
            status   = job[4]
            detached = job[5].upper() == "TRUE"

            if status == "QUEUED":
                status = "RUNNING" # QUEUED jobs are like RUNNING jobs in respect to selecting the
                                   # appropiate ascii/unicode symbol to use.

            if legend:
                X       = reverse_legend[job[0]][0]
                X_super = reverse_legend[job[0]][1]
            else:
                X       = job[0]
                X_super = job[0]

            # Depending on the length of the segment and the status of the associated job execution,
            # use a different type of ASCII/unicode representation
            #
            if start == stop:
                # Ultra short segment (1 char wide)
                #
                line[start]     = symbols[status][2][0]
                extra[start]    = X_super
                timeline[start] = job[1]

            elif start == stop-1:
                # Short segment (2 chars wide)
                #
                line[start]     = symbols[status][1][0]
                line[stop]      = symbols[status][1][1]
                extra[start]    = X_super
                timeline[start] = job[1]

            else:
                # Regular segment longer than 2 chars

                line[start] = symbols[status][0][0]
                line[stop]  = symbols[status][0][2]

                if detached:
                    for i in range (start+1, stop, 2):
                        line[i] = symbols[status][0][1]
                else:
                    for i in range (start+1, stop, 1):
                        line[i] = symbols[status][0][1]

                for i in range (start+1, start2, 1):
                    line[i] = "."

                line[start + int((stop-start)/2)] = X

                timeline[start] = job[1]
                timeline[stop]  = job[3]

            token_index += 1


        # Print the ASCII/unicode character to stdout
        #
        output_buffer.append("".join(line))

        if "".join(extra).strip():
            # If there is at least one non empty character in the extra line, print it
            output_buffer.append("".join(extra))


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print the global "t" horizontal axis
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    line  = [" "] * output_width
    extra = []

    if secs_per_unit > 0:
        if scale == "auto":
            if secs_per_unit * 100 < 60*60:  # If the total time spawn is less that 1 hour, use
                scale = "minutes"            # "minutes" precision (ie. print "Xm:Ys")
            else:
                scale = "hours"              # Otherwise, use "hours" precision ("Xh:Ym")

    for i in range(output_width):

        # Select timeline ASCII symbol
        #
        if i == 0:
            line[i] = "|"

        elif i == output_width-1:
            if unicode_supported:
                line[i] = "▶" # unicode. TODO: Search a better fit
            else:
                line[i] = ">"

        elif timeline[i]:
            line[i] = "*"

        else:
            if unicode_supported:
                line[i] = "⎻" # unicode
            else:
                line[i] = "-"

        # Figure out whether we need to print a timestamp or not
        #
        if timeline[i]:
            now = timeline[i]      # Event timestmp
        else:
            continue               # No timestamps needed


        # Print timestamp using auxiliary lines below the horizontal axis
        #
        if secs_per_unit > 0:
            seconds = now * secs_per_unit

            if scale == "minutes":
                minutes = int(seconds//60)
                seconds = seconds%60

                if minutes > 0:
                    timestamp = f"{minutes}m:{round(seconds):02}s"
                else:
                    timestamp = f"{round(seconds)}s"

            elif scale == "hours":
                hours   = int(seconds//(60*60))
                minutes = seconds%(60*60)/60

                if hours > 0:
                    timestamp = f"{hours}h:{round(minutes):02}m"
                else:
                    timestamp = f"{round(minutes)}m"

        else:
            timestamp = str(now)

        if i + len(timestamp) >= output_width:
            i = output_width - len(timestamp)

        for x in extra:
            if x[i-1] == " ":
                x[i:i+len(timestamp)] = list(timestamp)
                break
        else:
            extra.append([" "]*output_width)

            x = extra[-1]
            x[i:i+len(timestamp)] = list(timestamp)

    output_buffer.append("")
    output_buffer.append("".join(line))
    for x in extra:
        output_buffer.append("".join(x))


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print the legend
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    output_buffer.append("")

    if legend:
        output_buffer.append("LEGEND:")
        for k in sorted(legend.keys()):
              output_buffer.append(f"  {k} : {', '.join(legend[k])}")

        output_buffer.append("")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Decide what to return
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if stdout == "stdout":
        for line in output_buffer:
            print(line)

        return None

    elif stdout.startswith("file@"):
        target = stdout[5:]
        open(target, "w").write("\n".join(output_buffer))

        return None

    elif stdout == "buffer":
        return "\n".join(output_buffer)



####################################################################################################
# API
####################################################################################################

def draw_timeline(db_proxy, mode="ascii:150:stdout"):
    """
    Check @ref Pipeline.draw_timeline for details
    """

    pipeline_data = [f"Pipeline {db_proxy.pipeline.id}",
                 db_proxy.pipeline.metadata.start_time,
                 db_proxy.pipeline.metadata.stop_time,
                 db_proxy.pipeline.metadata.current_state]

    jobs_data = []


    # Obtain a topologically sorted list of jobs and their properties
    #
    for job_name in utils.topological_sort(db_proxy.job_dependencies):

        for job_db in db_proxy.jobs:
            if job_db.name == job_name:
                break
        else:
            print("")
            print("ERROR: Corrupted pipeline in the database?")
            print(f"ERROR: Job <{job_name}> is listed in the job dependencies list but does not exist if the pipeline")
            print("")

            return -1

        if len(job_db.metadata.start_times) > 0:
            for i, start in enumerate(job_db.metadata.start_times):

                if len(job_db.metadata.start2_times) > i:
                    start2 = job_db.metadata.start2_times[i]
                else:
                    start2 = None

                if len(job_db.metadata.stop_times) > i:
                    stop   = job_db.metadata.stop_times[i]
                    state  = job_db.metadata.results[i]
                else:
                    stop   = None
                    state  = job_db.metadata.current_state

                jobs_data.append([job_db.name, start, start2, stop, state, job_db.detached])
        else:
            start  = None
            start2 = None
            stop   = None
            state  = job_db.metadata.current_state
            jobs_data.append([job_db.name, start, start2, stop, state])


    # Right now timestamps are absolute, lets normalize them to 100 using the total pipeline
    # duration as reference. In case the pipeline has not finished executing yet, we will use the
    # biggest time (start or stop) registered in any job.
    #
    time_min = pipeline_data[1]

    if pipeline_data[2]:
        time_max = pipeline_data[2]
    else:
        all_times = [x for x in [t for job in jobs_data for t in [job[1], job[2], job[3]]]
                     if x is not None]

        if len(all_times) == 0:
            return

        time_max = max(all_times)

        if pipeline_data[3] == "RUNNING":
            time_max = datetime.datetime.utcnow()

    for job in jobs_data:
        if job[1] is None:
            continue

        job[1] = round((job[1]-time_min)/(time_max-time_min)*100)

        if job[2] is None:
            job[2] = 100 # Queued job. Still waiting.
        else:
            job[2] = round((job[2]-time_min)/(time_max-time_min)*100)

        if job[3] is None:
            job[3] = 100 # Unfinished job. Still running.
        else:
            job[3] = round((job[3]-time_min)/(time_max-time_min)*100)


    # We now have something like this:
    #
    #   jobs_data = [ ["A",  0, 0,  10,   "SUCCESS", "False"],
    #                 ["B",  0, 10, 20,   "SUCCESS", "False"],
    #                 ["C", 11, 13, None, "RUNNING", "False"],
    #                 ...]
    #
    # ...which would result is something like this:
    #
    #    |----A---||..---C-----...          (stack level = 0)
    #    |----B-------------|               (stack level = 1)
    #
    # We will start drawing them from left to right, according to the topological ordering, keeping
    # track of overlaps to decide which "stack level" to use for each job

    stacks = []  # For each stack level, all jobs it contains

    for job in jobs_data:

        if job[1] is None:
            continue # Job has not started

        for stack in stacks:
            if _job_fits(job, stack):
                stack.append(job)
                break
        else:
            # We need a new stack level
            #
            stacks.append([job])


    # For convenience, sort each stack level by start time
    #
    for stack in stacks:
        stack.sort(key = lambda x:x[1])

    # We now have something like this:
    #
    #   stacks = [ [["A", 0, 0, 10,  "SUCCESS", "False"), ("C", 11, 13, None, "RUNNING", "False")], # level 0
    #              [["B", 0, 10, 20, "SUCCESS", "False)]                                            # level 1
    #            ]

    if mode.startswith("ascii"):
        width  = int(mode.split(":")[1])
        stdout = mode.split(":")[2]
        scale  = mode.split(":")[3]

        return _print_ascii(stacks,
                            secs_per_unit=int((time_max-time_min).seconds)/100,
                            scale=scale,
                            output_width=width,
                            unicode_supported=False,
                            stdout=stdout)

    elif mode.startswith("unicode"):
        width = int(mode.split(":")[1])
        stdout = mode.split(":")[2]
        scale  = mode.split(":")[3]

        return _print_ascii(stacks,
                            secs_per_unit=int((time_max-time_min).seconds)/100,
                            scale=scale,
                            output_width=width,
                            unicode_supported=True,
                            stdout=stdout)

