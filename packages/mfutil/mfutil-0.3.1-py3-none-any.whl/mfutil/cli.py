# -*- coding: utf-8 -*-
"""Utility functions to build CLI (Python >= 3.6 only)."""

from __future__ import print_function
import six
import sys
try:
    from rich.progress import Progress, BarColumn, ProgressColumn, \
        TimeRemainingColumn
    from rich.text import Text
    from rich.bar import Bar
    from rich.table import Table
    from rich.console import Console
except ImportError:
    class Dummy():
        pass
    TimeRemainingColumn = Dummy
    BarColumn = Dummy
    ProgressColumn = Dummy
    Progress = Dummy
    Bar = Dummy

from mfutil.exc import MFUtilException

__pdoc__ = {
    "MFTimeRemainingColumn": False,
    "StateColumn": False
}

_STDOUT_CONSOLE = None
_STDERR_CONSOLE = None


def _get_console(**kwargs):
    global _STDOUT_CONSOLE, _STDERR_CONSOLE
    if len(kwargs) > 1 or \
            (len(kwargs) == 1 and
             (kwargs.get('file', None) not in (sys.stdout, sys.stderr))):
        return Console(**kwargs)
    file = kwargs.get('file', None)
    if file == sys.stdout:
        if _STDOUT_CONSOLE is None:
            _STDOUT_CONSOLE = Console(**kwargs)
        return _STDOUT_CONSOLE
    elif file == sys.stderr:
        if _STDERR_CONSOLE is None:
            _STDERR_CONSOLE = Console(**kwargs)
        return _STDERR_CONSOLE
    return Console(**kwargs)


def _is_interactive(f):
    c = _get_console(file=f)
    return c.is_terminal


def is_interactive(target=None):
    """Return True if we are in an interactive terminal.

    Args:
        target (string): can be None (for stdout AND stderr checking),
            "stdout" (for stdout checking only or "stderr" (for stderr checking
            only).

    Returns:
        boolean (True (interactive) or False (non-interactive).

    Raises:
        MFUtilException: if target is invalid

    """
    if target is None:
        return _is_interactive(sys.stdout) and _is_interactive(sys.stderr)
    elif target == "stdout":
        return _is_interactive(sys.stdout)
    elif target == "stderr":
        return _is_interactive(sys.stderr)
    else:
        raise MFUtilException("invalid target parameter: %s" % target)


def echo_ok(message=""):
    """Write [OK] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[32mOK\033[0;0m ] %s%s" % (
            message, " " * (13 - len(message)))
        )
    else:
        print(" [ OK ] %s" % message)


def echo_nok(message=""):
    """Write [ERROR] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[31mERROR\033[0;0m ] %s%s" % (
            message, " " * (10 - len(message)))
        )
    else:
        print(" [ ERROR ] %s" % message)


def echo_warning(message=""):
    """Write [WARNING] with colors if supported a little optional message.

    Args:
        message (string): little optional message.

    """
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[33mWARNING\033[0;0m ] %s" % message)
    else:
        print("[ WARNING ] %s" % message)


def echo_bold(message):
    """Write a message in bold (if supported).

    Args:
        message (string): message to write in bold.

    """
    if is_interactive("stdout"):
        print("\033[1m%s\033[0m" % message)
    else:
        print(message)


def echo_running(message=None):
    """Write [RUNNING] with colors if supported.

    You can pass an optional message which will be rendered before [RUNNING]
    on the same line.

    Args:
        message (string): little optional message.

    """
    if message is not None:
        if is_interactive("stdout"):
            if six.PY2:
                print(message, end="")
                sys.stdout.flush()
            else:
                print(message, end="", flush=True)
        else:
            print(message, end="")
    if is_interactive("stdout"):
        echo_clean()
        print("\033[60G[ \033[33mRUNNING\033[0;0m ]", end="")


def echo_clean():
    """Clean waiting status."""
    if is_interactive("stdout"):
        print("\033[60G[ \033           ", end="")


class StateColumn(ProgressColumn):

    def render(self, task):
        if task.finished:
            extra = task.fields.get('status_extra', '')
            if len(extra) > 0:
                extra = " (%s)" % extra
            if task.fields.get('status', 'OK') == 'ERROR':
                return Text.assemble(Text("[ "),
                                     Text("ERROR", style="red"),
                                     Text(" ]%s" % extra))
            elif task.fields.get('status', 'OK') == 'WARNING':
                return Text.assemble(Text("[ "),
                                     Text("WARNING", style="yellow"),
                                     Text(" ]%s" % extra))
            else:
                return Text.assemble(Text("[ "),
                                     Text("OK", style="green"),
                                     Text(" ]%s" % extra))
        else:
            return Text.assemble(Text("[ "),
                                 Text("RUNNING", style="yellow"),
                                 Text(" ]"))


class MFTimeRemainingColumn(TimeRemainingColumn):

    def render(self, task):
        if task.finished:
            return Text("")
        else:
            return TimeRemainingColumn.render(self, task)


class MFProgress(Progress):
    """[Rich Progress]
    (https://rich.readthedocs.io/en/latest/progress.html) child class.

    This class add three features to the original one:

    - support (basic) rendering in non-terminal
    - task status management
    - different default columns setup (but you can override this)
    - rendering on stdout by default (but you can change this by providing
        a custom Console object)

    You can use it exactly like the original [Progress class]
    (https://rich.readthedocs.io/en/latest/reference/progress.html):

    ```python
    import time
    from mfutil.cli import MFProgress

    with MFProgress() as progress:
        t1 = p.add_task("Foo task")
        t2 = p.add_task("Foo task")
        while not progress.finished:
            progress.update(t1, advance=10)
            progress.update(t2, advance=10)
            time.sleep(1)
    ```

    For status management:

    - if you leave MFProgress context manager, not finished tasks are
        automatically set to `ERROR` state, finished tasks are automatically
        set to `OK` state
    - you have 3 new methods to manually override this behaviour:
        (complete_task(), complete_task_nok(), complete_task_warning())

    Example:

    ```python
    import time
    from mfutil.cli import MFProgress

    with MFProgress() as progress:
        t1 = p.add_task("Foo task")
        t2 = p.add_task("Foo task")
        i = 0
        while not progress.finished:
            progress.update(t1, advance=10)
            if i < 5:
                progress.update(t2, advance=10)
            elif i == 5:
                progress.complete_task_failed(t2, "unknown error")
            time.sleep(1)
            i = i + 1
    ```

    """
    def __init__(self, *args, **kwargs):
        console = kwargs.get("console", None)
        if not console:
            self._interactive = _is_interactive(sys.stdout)
            kwargs["console"] = Console()
        else:
            self._interactive = _is_interactive(console.file)
        if len(args) == 0:
            columns = ["[progress.description]{task.description}",
                       BarColumn(12),
                       StateColumn(),
                       MFTimeRemainingColumn()]
            self.mfprogress_columns = True
        else:
            columns = args
            self.mfprogress_columns = False
        Progress.__init__(self, *columns, **kwargs)

    def make_tasks_table(self, tasks):
        if self.mfprogress_columns:
            return self._mfprogress_make_tasks_table(tasks)
        else:
            return MFProgress.make_tasks_table(self, tasks)

    def _mfprogress_make_tasks_table(self, tasks):
        """Get a table to render the Progress display."""
        table = Table.grid()
        table.pad_edge = True
        table.padding = (0, 1, 0, 0)
        try:
            finished = self.finished
        except Exception:
            finished = False
        if finished:
            table.add_column(width=57, no_wrap=True)
            table.add_column(width=0)
            table.add_column()
            table.add_column()
        else:
            table.add_column(width=45, no_wrap=True)
            table.add_column()
            table.add_column()
            table.add_column()
        for task in tasks:
            if task.visible:
                row = []
                append = row.append
                for index, column in enumerate(self.columns):
                    if isinstance(column, str):
                        txt = column.format(task=task)
                        if finished:
                            if len(txt) > 79:
                                txt = txt[0:74] + "[[...]]"
                        else:
                            if len(txt) > 67:
                                txt = txt[0:62] + "[[...]]"
                        append(txt)
                        table.columns[index].no_wrap = True
                    else:
                        widget = column(task)
                        append(widget)
                        if isinstance(widget, (str, Text)):
                            table.columns[index].no_wrap = True
                table.add_row(*row)
        return table

    def __exit__(self, *args, **kwargs):
        with self._lock:
            for tid, task in self._tasks.items():
                if not task.finished:
                    self.complete_task_nok(tid)
        Progress.__exit__(self, *args, **kwargs)

    def start(self, *args, **kwargs):
        if self._interactive:
            return Progress.start(self, *args, **kwargs)

    def __complete_task_nok_nolock(self, task_id, status_extra=""):
        task = self._tasks[task_id]
        self.update(task_id, completed=task.total, status="ERROR",
                    refresh=False, status_extra=status_extra)

    def complete_task_nok(self, task_id, status_extra=""):
        """Complete a task with ERROR status.

        Args:
            task_id (TaskID): a task ID.
            status_extra (str): a little extra message to add.

        """
        with self._lock:
            self.__complete_task_nok_nolock(task_id, status_extra=status_extra)

    def complete_task_warning(self, task_id, status_extra=""):
        """Complete a task with WARNING status.

        Args:
            task_id (TaskID): a task ID.
            status_extra (str): a little extra message to add.

        """
        with self._lock:
            task = self._tasks[task_id]
            self.update(task_id, completed=task.total, status="WARNING",
                        refresh=False, status_extra=status_extra)

    def complete_task(self, task_id, status_extra=""):
        """Complete a task with OK status.

        Args:
            task_id (TaskID): a task ID.
            status_extra (str): a little extra message to add.

        """
        with self._lock:
            task = self._tasks[task_id]
            self.update(task_id, completed=task.total, status="OK",
                        refresh=False, status_extra=status_extra)

    def stop(self):
        if self._interactive:
            return Progress.stop(self)
        else:
            with self._lock:
                for tid, task in self._tasks.items():
                    status = ""
                    extra = task.fields.get('status_extra', '')
                    if len(extra) > 0:
                        extra = " (%s)" % extra
                    if task.finished:
                        if task.fields.get('status', 'OK') == 'OK':
                            status = "OK"
                        elif task.fields.get('status', 'OK') == 'WARNING':
                            status = "WARNING"
                        else:
                            status = "ERROR"
                    print("%s [ %s ]%s" % (task.description, status, extra),
                          file=self.console.file)

    def refresh(self, *args, **kwargs):
        if self._interactive:
            return Progress.refresh(self, *args, **kwargs)
