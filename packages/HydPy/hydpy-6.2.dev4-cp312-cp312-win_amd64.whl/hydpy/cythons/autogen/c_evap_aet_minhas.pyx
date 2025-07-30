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
cdef class FactorSequences:
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
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._potentialinterceptionevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialinterceptionevaporation_length_0):
                self.potentialinterceptionevaporation[jdx0] = self._potentialinterceptionevaporation_ncarray[k]
                k += 1
        elif self._potentialinterceptionevaporation_ramflag:
            for jdx0 in range(self._potentialinterceptionevaporation_length_0):
                self.potentialinterceptionevaporation[jdx0] = self._potentialinterceptionevaporation_array[idx, jdx0]
        if self._potentialsoilevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialsoilevapotranspiration_length_0):
                self.potentialsoilevapotranspiration[jdx0] = self._potentialsoilevapotranspiration_ncarray[k]
                k += 1
        elif self._potentialsoilevapotranspiration_ramflag:
            for jdx0 in range(self._potentialsoilevapotranspiration_length_0):
                self.potentialsoilevapotranspiration[jdx0] = self._potentialsoilevapotranspiration_array[idx, jdx0]
        if self._potentialwaterevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialwaterevaporation_length_0):
                self.potentialwaterevaporation[jdx0] = self._potentialwaterevaporation_ncarray[k]
                k += 1
        elif self._potentialwaterevaporation_ramflag:
            for jdx0 in range(self._potentialwaterevaporation_length_0):
                self.potentialwaterevaporation[jdx0] = self._potentialwaterevaporation_array[idx, jdx0]
        if self._waterevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterevaporation_length_0):
                self.waterevaporation[jdx0] = self._waterevaporation_ncarray[k]
                k += 1
        elif self._waterevaporation_ramflag:
            for jdx0 in range(self._waterevaporation_length_0):
                self.waterevaporation[jdx0] = self._waterevaporation_array[idx, jdx0]
        if self._interceptionevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._interceptionevaporation_length_0):
                self.interceptionevaporation[jdx0] = self._interceptionevaporation_ncarray[k]
                k += 1
        elif self._interceptionevaporation_ramflag:
            for jdx0 in range(self._interceptionevaporation_length_0):
                self.interceptionevaporation[jdx0] = self._interceptionevaporation_array[idx, jdx0]
        if self._soilevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self.soilevapotranspiration[jdx0] = self._soilevapotranspiration_ncarray[k]
                k += 1
        elif self._soilevapotranspiration_ramflag:
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self.soilevapotranspiration[jdx0] = self._soilevapotranspiration_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._potentialinterceptionevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialinterceptionevaporation_length_0):
                self._potentialinterceptionevaporation_ncarray[k] = self.potentialinterceptionevaporation[jdx0]
                k += 1
        if self._potentialinterceptionevaporation_ramflag:
            for jdx0 in range(self._potentialinterceptionevaporation_length_0):
                self._potentialinterceptionevaporation_array[idx, jdx0] = self.potentialinterceptionevaporation[jdx0]
        if self._potentialsoilevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialsoilevapotranspiration_length_0):
                self._potentialsoilevapotranspiration_ncarray[k] = self.potentialsoilevapotranspiration[jdx0]
                k += 1
        if self._potentialsoilevapotranspiration_ramflag:
            for jdx0 in range(self._potentialsoilevapotranspiration_length_0):
                self._potentialsoilevapotranspiration_array[idx, jdx0] = self.potentialsoilevapotranspiration[jdx0]
        if self._potentialwaterevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialwaterevaporation_length_0):
                self._potentialwaterevaporation_ncarray[k] = self.potentialwaterevaporation[jdx0]
                k += 1
        if self._potentialwaterevaporation_ramflag:
            for jdx0 in range(self._potentialwaterevaporation_length_0):
                self._potentialwaterevaporation_array[idx, jdx0] = self.potentialwaterevaporation[jdx0]
        if self._waterevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterevaporation_length_0):
                self._waterevaporation_ncarray[k] = self.waterevaporation[jdx0]
                k += 1
        if self._waterevaporation_ramflag:
            for jdx0 in range(self._waterevaporation_length_0):
                self._waterevaporation_array[idx, jdx0] = self.waterevaporation[jdx0]
        if self._interceptionevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._interceptionevaporation_length_0):
                self._interceptionevaporation_ncarray[k] = self.interceptionevaporation[jdx0]
                k += 1
        if self._interceptionevaporation_ramflag:
            for jdx0 in range(self._interceptionevaporation_length_0):
                self._interceptionevaporation_array[idx, jdx0] = self.interceptionevaporation[jdx0]
        if self._soilevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self._soilevapotranspiration_ncarray[k] = self.soilevapotranspiration[jdx0]
                k += 1
        if self._soilevapotranspiration_ramflag:
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self._soilevapotranspiration_array[idx, jdx0] = self.soilevapotranspiration[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.intercmodel = None
        self.intercmodel_is_mainmodel = False
        self.petmodel = None
        self.petmodel_is_mainmodel = False
        self.soilwatermodel = None
        self.soilwatermodel_is_mainmodel = False
    def get_intercmodel(self) -> masterinterface.MasterInterface | None:
        return self.intercmodel
    def set_intercmodel(self, intercmodel: masterinterface.MasterInterface | None) -> None:
        self.intercmodel = intercmodel
    def get_petmodel(self) -> masterinterface.MasterInterface | None:
        return self.petmodel
    def set_petmodel(self, petmodel: masterinterface.MasterInterface | None) -> None:
        self.petmodel = petmodel
    def get_soilwatermodel(self) -> masterinterface.MasterInterface | None:
        return self.soilwatermodel
    def set_soilwatermodel(self, soilwatermodel: masterinterface.MasterInterface | None) -> None:
        self.soilwatermodel = soilwatermodel
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
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.reset_reuseflags()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.reset_reuseflags()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.load_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.load_data(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.save_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.save_data(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.new2old()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.new2old()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.determine_interceptionevaporation_v1()
        self.determine_soilevapotranspiration_v2()
        self.determine_waterevaporation_v2()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_inlets()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_inlets()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_outlets()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_outlets()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_receivers(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_receivers(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_senders(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_senders(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        pass
    cpdef double get_waterevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.waterevaporation[k]
    cpdef double get_interceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.interceptionevaporation[k]
    cpdef double get_soilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.soilevapotranspiration[k]
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialevapotranspiration()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialinterceptionevaporation[k] = (                submodel.get_potentialevapotranspiration(k)            )
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialinterceptionevaporation()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialinterceptionevaporation[k] = (                submodel.get_potentialinterceptionevaporation(k)            )
    cpdef inline void calc_potentialinterceptionevaporation_v3(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialinterceptionevaporation_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialinterceptionevaporation_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_potentialwaterevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialwaterevaporation[k] = submodel.get_potentialevapotranspiration(                k            )
    cpdef inline void calc_potentialwaterevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialwaterevaporation()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialwaterevaporation[k] = submodel.get_potentialwaterevaporation(k)
    cpdef inline void calc_potentialwaterevaporation_v1(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialwaterevaporation_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialwaterevaporation_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_waterevaporation_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.waterevaporation[k] = self.sequences.fluxes.potentialwaterevaporation[k]
            else:
                self.sequences.fluxes.waterevaporation[k] = 0.0
    cpdef inline void calc_interceptedwater_v1(self) noexcept nogil:
        if self.intercmodel_typeid == 1:
            self.calc_interceptedwater_intercmodel_v1(                (<masterinterface.MasterInterface>self.intercmodel)            )
    cpdef inline void calc_interceptionevaporation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                self.sequences.fluxes.interceptionevaporation[k] = min(                    self.sequences.fluxes.potentialinterceptionevaporation[k], self.sequences.factors.interceptedwater[k]                )
            else:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
    cpdef inline void calc_soilwater_v1(self) noexcept nogil:
        if self.soilwatermodel_typeid == 1:
            self.calc_soilwater_soilwatermodel_v1(                (<masterinterface.MasterInterface>self.soilwatermodel)            )
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialsoilevapotranspiration[k] = (                submodel.get_potentialevapotranspiration(k)            )
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialsoilevapotranspiration()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.potentialsoilevapotranspiration[k] = (                submodel.get_potentialsoilevapotranspiration(k)            )
    cpdef inline void calc_potentialsoilevapotranspiration_v2(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialsoilevapotranspiration_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialsoilevapotranspiration_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_soilevapotranspiration_v2(self) noexcept nogil:
        cdef double temp
        cdef double moisture
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.potentialsoilevapotranspiration[k]
                if self.sequences.fluxes.soilevapotranspiration[k] > 0.0:
                    moisture = self.sequences.factors.soilwater[k] / self.parameters.control.maxsoilwater[k]
                    if moisture <= 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = 0.0
                    elif moisture <= 1.0:
                        temp = exp(-self.parameters.control.dissefactor[k] * moisture)
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * ((1.0 - temp) / (                            1.0 + temp - 2.0 * exp(-self.parameters.control.dissefactor[k])                        ))
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
    cpdef inline void update_soilevapotranspiration_v3(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                if self.parameters.control.interception[k]:
                    if self.sequences.fluxes.potentialinterceptionevaporation[k] == 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = 0.0
                    else:
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * ((                            self.sequences.fluxes.potentialinterceptionevaporation[k]                            - self.sequences.fluxes.interceptionevaporation[k]                        ) / self.sequences.fluxes.potentialinterceptionevaporation[k])
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
    cpdef inline void calc_interceptedwater_intercmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.interceptedwater[k] = submodel.get_interceptedwater(k)
    cpdef inline void calc_soilwater_soilwatermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.soilwater[k] = submodel.get_soilwater(k)
    cpdef double get_waterevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.waterevaporation[k]
    cpdef double get_interceptionevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.interceptionevaporation[k]
    cpdef double get_soilevapotranspiration(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.soilevapotranspiration[k]
    cpdef inline void calc_potentialinterceptionevaporation(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialinterceptionevaporation_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialinterceptionevaporation_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_potentialwaterevaporation(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialwaterevaporation_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialwaterevaporation_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_waterevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.waterevaporation[k] = self.sequences.fluxes.potentialwaterevaporation[k]
            else:
                self.sequences.fluxes.waterevaporation[k] = 0.0
    cpdef inline void calc_interceptedwater(self) noexcept nogil:
        if self.intercmodel_typeid == 1:
            self.calc_interceptedwater_intercmodel_v1(                (<masterinterface.MasterInterface>self.intercmodel)            )
    cpdef inline void calc_interceptionevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                self.sequences.fluxes.interceptionevaporation[k] = min(                    self.sequences.fluxes.potentialinterceptionevaporation[k], self.sequences.factors.interceptedwater[k]                )
            else:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
    cpdef inline void calc_soilwater(self) noexcept nogil:
        if self.soilwatermodel_typeid == 1:
            self.calc_soilwater_soilwatermodel_v1(                (<masterinterface.MasterInterface>self.soilwatermodel)            )
    cpdef inline void calc_potentialsoilevapotranspiration(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_potentialsoilevapotranspiration_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_potentialsoilevapotranspiration_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_soilevapotranspiration(self) noexcept nogil:
        cdef double temp
        cdef double moisture
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.potentialsoilevapotranspiration[k]
                if self.sequences.fluxes.soilevapotranspiration[k] > 0.0:
                    moisture = self.sequences.factors.soilwater[k] / self.parameters.control.maxsoilwater[k]
                    if moisture <= 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = 0.0
                    elif moisture <= 1.0:
                        temp = exp(-self.parameters.control.dissefactor[k] * moisture)
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * ((1.0 - temp) / (                            1.0 + temp - 2.0 * exp(-self.parameters.control.dissefactor[k])                        ))
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
    cpdef inline void update_soilevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                if self.parameters.control.interception[k]:
                    if self.sequences.fluxes.potentialinterceptionevaporation[k] == 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = 0.0
                    else:
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * ((                            self.sequences.fluxes.potentialinterceptionevaporation[k]                            - self.sequences.fluxes.interceptionevaporation[k]                        ) / self.sequences.fluxes.potentialinterceptionevaporation[k])
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
    cpdef inline void calc_interceptedwater_intercmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.interceptedwater[k] = submodel.get_interceptedwater(k)
    cpdef inline void calc_soilwater_soilwatermodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.soilwater[k] = submodel.get_soilwater(k)
    cpdef void determine_interceptionevaporation_v1(self) noexcept nogil:
        self.calc_potentialinterceptionevaporation_v3()
        self.calc_interceptedwater_v1()
        self.calc_interceptionevaporation_v1()
    cpdef void determine_soilevapotranspiration_v2(self) noexcept nogil:
        self.calc_soilwater_v1()
        self.calc_potentialsoilevapotranspiration_v2()
        self.calc_soilevapotranspiration_v2()
        self.update_soilevapotranspiration_v3()
    cpdef void determine_waterevaporation_v2(self) noexcept nogil:
        self.calc_potentialwaterevaporation_v1()
        self.calc_waterevaporation_v2()
    cpdef void determine_interceptionevaporation(self) noexcept nogil:
        self.calc_potentialinterceptionevaporation_v3()
        self.calc_interceptedwater_v1()
        self.calc_interceptionevaporation_v1()
    cpdef void determine_soilevapotranspiration(self) noexcept nogil:
        self.calc_soilwater_v1()
        self.calc_potentialsoilevapotranspiration_v2()
        self.calc_soilevapotranspiration_v2()
        self.update_soilevapotranspiration_v3()
    cpdef void determine_waterevaporation(self) noexcept nogil:
        self.calc_potentialwaterevaporation_v1()
        self.calc_waterevaporation_v2()
