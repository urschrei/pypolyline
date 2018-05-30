
#ifndef cheddar_generated_header_h
#define cheddar_generated_header_h


#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>



/// A C-compatible `struct` used for passing arrays across the FFI boundary
typedef struct Array {
    void const* data;
    size_t len;
} Array;

Array decode_polyline_ffi(char const* pl, int precision);

char* encode_coordinates_ffi(Array coords, int precision);

void drop_float_array(Array arr);

void drop_cstring(char* p);

#ifdef __cplusplus
}
#endif


#endif
