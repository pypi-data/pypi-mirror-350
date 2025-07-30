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
@cython.final
cdef class ControlParameters:
    cdef public double area
    cdef public double imax
    cdef public double x1
    cdef public double x2
    cdef public double x3
    cdef public double x5
    cdef public double x6
@cython.final
cdef class DerivedParameters:
    cdef public double beta
    cdef public double qfactor
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
    cdef public double p
    cdef public numpy.int64_t _p_ndim
    cdef public numpy.int64_t _p_length
    cdef public bint _p_ramflag
    cdef public double[:] _p_array
    cdef public bint _p_diskflag_reading
    cdef public bint _p_diskflag_writing
    cdef public double[:] _p_ncarray
    cdef public bint _p_inputflag
    cdef double *_p_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FluxSequences:
    cdef public double e
    cdef public numpy.int64_t _e_ndim
    cdef public numpy.int64_t _e_length
    cdef public bint _e_ramflag
    cdef public double[:] _e_array
    cdef public bint _e_diskflag_reading
    cdef public bint _e_diskflag_writing
    cdef public double[:] _e_ncarray
    cdef public bint _e_outputflag
    cdef double *_e_outputpointer
    cdef public double en
    cdef public numpy.int64_t _en_ndim
    cdef public numpy.int64_t _en_length
    cdef public bint _en_ramflag
    cdef public double[:] _en_array
    cdef public bint _en_diskflag_reading
    cdef public bint _en_diskflag_writing
    cdef public double[:] _en_ncarray
    cdef public bint _en_outputflag
    cdef double *_en_outputpointer
    cdef public double pn
    cdef public numpy.int64_t _pn_ndim
    cdef public numpy.int64_t _pn_length
    cdef public bint _pn_ramflag
    cdef public double[:] _pn_array
    cdef public bint _pn_diskflag_reading
    cdef public bint _pn_diskflag_writing
    cdef public double[:] _pn_ncarray
    cdef public bint _pn_outputflag
    cdef double *_pn_outputpointer
    cdef public double ps
    cdef public numpy.int64_t _ps_ndim
    cdef public numpy.int64_t _ps_length
    cdef public bint _ps_ramflag
    cdef public double[:] _ps_array
    cdef public bint _ps_diskflag_reading
    cdef public bint _ps_diskflag_writing
    cdef public double[:] _ps_ncarray
    cdef public bint _ps_outputflag
    cdef double *_ps_outputpointer
    cdef public double ei
    cdef public numpy.int64_t _ei_ndim
    cdef public numpy.int64_t _ei_length
    cdef public bint _ei_ramflag
    cdef public double[:] _ei_array
    cdef public bint _ei_diskflag_reading
    cdef public bint _ei_diskflag_writing
    cdef public double[:] _ei_ncarray
    cdef public bint _ei_outputflag
    cdef double *_ei_outputpointer
    cdef public double es
    cdef public numpy.int64_t _es_ndim
    cdef public numpy.int64_t _es_length
    cdef public bint _es_ramflag
    cdef public double[:] _es_array
    cdef public bint _es_diskflag_reading
    cdef public bint _es_diskflag_writing
    cdef public double[:] _es_ncarray
    cdef public bint _es_outputflag
    cdef double *_es_outputpointer
    cdef public double ae
    cdef public numpy.int64_t _ae_ndim
    cdef public numpy.int64_t _ae_length
    cdef public bint _ae_ramflag
    cdef public double[:] _ae_array
    cdef public bint _ae_diskflag_reading
    cdef public bint _ae_diskflag_writing
    cdef public double[:] _ae_ncarray
    cdef public bint _ae_outputflag
    cdef double *_ae_outputpointer
    cdef public double pr
    cdef public numpy.int64_t _pr_ndim
    cdef public numpy.int64_t _pr_length
    cdef public bint _pr_ramflag
    cdef public double[:] _pr_array
    cdef public bint _pr_diskflag_reading
    cdef public bint _pr_diskflag_writing
    cdef public double[:] _pr_ncarray
    cdef public bint _pr_outputflag
    cdef double *_pr_outputpointer
    cdef public double pr9
    cdef public numpy.int64_t _pr9_ndim
    cdef public numpy.int64_t _pr9_length
    cdef public bint _pr9_ramflag
    cdef public double[:] _pr9_array
    cdef public bint _pr9_diskflag_reading
    cdef public bint _pr9_diskflag_writing
    cdef public double[:] _pr9_ncarray
    cdef public bint _pr9_outputflag
    cdef double *_pr9_outputpointer
    cdef public double pr1
    cdef public numpy.int64_t _pr1_ndim
    cdef public numpy.int64_t _pr1_length
    cdef public bint _pr1_ramflag
    cdef public double[:] _pr1_array
    cdef public bint _pr1_diskflag_reading
    cdef public bint _pr1_diskflag_writing
    cdef public double[:] _pr1_ncarray
    cdef public bint _pr1_outputflag
    cdef double *_pr1_outputpointer
    cdef public double perc
    cdef public numpy.int64_t _perc_ndim
    cdef public numpy.int64_t _perc_length
    cdef public bint _perc_ramflag
    cdef public double[:] _perc_array
    cdef public bint _perc_diskflag_reading
    cdef public bint _perc_diskflag_writing
    cdef public double[:] _perc_ncarray
    cdef public bint _perc_outputflag
    cdef double *_perc_outputpointer
    cdef public double q9
    cdef public numpy.int64_t _q9_ndim
    cdef public numpy.int64_t _q9_length
    cdef public bint _q9_ramflag
    cdef public double[:] _q9_array
    cdef public bint _q9_diskflag_reading
    cdef public bint _q9_diskflag_writing
    cdef public double[:] _q9_ncarray
    cdef public bint _q9_outputflag
    cdef double *_q9_outputpointer
    cdef public double q1
    cdef public numpy.int64_t _q1_ndim
    cdef public numpy.int64_t _q1_length
    cdef public bint _q1_ramflag
    cdef public double[:] _q1_array
    cdef public bint _q1_diskflag_reading
    cdef public bint _q1_diskflag_writing
    cdef public double[:] _q1_ncarray
    cdef public bint _q1_outputflag
    cdef double *_q1_outputpointer
    cdef public double fd
    cdef public numpy.int64_t _fd_ndim
    cdef public numpy.int64_t _fd_length
    cdef public bint _fd_ramflag
    cdef public double[:] _fd_array
    cdef public bint _fd_diskflag_reading
    cdef public bint _fd_diskflag_writing
    cdef public double[:] _fd_ncarray
    cdef public bint _fd_outputflag
    cdef double *_fd_outputpointer
    cdef public double fr
    cdef public numpy.int64_t _fr_ndim
    cdef public numpy.int64_t _fr_length
    cdef public bint _fr_ramflag
    cdef public double[:] _fr_array
    cdef public bint _fr_diskflag_reading
    cdef public bint _fr_diskflag_writing
    cdef public double[:] _fr_ncarray
    cdef public bint _fr_outputflag
    cdef double *_fr_outputpointer
    cdef public double fr2
    cdef public numpy.int64_t _fr2_ndim
    cdef public numpy.int64_t _fr2_length
    cdef public bint _fr2_ramflag
    cdef public double[:] _fr2_array
    cdef public bint _fr2_diskflag_reading
    cdef public bint _fr2_diskflag_writing
    cdef public double[:] _fr2_ncarray
    cdef public bint _fr2_outputflag
    cdef double *_fr2_outputpointer
    cdef public double qr
    cdef public numpy.int64_t _qr_ndim
    cdef public numpy.int64_t _qr_length
    cdef public bint _qr_ramflag
    cdef public double[:] _qr_array
    cdef public bint _qr_diskflag_reading
    cdef public bint _qr_diskflag_writing
    cdef public double[:] _qr_ncarray
    cdef public bint _qr_outputflag
    cdef double *_qr_outputpointer
    cdef public double qr2
    cdef public numpy.int64_t _qr2_ndim
    cdef public numpy.int64_t _qr2_length
    cdef public bint _qr2_ramflag
    cdef public double[:] _qr2_array
    cdef public bint _qr2_diskflag_reading
    cdef public bint _qr2_diskflag_writing
    cdef public double[:] _qr2_ncarray
    cdef public bint _qr2_outputflag
    cdef double *_qr2_outputpointer
    cdef public double qd
    cdef public numpy.int64_t _qd_ndim
    cdef public numpy.int64_t _qd_length
    cdef public bint _qd_ramflag
    cdef public double[:] _qd_array
    cdef public bint _qd_diskflag_reading
    cdef public bint _qd_diskflag_writing
    cdef public double[:] _qd_ncarray
    cdef public bint _qd_outputflag
    cdef double *_qd_outputpointer
    cdef public double qh
    cdef public numpy.int64_t _qh_ndim
    cdef public numpy.int64_t _qh_length
    cdef public bint _qh_ramflag
    cdef public double[:] _qh_array
    cdef public bint _qh_diskflag_reading
    cdef public bint _qh_diskflag_writing
    cdef public double[:] _qh_ncarray
    cdef public bint _qh_outputflag
    cdef double *_qh_outputpointer
    cdef public double qv
    cdef public numpy.int64_t _qv_ndim
    cdef public numpy.int64_t _qv_length
    cdef public bint _qv_ramflag
    cdef public double[:] _qv_array
    cdef public bint _qv_diskflag_reading
    cdef public bint _qv_diskflag_writing
    cdef public double[:] _qv_ncarray
    cdef public bint _qv_outputflag
    cdef double *_qv_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double i
    cdef public numpy.int64_t _i_ndim
    cdef public numpy.int64_t _i_length
    cdef public bint _i_ramflag
    cdef public double[:] _i_array
    cdef public bint _i_diskflag_reading
    cdef public bint _i_diskflag_writing
    cdef public double[:] _i_ncarray
    cdef public bint _i_outputflag
    cdef double *_i_outputpointer
    cdef public double s
    cdef public numpy.int64_t _s_ndim
    cdef public numpy.int64_t _s_length
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_diskflag_reading
    cdef public bint _s_diskflag_writing
    cdef public double[:] _s_ncarray
    cdef public bint _s_outputflag
    cdef double *_s_outputpointer
    cdef public double r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef public bint _r_outputflag
    cdef double *_r_outputpointer
    cdef public double r2
    cdef public numpy.int64_t _r2_ndim
    cdef public numpy.int64_t _r2_length
    cdef public bint _r2_ramflag
    cdef public double[:] _r2_array
    cdef public bint _r2_diskflag_reading
    cdef public bint _r2_diskflag_writing
    cdef public double[:] _r2_ncarray
    cdef public bint _r2_outputflag
    cdef double *_r2_outputpointer
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
cdef class Model:
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface petmodel
    cdef public numpy.npy_bool petmodel_is_mainmodel
    cdef public numpy.int64_t petmodel_typeid
    cdef public masterinterface.MasterInterface rconcmodel_directflow
    cdef public numpy.npy_bool rconcmodel_directflow_is_mainmodel
    cdef public numpy.int64_t rconcmodel_directflow_typeid
    cdef public masterinterface.MasterInterface rconcmodel_routingstore
    cdef public numpy.npy_bool rconcmodel_routingstore_is_mainmodel
    cdef public numpy.int64_t rconcmodel_routingstore_typeid
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
    cpdef inline void calc_e_v1(self) noexcept nogil
    cpdef inline void calc_ei_v1(self) noexcept nogil
    cpdef inline void calc_pn_v1(self) noexcept nogil
    cpdef inline void calc_en_v1(self) noexcept nogil
    cpdef inline void update_i_v1(self) noexcept nogil
    cpdef inline void calc_ps_v1(self) noexcept nogil
    cpdef inline void calc_es_v1(self) noexcept nogil
    cpdef inline void update_s_v1(self) noexcept nogil
    cpdef inline void calc_perc_v1(self) noexcept nogil
    cpdef inline void update_s_v2(self) noexcept nogil
    cpdef inline void calc_ae_v1(self) noexcept nogil
    cpdef inline void calc_pr_v1(self) noexcept nogil
    cpdef inline void calc_pr1_pr9_v1(self) noexcept nogil
    cpdef inline void calc_q9_v1(self) noexcept nogil
    cpdef inline void calc_q1_v1(self) noexcept nogil
    cpdef inline void calc_fr_v2(self) noexcept nogil
    cpdef inline void calc_fr2_v1(self) noexcept nogil
    cpdef inline void update_r_v2(self) noexcept nogil
    cpdef inline void calc_qr_v1(self) noexcept nogil
    cpdef inline void update_r_v3(self) noexcept nogil
    cpdef inline void update_r2_v1(self) noexcept nogil
    cpdef inline void calc_qr2_r2_v1(self) noexcept nogil
    cpdef inline void calc_fd_v1(self) noexcept nogil
    cpdef inline void calc_qd_v1(self) noexcept nogil
    cpdef inline void calc_qh_v2(self) noexcept nogil
    cpdef inline void calc_qv_v1(self) noexcept nogil
    cpdef inline void calc_e_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline double calc_q_rconcmodel_v1(self, masterinterface.MasterInterface submodel, double inflow) noexcept nogil
    cpdef inline void pass_q_v1(self) noexcept nogil
    cpdef inline void calc_e(self) noexcept nogil
    cpdef inline void calc_ei(self) noexcept nogil
    cpdef inline void calc_pn(self) noexcept nogil
    cpdef inline void calc_en(self) noexcept nogil
    cpdef inline void update_i(self) noexcept nogil
    cpdef inline void calc_ps(self) noexcept nogil
    cpdef inline void calc_es(self) noexcept nogil
    cpdef inline void calc_perc(self) noexcept nogil
    cpdef inline void calc_ae(self) noexcept nogil
    cpdef inline void calc_pr(self) noexcept nogil
    cpdef inline void calc_pr1_pr9(self) noexcept nogil
    cpdef inline void calc_q9(self) noexcept nogil
    cpdef inline void calc_q1(self) noexcept nogil
    cpdef inline void calc_fr(self) noexcept nogil
    cpdef inline void calc_fr2(self) noexcept nogil
    cpdef inline void calc_qr(self) noexcept nogil
    cpdef inline void update_r2(self) noexcept nogil
    cpdef inline void calc_qr2_r2(self) noexcept nogil
    cpdef inline void calc_fd(self) noexcept nogil
    cpdef inline void calc_qd(self) noexcept nogil
    cpdef inline void calc_qh(self) noexcept nogil
    cpdef inline void calc_qv(self) noexcept nogil
    cpdef inline void calc_e_petmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline double calc_q_rconcmodel(self, masterinterface.MasterInterface submodel, double inflow) noexcept nogil
    cpdef inline void pass_q(self) noexcept nogil
