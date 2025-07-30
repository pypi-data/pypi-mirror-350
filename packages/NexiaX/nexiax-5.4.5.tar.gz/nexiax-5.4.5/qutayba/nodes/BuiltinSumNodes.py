#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Node the calls to the 'sum' built-in.

This is a rather challenging case for optimization, as it has C code behind
it that could be in-lined sometimes for more static analysis.

"""

from qutayba.specs import BuiltinParameterSpecs

from .ChildrenHavingMixins import (
    ChildHavingSequenceMixin,
    ChildrenHavingSequenceStartMixin,
)
from .ExpressionBases import ExpressionBase


class ExpressionBuiltinSumMixin(object):
    # Mixins are required to define empty slots
    __slots__ = ()

    builtin_spec = BuiltinParameterSpecs.builtin_sum_spec

    def computeBuiltinSpec(self, trace_collection, given_values):
        assert self.builtin_spec is not None, self

        if not self.builtin_spec.isCompileTimeComputable(given_values):
            trace_collection.onExceptionRaiseExit(BaseException)

            # TODO: Raise exception known step 0.

            return self, None, None

        return trace_collection.getCompileTimeComputationResult(
            node=self,
            computation=lambda: self.builtin_spec.simulateCall(given_values),
            description="Built-in call to '%s' computed."
            % (self.builtin_spec.getName()),
        )


class ExpressionBuiltinSum1(
    ExpressionBuiltinSumMixin, ChildHavingSequenceMixin, ExpressionBase
):
    kind = "EXPRESSION_BUILTIN_SUM1"

    named_children = ("sequence",)

    def __init__(self, sequence, source_ref):
        ChildHavingSequenceMixin.__init__(self, sequence=sequence)

        ExpressionBase.__init__(self, source_ref)

    def computeExpression(self, trace_collection):
        sequence = self.subnode_sequence

        # TODO: Protect against large xrange constants
        return self.computeBuiltinSpec(
            trace_collection=trace_collection, given_values=(sequence,)
        )


class ExpressionBuiltinSum2(
    ExpressionBuiltinSumMixin, ChildrenHavingSequenceStartMixin, ExpressionBase
):
    kind = "EXPRESSION_BUILTIN_SUM2"

    named_children = ("sequence", "start")

    def __init__(self, sequence, start, source_ref):
        ChildrenHavingSequenceStartMixin.__init__(
            self,
            sequence=sequence,
            start=start,
        )

        ExpressionBase.__init__(self, source_ref)

    def computeExpression(self, trace_collection):
        sequence = self.subnode_sequence
        start = self.subnode_start

        # TODO: Protect against large xrange constants
        return self.computeBuiltinSpec(
            trace_collection=trace_collection, given_values=(sequence, start)
        )



