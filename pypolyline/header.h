
#ifndef cheddar_generated_header_h
#define cheddar_generated_header_h


#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>



/// A C-compatible `struct` used for passing arrays across the FFI boundary
typedef struct _FFIArray {
    void const* data;
    size_t len;
} _FFIArray;


_FFIArray decode_polyline_ffi(char* pl, int precision);

char* encode_coordinates_ffi(_FFIArray coords, int precision);

void drop_float_array(_FFIArray arr);

void drop_cstring(char* p);



#ifdef __cplusplus
}
#endif


#endif
