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
        for reg, key in self.session.plugins.printkey(recursive=True).list_keys():
            self._get_key(reg, key)

        return self.keys

    def _get_key(self, reg, key):
        #For this level of the registry get the details for the current key
        key_entry = {}
        key_entry['last_write'] = key.LastWriteTime.as_datetime().isoformat() or None
        key_entry['name'] = str(key.Name)
        key_entry['path'] = str(key.Path)
        key_entry['hive'] = str(reg.Name)
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
                    value_entry['value'] = utils.Hexdump(data)
            else:
                try:
                    value_entry['value'] = str(utils.SmartUnicode(value.DecodedData).strip())
                except:
                    value_entry['value'] = utils.SmartUnicode(value.DecodedData).strip()

            values.append(value_entry)

        key_entry['values'] = values
        self.keys.append(key_entry)
        #Spider through the subkeys
        for subkey in key.subkeys():
            self._get_key(reg, subkey)


    def summary(self):
        return {
            'registry': self.get_keys()
        }