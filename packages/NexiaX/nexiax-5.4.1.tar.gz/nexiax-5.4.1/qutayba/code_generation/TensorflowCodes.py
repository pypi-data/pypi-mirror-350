#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Code generation for tensorflow module specific stuff. """

from .BuiltinCodes import getBuiltinCallViaSpecCode
from .ImportCodes import getImportModuleNameHardCode
from .JitCodes import addUncompiledFunctionSourceDict


def generateTensorflowFunctionCallCode(to_name, expression, emit, context):
    """This is for tensorflow.function calls."""

    # TODO: Have global cached forms of hard attribute lookup results too.
    tensorflow_function_name = context.allocateTempName(
        "tensorflow_function", unique=True
    )

    getImportModuleNameHardCode(
        to_name=tensorflow_function_name,
        module_name="tensorflow",
        import_name="function",
        needs_check=False,
        emit=emit,
        context=context,
    )

    # Include source code of "tensorflow.function" decorated functions.
    addUncompiledFunctionSourceDict(func_value=expression.subnode_func, context=context)

    getBuiltinCallViaSpecCode(
        spec=expression.spec,
        called_name=tensorflow_function_name,
        to_name=to_name,
        expression=expression,
        emit=emit,
        context=context,
    )



