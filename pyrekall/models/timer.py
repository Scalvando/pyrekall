import pyrekall.models.common

class Timer(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represents kernel timers and their associated module DPCs.
    """

    def __init__(self, timer):
        super(Timer, self).__init__()
        
        self.table = timer[0]
        self.due_high = timer[2]
        self.due = timer[3].as_datetime().isoformat() or None
        self.period = int(timer[4])
        self.signaled = timer[5]
        self.routine = hex(timer[6])
        self.symbol = str(timer[7])

    def summary(self):
        return {
            'table': self.table,
            'due_high': self.due_high,
            'due': self.due,
            'period': self.period,
            'signaled': self.signaled,
            'routine': self.routine,
            'symbol': self.symbol
        }