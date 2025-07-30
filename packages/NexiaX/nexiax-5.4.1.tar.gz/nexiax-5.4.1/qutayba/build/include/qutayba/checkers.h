//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_CHECKERS_H__
#define __DEVILPY_CHECKERS_H__

// Helper to check that an object is valid and has positive reference count.
#define CHECK_OBJECT(value) (assert((value) != NULL), assert(Py_REFCNT(value) > 0))
#define CHECK_OBJECT_X(value) (assert((value) == NULL || Py_REFCNT(value) > 0))

// Helper to check an array of objects with CHECK_OBJECT
#ifndef __DEVILPY_NO_ASSERT__
#define CHECK_OBJECTS(values, count)                                                                                   \
    {                                                                                                                  \
        for (int i = 0; i < count; i++) {                                                                              \
            CHECK_OBJECT((values)[i]);                                                                                 \
        }                                                                                                              \
    }
#else
#define CHECK_OBJECTS(values, count)
#endif

extern void CHECK_OBJECT_DEEP(PyObject *value);
extern void CHECK_OBJECTS_DEEP(PyObject *const *values, Py_ssize_t size);

#endif

