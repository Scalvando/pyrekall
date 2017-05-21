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

        self.session = session
        self.obj = process

        self.name = str(process.ImageFileName)
        self.pid = int(process.UniqueProcessId)
        self.ppid = int(process.InheritedFromUniqueProcessId)

        self.parent = None
        self.children = None

        # Handles
        self.number_of_handles = int(process.ObjectTable.m("HandleCount"))
        self.number_of_active_threads = int(process.ActiveThreads)

        # PEB fields
        self.peb = process.Peb
        self.path = self.peb.ProcessParameters.ImagePathName
        self.command_line = self.peb.ProcessParameters.CommandLine
        self.current_directory = self.peb.ProcessParameters.CurrentDirectory.DosPath
        self.dll_path = self.peb.ProcessParameters.DllPath

        # Time fields
        self.create_time = process.CreateTime.as_datetime().strftime("%Y-%m-%d %H:%M:%S") or None
        self.exit_time = process.ExitTime.as_datetime().strftime("%Y-%m-%d %H:%M:%S") or None

        # Address space fields
        self.virtual_offset = format(process.obj_offset, 'x')
        self.physical_offset = format(process.obj_vm.vtop(process.obj_offset), 'x')

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

    @property
    def environment_variables(self):
        if self._environment_variables is None:
            e = {}
            for x in self.peb.ProcessParameters.Environment:
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
                                                      image_base=self.peb.ImageBaseAddress)
            return pyrekall.models.executable.PE(data=fd.getvalue())
        except pefile.PEFormatError:
            logger.exception("Failed to extract the executable associated with the {} process (PID: {})".format(
                self.name, self.pid))

    def __str__(self):
        return "{} @ {}".format(self.name, self.virtual_offset)