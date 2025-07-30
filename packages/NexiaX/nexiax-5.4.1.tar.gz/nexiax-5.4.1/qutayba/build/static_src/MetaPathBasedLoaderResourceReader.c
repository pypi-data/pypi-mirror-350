//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// This implements the resource reader for of C compiled modules and
// shared library extension modules bundled for standalone mode with
// newer Python.

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#include "qutayba/unfreezing.h"
#endif

// Just for the IDE to know, this file is not included otherwise.
#if PYTHON_VERSION >= 0x370

struct nexium_ResourceReaderObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* The loader entry, to know this is about exactly. */
        struct nexium_MetaPathBasedLoaderEntry const *m_loader_entry;
};

static void nexium_ResourceReader_tp_dealloc(struct nexium_ResourceReaderObject *reader) {
    nexium_GC_UnTrack(reader);

    PyObject_GC_Del(reader);
}

static PyObject *nexium_ResourceReader_tp_repr(struct nexium_ResourceReaderObject *reader) {
    return PyUnicode_FromFormat("<qutayba_resource_reader for '%s'>", reader->m_loader_entry->name);
}

// Obligatory, even if we have nothing to own
static int nexium_ResourceReader_tp_traverse(struct nexium_ResourceReaderObject *reader, visitproc visit, void *arg) {
    return 0;
}

static PyObject *_nexium_ResourceReader_resource_path(PyThreadState *tstate, struct nexium_ResourceReaderObject *reader,
                                                      PyObject *resource) {
    PyObject *dir_name = getModuleDirectory(tstate, reader->m_loader_entry);

    if (unlikely(dir_name == NULL)) {
        return NULL;
    }

    PyObject *result = JOIN_PATH2(dir_name, resource);
    Py_DECREF(dir_name);

    return result;
}

static PyObject *nexium_ResourceReader_resource_path(struct nexium_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:resource_path", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    return _nexium_ResourceReader_resource_path(tstate, reader, resource);
}

static PyObject *nexium_ResourceReader_open_resource(struct nexium_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:open_resource", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    PyObject *filename = _nexium_ResourceReader_resource_path(tstate, reader, resource);

    return BUILTIN_OPEN_BINARY_READ_SIMPLE(tstate, filename);
}

#include "MetaPathBasedLoaderResourceReaderFiles.c"

static PyObject *nexium_ResourceReader_files(struct nexium_ResourceReaderObject *reader, PyObject *args,
                                             PyObject *kwds) {

    PyThreadState *tstate = PyThreadState_GET();
    return nexium_ResourceReaderFiles_New(tstate, reader->m_loader_entry, const_str_empty);
}

static PyMethodDef nexium_ResourceReader_methods[] = {
    {"resource_path", (PyCFunction)nexium_ResourceReader_resource_path, METH_VARARGS | METH_KEYWORDS, NULL},
    {"open_resource", (PyCFunction)nexium_ResourceReader_open_resource, METH_VARARGS | METH_KEYWORDS, NULL},
    {"files", (PyCFunction)nexium_ResourceReader_files, METH_NOARGS, NULL},
    {NULL}};

static PyTypeObject nexium_ResourceReader_Type = {
    PyVarObject_HEAD_INIT(NULL, 0) "qutayba_resource_reader",
    sizeof(struct nexium_ResourceReaderObject),      // tp_basicsize
    0,                                               // tp_itemsize
    (destructor)nexium_ResourceReader_tp_dealloc,    // tp_dealloc
    0,                                               // tp_print
    0,                                               // tp_getattr
    0,                                               // tp_setattr
    0,                                               // tp_reserved
    (reprfunc)nexium_ResourceReader_tp_repr,         // tp_repr
    0,                                               // tp_as_number
    0,                                               // tp_as_sequence
    0,                                               // tp_as_mapping
    0,                                               // tp_hash
    0,                                               // tp_call
    0,                                               // tp_str
    0,                                               // tp_getattro (PyObject_GenericGetAttr)
    0,                                               // tp_setattro
    0,                                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,         // tp_flags
    0,                                               // tp_doc
    (traverseproc)nexium_ResourceReader_tp_traverse, // tp_traverse
    0,                                               // tp_clear
    0,                                               // tp_richcompare
    0,                                               // tp_weaklistoffset
    0,                                               // tp_iter
    0,                                               // tp_iternext
    nexium_ResourceReader_methods,                   // tp_methods
    0,                                               // tp_members
    0,                                               // tp_getset
};

static PyObject *nexium_ResourceReader_New(struct nexium_MetaPathBasedLoaderEntry const *entry) {
    struct nexium_ResourceReaderObject *result;

    result = (struct nexium_ResourceReaderObject *)nexium_GC_New(&nexium_ResourceReader_Type);
    nexium_GC_Track(result);

    result->m_loader_entry = entry;

    return (PyObject *)result;
}

#endif

