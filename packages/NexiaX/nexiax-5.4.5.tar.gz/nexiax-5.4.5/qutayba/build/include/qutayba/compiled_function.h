//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_COMPILED_FUNCTION_H__
#define __DEVILPY_COMPILED_FUNCTION_H__

#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

// Compiled function type.

// The backbone of the integration into CPython. Try to behave as well as normal
// functions and built-in functions, or even better.

struct nexium_FunctionObject;

// The actual function code with arguments as an array.
typedef PyObject *(*function_impl_code)(PyThreadState *tstate, struct nexium_FunctionObject const *, PyObject **);

// The nexium_FunctionObject is the storage associated with a compiled function
// instance of which there can be many for each code.
struct nexium_FunctionObject {
    /* Python object folklore: */
    PyObject_VAR_HEAD

        PyObject *m_name;

    PyObject *m_module;
    PyObject *m_doc;

    PyCodeObject *m_code_object;
    Py_ssize_t m_args_overall_count;
    Py_ssize_t m_args_positional_count;
    Py_ssize_t m_args_keywords_count;
    bool m_args_simple;
    Py_ssize_t m_args_star_list_index;
    Py_ssize_t m_args_star_dict_index;

#if PYTHON_VERSION >= 0x380
    Py_ssize_t m_args_pos_only_count;
#endif

    // Same as code_object->co_varnames
    PyObject **m_varnames;

    // C implementation of the function
    function_impl_code m_c_code;

#if PYTHON_VERSION >= 0x380
    vectorcallfunc m_vectorcall;
#endif

    PyObject *m_dict;
    PyObject *m_weakrefs;

    // Tuple of defaults, for use in __defaults__ and parameter parsing.
    PyObject *m_defaults;
    Py_ssize_t m_defaults_given;

#if PYTHON_VERSION >= 0x300
    // List of keyword only defaults, for use in __kwdefaults__ and parameter
    // parsing.
    PyObject *m_kwdefaults;

    // Annotations to the function arguments and return value.
    PyObject *m_annotations;
#endif

#if PYTHON_VERSION >= 0x300
    PyObject *m_qualname;
#endif

#if PYTHON_VERSION >= 0x3c0
    PyObject *m_type_params;
#endif

    // Constant return value to use.
    PyObject *m_constant_return_value;

    // A kind of uuid for the function object, used in comparisons.
    long m_counter;

    // Closure taken objects, for use in __closure__ and for accessing it.
    Py_ssize_t m_closure_given;
    struct nexium_CellObject *m_closure[1];
};

extern PyTypeObject nexium_Function_Type;

// Make a function with context.
#if PYTHON_VERSION < 0x300
extern struct nexium_FunctionObject *nexium_Function_New(function_impl_code c_code, PyObject *name,
                                                         PyCodeObject *code_object, PyObject *defaults,
                                                         PyObject *module, PyObject *doc,
                                                         struct nexium_CellObject **closure, Py_ssize_t closure_given);
#else
extern struct nexium_FunctionObject *nexium_Function_New(function_impl_code c_code, PyObject *name, PyObject *qualname,
                                                         PyCodeObject *code_object, PyObject *defaults,
                                                         PyObject *kw_defaults, PyObject *annotations, PyObject *module,
                                                         PyObject *doc, struct nexium_CellObject **closure,
                                                         Py_ssize_t closure_given);
#endif

extern void nexium_Function_EnableConstReturnTrue(struct nexium_FunctionObject *function);

extern void nexium_Function_EnableConstReturnFalse(struct nexium_FunctionObject *function);

extern void nexium_Function_EnableConstReturnGeneric(struct nexium_FunctionObject *function, PyObject *value);

#ifdef _DEVILPY_PLUGIN_DILL_ENABLED
extern PyObject *nexium_Function_GetFunctionState(struct nexium_FunctionObject *function,
                                                  function_impl_code const *function_table);
extern struct nexium_FunctionObject *nexium_Function_CreateFunctionViaCodeIndex(
    PyObject *module, PyObject *function_qualname, PyObject *function_index, PyObject *code_object_desc,
    PyObject *constant_return_value, PyObject *defaults, PyObject *kw_defaults, PyObject *doc, PyObject *closure,
    PyObject *annotations, PyObject *func_dict, function_impl_code const *function_table, int function_table_size);
extern PyObject *nexium_Function_ExtractCodeObjectDescription(PyThreadState *tstate,
                                                              struct nexium_FunctionObject *function);
#endif

static inline bool nexium_Function_Check(PyObject *object) { return Py_TYPE(object) == &nexium_Function_Type; }

static inline PyObject *nexium_Function_GetName(PyObject *object) {
    return ((struct nexium_FunctionObject *)object)->m_name;
}

PyObject *nexium_CallFunctionNoArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function);

PyObject *nexium_CallFunctionPosArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                     PyObject *const *args, Py_ssize_t args_size);

PyObject *nexium_CallFunctionVectorcall(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                        PyObject *const *args, Py_ssize_t args_size, PyObject *const *kw_names,
                                        Py_ssize_t kw_size);
PyObject *nexium_CallFunctionPosArgsKwArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                           PyObject *const *args, Py_ssize_t args_size, PyObject *kw);
PyObject *nexium_CallFunctionPosArgsKwSplit(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                            PyObject *const *args, Py_ssize_t args_size, PyObject *const *kw_values,
                                            PyObject *kw_names);

PyObject *nexium_CallMethodFunctionNoArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                          PyObject *object);
PyObject *nexium_CallMethodFunctionPosArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                           PyObject *object, PyObject *const *args, Py_ssize_t args_size);
PyObject *nexium_CallMethodFunctionPosArgsKwArgs(PyThreadState *tstate, struct nexium_FunctionObject const *function,
                                                 PyObject *object, PyObject *const *args, Py_ssize_t args_size,
                                                 PyObject *kw);

#if _DEBUG_REFCOUNTS
extern int count_active_nexium_Function_Type;
extern int count_allocated_nexium_Function_Type;
extern int count_released_nexium_Function_Type;
#endif

#endif


