import pyrekall.models.common

from rekall import utils

class UnlinkedDLL(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent unlinked DLLs.
    """

    def __init__(self, unlinked_dll):
        super(UnlinkedDLL, self).__init__()

        process = unlinked_dll['_EPROCESS']
        self.pid = int(process.UniqueProcessId)
        self.process = utils.SmartStr(process.ImageFileName)
        self.base = hex(unlinked_dll['base'])
        self.in_load = unlinked_dll['in_load']
        self.in_load_path = utils.SmartStr(unlinked_dll['in_load_path'])
        self.in_init = unlinked_dll['in_init']
        self.in_init_path = utils.SmartStr(unlinked_dll['in_init_path'])
        self.in_mem = unlinked_dll['in_mem']
        self.in_mem_path = utils.SmartStr(unlinked_dll['in_mem_path'])
        self.mapped_path = utils.SmartStr(unlinked_dll['mapped'])


    def summary(self):
        return {
            'pid': self.pid,
            'process': self.process,
            'base_address': self.base,
            'in_load': self.in_load,
            'in_load_path': self.in_load_path,
            'in_init': self.in_init,
            'in_init_path': self.in_init_path,
            'in_mem': self.in_mem,
            'in_mem_path': self.in_mem_path,
            'mapped_path': self.mapped_path
        }
