#cython: boundscheck=False
# -*- coding: utf-8 -*-
"""
cutil.pyx

Created by Stephan Hügel on 2016-07-31

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
__author__ = u"Stephan Hügel"

import numpy as np
from pypolyline_p cimport (
    ExternalArray,
    InternalArray,
    decode_polyline_ffi,
    encode_coordinates_ffi,
    drop_float_array,
    drop_cstring
    )

def encode_coordinates(coords, int precision):
    """
    Encode coordinates as a Polyline.
    Input: a list of lat, lon coordinates, and a precision int (5 for Google, 6 for OSM-derived).
    Output: an encoded Polyline string.

    Example: encode_coordinates([[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]], 5)
    Result: "_p~iF~ps|U_ulLnnqC_mqNvxq`@"

    """
    cdef double[:,::1] ncoords = np.array(coords, dtype=np.float64)
    cdef ExternalArray coords_ffi
    coords_ffi.data = <void*>&ncoords[0, 0]
    coords_ffi.len = ncoords.shape[0]
    cdef char* result = encode_coordinates_ffi(coords_ffi, precision)
    cdef bytes polyline = result
    drop_cstring(result)
    return polyline

def decode_polyline(bytes polyline, int precision):
    """
    Decode an encoded Polyline to coordinates.
    Input: a Polyline string, and a precision int (5 for Google, 6 for OSM-derived).
    Output: a list of lat, lon coordinates.

    Example: decode_polyline(_p~iF~ps|U_ulLnnqC_mqNvxq`@, 5)
    Result: [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]

    """
    cdef char* to_send = polyline
    cdef InternalArray result = decode_polyline_ffi(to_send, precision)
    cdef double* incoming_ptr = <double*>(result.data)
    cdef double[:, ::1] view = <double[:result.len,:2:1]>incoming_ptr
    cdef coords = np.copy(view).tolist()
    drop_float_array(result)
    return coords
