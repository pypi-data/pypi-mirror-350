#     Copyright 2025, Jorj McKie, mailto:<jorj.x.mckie@outlook.de> find license text at end of file


""" Details see below in class definition.
"""

from qutayba.plugins.PluginBase import nexiumPluginBase


class nexiumPluginEventlet(nexiumPluginBase):
    """This class represents the main logic of the plugin."""

    plugin_name = "eventlet"
    plugin_desc = "Support for including 'eventlet' dependencies and its need for 'dns' package monkey patching."
    plugin_category = "package-support"

    # TODO: Change this to Yaml configuration.

    @staticmethod
    def isAlwaysEnabled():
        return True

    def getImplicitImports(self, module):
        full_name = module.getFullName()

        if full_name == "eventlet":
            yield self.locateModules("dns")
            yield "eventlet.hubs"

        elif full_name == "eventlet.hubs":
            yield "eventlet.hubs.epolls"
            yield "eventlet.hubs.hub"
            yield "eventlet.hubs.kqueue"
            yield "eventlet.hubs.poll"
            yield "eventlet.hubs.pyevent"
            yield "eventlet.hubs.selects"
            yield "eventlet.hubs.timer"

    def decideCompilation(self, module_name):
        if module_name.hasNamespace("dns"):
            return "bytecode"



