import unittest
import pyrekall.helpers.files


class TestFilesHelper(object):

    def test_set_file_extension(self):
        for path, extension, result in [
            ('42.tar.gz', 'txt', '42.txt'),
            ('42.tar.gz', '.txt', '42.txt'),
            ('/home/rick/42.tar', 'txt', '/home/rick/42.txt'),
            ('/home/astley/42.tar', '.txt', '/home/astley/42.txt'),
        ]:
            yield self.set_file_extension, path, extension, result

    def set_file_extension(self, path, extension, expected):
        result = pyrekall.helpers.files.set_extension(path=path, extension=extension)
        assert expected == result, "Expected %s got %s" % (expected, result)