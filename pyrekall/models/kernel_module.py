import pyrekall.models.common
import pyrekall.helpers.usability

from rekall import utils

class KernelModule(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent loaded kernel modules.
    """

    def __init__(self, kernel_module):
        super(KernelModule, self).__init__()
        
        module = kernel_module['_LDR_DATA_TABLE_ENTRY']
        self.entry_point = hex(module.EntryPoint)
        self.load_count = int(module.LoadCount)
        self.name = utils.SmartStr(kernel_module['name'])
        self.base = hex(kernel_module['base'])
        self.size = pyrekall.helpers.usability.sizeof_fmt(kernel_module['size'])
        self.path = utils.SmartStr(kernel_module['path'])

    def summary(self):
        return {
            'entry_point': self.entry_point,
            'load_count': self.load_count,
            'name': self.name,
            'base': self.base,
            'size': self.size,
            'path': self.path
        }