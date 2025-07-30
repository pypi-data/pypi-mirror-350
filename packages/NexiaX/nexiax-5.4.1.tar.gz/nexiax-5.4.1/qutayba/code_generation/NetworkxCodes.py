#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Code generation for networkx module specific stuff. """

from .BuiltinCodes import getBuiltinCallViaSpecCode
from .ImportCodes import getImportModuleNameHardCode
from .JitCodes import addUncompiledFunctionSourceDict


def generateNetworkxUtilsDecoratorsArgmapCallCode(to_name, expression, emit, context):
    """This is for networkx.utils.decorators.argmap calls."""

    # TODO: Have global cached forms of hard attribute lookup results too.
    argmap_class_name = context.allocateTempName("argmap_class", unique=True)

    getImportModuleNameHardCode(
        to_name=argmap_class_name,
        module_name="networkx.utils.decorators",
        import_name="argmap",
        needs_check=False,
        emit=emit,
        context=context,
    )

    addUncompiledFunctionSourceDict(func_value=expression.subnode_func, context=context)

    getBuiltinCallViaSpecCode(
        spec=expression.spec,
        called_name=argmap_class_name,
        to_name=to_name,
        expression=expression,
        emit=emit,
        context=context,
    )



