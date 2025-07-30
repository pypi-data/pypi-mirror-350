#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" CType classes for C "long", and C "digit" (used in conjunction with PyLongObject *)

"""

from .CTypeBases import CTypeBase


class CTypeCLongMixin(CTypeBase):
    @classmethod
    def emitAssignmentCodeFromConstant(
        cls, to_name, constant, may_escape, emit, context
    ):
        # No context needed, pylint: disable=unused-argument
        emit("%s = %s;" % (to_name, constant))


class CTypeCLong(CTypeCLongMixin, CTypeBase):
    c_type = "long"

    helper_code = "CLONG"


class CTypeCLongDigit(CTypeCLongMixin, CTypeBase):
    c_type = "qutayba_digit"

    helper_code = "DIGIT"



