import rekall.obj
import abc


class AbstractWrapper(object):
    __metaclass__ = abc.ABCMeta

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v