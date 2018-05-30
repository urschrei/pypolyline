
#ifndef cheddar_generated_my_header_h
#define cheddar_generated_my_header_h


#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

typedef struct Array {
    void const* data;
    size_t len;
} Array;

Array decode_polyline_ffi(char const* pl, uint32_t precision);

char* encode_coordinates_ffi(Array coords, uint32_t precision);

void drop_float_array(Array arr);

void drop_cstring(char* p);

#ifdef __cplusplus
}
#endif


#endif
