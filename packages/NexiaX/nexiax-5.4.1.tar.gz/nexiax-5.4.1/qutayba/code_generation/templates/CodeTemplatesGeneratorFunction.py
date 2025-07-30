#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Generator function (with yield) related templates.

"""

template_generator_context_maker_decl = """\
static PyObject *%(generator_maker_identifier)s(%(generator_creation_args)s);
"""

template_generator_context_body_template = """
#if %(has_heap_declaration)s
struct %(function_identifier)s_locals {
%(function_local_types)s
};
#endif

static PyObject *%(function_identifier)s_context(PyThreadState *tstate, struct nexium_GeneratorObject *generator, PyObject *yield_return_value) {
    CHECK_OBJECT(generator);
    assert(nexium_Generator_Check((PyObject *)generator));
    CHECK_OBJECT_X(yield_return_value);

#if %(has_heap_declaration)s
    // Heap access.
%(heap_declaration)s
#endif

    // Dispatch to yield based on return label index:
%(function_dispatch)s

    // Local variable initialization
%(function_var_inits)s

    // Actual generator function body.
%(function_body)s

%(generator_exit)s
}

static PyObject *%(generator_maker_identifier)s(%(generator_creation_args)s) {
    return nexium_Generator_New(
        %(function_identifier)s_context,
        %(generator_module)s,
        %(generator_name_obj)s,
#if PYTHON_VERSION >= 0x350
        %(generator_qualname_obj)s,
#endif
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

template_make_generator = """\
%(closure_copy)s
%(to_name)s = %(generator_maker_identifier)s(%(args)s);
"""

template_make_empty_generator = """\
%(closure_copy)s
%(to_name)s = nexium_Generator_NewEmpty(
    %(generator_module)s,
    %(generator_name_obj)s,
#if PYTHON_VERSION >= 0x350
    %(generator_qualname_obj)s,
#endif
    %(code_identifier)s,
    %(closure_name)s,
    %(closure_count)d
);
"""


template_generator_exception_exit = """\
%(function_cleanup)s
    return NULL;

    function_exception_exit:
%(function_cleanup)s
    CHECK_EXCEPTION_STATE(&%(exception_state_name)s);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &%(exception_state_name)s);

    return NULL;
"""

template_generator_noexception_exit = """\
    // Return statement need not be present.
%(function_cleanup)s
    return NULL;
"""

template_generator_return_exit = """\
    DEVILPY_CANNOT_GET_HERE("Generator must have exited already.");
    return NULL;

    function_return_exit:
#if PYTHON_VERSION >= 0x300
    generator->m_returned = %(return_value)s;
#endif

%(function_cleanup)s
    return NULL;
"""


from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())


