//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_STRINGS_H__
#define __DEVILPY_STRINGS_H__

#if PYTHON_VERSION < 0x300
extern PyObject *STR_JOIN(PyThreadState *tstate, PyObject *str, PyObject *iterable);
#endif

extern PyObject *UNICODE_JOIN(PyThreadState *tstate, PyObject *str, PyObject *iterable);
extern PyObject *UNICODE_PARTITION(PyThreadState *tstate, PyObject *str, PyObject *sep);
extern PyObject *UNICODE_RPARTITION(PyThreadState *tstate, PyObject *str, PyObject *sep);

extern PyObject *nexiumUnicode_FromWideChar(wchar_t const *str, Py_ssize_t size);

#endif

