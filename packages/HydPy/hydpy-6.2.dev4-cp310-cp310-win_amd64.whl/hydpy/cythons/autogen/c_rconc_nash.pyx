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

cdef public numpy.npy_bool TYPE_CHECKING = False
@cython.final
cdef class Parameters:
    pass
@cython.final
cdef class ControlParameters:
    pass
@cython.final
cdef class DerivedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._inflow_diskflag_reading:
            self.inflow = self._inflow_ncarray[0]
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._outflow_diskflag_reading:
            self.outflow = self._outflow_ncarray[0]
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._inflow_diskflag_writing:
            self._inflow_ncarray[0] = self.inflow
        if self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._outflow_diskflag_writing:
            self._outflow_ncarray[0] = self.outflow
        if self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._sc_diskflag_reading:
            k = 0
            for jdx0 in range(self._sc_length_0):
                self.sc[jdx0] = self._sc_ncarray[k]
                k += 1
        elif self._sc_ramflag:
            for jdx0 in range(self._sc_length_0):
                self.sc[jdx0] = self._sc_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._sc_diskflag_writing:
            k = 0
            for jdx0 in range(self._sc_length_0):
                self._sc_ncarray[k] = self.sc[jdx0]
                k += 1
        if self._sc_ramflag:
            for jdx0 in range(self._sc_length_0):
                self._sc_array[idx, jdx0] = self.sc[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.run()
        self.new2old()
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
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._sc_length_0):
            self.sequences.old_states.sc[jdx0] = self.sequences.new_states.sc[jdx0]
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
        if not self.threading:
            self.sequences.fluxes.update_outputs()
    cpdef void set_inflow_v1(self, double inflow) noexcept nogil:
        self.sequences.fluxes.inflow = inflow
    cpdef void determine_outflow_v2(self) noexcept nogil:
        cdef double d_q
        cdef numpy.int64_t j
        cdef numpy.int64_t _
        if (self.parameters.control.nmbstorages == 0) or isinf(self.parameters.derived.ksc):
            self.sequences.fluxes.outflow = self.sequences.fluxes.inflow
        else:
            self.sequences.fluxes.outflow = 0.0
            for _ in range(self.parameters.control.nmbsteps):
                self.sequences.states.sc[0] = self.sequences.states.sc[0] + (self.parameters.derived.dt * self.sequences.fluxes.inflow)
                for j in range(self.parameters.control.nmbstorages - 1):
                    d_q = min(self.parameters.derived.dt * self.parameters.derived.ksc * self.sequences.states.sc[j], self.sequences.states.sc[j])
                    self.sequences.states.sc[j] = self.sequences.states.sc[j] - (d_q)
                    self.sequences.states.sc[j + 1] = self.sequences.states.sc[j + 1] + (d_q)
                j = self.parameters.control.nmbstorages - 1
                d_q = min(self.parameters.derived.dt * self.parameters.derived.ksc * self.sequences.states.sc[j], self.sequences.states.sc[j])
                self.sequences.states.sc[j] = self.sequences.states.sc[j] - (d_q)
                self.sequences.fluxes.outflow = self.sequences.fluxes.outflow + (d_q)
    cpdef double get_outflow_v1(self) noexcept nogil:
        return self.sequences.fluxes.outflow
    cpdef void set_inflow(self, double inflow) noexcept nogil:
        self.sequences.fluxes.inflow = inflow
    cpdef void determine_outflow(self) noexcept nogil:
        cdef double d_q
        cdef numpy.int64_t j
        cdef numpy.int64_t _
        if (self.parameters.control.nmbstorages == 0) or isinf(self.parameters.derived.ksc):
            self.sequences.fluxes.outflow = self.sequences.fluxes.inflow
        else:
            self.sequences.fluxes.outflow = 0.0
            for _ in range(self.parameters.control.nmbsteps):
                self.sequences.states.sc[0] = self.sequences.states.sc[0] + (self.parameters.derived.dt * self.sequences.fluxes.inflow)
                for j in range(self.parameters.control.nmbstorages - 1):
                    d_q = min(self.parameters.derived.dt * self.parameters.derived.ksc * self.sequences.states.sc[j], self.sequences.states.sc[j])
                    self.sequences.states.sc[j] = self.sequences.states.sc[j] - (d_q)
                    self.sequences.states.sc[j + 1] = self.sequences.states.sc[j + 1] + (d_q)
                j = self.parameters.control.nmbstorages - 1
                d_q = min(self.parameters.derived.dt * self.parameters.derived.ksc * self.sequences.states.sc[j], self.sequences.states.sc[j])
                self.sequences.states.sc[j] = self.sequences.states.sc[j] - (d_q)
                self.sequences.fluxes.outflow = self.sequences.fluxes.outflow + (d_q)
    cpdef double get_outflow(self) noexcept nogil:
        return self.sequences.fluxes.outflow
