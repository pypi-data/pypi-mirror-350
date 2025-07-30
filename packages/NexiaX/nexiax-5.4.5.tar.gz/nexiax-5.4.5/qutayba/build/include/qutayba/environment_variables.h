//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_ENVIRONMENT_VARIABLES_H__
#define __DEVILPY_ENVIRONMENT_VARIABLES_H__

#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

#include "qutayba/environment_variables_system.h"

extern void undoEnvironmentVariable(PyThreadState *tstate, char const *variable_name,
                                    environment_char_t const *old_value);

#endif


