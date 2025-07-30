#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Templates for the iterator handling.

"""

template_loop_break_next = """\
if (%(to_name)s == NULL) {
    if (CHECK_AND_CLEAR_STOP_ITERATION_OCCURRED(tstate)) {
%(break_indicator_code)s
        goto %(break_target)s;
    } else {
%(release_temps)s
        FETCH_ERROR_OCCURRED_STATE(tstate, &%(exception_state_name)s);
%(var_description_code)s
%(line_number_code)s
        goto %(exception_target)s;
    }
}
"""

from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())


