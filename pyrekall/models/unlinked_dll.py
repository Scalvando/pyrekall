import pyrekall.models.common

class UnlinkedDLL(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent unlinked DLLs.
    """

    def __init__(self, unlinked_dll):
        super(UnlinkedDLL, self).__init__()

        process = unlinked_dll[1]
        self.pid = int(process.UniqueProcessId)
        self.process_name = str(process.ImageFileName)
        self.base_address = hex(unlinked_dll[2])
        self.in_load = unlinked_dll[3]
        self.in_load_path = str(unlinked_dll[4])
        self.in_init = unlinked_dll[5]
        self.in_init_path = str(unlinked_dll[6])
        self.in_mem = unlinked_dll[7]
        self.in_mem_path = str(unlinked_dll[8])
        self.mapped_path = str(unlinked_dll[9])


    def summary(self):
        return {
            'pid': self.pid,
            'process': self.process_name,
            'base_address': self.base_address,
            'in_load': self.in_load,
            'in_load_path': self.in_load_path,
            'in_init': self.in_init,
            'in_init_path': self.in_init_path,
            'in_mem': self.in_mem,
            'in_mem_path': self.in_mem_path,
            'mapped_path': self.mapped_path
        }
