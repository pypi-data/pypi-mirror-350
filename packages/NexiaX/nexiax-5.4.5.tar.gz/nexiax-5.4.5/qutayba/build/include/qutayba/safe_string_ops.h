//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_SAFE_STRING_OPS_H__
#define __DEVILPY_SAFE_STRING_OPS_H__

#include <errno.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Safe to use function to copy a string, will abort program for overflow. */
extern void copyStringSafe(char *buffer, char const *source, size_t buffer_size);
extern void copyStringSafeN(char *buffer, char const *source, size_t n, size_t buffer_size);
extern void copyStringSafeW(wchar_t *buffer, wchar_t const *source, size_t buffer_size);

/* Safe to use function to append a string, will abort program for overflow. */
extern void appendCharSafe(char *target, char c, size_t buffer_size);
extern void appendStringSafe(char *target, char const *source, size_t buffer_size);

/* Safe to use functions to append a wide char string, will abort program for overflow. */
extern void appendCharSafeW(wchar_t *target, char c, size_t buffer_size);
extern void appendWCharSafeW(wchar_t *target, wchar_t c, size_t buffer_size);
extern void appendStringSafeW(wchar_t *target, char const *source, size_t buffer_size);
extern void appendWStringSafeW(wchar_t *target, wchar_t const *source, size_t buffer_size);

// Check that a string value is actually a number, used to prevent path
// injections with inherited environment variables.
void checkWStringNumber(wchar_t const *value);
void checkStringNumber(char const *value);

/* Get OS error code and print it to stderr. */
#ifdef _WIN32
typedef DWORD error_code_t;
#define ERROR_CODE_FORMAT_STR "%ld"
static inline error_code_t getCurrentErrorCode(void) { return GetLastError(); }
#else
typedef int error_code_t;
#define ERROR_CODE_FORMAT_STR "%d"
static inline error_code_t getCurrentErrorCode(void) { return errno; }
#endif
extern void printOSErrorMessage(char const *message, error_code_t error_code);

#endif

