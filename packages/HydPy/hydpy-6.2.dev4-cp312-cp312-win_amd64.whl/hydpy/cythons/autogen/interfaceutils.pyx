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

import numpy

from cpython cimport Py_DECREF
from libc.stdlib cimport free, malloc, realloc
cimport cython

from hydpy import config


cdef class BaseInterface:

    cdef void reset_reuseflags(self) noexcept nogil:
        pass

    cdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        pass

    cdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        pass

    cdef void update_inlets(self) noexcept nogil:
        pass

    cdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        pass

    cdef void update_outlets(self) noexcept nogil:
        pass

    cdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        pass

    cdef void update_outputs(self) noexcept nogil:
        pass


cdef class SubmodelsProperty:

    def __init__(self) -> None:
        self.set_number(0)

    def _get_number(self) -> int:
        return self.number

    def set_number(self, numpy.int64_t number) -> None:
        assert number >= 0
        free(self.submodels)
        self.number = number
        self.typeids = numpy.zeros(number, dtype=config.NP_INT)
        self.submodels = <PyObject **>malloc(
            number * cython.sizeof(cython.pointer(PyObject))
        )
        for i in range(number):
            self.submodels[i] = <PyObject*>None

    def _get_typeid(self, numpy.int64_t position) -> int:
        assert 0 <= position < self.number
        return self.typeids[position]

    def _get_submodel(self, numpy.int64_t position):
        assert 0 <= position < self.number
        submodel = <object>self.submodels[position]
        Py_DECREF(submodel)
        return submodel

    def put_submodel(self, submodel, numpy.int64_t typeid, numpy.int64_t position) -> None:
        assert 0 <= position < self.number
        self.typeids[position] = typeid
        self.submodels[position] = <PyObject*>submodel

    def append_submodel(self, submodel, numpy.int64_t typeid) -> None:
        self.number += 1
        if self.number > 1:
            typeids = numpy.asarray(self.typeids).copy()
        self.typeids = numpy.zeros(self.number, dtype=config.NP_INT)
        for i in range(self.number - 1):
            self.typeids[i] = typeids[i]
        self.typeids[self.number - 1] = typeid
        self.submodels = <PyObject **>realloc(
            self.submodels, self.number * cython.sizeof(cython.pointer(PyObject))
        )
        self.submodels[self.number - 1] = <PyObject*>submodel

    def __dealloc__(self) -> None:
        free(self.submodels)
