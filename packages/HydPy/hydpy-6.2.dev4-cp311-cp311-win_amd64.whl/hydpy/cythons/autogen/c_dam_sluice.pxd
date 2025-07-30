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
cdef public numpy.npy_bool TYPE_CHECKING = False
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double surfacearea
    cdef public double catchmentarea
    cdef public double correctionprecipitation
    cdef public double correctionevaporation
    cdef public double weightevaporation
    cdef public double remotewaterlevelmaximumthreshold
    cdef public double remotewaterlevelmaximumtolerance
    cdef public double thresholdevaporation
    cdef public double toleranceevaporation
    cdef public interputils.SimpleInterpolator watervolume2waterlevel
    cdef public interputils.SeasonalInterpolator waterleveldifference2maxfreedischarge
    cdef public double dischargetolerance
    cdef public double crestlevel
    cdef public double crestleveltolerance
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] toy
    cdef public double seconds
    cdef public double inputfactor
    cdef public double remotewaterlevelmaximumsmoothpar
    cdef public double smoothparevaporation
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
cdef class ReceiverSequences:
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
    cdef public double[:] loggedadjustedevaporation
    cdef public numpy.int64_t _loggedadjustedevaporation_ndim
    cdef public numpy.int64_t _loggedadjustedevaporation_length
    cdef public numpy.int64_t _loggedadjustedevaporation_length_0
    cdef public double[:] loggedouterwaterlevel
    cdef public numpy.int64_t _loggedouterwaterlevel_ndim
    cdef public numpy.int64_t _loggedouterwaterlevel_length
    cdef public numpy.int64_t _loggedouterwaterlevel_length_0
    cdef public double[:] loggedremotewaterlevel
    cdef public numpy.int64_t _loggedremotewaterlevel_ndim
    cdef public numpy.int64_t _loggedremotewaterlevel_length
    cdef public numpy.int64_t _loggedremotewaterlevel_length_0
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
    cpdef inline void pick_loggedouterwaterlevel_v1(self) noexcept nogil
    cpdef inline void pick_loggedremotewaterlevel_v1(self) noexcept nogil
    cpdef inline void calc_precipitation_v1(self) noexcept nogil
    cpdef inline void calc_potentialevaporation_v1(self) noexcept nogil
    cpdef inline void calc_adjustedevaporation_v1(self) noexcept nogil
    cpdef inline void calc_adjustedprecipitation_v1(self) noexcept nogil
    cpdef inline void pic_inflow_v1(self) noexcept nogil
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil
    cpdef inline void calc_outerwaterlevel_v1(self) noexcept nogil
    cpdef inline void calc_remotewaterlevel_v1(self) noexcept nogil
    cpdef inline void calc_effectivewaterleveldifference_v1(self) noexcept nogil
    cpdef inline void calc_maxfreedischarge_v1(self) noexcept nogil
    cpdef inline void calc_freedischarge_v1(self) noexcept nogil
    cpdef inline void calc_actualevaporation_v1(self) noexcept nogil
    cpdef inline void calc_outflow_v4(self) noexcept nogil
    cpdef inline void update_watervolume_v1(self) noexcept nogil
    cpdef inline void pass_outflow_v1(self) noexcept nogil
    cpdef inline void pick_loggedouterwaterlevel(self) noexcept nogil
    cpdef inline void pick_loggedremotewaterlevel(self) noexcept nogil
    cpdef inline void calc_precipitation(self) noexcept nogil
    cpdef inline void calc_potentialevaporation(self) noexcept nogil
    cpdef inline void calc_adjustedevaporation(self) noexcept nogil
    cpdef inline void calc_adjustedprecipitation(self) noexcept nogil
    cpdef inline void pic_inflow(self) noexcept nogil
    cpdef inline void calc_waterlevel(self) noexcept nogil
    cpdef inline void calc_outerwaterlevel(self) noexcept nogil
    cpdef inline void calc_remotewaterlevel(self) noexcept nogil
    cpdef inline void calc_effectivewaterleveldifference(self) noexcept nogil
    cpdef inline void calc_maxfreedischarge(self) noexcept nogil
    cpdef inline void calc_freedischarge(self) noexcept nogil
    cpdef inline void calc_actualevaporation(self) noexcept nogil
    cpdef inline void calc_outflow(self) noexcept nogil
    cpdef inline void update_watervolume(self) noexcept nogil
    cpdef inline void pass_outflow(self) noexcept nogil
