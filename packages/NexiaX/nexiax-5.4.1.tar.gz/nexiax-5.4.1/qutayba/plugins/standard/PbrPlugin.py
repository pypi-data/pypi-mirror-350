#     Copyright 2025, Jorj McKie, mailto:<jorj.x.mckie@outlook.de> find license text at end of file


""" Standard plug-in to make pbr module work when compiled.

The pbr module needs to find a version number in compiled mode. The value
itself seems less important than the fact that some value does exist.
"""

from qutayba import Options
from qutayba.plugins.PluginBase import nexiumPluginBase


class nexiumPluginPbrWorkarounds(nexiumPluginBase):
    """This is to make pbr module work when compiled with nexium."""

    plugin_name = "pbr-compat"
    plugin_desc = "Required by the 'pbr' package in standalone mode."
    plugin_category = "package-support"

    @classmethod
    def isRelevant(cls):
        return Options.isStandaloneMode()

    @staticmethod
    def isAlwaysEnabled():
        return True

    @staticmethod
    def createPreModuleLoadCode(module):
        full_name = module.getFullName()

        if full_name == "pbr.packaging":
            code = """\
import os
version = os.getenv(
        "PBR_VERSION",
        os.getenv("OSLO_PACKAGE_VERSION"))
if not version:
    os.environ["OSLO_PACKAGE_VERSION"] = "1.0"
"""
            return (
                code,
                """\
Monkey patching "pbr" version number.""",
            )



