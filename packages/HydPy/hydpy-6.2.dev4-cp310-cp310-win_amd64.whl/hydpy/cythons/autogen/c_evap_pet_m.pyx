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
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._referenceevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self.referenceevapotranspiration[jdx0] = self._referenceevapotranspiration_ncarray[k]
                k += 1
        elif self._referenceevapotranspiration_ramflag:
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self.referenceevapotranspiration[jdx0] = self._referenceevapotranspiration_array[idx, jdx0]
        if self._potentialevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialevapotranspiration_length_0):
                self.potentialevapotranspiration[jdx0] = self._potentialevapotranspiration_ncarray[k]
                k += 1
        elif self._potentialevapotranspiration_ramflag:
            for jdx0 in range(self._potentialevapotranspiration_length_0):
                self.potentialevapotranspiration[jdx0] = self._potentialevapotranspiration_array[idx, jdx0]
        if self._meanpotentialevapotranspiration_diskflag_reading:
            self.meanpotentialevapotranspiration = self._meanpotentialevapotranspiration_ncarray[0]
        elif self._meanpotentialevapotranspiration_ramflag:
            self.meanpotentialevapotranspiration = self._meanpotentialevapotranspiration_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._referenceevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self._referenceevapotranspiration_ncarray[k] = self.referenceevapotranspiration[jdx0]
                k += 1
        if self._referenceevapotranspiration_ramflag:
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self._referenceevapotranspiration_array[idx, jdx0] = self.referenceevapotranspiration[jdx0]
        if self._potentialevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialevapotranspiration_length_0):
                self._potentialevapotranspiration_ncarray[k] = self.potentialevapotranspiration[jdx0]
                k += 1
        if self._potentialevapotranspiration_ramflag:
            for jdx0 in range(self._potentialevapotranspiration_length_0):
                self._potentialevapotranspiration_array[idx, jdx0] = self.potentialevapotranspiration[jdx0]
        if self._meanpotentialevapotranspiration_diskflag_writing:
            self._meanpotentialevapotranspiration_ncarray[0] = self.meanpotentialevapotranspiration
        if self._meanpotentialevapotranspiration_ramflag:
            self._meanpotentialevapotranspiration_array[idx] = self.meanpotentialevapotranspiration
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "meanpotentialevapotranspiration":
            self._meanpotentialevapotranspiration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._meanpotentialevapotranspiration_outputflag:
            self._meanpotentialevapotranspiration_outputpointer[0] = self.meanpotentialevapotranspiration
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.retmodel = None
        self.retmodel_is_mainmodel = False
    def get_retmodel(self) -> masterinterface.MasterInterface | None:
        return self.retmodel
    def set_retmodel(self, retmodel: masterinterface.MasterInterface | None) -> None:
        self.retmodel = retmodel
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.reset_reuseflags()
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
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.fluxes.save_data(idx)
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.calc_referenceevapotranspiration_v4()
        self.calc_potentialevapotranspiration_v1()
        self.update_potentialevapotranspiration_v1()
        self.calc_meanpotentialevapotranspiration_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
        if (self.retmodel is not None) and not self.retmodel_is_mainmodel:
            self.retmodel.update_outputs()
    cpdef inline void calc_referenceevapotranspiration_v4(self) noexcept nogil:
        if self.retmodel_typeid == 1:
            self.calc_referenceevapotranspiration_petmodel_v1(                (<masterinterface.MasterInterface>self.retmodel)            )
    cpdef inline void calc_potentialevapotranspiration_v1(self) noexcept nogil:
        cdef double factor
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            factor = self.parameters.control.monthfactor[                self.parameters.derived.moy[self.idx_sim] - self.parameters.control._monthfactor_entrymin            ]
            self.sequences.fluxes.potentialevapotranspiration[k] = (                factor * self.sequences.fluxes.referenceevapotranspiration[k]            )
    cpdef inline void update_potentialevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialevapotranspiration[k] = (                self.parameters.control.dampingfactor[k] * self.sequences.fluxes.potentialevapotranspiration[k]                + (1.0 - self.parameters.control.dampingfactor[k])                * self.sequences.logs.loggedpotentialevapotranspiration[0, k]            )
            self.sequences.logs.loggedpotentialevapotranspiration[0, k] = (                self.sequences.fluxes.potentialevapotranspiration[k]            )
    cpdef inline void calc_meanpotentialevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanpotentialevapotranspiration = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanpotentialevapotranspiration = self.sequences.fluxes.meanpotentialevapotranspiration + ((                self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.potentialevapotranspiration[s]            ))
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil:
        self.run()
    cpdef double get_potentialevapotranspiration_v2(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialevapotranspiration[k]
    cpdef double get_meanpotentialevapotranspiration_v2(self) noexcept nogil:
        return self.sequences.fluxes.meanpotentialevapotranspiration
    cpdef inline void calc_referenceevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialevapotranspiration()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                submodel.get_potentialevapotranspiration(k)            )
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil:
        if self.retmodel_typeid == 1:
            self.calc_referenceevapotranspiration_petmodel_v1(                (<masterinterface.MasterInterface>self.retmodel)            )
    cpdef inline void calc_potentialevapotranspiration(self) noexcept nogil:
        cdef double factor
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            factor = self.parameters.control.monthfactor[                self.parameters.derived.moy[self.idx_sim] - self.parameters.control._monthfactor_entrymin            ]
            self.sequences.fluxes.potentialevapotranspiration[k] = (                factor * self.sequences.fluxes.referenceevapotranspiration[k]            )
    cpdef inline void update_potentialevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialevapotranspiration[k] = (                self.parameters.control.dampingfactor[k] * self.sequences.fluxes.potentialevapotranspiration[k]                + (1.0 - self.parameters.control.dampingfactor[k])                * self.sequences.logs.loggedpotentialevapotranspiration[0, k]            )
            self.sequences.logs.loggedpotentialevapotranspiration[0, k] = (                self.sequences.fluxes.potentialevapotranspiration[k]            )
    cpdef inline void calc_meanpotentialevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanpotentialevapotranspiration = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanpotentialevapotranspiration = self.sequences.fluxes.meanpotentialevapotranspiration + ((                self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.potentialevapotranspiration[s]            ))
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil:
        self.run()
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialevapotranspiration[k]
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil:
        return self.sequences.fluxes.meanpotentialevapotranspiration
    cpdef inline void calc_referenceevapotranspiration_petmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialevapotranspiration()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                submodel.get_potentialevapotranspiration(k)            )
