import unittest
import pyrekall.helpers.usability


class TestUsabilityHelper(unittest.TestCase):

    def test_sizeof_fmt(self):
        expected = "95.4MiB"
        result = pyrekall.helpers.usability.sizeof_fmt(10**8)
        assert expected == result, "%s != %s" % (expected, result)