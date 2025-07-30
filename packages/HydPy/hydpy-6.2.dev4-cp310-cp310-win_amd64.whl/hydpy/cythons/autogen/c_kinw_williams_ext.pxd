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
    cdef public double laen
    cdef public numpy.int64_t gts
    cdef public interputils.SimpleInterpolator vg2fg
    cdef public double ek
@cython.final
cdef class DerivedParameters:
    cdef public double sek
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public StateSequences states
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
    cdef public double qza
    cdef public numpy.int64_t _qza_ndim
    cdef public numpy.int64_t _qza_length
    cdef public double[:] _qza_points
    cdef public double[:] _qza_results
    cdef public double[:] _qza_integrals
    cdef public double _qza_sum
    cdef public bint _qza_ramflag
    cdef public double[:] _qza_array
    cdef public bint _qza_diskflag_reading
    cdef public bint _qza_diskflag_writing
    cdef public double[:] _qza_ncarray
    cdef public bint _qza_outputflag
    cdef double *_qza_outputpointer
    cdef public double[:] qg
    cdef public numpy.int64_t _qg_ndim
    cdef public numpy.int64_t _qg_length
    cdef public numpy.int64_t _qg_length_0
    cdef public double[:,:] _qg_points
    cdef public double[:,:] _qg_results
    cdef public double[:,:] _qg_integrals
    cdef public double[:] _qg_sum
    cdef public bint _qg_ramflag
    cdef public double[:,:] _qg_array
    cdef public bint _qg_diskflag_reading
    cdef public bint _qg_diskflag_writing
    cdef public double[:] _qg_ncarray
    cdef public double qa
    cdef public numpy.int64_t _qa_ndim
    cdef public numpy.int64_t _qa_length
    cdef public double[:] _qa_points
    cdef public double[:] _qa_results
    cdef public double[:] _qa_integrals
    cdef public double _qa_sum
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
    cdef public double[:] vg
    cdef public numpy.int64_t _vg_ndim
    cdef public numpy.int64_t _vg_length
    cdef public numpy.int64_t _vg_length_0
    cdef public double[:,:] _vg_points
    cdef public double[:,:] _vg_results
    cdef public bint _vg_ramflag
    cdef public double[:,:] _vg_array
    cdef public bint _vg_diskflag_reading
    cdef public bint _vg_diskflag_writing
    cdef public double[:] _vg_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
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
    cpdef inline void pick_q_v1(self) noexcept nogil
    cpdef inline void calc_qza_v1(self) noexcept nogil
    cpdef inline void calc_qg_v2(self) noexcept nogil
    cpdef inline void calc_qa_v1(self) noexcept nogil
    cpdef inline void update_vg_v1(self) noexcept nogil
    cpdef inline void pass_q_v1(self) noexcept nogil
    cpdef inline void pick_q(self) noexcept nogil
    cpdef inline void calc_qza(self) noexcept nogil
    cpdef inline void calc_qg(self) noexcept nogil
    cpdef inline void calc_qa(self) noexcept nogil
    cpdef inline void update_vg(self) noexcept nogil
    cpdef inline void pass_q(self) noexcept nogil
