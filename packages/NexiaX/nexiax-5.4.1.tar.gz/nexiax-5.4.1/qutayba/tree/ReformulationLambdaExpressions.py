#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Reformulation of lambda expressions.

Consult the Developer Manual for information. TODO: Add ability to sync
source code comments with Developer Manual sections.

"""

from qutayba.nodes.ComparisonNodes import ExpressionComparisonIsNot
from qutayba.nodes.ConditionalNodes import makeStatementConditional
from qutayba.nodes.ConstantRefNodes import ExpressionConstantNoneRef
from qutayba.nodes.FrameNodes import (
    StatementsFrameFunction,
    StatementsFrameGenerator,
)
from qutayba.nodes.FunctionNodes import (
    ExpressionFunctionRef,
    makeExpressionFunctionCreation,
)
from qutayba.nodes.GeneratorNodes import (
    ExpressionGeneratorObjectBody,
    ExpressionMakeGeneratorObject,
)
from qutayba.nodes.ReturnNodes import StatementReturn
from qutayba.nodes.StatementNodes import StatementExpressionOnly
from qutayba.nodes.VariableAssignNodes import makeStatementAssignmentVariable
from qutayba.nodes.VariableRefNodes import ExpressionTempVariableRef
from qutayba.nodes.YieldNodes import ExpressionYield
from qutayba.PythonVersions import python_version

from .ReformulationFunctionStatements import (
    buildFunctionWithParsing,
    buildParameterAnnotations,
    buildParameterKwDefaults,
)
from .ReformulationTryFinallyStatements import makeTryFinallyReleaseStatement
from .TreeHelpers import (
    buildNode,
    buildNodeTuple,
    detectFunctionBodyKind,
    getKind,
    makeStatementsSequenceFromStatement,
    mergeStatements,
)


def buildLambdaNode(provider, node, source_ref):
    # Many details to deal with, pylint: disable=too-many-locals

    assert getKind(node) == "Lambda"

    function_kind, flags = detectFunctionBodyKind(nodes=(node.body,))

    outer_body, function_body, code_object = buildFunctionWithParsing(
        provider=provider,
        function_kind=function_kind,
        name="<lambda>",
        function_doc=None,
        flags=flags,
        node=node,
        source_ref=source_ref,
    )

    if function_kind == "Function":
        code_body = function_body
    else:
        code_body = ExpressionGeneratorObjectBody(
            provider=function_body,
            name="<lambda>",
            code_object=code_object,
            flags=None,
            auto_release=None,
            source_ref=source_ref,
        )
        code_body.qualname_provider = provider

    if function_kind == "Generator":
        function_body.setChildBody(
            makeStatementsSequenceFromStatement(
                statement=StatementReturn(
                    expression=ExpressionMakeGeneratorObject(
                        generator_ref=ExpressionFunctionRef(
                            function_body=code_body, source_ref=source_ref
                        ),
                        source_ref=source_ref,
                    ),
                    source_ref=source_ref,
                )
            )
        )

    defaults = buildNodeTuple(provider, node.args.defaults, source_ref)
    kw_defaults = buildParameterKwDefaults(
        provider=provider, node=node, function_body=function_body, source_ref=source_ref
    )

    body = buildNode(provider=code_body, node=node.body, source_ref=source_ref)

    if function_kind == "Generator":
        if python_version < 0x270:
            tmp_return_value = code_body.allocateTempVariable(
                temp_scope=None, name="yield_return", temp_type="object"
            )

            statements = (
                makeStatementAssignmentVariable(
                    variable=tmp_return_value, source=body, source_ref=source_ref
                ),
                makeStatementConditional(
                    condition=ExpressionComparisonIsNot(
                        left=ExpressionTempVariableRef(
                            variable=tmp_return_value, source_ref=source_ref
                        ),
                        right=ExpressionConstantNoneRef(source_ref=source_ref),
                        source_ref=source_ref,
                    ),
                    yes_branch=StatementExpressionOnly(
                        expression=ExpressionYield(
                            expression=ExpressionTempVariableRef(
                                variable=tmp_return_value, source_ref=source_ref
                            ),
                            source_ref=source_ref,
                        ),
                        source_ref=source_ref,
                    ),
                    no_branch=None,
                    source_ref=source_ref,
                ),
            )
            body = makeTryFinallyReleaseStatement(
                provider=provider,
                tried=statements,
                variables=(tmp_return_value,),
                source_ref=source_ref,
            )
        else:
            body = StatementExpressionOnly(expression=body, source_ref=source_ref)
    else:
        body = StatementReturn(expression=body, source_ref=source_ref)

    if function_kind == "Generator":
        frame_class = StatementsFrameGenerator
    else:
        frame_class = StatementsFrameFunction

    body = frame_class(
        statements=mergeStatements((body,)),
        code_object=code_object,
        owner_code_name=code_body.getCodeName(),
        source_ref=body.getSourceReference(),
    )

    body = makeStatementsSequenceFromStatement(statement=body)

    code_body.setChildBody(body)

    annotations = buildParameterAnnotations(provider, node, source_ref)

    return makeExpressionFunctionCreation(
        function_ref=ExpressionFunctionRef(
            function_body=outer_body, source_ref=source_ref
        ),
        defaults=defaults,
        kw_defaults=kw_defaults,
        annotations=annotations,
        source_ref=source_ref,
    )



