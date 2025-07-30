//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_BOOLEAN_H__
#define __DEVILPY_HELPER_BOOLEAN_H__

// The slot in Python3 got renamed, compensate it like this.
#if PYTHON_VERSION >= 0x300
#define nb_nonzero nb_bool
#endif

DEVILPY_MAY_BE_UNUSED static int CHECK_IF_TRUE(PyObject *object) {
    CHECK_OBJECT(object);

    if (object == Py_True) {
        return 1;
    } else if (object == Py_False || object == Py_None) {
        return 0;
    } else {
        Py_ssize_t result;

        if (Py_TYPE(object)->tp_as_number != NULL && Py_TYPE(object)->tp_as_number->nb_nonzero != NULL) {
            result = (*Py_TYPE(object)->tp_as_number->nb_nonzero)(object);
        } else if (Py_TYPE(object)->tp_as_mapping != NULL && Py_TYPE(object)->tp_as_mapping->mp_length != NULL) {
            result = (*Py_TYPE(object)->tp_as_mapping->mp_length)(object);
        } else if (Py_TYPE(object)->tp_as_sequence != NULL && Py_TYPE(object)->tp_as_sequence->sq_length != NULL) {
            result = (*Py_TYPE(object)->tp_as_sequence->sq_length)(object);
        } else {
            return 1;
        }

        if (result > 0) {
            return 1;
        } else if (result == 0) {
            return 0;
        } else {
            return -1;
        }
    }
}

DEVILPY_MAY_BE_UNUSED static int CHECK_IF_FALSE(PyObject *object) {
    int result = CHECK_IF_TRUE(object);

    if (result == 0) {
        return 1;
    }
    if (result == 1) {
        return 0;
    }
    return -1;
}

DEVILPY_MAY_BE_UNUSED static inline PyObject *BOOL_FROM(bool value) {
    CHECK_OBJECT(Py_True);
    CHECK_OBJECT(Py_False);

    return value ? Py_True : Py_False;
}

#undef nb_nonzero

typedef enum {
    DEVILPY_BOOL_FALSE = 0,
    DEVILPY_BOOL_TRUE = 1,
    DEVILPY_BOOL_UNASSIGNED = 2,
    DEVILPY_BOOL_EXCEPTION = -1
} qutayba_bool;

typedef enum { DEVILPY_VOID_OK = 0, DEVILPY_VOID_EXCEPTION = 1 } qutayba_void;

#endif


