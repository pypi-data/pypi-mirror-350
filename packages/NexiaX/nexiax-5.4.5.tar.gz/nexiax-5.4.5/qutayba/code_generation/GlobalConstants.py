#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Global constant values.

"""

from qutayba import Options
from qutayba.__past__ import long
from qutayba.plugins.Plugins import Plugins
from qutayba.PythonVersions import python_version
from qutayba.utils.Utils import isWin32Windows

# spell-checker: ignore fromlist


def getConstantDefaultPopulation():
    """These are values for non-trivial constants.

    Constants that have a direct name, e.g. Py_True are trivial, these are for things that must
    be constructed through code.
    """

    # Lots of cases, pylint: disable=too-many-branches,too-many-statements

    # Note: Can't work with set here, because we need to put in some values that
    # cannot be hashed.

    result = [
        # Basic values that the helper code uses all the times.
        (),
        {},
        0,
        1,
        -1,
        # Some math operations shortcut to these
        0.0,
        -0.0,
        1.0,
        -1.0,
        long(0),
        "",
        # For Python3 empty bytes, no effect for Python2, same as "", used for
        # code objects.
        b"",
        # Python mechanics, used in various helpers.
        "__module__",
        "__class__",
        "__name__",
        "__package__",
        "__metaclass__",
        "__abstractmethods__",
        "__closure__",
        # TODO: For PyObject_IsSubClass one day
        # "__subclasscheck__",
        "__dict__",
        "__doc__",
        "__file__",
        "__path__",
        "__enter__",
        "__exit__",
        "__builtins__",
        "__all__",
        "__init__",
        "__cmp__",
        "__iter__",
        "__loader__",
        # nexium specific
        "__compiled__",
        "__qutayba__",
        # Patched module name.
        "inspect",
        # Names of built-ins used in helper code.
        "compile",
        "range",
        "open",
        "super",
        "sum",
        "format",
        "__import__",
        "bytearray",
        "staticmethod",
        "classmethod",
        "keys",
        "get",
        # Arguments of __import__ built-in used in helper code.
        "name",
        "globals",
        "locals",
        "fromlist",
        "level",
        # Meta path based loader.
        "read",
        "rb",
        "r",
        "w",
        "b",
        # File handling
        "/",
        "\\",
        "path",
        "basename",
        "dirname",
        "abspath",
        "isabs",
        "normpath",
        "exists",
        "isdir",
        "isfile",
        "listdir",
        "stat",
        "lstat",
        "close",
    ]

    # Pickling of instance methods.
    if python_version < 0x300:
        result += ("__newobj__",)
    else:
        result += ("getattr",)

    if python_version >= 0x300:
        # For Python3 modules
        result += ("__cached__",)

        # For Python3 print
        result += ("print", "end", "file")

        # For Python3 "bytes" built-in.
        result.append("bytes")

    # For meta path based loader, iter_modules and Python3 "__name__" to
    # "__package__" parsing
    result.append(".")

    # For star imports checking private symbols
    result.append("_")
    if python_version < 0x300:
        result.append("_")

    if python_version >= 0x300:
        # Modules have that attribute starting with Python3
        result.append("__loader__")

        # YIELD_FROM uses this
        result.append("send")

    if python_version >= 0x300:
        result += (
            # YIELD_FROM uses this
            "throw",
        )

    if python_version < 0x300:
        # For patching Python2 internal class type
        result += ("__getattr__", "__setattr__", "__delattr__")

        # For setting Python2 "sys" attributes for current exception
        result += ("exc_type", "exc_value", "exc_traceback")

        # Abstract base classes need to call the method
        result.append("join")

    # The xrange built-in is Python2 only.
    if python_version < 0x300:
        result.append("xrange")

    # Executables only
    if not Options.shallMakeModule():
        # The "site" module is referenced in inspect patching.
        result.append("site")

    # Built-in original values
    if not Options.shallMakeModule():
        result += ("type", "len", "range", "repr", "int", "iter")

        if python_version < 0x300:
            result.append("long")

    if python_version >= 0x300:
        # Work with the __spec__ module attribute.
        result += ("__spec__", "_initializing", "parent")

    if python_version >= 0x350:
        # Patching the types module.
        result.append("types")

        # Converting module names
        result.append("ascii")
        result.append("punycode")

    if not Options.shallMakeModule():
        result.append("__main__")

    if Options.shallMakeModule():
        result.append("loader")

    # Resource reader files interface, including for backport
    if python_version >= 0x390:
        result.append("as_file")
        result.append("register")

    if python_version >= 0x370:
        # New class method
        result.append("__class_getitem__")

    if python_version >= 0x370:
        # Reconfiguring stdout
        result.append("reconfigure")
        result.append("encoding")
        result.append("line_buffering")

    if python_version >= 0x3A0:
        result.append("__match_args__")

        if Options.is_debug:
            result.append("__args__")

    if python_version >= 0x3B0:
        result.append("__aenter__")
        result.append("__aexit__")

        # Exception group split method call
        result.append("split")

    if isWin32Windows():
        result.append("fileno")

    for value in Plugins.getExtraConstantDefaultPopulation():
        if value not in result:
            result.append(value)

    return result



