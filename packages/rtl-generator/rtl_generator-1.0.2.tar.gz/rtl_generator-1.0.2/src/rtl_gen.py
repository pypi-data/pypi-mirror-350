import argparse
import os
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from dataclasses import dataclass

from rtl_generator import (add_args, fill_in_template, get_pretty_name,
                           get_subdirs, replace_includes, rtl_generator)


def run_generator(rtl_name: str, cli_args: argparse.Namespace, mod_str: str, **kwargs) -> str:
    """
    Run the RTL generator for a given module
    """
    try:
        import_module(mod_str)
        calling_module = sys.modules[mod_str]
        mod_vars = vars(calling_module)
    except ImportError:
        mod_vars = {}
        
    return rtl_generator(rtl_name, cli_args, mod_vars, **kwargs)

@dataclass
class setup:
    """
    Set up the RTL generation environment.

    Script entry
    """
    cli_args: argparse.Namespace

    def __call__(self, rtl_name: str, proj_path: str | Path) -> None:
        if os.path.exists(str(Path(proj_path, "options.yml"))):
            print("RTL Generator environment already exists")
            return
        
        print(f"Setting up RTL Generator environment for project: {get_pretty_name(rtl_name)}")

        subprocess.run(["cp", str(Path(Path(__file__).parent, "options.yml")), str(proj_path)])

        with open(Path(Path(__file__).parent, "top_level.py")) as f:
            top_level_py = f.read()
        top_level_py = fill_in_template(top_level_py, None, vars())
        with open(Path(proj_path, f"gen_{rtl_name}.py"), "w") as f:
            f.write(top_level_py)
        
        update(self.cli_args)(rtl_name, proj_path)

        print(f"\nFinished setting up RTL Generator environment for project: {get_pretty_name(rtl_name)}")
        print('-' * os.get_terminal_size().columns)

    @staticmethod
    def add_args(rtl_name: str, proj_path: str | Path, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        return parser


@dataclass
class update:
    """
    Update the generation scripts in the hierarchy

    Script entry
    """
    cli_args: argparse.Namespace

    def __call__(self, rtl_name: str, proj_path: str | Path) -> None:
        print(f"Updating generators in RTL heirarchy for: {get_pretty_name(rtl_name)}")

        for submod in get_subdirs(proj_path):
            os.chdir(submod)
            submod_name = submod.name

            gen_path = Path(submod, f"gen_{submod_name}.py")
            if not gen_path.exists():
                with open(Path(Path(__file__).parent, "sub_level.py")) as f:
                    sub_level_py = f.read()
                sub_level_py = fill_in_template(sub_level_py, None, vars())
                with open(gen_path, "w") as f:
                    f.write(sub_level_py)

            self(submod_name, submod)

            os.chdir(proj_path)

        print(f"\nFinished updating generators in RTL heirarchy for: {get_pretty_name(rtl_name)}")
        print('-' * os.get_terminal_size().columns)

    @staticmethod
    def add_args(rtl_name: str, proj_path: str | Path, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        return parser


@dataclass
class generate:
    """
    Generate RTL

    Script entry
    """
    cli_args: argparse.Namespace

    def __call__(self, rtl_name: str, proj_path: str | Path) -> None:
        print(f"Generating RTL for project: {get_pretty_name(rtl_name)}")

        generated_rtl = run_generator(rtl_name, self.cli_args, f"gen_{rtl_name}")
        
        submod_rtls = {}
        available_submods = get_subdirs(proj_path)
        while available_submods:
            submod_path = available_submods.pop()
            os.chdir(submod_path)

            name = submod_path.name
            submod_rtls[name] = run_generator(name, self.cli_args, f"{name}.gen_{name}")

            available_submods.extend(get_subdirs(submod_path))
            os.chdir(proj_path)

        if self.cli_args.replace_includes:
            submod_rtls = {rtl_name: replace_includes(generated_rtl, submod_rtls)}
        else:
            submod_rtls[rtl_name] = generated_rtl

        print(f"\n{'-' * os.get_terminal_size().columns}\nWriting RTL to files...\n")
        for rtl_name, rtl in submod_rtls.items():
            output_file = getattr(self.cli_args, f"{rtl_name}_output")
            with open(output_file, "w") as f:
                f.write(rtl)
                print(f"Generated RTL for {rtl_name} saved to {f.name}")

        print(f"\nFinished generating RTL for project: {get_pretty_name(rtl_name)}")
        print('-' * os.get_terminal_size().columns)

    @staticmethod
    def add_args(rtl_name: str, proj_path: str | Path, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        return add_args(rtl_name, proj_path, parser)


def main() -> None:
    """
    Main entry point for the script
    
    Create CLI parser and add arguments

    Call the requested function
    """
    proj_path = Path(os.getcwd())
    sys.path.insert(0, str(proj_path))
    rtl_name = proj_path.name

    # Create CLI
    parser = argparse.ArgumentParser(description=f"RTL Generator")
    subparsers = parser.add_subparsers(title="Commands")
    for f in filter(lambda f: callable(f) and f.__doc__ and f.__doc__.strip().splitlines()[-1].endswith("Script entry"), globals().values()):
        command_name = f.__name__
        help_str = "\n".join(filter(None, f.__doc__.strip().splitlines()[:-1]))
        subparser = subparsers.add_parser(command_name, description=f"{command_name}: {help_str}")
        f.add_args(rtl_name, proj_path, subparser)
        subparser.set_defaults(func=f)

    # Parse arguments and run function
    args = parser.parse_args()
    func = args.func(args)
    func(rtl_name, proj_path)


if __name__ == "__main__":
    main()
