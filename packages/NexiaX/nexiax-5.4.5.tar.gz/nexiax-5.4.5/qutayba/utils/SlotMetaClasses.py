#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Helper for portable metaclasses that do checks. """

from abc import ABCMeta

from qutayba.Errors import nexiumNodeDesignError


def getMetaClassBase(meta_class_prefix, require_slots):
    """For Python2/3 compatible source, we create a base class that has the metaclass
    used and doesn't require making a syntax choice.

    Also this allows to enforce the proper usage of "__slots__" for all classes using
    it optionally.
    """

    class MetaClass(ABCMeta):
        def __new__(
            mcs, name, bases, dictionary
        ):  # pylint: disable=I0021,arguments-differ
            if require_slots:
                for base in bases:
                    if base is not object and "__slots__" not in base.__dict__:
                        raise nexiumNodeDesignError(
                            name, "All bases must set __slots__.", base
                        )

                if "__slots__" not in dictionary:
                    raise nexiumNodeDesignError(name, "Class must set __slots__.", name)

            return ABCMeta.__new__(mcs, name, bases, dictionary)

    MetaClassBase = MetaClass(
        "%sMetaClassBase" % meta_class_prefix,
        (object,),
        {"__slots__": ()} if require_slots else {},
    )

    return MetaClassBase



