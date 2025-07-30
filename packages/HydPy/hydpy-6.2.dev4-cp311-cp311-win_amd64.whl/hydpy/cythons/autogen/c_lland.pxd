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
cdef public numpy.int64_t SIED_D = 1
cdef public numpy.int64_t SIED_L = 2
cdef public numpy.int64_t VERS = 3
cdef public numpy.int64_t ACKER = 4
cdef public numpy.int64_t WEINB = 5
cdef public numpy.int64_t OBSTB = 6
cdef public numpy.int64_t BODEN = 7
cdef public numpy.int64_t GLETS = 8
cdef public numpy.int64_t GRUE_I = 9
cdef public numpy.int64_t FEUCHT = 10
cdef public numpy.int64_t GRUE_E = 11
cdef public numpy.int64_t BAUMB = 12
cdef public numpy.int64_t NADELW = 13
cdef public numpy.int64_t LAUBW = 14
cdef public numpy.int64_t MISCHW = 15
cdef public numpy.int64_t WASSER = 16
cdef public numpy.int64_t FLUSS = 17
cdef public numpy.int64_t SEE = 18
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
@cython.final
cdef class ControlParameters:
    cdef public double ft
    cdef public numpy.int64_t nhru
    cdef public numpy.int64_t[:] lnk
    cdef public double[:] fhru
    cdef public double[:] kg
    cdef public double[:] kt
    cdef public double p1strahl
    cdef public double p2strahl
    cdef public double albedo0snow
    cdef public double snowagingfactor
    cdef public double turb0
    cdef public double turb1
    cdef public double measuringheightwindspeed
    cdef public double p1wind
    cdef public double p2wind
    cdef public double[:,:] lai
    cdef public numpy.int64_t _lai_rowmin
    cdef public numpy.int64_t _lai_columnmin
    cdef public double hinz
    cdef public double p1simax
    cdef public double p2simax
    cdef public double p1sirate
    cdef public double p2sirate
    cdef public double p3sirate
    cdef public double[:] treft
    cdef public double[:] trefn
    cdef public double[:] tgr
    cdef public double[:] tsp
    cdef public double[:] gtf
    cdef public double[:] pwmax
    cdef public numpy.int64_t refreezeflag
    cdef public double ktschnee
    cdef public double[:] wg2z
    cdef public numpy.int64_t _wg2z_entrymin
    cdef public double[:] wmax
    cdef public double[:] fk
    cdef public double[:] pwp
    cdef public double[:] bsf
    cdef public double fvf
    cdef public double bsff
    cdef public double[:] dmin
    cdef public double[:] dmax
    cdef public double[:] beta
    cdef public double[:] fbeta
    cdef public double[:] kapmax
    cdef public double[:,:] kapgrenz
    cdef public numpy.npy_bool rbeta
    cdef public double volbmax
    cdef public double gsbmax
    cdef public double gsbgrad1
    cdef public double gsbgrad2
    cdef public double a1
    cdef public double a2
    cdef public double tind
    cdef public double eqb
    cdef public double eqi1
    cdef public double eqi2
    cdef public double eqd1
    cdef public double eqd2
    cdef public numpy.npy_bool negq
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public double seconds
    cdef public numpy.int64_t nmblogentries
    cdef public double[:] absfhru
    cdef public double[:,:] kinz
    cdef public numpy.int64_t _kinz_rowmin
    cdef public numpy.int64_t _kinz_columnmin
    cdef public double[:] heatoffusion
    cdef public double[:,:] fr
    cdef public numpy.int64_t _fr_rowmin
    cdef public numpy.int64_t _fr_columnmin
    cdef public double kb
    cdef public double ki1
    cdef public double ki2
    cdef public double kd1
    cdef public double kd2
    cdef public double qfactor
@cython.final
cdef class FixedParameters:
    cdef public double cpwasser
    cdef public double cpeis
    cdef public double rschmelz
    cdef public double z
    cdef public double[:] bowa2z
    cdef public double lambdag
    cdef public double sigma
    cdef public double lwe
    cdef public double psyinv
    cdef public double z0
    cdef public double fratm
    cdef public double cg
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences:
    cdef public double[:] q
    cdef public numpy.int64_t _q_ndim
    cdef public numpy.int64_t _q_length
    cdef public numpy.int64_t _q_length_0
    cdef public bint _q_ramflag
    cdef public double[:,:] _q_array
    cdef public bint _q_diskflag_reading
    cdef public bint _q_diskflag_writing
    cdef public double[:] _q_ncarray
    cdef double **_q_pointer
    cdef public numpy.int64_t len_q
    cdef public numpy.int64_t[:] _q_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class InputSequences:
    cdef public double nied
    cdef public numpy.int64_t _nied_ndim
    cdef public numpy.int64_t _nied_length
    cdef public bint _nied_ramflag
    cdef public double[:] _nied_array
    cdef public bint _nied_diskflag_reading
    cdef public bint _nied_diskflag_writing
    cdef public double[:] _nied_ncarray
    cdef public bint _nied_inputflag
    cdef double *_nied_inputpointer
    cdef public double teml
    cdef public numpy.int64_t _teml_ndim
    cdef public numpy.int64_t _teml_length
    cdef public bint _teml_ramflag
    cdef public double[:] _teml_array
    cdef public bint _teml_diskflag_reading
    cdef public bint _teml_diskflag_writing
    cdef public double[:] _teml_ncarray
    cdef public bint _teml_inputflag
    cdef double *_teml_inputpointer
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double qz
    cdef public numpy.int64_t _qz_ndim
    cdef public numpy.int64_t _qz_length
    cdef public bint _qz_ramflag
    cdef public double[:] _qz_array
    cdef public bint _qz_diskflag_reading
    cdef public bint _qz_diskflag_writing
    cdef public double[:] _qz_ncarray
    cdef public bint _qz_outputflag
    cdef double *_qz_outputpointer
    cdef public double qzh
    cdef public numpy.int64_t _qzh_ndim
    cdef public numpy.int64_t _qzh_length
    cdef public bint _qzh_ramflag
    cdef public double[:] _qzh_array
    cdef public bint _qzh_diskflag_reading
    cdef public bint _qzh_diskflag_writing
    cdef public double[:] _qzh_ncarray
    cdef public bint _qzh_outputflag
    cdef double *_qzh_outputpointer
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
    cdef public double[:] nkor
    cdef public numpy.int64_t _nkor_ndim
    cdef public numpy.int64_t _nkor_length
    cdef public numpy.int64_t _nkor_length_0
    cdef public bint _nkor_ramflag
    cdef public double[:,:] _nkor_array
    cdef public bint _nkor_diskflag_reading
    cdef public bint _nkor_diskflag_writing
    cdef public double[:] _nkor_ncarray
    cdef public double[:] tkor
    cdef public numpy.int64_t _tkor_ndim
    cdef public numpy.int64_t _tkor_length
    cdef public numpy.int64_t _tkor_length_0
    cdef public bint _tkor_ramflag
    cdef public double[:,:] _tkor_array
    cdef public bint _tkor_diskflag_reading
    cdef public bint _tkor_diskflag_writing
    cdef public double[:] _tkor_ncarray
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
    cdef public double[:] reducedwindspeed2m
    cdef public numpy.int64_t _reducedwindspeed2m_ndim
    cdef public numpy.int64_t _reducedwindspeed2m_length
    cdef public numpy.int64_t _reducedwindspeed2m_length_0
    cdef public bint _reducedwindspeed2m_ramflag
    cdef public double[:,:] _reducedwindspeed2m_array
    cdef public bint _reducedwindspeed2m_diskflag_reading
    cdef public bint _reducedwindspeed2m_diskflag_writing
    cdef public double[:] _reducedwindspeed2m_ncarray
    cdef public double[:] saturationvapourpressure
    cdef public numpy.int64_t _saturationvapourpressure_ndim
    cdef public numpy.int64_t _saturationvapourpressure_length
    cdef public numpy.int64_t _saturationvapourpressure_length_0
    cdef public bint _saturationvapourpressure_ramflag
    cdef public double[:,:] _saturationvapourpressure_array
    cdef public bint _saturationvapourpressure_diskflag_reading
    cdef public bint _saturationvapourpressure_diskflag_writing
    cdef public double[:] _saturationvapourpressure_ncarray
    cdef public double[:] saturationvapourpressureinz
    cdef public numpy.int64_t _saturationvapourpressureinz_ndim
    cdef public numpy.int64_t _saturationvapourpressureinz_length
    cdef public numpy.int64_t _saturationvapourpressureinz_length_0
    cdef public bint _saturationvapourpressureinz_ramflag
    cdef public double[:,:] _saturationvapourpressureinz_array
    cdef public bint _saturationvapourpressureinz_diskflag_reading
    cdef public bint _saturationvapourpressureinz_diskflag_writing
    cdef public double[:] _saturationvapourpressureinz_ncarray
    cdef public double[:] saturationvapourpressuresnow
    cdef public numpy.int64_t _saturationvapourpressuresnow_ndim
    cdef public numpy.int64_t _saturationvapourpressuresnow_length
    cdef public numpy.int64_t _saturationvapourpressuresnow_length_0
    cdef public bint _saturationvapourpressuresnow_ramflag
    cdef public double[:,:] _saturationvapourpressuresnow_array
    cdef public bint _saturationvapourpressuresnow_diskflag_reading
    cdef public bint _saturationvapourpressuresnow_diskflag_writing
    cdef public double[:] _saturationvapourpressuresnow_ncarray
    cdef public double[:] actualvapourpressure
    cdef public numpy.int64_t _actualvapourpressure_ndim
    cdef public numpy.int64_t _actualvapourpressure_length
    cdef public numpy.int64_t _actualvapourpressure_length_0
    cdef public bint _actualvapourpressure_ramflag
    cdef public double[:,:] _actualvapourpressure_array
    cdef public bint _actualvapourpressure_diskflag_reading
    cdef public bint _actualvapourpressure_diskflag_writing
    cdef public double[:] _actualvapourpressure_ncarray
    cdef public double[:] tz
    cdef public numpy.int64_t _tz_ndim
    cdef public numpy.int64_t _tz_length
    cdef public numpy.int64_t _tz_length_0
    cdef public bint _tz_ramflag
    cdef public double[:,:] _tz_array
    cdef public bint _tz_diskflag_reading
    cdef public bint _tz_diskflag_writing
    cdef public double[:] _tz_ncarray
    cdef public double[:] wg
    cdef public numpy.int64_t _wg_ndim
    cdef public numpy.int64_t _wg_length
    cdef public numpy.int64_t _wg_length_0
    cdef public bint _wg_ramflag
    cdef public double[:,:] _wg_array
    cdef public bint _wg_diskflag_reading
    cdef public bint _wg_diskflag_writing
    cdef public double[:] _wg_ncarray
    cdef public double[:] netshortwaveradiationinz
    cdef public numpy.int64_t _netshortwaveradiationinz_ndim
    cdef public numpy.int64_t _netshortwaveradiationinz_length
    cdef public numpy.int64_t _netshortwaveradiationinz_length_0
    cdef public bint _netshortwaveradiationinz_ramflag
    cdef public double[:,:] _netshortwaveradiationinz_array
    cdef public bint _netshortwaveradiationinz_diskflag_reading
    cdef public bint _netshortwaveradiationinz_diskflag_writing
    cdef public double[:] _netshortwaveradiationinz_ncarray
    cdef public double[:] netshortwaveradiationsnow
    cdef public numpy.int64_t _netshortwaveradiationsnow_ndim
    cdef public numpy.int64_t _netshortwaveradiationsnow_length
    cdef public numpy.int64_t _netshortwaveradiationsnow_length_0
    cdef public bint _netshortwaveradiationsnow_ramflag
    cdef public double[:,:] _netshortwaveradiationsnow_array
    cdef public bint _netshortwaveradiationsnow_diskflag_reading
    cdef public bint _netshortwaveradiationsnow_diskflag_writing
    cdef public double[:] _netshortwaveradiationsnow_ncarray
    cdef public double[:] netlongwaveradiationinz
    cdef public numpy.int64_t _netlongwaveradiationinz_ndim
    cdef public numpy.int64_t _netlongwaveradiationinz_length
    cdef public numpy.int64_t _netlongwaveradiationinz_length_0
    cdef public bint _netlongwaveradiationinz_ramflag
    cdef public double[:,:] _netlongwaveradiationinz_array
    cdef public bint _netlongwaveradiationinz_diskflag_reading
    cdef public bint _netlongwaveradiationinz_diskflag_writing
    cdef public double[:] _netlongwaveradiationinz_ncarray
    cdef public double[:] netlongwaveradiationsnow
    cdef public numpy.int64_t _netlongwaveradiationsnow_ndim
    cdef public numpy.int64_t _netlongwaveradiationsnow_length
    cdef public numpy.int64_t _netlongwaveradiationsnow_length_0
    cdef public bint _netlongwaveradiationsnow_ramflag
    cdef public double[:,:] _netlongwaveradiationsnow_array
    cdef public bint _netlongwaveradiationsnow_diskflag_reading
    cdef public bint _netlongwaveradiationsnow_diskflag_writing
    cdef public double[:] _netlongwaveradiationsnow_ncarray
    cdef public double[:] netradiationinz
    cdef public numpy.int64_t _netradiationinz_ndim
    cdef public numpy.int64_t _netradiationinz_length
    cdef public numpy.int64_t _netradiationinz_length_0
    cdef public bint _netradiationinz_ramflag
    cdef public double[:,:] _netradiationinz_array
    cdef public bint _netradiationinz_diskflag_reading
    cdef public bint _netradiationinz_diskflag_writing
    cdef public double[:] _netradiationinz_ncarray
    cdef public double[:] netradiationsnow
    cdef public numpy.int64_t _netradiationsnow_ndim
    cdef public numpy.int64_t _netradiationsnow_length
    cdef public numpy.int64_t _netradiationsnow_length_0
    cdef public bint _netradiationsnow_ramflag
    cdef public double[:,:] _netradiationsnow_array
    cdef public bint _netradiationsnow_diskflag_reading
    cdef public bint _netradiationsnow_diskflag_writing
    cdef public double[:] _netradiationsnow_ncarray
    cdef public double[:] nbes
    cdef public numpy.int64_t _nbes_ndim
    cdef public numpy.int64_t _nbes_length
    cdef public numpy.int64_t _nbes_length_0
    cdef public bint _nbes_ramflag
    cdef public double[:,:] _nbes_array
    cdef public bint _nbes_diskflag_reading
    cdef public bint _nbes_diskflag_writing
    cdef public double[:] _nbes_ncarray
    cdef public double[:] sbes
    cdef public numpy.int64_t _sbes_ndim
    cdef public numpy.int64_t _sbes_length
    cdef public numpy.int64_t _sbes_length_0
    cdef public bint _sbes_ramflag
    cdef public double[:,:] _sbes_array
    cdef public bint _sbes_diskflag_reading
    cdef public bint _sbes_diskflag_writing
    cdef public double[:] _sbes_ncarray
    cdef public double[:] snowintmax
    cdef public numpy.int64_t _snowintmax_ndim
    cdef public numpy.int64_t _snowintmax_length
    cdef public numpy.int64_t _snowintmax_length_0
    cdef public bint _snowintmax_ramflag
    cdef public double[:,:] _snowintmax_array
    cdef public bint _snowintmax_diskflag_reading
    cdef public bint _snowintmax_diskflag_writing
    cdef public double[:] _snowintmax_ncarray
    cdef public double[:] snowintrate
    cdef public numpy.int64_t _snowintrate_ndim
    cdef public numpy.int64_t _snowintrate_length
    cdef public numpy.int64_t _snowintrate_length_0
    cdef public bint _snowintrate_ramflag
    cdef public double[:,:] _snowintrate_array
    cdef public bint _snowintrate_diskflag_reading
    cdef public bint _snowintrate_diskflag_writing
    cdef public double[:] _snowintrate_ncarray
    cdef public double[:] nbesinz
    cdef public numpy.int64_t _nbesinz_ndim
    cdef public numpy.int64_t _nbesinz_length
    cdef public numpy.int64_t _nbesinz_length_0
    cdef public bint _nbesinz_ramflag
    cdef public double[:,:] _nbesinz_array
    cdef public bint _nbesinz_diskflag_reading
    cdef public bint _nbesinz_diskflag_writing
    cdef public double[:] _nbesinz_ncarray
    cdef public double[:] sbesinz
    cdef public numpy.int64_t _sbesinz_ndim
    cdef public numpy.int64_t _sbesinz_length
    cdef public numpy.int64_t _sbesinz_length_0
    cdef public bint _sbesinz_ramflag
    cdef public double[:,:] _sbesinz_array
    cdef public bint _sbesinz_diskflag_reading
    cdef public bint _sbesinz_diskflag_writing
    cdef public double[:] _sbesinz_ncarray
    cdef public double[:] wniedinz
    cdef public numpy.int64_t _wniedinz_ndim
    cdef public numpy.int64_t _wniedinz_length
    cdef public numpy.int64_t _wniedinz_length_0
    cdef public bint _wniedinz_ramflag
    cdef public double[:,:] _wniedinz_array
    cdef public bint _wniedinz_diskflag_reading
    cdef public bint _wniedinz_diskflag_writing
    cdef public double[:] _wniedinz_ncarray
    cdef public double[:] actualalbedoinz
    cdef public numpy.int64_t _actualalbedoinz_ndim
    cdef public numpy.int64_t _actualalbedoinz_length
    cdef public numpy.int64_t _actualalbedoinz_length_0
    cdef public bint _actualalbedoinz_ramflag
    cdef public double[:,:] _actualalbedoinz_array
    cdef public bint _actualalbedoinz_diskflag_reading
    cdef public bint _actualalbedoinz_diskflag_writing
    cdef public double[:] _actualalbedoinz_ncarray
    cdef public double[:] wadainz
    cdef public numpy.int64_t _wadainz_ndim
    cdef public numpy.int64_t _wadainz_length
    cdef public numpy.int64_t _wadainz_length_0
    cdef public bint _wadainz_ramflag
    cdef public double[:,:] _wadainz_array
    cdef public bint _wadainz_diskflag_reading
    cdef public bint _wadainz_diskflag_writing
    cdef public double[:] _wadainz_ncarray
    cdef public double[:] schmpotinz
    cdef public numpy.int64_t _schmpotinz_ndim
    cdef public numpy.int64_t _schmpotinz_length
    cdef public numpy.int64_t _schmpotinz_length_0
    cdef public bint _schmpotinz_ramflag
    cdef public double[:,:] _schmpotinz_array
    cdef public bint _schmpotinz_diskflag_reading
    cdef public bint _schmpotinz_diskflag_writing
    cdef public double[:] _schmpotinz_ncarray
    cdef public double[:] schminz
    cdef public numpy.int64_t _schminz_ndim
    cdef public numpy.int64_t _schminz_length
    cdef public numpy.int64_t _schminz_length_0
    cdef public bint _schminz_ramflag
    cdef public double[:,:] _schminz_array
    cdef public bint _schminz_diskflag_reading
    cdef public bint _schminz_diskflag_writing
    cdef public double[:] _schminz_ncarray
    cdef public double[:] gefrpotinz
    cdef public numpy.int64_t _gefrpotinz_ndim
    cdef public numpy.int64_t _gefrpotinz_length
    cdef public numpy.int64_t _gefrpotinz_length_0
    cdef public bint _gefrpotinz_ramflag
    cdef public double[:,:] _gefrpotinz_array
    cdef public bint _gefrpotinz_diskflag_reading
    cdef public bint _gefrpotinz_diskflag_writing
    cdef public double[:] _gefrpotinz_ncarray
    cdef public double[:] gefrinz
    cdef public numpy.int64_t _gefrinz_ndim
    cdef public numpy.int64_t _gefrinz_length
    cdef public numpy.int64_t _gefrinz_length_0
    cdef public bint _gefrinz_ramflag
    cdef public double[:,:] _gefrinz_array
    cdef public bint _gefrinz_diskflag_reading
    cdef public bint _gefrinz_diskflag_writing
    cdef public double[:] _gefrinz_ncarray
    cdef public double[:] evsinz
    cdef public numpy.int64_t _evsinz_ndim
    cdef public numpy.int64_t _evsinz_length
    cdef public numpy.int64_t _evsinz_length_0
    cdef public bint _evsinz_ramflag
    cdef public double[:,:] _evsinz_array
    cdef public bint _evsinz_diskflag_reading
    cdef public bint _evsinz_diskflag_writing
    cdef public double[:] _evsinz_ncarray
    cdef public double[:] evi
    cdef public numpy.int64_t _evi_ndim
    cdef public numpy.int64_t _evi_length
    cdef public numpy.int64_t _evi_length_0
    cdef public bint _evi_ramflag
    cdef public double[:,:] _evi_array
    cdef public bint _evi_diskflag_reading
    cdef public bint _evi_diskflag_writing
    cdef public double[:] _evi_ncarray
    cdef public double[:] evb
    cdef public numpy.int64_t _evb_ndim
    cdef public numpy.int64_t _evb_length
    cdef public numpy.int64_t _evb_length_0
    cdef public bint _evb_ramflag
    cdef public double[:,:] _evb_array
    cdef public bint _evb_diskflag_reading
    cdef public bint _evb_diskflag_writing
    cdef public double[:] _evb_ncarray
    cdef public double[:] evs
    cdef public numpy.int64_t _evs_ndim
    cdef public numpy.int64_t _evs_length
    cdef public numpy.int64_t _evs_length_0
    cdef public bint _evs_ramflag
    cdef public double[:,:] _evs_array
    cdef public bint _evs_diskflag_reading
    cdef public bint _evs_diskflag_writing
    cdef public double[:] _evs_ncarray
    cdef public double[:] wgtf
    cdef public numpy.int64_t _wgtf_ndim
    cdef public numpy.int64_t _wgtf_length
    cdef public numpy.int64_t _wgtf_length_0
    cdef public bint _wgtf_ramflag
    cdef public double[:,:] _wgtf_array
    cdef public bint _wgtf_diskflag_reading
    cdef public bint _wgtf_diskflag_writing
    cdef public double[:] _wgtf_ncarray
    cdef public double[:] wnied
    cdef public numpy.int64_t _wnied_ndim
    cdef public numpy.int64_t _wnied_length
    cdef public numpy.int64_t _wnied_length_0
    cdef public bint _wnied_ramflag
    cdef public double[:,:] _wnied_array
    cdef public bint _wnied_diskflag_reading
    cdef public bint _wnied_diskflag_writing
    cdef public double[:] _wnied_ncarray
    cdef public double[:] tempssurface
    cdef public numpy.int64_t _tempssurface_ndim
    cdef public numpy.int64_t _tempssurface_length
    cdef public numpy.int64_t _tempssurface_length_0
    cdef public bint _tempssurface_ramflag
    cdef public double[:,:] _tempssurface_array
    cdef public bint _tempssurface_diskflag_reading
    cdef public bint _tempssurface_diskflag_writing
    cdef public double[:] _tempssurface_ncarray
    cdef public double[:] actualalbedo
    cdef public numpy.int64_t _actualalbedo_ndim
    cdef public numpy.int64_t _actualalbedo_length
    cdef public numpy.int64_t _actualalbedo_length_0
    cdef public bint _actualalbedo_ramflag
    cdef public double[:,:] _actualalbedo_array
    cdef public bint _actualalbedo_diskflag_reading
    cdef public bint _actualalbedo_diskflag_writing
    cdef public double[:] _actualalbedo_ncarray
    cdef public double[:] schmpot
    cdef public numpy.int64_t _schmpot_ndim
    cdef public numpy.int64_t _schmpot_length
    cdef public numpy.int64_t _schmpot_length_0
    cdef public bint _schmpot_ramflag
    cdef public double[:,:] _schmpot_array
    cdef public bint _schmpot_diskflag_reading
    cdef public bint _schmpot_diskflag_writing
    cdef public double[:] _schmpot_ncarray
    cdef public double[:] schm
    cdef public numpy.int64_t _schm_ndim
    cdef public numpy.int64_t _schm_length
    cdef public numpy.int64_t _schm_length_0
    cdef public bint _schm_ramflag
    cdef public double[:,:] _schm_array
    cdef public bint _schm_diskflag_reading
    cdef public bint _schm_diskflag_writing
    cdef public double[:] _schm_ncarray
    cdef public double[:] gefrpot
    cdef public numpy.int64_t _gefrpot_ndim
    cdef public numpy.int64_t _gefrpot_length
    cdef public numpy.int64_t _gefrpot_length_0
    cdef public bint _gefrpot_ramflag
    cdef public double[:,:] _gefrpot_array
    cdef public bint _gefrpot_diskflag_reading
    cdef public bint _gefrpot_diskflag_writing
    cdef public double[:] _gefrpot_ncarray
    cdef public double[:] gefr
    cdef public numpy.int64_t _gefr_ndim
    cdef public numpy.int64_t _gefr_length
    cdef public numpy.int64_t _gefr_length_0
    cdef public bint _gefr_ramflag
    cdef public double[:,:] _gefr_array
    cdef public bint _gefr_diskflag_reading
    cdef public bint _gefr_diskflag_writing
    cdef public double[:] _gefr_ncarray
    cdef public double[:] wlatinz
    cdef public numpy.int64_t _wlatinz_ndim
    cdef public numpy.int64_t _wlatinz_length
    cdef public numpy.int64_t _wlatinz_length_0
    cdef public bint _wlatinz_ramflag
    cdef public double[:,:] _wlatinz_array
    cdef public bint _wlatinz_diskflag_reading
    cdef public bint _wlatinz_diskflag_writing
    cdef public double[:] _wlatinz_ncarray
    cdef public double[:] wlatsnow
    cdef public numpy.int64_t _wlatsnow_ndim
    cdef public numpy.int64_t _wlatsnow_length
    cdef public numpy.int64_t _wlatsnow_length_0
    cdef public bint _wlatsnow_ramflag
    cdef public double[:,:] _wlatsnow_array
    cdef public bint _wlatsnow_diskflag_reading
    cdef public bint _wlatsnow_diskflag_writing
    cdef public double[:] _wlatsnow_ncarray
    cdef public double[:] wsensinz
    cdef public numpy.int64_t _wsensinz_ndim
    cdef public numpy.int64_t _wsensinz_length
    cdef public numpy.int64_t _wsensinz_length_0
    cdef public bint _wsensinz_ramflag
    cdef public double[:,:] _wsensinz_array
    cdef public bint _wsensinz_diskflag_reading
    cdef public bint _wsensinz_diskflag_writing
    cdef public double[:] _wsensinz_ncarray
    cdef public double[:] wsenssnow
    cdef public numpy.int64_t _wsenssnow_ndim
    cdef public numpy.int64_t _wsenssnow_length
    cdef public numpy.int64_t _wsenssnow_length_0
    cdef public bint _wsenssnow_ramflag
    cdef public double[:,:] _wsenssnow_array
    cdef public bint _wsenssnow_diskflag_reading
    cdef public bint _wsenssnow_diskflag_writing
    cdef public double[:] _wsenssnow_ncarray
    cdef public double[:] wsurfinz
    cdef public numpy.int64_t _wsurfinz_ndim
    cdef public numpy.int64_t _wsurfinz_length
    cdef public numpy.int64_t _wsurfinz_length_0
    cdef public bint _wsurfinz_ramflag
    cdef public double[:,:] _wsurfinz_array
    cdef public bint _wsurfinz_diskflag_reading
    cdef public bint _wsurfinz_diskflag_writing
    cdef public double[:] _wsurfinz_ncarray
    cdef public double[:] wsurf
    cdef public numpy.int64_t _wsurf_ndim
    cdef public numpy.int64_t _wsurf_length
    cdef public numpy.int64_t _wsurf_length_0
    cdef public bint _wsurf_ramflag
    cdef public double[:,:] _wsurf_array
    cdef public bint _wsurf_diskflag_reading
    cdef public bint _wsurf_diskflag_writing
    cdef public double[:] _wsurf_ncarray
    cdef public double[:] sff
    cdef public numpy.int64_t _sff_ndim
    cdef public numpy.int64_t _sff_length
    cdef public numpy.int64_t _sff_length_0
    cdef public bint _sff_ramflag
    cdef public double[:,:] _sff_array
    cdef public bint _sff_diskflag_reading
    cdef public bint _sff_diskflag_writing
    cdef public double[:] _sff_ncarray
    cdef public double[:] fvg
    cdef public numpy.int64_t _fvg_ndim
    cdef public numpy.int64_t _fvg_length
    cdef public numpy.int64_t _fvg_length_0
    cdef public bint _fvg_ramflag
    cdef public double[:,:] _fvg_array
    cdef public bint _fvg_diskflag_reading
    cdef public bint _fvg_diskflag_writing
    cdef public double[:] _fvg_ncarray
    cdef public double[:] wada
    cdef public numpy.int64_t _wada_ndim
    cdef public numpy.int64_t _wada_length
    cdef public numpy.int64_t _wada_length_0
    cdef public bint _wada_ramflag
    cdef public double[:,:] _wada_array
    cdef public bint _wada_diskflag_reading
    cdef public bint _wada_diskflag_writing
    cdef public double[:] _wada_ncarray
    cdef public double[:] qdb
    cdef public numpy.int64_t _qdb_ndim
    cdef public numpy.int64_t _qdb_length
    cdef public numpy.int64_t _qdb_length_0
    cdef public bint _qdb_ramflag
    cdef public double[:,:] _qdb_array
    cdef public bint _qdb_diskflag_reading
    cdef public bint _qdb_diskflag_writing
    cdef public double[:] _qdb_ncarray
    cdef public double[:] qib1
    cdef public numpy.int64_t _qib1_ndim
    cdef public numpy.int64_t _qib1_length
    cdef public numpy.int64_t _qib1_length_0
    cdef public bint _qib1_ramflag
    cdef public double[:,:] _qib1_array
    cdef public bint _qib1_diskflag_reading
    cdef public bint _qib1_diskflag_writing
    cdef public double[:] _qib1_ncarray
    cdef public double[:] qib2
    cdef public numpy.int64_t _qib2_ndim
    cdef public numpy.int64_t _qib2_length
    cdef public numpy.int64_t _qib2_length_0
    cdef public bint _qib2_ramflag
    cdef public double[:,:] _qib2_array
    cdef public bint _qib2_diskflag_reading
    cdef public bint _qib2_diskflag_writing
    cdef public double[:] _qib2_ncarray
    cdef public double[:] qbb
    cdef public numpy.int64_t _qbb_ndim
    cdef public numpy.int64_t _qbb_length
    cdef public numpy.int64_t _qbb_length_0
    cdef public bint _qbb_ramflag
    cdef public double[:,:] _qbb_array
    cdef public bint _qbb_diskflag_reading
    cdef public bint _qbb_diskflag_writing
    cdef public double[:] _qbb_ncarray
    cdef public double[:] qkap
    cdef public numpy.int64_t _qkap_ndim
    cdef public numpy.int64_t _qkap_length
    cdef public numpy.int64_t _qkap_length_0
    cdef public bint _qkap_ramflag
    cdef public double[:,:] _qkap_array
    cdef public bint _qkap_diskflag_reading
    cdef public bint _qkap_diskflag_writing
    cdef public double[:] _qkap_ncarray
    cdef public double qdgz
    cdef public numpy.int64_t _qdgz_ndim
    cdef public numpy.int64_t _qdgz_length
    cdef public bint _qdgz_ramflag
    cdef public double[:] _qdgz_array
    cdef public bint _qdgz_diskflag_reading
    cdef public bint _qdgz_diskflag_writing
    cdef public double[:] _qdgz_ncarray
    cdef public bint _qdgz_outputflag
    cdef double *_qdgz_outputpointer
    cdef public double qdgz1
    cdef public numpy.int64_t _qdgz1_ndim
    cdef public numpy.int64_t _qdgz1_length
    cdef public bint _qdgz1_ramflag
    cdef public double[:] _qdgz1_array
    cdef public bint _qdgz1_diskflag_reading
    cdef public bint _qdgz1_diskflag_writing
    cdef public double[:] _qdgz1_ncarray
    cdef public bint _qdgz1_outputflag
    cdef double *_qdgz1_outputpointer
    cdef public double qdgz2
    cdef public numpy.int64_t _qdgz2_ndim
    cdef public numpy.int64_t _qdgz2_length
    cdef public bint _qdgz2_ramflag
    cdef public double[:] _qdgz2_array
    cdef public bint _qdgz2_diskflag_reading
    cdef public bint _qdgz2_diskflag_writing
    cdef public double[:] _qdgz2_ncarray
    cdef public bint _qdgz2_outputflag
    cdef double *_qdgz2_outputpointer
    cdef public double qigz1
    cdef public numpy.int64_t _qigz1_ndim
    cdef public numpy.int64_t _qigz1_length
    cdef public bint _qigz1_ramflag
    cdef public double[:] _qigz1_array
    cdef public bint _qigz1_diskflag_reading
    cdef public bint _qigz1_diskflag_writing
    cdef public double[:] _qigz1_ncarray
    cdef public bint _qigz1_outputflag
    cdef double *_qigz1_outputpointer
    cdef public double qigz2
    cdef public numpy.int64_t _qigz2_ndim
    cdef public numpy.int64_t _qigz2_length
    cdef public bint _qigz2_ramflag
    cdef public double[:] _qigz2_array
    cdef public bint _qigz2_diskflag_reading
    cdef public bint _qigz2_diskflag_writing
    cdef public double[:] _qigz2_ncarray
    cdef public bint _qigz2_outputflag
    cdef double *_qigz2_outputpointer
    cdef public double qbgz
    cdef public numpy.int64_t _qbgz_ndim
    cdef public numpy.int64_t _qbgz_length
    cdef public bint _qbgz_ramflag
    cdef public double[:] _qbgz_array
    cdef public bint _qbgz_diskflag_reading
    cdef public bint _qbgz_diskflag_writing
    cdef public double[:] _qbgz_ncarray
    cdef public bint _qbgz_outputflag
    cdef double *_qbgz_outputpointer
    cdef public double qdga1
    cdef public numpy.int64_t _qdga1_ndim
    cdef public numpy.int64_t _qdga1_length
    cdef public bint _qdga1_ramflag
    cdef public double[:] _qdga1_array
    cdef public bint _qdga1_diskflag_reading
    cdef public bint _qdga1_diskflag_writing
    cdef public double[:] _qdga1_ncarray
    cdef public bint _qdga1_outputflag
    cdef double *_qdga1_outputpointer
    cdef public double qdga2
    cdef public numpy.int64_t _qdga2_ndim
    cdef public numpy.int64_t _qdga2_length
    cdef public bint _qdga2_ramflag
    cdef public double[:] _qdga2_array
    cdef public bint _qdga2_diskflag_reading
    cdef public bint _qdga2_diskflag_writing
    cdef public double[:] _qdga2_ncarray
    cdef public bint _qdga2_outputflag
    cdef double *_qdga2_outputpointer
    cdef public double qiga1
    cdef public numpy.int64_t _qiga1_ndim
    cdef public numpy.int64_t _qiga1_length
    cdef public bint _qiga1_ramflag
    cdef public double[:] _qiga1_array
    cdef public bint _qiga1_diskflag_reading
    cdef public bint _qiga1_diskflag_writing
    cdef public double[:] _qiga1_ncarray
    cdef public bint _qiga1_outputflag
    cdef double *_qiga1_outputpointer
    cdef public double qiga2
    cdef public numpy.int64_t _qiga2_ndim
    cdef public numpy.int64_t _qiga2_length
    cdef public bint _qiga2_ramflag
    cdef public double[:] _qiga2_array
    cdef public bint _qiga2_diskflag_reading
    cdef public bint _qiga2_diskflag_writing
    cdef public double[:] _qiga2_ncarray
    cdef public bint _qiga2_outputflag
    cdef double *_qiga2_outputpointer
    cdef public double qbga
    cdef public numpy.int64_t _qbga_ndim
    cdef public numpy.int64_t _qbga_length
    cdef public bint _qbga_ramflag
    cdef public double[:] _qbga_array
    cdef public bint _qbga_diskflag_reading
    cdef public bint _qbga_diskflag_writing
    cdef public double[:] _qbga_ncarray
    cdef public bint _qbga_outputflag
    cdef double *_qbga_outputpointer
    cdef public double qah
    cdef public numpy.int64_t _qah_ndim
    cdef public numpy.int64_t _qah_length
    cdef public bint _qah_ramflag
    cdef public double[:] _qah_array
    cdef public bint _qah_diskflag_reading
    cdef public bint _qah_diskflag_writing
    cdef public double[:] _qah_ncarray
    cdef public bint _qah_outputflag
    cdef double *_qah_outputpointer
    cdef public double qa
    cdef public numpy.int64_t _qa_ndim
    cdef public numpy.int64_t _qa_length
    cdef public bint _qa_ramflag
    cdef public double[:] _qa_array
    cdef public bint _qa_diskflag_reading
    cdef public bint _qa_diskflag_writing
    cdef public double[:] _qa_ncarray
    cdef public bint _qa_outputflag
    cdef double *_qa_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double[:] inzp
    cdef public numpy.int64_t _inzp_ndim
    cdef public numpy.int64_t _inzp_length
    cdef public numpy.int64_t _inzp_length_0
    cdef public bint _inzp_ramflag
    cdef public double[:,:] _inzp_array
    cdef public bint _inzp_diskflag_reading
    cdef public bint _inzp_diskflag_writing
    cdef public double[:] _inzp_ncarray
    cdef public double[:] stinz
    cdef public numpy.int64_t _stinz_ndim
    cdef public numpy.int64_t _stinz_length
    cdef public numpy.int64_t _stinz_length_0
    cdef public bint _stinz_ramflag
    cdef public double[:,:] _stinz_array
    cdef public bint _stinz_diskflag_reading
    cdef public bint _stinz_diskflag_writing
    cdef public double[:] _stinz_ncarray
    cdef public double[:] sinz
    cdef public numpy.int64_t _sinz_ndim
    cdef public numpy.int64_t _sinz_length
    cdef public numpy.int64_t _sinz_length_0
    cdef public bint _sinz_ramflag
    cdef public double[:,:] _sinz_array
    cdef public bint _sinz_diskflag_reading
    cdef public bint _sinz_diskflag_writing
    cdef public double[:] _sinz_ncarray
    cdef public double[:] esnowinz
    cdef public numpy.int64_t _esnowinz_ndim
    cdef public numpy.int64_t _esnowinz_length
    cdef public numpy.int64_t _esnowinz_length_0
    cdef public bint _esnowinz_ramflag
    cdef public double[:,:] _esnowinz_array
    cdef public bint _esnowinz_diskflag_reading
    cdef public bint _esnowinz_diskflag_writing
    cdef public double[:] _esnowinz_ncarray
    cdef public double[:] asinz
    cdef public numpy.int64_t _asinz_ndim
    cdef public numpy.int64_t _asinz_length
    cdef public numpy.int64_t _asinz_length_0
    cdef public bint _asinz_ramflag
    cdef public double[:,:] _asinz_array
    cdef public bint _asinz_diskflag_reading
    cdef public bint _asinz_diskflag_writing
    cdef public double[:] _asinz_ncarray
    cdef public double[:] wats
    cdef public numpy.int64_t _wats_ndim
    cdef public numpy.int64_t _wats_length
    cdef public numpy.int64_t _wats_length_0
    cdef public bint _wats_ramflag
    cdef public double[:,:] _wats_array
    cdef public bint _wats_diskflag_reading
    cdef public bint _wats_diskflag_writing
    cdef public double[:] _wats_ncarray
    cdef public double[:] waes
    cdef public numpy.int64_t _waes_ndim
    cdef public numpy.int64_t _waes_length
    cdef public numpy.int64_t _waes_length_0
    cdef public bint _waes_ramflag
    cdef public double[:,:] _waes_array
    cdef public bint _waes_diskflag_reading
    cdef public bint _waes_diskflag_writing
    cdef public double[:] _waes_ncarray
    cdef public double[:] esnow
    cdef public numpy.int64_t _esnow_ndim
    cdef public numpy.int64_t _esnow_length
    cdef public numpy.int64_t _esnow_length_0
    cdef public bint _esnow_ramflag
    cdef public double[:,:] _esnow_array
    cdef public bint _esnow_diskflag_reading
    cdef public bint _esnow_diskflag_writing
    cdef public double[:] _esnow_ncarray
    cdef public double[:] taus
    cdef public numpy.int64_t _taus_ndim
    cdef public numpy.int64_t _taus_length
    cdef public numpy.int64_t _taus_length_0
    cdef public bint _taus_ramflag
    cdef public double[:,:] _taus_array
    cdef public bint _taus_diskflag_reading
    cdef public bint _taus_diskflag_writing
    cdef public double[:] _taus_ncarray
    cdef public double[:] ebdn
    cdef public numpy.int64_t _ebdn_ndim
    cdef public numpy.int64_t _ebdn_length
    cdef public numpy.int64_t _ebdn_length_0
    cdef public bint _ebdn_ramflag
    cdef public double[:,:] _ebdn_array
    cdef public bint _ebdn_diskflag_reading
    cdef public bint _ebdn_diskflag_writing
    cdef public double[:] _ebdn_ncarray
    cdef public double[:] bowa
    cdef public numpy.int64_t _bowa_ndim
    cdef public numpy.int64_t _bowa_length
    cdef public numpy.int64_t _bowa_length_0
    cdef public bint _bowa_ramflag
    cdef public double[:,:] _bowa_array
    cdef public bint _bowa_diskflag_reading
    cdef public bint _bowa_diskflag_writing
    cdef public double[:] _bowa_ncarray
    cdef public double sdg1
    cdef public numpy.int64_t _sdg1_ndim
    cdef public numpy.int64_t _sdg1_length
    cdef public bint _sdg1_ramflag
    cdef public double[:] _sdg1_array
    cdef public bint _sdg1_diskflag_reading
    cdef public bint _sdg1_diskflag_writing
    cdef public double[:] _sdg1_ncarray
    cdef public bint _sdg1_outputflag
    cdef double *_sdg1_outputpointer
    cdef public double sdg2
    cdef public numpy.int64_t _sdg2_ndim
    cdef public numpy.int64_t _sdg2_length
    cdef public bint _sdg2_ramflag
    cdef public double[:] _sdg2_array
    cdef public bint _sdg2_diskflag_reading
    cdef public bint _sdg2_diskflag_writing
    cdef public double[:] _sdg2_ncarray
    cdef public bint _sdg2_outputflag
    cdef double *_sdg2_outputpointer
    cdef public double sig1
    cdef public numpy.int64_t _sig1_ndim
    cdef public numpy.int64_t _sig1_length
    cdef public bint _sig1_ramflag
    cdef public double[:] _sig1_array
    cdef public bint _sig1_diskflag_reading
    cdef public bint _sig1_diskflag_writing
    cdef public double[:] _sig1_ncarray
    cdef public bint _sig1_outputflag
    cdef double *_sig1_outputpointer
    cdef public double sig2
    cdef public numpy.int64_t _sig2_ndim
    cdef public numpy.int64_t _sig2_length
    cdef public bint _sig2_ramflag
    cdef public double[:] _sig2_array
    cdef public bint _sig2_diskflag_reading
    cdef public bint _sig2_diskflag_writing
    cdef public double[:] _sig2_ncarray
    cdef public bint _sig2_outputflag
    cdef double *_sig2_outputpointer
    cdef public double sbg
    cdef public numpy.int64_t _sbg_ndim
    cdef public numpy.int64_t _sbg_length
    cdef public bint _sbg_ramflag
    cdef public double[:] _sbg_array
    cdef public bint _sbg_diskflag_reading
    cdef public bint _sbg_diskflag_writing
    cdef public double[:] _sbg_ncarray
    cdef public bint _sbg_outputflag
    cdef double *_sbg_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:] loggedsunshineduration
    cdef public numpy.int64_t _loggedsunshineduration_ndim
    cdef public numpy.int64_t _loggedsunshineduration_length
    cdef public numpy.int64_t _loggedsunshineduration_length_0
    cdef public double[:] loggedpossiblesunshineduration
    cdef public numpy.int64_t _loggedpossiblesunshineduration_ndim
    cdef public numpy.int64_t _loggedpossiblesunshineduration_length
    cdef public numpy.int64_t _loggedpossiblesunshineduration_length_0
@cython.final
cdef class AideSequences:
    cdef public double[:] snratio
    cdef public numpy.int64_t _snratio_ndim
    cdef public numpy.int64_t _snratio_length
    cdef public numpy.int64_t _snratio_length_0
    cdef public double[:] rlatm
    cdef public numpy.int64_t _rlatm_ndim
    cdef public numpy.int64_t _rlatm_length
    cdef public numpy.int64_t _rlatm_length_0
    cdef public double[:] temps
    cdef public numpy.int64_t _temps_ndim
    cdef public numpy.int64_t _temps_length
    cdef public numpy.int64_t _temps_length_0
    cdef public double[:] tempsinz
    cdef public numpy.int64_t _tempsinz_ndim
    cdef public numpy.int64_t _tempsinz_length
    cdef public numpy.int64_t _tempsinz_length_0
@cython.final
cdef class OutletSequences:
    cdef public double q
    cdef public numpy.int64_t _q_ndim
    cdef public numpy.int64_t _q_length
    cdef public bint _q_ramflag
    cdef public double[:] _q_array
    cdef public bint _q_diskflag_reading
    cdef public bint _q_diskflag_writing
    cdef public double[:] _q_ncarray
    cdef double *_q_pointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class PegasusESnowInz(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class PegasusESnow(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class PegasusTempSSurface(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_hru
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface aetmodel
    cdef public numpy.npy_bool aetmodel_is_mainmodel
    cdef public numpy.int64_t aetmodel_typeid
    cdef public masterinterface.MasterInterface radiationmodel
    cdef public numpy.npy_bool radiationmodel_is_mainmodel
    cdef public numpy.int64_t radiationmodel_typeid
    cdef public masterinterface.MasterInterface soilmodel
    cdef public numpy.npy_bool soilmodel_is_mainmodel
    cdef public numpy.int64_t soilmodel_typeid
    cdef public PegasusESnowInz pegasusesnowinz
    cdef public PegasusESnow pegasusesnow
    cdef public PegasusTempSSurface pegasustempssurface
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
    cpdef inline void pick_qz_v1(self) noexcept nogil
    cpdef inline void calc_qzh_v1(self) noexcept nogil
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil
    cpdef inline void update_loggedsunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration_v1(self) noexcept nogil
    cpdef inline void update_loggedpossiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_nkor_v1(self) noexcept nogil
    cpdef inline void calc_tkor_v1(self) noexcept nogil
    cpdef inline void calc_windspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_reducedwindspeed2m_v1(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil
    cpdef inline void calc_nbes_inzp_v1(self) noexcept nogil
    cpdef inline void calc_snratio_v1(self) noexcept nogil
    cpdef inline void calc_sbes_v1(self) noexcept nogil
    cpdef inline void calc_snowintmax_v1(self) noexcept nogil
    cpdef inline void calc_snowintrate_v1(self) noexcept nogil
    cpdef inline void calc_nbesinz_v1(self) noexcept nogil
    cpdef inline void calc_sbesinz_v1(self) noexcept nogil
    cpdef inline void calc_stinz_v1(self) noexcept nogil
    cpdef inline void calc_wadainz_sinz_v1(self) noexcept nogil
    cpdef inline void calc_wniedinz_esnowinz_v1(self) noexcept nogil
    cpdef inline void calc_tempsinz_v1(self) noexcept nogil
    cpdef inline void update_asinz_v1(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiationinz_v1(self) noexcept nogil
    cpdef inline void calc_actualalbedoinz_v1(self) noexcept nogil
    cpdef inline void update_esnowinz_v1(self) noexcept nogil
    cpdef inline void calc_schmpotinz_v1(self) noexcept nogil
    cpdef inline void calc_schminz_stinz_v1(self) noexcept nogil
    cpdef inline void calc_gefrpotinz_v1(self) noexcept nogil
    cpdef inline void calc_gefrinz_stinz_v1(self) noexcept nogil
    cpdef inline void calc_evsinz_sinz_stinz_v1(self) noexcept nogil
    cpdef inline void update_wadainz_sinz_v1(self) noexcept nogil
    cpdef inline void update_esnowinz_v2(self) noexcept nogil
    cpdef inline void calc_wats_v1(self) noexcept nogil
    cpdef inline void calc_wats_v2(self) noexcept nogil
    cpdef inline void calc_wada_waes_v1(self) noexcept nogil
    cpdef inline void calc_wada_waes_v2(self) noexcept nogil
    cpdef inline void calc_wgtf_v1(self) noexcept nogil
    cpdef inline void calc_wnied_v1(self) noexcept nogil
    cpdef inline void calc_wnied_esnow_v1(self) noexcept nogil
    cpdef inline void calc_tz_v1(self) noexcept nogil
    cpdef inline void calc_wg_v1(self) noexcept nogil
    cpdef inline void calc_temps_v1(self) noexcept nogil
    cpdef inline void update_taus_v1(self) noexcept nogil
    cpdef inline void calc_actualalbedo_v1(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiationsnow_v1(self) noexcept nogil
    cpdef inline void calc_rlatm_v1(self) noexcept nogil
    cpdef inline void update_ebdn_v1(self) noexcept nogil
    cpdef inline void update_esnow_v1(self) noexcept nogil
    cpdef inline void calc_evi_inzp_v1(self) noexcept nogil
    cpdef inline void calc_evb_v1(self) noexcept nogil
    cpdef inline void calc_schmpot_v1(self) noexcept nogil
    cpdef inline void calc_schmpot_v2(self) noexcept nogil
    cpdef inline void calc_gefrpot_v1(self) noexcept nogil
    cpdef inline void calc_schm_wats_v1(self) noexcept nogil
    cpdef inline void calc_gefr_wats_v1(self) noexcept nogil
    cpdef inline void calc_evs_waes_wats_v1(self) noexcept nogil
    cpdef inline void update_wada_waes_v1(self) noexcept nogil
    cpdef inline void update_esnow_v2(self) noexcept nogil
    cpdef inline void calc_sff_v1(self) noexcept nogil
    cpdef inline void calc_fvg_v1(self) noexcept nogil
    cpdef inline void calc_qkap_v1(self) noexcept nogil
    cpdef inline void calc_qbb_v1(self) noexcept nogil
    cpdef inline void calc_qib1_v1(self) noexcept nogil
    cpdef inline void calc_qib2_v1(self) noexcept nogil
    cpdef inline void calc_qdb_v1(self) noexcept nogil
    cpdef inline void update_qdb_v1(self) noexcept nogil
    cpdef inline void calc_bowa_v1(self) noexcept nogil
    cpdef inline void calc_qbgz_v1(self) noexcept nogil
    cpdef inline void calc_qigz1_v1(self) noexcept nogil
    cpdef inline void calc_qigz2_v1(self) noexcept nogil
    cpdef inline void calc_qdgz_v1(self) noexcept nogil
    cpdef inline void calc_qbga_sbg_v1(self) noexcept nogil
    cpdef inline void calc_qbga_sbg_qbgz_qdgz_v1(self) noexcept nogil
    cpdef inline void calc_qiga1_sig1_v1(self) noexcept nogil
    cpdef inline void calc_qiga2_sig2_v1(self) noexcept nogil
    cpdef inline void calc_qdgz1_qdgz2_v1(self) noexcept nogil
    cpdef inline void calc_qdga1_sdg1_v1(self) noexcept nogil
    cpdef inline void calc_qdga2_sdg2_v1(self) noexcept nogil
    cpdef inline void calc_qah_v1(self) noexcept nogil
    cpdef inline void calc_qa_v1(self) noexcept nogil
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature_v1(self) noexcept nogil
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowycanopy_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowalbedo_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_evi_inzp_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_evb_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline double return_netlongwaveradiationinz_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_netlongwaveradiationsnow_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_energygainsnowsurface_v1(self, double tempssurface) noexcept nogil
    cpdef inline double return_saturationvapourpressure_v1(self, double temperature) noexcept nogil
    cpdef inline double return_netradiation_v1(self, double netshortwaveradiation, double netlongwaveradiation) noexcept nogil
    cpdef inline double return_wsensinz_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsenssnow_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wlatinz_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wlatsnow_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsurfinz_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsurf_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_backwardeulererrorinz_v1(self, double esnowinz) noexcept nogil
    cpdef inline double return_backwardeulererror_v1(self, double esnow) noexcept nogil
    cpdef inline double return_tempsinz_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_temps_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wg_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_esnowinz_v1(self, numpy.int64_t k, double temps) noexcept nogil
    cpdef inline double return_esnow_v1(self, numpy.int64_t k, double temps) noexcept nogil
    cpdef inline double return_tempssurface_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_sg_v1(self, double k, double s, double qz, double dt) noexcept nogil
    cpdef inline void calc_bowa_default_v1(self) noexcept nogil
    cpdef inline void calc_bowa_soilmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_qa_v1(self) noexcept nogil
    cpdef inline void pick_qz(self) noexcept nogil
    cpdef inline void calc_qzh(self) noexcept nogil
    cpdef inline void process_radiationmodel(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_sunshineduration(self) noexcept nogil
    cpdef inline void calc_globalradiation(self) noexcept nogil
    cpdef inline void update_loggedsunshineduration(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration(self) noexcept nogil
    cpdef inline void update_loggedpossiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_nkor(self) noexcept nogil
    cpdef inline void calc_tkor(self) noexcept nogil
    cpdef inline void calc_windspeed2m(self) noexcept nogil
    cpdef inline void calc_reducedwindspeed2m(self) noexcept nogil
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil
    cpdef inline void calc_nbes_inzp(self) noexcept nogil
    cpdef inline void calc_snratio(self) noexcept nogil
    cpdef inline void calc_sbes(self) noexcept nogil
    cpdef inline void calc_snowintmax(self) noexcept nogil
    cpdef inline void calc_snowintrate(self) noexcept nogil
    cpdef inline void calc_nbesinz(self) noexcept nogil
    cpdef inline void calc_sbesinz(self) noexcept nogil
    cpdef inline void calc_stinz(self) noexcept nogil
    cpdef inline void calc_wadainz_sinz(self) noexcept nogil
    cpdef inline void calc_wniedinz_esnowinz(self) noexcept nogil
    cpdef inline void calc_tempsinz(self) noexcept nogil
    cpdef inline void update_asinz(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiationinz(self) noexcept nogil
    cpdef inline void calc_actualalbedoinz(self) noexcept nogil
    cpdef inline void calc_schmpotinz(self) noexcept nogil
    cpdef inline void calc_schminz_stinz(self) noexcept nogil
    cpdef inline void calc_gefrpotinz(self) noexcept nogil
    cpdef inline void calc_gefrinz_stinz(self) noexcept nogil
    cpdef inline void calc_evsinz_sinz_stinz(self) noexcept nogil
    cpdef inline void update_wadainz_sinz(self) noexcept nogil
    cpdef inline void calc_wgtf(self) noexcept nogil
    cpdef inline void calc_wnied(self) noexcept nogil
    cpdef inline void calc_wnied_esnow(self) noexcept nogil
    cpdef inline void calc_tz(self) noexcept nogil
    cpdef inline void calc_wg(self) noexcept nogil
    cpdef inline void calc_temps(self) noexcept nogil
    cpdef inline void update_taus(self) noexcept nogil
    cpdef inline void calc_actualalbedo(self) noexcept nogil
    cpdef inline void calc_netshortwaveradiationsnow(self) noexcept nogil
    cpdef inline void calc_rlatm(self) noexcept nogil
    cpdef inline void update_ebdn(self) noexcept nogil
    cpdef inline void calc_evi_inzp(self) noexcept nogil
    cpdef inline void calc_evb(self) noexcept nogil
    cpdef inline void calc_gefrpot(self) noexcept nogil
    cpdef inline void calc_schm_wats(self) noexcept nogil
    cpdef inline void calc_gefr_wats(self) noexcept nogil
    cpdef inline void calc_evs_waes_wats(self) noexcept nogil
    cpdef inline void update_wada_waes(self) noexcept nogil
    cpdef inline void calc_sff(self) noexcept nogil
    cpdef inline void calc_fvg(self) noexcept nogil
    cpdef inline void calc_qkap(self) noexcept nogil
    cpdef inline void calc_qbb(self) noexcept nogil
    cpdef inline void calc_qib1(self) noexcept nogil
    cpdef inline void calc_qib2(self) noexcept nogil
    cpdef inline void calc_qdb(self) noexcept nogil
    cpdef inline void update_qdb(self) noexcept nogil
    cpdef inline void calc_bowa(self) noexcept nogil
    cpdef inline void calc_qbgz(self) noexcept nogil
    cpdef inline void calc_qigz1(self) noexcept nogil
    cpdef inline void calc_qigz2(self) noexcept nogil
    cpdef inline void calc_qdgz(self) noexcept nogil
    cpdef inline void calc_qbga_sbg(self) noexcept nogil
    cpdef inline void calc_qbga_sbg_qbgz_qdgz(self) noexcept nogil
    cpdef inline void calc_qiga1_sig1(self) noexcept nogil
    cpdef inline void calc_qiga2_sig2(self) noexcept nogil
    cpdef inline void calc_qdgz1_qdgz2(self) noexcept nogil
    cpdef inline void calc_qdga1_sdg1(self) noexcept nogil
    cpdef inline void calc_qdga2_sdg2(self) noexcept nogil
    cpdef inline void calc_qah(self) noexcept nogil
    cpdef inline void calc_qa(self) noexcept nogil
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature(self) noexcept nogil
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowycanopy(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowalbedo(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_evi_inzp_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_evb_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline double return_netlongwaveradiationinz(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_netlongwaveradiationsnow(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_energygainsnowsurface(self, double tempssurface) noexcept nogil
    cpdef inline double return_saturationvapourpressure(self, double temperature) noexcept nogil
    cpdef inline double return_netradiation(self, double netshortwaveradiation, double netlongwaveradiation) noexcept nogil
    cpdef inline double return_wsensinz(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsenssnow(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wlatinz(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wlatsnow(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsurfinz(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wsurf(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_backwardeulererrorinz(self, double esnowinz) noexcept nogil
    cpdef inline double return_backwardeulererror(self, double esnow) noexcept nogil
    cpdef inline double return_tempsinz(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_temps(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_wg(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_esnowinz(self, numpy.int64_t k, double temps) noexcept nogil
    cpdef inline double return_esnow(self, numpy.int64_t k, double temps) noexcept nogil
    cpdef inline double return_tempssurface(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_sg(self, double k, double s, double qz, double dt) noexcept nogil
    cpdef inline void calc_bowa_default(self) noexcept nogil
    cpdef inline void calc_bowa_soilmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_qa(self) noexcept nogil
