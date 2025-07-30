# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This Cython module implements the performance-critical features of the
Python module |roottools|."""

cimport numpy

cdef class PegasusBase:

    cdef double apply_method0(self, double x) noexcept nogil

    cdef double find_x(
        self,
        double x0,
        double x1,
        double xmin,
        double xmax,
        double xtol,
        double ytol,
        numpy.int64_t itermax,
    ) noexcept nogil
