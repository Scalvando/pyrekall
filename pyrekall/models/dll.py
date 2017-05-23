import pyrekall.models.common
import pyrekall.helpers.usability


class Dll(pyrekall.models.common.AbstractWrapper):
    def __init__(self, dll):
        super(Dll, self).__init__()

        self.name = str(dll.BaseDllName)
        self.path = str(dll.FullDllName)
        self.size = int(dll.SizeOfImage)
        self.base_address = int(dll.DllBase)