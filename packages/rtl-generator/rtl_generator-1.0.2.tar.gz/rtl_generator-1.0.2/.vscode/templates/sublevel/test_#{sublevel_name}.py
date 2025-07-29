#!/usr/bin/env python3

###########################################
# Sub-level testbench template for cocotb #
###########################################

import cocotb, os, sys
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
from pathlib import Path

proj_path = Path(__file__).resolve().parent
sys.path.append(str(proj_path.parent))

### Import necessary modules from the test_toplevel.py file ###
from test_#{toplevel_name} import runner, load_generated_options
globals().update(load_generated_options(os.path.join(proj_path, os.path.basename(__file__).replace("test_", "").replace(".py", ".#{hdl_ext}"))))


### Define any helper functions here ###


### Define any test functions here ###


### Call the runner function from the test_toplevel.py file ###
if __name__ == "__main__":
    runner(os.path.basename(__file__).replace(".py", "").replace("test_", ""), proj_path, "#{hdl_ext}")
