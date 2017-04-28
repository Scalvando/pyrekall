import pyrekall.models.common


class Handle(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent the handles used by a given process
    """
    def __init__(self, process, handle, details, type):
        super(Handle, self).__init__()

        self.object = handle
        self.process = process

        self.type = str(type)
        self.details = str(details)
        self.handle = hex(handle.HandleValue)
        self.access = hex(handle.GrantedAccess)
        self.pid = int(process.pid)

    def summary(self):
        return {
            'pid': self.pid,
            'handle': self.handle,
            'access': self.access,
            'details': self.details,
            'type': self.type,
        }