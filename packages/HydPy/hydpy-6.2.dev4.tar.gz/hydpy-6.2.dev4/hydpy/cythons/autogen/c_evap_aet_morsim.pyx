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
        if self._dailyairtemperature_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailyairtemperature_length_0):
                self.dailyairtemperature[jdx0] = self._dailyairtemperature_ncarray[k]
                k += 1
        elif self._dailyairtemperature_ramflag:
            for jdx0 in range(self._dailyairtemperature_length_0):
                self.dailyairtemperature[jdx0] = self._dailyairtemperature_array[idx, jdx0]
        if self._windspeed2m_diskflag_reading:
            self.windspeed2m = self._windspeed2m_ncarray[0]
        elif self._windspeed2m_ramflag:
            self.windspeed2m = self._windspeed2m_array[idx]
        if self._dailywindspeed2m_diskflag_reading:
            self.dailywindspeed2m = self._dailywindspeed2m_ncarray[0]
        elif self._dailywindspeed2m_ramflag:
            self.dailywindspeed2m = self._dailywindspeed2m_array[idx]
        if self._windspeed10m_diskflag_reading:
            self.windspeed10m = self._windspeed10m_ncarray[0]
        elif self._windspeed10m_ramflag:
            self.windspeed10m = self._windspeed10m_array[idx]
        if self._dailyrelativehumidity_diskflag_reading:
            self.dailyrelativehumidity = self._dailyrelativehumidity_ncarray[0]
        elif self._dailyrelativehumidity_ramflag:
            self.dailyrelativehumidity = self._dailyrelativehumidity_array[idx]
        if self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
        if self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._dailysunshineduration_diskflag_reading:
            self.dailysunshineduration = self._dailysunshineduration_ncarray[0]
        elif self._dailysunshineduration_ramflag:
            self.dailysunshineduration = self._dailysunshineduration_array[idx]
        if self._dailypossiblesunshineduration_diskflag_reading:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_ncarray[0]
        elif self._dailypossiblesunshineduration_ramflag:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_array[idx]
        if self._saturationvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_ncarray[k]
                k += 1
        elif self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_array[idx, jdx0]
        if self._dailysaturationvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailysaturationvapourpressure_length_0):
                self.dailysaturationvapourpressure[jdx0] = self._dailysaturationvapourpressure_ncarray[k]
                k += 1
        elif self._dailysaturationvapourpressure_ramflag:
            for jdx0 in range(self._dailysaturationvapourpressure_length_0):
                self.dailysaturationvapourpressure[jdx0] = self._dailysaturationvapourpressure_array[idx, jdx0]
        if self._saturationvapourpressureslope_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self.saturationvapourpressureslope[jdx0] = self._saturationvapourpressureslope_ncarray[k]
                k += 1
        elif self._saturationvapourpressureslope_ramflag:
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self.saturationvapourpressureslope[jdx0] = self._saturationvapourpressureslope_array[idx, jdx0]
        if self._dailysaturationvapourpressureslope_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailysaturationvapourpressureslope_length_0):
                self.dailysaturationvapourpressureslope[jdx0] = self._dailysaturationvapourpressureslope_ncarray[k]
                k += 1
        elif self._dailysaturationvapourpressureslope_ramflag:
            for jdx0 in range(self._dailysaturationvapourpressureslope_length_0):
                self.dailysaturationvapourpressureslope[jdx0] = self._dailysaturationvapourpressureslope_array[idx, jdx0]
        if self._actualvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_ncarray[k]
                k += 1
        elif self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_array[idx, jdx0]
        if self._dailyactualvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailyactualvapourpressure_length_0):
                self.dailyactualvapourpressure[jdx0] = self._dailyactualvapourpressure_ncarray[k]
                k += 1
        elif self._dailyactualvapourpressure_ramflag:
            for jdx0 in range(self._dailyactualvapourpressure_length_0):
                self.dailyactualvapourpressure[jdx0] = self._dailyactualvapourpressure_array[idx, jdx0]
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
        if self._aerodynamicresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self.aerodynamicresistance[jdx0] = self._aerodynamicresistance_ncarray[k]
                k += 1
        elif self._aerodynamicresistance_ramflag:
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self.aerodynamicresistance[jdx0] = self._aerodynamicresistance_array[idx, jdx0]
        if self._soilsurfaceresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilsurfaceresistance_length_0):
                self.soilsurfaceresistance[jdx0] = self._soilsurfaceresistance_ncarray[k]
                k += 1
        elif self._soilsurfaceresistance_ramflag:
            for jdx0 in range(self._soilsurfaceresistance_length_0):
                self.soilsurfaceresistance[jdx0] = self._soilsurfaceresistance_array[idx, jdx0]
        if self._landusesurfaceresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._landusesurfaceresistance_length_0):
                self.landusesurfaceresistance[jdx0] = self._landusesurfaceresistance_ncarray[k]
                k += 1
        elif self._landusesurfaceresistance_ramflag:
            for jdx0 in range(self._landusesurfaceresistance_length_0):
                self.landusesurfaceresistance[jdx0] = self._landusesurfaceresistance_array[idx, jdx0]
        if self._actualsurfaceresistance_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self.actualsurfaceresistance[jdx0] = self._actualsurfaceresistance_ncarray[k]
                k += 1
        elif self._actualsurfaceresistance_ramflag:
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self.actualsurfaceresistance[jdx0] = self._actualsurfaceresistance_array[idx, jdx0]
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
        if self._dailyairtemperature_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailyairtemperature_length_0):
                self._dailyairtemperature_ncarray[k] = self.dailyairtemperature[jdx0]
                k += 1
        if self._dailyairtemperature_ramflag:
            for jdx0 in range(self._dailyairtemperature_length_0):
                self._dailyairtemperature_array[idx, jdx0] = self.dailyairtemperature[jdx0]
        if self._windspeed2m_diskflag_writing:
            self._windspeed2m_ncarray[0] = self.windspeed2m
        if self._windspeed2m_ramflag:
            self._windspeed2m_array[idx] = self.windspeed2m
        if self._dailywindspeed2m_diskflag_writing:
            self._dailywindspeed2m_ncarray[0] = self.dailywindspeed2m
        if self._dailywindspeed2m_ramflag:
            self._dailywindspeed2m_array[idx] = self.dailywindspeed2m
        if self._windspeed10m_diskflag_writing:
            self._windspeed10m_ncarray[0] = self.windspeed10m
        if self._windspeed10m_ramflag:
            self._windspeed10m_array[idx] = self.windspeed10m
        if self._dailyrelativehumidity_diskflag_writing:
            self._dailyrelativehumidity_ncarray[0] = self.dailyrelativehumidity
        if self._dailyrelativehumidity_ramflag:
            self._dailyrelativehumidity_array[idx] = self.dailyrelativehumidity
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._dailysunshineduration_diskflag_writing:
            self._dailysunshineduration_ncarray[0] = self.dailysunshineduration
        if self._dailysunshineduration_ramflag:
            self._dailysunshineduration_array[idx] = self.dailysunshineduration
        if self._dailypossiblesunshineduration_diskflag_writing:
            self._dailypossiblesunshineduration_ncarray[0] = self.dailypossiblesunshineduration
        if self._dailypossiblesunshineduration_ramflag:
            self._dailypossiblesunshineduration_array[idx] = self.dailypossiblesunshineduration
        if self._saturationvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_ncarray[k] = self.saturationvapourpressure[jdx0]
                k += 1
        if self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_array[idx, jdx0] = self.saturationvapourpressure[jdx0]
        if self._dailysaturationvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailysaturationvapourpressure_length_0):
                self._dailysaturationvapourpressure_ncarray[k] = self.dailysaturationvapourpressure[jdx0]
                k += 1
        if self._dailysaturationvapourpressure_ramflag:
            for jdx0 in range(self._dailysaturationvapourpressure_length_0):
                self._dailysaturationvapourpressure_array[idx, jdx0] = self.dailysaturationvapourpressure[jdx0]
        if self._saturationvapourpressureslope_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self._saturationvapourpressureslope_ncarray[k] = self.saturationvapourpressureslope[jdx0]
                k += 1
        if self._saturationvapourpressureslope_ramflag:
            for jdx0 in range(self._saturationvapourpressureslope_length_0):
                self._saturationvapourpressureslope_array[idx, jdx0] = self.saturationvapourpressureslope[jdx0]
        if self._dailysaturationvapourpressureslope_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailysaturationvapourpressureslope_length_0):
                self._dailysaturationvapourpressureslope_ncarray[k] = self.dailysaturationvapourpressureslope[jdx0]
                k += 1
        if self._dailysaturationvapourpressureslope_ramflag:
            for jdx0 in range(self._dailysaturationvapourpressureslope_length_0):
                self._dailysaturationvapourpressureslope_array[idx, jdx0] = self.dailysaturationvapourpressureslope[jdx0]
        if self._actualvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_ncarray[k] = self.actualvapourpressure[jdx0]
                k += 1
        if self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_array[idx, jdx0] = self.actualvapourpressure[jdx0]
        if self._dailyactualvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailyactualvapourpressure_length_0):
                self._dailyactualvapourpressure_ncarray[k] = self.dailyactualvapourpressure[jdx0]
                k += 1
        if self._dailyactualvapourpressure_ramflag:
            for jdx0 in range(self._dailyactualvapourpressure_length_0):
                self._dailyactualvapourpressure_array[idx, jdx0] = self.dailyactualvapourpressure[jdx0]
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
        if self._aerodynamicresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self._aerodynamicresistance_ncarray[k] = self.aerodynamicresistance[jdx0]
                k += 1
        if self._aerodynamicresistance_ramflag:
            for jdx0 in range(self._aerodynamicresistance_length_0):
                self._aerodynamicresistance_array[idx, jdx0] = self.aerodynamicresistance[jdx0]
        if self._soilsurfaceresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilsurfaceresistance_length_0):
                self._soilsurfaceresistance_ncarray[k] = self.soilsurfaceresistance[jdx0]
                k += 1
        if self._soilsurfaceresistance_ramflag:
            for jdx0 in range(self._soilsurfaceresistance_length_0):
                self._soilsurfaceresistance_array[idx, jdx0] = self.soilsurfaceresistance[jdx0]
        if self._landusesurfaceresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._landusesurfaceresistance_length_0):
                self._landusesurfaceresistance_ncarray[k] = self.landusesurfaceresistance[jdx0]
                k += 1
        if self._landusesurfaceresistance_ramflag:
            for jdx0 in range(self._landusesurfaceresistance_length_0):
                self._landusesurfaceresistance_array[idx, jdx0] = self.landusesurfaceresistance[jdx0]
        if self._actualsurfaceresistance_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self._actualsurfaceresistance_ncarray[k] = self.actualsurfaceresistance[jdx0]
                k += 1
        if self._actualsurfaceresistance_ramflag:
            for jdx0 in range(self._actualsurfaceresistance_length_0):
                self._actualsurfaceresistance_array[idx, jdx0] = self.actualsurfaceresistance[jdx0]
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
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "windspeed2m":
            self._windspeed2m_outputpointer = value.p_value
        if name == "dailywindspeed2m":
            self._dailywindspeed2m_outputpointer = value.p_value
        if name == "windspeed10m":
            self._windspeed10m_outputpointer = value.p_value
        if name == "dailyrelativehumidity":
            self._dailyrelativehumidity_outputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_outputpointer = value.p_value
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "dailysunshineduration":
            self._dailysunshineduration_outputpointer = value.p_value
        if name == "dailypossiblesunshineduration":
            self._dailypossiblesunshineduration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._windspeed2m_outputflag:
            self._windspeed2m_outputpointer[0] = self.windspeed2m
        if self._dailywindspeed2m_outputflag:
            self._dailywindspeed2m_outputpointer[0] = self.dailywindspeed2m
        if self._windspeed10m_outputflag:
            self._windspeed10m_outputpointer[0] = self.windspeed10m
        if self._dailyrelativehumidity_outputflag:
            self._dailyrelativehumidity_outputpointer[0] = self.dailyrelativehumidity
        if self._sunshineduration_outputflag:
            self._sunshineduration_outputpointer[0] = self.sunshineduration
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._dailysunshineduration_outputflag:
            self._dailysunshineduration_outputpointer[0] = self.dailysunshineduration
        if self._dailypossiblesunshineduration_outputflag:
            self._dailypossiblesunshineduration_outputpointer[0] = self.dailypossiblesunshineduration
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._dailyglobalradiation_diskflag_reading:
            self.dailyglobalradiation = self._dailyglobalradiation_ncarray[0]
        elif self._dailyglobalradiation_ramflag:
            self.dailyglobalradiation = self._dailyglobalradiation_array[idx]
        if self._netshortwaveradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self.netshortwaveradiation[jdx0] = self._netshortwaveradiation_ncarray[k]
                k += 1
        elif self._netshortwaveradiation_ramflag:
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self.netshortwaveradiation[jdx0] = self._netshortwaveradiation_array[idx, jdx0]
        if self._dailynetshortwaveradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailynetshortwaveradiation_length_0):
                self.dailynetshortwaveradiation[jdx0] = self._dailynetshortwaveradiation_ncarray[k]
                k += 1
        elif self._dailynetshortwaveradiation_ramflag:
            for jdx0 in range(self._dailynetshortwaveradiation_length_0):
                self.dailynetshortwaveradiation[jdx0] = self._dailynetshortwaveradiation_array[idx, jdx0]
        if self._dailynetlongwaveradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailynetlongwaveradiation_length_0):
                self.dailynetlongwaveradiation[jdx0] = self._dailynetlongwaveradiation_ncarray[k]
                k += 1
        elif self._dailynetlongwaveradiation_ramflag:
            for jdx0 in range(self._dailynetlongwaveradiation_length_0):
                self.dailynetlongwaveradiation[jdx0] = self._dailynetlongwaveradiation_array[idx, jdx0]
        if self._netradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._netradiation_length_0):
                self.netradiation[jdx0] = self._netradiation_ncarray[k]
                k += 1
        elif self._netradiation_ramflag:
            for jdx0 in range(self._netradiation_length_0):
                self.netradiation[jdx0] = self._netradiation_array[idx, jdx0]
        if self._dailynetradiation_diskflag_reading:
            k = 0
            for jdx0 in range(self._dailynetradiation_length_0):
                self.dailynetradiation[jdx0] = self._dailynetradiation_ncarray[k]
                k += 1
        elif self._dailynetradiation_ramflag:
            for jdx0 in range(self._dailynetradiation_length_0):
                self.dailynetradiation[jdx0] = self._dailynetradiation_array[idx, jdx0]
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
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._dailyglobalradiation_diskflag_writing:
            self._dailyglobalradiation_ncarray[0] = self.dailyglobalradiation
        if self._dailyglobalradiation_ramflag:
            self._dailyglobalradiation_array[idx] = self.dailyglobalradiation
        if self._netshortwaveradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self._netshortwaveradiation_ncarray[k] = self.netshortwaveradiation[jdx0]
                k += 1
        if self._netshortwaveradiation_ramflag:
            for jdx0 in range(self._netshortwaveradiation_length_0):
                self._netshortwaveradiation_array[idx, jdx0] = self.netshortwaveradiation[jdx0]
        if self._dailynetshortwaveradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailynetshortwaveradiation_length_0):
                self._dailynetshortwaveradiation_ncarray[k] = self.dailynetshortwaveradiation[jdx0]
                k += 1
        if self._dailynetshortwaveradiation_ramflag:
            for jdx0 in range(self._dailynetshortwaveradiation_length_0):
                self._dailynetshortwaveradiation_array[idx, jdx0] = self.dailynetshortwaveradiation[jdx0]
        if self._dailynetlongwaveradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailynetlongwaveradiation_length_0):
                self._dailynetlongwaveradiation_ncarray[k] = self.dailynetlongwaveradiation[jdx0]
                k += 1
        if self._dailynetlongwaveradiation_ramflag:
            for jdx0 in range(self._dailynetlongwaveradiation_length_0):
                self._dailynetlongwaveradiation_array[idx, jdx0] = self.dailynetlongwaveradiation[jdx0]
        if self._netradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._netradiation_length_0):
                self._netradiation_ncarray[k] = self.netradiation[jdx0]
                k += 1
        if self._netradiation_ramflag:
            for jdx0 in range(self._netradiation_length_0):
                self._netradiation_array[idx, jdx0] = self.netradiation[jdx0]
        if self._dailynetradiation_diskflag_writing:
            k = 0
            for jdx0 in range(self._dailynetradiation_length_0):
                self._dailynetradiation_ncarray[k] = self.dailynetradiation[jdx0]
                k += 1
        if self._dailynetradiation_ramflag:
            for jdx0 in range(self._dailynetradiation_length_0):
                self._dailynetradiation_array[idx, jdx0] = self.dailynetradiation[jdx0]
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
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
        if name == "dailyglobalradiation":
            self._dailyglobalradiation_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._dailyglobalradiation_outputflag:
            self._dailyglobalradiation_outputpointer[0] = self.dailyglobalradiation
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.intercmodel = None
        self.intercmodel_is_mainmodel = False
        self.radiationmodel = None
        self.radiationmodel_is_mainmodel = False
        self.snowalbedomodel = None
        self.snowalbedomodel_is_mainmodel = False
        self.snowcovermodel = None
        self.snowcovermodel_is_mainmodel = False
        self.snowycanopymodel = None
        self.snowycanopymodel_is_mainmodel = False
        self.soilwatermodel = None
        self.soilwatermodel_is_mainmodel = False
        self.tempmodel = None
        self.tempmodel_is_mainmodel = False
    def get_intercmodel(self) -> masterinterface.MasterInterface | None:
        return self.intercmodel
    def set_intercmodel(self, intercmodel: masterinterface.MasterInterface | None) -> None:
        self.intercmodel = intercmodel
    def get_radiationmodel(self) -> masterinterface.MasterInterface | None:
        return self.radiationmodel
    def set_radiationmodel(self, radiationmodel: masterinterface.MasterInterface | None) -> None:
        self.radiationmodel = radiationmodel
    def get_snowalbedomodel(self) -> masterinterface.MasterInterface | None:
        return self.snowalbedomodel
    def set_snowalbedomodel(self, snowalbedomodel: masterinterface.MasterInterface | None) -> None:
        self.snowalbedomodel = snowalbedomodel
    def get_snowcovermodel(self) -> masterinterface.MasterInterface | None:
        return self.snowcovermodel
    def set_snowcovermodel(self, snowcovermodel: masterinterface.MasterInterface | None) -> None:
        self.snowcovermodel = snowcovermodel
    def get_snowycanopymodel(self) -> masterinterface.MasterInterface | None:
        return self.snowycanopymodel
    def set_snowycanopymodel(self, snowycanopymodel: masterinterface.MasterInterface | None) -> None:
        self.snowycanopymodel = snowycanopymodel
    def get_soilwatermodel(self) -> masterinterface.MasterInterface | None:
        return self.soilwatermodel
    def set_soilwatermodel(self, soilwatermodel: masterinterface.MasterInterface | None) -> None:
        self.soilwatermodel = soilwatermodel
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
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.reset_reuseflags()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.reset_reuseflags()
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.reset_reuseflags()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.reset_reuseflags()
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.reset_reuseflags()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.reset_reuseflags()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.load_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.load_data(idx)
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.load_data(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.load_data(idx)
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.load_data(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.load_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.save_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.save_data(idx)
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.save_data(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.save_data(idx)
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.save_data(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.save_data(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.new2old()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.new2old()
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.new2old()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.new2old()
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.new2old()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.new2old()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.determine_interceptionevaporation_v2()
        self.determine_soilevapotranspiration_v3()
        self.determine_waterevaporation_v3()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_inlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_inlets()
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.update_inlets()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_inlets()
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.update_inlets()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_inlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_outlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outlets()
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.update_outlets()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_outlets()
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.update_outlets()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_outlets()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_receivers(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_receivers(idx)
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.update_receivers(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_receivers(idx)
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.update_receivers(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_receivers(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_senders(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_senders(idx)
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.update_senders(idx)
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_senders(idx)
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.update_senders(idx)
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_senders(idx)
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
        if (self.intercmodel is not None) and not self.intercmodel_is_mainmodel:
            self.intercmodel.update_outputs()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outputs()
        if (self.snowalbedomodel is not None) and not self.snowalbedomodel_is_mainmodel:
            self.snowalbedomodel.update_outputs()
        if (self.snowcovermodel is not None) and not self.snowcovermodel_is_mainmodel:
            self.snowcovermodel.update_outputs()
        if (self.snowycanopymodel is not None) and not self.snowycanopymodel_is_mainmodel:
            self.snowycanopymodel.update_outputs()
        if (self.soilwatermodel is not None) and not self.soilwatermodel_is_mainmodel:
            self.soilwatermodel.update_outputs()
        if (self.tempmodel is not None) and not self.tempmodel_is_mainmodel:
            self.tempmodel.update_outputs()
    cpdef double get_waterevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.waterevaporation[k]
    cpdef double get_interceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.interceptionevaporation[k]
    cpdef double get_soilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.soilevapotranspiration[k]
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
    cpdef inline void update_loggedairtemperature_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedairtemperature[idx, k] = self.sequences.logs.loggedairtemperature[idx - 1, k]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedairtemperature[0, k] = self.sequences.factors.airtemperature[k]
    cpdef inline void calc_dailyairtemperature_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyairtemperature[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.dailyairtemperature[k] = self.sequences.factors.dailyairtemperature[k] + (self.sequences.logs.loggedairtemperature[idx, k])
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyairtemperature[k] = self.sequences.factors.dailyairtemperature[k] / (self.parameters.derived.nmblogentries)
    cpdef inline double return_adjustedwindspeed_v1(self, double h) noexcept nogil:
        if h == self.parameters.control.measuringheightwindspeed:
            return self.sequences.inputs.windspeed
        return self.sequences.inputs.windspeed * (            log(h / self.parameters.fixed.roughnesslengthgrass)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.roughnesslengthgrass)        )
    cpdef inline void calc_windspeed2m_v2(self) noexcept nogil:
        self.sequences.factors.windspeed2m = self.return_adjustedwindspeed_v1(2.0)
    cpdef inline void update_loggedwindspeed2m_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedwindspeed2m[idx] = self.sequences.logs.loggedwindspeed2m[idx - 1]
        self.sequences.logs.loggedwindspeed2m[0] = self.sequences.factors.windspeed2m
    cpdef inline void calc_dailywindspeed2m_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailywindspeed2m = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailywindspeed2m = self.sequences.factors.dailywindspeed2m + (self.sequences.logs.loggedwindspeed2m[idx])
        self.sequences.factors.dailywindspeed2m = self.sequences.factors.dailywindspeed2m / (self.parameters.derived.nmblogentries)
    cpdef inline void calc_windspeed10m_v1(self) noexcept nogil:
        self.sequences.factors.windspeed10m = self.return_adjustedwindspeed_v1(10.0)
    cpdef inline void update_loggedrelativehumidity_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedrelativehumidity[idx] = self.sequences.logs.loggedrelativehumidity[idx - 1]
        self.sequences.logs.loggedrelativehumidity[0] = self.sequences.inputs.relativehumidity
    cpdef inline void calc_dailyrelativehumidity_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailyrelativehumidity = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailyrelativehumidity = self.sequences.factors.dailyrelativehumidity + (self.sequences.logs.loggedrelativehumidity[idx])
        self.sequences.factors.dailyrelativehumidity = self.sequences.factors.dailyrelativehumidity / (self.parameters.derived.nmblogentries)
    cpdef inline double return_saturationvapourpressure_v1(self, double airtemperature) noexcept nogil:
        return 6.1078 * 2.71828 ** (            17.08085 * airtemperature / (airtemperature + 234.175)        )
    cpdef inline void calc_saturationvapourpressure_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressure[k] = self.return_saturationvapourpressure_v1(                self.sequences.factors.airtemperature[k]            )
    cpdef inline void calc_dailysaturationvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailysaturationvapourpressure[k] = (                self.return_saturationvapourpressure_v1(self.sequences.factors.dailyairtemperature[k])            )
    cpdef inline double return_saturationvapourpressureslope_v1(self, double t) noexcept nogil:
        return (            24430.6 * exp(17.08085 * t / (t + 234.175)) / (t + 234.175) ** 2        )
    cpdef inline void calc_saturationvapourpressureslope_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressureslope[k] = (                self.return_saturationvapourpressureslope_v1(self.sequences.factors.airtemperature[k])            )
    cpdef inline void calc_dailysaturationvapourpressureslope_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailysaturationvapourpressureslope[k] = (                self.return_saturationvapourpressureslope_v1(                    self.sequences.factors.dailyairtemperature[k]                )            )
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
    cpdef inline void calc_dailyactualvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyactualvapourpressure[k] = (                self.sequences.factors.dailysaturationvapourpressure[k] * self.sequences.factors.dailyrelativehumidity / 100.0            )
    cpdef inline void update_loggedsunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.factors.sunshineduration
    cpdef inline void calc_dailysunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailysunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailysunshineduration = self.sequences.factors.dailysunshineduration + (self.sequences.logs.loggedsunshineduration[idx])
    cpdef inline void update_loggedpossiblesunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedpossiblesunshineduration[idx] = (                self.sequences.logs.loggedpossiblesunshineduration[idx - 1]            )
        self.sequences.logs.loggedpossiblesunshineduration[0] = self.sequences.factors.possiblesunshineduration
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailypossiblesunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailypossiblesunshineduration = self.sequences.factors.dailypossiblesunshineduration + (self.sequences.logs.loggedpossiblesunshineduration[idx])
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_dailyglobalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailyglobalradiation = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation / (self.parameters.derived.nmblogentries)
    cpdef inline void calc_currentalbedo_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.snowalbedomodel is None:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.currentalbedo[k] = self.parameters.control.albedo[                    self.parameters.control.hrutype[k] - self.parameters.control._albedo_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._albedo_columnmin,                ]
        elif self.snowalbedomodel_typeid == 1:
            self.calc_currentalbedo_snowalbedomodel_v1(                (<masterinterface.MasterInterface>self.snowalbedomodel)            )
            for k in range(self.parameters.control.nmbhru):
                if isnan(self.sequences.factors.currentalbedo[k]):
                    self.sequences.factors.currentalbedo[k] = self.parameters.control.albedo[                        self.parameters.control.hrutype[k] - self.parameters.control._albedo_rowmin,                        self.parameters.derived.moy[self.idx_sim] - self.parameters.control._albedo_columnmin,                    ]
    cpdef inline void calc_netshortwaveradiation_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = self.sequences.fluxes.globalradiation * (                1.0 - self.sequences.factors.currentalbedo[k]            )
    cpdef inline void calc_dailynetshortwaveradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailynetshortwaveradiation[k] = (                1.0 - self.sequences.factors.currentalbedo[k]            ) * self.sequences.fluxes.dailyglobalradiation
    cpdef inline void calc_dailynetlongwaveradiation_v1(self) noexcept nogil:
        cdef double t
        cdef numpy.int64_t k
        cdef double rel_sunshine
        rel_sunshine = min(            self.sequences.factors.dailysunshineduration / self.sequences.factors.dailypossiblesunshineduration, 1.0        )
        for k in range(self.parameters.control.nmbhru):
            t = self.sequences.factors.dailyairtemperature[k] + 273.15
            self.sequences.fluxes.dailynetlongwaveradiation[k] = (                (0.2 + 0.8 * rel_sunshine)                * (self.parameters.fixed.stefanboltzmannconstant * t**4)                * (                    self.parameters.control.emissivity                    - self.parameters.fixed.factorcounterradiation                    * (self.sequences.factors.dailyactualvapourpressure[k] / t) ** (1.0 / 7.0)                )            )
    cpdef inline void calc_netradiation_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.dailynetlongwaveradiation[k]            )
    cpdef inline void calc_dailynetradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailynetradiation[k] = (                self.sequences.fluxes.dailynetshortwaveradiation[k] - self.sequences.fluxes.dailynetlongwaveradiation[k]            )
    cpdef inline void calc_aerodynamicresistance_v1(self) noexcept nogil:
        cdef double z0
        cdef double ch
        cdef numpy.int64_t k
        if self.sequences.factors.windspeed10m > 0.0:
            for k in range(self.parameters.control.nmbhru):
                ch = self.parameters.control.cropheight[                    self.parameters.control.hrutype[k] - self.parameters.control._cropheight_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._cropheight_columnmin,                ]
                if ch < 10.0:
                    z0 = 0.021 + 0.163 * ch
                    self.sequences.factors.aerodynamicresistance[k] = (                        6.25 / self.sequences.factors.windspeed10m * log(10.0 / z0) ** 2                    )
                else:
                    self.sequences.factors.aerodynamicresistance[k] = 94.0 / self.sequences.factors.windspeed10m
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.aerodynamicresistance[k] = inf
    cpdef inline void calc_soilsurfaceresistance_v1(self) noexcept nogil:
        cdef double sw_act
        cdef double sw_max
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            sw_max = self.parameters.control.maxsoilwater[k]
            if not self.parameters.control.soil[k]:
                self.sequences.factors.soilsurfaceresistance[k] = nan
            elif sw_max > 20.0:
                self.sequences.factors.soilsurfaceresistance[k] = 100.0
            elif sw_max > 0.0:
                sw_act = min(max(self.sequences.factors.soilwater[k], 0.0), sw_max)
                self.sequences.factors.soilsurfaceresistance[k] = 100.0 * sw_max / (sw_act + 0.01 * sw_max)
            else:
                self.sequences.factors.soilsurfaceresistance[k] = inf
    cpdef inline void calc_landusesurfaceresistance_v1(self) noexcept nogil:
        cdef double thresh
        cdef double sw
        cdef double d
        cdef double r
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            r = self.parameters.control.surfaceresistance[                self.parameters.control.hrutype[k] - self.parameters.control._surfaceresistance_rowmin,                self.parameters.derived.moy[self.idx_sim] - self.parameters.control._surfaceresistance_columnmin,            ]
            if self.parameters.control.conifer[k]:
                d = self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k]
                if (self.sequences.factors.airtemperature[k] <= -5.0) or (d >= 20.0):
                    self.sequences.factors.landusesurfaceresistance[k] = 10000.0
                elif self.sequences.factors.airtemperature[k] < 20.0:
                    self.sequences.factors.landusesurfaceresistance[k] = min(                        (25.0 * r) / (self.sequences.factors.airtemperature[k] + 5.0) / (1.0 - 0.05 * d),                        10000.0,                    )
                else:
                    self.sequences.factors.landusesurfaceresistance[k] = min(r / (1.0 - 0.05 * d), 10000.0)
            else:
                self.sequences.factors.landusesurfaceresistance[k] = r
            if self.parameters.control.soil[k]:
                sw = self.sequences.factors.soilwater[k]
                if sw <= 0.0:
                    self.sequences.factors.landusesurfaceresistance[k] = inf
                else:
                    thresh = self.parameters.control.soilmoisturelimit[k] * self.parameters.control.maxsoilwater[k]
                    if sw < thresh:
                        self.sequences.factors.landusesurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k] * (3.5 * (                            1.0 - sw / thresh                        ) + exp(0.2 * thresh / sw))
                    else:
                        self.sequences.factors.landusesurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k] * (exp(0.2))
    cpdef inline void calc_actualsurfaceresistance_v1(self) noexcept nogil:
        cdef double w
        cdef double invsrnight
        cdef double invsrday
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                invsrday = (                    (1.0 - 0.7**lai) / self.sequences.factors.landusesurfaceresistance[k]                ) + 0.7**lai / self.sequences.factors.soilsurfaceresistance[k]
                invsrnight = lai / 2500.0 + 1.0 / self.sequences.factors.soilsurfaceresistance[k]
                w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
                self.sequences.factors.actualsurfaceresistance[k] = 1.0 / (                    w * invsrday + (1.0 - w) * invsrnight                )
            else:
                self.sequences.factors.actualsurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k]
    cpdef inline void calc_interceptedwater_v1(self) noexcept nogil:
        if self.intercmodel_typeid == 1:
            self.calc_interceptedwater_intercmodel_v1(                (<masterinterface.MasterInterface>self.intercmodel)            )
    cpdef inline void calc_snowycanopy_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.snowycanopymodel is None:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.snowycanopy[k] = nan
        elif self.snowycanopymodel_typeid == 1:
            self.calc_snowycanopy_snowycanopymodel_v1(                (<masterinterface.MasterInterface>self.snowycanopymodel)            )
    cpdef inline double return_evaporation_penmanmonteith_v1(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil:
        cdef double c
        cdef double b
        cdef double t
        cdef double ar
        ar = min(max(self.sequences.factors.aerodynamicresistance[k], 1e-6), 1e6)
        t = 273.15 + self.sequences.factors.airtemperature[k]
        b = (4.0 * self.parameters.control.emissivity * self.parameters.fixed.stefanboltzmannconstant) * t**3
        c = 1.0 + b * ar / self.sequences.factors.airdensity[k] / self.parameters.fixed.heatcapacityair
        return (            (                self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (c * self.sequences.factors.airdensity[k] * self.parameters.fixed.heatcapacityair)                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])                / ar            )            / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.parameters.fixed.psychrometricconstant * c * (1.0 + actualsurfaceresistance / ar)            )            / self.parameters.fixed.heatofcondensation        )
    cpdef inline void calc_interceptionevaporation_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if (                self.parameters.control.interception[k]                and (self.parameters.control.tree[k] or (self.sequences.factors.snowcover[k] == 0.0))                and not (self.parameters.control.tree[k] and (self.sequences.factors.snowycanopy[k] > 0.0))            ):
                self.sequences.fluxes.interceptionevaporation[k] = min(                    self.sequences.fluxes.potentialinterceptionevaporation[k], self.sequences.factors.interceptedwater[k]                )
            else:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
    cpdef inline void calc_soilwater_v1(self) noexcept nogil:
        if self.soilwatermodel_typeid == 1:
            self.calc_soilwater_soilwatermodel_v1(                (<masterinterface.MasterInterface>self.soilwatermodel)            )
    cpdef inline void calc_snowcover_v1(self) noexcept nogil:
        if self.snowcovermodel_typeid == 1:
            self.calc_snowcover_snowcovermodel_v1(                (<masterinterface.MasterInterface>self.snowcovermodel)            )
    cpdef inline void calc_soilheatflux_v3(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.soilheatflux[k] = 0.0
            else:
                self.sequences.fluxes.soilheatflux[k] = self.parameters.control.averagesoilheatflux[self.parameters.derived.moy[self.idx_sim]]
    cpdef inline void calc_soilevapotranspiration_v3(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k] and (self.parameters.control.tree[k] or self.sequences.factors.snowcover[k] == 0.0):
                self.sequences.fluxes.soilevapotranspiration[k] = (                    self.return_evaporation_penmanmonteith_v1(                        k, self.sequences.factors.actualsurfaceresistance[k]                    )                )
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
    cpdef inline void calc_waterevaporation_v3(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.waterevaporation[k] = (                    self.sequences.factors.dailysaturationvapourpressureslope[k]                    * self.sequences.fluxes.dailynetradiation[k]                    / self.parameters.fixed.heatofcondensation                    + self.parameters.fixed.psychrometricconstant                    * self.parameters.derived.days                    * (0.13 + 0.094 * self.sequences.factors.dailywindspeed2m)                    * (                        self.sequences.factors.dailysaturationvapourpressure[k]                        - self.sequences.factors.dailyactualvapourpressure[k]                    )                ) / (                    self.sequences.factors.dailysaturationvapourpressureslope[k]                    + self.parameters.fixed.psychrometricconstant                )
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
    cpdef inline void calc_interceptedwater_intercmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.interceptedwater[k] = submodel.get_interceptedwater(k)
    cpdef inline void calc_soilwater_soilwatermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.soilwater[k] = submodel.get_soilwater(k)
    cpdef inline void calc_snowcover_snowcovermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowcover[k] = submodel.get_snowcover(k)
    cpdef inline void calc_snowycanopy_snowycanopymodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowycanopy[k] = submodel.get_snowycanopy(k)
    cpdef inline void calc_currentalbedo_snowalbedomodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.currentalbedo[k] = submodel.get_snowalbedo(k)
    cpdef inline void calc_potentialinterceptionevaporation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = (                    self.return_evaporation_penmanmonteith_v1(k, 0.0)                )
            else:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = 0.0
    cpdef double get_waterevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.waterevaporation[k]
    cpdef double get_interceptionevaporation(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.interceptionevaporation[k]
    cpdef double get_soilevapotranspiration(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.soilevapotranspiration[k]
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
    cpdef inline void update_loggedairtemperature(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.logs.loggedairtemperature[idx, k] = self.sequences.logs.loggedairtemperature[idx - 1, k]
        for k in range(self.parameters.control.nmbhru):
            self.sequences.logs.loggedairtemperature[0, k] = self.sequences.factors.airtemperature[k]
    cpdef inline void calc_dailyairtemperature(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyairtemperature[k] = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.dailyairtemperature[k] = self.sequences.factors.dailyairtemperature[k] + (self.sequences.logs.loggedairtemperature[idx, k])
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyairtemperature[k] = self.sequences.factors.dailyairtemperature[k] / (self.parameters.derived.nmblogentries)
    cpdef inline double return_adjustedwindspeed(self, double h) noexcept nogil:
        if h == self.parameters.control.measuringheightwindspeed:
            return self.sequences.inputs.windspeed
        return self.sequences.inputs.windspeed * (            log(h / self.parameters.fixed.roughnesslengthgrass)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.roughnesslengthgrass)        )
    cpdef inline void calc_windspeed2m(self) noexcept nogil:
        self.sequences.factors.windspeed2m = self.return_adjustedwindspeed_v1(2.0)
    cpdef inline void update_loggedwindspeed2m(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedwindspeed2m[idx] = self.sequences.logs.loggedwindspeed2m[idx - 1]
        self.sequences.logs.loggedwindspeed2m[0] = self.sequences.factors.windspeed2m
    cpdef inline void calc_dailywindspeed2m(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailywindspeed2m = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailywindspeed2m = self.sequences.factors.dailywindspeed2m + (self.sequences.logs.loggedwindspeed2m[idx])
        self.sequences.factors.dailywindspeed2m = self.sequences.factors.dailywindspeed2m / (self.parameters.derived.nmblogentries)
    cpdef inline void calc_windspeed10m(self) noexcept nogil:
        self.sequences.factors.windspeed10m = self.return_adjustedwindspeed_v1(10.0)
    cpdef inline void update_loggedrelativehumidity(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedrelativehumidity[idx] = self.sequences.logs.loggedrelativehumidity[idx - 1]
        self.sequences.logs.loggedrelativehumidity[0] = self.sequences.inputs.relativehumidity
    cpdef inline void calc_dailyrelativehumidity(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailyrelativehumidity = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailyrelativehumidity = self.sequences.factors.dailyrelativehumidity + (self.sequences.logs.loggedrelativehumidity[idx])
        self.sequences.factors.dailyrelativehumidity = self.sequences.factors.dailyrelativehumidity / (self.parameters.derived.nmblogentries)
    cpdef inline double return_saturationvapourpressure(self, double airtemperature) noexcept nogil:
        return 6.1078 * 2.71828 ** (            17.08085 * airtemperature / (airtemperature + 234.175)        )
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressure[k] = self.return_saturationvapourpressure_v1(                self.sequences.factors.airtemperature[k]            )
    cpdef inline void calc_dailysaturationvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailysaturationvapourpressure[k] = (                self.return_saturationvapourpressure_v1(self.sequences.factors.dailyairtemperature[k])            )
    cpdef inline double return_saturationvapourpressureslope(self, double t) noexcept nogil:
        return (            24430.6 * exp(17.08085 * t / (t + 234.175)) / (t + 234.175) ** 2        )
    cpdef inline void calc_saturationvapourpressureslope(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.saturationvapourpressureslope[k] = (                self.return_saturationvapourpressureslope_v1(self.sequences.factors.airtemperature[k])            )
    cpdef inline void calc_dailysaturationvapourpressureslope(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailysaturationvapourpressureslope[k] = (                self.return_saturationvapourpressureslope_v1(                    self.sequences.factors.dailyairtemperature[k]                )            )
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
    cpdef inline void calc_dailyactualvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.dailyactualvapourpressure[k] = (                self.sequences.factors.dailysaturationvapourpressure[k] * self.sequences.factors.dailyrelativehumidity / 100.0            )
    cpdef inline void update_loggedsunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.factors.sunshineduration
    cpdef inline void calc_dailysunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailysunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailysunshineduration = self.sequences.factors.dailysunshineduration + (self.sequences.logs.loggedsunshineduration[idx])
    cpdef inline void update_loggedpossiblesunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedpossiblesunshineduration[idx] = (                self.sequences.logs.loggedpossiblesunshineduration[idx - 1]            )
        self.sequences.logs.loggedpossiblesunshineduration[0] = self.sequences.factors.possiblesunshineduration
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailypossiblesunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailypossiblesunshineduration = self.sequences.factors.dailypossiblesunshineduration + (self.sequences.logs.loggedpossiblesunshineduration[idx])
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_dailyglobalradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailyglobalradiation = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation / (self.parameters.derived.nmblogentries)
    cpdef inline void calc_currentalbedo(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.snowalbedomodel is None:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.currentalbedo[k] = self.parameters.control.albedo[                    self.parameters.control.hrutype[k] - self.parameters.control._albedo_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._albedo_columnmin,                ]
        elif self.snowalbedomodel_typeid == 1:
            self.calc_currentalbedo_snowalbedomodel_v1(                (<masterinterface.MasterInterface>self.snowalbedomodel)            )
            for k in range(self.parameters.control.nmbhru):
                if isnan(self.sequences.factors.currentalbedo[k]):
                    self.sequences.factors.currentalbedo[k] = self.parameters.control.albedo[                        self.parameters.control.hrutype[k] - self.parameters.control._albedo_rowmin,                        self.parameters.derived.moy[self.idx_sim] - self.parameters.control._albedo_columnmin,                    ]
    cpdef inline void calc_netshortwaveradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netshortwaveradiation[k] = self.sequences.fluxes.globalradiation * (                1.0 - self.sequences.factors.currentalbedo[k]            )
    cpdef inline void calc_dailynetshortwaveradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailynetshortwaveradiation[k] = (                1.0 - self.sequences.factors.currentalbedo[k]            ) * self.sequences.fluxes.dailyglobalradiation
    cpdef inline void calc_dailynetlongwaveradiation(self) noexcept nogil:
        cdef double t
        cdef numpy.int64_t k
        cdef double rel_sunshine
        rel_sunshine = min(            self.sequences.factors.dailysunshineduration / self.sequences.factors.dailypossiblesunshineduration, 1.0        )
        for k in range(self.parameters.control.nmbhru):
            t = self.sequences.factors.dailyairtemperature[k] + 273.15
            self.sequences.fluxes.dailynetlongwaveradiation[k] = (                (0.2 + 0.8 * rel_sunshine)                * (self.parameters.fixed.stefanboltzmannconstant * t**4)                * (                    self.parameters.control.emissivity                    - self.parameters.fixed.factorcounterradiation                    * (self.sequences.factors.dailyactualvapourpressure[k] / t) ** (1.0 / 7.0)                )            )
    cpdef inline void calc_netradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.netradiation[k] = (                self.sequences.fluxes.netshortwaveradiation[k] - self.sequences.fluxes.dailynetlongwaveradiation[k]            )
    cpdef inline void calc_dailynetradiation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.dailynetradiation[k] = (                self.sequences.fluxes.dailynetshortwaveradiation[k] - self.sequences.fluxes.dailynetlongwaveradiation[k]            )
    cpdef inline void calc_aerodynamicresistance(self) noexcept nogil:
        cdef double z0
        cdef double ch
        cdef numpy.int64_t k
        if self.sequences.factors.windspeed10m > 0.0:
            for k in range(self.parameters.control.nmbhru):
                ch = self.parameters.control.cropheight[                    self.parameters.control.hrutype[k] - self.parameters.control._cropheight_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._cropheight_columnmin,                ]
                if ch < 10.0:
                    z0 = 0.021 + 0.163 * ch
                    self.sequences.factors.aerodynamicresistance[k] = (                        6.25 / self.sequences.factors.windspeed10m * log(10.0 / z0) ** 2                    )
                else:
                    self.sequences.factors.aerodynamicresistance[k] = 94.0 / self.sequences.factors.windspeed10m
        else:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.aerodynamicresistance[k] = inf
    cpdef inline void calc_soilsurfaceresistance(self) noexcept nogil:
        cdef double sw_act
        cdef double sw_max
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            sw_max = self.parameters.control.maxsoilwater[k]
            if not self.parameters.control.soil[k]:
                self.sequences.factors.soilsurfaceresistance[k] = nan
            elif sw_max > 20.0:
                self.sequences.factors.soilsurfaceresistance[k] = 100.0
            elif sw_max > 0.0:
                sw_act = min(max(self.sequences.factors.soilwater[k], 0.0), sw_max)
                self.sequences.factors.soilsurfaceresistance[k] = 100.0 * sw_max / (sw_act + 0.01 * sw_max)
            else:
                self.sequences.factors.soilsurfaceresistance[k] = inf
    cpdef inline void calc_landusesurfaceresistance(self) noexcept nogil:
        cdef double thresh
        cdef double sw
        cdef double d
        cdef double r
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            r = self.parameters.control.surfaceresistance[                self.parameters.control.hrutype[k] - self.parameters.control._surfaceresistance_rowmin,                self.parameters.derived.moy[self.idx_sim] - self.parameters.control._surfaceresistance_columnmin,            ]
            if self.parameters.control.conifer[k]:
                d = self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k]
                if (self.sequences.factors.airtemperature[k] <= -5.0) or (d >= 20.0):
                    self.sequences.factors.landusesurfaceresistance[k] = 10000.0
                elif self.sequences.factors.airtemperature[k] < 20.0:
                    self.sequences.factors.landusesurfaceresistance[k] = min(                        (25.0 * r) / (self.sequences.factors.airtemperature[k] + 5.0) / (1.0 - 0.05 * d),                        10000.0,                    )
                else:
                    self.sequences.factors.landusesurfaceresistance[k] = min(r / (1.0 - 0.05 * d), 10000.0)
            else:
                self.sequences.factors.landusesurfaceresistance[k] = r
            if self.parameters.control.soil[k]:
                sw = self.sequences.factors.soilwater[k]
                if sw <= 0.0:
                    self.sequences.factors.landusesurfaceresistance[k] = inf
                else:
                    thresh = self.parameters.control.soilmoisturelimit[k] * self.parameters.control.maxsoilwater[k]
                    if sw < thresh:
                        self.sequences.factors.landusesurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k] * (3.5 * (                            1.0 - sw / thresh                        ) + exp(0.2 * thresh / sw))
                    else:
                        self.sequences.factors.landusesurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k] * (exp(0.2))
    cpdef inline void calc_actualsurfaceresistance(self) noexcept nogil:
        cdef double w
        cdef double invsrnight
        cdef double invsrday
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k]:
                lai = self.parameters.control.leafareaindex[                    self.parameters.control.hrutype[k] - self.parameters.control._leafareaindex_rowmin,                    self.parameters.derived.moy[self.idx_sim] - self.parameters.control._leafareaindex_columnmin,                ]
                invsrday = (                    (1.0 - 0.7**lai) / self.sequences.factors.landusesurfaceresistance[k]                ) + 0.7**lai / self.sequences.factors.soilsurfaceresistance[k]
                invsrnight = lai / 2500.0 + 1.0 / self.sequences.factors.soilsurfaceresistance[k]
                w = self.sequences.factors.possiblesunshineduration / self.parameters.derived.hours
                self.sequences.factors.actualsurfaceresistance[k] = 1.0 / (                    w * invsrday + (1.0 - w) * invsrnight                )
            else:
                self.sequences.factors.actualsurfaceresistance[k] = self.sequences.factors.landusesurfaceresistance[k]
    cpdef inline void calc_interceptedwater(self) noexcept nogil:
        if self.intercmodel_typeid == 1:
            self.calc_interceptedwater_intercmodel_v1(                (<masterinterface.MasterInterface>self.intercmodel)            )
    cpdef inline void calc_snowycanopy(self) noexcept nogil:
        cdef numpy.int64_t k
        if self.snowycanopymodel is None:
            for k in range(self.parameters.control.nmbhru):
                self.sequences.factors.snowycanopy[k] = nan
        elif self.snowycanopymodel_typeid == 1:
            self.calc_snowycanopy_snowycanopymodel_v1(                (<masterinterface.MasterInterface>self.snowycanopymodel)            )
    cpdef inline double return_evaporation_penmanmonteith(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil:
        cdef double c
        cdef double b
        cdef double t
        cdef double ar
        ar = min(max(self.sequences.factors.aerodynamicresistance[k], 1e-6), 1e6)
        t = 273.15 + self.sequences.factors.airtemperature[k]
        b = (4.0 * self.parameters.control.emissivity * self.parameters.fixed.stefanboltzmannconstant) * t**3
        c = 1.0 + b * ar / self.sequences.factors.airdensity[k] / self.parameters.fixed.heatcapacityair
        return (            (                self.sequences.factors.saturationvapourpressureslope[k]                * (self.sequences.fluxes.netradiation[k] - self.sequences.fluxes.soilheatflux[k])                + (c * self.sequences.factors.airdensity[k] * self.parameters.fixed.heatcapacityair)                * (self.sequences.factors.saturationvapourpressure[k] - self.sequences.factors.actualvapourpressure[k])                / ar            )            / (                self.sequences.factors.saturationvapourpressureslope[k]                + self.parameters.fixed.psychrometricconstant * c * (1.0 + actualsurfaceresistance / ar)            )            / self.parameters.fixed.heatofcondensation        )
    cpdef inline void calc_interceptionevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if (                self.parameters.control.interception[k]                and (self.parameters.control.tree[k] or (self.sequences.factors.snowcover[k] == 0.0))                and not (self.parameters.control.tree[k] and (self.sequences.factors.snowycanopy[k] > 0.0))            ):
                self.sequences.fluxes.interceptionevaporation[k] = min(                    self.sequences.fluxes.potentialinterceptionevaporation[k], self.sequences.factors.interceptedwater[k]                )
            else:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
    cpdef inline void calc_soilwater(self) noexcept nogil:
        if self.soilwatermodel_typeid == 1:
            self.calc_soilwater_soilwatermodel_v1(                (<masterinterface.MasterInterface>self.soilwatermodel)            )
    cpdef inline void calc_snowcover(self) noexcept nogil:
        if self.snowcovermodel_typeid == 1:
            self.calc_snowcover_snowcovermodel_v1(                (<masterinterface.MasterInterface>self.snowcovermodel)            )
    cpdef inline void calc_soilheatflux(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.soilheatflux[k] = 0.0
            else:
                self.sequences.fluxes.soilheatflux[k] = self.parameters.control.averagesoilheatflux[self.parameters.derived.moy[self.idx_sim]]
    cpdef inline void calc_soilevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.soil[k] and (self.parameters.control.tree[k] or self.sequences.factors.snowcover[k] == 0.0):
                self.sequences.fluxes.soilevapotranspiration[k] = (                    self.return_evaporation_penmanmonteith_v1(                        k, self.sequences.factors.actualsurfaceresistance[k]                    )                )
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
    cpdef inline void calc_waterevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.water[k]:
                self.sequences.fluxes.waterevaporation[k] = (                    self.sequences.factors.dailysaturationvapourpressureslope[k]                    * self.sequences.fluxes.dailynetradiation[k]                    / self.parameters.fixed.heatofcondensation                    + self.parameters.fixed.psychrometricconstant                    * self.parameters.derived.days                    * (0.13 + 0.094 * self.sequences.factors.dailywindspeed2m)                    * (                        self.sequences.factors.dailysaturationvapourpressure[k]                        - self.sequences.factors.dailyactualvapourpressure[k]                    )                ) / (                    self.sequences.factors.dailysaturationvapourpressureslope[k]                    + self.parameters.fixed.psychrometricconstant                )
            else:
                self.sequences.fluxes.waterevaporation[k] = 0.0
    cpdef inline void calc_interceptedwater_intercmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.interceptedwater[k] = submodel.get_interceptedwater(k)
    cpdef inline void calc_soilwater_soilwatermodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.soilwater[k] = submodel.get_soilwater(k)
    cpdef inline void calc_snowcover_snowcovermodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowcover[k] = submodel.get_snowcover(k)
    cpdef inline void calc_snowycanopy_snowycanopymodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.snowycanopy[k] = submodel.get_snowycanopy(k)
    cpdef inline void calc_currentalbedo_snowalbedomodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.currentalbedo[k] = submodel.get_snowalbedo(k)
    cpdef inline void calc_potentialinterceptionevaporation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            if self.parameters.control.interception[k]:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = (                    self.return_evaporation_penmanmonteith_v1(k, 0.0)                )
            else:
                self.sequences.fluxes.potentialinterceptionevaporation[k] = 0.0
    cpdef void determine_interceptionevaporation_v2(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_sunshineduration_v1()
        self.calc_globalradiation_v1()
        self.calc_airtemperature_v1()
        self.update_loggedairtemperature_v1()
        self.calc_dailyairtemperature_v1()
        self.calc_windspeed10m_v1()
        self.update_loggedrelativehumidity_v1()
        self.calc_dailyrelativehumidity_v1()
        self.calc_saturationvapourpressure_v2()
        self.calc_dailysaturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v2()
        self.calc_dailysaturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_dailyactualvapourpressure_v1()
        self.calc_dryairpressure_v1()
        self.calc_airdensity_v1()
        self.calc_aerodynamicresistance_v1()
        self.calc_snowcover_v1()
        self.calc_snowycanopy_v1()
        self.update_loggedsunshineduration_v1()
        self.calc_dailysunshineduration_v1()
        self.update_loggedpossiblesunshineduration_v1()
        self.calc_dailypossiblesunshineduration_v1()
        self.calc_currentalbedo_v1()
        self.calc_netshortwaveradiation_v2()
        self.calc_dailynetlongwaveradiation_v1()
        self.calc_netradiation_v2()
        self.calc_soilheatflux_v3()
        self.calc_potentialinterceptionevaporation_v1()
        self.calc_interceptedwater_v1()
        self.calc_interceptionevaporation_v2()
    cpdef void determine_soilevapotranspiration_v3(self) noexcept nogil:
        self.calc_soilwater_v1()
        self.calc_snowcover_v1()
        self.calc_soilsurfaceresistance_v1()
        self.calc_landusesurfaceresistance_v1()
        self.calc_actualsurfaceresistance_v1()
        self.calc_soilevapotranspiration_v3()
        self.update_soilevapotranspiration_v3()
    cpdef void determine_waterevaporation_v3(self) noexcept nogil:
        self.calc_windspeed2m_v2()
        self.update_loggedwindspeed2m_v1()
        self.calc_dailywindspeed2m_v1()
        self.update_loggedglobalradiation_v1()
        self.calc_dailyglobalradiation_v1()
        self.calc_dailynetshortwaveradiation_v1()
        self.calc_dailynetradiation_v1()
        self.calc_waterevaporation_v3()
    cpdef void determine_interceptionevaporation(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_sunshineduration_v1()
        self.calc_globalradiation_v1()
        self.calc_airtemperature_v1()
        self.update_loggedairtemperature_v1()
        self.calc_dailyairtemperature_v1()
        self.calc_windspeed10m_v1()
        self.update_loggedrelativehumidity_v1()
        self.calc_dailyrelativehumidity_v1()
        self.calc_saturationvapourpressure_v2()
        self.calc_dailysaturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v2()
        self.calc_dailysaturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_dailyactualvapourpressure_v1()
        self.calc_dryairpressure_v1()
        self.calc_airdensity_v1()
        self.calc_aerodynamicresistance_v1()
        self.calc_snowcover_v1()
        self.calc_snowycanopy_v1()
        self.update_loggedsunshineduration_v1()
        self.calc_dailysunshineduration_v1()
        self.update_loggedpossiblesunshineduration_v1()
        self.calc_dailypossiblesunshineduration_v1()
        self.calc_currentalbedo_v1()
        self.calc_netshortwaveradiation_v2()
        self.calc_dailynetlongwaveradiation_v1()
        self.calc_netradiation_v2()
        self.calc_soilheatflux_v3()
        self.calc_potentialinterceptionevaporation_v1()
        self.calc_interceptedwater_v1()
        self.calc_interceptionevaporation_v2()
    cpdef void determine_soilevapotranspiration(self) noexcept nogil:
        self.calc_soilwater_v1()
        self.calc_snowcover_v1()
        self.calc_soilsurfaceresistance_v1()
        self.calc_landusesurfaceresistance_v1()
        self.calc_actualsurfaceresistance_v1()
        self.calc_soilevapotranspiration_v3()
        self.update_soilevapotranspiration_v3()
    cpdef void determine_waterevaporation(self) noexcept nogil:
        self.calc_windspeed2m_v2()
        self.update_loggedwindspeed2m_v1()
        self.calc_dailywindspeed2m_v1()
        self.update_loggedglobalradiation_v1()
        self.calc_dailyglobalradiation_v1()
        self.calc_dailynetshortwaveradiation_v1()
        self.calc_dailynetradiation_v1()
        self.calc_waterevaporation_v3()
