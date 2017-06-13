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
        self.physical_offset = format(driver['offset'], 'X')
        self.ptr_count = int(driver['ptr_no'])
        self.hnd_count = int(driver['hnd_no'])
        self.driver_start = format(driver['start'], 'X')
        self.size = pyrekall.helpers.usability.sizeof_fmt(driver['size'])
        self.service_key = utils.SmartStr(driver['servicekey'])
        self.name = utils.SmartStr(driver['name'])
        self.path = utils.SmartStr(driver['path'])

    def summary(self):
        return {
            'allocated': self.allocated,
            'physical_offset': self.physical_offset,
            'number_of_pointers': self.ptr_count,
            'number_of_handles': self.hnd_count,
            'start_address': self.driver_start,
            'size': self.size,
            'service_key': self.service_key,
            'name': self.name,
            'path': self.path
        }
