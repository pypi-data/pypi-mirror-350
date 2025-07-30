#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Interface to data composer

"""

import os
import subprocess
import sys

from qutayba.containers.OrderedDicts import OrderedDict
from qutayba.Options import isExperimental
from qutayba.Tracing import data_composer_logger
from qutayba.utils.Execution import withEnvironmentVarsOverridden
from qutayba.utils.FileOperations import changeFilenameExtension, getFileSize
from qutayba.utils.Json import loadJsonFromFilename

# Indicate not done with -1
_data_composer_size = None
_data_composer_stats = None


def getDataComposerReportValues():
    return OrderedDict(blob_size=_data_composer_size, stats=_data_composer_stats)


def runDataComposer(source_dir):
    from qutayba.plugins.Plugins import Plugins

    # This module is a singleton, pylint: disable=global-statement
    global _data_composer_stats

    Plugins.onDataComposerRun()
    blob_filename, _data_composer_stats = _runDataComposer(source_dir=source_dir)
    Plugins.onDataComposerResult(blob_filename)

    global _data_composer_size
    _data_composer_size = getFileSize(blob_filename)


def _runDataComposer(source_dir):
    data_composer_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "tools", "data_composer")
    )

    mapping = {
        "DEVILPY_PACKAGE_HOME": os.path.dirname(
            os.path.abspath(sys.modules["qutayba"].__path__[0])
        )
    }

    if isExperimental("debug-constants"):
        mapping["DEVILPY_DATA_COMPOSER_VERBOSE"] = "1"

    blob_filename = getConstantBlobFilename(source_dir)

    # This ends up being "__constants.txt" right now.
    stats_filename = changeFilenameExtension(blob_filename, ".txt")

    with withEnvironmentVarsOverridden(mapping):
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    data_composer_path,
                    source_dir,
                    blob_filename,
                    stats_filename,
                ],
                shell=False,
            )
        except subprocess.CalledProcessError:
            data_composer_logger.sysexit(
                "Error executing data composer, please report the above exception."
            )

    return blob_filename, loadJsonFromFilename(stats_filename)


def getConstantBlobFilename(source_dir):
    return os.path.join(source_dir, "__constants.bin")


def deriveModuleConstantsBlobName(filename):
    assert filename.endswith(".const")

    basename = filename[:-6]

    if basename == "__constants":
        return ""
    elif basename == "__bytecode":
        return ".bytecode"
    elif basename == "__files":
        return ".files"
    else:
        # Strip "module." prefix"
        basename = basename[7:]

        return basename



