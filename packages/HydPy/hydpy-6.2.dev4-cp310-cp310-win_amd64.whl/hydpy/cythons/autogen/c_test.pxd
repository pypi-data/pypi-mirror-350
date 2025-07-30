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
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double k
    cdef public numpy.int64_t n
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class FluxSequences:
    cdef public double q
    cdef public numpy.int64_t _q_ndim
    cdef public numpy.int64_t _q_length
    cdef public double[:] _q_points
    cdef public double[:] _q_results
    cdef public double[:] _q_integrals
    cdef public double _q_sum
    cdef public bint _q_ramflag
    cdef public double[:] _q_array
    cdef public bint _q_diskflag_reading
    cdef public bint _q_diskflag_writing
    cdef public double[:] _q_ncarray
    cdef public bint _q_outputflag
    cdef double *_q_outputpointer
    cdef public double[:] qv
    cdef public numpy.int64_t _qv_ndim
    cdef public numpy.int64_t _qv_length
    cdef public numpy.int64_t _qv_length_0
    cdef public double[:,:] _qv_points
    cdef public double[:,:] _qv_results
    cdef public double[:,:] _qv_integrals
    cdef public double[:] _qv_sum
    cdef public bint _qv_ramflag
    cdef public double[:,:] _qv_array
    cdef public bint _qv_diskflag_reading
    cdef public bint _qv_diskflag_writing
    cdef public double[:] _qv_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public double[:] _s_points
    cdef public double[:] _s_results
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef public bint _s_outputflag
    cdef double *_s_outputpointer
    cdef public double[:] sv
    cdef public numpy.int64_t _sv_ndim
    cdef public numpy.int64_t _sv_length
    cdef public numpy.int64_t _sv_length_0
    cdef public double[:,:] _sv_points
    cdef public double[:,:] _sv_results
    cdef public bint _sv_ramflag
    cdef public double[:,:] _sv_array
    cdef public bint _sv_diskflag_reading
    cdef public bint _sv_diskflag_writing
    cdef public double[:] _sv_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
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
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
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
    cpdef inline void calc_q_v1(self) noexcept nogil
    cpdef inline void calc_q_v2(self) noexcept nogil
    cpdef inline void calc_qv_v1(self) noexcept nogil
    cpdef inline void calc_s_v1(self) noexcept nogil
    cpdef inline void calc_sv_v1(self) noexcept nogil
    cpdef inline void calc_qv(self) noexcept nogil
    cpdef inline void calc_s(self) noexcept nogil
    cpdef inline void calc_sv(self) noexcept nogil
