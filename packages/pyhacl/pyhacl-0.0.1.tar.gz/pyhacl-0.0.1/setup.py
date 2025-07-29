import itertools
import os
import pathlib
from setuptools import Extension, setup
from Cython.Build import cythonize

root = pathlib.Path(__file__).parent
hacl_packages = root.joinpath('hacl-packages')
include_dirs = [
    os.fspath(include_dir)
    for include_dir, _
    in itertools.groupby(
        hacl_packages.glob('**/*.h'),
        lambda path: path.parent
    )
    if 'benchmarks' not in include_dir.parents
    if 'build' not in include_dir.parents
    if 'config' not in include_dir.parents
    if 'msvc' not in include_dir.parents
    if 'rust' not in include_dir.parents
    if 'tests' not in include_dir.parents
]
cython_extensions = [
    Extension(
        name=os.fspath(
            path.relative_to(root/'src').with_suffix('')
        ).replace('/', '.'),
        sources=[os.fspath(path.relative_to(root))],
        include_dirs=include_dirs
    )
    for path in root.glob('src/pyhacl/**/*.py')
    if path.with_suffix('.pxd').is_file()
]

setup(
    ext_modules=cythonize(
        cython_extensions,
        annotate=True,
        language_level='3'
    )
)
