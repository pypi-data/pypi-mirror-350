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
        if self._normalairtemperature_inputflag:
            self.normalairtemperature = self._normalairtemperature_inputpointer[0]
        elif self._normalairtemperature_diskflag_reading:
            self.normalairtemperature = self._normalairtemperature_ncarray[0]
        elif self._normalairtemperature_ramflag:
            self.normalairtemperature = self._normalairtemperature_array[idx]
        if self._normalevapotranspiration_inputflag:
            self.normalevapotranspiration = self._normalevapotranspiration_inputpointer[0]
        elif self._normalevapotranspiration_diskflag_reading:
            self.normalevapotranspiration = self._normalevapotranspiration_ncarray[0]
        elif self._normalevapotranspiration_ramflag:
            self.normalevapotranspiration = self._normalevapotranspiration_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._normalairtemperature_diskflag_writing:
            self._normalairtemperature_ncarray[0] = self.normalairtemperature
        if self._normalairtemperature_ramflag:
            self._normalairtemperature_array[idx] = self.normalairtemperature
        if self._normalevapotranspiration_diskflag_writing:
            self._normalevapotranspiration_ncarray[0] = self.normalevapotranspiration
        if self._normalevapotranspiration_ramflag:
            self._normalevapotranspiration_array[idx] = self.normalevapotranspiration
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "normalairtemperature":
            self._normalairtemperature_inputpointer = value.p_value
        if name == "normalevapotranspiration":
            self._normalevapotranspiration_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._meanairtemperature_diskflag_reading:
            self.meanairtemperature = self._meanairtemperature_ncarray[0]
        elif self._meanairtemperature_ramflag:
            self.meanairtemperature = self._meanairtemperature_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._meanairtemperature_diskflag_writing:
            self._meanairtemperature_ncarray[0] = self.meanairtemperature
        if self._meanairtemperature_ramflag:
            self._meanairtemperature_array[idx] = self.meanairtemperature
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "meanairtemperature":
            self._meanairtemperature_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._meanairtemperature_outputflag:
            self._meanairtemperature_outputpointer[0] = self.meanairtemperature
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
        if self._precipitation_diskflag_writing:
            k = 0
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_ncarray[k] = self.precipitation[jdx0]
                k += 1
        if self._precipitation_ramflag:
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_array[idx, jdx0] = self.precipitation[jdx0]
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
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.precipmodel = None
        self.precipmodel_is_mainmodel = False
        self.tempmodel = None
        self.tempmodel_is_mainmodel = False
    def get_precipmodel(self) -> masterinterface.MasterInterface | None:
        return self.precipmodel
    def set_precipmodel(self, precipmodel: masterinterface.MasterInterface | None) -> None:
        self.precipmodel = precipmodel
    def get_tempmodel(self) -> masterinterface.MasterInterface | None:
        return self.tempmodel
    def set_tempmodel(self, tempmodel: masterinterface.MasterInterface | None) -> None:
        self.tempmodel = tempmodel
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
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.reset_reuseflags()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.load_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.save_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.new2old()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.calc_meanairtemperature_v1()
        self.calc_precipitation_v1()
        self.calc_referenceevapotranspiration_v5()
        self.adjust_referenceevapotranspiration_v1()
        self.calc_potentialevapotranspiration_v3()
        self.calc_meanpotentialevapotranspiration_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_inlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_receivers(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_senders(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outputs()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outputs()
    cpdef inline void calc_meanairtemperature_v1(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_meanairtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_meanairtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        if self.precipmodel_typeid == 1:
            self.calc_precipitation_precipmodel_v1(                (<masterinterface.MasterInterface>self.precipmodel)            )
        elif self.precipmodel_typeid == 2:
            self.calc_precipitation_precipmodel_v2(                (<masterinterface.MasterInterface>self.precipmodel)            )
    cpdef inline void calc_referenceevapotranspiration_v5(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.inputs.normalevapotranspiration * (                1.0                + self.parameters.control.airtemperaturefactor[k]                * (self.sequences.factors.meanairtemperature - self.sequences.inputs.normalairtemperature)            )
            self.sequences.fluxes.referenceevapotranspiration[k] = min(                max(self.sequences.fluxes.referenceevapotranspiration[k], 0.0),                2.0 * self.sequences.inputs.normalevapotranspiration,            )
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (self.parameters.control.evapotranspirationfactor[k])
    cpdef inline void calc_potentialevapotranspiration_v3(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (                1.0                - self.parameters.control.altitudefactor[k] / 100.0 * (self.parameters.control.hrualtitude[k] - self.parameters.derived.altitude)            )
            if self.sequences.fluxes.potentialevapotranspiration[k] <= 0.0:
                self.sequences.fluxes.potentialevapotranspiration[k] = 0.0
            else:
                self.sequences.fluxes.potentialevapotranspiration[k] = self.sequences.fluxes.potentialevapotranspiration[k] * (exp(                    -self.parameters.control.precipitationfactor[k] * self.sequences.fluxes.precipitation[k]                ))
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
    cpdef inline void calc_meanairtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        self.sequences.factors.meanairtemperature = submodel.get_meantemperature()
    cpdef inline void calc_meanairtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.determine_temperature()
        self.sequences.factors.meanairtemperature = submodel.get_meantemperature()
    cpdef inline void calc_precipitation_precipmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = submodel.get_precipitation(k)
    cpdef inline void calc_precipitation_precipmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_precipitation()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = submodel.get_precipitation(k)
    cpdef inline void calc_meanairtemperature(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_meanairtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_meanairtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_precipitation(self) noexcept nogil:
        if self.precipmodel_typeid == 1:
            self.calc_precipitation_precipmodel_v1(                (<masterinterface.MasterInterface>self.precipmodel)            )
        elif self.precipmodel_typeid == 2:
            self.calc_precipitation_precipmodel_v2(                (<masterinterface.MasterInterface>self.precipmodel)            )
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.inputs.normalevapotranspiration * (                1.0                + self.parameters.control.airtemperaturefactor[k]                * (self.sequences.factors.meanairtemperature - self.sequences.inputs.normalairtemperature)            )
            self.sequences.fluxes.referenceevapotranspiration[k] = min(                max(self.sequences.fluxes.referenceevapotranspiration[k], 0.0),                2.0 * self.sequences.inputs.normalevapotranspiration,            )
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (self.parameters.control.evapotranspirationfactor[k])
    cpdef inline void calc_potentialevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (                1.0                - self.parameters.control.altitudefactor[k] / 100.0 * (self.parameters.control.hrualtitude[k] - self.parameters.derived.altitude)            )
            if self.sequences.fluxes.potentialevapotranspiration[k] <= 0.0:
                self.sequences.fluxes.potentialevapotranspiration[k] = 0.0
            else:
                self.sequences.fluxes.potentialevapotranspiration[k] = self.sequences.fluxes.potentialevapotranspiration[k] * (exp(                    -self.parameters.control.precipitationfactor[k] * self.sequences.fluxes.precipitation[k]                ))
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
