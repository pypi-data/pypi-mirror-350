#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Reformulation of boolean and/or expressions.

Consult the Developer Manual for information. TODO: Add ability to sync
source code comments with Developer Manual sections.

"""

from qutayba.nodes.ConditionalNodes import (
    ExpressionConditionalAnd,
    ExpressionConditionalOr,
    makeNotExpression,
)

from .TreeHelpers import buildNode, buildNodeList, getKind


def buildBoolOpNode(provider, node, source_ref):
    bool_op = getKind(node.op)

    if bool_op == "Or":
        # The "or" may be short circuit and is therefore not a plain operation.
        values = buildNodeList(provider, node.values, source_ref)

        for value in values[:-1]:
            value.setCompatibleSourceReference(values[-1].getSourceReference())

        source_ref = values[-1].getSourceReference()

        return makeOrNode(values=values, source_ref=source_ref)

    elif bool_op == "And":
        # The "and" may be short circuit and is therefore not a plain operation.
        values = buildNodeList(provider, node.values, source_ref)

        for value in values[:-1]:
            value.setCompatibleSourceReference(values[-1].getSourceReference())

        source_ref = values[-1].getSourceReference()

        return makeAndNode(values=values, source_ref=source_ref)
    elif bool_op == "Not":
        # The "not" is really only a unary operation and no special.
        return makeNotExpression(
            expression=buildNode(provider, node.operand, source_ref)
        )
    else:
        assert False, bool_op


def makeOrNode(values, source_ref):
    values = list(values)

    result = values.pop()

    # When we encounter, "or", we expect it to be at least two values.
    assert values

    while values:
        result = ExpressionConditionalOr(
            left=values.pop(), right=result, source_ref=source_ref
        )

    return result


def makeAndNode(values, source_ref):
    values = list(values)

    result = values.pop()

    # Unlike "or", for "and", this is used with only one value.

    while values:
        result = ExpressionConditionalAnd(
            left=values.pop(), right=result, source_ref=source_ref
        )

    return result



