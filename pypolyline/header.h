#ifndef HEADER_H
#define HEADER_H

typedef struct _FFIArray {
    void* data;
    size_t len;
} _FFIArray;

_FFIArray decode_polyline_ffi(char* pl, int precision);

char* encode_coordinates_ffi(_FFIArray coords, int precision);

void drop_float_array(_FFIArray arr);

void drop_cstring(char* p);


#endif
