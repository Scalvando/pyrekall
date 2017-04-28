import unittest
import pyrekall.helpers.crypto


class TestCryptoHelper(unittest.TestCase):

    def test_md5(self):
        m = "42"
        c1 = 215089739385482443301854222253501995174
        c2 = pyrekall.helpers.crypto.md5(m)
        assert c1 == c2, "%s != %s" % (c1, c2)

    def test_sha1(self):
        m = "42"
        c1 = 838146913046966959093018715372872234545534447190
        c2 = pyrekall.helpers.crypto.sha1(m)
        assert c1 == c2, "%s != %s" % (c1, c2)

    def test_sha256(self):
        m = "42"
        c1 = 52142063543217935108392605932536905068334213121597159393376024684286053089353
        c2 = pyrekall.helpers.crypto.sha256(m)
        assert c1 == c2, "%s != %s" % (c1, c2)