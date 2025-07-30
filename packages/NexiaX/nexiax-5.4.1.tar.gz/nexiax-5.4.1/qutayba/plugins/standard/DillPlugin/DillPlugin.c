//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// C code for use when the dill-plugin is active

#include "qutayba/prelude.h"

void registerDillPluginTables(PyThreadState *tstate, char const *module_name, PyMethodDef *reduce_compiled_function,
                              PyMethodDef *create_compiled_function) {
    PyObject *function_tables = PyObject_GetAttrString((PyObject *)builtin_module, "compiled_function_tables");

    if (function_tables == NULL) {
        CLEAR_ERROR_OCCURRED(tstate);

        function_tables = MAKE_DICT_EMPTY(tstate);
        PyObject_SetAttrString((PyObject *)builtin_module, "compiled_function_tables", function_tables);
    }

    PyObject *funcs = MAKE_TUPLE2_0(tstate, PyCFunction_New(reduce_compiled_function, NULL),
                                    PyCFunction_New(create_compiled_function, NULL));

    PyDict_SetItemString(function_tables, module_name, funcs);
}


