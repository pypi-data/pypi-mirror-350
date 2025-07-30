//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* WARNING, this code is GENERATED. Modify the template HelperOperationInplace.c.j2 instead! */

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

/* C helpers for type in-place "@" (MATMULT) operations */

#if PYTHON_VERSION >= 0x350
/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_MATMULT_LONG_LONG(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "OBJECT" corresponds to any Python object and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_MATMULT_OBJECT_LONG(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_MATMULT_LONG_OBJECT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "FLOAT" corresponds to Python 'float' and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_MATMULT_FLOAT_FLOAT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "OBJECT" corresponds to any Python object and "FLOAT" to Python 'float'. */
extern bool INPLACE_OPERATION_MATMULT_OBJECT_FLOAT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "FLOAT" corresponds to Python 'float' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_MATMULT_FLOAT_OBJECT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION >= 0x350
/* Code referring to "OBJECT" corresponds to any Python object and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_MATMULT_OBJECT_OBJECT(PyObject **operand1, PyObject *operand2);
#endif


