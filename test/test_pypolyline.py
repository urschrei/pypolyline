# -*- coding: utf-8 -*-

import unittest
from pypolyline.util import (
    encode_coordinates,
    decode_polyline,
    EncodingError,
    DecodingError,
)
from pypolyline.cutil import (
    encode_coordinates as cencode_coordinates,
    decode_polyline as cdecode_polyline,
)


class PolylineTests(unittest.TestCase):
    """ Tests for py_polyline """

    def setUp(self):
        """ make these available to all tests """
        self.coords = [[-120.2, 38.5], [-120.95, 40.7], [-126.453, 43.252]]
        try:
            self.polyline = bytes("_p~iF~ps|U_ulLnnqC_mqNvxq`@", "utf-8")
            self.bad_polyline = bytes("ynh`IcftoCyq@Ne@ncB💀ds@EEycB", "utf-8")
        except TypeError:
            # python 2
            self.polyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
            self.bad_polyline = "ynh`IcftoCyq@Ne@ncB💀ds@EEycB"

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
        coords = [[110.0, 95.0], [1.0, 2.0]]
        with self.assertRaises(EncodingError):
            encode_coordinates(coords, 5)

    def testDecodeBadPolyline(self):
        """ Test that bad Polylines throw the correct error """
        with self.assertRaises(DecodingError):
            decode_polyline(self.bad_polyline, 5)

    def testLongCoords(self):
        """ Test that round-tripping is OK.
        See https://github.com/urschrei/polyline-ffi/issues/1

        """
        coords = [
            [13.37053, 52.48803],
            [13.37067, 52.48941],
            [13.37073, 52.49048],
            [13.37078, 52.49072],
            [13.37093, 52.49267],
            [13.37628, 52.49158],
            [13.37638, 52.49153],
            [13.37659, 52.49148],
            [13.37659, 52.49148],
            [13.37758, 52.49169],
            [13.37934, 52.49224],
            [13.38273, 52.49335],
            [13.38349, 52.49352],
            [13.38402, 52.49516],
            [13.38521, 52.49849],
            [13.38921, 52.49755],
            [13.38986, 52.49746],
            [13.39063, 52.49739],
            [13.39139, 52.49737],
            [13.39203, 52.4974,],
            [13.39278, 52.49742],
            [13.39486, 52.49761],
            [13.3956, 52.49781],
            [13.39586, 52.49793],
            [13.39593, 52.49812],
            [13.39594, 52.49837],
            [13.39584, 52.49877],
            [13.39574, 52.499],
            [13.39474, 52.50068],
            [13.39461, 52.50094],
            [13.39448, 52.50141],
            [13.39448, 52.50165],
            [13.39451, 52.50186],
            [13.39463, 52.5022,],
            [13.39478, 52.50246],
            [13.39508, 52.50283],
            [13.39543, 52.50319],
            [13.39571, 52.50355],
            [13.39703, 52.50533],
            [13.39712, 52.5055],
            [13.39734, 52.50585],
            [13.39757, 52.50616],
            [13.39775, 52.50635],
            [13.39829, 52.50708],
            [13.39842, 52.5073,],
            [13.39859, 52.50754],
            [13.3991, 52.50819],
            [13.40001, 52.5095],
            [13.40019, 52.50968],
            [13.40099, 52.51031],
            [13.40126, 52.51056],
            [13.40131, 52.51065],
            [13.40134, 52.51082],
            [13.40131, 52.51101],
            [13.40126, 52.51122],
            [13.40142, 52.51125],
            [13.40173, 52.51135],
            [13.4018, 52.51137],
            [13.40231, 52.5116],
            [13.40318, 52.51215],
            [13.40468, 52.51319],
            [13.40582, 52.51402],
            [13.40746, 52.51534],
            [13.40796, 52.51576],
            [13.40894, 52.51653],
            [13.40927, 52.5168],
            [13.41087, 52.51819],
            [13.41141, 52.51858],
            [13.41215, 52.51899],
            [13.41236, 52.51915],
            [13.41256, 52.51927],
            [13.41429, 52.52009],
            [13.4145, 52.52021],
            [13.41468, 52.52033],
            [13.41532, 52.52087],
            [13.41641, 52.52194],
            [13.41802, 52.52341],
            [13.41832, 52.52366],
            [13.4188, 52.52398],
            [13.41996, 52.52498],
            [13.42022, 52.52522],
            [13.41848, 52.52593],
        ]
        s = b"eqj_IylrpAsG[uEKo@IeK]xEm`@HSHi@??i@eEmB_J}EeTa@wCgIiBySmFzD_XPaCLyCBwCE_CCuCe@_Lg@sCWs@e@Mq@AoARm@RoIfEs@X}AXo@?i@EcAWs@]iA{@gAeAgAw@cJgGa@QeAk@}@m@e@c@qCkBk@Yo@a@aCeBeGuDc@c@}B_Dq@u@QIa@Ee@Di@HE_@S}@CMm@eBmBmDoEkHeDcFgGgIsAcByCcEu@aAuG_ImAkBqAsC_@i@Wg@cDyIWi@Wc@kB_CuEyEeHaIq@{@_A_BgEgFo@s@mCzI"
        for _ in range(10000):
            # encode using ctypes and cython
            cencoded = cencode_coordinates(coords, 5)
            encoded = encode_coordinates(coords, 5)
            # decode using ctypes and cython
            cdecoded = cdecode_polyline(cencoded, 5)
            decoded = decode_polyline(encoded, 5)
            # is round-tripping OK
            self.assertEqual(
                decoded, coords,
            )
            self.assertEqual(
                cdecoded, coords,
            )
            # does encoded string match Google's output?
            self.assertEqual(encoded, s)
            self.assertEqual(cencoded, s)
