import pyrekall.helpers.crypto
import pyrekall.models.common
import pyrekall.models.handles
import pyrekall.models.executable
import pyrekall.models.dll

import logging
import cStringIO
import pefile

logger = logging.getLogger(__name__)


class Process(pyrekall.models.common.AbstractWrapper):
    def __init__(self, process, session):
        super(Process, self).__init__()

        self._session = session
        self._obj = process

        self._parent = None
        self._children = None

        self.name = str(process.ImageFileName)
        self.pid = int(process.UniqueProcessId)
        self.ppid = int(process.InheritedFromUniqueProcessId)

        # Handles
        self.number_of_handles = int(process.ObjectTable.m("HandleCount"))
        self.number_of_active_threads = int(process.ActiveThreads)

        # PEB fields
        self._peb = process.Peb
        self.path = process.Peb.ProcessParameters.ImagePathName
        self.command_line = process.Peb.ProcessParameters.CommandLine
        self.current_directory = process.Peb.ProcessParameters.CurrentDirectory.DosPath
        self.dll_path = process.Peb.ProcessParameters.DllPath

        # Time fields
        self.create_time = process.CreateTime
        self.exit_time = process.ExitTime

        # Address space fields
        self.virtual_offset = long(process.obj_offset)
        self.physical_offset = long(process.obj_vm.vtop(process.obj_offset))

        self.address_space_initialized = bool(process.AddressSpaceInitialized)
        self.has_address_space = bool(process.HasAddressSpace)

        # Other fields
        self.sub_system_major_version = int(process.SubSystemMajorVersion)
        self.sub_system_minor_version = int(process.SubSystemMinorVersion)
        self.sub_system_version = int(process.SubSystemVersion)

        # Lazy-loaded fields
        self._environment_variables = None
        self._handles = None
        self._dlls = None

        [setattr(self, k, self.unwrap(k, v)) for k, v in self]

    @property
    def session(self):
        return self._session

    @property
    def obj(self):
        return self._obj

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, v):
        self._parent = v

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, v):
        self._children = v

    @property
    def environment_variables(self):
        if self._environment_variables is None:
            e = {}
            for x in self._peb.ProcessParameters.Environment:
                k, v = str(x).split("=", 1)
                e[k] = v
            else:
                self._environment_variables = e
        return self._environment_variables

    def get_environment_variables(self):
        return self.environment_variables

    @property
    def handles(self):
        if self._handles is None:
            handles = []
            for object_header, handle_type, details in self.session.plugins.handles().enumerate_handles(self.obj):
                handle = pyrekall.models.handles.HandleFactory.create(
                    process=self,
                    handle=object_header,
                    details=details,
                    handle_type=handle_type)
                handles.append(handle)
            self._handles = handles
        return self._handles

    def get_handles(self):
        return self.handles

    @property
    def dlls(self):
        if self._dlls is None:
            if not self.peb:
                return []
            else:
                dlls = []
                for module in self.obj.get_load_modules():
                    dll = pyrekall.models.dll.Dll(module)
                    if self.path != dll.path:
                        dlls.append(dll)

            self._dlls = dlls
        return self._dlls

    def get_dlls(self):
        return self.dlls

    def get_executable(self):
        try:
            fd = cStringIO.StringIO()
            self.session.plugins.pedump().WritePEFile(fd=fd, address_space=self.obj.get_process_address_space(),
                                                      image_base=self._peb.ImageBaseAddress)
            return pyrekall.models.executable.PE(process=self, data=fd.getvalue())
        except pefile.PEFormatError:
            logger.warning("Failed to extract the executable associated with the {} process (PID: {})".format(
                self.name, self.pid))

    def __str__(self):
        return "{} @ {} (PID: {})".format(self.name, self.virtual_offset, self.pid)

