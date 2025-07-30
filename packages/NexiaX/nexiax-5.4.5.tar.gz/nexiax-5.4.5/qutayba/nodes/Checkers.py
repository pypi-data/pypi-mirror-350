#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Node children checkers.

The role of checkers is to make sure that node children have specific value
types only.

"""


def checkStatementsSequenceOrNone(value):
    if value is not None:
        assert value.kind == "STATEMENTS_SEQUENCE", value

        if not value.subnode_statements:
            return None

    return value


def checkStatementsSequence(value):
    assert value is not None and value.kind == "STATEMENTS_SEQUENCE", value

    return value


def convertNoneConstantToNone(node):
    if node is None or node.isExpressionConstantNoneRef():
        return None
    else:
        return node


def convertEmptyStrConstantToNone(node):
    if node is None or node.isExpressionConstantStrEmptyRef():
        return None
    else:
        return node



