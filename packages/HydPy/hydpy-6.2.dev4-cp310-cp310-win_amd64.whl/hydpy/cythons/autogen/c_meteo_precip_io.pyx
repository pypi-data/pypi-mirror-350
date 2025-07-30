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
cdef class DerivedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_inputflag:
            self.precipitation = self._precipitation_inputpointer[0]
        elif self._precipitation_diskflag_reading:
            self.precipitation = self._precipitation_ncarray[0]
        elif self._precipitation_ramflag:
            self.precipitation = self._precipitation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_diskflag_writing:
            self._precipitation_ncarray[0] = self.precipitation
        if self._precipitation_ramflag:
            self._precipitation_array[idx] = self.precipitation
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "precipitation":
            self._precipitation_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._precipitation_diskflag_reading:
            k = 0
            for jdx0 in range(self._precipitation_length_0):
                self.precipitation[jdx0] = self._precipitation_ncarray[k]
                k += 1
        elif self._precipitation_ramflag:
            for jdx0 in range(self._precipitation_length_0):
                self.precipitation[jdx0] = self._precipitation_array[idx, jdx0]
        if self._meanprecipitation_diskflag_reading:
            self.meanprecipitation = self._meanprecipitation_ncarray[0]
        elif self._meanprecipitation_ramflag:
            self.meanprecipitation = self._meanprecipitation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._precipitation_diskflag_writing:
            k = 0
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_ncarray[k] = self.precipitation[jdx0]
                k += 1
        if self._precipitation_ramflag:
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_array[idx, jdx0] = self.precipitation[jdx0]
        if self._meanprecipitation_diskflag_writing:
            self._meanprecipitation_ncarray[0] = self.meanprecipitation
        if self._meanprecipitation_ramflag:
            self._meanprecipitation_array[idx] = self.meanprecipitation
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "meanprecipitation":
            self._meanprecipitation_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._meanprecipitation_outputflag:
            self._meanprecipitation_outputpointer[0] = self.meanprecipitation
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.run()
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
        self.sequences.inputs.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.fluxes.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.calc_precipitation_v1()
        self.adjust_precipitation_v1()
        self.calc_meanprecipitation_v1()
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
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.inputs.precipitation
    cpdef inline void adjust_precipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.fluxes.precipitation[k] * (self.parameters.control.precipitationfactor[k])
    cpdef inline void calc_meanprecipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanprecipitation = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanprecipitation = self.sequences.fluxes.meanprecipitation + (self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.precipitation[s])
    cpdef void determine_precipitation_v1(self) noexcept nogil:
        self.run()
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.precipitation[s]
    cpdef double get_meanprecipitation_v1(self) noexcept nogil:
        return self.sequences.fluxes.meanprecipitation
    cpdef inline void calc_precipitation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.inputs.precipitation
    cpdef inline void adjust_precipitation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.fluxes.precipitation[k] * (self.parameters.control.precipitationfactor[k])
    cpdef inline void calc_meanprecipitation(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanprecipitation = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanprecipitation = self.sequences.fluxes.meanprecipitation + (self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.precipitation[s])
    cpdef void determine_precipitation(self) noexcept nogil:
        self.run()
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.precipitation[s]
    cpdef double get_meanprecipitation(self) noexcept nogil:
        return self.sequences.fluxes.meanprecipitation
