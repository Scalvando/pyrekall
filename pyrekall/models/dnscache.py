import pyrekall.models.common


class DnsCache(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a DNS Cache Record
    """
    def __init__(self, dns, parentRecord):
        super(DnsCache, self).__init__()

        self.name = str(dns['Name'])
        self.type = str(dns['type'])
        self.data = str(dns['data'] if 'data' in dns else '')
        self.record = format(dns['record'].obj_offset, 'X')
        self.parent = format(parentRecord.obj_offset, 'X') if parentRecord is not None else None

    def summary(self):
        summary = {
            'name': self.name,
            'type': self.type,
            'data': self.data,
            'record': self.record,
            'parent': self.parent
        }
        return summary