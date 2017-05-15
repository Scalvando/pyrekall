import rekall.plugins.overlays.basic
import rekall.obj
import collections
import pprint
import json
import abc


class AbstractWrapper(object):
    """
    This class serves as an abstract wrapper class and should be used by any class which wraps the pyrekall API. In
    doing so, a degree of simplicity is achieved.
    """
    __metaclass__ = abc.ABCMeta

    flags = {
        'human_readable': False,
        'include_dlls': False,
        'include_handles': False
    }

    def post_init(self):
        """
        This method should be executed after the __init__() method of any subclass. The purpose of this method is to
        unravel a subset of the objected used for the purpose of wrapping primitive types within the scope of the
        Google Rekall framework
        """
        for k, v in self.__iter__():
            if isinstance(v, (str, int)):
                continue

            elif v == '' or v == '-' or isinstance(v, rekall.obj.NoneObject):
                v = None

            elif isinstance(v, (unicode, rekall.plugins.overlays.basic.String
            )) or v.__class__.__name__ in ['UNICODE_STRING', '_UNICODE_STRING']:
                v = str(v)

            elif isinstance(v, rekall.plugins.overlays.basic.WinFileTime):
                v = v.as_datetime() or None
                if v:
                    v = v.strftime("%Y-%m-%d %H:%M:%S")

            elif v.__class__.__name__ == 'Hash':
                v = hex(int(v.Value, 16))

            setattr(self, k, v)

    @abc.abstractmethod
    def summary(self, *args, **kwargs):
        """
        The summary method is used to summarise any of the wrapped objects used within the framework. This may include
        the objects associated with users, processes, YARA scans, IAT/EAT/API hooks, DLLs, etc.

        :param kwargs: a dictionary of keyword arguments
        :return: a dictionary of attributes which summarise a given object
        """
        pass

    def to_namedtuple(self):
        """
        This method is used to export the result of the summary() method to a collections.namedtuple object. This is
        mainly convenience method which can be used by the framework's developers.

        :return: a namedtuple of attributes which summarise a given object
        """
        return collections.namedtuple(self.__class__.__name__, self.summary().keys())(**self.summary())

    def to_json(self):
        """
        This method is used to export the result of the summary() method to a json object. This is a convenience method
        which is used within main() to export information as JSON objects.

        :return: a json object of attributes which summarise a given object
        """
        return json.dumps(self.summary())

    def __str__(self):
        """
        This convenience method is used when printing any subclass using the print() call. This method is simply a
        convenience method used by the framework's developers.

        :return: a pretty-printed dictionary representation of the summary of a particular object
        """
        return pprint.pformat(self.summary())

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            yield k, v