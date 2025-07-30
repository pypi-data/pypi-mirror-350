#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Operations on Containers.

"""

from .ChildrenHavingMixins import ChildrenExpressionSetOperationUpdateMixin
from .ExpressionBases import ExpressionBase
from .StatementBasesGenerated import (
    StatementListOperationAppendBase,
    StatementSetOperationAddBase,
)


class StatementListOperationAppend(StatementListOperationAppendBase):
    kind = "STATEMENT_LIST_OPERATION_APPEND"

    named_children = ("list_arg", "value")
    auto_compute_handling = "operation"

    def computeStatementOperation(self, trace_collection):
        # TODO: Until we have proper list tracing.
        trace_collection.removeKnowledge(self.subnode_list_arg)

        return self, None, None

    def mayRaiseException(self, exception_type):
        return self.subnode_list_arg.mayRaiseException(
            exception_type
        ) or self.subnode_value.mayRaiseException(exception_type)


class StatementSetOperationAdd(StatementSetOperationAddBase):
    kind = "STATEMENT_SET_OPERATION_ADD"

    named_children = ("set_arg", "value")
    auto_compute_handling = "operation"

    def computeStatementOperation(self, trace_collection):
        # TODO: Until we have proper set tracing.
        trace_collection.removeKnowledge(self.subnode_set_arg)

        return self, None, None

    def mayRaiseException(self, exception_type):
        return self.subnode_set_arg.mayRaiseException(
            exception_type
        ) or self.subnode_value.mayRaiseException(exception_type)


class ExpressionSetOperationUpdate(
    ChildrenExpressionSetOperationUpdateMixin, ExpressionBase
):
    kind = "EXPRESSION_SET_OPERATION_UPDATE"

    named_children = ("set_arg", "value")

    def __init__(self, set_arg, value, source_ref):
        ChildrenExpressionSetOperationUpdateMixin.__init__(
            self,
            set_arg=set_arg,
            value=value,
        )

        ExpressionBase.__init__(self, source_ref)

    def computeExpression(self, trace_collection):
        trace_collection.removeKnowledge(self.subnode_set_arg)

        return self, None, None



