from cryptography.hazmat.primitives import hashes

from pyrekall.models.common import AbstractWrapper
from pyrekall.models.processes import Process
from pyrekall.models.services import Service
from pyrekall.models.registry import Registry
from pyrekall.models.connections import Connection
from pyrekall.models.user import User

from hodgepodge.common.iterables import chunks

import pyrekall.helpers.usability
import pyrekall.helpers.files
import pyrekall.helpers.crypto
import rekall.session
import collections
import os


class Sample(AbstractWrapper):
    def __init__(self, path):
        super(Sample, self).__init__()

        self.filename = os.path.abspath(path)

        self._session = None
        self._profile = None

        self._md5 = None
        self._sha1 = None
        self._sha256 = None

        self._processes = None

    @property
    def session(self):
        if self._session is None:
            self._session = rekall.session.InteractiveSession(filename=self.filename)
            self._profile = self.session.profile
        return self._session

    @property
    def profile(self):
        return self.session.profile

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

    @property
    def processes(self):
        if self._processes is None:
            processes = list(map(
                lambda p: Process(process=p, session=self.session), self.session.plugins.pslist().filter_processes()))

            for p1 in processes:
                p1.children = []
                for p2 in processes:
                    if p1.pid == p2.ppid:
                        p1.children.append(p2)

                    if p1.ppid == p2.pid:
                        p1.parent = p2
            self._processes = sorted(processes, key=lambda p: p.pid)
        return self._processes

    def get_processes(self):
        return self.processes

    def get_processes_by_name(self, name=None):
        if name is None:
            for process in self.get_processes():
                yield process
        else:
            for process in filter(lambda p: p.name == name, self.processes):
                yield process

    def get_process_by_name(self, name):
        return next(self.get_processes_by_name(name), None)

    def get_process_by_pid(self, pid):
        for process in self.get_processes():
            if process.pid == pid:
                return process

    def get_all_process_environment_variables(self):
        e = {}

        for p in self.processes:
            for k, v in p.get_environment_variables().items():
                values = e.get(k, set())
                values.add(v)
                e[k] = values
        else:
            for k, v in e.items():
                e[k] = list(v)
        return e

    def get_service_sids(self):
        for k, v in self.session.plugins.getservicesids().get_service_sids():
            yield k, str(v)

    def get_services(self):
        for service in self.session.plugins.services().GenerateServices():
            yield Service(service)

    def get_registry(self):
        return Registry(self.session)

    def get_users(self):
        for u, v, f in self.session.plugins.users().GenerateUsers():
            users.append(User(u, v, f))
        return users
    
    def get_connections(self):
        """
        This function is used for the purpose of getting connections
        :return: a list of connections
        """
        return [Connection(c) for c in self.session.plugins.netstat().collect()]

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
            yield User(u, v, f)
