#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Return codes

This handles code generation for return statements of normal functions and of
generator functions. Also the value currently being returned, and intercepted
by a try statement is accessible this way.

"""

from qutayba.PythonVersions import python_version

from .CodeHelpers import generateExpressionCode
from .ExceptionCodes import getExceptionUnpublishedReleaseCode
from .LabelCodes import getGotoCode


def generateReturnCode(statement, emit, context):
    getExceptionUnpublishedReleaseCode(emit, context)

    return_value = statement.subnode_expression

    return_value_name = context.getReturnValueName()

    if context.getReturnReleaseMode():
        emit("CHECK_OBJECT(%s);" % return_value_name)
        emit("Py_DECREF(%s);" % return_value_name)

    generateExpressionCode(
        to_name=return_value_name,
        expression=return_value,
        emit=emit,
        context=context,
    )

    if context.needsCleanup(return_value_name):
        context.removeCleanupTempName(return_value_name)
    else:
        emit("Py_INCREF(%s);" % return_value_name)

    getGotoCode(label=context.getReturnTarget(), emit=emit)


def generateReturnedValueCode(statement, emit, context):
    # We don't need the statement, pylint: disable=unused-argument

    getExceptionUnpublishedReleaseCode(emit, context)

    getGotoCode(label=context.getReturnTarget(), emit=emit)


def generateReturnConstantCode(statement, emit, context):
    getExceptionUnpublishedReleaseCode(emit, context)

    return_value_name = context.getReturnValueName()

    if context.getReturnReleaseMode():
        emit("CHECK_OBJECT(%s);" % return_value_name)
        emit("Py_DECREF(%s);" % return_value_name)

    return_value_name.getCType().emitAssignmentCodeFromConstant(
        to_name=return_value_name,
        constant=statement.getConstant(),
        may_escape=True,
        emit=emit,
        context=context,
    )

    if context.needsCleanup(return_value_name):
        context.removeCleanupTempName(return_value_name)
    else:
        emit("Py_INCREF(%s);" % return_value_name)

    getGotoCode(label=context.getReturnTarget(), emit=emit)


def generateGeneratorReturnValueCode(statement, emit, context):
    if context.getOwner().isExpressionAsyncgenObjectBody():
        pass
    elif python_version >= 0x300:
        return_value_name = context.getGeneratorReturnValueName()

        expression = statement.subnode_expression

        if context.getReturnReleaseMode():
            emit("CHECK_OBJECT(%s);" % return_value_name)
            emit("Py_DECREF(%s);" % return_value_name)

        generateExpressionCode(
            to_name=return_value_name, expression=expression, emit=emit, context=context
        )

        if context.needsCleanup(return_value_name):
            context.removeCleanupTempName(return_value_name)
        else:
            emit("Py_INCREF(%s);" % return_value_name)

    getGotoCode(context.getReturnTarget(), emit)


def generateGeneratorReturnNoneCode(statement, emit, context):
    # We don't need the statement, pylint: disable=unused-argument

    if context.getOwner().isExpressionAsyncgenObjectBody():
        pass
    elif python_version >= 0x300:
        return_value_name = context.getGeneratorReturnValueName()

        if context.getReturnReleaseMode():
            emit("CHECK_OBJECT(%s);" % return_value_name)
            emit("Py_DECREF(%s);" % return_value_name)

        return_value_name.getCType().emitAssignmentCodeFromConstant(
            to_name=return_value_name,
            constant=None,
            may_escape=False,
            emit=emit,
            context=context,
        )

        if context.needsCleanup(return_value_name):
            context.removeCleanupTempName(return_value_name)
        else:
            emit("Py_INCREF(%s);" % return_value_name)

    getGotoCode(context.getReturnTarget(), emit)



