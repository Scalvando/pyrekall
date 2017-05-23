import rekall.obj
import json
import abc


class AbstractWrapper(object):
    __metaclass__ = abc.ABCMeta

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v

    def __repr__(self):
        return self.__str__()

    def unwrap(self, k, v):
        if v is None:
            return v

        elif isinstance(v, (unicode, rekall.plugins.overlays.basic.String)) or \
                        v.__class__.__name__ in ['UNICODE_STRING', '_UNICODE_STRING']:
            return self.unwrap(k, str(v))

        elif str(v) in ['', '-'] or isinstance(v, rekall.obj.NoneObject):
            return None

        elif isinstance(v, rekall.plugins.overlays.basic.WinFileTime):
            return v.as_arrow().timestamp

        elif v.__class__.__name__ == "Hash":
            return format(int(v.Value, 16), 'x')

        return v

    def as_json(self, fp=None, indent=4, sort_keys=True):
        d = dict((k, v) for k, v in self if not k.startswith('_'))
        if fp:
            json.dump(d, indent=indent, sort_keys=sort_keys)
        else:
            return json.dumps(d)