#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Finalize the markups

Set flags on functions and classes to indicate if a locals dict is really
needed.

Set a flag on loops if they really need to catch Continue and Break exceptions
or if it can be more simple code.

Set a flag on return statements and functions that require the use of
"ReturnValue" exceptions, or if it can be more simple code.

Set a flag on re-raises of exceptions if they can be simple throws or if they
are in another context.

"""

from qutayba import Tracing
from qutayba.PythonVersions import python_version
from qutayba.tree.Operations import VisitorNoopMixin


class FinalizeMarkups(VisitorNoopMixin):
    def __init__(self, module):
        self.module = module

    def onEnterNode(self, node):
        try:
            self._onEnterNode(node)
        except Exception:
            Tracing.printError(
                "Problem with %r at %s"
                % (node, node.getSourceReference().getAsString())
            )
            raise

    def _onEnterNode(self, node):
        # This has many different things it deals with, so there need to be a
        # lot of branches and statements, pylint: disable=too-many-branches

        if node.isStatementReturn() or node.isStatementGeneratorReturn():
            # Search up to the containing function, and check for a try/finally
            # containing the "return" statement.
            search = node.getParentReturnConsumer()

            if (
                search.isExpressionGeneratorObjectBody()
                or search.isExpressionCoroutineObjectBody()
                or search.isExpressionAsyncgenObjectBody()
            ):
                search.markAsNeedsGeneratorReturnHandling()

        if node.isExpressionFunctionCreation():
            if (
                not node.getParent().isExpressionFunctionCall()
                or node.getParent().subnode_function is not node
            ):
                node.subnode_function_ref.getFunctionBody().markAsNeedsCreation()

        if node.isExpressionFunctionCall():
            node.subnode_function.subnode_function_ref.getFunctionBody().markAsDirectlyCalled()

        if node.isExpressionFunctionRef():
            function_body = node.getFunctionBody()
            parent_module = function_body.getParentModule()

            if self.module is not parent_module:
                function_body.markAsCrossModuleUsed()

                self.module.addCrossUsedFunction(function_body)

        if node.isStatementAssignmentVariable():
            target_var = node.getVariable()
            assign_source = node.subnode_source

            if assign_source.isExpressionOperationBinary():
                left_arg = assign_source.subnode_left

                if left_arg.isExpressionVariableRefOrTempVariableRef():
                    if assign_source.subnode_left.getVariable() is target_var:
                        if assign_source.isInplaceSuspect():
                            node.markAsInplaceSuspect()
                elif left_arg.isExpressionLocalsVariableRefOrFallback():
                    # TODO: This might be bad.
                    assign_source.removeMarkAsInplaceSuspect()

            if target_var.isModuleVariable():
                pass

        if python_version < 0x300 and node.isStatementPublishException():
            node.getParentStatementsFrame().markAsFrameExceptionPreserving()

        if python_version >= 0x300:
            if (
                node.isExpressionYield()
                or node.isExpressionYieldFrom()
                or node.isExpressionYieldFromAwaitable()
            ):
                search = node.getParent()

                # TODO: This is best achieved by having different yield nodes
                # depending on containing function kind to begin with and should
                # be discovered during the build.

                while (
                    not search.isExpressionGeneratorObjectBody()
                    and not search.isExpressionCoroutineObjectBody()
                    and not search.isExpressionAsyncgenObjectBody()
                ):
                    last_search = search
                    search = search.getParent()

                    if (
                        search.isStatementTry()
                        and last_search == search.subnode_except_handler
                    ):
                        node.markAsExceptionPreserving()
                        break



