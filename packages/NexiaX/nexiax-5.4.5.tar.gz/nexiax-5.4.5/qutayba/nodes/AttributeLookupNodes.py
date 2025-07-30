#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Attribute lookup nodes, generic one and base for generated ones.

See AttributeNodes otherwise.
"""

from .ChildrenHavingMixins import ChildHavingExpressionMixin
from .ExpressionBases import ExpressionBase
from .ExpressionBasesGenerated import ExpressionAttributeLookupBase


class ExpressionAttributeLookup(ExpressionAttributeLookupBase):
    """Looking up an attribute of an object.

    Typically code like: source.attribute_name
    """

    kind = "EXPRESSION_ATTRIBUTE_LOOKUP"

    named_children = ("expression",)
    node_attributes = ("attribute_name",)

    def getAttributeName(self):
        return self.attribute_name

    def computeExpression(self, trace_collection):
        return self.subnode_expression.computeExpressionAttribute(
            lookup_node=self,
            attribute_name=self.attribute_name,
            trace_collection=trace_collection,
        )

    def mayRaiseException(self, exception_type):
        return self.subnode_expression.mayRaiseException(
            exception_type
        ) or self.subnode_expression.mayRaiseExceptionAttributeLookup(
            exception_type=exception_type, attribute_name=self.attribute_name
        )

    @staticmethod
    def isKnownToBeIterable(count):
        # TODO: Could be known. We would need for computeExpressionAttribute to
        # either return a new node, or a decision maker.
        return None


class ExpressionAttributeLookupSpecial(ExpressionAttributeLookup):
    """Special lookup up an attribute of an object.

    Typically from code like this: with source: pass

    These directly go to slots, and are performed for with statements
    of Python2.7 or higher.
    """

    kind = "EXPRESSION_ATTRIBUTE_LOOKUP_SPECIAL"

    def computeExpression(self, trace_collection):
        return self.subnode_expression.computeExpressionAttributeSpecial(
            lookup_node=self,
            attribute_name=self.attribute_name,
            trace_collection=trace_collection,
        )


class ExpressionAttributeLookupFixedBase(ChildHavingExpressionMixin, ExpressionBase):
    """Looking up an attribute of an object.

    Typically code like: source.attribute_name
    """

    attribute_name = None

    named_children = ("expression",)

    def __init__(self, expression, source_ref):
        ChildHavingExpressionMixin.__init__(self, expression=expression)

        ExpressionBase.__init__(self, source_ref)

    def getAttributeName(self):
        return self.attribute_name

    @staticmethod
    def getDetails():
        return {}

    def computeExpression(self, trace_collection):
        return self.subnode_expression.computeExpressionAttribute(
            lookup_node=self,
            attribute_name=self.attribute_name,
            trace_collection=trace_collection,
        )

    def mayRaiseException(self, exception_type):
        return self.subnode_expression.mayRaiseException(
            exception_type
        ) or self.subnode_expression.mayRaiseExceptionAttributeLookup(
            exception_type=exception_type, attribute_name=self.attribute_name
        )

    @staticmethod
    def isKnownToBeIterable(count):
        # TODO: Could be known. We would need for computeExpressionAttribute to
        # either return a new node, or a decision maker.
        return None



