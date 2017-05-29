import pyrekall.models.common
from rekall import utils

class File(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent pooled files.
    """

    def __init__(self, file):
        super(File, self).__init__()

        self.allocated = file['a']
        self.physical_offset = hex(file['offset'])
        self.ptr_count = int(file['ptr_no'])
        self.hnd_count = int(file['hnd_no'])
        self.access = file['access']
        self.pid = int(file['Owner'].UniqueProcessId)
        self.path = utils.SmartStr(file['path'])

    def summary(self):
        return {
            'allocated': self.allocated,
            'physical_offset': self.physical_offset,
            'ptr_count': self.ptr_count,
            'hnd_count': self.hnd_count,
            'access': self.access,
            'pid': self.pid,
            'path': self.path
        }
