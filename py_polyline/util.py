import os
from sys import platform, version_info
from ctypes import Structure, POINTER, c_void_p, c_size_t, c_double, c_uint32, c_char_p, cast, cdll, string_at
import numpy as np

file_path = os.path.dirname(__file__)

if platform == "darwin":
    prefix = 'lib'
    ext = "dylib"
elif "linux" in platform:
    prefix = 'lib'
    ext = "so"
    fpath = os.path.join(file_path, ".libs")

elif "win32" in platform:
    prefix = ''
    ext = 'dll'

prefix = {'win32': ''}.get(platform, 'lib')
extension = {'darwin': '.dylib', 'win32': '.dll'}.get(platform, '.so')

# Python 3 check
if (version_info > (3, 0)):
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


class _FFIArray(Structure):
    """
    Convert sequence of float lists to a C-compatible void array
    example: [[1.0, 2.0], [3.0, 4.0]]

    """
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    @classmethod
    def from_param(cls, seq):
        """  Allow implicit conversions """
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type = c_double):
        ptr = POINTER(data_type)
        nparr = np.array(seq, dtype=np.float64)
        arr = nparr.ctypes.data_as(ptr)
        self.data = cast(arr, c_void_p)
        self.len = len(seq)


class _CoordResult(Structure):
    """ Container for returned FFI coordinate data """
    _fields_ = [("coords", _FFIArray)]


class _PolylineResult(Structure):
    """ Container for returned FFI Polyline data """
    _fields_ = [("line", c_void_p)]


def _void_array_to_nested_list(res, _func, _args):
    """ Dereference the FFI result to a list of coordinates """
    shape = (res.coords.len, 2)
    array_size = np.prod(shape)
    mem_size = 8 * array_size
    array_str = string_at(res.coords.data, mem_size)
    array = np.frombuffer(array_str, float, array_size).reshape(shape).tolist()
    drop_array(res.coords)
    return array

def void_array_to_string(res, _func, _args):
    """ Dereference the FFI result to a utf8 polyline """
    result = cast(res.line, c_char_p)
    polyline = result.value
    drop_cstring(res.line)
    return polyline

decode_polyline = lib.decode_polyline_ffi
decode_polyline.argtypes = (c_char_p, c_uint32)
decode_polyline.restype = _CoordResult
decode_polyline.errcheck = _void_array_to_nested_list

encode_coordinates = lib.encode_coordinates_ffi
encode_coordinates.argtypes = (_FFIArray, c_uint32)
encode_coordinates.restype = _PolylineResult
encode_coordinates.errcheck = void_array_to_string

# Free FFI-allocated memory
drop_cstring = lib.drop_cstring
drop_cstring.argtypes = (c_void_p,)
drop_cstring.restype = None

drop_array = lib.drop_float_array
drop_array.argtypes = (_FFIArray,)
drop_array.restype = None
