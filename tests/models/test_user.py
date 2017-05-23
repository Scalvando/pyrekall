from pyrekall.models.sample import Sample

import unittest
import os


class MockSample(Sample):
    def __init__(self, path):
        super(MockSample, self).__init__(path=path)

    def _compute_checksums(self):
        self._md5 = "9fb971822dcb393f930227c8854f7679"
        self._sha1 = "6783d95883a32762042cae731887ae3693b030c1"
        self._sha256 = "5f19ff1333fc3901fbf3fafb50d2adb0c495cf6d33789e5a959499a92aeefe77"


class UserTestCases(unittest.TestCase):
    filename = os.path.join(os.path.dirname(__file__), "../../samples/stuxnet.vmem")
    sample = MockSample(path=filename)

    def setUp(self):
        self.user = self.sample.get_users()[0]

    def test_key(self):
        self.assertEqual("SAM/SAM/Domains/Account/Users/000001F4", self.user.key)

    def test_name(self):
        self.assertEqual("Administrator", self.user.name)

    def test_full_name(self):
        self.assertEqual(None, self.user.full_name)

    def test_type(self):
        self.assertEqual("Default Admin User", self.user.type)

    def test_comment(self):
        self.assertEqual("Built-in account for administering the computer/domain", self.user.comment)

    def test_account_expiration(self):
        self.assertEqual(None, self.user.account_expiration)

    def test_password_failed_time(self):
        self.assertEqual(1288372136, self.user.password_failed_time)

    def test_password_reset_date(self):
        self.assertEqual(1282484066, self.user.password_reset_date)

    def test_last_login_time(self):
        self.assertEqual(1288372307, self.user.last_login_time)

    def test_login_count(self):
        self.assertEqual(7, self.user.login_count)

    def test_failed_login_count(self):
        self.assertEqual(0, self.user.failed_login_count)

    def test_flags(self):
        expected = ['Password does not expire', 'Normal user account']
        self.assertEqual(expected, self.user.flags)

    def test_rid(self):
        self.assertEqual(500, self.user.rid)