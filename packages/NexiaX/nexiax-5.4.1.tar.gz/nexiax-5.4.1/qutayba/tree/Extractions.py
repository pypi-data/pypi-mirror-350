#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Extracting visitors.

This is used for lookahead supporting abstract execution. We need to e.g.
know the variables written by a piece of code ahead of abstractly executing a
loop.
"""

from .Operations import VisitorNoopMixin, visitTree


class VariableUsageUpdater(VisitorNoopMixin):
    def __init__(self, old_variable, new_variable):
        self.old_variable = old_variable
        self.new_variable = new_variable

    def onEnterNode(self, node):
        if (
            node.isStatementAssignmentVariable()
            or node.isStatementDelVariable()
            or node.isStatementReleaseVariable()
        ):
            if node.getVariable() is self.old_variable:
                node.setVariable(self.new_variable)


def updateVariableUsage(provider, old_variable, new_variable):
    visitor = VariableUsageUpdater(old_variable=old_variable, new_variable=new_variable)

    visitTree(provider, visitor)



