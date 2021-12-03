cdef extern from "header.h":
    struct InternalArray:
        void* data
        size_t len

    struct ExternalArray:
        void* data
        size_t len

    cdef InternalArray decode_polyline_ffi(char* polyline, int precision);
    cdef char* encode_coordinates_ffi(ExternalArray, int precision);
    cdef void drop_float_array(InternalArray coords);
    cdef void drop_cstring(char* polyline)
