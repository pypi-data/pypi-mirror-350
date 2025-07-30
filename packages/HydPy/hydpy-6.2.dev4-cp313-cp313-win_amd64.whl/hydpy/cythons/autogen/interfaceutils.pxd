# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This module implements only the interface base class required to support casting to
specific subclasses in Cython."""

from cpython cimport PyObject
cimport numpy


cdef class BaseInterface:

    cdef public numpy.int64_t typeid
    cdef public numpy.int64_t idx_sim

    cdef void reset_reuseflags(self) noexcept nogil
    cdef void load_data(self, numpy.int64_t idx) noexcept nogil
    cdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cdef void update_inlets(self) noexcept nogil
    cdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cdef void update_outlets(self) noexcept nogil
    cdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cdef void update_outputs(self) noexcept nogil


cdef class SubmodelsProperty:

    cdef numpy.int64_t number
    cdef numpy.int64_t[:] typeids
    cdef PyObject **submodels
