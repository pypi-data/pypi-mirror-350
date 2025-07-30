#!/usr/bin/python

import os
import sys
import time
import random

try:
    import pipeforge      # For regular users
except Exception:
    sys.path.append(".")  # For developers
    import pipeforge

jp    = pipeforge.JobParams(os.getenv("JOB_ID"))
p_in  = jp.get_input_parameters_and_values()
p_out = {}

print(f"Hello, {p_in['my_name']}. Obtaining your purpose in life...")

time.sleep(3)

if p_in["my_name"] == "John Rambo":
    purpose_in_life = "find Charlies"
else:
    purpose_in_life = random.choice(["be happy",
                                     "make lots of money",
                                     "travel back in time",
                                     "run for president"])

print(f"Your purpose in life is to {purpose_in_life}")

p_out["my_purpose_in_life"] = purpose_in_life
jp.set_output_parameters_and_values(p_out)

