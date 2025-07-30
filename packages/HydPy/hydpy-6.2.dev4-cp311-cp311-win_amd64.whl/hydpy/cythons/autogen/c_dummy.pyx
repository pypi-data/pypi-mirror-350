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
cdef class Sequences:
    pass
@cython.final
cdef class InletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            k = 0
            for jdx0 in range(self._q_length_0):
                self.q[jdx0] = self._q_ncarray[k]
                k += 1
        elif self._q_ramflag:
            for jdx0 in range(self._q_length_0):
                self.q[jdx0] = self._q_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            k = 0
            for jdx0 in range(self._q_length_0):
                self._q_ncarray[k] = self.q[jdx0]
                k += 1
        if self._q_ramflag:
            for jdx0 in range(self._q_length_0):
                self._q_array[idx, jdx0] = self.q[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "q":
            self._q_length_0 = length
            self._q_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._q_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "q":
            PyMem_Free(self._q_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer[idx] = pointer.p_value
            self._q_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            values = numpy.empty(self.len_q)
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                values[idx] = self._q_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "q":
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                self._q_pointer[idx][0] = value[idx]
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptedwater_diskflag_reading:
            k = 0
            for jdx0 in range(self._interceptedwater_length_0):
                self.interceptedwater[jdx0] = self._interceptedwater_ncarray[k]
                k += 1
        elif self._interceptedwater_ramflag:
            for jdx0 in range(self._interceptedwater_length_0):
                self.interceptedwater[jdx0] = self._interceptedwater_array[idx, jdx0]
        if self._soilwater_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilwater_length_0):
                self.soilwater[jdx0] = self._soilwater_ncarray[k]
                k += 1
        elif self._soilwater_ramflag:
            for jdx0 in range(self._soilwater_length_0):
                self.soilwater[jdx0] = self._soilwater_array[idx, jdx0]
        if self._snowcover_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowcover_length_0):
                self.snowcover[jdx0] = self._snowcover_ncarray[k]
                k += 1
        elif self._snowcover_ramflag:
            for jdx0 in range(self._snowcover_length_0):
                self.snowcover[jdx0] = self._snowcover_array[idx, jdx0]
        if self._snowycanopy_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowycanopy_length_0):
                self.snowycanopy[jdx0] = self._snowycanopy_ncarray[k]
                k += 1
        elif self._snowycanopy_ramflag:
            for jdx0 in range(self._snowycanopy_length_0):
                self.snowycanopy[jdx0] = self._snowycanopy_array[idx, jdx0]
        if self._snowalbedo_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowalbedo_length_0):
                self.snowalbedo[jdx0] = self._snowalbedo_ncarray[k]
                k += 1
        elif self._snowalbedo_ramflag:
            for jdx0 in range(self._snowalbedo_length_0):
                self.snowalbedo[jdx0] = self._snowalbedo_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptedwater_diskflag_writing:
            k = 0
            for jdx0 in range(self._interceptedwater_length_0):
                self._interceptedwater_ncarray[k] = self.interceptedwater[jdx0]
                k += 1
        if self._interceptedwater_ramflag:
            for jdx0 in range(self._interceptedwater_length_0):
                self._interceptedwater_array[idx, jdx0] = self.interceptedwater[jdx0]
        if self._soilwater_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilwater_length_0):
                self._soilwater_ncarray[k] = self.soilwater[jdx0]
                k += 1
        if self._soilwater_ramflag:
            for jdx0 in range(self._soilwater_length_0):
                self._soilwater_array[idx, jdx0] = self.soilwater[jdx0]
        if self._snowcover_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowcover_length_0):
                self._snowcover_ncarray[k] = self.snowcover[jdx0]
                k += 1
        if self._snowcover_ramflag:
            for jdx0 in range(self._snowcover_length_0):
                self._snowcover_array[idx, jdx0] = self.snowcover[jdx0]
        if self._snowycanopy_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowycanopy_length_0):
                self._snowycanopy_ncarray[k] = self.snowycanopy[jdx0]
                k += 1
        if self._snowycanopy_ramflag:
            for jdx0 in range(self._snowycanopy_length_0):
                self._snowycanopy_array[idx, jdx0] = self.snowycanopy[jdx0]
        if self._snowalbedo_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowalbedo_length_0):
                self._snowalbedo_ncarray[k] = self.snowalbedo[jdx0]
                k += 1
        if self._snowalbedo_ramflag:
            for jdx0 in range(self._snowalbedo_length_0):
                self._snowalbedo_array[idx, jdx0] = self.snowalbedo[jdx0]
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            self.q = self._q_ncarray[0]
        elif self._q_ramflag:
            self.q = self._q_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            self._q_ncarray[0] = self.q
        if self._q_ramflag:
            self._q_array[idx] = self.q
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "q":
            self._q_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._q_outputflag:
            self._q_outputpointer[0] = self.q
@cython.final
cdef class OutletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            self.q = self._q_ncarray[0]
        elif self._q_ramflag:
            self.q = self._q_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            self._q_ncarray[0] = self.q
        if self._q_ramflag:
            self._q_array[idx] = self.q
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            return self._q_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self._q_pointer[0] = value
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.update_inlets()
        self.run()
        self.update_outlets()
        self.update_outputs()
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
        self.sequences.inlets.load_data(idx)
        self.sequences.inputs.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.inputs.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.pick_q_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_q_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i
        pass
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
    cpdef inline void pick_q_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.q = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.q = self.sequences.fluxes.q + (self.sequences.inlets.q[idx])
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.interceptedwater[k]
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.soilwater[k]
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowcover[k]
    cpdef double get_snowycanopy_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowycanopy[k]
    cpdef double get_snowalbedo_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowalbedo[k]
    cpdef inline void pass_q_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.q
    cpdef inline void pick_q(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.q = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.q = self.sequences.fluxes.q + (self.sequences.inlets.q[idx])
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.interceptedwater[k]
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.soilwater[k]
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowcover[k]
    cpdef double get_snowycanopy(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowycanopy[k]
    cpdef double get_snowalbedo(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.inputs.snowalbedo[k]
    cpdef inline void pass_q(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.q
