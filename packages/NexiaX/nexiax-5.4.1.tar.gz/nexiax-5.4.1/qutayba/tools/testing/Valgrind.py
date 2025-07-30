#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Valgrind tool usage.

We are using it for benchmarking purposes, as it's an analysis tool at the
same time and gives deterministic results.
"""

import sys

from qutayba.Tracing import my_print
from qutayba.utils.Execution import check_output, executeProcess
from qutayba.utils.FileOperations import (
    copyFile,
    getFileContentByLine,
    withTemporaryFile,
)
from qutayba.utils.Utils import isWin32Windows


def runValgrind(descr, tool, args, include_startup, save_logfilename=None):
    # Many cases to deal with, pylint: disable=too-many-branches

    if isWin32Windows():
        sys.exit("Error, valgrind is not available on Windows.")

    if descr:
        my_print(descr, tool, file=sys.stderr, end="... ")

    with withTemporaryFile() as log_file:
        log_filename = log_file.name

        command = ["valgrind", "-q"]

        if tool == "callgrind":
            command += ("--tool=callgrind", "--callgrind-out-file=%s" % log_filename)
        elif tool == "massif":
            command += ("--tool=massif", "--massif-out-file=%s" % log_filename)
        else:
            sys.exit("Error, no support for tool '%s' yet." % tool)

        # Do not count things before main module starts its work.
        if not include_startup:
            command += (
                "--zero-before=init__main__()",
                "--zero-before=init__main__",
                "--zero-before=PyInit___main__",
                "--zero-before=PyInit___main__()",
            )

        command.extend(args)

        _stdout_valgrind, stderr_valgrind, exit_valgrind = executeProcess(command)

        assert exit_valgrind == 0, stderr_valgrind
        if descr:
            my_print("OK", file=sys.stderr)

        if save_logfilename is not None:
            copyFile(log_filename, save_logfilename)

        max_mem = None

        for line in getFileContentByLine(log_filename):
            if tool == "callgrind" and line.startswith("summary:"):
                return int(line.split()[1])
            elif tool == "massif" and line.startswith("mem_heap_B="):
                mem = int(line.split("=")[1])

                if max_mem is None:
                    max_mem = 0

                max_mem = max(mem, max_mem)

        if tool == "massif" and max_mem is not None:
            return max_mem

        sys.exit("Error, didn't parse Valgrind log file successfully.")


def getBinarySizes(filename):
    command = ["size", filename]
    sizes = check_output(command).strip()
    sizes = sizes.split(b"\n")[-1].replace(b"\t", b"").split()

    return int(sizes[0]), int(sizes[1])



