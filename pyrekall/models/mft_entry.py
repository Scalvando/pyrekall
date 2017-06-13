import pyrekall.models.common

class MFTEntry(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent MFT entries.
    """

    def __init__(self, mft_entry):
        super(MFTEntry, self).__init__()

        self.mft = mft_entry['MFT']
        #self.mft_entry = str(mft_entry['mft_entry'])
        self.file_modified = mft_entry['file_modified'].as_datetime().isoformat() or None
        self.mft_modified = mft_entry['mft_modified'].as_datetime().isoformat() or None
        self.access = mft_entry['access'].as_datetime().isoformat() or None
        self.create_time = mft_entry['create_time'].as_datetime().isoformat() or None
        self.name = str(mft_entry['Name'])

    def summary(self):
        return {
            'mft': self.mft,
            #'mft_entry': self.mft_entry,
            'file_modified': self.file_modified,
            'mft_modified': self.mft_modified,
            'access': self.access,
            'creation_time': self.create_time,
            'name': self.name
        }