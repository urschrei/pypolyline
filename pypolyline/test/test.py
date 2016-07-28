# -*- coding: utf-8 -*-
import unittest
from pypolyline.util import encode_coordinates, decode_polyline, EncodingError, DecodingError
from pypolyline.native_numpy import decode_polyline as decode_polyline_np

class PolylineTests(unittest.TestCase):
    """ Tests for py_polyline """

    def setUp(self):
        """ make these available to all tests """
        self.coords = [
            [38.5, -120.2],
            [40.7, -120.95],
            [43.252, -126.453]
        ]
        self.polyline = '_p~iF~ps|U_ulLnnqC_mqNvxq`@'

    def testDecodePolyline(self):
        """ Test that Polylines can be decoded """
        expected = self.coords
        result = decode_polyline(self.polyline, 5)
        for _ in range(100):
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

    def testBadCoordinates(self):
        """ Test that bad coordinates return the correct string """
        coords = [[110., 95.], [1., 2.]]
        with self.assertRaises(EncodingError):
            encode_coordinates(coords, 5)

    def testDecodeBadPolyline(self):
        """ Test that Polylines return NaN """
        polyline = 'ynh`IcftoCyq@Ne@ncB💀ds@EEycB'
        with self.assertRaises(DecodingError):
            decode_polyline(polyline, 5)
