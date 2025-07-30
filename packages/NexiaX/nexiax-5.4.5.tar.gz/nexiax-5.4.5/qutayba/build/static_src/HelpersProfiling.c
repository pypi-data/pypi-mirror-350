//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/**
 * This is responsible for profiling nexium using "vmprof".
 */

#if _DEVILPY_PROFILE

#include <time.h>

struct timespec diff(struct timespec start, struct timespec end);

static struct timespec getTimespecDiff(struct timespec start, struct timespec end) {
    struct timespec temp;

    if ((end.tv_nsec - start.tv_nsec) < 0) {
        temp.tv_sec = end.tv_sec - start.tv_sec - 1;
        temp.tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
    } else {
        temp.tv_sec = end.tv_sec - start.tv_sec;
        temp.tv_nsec = end.tv_nsec - start.tv_nsec;
    }

    return temp;
}

static FILE *tempfile_profile;
static PyObject *vmprof_module;

static struct timespec time1, time2;

void startProfiling(void) {
    tempfile_profile = fopen("qutayba-performance.dat", "w+b");

    // Might be necessary to import "site" module to find "vmprof", lets just
    // hope we don't suffer too much from that. If we do, what might be done
    // is to try and just have the "PYTHONPATH" from it from out user.
    PyImport_ImportModule("site");
    vmprof_module = PyImport_ImportModule("vmprof");

    // Abort if it's not there.
    if (vmprof_module == NULL) {
        PyErr_Print();
        abort();
    }

    PyThreadState *tstate = PyThreadState_GET();

    PyObject *result = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, PyObject_GetAttrString(vmprof_module, "enable"),
                                                     nexium_PyInt_FromLong(fileno(tempfile_profile)));

    if (result == NULL) {
        PyErr_Print();
        abort();
    }

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time1);
}

void stopProfiling(void) {
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time2);

    // Save the current exception, if any, we must preserve it.
    PyThreadState *tstate = PyThreadState_GET();

    struct nexium_ExceptionPreservationItem saved_exception_state;
    FETCH_ERROR_OCCURRED_STATE(tstate, &saved_exception_state);

    PyObject *result = CALL_FUNCTION_NO_ARGS(tstate, PyObject_GetAttrString(vmprof_module, "disable"));

    if (result == NULL) {
        CLEAR_ERROR_OCCURRED(tstate);
    }

    fclose(tempfile_profile);

    FILE *tempfile_times = fopen("qutayba-times.dat", "wb");

    struct timespec diff = getTimespecDiff(time1, time2);

    long delta_ns = diff.tv_sec * 1000000000 + diff.tv_nsec;
    fprintf(tempfile_times, "%ld\n", delta_ns);

    fclose(tempfile_times);

    RESTORE_ERROR_OCCURRED_STATE(tstate, &saved_exception_state);
}

#endif


