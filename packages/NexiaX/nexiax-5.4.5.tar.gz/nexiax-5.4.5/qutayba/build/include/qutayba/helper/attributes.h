//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_ATTRIBUTES_H__
#define __DEVILPY_HELPER_ATTRIBUTES_H__

// Attribute lookup except special slots below.
extern PyObject *LOOKUP_ATTRIBUTE(PyThreadState *tstate, PyObject *source, PyObject *attr_name);

// Attribute lookup of attribute slot "__dict__".
extern PyObject *LOOKUP_ATTRIBUTE_DICT_SLOT(PyThreadState *tstate, PyObject *source);

// Attribute lookup of attribute slot "__class__".
extern PyObject *LOOKUP_ATTRIBUTE_CLASS_SLOT(PyThreadState *tstate, PyObject *source);

// For built-in "hasattr" functionality.
extern int BUILTIN_HASATTR_BOOL(PyThreadState *tstate, PyObject *source, PyObject *attr_name);

// Check for an attribute, cannot raise an exception.
extern bool HAS_ATTR_BOOL(PyThreadState *tstate, PyObject *source, PyObject *attr_name);

// Check for an attribute, can raise an exception.
extern int HAS_ATTR_BOOL2(PyThreadState *tstate, PyObject *source, PyObject *attr_name);

// Set an attribute except for attribute slots below.
extern bool SET_ATTRIBUTE(PyThreadState *tstate, PyObject *target, PyObject *attr_name, PyObject *value);

// Set the "__dict__" special attribute slot.
extern bool SET_ATTRIBUTE_DICT_SLOT(PyThreadState *tstate, PyObject *target, PyObject *value);

// Set the "__class__" special attribute slot.
extern bool SET_ATTRIBUTE_CLASS_SLOT(PyThreadState *tstate, PyObject *target, PyObject *value);

// Special attribute lookups, e.g. "__enter__".
extern PyObject *LOOKUP_SPECIAL(PyThreadState *tstate, PyObject *source, PyObject *attr_name);

// Find an attribute in a class, Python2 only.
#if PYTHON_VERSION < 0x300
extern PyObject *FIND_ATTRIBUTE_IN_CLASS(PyClassObject *class_object, PyObject *attr_name);
#endif

extern PyObject *LOOKUP_MODULE_VALUE(PyDictObject *module_dict, PyObject *var_name);

// In case of DLL usage, this avoids looking up the symbol from it.
extern getattrofunc PyObject_GenericGetAttr_resolved;

// Avoid repeated code, this checks if a type has the standard implementation, then
// we can just try and do the same in slightly faster ways.
static inline bool hasTypeGenericGetAttr(PyTypeObject *type) {
#if PYTHON_VERSION >= 0x3b0
    // TODO: Big performance loss here
    return false;
#else
    return type->tp_getattro == PyObject_GenericGetAttr_resolved;
#endif
}

// In case of DLL usage, this avoids looking up the symbol from it.
extern setattrofunc PyObject_GenericSetAttr_resolved;

static inline bool hasTypeGenericSetAttr(PyTypeObject *type) {
#if PYTHON_VERSION >= 0x3b0
    // TODO: Big performance loss here
    return false;
#else
    return type->tp_setattro == PyObject_GenericSetAttr_resolved;
#endif
}

#if PYTHON_VERSION >= 0x3a0
static inline bool nexium_Descr_IsData(PyObject *object) { return Py_TYPE(object)->tp_descr_set != NULL; }
#else
#define nexium_Descr_IsData(object) PyDescr_IsData(object)
#endif

#endif


