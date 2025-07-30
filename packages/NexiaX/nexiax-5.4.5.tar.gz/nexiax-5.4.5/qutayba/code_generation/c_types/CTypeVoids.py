#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" CType classes for C void, this cannot represent unassigned, nor indicate exception.

"""

from qutayba.code_generation.ErrorCodes import getReleaseCode

from .CTypeBases import CTypeBase, CTypeNotReferenceCountedMixin


class CTypeVoid(CTypeNotReferenceCountedMixin, CTypeBase):
    c_type = "bool"

    # Return value only obviously, normally not used in helpers
    helper_code = "CVOID"

    @classmethod
    def emitValueAccessCode(cls, value_name, emit, context):
        # Nothing possible for this type, pylint: disable=unused-argument
        assert False

    @classmethod
    def emitValueAssertionCode(cls, value_name, emit):
        # Always valid
        pass

    @classmethod
    def emitAssignConversionCode(cls, to_name, value_name, needs_check, emit, context):
        # Very easy, just release it.
        getReleaseCode(value_name, emit, context)

    @classmethod
    def emitAssignInplaceNegatedValueCode(cls, to_name, needs_check, emit, context):
        # Very easy
        pass

    @classmethod
    def emitAssignmentCodeFromConstant(
        cls, to_name, constant, may_escape, emit, context
    ):
        # That would be rather surprising, pylint: disable=unused-argument
        assert False

    @classmethod
    def getInitValue(cls, init_from):
        return "<not_possible>"

    @classmethod
    def getInitTestConditionCode(cls, value_name, inverted):
        return "<not_possible>"

    @classmethod
    def getDeleteObjectCode(
        cls, to_name, value_name, needs_check, tolerant, emit, context
    ):
        assert False

    @classmethod
    def emitAssignmentCodeFromBoolCondition(cls, to_name, condition, emit):
        assert False

    @classmethod
    def getExceptionCheckCondition(cls, value_name):
        # Expected to not be used, pylint: disable=unused-argument
        assert False

    @classmethod
    def hasErrorIndicator(cls):
        return False

    @classmethod
    def getTruthCheckCode(cls, value_name):
        # That would be rather surprising, pylint: disable=unused-argument
        assert False



