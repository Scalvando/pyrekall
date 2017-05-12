import pyrekall.models.common
import pyrekall.helpers.usability


class Dll(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent the Dynamic Link Library (DLL) dependencies of a given process
    """
    def __init__(self, dll):
        super(Dll, self).__init__()

        self.name = str(dll.BaseDllName)
        self.path = str(dll.FullDllName)
        self.base = hex(dll.DllBase)
        self.size = pyrekall.helpers.usability.sizeof_fmt(dll.SizeOfImage)

    def summary(self):
        summary = {
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'base': self.base,
        }
        if self.flags['human_readable']:
            summary['size'] = pyrekall.helpers.usability.sizeof_fmt(summary['size'])
        return summary