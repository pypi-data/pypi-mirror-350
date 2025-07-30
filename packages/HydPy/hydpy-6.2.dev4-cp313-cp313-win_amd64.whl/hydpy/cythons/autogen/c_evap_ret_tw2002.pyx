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
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._airtemperature_diskflag_reading:
            k = 0
            for jdx0 in range(self._airtemperature_length_0):
                self.airtemperature[jdx0] = self._airtemperature_ncarray[k]
                k += 1
        elif self._airtemperature_ramflag:
            for jdx0 in range(self._airtemperature_length_0):
                self.airtemperature[jdx0] = self._airtemperature_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._airtemperature_diskflag_writing:
            k = 0
            for jdx0 in range(self._airtemperature_length_0):
                self._airtemperature_ncarray[k] = self.airtemperature[jdx0]
                k += 1
        if self._airtemperature_ramflag:
            for jdx0 in range(self._airtemperature_length_0):
                self._airtemperature_array[idx, jdx0] = self.airtemperature[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._referenceevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self.referenceevapotranspiration[jdx0] = self._referenceevapotranspiration_ncarray[k]
                k += 1
        elif self._referenceevapotranspiration_ramflag:
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self.referenceevapotranspiration[jdx0] = self._referenceevapotranspiration_array[idx, jdx0]
        if self._meanreferenceevapotranspiration_diskflag_reading:
            self.meanreferenceevapotranspiration = self._meanreferenceevapotranspiration_ncarray[0]
        elif self._meanreferenceevapotranspiration_ramflag:
            self.meanreferenceevapotranspiration = self._meanreferenceevapotranspiration_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._referenceevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self._referenceevapotranspiration_ncarray[k] = self.referenceevapotranspiration[jdx0]
                k += 1
        if self._referenceevapotranspiration_ramflag:
            for jdx0 in range(self._referenceevapotranspiration_length_0):
                self._referenceevapotranspiration_array[idx, jdx0] = self.referenceevapotranspiration[jdx0]
        if self._meanreferenceevapotranspiration_diskflag_writing:
            self._meanreferenceevapotranspiration_ncarray[0] = self.meanreferenceevapotranspiration
        if self._meanreferenceevapotranspiration_ramflag:
            self._meanreferenceevapotranspiration_array[idx] = self.meanreferenceevapotranspiration
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
        if name == "meanreferenceevapotranspiration":
            self._meanreferenceevapotranspiration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._meanreferenceevapotranspiration_outputflag:
            self._meanreferenceevapotranspiration_outputpointer[0] = self.meanreferenceevapotranspiration
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.radiationmodel = None
        self.radiationmodel_is_mainmodel = False
        self.tempmodel = None
        self.tempmodel_is_mainmodel = False
    def get_radiationmodel(self) -> masterinterface.MasterInterface | None:
        return self.radiationmodel
    def set_radiationmodel(self, radiationmodel: masterinterface.MasterInterface | None) -> None:
        self.radiationmodel = radiationmodel
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
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.reset_reuseflags()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.load_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.save_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.new2old()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_globalradiation_v1()
        self.calc_airtemperature_v1()
        self.calc_referenceevapotranspiration_v2()
        self.adjust_referenceevapotranspiration_v1()
        self.calc_meanreferenceevapotranspiration_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_inlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_receivers(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_senders(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outputs()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outputs()
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 2:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_airtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_airtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_referenceevapotranspiration_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                (8.64 * self.sequences.fluxes.globalradiation + 93.0 * self.parameters.control.coastfactor[k])                * (self.sequences.factors.airtemperature[k] + 22.0)            ) / (                165.0                * (self.sequences.factors.airtemperature[k] + 123.0)                * (1.0 + 0.00019 * min(self.parameters.control.hrualtitude[k], 600.0))            )
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (self.parameters.control.evapotranspirationfactor[k])
    cpdef inline void calc_meanreferenceevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanreferenceevapotranspiration = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanreferenceevapotranspiration = self.sequences.fluxes.meanreferenceevapotranspiration + ((                self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.referenceevapotranspiration[s]            ))
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil:
        self.run()
    cpdef double get_potentialevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.referenceevapotranspiration[k]
    cpdef double get_meanpotentialevapotranspiration_v1(self) noexcept nogil:
        return self.sequences.fluxes.meanreferenceevapotranspiration
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airtemperature[k] = submodel.get_temperature(k)
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_temperature()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airtemperature[k] = submodel.get_temperature(k)
    cpdef inline void process_radiationmodel(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_globalradiation(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 2:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_airtemperature(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_airtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_airtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                (8.64 * self.sequences.fluxes.globalradiation + 93.0 * self.parameters.control.coastfactor[k])                * (self.sequences.factors.airtemperature[k] + 22.0)            ) / (                165.0                * (self.sequences.factors.airtemperature[k] + 123.0)                * (1.0 + 0.00019 * min(self.parameters.control.hrualtitude[k], 600.0))            )
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = self.sequences.fluxes.referenceevapotranspiration[k] * (self.parameters.control.evapotranspirationfactor[k])
    cpdef inline void calc_meanreferenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanreferenceevapotranspiration = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanreferenceevapotranspiration = self.sequences.fluxes.meanreferenceevapotranspiration + ((                self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.referenceevapotranspiration[s]            ))
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil:
        self.run()
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.referenceevapotranspiration[k]
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil:
        return self.sequences.fluxes.meanreferenceevapotranspiration
