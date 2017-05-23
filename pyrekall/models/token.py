import pyrekall.models.common

class Token(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a process token and the SID that owns them.
    """

    def __init__(self, token):
        super(Token, self).__init__()
        
        process = token[0]
        self.pid = int(process.UniqueProcessId)
        self.process_name = str(process.ImageFileName)
        self.sid = str(token[1])
        self.comment = str(token[2])

    def summary(self):
        return {
           'pid': self.pid,
           'process': self.process_name,
           'sid': self.sid,
           'comment': self.comment
        }
