#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Reformulation of assert statements.

Consult the Developer Manual for information. TODO: Add ability to sync
source code comments with Developer Manual sections.

"""

from qutayba.nodes.BuiltinRefNodes import ExpressionBuiltinExceptionRef
from qutayba.nodes.ConditionalNodes import makeStatementConditional
from qutayba.nodes.ContainerMakingNodes import makeExpressionMakeTuple
from qutayba.nodes.ExceptionNodes import (
    StatementRaiseException,
    makeBuiltinMakeExceptionNode,
)
from qutayba.nodes.OperatorNodesUnary import ExpressionOperationNot
from qutayba.Options import hasPythonFlagNoAsserts
from qutayba.PythonVersions import python_version

from .TreeHelpers import buildNode


def buildAssertNode(provider, node, source_ref):
    # Build assert statements. These are re-formulated as described in the
    # Developer Manual too. They end up as conditional statement with raises of
    # AssertionError exceptions.

    # Underlying assumption:
    #
    # Assert x, y is the same as:
    # if not x:
    #     raise AssertionError, y

    # Therefore assert statements are really just conditional statements with a
    # static raise contained.
    #

    exception_value = buildNode(provider, node.msg, source_ref, True)

    if hasPythonFlagNoAsserts():
        return None

    if python_version < 0x3C0:
        if exception_value is not None and python_version >= 0x272:
            exception_value = makeExpressionMakeTuple(
                elements=(exception_value,), source_ref=source_ref
            )

        raise_statement = StatementRaiseException(
            exception_type=ExpressionBuiltinExceptionRef(
                exception_name="AssertionError", source_ref=source_ref
            ),
            exception_value=exception_value,
            exception_trace=None,
            exception_cause=None,
            source_ref=source_ref,
        )
    else:
        raise_statement = StatementRaiseException(
            exception_type=makeBuiltinMakeExceptionNode(
                exception_name="AssertionError",
                args=(exception_value,) if exception_value else (),
                for_raise=False,
                source_ref=source_ref,
            ),
            exception_value=None,
            exception_cause=None,
            exception_trace=None,
            source_ref=source_ref,
        )

    return makeStatementConditional(
        condition=ExpressionOperationNot(
            operand=buildNode(provider, node.test, source_ref), source_ref=source_ref
        ),
        yes_branch=raise_statement,
        no_branch=None,
        source_ref=source_ref,
    )



