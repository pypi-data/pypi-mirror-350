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
cdef public numpy.int64_t SAND = 1
cdef public numpy.int64_t LOAMY_SAND = 2
cdef public numpy.int64_t SANDY_LOAM = 3
cdef public numpy.int64_t SILT_LOAM = 4
cdef public numpy.int64_t LOAM = 5
cdef public numpy.int64_t SANDY_CLAY_LOAM = 6
cdef public numpy.int64_t SILT_CLAY_LOAM = 7
cdef public numpy.int64_t CLAY_LOAM = 8
cdef public numpy.int64_t SANDY_CLAY = 9
cdef public numpy.int64_t SILTY_CLAY = 10
cdef public numpy.int64_t CLAY = 11
cdef public numpy.int64_t SEALED = 12
cdef public numpy.int64_t FIELD = 13
cdef public numpy.int64_t WINE = 14
cdef public numpy.int64_t ORCHARD = 15
cdef public numpy.int64_t SOIL = 16
cdef public numpy.int64_t PASTURE = 17
cdef public numpy.int64_t WETLAND = 18
cdef public numpy.int64_t TREES = 19
cdef public numpy.int64_t CONIFER = 20
cdef public numpy.int64_t DECIDIOUS = 21
cdef public numpy.int64_t MIXED = 22
cdef public numpy.int64_t WATER = 23
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double at
    cdef public numpy.int64_t nu
    cdef public numpy.int64_t[:] lt
    cdef public numpy.npy_bool[:] er
    cdef public double[:] aur
    cdef public double gl
    cdef public double bl
    cdef public double cp
    cdef public double[:,:] lai
    cdef public numpy.int64_t _lai_rowmin
    cdef public numpy.int64_t _lai_columnmin
    cdef public double ih
    cdef public double tt
    cdef public double ti
    cdef public double[:] ddf
    cdef public double ddt
    cdef public double cwe
    cdef public double cw
    cdef public double cv
    cdef public double cge
    cdef public double cg
    cdef public numpy.npy_bool rg
    cdef public double cgf
    cdef public double cq
    cdef public double b
    cdef public double psiae
    cdef public double thetas
    cdef public double thetar
    cdef public double ac
    cdef public double zeta1
    cdef public double zeta2
    cdef public double sh
    cdef public double st
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public numpy.int64_t nul
    cdef public numpy.int64_t nuge
    cdef public numpy.int64_t nug
    cdef public double alr
    cdef public double asr
    cdef public double agre
    cdef public double agr
    cdef public double qf
    cdef public double cd
    cdef public double rh1
    cdef public double rh2
    cdef public double rt2
@cython.final
cdef class FixedParameters:
    cdef public double pi
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
    cdef public double t
    cdef public numpy.int64_t _t_ndim
    cdef public numpy.int64_t _t_length
    cdef public bint _t_ramflag
    cdef public double[:] _t_array
    cdef public bint _t_diskflag_reading
    cdef public bint _t_diskflag_writing
    cdef public double[:] _t_ncarray
    cdef public bint _t_inputflag
    cdef double *_t_inputpointer
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
    cdef public double fxg
    cdef public numpy.int64_t _fxg_ndim
    cdef public numpy.int64_t _fxg_length
    cdef public double[:] _fxg_points
    cdef public double[:] _fxg_results
    cdef public bint _fxg_ramflag
    cdef public double[:] _fxg_array
    cdef public bint _fxg_diskflag_reading
    cdef public bint _fxg_diskflag_writing
    cdef public double[:] _fxg_ncarray
    cdef public bint _fxg_inputflag
    cdef double *_fxg_inputpointer
    cdef public double fxs
    cdef public numpy.int64_t _fxs_ndim
    cdef public numpy.int64_t _fxs_length
    cdef public bint _fxs_ramflag
    cdef public double[:] _fxs_array
    cdef public bint _fxs_diskflag_reading
    cdef public bint _fxs_diskflag_writing
    cdef public double[:] _fxs_ncarray
    cdef public bint _fxs_inputflag
    cdef double *_fxs_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double dhs
    cdef public numpy.int64_t _dhs_ndim
    cdef public numpy.int64_t _dhs_length
    cdef public bint _dhs_ramflag
    cdef public double[:] _dhs_array
    cdef public bint _dhs_diskflag_reading
    cdef public bint _dhs_diskflag_writing
    cdef public double[:] _dhs_ncarray
    cdef public bint _dhs_outputflag
    cdef double *_dhs_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double pc
    cdef public numpy.int64_t _pc_ndim
    cdef public numpy.int64_t _pc_length
    cdef public double[:] _pc_points
    cdef public double[:] _pc_results
    cdef public double[:] _pc_integrals
    cdef public double _pc_sum
    cdef public bint _pc_ramflag
    cdef public double[:] _pc_array
    cdef public bint _pc_diskflag_reading
    cdef public bint _pc_diskflag_writing
    cdef public double[:] _pc_ncarray
    cdef public bint _pc_outputflag
    cdef double *_pc_outputpointer
    cdef public double[:] pe
    cdef public numpy.int64_t _pe_ndim
    cdef public numpy.int64_t _pe_length
    cdef public numpy.int64_t _pe_length_0
    cdef public bint _pe_ramflag
    cdef public double[:,:] _pe_array
    cdef public bint _pe_diskflag_reading
    cdef public bint _pe_diskflag_writing
    cdef public double[:] _pe_ncarray
    cdef public double[:] pet
    cdef public numpy.int64_t _pet_ndim
    cdef public numpy.int64_t _pet_length
    cdef public numpy.int64_t _pet_length_0
    cdef public bint _pet_ramflag
    cdef public double[:,:] _pet_array
    cdef public bint _pet_diskflag_reading
    cdef public bint _pet_diskflag_writing
    cdef public double[:] _pet_ncarray
    cdef public double[:] tf
    cdef public numpy.int64_t _tf_ndim
    cdef public numpy.int64_t _tf_length
    cdef public numpy.int64_t _tf_length_0
    cdef public double[:,:] _tf_points
    cdef public double[:,:] _tf_results
    cdef public double[:,:] _tf_integrals
    cdef public double[:] _tf_sum
    cdef public bint _tf_ramflag
    cdef public double[:,:] _tf_array
    cdef public bint _tf_diskflag_reading
    cdef public bint _tf_diskflag_writing
    cdef public double[:] _tf_ncarray
    cdef public double[:] ei
    cdef public numpy.int64_t _ei_ndim
    cdef public numpy.int64_t _ei_length
    cdef public numpy.int64_t _ei_length_0
    cdef public double[:,:] _ei_points
    cdef public double[:,:] _ei_results
    cdef public double[:,:] _ei_integrals
    cdef public double[:] _ei_sum
    cdef public bint _ei_ramflag
    cdef public double[:,:] _ei_array
    cdef public bint _ei_diskflag_reading
    cdef public bint _ei_diskflag_writing
    cdef public double[:] _ei_ncarray
    cdef public double[:] rf
    cdef public numpy.int64_t _rf_ndim
    cdef public numpy.int64_t _rf_length
    cdef public numpy.int64_t _rf_length_0
    cdef public double[:,:] _rf_points
    cdef public double[:,:] _rf_results
    cdef public double[:,:] _rf_integrals
    cdef public double[:] _rf_sum
    cdef public bint _rf_ramflag
    cdef public double[:,:] _rf_array
    cdef public bint _rf_diskflag_reading
    cdef public bint _rf_diskflag_writing
    cdef public double[:] _rf_ncarray
    cdef public double[:] sf
    cdef public numpy.int64_t _sf_ndim
    cdef public numpy.int64_t _sf_length
    cdef public numpy.int64_t _sf_length_0
    cdef public double[:,:] _sf_points
    cdef public double[:,:] _sf_results
    cdef public double[:,:] _sf_integrals
    cdef public double[:] _sf_sum
    cdef public bint _sf_ramflag
    cdef public double[:,:] _sf_array
    cdef public bint _sf_diskflag_reading
    cdef public bint _sf_diskflag_writing
    cdef public double[:] _sf_ncarray
    cdef public double[:] pm
    cdef public numpy.int64_t _pm_ndim
    cdef public numpy.int64_t _pm_length
    cdef public numpy.int64_t _pm_length_0
    cdef public bint _pm_ramflag
    cdef public double[:,:] _pm_array
    cdef public bint _pm_diskflag_reading
    cdef public bint _pm_diskflag_writing
    cdef public double[:] _pm_ncarray
    cdef public double[:] am
    cdef public numpy.int64_t _am_ndim
    cdef public numpy.int64_t _am_length
    cdef public numpy.int64_t _am_length_0
    cdef public double[:,:] _am_points
    cdef public double[:,:] _am_results
    cdef public double[:,:] _am_integrals
    cdef public double[:] _am_sum
    cdef public bint _am_ramflag
    cdef public double[:,:] _am_array
    cdef public bint _am_diskflag_reading
    cdef public bint _am_diskflag_writing
    cdef public double[:] _am_ncarray
    cdef public double ps
    cdef public numpy.int64_t _ps_ndim
    cdef public numpy.int64_t _ps_length
    cdef public double[:] _ps_points
    cdef public double[:] _ps_results
    cdef public double[:] _ps_integrals
    cdef public double _ps_sum
    cdef public bint _ps_ramflag
    cdef public double[:] _ps_array
    cdef public bint _ps_diskflag_reading
    cdef public bint _ps_diskflag_writing
    cdef public double[:] _ps_ncarray
    cdef public bint _ps_outputflag
    cdef double *_ps_outputpointer
    cdef public double pve
    cdef public numpy.int64_t _pve_ndim
    cdef public numpy.int64_t _pve_length
    cdef public double[:] _pve_points
    cdef public double[:] _pve_results
    cdef public double[:] _pve_integrals
    cdef public double _pve_sum
    cdef public bint _pve_ramflag
    cdef public double[:] _pve_array
    cdef public bint _pve_diskflag_reading
    cdef public bint _pve_diskflag_writing
    cdef public double[:] _pve_ncarray
    cdef public bint _pve_outputflag
    cdef double *_pve_outputpointer
    cdef public double pv
    cdef public numpy.int64_t _pv_ndim
    cdef public numpy.int64_t _pv_length
    cdef public double[:] _pv_points
    cdef public double[:] _pv_results
    cdef public double[:] _pv_integrals
    cdef public double _pv_sum
    cdef public bint _pv_ramflag
    cdef public double[:] _pv_array
    cdef public bint _pv_diskflag_reading
    cdef public bint _pv_diskflag_writing
    cdef public double[:] _pv_ncarray
    cdef public bint _pv_outputflag
    cdef double *_pv_outputpointer
    cdef public double pq
    cdef public numpy.int64_t _pq_ndim
    cdef public numpy.int64_t _pq_length
    cdef public double[:] _pq_points
    cdef public double[:] _pq_results
    cdef public double[:] _pq_integrals
    cdef public double _pq_sum
    cdef public bint _pq_ramflag
    cdef public double[:] _pq_array
    cdef public bint _pq_diskflag_reading
    cdef public bint _pq_diskflag_writing
    cdef public double[:] _pq_ncarray
    cdef public bint _pq_outputflag
    cdef double *_pq_outputpointer
    cdef public double etve
    cdef public numpy.int64_t _etve_ndim
    cdef public numpy.int64_t _etve_length
    cdef public double[:] _etve_points
    cdef public double[:] _etve_results
    cdef public double[:] _etve_integrals
    cdef public double _etve_sum
    cdef public bint _etve_ramflag
    cdef public double[:] _etve_array
    cdef public bint _etve_diskflag_reading
    cdef public bint _etve_diskflag_writing
    cdef public double[:] _etve_ncarray
    cdef public bint _etve_outputflag
    cdef double *_etve_outputpointer
    cdef public double etv
    cdef public numpy.int64_t _etv_ndim
    cdef public numpy.int64_t _etv_length
    cdef public double[:] _etv_points
    cdef public double[:] _etv_results
    cdef public double[:] _etv_integrals
    cdef public double _etv_sum
    cdef public bint _etv_ramflag
    cdef public double[:] _etv_array
    cdef public bint _etv_diskflag_reading
    cdef public bint _etv_diskflag_writing
    cdef public double[:] _etv_ncarray
    cdef public bint _etv_outputflag
    cdef double *_etv_outputpointer
    cdef public double es
    cdef public numpy.int64_t _es_ndim
    cdef public numpy.int64_t _es_length
    cdef public double[:] _es_points
    cdef public double[:] _es_results
    cdef public double[:] _es_integrals
    cdef public double _es_sum
    cdef public bint _es_ramflag
    cdef public double[:] _es_array
    cdef public bint _es_diskflag_reading
    cdef public bint _es_diskflag_writing
    cdef public double[:] _es_ncarray
    cdef public bint _es_outputflag
    cdef double *_es_outputpointer
    cdef public double et
    cdef public numpy.int64_t _et_ndim
    cdef public numpy.int64_t _et_length
    cdef public bint _et_ramflag
    cdef public double[:] _et_array
    cdef public bint _et_diskflag_reading
    cdef public bint _et_diskflag_writing
    cdef public double[:] _et_ncarray
    cdef public bint _et_outputflag
    cdef double *_et_outputpointer
    cdef public double gr
    cdef public numpy.int64_t _gr_ndim
    cdef public numpy.int64_t _gr_length
    cdef public double[:] _gr_points
    cdef public double[:] _gr_results
    cdef public double[:] _gr_integrals
    cdef public double _gr_sum
    cdef public bint _gr_ramflag
    cdef public double[:] _gr_array
    cdef public bint _gr_diskflag_reading
    cdef public bint _gr_diskflag_writing
    cdef public double[:] _gr_ncarray
    cdef public bint _gr_outputflag
    cdef double *_gr_outputpointer
    cdef public double fxs
    cdef public numpy.int64_t _fxs_ndim
    cdef public numpy.int64_t _fxs_length
    cdef public double[:] _fxs_points
    cdef public double[:] _fxs_results
    cdef public double[:] _fxs_integrals
    cdef public double _fxs_sum
    cdef public bint _fxs_ramflag
    cdef public double[:] _fxs_array
    cdef public bint _fxs_diskflag_reading
    cdef public bint _fxs_diskflag_writing
    cdef public double[:] _fxs_ncarray
    cdef public bint _fxs_outputflag
    cdef double *_fxs_outputpointer
    cdef public double fxg
    cdef public numpy.int64_t _fxg_ndim
    cdef public numpy.int64_t _fxg_length
    cdef public double[:] _fxg_points
    cdef public double[:] _fxg_results
    cdef public double[:] _fxg_integrals
    cdef public double _fxg_sum
    cdef public bint _fxg_ramflag
    cdef public double[:] _fxg_array
    cdef public bint _fxg_diskflag_reading
    cdef public bint _fxg_diskflag_writing
    cdef public double[:] _fxg_ncarray
    cdef public bint _fxg_outputflag
    cdef double *_fxg_outputpointer
    cdef public double cdg
    cdef public numpy.int64_t _cdg_ndim
    cdef public numpy.int64_t _cdg_length
    cdef public double[:] _cdg_points
    cdef public double[:] _cdg_results
    cdef public double[:] _cdg_integrals
    cdef public double _cdg_sum
    cdef public bint _cdg_ramflag
    cdef public double[:] _cdg_array
    cdef public bint _cdg_diskflag_reading
    cdef public bint _cdg_diskflag_writing
    cdef public double[:] _cdg_ncarray
    cdef public bint _cdg_outputflag
    cdef double *_cdg_outputpointer
    cdef public double fgse
    cdef public numpy.int64_t _fgse_ndim
    cdef public numpy.int64_t _fgse_length
    cdef public double[:] _fgse_points
    cdef public double[:] _fgse_results
    cdef public double[:] _fgse_integrals
    cdef public double _fgse_sum
    cdef public bint _fgse_ramflag
    cdef public double[:] _fgse_array
    cdef public bint _fgse_diskflag_reading
    cdef public bint _fgse_diskflag_writing
    cdef public double[:] _fgse_ncarray
    cdef public bint _fgse_outputflag
    cdef double *_fgse_outputpointer
    cdef public double fgs
    cdef public numpy.int64_t _fgs_ndim
    cdef public numpy.int64_t _fgs_length
    cdef public double[:] _fgs_points
    cdef public double[:] _fgs_results
    cdef public double[:] _fgs_integrals
    cdef public double _fgs_sum
    cdef public bint _fgs_ramflag
    cdef public double[:] _fgs_array
    cdef public bint _fgs_diskflag_reading
    cdef public bint _fgs_diskflag_writing
    cdef public double[:] _fgs_ncarray
    cdef public bint _fgs_outputflag
    cdef double *_fgs_outputpointer
    cdef public double fqs
    cdef public numpy.int64_t _fqs_ndim
    cdef public numpy.int64_t _fqs_length
    cdef public double[:] _fqs_points
    cdef public double[:] _fqs_results
    cdef public double[:] _fqs_integrals
    cdef public double _fqs_sum
    cdef public bint _fqs_ramflag
    cdef public double[:] _fqs_array
    cdef public bint _fqs_diskflag_reading
    cdef public bint _fqs_diskflag_writing
    cdef public double[:] _fqs_ncarray
    cdef public bint _fqs_outputflag
    cdef double *_fqs_outputpointer
    cdef public double rh
    cdef public numpy.int64_t _rh_ndim
    cdef public numpy.int64_t _rh_length
    cdef public double[:] _rh_points
    cdef public double[:] _rh_results
    cdef public double[:] _rh_integrals
    cdef public double _rh_sum
    cdef public bint _rh_ramflag
    cdef public double[:] _rh_array
    cdef public bint _rh_diskflag_reading
    cdef public bint _rh_diskflag_writing
    cdef public double[:] _rh_ncarray
    cdef public bint _rh_outputflag
    cdef double *_rh_outputpointer
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double[:] ic
    cdef public numpy.int64_t _ic_ndim
    cdef public numpy.int64_t _ic_length
    cdef public numpy.int64_t _ic_length_0
    cdef public double[:,:] _ic_points
    cdef public double[:,:] _ic_results
    cdef public bint _ic_ramflag
    cdef public double[:,:] _ic_array
    cdef public bint _ic_diskflag_reading
    cdef public bint _ic_diskflag_writing
    cdef public double[:] _ic_ncarray
    cdef public double[:] sp
    cdef public numpy.int64_t _sp_ndim
    cdef public numpy.int64_t _sp_length
    cdef public numpy.int64_t _sp_length_0
    cdef public double[:,:] _sp_points
    cdef public double[:,:] _sp_results
    cdef public bint _sp_ramflag
    cdef public double[:,:] _sp_array
    cdef public bint _sp_diskflag_reading
    cdef public bint _sp_diskflag_writing
    cdef public double[:] _sp_ncarray
    cdef public double dve
    cdef public numpy.int64_t _dve_ndim
    cdef public numpy.int64_t _dve_length
    cdef public double[:] _dve_points
    cdef public double[:] _dve_results
    cdef public bint _dve_ramflag
    cdef public double[:] _dve_array
    cdef public bint _dve_diskflag_reading
    cdef public bint _dve_diskflag_writing
    cdef public double[:] _dve_ncarray
    cdef public bint _dve_outputflag
    cdef double *_dve_outputpointer
    cdef public double dv
    cdef public numpy.int64_t _dv_ndim
    cdef public numpy.int64_t _dv_length
    cdef public double[:] _dv_points
    cdef public double[:] _dv_results
    cdef public bint _dv_ramflag
    cdef public double[:] _dv_array
    cdef public bint _dv_diskflag_reading
    cdef public bint _dv_diskflag_writing
    cdef public double[:] _dv_ncarray
    cdef public bint _dv_outputflag
    cdef double *_dv_outputpointer
    cdef public double hge
    cdef public numpy.int64_t _hge_ndim
    cdef public numpy.int64_t _hge_length
    cdef public double[:] _hge_points
    cdef public double[:] _hge_results
    cdef public bint _hge_ramflag
    cdef public double[:] _hge_array
    cdef public bint _hge_diskflag_reading
    cdef public bint _hge_diskflag_writing
    cdef public double[:] _hge_ncarray
    cdef public bint _hge_outputflag
    cdef double *_hge_outputpointer
    cdef public double dg
    cdef public numpy.int64_t _dg_ndim
    cdef public numpy.int64_t _dg_length
    cdef public double[:] _dg_points
    cdef public double[:] _dg_results
    cdef public bint _dg_ramflag
    cdef public double[:] _dg_array
    cdef public bint _dg_diskflag_reading
    cdef public bint _dg_diskflag_writing
    cdef public double[:] _dg_ncarray
    cdef public bint _dg_outputflag
    cdef double *_dg_outputpointer
    cdef public double hq
    cdef public numpy.int64_t _hq_ndim
    cdef public numpy.int64_t _hq_length
    cdef public double[:] _hq_points
    cdef public double[:] _hq_results
    cdef public bint _hq_ramflag
    cdef public double[:] _hq_array
    cdef public bint _hq_diskflag_reading
    cdef public bint _hq_diskflag_writing
    cdef public double[:] _hq_ncarray
    cdef public bint _hq_outputflag
    cdef double *_hq_outputpointer
    cdef public double hs
    cdef public numpy.int64_t _hs_ndim
    cdef public numpy.int64_t _hs_length
    cdef public double[:] _hs_points
    cdef public double[:] _hs_results
    cdef public bint _hs_ramflag
    cdef public double[:] _hs_array
    cdef public bint _hs_diskflag_reading
    cdef public bint _hs_diskflag_writing
    cdef public double[:] _hs_ncarray
    cdef public bint _hs_outputflag
    cdef double *_hs_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class AideSequences:
    cdef public double fr
    cdef public numpy.int64_t _fr_ndim
    cdef public numpy.int64_t _fr_length
    cdef public double we
    cdef public numpy.int64_t _we_ndim
    cdef public numpy.int64_t _we_length
    cdef public double w
    cdef public numpy.int64_t _w_ndim
    cdef public numpy.int64_t _w_length
    cdef public double betae
    cdef public numpy.int64_t _betae_ndim
    cdef public numpy.int64_t _betae_length
    cdef public double beta
    cdef public numpy.int64_t _beta_ndim
    cdef public numpy.int64_t _beta_length
    cdef public double dveq
    cdef public numpy.int64_t _dveq_ndim
    cdef public numpy.int64_t _dveq_length
    cdef public double dgeq
    cdef public numpy.int64_t _dgeq_ndim
    cdef public numpy.int64_t _dgeq_length
    cdef public double gf
    cdef public numpy.int64_t _gf_ndim
    cdef public numpy.int64_t _gf_length
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
cdef class PegasusDGEq(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface dischargemodel
    cdef public numpy.npy_bool dischargemodel_is_mainmodel
    cdef public numpy.int64_t dischargemodel_typeid
    cdef public masterinterface.MasterInterface petmodel
    cdef public numpy.npy_bool petmodel_is_mainmodel
    cdef public numpy.int64_t petmodel_typeid
    cdef public masterinterface.MasterInterface waterlevelmodel
    cdef public numpy.npy_bool waterlevelmodel_is_mainmodel
    cdef public numpy.int64_t waterlevelmodel_typeid
    cdef public PegasusDGEq pegasusdgeq
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
    cpdef inline void pick_hs_v1(self) noexcept nogil
    cpdef inline void calc_pe_pet_v1(self) noexcept nogil
    cpdef inline void calc_fr_v1(self) noexcept nogil
    cpdef inline void calc_pm_v1(self) noexcept nogil
    cpdef inline void calc_fxs_v1(self) noexcept nogil
    cpdef inline void calc_fxg_v1(self) noexcept nogil
    cpdef inline void calc_pc_v1(self) noexcept nogil
    cpdef inline void calc_tf_v1(self) noexcept nogil
    cpdef inline void calc_ei_v1(self) noexcept nogil
    cpdef inline void calc_rf_v1(self) noexcept nogil
    cpdef inline void calc_sf_v1(self) noexcept nogil
    cpdef inline void calc_am_v1(self) noexcept nogil
    cpdef inline void calc_ps_v1(self) noexcept nogil
    cpdef inline void calc_we_w_v1(self) noexcept nogil
    cpdef inline void calc_pve_pv_v1(self) noexcept nogil
    cpdef inline void calc_pq_v1(self) noexcept nogil
    cpdef inline void calc_betae_beta_v1(self) noexcept nogil
    cpdef inline void calc_etve_etv_v1(self) noexcept nogil
    cpdef inline void calc_es_v1(self) noexcept nogil
    cpdef inline void calc_gr_v1(self) noexcept nogil
    cpdef inline void calc_fqs_v1(self) noexcept nogil
    cpdef inline void calc_fgse_v1(self) noexcept nogil
    cpdef inline void calc_fgs_v1(self) noexcept nogil
    cpdef inline void calc_rh_v1(self) noexcept nogil
    cpdef inline void calc_dveq_v3(self) noexcept nogil
    cpdef inline void calc_dgeq_v1(self) noexcept nogil
    cpdef inline void calc_gf_v1(self) noexcept nogil
    cpdef inline void calc_cdg_v2(self) noexcept nogil
    cpdef inline void update_ic_v1(self) noexcept nogil
    cpdef inline void update_sp_v1(self) noexcept nogil
    cpdef inline void update_dve_v1(self) noexcept nogil
    cpdef inline void update_dv_v1(self) noexcept nogil
    cpdef inline void update_hge_v1(self) noexcept nogil
    cpdef inline void update_dg_v1(self) noexcept nogil
    cpdef inline void update_hq_v1(self) noexcept nogil
    cpdef inline void update_hs_v1(self) noexcept nogil
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature_v1(self) noexcept nogil
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_pe_pet_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_pe_pet_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline double return_dvh_v2(self, double h) noexcept nogil
    cpdef inline double return_errordv_v1(self, double dg) noexcept nogil
    cpdef inline void calc_et_v1(self) noexcept nogil
    cpdef inline void calc_r_v1(self) noexcept nogil
    cpdef inline void pass_r_v1(self) noexcept nogil
    cpdef inline void pick_hs(self) noexcept nogil
    cpdef inline void calc_pe_pet(self) noexcept nogil
    cpdef inline void calc_fr(self) noexcept nogil
    cpdef inline void calc_pm(self) noexcept nogil
    cpdef inline void calc_fxs(self) noexcept nogil
    cpdef inline void calc_fxg(self) noexcept nogil
    cpdef inline void calc_pc(self) noexcept nogil
    cpdef inline void calc_tf(self) noexcept nogil
    cpdef inline void calc_ei(self) noexcept nogil
    cpdef inline void calc_rf(self) noexcept nogil
    cpdef inline void calc_sf(self) noexcept nogil
    cpdef inline void calc_am(self) noexcept nogil
    cpdef inline void calc_ps(self) noexcept nogil
    cpdef inline void calc_we_w(self) noexcept nogil
    cpdef inline void calc_pve_pv(self) noexcept nogil
    cpdef inline void calc_pq(self) noexcept nogil
    cpdef inline void calc_betae_beta(self) noexcept nogil
    cpdef inline void calc_etve_etv(self) noexcept nogil
    cpdef inline void calc_es(self) noexcept nogil
    cpdef inline void calc_gr(self) noexcept nogil
    cpdef inline void calc_fqs(self) noexcept nogil
    cpdef inline void calc_fgse(self) noexcept nogil
    cpdef inline void calc_fgs(self) noexcept nogil
    cpdef inline void calc_rh(self) noexcept nogil
    cpdef inline void calc_dveq(self) noexcept nogil
    cpdef inline void calc_dgeq(self) noexcept nogil
    cpdef inline void calc_gf(self) noexcept nogil
    cpdef inline void calc_cdg(self) noexcept nogil
    cpdef inline void update_ic(self) noexcept nogil
    cpdef inline void update_sp(self) noexcept nogil
    cpdef inline void update_dve(self) noexcept nogil
    cpdef inline void update_dv(self) noexcept nogil
    cpdef inline void update_hge(self) noexcept nogil
    cpdef inline void update_dg(self) noexcept nogil
    cpdef inline void update_hq(self) noexcept nogil
    cpdef inline void update_hs(self) noexcept nogil
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature(self) noexcept nogil
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil
    cpdef inline double return_dvh(self, double h) noexcept nogil
    cpdef inline double return_errordv(self, double dg) noexcept nogil
    cpdef inline void calc_et(self) noexcept nogil
    cpdef inline void calc_r(self) noexcept nogil
    cpdef inline void pass_r(self) noexcept nogil
