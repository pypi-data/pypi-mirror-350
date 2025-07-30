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

for i in range(int(p_in["repeat"])):
    print(f"{i} - Your purpose in life is to {p_in['purpose_in_life']}")

print("")
print("Figuring out if this provides you satisfaction...")
time.sleep(3)

if i > 10:
    print("YES!")
    p_out["satisfied"] = "yes"
else:
    print("NO!")
    p_out["satisfied"] = "no"

jp.set_output_parameters_and_values(p_out)


