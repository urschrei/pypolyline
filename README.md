[![Build Status](https://travis-ci.org/urschrei/pypolyline.svg?branch=master)](https://travis-ci.org/urschrei/pypolyline) [![Build status](https://ci.appveyor.com/api/projects/status/0n7d5iwb3uqhsos6/branch/master?svg=true)](https://ci.appveyor.com/project/urschrei/pypolyline/branch/master) [![Coverage Status](https://coveralls.io/repos/github/urschrei/pypolyline/badge.svg?branch=master)](https://coveralls.io/github/urschrei/pypolyline?branch=master)

# Fast Google [Polyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm) Encoding and Decoding

## Installation
`pip install pypolyline`  
Please use a recent (>= 8.1.2) version of `pip`.

### Supported Python Versions
- Python 2.7
- Python 3.6

### Supported Platforms
- Linux (`manylinux1`-compatible)  
- OS X
- Windows 32-bit / 64-bit 

## Usage
```python
from pypolyline.util import encode_coordinates, decode_polyline

coords = [
            [52.64125, 23.70162],
            [52.64938, 23.70154],
            [52.64957, 23.68546],
            [52.64122, 23.68549],
            [52.64125, 23.70162]
         ]

# precision is 5 for Google Polyline, 6 for OSRM / Valhalla
polyline = encode_coordinates(coords, 5)
# polyline is 'ynh`IcftoCyq@Ne@ncBds@EEycB'
decoded_coords = decode_polyline(polyline, 5)
```

Attempts to decode an invalid Polyline will throw `util.EncodingError`  
Attempts to encode invalid coordinates will throw `util.DecodingError`

## Cython Module 🔥
If you're comfortable with a lack of built-in exceptions, you may use the compiled Cython version of the functions, giving a 3x speedup over the `ctypes` functions:
```python
from pypolyline.cutil import encode_coordinates, decode_polyline
```
- Longitude errors will return strings beginning with `Longitude error:`
- Latitude errors will return strings beginning with `Latitude error:`
- Polyline errors will return `[[nan, nan]]`

## How it Works
FFI and a [Rust binary](https://github.com/urschrei/polyline-ffi)

## Is It Fast
…Yes.  
You can verify this by installing the `polyline` and `cgpolyencode` packages, then running [`benchmarks.py`](benchmarks.py), a calibrated benchmark using `cProfile`.  
On a 1.8 GHz Intel Core i7, The pure-Python test runs in ~21 s, the C++ (`cgpolyencode.GPolyEncoder`) test runs in around 600 ms, and The Rust + Cython benchmark runs in around 400 ms (33% faster).

## License
[MIT](license.txt)
