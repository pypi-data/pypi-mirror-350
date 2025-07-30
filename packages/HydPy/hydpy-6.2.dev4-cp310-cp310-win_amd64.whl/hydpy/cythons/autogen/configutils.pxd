# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This module defines the Cython declarations related to module
|configutils|.
"""

cdef class Config(object):

    cdef public double _abs_error_max
    cdef public double _rel_dt_min
