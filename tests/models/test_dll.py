import unittest
import pyrekall.models.sample
import json


class TestDllModel(unittest.TestCase):
    _multiprocess_can_split_ = True

    sample = pyrekall.models.sample.Sample(path="samples/stuxnet.vmem")

    def test_summary(self):
        pass

    def test_get_dlls(self):
        expected = {'WSOCK32.dll', 'CLUSAPI.DLL', 'IpHlpApi.dll', 'wzcsvc.dll', 'CSRSRV.dll', 'WINSCARD.DLL'}
        result = set()
        for process in self.sample.get_processes():
            for dll in process.get_dlls():
                result.add(dll.name)
        assert expected.issubset(result), "Expected list of DLLs to contain %s, got %s" % (expected, result)