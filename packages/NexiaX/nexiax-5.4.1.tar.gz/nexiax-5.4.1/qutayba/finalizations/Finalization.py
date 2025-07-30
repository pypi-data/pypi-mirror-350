#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Finalizations. Last steps directly before code creation is called.

Here the final tasks are executed. Things normally volatile during optimization
can be computed here, so the code generation can be quick and doesn't have to
check it many times.

"""

from qutayba.tree import Operations

from .FinalizeMarkups import FinalizeMarkups


def prepareCodeGeneration(module):
    visitor = FinalizeMarkups(module)
    Operations.visitTree(module, visitor)



