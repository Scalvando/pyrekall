import pyrekall.models.common

class SSDT(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent system service descriptors.
    """

    def __init__(self, ssdt):
        super(SSDT, self).__init__()
        
        self.entry = hex(ssdt['entry'])
        self.target = hex(ssdt['target'])
        self.symbol = str(ssdt['symbol'])

    def summary(self):
        return {
           'entry': self.entry,
           'target': self.target,
           'symbol': self.symbol
        }
