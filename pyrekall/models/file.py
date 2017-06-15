import pyrekall.models.common
from rekall import utils

class File(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent pooled files.
    """

    def __init__(self, file):
        super(File, self).__init__()

        self.allocated = file['a']
        self.physical_offset = format(file['offset'], 'X')
        self.ptr_count = int(file['ptr_no'])
        self.hnd_count = int(file['hnd_no'])
        self.access = file['access']
        self.pid = int(file['Owner'].UniqueProcessId)
        self.path = utils.SmartStr(file['path'])

    def summary(self):
        return {
            'allocated': self.allocated,
            'physical_offset': self.physical_offset,
            'number_of_pointers': self.ptr_count,
            'number_of_handles': self.hnd_count,
            'file_access': self.access,
            'pid': self.pid,
            'path': self.path
        }
