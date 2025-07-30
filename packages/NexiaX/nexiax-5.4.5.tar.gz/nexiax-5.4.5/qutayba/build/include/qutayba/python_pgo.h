//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_PYTHON_PGO_H__
#define __DEVILPY_PYTHON_PGO_H__

// In Visual Code, evaluate the code for PGO so we see errors of it sooner.
#ifdef __IDE_ONLY__
#define _DEVILPY_PGO_PYTHON 1
#include "qutayba/prelude.h"
#endif

#if _DEVILPY_PGO_PYTHON

#include <stdint.h>

// Initialize PGO data collection.
extern void PGO_Initialize(void);

// At end of program, write tables.
extern void PGO_Finalize(void);

// When a module is entered.
extern void PGO_onModuleEntered(char const *module_name);
// When a module is exited.
extern void PGO_onModuleExit(char const *module_name, bool had_error);

extern void PGO_onProbePassed(char const *module_name, char const *probe_id, uint32_t probe_arg);

extern void PGO_onTechnicalModule(char const *module_name);

#else

#define PGO_Initialize()
#define PGO_Finalize()

#define PGO_onModuleEntered(module_name) ;
#define PGO_onModuleExit(module_name, had_error) ;

#define PGO_onProbePassed(module_name, probe_id, probe_arg) ;

#endif

#endif

