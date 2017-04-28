### pyrekall: a wrapper for Google Rekall

[![Build Status](https://travis-ci.org/TylerJFisher/pyrekall.svg?branch=master)](https://travis-ci.org/TylerJFisher/pyrekal)

`pyrekall` is a simple, and concise wrapper for the Google Rekall volatile memory analysis framework.

### Installation

```
sudo pip2 install pyrekall
```

### Features

The wrapper has the ability to identify the following information about memory samples, processes, services, and users:
    
- *__Processes__*: name of the process, and the path to its executable, cryptographic checksums of the associated executable, virtual/physical offset, parent/child processes, number of active threads, number of open handles, command line arguments, environment variables, DLL dependencies, process creation / exit timestamps, and more™
- *__Services__*: name, display name, tags, group, description of the service, path to the associated executable, service type, group / service dependencies
- *__Users__*: user name, full name, description of the account, account expiry information, corresponding SAM registry key name, account flags, timestamps corresponding to successful / failed log-in, password reset / failure timestamps

### Usage

The wrapper has been designed for use as a module, or as an interactive command-line application. That being said, a readily extensible command-line interface has been provided.

To list the command line arguments, and switches:

```
python2 pyrekall/main.py samples/xp.vmem -h
usage: main.py [-h] [-A] [-X] [-S] [-U] [-P] [--include-handles]
               [--include-dlls] [--pretty-print] [--human-readable]
               file

positional arguments:
  file               the name of the memory sample to use

optional arguments:
  -h, --help         show this help message and exit
  -A, --all          list everything of interest
  -X, --sample       list high-level information about the memory sample
  -S, --services     list running services
  -U, --users        list users
  -P, --processes    list running processes
  --include-handles  include handles in process summaries
  --include-dlls     include DLL dependencies in process summaries
  --pretty-print     pretty print the CLI output
  --human-readable   Use human readable representations of integers where
                     applicable (e.g. 128868 → 126MiB )
```

#### How do you identify processes within a particular memory sample?

```
python2 pyrekall/main.py samples/xp.vmem --pretty-print -P --include-dlls
...
{'command_line_arguments': 'C:\\WINDOWS\\system32\\wscntfy.exe',
                'creation_time': '2010-10-29 17:11:49',
                'current_directory': 'C:\\WINDOWS\\system32\\',
                'dlls': [{'base': '0x7c900000',
                          'name': 'ntdll.dll',
                          'path': 'C:\\WINDOWS\\system32\\ntdll.dll',
                          'size': '700.0KiB'},
                         ...
                         {'base': '0x5ad70000',
                          'name': 'uxtheme.dll',
                          'path': 'C:\\WINDOWS\\system32\\uxtheme.dll',
                          'size': '224.0KiB'}],
                'environment_variables': {'ALLUSERSPROFILE': 'C:\\Documents and Settings\\All Users',
                                          'APPDATA': 'C:\\Documents and Settings\\Administrator\\Application Data',
                                          'COMPUTERNAME': 'JAN-DF663B3DBF1',
                                          ...
                                          'windir': 'C:\\WINDOWS'},
                'exit_time': None,
                'handles': [],
                'md5': '0xe34432676aed50096e79571cfa67a727L',
                'name': 'wscntfy.exe',
                'number_of_active_threads': 1,
                'number_of_handles': 28,
                'path': 'C:\\WINDOWS\\system32\\wscntfy.exe',
                'physical_offset': '0x22ecc10',
                'pid': 2040,
                'ppid': 1032,
                'sha1': '0x491e20e5bd36ad366931e5e0bef87aa55a5b124aL',
                'sha256': '0x6e9c0b22e4d4a09e08a6f893fa8d14d3c05232d804cb0bb33f43fb525ddc3d83L',
                'virtual_offset': '0x820ecc10'}
```


### Tests

In order to run the unit and integration tests for `pyrekall`, simply clone this repository, and run `tox`:

```bash
git clone https://github.com/TylerJFisher/pyrekall.git
cd pyrekall
pip install tox
tox
```
