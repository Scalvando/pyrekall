import unittest
import pyrekall.models.sample
import json


class TestHandleModel(unittest.TestCase):
    _multiprocess_can_split_ = True

    sample = pyrekall.models.sample.Sample(path="samples/stuxnet.vmem")

    def test_summary_is_json(self):
        pass

    def test_process_handles(self):
        handles = set()
        for process in self.sample.get_processes():
            handles.update(set(process.get_handles()))

        types = set(map(lambda x: x.type, handles))
        expected_types = {'WaitablePort', 'Desktop', 'FilterCommunicationPort', 'Semaphore', 'FilterConnectionPort',
                          'Job', 'Key', 'IoCompletion', 'Section', 'Thread', 'Timer', 'Token', 'WmiGuid',
                          'Directory', 'WindowStation', 'Mutant', 'KeyedEvent', 'Process', 'Port', 'File',
                          'SymbolicLink', 'Event'}
        assert expected_types == types, "Expected set of types to match. Expected %s, got %s" % (expected_types, types)

        details = set(map(lambda x: (x.type, x.details), handles))
        expected_details = {
            ('Key', 'MACHINE\\SOFTWARE\\MICROSOFT\\WINDOWS NT\\CURRENTVERSION\\NETWORK\\LOCATION AWARENESS'),
            ('File', '\\Device\\NamedPipe\\TSVNCacheCommand-0000000000029b4c'),
            ('Thread', 'TID 1096 PID 1412'),
        }
        assert details.issuperset(expected_details), "Expected list of details to contain %s, got %s" % (expected_details,
                                                                                                       details)