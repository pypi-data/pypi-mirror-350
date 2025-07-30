//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_TRACING_H__
#define __DEVILPY_TRACING_H__

/* Stupid tracing, intended to help where debugging is not an option
 * and to give kind of progress record of startup and the running of
 * the program.
 */

#ifdef _DEVILPY_TRACE

#define DEVILPY_PRINT_TRACE(value)                                                                                      \
    {                                                                                                                  \
        puts(value);                                                                                                   \
        fflush(stdout);                                                                                                \
    }
#define DEVILPY_PRINTF_TRACE(...)                                                                                       \
    {                                                                                                                  \
        printf(__VA_ARGS__);                                                                                           \
        fflush(stdout);                                                                                                \
    }

#else
#define DEVILPY_PRINT_TRACE(value)
#define DEVILPY_PRINTF_TRACE(...)

#endif

#if defined(_DEVILPY_EXPERIMENTAL_SHOW_STARTUP_TIME)

#if defined(_WIN32)

#include <windows.h>
static void inline PRINT_TIME_STAMP(void) {
    SYSTEMTIME t;
    GetSystemTime(&t); // or GetLocalTime(&t)
    printf("%02d:%02d:%02d.%03d:", t.wHour, t.wMinute, t.wSecond, t.wMilliseconds);
}
#else
static void inline PRINT_TIME_STAMP(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);

    time_t now_time = tv.tv_sec;
    struct tm *now_tm = localtime(&now_time);

    char tm_buf[64];
    strftime(tm_buf, sizeof(tm_buf), "%Y-%m-%d %H:%M:%S", now_tm);
    printf("%s.%03ld ", tm_buf, tv.tv_usec / 1000);
}
#endif

#define DEVILPY_PRINT_TIMING(value)                                                                                     \
    {                                                                                                                  \
        PRINT_TIME_STAMP();                                                                                            \
        puts(value);                                                                                                   \
        fflush(stdout);                                                                                                \
    }

#else

#define DEVILPY_PRINT_TIMING(value) DEVILPY_PRINT_TRACE(value)

#endif

#endif


