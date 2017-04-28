from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def _hash(algorithm, data, backend=default_backend()):
    """
    A helper function used to apply a particular cryptographic hash function to a particular object

    :param algorithm: an instance of the chosen cryptographic hash function
    :param data: the data to be hashed
    :param backend: the backend to use for cryptography.io
    :return: the output of the selected cryptographic hash function as an integer
    """
    digest = hashes.Hash(algorithm, backend)
    digest.update(data)
    return int(digest.finalize().encode('hex'), 16)


def sha1(data):
    """
    A helper function used to apply the SHA-1 cryptographic hash function to a given block of input data

    :param data: the data to be hashed
    :return: the output of the SHA-1 cryptographic hash function represented as an integer
    """
    return _hash(algorithm=hashes.SHA1(), data=data)


def sha256(data):
    """
    A helper function used to apply the SHA-256 cryptographic hash function to a given block of input data

    :param data: the data to be hashed
    :return: the output of the SHA-256 cryptographic hash function represented as an integer
    """
    return _hash(algorithm=hashes.SHA256(), data=data)


def md5(data):
    """
    A helper function used to apply the MD5 cryptographic hash function to a given block of input data

    :param data: the data to be hashed
    :return: the output of the MD5 cryptographic hash function represented as an integer
    """
    return _hash(algorithm=hashes.MD5(), data=data)
