"""Generic utility classes and functions."""

import uuid
import errno
import os
import logging
import tempfile
import socket
import psutil
import pickle
import hashlib
from datetime import datetime, timezone
import time
import fnmatch

from inotify_simple import flags
from mfutil.exc import MFUtilException
from mfutil.eval import SandboxedEval

__pdoc__ = {
    "add_inotify_watch": False
}


def __get_logger():
    return logging.getLogger("mfutil")


def eval(expr, variables=None):
    """Evaluate (safely) a python expression (as a string).

    The eval is done with simpleeval library.

    Following functions are available (in expressions):

    - re_match: see match() function of re module
    - re_imatch: insensitive match() function of re module
    - fnmatch.fnmatch: fnmatch() function of fnmatch module

    Args:
        expr (string): the python expression to eval.
        variables (dict): if set, inject some variables/values
            in the expression.

    """

    s = SandboxedEval(names=variables)
    return s.eval(expr)


def get_unique_hexa_identifier():
    """Return an unique hexa identifier on 32 bytes.

    The idenfier is made only with 0123456789abcdef
    characters.

    Returns:
        (string) unique hexa identifier.

    """
    return str(uuid.uuid4()).replace('-', '')


def get_utc_unix_timestamp():
    """Return the current unix UTC timestamp on all platforms.

    It works even if the machine is configured in local time.

    Returns:
        (int) a int corresponding to the current unix utc timestamp.

    """

    # utcnow() is deprecated  and should be replaced by now(datetime.UTC)
    #   (for python >= 3.11)
    try:
        dts = datetime.now(timezone.utc).replace(tzinfo=None)
    except Exception:
        dts = datetime.utcnow()

    return int(time.mktime(dts.timetuple()))


def mkdir_p(path, nodebug=False, nowarning=False):
    """Make a directory recursively (clone of mkdir -p).

    Thanks to http://stackoverflow.com/questions/600268/
        mkdir-p-functionality-in-python .

    Any exceptions are catched and a warning message
    is logged in case of problems.

    If the directory already exists, True is returned
    with no debug or warning.

    Args:
        path (string): complete path to create.
        nodebug (boolean): if True, no debug messages are logged.
        nowarning (boolean): if True, no message are logged in
            case of problems.

    Returns:
        boolean: True if the directory exists at the end.

    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            return True
        else:
            if not nowarning:
                __get_logger().warning("can't create %s directory", path)
            return False
    # We do not log debug message because it is logged in circus
    #   configuration file
    # if not nodebug:
    #    __get_logger().debug("%s directory created", path)
    return True


def mkdir_p_or_die(path, nodebug=False, exit_code=2):
    """Make a directory recursively (clone of mkdir -p).

    If the directory already exists, True is returned
    with no debug or warning.

    Any exceptions are catched.

    In case of problems, the program dies here with corresponding
    exit_code.

    Args:
        path (string): complete path to create.
        nodebug (boolean): if True, no debug messages are logged.
        exit_code (int): os._exit() exit code.

    """
    res = mkdir_p(path, nodebug=nodebug, nowarning=True)
    if not res:
        __get_logger().error("can't create %s directory", path)
        os._exit(exit_code)


def _get_temp_dir(tmp_dir=None):
    """Return system temp dir or used choosen temp dir.

    If the user provides a tmp_dir argument, the
    directory is created (if necessary).

    If the user don't provide a tmp_dir argument,
    the function returns a system temp dir.

    If the directory is not good or can be created,
    an exception is raised.

    Args:
        tmp_dir (string): user provided tmp directory (None
            to use the system temp dir).

    Returns:
        (string) temp directory

    Raises:
        MFUtilException if the temp directory is not good or can't
            be created.

    """
    if tmp_dir is None:
        tmp_dir = tempfile.gettempdir()
    res = mkdir_p(tmp_dir)
    if not res:
        raise MFUtilException("can't create temp_dir: %s", tmp_dir)
    return tmp_dir


def get_tmp_filepath(tmp_dir=None, prefix=""):
    """Return a tmp (complete) filepath.

    The filename is made with get_unique_hexa_identifier() identifier
    so 32 hexa characters.

    The dirname can be provided by the user (or be a system one).
    He will be created if necessary. An exception can be raised if any
    problems at this side.

    Note: the file is not created or open at all. The function just
    returns a filename.

    Args:
        tmp_dir (string): user provided tmp directory (None
            to use the system temp dir).
        prefix (string): you can add here a prefix for filenames
            (will be preprended before the 32 hexa characters).

    Returns:
        (string) tmp (complete) filepath.

    Raises:
        MFUtilException if the temp directory is not good or can't
            be created.

    """
    temp_dir = _get_temp_dir(tmp_dir)
    return os.path.join(temp_dir, prefix + get_unique_hexa_identifier())


def create_tmp_dirpath(tmp_dir=None, prefix=""):
    """Create and return a temporary directory inside a father
    tempory directory.

    The dirname is made with get_unique_hexa_identifier() identifier
    so 32 hexa characters.

    The father dirname can be provided by the user (or be a system one).
    He will be created if necessary. An exception can be raised if any
    problems at this side.

    Note: the temporary directory is created.

    Args:
        tmp_dir (string): user provided tmp directory (None
            to use the system temp dir).
        prefix (string): you can add here a prefix for dirnames
            (will be preprended before the 32 hexa characters).

    Returns:
        (string) complete path of a newly created temporary directory.

    Raises:
        MFUtilException if the temp directory can't be created.

    """
    temp_dir = _get_temp_dir(tmp_dir)
    new_temp_dir = os.path.join(temp_dir,
                                prefix + get_unique_hexa_identifier())
    res = mkdir_p(new_temp_dir, nowarning=True)
    if not res:
        raise MFUtilException("can't create temp_dir: %s", new_temp_dir)
    return new_temp_dir


def get_ipv4_for_hostname(hostname, static_mappings={}):
    """Translate a host name to IPv4 address format.

    The IPv4 address is returned as a string, such as '100.50.200.5'.
    If the host name is an IPv4 address itself it is returned unchanged.

    You can provide a dictionnary with static mappings.
    Following mappings are added by default:
    '127.0.0.1' => '127.0.0.1'
    'localhost' => '127.0.0.1'
    'localhost.localdomain' => '127.0.0.1'

    Args:
        hostname (string): hostname.
        static_mappings (dict): dictionnary of static mappings
            ((hostname) string: (ip) string).

    Returns:
        (string) IPv4 address for the given hostname (None if any problem)

    """
    hostname = hostname.lower()
    static_mappings.update({'127.0.0.1': '127.0.0.1', 'localhost': '127.0.0.1',
                            'localhost.localdomain': '127.0.0.1'})
    if hostname in static_mappings:
        return static_mappings[hostname]
    try:
        return socket.gethostbyname(hostname)
    except Exception:
        return None


def get_recursive_mtime(directory, ignores=[]):
    """Get the latest mtime recursivly on a directory.

    Args:
        directory (string): complete path of a directory to scan.
        ignores (list of strings): list of shell-style wildcards
            to define which filenames/dirnames to ignores (see fnmatch).

    Returns:
        (int) timestamp of the latest mtime on the directory.

    """
    result = 0
    for name in os.listdir(directory):
        ignored = False
        for ssw in ignores:
            if fnmatch.fnmatch(name, ssw):
                ignored = True
                break
        if ignored:
            continue
        fullpath = os.path.join(directory, name)
        if os.path.isdir(fullpath):
            mtime = get_recursive_mtime(fullpath, ignores=ignores)
        else:
            mtime = 0
            try:
                mtime = int(os.path.getmtime(fullpath))
            except Exception:
                pass
        if mtime > result:
            result = mtime
    return result


def add_inotify_watch(inotify, directory, ignores=[]):
    """Register recursively directories to watch.

    Args:
        inotify (inotify object): object that owns the file descriptors
        directory (string): complete path of a directory to scan.
        ignores (list of strings): list of shell-style wildcards
        to define which filenames/dirnames to ignores (see fnmatch).

    """
    watch_flags = flags.MODIFY | flags.CREATE |\
        flags.DELETE | flags.DELETE_SELF
    try:
        __get_logger().info("watch %s" % directory)
        inotify.add_watch(directory, watch_flags)
    except Exception as e:
        __get_logger().warning("cannot watch %s: %s" % (directory, e))

    if not os.access(directory, os.R_OK):
        __get_logger().warning("cannot enter into %s" % directory)
        return

    for name in os.listdir(directory):
        ignored = False
        for ssw in ignores:
            if fnmatch.fnmatch(name, ssw):
                ignored = True
                break
        if ignored:
            continue
        fullpath = os.path.join(directory, name)
        if os.path.isdir(fullpath):
            add_inotify_watch(inotify, fullpath, ignores=ignores)


def _kill_process_and_children(process):
    children = None
    all_children = None
    # First we keep the full view of the process tree to kill
    try:
        all_children = process.children(recursive=True)
    except psutil.NoSuchProcess:
        pass
    # Then, we keep just immediate children to kill in the "good" order
    try:
        children = process.children(recursive=False)
    except psutil.NoSuchProcess:
        pass
    try:
        process.kill()
    except psutil.NoSuchProcess:
        pass
    if children is not None:
        for child in children:
            _kill_process_and_children(child)
    # To be sure, we didn't miss something, we kill the initial full list
    if all_children is not None:
        for child in all_children:
            _kill_process_and_children(child)


def kill_process_and_children(pid):
    """Kill recursively a complete tree of processes.

    Given a pid, this method recursively kills the complete tree (children and
    children of each child...) of this process.

    The SIGKILL signal is used.

    Args:
        pid (int): process PID to kill.

    """
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    _kill_process_and_children(process)


def hash_generator(*args):
    """Generate a hash from a variable number of arguments as a safe string.

    Note that pickle is used so arguments have to be serializable.

    Args:
        *args: arguments to hash

    """
    temp = pickle.dumps(args, pickle.HIGHEST_PROTOCOL)
    return hashlib.md5(temp).hexdigest()
