from pyrekall.models.common import AbstractWrapper

import functools

HANDLE_TYPE_FILTER_COMMUNICATION_PORT = "FilterCommunicationPort"
HANDLE_TYPE_WINDOW_STATION = "WindowStation"
HANDLE_TYPE_IO_COMPLETION = "IoCompletion"
HANDLE_TYPE_KEYED_EVENT = "KeyedEvent"
HANDLE_TYPE_DIRECTORY = "Directory"
HANDLE_TYPE_SEMAPHORE = "Semaphore"
HANDLE_TYPE_DESKTOP = "Desktop"
HANDLE_TYPE_SECTION = "Section"
HANDLE_TYPE_PROCESS = "Process"
HANDLE_TYPE_MUTANT = "Mutant"
HANDLE_TYPE_THREAD = "Thread"
HANDLE_TYPE_TIMER = "Timer"
HANDLE_TYPE_TOKEN = "Token"
HANDLE_TYPE_EVENT = "Event"
HANDLE_TYPE_FILE = "File"
HANDLE_TYPE_PORT = "Port"
HANDLE_TYPE_KEY = "Key"


class HandleFactory:
    @staticmethod
    def create(process, handle, details, handle_type):
        handle_type = str(handle_type)

        h = lambda c: c(process=process, handle=handle, details=details, handle_type=handle_type)

        if handle_type == HANDLE_TYPE_PROCESS:
            return h(ProcessHandle)
        elif handle_type == HANDLE_TYPE_FILE:
            return h(FileHandle)
        elif handle_type == HANDLE_TYPE_KEY:
            return h(KeyHandle)
        elif handle_type == HANDLE_TYPE_THREAD:
            return h(ThreadHandle)
        else:
            return h(Handle)


class Handle(AbstractWrapper):
    def __init__(self, process, handle, details, handle_type):
        super(Handle, self).__init__()

        self.object = handle
        self.process = process

        self.name = str(handle.NameInfo.Name) or None
        self.handle_type = str(handle_type)

        self.details = str(details)
        self.handle = hex(handle.HandleValue)
        self.access = hex(handle.GrantedAccess)

        self.pid = int(process.pid)

    def __str__(self):
        return "{} handle ({})".format(self.handle_type, self.process.__str__())


class ThreadHandle(Handle):
    def __init__(self, process, handle, details, handle_type):
        super(ThreadHandle, self).__init__(process, handle, details, handle_type)

        self.obj = handle.dereference_as("_ETHREAD")
        self.thread_id = self.obj.Cid.UniqueThread


class KeyHandle(Handle):
    def __init__(self, process, handle, details, handle_type):
        super(KeyHandle, self).__init__(process, handle, details, handle_type)

        self.obj = handle.dereference_as("_CM_KEY_BODY")
        self.name = self.obj.full_key_name()


class FileHandle(Handle):
    def __init__(self, process, handle, details, handle_type):
        super(FileHandle, self).__init__(process, handle, details, handle_type)

        self.obj = handle.dereference_as("_FILE_OBJECT")
        self.filename_with_drive = str(self.obj.file_name_with_drive())
        self.filename_with_device = str(self.obj.file_name_with_device())
        self.filename = self.filename_with_drive or self.filename_with_device


class ProcessHandle(Handle):
    def __init__(self, process, handle, details, handle_type):
        super(ProcessHandle, self).__init__(process, handle, details, handle_type)

    def get_process(self):
        return self.process

    def get_parent_process(self):
        return self.process.parent

    def get_pid(self):
        return self.process.pid

    def get_ppid(self):
        return self.process.ppid