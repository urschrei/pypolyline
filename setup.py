#!/usr/bin/env python
"""
setup.py

Created by Stephan Hügel on 2016-07-25
"""

import sys
from setuptools import setup, Extension
import numpy
from Cython.Build import cythonize


# # Set dynamic RPATH differently, depending on platform
ldirs = []
ddirs = []
if "linux" in sys.platform:
    # from http://stackoverflow.com/a/10252190/416626
    # the $ORIGIN trick is not perfect, though
    ldirs = ["-Wl,-rpath", "-Wl,$ORIGIN"]
    platform_lib = "libpolylineffi.so"
if sys.platform == "darwin":
    # You must compile your binary with rpath support for this to work
    # RUSTFLAGS="-C rpath" cargo build --release
    platform_lib = "libpolyline_ffi.dylib"
    ldirs = ["-Wl,-rpath", "-Wl,@loader_path/"]
if sys.platform == "win32":
    ddirs = ["pypolyline/header.h"]
    platform_lib = "polylineffi.dll"


extensions = Extension(
    "pypolyline.cutil",
    sources=["pypolyline/cutil.pyx"],
    libraries=["polylineffi"],
    depends=ddirs,
    language="c",
    include_dirs=["pypolyline", numpy.get_include()],
    library_dirs=["pypolyline"],
    extra_compile_args=["-O3"],
    extra_link_args=ldirs,
)

extensions = cythonize(
    [
        extensions,
    ],
    compiler_directives={"language_level": "3"},
)

setup(
    package_data={
        "pypolyline": [platform_lib],
    },
    ext_modules=extensions,
)
