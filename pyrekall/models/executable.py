from cryptography.hazmat.primitives import hashes

import pyrekall.helpers.crypto
import pefile
import enum


class InstructionSet(enum.IntEnum):
    i386 = 0x14c
    i486 = 0x14c
    i586 = 0x14c


class InstructionSetArchitecture(enum.OrderedDict):
    x86 = {InstructionSet.i386, InstructionSet.i486, InstructionSet.i586}


class MagicNumbers(enum.IntEnum):
    IMAGE_NT_OPTIONAL_HDR32_MAGIC = 0x10b
    IMAGE_NT_OPTIONAL_HDR64_MAGIC = 0x20b
    IMAGE_ROM_OPTIONAL_HDR_MAGIC = 0x107


class PE(pefile.PE):
    def __init__(self, process, data):
        super(PE, self).__init__(data=data)

        self.process = process
        self.path = process.path

        self.number_of_sections = int(self.FILE_HEADER.NumberOfSections)
        self.number_of_symbols = int(self.FILE_HEADER.NumberOfSymbols)
        self.timestamp = int(self.FILE_HEADER.TimeDateStamp)

        self._md5 = None
        self._sha1 = None
        self._sha256 = None

    @property
    def md5(self):
        if self._md5 is None:
            self._compute_checksums()
        return self._md5

    @property
    def sha1(self):
        if self._sha1 is None:
            self._compute_checksums()
        return self._sha1

    @property
    def sha256(self):
        if self._sha256 is None:
            self._compute_checksums()
        return self._sha256

    def _compute_checksums(self):
        with open(self.filename, "rb") as fp:
            self._md5, \
            self._sha1, \
            self._sha256 = pyrekall.helpers.crypto.compute_checksum(
                fp, hashes.MD5(), hashes.SHA1(), hashes.SHA256())

    def is_32_bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR32_MAGIC

    def is_64_bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR64_MAGIC

    def get_sections(self):
        return list(map(lambda e: Section(e, self), self.sections))


class Section:
    def __init__(self, section, pe):
        self.obj = section
        self.name = str(section.Name)
        self.virtual_address = format(section.VirtualAddress, 'x')
        self.size = long(section.SizeOfRawData)

        self._md5 = None
        self._sha1 = None
        self._sha256 = None

    @property
    def md5(self):
        if self._md5 is None:
            self._compute_checksums()
        return self._md5

    @property
    def sha1(self):
        if self._sha1 is None:
            self._compute_checksums()
        return self._sha1

    @property
    def sha256(self):
        if self._sha256 is None:
            self._compute_checksums()
        return self._sha256

    def _compute_checksums(self):
        self._md5, \
        self._sha1, \
        self._sha256 = pyrekall.helpers.crypto.compute_checksum(
            self.get_data(), hashes.MD5(), hashes.SHA1(), hashes.SHA256())

    def get_data(self):
        return self.obj.get_data()

    def __str__(self):
        return "{} @ {}".format(self.name, self.virtual_address)