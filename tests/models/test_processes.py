from pyrekall.models.processes import Process
from pyrekall.models.sample import Sample
from pyrekall.models.executable import PE

import unittest
import os


class MockSample(Sample):
    def __init__(self, path):
        super(MockSample, self).__init__(path=path)

    def _compute_checksums(self):
        self._md5 = "9fb971822dcb393f930227c8854f7679"
        self._sha1 = "6783d95883a32762042cae731887ae3693b030c1"
        self._sha256 = "5f19ff1333fc3901fbf3fafb50d2adb0c495cf6d33789e5a959499a92aeefe77"


class ProcessTestCases(unittest.TestCase):
    _multiprocess_can_split_ = True

    filename = os.path.join(os.path.dirname(__file__), "../../samples/stuxnet.vmem")
    sample = MockSample(path=filename)
    process = sample.get_process_by_name("lsass.exe")

    def test_name(self):
        self.assertEqual("lsass.exe", self.process.name)

    def test_pid(self):
        self.assertEqual(680, self.process.pid)

    def test_ppid(self):
        self.assertEqual(624, self.process.ppid)

    def test_number_of_handles(self):
        self.assertEqual(342, self.process.number_of_handles)

    def test_number_of_active_threads(self):
        self.assertEqual(19, self.process.number_of_active_threads)

    def test_path(self):
        self.assertEqual("C:\\WINDOWS\\system32\\lsass.exe", self.process.path)

    def test_command_line(self):
        self.assertEqual("C:\\WINDOWS\\system32\\lsass.exe", self.process.command_line)

    def test_current_directory(self):
        self.assertEqual("C:\\WINDOWS\\system32\\", self.process.current_directory)

    def test_dll_path(self):
        self.assertEqual('C:\\WINDOWS\\system32;C:\\WINDOWS\\system32;C:\\WINDOWS\\system;C:\\WINDOWS;.;C:\\Perl\\'
                         'site\\bin;C:\\Perl\\bin;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\'
                         'Python26;C:\\Program Files\\TortoiseSVN\\bin', self.process.dll_path)

    def test_create_time(self):
        self.assertEqual(1288372134, self.process.create_time)

    def test_exit_time(self):
        self.assertEqual(None, self.process.exit_time)

    def test_virtual_offset(self):
        self.assertEqual(2179399712L, self.process.virtual_offset)

    def test_physical_offset(self):
        self.assertEqual(34013216L, self.process.physical_offset)

    def test_address_space_initialized(self):
        self.assertEqual(True, self.process.address_space_initialized)

    def test_has_address_space(self):
        self.assertEqual(True, self.process.has_address_space)

    def test_sub_system_major_version(self):
        self.assertEqual(4, self.process.sub_system_major_version)

    def test_sub_system_minor_version(self):
        self.assertEqual(0, self.process.sub_system_minor_version)

    def test_sub_system_version(self):
        self.assertEqual(1024, self.process.sub_system_version)

    def test_parent(self):
        self.assertTrue(isinstance(self.process, Process))
        self.assertTrue(isinstance(self.process.parent, Process))
        self.assertEqual(self.process.ppid, self.process.parent.pid)

    def test_children(self):
        p = self.sample.get_process_by_name("services.exe")
        self.assertTrue(isinstance(p, Process))
        self.assertTrue(isinstance(p.children, list))
        self.assertEqual(14, len(p.children))

        expected = {1664, 868, 1032, 940, 844, 1816, 1200, 1080, 1928, 756, 856, 1412, 188, 1580}
        results = set(map(lambda p: p.pid, p.children))
        self.assertEqual(expected, results)

    def test_environment_variables(self):
        e = self.process.get_environment_variables()
        self.assertTrue(isinstance(e, dict))
        self.assertEqual(21, len(e))

        expected = {'FP_NO_HOST_CHECK', 'TMP', 'COMPUTERNAME', 'ComSpec', 'TEMP', 'windir', 'VS100COMNTOOLS',
                        'SystemDrive', 'PROCESSOR_ARCHITECTURE', 'NUMBER_OF_PROCESSORS', 'CommonProgramFiles',
                        'ALLUSERSPROFILE', 'PROCESSOR_IDENTIFIER', 'PROCESSOR_LEVEL', 'ProgramFiles',
                        'PROCESSOR_REVISION', 'PATHEXT', 'SystemRoot', 'USERPROFILE', 'OS', 'Path'}

        results = set(e.keys())
        self.assertEqual(expected, results)

    def test_get_executable(self):
        e = self.process.get_executable()
        self.assertTrue(isinstance(e, PE))