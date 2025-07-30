#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Policies for locating inline copies."""

import os

from qutayba.PythonVersions import python_version


def _getInlineCopyBaseFolder():
    """Base folder for inline copies."""
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "build", "inline_copy")
    )


def getInlineCopyFolder(module_name):
    """Get the inline copy folder for a given name."""
    folder_name = os.path.join(_getInlineCopyBaseFolder(), module_name)

    candidate_27 = folder_name + "_27"
    candidate_35 = folder_name + "_35"

    # Use specific versions if needed.
    if python_version < 0x300 and os.path.exists(candidate_27):
        folder_name = candidate_27
    elif python_version < 0x360 and os.path.exists(candidate_35):
        folder_name = candidate_35

    return folder_name


def getDownloadCopyFolder():
    """Get the inline copy folder for a given name."""
    return os.path.join(_getInlineCopyBaseFolder(), "downloads", "pip")



