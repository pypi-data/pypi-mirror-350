"""Generic utility classes and functions."""

__pdoc__ = {
    "mfutil.jinja2_extensions": False,
    "mfutil.cli_tools": False,
    "mfutil.eval": False,
    "BashWrapper": False,
    "BashWrapperException": False,
    "BashWrapperOrRaise": False,
    "mfutil.exc": False,
    "add_inotify_watch": False,
    "create_tmp_dirpath": False,
    "eval": False,
    "get_ipv4_for_hostname": False,
    "get_recursive_mtime": False,
    "get_tmp_filepath": False,
    "get_unique_hexa_identifier": False,
    "get_utc_unix_timestamp": False,
    "hash_generator": False,
    "kill_process_and_children": False,
    "mkdir_p": False,
    "mkdir_p_or_die": False
}

from mfutil.bash_wrapper import (
    BashWrapper,
    BashWrapperOrRaise,
    BashWrapperException,
)
from mfutil.misc import (
    eval,
    get_unique_hexa_identifier,
    get_utc_unix_timestamp,
    mkdir_p,
    mkdir_p_or_die,
    get_tmp_filepath,
    create_tmp_dirpath,
    get_ipv4_for_hostname,
    get_recursive_mtime,
    kill_process_and_children,
    add_inotify_watch,
    hash_generator,
)
from mfutil.exc import MFUtilException

__all__ = [
    "BashWrapper",
    "BashWrapperOrRaise",
    "BashWrapperException",
    "MFUtilException",
    "get_unique_hexa_identifier",
    "eval",
    "get_utc_unix_timestamp",
    "mkdir_p",
    "mkdir_p_or_die",
    "get_tmp_filepath",
    "create_tmp_dirpath",
    "get_ipv4_for_hostname",
    "get_recursive_mtime",
    "kill_process_and_children",
    "add_inotify_watch",
    "hash_generator"
]
