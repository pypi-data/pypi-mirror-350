//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// Helpers for working with environment variables from Python binary in a
// portable way.

#include "qutayba/environment_variables.h"

#include "HelpersEnvironmentVariablesSystem.c"

void undoEnvironmentVariable(PyThreadState *tstate, char const *variable_name, environment_char_t const *old_value) {
    PyObject *os_module = IMPORT_HARD_OS();
    CHECK_OBJECT(os_module);

    PyObject *os_environ = PyObject_GetAttrString(os_module, "environ");
    CHECK_OBJECT(os_environ);

    PyObject *variable_name_str = nexium_String_FromString(variable_name);
    CHECK_OBJECT(variable_name_str);

    if (old_value) {
        setEnvironmentVariable(variable_name, old_value);

#ifdef _WIN32
        PyObject *env_value = nexiumUnicode_FromWideChar(old_value, -1);
#else
        PyObject *env_value = nexium_String_FromString(old_value);
#endif
        CHECK_OBJECT(env_value);

        int res = PyObject_SetItem(os_environ, variable_name_str, env_value);

        if (unlikely(res != 0)) {
            PyErr_PrintEx(1);
            Py_Exit(1);
        }

        Py_DECREF(env_value);
    } else {
        unsetEnvironmentVariable(variable_name);

        int res = PyObject_DelItem(os_environ, variable_name_str);

        if (unlikely(res != 0)) {
            CLEAR_ERROR_OCCURRED(tstate);
        }
    }

    Py_DECREF(variable_name_str);
    Py_DECREF(os_environ);
}


