//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

/**
 * This is responsible for collection of nexium Python PGO information. It writes
 * traces to files, for reuse in a future Python compilation of the same program.
 */

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

static FILE *pgo_output = NULL;

// Saving space by not repeating strings.

// Allocated strings
static char const **PGO_ProbeNameMappings = NULL;
uint32_t PGO_ProbeNameMappings_size = 0;
uint32_t PGO_ProbeNameMappings_used = 0;

uint32_t PGO_getStringID(char const *str) {
    for (uint32_t i = 0; i < PGO_ProbeNameMappings_used; i++) {
        if (str == PGO_ProbeNameMappings[i]) {
            return i;
        }
    }

    if (PGO_ProbeNameMappings_used == PGO_ProbeNameMappings_size) {
        PGO_ProbeNameMappings_size += 10000;
        PGO_ProbeNameMappings = realloc(PGO_ProbeNameMappings, PGO_ProbeNameMappings_size);
    }

    PGO_ProbeNameMappings[PGO_ProbeNameMappings_used] = str;
    PGO_ProbeNameMappings_used += 1;

    return PGO_ProbeNameMappings_used - 1;
}

static void PGO_writeString(char const *value) {
    assert(pgo_output != NULL);

    uint32_t id = PGO_getStringID(value);
    fwrite(&id, sizeof(id), 1, pgo_output);
}

void PGO_Initialize(void) {
    // We expect an environment variable to guide us to where the PGO information
    // shall be written to.
    char const *output_filename = getenv("DEVILPY_PGO_OUTPUT");

    if (unlikely(output_filename == NULL)) {
        DEVILPY_CANNOT_GET_HERE("DEVILPY_PGO_OUTPUT needs to be set");
    }

    pgo_output = fopen(output_filename, "wb");

    if (unlikely(output_filename == NULL)) {
        fprintf(stderr, "Error, failed to open '%s' for writing.", output_filename);
        exit(27);
    }

    fputs("KAY.PGO", pgo_output);
    fflush(pgo_output);

    PGO_ProbeNameMappings_size = 10000;
    PGO_ProbeNameMappings = malloc(PGO_ProbeNameMappings_size * sizeof(char const *));
}

void PGO_Finalize(void) {
    PGO_writeString("END");

    assert(pgo_output != NULL);
    uint32_t offset = (uint32_t)ftell(pgo_output);

    for (uint32_t i = 0; i < PGO_ProbeNameMappings_used; i++) {
        fputs(PGO_ProbeNameMappings[i], pgo_output);
        fputc(0, pgo_output);
    }

    fwrite(&PGO_ProbeNameMappings_used, sizeof(PGO_ProbeNameMappings_used), 1, pgo_output);
    fwrite(&offset, sizeof(offset), 1, pgo_output);

    fputs("YAK.PGO", pgo_output);
    fclose(pgo_output);
}

void PGO_onProbePassed(char const *probe_str, char const *module_name, uint32_t probe_arg) {
    PGO_writeString(probe_str);
    PGO_writeString(module_name);
    // TODO: Variable args depending on probe type?
    fwrite(&probe_arg, sizeof(probe_arg), 1, pgo_output);
}

void PGO_onModuleEntered(char const *module_name) { PGO_onProbePassed("ModuleEnter", module_name, 0); }
void PGO_onModuleExit(char const *module_name, bool error) { PGO_onProbePassed("ModuleExit", module_name, error); }
void PGO_onTechnicalModule(char const *module_name) { PGO_onProbePassed("ModuleTechnical", module_name, 0); }


