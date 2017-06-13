import pyrekall.models.common


class SymLink(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a Symbolic Link Object
    """
    def __init__(self, symlink):
        super(SymLink, self).__init__()

        self.a = str(symlink['a'])
        self.from_link = str(symlink['from_link'])
        self.to_link = str(symlink['to_link'])
        self.ptr_no = int(symlink['ptr_no'])
        self.creation_time = symlink['creation_time'].as_datetime().isoformat() or None
        self.hnd_no = int(symlink['hnd_no'])
        self.offset = format(symlink['offset'], 'X')

    def summary(self):
        summary = {
            'allocated': self.a,
            'physical_offset': self.offset,
            'number_of_pointers': self.ptr_no,
            'number_of_handles': self.hnd_no,
            'creation_time': self.creation_time,
            'from': self.from_link,
            'to': self.to_link
        }
        return summary