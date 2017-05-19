import pyrekall.models.common
import pyrekall.helpers.usability


class SymLink(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent a Symbolic Link Object
    """
    def __init__(self, symlink):
        super(SymLink, self).__init__()

        self.a = str(symlink['a'])
        self.from_link = str(symlink['from_link'])
        self.to_link = str(symlink['to_link'])
        self.ptr_no = str(symlink['ptr_no'])
        self.creation_time = str(symlink['creation_time'])
        self.hnd_no = str(symlink['hnd_no'])
        self.offset = str(symlink['offset'])

    def summary(self):
        summary = {
            'a': self.a,
            'from_link': self.from_link,
            'to_link': self.to_link,
            'ptr_no': self.ptr_no,
            'creation_time': self.creation_time,
            'hnd_no': self.hnd_no,
            'offset': self.offset,

        }
        return summary