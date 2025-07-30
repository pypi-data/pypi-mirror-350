#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Test tool to run a program with various Pythons. """

from qutayba.PythonVersions import getSupportedPythonVersions
from qutayba.utils.Execution import check_output
from qutayba.utils.InstalledPythons import findPythons


def findAllPythons():
    for python_version in getSupportedPythonVersions():
        for python in findPythons(python_version):
            yield python, python_version


def executeWithInstalledPython(python, args):
    return check_output([python.getPythonExe()] + args)



