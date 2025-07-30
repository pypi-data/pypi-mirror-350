#!/usr/bin/python

import os
import sys
import time

try:
    import pipeforge      # For regular users
except Exception:
    sys.path.append(".")  # For developers
    import pipeforge

jp    = pipeforge.JobParams(os.getenv("JOB_ID"))
p_in  = jp.get_input_parameters_and_values()
p_out = {}

print("Summary:")
print(f"Satisfaction #1: {p_in['satisfaction_1']}")
print(f"Satisfaction #2: {p_in['satisfaction_2']}")

time.sleep(3)

if p_in["satisfaction_1"] == "no" or p_in["satisfaction_2"] == "no":
    sys.exit(-1)
else:
    sys.exit(0)

