#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Access package data. """

import os
import pkgutil

from qutayba.importing.Importing import locateModule

from .FileOperations import getFileContents


def getPackageData(package_name, resource):
    """Get the package data, but without loading the code, i.e. we try and avoids its loader.

    If it's absolutely necessary, we fallback to "pkgutil.get_data" but
    only if we absolutely cannot find it easily.
    """
    package_directory = locateModule(package_name, None, 0)[1]

    if package_directory is not None:
        resource_filename = os.path.join(package_directory, resource)

        if os.path.exists(resource_filename):
            return getFileContents(resource_filename, mode="rb")

    return pkgutil.get_data(package_name.asString(), resource)



