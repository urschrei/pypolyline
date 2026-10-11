# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-11

### Changed

- **Breaking:** a `precision` other than `5` or `6` now raises `ValueError`. Previously, `encode_coordinates` returned the error message `b"Bad precision parameter supplied"` as though it were an encoded Polyline, and `decode_polyline` raised `RuntimeError`.
- **Breaking:** `precision` must be an `int`. Passing a `float` (e.g. `5.0`) now raises `TypeError`.
- **Breaking:** coordinates passed to `encode_coordinates` must have shape `(N, 2)`, and anything else raises `ValueError`. Previously, an `(N, 3)` input was silently misread, producing an incorrect Polyline.
- **Breaking:** coordinates must be numbers. Numeric strings such as `"1.0"` are no longer converted, and raise `ValueError`.
- The `RuntimeError` raised when coordinates cannot be encoded now has a plain message, e.g. `latitude out of bounds: 95 at position 0`, instead of the `repr` of a bytes object, e.g. `b'latitude out of bounds: 95 at position 0'`.
- Passing something other than `bytes` or `str` to `decode_polyline` raises `TypeError` with the message `polyline must be bytes or str, not <type>`.
- The extension is now built from the Rust [polyline](https://crates.io/crates/polyline) crate using [PyO3](https://pyo3.rs) and [maturin](https://www.maturin.rs), replacing the Cython wrapper around the prebuilt [polyline-ffi](https://github.com/urschrei/polyline-ffi) library. The wheel no longer bundles a separate shared library.
- The GIL is released while encoding and decoding.
- Encoding and decoding are faster, especially for small inputs and for lists of coordinates.
- Wheels target the CPython Stable ABI (`abi3`): a single wheel per platform covers CPython 3.11 and later.

### Added

- `decode_polyline` accepts a `str` as well as `bytes`.
- `encode_coordinates` accepts any `(N, 2)` float64 object that supports the buffer protocol, in any memory layout, including Fortran-ordered and strided NumPy arrays.
- Type stubs, with a `py.typed` marker ([PEP 561](https://peps.python.org/pep-0561/)).
- The source distribution can now be built and installed on platforms without a prebuilt wheel, given a Rust toolchain.
- The extension module declares support for free-threaded CPython builds.

### Removed

- **Breaking:** support for Python 3.10.
- NumPy is no longer a runtime dependency.

### Fixed

- `decode_polyline(b"", precision)` returns `[]`, instead of raising a `ValueError` about an invalid array shape.

## [0.5.8] and earlier

See the [commit history](https://github.com/urschrei/pypolyline/commits/v0.5.8).

[1.0.0]: https://github.com/urschrei/pypolyline/compare/v0.5.8...v1.0.0
[0.5.8]: https://github.com/urschrei/pypolyline/releases/tag/v0.5.8
