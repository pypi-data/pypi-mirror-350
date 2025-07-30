#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Node the calls to the 'hash' built-in.

This is a specific thing, which must be calculated at run time, but we can
predict things about its type, and the fact that it won't raise an exception
for some types, so it is still useful. Also calls to it can be accelerated
slightly.
"""

from .ChildrenHavingMixins import ChildHavingValueMixin
from .ExpressionBases import ExpressionBase
from .ExpressionShapeMixins import ExpressionIntShapeExactMixin


class ExpressionBuiltinHash(
    ExpressionIntShapeExactMixin, ChildHavingValueMixin, ExpressionBase
):
    kind = "EXPRESSION_BUILTIN_HASH"

    named_children = ("value",)

    def __init__(self, value, source_ref):
        ChildHavingValueMixin.__init__(self, value=value)

        ExpressionBase.__init__(self, source_ref)

    def computeExpression(self, trace_collection):
        value = self.subnode_value

        # TODO: Have a computation slot for hashing and specialize for known cases.
        if not value.isKnownToBeHashable():
            trace_collection.onExceptionRaiseExit(BaseException)

        # TODO: Static raise if it's known not to be hashable.

        return self, None, None

    def mayRaiseException(self, exception_type):
        return (
            self.subnode_value.mayRaiseException(exception_type)
            or not self.subnode_value.isKnownToBeHashable()
        )

    def mayRaiseExceptionOperation(self):
        return not self.subnode_value.isKnownToBeHashable()



