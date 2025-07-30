//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* WARNING, this code is GENERATED. Modify the template HelperOperationInplace.c.j2 instead! */

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

/* C helpers for type in-place "&" (BITAND) operations */

/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_BITAND_LONG_LONG(PyObject **operand1, PyObject *operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_BITAND_OBJECT_LONG(PyObject **operand1, PyObject *operand2);

/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_BITAND_LONG_OBJECT(PyObject **operand1, PyObject *operand2);

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_BITAND_INT_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "OBJECT" corresponds to any Python object and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_BITAND_OBJECT_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_BITAND_INT_OBJECT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "CLONG" to C platform long value. */
extern bool INPLACE_OPERATION_BITAND_INT_CLONG(PyObject **operand1, long operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "LONG" corresponds to Python2 'long', Python3 'int' and "INT" to Python2 'int'. */
extern bool INPLACE_OPERATION_BITAND_LONG_INT(PyObject **operand1, PyObject *operand2);
#endif

#if PYTHON_VERSION < 0x300
/* Code referring to "INT" corresponds to Python2 'int' and "LONG" to Python2 'long', Python3 'int'. */
extern bool INPLACE_OPERATION_BITAND_INT_LONG(PyObject **operand1, PyObject *operand2);
#endif

/* Code referring to "SET" corresponds to Python 'set' and "SET" to Python 'set'. */
extern bool INPLACE_OPERATION_BITAND_SET_SET(PyObject **operand1, PyObject *operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "SET" to Python 'set'. */
extern bool INPLACE_OPERATION_BITAND_OBJECT_SET(PyObject **operand1, PyObject *operand2);

/* Code referring to "SET" corresponds to Python 'set' and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_BITAND_SET_OBJECT(PyObject **operand1, PyObject *operand2);

/* Code referring to "OBJECT" corresponds to any Python object and "OBJECT" to any Python object. */
extern bool INPLACE_OPERATION_BITAND_OBJECT_OBJECT(PyObject **operand1, PyObject *operand2);


