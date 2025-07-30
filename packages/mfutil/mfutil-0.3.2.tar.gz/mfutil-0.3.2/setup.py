import sys
from setuptools import setup
from setuptools import find_packages

required = []
dependency_links = []
EGG_MARK = '#egg='
with open('requirements.txt') as reqs:
    for line in reqs.read().split('\n'):
        if line.startswith('-e git:') or line.startswith('-e git+') or \
                line.startswith('git:') or line.startswith('git+'):
            if EGG_MARK in line:
                package_name = line[line.find(EGG_MARK) + len(EGG_MARK):]
                required.append(package_name)
                dependency_links.append(line)
            else:
                print('Dependency to a git repository should have the format:')
                print('git+ssh://git@github.com/xxxxx/xxxxxx#egg=package_name')
                sys.exit(1)
        else:
            required.append(line)

required.append("inotify_simple")

setup(
    version="0.3.2",
    name='mfutil',
    url="https://github.com/metwork-framework/mfutil",
    packages=find_packages(),
    install_requires=required,
    python_requires='>=3.8',
    dependency_links=dependency_links,
    entry_points={
        "console_scripts": [
            "get_ip_for_hostname = mfutil.cli_tools.get_ip_for_hostname:main",
            "get_simple_hostname = mfutil.cli_tools.get_simple_hostname:main",
            "get_full_hostname = mfutil.cli_tools.get_full_hostname:main",
            "get_domainname = mfutil.cli_tools.get_domainname:main",
            "get_real_ip = mfutil.cli_tools.get_real_ip:main",
            "ping_tcp_port = mfutil.cli_tools.ping_tcp_port:main",
            "mfprogress = mfutil.cli_tools.mfprogress:main",
            "recursive_kill.py = mfutil.cli_tools.recursive_kill:main",
        ]
    }
)
