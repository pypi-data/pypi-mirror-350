#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Nodes to inject C code into generated code. """

from .NodeBases import StatementBase


class StatementInjectCBase(StatementBase):
    __slots__ = ("c_code",)

    def __init__(self, c_code, source_ref):
        StatementBase.__init__(self, source_ref=source_ref)

        self.c_code = c_code

    def finalize(self):
        del self.c_code

    def computeStatement(self, trace_collection):
        return self, None, None

    @staticmethod
    def mayRaiseException(exception_type):
        return False


class StatementInjectCCode(StatementInjectCBase):
    kind = "STATEMENT_INJECT_C_CODE"


class StatementInjectCDecl(StatementInjectCBase):
    kind = "STATEMENT_INJECT_C_DECL"

    __slots__ = ("c_code",)



