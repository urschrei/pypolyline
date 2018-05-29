cdef extern from "header.h":
    struct Array:
        void* data
        size_t len

    cdef Array decode_polyline_ffi(char* polyline, int precision);
    cdef char* encode_coordinates_ffi(Array, int precision);
    cdef void drop_float_array(Array coords);
    cdef void drop_cstring(char* polyline)
