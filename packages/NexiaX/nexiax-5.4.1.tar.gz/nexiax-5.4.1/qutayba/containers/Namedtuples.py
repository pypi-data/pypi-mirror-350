#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" This module is only an abstraction of namedtuple.

It works around bugs present in some version of Python, and provides extra
methods like "asDict".
"""

from collections import namedtuple


def makeNamedtupleClass(name, element_names):
    # TODO: Have a namedtuple factory that does these things.

    namedtuple_class = namedtuple(name, element_names)

    class DynamicNamedtuple(namedtuple_class):
        __qualname__ = name

        # Avoids bugs on early Python3.4 and Python3.5 versions.
        __slots__ = ()

        def asDict(self):
            return self._asdict()

        def replace(self, **kwargs):
            new_data = self.asDict()
            new_data.update(**kwargs)

            return self.__class__(**new_data)

    DynamicNamedtuple.__name__ = name

    return DynamicNamedtuple



