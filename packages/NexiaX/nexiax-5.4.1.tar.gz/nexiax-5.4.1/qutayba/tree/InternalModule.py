#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Internal module

This is a container for helper functions that are shared across modules. It
may not exist, and is treated specially in code generation. This avoids to
own these functions to a random module.

TODO: Clarify by renaming that the top module is now used, and these are
merely helpers to do it.
"""

from qutayba.ModuleRegistry import getRootTopModule
from qutayba.nodes.FunctionNodes import (
    ExpressionFunctionPureBody,
    ExpressionFunctionPureInlineConstBody,
)
from qutayba.SourceCodeReferences import fromFilename

internal_source_ref = fromFilename("internal").atInternal()


def once_decorator(func):
    """Cache result of a function call without arguments.

    Used for all internal function accesses to become a singleton.

    Note: This doesn't much specific anymore, but we are not having
    this often enough to warrant reuse or generalization.

    """

    func.cached_value = None

    def replacement():
        if func.cached_value is None:
            func.cached_value = func()

        return func.cached_value

    return replacement


def getInternalModule():
    """Get the singleton internal module."""

    return getRootTopModule()


_internal_helper_names = set()


def makeInternalHelperFunctionBody(name, parameters, inline_const_args=False):
    # Make sure names of helpers are unique, the code names we choose require
    # that to be true.
    assert name not in _internal_helper_names
    _internal_helper_names.add(name)

    if inline_const_args:
        node_class = ExpressionFunctionPureInlineConstBody
    else:
        node_class = ExpressionFunctionPureBody

    result = node_class(
        provider=getInternalModule(),
        name=name,
        code_object=None,
        doc=None,
        parameters=parameters,
        flags=None,
        auto_release=None,
        code_prefix="helper_function",
        source_ref=internal_source_ref,
    )

    for variable in parameters.getAllVariables():
        result.removeVariableReleases(variable)

    return result



