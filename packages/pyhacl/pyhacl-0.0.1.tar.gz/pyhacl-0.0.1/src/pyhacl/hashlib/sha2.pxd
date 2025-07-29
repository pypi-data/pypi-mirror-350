from libc.stdint cimport uint8_t, uint32_t, uint64_t
from cython.cimports.pyhacl.streaming_types import (
    Hacl_Streaming_Types_error_code,
    Hacl_Streaming_MD_state_32,
    Hacl_Streaming_MD_state_64,
)

cdef extern from "Hacl_Hash_SHA2.h":
    ctypedef Hacl_Streaming_MD_state_32 Hacl_Hash_SHA2_state_t_224
    Hacl_Streaming_MD_state_32 *Hacl_Hash_SHA2_malloc_224()
    Hacl_Streaming_Types_error_code Hacl_Hash_SHA2_update_224(Hacl_Streaming_MD_state_32 *state, uint8_t *input, uint32_t input_len)
    void Hacl_Hash_SHA2_digest_224(Hacl_Streaming_MD_state_32 *state, uint8_t *output)
    void Hacl_Hash_SHA2_reset_224(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA2_free_224(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA2_hash_224(uint8_t *output, uint8_t *input, uint32_t input_len)

    ctypedef Hacl_Streaming_MD_state_32 Hacl_Hash_SHA2_state_t_256
    Hacl_Streaming_MD_state_32 *Hacl_Hash_SHA2_malloc_256()
    Hacl_Streaming_Types_error_code Hacl_Hash_SHA2_update_256(Hacl_Streaming_MD_state_32 *state, uint8_t *input, uint32_t input_len)
    void Hacl_Hash_SHA2_digest_256(Hacl_Streaming_MD_state_32 *state, uint8_t *output)
    void Hacl_Hash_SHA2_reset_256(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA2_free_256(Hacl_Streaming_MD_state_32 *state)
    void Hacl_Hash_SHA2_hash_256(uint8_t *output, uint8_t *input, uint32_t input_len)

    ctypedef Hacl_Streaming_MD_state_64 Hacl_Hash_SHA2_state_t_384
    Hacl_Streaming_MD_state_64 *Hacl_Hash_SHA2_malloc_384()
    Hacl_Streaming_Types_error_code Hacl_Hash_SHA2_update_384(Hacl_Streaming_MD_state_64 *state, uint8_t *input, uint32_t input_len)
    void Hacl_Hash_SHA2_digest_384(Hacl_Streaming_MD_state_64 *state, uint8_t *output)
    void Hacl_Hash_SHA2_reset_384(Hacl_Streaming_MD_state_64 *state)
    void Hacl_Hash_SHA2_free_384(Hacl_Streaming_MD_state_64 *state)
    void Hacl_Hash_SHA2_hash_384(uint8_t *output, uint8_t *input, uint32_t input_len)

    ctypedef Hacl_Streaming_MD_state_64 Hacl_Hash_SHA2_state_t_512
    Hacl_Streaming_MD_state_64 *Hacl_Hash_SHA2_malloc_512()
    Hacl_Streaming_Types_error_code Hacl_Hash_SHA2_update_512(Hacl_Streaming_MD_state_64 *state, uint8_t *input, uint32_t input_len)
    void Hacl_Hash_SHA2_digest_512(Hacl_Streaming_MD_state_64 *state, uint8_t *output)
    void Hacl_Hash_SHA2_reset_512(Hacl_Streaming_MD_state_64 *state)
    void Hacl_Hash_SHA2_free_512(Hacl_Streaming_MD_state_64 *state)
    void Hacl_Hash_SHA2_hash_512(uint8_t *output, uint8_t *input, uint32_t input_len)
