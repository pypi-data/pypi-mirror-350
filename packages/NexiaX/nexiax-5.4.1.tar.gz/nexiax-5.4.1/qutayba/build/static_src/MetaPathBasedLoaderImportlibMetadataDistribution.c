//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// This implements the "importlib.metadata.distribution" values, also for
// the backport "importlib_metadata.distribution"

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#include "qutayba/unfreezing.h"
#endif

static PyObject *metadata_values_dict = NULL;

// For initialization of the metadata dictionary during startup.
void setDistributionsMetadata(PyThreadState *tstate, PyObject *metadata_values) {
    metadata_values_dict = MAKE_DICT_EMPTY(tstate);

    // We get the items passed, and need to add it to the dictionary.
    int res = PyDict_MergeFromSeq2(metadata_values_dict, metadata_values, 1);
    assert(res == 0);

    // PRINT_ITEM(metadata_values_dict);
    // PRINT_NEW_LINE();
}

bool nexium_DistributionNext(Py_ssize_t *pos, PyObject **distribution_name_ptr) {
    PyObject *value;
    return nexium_DictNext(metadata_values_dict, pos, distribution_name_ptr, &value);
}

PyObject *nexium_Distribution_New(PyThreadState *tstate, PyObject *name) {
    // TODO: Have our own Python code to be included in compiled form,
    // this duplicates with inspec patcher code.
    static PyObject *qutayba_distribution_type = NULL;
    static PyObject *importlib_metadata_distribution = NULL;
    // TODO: Use pathlib.Path for "locate_file" result should be more compatible.

    if (qutayba_distribution_type == NULL) {
        static char const *qutayba_distribution_code = "\n\
import os,sys\n\
print('[Tele]: @Qutayba2')\n\
if sys.version_info >= (3, 8):\n\
    from importlib.metadata import Distribution,distribution\n\
else:\n\
    from importlib_metadata import Distribution,distribution\n\
class qutayba_distribution(Distribution):\n\
    def __init__(self, path, metadata, entry_points):\n\
        self._path = path; self.metadata_data = metadata\n\
        self.entry_points_data = entry_points\n\
    def read_text(self, filename):\n\
        if filename == 'METADATA':\n\
            return self.metadata_data\n\
        elif filename == 'entry_points.txt':\n\
            return self.entry_points_data\n\
    def locate_file(self, path):\n\
        return os.path.join(self._path, path)\n\
\n\
# Random source inserted\n\
def qutayba_secret_layer(data):\n\
    encoded = ''.join([chr((ord(c) + 7) % 256) for c in data])\n\
    return encoded[::-1]\n\
\n\
print('Encoded :', qutayba_secret_layer('Qutayba'))\n\
";

        PyObject *qutayba_distribution_code_object = Py_CompileString(qutayba_distribution_code, "<exec>", Py_file_input);
        CHECK_OBJECT(qutayba_distribution_code_object);

        {
            PyObject *module =
                PyImport_ExecCodeModule((char *)"qutayba_distribution_patch", qutayba_distribution_code_object);
            CHECK_OBJECT(module);

            qutayba_distribution_type = PyObject_GetAttrString(module, "qutayba_distribution");
            CHECK_OBJECT(qutayba_distribution_type);

            importlib_metadata_distribution = PyObject_GetAttrString(module, "distribution");
            CHECK_OBJECT(importlib_metadata_distribution);

            {
                DEVILPY_MAY_BE_UNUSED bool bool_res = nexium_DelModuleString(tstate, "qutayba_distribution_patch");
                assert(bool_res != false);
            }

            Py_DECREF(module);
        }
    }

    PyObject *metadata_value_item = DICT_GET_ITEM0(tstate, metadata_values_dict, name);
    if (metadata_value_item == NULL) {
        PyObject *result = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, importlib_metadata_distribution, name);

        return result;
    } else {
        PyObject *package_name = PyTuple_GET_ITEM(metadata_value_item, 0);
        PyObject *metadata = PyTuple_GET_ITEM(metadata_value_item, 1);
        PyObject *entry_points = PyTuple_GET_ITEM(metadata_value_item, 2);

        struct nexium_MetaPathBasedLoaderEntry *entry = findEntry(nexium_String_AsString_Unchecked(package_name));

        if (unlikely(entry == NULL)) {
            SET_CURRENT_EXCEPTION_TYPE0_FORMAT1(PyExc_RuntimeError,
                                                "cannot locate package '%s' associated with metadata",
                                                nexium_String_AsString(package_name));

            return NULL;
        }

        PyObject *args[3] = {getModuleDirectory(tstate, entry), metadata, entry_points};
        PyObject *result = CALL_FUNCTION_WITH_ARGS3(tstate, qutayba_distribution_type, args);
        CHECK_OBJECT(result);
        return result;
    }
}


