#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


"""List operation specs. """

from qutayba.nodes.shapes.BuiltinTypeShapes import (
    tshape_int_or_long,
    tshape_list,
    tshape_none,
)

from .BuiltinParameterSpecs import (
    BuiltinMethodParameterSpecBase,
    BuiltinMethodParameterSpecNoKeywordsBase,
)


class ListMethodSpecNoKeywords(BuiltinMethodParameterSpecNoKeywordsBase):
    __slots__ = ()

    method_prefix = "list"


class ListMethodSpec(BuiltinMethodParameterSpecBase):
    __slots__ = ()

    method_prefix = "list"


# Python3 only
list_clear_spec = ListMethodSpecNoKeywords(
    "clear", arg_names=(), type_shape=tshape_none
)

list_append_spec = ListMethodSpecNoKeywords(
    "append", arg_names=("item",), type_shape=tshape_none
)
list_copy_spec = ListMethodSpecNoKeywords("copy", arg_names=(), type_shape=tshape_list)
list_count_spec = ListMethodSpecNoKeywords(
    "count", arg_names=("value",), type_shape=tshape_int_or_long
)
list_extend_spec = ListMethodSpecNoKeywords(
    "extend", arg_names=("value",), type_shape=tshape_none
)
list_index_spec = ListMethodSpecNoKeywords(
    "index",
    arg_names=("value", "start", "stop"),
    default_count=2,
    type_shape=tshape_int_or_long,
)
list_insert_spec = ListMethodSpecNoKeywords(
    "insert", arg_names=("index", "item"), type_shape=tshape_none
)
list_pop_spec = ListMethodSpecNoKeywords("pop", arg_names=("index",), default_count=1)
list_remove_spec = ListMethodSpecNoKeywords(
    "remove", arg_names=("value",), type_shape=tshape_none
)
list_reverse_spec = ListMethodSpecNoKeywords(
    "reverse", arg_names=(), type_shape=tshape_none
)

# TODO: Version dependent with keyword only args in Python3
# list_sort_spec = ListMethodSpec(
#     "sort", arg_names=("key", "reverse"), default_count=2, type_shape=tshape_none
# )


