#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" State of a stack of future specs during parsing. """

from qutayba.nodes.FutureSpecs import FutureSpec
from qutayba.plugins.Plugins import Plugins
from qutayba.PythonVersions import python_version

from .SyntaxErrors import raiseSyntaxError

_future_specs = []


def pushFutureSpec(module_name):
    _future_specs.append(
        FutureSpec(use_annotations=Plugins.decideAnnotations(module_name))
    )


def getFutureSpec():
    return _future_specs[-1]


def popFutureSpec():
    del _future_specs[-1]


def enableFutureFeature(node, object_name, source_ref):
    future_spec = _future_specs[-1]

    if object_name == "unicode_literals":
        future_spec.enableUnicodeLiterals()
    elif object_name == "absolute_import":
        future_spec.enableAbsoluteImport()
    elif object_name == "division":
        future_spec.enableFutureDivision()
    elif object_name == "print_function":
        future_spec.enableFuturePrint()
    elif object_name == "barry_as_FLUFL" and python_version >= 0x300:
        future_spec.enableBarry()
    elif object_name == "generator_stop":
        future_spec.enableGeneratorStop()
    elif object_name == "braces":
        raiseSyntaxError("not a chance", source_ref.atColumnNumber(node.col_offset))
    elif object_name in ("nested_scopes", "generators", "with_statement"):
        # These are enabled in all cases already.
        pass
    elif object_name == "annotations" and python_version >= 0x370:
        future_spec.enableFutureAnnotations()
    else:
        raiseSyntaxError(
            "future feature %s is not defined" % object_name,
            source_ref.atColumnNumber(node.col_offset),
        )



