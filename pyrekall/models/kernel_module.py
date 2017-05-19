import pyrekall.models.common
import pyrekall.helpers.usability

class KernelModule(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent loaded kernel modules.
    """

    def __init__(self, kernel_module):
        super(KernelModule, self).__init__()
        
        module = kernel_module[0]
        self.entry_point = hex(module.EntryPoint)
        self.load_count = int(module.LoadCount)
        self.file_name = str(kernel_module[1])
        self.module_base = hex(kernel_module[2])
        self.module_size = pyrekall.helpers.usability.sizeof_fmt(kernel_module[3])
        self.path = str(kernel_module[4])

    def summary(self):
        return {
            'entry_point': self.entry_point,
            'load_count': self.load_count,
            'file_name': self.file_name,
            'module_base': self.module_base,
            'module_size': self.module_size,
            'path': self.path
        }