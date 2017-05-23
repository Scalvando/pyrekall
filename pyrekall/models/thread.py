import pyrekall.models.common

class Thread(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent threads.
    """

    def __init__(self, thread):
        super(Thread, self).__init__()

        self.offset = hex(thread[0])
        self.pid = int(thread[1])
        self.tid = int(thread[2])
        self.start_address = hex(thread[3])
        self.create_time = thread[4].as_datetime().isoformat() or None
        self.exit_time = thread[5].as_datetime().isoformat() or None
        self.process = str(thread[6])
        self.symbol = str(thread[7])

    def summary(self):
        return {
            'offset': self.offset,
            'pid': self.pid,
            'tid': self.tid,
            'start_address': self.start_address,
            'created': self.create_time,
            'exited': self.exit_time,
            'process': self.process,
            'symbol': self.symbol
        }
