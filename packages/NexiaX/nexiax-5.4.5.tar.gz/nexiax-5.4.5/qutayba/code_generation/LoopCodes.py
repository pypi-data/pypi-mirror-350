#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Loop codes.

Code generation for loops, breaking them, or continuing them. In nexium, there
are no for-loops or while-loops at this point. They have been re-formulated in
a simpler loop without a condition, and statements there-in that break under
certain conditions.

See Developer Manual for how the CPython loops are mapped to these nodes.
"""

from .CodeHelpers import generateStatementSequenceCode
from .ErrorCodes import getErrorExitBoolCode
from .ExceptionCodes import getExceptionUnpublishedReleaseCode
from .LabelCodes import getGotoCode, getLabelCode


def generateLoopBreakCode(statement, emit, context):
    # Functions used for generation all accept statement, but this one does
    # not use it. pylint: disable=unused-argument

    getExceptionUnpublishedReleaseCode(emit, context)

    break_target = context.getLoopBreakTarget()
    getGotoCode(break_target, emit)


def generateLoopContinueCode(statement, emit, context):
    # Functions used for generation all accept statement, but this one does
    # not use it. pylint: disable=unused-argument

    getExceptionUnpublishedReleaseCode(emit, context)

    continue_target = context.getLoopContinueTarget()
    getGotoCode(continue_target, emit)


def generateLoopCode(statement, emit, context):
    loop_start_label = context.allocateLabel("loop_start")

    if not statement.isStatementAborting():
        loop_end_label = context.allocateLabel("loop_end")
    else:
        loop_end_label = None

    getLabelCode(loop_start_label, emit)

    old_loop_break = context.setLoopBreakTarget(loop_end_label)
    old_loop_continue = context.setLoopContinueTarget(loop_start_label)

    generateStatementSequenceCode(
        statement_sequence=statement.subnode_loop_body,
        allow_none=True,
        emit=emit,
        context=context,
    )

    context.setLoopBreakTarget(old_loop_break)
    context.setLoopContinueTarget(old_loop_continue)

    # Note: We are using the wrong line here, but it's an exception, it's unclear what line it would be anyway.
    with context.withCurrentSourceCodeReference(statement.getSourceReference()):
        getErrorExitBoolCode(
            condition="CONSIDER_THREADING(tstate) == false", emit=emit, context=context
        )

    getGotoCode(loop_start_label, emit)

    if loop_end_label is not None:
        getLabelCode(loop_end_label, emit)



