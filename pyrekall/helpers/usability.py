import re

re_first_cap = re.compile('(.)([A-Z][a-z]+)')
re_all_cap = re.compile('([a-z0-9])([A-Z])')


def camelcase_to_snakecase(string):
    """
    This helper function is used to transform any string in CamelCase into snake_case.

    :param name:
    :return:
    """
    s1 = re_first_cap.sub(r'\1_\2', string)
    return re_all_cap.sub(r'\1_\2', s1).lower()


def sizeof_fmt(num, suffix='B'):
    """
    This helper function is used to transform any number of bytes into a human readable representation of them.

    >>> import pyrekall.helpers.usability
    >>> pyrekall.helpers.usability.sizeof_fmt(1234567890)
    '1.1GiB'

    :param num: a number of bytes
    :param suffix: the default suffix to be used
    :return: a human-readable representation of a number of bytes
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
