//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_CALLING_H__
#define __DEVILPY_CALLING_H__

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

// For exception test formatting and call code mostly.
extern char const *GET_CALLABLE_NAME(PyObject *object);
extern char const *GET_CALLABLE_DESC(PyObject *object);
extern char const *GET_CLASS_NAME(PyObject *class_object);
extern char const *GET_INSTANCE_CLASS_NAME(PyThreadState *tstate, PyObject *instance);

// Also used in generated helper code.
DEVILPY_MAY_BE_UNUSED static inline PyObject *nexium_CheckFunctionResult(PyThreadState *tstate, PyObject *callable,
                                                                        PyObject *result) {
    if (result == NULL) {
        if (unlikely(!HAS_ERROR_OCCURRED(tstate))) {
#if PYTHON_VERSION < 0x3b0
            SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_SystemError, "NULL result without error from call");
#else
            PyErr_Format(PyExc_SystemError, "%R returned NULL without setting an exception", callable);
#endif
        }

        return NULL;
    } else {
        // Some buggy C functions do this, and nexium inner workings can get
        // upset from it.
        if (unlikely(DROP_ERROR_OCCURRED(tstate))) {
            Py_DECREF(result);

#if PYTHON_VERSION < 0x3a0
            SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_SystemError, "result with error set from call");
#elif PYTHON_VERSION < 0x3b0
            SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_SystemError, "result with exception set from call");
#else
            SET_CURRENT_EXCEPTION_TYPE0_FORMAT1(PyExc_SystemError, "%s() returned a result with an exception set",
                                                GET_CALLABLE_NAME(callable));
#endif
            return NULL;
        }

        return result;
    }
}

DEVILPY_MAY_BE_UNUSED static PyObject *CALL_FUNCTION(PyThreadState *tstate, PyObject *function_object,
                                                    PyObject *positional_args, PyObject *named_args) {
    // Not allowed to enter with an error set. This often catches leaked errors from
    // elsewhere.
    assert(!HAS_ERROR_OCCURRED(tstate));

    CHECK_OBJECT(function_object);
    CHECK_OBJECT(positional_args);
    assert(named_args == NULL || Py_REFCNT(named_args) > 0);

    ternaryfunc call_slot = Py_TYPE(function_object)->tp_call;

    if (unlikely(call_slot == NULL)) {
        SET_CURRENT_EXCEPTION_TYPE_COMPLAINT("'%s' object is not callable", function_object);

        return NULL;
    }

    if (unlikely(Py_EnterRecursiveCall((char *)" while calling a Python object"))) {
        return NULL;
    }

    PyObject *result = (*call_slot)(function_object, positional_args, named_args);

    Py_LeaveRecursiveCall();

    return nexium_CheckFunctionResult(tstate, function_object, result);
}

// Function call variant with no arguments provided at all.
extern PyObject *CALL_FUNCTION_NO_ARGS(PyThreadState *tstate, PyObject *called);

// Function call variants with positional arguments tuple.
DEVILPY_MAY_BE_UNUSED static PyObject *CALL_FUNCTION_WITH_POS_ARGS(PyThreadState *tstate, PyObject *function_object,
                                                                  PyObject *positional_args) {
    return CALL_FUNCTION(tstate, function_object, positional_args, NULL);
}

// Method call variants with positional arguments tuple.
extern PyObject *CALL_METHOD_WITH_POS_ARGS(PyThreadState *tstate, PyObject *source, PyObject *attr_name,
                                           PyObject *positional_args);

// TODO: Specialize in template too.
DEVILPY_MAY_BE_UNUSED static PyObject *CALL_FUNCTION_WITH_KW_ARGS(PyThreadState *tstate, PyObject *function_object,
                                                                 PyObject *named_args) {
    return CALL_FUNCTION(tstate, function_object, const_tuple_empty, named_args);
}

// Call built-in functions with using defaulted values.
extern PyObject *CALL_BUILTIN_KW_ARGS(PyThreadState *tstate, PyObject *callable, PyObject **args,
                                      char const **arg_names, int max_args, int kw_only_args);

// For abstract class instantiation error message, during call.
extern void formatCannotInstantiateAbstractClass(PyThreadState *tstate, PyTypeObject *type);

#include "qutayba/helper/calling_generated.h"

#endif


