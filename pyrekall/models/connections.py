import pyrekall.models.common

from rekall import utils

class Connection(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent connections and sockets.
    """

    def __init__(self, connection):
        super(Connection, self).__init__()

        self.offset = format(connection[0], 'X')
        self.protocol = utils.SmartStr(connection[1])
        laddr = utils.SmartStr(connection[2]).rsplit(':', 1)
        self.local_addr = laddr[0]
        self.local_port = laddr[1]
        raddr = utils.SmartStr(connection[3]).rsplit(':', 1)
        self.remote_addr = raddr[0]
        self.remote_port = raddr[1]
        self.state = utils.SmartStr(connection[4])
        self.pid = int(connection[5])
        self.owner = utils.SmartStr(connection[6])
        self.created = connection[7].as_datetime().isoformat() or None

    def summary(self):
        return {
            'physical_offset': self.offset,
            'protocol': self.protocol,
            'local_address': self.local_addr,
            'local_port': self.local_port,
            'remote_address': self.remote_addr,
            'remote_port': self.remote_port,
            'state': self.state,
            'pid': self.pid,
            'process_name': self.owner,
            'creation_time': self.created
        }
