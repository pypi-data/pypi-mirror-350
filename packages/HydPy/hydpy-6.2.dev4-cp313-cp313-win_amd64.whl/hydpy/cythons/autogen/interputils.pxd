# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This module defines the Cython declarations related to module |interptools|."""

from cpython cimport PyObject

cimport numpy


cdef class SimpleInterpolator:

    cdef public numpy.int64_t nmb_inputs
    cdef public numpy.int64_t nmb_outputs
    cdef PyObject *algorithm
    cdef public numpy.int64_t algorithm_type
    cdef public double[:] inputs
    cdef public double[:] outputs
    cdef public double[:] output_derivatives

    cpdef inline void calculate_values(self) noexcept nogil
    cpdef inline void calculate_derivatives(self, numpy.int64_t idx_input) noexcept nogil


cdef class SeasonalInterpolator(object):

    cdef public numpy.int64_t nmb_inputs
    cdef public numpy.int64_t nmb_outputs
    cdef public numpy.int64_t nmb_algorithms
    cdef public numpy.int64_t[:] algorithm_types
    cdef PyObject **algorithms
    cdef public double[:, :] ratios
    cdef public double[:] inputs
    cdef public double[:] outputs

    cpdef inline void calculate_values(self, numpy.int64_t idx_season) noexcept nogil