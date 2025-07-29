# RTL-Generator

## Overview

This repository contains an RTL-Generator and flexible parameterizer written in Python. Documentation is currently a work in progress.

![RTL Generator Architecture](docs/architecture.svg)  
*Intended workflow using RTL-Generator.*

RTL-Generator is built to enable easy and flexible parameterization of RTL code. Currently, only Verilog/SystemVerilog is supported (due to use of formatter). Using RTL-Generator with an existing or new RTL project is easy: simply run `gen-rtl setup` at the top-level of your heirarchy, add your configuration options to `options.yml`, add parameter keys to the RTL, and add any more complex parameterization to a `gen_<module_name>.py` script. `gen-rtl generate` will then automatically generate your parameterized RTL project!

## Installation

RTL-Generator can be installed using `python -m pip install rtl-generator`, and running any of `gen-rtl setup`, `gen-rtl update`, or `gen-rtl generate`.

RTL-generator also depends on [Verible](https://github.com/chipsalliance/verible) to format output RTL. Follow Verible's install directions and ensure `which verible-verilog-format` outputs the path to the Verible formatter executable.

## Usage

In short, the subcommands provided by `gen-rtl` are:

- [setup](#setup): Sets up necessary files to use RTL-Generator in a new/existing project
- [update](#update): Ensure necessary files to use RTL-Generator are in place after modifying the RTL heirarchy
- [generate](#generate): Generate the parameterized RTL

Additionally, a number of files within the project directory structure are necessary:

- [options.yml](#options-yaml): A YAML file in the top level directory that defines arguments for the generator.
- [gen_{rtl_name}.py](#generator-helpers): Python scripts alongside any module in the heirarchy, used to integrate any module-specific generation functionality.

These files can be automatically created using the `setup` and `update` commands.

### Setup

This subcommand is run using `gen-rtl setup` in the same directory as the top-level module in your project. The name of this directory is used as `rtl_name` in file creation. 

- A python script named `gen_{rtl_name}.py`. This is used by default to ensure all submodules pick up the same top level `options.yml` file in generation, so default arguments only need to be modified in a single place.
- Additional scripts named `gen_{submodule_name}.py` in any submodule directory, following the same directory name to script name transform.

This command takes no arguments, and only executes if `options.yml` does not exist.

### Update

This subcommand is run using `gen-rtl update` in any directory in your project. It will automatically create submodule scripts in any submodule directory of the directory it is ran in, if such a script does not already exist. This command takes no arguments.

### Generate

This subcommand is run using `gen-rtl generate` in any directory in your project. It triggers the generator to generate the RTL for the module in that directory and any submodules thereof, propagating the same options to all generated RTL. This command takes any argument defined in the top level `options.yml`, as well as `--{module_name}_input`, `--{module_name}_output`, which define the path to the input template file and output RTL files respectively, and `--replace_includes`, which tells the generator to merge all of the generated and included RTL into the same top-level RTL file.

The generator finds parameterizable sections by looking for instances of the tag `#{(parameter_name)}`. If a tag is contained within a comment of the RTL, the tag is not replaced by the generator, and needs a matching `#{/(parameter_name)}` tag also within a comment to indicate the end of the section. By not replacing the tag, the generated RTL can be re-used as the template in future runs of the generator. Tags not within comments are replaced by the generator, and are intended for use as single-generation only.

The generator determines what to replace parameterized sections with by searching for a match of `parameter_name` in the following order:

- Variable in current Generator Helper scope: replaces the section with the value of the variable
- Function in the current Generator Helper scope: replaces the section with the returned string from calling the function
- Variable in the global scope (this includes passed arguments): replaces the section with the value of the variable
- Function in the global scope: replaces the section with the returned string from calling the function

A `KeyError` is raised and generated RTL not written if `parameter_name` is not found in any of the above locations.

### Files used by RTL-Generator

#### Options YAML

The `options.yml` file is used to automatically create the CLI for the generator for a project. This project uses [Argparse](https://docs.python.org/3/library/argparse.html), so any keyword arg used in creating a CLI using argparse can be defined in this file. Generating at any level of the heirarchy references the same `options.yml` file at the top level, meaning default argument values only have to be modified in one place.

#### Generator Helpers

These python scripts get loaded when a module is being generated, and are not intended to be ran standalone. The default versions generated by running `setup` or `update` import their parent helper, with the top level helper defining the path to `options.yml` used by `generate`.

These scripts are where more complex parameterization is intended to take place: other Python modules can be included here to calculate options or generate RTL at runtime. An example of this for a Bluetooth Low Energy Digital Baseband can be seen on the `dev` branch.

### Included Methods

There are other useful methods that this module exposes, though documentation/development of these is ongoing. Examples can be seen in the example Bluetooth Low Energy Digital Baseband on the `dev` branch.

## Development

Development on this project is done on the `dev` branch.

## Attribution and Related Publications:

Please cite RTL-Generator by the following publication:

```
@article{rtl-generator,
  author={Hippe, Brandon P. and Burnett, David C.},
  journal={2025 Workshop on Conventions, Tools, and Ideas in Physical Design (WOVEN)},
  title={A Python-based RTL Generator Demonstrated on a Low-IF 2-FSK Wireless Communication System},
  year={2025},
  pages={1-3},
  note={Accepted, to appear},
}
```