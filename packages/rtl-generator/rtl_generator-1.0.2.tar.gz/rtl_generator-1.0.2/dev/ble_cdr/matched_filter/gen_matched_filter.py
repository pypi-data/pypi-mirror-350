"""
Generate Matched Filter RTL code
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from rtl_generator import *
from gen_ble_cdr import *


# User-defined imports, functions, and globals
from itertools import product
from math import ceil, log2

import numpy as np
import prettytable
# from test_matched_filter import genTemplates


def calc_templates(scope: dict) -> str:
    """
    Calculate all template-related values
    """

    rtl = """
    localparam int TEMPLATE_WIDTH = #{(template_width)};
    localparam int PROD_WIDTH = DATA_WIDTH + TEMPLATE_WIDTH;
    localparam int PROD_SUM_WIDTH = $clog2(SAMPLE_RATE) + PROD_WIDTH;
    localparam int SQR_WIDTH = 2 * PROD_SUM_WIDTH;
    localparam int SCORE_WIDTH = SQR_WIDTH + 1;

//! Template Table
#{(template_table)}
    """

    return fill_in_template(rtl, scope.get("args", None), scope)


def template_width(existing_vars: dict) -> str:
    """
    Calculate the width of the templates
    """
    update_used_args(existing_vars, ['amp'])
    amp = existing_vars['amp']
    template_width = ceil(log2(amp + 1)) + 1
    existing_vars['template_width'] = template_width

    return str(template_width)


def template_table(existing_vars: dict) -> str:
    """
    Generate the matched filter templates and display them in a table
    """
    update_used_args(existing_vars, ['ifreq', 'fsym', 'amp'])
    if callable(samples_per_symbol):
        samples_per_symbol(existing_vars)

    ifreq = existing_vars['ifreq']
    symbol_rate = existing_vars['fsym']
    df = symbol_rate * 0.25
    amp = existing_vars['amp']
    samples_per_bit = existing_vars['samples_per_symbol']
    
    templates = genTemplates(ifreq, df, samples_per_bit, 1/symbol_rate, amp, 0)
    high_template_i = np.array(np.real(templates[1]), dtype=int)
    high_template_q = np.array(np.imag(templates[1]), dtype=int)
    low_template_i = np.array(np.real(templates[0]), dtype=int)
    low_template_q = np.array(np.imag(templates[0]), dtype=int)

    print("\nGenerated matched filter templates:")
    template_table = prettytable.PrettyTable()
    template_table.set_style(prettytable.DOUBLE_BORDER)
    template_table.add_column("Template", ["0 Template I", "0 Template Q", "1 Template I", "1 Template Q"])
    for ix in range(len(templates[0])):
        template_table.add_column(str(ix), [low_template_i[ix], low_template_q[ix], high_template_i[ix], high_template_q[ix]], align='r')

    print(template_table)
    template_table.set_style(prettytable.MARKDOWN)
    template_table = template_table.get_string()

    existing_vars['low_template_i'] = low_template_i
    existing_vars['low_template_q'] = low_template_q
    existing_vars['high_template_i'] = high_template_i
    existing_vars['high_template_q'] = high_template_q
    existing_vars['template_table'] = template_table
    return "\n".join(map(lambda l: f"//! {l}", template_table.splitlines()))


def template_product_sum(existing_vars: dict) -> str:
   """ 
   Create the rtl for calculating the sum of the template products with received I/Q data
   """

   samples_per_symbol = existing_vars['samples_per_symbol']

   sv_code = []
   for template, phase in product(["low", "high"], ["i", "q"]):
      sv_code.append(f"// {template.capitalize()} template {phase} product and sum") 
      sv_code.append(f"{template}_i_{phase}_prod_sum = 0;") 
      sv_code.append(f"{template}_q_{phase}_prod_sum = 0;") 

      template_arr = existing_vars[f"{template}_template_{phase}"]

      for ix, template_val in enumerate(template_arr):
         if template_val == 0:
               continue

         op = "+" if template_val > 0 else "-"

         shift_amt = 0
         template_val = abs(template_val)
         while template_val != 0:
               if template_val % 2 == 1:
                  sv_code.append(f"{template}_i_{phase}_prod_sum = {template}_i_{phase}_prod_sum {op} (i_buffer[{samples_per_symbol - (ix + 1)}] << {shift_amt});") 
                  sv_code.append(f"{template}_q_{phase}_prod_sum = {template}_q_{phase}_prod_sum {op} (q_buffer[{samples_per_symbol - (ix + 1)}] << {shift_amt});") 

               shift_amt += 1
               template_val >>= 1

         sv_code.append("") 

   return "\n".join(sv_code[:-1])
