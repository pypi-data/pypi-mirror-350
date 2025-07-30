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
    cdef public double latitude
    cdef public double longitude
    cdef public double[:] angstromconstant
    cdef public numpy.int64_t _angstromconstant_entrymin
    cdef public double[:] angstromfactor
    cdef public numpy.int64_t _angstromfactor_entrymin
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] doy
    cdef public numpy.int64_t[:] moy
    cdef public double hours
    cdef public double[:] sct
    cdef public numpy.int64_t nmblogentries
    cdef public numpy.int64_t utclongitude
    cdef public double latituderad
@cython.final
cdef class FixedParameters:
    cdef public double pi
    cdef public double solarconstant
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public LogSequences logs
@cython.final
cdef class InputSequences:
    cdef public double globalradiation
    cdef public numpy.int64_t _globalradiation_ndim
    cdef public numpy.int64_t _globalradiation_length
    cdef public bint _globalradiation_ramflag
    cdef public double[:] _globalradiation_array
    cdef public bint _globalradiation_diskflag_reading
    cdef public bint _globalradiation_diskflag_writing
    cdef public double[:] _globalradiation_ncarray
    cdef public bint _globalradiation_inputflag
    cdef double *_globalradiation_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double earthsundistance
    cdef public numpy.int64_t _earthsundistance_ndim
    cdef public numpy.int64_t _earthsundistance_length
    cdef public bint _earthsundistance_ramflag
    cdef public double[:] _earthsundistance_array
    cdef public bint _earthsundistance_diskflag_reading
    cdef public bint _earthsundistance_diskflag_writing
    cdef public double[:] _earthsundistance_ncarray
    cdef public bint _earthsundistance_outputflag
    cdef double *_earthsundistance_outputpointer
    cdef public double solardeclination
    cdef public numpy.int64_t _solardeclination_ndim
    cdef public numpy.int64_t _solardeclination_length
    cdef public bint _solardeclination_ramflag
    cdef public double[:] _solardeclination_array
    cdef public bint _solardeclination_diskflag_reading
    cdef public bint _solardeclination_diskflag_writing
    cdef public double[:] _solardeclination_ncarray
    cdef public bint _solardeclination_outputflag
    cdef double *_solardeclination_outputpointer
    cdef public double timeofsunrise
    cdef public numpy.int64_t _timeofsunrise_ndim
    cdef public numpy.int64_t _timeofsunrise_length
    cdef public bint _timeofsunrise_ramflag
    cdef public double[:] _timeofsunrise_array
    cdef public bint _timeofsunrise_diskflag_reading
    cdef public bint _timeofsunrise_diskflag_writing
    cdef public double[:] _timeofsunrise_ncarray
    cdef public bint _timeofsunrise_outputflag
    cdef double *_timeofsunrise_outputpointer
    cdef public double timeofsunset
    cdef public numpy.int64_t _timeofsunset_ndim
    cdef public numpy.int64_t _timeofsunset_length
    cdef public bint _timeofsunset_ramflag
    cdef public double[:] _timeofsunset_array
    cdef public bint _timeofsunset_diskflag_reading
    cdef public bint _timeofsunset_diskflag_writing
    cdef public double[:] _timeofsunset_ncarray
    cdef public bint _timeofsunset_outputflag
    cdef double *_timeofsunset_outputpointer
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
    cdef public double unadjustedsunshineduration
    cdef public numpy.int64_t _unadjustedsunshineduration_ndim
    cdef public numpy.int64_t _unadjustedsunshineduration_length
    cdef public bint _unadjustedsunshineduration_ramflag
    cdef public double[:] _unadjustedsunshineduration_array
    cdef public bint _unadjustedsunshineduration_diskflag_reading
    cdef public bint _unadjustedsunshineduration_diskflag_writing
    cdef public double[:] _unadjustedsunshineduration_ncarray
    cdef public bint _unadjustedsunshineduration_outputflag
    cdef double *_unadjustedsunshineduration_outputpointer
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
    cdef public double portiondailyradiation
    cdef public numpy.int64_t _portiondailyradiation_ndim
    cdef public numpy.int64_t _portiondailyradiation_length
    cdef public bint _portiondailyradiation_ramflag
    cdef public double[:] _portiondailyradiation_array
    cdef public bint _portiondailyradiation_diskflag_reading
    cdef public bint _portiondailyradiation_diskflag_writing
    cdef public double[:] _portiondailyradiation_ncarray
    cdef public bint _portiondailyradiation_outputflag
    cdef double *_portiondailyradiation_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double extraterrestrialradiation
    cdef public numpy.int64_t _extraterrestrialradiation_ndim
    cdef public numpy.int64_t _extraterrestrialradiation_length
    cdef public bint _extraterrestrialradiation_ramflag
    cdef public double[:] _extraterrestrialradiation_array
    cdef public bint _extraterrestrialradiation_diskflag_reading
    cdef public bint _extraterrestrialradiation_diskflag_writing
    cdef public double[:] _extraterrestrialradiation_ncarray
    cdef public bint _extraterrestrialradiation_outputflag
    cdef double *_extraterrestrialradiation_outputpointer
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
    cdef public double[:] loggedunadjustedsunshineduration
    cdef public numpy.int64_t _loggedunadjustedsunshineduration_ndim
    cdef public numpy.int64_t _loggedunadjustedsunshineduration_length
    cdef public numpy.int64_t _loggedunadjustedsunshineduration_length_0
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef bint __hydpy_reuse_process_radiation_v1__
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef inline void calc_earthsundistance_v1(self) noexcept nogil
    cpdef inline void calc_solardeclination_v2(self) noexcept nogil
    cpdef inline void calc_timeofsunrise_timeofsunset_v1(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration_v2(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil
    cpdef inline void calc_dailyglobalradiation_v2(self) noexcept nogil
    cpdef inline void calc_extraterrestrialradiation_v2(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration_v2(self) noexcept nogil
    cpdef inline void calc_portiondailyradiation_v1(self) noexcept nogil
    cpdef inline void adjust_clearskysolarradiation_v1(self) noexcept nogil
    cpdef inline void calc_unadjustedsunshineduration_v1(self) noexcept nogil
    cpdef inline void update_loggedunadjustedsunshineduration_v1(self) noexcept nogil
    cpdef inline void calc_sunshineduration_v2(self) noexcept nogil
    cpdef void process_radiation_v1(self) noexcept nogil
    cpdef double get_possiblesunshineduration_v1(self) noexcept nogil
    cpdef double get_sunshineduration_v1(self) noexcept nogil
    cpdef double get_clearskysolarradiation_v1(self) noexcept nogil
    cpdef double get_globalradiation_v2(self) noexcept nogil
    cpdef inline double return_sunshineduration_v1(self, double globalradiation, double extraterrestrialradiation, double possiblesunshineduration) noexcept nogil
    cpdef inline void calc_earthsundistance(self) noexcept nogil
    cpdef inline void calc_solardeclination(self) noexcept nogil
    cpdef inline void calc_timeofsunrise_timeofsunset(self) noexcept nogil
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil
    cpdef inline void calc_dailyglobalradiation(self) noexcept nogil
    cpdef inline void calc_extraterrestrialradiation(self) noexcept nogil
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil
    cpdef inline void calc_dailysunshineduration(self) noexcept nogil
    cpdef inline void calc_portiondailyradiation(self) noexcept nogil
    cpdef inline void adjust_clearskysolarradiation(self) noexcept nogil
    cpdef inline void calc_unadjustedsunshineduration(self) noexcept nogil
    cpdef inline void update_loggedunadjustedsunshineduration(self) noexcept nogil
    cpdef inline void calc_sunshineduration(self) noexcept nogil
    cpdef void process_radiation(self) noexcept nogil
    cpdef double get_possiblesunshineduration(self) noexcept nogil
    cpdef double get_sunshineduration(self) noexcept nogil
    cpdef double get_clearskysolarradiation(self) noexcept nogil
    cpdef double get_globalradiation(self) noexcept nogil
    cpdef inline double return_sunshineduration(self, double globalradiation, double extraterrestrialradiation, double possiblesunshineduration) noexcept nogil
