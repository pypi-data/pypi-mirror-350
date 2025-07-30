#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Nodes for match statement for Python3.10+ """

from .ChildrenHavingMixins import ChildrenHavingExpressionMatchTypeMixin
from .ExpressionBases import ExpressionBase
from .ExpressionShapeMixins import ExpressionTupleShapeExactMixin


class ExpressionMatchArgs(
    ExpressionTupleShapeExactMixin,
    ChildrenHavingExpressionMatchTypeMixin,
    ExpressionBase,
):
    kind = "EXPRESSION_MATCH_ARGS"

    named_children = ("expression", "match_type")

    __slots__ = ("positional_count", "keywords")

    def __init__(self, expression, match_type, max_allowed, keywords, source_ref):
        ChildrenHavingExpressionMatchTypeMixin.__init__(
            self, expression=expression, match_type=match_type
        )

        ExpressionBase.__init__(self, source_ref)

        self.positional_count = max_allowed
        self.keywords = tuple(keywords)

    def computeExpression(self, trace_collection):
        # TODO: May know that match args doesn't raise from the shape of
        # the matches expression, most don't.

        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None

    def getPositionalArgsCount(self):
        return self.positional_count

    def getKeywordArgs(self):
        return self.keywords



