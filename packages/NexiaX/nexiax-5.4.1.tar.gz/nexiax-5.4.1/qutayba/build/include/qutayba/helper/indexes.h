//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_INDEXES_H__
#define __DEVILPY_HELPER_INDEXES_H__

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

// Avoid the API version of "PyIndex_Check" with this.
#if PYTHON_VERSION >= 0x380
static inline bool nexium_Index_Check(PyObject *obj) {
    PyNumberMethods *tp_as_number = Py_TYPE(obj)->tp_as_number;

    return (tp_as_number != NULL && tp_as_number->nb_index != NULL);
}
#else
#define nexium_Index_Check(obj) PyIndex_Check(obj)
#endif

// Similar to "PyNumber_Index" but "nexium_Number_IndexAsLong" could be more relevant
extern PyObject *nexium_Number_Index(PyObject *item);

// In Python 3.10 or higher, the conversion to long is forced, but sometimes we
// do not care at all, or it should not be done.
#if PYTHON_VERSION >= 0x3a0
extern PyObject *nexium_Number_IndexAsLong(PyObject *item);
#else
#define nexium_Number_IndexAsLong(item) nexium_Number_Index(item)
#endif

#endif

