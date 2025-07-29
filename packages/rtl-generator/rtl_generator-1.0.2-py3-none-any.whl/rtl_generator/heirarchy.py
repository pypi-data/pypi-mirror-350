"""
Handle the RTL heirarchy
"""
import os
import re
from pathlib import Path
from typing import Dict, List


def replace_includes(generated_rtl: str, submod_rtls: Dict[str, str]) -> str:
    """
    Recursively replaces include statements in the generated RTL code with the contents of the included file.

    If an included file exists in generated RTL, includes generated RTL for that file.
    Otherwise, includes the contents of the existing file.
    """
    while True:
        match = re.search(r"`include \"(.+?)\"", generated_rtl)
        if match is None:
            break

        start, end = match.span()
        start = generated_rtl.rfind('\n', 0, start)

        include_file = match.group(1)
        submod_name = include_file.split('/')[-1].replace('.sv', '')

        if f"{submod_name}.gen_{submod_name}" in submod_rtls:
            include_rtl = submod_rtls[f"{submod_name}.gen_{submod_name}"]
        else:
            with open(include_file, "r") as f:
                include_rtl = f.read()
        
            pdir = os.getcwd()
            os.chdir(Path(include_file).parent)
            include_rtl = replace_includes(include_rtl, submod_rtls)
            os.chdir(pdir)
        
        generated_rtl = generated_rtl[:start] + generated_rtl[end:] + f"\n{include_rtl}"
        print(f"Included {submod_name}")

    return generated_rtl


def get_subdirs(module_path: str | Path) -> List[Path]:
    paths = []
    for d in filter(lambda d: Path(module_path, d).is_dir(), os.listdir(module_path)):
        if d in ['sim_build', 'models']:
            continue
        if re.search(r"__$", d) or re.search(r"^\.", d):
            continue

        paths.append(Path(module_path, d))

    return paths
