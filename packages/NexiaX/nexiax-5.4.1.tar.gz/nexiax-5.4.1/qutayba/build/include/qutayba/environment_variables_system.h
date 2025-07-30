//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_ENVIRONMENT_VARIABLES_SYSTEM_H__
#define __DEVILPY_ENVIRONMENT_VARIABLES_SYSTEM_H__

#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

#include "qutayba/filesystem_paths.h"

// Helpers for working with environment variables in a portable way. This mainly
// abstracts the string type differences between Win32 and non-Win32 environment
// variables.
#if defined(_WIN32)
#define environment_char_t wchar_t
#define native_command_line_argument_t wchar_t
#define compareEnvironmentString(a, b) wcscmp(a, b)
#define makeEnvironmentLiteral(x) L##x
#else
#define environment_char_t char
#define native_command_line_argument_t char
#define compareEnvironmentString(a, b) strcmp(a, b)
#define makeEnvironmentLiteral(x) x
#endif

extern environment_char_t const *getEnvironmentVariable(char const *name);
extern environment_char_t const *getEnvironmentVariableW(wchar_t const *name);
extern void setEnvironmentVariable(char const *name, environment_char_t const *value);
extern void setEnvironmentVariableFromLong(char const *name, long value);
extern void setEnvironmentVariableFromFilename(char const *name, filename_char_t const *value);
extern void unsetEnvironmentVariable(char const *name);

// Get the original argv0 value.
extern filename_char_t const *getOriginalArgv0(void);

#endif

