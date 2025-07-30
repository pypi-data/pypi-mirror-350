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
@cython.final
cdef class ControlParameters:
    cdef public numpy.int64_t nmbhru
    cdef public double[:] hruarea
    cdef public double measuringheightwindspeed
    cdef public double[:] evapotranspirationfactor
@cython.final
cdef class DerivedParameters:
    cdef public double[:] hruareafraction
    cdef public double hours
    cdef public double days
    cdef public numpy.int64_t nmblogentries
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public LogSequences logs
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
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
    cdef public double[:] referenceevapotranspiration
    cdef public numpy.int64_t _referenceevapotranspiration_ndim
    cdef public numpy.int64_t _referenceevapotranspiration_length
    cdef public numpy.int64_t _referenceevapotranspiration_length_0
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:,:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_diskflag_reading
    cdef public bint _referenceevapotranspiration_diskflag_writing
    cdef public double[:] _referenceevapotranspiration_ncarray
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:] loggedglobalradiation
    cdef public numpy.int64_t _loggedglobalradiation_ndim
    cdef public numpy.int64_t _loggedglobalradiation_length
    cdef public numpy.int64_t _loggedglobalradiation_length_0
    cdef public double[:] loggedclearskysolarradiation
    cdef public numpy.int64_t _loggedclearskysolarradiation_ndim
    cdef public numpy.int64_t _loggedclearskysolarradiation_length
    cdef public numpy.int64_t _loggedclearskysolarradiation_length_0
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface radiationmodel
    cdef public numpy.npy_bool radiationmodel_is_mainmodel
    cdef public numpy.int64_t radiationmodel_typeid
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
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil
    cpdef inline void calc_windspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope_v1(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil
    cpdef inline void update_loggedclearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation_v1(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation_v1(self) noexcept nogil
    cpdef inline void calc_netradiation_v1(self) noexcept nogil
    cpdef inline void calc_soilheatflux_v1(self) noexcept nogil
    cpdef inline void calc_psychrometricconstant_v1(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_potentialevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void process_radiationmodel(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil
    cpdef inline void calc_globalradiation(self) noexcept nogil
    cpdef inline void calc_windspeed2m(self) noexcept nogil
    cpdef inline void calc_airtemperature(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressureslope(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil
    cpdef inline void update_loggedclearskysolarradiation(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiation(self) noexcept nogil
    cpdef inline void calc_netlongwaveradiation(self) noexcept nogil
    cpdef inline void calc_netradiation(self) noexcept nogil
    cpdef inline void calc_soilheatflux(self) noexcept nogil
    cpdef inline void calc_psychrometricconstant(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil
