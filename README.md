# Fast Google Polyline Encoding and Decoding

## Usage

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

## How it Works
FFI using `ctypes` and a [Rust binary](https://github.com/urschrei/polyline-ffi)

## License
[MIT](license.txt)
