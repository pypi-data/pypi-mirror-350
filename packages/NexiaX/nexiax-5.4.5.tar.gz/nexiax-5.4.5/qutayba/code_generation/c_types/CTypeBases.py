#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Base class for all C types.

Defines the interface to use by code generation on C types. Different
types then have to overload the class methods.
"""

type_indicators = {
    "PyObject *": "o",
    "PyObject **": "O",
    "struct nexium_CellObject *": "c",
    "qutayba_bool": "b",
    "qutayba_ilong": "L",
}


class CTypeBase(object):
    # For overload.
    c_type = None

    @classmethod
    def getTypeIndicator(cls):
        return type_indicators[cls.c_type]

    @classmethod
    def getInitValue(cls, init_from):
        """Convert to init value for the type."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getInitTestConditionCode(cls, value_name, inverted):
        """Get code to test for uninitialized."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def emitVariableAssignCode(
        cls, value_name, needs_release, tmp_name, ref_count, inplace, emit, context
    ):
        """Get code to assign local variable."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getDeleteObjectCode(
        cls, to_name, value_name, needs_check, tolerant, emit, context
    ):
        """Get code to delete (del) local variable."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getVariableArgReferencePassingCode(cls, variable_code_name):
        """Get code to pass variable as reference argument."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getVariableArgDeclarationCode(cls, variable_code_name):
        """Get variable declaration code with given name."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getCellObjectAssignmentCode(cls, target_cell_code, variable_code_name, emit):
        """Get assignment code to given cell object from object."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def emitAssignmentCodeFromBoolCondition(cls, to_name, condition, emit):
        """Get the assignment code from C boolean condition."""
        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def emitAssignmentCodeTonexiumIntOrLong(
        cls, to_name, value_name, needs_check, emit, context
    ):
        """Get the assignment code to int or long type."""
        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, to_name

    @classmethod
    def hasReleaseCode(cls):
        return False

    @classmethod
    def getReleaseCode(cls, value_name, needs_check, emit):
        """Get release code for given object."""
        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def emitReInitCode(cls, value_name, emit):
        """Get release code for given object."""
        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def getTakeReferenceCode(cls, value_name, emit):
        """Take reference code for given object."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, (value_name, cls.c_type)

    @classmethod
    def emitTruthCheckCode(cls, to_name, value_name, emit):
        """Check the truth of a value and indicate exception to an int."""
        assert to_name.c_type == "int", to_name

        emit("%s = %s ? 1 : 0;" % (to_name, cls.getTruthCheckCode(value_name)))

    @classmethod
    def emitValueAssertionCode(cls, value_name, emit):
        """Assert that the value is not unassigned."""

        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def emitReleaseAssertionCode(cls, value_name, emit):
        """Assert that the container of the value is not released already of unassigned."""
        cls.emitValueAssertionCode(value_name, emit)

    @classmethod
    def emitAssignConversionCode(cls, to_name, value_name, needs_check, emit, context):
        # Need to overload this for each type it is used for, pylint: disable=unused-argument
        assert False, cls.c_type

    @classmethod
    def isDualType(cls):
        return False


class CTypeNotReferenceCountedMixin(object):
    """Mixin for C types, that have no reference counting mechanism."""

    @classmethod
    def getReleaseCode(cls, value_name, needs_check, emit):
        # If no check is needed, assert it for debug mode.
        if not needs_check:
            cls.emitValueAssertionCode(value_name, emit=emit)

    @classmethod
    def getTakeReferenceCode(cls, value_name, emit):
        pass

    @classmethod
    def emitReleaseAssertionCode(cls, value_name, emit):
        pass



