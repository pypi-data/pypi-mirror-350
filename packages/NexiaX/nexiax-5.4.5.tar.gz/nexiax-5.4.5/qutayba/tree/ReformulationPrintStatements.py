#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Reformulation of print statements.

Consult the Developer Manual for information. TODO: Add ability to sync
source code comments with Developer Manual sections.

"""

from qutayba.nodes.ComparisonNodes import ExpressionComparisonIs
from qutayba.nodes.ConditionalNodes import makeStatementConditional
from qutayba.nodes.ConstantRefNodes import ExpressionConstantNoneRef
from qutayba.nodes.ImportNodes import makeExpressionImportModuleNameHard
from qutayba.nodes.PrintNodes import StatementPrintNewline, StatementPrintValue
from qutayba.nodes.VariableAssignNodes import makeStatementAssignmentVariable
from qutayba.nodes.VariableRefNodes import ExpressionTempVariableRef

from .ReformulationTryFinallyStatements import makeTryFinallyReleaseStatement
from .TreeHelpers import (
    buildNode,
    buildNodeTuple,
    makeStatementsSequenceFromStatements,
)


def buildPrintNode(provider, node, source_ref):
    # "print" statements, should only occur with Python2.

    if node.dest is not None:
        temp_scope = provider.allocateTempScope("print")

        tmp_target_variable = provider.allocateTempVariable(
            temp_scope=temp_scope, name="target", temp_type="object"
        )

        target_default_statement = makeStatementAssignmentVariable(
            variable=tmp_target_variable,
            source=makeExpressionImportModuleNameHard(
                module_name="sys",
                import_name="stdout",
                module_guaranteed=True,
                source_ref=source_ref,
            ),
            source_ref=source_ref,
        )

        statements = [
            makeStatementAssignmentVariable(
                variable=tmp_target_variable,
                source=buildNode(
                    provider=provider, node=node.dest, source_ref=source_ref
                ),
                source_ref=source_ref,
            ),
            makeStatementConditional(
                condition=ExpressionComparisonIs(
                    left=ExpressionTempVariableRef(
                        variable=tmp_target_variable, source_ref=source_ref
                    ),
                    right=ExpressionConstantNoneRef(source_ref=source_ref),
                    source_ref=source_ref,
                ),
                yes_branch=target_default_statement,
                no_branch=None,
                source_ref=source_ref,
            ),
        ]

    values = buildNodeTuple(provider=provider, nodes=node.values, source_ref=source_ref)

    if node.dest is not None:
        print_statements = [
            StatementPrintValue(
                dest=ExpressionTempVariableRef(
                    variable=tmp_target_variable, source_ref=source_ref
                ),
                value=value,
                source_ref=source_ref,
            )
            for value in values
        ]

        if node.nl:
            print_statements.append(
                StatementPrintNewline(
                    dest=ExpressionTempVariableRef(
                        variable=tmp_target_variable, source_ref=source_ref
                    ),
                    source_ref=source_ref,
                )
            )

        statements.append(
            makeTryFinallyReleaseStatement(
                provider=provider,
                tried=print_statements,
                variables=(tmp_target_variable,),
                source_ref=source_ref,
            )
        )
    else:
        statements = [
            StatementPrintValue(dest=None, value=value, source_ref=source_ref)
            for value in values
        ]

        if node.nl:
            statements.append(StatementPrintNewline(dest=None, source_ref=source_ref))

    return makeStatementsSequenceFromStatements(*statements)



