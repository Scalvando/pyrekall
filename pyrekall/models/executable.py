from cryptography.hazmat.primitives import hashes

import pyrekall.helpers.crypto
import datetime
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
    def __init__(self, data):
        super(PE, self).__init__(data=data)

        self.number_of_sections = int(self.FILE_HEADER.NumberOfSections)
        self.number_of_symbols = int(self.FILE_HEADER.NumberOfSymbols)

        self.timestamp = datetime.datetime.fromtimestamp(self.FILE_HEADER.TimeDateStamp).strftime("%Y-%m-%d %H:%M:%S")

        self.md5, self.sha1, self.sha256 = pyrekall.helpers.crypto.compute_checksum(
            data, hashes.MD5(), hashes.SHA1(), hashes.SHA256()
        )

    def is_32bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR32_MAGIC

    def is_64bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR64_MAGIC

    def get_sections(self):
        for section in self.sections:
            yield Section(section, self)


class Section:
    def __init__(self, section, pe):
        self.obj = section
        self.name = str(section.Name)
        self.virtual_address = format(section.VirtualAddress, 'x')
        self.size = long(section.SizeOfRawData)

        self.md5, self.sha1, self.sha256 = pyrekall.helpers.crypto.compute_checksum(
            self.get_data(), hashes.MD5(), hashes.SHA1(), hashes.SHA256()
        )

    def get_data(self):
        return self.obj.get_data()

    def __repr__(self):
        return "{} @ {}".format(self.name, self.virtual_address)

    def __str__(self):
        return self.obj.__str__()