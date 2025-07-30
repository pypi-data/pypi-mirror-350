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
cdef class FixedParameters:
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
        if self._windspeed10m_diskflag_reading:
            self.windspeed10m = self._windspeed10m_ncarray[0]
        elif self._windspeed10m_ramflag:
            self.windspeed10m = self._windspeed10m_array[idx]
        if self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
        if self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
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
        if self._dryairpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._dryairpressure_length_0):
                self.dryairpressure[jdx0] = self._dryairpressure_ncarray[k]
                k += 1
        elif self._dryairpressure_ramflag:
            for jdx0 in range(self._dryairpressure_length_0):
                self.dryairpressure[jdx0] = self._dryairpressure_array[idx, jdx0]
        if self._airdensity_diskflag_reading:
            k = 0
            for jdx0 in range(self._airdensity_length_0):
                self.airdensity[jdx0] = self._airdensity_ncarray[k]
                k += 1
        elif self._airdensity_ramflag:
            for jdx0 in range(self._airdensity_length_0):
                self.airdensity[jdx0] = self._airdensity_array[idx, jdx0]
        if self._currentalbedo_diskflag_reading:
            k = 0
            for jdx0 in range(self._currentalbedo_length_0):
                self.currentalbedo[jdx0] = self._currentalbedo_ncarray[k]
                k += 1
        elif self._currentalbedo_ramflag:
            for jdx0 in range(self._currentalbedo_length_0):
                self.currentalbedo[jdx0] = self._currentalbedo_array[idx, jdx0]
        if self._adjustedcloudcoverage_diskflag_reading:
            self.adjustedcloudcoverage = self._adjustedcloudcoverage_ncarray[0]
        elif self._adjustedcloudcoverage_ramflag:
            self.adjustedcloudcoverage = self._adjustedcloudcoverage_array[idx]
        if self._aerodynamicresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self.aerodynamicresistance[jdx0] = self._aerodynamicresistance_ncarray[k]
                k += 1
        elif self._aerodynamicresistance_ramflag:
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self.aerodynamicresistance[jdx0] = self._aerodynamicresistance_array[idx, jdx0]
        if self._actualsurfaceresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self.actualsurfaceresistance[jdx0] = self._actualsurfaceresistance_ncarray[k]
                k += 1
        elif self._actualsurfaceresistance_ramflag:
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self.actualsurfaceresistance[jdx0] = self._actualsurfaceresistance_array[idx, jdx0]
        if self._snowcover_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowcover_length_0):
                self.snowcover[jdx0] = self._snowcover_ncarray[k]
                k += 1
        elif self._snowcover_ramflag:
            for jdx0 in range(self._snowcover_length_0):
                self.snowcover[jdx0] = self._snowcover_array[idx, jdx0]
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
        if self._windspeed10m_diskflag_writing:
            self._windspeed10m_ncarray[0] = self.windspeed10m
        if self._windspeed10m_ramflag:
            self._windspeed10m_array[idx] = self.windspeed10m
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
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
        if self._dryairpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._dryairpressure_length_0):
                self._dryairpressure_ncarray[k] = self.dryairpressure[jdx0]
                k += 1
        if self._dryairpressure_ramflag:
            for jdx0 in range(self._dryairpressure_length_0):
                self._dryairpressure_array[idx, jdx0] = self.dryairpressure[jdx0]
        if self._airdensity_diskflag_writing:
            k = 0
            for jdx0 in range(self._airdensity_length_0):
                self._airdensity_ncarray[k] = self.airdensity[jdx0]
                k += 1
        if self._airdensity_ramflag:
            for jdx0 in range(self._airdensity_length_0):
                self._airdensity_array[idx, jdx0] = self.airdensity[jdx0]
        if self._currentalbedo_diskflag_writing:
            k = 0
            for jdx0 in range(self._currentalbedo_length_0):
                self._currentalbedo_ncarray[k] = self.currentalbedo[jdx0]
                k += 1
        if self._currentalbedo_ramflag:
            for jdx0 in range(self._currentalbedo_length_0):
                self._currentalbedo_array[idx, jdx0] = self.currentalbedo[jdx0]
        if self._adjustedcloudcoverage_diskflag_writing:
            self._adjustedcloudcoverage_ncarray[0] = self.adjustedcloudcoverage
        if self._adjustedcloudcoverage_ramflag:
            self._adjustedcloudcoverage_array[idx] = self.adjustedcloudcoverage
        if self._aerodynamicresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self._aerodynamicresistance_ncarray[k] = self.aerodynamicresistance[jdx0]
                k += 1
        if self._aerodynamicresistance_ramflag:
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self._aerodynamicresistance_array[idx, jdx0] = self.aerodynamicresistance[jdx0]
        if self._actualsurfaceresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self._actualsurfaceresistance_ncarray[k] = self.actualsurfaceresistance[jdx0]
                k += 1
        if self._actualsurfaceresistance_ramflag:
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self._actualsurfaceresistance_array[idx, jdx0] = self.actualsurfaceresistance[jdx0]
        if self._snowcover_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowcover_length_0):
                self._snowcover_ncarray[k] = self.snowcover[jdx0]
                k += 1
        if self._snowcover_ramflag:
            for jdx0 in range(self._snowcover_length_0):
                self._snowcover_array[idx, jdx0] = self.snowcover[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "windspeed10m":
            self._windspeed10m_outputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_outputpointer = value.p_value
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "adjustedcloudcoverage":
            self._adjustedcloudcoverage_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._windspeed10m_outputflag:
            self._windspeed10m_outputpointer[0] = self.windspeed10m
        if self._sunshineduration_outputflag:
            self._sunshineduration_outputpointer[0] = self.sunshineduration
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._adjustedcloudcoverage_outputflag:
            self._adjustedcloudcoverage_outputpointer[0] = self.adjustedcloudcoverage
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
        if self._dailyprecipitation_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailyprecipitation_length_0):
                self.dailyprecipitation[jdx0] = self._dailyprecipitation_ncarray[k]
                k += 1
        elif self._dailyprecipitation_ramflag:
            for jdx0 in range(self._dailyprecipitation_length_0):
                self.dailyprecipitation[jdx0] = self._dailyprecipitation_array[idx, jdx0]
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
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
        if self._dailypotentialsoilevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailypotentialsoilevapotranspiration_length_0):
                self.dailypotentialsoilevapotranspiration[jdx0] = self._dailypotentialsoilevapotranspiration_ncarray[k]
                k += 1
        elif self._dailypotentialsoilevapotranspiration_ramflag:
            for jdx0 in range(self._dailypotentialsoilevapotranspiration_length_0):
                self.dailypotentialsoilevapotranspiration[jdx0] = self._dailypotentialsoilevapotranspiration_array[idx, jdx0]
        if self._waterevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterevaporation_length_0):
                self.waterevaporation[jdx0] = self._waterevaporation_ncarray[k]
                k += 1
        elif self._waterevaporation_ramflag:
            for jdx0 in range(self._waterevaporation_length_0):
                self.waterevaporation[jdx0] = self._waterevaporation_array[idx, jdx0]
        if self._dailywaterevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailywaterevaporation_length_0):
                self.dailywaterevaporation[jdx0] = self._dailywaterevaporation_ncarray[k]
                k += 1
        elif self._dailywaterevaporation_ramflag:
            for jdx0 in range(self._dailywaterevaporation_length_0):
                self.dailywaterevaporation[jdx0] = self._dailywaterevaporation_array[idx, jdx0]
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
        if self._dailyprecipitation_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailyprecipitation_length_0):
                self._dailyprecipitation_ncarray[k] = self.dailyprecipitation[jdx0]
                k += 1
        if self._dailyprecipitation_ramflag:
            for jdx0 in range(self._dailyprecipitation_length_0):
                self._dailyprecipitation_array[idx, jdx0] = self.dailyprecipitation[jdx0]
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
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
        if self._dailypotentialsoilevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailypotentialsoilevapotranspiration_length_0):
                self._dailypotentialsoilevapotranspiration_ncarray[k] = self.dailypotentialsoilevapotranspiration[jdx0]
                k += 1
        if self._dailypotentialsoilevapotranspiration_ramflag:
            for jdx0 in range(self._dailypotentialsoilevapotranspiration_length_0):
                self._dailypotentialsoilevapotranspiration_array[idx, jdx0] = self.dailypotentialsoilevapotranspiration[jdx0]
        if self._waterevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterevaporation_length_0):
                self._waterevaporation_ncarray[k] = self.waterevaporation[jdx0]
                k += 1
        if self._waterevaporation_ramflag:
            for jdx0 in range(self._waterevaporation_length_0):
                self._waterevaporation_array[idx, jdx0] = self.waterevaporation[jdx0]
        if self._dailywaterevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailywaterevaporation_length_0):
                self._dailywaterevaporation_ncarray[k] = self.dailywaterevaporation[jdx0]
                k += 1
        if self._dailywaterevaporation_ramflag:
            for jdx0 in range(self._dailywaterevaporation_length_0):
                self._dailywaterevaporation_array[idx, jdx0] = self.dailywaterevaporation[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._cloudcoverage_diskflag_reading:
            self.cloudcoverage = self._cloudcoverage_ncarray[0]
        elif self._cloudcoverage_ramflag:
            self.cloudcoverage = self._cloudcoverage_array[idx]
        if self._soilresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilresistance_length_0):
                self.soilresistance[jdx0] = self._soilresistance_ncarray[k]
                k += 1
        elif self._soilresistance_ramflag:
            for jdx0 in range(self._soilresistance_length_0):
                self.soilresistance[jdx0] = self._soilresistance_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._cloudcoverage_diskflag_writing:
            self._cloudcoverage_ncarray[0] = self.cloudcoverage
        if self._cloudcoverage_ramflag:
            self._cloudcoverage_array[idx] = self.cloudcoverage
        if self._soilresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilresistance_length_0):
                self._soilresistance_ncarray[k] = self.soilresistance[jdx0]
                k += 1
        if self._soilresistance_ramflag:
            for jdx0 in range(self._soilresistance_length_0):
                self._soilresistance_array[idx, jdx0] = self.soilresistance[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "cloudcoverage":
            self._cloudcoverage_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._cloudcoverage_outputflag:
            self._cloudcoverage_outputpointer[0] = self.cloudcoverage
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.precipmodel = None
        self.precipmodel_is_mainmodel = False
        self.radiationmodel = None
        self.radiationmodel_is_mainmodel = False
        self.snowcovermodel = None
        self.snowcovermodel_is_mainmodel = False
        self.tempmodel = None
        self.tempmodel_is_mainmodel = False
    def get_precipmodel(self) -> masterinterface.MasterInterface | None:
        return self.precipmodel
    def set_precipmodel(self, precipmodel: masterinterface.MasterInterface | None) -> None:
        self.precipmodel = precipmodel
    def get_radiationmodel(self) -> masterinterface.MasterInterface | None:
        return self.radiationmodel
    def set_radiationmodel(self, radiationmodel: masterinterface.MasterInterface | None) -> None:
        self.radiationmodel = radiationmodel
    def get_snowcovermodel(self) -> masterinterface.MasterInterface | None:
        return self.snowcovermodel
    def set_snowcovermodel(self, snowcovermodel: masterinterface.MasterInterface | None) -> None:
        self.snowcovermodel = snowcovermodel
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
        self.new2old()
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
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.reset_reuseflags()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.reset_reuseflags()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.load_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.load_data(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.load_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.save_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.save_data(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.save_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        self.sequences.old_states.cloudcoverage = self.sequences.new_states.cloudcoverage
        for jdx0 in range(self.sequences.states._soilresistance_length_0):
            self.sequences.old_states.soilresistance[jdx0] = self.sequences.new_states.soilresistance[jdx0]
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.new2old()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.new2old()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.new2old()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.determine_potentialinterceptionevaporation_v1()
        self.determine_potentialsoilevapotranspiration_v1()
        self.determine_potentialwaterevaporation_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_inlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_inlets()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_inlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outlets()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_outlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_receivers(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_receivers(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_receivers(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_senders(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_senders(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_senders(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outputs()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outputs()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_outputs()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outputs()
    cpdef double get_potentialwaterevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.parameters.derived.days * self.sequences.fluxes.dailywaterevaporation[k]
    cpdef double get_potentialinterceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialinterceptionevaporation[k]
    cpdef double get_potentialsoilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialsoilevapotranspiration[k]
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
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
    cpdef inline double return_adjustedwindspeed_v1(self, double h) noexcept nogil:
        if h == self.parameters.control.measuringheightwindspeed:
            return self.sequences.inputs.windspeed
        return self.sequences.inputs.windspeed * (            log(h / self.parameters.fixed.roughnesslengthgrass)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.roughnesslengthgrass)        )
    cpdef inline void calc_windspeed10m_v1(self) noexcept nogil:
        self.sequences.factors.windspeed10m = self.return_adjustedwindspeed_v1(10.0)
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
    cpdef inline void calc_dryairpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dryairpressure[k] = (                self.sequences.inputs.atmosphericpressure - self.sequences.factors.actualvapourpressure[k]            )
    cpdef inline void calc_airdensity_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airdensity[k] = (100.0 / (self.sequences.factors.airtemperature[k] + 273.15)) * (                self.sequences.factors.dryairpressure[k] / self.parameters.fixed.gasconstantdryair                + self.sequences.factors.actualvapourpressure[k] / self.parameters.fixed.gasconstantwatervapour            )
    cpdef inline void calc_currentalbedo_v2(self) noexcept nogil:
        cdef double lai
        cdef double a_l
        cdef double a_g
        cdef double wetness
        cdef double a_s
        cdef double w
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            w = self.sequences.factors.snowcover[k]
            a_s = self.parameters.control.groundalbedo[k]
            if self.parameters.control.soil[k]:
                wetness = self.sequences.fluxes.dailyprecipitation[k] / self.parameters.control.wetnessthreshold[k]
                if wetness >= self.sequences.fluxes.dailypotentialsoilevapotranspiration[k]:
                    a_s = a_s / (2.0)
            a_g = w * self.parameters.control.groundalbedosnow[k] + (1.0 - w) * a_s
            a_l = w * self.parameters.control.leafalbedosnow[k] + (1.0 - w) * self.parameters.control.leafalbedo[k]
            if self.parameters.control.plant[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                if lai < 4.0:
                    self.sequences.factors.currentalbedo[k] = a_g + 0.25 * (a_l - a_g) * lai
                else:
                    self.sequences.factors.currentalbedo[k] = a_l
            else:
                self.sequences.factors.currentalbedo[k] = a_g
    cpdef inline void calc_netshortwaveradiation_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = self.sequences.fluxes.globalradiation * (                1.0 - self.sequences.factors.currentalbedo[k]            )
    cpdef inline void update_cloudcoverage_v1(self) noexcept nogil:
        cdef double p0
        p0 = self.sequences.factors.possiblesunshineduration
        if (self.parameters.derived.days >= 1.0) or (p0 >= self.parameters.derived.hours):
            self.sequences.states.cloudcoverage = min(self.sequences.factors.sunshineduration / p0, 1.0)
    cpdef inline void calc_adjustedcloudcoverage_v1(self) noexcept nogil:
        cdef double n
        cdef double c
        cdef double w
        w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
        c = self.sequences.states.cloudcoverage
        n = self.parameters.control.nightcloudfactor
        self.sequences.factors.adjustedcloudcoverage = w * c + (1.0 - w) * min(n * c, 1.0)
    cpdef inline void calc_netlongwaveradiation_v2(self) noexcept nogil:
        cdef double ra
        cdef double rs
        cdef double a
        cdef double t
        cdef numpy.int64_t k
        cdef double f
        cdef double g
        cdef double s
        s = self.parameters.fixed.stefanboltzmannconstant
        g = self.sequences.fluxes.globalradiation
        f = 1.0 + self.parameters.control.cloudtypefactor * self.sequences.factors.adjustedcloudcoverage**2.0
        for k in range(self.parameters.control.nmbhru):
            t = self.sequences.factors.airtemperature[k]
            a = self.sequences.factors.currentalbedo[k]
            rs = 0.97 * s * (t + 273.1) ** 4.0 + 0.07 * (1.0 - a) * g
            ra = f * (                (1.0 - 0.261 * exp(-0.000777 * t**2.0))                * (s * (t + 273.1) ** 4.0)            )
            self.sequences.fluxes.netlongwaveradiation[k] = rs - ra
    cpdef inline void calc_netradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.netlongwaveradiation[k]            )
    cpdef inline void calc_aerodynamicresistance_v2(self) noexcept nogil:
        cdef double f
        cdef numpy.int64_t k
        if self.sequences.factors.windspeed10m > 0.0:
            for k in range(self.parameters.control.nmbhru):
                f = self.parameters.derived.aerodynamicresistancefactor[                    self.parameters.control.hrutype[k] - self.parameters.derived._aerodynamicresistancefactor_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.derived._aerodynamicresistancefactor_columnmin,                ]
                self.sequences.factors.aerodynamicresistance[k] = f / self.sequences.factors.windspeed10m
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.aerodynamicresistance[k] = inf
    cpdef inline void calc_dailyprecipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailyprecipitation[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailyprecipitation[k] = self.sequences.fluxes.dailyprecipitation[k] + (self.sequences.logs.loggedprecipitation[idx, k])
    cpdef inline void calc_dailypotentialsoilevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailypotentialsoilevapotranspiration[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailypotentialsoilevapotranspiration[                    k                ] = self.sequences.fluxes.dailypotentialsoilevapotranspiration[                    k                ] + (self.sequences.logs.loggedpotentialsoilevapotranspiration[idx, k])
    cpdef inline void update_soilresistance_v1(self) noexcept nogil:
        cdef double wetness
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                wetness = self.sequences.fluxes.dailyprecipitation[k] / self.parameters.control.wetnessthreshold[k]
                if wetness < self.sequences.fluxes.dailypotentialsoilevapotranspiration[k]:
                    self.sequences.states.soilresistance[k] = self.sequences.states.soilresistance[k] + (self.parameters.control.soilresistanceincrease[k])
                else:
                    self.sequences.states.soilresistance[k] = self.parameters.control.wetsoilresistance[k]
            else:
                self.sequences.states.soilresistance[k] = nan
    cpdef inline void calc_actualsurfaceresistance_v2(self) noexcept nogil:
        cdef double w_day
        cdef double r_night_inv
        cdef double r_leaf_night
        cdef double r_day_inv
        cdef double r_leaf_day
        cdef double r_soil
        cdef double w_soil
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.plant[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                w_soil = (0.8 if lai < 1.0 else 0.7) ** lai
                r_soil = self.sequences.states.soilresistance[k]
                r_leaf_day = self.parameters.control.leafresistance[k]
                r_day_inv = w_soil / r_soil + (1.0 - w_soil) / r_leaf_day
                r_leaf_night = 2800.0
                r_night_inv = 1.0 / r_soil + lai / r_leaf_night
                w_day = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
                self.sequences.factors.actualsurfaceresistance[k] = 1.0 / (                    w_day * r_day_inv + (1.0 - w_day) * r_night_inv                )
            elif self.parameters.control.soil[k]:
                self.sequences.factors.actualsurfaceresistance[k] = self.sequences.states.soilresistance[k]
            else:
                self.sequences.factors.actualsurfaceresistance[k] = 0.0
    cpdef inline void calc_potentialsoilevapotranspiration_v1(self) noexcept nogil:
        cdef double pet
        cdef double r
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                r = self.sequences.factors.actualsurfaceresistance[k]
                pet = self.return_evaporation_penmanmonteith_v2(k, r)
                self.sequences.fluxes.potentialsoilevapotranspiration[k] = pet
            else:
                self.sequences.fluxes.potentialsoilevapotranspiration[k] = 0.0
    cpdef inline double return_evaporation_penmanmonteith_v2(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil:
        cdef double ar
        ar = min(max(self.sequences.factors.aerodynamicresistance[k], 1e-6), 1e6)
        return (            (                self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (self.sequences.factors.airdensity[k] * self.parameters.fixed.heatcapacityair)                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])                / ar            )            / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.parameters.fixed.psychrometricconstant * (1.0 + actualsurfaceresistance / ar)            )        ) / self.parameters.fixed.heatofcondensation
    cpdef inline void calc_snowcover_v1(self) noexcept nogil:
        if self.snowcovermodel_typeid == 1:
            self.calc_snowcover_snowcovermodel_v1(                (<masterinterface.MasterInterface>self.snowcovermodel)            )
    cpdef inline void calc_soilheatflux_v4(self) noexcept nogil:
        cdef double lai
        cdef numpy.int64_t k
        cdef double b
        cdef double a
        cdef double w
        w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
        a = w * 0.2 + (1.0 - w) * 0.5
        b = a * 0.03 / 0.2
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.soilheatflux[k] = 0.0
            else:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                self.sequences.fluxes.soilheatflux[k] = max(a - b * lai, 0.0) * self.sequences.fluxes.netradiation[k]
    cpdef inline void calc_waterevaporation_v4(self) noexcept nogil:
        cdef double evap
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                evap = self.return_evaporation_penmanmonteith_v2(k, 0.0)
                self.sequences.fluxes.waterevaporation[k] = evap
            else:
                self.sequences.fluxes.waterevaporation[k] = 0.0
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airtemperature[k] = submodel.get_temperature(k)
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_temperature()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airtemperature[k] = submodel.get_temperature(k)
    cpdef inline void calc_snowcover_snowcovermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowcover[k] = submodel.get_snowcover(k)
    cpdef inline void calc_potentialinterceptionevaporation_v2(self) noexcept nogil:
        cdef double evap
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                evap = self.return_evaporation_penmanmonteith_v2(k, 0.0)
                self.sequences.fluxes.potentialinterceptionevaporation[k] = evap
            else:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = 0.0
    cpdef inline void calc_precipitation_precipmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = submodel.get_precipitation(k)
    cpdef inline void calc_precipitation_precipmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_precipitation()
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = submodel.get_precipitation(k)
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        if self.precipmodel_typeid == 1:
            self.calc_precipitation_precipmodel_v1(                (<masterinterface.MasterInterface>self.precipmodel)            )
        elif self.precipmodel_typeid == 2:
            self.calc_precipitation_precipmodel_v2(                (<masterinterface.MasterInterface>self.precipmodel)            )
    cpdef inline void update_loggedprecipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedprecipitation[idx, k] = self.sequences.logs.loggedprecipitation[idx - 1, k]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedprecipitation[0, k] = self.sequences.fluxes.precipitation[k]
    cpdef inline void update_loggedpotentialsoilevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedpotentialsoilevapotranspiration[idx, k] = (                    self.sequences.logs.loggedpotentialsoilevapotranspiration[idx - 1, k]                )
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedpotentialsoilevapotranspiration[0, k] = (                self.sequences.fluxes.potentialsoilevapotranspiration[k]            )
    cpdef inline void update_loggedwaterevaporation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedwaterevaporation[idx, k] = self.sequences.logs.loggedwaterevaporation[                    idx - 1, k                ]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedwaterevaporation[0, k] = self.sequences.fluxes.waterevaporation[k]
    cpdef inline void calc_dailywaterevaporation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailywaterevaporation[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailywaterevaporation[k] = self.sequences.fluxes.dailywaterevaporation[k] + (self.sequences.logs.loggedwaterevaporation[idx, k])
    cpdef double get_potentialwaterevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.parameters.derived.days * self.sequences.fluxes.dailywaterevaporation[k]
    cpdef double get_potentialinterceptionevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialinterceptionevaporation[k]
    cpdef double get_potentialsoilevapotranspiration(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.potentialsoilevapotranspiration[k]
    cpdef inline void process_radiationmodel(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
    cpdef inline void calc_sunshineduration(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
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
    cpdef inline double return_adjustedwindspeed(self, double h) noexcept nogil:
        if h == self.parameters.control.measuringheightwindspeed:
            return self.sequences.inputs.windspeed
        return self.sequences.inputs.windspeed * (            log(h / self.parameters.fixed.roughnesslengthgrass)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.roughnesslengthgrass)        )
    cpdef inline void calc_windspeed10m(self) noexcept nogil:
        self.sequences.factors.windspeed10m = self.return_adjustedwindspeed_v1(10.0)
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
    cpdef inline void calc_dryairpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dryairpressure[k] = (                self.sequences.inputs.atmosphericpressure - self.sequences.factors.actualvapourpressure[k]            )
    cpdef inline void calc_airdensity(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.airdensity[k] = (100.0 / (self.sequences.factors.airtemperature[k] + 273.15)) * (                self.sequences.factors.dryairpressure[k] / self.parameters.fixed.gasconstantdryair                + self.sequences.factors.actualvapourpressure[k] / self.parameters.fixed.gasconstantwatervapour            )
    cpdef inline void calc_currentalbedo(self) noexcept nogil:
        cdef double lai
        cdef double a_l
        cdef double a_g
        cdef double wetness
        cdef double a_s
        cdef double w
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            w = self.sequences.factors.snowcover[k]
            a_s = self.parameters.control.groundalbedo[k]
            if self.parameters.control.soil[k]:
                wetness = self.sequences.fluxes.dailyprecipitation[k] / self.parameters.control.wetnessthreshold[k]
                if wetness >= self.sequences.fluxes.dailypotentialsoilevapotranspiration[k]:
                    a_s = a_s / (2.0)
            a_g = w * self.parameters.control.groundalbedosnow[k] + (1.0 - w) * a_s
            a_l = w * self.parameters.control.leafalbedosnow[k] + (1.0 - w) * self.parameters.control.leafalbedo[k]
            if self.parameters.control.plant[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                if lai < 4.0:
                    self.sequences.factors.currentalbedo[k] = a_g + 0.25 * (a_l - a_g) * lai
                else:
                    self.sequences.factors.currentalbedo[k] = a_l
            else:
                self.sequences.factors.currentalbedo[k] = a_g
    cpdef inline void calc_netshortwaveradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = self.sequences.fluxes.globalradiation * (                1.0 - self.sequences.factors.currentalbedo[k]            )
    cpdef inline void update_cloudcoverage(self) noexcept nogil:
        cdef double p0
        p0 = self.sequences.factors.possiblesunshineduration
        if (self.parameters.derived.days >= 1.0) or (p0 >= self.parameters.derived.hours):
            self.sequences.states.cloudcoverage = min(self.sequences.factors.sunshineduration / p0, 1.0)
    cpdef inline void calc_adjustedcloudcoverage(self) noexcept nogil:
        cdef double n
        cdef double c
        cdef double w
        w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
        c = self.sequences.states.cloudcoverage
        n = self.parameters.control.nightcloudfactor
        self.sequences.factors.adjustedcloudcoverage = w * c + (1.0 - w) * min(n * c, 1.0)
    cpdef inline void calc_netlongwaveradiation(self) noexcept nogil:
        cdef double ra
        cdef double rs
        cdef double a
        cdef double t
        cdef numpy.int64_t k
        cdef double f
        cdef double g
        cdef double s
        s = self.parameters.fixed.stefanboltzmannconstant
        g = self.sequences.fluxes.globalradiation
        f = 1.0 + self.parameters.control.cloudtypefactor * self.sequences.factors.adjustedcloudcoverage**2.0
        for k in range(self.parameters.control.nmbhru):
            t = self.sequences.factors.airtemperature[k]
            a = self.sequences.factors.currentalbedo[k]
            rs = 0.97 * s * (t + 273.1) ** 4.0 + 0.07 * (1.0 - a) * g
            ra = f * (                (1.0 - 0.261 * exp(-0.000777 * t**2.0))                * (s * (t + 273.1) ** 4.0)            )
            self.sequences.fluxes.netlongwaveradiation[k] = rs - ra
    cpdef inline void calc_netradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.netlongwaveradiation[k]            )
    cpdef inline void calc_aerodynamicresistance(self) noexcept nogil:
        cdef double f
        cdef numpy.int64_t k
        if self.sequences.factors.windspeed10m > 0.0:
            for k in range(self.parameters.control.nmbhru):
                f = self.parameters.derived.aerodynamicresistancefactor[                    self.parameters.control.hrutype[k] - self.parameters.derived._aerodynamicresistancefactor_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.derived._aerodynamicresistancefactor_columnmin,                ]
                self.sequences.factors.aerodynamicresistance[k] = f / self.sequences.factors.windspeed10m
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.aerodynamicresistance[k] = inf
    cpdef inline void calc_dailyprecipitation(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailyprecipitation[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailyprecipitation[k] = self.sequences.fluxes.dailyprecipitation[k] + (self.sequences.logs.loggedprecipitation[idx, k])
    cpdef inline void calc_dailypotentialsoilevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailypotentialsoilevapotranspiration[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailypotentialsoilevapotranspiration[                    k                ] = self.sequences.fluxes.dailypotentialsoilevapotranspiration[                    k                ] + (self.sequences.logs.loggedpotentialsoilevapotranspiration[idx, k])
    cpdef inline void update_soilresistance(self) noexcept nogil:
        cdef double wetness
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                wetness = self.sequences.fluxes.dailyprecipitation[k] / self.parameters.control.wetnessthreshold[k]
                if wetness < self.sequences.fluxes.dailypotentialsoilevapotranspiration[k]:
                    self.sequences.states.soilresistance[k] = self.sequences.states.soilresistance[k] + (self.parameters.control.soilresistanceincrease[k])
                else:
                    self.sequences.states.soilresistance[k] = self.parameters.control.wetsoilresistance[k]
            else:
                self.sequences.states.soilresistance[k] = nan
    cpdef inline void calc_actualsurfaceresistance(self) noexcept nogil:
        cdef double w_day
        cdef double r_night_inv
        cdef double r_leaf_night
        cdef double r_day_inv
        cdef double r_leaf_day
        cdef double r_soil
        cdef double w_soil
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.plant[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                w_soil = (0.8 if lai < 1.0 else 0.7) ** lai
                r_soil = self.sequences.states.soilresistance[k]
                r_leaf_day = self.parameters.control.leafresistance[k]
                r_day_inv = w_soil / r_soil + (1.0 - w_soil) / r_leaf_day
                r_leaf_night = 2800.0
                r_night_inv = 1.0 / r_soil + lai / r_leaf_night
                w_day = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
                self.sequences.factors.actualsurfaceresistance[k] = 1.0 / (                    w_day * r_day_inv + (1.0 - w_day) * r_night_inv                )
            elif self.parameters.control.soil[k]:
                self.sequences.factors.actualsurfaceresistance[k] = self.sequences.states.soilresistance[k]
            else:
                self.sequences.factors.actualsurfaceresistance[k] = 0.0
    cpdef inline void calc_potentialsoilevapotranspiration(self) noexcept nogil:
        cdef double pet
        cdef double r
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                r = self.sequences.factors.actualsurfaceresistance[k]
                pet = self.return_evaporation_penmanmonteith_v2(k, r)
                self.sequences.fluxes.potentialsoilevapotranspiration[k] = pet
            else:
                self.sequences.fluxes.potentialsoilevapotranspiration[k] = 0.0
    cpdef inline double return_evaporation_penmanmonteith(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil:
        cdef double ar
        ar = min(max(self.sequences.factors.aerodynamicresistance[k], 1e-6), 1e6)
        return (            (                self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (self.sequences.factors.airdensity[k] * self.parameters.fixed.heatcapacityair)                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])                / ar            )            / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.parameters.fixed.psychrometricconstant * (1.0 + actualsurfaceresistance / ar)            )        ) / self.parameters.fixed.heatofcondensation
    cpdef inline void calc_snowcover(self) noexcept nogil:
        if self.snowcovermodel_typeid == 1:
            self.calc_snowcover_snowcovermodel_v1(                (<masterinterface.MasterInterface>self.snowcovermodel)            )
    cpdef inline void calc_soilheatflux(self) noexcept nogil:
        cdef double lai
        cdef numpy.int64_t k
        cdef double b
        cdef double a
        cdef double w
        w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
        a = w * 0.2 + (1.0 - w) * 0.5
        b = a * 0.03 / 0.2
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.soilheatflux[k] = 0.0
            else:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                self.sequences.fluxes.soilheatflux[k] = max(a - b * lai, 0.0) * self.sequences.fluxes.netradiation[k]
    cpdef inline void calc_waterevaporation(self) noexcept nogil:
        cdef double evap
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                evap = self.return_evaporation_penmanmonteith_v2(k, 0.0)
                self.sequences.fluxes.waterevaporation[k] = evap
            else:
                self.sequences.fluxes.waterevaporation[k] = 0.0
    cpdef inline void calc_snowcover_snowcovermodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowcover[k] = submodel.get_snowcover(k)
    cpdef inline void calc_potentialinterceptionevaporation(self) noexcept nogil:
        cdef double evap
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                evap = self.return_evaporation_penmanmonteith_v2(k, 0.0)
                self.sequences.fluxes.potentialinterceptionevaporation[k] = evap
            else:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = 0.0
    cpdef inline void calc_precipitation(self) noexcept nogil:
        if self.precipmodel_typeid == 1:
            self.calc_precipitation_precipmodel_v1(                (<masterinterface.MasterInterface>self.precipmodel)            )
        elif self.precipmodel_typeid == 2:
            self.calc_precipitation_precipmodel_v2(                (<masterinterface.MasterInterface>self.precipmodel)            )
    cpdef inline void update_loggedprecipitation(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedprecipitation[idx, k] = self.sequences.logs.loggedprecipitation[idx - 1, k]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedprecipitation[0, k] = self.sequences.fluxes.precipitation[k]
    cpdef inline void update_loggedpotentialsoilevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedpotentialsoilevapotranspiration[idx, k] = (                    self.sequences.logs.loggedpotentialsoilevapotranspiration[idx - 1, k]                )
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedpotentialsoilevapotranspiration[0, k] = (                self.sequences.fluxes.potentialsoilevapotranspiration[k]            )
    cpdef inline void update_loggedwaterevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedwaterevaporation[idx, k] = self.sequences.logs.loggedwaterevaporation[                    idx - 1, k                ]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedwaterevaporation[0, k] = self.sequences.fluxes.waterevaporation[k]
    cpdef inline void calc_dailywaterevaporation(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailywaterevaporation[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.fluxes.dailywaterevaporation[k] = self.sequences.fluxes.dailywaterevaporation[k] + (self.sequences.logs.loggedwaterevaporation[idx, k])
    cpdef void determine_potentialinterceptionevaporation_v1(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_sunshineduration_v1()
        self.calc_globalradiation_v1()
        self.calc_airtemperature_v1()
        self.calc_windspeed10m_v1()
        self.calc_saturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_dryairpressure_v1()
        self.calc_airdensity_v1()
        self.calc_aerodynamicresistance_v2()
        self.calc_snowcover_v1()
        self.calc_dailyprecipitation_v1()
        self.calc_dailypotentialsoilevapotranspiration_v1()
        self.calc_currentalbedo_v2()
        self.calc_netshortwaveradiation_v2()
        self.update_cloudcoverage_v1()
        self.calc_adjustedcloudcoverage_v1()
        self.calc_netlongwaveradiation_v2()
        self.calc_netradiation_v1()
        self.calc_soilheatflux_v4()
        self.calc_potentialinterceptionevaporation_v2()
    cpdef void determine_potentialsoilevapotranspiration_v1(self) noexcept nogil:
        self.update_soilresistance_v1()
        self.calc_actualsurfaceresistance_v2()
        self.calc_potentialsoilevapotranspiration_v1()
        self.update_loggedpotentialsoilevapotranspiration_v1()
        self.calc_precipitation_v1()
        self.update_loggedprecipitation_v1()
    cpdef void determine_potentialwaterevaporation_v1(self) noexcept nogil:
        self.calc_waterevaporation_v4()
        self.update_loggedwaterevaporation_v1()
        self.calc_dailywaterevaporation_v1()
    cpdef void determine_potentialinterceptionevaporation(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_sunshineduration_v1()
        self.calc_globalradiation_v1()
        self.calc_airtemperature_v1()
        self.calc_windspeed10m_v1()
        self.calc_saturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_dryairpressure_v1()
        self.calc_airdensity_v1()
        self.calc_aerodynamicresistance_v2()
        self.calc_snowcover_v1()
        self.calc_dailyprecipitation_v1()
        self.calc_dailypotentialsoilevapotranspiration_v1()
        self.calc_currentalbedo_v2()
        self.calc_netshortwaveradiation_v2()
        self.update_cloudcoverage_v1()
        self.calc_adjustedcloudcoverage_v1()
        self.calc_netlongwaveradiation_v2()
        self.calc_netradiation_v1()
        self.calc_soilheatflux_v4()
        self.calc_potentialinterceptionevaporation_v2()
    cpdef void determine_potentialsoilevapotranspiration(self) noexcept nogil:
        self.update_soilresistance_v1()
        self.calc_actualsurfaceresistance_v2()
        self.calc_potentialsoilevapotranspiration_v1()
        self.update_loggedpotentialsoilevapotranspiration_v1()
        self.calc_precipitation_v1()
        self.update_loggedprecipitation_v1()
    cpdef void determine_potentialwaterevaporation(self) noexcept nogil:
        self.calc_waterevaporation_v4()
        self.update_loggedwaterevaporation_v1()
        self.calc_dailywaterevaporation_v1()
