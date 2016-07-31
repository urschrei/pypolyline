# -*- coding: utf-8 -*-

import unittest
from pypolyline.util import encode_coordinates, decode_polyline, EncodingError, DecodingError
from pypolyline.cutil import encode_coordinates as cencode_coordinates , decode_polyline as cdecode_polyline

class PolylineTests(unittest.TestCase):
    """ Tests for py_polyline """

    def setUp(self):
        """ make these available to all tests """
        self.coords = [
            [38.5, -120.2],
            [40.7, -120.95],
            [43.252, -126.453]
        ]
        try:
            self.polyline = bytes('_p~iF~ps|U_ulLnnqC_mqNvxq`@', 'utf-8')
            self.bad_polyline = bytes('ynh`IcftoCyq@Ne@ncB💀ds@EEycB', 'utf-8')
        except TypeError:
            # python 2
            self.polyline = '_p~iF~ps|U_ulLnnqC_mqNvxq`@'
            self.bad_polyline = 'ynh`IcftoCyq@Ne@ncB💀ds@EEycB'

    def testDecodePolyline(self):
        """ Test that Polylines can be decoded """
        expected = self.coords
        result = decode_polyline(self.polyline, 5)
        for _ in range(100):
            self.assertEqual(result, expected)

    def testEncodeCoordinates(self):
        """ Test that coordinates can be encoded """
        expected = self.polyline 
        result = encode_coordinates(self.coords, 5)
        self.assertEqual(result, expected)

    def testCDecodePolyline(self):
        """ Test that Polylines can be decoded (Cython) """
        expected = self.coords
        result = cdecode_polyline(self.polyline, 5)
        for _ in range(100):
            self.assertEqual(result, expected)

    def testCEncodeCoordinates(self):
        """ Test that coordinates can be encoded (Cython) """
        expected = self.polyline 
        result = cencode_coordinates(self.coords, 5)
        self.assertEqual(result, expected)

    def testBadCoordinates(self):
        """ Test that bad coordinates throw the correct error """
        coords = [[110., 95.], [1., 2.]]
        with self.assertRaises(EncodingError):
            encode_coordinates(coords, 5)

    def testDecodeBadPolyline(self):
        """ Test that bad Polylines throw the correct error """
        with self.assertRaises(DecodingError):
            decode_polyline(self.bad_polyline, 5)
