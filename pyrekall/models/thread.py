import pyrekall.models.common

from rekall import utils 

class Thread(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent threads.
    """

    def __init__(self, thread):
        super(Thread, self).__init__()

        self.offset = format(thread[0], 'X')
        self.pid = int(thread[1])
        self.tid = int(thread[2])
        self.start_address = format(thread[3], 'X')
        self.create_time = thread[4].as_datetime().isoformat() or None
        self.exit_time = thread[5].as_datetime().isoformat() or None
        self.process = utils.SmartStr(thread[6])

    def summary(self):
        return {
            'physical_offset': self.offset,
            'pid': self.pid,
            'thread_id': self.tid,
            'start_address': self.start_address,
            'creation_time': self.create_time,
            'exit_time': self.exit_time,
            'process_name': self.process
        }
