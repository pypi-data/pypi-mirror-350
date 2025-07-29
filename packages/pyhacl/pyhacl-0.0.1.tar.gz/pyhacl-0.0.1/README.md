# pyhacl

Python binding to the HACL* library

## Build

Install the necessary tools for building hacl*: cmake, ninja and clang.

Move inside the hacl-packages submodule and run `./mach build --release`, it
compiles the files necessary for pyhacl.

Move back in the pyhacl project root to create a virtual environment and install
the project inside: `python3 -m venv .venv && .venv/bin/pip install -e .[dev]`.

Starting here you should be able to use the `.venv/bin/pyhacl` binary.

To recompile the cython files run `.venv/bin/python setup.py build_ext --inplace`.
