import ctypes
from ctypes import Structure, POINTER, c_void_p, c_size_t, c_double, c_char_p, cast

from array import array
import numpy as np
import ipdb

lib = ctypes.cdll.LoadLibrary("libpolyline_ffi.dylib")

class _FFIArray(Structure):
    """
    Convert sequence of float lists to a C-compatible void array
    example: [[1.0, 2.0], [3.0, 4.0]]
    Sequence members are _CoordArray instances

    """
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions from a sequence of 64-bit floats."""
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type = c_double):
        arr = ((c_double * 2) * len(seq))()
        for i, member in enumerate(seq):
            arr[i][0] = member[0]
            arr[i][1] = member[1]
        self.data = cast(arr, c_void_p)
        self.len = len(seq)


class _Result(Structure):
    """ Container for returned FFI data """
    _fields_ = [("coords", _FFIArray)]


def _void_array_to_nested_list(res, _func, _args):
    """ Convert the FFI result to Python data structures """
    coords = [list(pair) for pair in
        ((POINTER(c_double * 2).from_buffer_copy(res.coords)[:res.coords.len]))
        ]
    drop_array(res.coords)
    return coords

def char_array_to_string(res, _func, _args):
    converted = cast(res, c_char_p)
    result = converted.value
    drop_cstring(converted)
    return result

decode_polyline = lib.decode_polyline_ffi
decode_polyline.argtypes = (c_char_p,)
decode_polyline.restype = _Result
decode_polyline.errcheck = _void_array_to_nested_list

encode_coordinates = lib.encode_coordinates_ffi
encode_coordinates.argtypes = (_FFIArray,)
encode_coordinates.restype = c_void_p
encode_coordinates.errcheck = char_array_to_string


# Free FFI-allocated memory
drop_cstring = lib.drop_cstring
drop_cstring.argtypes = (c_char_p,)
drop_cstring.restype = None

drop_array = lib.drop_float_array
drop_array.argtypes = (_FFIArray,)
drop_array.restype = None

# pl = "_ibE_seK_seK_seK"
# print decode_polyline(pl)
print encode_coordinates([[1.0, 2.0], [3.0, 4.0]])

