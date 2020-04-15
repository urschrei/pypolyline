# -*- coding: utf-8 -*-
"""
util.py

Created by Stephan Hügel on 2016-07-19

This file is part of pypolyline.

The MIT License (MIT)

Copyright (c) 2016 Stephan Hügel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import os
from sys import platform, version_info
from ctypes import (
    Structure,
    POINTER,
    c_void_p,
    c_size_t,
    c_double,
    c_uint32,
    c_char_p,
    cast,
    cdll,
)
import numpy as np

__author__ = u"Stephan Hügel"
__version__ = "0.2.2"

file_path = os.path.dirname(__file__)

prefix = {"win32": ""}.get(platform, "lib")
extension = {"darwin": ".dylib", "win32": ".dll"}.get(platform, ".so")
fpath = {"darwin": "", "win32": ""}.get(platform, os.path.join(file_path, ".libs"))

# Python 3 check
if version_info > (3, 0):
    from subprocess import getoutput as spop

    py3 = True
else:
    from subprocess import check_output as spop

    py3 = False

try:
    lib = cdll.LoadLibrary(os.path.join(file_path, prefix + "polyline_ffi" + extension))
except OSError:
    # the Rust lib's been grafted by manylinux1
    if not py3:
        fname = spop(["ls", fpath]).split()[0]
    else:
        fname = spop(["ls %s" % fpath]).split()[0]
    lib = cdll.LoadLibrary(os.path.join(file_path, ".libs", fname))


class EncodingError(Exception):
    def __init__(self, message):
        super(EncodingError, self).__init__(message)


class DecodingError(Exception):
    def __init__(self, message):
        super(DecodingError, self).__init__(message)


class _FFIArray(Structure):
    """
    Convert sequence of float lists to a C-compatible void array
    example: [[1.0, 2.0], [3.0, 4.0]]

    """

    _fields_ = [("data", c_void_p), ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions """
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type=c_double):
        array = np.array(seq, dtype=np.float64)
        self._buffer = array.data
        self.data = cast(array.ctypes.data_as(POINTER(data_type)), c_void_p)
        self.len = len(seq)


class _CoordResult(Structure):
    """ Container for returned FFI coordinate data """

    _fields_ = [("coords", _FFIArray)]


class _PolylineResult(Structure):
    """ Container for returned FFI Polyline data """

    _fields_ = [("line", c_void_p)]


def _void_array_to_nested_list(res, _func, _args):
    """ Dereference the FFI result to a list of coordinates """
    try:
        shape = res.coords.len, 2
        ptr = cast(res.coords.data, POINTER(c_double))
        array = np.ctypeslib.as_array(ptr, shape)
        if np.isnan(np.sum(array)):
            raise DecodingError("Your Polyline was not valid and could not be decoded")
        return array.tolist()
    finally:
        _drop_array(res.coords)


def _void_array_to_string(res, _func, _args):
    """ Dereference the FFI result to a utf8 polyline """
    try:
        result = cast(res.line, c_char_p)
        polyline = bytes(result.value)
        if polyline.startswith(b"Latitude"):
            raise EncodingError(
                "%s. Latitudes must be between -90.0 and 90.0" % polyline
            )
        elif polyline.startswith(b"Longitude"):
            raise EncodingError(
                "%s. Longitudes must be between -180.0 and 180.0" % polyline
            )
        return polyline
    finally:
        _drop_cstring(res.line)


decode_polyline = lib.decode_polyline_ffi
decode_polyline.argtypes = (c_char_p, c_uint32)
decode_polyline.restype = _CoordResult
decode_polyline.errcheck = _void_array_to_nested_list
decode_polyline.__doc__ = """
    Decode an encoded Polyline to coordinates.
    Input: a Polyline string, and a precision int (5 for Google, 6 for OSM-derived).
    Output: a list of lon, lat coordinates.

    Example: decode_polyline(_p~iF~ps|U_ulLnnqC_mqNvxq`@, 5)
    Result: [[-120.2, 38.5], [-120.95, 40.7], [-126.453, 43.252]]

    Incorrect Polyline input will throw util.DecodingError

 """

encode_coordinates = lib.encode_coordinates_ffi
encode_coordinates.argtypes = (_FFIArray, c_uint32)
encode_coordinates.restype = _PolylineResult
encode_coordinates.errcheck = _void_array_to_string
encode_coordinates.__doc__ = """
    Encode coordinates as a Polyline.
    Input: a list of lon, lat coordinates, and a precision int (5 for Google, 6 for OSM-derived).
    Output: an encoded Polyline string.

    Example: encode_coordinates([[-120.2, 38.5], [-120.95, 40.7], [-126.453, 43.252]], 5)
    Result: "_p~iF~ps|U_ulLnnqC_mqNvxq`@"

    Incorrect coordinate input will throw util.EncodingError

"""

# Free FFI-allocated memory
_drop_cstring = lib.drop_cstring
_drop_cstring.argtypes = (c_void_p,)
_drop_cstring.restype = None

_drop_array = lib.drop_float_array
_drop_array.argtypes = (_FFIArray,)
_drop_array.restype = None
