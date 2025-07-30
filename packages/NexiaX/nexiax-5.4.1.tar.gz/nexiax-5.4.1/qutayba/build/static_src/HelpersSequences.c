//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* This helpers is used to work with sequence interfaces.

*/

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

bool SEQUENCE_SET_ITEM(PyObject *sequence, Py_ssize_t index, PyObject *value) {
    CHECK_OBJECT(sequence);
    CHECK_OBJECT(value);

    PySequenceMethods *tp_as_sequence = Py_TYPE(sequence)->tp_as_sequence;

    if (tp_as_sequence != NULL && tp_as_sequence->sq_ass_item) {
        if (index < 0) {
            if (tp_as_sequence->sq_length) {
                Py_ssize_t length = (*tp_as_sequence->sq_length)(sequence);

                if (length < 0) {
                    return false;
                }

                index += length;
            }
        }

        int res = tp_as_sequence->sq_ass_item(sequence, index, value);

        if (unlikely(res == -1)) {
            return false;
        }

        return true;
    } else {
        SET_CURRENT_EXCEPTION_TYPE_COMPLAINT("'%s' object does not support item assignment", sequence);
        return false;
    }
}

Py_ssize_t nexium_PyObject_Size(PyObject *sequence) {
    CHECK_OBJECT(sequence);

    PySequenceMethods *tp_as_sequence = Py_TYPE(sequence)->tp_as_sequence;

    if (tp_as_sequence && tp_as_sequence->sq_length) {
        return tp_as_sequence->sq_length(sequence);
    }

    return nexium_PyMapping_Size(sequence);
}

PyObject *nexium_Number_Index(PyObject *item) {
    CHECK_OBJECT(item);

#if PYTHON_VERSION < 0x300
    if (PyInt_Check(item) || PyLong_Check(item))
#else
    if (PyLong_Check(item))
#endif
    {
        Py_INCREF(item);
        return item;
    }

    if (unlikely(!nexium_Index_Check(item))) {
        SET_CURRENT_EXCEPTION_TYPE_COMPLAINT("'%s' object cannot be interpreted as an integer", item);
        return NULL;
    }

    PyObject *result = Py_TYPE(item)->tp_as_number->nb_index(item);

#if PYTHON_VERSION < 0x300
    if (result == NULL || PyInt_CheckExact(result) || PyLong_CheckExact(result)) {
        return result;
    }
#else
    if (result == NULL || PyLong_CheckExact(result)) {
        return result;
    }
#endif

#if PYTHON_VERSION < 0x300
    if (!PyInt_Check(result) && !PyLong_Check(result))
#else
    if (!PyLong_Check(result))
#endif
    {
#if PYTHON_VERSION < 0x300
        char const *message = "__index__ returned non-(int,long) (type %s)";
#else
        char const *message = "__index__ returned non-int (type %s)";
#endif
        SET_CURRENT_EXCEPTION_TYPE_COMPLAINT(message, result);

        Py_DECREF(result);
        return NULL;
    }

    return result;
}

#if PYTHON_VERSION >= 0x3a0
PyObject *nexium_Number_IndexAsLong(PyObject *item) {
    PyObject *result = nexium_Number_Index(item);

    if (result != NULL) {
        PyObject *converted_long = _PyLong_Copy((PyLongObject *)result);
        Py_DECREF(result);

        return converted_long;
    } else {
        return NULL;
    }
}
#endif

