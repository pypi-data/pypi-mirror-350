"""
Handle formatting of the generated RTL code
"""
import re
import subprocess
from typing import Dict

VERIBLE_FORMAT_PATH = subprocess.run(['which', 'verible-verilog-format'], capture_output=True).stdout.decode().strip()
assert VERIBLE_FORMAT_PATH, "Verible not found in PATH"


def get_pretty_name(name: str) -> str:
    """
    Convert a snake_case name to a pretty name
    """
    return " ".join(re.split(r"[\W_]+", name)).title()


def format_rtl(rtl_code: str) -> str:
    """
    Format the generated RTL code to be more readable
    """
    return subprocess.run([
        VERIBLE_FORMAT_PATH,
        "-"
    ], input=rtl_code.encode(), capture_output=True).stdout.decode()


def indent_line(line: str, spaces: Dict[str, int]={'indent_amt': 0}) -> str:
    """
    Automatically indent lines in the generated RTL code

    Uses the spaces dictionary to keep track of the current indentation level [key: 'indent_amt']
    """
    if line.strip().startswith('end'):
        assert spaces['indent_amt'] >= 4, "Indentation error: indent_amt should be >= 4"
        spaces['indent_amt'] -= 4

    return_line = " " * spaces['indent_amt'] + line + ('\n' if line[-1] != '\n' else '')

    if line.strip().endswith('begin'):
        spaces['indent_amt'] += 4

    return return_line
