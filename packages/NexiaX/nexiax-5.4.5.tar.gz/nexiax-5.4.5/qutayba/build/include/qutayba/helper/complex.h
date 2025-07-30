//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_COMPLEX_H__
#define __DEVILPY_HELPER_COMPLEX_H__

DEVILPY_MAY_BE_UNUSED static PyObject *BUILTIN_COMPLEX1(PyThreadState *tstate, PyObject *real) {
    CHECK_OBJECT(real);

    // TODO: Very lazy here, we should create the values ourselves, surely a
    // a lot of optimization can be had that way. At least use PyComplex_RealAsDouble
    // where possible.
    return CALL_FUNCTION_WITH_SINGLE_ARG(tstate, (PyObject *)&PyComplex_Type, real);
}

DEVILPY_MAY_BE_UNUSED static PyObject *BUILTIN_COMPLEX2(PyThreadState *tstate, PyObject *real, PyObject *imag) {
    if (real == NULL) {
        assert(imag != NULL);

        real = const_int_0;
    }

    CHECK_OBJECT(real);
    CHECK_OBJECT(imag);

    // TODO: Very lazy here, we should create the values ourselves, surely a
    // a lot of optimization can be had that way. At least use PyComplex_FromDoubles
    PyObject *args[] = {real, imag};
    return CALL_FUNCTION_WITH_ARGS2(tstate, (PyObject *)&PyComplex_Type, args);
}

#endif


