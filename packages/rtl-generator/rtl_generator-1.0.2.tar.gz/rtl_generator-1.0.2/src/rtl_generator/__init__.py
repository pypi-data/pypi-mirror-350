#!/usr/bin/env python3
f''' 
RTL Generator/Parameterizer

Written by Brandon Hippe (bhippe@pdx.edu)
'''

from .arguments import add_args, update_used_args
from .format import format_rtl, get_pretty_name
from .generator import fill_in_template, rtl_generator
from .heirarchy import get_subdirs, replace_includes

__all__ = [
    'rtl_generator',
    'add_args',
    'update_used_args',
    'replace_includes',
    'format_rtl',
    'get_subdirs',
    'get_pretty_name',
    'fill_in_template',
]
