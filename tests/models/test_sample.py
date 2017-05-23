from pyrekall.models.registry import Registry
from pyrekall.models.processes import Process
from pyrekall.models.services import Service
from pyrekall.models.sample import Sample
from pyrekall.models.executable import PE
from pyrekall.models.user import User

import unittest
import os


class MockSample(Sample):
    def __init__(self, path):
        super(MockSample, self).__init__(path=path)

    def _compute_checksums(self):
        self._md5 = "9fb971822dcb393f930227c8854f7679"
        self._sha1 = "6783d95883a32762042cae731887ae3693b030c1"
        self._sha256 = "5f19ff1333fc3901fbf3fafb50d2adb0c495cf6d33789e5a959499a92aeefe77"

    def get_executables(self):
        return list(map(lambda e: e.get_executable(), self.get_processes_by_name("lsass.exe")))


class SampleTestCases(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), "../../samples/stuxnet.vmem")
        self.sample = MockSample(path=self.filename)

    def test__compute_checksums(self):
        self.assertIsNone(self.sample._md5)
        self.assertIsNone(self.sample._sha1)
        self.assertIsNone(self.sample._sha256)

        self.sample._compute_checksums()

        self.assertEqual(self.sample._md5, "9fb971822dcb393f930227c8854f7679")
        self.assertEqual(self.sample._sha1, "6783d95883a32762042cae731887ae3693b030c1")
        self.assertEqual(self.sample._sha256, "5f19ff1333fc3901fbf3fafb50d2adb0c495cf6d33789e5a959499a92aeefe77")

    def test_filename(self):
        self.assertTrue(os.path.exists(self.sample.filename))

    def test_profile(self):
        self.assertIsNone(self.sample._profile, None)
        self.assertIsNotNone(self.sample.profile)
        self.assertIsNotNone(self.sample._profile)

    def test_md5(self):
        self.assertIsNone(self.sample._md5)
        self.sample._compute_checksums()
        self.assertEqual(self.sample._md5, "9fb971822dcb393f930227c8854f7679")

    def test_sha1(self):
        self.assertIsNone(self.sample._sha1)
        self.sample._compute_checksums()
        self.assertEqual(self.sample._sha1, "6783d95883a32762042cae731887ae3693b030c1")

    def test_sha256(self):
        self.assertIsNone(self.sample._sha256)
        self.sample._compute_checksums()
        self.assertEqual(self.sample._sha256, "5f19ff1333fc3901fbf3fafb50d2adb0c495cf6d33789e5a959499a92aeefe77")

    def test_processes(self):
        self.assertIsNone(self.sample._processes)
        processes = self.sample.processes
        self.assertIsNotNone(self.sample._processes)
        self.assertIsInstance(processes, list)
        self.assertEqual(31, len(processes))
        self.assertTrue(all(map(lambda p: isinstance(p, Process), processes)))

    def test_get_processes(self):
        processes = self.sample.get_processes()
        self.assertIsInstance(processes, list)
        self.assertEqual(31, len(processes))
        self.assertTrue(all(map(lambda p: isinstance(p, Process), processes)))

        expected = {'System', 'alg.exe', 'ipconfig.exe', 'TSVNCache.exe', 'smss.exe', 'csrss.exe', 'winlogon.exe',
                    'Procmon.exe', 'services.exe', 'lsass.exe', 'imapi.exe', 'vmacthlp.exe', 'svchost.exe', 'lsass.exe',
                    'svchost.exe', 'cmd.exe', 'wuauclt.exe', 'svchost.exe', 'svchost.exe', 'explorer.exe',
                    'svchost.exe', 'VMwareUser.exe', 'spoolsv.exe', 'jqs.exe', 'vmtoolsd.exe', 'jusched.exe',
                    'VMUpgradeHelper', 'wmiprvse.exe', 'VMwareTray.exe', 'lsass.exe', 'wscntfy.exe'}

        result = set(map(lambda x: x.name, processes))
        self.assertEqual(expected, result)

    def test_get_process_by_name(self):
        process = self.sample.get_process_by_name("lsass.exe")
        self.assertIsInstance(process, Process)
        self.assertEqual(process.name, "lsass.exe")

    def test_get_processes_by_name(self):
        expected = {680, 868, 1928}
        processes = self.sample.get_processes_by_name("lsass.exe")
        results = set(map(
            lambda p: p.pid, processes)
        )
        self.assertTrue(all(map(lambda p: p.name == "lsass.exe", processes)))
        self.assertEqual(expected, results)

    def test_get_process_by_pid(self):
        process = self.sample.get_process_by_pid(680)
        self.assertIsInstance(process, Process)
        self.assertEqual(process.pid, 680)

    def test_get_processes_by_ppid(self):
        expected = {668, 680}
        processes = self.sample.get_processes_by_ppid(624)
        results = set(map(
            lambda p: p.pid, processes)
        )
        self.assertEqual(expected, results)

    def test_get_executables(self):
        executables = self.sample.get_executables()
        self.assertIsInstance(executables, list)
        self.assertEqual(3, len(executables))
        self.assertTrue(all(map(lambda p: isinstance(p, PE), executables)))

    def test_get_all_process_environment_variables(self):
        environment_variables = self.sample.get_all_process_environment_variables()
        self.assertIsInstance(environment_variables, dict)
        self.assertEqual(54, len(environment_variables))

    def test_get_service_sids(self):
        sids = self.sample.get_service_sids()
        self.assertIsInstance(sids, list)
        self.assertEqual(310, len(sids))
        self.assertTrue(all(map(lambda e: isinstance(e[0], str) and isinstance(e[1], str), sids)))

    def test_get_services(self):
        services = self.sample.get_services()
        self.assertIsInstance(services, list)
        self.assertEqual(310, len(services))
        self.assertTrue(all(map(lambda e: isinstance(e, Service), services)))

    def test_get_users(self):
        users = self.sample.get_users()
        self.assertIsInstance(users, list)
        self.assertEqual(5, len(users))
        self.assertTrue(all(map(lambda u: isinstance(u, User), users)))

    def test_get_registry(self):
        registry = self.sample.get_registry()
        self.assertIsInstance(registry, Registry)
