#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


"""Type operation specs. """

from .BuiltinParameterSpecs import BuiltinMethodParameterSpecBase


class TypeMethodSpec(BuiltinMethodParameterSpecBase):
    """Method spec of exactly the `type` built-in value/type."""

    __slots__ = ()

    method_prefix = "type"


type___prepare___spec = TypeMethodSpec(
    name="__prepare__", list_star_arg="args", dict_star_arg="kwargs"
)


