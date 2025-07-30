//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_RANGEOBJECTS_H__
#define __DEVILPY_HELPER_RANGEOBJECTS_H__

/* For built-in built-in range() functionality. */

extern PyObject *BUILTIN_RANGE3(PyThreadState *tstate, PyObject *low, PyObject *high, PyObject *step);
extern PyObject *BUILTIN_RANGE2(PyThreadState *tstate, PyObject *low, PyObject *high);
extern PyObject *BUILTIN_RANGE(PyThreadState *tstate, PyObject *boundary);

/* For built-in built-in xrange() functionality. */
extern PyObject *BUILTIN_XRANGE1(PyThreadState *tstate, PyObject *high);
extern PyObject *BUILTIN_XRANGE2(PyThreadState *tstate, PyObject *low, PyObject *high);
extern PyObject *BUILTIN_XRANGE3(PyThreadState *tstate, PyObject *low, PyObject *high, PyObject *step);

#if PYTHON_VERSION >= 0x300

/* Python3 range objects */
struct _rangeobject3 {
    /* Python object folklore: */
    PyObject_HEAD

        PyObject *start;
    PyObject *stop;
    PyObject *step;
    PyObject *length;
};

DEVILPY_MAY_BE_UNUSED static PyObject *PyRange_Start(PyObject *range) { return ((struct _rangeobject3 *)range)->start; }

DEVILPY_MAY_BE_UNUSED static PyObject *PyRange_Stop(PyObject *range) { return ((struct _rangeobject3 *)range)->stop; }

DEVILPY_MAY_BE_UNUSED static PyObject *PyRange_Step(PyObject *range) { return ((struct _rangeobject3 *)range)->step; }

#else

struct _rangeobject2 {
    /* Python object folklore: */
    PyObject_HEAD

        long start;
    long step;
    long len;
};

extern PyObject *MAKE_XRANGE(PyThreadState *tstate, long start, long stop, long step);

#endif

#endif


