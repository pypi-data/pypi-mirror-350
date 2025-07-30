#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Code generation for match statement helpers.

"""

from .CodeHelpers import (
    generateChildExpressionsCode,
    withObjectCodeTemporaryAssignment,
)
from .ErrorCodes import getErrorExitCode


def generateMatchArgsCode(to_name, expression, emit, context):
    (matched_value_name, match_type_name) = generateChildExpressionsCode(
        expression=expression, emit=emit, context=context
    )

    # TODO: Prefer "PyObject **" of course once we have that.
    keywords = expression.getKeywordArgs()

    if keywords:
        keywords_name = context.getConstantCode(constant=keywords)
        keywords_name = "&PyTuple_GET_ITEM(%s, 0)" % keywords_name
    else:
        keywords_name = "NULL"

    with withObjectCodeTemporaryAssignment(
        to_name, "match_args_value", expression, emit, context
    ) as value_name:
        emit(
            "%s = MATCH_CLASS_ARGS(tstate, %s, %s, %d, %s, %d);"
            % (
                value_name,
                matched_value_name,
                match_type_name,
                expression.getPositionalArgsCount(),
                keywords_name,
                len(keywords),
            )
        )

        getErrorExitCode(
            check_name=value_name,
            release_names=(matched_value_name, match_type_name),
            emit=emit,
            context=context,
        )

        context.addCleanupTempName(value_name)



