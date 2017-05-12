import pyrekall.models.common


class Connection(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent connections. This class should be expanded to include the process associated with a
    particular connection.
    """

    def __init__(self, connection):
        super(Connection, self).__init__()

        self.offset = connection[0]
        self.protocol = connection[1]
        self.local_addr = connection[2]
        self.remote_addr = connection[3]
        self.state = connection[4]
        self.pid = connection[5]
        self.owner = connection[6]
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
