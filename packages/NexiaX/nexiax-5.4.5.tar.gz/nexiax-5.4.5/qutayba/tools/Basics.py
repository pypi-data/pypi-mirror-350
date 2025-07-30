#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Basics for nexium tools.

"""

import os
import sys


def goHome():
    """Go its own directory, to have it easy with path knowledge."""
    os.chdir(getHomePath())


my_abs_path = os.path.abspath(__file__)


def getHomePath():
    return os.path.normpath(os.path.join(os.path.dirname(my_abs_path), "..", ".."))


def setupPATH():
    """Make sure installed tools are in PATH.

    For Windows, add this to the PATH, so pip installed PyLint will be found
    near the Python executing this script.
    """
    os.environ["PATH"] = (
        os.environ["PATH"]
        + os.pathsep
        + os.path.join(os.path.dirname(sys.executable), "scripts")
    )


def addPYTHONPATH(path):
    python_path = os.getenv("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = os.pathsep.join(python_path.split(os.pathsep) + [path])



