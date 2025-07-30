#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


"""Dedicated nodes used for the 3.10 matching

Not usable with older Python as it depends on type flags not present.
"""

from .ChildrenHavingMixins import ChildHavingValueMixin
from .ExpressionBases import ExpressionBase
from .ExpressionShapeMixins import ExpressionBoolShapeExactMixin
from .NodeBases import SideEffectsFromChildrenMixin


class ExpressionMatchTypeCheckBase(
    ExpressionBoolShapeExactMixin,
    SideEffectsFromChildrenMixin,
    ChildHavingValueMixin,
    ExpressionBase,
):
    named_children = ("value",)

    def __init__(self, value, source_ref):
        ChildHavingValueMixin.__init__(self, value=value)

        ExpressionBase.__init__(self, source_ref)

    def mayRaiseException(self, exception_type):
        return self.subnode_value.mayRaiseException(exception_type)


class ExpressionMatchTypeCheckSequence(ExpressionMatchTypeCheckBase):
    kind = "EXPRESSION_MATCH_TYPE_CHECK_SEQUENCE"

    def computeExpression(self, trace_collection):
        # TODO: Quite some cases should be possible to predict, based on argument
        # shape, this could evaluate to statically True/False and then will allow
        # optimization into match branches.
        return self, None, None


class ExpressionMatchTypeCheckMapping(ExpressionMatchTypeCheckBase):
    kind = "EXPRESSION_MATCH_TYPE_CHECK_MAPPING"

    def computeExpression(self, trace_collection):
        # TODO: Quite some cases should be possible to predict, based on argument
        # shape, this could evaluate to statically True/False and then will allow
        # optimization into match branches.
        return self, None, None



