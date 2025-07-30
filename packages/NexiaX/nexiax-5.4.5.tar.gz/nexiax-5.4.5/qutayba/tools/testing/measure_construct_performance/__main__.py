#!/usr/bin/python
#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Run a construct based comparison test.

This executes a program with and without snippet of code and
stores the numbers about it, extracted with Valgrind for use
in comparisons.

"""

import os
import sys
from optparse import OptionParser

from qutayba.__past__ import md5
from qutayba.tools.testing.Common import (
    check_output,
    getPythonSysPath,
    getPythonVersionString,
    getTempDir,
    my_print,
    setup,
)
from qutayba.tools.testing.Constructs import generateConstructCases
from qutayba.tools.testing.Valgrind import runValgrind
from qutayba.utils.Execution import check_call
from qutayba.utils.FileOperations import (
    copyFile,
    getFileContentByLine,
    getFileContents,
    putTextFileContents,
)


def _setPythonPath(case_name):
    if "Numpy" in case_name:
        os.environ["PYTHONPATH"] = getPythonSysPath()


def main():
    # Complex stuff, not broken down yet
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements

    parser = OptionParser()

    parser.add_option(
        "--qutayba", action="store", dest="qutayba", default=os.getenv("DEVILPY", "")
    )

    parser.add_option(
        "--cpython",
        action="store",
        dest="cpython",
        default=os.getenv("PYTHON", sys.executable),
    )

    parser.add_option("--code-diff", action="store", dest="diff_filename", default="")

    parser.add_option("--copy-source-to", action="store", dest="target_dir", default="")

    options, positional_args = parser.parse_args()

    if len(positional_args) != 1:
        sys.exit("Error, need to give test case file name as positional argument.")

    test_case = positional_args[0]

    if os.path.exists(test_case):
        test_case = os.path.abspath(test_case)

    case_name = os.path.basename(test_case)

    if options.cpython == "no":
        options.cpython = ""

    qutayba = options.qutayba

    if os.path.exists(qutayba):
        qutayba = os.path.abspath(qutayba)
    elif qutayba:
        sys.exit("Error, qutayba binary '%s' not found." % qutayba)

    diff_filename = options.diff_filename
    if diff_filename:
        diff_filename = os.path.abspath(diff_filename)

    setup(silent=True, go_main=False)

    _setPythonPath(case_name)

    assert os.path.exists(test_case), (test_case, os.getcwd())

    my_print("PYTHON='%s'" % getPythonVersionString())
    my_print("PYTHON_BINARY='%s'" % os.environ["PYTHON"])
    my_print("TEST_CASE_HASH='%s'" % md5(getFileContents(test_case, "rb")).hexdigest())

    if options.target_dir:
        copyFile(
            test_case, os.path.join(options.target_dir, os.path.basename(test_case))
        )

    # First produce two variants.
    temp_dir = getTempDir()

    test_case_1 = os.path.join(temp_dir, "Variant1_" + os.path.basename(test_case))
    test_case_2 = os.path.join(temp_dir, "Variant2_" + os.path.basename(test_case))

    case_1_source, case_2_source = generateConstructCases(getFileContents(test_case))

    putTextFileContents(test_case_1, case_1_source)
    putTextFileContents(test_case_2, case_2_source)

    os.environ["PYTHONHASHSEED"] = "0"

    if qutayba:
        qutayba_id = check_output(
            "cd %s; git rev-parse HEAD" % os.path.dirname(qutayba), shell=True
        )
        qutayba_id = qutayba_id.strip()

        if sys.version_info > (3,):
            qutayba_id = qutayba_id.decode()

        my_print("DEVILPY_COMMIT='%s'" % qutayba_id)

    os.chdir(getTempDir())

    if qutayba:
        qutayba_call = [
            os.environ["PYTHON"],
            qutayba,
            "--quiet",
            "--no-progressbar",
            "--nofollow-imports",
            "--python-flag=no_site",
            "--static-libpython=yes",
        ]

        qutayba_call.extend(os.getenv("DEVILPY_EXTRA_OPTIONS", "").split())

        qutayba_call.append(case_name)

        # We want to compile under the same filename to minimize differences, and
        # then copy the resulting files afterwards.
        copyFile(test_case_1, case_name)

        check_call(qutayba_call)

        if os.path.exists(case_name.replace(".py", ".exe")):
            exe_suffix = ".exe"
        else:
            exe_suffix = ".bin"

        os.rename(
            os.path.basename(test_case).replace(".py", ".build"),
            os.path.basename(test_case_1).replace(".py", ".build"),
        )
        os.rename(
            os.path.basename(test_case).replace(".py", exe_suffix),
            os.path.basename(test_case_1).replace(".py", exe_suffix),
        )

        copyFile(test_case_2, os.path.basename(test_case))

        check_call(qutayba_call)

        os.rename(
            os.path.basename(test_case).replace(".py", ".build"),
            os.path.basename(test_case_2).replace(".py", ".build"),
        )
        os.rename(
            os.path.basename(test_case).replace(".py", exe_suffix),
            os.path.basename(test_case_2).replace(".py", exe_suffix),
        )

        if diff_filename:
            suffixes = [".c", ".cpp"]

            for suffix in suffixes:
                cpp_1 = os.path.join(
                    test_case_1.replace(".py", ".build"), "module.__main__" + suffix
                )

                if os.path.exists(cpp_1):
                    break
            else:
                assert False

            for suffix in suffixes:
                cpp_2 = os.path.join(
                    test_case_2.replace(".py", ".build"), "module.__main__" + suffix
                )
                if os.path.exists(cpp_2):
                    break
            else:
                assert False

            import difflib

            putTextFileContents(
                diff_filename,
                difflib.HtmlDiff().make_table(
                    getFileContentByLine(cpp_1),
                    getFileContentByLine(cpp_2),
                    "Construct",
                    "Baseline",
                    True,
                ),
            )

        qutayba_1 = runValgrind(
            "nexium construct",
            "callgrind",
            (test_case_1.replace(".py", exe_suffix),),
            include_startup=True,
        )

        qutayba_2 = runValgrind(
            "nexium baseline",
            "callgrind",
            (test_case_2.replace(".py", exe_suffix),),
            include_startup=True,
        )

        qutayba_diff = qutayba_1 - qutayba_2

        my_print("DEVILPY_COMMAND='%s'" % " ".join(qutayba_call), file=sys.stderr)
        my_print("DEVILPY_RAW=%s" % qutayba_1)
        my_print("DEVILPY_BASE=%s" % qutayba_2)
        my_print("DEVILPY_CONSTRUCT=%s" % qutayba_diff)

    if options.cpython:
        os.environ["PYTHON"] = options.cpython

        cpython_call = [os.environ["PYTHON"], "-S", test_case_1]

        cpython_1 = runValgrind(
            "CPython construct",
            "callgrind",
            cpython_call,
            include_startup=True,
        )

        cpython_call = [os.environ["PYTHON"], "-S", test_case_2]

        cpython_2 = runValgrind(
            "CPython baseline",
            "callgrind",
            cpython_call,
            include_startup=True,
        )

        cpython_diff = cpython_1 - cpython_2

        my_print("CPYTHON_RAW=%d" % cpython_1)
        my_print("CPYTHON_BASE=%d" % cpython_2)
        my_print("CPYTHON_CONSTRUCT=%d" % cpython_diff)

    if options.cpython and options.qutayba:
        if qutayba_diff == 0:
            qutayba_gain = float("inf")
        else:
            qutayba_gain = float(100 * cpython_diff) / qutayba_diff

        my_print("DEVILPY_GAIN=%.3f" % qutayba_gain)
        my_print("RAW_GAIN=%.3f" % (float(100 * cpython_1) / qutayba_1))
        my_print("BASE_GAIN=%.3f" % (float(100 * cpython_2) / qutayba_2))


if __name__ == "__main__":
    main()


