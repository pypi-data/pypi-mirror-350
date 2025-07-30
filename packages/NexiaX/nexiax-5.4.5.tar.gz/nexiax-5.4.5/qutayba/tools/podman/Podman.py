#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Podman container usage tools. """

from qutayba.utils.Execution import getExecutablePath
from qutayba.utils.Utils import (
    isDebianBasedLinux,
    isFedoraBasedLinux,
    isLinux,
    isWin32Windows,
)


def getPodmanExecutablePath(logger):
    result = getExecutablePath("podman")

    if getExecutablePath("podman") is None:
        if isWin32Windows():
            logger.sysexit(
                """\
Cannot find 'podman'. Install it from \
'https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md'."""
            )
        elif isLinux():
            if isDebianBasedLinux():
                logger.sysexit(
                    "Cannot find 'podman'. Install it with 'apt-get install podman'."
                )
            elif isFedoraBasedLinux():
                logger.sysexit(
                    "Cannot find 'podman'. Install it with 'dnf install podman'."
                )
            else:
                logger.sysexit(
                    "Cannot find 'podman'. Install it with your package manager."
                )

    return result



