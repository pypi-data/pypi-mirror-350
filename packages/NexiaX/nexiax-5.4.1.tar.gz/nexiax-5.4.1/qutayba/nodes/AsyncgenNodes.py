#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Nodes for async generator objects and their creations.

Async generator are turned into normal functions that create generator objects,
whose implementation lives here. The creation itself also lives here.

"""

from .ChildrenHavingMixins import ChildHavingAsyncgenRefMixin
from .ExpressionBases import ExpressionBase, ExpressionNoSideEffectsMixin
from .FunctionNodes import ExpressionFunctionEntryPointBase


class ExpressionMakeAsyncgenObject(
    ExpressionNoSideEffectsMixin, ChildHavingAsyncgenRefMixin, ExpressionBase
):
    kind = "EXPRESSION_MAKE_ASYNCGEN_OBJECT"

    named_children = ("asyncgen_ref",)

    __slots__ = ("variable_closure_traces",)

    def __init__(self, asyncgen_ref, source_ref):
        assert asyncgen_ref.getFunctionBody().isExpressionAsyncgenObjectBody()

        ChildHavingAsyncgenRefMixin.__init__(self, asyncgen_ref=asyncgen_ref)

        ExpressionBase.__init__(self, source_ref)

        self.variable_closure_traces = []

    def getDetailsForDisplay(self):
        return {"asyncgen": self.subnode_asyncgen_ref.getFunctionBody().getCodeName()}

    def computeExpression(self, trace_collection):
        self.variable_closure_traces = []

        for (
            closure_variable
        ) in self.subnode_asyncgen_ref.getFunctionBody().getClosureVariables():
            trace = trace_collection.getVariableCurrentTrace(closure_variable)
            trace.addNameUsage()

            self.variable_closure_traces.append((closure_variable, trace))

        # TODO: Asyncgen body may know something too.
        return self, None, None

    def getClosureVariableVersions(self):
        return self.variable_closure_traces


class ExpressionAsyncgenObjectBody(ExpressionFunctionEntryPointBase):
    kind = "EXPRESSION_ASYNCGEN_OBJECT_BODY"

    __slots__ = ("qualname_setup", "needs_generator_return_exit")

    def __init__(self, provider, name, code_object, flags, auto_release, source_ref):
        ExpressionFunctionEntryPointBase.__init__(
            self,
            provider=provider,
            name=name,
            code_object=code_object,
            code_prefix="asyncgen",
            flags=flags,
            auto_release=auto_release,
            source_ref=source_ref,
        )

        self.needs_generator_return_exit = False

        self.qualname_setup = None

    def getFunctionName(self):
        return self.name

    def markAsNeedsGeneratorReturnHandling(self):
        self.needs_generator_return_exit = True

    def needsGeneratorReturnExit(self):
        return self.needs_generator_return_exit

    @staticmethod
    def needsCreation():
        return False

    @staticmethod
    def isUnoptimized():
        return False



