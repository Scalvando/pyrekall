import pyrekall.models.common
import pyrekall.helpers.usability

class Driver(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent drivers.
    """

    def __init__(self, driver):
        super(Driver, self).__init__()

        self.allocated = driver[0]
        self.physical_offset = hex(driver[1])
        self.ptr_count = int(driver[2])
        self.hnd_count = int(driver[3])
        self.driver_start = hex(driver[4])
        self.size = pyrekall.helpers.usability.sizeof_fmt(driver[5])
        self.service_key = str(driver[6]) or driver[6]
        self.path = str(driver[7]) or driver[7]

    def summary(self):
        return {
            'allocated': self.allocated,
            'physical_offset': self.physical_offset,
            'ptr_count': self.ptr_count,
            'hnd_count': self.hnd_count,
            'driver_start': self.driver_start,
            'size': self.size,
            'service_key': self.service_key,
            'path': self.path
        }
