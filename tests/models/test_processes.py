import unittest
import pyrekall.models.sample
import json


class TestProcessModel(unittest.TestCase):
    _multiprocess_can_split_ = True

    sample = pyrekall.models.sample.Sample(path="samples/stuxnet.vmem")

    def test_summary(self):
        pass

    def test_list_running_processes(self):
        expected = {'System', 'alg.exe', 'ipconfig.exe', 'TSVNCache.exe', 'smss.exe', 'csrss.exe', 'winlogon.exe',
                    'Procmon.exe', 'services.exe', 'lsass.exe', 'imapi.exe', 'vmacthlp.exe', 'svchost.exe', 'lsass.exe',
                    'svchost.exe', 'cmd.exe', 'wuauclt.exe', 'svchost.exe', 'svchost.exe', 'explorer.exe',
                    'svchost.exe', 'VMwareUser.exe', 'spoolsv.exe', 'jqs.exe', 'vmtoolsd.exe', 'jusched.exe',
                    'VMUpgradeHelper', 'wmiprvse.exe', 'VMwareTray.exe', 'lsass.exe', 'wscntfy.exe'}
        result = set(map(lambda x: x.name, self.sample.get_processes()))
        assert expected == result, "Expected list of running processes to be %s, got %s" % (expected, result)

    def test_process_children(self):
        expected = [976, 2040]
        result = list(
            map(lambda p: p.pid, self.sample.get_process_by_pid(1032).children)
        )
        assert expected == result, "Expected %s, got %s" % (expected, result)

    def test_process_parent(self):
        expected = 968
        result = self.sample.get_process_by_pid(304).parent.pid
        assert expected == result, "Expected %s, got %s" % (expected, result)