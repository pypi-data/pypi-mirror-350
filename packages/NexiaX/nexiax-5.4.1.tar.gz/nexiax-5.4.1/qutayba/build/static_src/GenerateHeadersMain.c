//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#include <Python.h>

void main(void) {
#if defined(_MSC_VER) && __STDC_VERSION__ >= 201101L
    fprintf(stderr, "Generating offsets header input file.");
#else
    fprintf(stderr, "Run this program compiled with MSVC in C11 mode only.");
    exit(1);
#endif

    // Allow end of output to be recognized.
    puts("OK.");
    exit(0);
}

