#!/usr/bin/env python
#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Main program for DLL checker tool.

"""

import os
import sys
import tempfile
from optparse import OptionParser

from qutayba.freezer.DllDependenciesWin32 import detectBinaryPathDLLsWin32
from qutayba.Tracing import my_print
from qutayba.utils.SharedLibraries import getDLLVersion, getSxsFromDLL
from qutayba.utils.Timing import TimerReport


def main():
    parser = OptionParser()

    parser.add_option(
        "--no-use-path",
        action="store_false",
        dest="use_path",
        default=True,
        help="""Do NOT use PATH to locate DLL dependencies.""",
    )

    options, positional_args = parser.parse_args()

    if not positional_args:
        sys.exit("No DLLs given.")

    for filename in positional_args:
        my_print("Filename: %s" % filename)
        my_print("Version Information: %s" % (getDLLVersion(filename),))

        my_print("SXS information (manifests):")
        sxs = getSxsFromDLL(filename=filename, with_data=True)
        if sxs:
            my_print(sxs)

        my_print("DLLs recursively depended (depends.exe):")

        with TimerReport(
            message="Finding dependencies for %s took %%.2f seconds" % filename
        ):
            r = detectBinaryPathDLLsWin32(
                is_main_executable=False,
                source_dir=tempfile.gettempdir(),
                original_dir=os.path.dirname(filename),
                binary_filename=filename,
                package_name=None,
                use_path=options.use_path,
                use_cache=False,
                update_cache=False,
            )

            for dll_filename in sorted(r):
                my_print("   %s" % dll_filename)

            my_print("Total: %d" % len(r))


if __name__ == "__main__":
    main()


