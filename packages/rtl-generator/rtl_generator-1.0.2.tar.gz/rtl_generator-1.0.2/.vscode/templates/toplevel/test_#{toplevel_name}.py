#!/usr/bin/env python3

###########################################
# Top level testbench template for cocotb #
###########################################


import cocotb, os, sys, yaml, builtins, re
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
from cocotb.runner import get_runner
from pathlib import Path


proj_path = Path(__file__).resolve().parent
sys.path.append(str(proj_path.parent))


### Define any helper functions here ###
def load_generated_options(filepath: Path) -> dict:
    '''
    Load the options used in generating rtl
    '''
    generated_options = {}
    with open(filepath.replace(".#{hdl_ext}", "") + "_options.yml") as f:
        yaml_options = yaml.safe_load(f)

    with open(filepath, "r") as f:
        rtl = f.read().strip()

    options = re.match(r"\/\*([^/*]*)\*\/", rtl)
    if options:
        table_ix = 0
        for option in options.group(1).splitlines():
            option = option.strip()
            if re.match(r"\+[-+]*\+$", option):
                table_ix += 1
                continue

            if table_ix % 3 == 2:
                k, v = re.search(r"\|\s*(\S+)\s*\|\s*(\S+)", option).group(1, 2)
                if k not in yaml_options:
                    continue

                if 'type' in yaml_options[k]:
                    v = getattr(builtins, yaml_options[k]['type'])(v)
                generated_options[k] = v

        rtl = rtl[options.end():]

    for line in rtl.splitlines():
        line = line.strip()
        include_file = re.match(r"`include \"(.*)\"$", line)
        if include_file:
            generated_options.update(load_generated_options(os.path.join(os.sep.join(filepath.split(os.sep)[:-1]), include_file.group(1))))

    return generated_options


def conv_signed_int(bin_str, bit_vals):
    return sum([int(bit) * bit_val for bit, bit_val in zip(bin_str, bit_vals)])


### Define any test functions here ###


### Define the runner function ###
def runner(proj_name, proj_path, hdl_ext="#{hdl_ext}"):
    sim = os.getenv("SIM", "verilator")
    print(f"Running {proj_name} test")
    print(f"Project path: {proj_path}")
    

    sources = [proj_path / f"{proj_name}.{hdl_ext}"]

    runner = get_runner(sim)
    if hdl_ext in ['v', 'sv', 'verilog', 'systemverilog']:
        runner.build(
            verilog_sources=sources,
            hdl_toplevel=f"{proj_name}",
            always=True,
            build_args=[f"-I{proj_path}"],
        )
    else:
        runner.build(
            vhdl_sources=sources,
            hdl_toplevel=f"{proj_name}",
            always=True,
            build_args=[f"-I{proj_path}"],
            waves=True,
        )

    runner.test(test_module=f"test_{proj_name}", hdl_toplevel=f"{proj_name}", test_dir=proj_path, waves=True, verbose=True)


if __name__ == "__main__":
    runner(os.path.basename(__file__).replace(".py", "").replace("test_", ""), Path(__file__).resolve().parent, "#{hdl_ext}")