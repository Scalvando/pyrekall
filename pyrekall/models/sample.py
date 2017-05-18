from pyrekall.models.common import AbstractWrapper
from pyrekall.models.processes import Process
from pyrekall.models.services import Service
from pyrekall.models.registry import Registry
from pyrekall.models.user import User
from pyrekall.models.mft_entry import MFT_Entry
from pyrekall.models.file import File
from pyrekall.models.driver import Driver
from pyrekall.models.ssdt import SSDT
from pyrekall.models.connections import Connection

import pyrekall.helpers.usability
import pyrekall.helpers.files
import pyrekall.helpers.crypto
import rekall.session


class Sample(AbstractWrapper):
    """
    This class is used to represent a physical memory snapshot, and provides methods to be used for the purpose of
    working with memory samples
    """
    def __init__(self, path):
        super(Sample, self).__init__()

        self.session = rekall.session.InteractiveSession(filename=path)
        self.profile = self.session.profile

        self.filename = self.session.physical_address_space.fname
        self.size = self.session.physical_address_space.fsize
        self.profile_name = self.profile.name

        self.physical_address_space = str(self.session.physical_address_space)

        contents = pyrekall.helpers.files.load(path=path)
        self.md5 = hex(pyrekall.helpers.crypto.md5(contents))
        self.sha1 = hex(pyrekall.helpers.crypto.sha1(contents))
        self.sha256 = hex(pyrekall.helpers.crypto.sha256(contents))

        super(Sample, self).post_init()

    def get_process_by_name(self, name):
        """
        This function is used to identify processes by name. In the event that multiple processes share the same name,
        only the first process will be returned.

        :param name: the name of the process to search for
        :return: a process
        """
        for process in self.get_processes():
            if process.name == name:
                return process

    def get_process_by_pid(self, pid):
        """
        This function is used to identify processes using their associated PID

        :param pid: the pid of the process to search for
        :return: a process
        """
        for process in self.get_processes():
            if process.pid == pid:
                return process

    def get_processes(self):
        """
        This function is used to identify processes within a particular memory snapshot. Since certain processes have
        parents, and children, this is taken into consideration.

        :return: a list of processes
        """
        processes = []
        for process in self.session.plugins.pslist().filter_processes():
            processes.append(Process(process=process, session=self.session))

        for p1 in processes:
            children = []
            for p2 in processes:
                if p1.pid == p2.ppid:
                    children.append(p2)

                if p1.ppid == p2.pid:
                    p1.parent = p2
            else:
                p1.children = children
        return processes

    def get_service_sids(self):
        """
        This function is used to identify service SIDs
        :return: a list of service SIDs
        """
        service_sids = []
        for k, v in self.session.plugins.getservicesids().get_service_sids():
            service_sids.append(
                (k, str(v))
            )
        return service_sids

    def get_services(self):
        """
        This function is used to identify services
        :return: a list of services
        """
        return list(map(lambda s: Service(s), self.session.plugins.services().GenerateServices()))

    def get_registry(self):
        """
        This function presents an interface to the Windows registry
        :return: an interface to the Windows registry
        """
        return Registry(self.session)

    def get_users(self):
        """
        This function is used for the purpose of identifying users
        :return: a list of users
        """
        users = []
        for u, v, f in self.session.plugins.users().GenerateUsers():
            users.append(User(u, v, f))
        return users
    
    def get_connections(self):
        """
        This function is used for the purpose of getting connections
        :return: a list of connections
        """
        return [Connection(c) for c in self.session.plugins.netscan().collect()]
    
    def get_mft(self):
        """
        This function is used for the purpose of getting MFT entries
        :return: a list of MFT entries
        """
        return [MFT_Entry(e) for e in self.session.plugins.mftdump().collect()]
    
    def get_files(self):
        """
        This function is used for the purpose of getting pooled files
        :return: a list of files
        """
        return [File(f) for f in self.session.plugins.filescan().collect()]

    def get_drivers(self):
        """
        This function is used for the purpose of getting drivers
        :return: a list of drivers
        """
        return [Driver(d) for d in self.session.plugins.driverscan().collect()]

    def get_ssdt(self):
        """
        This function is used for the purpose of getting the System Service Descriptor 
        Table
        :return: a list of SSDT entries
        """
        return [SSDT(d) for d in self.session.plugins.ssdt().collect() if 'divider' not in d]
    
    def get_sockets(self):
        """
        This function is used for the purpose of getting active sockets
        :return: a list of active sockets
        """
        return [Socket(s) for s in self.session.plugins.sockets().collect()]

    def summary(self, all=False):
        summary = {
            "filename": self.filename,
            "profile_name": self.profile_name,
            "physical_address_space": self.physical_address_space,
            "size": self.size,
            "md5": self.md5,
            "sha1": self.sha1,
            "sha256": self.sha256,
        }

        if self.flags['human_readable']:
            summary['size'] = pyrekall.helpers.usability.sizeof_fmt(self.size)

        if all:
            summary['processes'] = list(map(lambda x: x.summary(), self.get_processes()))
            summary['services'] = list(map(lambda p: p.summary(), self.get_services()))
            summary['users'] = list(map(lambda x: x.summary(), self.get_users()))

        return summary
