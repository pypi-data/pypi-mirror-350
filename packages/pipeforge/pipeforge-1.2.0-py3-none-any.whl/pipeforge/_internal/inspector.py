#!/bin/env python
# vim: colorcolumn=101 textwidth=100

import os
import sys
import textwrap
import random

try:
    import curses
    import curses.textpad
except Exception:
    print("")
    print("ERROR: 'curses' package not found")
    print("ERROR: If you are on Windows, try installing it with this command:")
    print("ERROR:")
    print("ERROR:     > python -m pip install -i https://pypi.org/project windows-curses")
    print("ERROR:")
    print("")
    sys.exit(1)


try:
    from .._internal import database  # Local module
    from .._internal import drawing   # Local module
except Exception:
    from _internal import database  # Local module
    from _internal import drawing   # Local module



####################################################################################################
# API
####################################################################################################

class TUI:
    """
    Terminnal user interface for querying the pipelines database
    """

    def __init__(self, database_url):

        self._database_url     = database_url
        self._all_pipelines    = None
        self._current_pipeline = None

        self._refresh_list_of_all_pipelines()

        # Save all non-running pipelines into the cache
        #
        self._cache = {}

        for i, pipeline in enumerate(self._all_pipelines):
            if pipeline.metadata.current_state not in [ "RUNNING", "WAITING" ]:
                self._current_pipeline_index = i
                self._refresh_current_pipeline()

        self._current_pipeline_index = 0
        self._refresh_current_pipeline()

        self._current_job_index = 0
        self._focus             = "pipelines"

        self._help = 0


    def _refresh_list_of_all_pipelines(self):
        # This triggers a DB query
        #
        self._all_pipelines = [
            x for x in
            database.Pipeline.objects().order_by('-metadata__start_time')[0:10]
        ]


    def _refresh_current_pipeline(self):
        # This triggers a DB query if not already in the cache
        #
        if len(self._all_pipelines) == 0:
            return

        pipeline_id = str(self._all_pipelines[self._current_pipeline_index].id)

        if pipeline_id in self._cache:
            self._current_pipeline = self._cache[pipeline_id]
        else:
            self._current_pipeline = database.DBProxy(self._database_url,
                                       str(self._all_pipelines[self._current_pipeline_index].id))

            if self._current_pipeline.pipeline.metadata.current_state not in ["RUNNING", "WAITING"]:
                # This pipeline is not going to change state anymore.
                # We can add it to the cache.
                #
                self._cache[pipeline_id] = self._current_pipeline


    def _draw(self,
              stdscr,
              top_pane_geometry,
              middle_top_pane_geometry,
              middle_bottom_pane_geometry,
              bottom_pane_geometry):

        top           = stdscr.subwin(*top_pane_geometry)
        middle_top    = stdscr.subwin(*middle_top_pane_geometry)
        middle_bottom = stdscr.subwin(*middle_bottom_pane_geometry)
        #raise Exception(f"ERROR: {bottom_pane_geometry}")
        bottom        = stdscr.subwin(*bottom_pane_geometry)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Top pane: pipeline selector
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        top.addstr(0, 0,
            f"{'#':>2}  "
            f"{textwrap.shorten('pipeline id',   width=28, placeholder='...'):28}"
            f"{textwrap.shorten('started',       width=23, placeholder='...'):23}"
            f"{textwrap.shorten('from',          width=25, placeholder='...'):25}"
            f"{textwrap.shorten('current state', width=20, placeholder='...'):20}"
        )
        top.addstr(1, 0, "-"*100)

        if len(self._all_pipelines) == 0:
            # Nothing to draw
            #
            return

        parent_of_currently_selected = \
                self._all_pipelines[self._current_pipeline_index].metadata.parent

        child_of_currently_selected = None
        for i, pipeline in enumerate(self._all_pipelines):
            if pipeline.metadata.parent == self._all_pipelines[self._current_pipeline_index]:
                child_of_currently_selected = pipeline
                break

        for i, pipeline in enumerate(self._all_pipelines):

            id_str = str(pipeline.id)

            if i == self._current_pipeline_index :

                if pipeline.metadata.current_state in [ "RUNNING", "WAITING" ]:
                    pipeline.reload()

                if self._focus == "pipelines":
                    attr = curses.A_REVERSE
                else:
                    attr = curses.A_UNDERLINE
            else:
                attr = 0

            if pipeline.metadata.start_time:
                start_time = pipeline.metadata.start_time.isoformat(' ', 'seconds')
            else:
                start_time = "?"

            if pipeline.metadata.current_state:
                current_state = pipeline.metadata.current_state
            else:
                current_state = "?"

            if pipeline == parent_of_currently_selected:
                indicator = "<-"
            elif pipeline == child_of_currently_selected:
                indicator = "->"
            else:
                indicator = ""

            try:
                top.addstr(i+2, 0,
                    f"{i:>2}  "
                    f"{textwrap.shorten(id_str,                                width=28, placeholder='...'):28}"
                    f"{textwrap.shorten(start_time,                            width=23, placeholder='...'):23}"
                    f"{textwrap.shorten(os.path.basename(pipeline.file_path),  width=25, placeholder='...'):25}"
                    f"{textwrap.shorten(current_state,                         width=20, placeholder='...'):20}{indicator}",
                    attr
                )
            except Exception:
                # TODO: Implement scroll
                pass


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Top pane: keys
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self._help == 1:
            top.addstr( 0, top_pane_geometry[1]-96, r"""          .  .            """)
            top.addstr( 1, top_pane_geometry[1]-96, r"""          |\_|\           """)
            top.addstr( 2, top_pane_geometry[1]-96, r"""          | a_a\          """)
            top.addstr( 3, top_pane_geometry[1]-96, r"""          | | "]          """)
            top.addstr( 4, top_pane_geometry[1]-96, r"""      ____| '-\___        """)
            top.addstr( 5, top_pane_geometry[1]-96, r"""     /.----.___.-'\       """)
            top.addstr( 6, top_pane_geometry[1]-96, r"""    //        _    \      """)
            top.addstr( 7, top_pane_geometry[1]-96, r"""   //   .-. (~v~) /|      """)
            top.addstr( 8, top_pane_geometry[1]-96, r"""  |'|  /\:  .--  / \      """)
            top.addstr( 9, top_pane_geometry[1]-96, r""" // |-/  \_/____/\/~|     """)
            top.addstr(10, top_pane_geometry[1]-96, r"""|/  \ |  []_|_|_] \ |     """)
            top.addstr(11, top_pane_geometry[1]-96, r"""| \  | \ |___   _\ ]_}    """)
        elif self._help == 2:
            top.addstr( 0, top_pane_geometry[1]-96, r"""         .=.,             """)
            top.addstr( 1, top_pane_geometry[1]-96, r"""        ;c =\             """)
            top.addstr( 2, top_pane_geometry[1]-96, r"""      __|  _/             """)
            top.addstr( 3, top_pane_geometry[1]-96, r"""    .'-'-._/-'-._         """)
            top.addstr( 4, top_pane_geometry[1]-96, r"""   /..   ____    \        """)
            top.addstr( 5, top_pane_geometry[1]-96, r"""  /' _  [<_->] )  \       """)
            top.addstr( 6, top_pane_geometry[1]-96, r""" (  / \--\_>/-/'._ )      """)
            top.addstr( 7, top_pane_geometry[1]-96, r"""  \-;_/\__;__/ _/ _/      """)
            top.addstr( 8, top_pane_geometry[1]-96, r"""   '._}|==o==\{_\/        """)
            top.addstr( 9, top_pane_geometry[1]-96, r"""    /  /-._.--\  \_       """)
            top.addstr(10, top_pane_geometry[1]-96, r"""   // /   /|   \ \ \      """)
            top.addstr(11, top_pane_geometry[1]-96, r"""  / | |   | \;  |  \ \    """)
        elif self._help == 3:
            top.addstr( 0, top_pane_geometry[1]-96, r"""         .-'-.            """)
            top.addstr( 1, top_pane_geometry[1]-96, r"""       /`     |__         """)
            top.addstr( 2, top_pane_geometry[1]-96, r"""     /`  _.--`-,-`        """)
            top.addstr( 3, top_pane_geometry[1]-96, r"""     '-|`   a '<-.   []   """)
            top.addstr( 4, top_pane_geometry[1]-96, r"""       \     _\__) \=`    """)
            top.addstr( 5, top_pane_geometry[1]-96, r"""        C_  `    ,_/      """)
            top.addstr( 6, top_pane_geometry[1]-96, r"""          | ;----'        """)
            top.addstr( 7, top_pane_geometry[1]-96, r"""     _.---| |--._         """)
            top.addstr( 8, top_pane_geometry[1]-96, r"""   .'  _./' '\._ '.       """)
            top.addstr( 9, top_pane_geometry[1]-96, r"""  /--'`  `-.-`  `'-\      """)
            top.addstr(10, top_pane_geometry[1]-96, r""" |         o        \     """)
            top.addstr(11, top_pane_geometry[1]-96, r""" |__ .             / )    """)
        elif self._help == 4:
            top.addstr( 0, top_pane_geometry[1]-96, r"""      ,___          .-;'  """)
            top.addstr( 1, top_pane_geometry[1]-96, r"""       `"-.`\_...._/`.`   """)
            top.addstr( 2, top_pane_geometry[1]-96, r"""    ,      \        /     """)
            top.addstr( 3, top_pane_geometry[1]-96, r""" .-' ',    / ()   ()\     """)
            top.addstr( 4, top_pane_geometry[1]-96, r"""`'._   \  /()    .  (|    """)
            top.addstr( 5, top_pane_geometry[1]-96, r"""    > .' ;,     -'-  /    """)
            top.addstr( 6, top_pane_geometry[1]-96, r"""   / <   |;,     __.;     """)
            top.addstr( 7, top_pane_geometry[1]-96, r"""   '-.'-.|  , \    , \    """)
            top.addstr( 8, top_pane_geometry[1]-96, r"""      `>.|;, \_)    \_)   """)
            top.addstr( 9, top_pane_geometry[1]-96, r"""       `-;     ,    /     """)
            top.addstr(10, top_pane_geometry[1]-96, r"""          \    /   <      """)
            top.addstr(11, top_pane_geometry[1]-96, r"""           '. <`'-,_)     """)
        elif self._help == 5:
            top.addstr( 0, top_pane_geometry[1]-96, r"""                          """)
            top.addstr( 1, top_pane_geometry[1]-96, r"""                 \WWW/    """)
            top.addstr( 2, top_pane_geometry[1]-96, r"""                 /   \    """)
            top.addstr( 3, top_pane_geometry[1]-96, r"""                /wwwww\   """)
            top.addstr( 4, top_pane_geometry[1]-96, r"""              _|  o_o  |_ """)
            top.addstr( 5, top_pane_geometry[1]-96, r"""   \WWWWWWW/ (_   / \   _)""")
            top.addstr( 6, top_pane_geometry[1]-96, r""" _.'` o_o `'._ |  \_/  |  """)
            top.addstr( 7, top_pane_geometry[1]-96, r"""(_    (_)    _): ~~~~~ :  """)
            top.addstr( 8, top_pane_geometry[1]-96, r"""  '.'-...-'.'   \_____/   """)
            top.addstr( 9, top_pane_geometry[1]-96, r"""   (`'---'`)    [     ]   """)
            top.addstr(10, top_pane_geometry[1]-96, r"""    `""'""`     `""'""`   """)
            top.addstr(11, top_pane_geometry[1]-96, r"""                          """)

        top.addstr( 1, top_pane_geometry[1]-67, "== Keys =======================================================")
        top.addstr( 2, top_pane_geometry[1]-67, "|                                                             |")
        top.addstr( 3, top_pane_geometry[1]-67, "|  <tab> : toggle between pipelines and jobs                  |")
        top.addstr( 4, top_pane_geometry[1]-67, "|  j/k   : select new pipeline/job                            |")
        top.addstr( 5, top_pane_geometry[1]-67, "|  r     : re-query DB for new recently triggered pipelines   |")
        top.addstr( 6, top_pane_geometry[1]-67, "|  h     : ask for help                                       |")
        top.addstr( 7, top_pane_geometry[1]-67, "|  q     : exit                                               |")
        top.addstr( 8, top_pane_geometry[1]-67, "|                                                             |")
        top.addstr( 9, top_pane_geometry[1]-67, "===============================================================")


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Bottom pane: pipeline timeline
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        timeline = drawing.draw_timeline(
                      self._current_pipeline,
                      mode=f"unicode:{bottom_pane_geometry[1]-2}:buffer:auto")

        i      = 0
        legend = None
        buffer = []

        # Extract legend and save lines to print to a tmp buffer to see how many lines there are
        #
        if timeline:
            for line in timeline.split("\n"):

                if "LEGEND" in line:
                    legend = {}
                    continue

                if legend is None:
                    buffer.append(line)
                else:
                    # Don't print anything else, just save the legend aliases for later
                    #
                    if ":" in line:
                        alias, full_name          = line.split(":")
                        legend[full_name.strip()] = alias.strip()

            # Print
            #
            i = 0
            for line in buffer:
                if i < bottom_pane_geometry[0]:
                    bottom.addstr(i, 0, line)
                    i += 1


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Middle top pane: pipeline jobs data
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        middle_top.addstr(0, 0,
                f"{textwrap.shorten('alias',                    width=7,  placeholder='...'):7}"
                f"{textwrap.shorten('name',                     width=30, placeholder='...'):30}"
                f"{textwrap.shorten('script',                   width=25, placeholder='...'):25}"
                f"{textwrap.shorten('runner',                   width=20, placeholder='...'):20}"
                f"{textwrap.shorten('detached',                 width=12, placeholder='...'):12}"
                f"{textwrap.shorten('timeout',                  width=14, placeholder='...'):14}"
                f"{textwrap.shorten('retries',                  width=11, placeholder='...'):11}"
                f"{textwrap.shorten('on failure',               width=12, placeholder='...'):18}"
                f"{textwrap.shorten('on input error',           width=16, placeholder='...'):18}"
                f"{textwrap.shorten('current state',            width=14, placeholder='...'):14}"
        )
        middle_top.addstr(1, 0, "-"*168)

        i = 2
        for job in self._current_pipeline.jobs:

            if legend:
                if job.name in legend.keys():
                    alias = legend[job.name]
                else:
                    alias = "-"
            else:
                alias = job.name

            if i-2 == self._current_job_index:

                if self._focus == "jobs":
                    attr = curses.A_REVERSE
                else:
                    attr = 0
            else:
                attr = 0

            try:
                middle_top.addstr(i, 0,
                    f"{textwrap.shorten(alias,                      width=7,  placeholder='...'):7}"
                    f"{textwrap.shorten(job.name,                   width=30, placeholder='...'):30}"
                    f"{textwrap.shorten(job.script,                 width=25, placeholder='...'):25}"
                    f"{textwrap.shorten(job.runner,                 width=20, placeholder='...'):20}"
                    f"{textwrap.shorten(job.detached,               width=12, placeholder='...'):12}"
                    f"{textwrap.shorten(job.timeout,                width=14, placeholder='...'):14}"
                    f"{textwrap.shorten(job.retries,                width=11, placeholder='...'):11}"
                    f"{textwrap.shorten(job.on_failure,             width=18, placeholder='...'):18}"
                    f"{textwrap.shorten(job.on_input_err,           width=18, placeholder='...'):18}"
                    f"{textwrap.shorten(job.metadata.current_state, width=14, placeholder='...'):14}",
                    attr
                )
            except Exception:
                # TODO: Implement scroll
                pass

            i +=1


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Middle bottom pane: job input/output parameters
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self._focus == "jobs":

            middle_bottom.addstr(0, 0,
                    f"{textwrap.shorten('input',                    width=100, placeholder='...'):100}"
                    f"{textwrap.shorten('output',                   width=100, placeholder='...'):100}"
            )
            middle_bottom.addstr(1, 0, "-"*(bottom_pane_geometry[1]-1))

            for i, job in enumerate(self._current_pipeline.jobs):
                if i == self._current_job_index:
                    break
            else:
                return

            input_params  = [ f"{k}={v}" for k,v in job.input.items()]
            output_params = [ f"{k}={v}" for k,v in job.output.items()]

            total_rows = max(len(input_params), len(output_params))

            input_params  += [""] * (total_rows-len(input_params))
            output_params += [""] * (total_rows-len(output_params))

            if input_params  == []: input_params  = [""]
            if output_params == []: output_params = [""]

            i = 2
            for param_index in range(total_rows):

                try:
                    middle_bottom.addstr(i, 0,
                        f"{textwrap.shorten(input_params[param_index],  width=100, placeholder='...'):100}"
                        f"{textwrap.shorten(output_params[param_index], width=100, placeholder='...'):100}"
                    )
                except Exception:
                    # TODO: Implement scroll
                    pass

                i +=1


    def _process_input(self, key, stdscr):
        """
        Change the currently selected item
        """

        if key == "j" or key == "KEY_DOWN":
            if self._focus == "pipelines":
                if self._current_pipeline_index < len(self._all_pipelines)-1:
                    self._current_pipeline_index += 1
                    self._refresh_current_pipeline()
            else:
                if self._current_job_index < len(self._current_pipeline.jobs)-1:
                    self._current_job_index += 1

        elif key == "k" or key == "KEY_UP":
            if self._focus == "pipelines":
                if self._current_pipeline_index > 0:
                    self._current_pipeline_index -= 1
                    self._refresh_current_pipeline()
            else:
                if self._current_job_index > 0:
                    self._current_job_index -= 1

        elif key == "r":
            old_pipelines = len(self._all_pipelines)
            self._refresh_list_of_all_pipelines()
            new_pipelines = len(self._all_pipelines)

            if new_pipelines != old_pipelines:
                # Reset selection
                #
                self._current_pipeline_index = 0
                self._refresh_current_pipeline()

        elif key == chr(9): # TAB key
            if self._focus == "pipelines":
                self._focus = "jobs"
                self._current_job_index = 0
            else:
                self._focus = "pipelines"

        elif key == chr(10): # ENTER key
            if self._focus == "pipelines":
                self._focus = "jobs"
                self._current_job_index = 0
            else:
                self._focus = "pipelines"

        elif key == "h":
            if self._help == 0:
                self._help = random.randint(1,5)
            else:
                self._help = 0

        elif key == "q":
            raise Exception("Quit")


    def loop(self, stdscr):
        """
        Processing loop that takes input and updates the display.
        """

        # Hide cursor
        #
        curses.curs_set(0)


        # Geometry
        #
        #     -----------------------------
        #     |        top                | 1/4
        #     |---------------------------|
        #     |        middle top         | 3/8
        #     |---------------------------|
        #     |        middle bottom      | 1/4 (-2 rows)
        #     |---------------------------|
        #     |        bottom             | 1/8 (+ 2 rows)
        #     -----------------------------
        #
        BORDER = 2

        top_pane_geometry  = (
            ((curses.LINES - BORDER)*2)//8,                       # height
            (curses.COLS  - BORDER),                              # width
            BORDER,                                               # y_off
            BORDER                                                # x_off
        )

        middle_top_pane_geometry = (
            ((curses.LINES - BORDER)*3)//8,                       # height
            (curses.COLS  - BORDER),                              # width
            BORDER + ((curses.LINES - BORDER)*2)//8,              # y_off
            BORDER                                                # x_off
        )

        middle_bottom_pane_geometry = (
            ((curses.LINES - BORDER)*2)//8 - 2,                   # height
            (curses.COLS  - BORDER),                              # width
            BORDER + ((curses.LINES - BORDER)*5)//8,              # y_off
            BORDER                                                # x_off
        )

        bottom_pane_geometry = (
            ((curses.LINES - BORDER)*1)//8 + 2,                   # height
            (curses.COLS  - BORDER),                              # width
            BORDER + ((curses.LINES - BORDER)*7)//8 - 2,          # y_off
            BORDER                                                # x_off
        )


        # Main loop (draw + process input + draw + ...)
        #
        stdscr.timeout(500) # If there is no input from the user in 0.5 seconds, getkey() will raise
                            # an exception

        while True:
            stdscr.clear()

            self._draw(
              stdscr,
              top_pane_geometry,
              middle_top_pane_geometry,
              middle_bottom_pane_geometry,
              bottom_pane_geometry,
            )

            while True:
                try:
                    key = stdscr.getkey()
                    self._process_input(key, stdscr)
                    break

                except Exception as e:
                    if str(e) == "Quit":
                        return ""
                    elif str(e).startswith("ERROR:"):
                        raise e

                    # Time out! Refresh current pipeline and jobs if needed
                    #
                    if len(self._all_pipelines) > 0:
                        if self._current_pipeline.pipeline.metadata.current_state in [ "RUNNING", "WAITING" ]:
                            self._refresh_current_pipeline()
                            break

            stdscr.refresh()

