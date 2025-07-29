from libc.stdint cimport uint8_t, uint32_t, uint64_t
from cython.cimports.pyhacl.streaming_types import (
    Hacl_Streaming_Types_error_code,
    Hacl_Streaming_MD_state_32,
)

cdef extern from "Hacl_Hash_SHA1.h":
    ctypedef Hacl_Streaming_MD_state_32 Hacl_Hash_SHA1_state_t
    Hacl_Streaming_MD_state_32 *Hacl_Hash_SHA1_malloc()
    Hacl_Streaming_Types_error_code Hacl_Hash_SHA1_update(Hacl_Streaming_MD_state_32 *state, uint8_t *chunk, uint32_t chunk_len)
    void Hacl_Hash_SHA1_digest(Hacl_Streaming_MD_state_32 *state, uint8_t *output)
    void Hacl_Hash_SHA1_reset(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA1_free(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA1_hash(uint8_t *output, uint8_t *input, uint32_t input_len)
