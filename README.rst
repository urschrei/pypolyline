Fast Google Polyline Encoding and Decoding
==========================================

Installation
------------

``pip install pypolyline``
Please use a recent (>= 8.1.2) version of ``pip``.

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

Python 2.7 Python 3.5

Supported Platforms
~~~~~~~~~~~~~~~~~~~


-  Linux (manylinux1-compatible)
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


How it Works
------------

FFI using ``ctypes`` and a
`Rust binary <https://github.com/urschrei/polyline-ffi>`_

License
-------

`MIT <license.txt>`_
