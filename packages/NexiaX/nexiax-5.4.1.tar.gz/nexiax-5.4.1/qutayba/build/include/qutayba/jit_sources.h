//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_JIT_SOURCES_H__
#define __DEVILPY_JIT_SOURCES_H__

// Helpers for making source available at run-time for JIT systems
// outside of nexium that want it.

extern void SET_UNCOMPILED_FUNCTION_SOURCE_DICT(PyObject *name, PyObject *source);

#endif

