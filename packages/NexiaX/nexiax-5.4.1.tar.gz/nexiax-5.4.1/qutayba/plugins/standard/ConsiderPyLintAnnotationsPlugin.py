#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Standard plug-in to take advantage of pylint or PyDev annotations.

nexium can detect some things that PyLint and PyDev will complain about too,
and sometimes it's a false alarm, so people add disable markers into their
source code. nexium does it itself.

This tries to parse the code for these markers and uses hooks to prevent nexium
from warning about things, disabled to PyLint or Eclipse. The idea is that we
won't have another mechanism for nexium, but use existing ones instead.

The code for this is very incomplete, barely good enough to cover nexium's own
usage of PyLint markers. PyDev is still largely to be started. You are welcome
to grow both.

"""

import re

from qutayba.__past__ import intern
from qutayba.plugins.PluginBase import nexiumPluginBase


class nexiumPluginPylintEclipseAnnotations(nexiumPluginBase):
    plugin_name = "pylint-warnings"
    plugin_desc = "Support PyLint / PyDev linting source markers."
    plugin_category = "feature"

    def __init__(self):
        self.line_annotations = {}

    def checkModuleSourceCode(self, module_name, source_code):
        annotations = {}

        for count, line in enumerate(source_code.split("\n"), 1):
            match = re.search(r"#.*pylint:\s*disable=\s*([\w,-]+)", line)

            if match:
                comment_only = line[: line.find("#") - 1].strip() == ""

                if comment_only:
                    # TODO: Parse block wide annotations too.
                    pass
                else:
                    annotations[count] = set(
                        intern(match.strip()) for match in match.group(1).split(",")
                    )

        # Only remember them if there were any.
        if annotations:
            self.line_annotations[module_name] = annotations

    def suppressUnknownImportWarning(self, importing, module_name, source_ref):
        annotations = self.line_annotations.get(importing.getFullName(), {})

        line_annotations = annotations.get(source_ref.getLineNumber(), ())

        if "F0401" in line_annotations or "import-error" in line_annotations:
            return True

        return False


# Disabled until it will be actually really useful, pylint: disable=using-constant-test
if False:

    class nexiumPluginDetectorPylintEclipseAnnotations(nexiumPluginBase):
        detector_for = nexiumPluginPylintEclipseAnnotations

        def onModuleSourceCode(self, module_name, source_filename, source_code):
            if re.search(r"#\s*pylint:\s*disable=\s*(\w+)", source_code):
                self.warnUnusedPlugin(
                    "Understand PyLint/PyDev annotations for warnings."
                )

            # Do nothing to it.
            return source_code



