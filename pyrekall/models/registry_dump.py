import pyrekall.models.common


class RegistryDump(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent registry keys.
    """

    def __init__(self, session):
        super(RegistryDump, self).__init__()

        self.session = session
        self.keys = []
    
    def dump(self, key):
        #For this level of the registry get the details for the current key
        key_entry = {}
        key_entry['last_write'] = key.LastWriteTime.as_datetime().isoformat() or None
        key_entry['name'] = str(key.Name)
        values = []
        #For all the values associated with the key, put them in a dictionary
        for value in key.values():
            value_entry = {}
            value_entry['type'] = value.Type
            #Attempt to extract the data as plain text - This may need to be done as
            #base64 for compatibility reasons with JSON
            data = value.DecodedData
            if isinstance(data, basestring)
            except:
                try:
                    value_data = value.value().decode('utf-16').encode('utf-8')
                except:
                    value_data = " ".join(["%02X" % (ord(c)) for c in value.raw_data()])

            value_entry['data'] = value_data

            value_entry['name'] = value.name()
            values.append(value_entry)

        key_entry['values'] = values
        keys.append(key_entry)
        #Spider through the subkeys
        for subkey in key.subkeys():
            dump(subkey)


    def summary(self):
        return {
            
        }