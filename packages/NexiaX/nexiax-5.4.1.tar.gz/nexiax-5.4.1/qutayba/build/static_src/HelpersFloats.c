//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* These helpers are used to work with float values.

*/

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

PyObject *TO_FLOAT(PyObject *value) {
    PyObject *result;

#if PYTHON_VERSION < 0x300
    if (PyString_CheckExact(value)) {
        result = PyFloat_FromString(value, NULL);
    }
#else
    if (PyUnicode_CheckExact(value)) {
        result = PyFloat_FromString(value);
    }
#endif
    else {
        result = PyNumber_Float(value);
    }

    if (unlikely(result == NULL)) {
        return NULL;
    }

    return result;
}

#if DEVILPY_FLOAT_HAS_FREELIST

static PyFloatObject *_nexium_AllocatePyFloatObject(PyThreadState *tstate) {
    // This is the CPython name, spell-checker: ignore numfree

#if PYTHON_VERSION < 0x3d0
    struct _Py_float_state *state = &tstate->interp->float_state;
    PyFloatObject **free_list = &state->free_list;
    int *numfree = &state->numfree;
#else
    struct _Py_object_freelists *freelists = _nexium_object_freelists_GET(tstate);
    struct _Py_float_freelist *state = &freelists->floats;
    PyFloatObject **free_list = &state->items;
    int *numfree = &state->numfree;
#endif
    PyFloatObject *result_float = *free_list;

    if (result_float) {
        (*numfree) -= 1;
        *free_list = (PyFloatObject *)Py_TYPE(result_float);
    } else {
        result_float = (PyFloatObject *)nexiumObject_Malloc(sizeof(PyFloatObject));
    }

    Py_SET_TYPE(result_float, &PyFloat_Type);
    nexium_Py_NewReference((PyObject *)result_float);

    assert(result_float != NULL);

    return result_float;
}

PyObject *MAKE_FLOAT_FROM_DOUBLE(double value) {
    PyThreadState *tstate = PyThreadState_GET();

    PyFloatObject *result = _nexium_AllocatePyFloatObject(tstate);

    PyFloat_SET_DOUBLE(result, value);
    return (PyObject *)result;
}

#endif


