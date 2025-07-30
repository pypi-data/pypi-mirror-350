# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

cimport numpy

cdef class DoubleBase:
    pass


cdef class Double(DoubleBase):

    cdef double value


cdef class PDouble(DoubleBase):

    cdef double *p_value


cdef class PPDouble:

    cdef object ready
    cdef numpy.int64_t length
    cdef double **pp_value
    cdef bint _allocated