"""
Generate Ble Cdr RTL code
"""
from pathlib import Path

from rtl_generator import *

YAML_PATH = Path(Path(__file__).parent, "options.yml").resolve()


# User-defined imports, functions, and globals
import os
import sys

modules_path = Path(os.environ.get("MODULES_PATH", "/home/brandonhippe/west/Research Projects/SCuM BLE/Python/Modules")).resolve()
sys.path.insert(0, str(modules_path))
from phy.demodulation import *
from phy.iq import *


def samples_per_symbol(existing_vars: dict) -> str:
    '''
    Calculate the number of samples per symbol based on the symbol rate and clock frequency
    '''
    update_used_args(existing_vars, ['fsym', 'clk_freq'])
    symbol_rate = existing_vars['fsym']
    clk_freq = existing_vars['clk_freq']
    assert clk_freq % symbol_rate == 0, "Clock rate must be an integer multiple of symbol rate"

    samples_per_symbol = clk_freq // symbol_rate
    existing_vars['samples_per_symbol'] = samples_per_symbol
    return str(samples_per_symbol)


def define_clock_recovery_type(existing_vars: dict) -> str:
    '''
    Define the clock recovery type
    '''
    update_used_args(existing_vars, ['mf_clock_rec'])
    mf_clock_rec = existing_vars['mf_clock_rec']
    if mf_clock_rec:
        return "`define MATCHED_FILTER_CLOCK_RECOVERY 1"
    else:
        return ""


def instantiate_clock_recovery(existing_vars: dict) -> str:
    update_used_args(existing_vars, ['mf_clock_rec'])

    if existing_vars["mf_clock_rec"]:
        rtl = """
// Clock recovery stuff
clock_recovery #(
    .SAMPLE_RATE(SAMPLE_RATE)
) cr (
    .clk(~clk),
    .en(en),
    .resetn(resetn),

    .mf_bit(demod_bit),

    .symbol_clk(symbol_clk)
);
        """
    else:
        rtl = """
// Preamble Detection stuff
logic preamble_detected;
preamble_detect #(
    .SAMPLE_RATE(SAMPLE_RATE)
) pd (
    .clk(clk),
    .resetn(resetn),
    .en(en),

    .data_bit(demod_bit),
    .preamble_detected(preamble_detected)
);

// Clock recovery stuff
clock_recovery #(
    .SAMPLE_RATE(SAMPLE_RATE),
    .DATA_WIDTH(DATA_WIDTH)
) cr (
    .clk(clk),
    .resetn(resetn),
    .en(en),

    .i_data(i_bpf),
    .q_data(q_bpf),
    .preamble_detected(preamble_detected),

    .symbol_clk(symbol_clk)
);
        """
    
    return fill_in_template(rtl.strip('\n'), existing_vars.get('args', None), existing_vars)
