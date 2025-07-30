//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

// Comment in to disable outside zlib usage for code size, very slow though,
// since it doesn't use assembly to use CPU crc32 instructions.
// #define _DEVILPY_USE_OWN_CRC32

#ifdef _DEVILPY_USE_OWN_CRC32
uint32_t _initCRC32(void) { return 0xFFFFFFFF; }

uint32_t _updateCRC32(uint32_t crc, unsigned char const *message, uint32_t size) {
    for (uint32_t i = 0; i < size; i++) {
        unsigned int c = message[i];
        crc = crc ^ c;

        for (int j = 7; j >= 0; j--) {
            uint32_t mask = ((crc & 1) != 0) ? 0xFFFFFFFF : 0;
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
    }

    return crc;
}

uint32_t _finalizeCRC32(uint32_t crc) { return ~crc; }

// No Python runtime is available yet, need to do this in C.
uint32_t calcCRC32(unsigned char const *message, uint32_t size) {
    return _finalizeCRC32(_updateCRC32(_initCRC32(), message, size));
}
#else

#ifdef _DEVILPY_USE_SYSTEM_CRC32
#include "zlib.h"
#else
#include "crc32.c"
#endif

uint32_t calcCRC32(unsigned char const *message, uint32_t size) { return crc32(0, message, size) & 0xFFFFFFFF; }
#endif

