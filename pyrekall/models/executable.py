import hodgepodge.cryptography.hashing
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

    def is_32bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR32_MAGIC

    def is_64bit(self):
        return self.OPTIONAL_HEADER.Magic == MagicNumbers.IMAGE_NT_OPTIONAL_HDR64_MAGIC

    def md5(self):
        return hex(hodgepodge.cryptography.hashing.md5(self.__data__))

    def sha1(self):
        return hex(hodgepodge.cryptography.hashing.sha1(self.__data__))

    def sha256(self):
        return hex(hodgepodge.cryptography.hashing.sha256(self.__data__))

    def get_sections(self):
        return map(lambda section: Section(section, self), self.sections)


class Section:
    def __init__(self, section, pe):
        self.obj = section
        self.name = str(section.Name)
        self.virtual_address = hex(section.VirtualAddress)
        self.size = long(section.SizeOfRawData)

    def md5(self):
        return hex(hodgepodge.cryptography.hashing.md5(self.obj.get_data()))

    def sha1(self):
        return hex(hodgepodge.cryptography.hashing.sha1(self.obj.get_data()))

    def sha256(self):
        return hex(hodgepodge.cryptography.hashing.sha256(self.obj.get_data()))

    def get_data(self):
        return self.obj.get_data()

    def __repr__(self):
        return "{}: (SHA-1: {})".format(self.name, self.sha1())

    def __str__(self):
        return self.obj.__str__()