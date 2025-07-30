#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Plugin for spacy.

spell-checker: ignore spacy
"""

from qutayba.code_generation.ConstantCodes import addDistributionMetadataValue
from qutayba.containers.OrderedSets import OrderedSet
from qutayba.Options import isStandaloneMode
from qutayba.plugins.PluginBase import nexiumPluginBase
from qutayba.utils.Distributions import getEntryPointGroup
from qutayba.utils.ModuleNames import ModuleName


class nexiumPluginSpacy(nexiumPluginBase):
    """This class represents the main logic of the plugin."""

    plugin_name = "spacy"
    plugin_desc = "Required by 'spacy' package."
    plugin_category = "package-support"

    def __init__(self, include_language_models):
        self.include_language_models = tuple(
            ModuleName(include_language_model)
            for include_language_model in include_language_models
        )
        self.available_language_models = None

        self.used_language_model_names = None

    @staticmethod
    def isAlwaysEnabled():
        return True

    @staticmethod
    def isRelevant():
        return isStandaloneMode()

    @classmethod
    def addPluginCommandLineOptions(cls, group):
        group.add_option(
            "--spacy-language-model",
            action="append",
            dest="include_language_models",
            default=[],
            help="""\
Spacy language models to use. Can be specified multiple times. Use 'all' to
include all downloaded models.""",
        )

    def _getInstalledSpaceLanguageModels(self):
        if self.available_language_models is None:
            self.available_language_models = tuple(
                entry_point.module_name
                for entry_point in sorted(getEntryPointGroup("spacy_models"))
            )

        return self.available_language_models

    def getImplicitImports(self, module):
        if module.getFullName() == "spacy":
            self.used_language_model_names = OrderedSet()

            if "all" in self.include_language_models:
                self.used_language_model_names.update(
                    self._getInstalledSpaceLanguageModels()
                )
            else:
                for include_language_model_name in self.include_language_models:
                    if (
                        include_language_model_name
                        in self._getInstalledSpaceLanguageModels()
                    ):
                        self.used_language_model_names.add(include_language_model_name)
                    else:
                        self.sysexit(
                            """\
Error, requested to include language model '%s' that was \
not found, the list of installed ones is '%s'."""
                            % (
                                include_language_model_name,
                                ",".join(self._getInstalledSpaceLanguageModels()),
                            )
                        )

            if not self.used_language_model_names:
                self.warning(
                    """\
No language models included. Use the option '--spacy-language-model=language_model_name' to \
include one. Use 'all' to include all downloaded ones, or select from the list of installed \
ones: %s"""
                    % ",".join(self._getInstalledSpaceLanguageModels())
                )

            for used_language_model_name in self.used_language_model_names:
                yield used_language_model_name

    def considerDataFiles(self, module):
        if module.getFullName() == "spacy":
            # Do not use it accidentally for anything else
            del module

            for used_language_model_name in self.used_language_model_names:
                # Meta data is required for language models to be accepted.
                addDistributionMetadataValue(
                    distribution_name=used_language_model_name.asString(),
                    distribution=None,
                    reason="for 'spacy' to locate the language model",
                )

                module_folder = self.locateModule(used_language_model_name)

                yield self.makeIncludedDataDirectory(
                    source_path=module_folder,
                    dest_path=used_language_model_name.asPath(),
                    reason="model data for %r" % (used_language_model_name.asString()),
                    tags="spacy",
                    raw=True,
                )



