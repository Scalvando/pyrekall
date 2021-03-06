import pyrekall.models.common
from rekall import utils

class RegistryDump(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent registry keys.
    """

    def __init__(self, session):
        super(RegistryDump, self).__init__()

        self.session = session
        self.keys = []

    def get_keys(self):
        for reg, key in self.session.plugins.printkey().list_keys():
            self._get_key(reg, key)

        return self.keys

    def _get_key(self, reg, key):
        #For this level of the registry get the details for the current key
        key_entry = {}
        key_entry['last_write'] = key.LastWriteTime.as_datetime().isoformat() or None
        key_entry['name'] = utils.SmartStr(key.Name)
        key_entry['path'] = utils.SmartStr(key.Path)
        key_entry['hive'] = str(reg.Name).split(" @ ")[0].strip()
        key_entry['hive_offset'] = str(reg.Name).split(" @ ")[1].strip()
        values = []
        #For all the values associated with the key, put them in a dictionary
        for value in key.values():
            value_entry = {}
            value_entry['name'] = str(value.Name)
            value_entry['type'] = str(value.Type)
            #Attempt to extract the data as plain text - This may need to be done as
            #base64 for compatibility reasons with JSON
            if value.Type == 'REG_BINARY':
                data = value.DecodedData
                if isinstance(data, basestring):
                    value_entry['value'] = " ".join(["{0:02X}".format(ord(x)) for x in data])
            else:
                    value_entry['value'] = utils.SmartStr(value.DecodedData).replace("\x00","")

            values.append(value_entry)
        
        if len(values) == 0:
            values = None
        key_entry['values'] = values
        self.keys.append(key_entry)
        #Spider through the subkeys
        for subkey in key.subkeys():
            self._get_key(reg, subkey)


    def summary(self):
        return self.get_keys()