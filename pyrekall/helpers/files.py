import pyrekall.helpers.usability
import glob
import os


def set_extension(path, extension):
    """
    Changes the file extension associated with a particular filename. Due to the recursive nature of this function,
    arbitrarily nested file extensions can be used.

    >>> import pyrekall.helpers.files
    >>> pyrekall.helpers.files.set_extension('42.tar.gz', 'dill')
    '42.dill'

    This is a convenience function which operates on strings, and does not actually change the file extension associated
    with a particular file.

    :param path: a path to an arbitrary file
    :param ext: the file extension to set
    :return: a new path with the specified file extension
    """
    def __current_extension(path, extension=''):
        """
        This inner function is used to identify the current file extension of a particular file. This function is used
        recursively within the set_extension() function

        :param path: a path to an arbitrary file
        :param extension: a string which stores the file extension associated with a particular file. It is updated
            recursively in order to handle nested file extensions

        :return: the current file extension of a particular file, as a string
        """
        p, e = os.path.splitext(path)
        if path != p:
            e += extension
            return __current_extension(path=p, extension=e)
        return extension

    if extension.startswith('.') is False:
        extension = '.' + extension
    return path.replace(__current_extension(path), extension)


def get_size(path, pretty=False):
    """
    This helper function allows you to determine the size of a particular file given an absolute or relative path

    >>> import pyrekall.helpers.files
    >>> pyrekall.helpers.files.get_size('LICENSE', pretty=True)
    '1.0KiB'

    :param path: the path to the file
    :param pretty: a boolean flag which indicates whether or not the output of this function should be human readable
    :return: the size of the file corresponding to the provided path
    """
    size = os.path.getsize(path)
    if pretty:
        return pyrekall.helpers.usability.sizeof_fmt(size)
    return size


def load(path, mode='rb'):
    """
    This helper function is used to read data from files. In the event that globbing is used, multiple files may be
    returned. If multiple files are returned, their contents will be returned within a list of file contents.

    :param path: the path to the file(s)
    :param mode: the mode to use when opening the file(s) (e.g. wb+)
    :return: the content of the file, or a list of file contents
    """
    def __load(path, mode):
        with open(path, mode) as fp:
            return fp.read()

    if glob.has_magic(path):
        contents = list(map(lambda p: __load(path=p, mode=mode), glob.glob(path)))
    else:
        contents = __load(path=path, mode=mode)

    if len(contents) == 1:
        return contents[0]
    else:
        return contents


def save(data, path, mode="wb+"):
    """
    This helper function is used to save files
    :param data: the data to write
    :param path: the path to the file
    :param mode: the mode to use when opening the file descriptor (e.g. wb+)
    """
    with open(path, mode) as fp:
        if isinstance(data, bytes) or isinstance(data, str):
            fp.write(data)
        else:
            fp.writelines(data)