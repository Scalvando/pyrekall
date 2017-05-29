import pyrekall.models.common
import pyrekall.helpers.usability
from rekall import utils

class ShimCache(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent Shim Cache entries.
    """

    def __init__(self, shimcache):
        super(ShimCache, self).__init__()

        print 
        self.last_modified = shimcache['last_mod'].as_datetime().isoformat() or None
        self.last_update = shimcache['last_update'].as_datetime().isoformat() or None
        if shimcache['size']:
            self.size = pyrekall.helpers.usability.sizeof_fmt(shimcache['size'])
        else:
            self.size = None
        self.path = utils.SmartStr(shimcache['Path'])

    def summary(self):
        return {
            'last_modified': self.last_modified,
            'last_update': self.last_update,
            'size': self.size,
            'path': self.path
        }
