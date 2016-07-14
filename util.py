import ctypes
from ctypes import Structure, POINTER, c_void_p, c_size_t, c_double, cast

from array import array
import numpy as np

lib = ctypes.cdll.LoadLibrary("libpolyline_ffi.dylib")

class _CoordArray(Structure):
    """
    Convert a list of floats to a C-compatible void array

    """
    _fields_ = [("data", c_void_p), ("len", c_size_t)]

    def __init__(self, seq, data_type = c_double):
        array_type = data_type * len(seq)
        try:
            raw_seq = array_type.from_buffer(seq.astype(np.float64))
        except (TypeError, AttributeError):
            try:
                raw_seq = array_type.from_buffer_copy(seq.astype(np.float64))
            except (TypeError, AttributeError):
                # it's a list or a tuple
                raw_seq = array_type.from_buffer(array('d', seq))
        self.data = cast(raw_seq, c_void_p)
        self.len = len(seq)


class _FFIArray(Structure):
    """
    Convert sequence of float lists to a C-compatible void array
    example: [[1.0, 2.0], [3.0, 4.0]]
    Sequence members are _CoordArray instances

    """
    _fields_ = [("data", POINTER(_CoordArray)),
                ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions from a sequence of 64-bit floats."""
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type = c_double):
        self.data = cast(_CoordArray(seq), c_void_p)
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
    result = res.value
    drop_cstring(res)
    return result

# lib.encode_coordinates_ffi.argtypes = (_FFIArray,)
# lib.encode_coordinates_ffi = ctypes.c_void_p
# lib.drop_cstring.argtypes = [ctypes.c_char_p]
decode_polyline = lib.decode_polyline_ffi
decode_polyline.argtypes = (ctypes.c_char_p,)
decode_polyline.restype = _Result
decode_polyline.errcheck = _void_array_to_nested_list

encode_coordinates = lib.encode_coordinates_ffi
encode_coordinates.argtypes = (_FFIArray,)
encode_coordinates.restype = ctypes.c_char_p
encode_coordinates.errcheck = char_array_to_string


# Free FFI-allocated memory
drop_cstring = lib.drop_cstring
drop_cstring.argtypes = (ctypes.c_char_p,)
drop_cstring.restype = None

drop_array = lib.drop_float_array
drop_array.argtypes = (_FFIArray,)
drop_array.restype = None


pl = "a`koG`qiiMrwH||R`|Qj_UbpRtuTj|K`aNjhQ~nUzqMzdSpxOzoUx{CpwOliYbwLdrZt_Md}[`zEro\\zfDzd\\zt@xw\\}lBjyQb~JikF~pYryCjqf@fxJ|nb@dyHrte@cjA`xf@siA`xg@uuFzhf@_cB`rg@hjAzkh@fn@hng@nbAzbi@lxAdvT~gB~qZxnD|v\\~}VtuFftTlaSnlTrdXrxQxl]zsJxld@jvQne_@`dOnyb@jySrpYndOx__@d`L|r`@~nLtrc@jrCdu`@bxH|bWtmLfw[hlG~tc@f{Hxf^rrKdp\\vuPj~WriFptL`cBfiM"
# pl = 'ynh`IcftoCyq@Ne@ncBds@EEycB'
print decode_polyline(pl)
print encode_coordinates([[1.0, 2.0], [3.0, 4.0]])

