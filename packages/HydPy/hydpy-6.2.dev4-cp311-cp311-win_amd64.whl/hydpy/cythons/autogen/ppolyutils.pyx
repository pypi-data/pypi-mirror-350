# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This Cython module implements the performance-critical methods of the
Python module |anntools|.
"""

# import...
# ...from standard library
import cython
from hydpy.cythons.autogen cimport smoothutils
# ...from site-packages
import numpy
# ...cimport
cimport cython
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from libc.math cimport NAN as nan
from libc.stdlib cimport malloc, free


@cython.final
cdef class PPoly:

    cpdef inline numpy.int64_t find_index(self) noexcept nogil:
        """Return the index of the polynomial coefficients."""
        cdef numpy.int64_t idx
        cdef double x = self.inputs[0]
        for idx in range(1, self.nmb_ps):
            if x < self.x0s[idx]:
                return idx - 1
        return self.nmb_ps - 1

    cpdef inline void calculate_values(self) noexcept nogil:
        cdef numpy.int64_t i, j
        cdef double x0, x, y
        i = self.find_index()
        x0 = self.x0s[i]
        x = self.inputs[0]
        y = 0.0
        for j in range(self.nmb_cs[i]):
            y += self.cs[i, j] * (x - x0) ** j
        self.outputs[0] = y

    cpdef inline void calculate_derivatives(self, numpy.int64_t idx_input) noexcept nogil:
        cdef numpy.int64_t i, j
        cdef double x0, x, y
        i = self.find_index()
        x0 = self.x0s[i]
        x = self.inputs[0]
        y = 0.0
        for j in range(1, self.nmb_cs[i]):
            y += j * self.cs[i, j] * (x - x0) ** (j - 1)
        self.output_derivatives[0] = y
