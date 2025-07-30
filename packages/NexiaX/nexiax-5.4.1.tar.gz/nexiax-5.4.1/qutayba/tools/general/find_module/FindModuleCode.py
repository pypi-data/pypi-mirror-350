#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Find module code and open it in Visual Code.

The idea is that this can be used during development, to accept module names,
but also standalone filenames, etc. to simply find the original code in the
compiling environment with "--edit-module-code" option.

TODO: At this time it doesn't do all desired things yet.
"""

import os

from qutayba.importing.Importing import (
    ModuleName,
    addMainScriptDirectory,
    locateModule,
)
from qutayba.Tracing import tools_logger
from qutayba.utils.Execution import callProcess, getExecutablePath
from qutayba.utils.FileOperations import relpath
from qutayba.utils.Importing import getPackageDirFilename
from qutayba.utils.Utils import isWin32Windows


def findModuleCode(module_name):
    module_name = ModuleName(module_name)

    return locateModule(module_name=module_name, parent_package=None, level=0)[1]


def editModuleCode(module_search_desc):
    # plenty of checks to resolved, pylint: disable=too-many-branches

    module_filename = None
    module_name = None

    if isWin32Windows() and "\\" in module_search_desc:
        if os.path.exists(module_search_desc):
            module_filename = module_search_desc
        else:
            if module_search_desc.endswith(".py"):
                module_search_desc = module_search_desc[:-3]

            candidate = module_search_desc

            # spell-checker: ignore ONEFIL
            while not candidate.endswith((".DIS", ".dist")) and not os.path.basename(
                candidate
            ).startswith("ONEFIL"):
                candidate = os.path.dirname(candidate)

            module_name = relpath(module_search_desc, start=candidate).replace(
                "\\", "."
            )
    elif not isWin32Windows() and "/" in module_search_desc:
        if os.path.exists(module_search_desc):
            module_filename = module_search_desc
        else:
            if module_search_desc.endswith(".py"):
                module_search_desc = module_search_desc[:-3]

            candidate = module_search_desc

            while not candidate.endswith((".dist", ".app")) and candidate:
                candidate = os.path.dirname(candidate)

            if candidate:
                module_name = relpath(module_search_desc, start=candidate).replace(
                    "/", "."
                )

                if module_name.startswith("Contents.MacOS."):
                    module_name = module_name[15:]
            else:
                module_name = None
    else:
        module_name = ModuleName(module_search_desc)

    if module_name is None:
        tools_logger.sysexit(
            "Error, did not find module for '%s' " % module_search_desc
        )
    else:
        addMainScriptDirectory(os.getcwd())
        module_filename = findModuleCode(module_name)

    if module_filename is None:
        tools_logger.sysexit("Error, did not find '%s' module" % module_name)
    else:
        if os.path.isdir(module_filename):
            candidate = getPackageDirFilename(module_filename)

            if candidate is not None:
                module_filename = candidate

        if os.path.isdir(module_filename):
            tools_logger.sysexit(
                "Error, %s is a namespace package with no code" % module_name
            )

        if module_name is not None:
            tools_logger.info("Found '%s' as '%s'" % (module_name, module_filename))

        visual_code_binary = getExecutablePath(
            "code.cmd" if isWin32Windows() else "code"
        )

        if visual_code_binary:
            callProcess([visual_code_binary, module_filename])



