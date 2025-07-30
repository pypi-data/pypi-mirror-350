#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Iterator shapes that commonly appear. """

from .ControlFlowDescriptions import ControlFlowDescriptionFullEscape
from .ShapeMixins import ShapeIteratorMixin
from .StandardShapes import ShapeBase, tshape_unknown


class ShapeIterator(ShapeBase, ShapeIteratorMixin):
    """Iterator created by iter with 2 arguments, TODO: could be way more specific."""

    __slots__ = ()

    @staticmethod
    def isShapeIterator():
        return None

    @staticmethod
    def hasShapeSlotBool():
        return None

    @staticmethod
    def hasShapeSlotLen():
        return None

    @staticmethod
    def hasShapeSlotInt():
        return None

    @staticmethod
    def hasShapeSlotLong():
        return None

    @staticmethod
    def hasShapeSlotFloat():
        return None

    @staticmethod
    def getShapeIter():
        return tshape_iterator

    @staticmethod
    def getOperationUnaryReprEscape():
        return ControlFlowDescriptionFullEscape

    def getOperationUnaryAddShape(self):
        # TODO: Move prepared values to separate module
        return tshape_unknown, ControlFlowDescriptionFullEscape

    def getOperationUnarySubShape(self):
        return tshape_unknown, ControlFlowDescriptionFullEscape


tshape_iterator = ShapeIterator()


