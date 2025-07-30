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
    cdef public double measuringheightwindspeed
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
    cdef public double[:] wetsoilresistance
    cdef public double[:] soilresistanceincrease
    cdef public double[:] wetnessthreshold
    cdef public double[:] leafresistance
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double[:] airtemperature
    cdef public numpy.int64_t _airtemperature_ndim
    cdef public numpy.int64_t _airtemperature_length
    cdef public numpy.int64_t _airtemperature_length_0
    cdef public bint _airtemperature_ramflag
    cdef public double[:,:] _airtemperature_array
    cdef public bint _airtemperature_diskflag_reading
    cdef public bint _airtemperature_diskflag_writing
    cdef public double[:] _airtemperature_ncarray
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
    cdef public double[:] saturationvapourpressure
    cdef public numpy.int64_t _saturationvapourpressure_ndim
    cdef public numpy.int64_t _saturationvapourpressure_length
    cdef public numpy.int64_t _saturationvapourpressure_length_0
    cdef public bint _saturationvapourpressure_ramflag
    cdef public double[:,:] _saturationvapourpressure_array
    cdef public bint _saturationvapourpressure_diskflag_reading
    cdef public bint _saturationvapourpressure_diskflag_writing
    cdef public double[:] _saturationvapourpressure_ncarray
    cdef public double[:] saturationvapourpressureslope
    cdef public numpy.int64_t _saturationvapourpressureslope_ndim
    cdef public numpy.int64_t _saturationvapourpressureslope_length
    cdef public numpy.int64_t _saturationvapourpressureslope_length_0
    cdef public bint _saturationvapourpressureslope_ramflag
    cdef public double[:,:] _saturationvapourpressureslope_array
    cdef public bint _saturationvapourpressureslope_diskflag_reading
    cdef public bint _saturationvapourpressureslope_diskflag_writing
    cdef public double[:] _saturationvapourpressureslope_ncarray
    cdef public double[:] actualvapourpressure
    cdef public numpy.int64_t _actualvapourpressure_ndim
    cdef public numpy.int64_t _actualvapourpressure_length
    cdef public numpy.int64_t _actualvapourpressure_length_0
    cdef public bint _actualvapourpressure_ramflag
    cdef public double[:,:] _actualvapourpressure_array
    cdef public bint _actualvapourpressure_diskflag_reading
    cdef public bint _actualvapourpressure_diskflag_writing
    cdef public double[:] _actualvapourpressure_ncarray
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
    cdef public double[:] actualsurfaceresistance
    cdef public numpy.int64_t _actualsurfaceresistance_ndim
    cdef public numpy.int64_t _actualsurfaceresistance_length
    cdef public numpy.int64_t _actualsurfaceresistance_length_0
    cdef public bint _actualsurfaceresistance_ramflag
    cdef public double[:,:] _actualsurfaceresistance_array
    cdef public bint _actualsurfaceresistance_diskflag_reading
    cdef public bint _actualsurfaceresistance_diskflag_writing
    cdef public double[:] _actualsurfaceresistance_ncarray
    cdef public double[:] snowcover
    cdef public numpy.int64_t _snowcover_ndim
    cdef public numpy.int64_t _snowcover_length
    cdef public numpy.int64_t _snowcover_length_0
    cdef public bint _snowcover_ramflag
    cdef public double[:,:] _snowcover_array
    cdef public bint _snowcover_diskflag_reading
    cdef public bint _snowcover_diskflag_writing
    cdef public double[:] _snowcover_ncarray
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
    cdef public double[:] netshortwaveradiation
    cdef public numpy.int64_t _netshortwaveradiation_ndim
    cdef public numpy.int64_t _netshortwaveradiation_length
    cdef public numpy.int64_t _netshortwaveradiation_length_0
    cdef public bint _netshortwaveradiation_ramflag
    cdef public double[:,:] _netshortwaveradiation_array
    cdef public bint _netshortwaveradiation_diskflag_reading
    cdef public bint _netshortwaveradiation_diskflag_writing
    cdef public double[:] _netshortwaveradiation_ncarray
    cdef public double[:] netlongwaveradiation
    cdef public numpy.int64_t _netlongwaveradiation_ndim
    cdef public numpy.int64_t _netlongwaveradiation_length
    cdef public numpy.int64_t _netlongwaveradiation_length_0
    cdef public bint _netlongwaveradiation_ramflag
    cdef public double[:,:] _netlongwaveradiation_array
    cdef public bint _netlongwaveradiation_diskflag_reading
    cdef public bint _netlongwaveradiation_diskflag_writing
    cdef public double[:] _netlongwaveradiation_ncarray
    cdef public double[:] netradiation
    cdef public numpy.int64_t _netradiation_ndim
    cdef public numpy.int64_t _netradiation_length
    cdef public numpy.int64_t _netradiation_length_0
    cdef public bint _netradiation_ramflag
    cdef public double[:,:] _netradiation_array
    cdef public bint _netradiation_diskflag_reading
    cdef public bint _netradiation_diskflag_writing
    cdef public double[:] _netradiation_ncarray
    cdef public double[:] soilheatflux
    cdef public numpy.int64_t _soilheatflux_ndim
    cdef public numpy.int64_t _soilheatflux_length
    cdef public numpy.int64_t _soilheatflux_length_0
    cdef public bint _soilheatflux_ramflag
    cdef public double[:,:] _soilheatflux_array
    cdef public bint _soilheatflux_diskflag_reading
    cdef public bint _soilheatflux_diskflag_writing
    cdef public double[:] _soilheatflux_ncarray
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
    cdef public double[:] dailypotentialsoilevapotranspiration
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_ndim
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_length
    cdef public numpy.int64_t _dailypotentialsoilevapotranspiration_length_0
    cdef public bint _dailypotentialsoilevapotranspiration_ramflag
    cdef public double[:,:] _dailypotentialsoilevapotranspiration_array
    cdef public bint _dailypotentialsoilevapotranspiration_diskflag_reading
    cdef public bint _dailypotentialsoilevapotranspiration_diskflag_writing
    cdef public double[:] _dailypotentialsoilevapotranspiration_ncarray
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
    cdef public double[:,:] loggedprecipitation
    cdef public numpy.int64_t _loggedprecipitation_ndim
    cdef public numpy.int64_t _loggedprecipitation_length
    cdef public numpy.int64_t _loggedprecipitation_length_0
    cdef public numpy.int64_t _loggedprecipitation_length_1
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
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface precipmodel
    cdef public numpy.npy_bool precipmodel_is_mainmodel
    cdef public numpy.int64_t precipmodel_typeid
    cdef public masterinterface.MasterInterface radiationmodel
    cdef public numpy.npy_bool radiationmodel_is_mainmodel
    cdef public numpy.int64_t radiationmodel_typeid
    cdef public masterinterface.MasterInterface snowcovermodel
    cdef public numpy.npy_bool snowcovermodel_is_mainmodel
    cdef public numpy.int64_t snowcovermodel_typeid
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
    cpdef double get_potentialwaterevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialinterceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialsoilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil
    cpdef inline double return_adjustedwindspeed_v1(self, double h) noexcept nogil
    cpdef inline void calc_windspeed10m_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope_v1(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_dryairpressure_v1(self) noexcept nogil
    cpdef inline void calc_airdensity_v1(self) noexcept nogil
    cpdef inline void calc_currentalbedo_v2(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation_v2(self) noexcept nogil
    cpdef inline void update_cloudcoverage_v1(self) noexcept nogil
    cpdef inline void calc_adjustedcloudcoverage_v1(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation_v2(self) noexcept nogil
    cpdef inline void calc_netradiation_v1(self) noexcept nogil
    cpdef inline void calc_aerodynamicresistance_v2(self) noexcept nogil
    cpdef inline void calc_dailyprecipitation_v1(self) noexcept nogil
    cpdef inline void calc_dailypotentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void update_soilresistance_v1(self) noexcept nogil
    cpdef inline void calc_actualsurfaceresistance_v2(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef inline double return_evaporation_penmanmonteith_v2(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil
    cpdef inline void calc_snowcover_v1(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v4(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v4(self) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_snowcover_snowcovermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_v2(self) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_v1(self) noexcept nogil
    cpdef inline void update_loggedprecipitation_v1(self) noexcept nogil
    cpdef inline void update_loggedpotentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void update_loggedwaterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_dailywaterevaporation_v1(self) noexcept nogil
    cpdef double get_potentialwaterevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialinterceptionevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_potentialsoilevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef inline void process_radiationmodel(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_sunshineduration(self) noexcept nogil
    cpdef inline void calc_globalradiation(self) noexcept nogil
    cpdef inline void calc_airtemperature(self) noexcept nogil
    cpdef inline double return_adjustedwindspeed(self, double h) noexcept nogil
    cpdef inline void calc_windspeed10m(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil
    cpdef inline void calc_dryairpressure(self) noexcept nogil
    cpdef inline void calc_airdensity(self) noexcept nogil
    cpdef inline void calc_currentalbedo(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation(self) noexcept nogil
    cpdef inline void update_cloudcoverage(self) noexcept nogil
    cpdef inline void calc_adjustedcloudcoverage(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation(self) noexcept nogil
    cpdef inline void calc_netradiation(self) noexcept nogil
    cpdef inline void calc_aerodynamicresistance(self) noexcept nogil
    cpdef inline void calc_dailyprecipitation(self) noexcept nogil
    cpdef inline void calc_dailypotentialsoilevapotranspiration(self) noexcept nogil
    cpdef inline void update_soilresistance(self) noexcept nogil
    cpdef inline void calc_actualsurfaceresistance(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration(self) noexcept nogil
    cpdef inline double return_evaporation_penmanmonteith(self, numpy.int64_t k, double actualsurfaceresistance) noexcept nogil
    cpdef inline void calc_snowcover(self) noexcept nogil
    cpdef inline void calc_soilheatflux(self) noexcept nogil
    cpdef inline void calc_waterevaporation(self) noexcept nogil
    cpdef inline void calc_snowcover_snowcovermodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation(self) noexcept nogil
    cpdef inline void calc_precipitation(self) noexcept nogil
    cpdef inline void update_loggedprecipitation(self) noexcept nogil
    cpdef inline void update_loggedpotentialsoilevapotranspiration(self) noexcept nogil
    cpdef inline void update_loggedwaterevaporation(self) noexcept nogil
    cpdef inline void calc_dailywaterevaporation(self) noexcept nogil
    cpdef void determine_potentialinterceptionevaporation_v1(self) noexcept nogil
    cpdef void determine_potentialsoilevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialwaterevaporation_v1(self) noexcept nogil
    cpdef void determine_potentialinterceptionevaporation(self) noexcept nogil
    cpdef void determine_potentialsoilevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialwaterevaporation(self) noexcept nogil
