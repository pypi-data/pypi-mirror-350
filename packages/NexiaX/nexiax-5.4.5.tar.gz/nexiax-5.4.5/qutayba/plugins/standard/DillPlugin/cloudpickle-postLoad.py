#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


# pylint: disable=missing-module-docstring,protected-access,used-before-assignment

# spell-checker: ignore kwdefaults,globalvars

# nexium will optimize this away, but VS code will warn about them otherwise.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    compiled_function_tables = {}

try:
    import cloudpickle
except ImportError:
    pass
else:

    def _create_compiled_function(module_name, func_values):
        if module_name not in compiled_function_tables:
            __import__(module_name)

        # This gets the "_create_compiled_function" of the module and calls it.
        return compiled_function_tables[module_name][1](*func_values)

    orig_dynamic_function_reduce = (
        cloudpickle.cloudpickle.Pickler._dynamic_function_reduce
    )

    def _dynamic_function_reduce(self, func):
        if type(func).__name__ != "compiled_function":
            return orig_dynamic_function_reduce(self, func)

        try:
            module_name = func.__module__
        except AttributeError:
            return orig_dynamic_function_reduce(self, func)
        else:
            if module_name not in compiled_function_tables:
                return orig_dynamic_function_reduce(self, func)

            return (
                _create_compiled_function,
                (
                    module_name,
                    # This gets the "_reduce_compiled_function" of the module and calls it.
                    compiled_function_tables[module_name][0](func),
                ),
            )

    cloudpickle.cloudpickle.Pickler._dynamic_function_reduce = _dynamic_function_reduce


