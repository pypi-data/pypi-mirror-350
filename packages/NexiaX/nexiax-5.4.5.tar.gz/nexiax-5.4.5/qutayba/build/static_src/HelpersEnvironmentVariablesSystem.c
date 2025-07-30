//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// Helpers for working with environment variables in a portable way. This mainly
// abstracts the string type differences between Win32 and non-Win32 environment
// variables.

#include "qutayba/environment_variables_system.h"
#include "qutayba/safe_string_ops.h"

#if defined(_WIN32)

environment_char_t const *getEnvironmentVariableW(wchar_t const *name) {
    // Max size for environment variables according to docs.
    wchar_t buffer[32768];
    buffer[0] = 0;

    // Size must be in bytes apparently, not in characters. Cannot be larger anyway.
    DWORD res = GetEnvironmentVariableW(name, buffer, 65536);

    if (res == 0 || res > sizeof(buffer)) {
        return NULL;
    }

    return wcsdup(buffer);
}

environment_char_t const *getEnvironmentVariable(char const *name) {
    wchar_t name_wide[40];
    name_wide[0] = 0;
    appendStringSafeW(name_wide, name, sizeof(name_wide) / sizeof(wchar_t));

    return getEnvironmentVariableW(name_wide);
}

void setEnvironmentVariable(char const *name, environment_char_t const *value) {
    assert(name != NULL);
    assert(value != NULL);

    wchar_t name_wide[40];
    name_wide[0] = 0;
    appendStringSafeW(name_wide, name, sizeof(name_wide) / sizeof(wchar_t));

    DWORD res = SetEnvironmentVariableW(name_wide, value);
    assert(wcscmp(getEnvironmentVariable(name), value) == 0);

    assert(res != 0);
}

void unsetEnvironmentVariable(char const *name) {
    wchar_t name_wide[40];
    name_wide[0] = 0;
    appendStringSafeW(name_wide, name, sizeof(name_wide) / sizeof(wchar_t));

    DWORD res = SetEnvironmentVariableW(name_wide, NULL);

    assert(res != 0);
}

#else

environment_char_t const *getEnvironmentVariable(char const *name) { return getenv(name); }

void setEnvironmentVariable(char const *name, environment_char_t const *value) { setenv(name, value, 1); }

void unsetEnvironmentVariable(char const *name) { unsetenv(name); }

#endif

void setEnvironmentVariableFromLong(char const *name, long value) {
    char buffer[128];
    snprintf(buffer, sizeof(buffer), "%ld", value);

#if defined(_WIN32)
    wchar_t buffer2[128];
    buffer2[0] = 0;
    appendStringSafeW(buffer2, buffer, 128);

    setEnvironmentVariable(name, buffer2);
#else
    setEnvironmentVariable(name, buffer);
#endif
}


