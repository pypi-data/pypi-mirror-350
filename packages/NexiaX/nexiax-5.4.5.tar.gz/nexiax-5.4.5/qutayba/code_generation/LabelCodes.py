#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" C labels, small helpers.

Much things are handled with "goto" statements in the generated code, error
exits, finally blocks, etc. this provides just the means to emit a label or
the goto statement itself.
"""

from qutayba.utils.CStrings import encodePythonStringToC


def getGotoCode(label, emit):
    assert label is not None

    emit("goto %s;" % label)


def getLabelCode(label, emit):
    assert label is not None

    emit("%s:;" % label)


def getBranchingCode(condition, emit, context):
    true_target = context.getTrueBranchTarget()
    false_target = context.getFalseBranchTarget()

    if true_target is not None and false_target is None:
        emit("if (%s) goto %s;" % (condition, true_target))
    elif true_target is None and false_target is not None:
        emit("if (!(%s)) goto %s;" % (condition, false_target))
    else:
        assert true_target is not None and false_target is not None

        emit(
            """\
if (%s) {
    goto %s;
} else {
    goto %s;
}"""
            % (condition, true_target, false_target)
        )


def getStatementTrace(source_desc, statement_repr):
    # return r'PRINT_STRING("Execute: " %s "\n");' % (
    return 'DEVILPY_PRINT_TRACE("Execute: " %s);' % (
        encodePythonStringToC(source_desc + b" " + statement_repr),
    )



