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

print(f"Execution number #{p_in['__job_attempt']}")

if p_in["__job_attempt"] == "0":
    time.sleep(10)
else:
    time.sleep(3)

sys.exit(0)

