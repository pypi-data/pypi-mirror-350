#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Nodes for all things "ctypes" stdlib module.

"""

from .HardImportNodesGenerated import (
    ExpressionCtypesCdllBefore38CallBase,
    ExpressionCtypesCdllSince38CallBase,
)


class ExpressionCtypesCdllSince38Call(ExpressionCtypesCdllSince38CallBase):
    """Function reference ctypes.CDLL"""

    kind = "EXPRESSION_CTYPES_CDLL_SINCE38_CALL"

    def replaceWithCompileTimeValue(self, trace_collection):
        # TODO: Locate DLLs and report to freezer
        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None


class ExpressionCtypesCdllBefore38Call(ExpressionCtypesCdllBefore38CallBase):
    """Function reference ctypes.CDLL"""

    kind = "EXPRESSION_CTYPES_CDLL_BEFORE38_CALL"

    def replaceWithCompileTimeValue(self, trace_collection):
        # TODO: Locate DLLs and report to freezer
        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None



