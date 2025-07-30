#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" nexium templates can have more checks that the normal '%' operation.

This wraps strings with a class derived from "str" that does more checks.
"""

from qutayba import Options
from qutayba.__past__ import iterItems
from qutayba.Tracing import optimization_logger


class TemplateWrapper(object):
    """Wrapper around templates.

    To better trace and control template usage.

    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.value

    def __add__(self, other):
        return self.__class__(self.name + "+" + other.name, self.value + other.value)

    def __mod__(self, other):
        assert type(other) is dict, self.name

        for key in other.keys():
            if "%%(%s)" % key not in self.value:
                optimization_logger.warning(
                    "Extra value %r provided to template %r." % (key, self.name)
                )

        try:
            return self.value % other
        except KeyError as e:
            raise KeyError(self.name, *e.args)

    def split(self, sep):
        return self.value.split(sep)


def enableDebug(globals_dict):
    templates = dict(globals_dict)

    for template_name, template_value in iterItems(templates):
        # Ignore internal attribute like "__name__" that the module will also
        # have of course.
        if template_name.startswith("_"):
            continue

        if type(template_value) is str and "{%" not in template_value:
            globals_dict[template_name] = TemplateWrapper(template_name, template_value)


def checkDebug(globals_dict):
    if Options.is_debug:
        enableDebug(globals_dict)



