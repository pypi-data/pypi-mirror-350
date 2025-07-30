#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Reports about code generation.

Initially this is about missing optimization only, but it should expand into
real stuff.
"""

from qutayba import Options
from qutayba.containers.OrderedDicts import OrderedDict
from qutayba.containers.OrderedSets import OrderedSet
from qutayba.Tracing import code_generation_logger, optimization_logger

_missing_helpers = OrderedDict()

_missing_operations = OrderedSet()

_missing_trust = OrderedDict()

_missing_overloads = OrderedDict()

_error_for_missing = False
# _error_for_missing = True


def doMissingOptimizationReport():
    for helper, source_refs in _missing_helpers.items():
        message = "Missing C helper code variant, used fallback: %s at %s" % (
            helper,
            ",".join(source_ref.getAsString() for source_ref in source_refs),
        )

        if _error_for_missing:
            code_generation_logger.warning(message)
        else:
            code_generation_logger.info(message)

    for desc in _missing_operations:
        message = "Missing optimization, used fallback: %s" % (desc,)
        if _error_for_missing:
            optimization_logger.warning(message)
        else:
            optimization_logger.info(message)

    for desc, source_refs in _missing_trust.items():
        message = desc[0] % desc[1:]
        message += " at %s" % ",".join(
            source_ref.getAsString() for source_ref in source_refs
        )

        if _error_for_missing:
            optimization_logger.warning(message)
        else:
            optimization_logger.info(message)

    for method_name, node in _missing_overloads.items():
        message = "Missing %s overload for %s" % (method_name, node)
        if _error_for_missing:
            optimization_logger.warning(message)
        else:
            optimization_logger.info(message)


def onMissingHelper(helper_name, source_ref):
    if source_ref:
        if helper_name not in _missing_helpers:
            _missing_helpers[helper_name] = []

        _missing_helpers[helper_name].append(source_ref)


def onMissingOperation(operation, left, right):
    # Avoid the circular dependency on tshape_uninitialized from StandardShapes.
    if right.__class__.__name__ != "ShapeTypeUninitialized":
        _missing_operations.add((operation, left, right))


def onMissingUnaryOperation(operation, shape):
    # Avoid the circular dependency on tshape_uninitialized from StandardShapes.
    if shape.__class__.__name__ != "ShapeTypeUninitialized":
        _missing_operations.add((operation, shape))


def onMissingTrust(operation, source_ref, *args):
    if Options.report_missing_trust:
        key = (operation,) + args

        if key not in _missing_trust:
            _missing_trust[key] = OrderedSet()

        _missing_trust[key].add(source_ref)


def onMissingOverload(method_name, node):
    if method_name not in _missing_overloads:
        _missing_overloads[method_name] = OrderedSet()

    _missing_overloads[method_name].add(node.kind)



