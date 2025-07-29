from libc.stdint cimport uint8_t, uint32_t, uint64_t

cdef extern from "Hacl_Streaming_Types.h":
    ctypedef uint8_t Hacl_Streaming_Types_error_code;

    cdef struct Hacl_Streaming_MD_state_32_s:
        uint32_t *block_state
        uint8_t *buf
        uint64_t total_len
    ctypedef Hacl_Streaming_MD_state_32_s Hacl_Streaming_MD_state_32;

    cdef struct Hacl_Streaming_MD_state_64_s:
        uint64_t *block_state;
        uint8_t *buf;
        uint64_t total_len;
    ctypedef Hacl_Streaming_MD_state_64_s Hacl_Streaming_MD_state_64;
