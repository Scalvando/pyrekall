import pyrekall.models.common
import pyrekall.helpers.usability
from rekall import utils

class Driver(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent drivers.
    """

    def __init__(self, driver):
        super(Driver, self).__init__()

        self.allocated = driver['a']
        self.physical_offset = hex(driver['offset'])
        self.ptr_count = int(driver['ptr_no'])
        self.hnd_count = int(driver['hnd_no'])
        self.driver_start = hex(driver['start'])
        self.size = pyrekall.helpers.usability.sizeof_fmt(driver['size'])
        self.service_key = utils.SmartStr(driver['servicekey'])
        self.name = utils.SmartStr(driver['name'])
        self.path = utils.SmartStr(driver['path'])

    def summary(self):
        return {
            'allocated': self.allocated,
            'offset': self.physical_offset,
            'pointer_count': self.ptr_count,
            'handle_count': self.hnd_count,
            'driver_start': self.driver_start,
            'size': self.size,
            'service_key': self.service_key,
            'name': self.name,
            'path': self.path
        }
