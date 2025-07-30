"""
A pipeline jobs orchestrator.



================================================================================
1. OVERVIEW
================================================================================

The purpose of the "pipeforge" module is to be used as part of a continuous
integration / continuous delivery (CI/CD) system in two ways:

    1. As the engine/orchestrator in charge of running each of the "jobs" that
       make up each of the possible "processes" (aka. "pipelines") that can be
       run in the CI/CD.

    2. As a library those "jobs" must use to communicate with the orchestrator.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1.1. "pipeforge" as an orchestrator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say that one of these pipelines is the one triggered when a developer is
ready to merge his changes into the main repository branch. Let's say that this
pipeline is made up of the following jobs:

    1. Statically analyze the source code
    2. Build software package for Windows
    3. Build software package for Linux
    4. Run tests on Windows
    5. Run tests on Linux
    6. Send report email

Some of these jobs can be done in parallel, thus the pipeline looks more like
this:

    Build for Windows    Build for Linux      Statically analyze
        |                     |               the source code
        |                     |                    |
        V                     V                    |
    Test on Windows      Test on Linux             |
        |                     |                    |
        |                     |                    |
        '---------------------+---+----------------'
                                  |
                                  V
                          Send report email

The "pipeforge" package includes an orchestrator that can help you take care of
what to run and when if you define the inputs, outputs and dependencies of the
different jobs using a *.toml file.

    NOTE: A *.toml file can always be converted into a *.json file (and the
    other way around). They are equivalent. The conversion is trivial once you
    understand the syntax. You can also use an online tool to perform it
    (example: https://pseitz.github.io/toml-to-json-online-converter/)

    The only difference is that comments (which start with "#") are allowed in
    *.toml files and not in *.json files. That's why I will be showing examples
    in toml syntax, but be aware that pipeforge accepts both formats.

Following with the example, the *.toml could be something like this:

    [[pipelines]]
    name = "main"

      [[pipelines.jobs]]
      name   = "Statically analyze the source code"
      script = "static_analysis.py"
      ...

        [pipelines.jobs.input]
        developer_branch = "origin/update_dependencies_to_latest_version"

        [pipelines.jobs.output]
        report = "?"


      [[pipelines.jobs]]
      name   = "Build software package for Windows"
      script = "build_windows.py"
      ...

        [pipelines.jobs.input]
        developer_branch = "origin/update_dependencies_to_latest_version"

        [pipelines.jobs.output]
        output_exe = "?"


      [[pipelines.jobs]]
      name   = "Build software package for Linux"
      script = "build_linux.py"
      ...

        [pipelines.jobs.input]
        developer_branch = "origin/update_dependencies_to_latest_version"

        [pipelines.jobs.output]
        output_exe = "?"


      [[pipelines.jobs]]
      name   = "Run tests on Windows"
      script = "test_windows.py"
      ...

        [pipelines.jobs.input]
        package = "@{Build software package for Windows::output_exe}"

        [pipelines.jobs.output]
        report = "?"


      [[pipelines.jobs]]
      name   = "Run tests on Linux"
      script = "test_linux.py"
      ...

        [pipelines.jobs.input]
        package = "@{Build software package for Linux::output_exe}"

        [pipelines.jobs.output]
        report = "?"


      [[pipelines.jobs]]
      name   = "Send report email"
      script = "send_email.py"
      ...

        [pipelines.jobs.input]
        static_analysis_report = "@{Statically analyze the source code::report}"
        windows_test_report    = "@{Run tests on Windows::report}"
        linux_test_report      = "@{Run tests on Linux::report}"


If you save that into a file called "merge_pull_request.toml" you could then use
"pipeforge" to automatically take care of the dependencies, figure out in which
order each job has to be executed (by analyzing which jobs have input parameters
that depend on other jobs output parameters) and then actually execute them:

    import pipeforge

    pipeforge.log_configure(...)

    p = pipeline.Pipeline(..., "merge_pull_request.toml")
    p.run(...)


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1.2. "pipeforge" as a library to access job parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each job is associated to a script (for example, the "Send report email" job
will run the "send_email.py" script). When the orchestrator runs each of these
jobs, it will provide them a "token" that they can use to read the input
parameters (defined in the *.toml file) and write the output parameters (also
defined in the *.toml file) using a different "pipeforge" API:

    import pipeforge

    params = pipeforge.JobParams(token)

    # Read input parameters
    #
    input_params = params.get_input_parameters_and_values()

    # Do whatever the script is meant to do
    #
    do_something(input_params['number_of_fingers'])
    ...

    # Write output parameters
    #
    output_params = {}
    for x in params.get_output_parameters():
        output_params[x] = ...

    params.set_output_parameters_and_values(output_params)

The way this "token" is received depends on the mechanism the orchestrator uses
to run the scripts (more on this later, in the SCRIPT MANAGER section)

In summary: "pipeforge" helps you run scripts whose inputs and outputs form a
network of inter-dependencies if you first declare them as jobs using a special
*.toml file.



================================================================================
2. SUPPORTING DATABASE
================================================================================

The way the pipeline runner (ie. the "orchestrator") communicates with the
script that is run on each job is through an external database.

This is how it works:

    1. When the orchestrator is about to run a new job, it checks the list of
       input parameters declared in the *.toml file.

    2. If any of those parameters contains a reference ("@") to the output of
       a previously executed job, the orchestrator will resolve them.

       Example: "@{Run test on Linux::report"} could be resolved into
                "/mnt/network/reports/test_14452.json"

    3. The orchestrator saves all input parameters _names and values_ of the job
       that is going to be run into an external database.

    4. The orchestrator saves all output parameters _names_ of the job that is
       going to be run into that same external database.

    5. The orchestrator "somehow" runs the script associated to the job, and
       provides it with a "token" that the script can later use to access the
       external database information.

       The way the script is run and the way the "token" is provided to the
       script is up to the user of "pipeforge" by providing a special class that
       inherits from "pipeforge.Script()" (more details on this later, in the
       SCRIPT MANAGER section).

       Some possibilities are:

       - The script is run in the local machine as a background process and the
         "token" is provided as an environment variable.

       - The script is run remotely in a Jenkins instance that we trigger using
         a REST API and the "token" is provided as one of the parameters in this
         REST API call.

       - Etc...

    6. The script uses the provided "token" and the "pipeforge" API (more
       specifically the "JobParams()" class) to read all input parameters'
       values, read the requested list of output parameters and provide a value
       for each of them.

This external database, as of today, must be a MongoDB instance whose URL is
provided when you create the "Pipeline" object:

    import pipeforge

    p = pipeline.Pipeline("mongodb://localhost:27017/pipelines", "merge_pull_request.toml")
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can easily deploy such a MongoDB instance using, for example, docker
(instructions here: https://hub.docker.com/_/mongo)



================================================================================
3. TOML FILE FORMAT
================================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3.1. Format description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *.toml file that defines a flow contains one or more pipelines. Example:

    [[pipelines]]
    name = "main"

    [[pipelines]]
    name = "clean up"

    [[pipelines]]
    name = "recovery"

    ...

"name" is the name of the pipeline and can contain spaces. One of the pipelines
*must* be named "main" (this is the pipeline that will be executed when no
specific pipeline name is given). The others can be called whatever you want.

Each of these pipeline entries must contain one or more job definitions. Each of
them looks like this:

    [[pipelines.jobs]]
    name         = <string>
    script       = <string>
    runner       = <string>
    detached     = <string>
    timeout      = <string>
    retries      = <string>
    on_failure   = <string>
    on_input_err = <string>

      [pipelines.jobs.input]
      ... = <string>
      ... = <string>
      ...

      [pipelines.jobs.ouput]
      ... = "?"
      ... = "?"
      ...

"name" is just the name of the job, as you want it to appear in logs and
reports. It can contain spaces. You should make it descriptive but not very
long. It must be *unique* among all the jobs defined in the same pipeline.

Examples:

    name = "Set globals"
    name = "Take repository snapshot"
    name = "Build FW"
    name = "Static analysis of FW"

"script" is the name that "represents" the script that will run to perform the
expected job at each step. Depending on the "running mode" (more on this later,
in the SCRIPT MANAGER section), this can be the patch to a script in the local
system, the URL of a remote Jenkins REST API endpoint, a key of a dictionary
containing predefined scripts, etc...

Examples:

    script = "/usr/local/bin/build_firmware.py"
    script = "http://my.jenkins.local/jobs/build_firmware/run"
    script = "build fw"

"runner" is a string that tells the orchestrator something about where (or how)
the script should be run. Depending on the "running mode" (more on this later,
in the SCRIPT MANAGER section), this can be a name of a specific remote machine,
a set of "tags" a Jenkins agent must contain, the name of a local container
image, etc...

Examples:

    runner = "<unused>"
    runner = "Linux machine"
    runner = "LINUX+FAST+EUROPE+BIG_RAM"
    runner = "

"detached" can be either "true" or "false". If "false" (which is the usual
case), the job will be part of the pipeline (ie. the job *must* have finished in
order for the pipeline to finish). If "true", once the job is triggered the
orchestrator will forget about it... in particular:

    - A detached job can fail and the orchestrator will ignore it
    - A detached job can still be running when the orchestrator decides to end
    - Other jobs cannot depend on output parameters from a detached job
    - A detached job does not have a "timeout" property
    - A detached job does not have a "retries" property
    - A detached job does not have a "on_failure" property

Examples:

    detached = "true"
    detached = "false"

"timeout" is how much time the job can be running before the orchestrator
decides to kill it (and return an error).

Examples:

    timeout = "20 minutes"
    timeout = "1 hour"
    timeout = "N/A"   <------ mandatory value when detached = "true"

"retries" is the number of times a job should be re-attempted in case it fails.
Ideally we would always want to set it to "0" but there are some times when we
know a particular job is prone fail due to external factors (network issues, low
hard disk space, etc...).

Examples:

    retries = "0"
    retries = "1"
    retries = "9"
    retries = "N/A"   <------ mandatory value when detached = "true"

"on_failure" is a string that indicates what happens after all retries (if any)
have been exhausted and the job is still failing. It can take one of these
values:

    - "continue"

       Keep running the pipeline as if nothing had happened. Note that when this
       happens output parameters might not have been set and later jobs that
       depend on them need to take this possibility into consideration (ie. they
       will receive "?" as the parameter's value, and they need how to handle
       that case)

    - "stop pipeline"

       All pending jobs are canceled and the pipeline is immediately stopped
       returning ERROR

    - "trigger pipeline : <pipeline name>"

       All pending jobs are canceled and pipeline <pipeline name> is triggered
       (note that it can be the same pipeline that was executing).

       <pipeline name> must match the "name" property of one of the pipelines
       defined in the *.toml file.

    - "N/A"

       You *must* use this value when parameter "detached" is set to "true".
       This makes sense as detached jobs are not monitored and we cannot take
       any action once it finishes (failing or not)

Examples:

    on_failure = "continue"
    on_failure = "stop pipeline"
    on_failure = "trigger pipeline : clean up"
    on_failure = "N/A"   <------ mandatory value when detached = "true"

"on_input_err" is a string that indicates what happens when one or more of the
input parameters are set to "?" (this is better explained later on). It can take
one of these values:

    - "run"

      Run the job normally. It will be the job responsibility to figure out what
      to do when reading the input parameter that returns "?" (for example, it
      might decide that the parameter is critical and immediately fail or, in
      the case of not-so-critical parameters, provide an alternative default
      value)

    - "fail"

      Act as if the first instruction of the job was "exit -1" and set the
      status of the job to "FAILURE".
      Note what when this happens output parameters of this job will not be set
      (ie. they will be passed down the pipeline with a value of "?")

    - "succeed"

      Act as if the first instruction of the job was "exit 0" and set the status
      of the job to "SUCCESS".
      Note what when this happens output parameters of this job will not be set
      (ie. they will be passed down the pipeline with a value of "?")

    - "skip"

       Act as if the first instruction of the job was "exit 0" and set the
       status of the job to "SKIPPED".
       Note what when this happens output parameters of this job will not be set
       (ie. they will be passed down the pipeline with a value of "?")

Each job *can* (ie. it's optional) define a set of input parameters. They can be
one of these:

    - A "fixed" string (ex: "developer_branch" from the "Statically analyze the
      source code" job). Some more examples:

          [pipelines.jobs.input]
          name    = "Peter"
          surname = "La Anguila"
          age     = "39"

      NOTE: If the input parameter name contains one or more dots ("."), you
      will need to enclose it in double quotes, like this:

          [pipelines.jobs.input]
          name     = "Peter"
          surname  = "La Anguila"
          "my.age" = "39"

      NOTE: If you decide to use JSON instead of TOML this is not something you
      need to worry about, as in JSON *all* parameter names must be enclosed in
      double quotes anyway.

    - A string that contains one or more references to the output parameters of
      other jobs (ex: "package" from "Run tests in Linux" contains a reference to
      parameter "output_exe" from the "Build software package for Linux" job).
      In this case the orchestrator will first "resolve" all these references so
      that what is saved into the database (for the job to later query) is a
      "fix" string at the end.

      The format of a reference is this one:

          @{<job name>::<output parameter name>}

      Some more examples:

          [pipelines.jobs.input]
          test_machine      = "@{Select machine::selection}"
          binary_to_install = "@{Build binary::package_path}/windows/msword.exe"
          report_receivers  = "@{Build binary::author},@{Static analysis::author}"

      Note that if a job wants to wait for another one to finish but does not
      depend on any specific output parameter from it, you can omit the
      "::<output_param_name>" part from the end. Example:

          [pipelines.jobs.input]
          wait_for_builds    = "@{Build firmware}, @{Build platform}"

      In this case, the value of @{...} will be expanded into the exit status of
      the referenced job, which can be either "SUCCESS" or "FAILURE". This means
      that if you were to read the value of input parameter "wait_for_builds"
      from the previous example (but, why would you want to do that?), you could
      get something like this:

          "SUCCESS, SUCCESS"

In addition to all input parameters explicitly defined in the *.toml file, a job
will always receive a set of "hidden" input parameters that start with "__"
(example: "__pipeline_id", which tells the job the ID of the pipeline that the
job is part of). For more details, check the documentation of
pipeforge._internal.params.JobParams.get_input_parameters_and_values.

Note that the "on_input_err" condition will be triggered when:

    - One or more of the input parameters are set to exactly "?"

    - One or more of the input parameters are referencing one or more output
      parameters from other jobs and one of the resolved values is "?", even if
      that resolved value is just a piece of the full input string. In other
      words, if an input parameter is defined like this:

          number_of_cows = "Total: @{Cow counter::output}"

      ...then, if "@{Cow counter::output}" turns out to be "?", the
      "on_input_err" condition will be triggered even though the actual input
      parameter is "Total: ?" and not just "?"

    - One or more of the input parameters are referencing another job directly
      (ex: "@{Cow counter}") instead of a job output parameter (ex:
      "@{Cow counter::output}") and that job exit status is different from
      SUCCESS.

Each job *can* (ie. it's optional) define a set of output parameters. They must
always set to "?" in the *.toml file and the associated job must always set it
to some value or else the orchestrator will complain. This is by design: all
output parameters are mandatory.

Examples:

    [pipelines.jobs.output]
    report_path = "?"
    result      = "?"

NOTE: As it was the case with input parameters, if your output parameters
contain one or more dots (".") in their name, you need to enclosure them in
double quotes.

There is also another section in the *.toml file called [config] which is
*optional* and is currently only used to contain the "run_always" parameter
described in the next section.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3.2. Additional considerations: syntactic sugar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "strict" format of the TOML file is what we just described in the previous
section. What comes next is just "syntactic sugar", which means it will get
"expanded" into the "strict" format before pipeforge processes it.

"Syntactic sugar" exists for the user convenience, to make the file less
verbose.

    * Environment variables expansion

      For convenience, before processing the *.toml file, the orchestrator will
      search for all references to variables named ${PIPEFORGE__...} and replace
      them by the value of the equally named environment variable.

      Example:

          [[pipelines.jobs]]
          ...
            [pipelines.job.input]
            development_branch = "${PIPEFORGE__PR_BRANCH_NAME}"

    * Single pipeline file

      If your file is only going to define one pipeline, you don't need to
      create the "pipelines" list of entries: It will be automatically be
      created for you and named "main".

      In other words, a file which contains this...

          [[pipelines]]
          name = "main"

            [[pipelines.jobs]]
            ...
            [[pipelines.jobs]]
            ...
            [[pipelines.jobs]]
            ...
            [[pipelines.jobs]]
            ...

      ...is equivalent to another file that only contains this:

          [[jobs]]
          ...
          [[jobs]]
          ...
          [[jobs]]
          ...
          [[jobs]]
          ...

    * Global parameters

      Each job must always define all the expected parameters ("name", "script",
      "runner", etc...). There are no default values if you forget one!
      Pipeforge will fail if it detects a missing parameter.

      In order to be able to work around this fact, the [global] section was
      introduced. It works like this: whatever you place inside the [global]
      section will be "injected" into each of the [[pipelines.jobs]] on each of
      the [[pipelines]] under the hood.

      For example, instead of writing this...

          [[pipelines]]
          name = "main"


            [[pipelines.jobs]]
            name         = "Compile product A"
            script       = "compile_a.py"
            runner       = "linux"
            detached     = "false"
            timeout      = "1 minutes"
            retries      = "0"
            on_failure   = "stop pipeline"
            on_input_err = "fail"

              [pipelines.jobs.input]
              version = "v1.0"
              flavor  = "debug"

              [pipelines.jobs.output]
              binaries_path = "?"


            [[pipelines.jobs]]
            name         = "Compile product B"
            script       = "compile_b.py"
            runner       = "windows"
            detached     = "false"
            timeout      = "1 minutes"
            retries      = "0"
            on_failure   = "stop pipeline"
            on_input_err = "fail"

              [pipelines.jobs.input]
              version = "v1.0"
              flavor  = "release"

              [pipelines.jobs.output]
              binaries_path      = "?"
              unit_tests_results = "?"

      ...we could write this (which is 100% equivalent and shorter):

          [global]
          runner       = "linux"
          detached     = "false"
          timeout      = "1 minutes"
          retries      = "0"
          on_failure   = "stop pipeline"
          on_input_err = "fail"

            [global.input]
            version = "v1.0"
            flavor  = "debug"

            [global.output]
            binaries_path = "?"


          [[pipelines]]
          name = "main"


            [[pipelines.jobs]]
            name       = "Compile product A"
            script     = "compile_a.py"


            [[pipelines.jobs]]
            name       = "Compile product B"
            script     = "compile_b.py"
            runner     = "windows"

              [pipelines.jobs.input]
              flavor  = "release"

              [pipelines.jobs.output]
              unit_tests_results = "?"

      Notice how the "global" section parameters are only "injected" into a
      given [[pipelines.job]] if it does not already define a value for it (ie.
      whatever we put in [[pipelines.job]] will always have precedence)

    * Implicit pipelines

      If you use special value "retrigger without : ..." in the "on_failure" job
      parameter, this is what will happen:

          1. A new pipeline will automatically be created for you which contains
             the same jobs as the current pipeline *except* for the ones listed
             after the ":" (example: "retrigger without : @{Test 1}, @{Test 2}")

          2. The original job "on_failure" parameter value will be replaced by
             "trigger pipeline : <name_of_the_new_pipeline>"

      In other words, instead of writing this...

          [[pipelines]]
          name = "main"

            [[pipelines.jobs]]
            name       = "Compile"
            script     = "compile.py"
            ...

            [[pipelines.jobs]]
            name       = "Test 1"
            script     = "test_1.py"
            ...

            [[pipelines.jobs]]
            name       = "Test 2"
            script     = "test_2.py"
            ...

            [[pipelines.jobs]]
            name       = "Merge"
            script     = "merge.py"
            on_failure = "trigger pipeline : auto_pipeline_1"
            ...

              [pipelines.jobs.input]
              results_1 = "@{Test 1::results}"
              results_2 = "@{Test 2::results}"


          [[pipelines]]
          name = "auto_pipeline_1"

            [[pipelines.jobs]]
            name       = "Compile"
            script     = "compile.py"
            ...

            [[pipelines.jobs]]
            name       = "Merge"
            script     = "merge.py"
            on_failure = "trigger pipeline : auto_pipeline_1"
            ...

              [pipelines.jobs.input]
              results_1 = "!!@{Compile}!!"
              results_2 = "!!@{Compile}!!"

      ...we could write this (which is 100% equivalent and shorter):

          [[pipelines]]
          name = "main"

            [[pipelines.jobs]]
            name       = "Compile"
            script     = "compile.py"
            ...

            [[pipelines.jobs]]
            name       = "Test 1"
            script     = "test_1.py"
            ...

            [[pipelines.jobs]]
            name       = "Test 2"
            script     = "test_2.py"
            ...

            [[pipelines.jobs]]
            name       = "Merge"
            script     = "merge.py"
            on_failure = "retrigger without : @{Test 1}, @{Test 2}"
            ...

              [pipelines.jobs.input]
              results_1 = "@{Test 1::results}"
              results_2 = "@{Test 2::results}"

      ...or, taking advantage of what was previously explained regarding single
      pipeline files, this (which is even shorter):

          [[jobs]]
          name       = "Compile"
          script     = "compile.py"
          ...

          [[jobs]]
          name       = "Test 1"
          script     = "test_1.py"
          ...

          [[jobs]]
          name       = "Test 2"
          script     = "test_2.py"
          ...

          [[jobs]]
          name       = "Merge"
          script     = "merge.py"
          on_failure = "retrigger without : @{Test 1}, @{Test 2}"
          ...

            [jobs.input]
            results_1 = "@{Test 1::results}"
            results_2 = "@{Test 2::results}"

      Note that when jobs are "removed" this way, dependencies are re-adjusted
      in a way that "makes sense". In the example above, the "Merge" job in the
      new "auto_pipeline_1" pipeline depends on "Compile":

          [[jobs]]
          name       = "Merge"
          script     = "merge.py"
          on_failure = "trigger pipeline : auto_pipeline_1"
          ...

            [jobs.input]
            results_1 = "!!@{Compile}!!"    # <----- HERE!
            results_2 = "!!@{Compile}!!"    # <----- HERE!

      This means they will receive the execution status of "Compile" (which is
      probably useless in this context) but, this way, we make sure "Merge" will
      not be executed until "Compile" has finished (as it was the case in the
      original "main" pipeline). Some extra considerations:

        - The replacement is the status of all dependencies of the job that is
          being removed (concatenated by a "+" sign).
          In the example there was just one dependency ("Compile") but in other
          scenarios you could end up with something like this (dependencies
          status concatenated by "+"):

              results_1 = "!!@{Prepare}+@{Compile}!!"

        - The replaced string will be surrounded by a pair of "!!".
          This is to let you know that whatever value you were expecting here
          has been replaced by the dependencies status implicit pipeline
          mechanism.

    * [meta] section

      You can add a [meta] section at the top of the file and whatever is found
      inside will be ignored.  This can be used to document the pipeline. Why
      not just use comments? For two reasons:

          1. While TOML files accept comments (line that start with a "#"), JSON
             files do not!

          3. Using a dedicated section allows you to have structured data which
             is easier to "extract" by other tools.

      Example:

          [meta]
          author      = "John Cobra"
          version     = "1.7"
          description = "Continuous integration pipeline for making pancakes"

    * Shortcut to always run a given job

      If a parameter called "run_always" is found in the optional [config]
      section, then all job names it contains will "run always". Each job
      reference in this string must be provided using the "@{<job_name>}"
      syntax. Example: if we want to always run jobs "Job M" and "Job S" we
      would use this:

          [config]
          run_always = "@{Job M}, @{Job S}"

      In practice this means that if a pipeline contains at least one job listed
      in "run_always", this is what happens under the hood:

          1. The "on_failure" property of all jobs in that pipeline is changed
             to "continue", overwriting the previous value.

          2. The "on_input_err" property of all jobs in that pipeline (except
             for those in the "run_always" list) is changed to "skip".

          3. The "on_input_err" property of all jobs in that pipeline that are
             listed in the "run_always" list is changed to "run".

      This is better understood with an example. Let's say we have this
      pipeline:

          A ---> B ---.
                      + ---> E
          C ---> D ---.

      ...defined like this:

          [[pipelines.jobs]]
          name         = "A"
          on_failure   = "stop pipeline"
          on_input_err = "fail"
          ...

          [[pipelines.jobs]]
          name         = "B"
          on_failure   = "stop pipeline"
          on_input_err = "fail"
          ...

          [[pipelines.jobs]]
          name         = "C"
          on_failure   = "stop pipeline"
          on_input_err = "fail"
          ...

          [[pipelines.jobs]]
          name         = "D"
          on_failure   = "stop pipeline"
          on_input_err = "fail"
          ...

          [[pipelines.jobs]]
          name         = "E"
          on_failure   = "stop pipeline"
          on_input_err = "fail"
          ...

      ...but we want "E" (which could be, for example, a stats collecting job)
      to always run even if any of the previous jobs fails.

      In order to achieve this we could add this at the top of the file:

          [config]
          run_always = "@{E}"

      ...which effectively "converts" the original pipeline definition file into
      this:

          [[pipelines.jobs]]
          name         = "A"
          on_failure   = "continue"
          on_input_err = "skip"
          ...

          [[pipelines.jobs]]
          name         = "B"
          on_failure   = "continue"
          on_input_err = "skip"
          ...

          [[pipelines.jobs]]
          name         = "C"
          on_failure   = "continue"
          on_input_err = "skip"
          ...

          [[pipelines.jobs]]
          name         = "D"
          on_failure   = "continue"
          on_input_err = "skip"
          ...

          [[pipelines.jobs]]
          name         = "E"
          on_failure   = "continue"
          on_input_err = "run"
          ...

      Notes:

        - When using "run_always" you won't be able to take advantage of
          "on_failure" and "on_input_err", as these properties will be
          overwritten in all pipeline jobs.

        - In particular, all your "on_failure = trigger pipeline : ..." entries
          are automatically discarded.

        - That's why, if you want a finer control over your pipeline, it is
          recommended not to use "run_always" and, instead, individually set the
          "on_failure" and "on_input_err" property of each job manually.



================================================================================
4. SCRIPT MANAGER
================================================================================

Remember how you call the orchestrator:

    import pipeforge

    pipeforge.log_configure(...)

    p = pipeline.Pipeline(..., "merge_pull_request.toml")
    p.run(...)

"run()" takes a parameter called "script_manager", which is what the
orchestrator uses to start, query and stop the script associated to each job.

This "script_manager" object is built like this:

    1. Create a specialized python subclass that inherits from
       "pipeforge.ScriptManager"

    2. Overwrite the class interface functions with your own implementation.
       In short you need to implement three functions:

         - run() to start execution a script
         - query() to return the current execution state
         - stop() to terminate the script execution

      Check "pipeforge.ScriptManager" documentation to see which parameters each
      of them take and what are they supposed to do in more detail.

    3. Create an instance of this new specialized subclass.

    4. Call "pipeline.Pipeline(script_manager=<instance_of_your_specialized_subclass>)

Example:

    class MyScriptManager(pipeforge.ScriptManager):

       def run(...):
          ...
       def query(...):
          ...
       def stop(...):
          ...

    x = MyScriptManager(...)

    p.run(script_manager=x, ...)

In this way, depending on how you want to run your jobs, you can create
specialized subclasses for...

    - Executing scripts on remote Jenkins instance
    - Executing scripts directly in a local or remote computer over SSH
    - Executing scripts inside a docker container
    - Etc...

In short, the responsibilities of each specialized subclass are:

    - Use the "script" and "runner" fields of the job definition to figure out
      how and where to run the script associated to a job.

    - Somehow pass the script being run a "token" which the orchestrator
      provides (this will later be needed by each script to read its input
      parameters and write its output parameters through "pipeforge.JobParams")

    - Be able to return the state of the script at any time ("RUNNING",
      "SUCCESS", etc...)

    - Be able to stop a running script.

Again, you will find more details in the documentation of
"pipeforge.ScriptManager". Just follow what is described there and you will be
ready to go.



================================================================================
5. LOGGING
================================================================================

When importing the "pipeforge" module, by default no log messages will be
printed to stdout. If you want to change that you must use
"pipeforge.log_configure()".

Through this function you can set the verbosity level and even a custom callback
function which will be called every time a new log message is ready so that you
can print it however you want (to stdout, to a file, etc...)



================================================================================
6. STAND-ALONE APPLICATION
================================================================================

The "pipeforge" module can also be used directly as an application, from the
shell, like this:

    $ python -m pipeforge <command> ...

For a list of valid commands and options, run this:

    $ python -m pipeforge --help

Note that, depending on the "pip" version you used when installing pipeforge, it
might be directly available as a script:

    $ pipeforge --help



================================================================================
7. JENKINS INTEGRATION
================================================================================

Jenkins can be used to run "pipeforge" jobs. All you need to do is this:

    1. Deploy a Jenkins instance.

    2. Create a new Jenkins job following the documentation in
       pipeforge._internal.script.JenkinsScriptManager. Let's call it, for
       example, "Job".

    3. In your PC, run this:

         $ export PIPEFORGESCRIPT_JENKINS_ENDPOINT=<Jenkins instance URL>:::<username>:::<password>:::<job_name>
         $ python -m pipeforge run <database_url> <path_to_toml_file> JenkinsScriptManager

       Example:

         $ export PIPEFORGESCRIPT_JENKINS_ENDPOINT='https://jenkins.example.com:::john:::cobra123:::Job'
         $ python -m pipeforge run mongodb://mongodb.example.com:27017/pipelines pull_request.toml JenkinsScriptManager

That's all: you are now running all the steps of your pipeline in remote slaves
managed by Jenkins.

There is one extra thing we can do to further integrate "pipeforge" with
Jenkins, and that is to *also* run the "pipeforge" engine itself in Jenkins
(instead of in your PC). For this follow these instructions:

    1. Create a new Jenkins job in your instance called, "Pipeline" (now you
       have two jobs: one called "Job", to run pipeline jobs/steps and this new
       one called "Pipeline" to run the pipeline engine that schedules jobs)

    2. In the "Configure" tab, select the "This project is parameterized"
       checkbox and add this entry:

       - Type: File Parameter
         Name: pipeline.toml
         Description:
             *.toml file containing the "pipeforge" pileline definition (as
             decribed in [1]) you want to run.  See [2] for examples.

             [1] help(pipeforge.__init__)
             [2] pipeforge/examples

    3. Select the "Execute concurrent builds if necessary" checkbox.

    4. In "Build Steps" add this entry:

       - Type: Execute shell
       - Command:

            export PIPEFORGESCRIPT_JENKINS_ENDPOINT='localhost:::<username>:::<password>:::Job'
            python -m pipeforge run <database_url> pipeline.toml JenkinsScriptManager

         Example:

            export PIPEFORGESCRIPT_JENKINS_ENDPOINT='localhost:::john:::cobra123:::Job'
            python -m pipeforge run mongodb://mongodb.example.com:27017/pipelines pipeline.toml JenkinsScriptManager

That's all!
Now, whenever you want to run a pipeline, simply go to your Jenkins instance and
trigger the "Pipeline" job. It will ask you for a TOML file. Upload it and go!

Note: when you do this (ie. running the "pipeforge" engine as a Jenkins job),
all jobs executed by "pipeforge" will receive an additional environment variable
("JENKINS_PARENT") containing the URL of the Jenkins job running the "pipeforge"
engine. This is for convenience, in case you want to include this link in your
job's output.

Finally, if you want to connect all of this to a source code management (SCM)
system (ie.  GitHub, BitBucket, ...) so that a pipeline is triggered on specific
actions (when a pull request is opened, when the developer presses a button,
etc...) you just need to do this:

    1. Install a hook in your SCM that is triggered on action X.

    2. The hook will forge a TOML file describing what we want to do.
       In this TOML file, input parameters to the first job will probably be
       information regarding the repository, such as the branch name, the target
       branch, etc...

    3. The hook will call our Jenkins REST API to send the TOML file and trigger
       the "Pipeline" job.

    4. (Optionally) One of the latest jobs in the pipeline is responsible for
       posting a message/comment back into the SCM including the pipeline
       result.
"""


# These are the internal symbols exported to users of this module:

# To users that want to run pipelines:
#
from ._internal.utils    import log_configure  # To configure module's logging
from ._internal.script   import ScriptManager  # To customize the script runner
from ._internal.pipeline import Pipeline       # To run pipelines

# To users that want to create scripts that run in a pipeline
#
from ._internal.params   import JobParams      # To access job parameters


