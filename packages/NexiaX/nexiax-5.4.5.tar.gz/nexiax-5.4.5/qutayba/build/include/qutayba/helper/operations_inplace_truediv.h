//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* WARNING, this code is GENERATED. Modify the template HelperOperationInplace.c.j2 instead! */

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

/* C helpers for type in-place "/" (TRUEDIV) operations */

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_INT_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "OBJECT" corresponds to any Python object and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_OBJECT_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_TRUEDIV_INT_OBJECT(PyObject **operand1, PyObject *operand2);
#endif

/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_LONG_LONG(PyObject **operand1, PyObject *operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_OBJECT_LONG(PyObject **operand1, PyObject *operand2);

/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_TRUEDIV_LONG_OBJECT(PyObject **operand1, PyObject *operand2);

/* Code referring to "FLOAT" corresponds to Python 'float' and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_TRUEDIV_FLOAT_FLOAT(PyObject **operand1, PyObject *operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_TRUEDIV_OBJECT_FLOAT(PyObject **operand1, PyObject *operand2);

/* Code referring to "FLOAT" corresponds to Python 'float' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_TRUEDIV_FLOAT_OBJECT(PyObject **operand1, PyObject *operand2);

/* Code referring to "FLOAT" corresponds to Python 'float' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_FLOAT_LONG(PyObject **operand1, PyObject *operand2);

/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_TRUEDIV_LONG_FLOAT(PyObject **operand1, PyObject *operand2);

#if PYTHON_VERSION < 0x300
/* Code referring to "FLOAT" corresponds to Python 'float' and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_FLOAT_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_TRUEDIV_INT_FLOAT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_LONG_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_TRUEDIV_INT_LONG(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "CLONG" to C platform long value. */
extern bool INPLACE_OPERATION_TRUEDIV_INT_CLONG(PyObject **operand1, long operand2);
#endif

/* Code referring to "FLOAT" corresponds to Python 'float' and "CFLOAT" to C platform float value. */
extern bool INPLACE_OPERATION_TRUEDIV_FLOAT_CFLOAT(PyObject **operand1, double operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_TRUEDIV_OBJECT_OBJECT(PyObject **operand1, PyObject *operand2);


