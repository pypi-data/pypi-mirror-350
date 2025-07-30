#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Operations on the tree.

This is mostly for the different kinds of visits that the node tree can have.
You can visit a scope, a tree (module), or every scope of a tree (module).

"""


def visitTree(tree, visitor):
    visitor.onEnterNode(tree)

    for visitable in tree.getVisitableNodes():
        if visitable is None:
            raise AssertionError("'None' child encountered", tree, tree.source_ref)

        visitTree(visitable, visitor)

    visitor.onLeaveNode(tree)


class VisitorNoopMixin(object):
    def onEnterNode(self, node):
        """Overloaded for operation before the node children were done."""

    def onLeaveNode(self, node):
        """Overloaded for operation after the node children were done."""



