#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Select from code helpers.

This aims at being general, but right now is only used for comparison code helpers.
"""

from qutayba import Options

from .c_types.CTypePyObjectPointers import CTypePyObjectPtr
from .Reports import onMissingHelper


def selectCodeHelper(
    prefix,
    specialized_helpers_set,
    non_specialized_helpers_set,
    result_type,
    left_shape,
    right_shape,
    left_c_type,
    right_c_type,
    argument_swap,
    report_missing,
    source_ref,
):
    if argument_swap:
        left_shape, right_shape = right_shape, left_shape
        left_c_type, right_c_type = right_c_type, left_c_type

    left_helper = (
        left_shape.helper_code
        if left_c_type is CTypePyObjectPtr
        else left_c_type.helper_code
    )
    right_helper = (
        right_shape.helper_code
        if right_c_type is CTypePyObjectPtr
        else right_c_type.helper_code
    )

    helper_function = "%s_%s%s_%s" % (
        prefix,
        ("%s_" % result_type.helper_code) if result_type is not None else "",
        left_helper,
        right_helper,
    )

    if helper_function not in specialized_helpers_set:
        if (
            report_missing
            and Options.report_missing_code_helpers
            and (
                not non_specialized_helpers_set
                or helper_function not in non_specialized_helpers_set
            )
        ):
            onMissingHelper(helper_function, source_ref)

        # print(helper_function, source_ref, len(specialized_helpers_set))

        helper_function = None

    return result_type, helper_function



