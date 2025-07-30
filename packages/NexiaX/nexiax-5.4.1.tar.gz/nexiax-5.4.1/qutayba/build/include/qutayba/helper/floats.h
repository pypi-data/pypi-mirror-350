//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_FLOATS_H__
#define __DEVILPY_HELPER_FLOATS_H__

#if PYTHON_VERSION >= 0x3a0
#define DEVILPY_FLOAT_HAS_FREELIST 1

// Replacement for PyFloat_FromDouble that is faster
extern PyObject *MAKE_FLOAT_FROM_DOUBLE(double value);
#else
#define DEVILPY_FLOAT_HAS_FREELIST 0
#define MAKE_FLOAT_FROM_DOUBLE(value) PyFloat_FromDouble(value)
#endif

extern PyObject *TO_FLOAT(PyObject *value);

#endif

