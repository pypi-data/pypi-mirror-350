//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_CONSTANTS_BLOB_H__
#define __DEVILPY_CONSTANTS_BLOB_H__

/** Declaration of the constants binary blob.
 *
 * There are multiple ways, the constants binary is accessed, and its
 * definition depends on how that is done.
 *
 * It could be a Windows resource, then it must be a pointer. If it's defined
 * externally in a C file, or at link time with "ld", it must be an array. This
 * hides these facts.
 *
 */

extern void loadConstantsBlob(PyThreadState *tstate, PyObject **, char const *name);

#endif


