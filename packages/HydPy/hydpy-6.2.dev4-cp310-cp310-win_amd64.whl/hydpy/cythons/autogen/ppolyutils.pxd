# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This module defines the Cython declarations related to module |ppolytools|."""

cimport numpy


cdef class PPoly:

    # required for usage as an "algorithm" by interputils:

    cdef public numpy.int64_t nmb_inputs
    cdef public numpy.int64_t nmb_outputs
    cdef public double[:] inputs
    cdef public double[:] outputs
    cdef public double[:] output_derivatives

    cpdef inline void calculate_values(self) noexcept nogil
    cpdef inline void calculate_derivatives(self, numpy.int64_t idx_input) noexcept nogil

    # algorithm-specific requirements:

    cdef public numpy.int64_t nmb_ps
    cdef public numpy.int64_t[:] nmb_cs
    cdef public double[:] x0s
    cdef public double[:, :] cs

    cpdef inline numpy.int64_t find_index(self) noexcept nogil
