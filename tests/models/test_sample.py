import unittest
import pyrekall.models.sample
import json


class TestSampleModel(unittest.TestCase):
    _multiprocess_can_split_ = True

    sample = pyrekall.models.sample.Sample(path="samples/stuxnet.vmem")

    def test_sample_summary_is_json_serializable(self):
        try:
            json.dumps(self.sample.summary())
        except ValueError as VE:
            self.fail(VE)

    def test_sample_summary_is_dict(self):
        assert isinstance(self.sample.summary(), dict), "Expected summary object to be a dictionary"

    def test_sample_summary_only_consists_of_primative_types(self):
        acceptable_types = (str, int)
        for k, v in self.sample.summary().items():
            assert isinstance(v, acceptable_types)

    def test_service_sids(self):
        expected = ('S-1-5-80-3615470141-4057994987-1930054357-1444440834-2714780835', 'VMUpgradeHelper')
        results = set(map(lambda x: x, self.sample.get_service_sids()))
        assert expected in results, "Expected %s to be in %s" % (expected, results)

    def test_get_services(self):
        expected = {
            'name': 'WebClient',
            'tag': None,
            'group': u'NetworkProvider\x00',
            'display_name': u'WebClient\x00',
            'object_name': u'NT AUTHORITY\\LocalService\x00',
            'image_path': u'%SystemRoot%\\system32\\svchost.exe -k LocalService\x00',
            'additional_attributes': {},
            'depends_on_groups': [],
            'depends_on_services': [u'MRxDAV'],
            'description':  u'Enables Windows-based programs to create, access, and modify Internet-based files. If '
                            u'this service is stopped, these functions will not be available. If this service is '
                            u'disabled, any services that explicitly depend on it will fail to start.\x00',
            'error_control': 'SERVICE_ERROR_NORMAL',
            'start': 'SERVICE_AUTO_START',
            'type': 'SERVICE_WIN32_SHARE_PROCESS'
        }
        services = {}
        for service in self.sample.get_services():
            services[service.name] = service.summary()

        assert expected['name'] in services.keys(), "Expected %s, got %s" % (expected['name'], services.keys())
        assert expected == services[expected['name']], "Expected %s to be in list of service summaries" % expected