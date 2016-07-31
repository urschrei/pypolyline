cdef extern from "header.h":
    struct _FFIArray:
        void* data
        size_t len

    cdef _FFIArray decode_polyline_ffi(char* polyline, int precision);
    cdef char* encode_coordinates_ffi(_FFIArray, int precision);
    cdef void drop_float_array(_FFIArray coords);
    cdef void drop_cstring(char* polyline)
