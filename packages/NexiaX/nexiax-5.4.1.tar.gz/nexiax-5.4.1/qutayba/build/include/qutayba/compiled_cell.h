//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_COMPILED_CELL_H__
#define __DEVILPY_COMPILED_CELL_H__

/* This is a clone of the normal PyCell structure. We should keep it binary
 * compatible, just in case somebody crazy insists on it.
 */

extern PyTypeObject nexium_Cell_Type;

static inline bool nexium_Cell_Check(PyObject *object) { return Py_TYPE(object) == &nexium_Cell_Type; }

struct nexium_CellObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* Content of the cell or NULL when empty */
        PyObject *ob_ref;
};

// Create cell with out value, and with or without reference given.
extern struct nexium_CellObject *nexium_Cell_NewEmpty(void);
extern struct nexium_CellObject *nexium_Cell_New0(PyObject *value);
extern struct nexium_CellObject *nexium_Cell_New1(PyObject *value);

// Check stuff while accessing a compile cell in debug mode.
#ifdef __DEVILPY_NO_ASSERT__
#define nexium_Cell_GET(cell) (((struct nexium_CellObject *)(cell))->ob_ref)
#else
#define nexium_Cell_GET(cell)                                                                                          \
    (CHECK_OBJECT(cell), assert(nexium_Cell_Check((PyObject *)cell)), (((struct nexium_CellObject *)(cell))->ob_ref))
#endif

#if _DEBUG_REFCOUNTS
extern int count_active_nexium_Cell_Type;
extern int count_allocated_nexium_Cell_Type;
extern int count_released_nexium_Cell_Type;
#endif

DEVILPY_MAY_BE_UNUSED static inline void nexium_Cell_SET(struct nexium_CellObject *cell_object, PyObject *value) {
    CHECK_OBJECT_X(value);
    CHECK_OBJECT(cell_object);

    assert(nexium_Cell_Check((PyObject *)cell_object));
    cell_object->ob_ref = value;
}

#endif


