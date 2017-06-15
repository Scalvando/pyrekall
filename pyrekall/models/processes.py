import pyrekall.helpers.crypto
import pyrekall.models.common
import pyrekall.models.handles
import pyrekall.models.dll

import cStringIO
import pefile


class Process(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent processes which have been identified within a given memory sample
    """
    def __init__(self, process, session):
        super(Process, self).__init__()

        self.session = session
        self.raw = process

        self.name = process.ImageFileName
        self.pid = int(process.UniqueProcessId)
        self.ppid = int(process.InheritedFromUniqueProcessId)

        self.parent = None
        self.children = None

        self.number_of_handles = int(process.ObjectTable.m("HandleCount"))
        self.number_of_active_threads = int(process.ActiveThreads)

        # PEB fields
        self.peb = process.Peb
        self.path = self.peb.ProcessParameters.ImagePathName
        self.command_line = self.peb.ProcessParameters.CommandLine
        self.current_directory = self.peb.ProcessParameters.CurrentDirectory.DosPath

        self.dlls = self.get_dlls()
        self.dll_path = self.peb.ProcessParameters.DllPath

        self.environment_variables = self.get_environment_variables()
        self.handles = self.get_handles()

        # Time fields
        self.create_time = process.CreateTime.as_datetime().isoformat() or None
        self.exit_time = process.ExitTime.as_datetime().isoformat() or None

        # Address space fields
        self.virtual_offset = format(process.obj_offset, 'X')
        self.physical_offset = format(process.obj_vm.vtop(process.obj_offset), 'X')
        self.address_space_initialized = bool(process.AddressSpaceInitialized)
        self.has_address_space = bool(process.HasAddressSpace)

        # The executable and any associated cryptographic checksums
        self.raw_pe = self._write_pe_to_stringio()
        self.sha256 = format(pyrekall.helpers.crypto.sha256(self.raw_pe),'X')
        self.sha1 = format(pyrekall.helpers.crypto.sha1(self.raw_pe), 'X')
        self.md5 = format(pyrekall.helpers.crypto.md5(self.raw_pe), 'X')

        # Other fields
        #self.sub_system_major_version = int(process.SubSystemMajorVersion)
        #self.sub_system_minor_version = int(process.SubSystemMinorVersion)
        #self.sub_system_version = int(process.SubSystemVersion)

        super(Process, self).post_init()

    def get_environment_variables(self):
        """
        This function is used to identify the environment variables associated with a particular process

        :return: a dictionary of process environment variables
        """
        environment_variables = {}
        old_key = ''
        for x in self.peb.ProcessParameters.Environment:
            if '=' in str(x):
                k, v = str(x).split("=", 1)

                if k == '':
                    k, v = str(v).split("=", 1)
                    
                old_key = k
                environment_variables[k] = v
            else:
                environment_variables[old_key] += str(x)
            
        return environment_variables

    def get_handles(self):
        """
        This function is used to identify the handles associated with a particular process. These handles may include
        processes, threads, files, mutants, ports, semaphores, and more!

        :return: a list of handles
        """
        handles = []
        for object_header, handle_type, details in self.session.plugins.handles().enumerate_handles(self.raw):
            handles.append(pyrekall.models.handles.Handle(process=self.raw, handle=object_header, details=details,
                                                          handle_type=handle_type))
        return handles

    def get_dlls(self):
        """
        This function returns a list of DLLs loaded by a particular process. This function should be expanded to
        include DLLs which have been loaded, unloaded, and/or injected into a given process.

        :return: a list of DLLs
        """
        if not self.peb:
            return []
        else:
            dlls = []
            for module in self.raw.get_load_modules():
                dll = pyrekall.models.dll.Dll(module)
                if self.path != dll.path:
                    dlls.append(dll)
            return dlls

    def _write_pe_to_stringio(self):
        """
        Reconstructs the executable associated with a particular process, and writes it to a StringIO buffer

        :return: a StringIO buffer containing an in-memory representation of a Portable Executable (PE) file
        """
        fd = cStringIO.StringIO()
        self.session.plugins.pedump().WritePEFile(fd=fd, address_space=self.raw.get_process_address_space(),
                                                  image_base=self.peb.ImageBaseAddress)
        return fd.getvalue()

    def to_pe(self, raw=None):
        raw = raw or self._write_pe_to_stringio()
        try:
            return pefile.PE(data=raw)
        except Exception as E:
            return None

    def summary(self):
        handles = dlls = []

        if self.flags['include_handles']:
            handles = list(map(lambda x: x.summary(), self.handles))

        if self.flags['include_dlls']:
            dlls = list(map(lambda x: x.summary(), self.dlls))

        return {
            'name': self.name,
            'path': self.path,
            'pid': self.pid,
            'ppid': self.ppid,
            'md5': self.md5,
            'sha1': self.sha1,
            'sha256': self.sha256,
            'virtual_offset': self.virtual_offset,
            'physical_offset': self.physical_offset,
            'number_of_active_threads': self.number_of_active_threads,
            'number_of_handles': self.number_of_handles,
            'arguments': self.command_line,
            'current_directory': self.current_directory,
            'environment_variables': self.environment_variables,
            'handles': handles,
            'dlls': dlls,
            'creation_time': self.create_time,
            'exit_time': self.exit_time,
        }