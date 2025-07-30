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
    cdef public FixedParameters fixed
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double laen
    cdef public double gef
    cdef public numpy.int64_t gts
    cdef public double hm
    cdef public double bm
    cdef public double bnm
    cdef public double[:] bv
    cdef public double[:] bbv
    cdef public double[:] bnv
    cdef public double[:] bnvr
    cdef public double skm
    cdef public double[:] skv
    cdef public double ekm
    cdef public double[:] ekv
    cdef public double hr
@cython.final
cdef class DerivedParameters:
    cdef public double sek
    cdef public double[:] hv
    cdef public double mfm
    cdef public double[:] mfv
    cdef public double bnmf
    cdef public double[:] bnvf
    cdef public double[:] bnvrf
    cdef public double hrp
@cython.final
cdef class FixedParameters:
    cdef public double wbmin
    cdef public double wbreg
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
    cdef public double[:] dh
    cdef public numpy.int64_t _dh_ndim
    cdef public numpy.int64_t _dh_length
    cdef public numpy.int64_t _dh_length_0
    cdef public double[:,:] _dh_points
    cdef public double[:,:] _dh_results
    cdef public double[:,:] _dh_integrals
    cdef public double[:] _dh_sum
    cdef public bint _dh_ramflag
    cdef public double[:,:] _dh_array
    cdef public bint _dh_diskflag_reading
    cdef public bint _dh_diskflag_writing
    cdef public double[:] _dh_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double[:] h
    cdef public numpy.int64_t _h_ndim
    cdef public numpy.int64_t _h_length
    cdef public numpy.int64_t _h_length_0
    cdef public double[:,:] _h_points
    cdef public double[:,:] _h_results
    cdef public bint _h_ramflag
    cdef public double[:,:] _h_array
    cdef public bint _h_diskflag_reading
    cdef public bint _h_diskflag_writing
    cdef public double[:] _h_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class AideSequences:
    cdef public double[:] wbm
    cdef public numpy.int64_t _wbm_ndim
    cdef public numpy.int64_t _wbm_length
    cdef public numpy.int64_t _wbm_length_0
    cdef public double[:] wblv
    cdef public numpy.int64_t _wblv_ndim
    cdef public numpy.int64_t _wblv_length
    cdef public numpy.int64_t _wblv_length_0
    cdef public double[:] wbrv
    cdef public numpy.int64_t _wbrv_ndim
    cdef public numpy.int64_t _wbrv_length
    cdef public numpy.int64_t _wbrv_length_0
    cdef public double[:] wblvr
    cdef public numpy.int64_t _wblvr_ndim
    cdef public numpy.int64_t _wblvr_length
    cdef public numpy.int64_t _wblvr_length_0
    cdef public double[:] wbrvr
    cdef public numpy.int64_t _wbrvr_ndim
    cdef public numpy.int64_t _wbrvr_length
    cdef public numpy.int64_t _wbrvr_length_0
    cdef public double[:] wbg
    cdef public numpy.int64_t _wbg_ndim
    cdef public numpy.int64_t _wbg_length
    cdef public numpy.int64_t _wbg_length_0
    cdef public double[:] am
    cdef public numpy.int64_t _am_ndim
    cdef public numpy.int64_t _am_length
    cdef public numpy.int64_t _am_length_0
    cdef public double[:] alv
    cdef public numpy.int64_t _alv_ndim
    cdef public numpy.int64_t _alv_length
    cdef public numpy.int64_t _alv_length_0
    cdef public double[:] arv
    cdef public numpy.int64_t _arv_ndim
    cdef public numpy.int64_t _arv_length
    cdef public numpy.int64_t _arv_length_0
    cdef public double[:] alvr
    cdef public numpy.int64_t _alvr_ndim
    cdef public numpy.int64_t _alvr_length
    cdef public numpy.int64_t _alvr_length_0
    cdef public double[:] arvr
    cdef public numpy.int64_t _arvr_ndim
    cdef public numpy.int64_t _arvr_length
    cdef public numpy.int64_t _arvr_length_0
    cdef public double[:] ag
    cdef public numpy.int64_t _ag_ndim
    cdef public numpy.int64_t _ag_length
    cdef public numpy.int64_t _ag_length_0
    cdef public double[:] um
    cdef public numpy.int64_t _um_ndim
    cdef public numpy.int64_t _um_length
    cdef public numpy.int64_t _um_length_0
    cdef public double[:] ulv
    cdef public numpy.int64_t _ulv_ndim
    cdef public numpy.int64_t _ulv_length
    cdef public numpy.int64_t _ulv_length_0
    cdef public double[:] urv
    cdef public numpy.int64_t _urv_ndim
    cdef public numpy.int64_t _urv_length
    cdef public numpy.int64_t _urv_length_0
    cdef public double[:] ulvr
    cdef public numpy.int64_t _ulvr_ndim
    cdef public numpy.int64_t _ulvr_length
    cdef public numpy.int64_t _ulvr_length_0
    cdef public double[:] urvr
    cdef public numpy.int64_t _urvr_ndim
    cdef public numpy.int64_t _urvr_length
    cdef public numpy.int64_t _urvr_length_0
    cdef public double[:] qm
    cdef public numpy.int64_t _qm_ndim
    cdef public numpy.int64_t _qm_length
    cdef public numpy.int64_t _qm_length_0
    cdef public double[:] qlv
    cdef public numpy.int64_t _qlv_ndim
    cdef public numpy.int64_t _qlv_length
    cdef public numpy.int64_t _qlv_length_0
    cdef public double[:] qrv
    cdef public numpy.int64_t _qrv_ndim
    cdef public numpy.int64_t _qrv_length
    cdef public numpy.int64_t _qrv_length_0
    cdef public double[:] qlvr
    cdef public numpy.int64_t _qlvr_ndim
    cdef public numpy.int64_t _qlvr_length
    cdef public numpy.int64_t _qlvr_length_0
    cdef public double[:] qrvr
    cdef public numpy.int64_t _qrvr_ndim
    cdef public numpy.int64_t _qrvr_length
    cdef public numpy.int64_t _qrvr_length_0
    cdef public double[:] rhm
    cdef public numpy.int64_t _rhm_ndim
    cdef public numpy.int64_t _rhm_length
    cdef public numpy.int64_t _rhm_length_0
    cdef public double[:] rhmdh
    cdef public numpy.int64_t _rhmdh_ndim
    cdef public numpy.int64_t _rhmdh_length
    cdef public numpy.int64_t _rhmdh_length_0
    cdef public double[:] rhv
    cdef public numpy.int64_t _rhv_ndim
    cdef public numpy.int64_t _rhv_length
    cdef public numpy.int64_t _rhv_length_0
    cdef public double[:] rhvdh
    cdef public numpy.int64_t _rhvdh_ndim
    cdef public numpy.int64_t _rhvdh_length
    cdef public numpy.int64_t _rhvdh_length_0
    cdef public double[:] rhlvr
    cdef public numpy.int64_t _rhlvr_ndim
    cdef public numpy.int64_t _rhlvr_length
    cdef public numpy.int64_t _rhlvr_length_0
    cdef public double[:] rhlvrdh
    cdef public numpy.int64_t _rhlvrdh_ndim
    cdef public numpy.int64_t _rhlvrdh_length
    cdef public numpy.int64_t _rhlvrdh_length_0
    cdef public double[:] rhrvr
    cdef public numpy.int64_t _rhrvr_ndim
    cdef public numpy.int64_t _rhrvr_length
    cdef public numpy.int64_t _rhrvr_length_0
    cdef public double[:] rhrvrdh
    cdef public numpy.int64_t _rhrvrdh_ndim
    cdef public numpy.int64_t _rhrvrdh_length
    cdef public numpy.int64_t _rhrvrdh_length_0
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
cdef class PegasusH(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public PegasusH pegasush
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
    cpdef inline void calc_rhm_v1(self) noexcept nogil
    cpdef inline void calc_rhmdh_v1(self) noexcept nogil
    cpdef inline void calc_rhv_v1(self) noexcept nogil
    cpdef inline void calc_rhvdh_v1(self) noexcept nogil
    cpdef inline void calc_rhlvr_rhrvr_v1(self) noexcept nogil
    cpdef inline void calc_rhlvrdh_rhrvrdh_v1(self) noexcept nogil
    cpdef inline void calc_am_um_v1(self) noexcept nogil
    cpdef inline void calc_alv_arv_ulv_urv_v1(self) noexcept nogil
    cpdef inline void calc_alvr_arvr_ulvr_urvr_v1(self) noexcept nogil
    cpdef inline void calc_qm_v1(self) noexcept nogil
    cpdef inline void calc_qlv_qrv_v1(self) noexcept nogil
    cpdef inline void calc_qlvr_qrvr_v1(self) noexcept nogil
    cpdef inline void calc_ag_v1(self) noexcept nogil
    cpdef inline void calc_qg_v1(self) noexcept nogil
    cpdef inline void calc_qa_v1(self) noexcept nogil
    cpdef inline void calc_wbm_v1(self) noexcept nogil
    cpdef inline void calc_wblv_wbrv_v1(self) noexcept nogil
    cpdef inline void calc_wblvr_wbrvr_v1(self) noexcept nogil
    cpdef inline void calc_wbg_v1(self) noexcept nogil
    cpdef inline void calc_dh_v1(self) noexcept nogil
    cpdef inline void update_h_v1(self) noexcept nogil
    cpdef inline double return_qf_v1(self, double h) noexcept nogil
    cpdef inline double return_h_v1(self) noexcept nogil
    cpdef inline void pass_q_v1(self) noexcept nogil
    cpdef inline void pick_q(self) noexcept nogil
    cpdef inline void calc_rhm(self) noexcept nogil
    cpdef inline void calc_rhmdh(self) noexcept nogil
    cpdef inline void calc_rhv(self) noexcept nogil
    cpdef inline void calc_rhvdh(self) noexcept nogil
    cpdef inline void calc_rhlvr_rhrvr(self) noexcept nogil
    cpdef inline void calc_rhlvrdh_rhrvrdh(self) noexcept nogil
    cpdef inline void calc_am_um(self) noexcept nogil
    cpdef inline void calc_alv_arv_ulv_urv(self) noexcept nogil
    cpdef inline void calc_alvr_arvr_ulvr_urvr(self) noexcept nogil
    cpdef inline void calc_qm(self) noexcept nogil
    cpdef inline void calc_qlv_qrv(self) noexcept nogil
    cpdef inline void calc_qlvr_qrvr(self) noexcept nogil
    cpdef inline void calc_ag(self) noexcept nogil
    cpdef inline void calc_qg(self) noexcept nogil
    cpdef inline void calc_qa(self) noexcept nogil
    cpdef inline void calc_wbm(self) noexcept nogil
    cpdef inline void calc_wblv_wbrv(self) noexcept nogil
    cpdef inline void calc_wblvr_wbrvr(self) noexcept nogil
    cpdef inline void calc_wbg(self) noexcept nogil
    cpdef inline void calc_dh(self) noexcept nogil
    cpdef inline void update_h(self) noexcept nogil
    cpdef inline double return_qf(self, double h) noexcept nogil
    cpdef inline double return_h(self) noexcept nogil
    cpdef inline void pass_q(self) noexcept nogil
