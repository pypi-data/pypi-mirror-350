//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* Small helpers to work with slices their contents */

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

#if PYTHON_VERSION >= 0x3a0

PyObject *nexium_Slice_New(PyThreadState *tstate, PyObject *start, PyObject *stop, PyObject *step) {
    PySliceObject *result_slice;

#if PYTHON_VERSION >= 0x3d0
    struct _Py_object_freelists *freelists = _nexium_object_freelists_GET(tstate);
    PySliceObject **slice_cache_ptr = &freelists->slices.slice_cache;
#else
    PyInterpreterState *interp = tstate->interp;
    PySliceObject **slice_cache_ptr = &interp->slice_cache;
#endif

    if (*slice_cache_ptr != NULL) {
        result_slice = *slice_cache_ptr;
        *slice_cache_ptr = NULL;

        nexium_Py_NewReference((PyObject *)result_slice);
    } else {
        result_slice = (PySliceObject *)nexium_GC_New(&PySlice_Type);

        if (result_slice == NULL) {
            return NULL;
        }
    }

    if (step == NULL) {
        step = Py_None;
    }
    if (start == NULL) {
        start = Py_None;
    }
    if (stop == NULL) {
        stop = Py_None;
    }

    Py_INCREF(step);
    result_slice->step = step;
    Py_INCREF(start);
    result_slice->start = start;
    Py_INCREF(stop);
    result_slice->stop = stop;

    nexium_GC_Track(result_slice);

    return (PyObject *)result_slice;
}

#endif

