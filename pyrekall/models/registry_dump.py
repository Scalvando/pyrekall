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
        key_entry['hive'] = utils.SmartStr(reg.Name)
        values = []
        #For all the values associated with the key, put them in a dictionary
        for value in key.values():
            value_entry = {}
            value_entry['name'] = utils.SmartStr(value.Name)
            value_entry['type'] = utils.SmartStr(value.Type)
            #Attempt to extract the data as plain text - This may need to be done as
            #base64 for compatibility reasons with JSON
            if value.Type == 'REG_BINARY':
                data = value.DecodedData
                if isinstance(data, basestring):
                    value_entry['data'] = " ".join(["{0:02X}".format(ord(x)) for x in data])
            elif value.Type == 'REG_MULTI_SZ':
                value_entry['value'] = [utils.SmartStr(v) for v in value.DecodedData if v != '']
            else:
                try:
                    value_entry['data'] = unicode(utils.SmartStr(value.DecodedData).replace("\x00", ""), "utf-8")
                except:
                    value_entry['data'] = " ".join(["{0:02X}".format(ord(x)) for x in value.DecodedData])

            values.append(value_entry)
        
        key_entry['number_of_values'] = len(values)
        
        key_entry['values'] = values
        self.keys.append(key_entry)
        #Spider through the subkeys
        for subkey in key.subkeys():
            self._get_key(reg, subkey)


    def summary(self):
        return self.get_keys()
