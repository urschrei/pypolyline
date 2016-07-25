from sys import version_info

def decode_polyline(point_str, gmaps=False):
    """
    Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    
    This is a generic method that returns a list of (lon, lat) 
    tuples, which are used as input to a Shapely LineString
    
    point_str: encoded polyline string
    returns: LineString instance
    """
    # some coordinate offsets are represented by 4 to 5 binary chunks
    if (version_info > (3, 0)):
        py3 = True
    else:
        py3 = False
    if not len(point_str):
        return np.nan
    coord_chunks = [[]]
    for char in point_str:
        # convert each character to decimal from ascii
        if not py3:
            value = ord(char) - 63
        else:
            value = char - 63
        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)   
        value &= 0x1F
        coord_chunks[-1].append(value)
        if split_after:
            coord_chunks.append([])
    del coord_chunks[-1]
    coords = []
    for coord_chunk in coord_chunks:
        coord = 0
        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)
        # there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        # https://github.com/Project-OSRM/osrm-backend/issues/713
        # (OSRM returns higher-precision coordinates)
        # NB this is not the case for Google Directions Polylines
        # they only need coord /= 100000.
        if not gmaps:
            coord /= 1000000.
        else:
            coord /= 100000.
        coords.append(coord)
    # convert the 1d list to a 2d list & offsets to actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue
        prev_x += coords[i + 1]
        prev_y += coords[i]
        # rounding to 6 digits ensures that the floats are the same as when 
        # they were encoded
        points.append([round(prev_y, 6), round(prev_x, 6)])
    if len(points) > 1:
        return points
    else:
        return np.nan
