#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Builtin vars node.

Not used much, esp. not in the form with arguments. Maybe used in some meta programming,
and hopefully can be predicted, because at run time, it is hard to support.
"""

from .ChildrenHavingMixins import ChildHavingSourceMixin
from .ExpressionBases import ExpressionBase


class ExpressionBuiltinVars(ChildHavingSourceMixin, ExpressionBase):
    kind = "EXPRESSION_BUILTIN_VARS"

    named_children = ("source",)

    def __init__(self, source, source_ref):
        ChildHavingSourceMixin.__init__(self, source=source)

        ExpressionBase.__init__(self, source_ref)

    def computeExpression(self, trace_collection):
        # TODO: Should be possible to predict this.

        trace_collection.onExceptionRaiseExit(BaseException)
        return self, None, None



