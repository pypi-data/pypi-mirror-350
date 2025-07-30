#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Templates for handling exceptions.

"""

template_publish_exception_to_handler = """\
{
    PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&%(keeper_exception_state_name)s);
    if (exception_tb == NULL) {
        exception_tb = %(tb_making)s;
        SET_EXCEPTION_STATE_TRACEBACK(&%(keeper_exception_state_name)s, exception_tb);
    } else if (%(keeper_lineno)s != 0) {
        exception_tb = ADD_TRACEBACK(exception_tb, %(frame_identifier)s, %(keeper_lineno)s);
        SET_EXCEPTION_STATE_TRACEBACK(&%(keeper_exception_state_name)s, exception_tb);
    }
}
"""

template_error_catch_fetched_exception = """\
if (%(condition)s) {
    assert(HAS_EXCEPTION_STATE(&%(exception_state_name)s));

%(release_temps)s

%(line_number_code)s
%(var_description_code)s
    goto %(exception_exit)s;
}"""

template_error_catch_exception = """\
if (%(condition)s) {
    assert(HAS_ERROR_OCCURRED(tstate));

    FETCH_ERROR_OCCURRED_STATE(tstate, &%(exception_state_name)s);
%(release_temps)s

%(line_number_code)s
%(var_description_code)s
    goto %(exception_exit)s;
}"""

template_error_format_string_exception = """\
if (%(condition)s) {
%(release_temps)s
%(set_exception)s

%(line_number_code)s
%(var_description_code)s
    goto %(exception_exit)s;
}
"""

template_error_format_name_error_exception = """\
if (unlikely(%(condition)s)) {
%(release_temps)s
%(raise_name_error_helper)s(tstate, &%(exception_state_name)s, %(variable_name)s);

%(line_number_code)s
%(var_description_code)s
    goto %(exception_exit)s;
}
"""


from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())


