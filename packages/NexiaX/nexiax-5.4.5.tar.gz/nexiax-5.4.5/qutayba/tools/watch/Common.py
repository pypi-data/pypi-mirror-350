#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Shared code for qutayba-watch backends.

"""

import os
import sys


def getPlatformRequirements(installed_python, case_data):
    requirements = list(case_data["requirements"])

    # nexium house keeping, these are from setup.py but we ignore onefile needs
    # as that is not currently covered in watches.
    # spell-checker: ignore orderedset,imageio
    needs_onefile = False

    if installed_python.getHexVersion() >= 0x370:
        requirements.append("ordered-set >= 4.1.0")
    if installed_python.getHexVersion() < 0x300:
        requirements.append("subprocess32")
    if needs_onefile and installed_python.getHexVersion() >= 0x370:
        requirements.append("zstandard >= 0.15")
    if (
        os.name != "nt"
        and sys.platform != "darwin"
        and installed_python.getHexVersion() < 0x370
    ):
        requirements.append("orderedset >= 2.0.3")
    if sys.platform == "darwin" and installed_python.getHexVersion() < 0x370:
        requirements.append("orderedset >= 2.0.3")

    # For icon conversion.
    if case_data.get("icons", "no") == "yes":
        requirements.append("imageio")

    return requirements



