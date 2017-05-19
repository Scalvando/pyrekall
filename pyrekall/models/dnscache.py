import pyrekall.models.common
import pyrekall.helpers.usability


class DnsCache(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a DNS Cache Record
    """
    def __init__(self, dns):
        super(DnsCache, self).__init__()

        self.name = str(dns['Name'])
        self.type = str(dns['type'])
        self.depth = str(dns['depth'])
        #self.data = str(dns['data'])
        self.record = str(dns['record'])

    def summary(self):
        summary = {
            'name': self.name,
            'type': self.type,
            'depth': self.depth,
            #'data': self.data,
            'record': self.record
        }
        return summary