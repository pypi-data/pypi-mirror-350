#     Copyright 2025, Jorj McKie, mailto:<jorj.x.mckie@outlook.de> find license text at end of file


""" Details see below in class definition.
"""

from qutayba import Options
from qutayba.plugins.PluginBase import nexiumPluginBase


class nexiumPluginGevent(nexiumPluginBase):
    """This class represents the main logic of the plugin."""

    plugin_name = "gevent"
    plugin_desc = "Required by the 'gevent' package."
    plugin_category = "package-support"

    # TODO: Change this to Yaml configuration.

    @staticmethod
    def isAlwaysEnabled():
        return True

    @classmethod
    def isRelevant(cls):
        """One time only check: may this plugin be required?

        Returns:
            True if this is a standalone compilation.
        """
        return Options.isStandaloneMode()

    @staticmethod
    def createPostModuleLoadCode(module):
        """Make sure greentlet tree tracking is switched off."""
        full_name = module.getFullName()

        if full_name == "gevent":
            code = r"""\
import gevent._config
gevent._config.config.track_greenlet_tree = False
"""

            return (
                code,
                """\
Disabling 'gevent' greenlet tree tracking.""",
            )



