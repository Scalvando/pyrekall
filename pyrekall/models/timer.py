import pyrekall.models.common

from rekall import utils

class Timer(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represents kernel timers and their associated module DPCs.
    """

    def __init__(self, timer):
        super(Timer, self).__init__()
        
        self.table = timer['Tbl']
        self.due = timer['due']
        self.due_time = timer['due_time'].as_datetime().isoformat() or None
        self.period = int(timer['period'])
        self.signaled = timer['sig']
        self.routine = hex(timer['routine'])
        self.symbol = utils.SmartStr(timer['symbol'])

    def summary(self):
        return {
            'table': self.table,
            'due': self.due,
            'due_time': self.due_time,
            'period': self.period,
            'signaled': self.signaled,
            'routine': self.routine,
            'symbol': self.symbol
        }