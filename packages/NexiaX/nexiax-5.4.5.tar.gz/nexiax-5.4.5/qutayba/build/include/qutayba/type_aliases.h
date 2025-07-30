//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_TYPE_ALIASES_H__
#define __DEVILPY_TYPE_ALIASES_H__

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

// Helpers for type aliases, type variables, and generic base classes.
extern PyObject *MAKE_TYPE_ALIAS(PyObject *name, PyObject *type_params, PyObject *value, PyObject *module_name);
extern PyObject *MAKE_TYPE_VAR(PyThreadState *tstate, PyObject *name);
extern PyObject *MAKE_TYPE_GENERIC(PyThreadState *tstate, PyObject *params);

#endif

