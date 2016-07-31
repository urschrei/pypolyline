Fast Google Polyline Encoding and Decoding
==========================================

Installation
------------

``pip install pypolyline``

Please use a recent (>= 8.1.2) version of ``pip``.

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~


- Python 2.7 (\*nix and Windows)
- Python 3.4 (Windows)
- Python 3.5 (\*nix)

Supported Platforms
~~~~~~~~~~~~~~~~~~~


-  Linux (``manylinux1``-compatible)
-  OS X
-  Windows 32-bit / 64-bit

Usage
-----

.. code-block:: python

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

Attempts to decode an invalid Polyline will throw ``util.DecodingError``

Attempts to encode invalid coordinates will throw ``util.EncodingError``


Cython Module
-------------

If you're comfortable with a lack of built-in exceptions, you may
use the compiled Cython version of the functions, instead, giving a
2x speedup over the ``ctypes`` functions:

.. code-block:: python

    from pypolyline.cutil import encode_coordinates, decode_polyline

-  Longitude errors will return strings beginning with ``Longitude error:``
-  Latitude errors will return strings beginning with ``Latitude error:``
-  Polyline errors will return ``[[nan, nan]]``

How it Works
------------

FFI and a
`Rust binary <https://github.com/urschrei/polyline-ffi>`_

Is It Fast
----------

| …Yes.
| You can verify this by installing the ``polyline`` and ``cgpolyencode`` packages, then running ``benchmarks.py``.
| 
| The C++ version runs around **18x** faster than the pure Python version.
| The Rust + Cython version runs around **54x** faster than the pure Python version.

License
-------

`MIT <license.txt>`_
