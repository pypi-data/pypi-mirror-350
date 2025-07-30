#!python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
from typing import Optional
import numpy
cimport numpy
from libc.math cimport exp, fabs, log, sin, cos, tan, tanh, asin, acos, atan, isnan, isinf
from libc.math cimport NAN as nan
from libc.math cimport INFINITY as inf
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen cimport interfaceutils
from hydpy.cythons.autogen cimport interputils
from hydpy.cythons.autogen import pointerutils
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport quadutils
from hydpy.cythons.autogen cimport rootutils
from hydpy.cythons.autogen cimport smoothutils
from hydpy.cythons.autogen cimport masterinterface


cdef void do_nothing(Model model)  noexcept nogil:
    pass

cpdef get_wrapper():
    cdef CallbackWrapper wrapper = CallbackWrapper()
    wrapper.callback = do_nothing
    return wrapper

@cython.final
cdef class Parameters:
    pass
@cython.final
cdef class ControlParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._snowycanopy_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowycanopy_length_0):
                self.snowycanopy[jdx0] = self._snowycanopy_ncarray[k]
                k += 1
        elif self._snowycanopy_ramflag:
            for jdx0 in range(self._snowycanopy_length_0):
                self.snowycanopy[jdx0] = self._snowycanopy_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._snowycanopy_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowycanopy_length_0):
                self._snowycanopy_ncarray[k] = self.snowycanopy[jdx0]
                k += 1
        if self._snowycanopy_ramflag:
            for jdx0 in range(self._snowycanopy_length_0):
                self._snowycanopy_array[idx, jdx0] = self.snowycanopy[jdx0]
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.run()
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil:
        cdef numpy.int64_t i
        with nogil:
            for i in range(i0, i1):
                self.simulate(i)
                self.update_senders(i)
                self.update_receivers(i)
                self.save_data(i)
    cpdef void reset_reuseflags(self) noexcept nogil:
        pass
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        pass
    cpdef void update_outlets(self) noexcept nogil:
        pass
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i
        pass
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        pass
    cpdef double get_snowycanopy_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowycanopy[k]
    cpdef double get_snowycanopy(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowycanopy[k]
