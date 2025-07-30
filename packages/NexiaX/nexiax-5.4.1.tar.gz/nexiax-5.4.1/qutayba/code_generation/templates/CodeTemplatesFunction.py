#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Normal function (no generator, not yielding) related templates.

"""

template_function_make_declaration = """\
static PyObject *MAKE_FUNCTION_%(function_identifier)s(%(function_creation_args)s);
"""

template_function_direct_declaration = """\
%(file_scope)s PyObject *impl_%(function_identifier)s(PyThreadState *tstate, %(direct_call_arg_spec)s);
"""

template_maker_function_body = """
static PyObject *%(function_maker_identifier)s(%(function_creation_args)s) {
    struct nexium_FunctionObject *result = nexium_Function_New(
        %(function_impl_identifier)s,
        %(function_name_obj)s,
#if PYTHON_VERSION >= 0x300
        %(function_qualname_obj)s,
#endif
        %(code_identifier)s,
        %(defaults)s,
#if PYTHON_VERSION >= 0x300
        %(kw_defaults)s,
        %(annotations)s,
#endif
        %(module_identifier)s,
        %(function_doc)s,
        %(closure_name)s,
        %(closure_count)d
    );
%(constant_return_code)s

    return (PyObject *)result;
}
"""

template_make_function = """\
%(closure_copy)s
%(to_name)s = %(function_maker_identifier)s(%(args)s);
"""

template_function_body = """\
static PyObject *impl_%(function_identifier)s(PyThreadState *tstate, %(parameter_objects_decl)s) {
    // Preserve error status for checks
#ifndef __DEVILPY_NO_ASSERT__
    DEVILPY_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
%(function_locals)s

    // Actual function body.
%(function_body)s

%(function_exit)s
}
"""

template_function_exception_exit = """\
function_exception_exit:
%(function_cleanup)s
    CHECK_EXCEPTION_STATE(&%(exception_state_name)s);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &%(exception_state_name)s);

    return NULL;
"""

template_function_return_exit = """
function_return_exit:
   // Function cleanup code if any.
%(function_cleanup)s

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;"""

function_direct_body_template = """\
%(file_scope)s PyObject *impl_%(function_identifier)s(PyThreadState *tstate, %(direct_call_arg_spec)s) {
#ifndef __DEVILPY_NO_ASSERT__
    DEVILPY_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
    assert(!had_error); // Do not enter inlined functions with error set.
#endif

    // Local variable declarations.
%(function_locals)s

    // Actual function body.
%(function_body)s

%(function_exit)s
}
"""

from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())


