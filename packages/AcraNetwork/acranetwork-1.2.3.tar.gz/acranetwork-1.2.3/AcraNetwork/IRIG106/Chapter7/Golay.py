"""
.. module:: Golay
    :platform: Unix, Windows
    :synopsis: Encode and decode Golay Codes based on IRIG106 Standard http://www.irig106.org/docs/106-17/chapter7.pdf

.. moduleauthor:: Diarmuid Collins <dcollins@curtisswright.com>

"""

__author__ = "Diarmuid Collins"
__copyright__ = "Copyright 2020"
__maintainer__ = "Diarmuid Collins"
__email__ = "dcollins@curtisswright.com"
__status__ = "Production"


# This is a direct porting of the C code from the IRIG106 starndard.
import struct
from functools import lru_cache


GOLAY_SIZE = 0x1000

G_P = [0xC75, 0x63B, 0xF68, 0x7B4, 0x3DA, 0xD99, 0x6CD, 0x367, 0xDC6, 0xA97, 0x93E, 0x8EB]

H_P = [0xA4F, 0xF68, 0x7B4, 0x3DA, 0x1ED, 0xAB9, 0xF13, 0xDC6, 0x6E3, 0x93E, 0x49F, 0xC75]


class Golay:
    """
    Encode and Decode Golay numbers
    """

    def __init__(self):
        self.SyndromeTable = [0] * GOLAY_SIZE
        self.CorrectTable = [0] * GOLAY_SIZE
        self.ErrorTable = [0] * GOLAY_SIZE

    @staticmethod
    @lru_cache()
    def _init_Table():
        EncodeTable = [0] * GOLAY_SIZE
        for x in range(GOLAY_SIZE):
            EncodeTable[x] = x << 12
            for i in range(12):
                if x >> (11 - i) & 1:
                    EncodeTable[x] ^= G_P[i]

        return EncodeTable

    @lru_cache(maxsize=20)
    def encode(self, raw, as_string=False):
        """
        Encode the value as a 24b code

        :type raw: int
        :return: int
        """
        if 0xFFF < raw < 0:
            raise Exception("Converestion of 12b value only")

        EncodeTable = Golay._init_Table()
        encoded = EncodeTable[raw & 0xFFF]
        if as_string:
            return struct.pack(">BH", encoded >> 16, encoded & 0xFFFF)
        else:
            return encoded

    @lru_cache(maxsize=20)
    def decode(self, encoded):
        """
        Decode a 24b number as a golay

        :type encoded: int|bytes
        :param encoded:
        :return:
        """
        if type(encoded) is bytes:
            if len(encoded) != 3:
                raise Exception("String to decode should be 3 bytes")
            (b, w) = struct.unpack(">BH", encoded)
            v = w + (b << 16)
        elif 0xFFFFF < encoded < 0:
            raise Exception("Only supports 24b unsigned numbers")
        else:
            v = encoded

        self._initgolaydecode()
        return self._decode2(((v) >> 12) & 0xFFF, (v) & 0xFFF)

    def _syndrome2(self, v1, v2):
        return self.SyndromeTable[v2] ^ (v1)

    def _syndrome(self, v):
        return self._syndrome2(((v) >> 12) & 0xFFF, (v) & 0xFFF)

    def _errors2(self, v1, v2):
        return self.ErrorTable[self._syndrome2(v1, v2)]

    def _decode2(self, v1, v2):
        return (v1) ^ self.CorrectTable[self._syndrome2(v1, v2)]

    def _errors(self, v):
        return self._errors2(((v) >> 12) & 0xFFF, (v) & 0xFFF)

    @staticmethod
    def _onesincode(code, size):
        """Optimised version of the code below. Runs 2x"""
        return bin(code)[2 : size + 2].count("1")

    @staticmethod
    def _onesincode_old(code, size):
        ret = 0

        for t in range(size):
            if (code >> t) & 1:
                ret += 1

        return ret

    @lru_cache()
    def _initgolaydecode(self):
        for x in range(GOLAY_SIZE):
            self.SyndromeTable[x] = 0
            for i in range(12):
                if (x >> (11 - i)) & 1:
                    self.SyndromeTable[x] ^= H_P[i]
                    self.ErrorTable[x] = 4
                    self.CorrectTable[x] = 0xFFF

        self.ErrorTable[0] = 0
        self.CorrectTable[0] = 0
        for i in range(24):
            for j in range(24):
                for k in range(24):
                    error = (1 << i) | (1 << j) | (1 << k)
                    syndrom = self._syndrome(error)
                    self.CorrectTable[syndrom] = (error >> 12) & 0xFFF
                    self.ErrorTable[syndrom] = Golay._onesincode(error, 24)

        return True
