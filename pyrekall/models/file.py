import pyrekall.models.common

class File(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent pooled files.
    """

    def __init__(self, file):
        super(File, self).__init__()

        self.allocated = file[0]
        self.physical_offset = hex(file[1])
        self.ptr_count = int(file[2])
        self.hnd_count = int(file[3])
        self.access = file[4]
        self.pid = int(file[5].UniqueProcessId)
        self.path = file[6]

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
