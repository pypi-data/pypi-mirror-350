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
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double surfacearea
    cdef public double catchmentarea
    cdef public numpy.int64_t nmblogentries
    cdef public double correctionprecipitation
    cdef public double correctionevaporation
    cdef public double weightevaporation
    cdef public double[:] remotedischargeminimum
    cdef public double[:] remotedischargesafety
    cdef public interputils.SimpleInterpolator waterlevel2possibleremoterelief
    cdef public double remoterelieftolerance
    cdef public double[:] neardischargeminimumthreshold
    cdef public double[:] neardischargeminimumtolerance
    cdef public numpy.npy_bool restricttargetedrelease
    cdef public double[:] watervolumeminimumthreshold
    cdef public double waterlevelminimumthreshold
    cdef public double waterlevelminimumtolerance
    cdef public double waterlevelmaximumthreshold
    cdef public double waterlevelmaximumtolerance
    cdef public double remotewaterlevelmaximumthreshold
    cdef public double remotewaterlevelmaximumtolerance
    cdef public double thresholdevaporation
    cdef public double toleranceevaporation
    cdef public double waterlevelminimumremotethreshold
    cdef public double waterlevelminimumremotetolerance
    cdef public double[:] highestremoterelief
    cdef public double[:] waterlevelreliefthreshold
    cdef public double[:] waterlevelrelieftolerance
    cdef public double[:] highestremotesupply
    cdef public double[:] waterlevelsupplythreshold
    cdef public double[:] waterlevelsupplytolerance
    cdef public double highestremotedischarge
    cdef public double highestremotetolerance
    cdef public interputils.SimpleInterpolator watervolume2waterlevel
    cdef public interputils.SeasonalInterpolator waterlevel2flooddischarge
    cdef public interputils.SeasonalInterpolator waterleveldifference2maxforceddischarge
    cdef public interputils.SeasonalInterpolator waterleveldifference2maxfreedischarge
    cdef public double allowedwaterleveldrop
    cdef public double[:] allowedrelease
    cdef public double[:] targetvolume
    cdef public double targetrangeabsolute
    cdef public double targetrangerelative
    cdef public double volumetolerance
    cdef public double dischargetolerance
    cdef public double crestlevel
    cdef public double crestleveltolerance
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] toy
    cdef public double seconds
    cdef public double inputfactor
    cdef public double[:] remotedischargesmoothpar
    cdef public double[:] neardischargeminimumsmoothpar1
    cdef public double[:] neardischargeminimumsmoothpar2
    cdef public double waterlevelminimumsmoothpar
    cdef public double waterlevelmaximumsmoothpar
    cdef public double remotewaterlevelmaximumsmoothpar
    cdef public double smoothparevaporation
    cdef public double waterlevelminimumremotesmoothpar
    cdef public double[:] waterlevelreliefsmoothpar
    cdef public double[:] waterlevelsupplysmoothpar
    cdef public double highestremotesmoothpar
    cdef public double volumesmoothparlog1
    cdef public double volumesmoothparlog2
    cdef public double dischargesmoothpar
    cdef public double crestlevelsmoothpar
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public ReceiverSequences receivers
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public SenderSequences senders
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
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef double *_s_pointer
    cdef public double r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef double *_r_pointer
    cdef public double[:] e
    cdef public numpy.int64_t _e_ndim
    cdef public numpy.int64_t _e_length
    cdef public numpy.int64_t _e_length_0
    cdef public bint _e_ramflag
    cdef public double[:,:] _e_array
    cdef public bint _e_diskflag_reading
    cdef public bint _e_diskflag_writing
    cdef public double[:] _e_ncarray
    cdef double **_e_pointer
    cdef public numpy.int64_t len_e
    cdef public numpy.int64_t[:] _e_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class ReceiverSequences:
    cdef public double q
    cdef public numpy.int64_t _q_ndim
    cdef public numpy.int64_t _q_length
    cdef public bint _q_ramflag
    cdef public double[:] _q_array
    cdef public bint _q_diskflag_reading
    cdef public bint _q_diskflag_writing
    cdef public double[:] _q_ncarray
    cdef double *_q_pointer
    cdef public double d
    cdef public numpy.int64_t _d_ndim
    cdef public numpy.int64_t _d_length
    cdef public bint _d_ramflag
    cdef public double[:] _d_array
    cdef public bint _d_diskflag_reading
    cdef public bint _d_diskflag_writing
    cdef public double[:] _d_ncarray
    cdef double *_d_pointer
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef double *_s_pointer
    cdef public double r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef double *_r_pointer
    cdef public double owl
    cdef public numpy.int64_t _owl_ndim
    cdef public numpy.int64_t _owl_length
    cdef public bint _owl_ramflag
    cdef public double[:] _owl_array
    cdef public bint _owl_diskflag_reading
    cdef public bint _owl_diskflag_writing
    cdef public double[:] _owl_ncarray
    cdef double *_owl_pointer
    cdef public double rwl
    cdef public numpy.int64_t _rwl_ndim
    cdef public numpy.int64_t _rwl_length
    cdef public bint _rwl_ramflag
    cdef public double[:] _rwl_array
    cdef public bint _rwl_diskflag_reading
    cdef public bint _rwl_diskflag_writing
    cdef public double[:] _rwl_ncarray
    cdef double *_rwl_pointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class FactorSequences:
    cdef public double waterlevel
    cdef public numpy.int64_t _waterlevel_ndim
    cdef public numpy.int64_t _waterlevel_length
    cdef public bint _waterlevel_ramflag
    cdef public double[:] _waterlevel_array
    cdef public bint _waterlevel_diskflag_reading
    cdef public bint _waterlevel_diskflag_writing
    cdef public double[:] _waterlevel_ncarray
    cdef public bint _waterlevel_outputflag
    cdef double *_waterlevel_outputpointer
    cdef public double outerwaterlevel
    cdef public numpy.int64_t _outerwaterlevel_ndim
    cdef public numpy.int64_t _outerwaterlevel_length
    cdef public bint _outerwaterlevel_ramflag
    cdef public double[:] _outerwaterlevel_array
    cdef public bint _outerwaterlevel_diskflag_reading
    cdef public bint _outerwaterlevel_diskflag_writing
    cdef public double[:] _outerwaterlevel_ncarray
    cdef public bint _outerwaterlevel_outputflag
    cdef double *_outerwaterlevel_outputpointer
    cdef public double remotewaterlevel
    cdef public numpy.int64_t _remotewaterlevel_ndim
    cdef public numpy.int64_t _remotewaterlevel_length
    cdef public bint _remotewaterlevel_ramflag
    cdef public double[:] _remotewaterlevel_array
    cdef public bint _remotewaterlevel_diskflag_reading
    cdef public bint _remotewaterlevel_diskflag_writing
    cdef public double[:] _remotewaterlevel_ncarray
    cdef public bint _remotewaterlevel_outputflag
    cdef double *_remotewaterlevel_outputpointer
    cdef public double waterleveldifference
    cdef public numpy.int64_t _waterleveldifference_ndim
    cdef public numpy.int64_t _waterleveldifference_length
    cdef public bint _waterleveldifference_ramflag
    cdef public double[:] _waterleveldifference_array
    cdef public bint _waterleveldifference_diskflag_reading
    cdef public bint _waterleveldifference_diskflag_writing
    cdef public double[:] _waterleveldifference_ncarray
    cdef public bint _waterleveldifference_outputflag
    cdef double *_waterleveldifference_outputpointer
    cdef public double effectivewaterleveldifference
    cdef public numpy.int64_t _effectivewaterleveldifference_ndim
    cdef public numpy.int64_t _effectivewaterleveldifference_length
    cdef public bint _effectivewaterleveldifference_ramflag
    cdef public double[:] _effectivewaterleveldifference_array
    cdef public bint _effectivewaterleveldifference_diskflag_reading
    cdef public bint _effectivewaterleveldifference_diskflag_writing
    cdef public double[:] _effectivewaterleveldifference_ncarray
    cdef public bint _effectivewaterleveldifference_outputflag
    cdef double *_effectivewaterleveldifference_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double precipitation
    cdef public numpy.int64_t _precipitation_ndim
    cdef public numpy.int64_t _precipitation_length
    cdef public bint _precipitation_ramflag
    cdef public double[:] _precipitation_array
    cdef public bint _precipitation_diskflag_reading
    cdef public bint _precipitation_diskflag_writing
    cdef public double[:] _precipitation_ncarray
    cdef public bint _precipitation_outputflag
    cdef double *_precipitation_outputpointer
    cdef public double adjustedprecipitation
    cdef public numpy.int64_t _adjustedprecipitation_ndim
    cdef public numpy.int64_t _adjustedprecipitation_length
    cdef public double[:] _adjustedprecipitation_points
    cdef public double[:] _adjustedprecipitation_results
    cdef public double[:] _adjustedprecipitation_integrals
    cdef public double _adjustedprecipitation_sum
    cdef public bint _adjustedprecipitation_ramflag
    cdef public double[:] _adjustedprecipitation_array
    cdef public bint _adjustedprecipitation_diskflag_reading
    cdef public bint _adjustedprecipitation_diskflag_writing
    cdef public double[:] _adjustedprecipitation_ncarray
    cdef public bint _adjustedprecipitation_outputflag
    cdef double *_adjustedprecipitation_outputpointer
    cdef public double potentialevaporation
    cdef public numpy.int64_t _potentialevaporation_ndim
    cdef public numpy.int64_t _potentialevaporation_length
    cdef public bint _potentialevaporation_ramflag
    cdef public double[:] _potentialevaporation_array
    cdef public bint _potentialevaporation_diskflag_reading
    cdef public bint _potentialevaporation_diskflag_writing
    cdef public double[:] _potentialevaporation_ncarray
    cdef public bint _potentialevaporation_outputflag
    cdef double *_potentialevaporation_outputpointer
    cdef public double adjustedevaporation
    cdef public numpy.int64_t _adjustedevaporation_ndim
    cdef public numpy.int64_t _adjustedevaporation_length
    cdef public bint _adjustedevaporation_ramflag
    cdef public double[:] _adjustedevaporation_array
    cdef public bint _adjustedevaporation_diskflag_reading
    cdef public bint _adjustedevaporation_diskflag_writing
    cdef public double[:] _adjustedevaporation_ncarray
    cdef public bint _adjustedevaporation_outputflag
    cdef double *_adjustedevaporation_outputpointer
    cdef public double actualevaporation
    cdef public numpy.int64_t _actualevaporation_ndim
    cdef public numpy.int64_t _actualevaporation_length
    cdef public double[:] _actualevaporation_points
    cdef public double[:] _actualevaporation_results
    cdef public double[:] _actualevaporation_integrals
    cdef public double _actualevaporation_sum
    cdef public bint _actualevaporation_ramflag
    cdef public double[:] _actualevaporation_array
    cdef public bint _actualevaporation_diskflag_reading
    cdef public bint _actualevaporation_diskflag_writing
    cdef public double[:] _actualevaporation_ncarray
    cdef public bint _actualevaporation_outputflag
    cdef double *_actualevaporation_outputpointer
    cdef public double inflow
    cdef public numpy.int64_t _inflow_ndim
    cdef public numpy.int64_t _inflow_length
    cdef public double[:] _inflow_points
    cdef public double[:] _inflow_results
    cdef public double[:] _inflow_integrals
    cdef public double _inflow_sum
    cdef public bint _inflow_ramflag
    cdef public double[:] _inflow_array
    cdef public bint _inflow_diskflag_reading
    cdef public bint _inflow_diskflag_writing
    cdef public double[:] _inflow_ncarray
    cdef public bint _inflow_outputflag
    cdef double *_inflow_outputpointer
    cdef public double exchange
    cdef public numpy.int64_t _exchange_ndim
    cdef public numpy.int64_t _exchange_length
    cdef public double[:] _exchange_points
    cdef public double[:] _exchange_results
    cdef public double[:] _exchange_integrals
    cdef public double _exchange_sum
    cdef public bint _exchange_ramflag
    cdef public double[:] _exchange_array
    cdef public bint _exchange_diskflag_reading
    cdef public bint _exchange_diskflag_writing
    cdef public double[:] _exchange_ncarray
    cdef public bint _exchange_outputflag
    cdef double *_exchange_outputpointer
    cdef public double totalremotedischarge
    cdef public numpy.int64_t _totalremotedischarge_ndim
    cdef public numpy.int64_t _totalremotedischarge_length
    cdef public bint _totalremotedischarge_ramflag
    cdef public double[:] _totalremotedischarge_array
    cdef public bint _totalremotedischarge_diskflag_reading
    cdef public bint _totalremotedischarge_diskflag_writing
    cdef public double[:] _totalremotedischarge_ncarray
    cdef public bint _totalremotedischarge_outputflag
    cdef double *_totalremotedischarge_outputpointer
    cdef public double naturalremotedischarge
    cdef public numpy.int64_t _naturalremotedischarge_ndim
    cdef public numpy.int64_t _naturalremotedischarge_length
    cdef public bint _naturalremotedischarge_ramflag
    cdef public double[:] _naturalremotedischarge_array
    cdef public bint _naturalremotedischarge_diskflag_reading
    cdef public bint _naturalremotedischarge_diskflag_writing
    cdef public double[:] _naturalremotedischarge_ncarray
    cdef public bint _naturalremotedischarge_outputflag
    cdef double *_naturalremotedischarge_outputpointer
    cdef public double remotedemand
    cdef public numpy.int64_t _remotedemand_ndim
    cdef public numpy.int64_t _remotedemand_length
    cdef public bint _remotedemand_ramflag
    cdef public double[:] _remotedemand_array
    cdef public bint _remotedemand_diskflag_reading
    cdef public bint _remotedemand_diskflag_writing
    cdef public double[:] _remotedemand_ncarray
    cdef public bint _remotedemand_outputflag
    cdef double *_remotedemand_outputpointer
    cdef public double remotefailure
    cdef public numpy.int64_t _remotefailure_ndim
    cdef public numpy.int64_t _remotefailure_length
    cdef public bint _remotefailure_ramflag
    cdef public double[:] _remotefailure_array
    cdef public bint _remotefailure_diskflag_reading
    cdef public bint _remotefailure_diskflag_writing
    cdef public double[:] _remotefailure_ncarray
    cdef public bint _remotefailure_outputflag
    cdef double *_remotefailure_outputpointer
    cdef public double requiredremoterelease
    cdef public numpy.int64_t _requiredremoterelease_ndim
    cdef public numpy.int64_t _requiredremoterelease_length
    cdef public bint _requiredremoterelease_ramflag
    cdef public double[:] _requiredremoterelease_array
    cdef public bint _requiredremoterelease_diskflag_reading
    cdef public bint _requiredremoterelease_diskflag_writing
    cdef public double[:] _requiredremoterelease_ncarray
    cdef public bint _requiredremoterelease_outputflag
    cdef double *_requiredremoterelease_outputpointer
    cdef public double allowedremoterelief
    cdef public numpy.int64_t _allowedremoterelief_ndim
    cdef public numpy.int64_t _allowedremoterelief_length
    cdef public bint _allowedremoterelief_ramflag
    cdef public double[:] _allowedremoterelief_array
    cdef public bint _allowedremoterelief_diskflag_reading
    cdef public bint _allowedremoterelief_diskflag_writing
    cdef public double[:] _allowedremoterelief_ncarray
    cdef public bint _allowedremoterelief_outputflag
    cdef double *_allowedremoterelief_outputpointer
    cdef public double requiredremotesupply
    cdef public numpy.int64_t _requiredremotesupply_ndim
    cdef public numpy.int64_t _requiredremotesupply_length
    cdef public bint _requiredremotesupply_ramflag
    cdef public double[:] _requiredremotesupply_array
    cdef public bint _requiredremotesupply_diskflag_reading
    cdef public bint _requiredremotesupply_diskflag_writing
    cdef public double[:] _requiredremotesupply_ncarray
    cdef public bint _requiredremotesupply_outputflag
    cdef double *_requiredremotesupply_outputpointer
    cdef public double possibleremoterelief
    cdef public numpy.int64_t _possibleremoterelief_ndim
    cdef public numpy.int64_t _possibleremoterelief_length
    cdef public double[:] _possibleremoterelief_points
    cdef public double[:] _possibleremoterelief_results
    cdef public double[:] _possibleremoterelief_integrals
    cdef public double _possibleremoterelief_sum
    cdef public bint _possibleremoterelief_ramflag
    cdef public double[:] _possibleremoterelief_array
    cdef public bint _possibleremoterelief_diskflag_reading
    cdef public bint _possibleremoterelief_diskflag_writing
    cdef public double[:] _possibleremoterelief_ncarray
    cdef public bint _possibleremoterelief_outputflag
    cdef double *_possibleremoterelief_outputpointer
    cdef public double actualremoterelief
    cdef public numpy.int64_t _actualremoterelief_ndim
    cdef public numpy.int64_t _actualremoterelief_length
    cdef public double[:] _actualremoterelief_points
    cdef public double[:] _actualremoterelief_results
    cdef public double[:] _actualremoterelief_integrals
    cdef public double _actualremoterelief_sum
    cdef public bint _actualremoterelief_ramflag
    cdef public double[:] _actualremoterelief_array
    cdef public bint _actualremoterelief_diskflag_reading
    cdef public bint _actualremoterelief_diskflag_writing
    cdef public double[:] _actualremoterelief_ncarray
    cdef public bint _actualremoterelief_outputflag
    cdef double *_actualremoterelief_outputpointer
    cdef public double requiredrelease
    cdef public numpy.int64_t _requiredrelease_ndim
    cdef public numpy.int64_t _requiredrelease_length
    cdef public bint _requiredrelease_ramflag
    cdef public double[:] _requiredrelease_array
    cdef public bint _requiredrelease_diskflag_reading
    cdef public bint _requiredrelease_diskflag_writing
    cdef public double[:] _requiredrelease_ncarray
    cdef public bint _requiredrelease_outputflag
    cdef double *_requiredrelease_outputpointer
    cdef public double targetedrelease
    cdef public numpy.int64_t _targetedrelease_ndim
    cdef public numpy.int64_t _targetedrelease_length
    cdef public bint _targetedrelease_ramflag
    cdef public double[:] _targetedrelease_array
    cdef public bint _targetedrelease_diskflag_reading
    cdef public bint _targetedrelease_diskflag_writing
    cdef public double[:] _targetedrelease_ncarray
    cdef public bint _targetedrelease_outputflag
    cdef double *_targetedrelease_outputpointer
    cdef public double actualrelease
    cdef public numpy.int64_t _actualrelease_ndim
    cdef public numpy.int64_t _actualrelease_length
    cdef public double[:] _actualrelease_points
    cdef public double[:] _actualrelease_results
    cdef public double[:] _actualrelease_integrals
    cdef public double _actualrelease_sum
    cdef public bint _actualrelease_ramflag
    cdef public double[:] _actualrelease_array
    cdef public bint _actualrelease_diskflag_reading
    cdef public bint _actualrelease_diskflag_writing
    cdef public double[:] _actualrelease_ncarray
    cdef public bint _actualrelease_outputflag
    cdef double *_actualrelease_outputpointer
    cdef public double missingremoterelease
    cdef public numpy.int64_t _missingremoterelease_ndim
    cdef public numpy.int64_t _missingremoterelease_length
    cdef public bint _missingremoterelease_ramflag
    cdef public double[:] _missingremoterelease_array
    cdef public bint _missingremoterelease_diskflag_reading
    cdef public bint _missingremoterelease_diskflag_writing
    cdef public double[:] _missingremoterelease_ncarray
    cdef public bint _missingremoterelease_outputflag
    cdef double *_missingremoterelease_outputpointer
    cdef public double actualremoterelease
    cdef public numpy.int64_t _actualremoterelease_ndim
    cdef public numpy.int64_t _actualremoterelease_length
    cdef public double[:] _actualremoterelease_points
    cdef public double[:] _actualremoterelease_results
    cdef public double[:] _actualremoterelease_integrals
    cdef public double _actualremoterelease_sum
    cdef public bint _actualremoterelease_ramflag
    cdef public double[:] _actualremoterelease_array
    cdef public bint _actualremoterelease_diskflag_reading
    cdef public bint _actualremoterelease_diskflag_writing
    cdef public double[:] _actualremoterelease_ncarray
    cdef public bint _actualremoterelease_outputflag
    cdef double *_actualremoterelease_outputpointer
    cdef public double flooddischarge
    cdef public numpy.int64_t _flooddischarge_ndim
    cdef public numpy.int64_t _flooddischarge_length
    cdef public double[:] _flooddischarge_points
    cdef public double[:] _flooddischarge_results
    cdef public double[:] _flooddischarge_integrals
    cdef public double _flooddischarge_sum
    cdef public bint _flooddischarge_ramflag
    cdef public double[:] _flooddischarge_array
    cdef public bint _flooddischarge_diskflag_reading
    cdef public bint _flooddischarge_diskflag_writing
    cdef public double[:] _flooddischarge_ncarray
    cdef public bint _flooddischarge_outputflag
    cdef double *_flooddischarge_outputpointer
    cdef public double freedischarge
    cdef public numpy.int64_t _freedischarge_ndim
    cdef public numpy.int64_t _freedischarge_length
    cdef public double[:] _freedischarge_points
    cdef public double[:] _freedischarge_results
    cdef public double[:] _freedischarge_integrals
    cdef public double _freedischarge_sum
    cdef public bint _freedischarge_ramflag
    cdef public double[:] _freedischarge_array
    cdef public bint _freedischarge_diskflag_reading
    cdef public bint _freedischarge_diskflag_writing
    cdef public double[:] _freedischarge_ncarray
    cdef public bint _freedischarge_outputflag
    cdef double *_freedischarge_outputpointer
    cdef public double maxforceddischarge
    cdef public numpy.int64_t _maxforceddischarge_ndim
    cdef public numpy.int64_t _maxforceddischarge_length
    cdef public double[:] _maxforceddischarge_points
    cdef public double[:] _maxforceddischarge_results
    cdef public double[:] _maxforceddischarge_integrals
    cdef public double _maxforceddischarge_sum
    cdef public bint _maxforceddischarge_ramflag
    cdef public double[:] _maxforceddischarge_array
    cdef public bint _maxforceddischarge_diskflag_reading
    cdef public bint _maxforceddischarge_diskflag_writing
    cdef public double[:] _maxforceddischarge_ncarray
    cdef public bint _maxforceddischarge_outputflag
    cdef double *_maxforceddischarge_outputpointer
    cdef public double maxfreedischarge
    cdef public numpy.int64_t _maxfreedischarge_ndim
    cdef public numpy.int64_t _maxfreedischarge_length
    cdef public double[:] _maxfreedischarge_points
    cdef public double[:] _maxfreedischarge_results
    cdef public double[:] _maxfreedischarge_integrals
    cdef public double _maxfreedischarge_sum
    cdef public bint _maxfreedischarge_ramflag
    cdef public double[:] _maxfreedischarge_array
    cdef public bint _maxfreedischarge_diskflag_reading
    cdef public bint _maxfreedischarge_diskflag_writing
    cdef public double[:] _maxfreedischarge_ncarray
    cdef public bint _maxfreedischarge_outputflag
    cdef double *_maxfreedischarge_outputpointer
    cdef public double forceddischarge
    cdef public numpy.int64_t _forceddischarge_ndim
    cdef public numpy.int64_t _forceddischarge_length
    cdef public double[:] _forceddischarge_points
    cdef public double[:] _forceddischarge_results
    cdef public double[:] _forceddischarge_integrals
    cdef public double _forceddischarge_sum
    cdef public bint _forceddischarge_ramflag
    cdef public double[:] _forceddischarge_array
    cdef public bint _forceddischarge_diskflag_reading
    cdef public bint _forceddischarge_diskflag_writing
    cdef public double[:] _forceddischarge_ncarray
    cdef public bint _forceddischarge_outputflag
    cdef double *_forceddischarge_outputpointer
    cdef public double outflow
    cdef public numpy.int64_t _outflow_ndim
    cdef public numpy.int64_t _outflow_length
    cdef public double[:] _outflow_points
    cdef public double[:] _outflow_results
    cdef public double[:] _outflow_integrals
    cdef public double _outflow_sum
    cdef public bint _outflow_ramflag
    cdef public double[:] _outflow_array
    cdef public bint _outflow_diskflag_reading
    cdef public bint _outflow_diskflag_writing
    cdef public double[:] _outflow_ncarray
    cdef public bint _outflow_outputflag
    cdef double *_outflow_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double watervolume
    cdef public numpy.int64_t _watervolume_ndim
    cdef public numpy.int64_t _watervolume_length
    cdef public double[:] _watervolume_points
    cdef public double[:] _watervolume_results
    cdef public bint _watervolume_ramflag
    cdef public double[:] _watervolume_array
    cdef public bint _watervolume_diskflag_reading
    cdef public bint _watervolume_diskflag_writing
    cdef public double[:] _watervolume_ncarray
    cdef public bint _watervolume_outputflag
    cdef double *_watervolume_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:] loggedtotalremotedischarge
    cdef public numpy.int64_t _loggedtotalremotedischarge_ndim
    cdef public numpy.int64_t _loggedtotalremotedischarge_length
    cdef public numpy.int64_t _loggedtotalremotedischarge_length_0
    cdef public double[:] loggedoutflow
    cdef public numpy.int64_t _loggedoutflow_ndim
    cdef public numpy.int64_t _loggedoutflow_length
    cdef public numpy.int64_t _loggedoutflow_length_0
    cdef public double[:] loggedadjustedevaporation
    cdef public numpy.int64_t _loggedadjustedevaporation_ndim
    cdef public numpy.int64_t _loggedadjustedevaporation_length
    cdef public numpy.int64_t _loggedadjustedevaporation_length_0
    cdef public double[:] loggedrequiredremoterelease
    cdef public numpy.int64_t _loggedrequiredremoterelease_ndim
    cdef public numpy.int64_t _loggedrequiredremoterelease_length
    cdef public numpy.int64_t _loggedrequiredremoterelease_length_0
    cdef public double[:] loggedallowedremoterelief
    cdef public numpy.int64_t _loggedallowedremoterelief_ndim
    cdef public numpy.int64_t _loggedallowedremoterelief_length
    cdef public numpy.int64_t _loggedallowedremoterelief_length_0
    cdef public double[:] loggedouterwaterlevel
    cdef public numpy.int64_t _loggedouterwaterlevel_ndim
    cdef public numpy.int64_t _loggedouterwaterlevel_length
    cdef public numpy.int64_t _loggedouterwaterlevel_length_0
    cdef public double[:] loggedremotewaterlevel
    cdef public numpy.int64_t _loggedremotewaterlevel_ndim
    cdef public numpy.int64_t _loggedremotewaterlevel_length
    cdef public numpy.int64_t _loggedremotewaterlevel_length_0
@cython.final
cdef class AideSequences:
    cdef public double surfacearea
    cdef public numpy.int64_t _surfacearea_ndim
    cdef public numpy.int64_t _surfacearea_length
    cdef public double[:] _surfacearea_points
    cdef public double[:] _surfacearea_results
    cdef public double alloweddischarge
    cdef public numpy.int64_t _alloweddischarge_ndim
    cdef public numpy.int64_t _alloweddischarge_length
    cdef public double[:] _alloweddischarge_points
    cdef public double[:] _alloweddischarge_results
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
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef double *_s_pointer
    cdef public double r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef double *_r_pointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class SenderSequences:
    cdef public double d
    cdef public numpy.int64_t _d_ndim
    cdef public numpy.int64_t _d_length
    cdef public bint _d_ramflag
    cdef public double[:] _d_array
    cdef public bint _d_diskflag_reading
    cdef public bint _d_diskflag_writing
    cdef public double[:] _d_ncarray
    cdef double *_d_pointer
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef double *_s_pointer
    cdef public double r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef double *_r_pointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class NumConsts:
    cdef public numpy.int64_t nmb_methods
    cdef public numpy.int64_t nmb_stages
    cdef public double dt_increase
    cdef public double dt_decrease
    cdef public configutils.Config pub
    cdef public double[:, :, :] a_coefs
@cython.final
cdef class NumVars:
    cdef public bint use_relerror
    cdef public numpy.int64_t nmb_calls
    cdef public numpy.int64_t idx_method
    cdef public numpy.int64_t idx_stage
    cdef public double t0
    cdef public double t1
    cdef public double dt
    cdef public double dt_est
    cdef public double abserror
    cdef public double relerror
    cdef public double last_abserror
    cdef public double last_relerror
    cdef public double extrapolated_abserror
    cdef public double extrapolated_relerror
    cdef public numpy.npy_bool f0_ready
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface pemodel
    cdef public numpy.npy_bool pemodel_is_mainmodel
    cdef public numpy.int64_t pemodel_typeid
    cdef public masterinterface.MasterInterface precipmodel
    cdef public numpy.npy_bool precipmodel_is_mainmodel
    cdef public numpy.int64_t precipmodel_typeid
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void new2old(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef inline void solve(self) noexcept nogil
    cpdef inline void calculate_single_terms(self) noexcept nogil
    cpdef inline void calculate_full_terms(self) noexcept nogil
    cpdef inline void get_point_states(self) noexcept nogil
    cpdef inline void set_point_states(self) noexcept nogil
    cpdef inline void set_result_states(self) noexcept nogil
    cpdef inline void get_sum_fluxes(self) noexcept nogil
    cpdef inline void set_point_fluxes(self) noexcept nogil
    cpdef inline void set_result_fluxes(self) noexcept nogil
    cpdef inline void integrate_fluxes(self) noexcept nogil
    cpdef inline void reset_sum_fluxes(self) noexcept nogil
    cpdef inline void addup_fluxes(self) noexcept nogil
    cpdef inline void calculate_error(self) noexcept nogil
    cpdef inline void extrapolate_error(self) noexcept nogil
    cpdef inline void pic_totalremotedischarge_v1(self) noexcept nogil
    cpdef inline void update_loggedtotalremotedischarge_v1(self) noexcept nogil
    cpdef inline void pick_loggedouterwaterlevel_v1(self) noexcept nogil
    cpdef inline void pick_loggedremotewaterlevel_v1(self) noexcept nogil
    cpdef inline void pic_loggedrequiredremoterelease_v1(self) noexcept nogil
    cpdef inline void pic_loggedrequiredremoterelease_v2(self) noexcept nogil
    cpdef inline void pic_exchange_v1(self) noexcept nogil
    cpdef inline void calc_requiredremoterelease_v2(self) noexcept nogil
    cpdef inline void pic_loggedallowedremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_allowedremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_precipitation_v1(self) noexcept nogil
    cpdef inline void calc_adjustedprecipitation_v1(self) noexcept nogil
    cpdef inline void calc_potentialevaporation_v1(self) noexcept nogil
    cpdef inline void calc_adjustedevaporation_v1(self) noexcept nogil
    cpdef inline void calc_actualevaporation_v1(self) noexcept nogil
    cpdef inline void pic_inflow_v1(self) noexcept nogil
    cpdef inline void pic_inflow_v2(self) noexcept nogil
    cpdef inline void calc_naturalremotedischarge_v1(self) noexcept nogil
    cpdef inline void calc_remotedemand_v1(self) noexcept nogil
    cpdef inline void calc_remotefailure_v1(self) noexcept nogil
    cpdef inline void calc_requiredremoterelease_v1(self) noexcept nogil
    cpdef inline void calc_requiredrelease_v1(self) noexcept nogil
    cpdef inline void calc_requiredrelease_v2(self) noexcept nogil
    cpdef inline void calc_targetedrelease_v1(self) noexcept nogil
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil
    cpdef inline void calc_outerwaterlevel_v1(self) noexcept nogil
    cpdef inline void calc_remotewaterlevel_v1(self) noexcept nogil
    cpdef inline void calc_waterleveldifference_v1(self) noexcept nogil
    cpdef inline void calc_effectivewaterleveldifference_v1(self) noexcept nogil
    cpdef inline void calc_surfacearea_v1(self) noexcept nogil
    cpdef inline void calc_alloweddischarge_v1(self) noexcept nogil
    cpdef inline void calc_alloweddischarge_v2(self) noexcept nogil
    cpdef inline void calc_actualrelease_v1(self) noexcept nogil
    cpdef inline void calc_actualrelease_v2(self) noexcept nogil
    cpdef inline void calc_actualrelease_v3(self) noexcept nogil
    cpdef inline void calc_possibleremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_actualremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_actualremoterelease_v1(self) noexcept nogil
    cpdef inline void update_actualremoterelief_v1(self) noexcept nogil
    cpdef inline void update_actualremoterelease_v1(self) noexcept nogil
    cpdef inline void calc_flooddischarge_v1(self) noexcept nogil
    cpdef inline void calc_maxforceddischarge_v1(self) noexcept nogil
    cpdef inline void calc_maxfreedischarge_v1(self) noexcept nogil
    cpdef inline void calc_forceddischarge_v1(self) noexcept nogil
    cpdef inline void calc_freedischarge_v1(self) noexcept nogil
    cpdef inline void calc_outflow_v1(self) noexcept nogil
    cpdef inline void calc_outflow_v2(self) noexcept nogil
    cpdef inline void calc_outflow_v3(self) noexcept nogil
    cpdef inline void calc_outflow_v4(self) noexcept nogil
    cpdef inline void calc_outflow_v5(self) noexcept nogil
    cpdef inline void update_watervolume_v1(self) noexcept nogil
    cpdef inline void update_watervolume_v2(self) noexcept nogil
    cpdef inline void update_watervolume_v3(self) noexcept nogil
    cpdef inline void update_watervolume_v4(self) noexcept nogil
    cpdef inline double fix_min1_v1(self, double input_, double threshold, double smoothpar, numpy.npy_bool relative) noexcept nogil
    cpdef inline void pass_outflow_v1(self) noexcept nogil
    cpdef inline void update_loggedoutflow_v1(self) noexcept nogil
    cpdef inline void pass_actualremoterelease_v1(self) noexcept nogil
    cpdef inline void pass_actualremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_missingremoterelease_v1(self) noexcept nogil
    cpdef inline void pass_missingremoterelease_v1(self) noexcept nogil
    cpdef inline void calc_allowedremoterelief_v2(self) noexcept nogil
    cpdef inline void pass_allowedremoterelief_v1(self) noexcept nogil
    cpdef inline void calc_requiredremotesupply_v1(self) noexcept nogil
    cpdef inline void pass_requiredremotesupply_v1(self) noexcept nogil
    cpdef inline void pic_totalremotedischarge(self) noexcept nogil
    cpdef inline void update_loggedtotalremotedischarge(self) noexcept nogil
    cpdef inline void pick_loggedouterwaterlevel(self) noexcept nogil
    cpdef inline void pick_loggedremotewaterlevel(self) noexcept nogil
    cpdef inline void pic_exchange(self) noexcept nogil
    cpdef inline void pic_loggedallowedremoterelief(self) noexcept nogil
    cpdef inline void calc_precipitation(self) noexcept nogil
    cpdef inline void calc_adjustedprecipitation(self) noexcept nogil
    cpdef inline void calc_potentialevaporation(self) noexcept nogil
    cpdef inline void calc_adjustedevaporation(self) noexcept nogil
    cpdef inline void calc_actualevaporation(self) noexcept nogil
    cpdef inline void calc_naturalremotedischarge(self) noexcept nogil
    cpdef inline void calc_remotedemand(self) noexcept nogil
    cpdef inline void calc_remotefailure(self) noexcept nogil
    cpdef inline void calc_targetedrelease(self) noexcept nogil
    cpdef inline void calc_waterlevel(self) noexcept nogil
    cpdef inline void calc_outerwaterlevel(self) noexcept nogil
    cpdef inline void calc_remotewaterlevel(self) noexcept nogil
    cpdef inline void calc_waterleveldifference(self) noexcept nogil
    cpdef inline void calc_effectivewaterleveldifference(self) noexcept nogil
    cpdef inline void calc_surfacearea(self) noexcept nogil
    cpdef inline void calc_possibleremoterelief(self) noexcept nogil
    cpdef inline void calc_actualremoterelief(self) noexcept nogil
    cpdef inline void calc_actualremoterelease(self) noexcept nogil
    cpdef inline void update_actualremoterelief(self) noexcept nogil
    cpdef inline void update_actualremoterelease(self) noexcept nogil
    cpdef inline void calc_flooddischarge(self) noexcept nogil
    cpdef inline void calc_maxforceddischarge(self) noexcept nogil
    cpdef inline void calc_maxfreedischarge(self) noexcept nogil
    cpdef inline void calc_forceddischarge(self) noexcept nogil
    cpdef inline void calc_freedischarge(self) noexcept nogil
    cpdef inline double fix_min1(self, double input_, double threshold, double smoothpar, numpy.npy_bool relative) noexcept nogil
    cpdef inline void pass_outflow(self) noexcept nogil
    cpdef inline void update_loggedoutflow(self) noexcept nogil
    cpdef inline void pass_actualremoterelease(self) noexcept nogil
    cpdef inline void pass_actualremoterelief(self) noexcept nogil
    cpdef inline void calc_missingremoterelease(self) noexcept nogil
    cpdef inline void pass_missingremoterelease(self) noexcept nogil
    cpdef inline void pass_allowedremoterelief(self) noexcept nogil
    cpdef inline void calc_requiredremotesupply(self) noexcept nogil
    cpdef inline void pass_requiredremotesupply(self) noexcept nogil
