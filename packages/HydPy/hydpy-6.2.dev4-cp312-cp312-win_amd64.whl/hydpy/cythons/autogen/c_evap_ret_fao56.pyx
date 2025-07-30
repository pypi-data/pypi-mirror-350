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
        if self._relativehumidity_inputflag:
            self.relativehumidity = self._relativehumidity_inputpointer[0]
        elif self._relativehumidity_diskflag_reading:
            self.relativehumidity = self._relativehumidity_ncarray[0]
        elif self._relativehumidity_ramflag:
            self.relativehumidity = self._relativehumidity_array[idx]
        if self._windspeed_inputflag:
            self.windspeed = self._windspeed_inputpointer[0]
        elif self._windspeed_diskflag_reading:
            self.windspeed = self._windspeed_ncarray[0]
        elif self._windspeed_ramflag:
            self.windspeed = self._windspeed_array[idx]
        if self._atmosphericpressure_inputflag:
            self.atmosphericpressure = self._atmosphericpressure_inputpointer[0]
        elif self._atmosphericpressure_diskflag_reading:
            self.atmosphericpressure = self._atmosphericpressure_ncarray[0]
        elif self._atmosphericpressure_ramflag:
            self.atmosphericpressure = self._atmosphericpressure_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._relativehumidity_diskflag_writing:
            self._relativehumidity_ncarray[0] = self.relativehumidity
        if self._relativehumidity_ramflag:
            self._relativehumidity_array[idx] = self.relativehumidity
        if self._windspeed_diskflag_writing:
            self._windspeed_ncarray[0] = self.windspeed
        if self._windspeed_ramflag:
            self._windspeed_array[idx] = self.windspeed
        if self._atmosphericpressure_diskflag_writing:
            self._atmosphericpressure_ncarray[0] = self.atmosphericpressure
        if self._atmosphericpressure_ramflag:
            self._atmosphericpressure_array[idx] = self.atmosphericpressure
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "relativehumidity":
            self._relativehumidity_inputpointer = value.p_value
        if name == "windspeed":
            self._windspeed_inputpointer = value.p_value
        if name == "atmosphericpressure":
            self._atmosphericpressure_inputpointer = value.p_value
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
        if self._windspeed2m_diskflag_reading:
            self.windspeed2m = self._windspeed2m_ncarray[0]
        elif self._windspeed2m_ramflag:
            self.windspeed2m = self._windspeed2m_array[idx]
        if self._saturationvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_ncarray[k]
                k += 1
        elif self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_array[idx, jdx0]
        if self._saturationvapourpressureslope_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self.saturationvapourpressureslope[jdx0] = self._saturationvapourpressureslope_ncarray[k]
                k += 1
        elif self._saturationvapourpressureslope_ramflag:
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self.saturationvapourpressureslope[jdx0] = self._saturationvapourpressureslope_array[idx, jdx0]
        if self._actualvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_ncarray[k]
                k += 1
        elif self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_array[idx, jdx0]
        if self._psychrometricconstant_diskflag_reading:
            self.psychrometricconstant = self._psychrometricconstant_ncarray[0]
        elif self._psychrometricconstant_ramflag:
            self.psychrometricconstant = self._psychrometricconstant_array[idx]
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
        if self._windspeed2m_diskflag_writing:
            self._windspeed2m_ncarray[0] = self.windspeed2m
        if self._windspeed2m_ramflag:
            self._windspeed2m_array[idx] = self.windspeed2m
        if self._saturationvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_ncarray[k] = self.saturationvapourpressure[jdx0]
                k += 1
        if self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_array[idx, jdx0] = self.saturationvapourpressure[jdx0]
        if self._saturationvapourpressureslope_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self._saturationvapourpressureslope_ncarray[k] = self.saturationvapourpressureslope[jdx0]
                k += 1
        if self._saturationvapourpressureslope_ramflag:
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self._saturationvapourpressureslope_array[idx, jdx0] = self.saturationvapourpressureslope[jdx0]
        if self._actualvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_ncarray[k] = self.actualvapourpressure[jdx0]
                k += 1
        if self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_array[idx, jdx0] = self.actualvapourpressure[jdx0]
        if self._psychrometricconstant_diskflag_writing:
            self._psychrometricconstant_ncarray[0] = self.psychrometricconstant
        if self._psychrometricconstant_ramflag:
            self._psychrometricconstant_array[idx] = self.psychrometricconstant
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "windspeed2m":
            self._windspeed2m_outputpointer = value.p_value
        if name == "psychrometricconstant":
            self._psychrometricconstant_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._windspeed2m_outputflag:
            self._windspeed2m_outputpointer[0] = self.windspeed2m
        if self._psychrometricconstant_outputflag:
            self._psychrometricconstant_outputpointer[0] = self.psychrometricconstant
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._clearskysolarradiation_diskflag_reading:
            self.clearskysolarradiation = self._clearskysolarradiation_ncarray[0]
        elif self._clearskysolarradiation_ramflag:
            self.clearskysolarradiation = self._clearskysolarradiation_array[idx]
        if self._netshortwaveradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self.netshortwaveradiation[jdx0] = self._netshortwaveradiation_ncarray[k]
                k += 1
        elif self._netshortwaveradiation_ramflag:
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self.netshortwaveradiation[jdx0] = self._netshortwaveradiation_array[idx, jdx0]
        if self._netlongwaveradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._netlongwaveradiation_length_0):
                self.netlongwaveradiation[jdx0] = self._netlongwaveradiation_ncarray[k]
                k += 1
        elif self._netlongwaveradiation_ramflag:
            for jdx0 in range(self._netlongwaveradiation_length_0):
                self.netlongwaveradiation[jdx0] = self._netlongwaveradiation_array[idx, jdx0]
        if self._netradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._netradiation_length_0):
                self.netradiation[jdx0] = self._netradiation_ncarray[k]
                k += 1
        elif self._netradiation_ramflag:
            for jdx0 in range(self._netradiation_length_0):
                self.netradiation[jdx0] = self._netradiation_array[idx, jdx0]
        if self._soilheatflux_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilheatflux_length_0):
                self.soilheatflux[jdx0] = self._soilheatflux_ncarray[k]
                k += 1
        elif self._soilheatflux_ramflag:
            for jdx0 in range(self._soilheatflux_length_0):
                self.soilheatflux[jdx0] = self._soilheatflux_array[idx, jdx0]
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
        if self._clearskysolarradiation_diskflag_writing:
            self._clearskysolarradiation_ncarray[0] = self.clearskysolarradiation
        if self._clearskysolarradiation_ramflag:
            self._clearskysolarradiation_array[idx] = self.clearskysolarradiation
        if self._netshortwaveradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self._netshortwaveradiation_ncarray[k] = self.netshortwaveradiation[jdx0]
                k += 1
        if self._netshortwaveradiation_ramflag:
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self._netshortwaveradiation_array[idx, jdx0] = self.netshortwaveradiation[jdx0]
        if self._netlongwaveradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._netlongwaveradiation_length_0):
                self._netlongwaveradiation_ncarray[k] = self.netlongwaveradiation[jdx0]
                k += 1
        if self._netlongwaveradiation_ramflag:
            for jdx0 in range(self._netlongwaveradiation_length_0):
                self._netlongwaveradiation_array[idx, jdx0] = self.netlongwaveradiation[jdx0]
        if self._netradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._netradiation_length_0):
                self._netradiation_ncarray[k] = self.netradiation[jdx0]
                k += 1
        if self._netradiation_ramflag:
            for jdx0 in range(self._netradiation_length_0):
                self._netradiation_array[idx, jdx0] = self.netradiation[jdx0]
        if self._soilheatflux_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilheatflux_length_0):
                self._soilheatflux_ncarray[k] = self.soilheatflux[jdx0]
                k += 1
        if self._soilheatflux_ramflag:
            for jdx0 in range(self._soilheatflux_length_0):
                self._soilheatflux_array[idx, jdx0] = self.soilheatflux[jdx0]
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
        if name == "clearskysolarradiation":
            self._clearskysolarradiation_outputpointer = value.p_value
        if name == "meanreferenceevapotranspiration":
            self._meanreferenceevapotranspiration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._clearskysolarradiation_outputflag:
            self._clearskysolarradiation_outputpointer[0] = self.clearskysolarradiation
        if self._meanreferenceevapotranspiration_outputflag:
            self._meanreferenceevapotranspiration_outputpointer[0] = self.meanreferenceevapotranspiration
@cython.final
cdef class LogSequences:
    pass
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
        self.sequences.inputs.load_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.load_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
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
        self.calc_clearskysolarradiation_v1()
        self.calc_globalradiation_v1()
        self.calc_windspeed2m_v1()
        self.calc_airtemperature_v1()
        self.calc_saturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.update_loggedclearskysolarradiation_v1()
        self.update_loggedglobalradiation_v1()
        self.calc_netshortwaveradiation_v1()
        self.calc_netlongwaveradiation_v1()
        self.calc_netradiation_v1()
        self.calc_soilheatflux_v1()
        self.calc_psychrometricconstant_v1()
        self.calc_referenceevapotranspiration_v1()
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
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outputs()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outputs()
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.clearskysolarradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_clearskysolarradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.clearskysolarradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_clearskysolarradiation()
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 2:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_windspeed2m_v1(self) noexcept nogil:
        cdef double z0
        cdef double d
        d = 2.0 / 3.0 * 0.12
        z0 = 0.123 * 0.12
        self.sequences.factors.windspeed2m = self.sequences.inputs.windspeed * (            log((2.0 - d) / z0)            / log((self.parameters.control.measuringheightwindspeed - d) / z0)        )
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_airtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_airtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressure[k] = 6.108 * exp(                17.27 * self.sequences.factors.airtemperature[k] / (self.sequences.factors.airtemperature[k] + 237.3)            )
    cpdef inline void calc_saturationvapourpressureslope_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressureslope[k] = (                4098.0                * self.sequences.factors.saturationvapourpressure[k]                / (self.sequences.factors.airtemperature[k] + 237.3) ** 2            )
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.actualvapourpressure[k] = (                self.sequences.factors.saturationvapourpressure[k] * self.sequences.inputs.relativehumidity / 100.0            )
    cpdef inline void update_loggedclearskysolarradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedclearskysolarradiation[idx] = self.sequences.logs.loggedclearskysolarradiation[                idx - 1            ]
        self.sequences.logs.loggedclearskysolarradiation[0] = self.sequences.fluxes.clearskysolarradiation
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_netshortwaveradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double netshortwaveradiation
        netshortwaveradiation = (1.0 - 0.23) * self.sequences.fluxes.globalradiation
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = netshortwaveradiation
    cpdef inline void calc_netlongwaveradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        cdef double clearskysolarradiation
        cdef double globalradiation
        if self.sequences.fluxes.clearskysolarradiation > 0.0:
            globalradiation = self.sequences.fluxes.globalradiation
            clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation
        else:
            globalradiation = 0.0
            clearskysolarradiation = 0.0
            for idx in range(self.parameters.derived.nmblogentries):
                clearskysolarradiation = clearskysolarradiation + (self.sequences.logs.loggedclearskysolarradiation[idx])
                globalradiation = globalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netlongwaveradiation[k] = (                5.674768518518519e-08                * (self.sequences.factors.airtemperature[k] + 273.16) ** 4                * (0.34 - 0.14 * (self.sequences.factors.actualvapourpressure[k] / 10.0) ** 0.5)                * (1.35 * min(globalradiation / clearskysolarradiation, 1.0) - 0.35)            )
    cpdef inline void calc_netradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.netlongwaveradiation[k]            )
    cpdef inline void calc_soilheatflux_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.parameters.derived.days < 1.0:
            for k in range(self.parameters.control.nmbhru):
                if self.sequences.fluxes.netradiation[k] >= 0.0:
                    self.sequences.fluxes.soilheatflux[k] = 0.1 * self.sequences.fluxes.netradiation[k]
                else:
                    self.sequences.fluxes.soilheatflux[k] = 0.5 * self.sequences.fluxes.netradiation[k]
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.soilheatflux[k] = 0.0
    cpdef inline void calc_psychrometricconstant_v1(self) noexcept nogil:
        self.sequences.factors.psychrometricconstant = 6.65e-4 * self.sequences.inputs.atmosphericpressure
    cpdef inline void calc_referenceevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                0.0352512                * self.parameters.derived.days                * self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (self.sequences.factors.psychrometricconstant * 3.75 * self.parameters.derived.hours)                / (self.sequences.factors.airtemperature[k] + 273.0)                * self.sequences.factors.windspeed2m                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])            ) / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.sequences.factors.psychrometricconstant * (1.0 + 0.34 * self.sequences.factors.windspeed2m)            )
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
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.clearskysolarradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_clearskysolarradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.clearskysolarradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_clearskysolarradiation()
    cpdef inline void calc_globalradiation(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 2:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 3:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_windspeed2m(self) noexcept nogil:
        cdef double z0
        cdef double d
        d = 2.0 / 3.0 * 0.12
        z0 = 0.123 * 0.12
        self.sequences.factors.windspeed2m = self.sequences.inputs.windspeed * (            log((2.0 - d) / z0)            / log((self.parameters.control.measuringheightwindspeed - d) / z0)        )
    cpdef inline void calc_airtemperature(self) noexcept nogil:
        if self.tempmodel_typeid == 1:
            self.calc_airtemperature_tempmodel_v1(                (<masterinterface.MasterInterface>self.tempmodel)            )
        elif self.tempmodel_typeid == 2:
            self.calc_airtemperature_tempmodel_v2(                (<masterinterface.MasterInterface>self.tempmodel)            )
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressure[k] = 6.108 * exp(                17.27 * self.sequences.factors.airtemperature[k] / (self.sequences.factors.airtemperature[k] + 237.3)            )
    cpdef inline void calc_saturationvapourpressureslope(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressureslope[k] = (                4098.0                * self.sequences.factors.saturationvapourpressure[k]                / (self.sequences.factors.airtemperature[k] + 237.3) ** 2            )
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.actualvapourpressure[k] = (                self.sequences.factors.saturationvapourpressure[k] * self.sequences.inputs.relativehumidity / 100.0            )
    cpdef inline void update_loggedclearskysolarradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedclearskysolarradiation[idx] = self.sequences.logs.loggedclearskysolarradiation[                idx - 1            ]
        self.sequences.logs.loggedclearskysolarradiation[0] = self.sequences.fluxes.clearskysolarradiation
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_netshortwaveradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double netshortwaveradiation
        netshortwaveradiation = (1.0 - 0.23) * self.sequences.fluxes.globalradiation
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = netshortwaveradiation
    cpdef inline void calc_netlongwaveradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        cdef double clearskysolarradiation
        cdef double globalradiation
        if self.sequences.fluxes.clearskysolarradiation > 0.0:
            globalradiation = self.sequences.fluxes.globalradiation
            clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation
        else:
            globalradiation = 0.0
            clearskysolarradiation = 0.0
            for idx in range(self.parameters.derived.nmblogentries):
                clearskysolarradiation = clearskysolarradiation + (self.sequences.logs.loggedclearskysolarradiation[idx])
                globalradiation = globalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netlongwaveradiation[k] = (                5.674768518518519e-08                * (self.sequences.factors.airtemperature[k] + 273.16) ** 4                * (0.34 - 0.14 * (self.sequences.factors.actualvapourpressure[k] / 10.0) ** 0.5)                * (1.35 * min(globalradiation / clearskysolarradiation, 1.0) - 0.35)            )
    cpdef inline void calc_netradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.netlongwaveradiation[k]            )
    cpdef inline void calc_soilheatflux(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.parameters.derived.days < 1.0:
            for k in range(self.parameters.control.nmbhru):
                if self.sequences.fluxes.netradiation[k] >= 0.0:
                    self.sequences.fluxes.soilheatflux[k] = 0.1 * self.sequences.fluxes.netradiation[k]
                else:
                    self.sequences.fluxes.soilheatflux[k] = 0.5 * self.sequences.fluxes.netradiation[k]
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.soilheatflux[k] = 0.0
    cpdef inline void calc_psychrometricconstant(self) noexcept nogil:
        self.sequences.factors.psychrometricconstant = 6.65e-4 * self.sequences.inputs.atmosphericpressure
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.referenceevapotranspiration[k] = (                0.0352512                * self.parameters.derived.days                * self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (self.sequences.factors.psychrometricconstant * 3.75 * self.parameters.derived.hours)                / (self.sequences.factors.airtemperature[k] + 273.0)                * self.sequences.factors.windspeed2m                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])            ) / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.sequences.factors.psychrometricconstant * (1.0 + 0.34 * self.sequences.factors.windspeed2m)            )
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
