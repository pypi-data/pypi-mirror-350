#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Pacman backend for maintaining locked package state with qutayba-watch. """

from qutayba.utils.Execution import check_call, executeToolChecked
from qutayba.utils.FileOperations import changeTextFileContents, openTextFile

from .Common import getPlatformRequirements


def updatePacmanFile(installed_python, case_data):
    pacman_filename = "Pacman.txt"
    pacman_package_requirements = []

    for requirement in getPlatformRequirements(
        installed_python=installed_python, case_data=case_data
    ):
        # Ignore spaces in requirements.
        requirement = requirement.replace(" ", "")

        pacman_package_requirements.append(requirement)

    changeTextFileContents(
        pacman_filename,
        """\
%(python_version)s
%(pacman_package_requirements)s
"""
        % {
            "pacman_package_requirements": "\n".join(pacman_package_requirements),
            "python_version": installed_python.getPythonVersion(),
        },
    )

    return pacman_filename


def updatePacmanLockFile(logger):
    pacman_lock_filename = "Pacman.lock"

    with openTextFile("Pacman.txt", "r") as pacman_env_file:
        check_call(["pacman", "-S", "-"], stdin=pacman_env_file)

    pacman_output = executeToolChecked(
        logger=logger,
        command=["pacman", "-Qe"],
        absence_message="needs pacman to query package status on MSYS2",
        decoding=str is not bytes,
    )
    pacman_output = "\n".join(
        line.replace(" ", "=") for line in pacman_output.splitlines()
    )

    changeTextFileContents(filename=pacman_lock_filename, contents=pacman_output)

    return pacman_lock_filename



