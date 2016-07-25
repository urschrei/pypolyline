from sys import version_info
import unittest
from pypolyline.util import encode_coordinates, decode_polyline
from pypolyline.native_numpy import decode_polyline as decode_polyline_np

class PolylineTests(unittest.TestCase):
    """ Tests for py_polyline """

    def setUp(self):
        """ make these available to all tests """
        self.coords = [
            [52.64125, 23.70162],
            [52.64938, 23.70154],
            [52.64957, 23.68546],
            [52.64122, 23.68549],
            [52.64125, 23.70162]
            ]


        if (version_info > (3, 0)):
            self.py3 = True
        else:
            self.py3 = False

        if not self.py3:
            self.polyline = u'ynh`IcftoCyq@Ne@ncBds@EEycB'.encode('utf8')
        else:
            self.polyline = 'ynh`IcftoCyq@Ne@ncBds@EEycB'.encode('utf8')


    def testDecodePolyline(self):
        """ Test that Polylines can be decoded """
        expected = self.coords
        result = decode_polyline(self.polyline, 5)
        self.assertEqual(result, expected)

    def testDecodePolylineNumpy(self):
        """ Test that Polylines can be decoded (NumPy) """
        expected = self.coords
        result = decode_polyline_np(self.polyline, gmaps=True)
        self.assertEqual(result, expected)

    def testEncodeCoordinates(self):
        """ Test that coordinates can be encoded """
        expected = self.polyline 
        result = encode_coordinates(self.coords, 5)
        self.assertEqual(result, expected)
