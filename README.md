![example workflow](https://github.com/urschrei/pypolyline/actions/workflows/wheels.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/urschrei/pypolyline/badge.svg?branch=master)](https://coveralls.io/github/urschrei/pypolyline?branch=master) [![Downloads](https://pepy.tech/badge/pypolyline)](https://pepy.tech/project/pypolyline)[![DOI](https://zenodo.org/badge/63355673.svg)](https://zenodo.org/badge/latestdoi/63355673)

# Fast Google [Polyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm) Encoding and Decoding

# Installation
`uv add pypolyline`  
`pip install pypolyline`  

## Installing for local development
1. Ensure you have a [Rust toolchain](https://rustup.rs) installed
2. run `uv sync --dev` (this builds the extension using [maturin](https://www.maturin.rs))
3. run `uv run pytest`

Changes to `Cargo.toml`, `Cargo.lock`, or any `.rs` file will bust the cache, triggering a rebuild when `uv` commands are run.

## Supported Python Versions
All [_currently_ supported Python versions](https://devguide.python.org/versions/).

Binary wheels target the CPython [Stable ABI](https://docs.python.org/3/c-api/stable.html) (`abi3`): a single `abi3` wheel per platform covers CPython 3.11 and later.

### Supported Platforms
- Linux (`manylinux*`-compatible, x86_64 and aarch64)
- macOS (x86_64 and arm64)
- Windows 64-bit

## Usage
Coordinates must be in (`Longitude, Latitude`) order, and can be any sequence of (`x, y`) pairs, or an `(N, 2)` NumPy array (or any other object supporting the buffer protocol). Polylines can be `bytes` or `str`. NumPy is not required.

```python
from pypolyline.cutil import encode_coordinates, decode_polyline

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

## Error Handling
- Failure to encode coordinates, or to decode a supplied Polyline, will raise a `RuntimeError` containing information about the invalid input.
- A precision other than 5 or 6, or coordinates that aren't `(N, 2)`, will raise a `ValueError`.
- A Polyline that isn't `bytes` or `str` will raise a `TypeError`.


## How it Works
[PyO3](https://pyo3.rs) bindings to the Rust [polyline](https://crates.io/crates/polyline) crate. The GIL is released while encoding and decoding.

## Is It Fast
…Yes.  
You can verify this by installing the `polyline` package, then running [`benchmarks.py`](benchmarks.py), a calibrated benchmark using `cProfile`.  
On an M2 MBP, The [pure-Python](https://pypi.org/project/polyline/) test runs in ~2500 ms, the [Flexpolyline](https://pypi.org/project/flexpolyline/) benchmark runs in ~1500 ms and the Rust benchmark runs in around 80 ms (30 x and 17.5 x faster, respectively).

## License
[The Blue Oak Model Licence 1.0.0](LICENCE.md)

## Citing `Pypolyline`
If Pypolyline has been significant in your research, and you would like to acknowledge the project in your academic publication, we suggest citing it as follows (example in APA style, 7th edition):

> Hügel, S. (2021). Pypolyline (Version X.Y.Z) [Computer software]. https://doi.org/10.5281/zenodo.5774925

In Bibtex format:


    @software{Hugel_Pypolyline_2021,
    author = {Hügel, Stephan},
    doi = {10.5281/zenodo.5774925},
    license = {MIT},
    month = {12},
    title = {{Pypolyline}},
    url = {https://github.com/urschrei/simplification},
    version = {X.Y.Z},
    year = {2021}
    }
