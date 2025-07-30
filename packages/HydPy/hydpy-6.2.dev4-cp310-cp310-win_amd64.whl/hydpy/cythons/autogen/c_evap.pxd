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
ctypedef void (*CallbackType) (Model)  noexcept nogil
cdef class CallbackWrapper:
    cdef CallbackType callback
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
@cython.final
cdef class ControlParameters:
    cdef public numpy.int64_t nmbhru
    cdef public numpy.int64_t[:] hrutype
    cdef public numpy.npy_bool[:] water
    cdef public numpy.npy_bool[:] interception
    cdef public numpy.npy_bool[:] soil
    cdef public numpy.npy_bool[:] plant
    cdef public numpy.npy_bool[:] tree
    cdef public numpy.npy_bool[:] conifer
    cdef public double[:] hruarea
    cdef public double[:] hrualtitude
    cdef public double measuringheightwindspeed
    cdef public double[:] coastfactor
    cdef public double[:,:] albedo
    cdef public numpy.int64_t _albedo_rowmin
    cdef public numpy.int64_t _albedo_columnmin
    cdef public double[:] groundalbedo
    cdef public double[:] groundalbedosnow
    cdef public double[:] leafalbedo
    cdef public double[:] leafalbedosnow
    cdef public double[:,:] leafareaindex
    cdef public numpy.int64_t _leafareaindex_rowmin
    cdef public numpy.int64_t _leafareaindex_columnmin
    cdef public double[:,:] cropheight
    cdef public numpy.int64_t _cropheight_rowmin
    cdef public numpy.int64_t _cropheight_columnmin
    cdef public double cloudtypefactor
    cdef public double nightcloudfactor
    cdef public double emissivity
    cdef public double[:] averagesoilheatflux
    cdef public numpy.int64_t _averagesoilheatflux_entrymin
    cdef public double[:,:] surfaceresistance
    cdef public numpy.int64_t _surfaceresistance_rowmin
    cdef public numpy.int64_t _surfaceresistance_columnmin
    cdef public double[:] wetsoilresistance
    cdef public double[:] soilresistanceincrease
    cdef public double[:] wetnessthreshold
    cdef public double[:] leafresistance
    cdef public double[:] evapotranspirationfactor
    cdef public double[:] monthfactor
    cdef public numpy.int64_t _monthfactor_entrymin
    cdef public double[:,:] landmonthfactor
    cdef public numpy.int64_t _landmonthfactor_rowmin
    cdef public numpy.int64_t _landmonthfactor_columnmin
    cdef public double[:] altitudefactor
    cdef public double[:] precipitationfactor
    cdef public double[:] airtemperaturefactor
    cdef public double[:] dampingfactor
    cdef public double[:] temperaturethresholdice
    cdef public double[:] maxsoilwater
    cdef public double[:] soilmoisturelimit
    cdef public double[:] excessreduction
    cdef public double[:] dissefactor
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public double[:] hruareafraction
    cdef public double altitude
    cdef public double hours
    cdef public double days
    cdef public numpy.int64_t nmblogentries
    cdef public double[:,:] roughnesslength
    cdef public numpy.int64_t _roughnesslength_rowmin
    cdef public numpy.int64_t _roughnesslength_columnmin
    cdef public double[:,:] aerodynamicresistancefactor
    cdef public numpy.int64_t _aerodynamicresistancefactor_rowmin
    cdef public numpy.int64_t _aerodynamicresistancefactor_columnmin
@cython.final
cdef class FixedParameters:
    cdef public double stefanboltzmannconstant
    cdef public double factorcounterradiation
    cdef public double gasconstantdryair
    cdef public double gasconstantwatervapour
    cdef public double heatcapacityair
    cdef public double heatofcondensation
    cdef public double roughnesslengthgrass
    cdef public double psychrometricconstant
    cdef public double aerodynamicresistancefactorminimum
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
    cdef public double referenceevapotranspiration
    cdef public numpy.int64_t _referenceevapotranspiration_ndim
    cdef public numpy.int64_t _referenceevapotranspiration_length
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_diskflag_reading
    cdef public bint _referenceevapotranspiration_diskflag_writing
    cdef public double[:] _referenceevapotranspiration_ncarray
    cdef public bint _referenceevapotranspiration_inputflag
    cdef double *_referenceevapotranspiration_inputpointer
    cdef public double relativehumidity
    cdef public numpy.int64_t _relativehumidity_ndim
    cdef public numpy.int64_t _relativehumidity_length
    cdef public bint _relativehumidity_ramflag
    cdef public double[:] _relativehumidity_array
    cdef public bint _relativehumidity_diskflag_reading
    cdef public bint _relativehumidity_diskflag_writing
    cdef public double[:] _relativehumidity_ncarray
    cdef public bint _relativehumidity_inputflag
    cdef double *_relativehumidity_inputpointer
    cdef public double windspeed
    cdef public numpy.int64_t _windspeed_ndim
    cdef public numpy.int64_t _windspeed_length
    cdef public bint _windspeed_ramflag
    cdef public double[:] _windspeed_array
    cdef public bint _windspeed_diskflag_reading
    cdef public bint _windspeed_diskflag_writing
    cdef public double[:] _windspeed_ncarray
    cdef public bint _windspeed_inputflag
    cdef double *_windspeed_inputpointer
    cdef public double atmosphericpressure
    cdef public numpy.int64_t _atmosphericpressure_ndim
    cdef public numpy.int64_t _atmosphericpressure_length
    cdef public bint _atmosphericpressure_ramflag
    cdef public double[:] _atmosphericpressure_array
    cdef public bint _atmosphericpressure_diskflag_reading
    cdef public bint _atmosphericpressure_diskflag_writing
    cdef public double[:] _atmosphericpressure_ncarray
    cdef public bint _atmosphericpressure_inputflag
    cdef double *_atmosphericpressure_inputpointer
    cdef public double normalairtemperature
    cdef public numpy.int64_t _normalairtemperature_ndim
    cdef public numpy.int64_t _normalairtemperature_length
    cdef public bint _normalairtemperature_ramflag
    cdef public double[:] _normalairtemperature_array
    cdef public bint _normalairtemperature_diskflag_reading
    cdef public bint _normalairtemperature_diskflag_writing
    cdef public double[:] _normalairtemperature_ncarray
    cdef public bint _normalairtemperature_inputflag
    cdef double *_normalairtemperature_inputpointer
    cdef public double normalevapotranspiration
    cdef public numpy.int64_t _normalevapotranspiration_ndim
    cdef public numpy.int64_t _normalevapotranspiration_length
    cdef public bint _normalevapotranspiration_ramflag
    cdef public double[:] _normalevapotranspiration_array
    cdef public bint _normalevapotranspiration_diskflag_reading
    cdef public bint _normalevapotranspiration_diskflag_writing
    cdef public double[:] _normalevapotranspiration_ncarray
    cdef public bint _normalevapotranspiration_inputflag
    cdef double *_normalevapotranspiration_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double meanairtemperature
    cdef public numpy.int64_t _meanairtemperature_ndim
    cdef public numpy.int64_t _meanairtemperature_length
    cdef public bint _meanairtemperature_ramflag
    cdef public double[:] _meanairtemperature_array
    cdef public bint _meanairtemperature_diskflag_reading
    cdef public bint _meanairtemperature_diskflag_writing
    cdef public double[:] _meanairtemperature_ncarray
    cdef public bint _meanairtemperature_outputflag
    cdef double *_meanairtemperature_outputpointer
    cdef public double[:] airtemperature
    cdef public numpy.int64_t _airtemperature_ndim
    cdef public numpy.int64_t _airtemperature_length
    cdef public numpy.int64_t _airtemperature_length_0
    cdef public bint _airtemperature_ramflag
    cdef public double[:,:] _airtemperature_array
    cdef public bint _airtemperature_diskflag_reading
    cdef public bint _airtemperature_diskflag_writing
    cdef public double[:] _airtemperature_ncarray
    cdef public double[:] dailyairtemperature
    cdef public numpy.int64_t _dailyairtemperature_ndim
    cdef public numpy.int64_t _dailyairtemperature_length
    cdef public numpy.int64_t _dailyairtemperature_length_0
    cdef public bint _dailyairtemperature_ramflag
    cdef public double[:,:] _dailyairtemperature_array
    cdef public bint _dailyairtemperature_diskflag_reading
    cdef public bint _dailyairtemperature_diskflag_writing
    cdef public double[:] _dailyairtemperature_ncarray
    cdef public double windspeed2m
    cdef public numpy.int64_t _windspeed2m_ndim
    cdef public numpy.int64_t _windspeed2m_length
    cdef public bint _windspeed2m_ramflag
    cdef public double[:] _windspeed2m_array
    cdef public bint _windspeed2m_diskflag_reading
    cdef public bint _windspeed2m_diskflag_writing
    cdef public double[:] _windspeed2m_ncarray
    cdef public bint _windspeed2m_outputflag
    cdef double *_windspeed2m_outputpointer
    cdef public double dailywindspeed2m
    cdef public numpy.int64_t _dailywindspeed2m_ndim
    cdef public numpy.int64_t _dailywindspeed2m_length
    cdef public bint _dailywindspeed2m_ramflag
    cdef public double[:] _dailywindspeed2m_array
    cdef public bint _dailywindspeed2m_diskflag_reading
    cdef public bint _dailywindspeed2m_diskflag_writing
    cdef public double[:] _dailywindspeed2m_ncarray
    cdef public bint _dailywindspeed2m_outputflag
    cdef double *_dailywindspeed2m_outputpointer
    cdef public double windspeed10m
    cdef public numpy.int64_t _windspeed10m_ndim
    cdef public numpy.int64_t _windspeed10m_length
    cdef public bint _windspeed10m_ramflag
    cdef public double[:] _windspeed10m_array
    cdef public bint _windspeed10m_diskflag_reading
    cdef public bint _windspeed10m_diskflag_writing
    cdef public double[:] _windspeed10m_ncarray
    cdef public bint _windspeed10m_outputflag
    cdef double *_windspeed10m_outputpointer
    cdef public double dailyrelativehumidity
    cdef public numpy.int64_t _dailyrelativehumidity_ndim
    cdef public numpy.int64_t _dailyrelativehumidity_length
    cdef public bint _dailyrelativehumidity_ramflag
    cdef public double[:] _dailyrelativehumidity_array
    cdef public bint _dailyrelativehumidity_diskflag_reading
    cdef public bint _dailyrelativehumidity_diskflag_writing
    cdef public double[:] _dailyrelativehumidity_ncarray
    cdef public bint _dailyrelativehumidity_outputflag
    cdef double *_dailyrelativehumidity_outputpointer
    cdef public double sunshineduration
    cdef public numpy.int64_t _sunshineduration_ndim
    cdef public numpy.int64_t _sunshineduration_length
    cdef public bint _sunshineduration_ramflag
    cdef public double[:] _sunshineduration_array
    cdef public bint _sunshineduration_diskflag_reading
    cdef public bint _sunshineduration_diskflag_writing
    cdef public double[:] _sunshineduration_ncarray
    cdef public bint _sunshineduration_outputflag
    cdef double *_sunshineduration_outputpointer
    cdef public double possiblesunshineduration
    cdef public numpy.int64_t _possiblesunshineduration_ndim
    cdef public numpy.int64_t _possiblesunshineduration_length
    cdef public bint _possiblesunshineduration_ramflag
    cdef public double[:] _possiblesunshineduration_array
    cdef public bint _possiblesunshineduration_diskflag_reading
    cdef public bint _possiblesunshineduration_diskflag_writing
    cdef public double[:] _possiblesunshineduration_ncarray
    cdef public bint _possiblesunshineduration_outputflag
    cdef double *_possiblesunshineduration_outputpointer
    cdef public double dailysunshineduration
    cdef public numpy.int64_t _dailysunshineduration_ndim
    cdef public numpy.int64_t _dailysunshineduration_length
    cdef public bint _dailysunshineduration_ramflag
    cdef public double[:] _dailysunshineduration_array
    cdef public bint _dailysunshineduration_diskflag_reading
    cdef public bint _dailysunshineduration_diskflag_writing
    cdef public double[:] _dailysunshineduration_ncarray
    cdef public bint _dailysunshineduration_outputflag
    cdef double *_dailysunshineduration_outputpointer
    cdef public double dailypossiblesunshineduration
    cdef public numpy.int64_t _dailypossiblesunshineduration_ndim
    cdef public numpy.int64_t _dailypossiblesunshineduration_length
    cdef public bint _dailypossiblesunshineduration_ramflag
    cdef public double[:] _dailypossiblesunshineduration_array
    cdef public bint _dailypossiblesunshineduration_diskflag_reading
    cdef public bint _dailypossiblesunshineduration_diskflag_writing
    cdef public double[:] _dailypossiblesunshineduration_ncarray
    cdef public bint _dailypossiblesunshineduration_outputflag
    cdef double *_dailypossiblesunshineduration_outputpointer
    cdef public double[:] saturationvapourpressure
    cdef public numpy.int64_t _saturationvapourpressure_ndim
    cdef public numpy.int64_t _saturationvapourpressure_length
    cdef public numpy.int64_t _saturationvapourpressure_length_0
    cdef public bint _saturationvapourpressure_ramflag
    cdef public double[:,:] _saturationvapourpressure_array
    cdef public bint _saturationvapourpressure_diskflag_reading
    cdef public bint _saturationvapourpressure_diskflag_writing
    cdef public double[:] _saturationvapourpressure_ncarray
    cdef public double[:] dailysaturationvapourpressure
    cdef public numpy.int64_t _dailysaturationvapourpressure_ndim
    cdef public numpy.int64_t _dailysaturationvapourpressure_length
    cdef public numpy.int64_t _dailysaturationvapourpressure_length_0
    cdef public bint _dailysaturationvapourpressure_ramflag
    cdef public double[:,:] _dailysaturationvapourpressure_array
    cdef public bint _dailysaturationvapourpressure_diskflag_reading
    cdef public bint _dailysaturationvapourpressure_diskflag_writing
    cdef public double[:] _dailysaturationvapourpressure_ncarray
    cdef public double[:] saturationvapourpressureslope
    cdef public numpy.int64_t _saturationvapourpressureslope_ndim
    cdef public numpy.int64_t _saturationvapourpressureslope_length
    cdef public numpy.int64_t _saturationvapourpressureslope_length_0
    cdef public bint _saturationvapourpressureslope_ramflag
    cdef public double[:,:] _saturationvapourpressureslope_array
    cdef public bint _saturationvapourpressureslope_diskflag_reading
    cdef public bint _saturationvapourpressureslope_diskflag_writing
    cdef public double[:] _saturationvapourpressureslope_ncarray
    cdef public double[:] dailysaturationvapourpressureslope
    cdef public numpy.int64_t _dailysaturationvapourpressureslope_ndim
    cdef public numpy.int64_t _dailysaturationvapourpressureslope_length
    cdef public numpy.int64_t _dailysaturationvapourpressureslope_length_0
    cdef public bint _dailysaturationvapourpressureslope_ramflag
    cdef public double[:,:] _dailysaturationvapourpressureslope_array
    cdef public bint _dailysaturationvapourpressureslope_diskflag_reading
    cdef public bint _dailysaturationvapourpressureslope_diskflag_writing
    cdef public double[:] _dailysaturationvapourpressureslope_ncarray
    cdef public double[:] actualvapourpressure
    cdef public numpy.int64_t _actualvapourpressure_ndim
    cdef public numpy.int64_t _actualvapourpressure_length
    cdef public numpy.int64_t _actualvapourpressure_length_0
    cdef public bint _actualvapourpressure_ramflag
    cdef public double[:,:] _actualvapourpressure_array
    cdef public bint _actualvapourpressure_diskflag_reading
    cdef public bint _actualvapourpressure_diskflag_writing
    cdef public double[:] _actualvapourpressure_ncarray
    cdef public double[:] dailyactualvapourpressure
    cdef public numpy.int64_t _dailyactualvapourpressure_ndim
    cdef public numpy.int64_t _dailyactualvapourpressure_length
    cdef public numpy.int64_t _dailyactualvapourpressure_length_0
    cdef public bint _dailyactualvapourpressure_ramflag
    cdef public double[:,:] _dailyactualvapourpressure_array
    cdef public bint _dailyactualvapourpressure_diskflag_reading
    cdef public bint _dailyactualvapourpressure_diskflag_writing
    cdef public double[:] _dailyactualvapourpressure_ncarray
    cdef public double[:] dryairpressure
    cdef public numpy.int64_t _dryairpressure_ndim
    cdef public numpy.int64_t _dryairpressure_length
    cdef public numpy.int64_t _dryairpressure_length_0
    cdef public bint _dryairpressure_ramflag
    cdef public double[:,:] _dryairpressure_array
    cdef public bint _dryairpressure_diskflag_reading
    cdef public bint _dryairpressure_diskflag_writing
    cdef public double[:] _dryairpressure_ncarray
    cdef public double[:] airdensity
    cdef public numpy.int64_t _airdensity_ndim
    cdef public numpy.int64_t _airdensity_length
    cdef public numpy.int64_t _airdensity_length_0
    cdef public bint _airdensity_ramflag
    cdef public double[:,:] _airdensity_array
    cdef public bint _airdensity_diskflag_reading
    cdef public bint _airdensity_diskflag_writing
    cdef public double[:] _airdensity_ncarray
    cdef public double psychrometricconstant
    cdef public numpy.int64_t _psychrometricconstant_ndim
    cdef public numpy.int64_t _psychrometricconstant_length
    cdef public bint _psychrometricconstant_ramflag
    cdef public double[:] _psychrometricconstant_array
    cdef public bint _psychrometricconstant_diskflag_reading
    cdef public bint _psychrometricconstant_diskflag_writing
    cdef public double[:] _psychrometricconstant_ncarray
    cdef public bint _psychrometricconstant_outputflag
    cdef double *_psychrometricconstant_outputpointer
    cdef public double[:] currentalbedo
    cdef public numpy.int64_t _currentalbedo_ndim
    cdef public numpy.int64_t _currentalbedo_length
    cdef public numpy.int64_t _currentalbedo_length_0
    cdef public bint _currentalbedo_ramflag
    cdef public double[:,:] _currentalbedo_array
    cdef public bint _currentalbedo_diskflag_reading
    cdef public bint _currentalbedo_diskflag_writing
    cdef public double[:] _currentalbedo_ncarray
    cdef public double adjustedcloudcoverage
    cdef public numpy.int64_t _adjustedcloudcoverage_ndim
    cdef public numpy.int64_t _adjustedcloudcoverage_length
    cdef public bint _adjustedcloudcoverage_ramflag
    cdef public double[:] _adjustedcloudcoverage_array
    cdef public bint _adjustedcloudcoverage_diskflag_reading
    cdef public bint _adjustedcloudcoverage_diskflag_writing
    cdef public double[:] _adjustedcloudcoverage_ncarray
    cdef public bint _adjustedcloudcoverage_outputflag
    cdef double *_adjustedcloudcoverage_outputpointer
    cdef public double[:] aerodynamicresistance
    cdef public numpy.int64_t _aerodynamicresistance_ndim
    cdef public numpy.int64_t _aerodynamicresistance_length
    cdef public numpy.int64_t _aerodynamicresistance_length_0
    cdef public bint _aerodynamicresistance_ramflag
    cdef public double[:,:] _aerodynamicresistance_array
    cdef public bint _aerodynamicresistance_diskflag_reading
    cdef public bint _aerodynamicresistance_diskflag_writing
    cdef public double[:] _aerodynamicresistance_ncarray
    cdef public double[:] soilsurfaceresistance
    cdef public numpy.int64_t _soilsurfaceresistance_ndim
    cdef public numpy.int64_t _soilsurfaceresistance_length
    cdef public numpy.int64_t _soilsurfaceresistance_length_0
    cdef public bint _soilsurfaceresistance_ramflag
    cdef public double[:,:] _soilsurfaceresistance_array
    cdef public bint _soilsurfaceresistance_diskflag_reading
    cdef public bint _soilsurfaceresistance_diskflag_writing
    cdef public double[:] _soilsurfaceresistance_ncarray
    cdef public double[:] landusesurfaceresistance
    cdef public numpy.int64_t _landusesurfaceresistance_ndim
    cdef public numpy.int64_t _landusesurfaceresistance_length
    cdef public numpy.int64_t _landusesurfaceresistance_length_0
    cdef public bint _landusesurfaceresistance_ramflag
    cdef public double[:,:] _landusesurfaceresistance_array
    cdef public bint _landusesurfaceresistance_diskflag_reading
    cdef public bint _landusesurfaceresistance_diskflag_writing
    cdef public double[:] _landusesurfaceresistance_ncarray
    cdef public double[:] actualsurfaceresistance
    cdef public numpy.int64_t _actualsurfaceresistance_ndim
    cdef public numpy.int64_t _actualsurfaceresistance_length
    cdef public numpy.int64_t _actualsurfaceresistance_length_0
    cdef public bint _actualsurfaceresistance_ramflag
    cdef public double[:,:] _actualsurfaceresistance_array
    cdef public bint _actualsurfaceresistance_diskflag_reading
    cdef public bint _actualsurfaceresistance_diskflag_writing
    cdef public double[:] _actualsurfaceresistance_ncarray
    cdef public double[:] interceptedwater
    cdef public numpy.int64_t _interceptedwater_ndim
    cdef public numpy.int64_t _interceptedwater_length
    cdef public numpy.int64_t _interceptedwater_length_0
    cdef public bint _interceptedwater_ramflag
    cdef public double[:,:] _interceptedwater_array
    cdef public bint _interceptedwater_diskflag_reading
    cdef public bint _interceptedwater_diskflag_writing
    cdef public double[:] _interceptedwater_ncarray
    cdef public double[:] soilwater
    cdef public numpy.int64_t _soilwater_ndim
    cdef public numpy.int64_t _soilwater_length
    cdef public numpy.int64_t _soilwater_length_0
    cdef public bint _soilwater_ramflag
    cdef public double[:,:] _soilwater_array
    cdef public bint _soilwater_diskflag_reading
    cdef public bint _soilwater_diskflag_writing
    cdef public double[:] _soilwater_ncarray
    cdef public double[:] snowcover
    cdef public numpy.int64_t _snowcover_ndim
    cdef public numpy.int64_t _snowcover_length
    cdef public numpy.int64_t _snowcover_length_0
    cdef public bint _snowcover_ramflag
    cdef public double[:,:] _snowcover_array
    cdef public bint _snowcover_diskflag_reading
    cdef public bint _snowcover_diskflag_writing
    cdef public double[:] _snowcover_ncarray
    cdef public double[:] snowycanopy
    cdef public numpy.int64_t _snowycanopy_ndim
    cdef public numpy.int64_t _snowycanopy_length
    cdef public numpy.int64_t _snowycanopy_length_0
    cdef public bint _snowycanopy_ramflag
    cdef public double[:,:] _snowycanopy_array
    cdef public bint _snowycanopy_diskflag_reading
    cdef public bint _snowycanopy_diskflag_writing
    cdef public double[:] _snowycanopy_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double[:] precipitation
    cdef public numpy.int64_t _precipitation_ndim
    cdef public numpy.int64_t _precipitation_length
    cdef public numpy.int64_t _precipitation_length_0
    cdef public bint _precipitation_ramflag
    cdef public double[:,:] _precipitation_array
    cdef public bint _precipitation_diskflag_reading
    cdef public bint _precipitation_diskflag_writing
    cdef public double[:] _precipitation_ncarray
    cdef public double[:] dailyprecipitation
    cdef public numpy.int64_t _dailyprecipitation_ndim
    cdef public numpy.int64_t _dailyprecipitation_length
    cdef public numpy.int64_t _dailyprecipitation_length_0
    cdef public bint _dailyprecipitation_ramflag
    cdef public double[:,:] _dailyprecipitation_array
    cdef public bint _dailyprecipitation_diskflag_reading
    cdef public bint _dailyprecipitation_diskflag_writing
    cdef public double[:] _dailyprecipitation_ncarray
    cdef public double globalradiation
    cdef public numpy.int64_t _globalradiation_ndim
    cdef public numpy.int64_t _globalradiation_length
    cdef public bint _globalradiation_ramflag
    cdef public double[:] _globalradiation_array
    cdef public bint _globalradiation_diskflag_reading
    cdef public bint _globalradiation_diskflag_writing
    cdef public double[:] _globalradiation_ncarray
    cdef public bint _globalradiation_outputflag
    cdef double *_globalradiation_outputpointer
    cdef public double clearskysolarradiation
    cdef public numpy.int64_t _clearskysolarradiation_ndim
    cdef public numpy.int64_t _clearskysolarradiation_length
    cdef public bint _clearskysolarradiation_ramflag
    cdef public double[:] _clearskysolarradiation_array
    cdef public bint _clearskysolarradiation_diskflag_reading
    cdef public bint _clearskysolarradiation_diskflag_writing
    cdef public double[:] _clearskysolarradiation_ncarray
    cdef public bint _clearskysolarradiation_outputflag
    cdef double *_clearskysolarradiation_outputpointer
    cdef public double dailyglobalradiation
    cdef public numpy.int64_t _dailyglobalradiation_ndim
    cdef public numpy.int64_t _dailyglobalradiation_length
    cdef public bint _dailyglobalradiation_ramflag
    cdef public double[:] _dailyglobalradiation_array
    cdef public bint _dailyglobalradiation_diskflag_reading
    cdef public bint _dailyglobalradiation_diskflag_writing
    cdef public double[:] _dailyglobalradiation_ncarray
    cdef public bint _dailyglobalradiation_outputflag
    cdef double *_dailyglobalradiation_outputpointer
    cdef public double[:] netshortwaveradiation
    cdef public numpy.int64_t _netshortwaveradiation_ndim
    cdef public numpy.int64_t _netshortwaveradiation_length
    cdef public numpy.int64_t _netshortwaveradiation_length_0
    cdef public bint _netshortwaveradiation_ramflag
    cdef public double[:,:] _netshortwaveradiation_array
    cdef public bint _netshortwaveradiation_diskflag_reading
    cdef public bint _netshortwaveradiation_diskflag_writing
    cdef public double[:] _netshortwaveradiation_ncarray
    cdef public double[:] dailynetshortwaveradiation
    cdef public numpy.int64_t _dailynetshortwaveradiation_ndim
    cdef public numpy.int64_t _dailynetshortwaveradiation_length
    cdef public numpy.int64_t _dailynetshortwaveradiation_length_0
    cdef public bint _dailynetshortwaveradiation_ramflag
    cdef public double[:,:] _dailynetshortwaveradiation_array
    cdef public bint _dailynetshortwaveradiation_diskflag_reading
    cdef public bint _dailynetshortwaveradiation_diskflag_writing
    cdef public double[:] _dailynetshortwaveradiation_ncarray
    cdef public double[:] netlongwaveradiation
    cdef public numpy.int64_t _netlongwaveradiation_ndim
    cdef public numpy.int64_t _netlongwaveradiation_length
    cdef public numpy.int64_t _netlongwaveradiation_length_0
    cdef public bint _netlongwaveradiation_ramflag
    cdef public double[:,:] _netlongwaveradiation_array
    cdef public bint _netlongwaveradiation_diskflag_reading
    cdef public bint _netlongwaveradiation_diskflag_writing
    cdef public double[:] _netlongwaveradiation_ncarray
    cdef public double[:] dailynetlongwaveradiation
    cdef public numpy.int64_t _dailynetlongwaveradiation_ndim
    cdef public numpy.int64_t _dailynetlongwaveradiation_length
    cdef public numpy.int64_t _dailynetlongwaveradiation_length_0
    cdef public bint _dailynetlongwaveradiation_ramflag
    cdef public double[:,:] _dailynetlongwaveradiation_array
    cdef public bint _dailynetlongwaveradiation_diskflag_reading
    cdef public bint _dailynetlongwaveradiation_diskflag_writing
    cdef public double[:] _dailynetlongwaveradiation_ncarray
    cdef public double[:] netradiation
    cdef public numpy.int64_t _netradiation_ndim
    cdef public numpy.int64_t _netradiation_length
    cdef public numpy.int64_t _netradiation_length_0
    cdef public bint _netradiation_ramflag
    cdef public double[:,:] _netradiation_array
    cdef public bint _netradiation_diskflag_reading
    cdef public bint _netradiation_diskflag_writing
    cdef public double[:] _netradiation_ncarray
    cdef public double[:] dailynetradiation
    cdef public numpy.int64_t _dailynetradiation_ndim
    cdef public numpy.int64_t _dailynetradiation_length
    cdef public numpy.int64_t _dailynetradiation_length_0
    cdef public bint _dailynetradiation_ramflag
    cdef public double[:,:] _dailynetradiation_array
    cdef public bint _dailynetradiation_diskflag_reading
    cdef public bint _dailynetradiation_diskflag_writing
    cdef public double[:] _dailynetradiation_ncarray
    cdef public double[:] soilheatflux
    cdef public numpy.int64_t _soilheatflux_ndim
    cdef public numpy.int64_t _soilheatflux_length
    cdef public numpy.int64_t _soilheatflux_length_0
    cdef public bint _soilheatflux_ramflag
    cdef public double[:,:] _soilheatflux_array
    cdef public bint _soilheatflux_diskflag_reading
    cdef public bint _soilheatflux_diskflag_writing
    cdef public double[:] _soilheatflux_ncarray
    cdef public double[:] referenceevapotranspiration
    cdef public numpy.int64_t _referenceevapotranspiration_ndim
    cdef public numpy.int64_t _referenceevapotranspiration_length
    cdef public numpy.int64_t _referenceevapotranspiration_length_0
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:,:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_diskflag_reading
    cdef public bint _referenceevapotranspiration_diskflag_writing
    cdef public double[:] _referenceevapotranspiration_ncarray
    cdef public double[:] potentialinterceptionevaporation
    cdef public numpy.int64_t _potentialinterceptionevaporation_ndim
    cdef public numpy.int64_t _potentialinterceptionevaporation_length
    cdef public numpy.int64_t _potentialinterceptionevaporation_length_0
    cdef public bint _potentialinterceptionevaporation_ramflag
    cdef public double[:,:] _potentialinterceptionevaporation_array
    cdef public bint _potentialinterceptionevaporation_diskflag_reading
    cdef public bint _potentialinterceptionevaporation_diskflag_writing
    cdef public double[:] _potentialinterceptionevaporation_ncarray
    cdef public double[:] potentialsoilevapotranspiration
    cdef public numpy.int64_t _potentialsoilevapotranspiration_ndim
    cdef public numpy.int64_t _potentialsoilevapotranspiration_length
    cdef public numpy.int64_t _potentialsoilevapotranspiration_length_0
    cdef public bint _potentialsoilevapotranspiration_ramflag
    cdef public double[:,:] _potentialsoilevapotranspiration_array
    cdef public bint _potentialsoilevapotranspiration_diskflag_reading
    cdef public bint _potentialsoilevapotranspiration_diskflag_writing
    cdef public double[:] _potentialsoilevapotranspiration_ncarray
    cdef public double[:] potentialevapotranspiration
    cdef public numpy.int64_t _potentialevapotranspiration_ndim
    cdef public numpy.int64_t _potentialevapotranspiration_length
    cdef public numpy.int64_t _potentialevapotranspiration_length_0
    cdef public bint _potentialevapotranspiration_ramflag
    cdef public double[:,:] _potentialevapotranspiration_array
    cdef public bint _potentialevapotranspiration_diskflag_reading
    cdef public bint _potentialevapotranspiration_diskflag_writing
    cdef public double[:] _potentialevapotranspiration_ncarray
    cdef public double[:] dailypotentialsoilevapotranspiration
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_ndim
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_length
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_length_0
    cdef public bint _dailypotentialsoilevapotranspiration_ramflag
    cdef public double[:,:] _dailypotentialsoilevapotranspiration_array
    cdef public bint _dailypotentialsoilevapotranspiration_diskflag_reading
    cdef public bint _dailypotentialsoilevapotranspiration_diskflag_writing
    cdef public double[:] _dailypotentialsoilevapotranspiration_ncarray
    cdef public double meanreferenceevapotranspiration
    cdef public numpy.int64_t _meanreferenceevapotranspiration_ndim
    cdef public numpy.int64_t _meanreferenceevapotranspiration_length
    cdef public bint _meanreferenceevapotranspiration_ramflag
    cdef public double[:] _meanreferenceevapotranspiration_array
    cdef public bint _meanreferenceevapotranspiration_diskflag_reading
    cdef public bint _meanreferenceevapotranspiration_diskflag_writing
    cdef public double[:] _meanreferenceevapotranspiration_ncarray
    cdef public bint _meanreferenceevapotranspiration_outputflag
    cdef double *_meanreferenceevapotranspiration_outputpointer
    cdef public double meanpotentialevapotranspiration
    cdef public numpy.int64_t _meanpotentialevapotranspiration_ndim
    cdef public numpy.int64_t _meanpotentialevapotranspiration_length
    cdef public bint _meanpotentialevapotranspiration_ramflag
    cdef public double[:] _meanpotentialevapotranspiration_array
    cdef public bint _meanpotentialevapotranspiration_diskflag_reading
    cdef public bint _meanpotentialevapotranspiration_diskflag_writing
    cdef public double[:] _meanpotentialevapotranspiration_ncarray
    cdef public bint _meanpotentialevapotranspiration_outputflag
    cdef double *_meanpotentialevapotranspiration_outputpointer
    cdef public double[:] potentialwaterevaporation
    cdef public numpy.int64_t _potentialwaterevaporation_ndim
    cdef public numpy.int64_t _potentialwaterevaporation_length
    cdef public numpy.int64_t _potentialwaterevaporation_length_0
    cdef public bint _potentialwaterevaporation_ramflag
    cdef public double[:,:] _potentialwaterevaporation_array
    cdef public bint _potentialwaterevaporation_diskflag_reading
    cdef public bint _potentialwaterevaporation_diskflag_writing
    cdef public double[:] _potentialwaterevaporation_ncarray
    cdef public double[:] waterevaporation
    cdef public numpy.int64_t _waterevaporation_ndim
    cdef public numpy.int64_t _waterevaporation_length
    cdef public numpy.int64_t _waterevaporation_length_0
    cdef public bint _waterevaporation_ramflag
    cdef public double[:,:] _waterevaporation_array
    cdef public bint _waterevaporation_diskflag_reading
    cdef public bint _waterevaporation_diskflag_writing
    cdef public double[:] _waterevaporation_ncarray
    cdef public double[:] dailywaterevaporation
    cdef public numpy.int64_t _dailywaterevaporation_ndim
    cdef public numpy.int64_t _dailywaterevaporation_length
    cdef public numpy.int64_t _dailywaterevaporation_length_0
    cdef public bint _dailywaterevaporation_ramflag
    cdef public double[:,:] _dailywaterevaporation_array
    cdef public bint _dailywaterevaporation_diskflag_reading
    cdef public bint _dailywaterevaporation_diskflag_writing
    cdef public double[:] _dailywaterevaporation_ncarray
    cdef public double[:] interceptionevaporation
    cdef public numpy.int64_t _interceptionevaporation_ndim
    cdef public numpy.int64_t _interceptionevaporation_length
    cdef public numpy.int64_t _interceptionevaporation_length_0
    cdef public bint _interceptionevaporation_ramflag
    cdef public double[:,:] _interceptionevaporation_array
    cdef public bint _interceptionevaporation_diskflag_reading
    cdef public bint _interceptionevaporation_diskflag_writing
    cdef public double[:] _interceptionevaporation_ncarray
    cdef public double[:] soilevapotranspiration
    cdef public numpy.int64_t _soilevapotranspiration_ndim
    cdef public numpy.int64_t _soilevapotranspiration_length
    cdef public numpy.int64_t _soilevapotranspiration_length_0
    cdef public bint _soilevapotranspiration_ramflag
    cdef public double[:,:] _soilevapotranspiration_array
    cdef public bint _soilevapotranspiration_diskflag_reading
    cdef public bint _soilevapotranspiration_diskflag_writing
    cdef public double[:] _soilevapotranspiration_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double cloudcoverage
    cdef public numpy.int64_t _cloudcoverage_ndim
    cdef public numpy.int64_t _cloudcoverage_length
    cdef public bint _cloudcoverage_ramflag
    cdef public double[:] _cloudcoverage_array
    cdef public bint _cloudcoverage_diskflag_reading
    cdef public bint _cloudcoverage_diskflag_writing
    cdef public double[:] _cloudcoverage_ncarray
    cdef public bint _cloudcoverage_outputflag
    cdef double *_cloudcoverage_outputpointer
    cdef public double[:] soilresistance
    cdef public numpy.int64_t _soilresistance_ndim
    cdef public numpy.int64_t _soilresistance_length
    cdef public numpy.int64_t _soilresistance_length_0
    cdef public bint _soilresistance_ramflag
    cdef public double[:,:] _soilresistance_array
    cdef public bint _soilresistance_diskflag_reading
    cdef public bint _soilresistance_diskflag_writing
    cdef public double[:] _soilresistance_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:,:] loggedairtemperature
    cdef public numpy.int64_t _loggedairtemperature_ndim
    cdef public numpy.int64_t _loggedairtemperature_length
    cdef public numpy.int64_t _loggedairtemperature_length_0
    cdef public numpy.int64_t _loggedairtemperature_length_1
    cdef public double[:,:] loggedprecipitation
    cdef public numpy.int64_t _loggedprecipitation_ndim
    cdef public numpy.int64_t _loggedprecipitation_length
    cdef public numpy.int64_t _loggedprecipitation_length_0
    cdef public numpy.int64_t _loggedprecipitation_length_1
    cdef public double[:] loggedwindspeed2m
    cdef public numpy.int64_t _loggedwindspeed2m_ndim
    cdef public numpy.int64_t _loggedwindspeed2m_length
    cdef public numpy.int64_t _loggedwindspeed2m_length_0
    cdef public double[:] loggedrelativehumidity
    cdef public numpy.int64_t _loggedrelativehumidity_ndim
    cdef public numpy.int64_t _loggedrelativehumidity_length
    cdef public numpy.int64_t _loggedrelativehumidity_length_0
    cdef public double[:] loggedsunshineduration
    cdef public numpy.int64_t _loggedsunshineduration_ndim
    cdef public numpy.int64_t _loggedsunshineduration_length
    cdef public numpy.int64_t _loggedsunshineduration_length_0
    cdef public double[:] loggedpossiblesunshineduration
    cdef public numpy.int64_t _loggedpossiblesunshineduration_ndim
    cdef public numpy.int64_t _loggedpossiblesunshineduration_length
    cdef public numpy.int64_t _loggedpossiblesunshineduration_length_0
    cdef public double[:] loggedglobalradiation
    cdef public numpy.int64_t _loggedglobalradiation_ndim
    cdef public numpy.int64_t _loggedglobalradiation_length
    cdef public numpy.int64_t _loggedglobalradiation_length_0
    cdef public double[:] loggedclearskysolarradiation
    cdef public numpy.int64_t _loggedclearskysolarradiation_ndim
    cdef public numpy.int64_t _loggedclearskysolarradiation_length
    cdef public numpy.int64_t _loggedclearskysolarradiation_length_0
    cdef public double[:,:] loggedpotentialevapotranspiration
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_ndim
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length_0
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length_1
    cdef public double[:,:] loggedwaterevaporation
    cdef public numpy.int64_t _loggedwaterevaporation_ndim
    cdef public numpy.int64_t _loggedwaterevaporation_length
    cdef public numpy.int64_t _loggedwaterevaporation_length_0
    cdef public numpy.int64_t _loggedwaterevaporation_length_1
    cdef public double[:,:] loggedpotentialsoilevapotranspiration
    cdef public numpy.int64_t _loggedpotentialsoilevapotranspiration_ndim
    cdef public numpy.int64_t _loggedpotentialsoilevapotranspiration_length
    cdef public numpy.int64_t _loggedpotentialsoilevapotranspiration_length_0
    cdef public numpy.int64_t _loggedpotentialsoilevapotranspiration_length_1
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface intercmodel
    cdef public numpy.npy_bool intercmodel_is_mainmodel
    cdef public numpy.int64_t intercmodel_typeid
    cdef public masterinterface.MasterInterface petmodel
    cdef public numpy.npy_bool petmodel_is_mainmodel
    cdef public numpy.int64_t petmodel_typeid
    cdef public masterinterface.MasterInterface precipmodel
    cdef public numpy.npy_bool precipmodel_is_mainmodel
    cdef public numpy.int64_t precipmodel_typeid
    cdef public masterinterface.MasterInterface radiationmodel
    cdef public numpy.npy_bool radiationmodel_is_mainmodel
    cdef public numpy.int64_t radiationmodel_typeid
    cdef public masterinterface.MasterInterface retmodel
    cdef public numpy.npy_bool retmodel_is_mainmodel
    cdef public numpy.int64_t retmodel_typeid
    cdef public masterinterface.MasterInterface snowalbedomodel
    cdef public numpy.npy_bool snowalbedomodel_is_mainmodel
    cdef public numpy.int64_t snowalbedomodel_typeid
    cdef public masterinterface.MasterInterface snowcovermodel
    cdef public numpy.npy_bool snowcovermodel_is_mainmodel
    cdef public numpy.int64_t snowcovermodel_typeid
    cdef public masterinterface.MasterInterface snowycanopymodel
    cdef public numpy.npy_bool snowycanopymodel_is_mainmodel
    cdef public numpy.int64_t snowycanopymodel_typeid
    cdef public masterinterface.MasterInterface soilwatermodel
    cdef public numpy.npy_bool soilwatermodel_is_mainmodel
    cdef public numpy.int64_t soilwatermodel_typeid
    cdef public masterinterface.MasterInterface tempmodel
    cdef public numpy.npy_bool tempmodel_is_mainmodel
    cdef public numpy.int64_t tempmodel_typeid
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void new2old(self) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil
    cpdef inline void update_loggedairtemperature_v1(self) noexcept nogil
    cpdef inline void calc_dailyairtemperature_v1(self) noexcept nogil
    cpdef inline void calc_windspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_windspeed2m_v2(self) noexcept nogil
    cpdef inline void update_loggedwindspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_dailywindspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_windspeed10m_v1(self) noexcept nogil
    cpdef inline void update_loggedrelativehumidity_v1(self) noexcept nogil
    cpdef inline void calc_dailyrelativehumidity_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure_v2(self) noexcept nogil
    cpdef inline void calc_dailysaturationvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope_v2(self) noexcept nogil
    cpdef inline void calc_dailysaturationvapourpressureslope_v1(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_dailyactualvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_dryairpressure_v1(self) noexcept nogil
    cpdef inline void calc_airdensity_v1(self) noexcept nogil
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil
    cpdef inline void update_loggedsunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration_v1(self) noexcept nogil
    cpdef inline void update_loggedpossiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void update_loggedclearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil
    cpdef inline void calc_currentalbedo_v1(self) noexcept nogil
    cpdef inline void calc_currentalbedo_v2(self) noexcept nogil
    cpdef inline void calc_dailyglobalradiation_v1(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation_v1(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation_v2(self) noexcept nogil
    cpdef inline void calc_dailynetshortwaveradiation_v1(self) noexcept nogil
    cpdef inline void update_cloudcoverage_v1(self) noexcept nogil
    cpdef inline void calc_adjustedcloudcoverage_v1(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation_v1(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation_v2(self) noexcept nogil
    cpdef inline void calc_dailynetlongwaveradiation_v1(self) noexcept nogil
    cpdef inline void calc_netradiation_v1(self) noexcept nogil
    cpdef inline void calc_netradiation_v2(self) noexcept nogil
    cpdef inline void calc_dailynetradiation_v1(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v1(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v2(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v3(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v4(self) noexcept nogil
    cpdef inline void calc_psychrometricconstant_v1(self) noexcept nogil
    cpdef inline void calc_aerodynamicresistance_v1(self) noexcept nogil
    cpdef inline void calc_aerodynamicresistance_v2(self) noexcept nogil
    cpdef inline void calc_soilsurfaceresistance_v1(self) noexcept nogil
    cpdef inline void calc_dailyprecipitation_v1(self) noexcept nogil
    cpdef inline void calc_dailypotentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void update_soilresistance_v1(self) noexcept nogil
    cpdef inline void calc_landusesurfaceresistance_v1(self) noexcept nogil
    cpdef inline void calc_actualsurfaceresistance_v1(self) noexcept nogil
    cpdef inline void calc_actualsurfaceresistance_v2(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v3(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v4(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v5(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration_v3(self) noexcept nogil
    cpdef inline void update_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_interceptedwater_v1(self) noexcept nogil
    cpdef inline void calc_soilwater_v1(self) noexcept nogil
    cpdef inline void calc_snowcover_v1(self) noexcept nogil
    cpdef inline void calc_snowycanopy_v1(self) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v2(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v3(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v4(self) noexcept nogil
    cpdef inline void update_loggedwaterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_dailywaterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation_v1(self) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_v1(self) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_v2(self) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_v3(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation_v2(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_v3(self) noexcept nogil
    cpdef inline void update_soilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void update_soilevapotranspiration_v2(self) noexcept nogil
    cpdef inline void update_soilevapotranspiration_v3(self) noexcept nogil
    cpdef inline void update_loggedprecipitation_v1(self) noexcept nogil
    cpdef inline void update_loggedpotentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_potentialevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialevapotranspiration_v2(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v2(self) noexcept nogil
    cpdef double get_waterevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialwaterevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialinterceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_interceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialsoilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_adjustedwindspeed_v1(self, double h) noexcept nogil
    cpdef inline double return_saturationvapourpressure_v1(self, double airtemperature) noexcept nogil
    cpdef inline double return_saturationvapourpressureslope_v1(self, double t) noexcept nogil
    cpdef inline double return_evaporation_penmanmonteith_v1(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil
    cpdef inline double return_evaporation_penmanmonteith_v2(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_interceptedwater_intercmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilwater_soilwatermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_snowcover_snowcovermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_snowycanopy_snowycanopymodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_currentalbedo_snowalbedomodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature(self) noexcept nogil
    cpdef inline void update_loggedairtemperature(self) noexcept nogil
    cpdef inline void calc_dailyairtemperature(self) noexcept nogil
    cpdef inline void update_loggedwindspeed2m(self) noexcept nogil
    cpdef inline void calc_dailywindspeed2m(self) noexcept nogil
    cpdef inline void calc_windspeed10m(self) noexcept nogil
    cpdef inline void update_loggedrelativehumidity(self) noexcept nogil
    cpdef inline void calc_dailyrelativehumidity(self) noexcept nogil
    cpdef inline void calc_dailysaturationvapourpressure(self) noexcept nogil
    cpdef inline void calc_dailysaturationvapourpressureslope(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil
    cpdef inline void calc_dailyactualvapourpressure(self) noexcept nogil
    cpdef inline void calc_dryairpressure(self) noexcept nogil
    cpdef inline void calc_airdensity(self) noexcept nogil
    cpdef inline void process_radiationmodel(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_sunshineduration(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil
    cpdef inline void calc_globalradiation(self) noexcept nogil
    cpdef inline void update_loggedsunshineduration(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration(self) noexcept nogil
    cpdef inline void update_loggedpossiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil
    cpdef inline void update_loggedclearskysolarradiation(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil
    cpdef inline void calc_dailyglobalradiation(self) noexcept nogil
    cpdef inline void calc_dailynetshortwaveradiation(self) noexcept nogil
    cpdef inline void update_cloudcoverage(self) noexcept nogil
    cpdef inline void calc_adjustedcloudcoverage(self) noexcept nogil
    cpdef inline void calc_dailynetlongwaveradiation(self) noexcept nogil
    cpdef inline void calc_dailynetradiation(self) noexcept nogil
    cpdef inline void calc_psychrometricconstant(self) noexcept nogil
    cpdef inline void calc_soilsurfaceresistance(self) noexcept nogil
    cpdef inline void calc_dailyprecipitation(self) noexcept nogil
    cpdef inline void calc_dailypotentialsoilevapotranspiration(self) noexcept nogil
    cpdef inline void update_soilresistance(self) noexcept nogil
    cpdef inline void calc_landusesurfaceresistance(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void update_potentialevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration(self) noexcept nogil
    cpdef inline void calc_interceptedwater(self) noexcept nogil
    cpdef inline void calc_soilwater(self) noexcept nogil
    cpdef inline void calc_snowcover(self) noexcept nogil
    cpdef inline void calc_snowycanopy(self) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation(self) noexcept nogil
    cpdef inline void update_loggedwaterevaporation(self) noexcept nogil
    cpdef inline void calc_dailywaterevaporation(self) noexcept nogil
    cpdef inline void update_loggedprecipitation(self) noexcept nogil
    cpdef inline void update_loggedpotentialsoilevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil
    cpdef double get_waterevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialwaterevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialinterceptionevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_interceptionevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialsoilevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_adjustedwindspeed(self, double h) noexcept nogil
    cpdef inline double return_saturationvapourpressure(self, double airtemperature) noexcept nogil
    cpdef inline double return_saturationvapourpressureslope(self, double t) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_petmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_interceptedwater_intercmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilwater_soilwatermodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_snowcover_snowcovermodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_snowycanopy_snowycanopymodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_currentalbedo_snowalbedomodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef void determine_interceptionevaporation_v1(self) noexcept nogil
    cpdef void determine_interceptionevaporation_v2(self) noexcept nogil
    cpdef void determine_potentialinterceptionevaporation_v1(self) noexcept nogil
    cpdef void determine_soilevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_soilevapotranspiration_v2(self) noexcept nogil
    cpdef void determine_soilevapotranspiration_v3(self) noexcept nogil
    cpdef void determine_waterevaporation_v1(self) noexcept nogil
    cpdef void determine_waterevaporation_v2(self) noexcept nogil
    cpdef void determine_waterevaporation_v3(self) noexcept nogil
    cpdef void determine_potentialinterceptionevaporation(self) noexcept nogil
