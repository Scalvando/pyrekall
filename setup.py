from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages
from pyrekall.__about__ import *


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        import tox
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        tox.cmdline(args=args)

setup(
    name = __name__,
    version = __version__,
    description = __description__,
    url = __url__,
    download_url = __download_url__,
    author = __author__,
    author_email = __email__,
    license = __license__,
    keywords = __keywords__,
    classifiers = __classifiers__,
    packages = find_packages(),
    zip_safe = False,
    install_requires = [
        'cryptography',
        'rekall',
        'pefile',
    ],
    tests_require = ['tox'],
    cmdclass = {'test': Tox},
)