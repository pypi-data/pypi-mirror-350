#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Code generation for JIT specific stuff, preserving source code for runtime. """

from qutayba.Options import isStandaloneMode


def addUncompiledFunctionSourceDict(func_value, context):
    if (
        isStandaloneMode()
        and func_value is not None
        and func_value.isExpressionFunctionCreation()
    ):
        function_ref = func_value.subnode_function_ref

        function_super_qualified_name = function_ref.getFunctionSuperQualifiedName()
        function_source_code = function_ref.getFunctionSourceCode()

        context.addModuleInitCode(
            """\
SET_UNCOMPILED_FUNCTION_SOURCE_DICT(%s, %s);
"""
            % (
                context.getConstantCode(function_super_qualified_name),
                context.getConstantCode(function_source_code),
            )
        )



