# 1. One line description

A pipeline jobs orchestrator library *and* stand-alone script (which can be used
directly from the command line)


# 2. Information for users


## 2.1. Installation

You don't want to use this repository directly. Instead you should install the
latest released version by running this command:

    $ python -m pip install pipeforge


## 2.2. User guide

Check [this file](pipeforge/__init__.py) for the full guide.

You can also access this same information from python itself:

    import pipeforge
    
    help(pipeforge)


All public classes and functions are fully documented:

    import pipeforge

    help(pipeforge.log_configure)
    help(pipeforge.ScriptManager)
    help(pipeforge.Pipeline)
    
    help(pipeforge.JobParams)


# 3. Information for developers


## 3.1. Development environment

First of all you need a mongoDB server running somewhere. You can deploy one
locally and make it listen on port 27017 by running this command:

    $ podman run -p 27017:27017 docker.io/library/mongo

Leave it running as "pipeforge" needs it in order to work.

Next, make sure you have all python modules listed in "dependencies" section
found inside the pyproject.toml file already installed, if not, use your distro
package manager to install them:

    $ cat pyproject.toml | awk '/dependencies/,/]/' 
    $ pacman -S ...

    NOTE: This (installing dependencies through the global package manager) is
    preferred to creating a virtual environment and using "python -m pip
    install" inside of it because it makes it simpler to run the examples.
    If you insist on using a virtual environment, this is what you need to do:

        $ python -m venv .venv
        $ source .venv/bin/activate
        $ python -m pip install .


Next, update the value of PYTHONPATH to make sure it searches for "pipeforce" in
the current folder (where the source code is) instead of in system paths (in
case you had already "pip install"ed it in the past):

    $ export PYTHONPATH=`pwd`:$PYTHONPATH


You can now run the different demos like this:

    DEMO #1:
    Run (locally) a few python scripts that share inputs and outputs one with
    each other. It takes ~10 seconds to complete.
        
        $ export PIPEFORGERUNNER_HEARTBEAT_SECONDS=1
        $ python pipeforge run mongodb://localhost:27017/pipelines__test pipeforge/examples/hello_world.toml LocalScriptManager

    DEMO #2:
    Simulate running a more complex pipeline with many steps without actually
    executing anything. It takes ~1 minute to complete.

        $ export PIPEFORGE__TARGET_BRANCH=origin/master
        $ export PIPEFORGE__FEATURE_BRANCH=origin/my_new_feature
        $ python pipeforge run mongodb://localhost:27017/pipelines__test pipeforge/examples/merge_pull_request.toml DummyScriptManager


While any of the previous demos is running you can monitor its real-time
execution progress by opening another terminal and running this command:

    $ python pipeforge inspector mongodb://localhost:27017/pipelines__test


## 3.2. Running built-in tests

In addition to running "demo pipelines" (such as those in the
"pipeforge/examples" folder that we used in the previous section) you can also
run a full suite of pre-built test cases:

    $ ./tests/run.py

Note you *must* make sure this command returns "OK" after making any change to
the source code!

If one test fail you can obtain a detailed log of what is going on by re-running
it in isolation like this:

    $ ./tests/run.py --test=A:7  # (or A:4, or B:3, ... depending on the test
                                 # template and number)


## 3.3. Running the code linter

Before merging new changes you *must* also check that the following command
returns an empty list of warnings:

    $ ruff check .

NOTE: You might need to install "ruff" first. If so, use you distro's package
manager.


## 3.4. Distribution


### 3.4.1. As a python package

The source code in this repository is meant to be distributed as a python
package that can be "pip install"ed.

Once you are ready to make a release:

  1. Increase the "version" number in file "pyproject.toml"
  2. Run the next command:

       $ ./release.sh package

  3. Publish the contents of the "dist" folder to a remote package repository
     such as PyPi (see
     [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/))

  4. Tell your users that a new version is available and that they can install
     it by running this command:

       $ python -m pip install pipeforge


### 3.4.2. As a python standalone script

You can also create a "single file" script that can be run directly from the
command line without the need to install it as a package.

In order to do that, run this command:

    $ ./release.sh script

The resulting binary ("pipeforge.pyz") can be copied to a different computer and
run like this:

    $ python pipeforge.pyz --help


### 3.4.3. As a standalone executable

Finally, you can create a single binary which does not even require python to be
installed in the system to work.

    $ ./release.sh exe

The resulting binary ("pipeforge.exe") can be copied to a different computer and
run like this:

    $ ./pipeforge.exe --help

NOTE: This will generate a Linux ELF executable if you run "release.sh exe" from
a Linux system, and a Windows EXE file if you run it from a Windows system.

