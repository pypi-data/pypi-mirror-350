#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Expression codes, side effects, or statements that are an unused expression.

When you write "f()", i.e. you don't use the return value, that is an expression
only statement.

"""

from .CodeHelpers import generateExpressionCode
from .ErrorCodes import getReleaseCode


def generateExpressionOnlyCode(statement, emit, context):
    return getStatementOnlyCode(
        value=statement.subnode_expression, emit=emit, context=context
    )


def getStatementOnlyCode(value, emit, context):
    tmp_name = context.allocateTempName(
        base_name="unused", type_name="qutayba_void", unique=True
    )
    tmp_name.maybe_unused = True

    generateExpressionCode(
        expression=value, to_name=tmp_name, emit=emit, context=context
    )

    # An error of the expression is dealt inside of this, not necessary here,
    # but we have to release non-error value if it has a reference.
    getReleaseCode(release_name=tmp_name, emit=emit, context=context)


def generateSideEffectsCode(to_name, expression, emit, context):
    for side_effect in expression.subnode_side_effects:
        getStatementOnlyCode(value=side_effect, emit=emit, context=context)

    generateExpressionCode(
        to_name=to_name,
        expression=expression.subnode_expression,
        emit=emit,
        context=context,
    )



