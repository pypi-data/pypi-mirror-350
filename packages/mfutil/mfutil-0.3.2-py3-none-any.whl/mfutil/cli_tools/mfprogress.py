#!/usr/bin/env python3

import argparse
import threading
import time
import sys
import os
from mfutil.cli import MFProgress
from mfutil.misc import kill_process_and_children
from mfutil.bash_wrapper import BashWrapper
import rich
import psutil
from rich.panel import Panel

DESCRIPTION = "execute a command with a nice progressbar"
TIMEOUT_FLAG = False
STOP_FLAG = False


def thread_advance(progress, tid, timeout):
    global TIMEOUT_FLAG
    i = 1
    while i <= timeout and not STOP_FLAG:
        if i < timeout:
            progress.update(tid, advance=1)
        time.sleep(1)
        i = i + 1
    if not STOP_FLAG:
        # timeout
        TIMEOUT_FLAG = True
        current_pid = os.getpid()
        process = psutil.Process(current_pid)
        children = process.children(recursive=False)
        [kill_process_and_children(x.pid) for x in children]


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("COMMAND", help="command to execute")
    parser.add_argument("COMMAND_ARG", nargs='*',
                        help="command arg")
    parser.add_argument("--timeout",
                        help="timeout (in seconds)", type=int,
                        default=180)
    parser.add_argument("--title",
                        help="title of the command", type=str,
                        default="title of the command")
    parser.add_argument("--silent", action="store_true",
                        help="if set, we don't add a debug output in case of "
                        "errors")
    args = parser.parse_args()

    command = " ".join([args.COMMAND] + args.COMMAND_ARG)

    status = True
    timeout = False
    with MFProgress() as progress:
        t = progress.add_task(args.title, total=args.timeout)
        x = threading.Thread(target=thread_advance, args=(progress, t,
                                                          args.timeout),
                             daemon=True)
        x.start()
        bw = BashWrapper(command)
        STOP_FLAG = True  # noqa:
        if bw:
            progress.complete_task(t)
        else:
            if TIMEOUT_FLAG:
                # timeout
                progress.complete_task_nok(t, "timeout")
                timeout = True
            else:
                progress.complete_task_nok(t, "bad exit code")
            status = False
    if not status:
        if not args.silent and not timeout:
            rich.print(Panel("[bold]Error details:[/bold]\n%s" %  # noqa: E999
                             str(bw)))
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
