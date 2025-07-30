//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* This helpers is used to work with mapping interfaces.

*/

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

Py_ssize_t nexium_PyMapping_Size(PyObject *mapping) {
    CHECK_OBJECT(mapping);

    PyMappingMethods *tp_as_mapping = Py_TYPE(mapping)->tp_as_mapping;

    if (tp_as_mapping != NULL && tp_as_mapping->mp_length) {
        Py_ssize_t result = tp_as_mapping->mp_length(mapping);
        assert(result >= 0);
        return result;
    }

    if (Py_TYPE(mapping)->tp_as_sequence && Py_TYPE(mapping)->tp_as_sequence->sq_length) {
        SET_CURRENT_EXCEPTION_TYPE_COMPLAINT("%s is not a mapping", mapping);
        return -1;
    }

    SET_CURRENT_EXCEPTION_TYPE_COMPLAINT("object of type '%s' has no len()", mapping);
    return -1;
}


