#!/bin/env python
# vim: colorcolumn=101 textwidth=100

import os
import sys
import mongoengine
import curses

try:
    from ._internal import file_loader # Local module
    from ._internal import inspector   # Local module
    from ._internal import pipeline    # Local module
    from ._internal import script      # Local module
    from ._internal import utils       # Local module

except Exception:

    try:
        from _internal import file_loader # Local module
        from _internal import inspector   # Local module
        from _internal import pipeline    # Local module
        from _internal import script      # Local module
        from _internal import utils       # Local module

    except Exception:
        from pipeforge._internal import file_loader # Local module
        from pipeforge._internal import inspector   # Local module
        from pipeforge._internal import pipeline    # Local module
        from pipeforge._internal import script      # Local module
        from pipeforge._internal import utils       # Local module



####################################################################################################
# Auxiliary functions
####################################################################################################

def print_help():
    print("")
    print("Usage:")
    print("")
    print("> Use case #1: Running a pipeline from a *.{json,toml} file")
    print("")
    print(f"    {sys.argv[0]} run <database_url> <path_to_file> [<ScriptManagerClass>]")
    print("")
    print("    ...where:")
    print("")
    print("        * <database_url> is the URL of the supporting database that we will use to save/")
    print("          query pipeline data. Example: mongodb://localhost:27017/pipelines")
    print("")
    print("        * <path_to_file> is a path to a JSON/TOML file defining the jobs that make")
    print("          the pipeline.")
    print("")
    print("        * <ScriptManagerClass> is an optional parameter that specifies which backend")
    print("          to use to run the scripts. If none is specified, 'DummyScriptManager' is used.")
    print("          Other possible values are 'TestScriptManager', 'LocalScriptManager' and")
    print("          'JenkinsScriptManager'. For details about each of them, run this from a python")
    print("          interpreter:")
    print("")
    print("              import pipeforge")
    print("              help(pipeforge._internal.script)")
    print("")
    print("    There are a series of environment variables that affect this mode's behavior:")
    print("")
    print("        * PIPEFORGERUNNER_LOG_LEVEL              : Can be 'NORMAL', 'DEBUG' or 'SHY'")
    print("        * PIPEFORGERUNNER_LOG_TIMESTAMP_DISABLED : Set to disable timestamps in logs")
    print("        * PIPEFORGERUNNER_HEARTBEAT_SECONDS      : Time between each core loop iteration")
    print("")
    print("")
    print("> Use case #2: Print an example of a *.{json,toml} file")
    print("")
    print(f"    {sys.argv[0]} example")
    print("")
    print("")
    print("> Use case #3: Check a *.{json,toml} file (make sure it contains no errors)")
    print("")
    print(f"    {sys.argv[0]} check <path_to_file>")
    print("")
    print("    ...where:")
    print("")
    print("        * <path_to_file> is a path to the JSON/TOML file you want to check.")
    print("")
    print("")
    print("> Use case #4: Interactive tool to inspect all pipelines in a database")
    print("")
    print(f"    {sys.argv[0]} inspector <database_url>")
    print("")
    print("    ...where:")
    print("")
    print("        * <database_url> is the URL of the supporting database that we will use to save/")
    print("          query pipeline data. Example: mongodb://localhost:27017/pipelines")
    print("")
    print("")



####################################################################################################
# main() Execution starts here.
####################################################################################################

if len(sys.argv) == 1 or sys.argv[1] not in ["run", "example", "check", "inspector"]:
    print_help()
    sys.exit(-1)

subcommand = sys.argv[1]


#~ RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if subcommand == "run":

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print_help()
        sys.exit(-1)

    database_url   = sys.argv[2]
    input_file     = sys.argv[3]

    if len(sys.argv) == 5:
        script_manager = eval("script." + sys.argv[4])
    else:
        script_manager = script.DummyScriptManager # default class

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(-1)

    utils.log_configure(
            os.getenv("PIPEFORGERUNNER_LOG_LEVEL", "NORMAL"),
            include_timestamp=("PIPEFORGERUNNER_LOG_TIMESTAMP_DISABLED" not in os.environ))

    p = pipeline.Pipeline(database_url, input_file)

    utils.log("DEBUG", "")
    utils.log("DEBUG+NORMAL", f"Running pipeline with URI = {p.uri} using {script_manager.__name__}")

    execution_results = p.run(
                          script_manager = script_manager(),
                          polling_period = int(os.getenv("PIPEFORGERUNNER_HEARTBEAT_SECONDS", "30")))

    for i, (ret, db_pipeline_id) in enumerate(execution_results):

        print("")
        print("")
        print(f"Pipeline #{i} result = {ret}")
        print(f"(DB,pipeline) ID   = {db_pipeline_id}")
        print("")

        #p.draw_timeline(mode="ascii:150:stdout:auto")
        pipeline.Pipeline(db_pipeline_id).draw_timeline(mode="ascii:150:stdout:auto")

    if ret == "SUCCESS": sys.exit(0)
    else               : sys.exit(-1)


#~ EXAMPLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elif subcommand == "example":
    example = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "examples",
                           "merge_pull_request.toml")

    print(open(example).read())


#~ CHECK ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elif subcommand == "check":

    if len(sys.argv) != 3:
        print_help()
        sys.exit(-1)

    utils.log_configure("NORMAL", include_timestamp=False)

    try:
        file_loader.FileLoader(sys.argv[2], validation_mode=True)
    except Exception:
        print("")
        print("File contains errors")

        #raise(e) # Uncomment this line for debugging purposes
        sys.exit(-1)

    print("")
    print("File is OK")


#~ INSPECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elif subcommand == "inspector":

    if len(sys.argv) != 3:
        print_help()
        sys.exit(-1)

    database_url = sys.argv[2]

    print("")
    print("Connecting to database, please wait...")

    mongoengine.connect(host=database_url)

    try:
        g = inspector.TUI(database_url)
        curses.wrapper(g.loop)

    except Exception as e:
        if str(e) != "Quit":
            raise e

