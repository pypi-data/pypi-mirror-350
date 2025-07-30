//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/* These are defines used in floordiv code.

 */

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

#include <float.h>

/* Check if unary negation would not fit into long */
#define UNARY_NEG_WOULD_OVERFLOW(x) ((x) < 0 && (unsigned long)(x) == 0 - (unsigned long)(x))
/* This is from pyport.h */
#define WIDTH_OF_ULONG (CHAR_BIT * SIZEOF_LONG)


