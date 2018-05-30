#ifndef HEADER_H
#define HEADER_H

typedef struct Array {
    void* data;
    size_t len;
} Array;

Array decode_polyline_ffi(char* pl, int precision);

char* encode_coordinates_ffi(Array coords, int precision);

void drop_float_array(Array arr);

void drop_cstring(char* p);


#endif
