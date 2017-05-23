from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def compute_checksum(data, *algorithms):
    checksums = {}

    def _finalize(algorithm):
        digest = checksums.get(algorithm.name)
        if digest:
            checksums[algorithm.name] = digest.finalize().encode('hex')

    def _update(algorithm, d):
        digest = checksums.get(algorithm.name, hashes.Hash(algorithm, backend=default_backend()))
        digest.update(d)
        checksums[algorithm.name] = digest

    #: If the argument is an open file descriptor,
    if isinstance(data, file):
        while True:
            chunk = data.read(100000)
            if chunk:
                [_update(algorithm, chunk) for algorithm in algorithms]
            else:
                break
    else:
        [_update(algorithm, data) for algorithm in algorithms]

    #: Finalise each of the cryptographic checksums
    [_finalize(algorithm) for algorithm in algorithms]

    #: Return a scalar value or a list of items
    if len(checksums) == 1:
        return checksums.values()[0]
    else:
        return checksums.values()


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


def blake2s(data):
    """
    A helper function used to apply the BLAKE-2s cryptographic hash function to a given block of input data

    :param data: the data to be hashed
    :return: the output of the BLAKE-2s cryptographic hash function represented as an integer
    """
    return _hash(algorithm=hashes.BLAKE2s, data=data)


def blake2b(data):
    """
    A helper function used to apply the BLAKE-2b cryptographic hash function to a given block of input data

    :param data: the data to be hashed
    :return: the output of the BLAKE-2b cryptographic hash function represented as an integer
    """
    return _hash(algorithm=hashes.BLAKE2b, data=data)