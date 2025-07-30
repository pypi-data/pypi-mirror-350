#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Coroutines function (await/async) related templates.

"""

template_coroutine_object_maker = """\
static PyObject *%(coroutine_maker_identifier)s(%(coroutine_creation_args)s);
"""

template_coroutine_object_body = """
#if %(has_heap_declaration)s
struct %(function_identifier)s_locals {
%(function_local_types)s
};
#endif

static PyObject *%(function_identifier)s_context(PyThreadState *tstate, struct nexium_CoroutineObject *coroutine, PyObject *yield_return_value) {
    CHECK_OBJECT(coroutine);
    assert(nexium_Coroutine_Check((PyObject *)coroutine));
    CHECK_OBJECT_X(yield_return_value);

#if %(has_heap_declaration)s
    // Heap access.
%(heap_declaration)s
#endif

    // Dispatch to yield based on return label index:
%(function_dispatch)s

    // Local variable initialization
%(function_var_inits)s

    // Actual coroutine body.
%(function_body)s

%(coroutine_exit)s
}

static PyObject *%(coroutine_maker_identifier)s(%(coroutine_creation_args)s) {
    return nexium_Coroutine_New(
        tstate,
        %(function_identifier)s_context,
        %(coroutine_module)s,
        %(coroutine_name_obj)s,
        %(coroutine_qualname_obj)s,
        %(code_identifier)s,
        %(closure_name)s,
        %(closure_count)d,
#if %(has_heap_declaration)s
        sizeof(struct %(function_identifier)s_locals)
#else
        0
#endif
    );
}
"""

template_make_coroutine = """\
%(closure_copy)s
%(to_name)s = %(coroutine_maker_identifier)s(%(args)s);
"""

# TODO: For functions DEVILPY_CANNOT_GET_HERE is injected by composing code.
template_coroutine_exception_exit = """\
    DEVILPY_CANNOT_GET_HERE("Return statement must be present");

    function_exception_exit:
%(function_cleanup)s
    CHECK_EXCEPTION_STATE(&%(exception_state_name)s);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &%(exception_state_name)s);
    return NULL;
"""

template_coroutine_noexception_exit = """\
    DEVILPY_CANNOT_GET_HERE("Return statement must be present");

%(function_cleanup)s
    return NULL;
"""

template_coroutine_return_exit = """\
    function_return_exit:;

    coroutine->m_returned = %(return_value)s;

    return NULL;
"""


from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())


