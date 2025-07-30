#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" CType classes for C bool, this cannot represent unassigned, nor indicate exception.

"""

from .CTypeBases import CTypeBase, CTypeNotReferenceCountedMixin


class CTypeBool(CTypeNotReferenceCountedMixin, CTypeBase):
    c_type = "bool"

    # Return value only obviously.
    helper_code = "CBOOL"

    @classmethod
    def emitValueAccessCode(cls, value_name, emit, context):
        # Nothing to do for this type, pylint: disable=unused-argument
        assert False

    @classmethod
    def emitValueAssertionCode(cls, value_name, emit):
        pass

    @classmethod
    def emitAssignConversionCode(cls, to_name, value_name, needs_check, emit, context):
        # Conversion cannot fail really.
        if value_name.c_type == cls.c_type:
            emit("%s = %s;" % (to_name, value_name))
        else:
            emit(
                "%s = %s;"
                % (
                    to_name,
                    value_name.getCType().getTruthCheckCode(value_name=value_name),
                )
            )

    @classmethod
    def emitAssignmentCodeFromConstant(
        cls, to_name, constant, may_escape, emit, context
    ):
        # No context needed, pylint: disable=unused-argument
        emit("%s = %s;" % (to_name, "true" if constant else "false"))

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
    def emitAssignmentCodeTonexiumBool(
        cls, to_name, value_name, needs_check, emit, context
    ):
        # Half way, virtual method: pylint: disable=unused-argument
        emit("%s = %s ? DEVILPY_BOOL_TRUE : DEVILPY_BOOL_FALSE;" % (to_name, value_name))

    @classmethod
    def emitAssignmentCodeFromBoolCondition(cls, to_name, condition, emit):
        emit("%s = (%s) ? true : false;" % (to_name, condition))

    @classmethod
    def emitAssignInplaceNegatedValueCode(cls, to_name, needs_check, emit, context):
        # Half way, virtual method: pylint: disable=unused-argument
        emit("%s = !%s;" % (to_name, to_name))

    @classmethod
    def getExceptionCheckCondition(cls, value_name):
        # Expected to not be used, pylint: disable=unused-argument
        assert False

    @classmethod
    def hasErrorIndicator(cls):
        return False

    @classmethod
    def getTruthCheckCode(cls, value_name):
        return "%s != false" % value_name



