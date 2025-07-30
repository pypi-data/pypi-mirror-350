#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Generate header files that provide compiler specifics."""

from qutayba.build.SconsInterface import (
    cleanSconsDirectory,
    getCommonSconsOptions,
    runScons,
    setPythonTargetOptions,
)
from qutayba.PythonVersions import isPythonWithGil, python_version_str
from qutayba.Tracing import offsets_logger
from qutayba.utils.Execution import check_output
from qutayba.utils.FileOperations import makePath, withTemporaryFilename


def generateHeader():
    scons_options, env_values = getCommonSconsOptions()

    setPythonTargetOptions(scons_options)

    scons_options["source_dir"] = "generate_header.build"
    cleanSconsDirectory(scons_options["source_dir"])
    makePath(scons_options["source_dir"])

    python_version_id = "%s_%s" % (
        python_version_str,
        "gil" if isPythonWithGil() else "no-gil",
    )

    with withTemporaryFilename(prefix=python_version_id, suffix=".exe") as result_exe:
        scons_options["result_exe"] = result_exe

        runScons(
            scons_options=scons_options,
            env_values=env_values,
            scons_filename="Offsets.scons",
        )

        header_output = check_output([result_exe])

        if str is not bytes:
            header_output = header_output.decode("utf8")

        offsets_logger.info(repr(header_output))

        lines = header_output.splitlines()

        if lines[-1] != "OK.":
            offsets_logger.sysexit("Error, failed to produce expected output.")
        del lines[-1]

        for line in lines:
            offsets_logger.info("Processing: %s" % line)

        offsets_logger.info("OK.")



