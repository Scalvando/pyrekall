import pyrekall.models.common

from rekall import utils

class Connection(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent connections and sockets.
    """

    def __init__(self, connection):
        super(Connection, self).__init__()

        self.offset = hex(connection[0])
        self.protocol = utils.SmartStr(connection[1])
        self.local_addr = utils.SmartStr(connection[2])
        self.remote_addr = utils.SmartStr(connection[3])
        self.state = utils.SmartStr(connection[4])
        self.pid = utils.SmartStr(connection[5])
        self.owner = utils.SmartStr(connection[6])
        self.created = connection[7].as_datetime().isoformat() or None

    def summary(self):
        return {
            'offset': self.offset,
            'protocol': self.protocol,
            'local_addr': self.local_addr,
            'remote_addr': self.remote_addr,
            'state': self.state,
            'pid': self.pid,
            'owner': self.owner,
            'created': self.created
        }
