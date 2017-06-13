import pyrekall.models.common


class ImportFunc(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a Imported Function
    """
    def __init__(self, iat, func, mod_name, func_name):
        super(ImportFunc, self).__init__()

        self.iat = format(iat,'X')
        self.call = format(func, 'X')
        self.module = str(mod_name)
        self.function = str(func_name)

    def summary(self):
        summary = {
            'iat': self.iat,
            'call': self.call,
            'module': self.module,
            'function': self.function
        }
        return summary