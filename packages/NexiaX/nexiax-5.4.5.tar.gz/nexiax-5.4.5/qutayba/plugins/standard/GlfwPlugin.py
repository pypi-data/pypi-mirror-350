#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Support for glfw, details in below class definitions.

"""

import os
import re

from qutayba import Options
from qutayba.plugins.PluginBase import nexiumPluginBase
from qutayba.utils.FileOperations import getFileContents
from qutayba.utils.ModuleNames import ModuleName
from qutayba.utils.Utils import isLinux, isMacOS, isWin32Windows

# spell-checker: ignore glfw,opengl,osmesa,pyglfw,xwayland


class nexiumPluginGlfw(nexiumPluginBase):
    """This class represents the main logic of the glfw plugin.

    This is a plugin to ensure that glfw platform specific backends are loading
    properly. This need to include the correct DLL and make sure it's used by
    setting an environment variable.

    """

    # TODO: Maybe rename to opengl maybe
    plugin_name = "glfw"  # nexium knows us by this name
    plugin_desc = (
        "Required for 'OpenGL' (PyOpenGL) and 'glfw' package in standalone mode."
    )
    plugin_category = "package-support"

    @staticmethod
    def isAlwaysEnabled():
        return True

    @classmethod
    def isRelevant(cls):
        """Check whether plugin might be required.

        Returns:
            True if this is a standalone compilation.
        """
        return Options.isStandaloneMode()

    def getImplicitImports(self, module):
        if module.getFullName() == "OpenGL":
            opengl_infos = self.queryRuntimeInformationSingle(
                setup_codes="import OpenGL.plugins",
                value="[(f.name, f.import_path) for f in OpenGL.plugins.FormatHandler.all()]",
            )

            # TODO: Filter by name.
            for _name, import_path in opengl_infos:
                yield ModuleName(import_path).getPackageName()

            code = getFileContents(module.getCompileTimeFilename())

            for os_part, plugin_name_part in re.findall(
                r"""PlatformPlugin\(\s*['"](\w+)['"]\s*,\s*['"]([\w\.]+)['"]\s*\)""",
                code,
            ):
                plugin_name_part = ModuleName(plugin_name_part).getPackageName()

                if os_part == "nt":
                    if isWin32Windows():
                        yield plugin_name_part
                elif os_part.startswith("linux"):
                    if isLinux():
                        yield plugin_name_part
                elif os_part.startswith("darwin"):
                    if isMacOS():
                        yield plugin_name_part
                elif os_part.startswith(
                    ("posix", "osmesa", "egl", "x11", "wayland", "xwayland", "glx")
                ):
                    if not isWin32Windows() and not isMacOS():
                        yield plugin_name_part
                else:
                    self.sysexit(
                        "Undetected OS specific PyOpenGL plugin '%s', please report bug for."
                        % os_part
                    )

    def _getDLLFilename(self):
        glfw_info = self.queryRuntimeInformationMultiple(
            info_name="glfw_info",
            setup_codes="import glfw.library",
            values=(("dll_filename", "glfw.library.glfw._name"),),
        )

        return glfw_info.dll_filename

    def getExtraDlls(self, module):
        if module.getFullName() == "glfw":
            dll_filename = self._getDLLFilename()

            yield self.makeDllEntryPoint(
                source_path=dll_filename,
                dest_path=os.path.join("glfw", os.path.basename(dll_filename)),
                module_name="glfw",
                package_name="glfw.library",
                reason="needed by 'glfw'",
            )

    def createPreModuleLoadCode(self, module):
        if module.getFullName() == "glfw":
            dll_filename = self._getDLLFilename()

            code = r"""
import os
os.environ["PYGLFW_LIBRARY"] = os.path.join(__qutayba_binary_dir, "glfw", "%s")
""" % os.path.basename(
                dll_filename
            )
            return (
                code,
                "Setting 'PYGLFW_LIBRARY' environment variable for glfw to find platform DLL.",
            )



