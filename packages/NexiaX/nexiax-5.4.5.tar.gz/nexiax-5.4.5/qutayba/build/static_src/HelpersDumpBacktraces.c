//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* These helpers are used to report C backtraces */

#include "backtrace/backtrace.h"

static struct backtrace_state *our_backtrace_state = NULL;

void INIT_C_BACKTRACES(void) {
    our_backtrace_state = backtrace_create_state(NULL, 1, NULL, NULL);
    assert(our_backtrace_state != NULL);
}

static int bt_frame_count = 0;

static int ourBacktraceFullCallback(void *data, uintptr_t pc, const char *filename, int lineno, const char *function) {
    if (strcmp(function, "DUMP_C_BACKTRACE") != 0) {
        fprintf(stderr, "#%d %s:%d %s\n", bt_frame_count, filename, lineno, function);
        bt_frame_count += 1;
    }

    if (strcmp(function, "main") == 0) {
        return 1;
    }

    return 0;
}

void DUMP_C_BACKTRACE(void) {
    assert(our_backtrace_state != NULL);

    bt_frame_count = 0;
    backtrace_full(our_backtrace_state, 0, ourBacktraceFullCallback, NULL, NULL);
}

#include "backtrace/backtrace.c"
#include "backtrace/dwarf.c"
#if !defined(_WIN32)
#include "backtrace/elf.c"
#include "backtrace/mmap.c"
#else
#include "backtrace/alloc.c"
#include "backtrace/pecoff.c"
#endif
#include "backtrace/fileline.c"
#include "backtrace/posix.c"
#include "backtrace/read.c"
#include "backtrace/sort.c"
#include "backtrace/state.c"

