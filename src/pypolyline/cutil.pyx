#cython: boundscheck=False
# -*- coding: utf-8 -*-
"""
cutil.pyx

Created by Stephan Hügel on 2016-07-31
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
    Input: a list of lon, lat coordinates, and a precision int (5 for Google, 6 for OSM-derived).
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
    if (
        np.char.startswith(polyline, b"latitude") or
        np.char.startswith(polyline, b"longitude") or
        np.char.startswith(polyline, b"no longitude") or
        np.char.startswith(polyline, b"couldn't")
    ):
        raise RuntimeError(polyline)
    return polyline

def decode_polyline(bytes polyline, int precision):
    """
    Decode an encoded Polyline to coordinates.
    Input: a Polyline string, and a precision int (5 for Google, 6 for OSM-derived).
    Output: a list of lon, lat coordinates.

    Example: decode_polyline(_p~iF~ps|U_ulLnnqC_mqNvxq`@, 5)
    Result: [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]

    """
    cdef char* to_send = polyline
    cdef InternalArray result = decode_polyline_ffi(to_send, precision)
    cdef double* incoming_ptr = <double*>(result.data)
    cdef double[:, ::1] view = <double[:result.len,:2:1]>incoming_ptr
    cdef coords = np.copy(view).tolist()
    drop_float_array(result)
    if np.isnan(coords[0][0]):
        raise RuntimeError("Polyline could not be decoded. Is it valid?")
    return coords
