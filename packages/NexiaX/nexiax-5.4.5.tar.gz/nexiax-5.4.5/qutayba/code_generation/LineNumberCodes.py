#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Generate code that updates the source code line.

"""


def getCurrentLineNumberCode(context):
    frame_handle = context.getFrameHandle()

    if frame_handle is None:
        return ""
    else:
        source_ref = context.getCurrentSourceCodeReference()

        if source_ref.isInternal():
            return ""
        else:
            return str(source_ref.getLineNumber())


def getLineNumberUpdateCode(context):
    lineno_value = getCurrentLineNumberCode(context)

    if lineno_value:
        frame_handle = context.getFrameHandle()

        return "%s->m_frame.f_lineno = %s;" % (frame_handle, lineno_value)
    else:
        return ""


def getErrorLineNumberUpdateCode(context):
    (
        _exception_state,
        exception_lineno,
    ) = context.variable_storage.getExceptionVariableDescriptions()

    lineno_value = getCurrentLineNumberCode(context)

    if lineno_value:
        return "%s = %s;" % (exception_lineno, lineno_value)
    else:
        return ""


def emitErrorLineNumberUpdateCode(emit, context):
    update_code = getErrorLineNumberUpdateCode(context)

    if update_code:
        emit(update_code)


def emitLineNumberUpdateCode(expression, emit, context):
    # Optional expression.
    if expression is not None:
        context.setCurrentSourceCodeReference(expression.getCompatibleSourceReference())

    code = getLineNumberUpdateCode(context)

    if code:
        emit(code)


def getSetLineNumberCodeRaw(to_name, emit, context):
    assert context.getFrameHandle() is not None

    emit("%s->m_frame.f_lineno = %s;" % (context.getFrameHandle(), to_name))


def getLineNumberCode(to_name, emit, context):
    assert context.getFrameHandle() is not None

    emit("%s = %s->m_frame.f_lineno;" % (to_name, context.getFrameHandle()))



