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
cdef public numpy.int64_t FIELD = 1
cdef public numpy.int64_t FOREST = 2
cdef public numpy.int64_t GLACIER = 3
cdef public numpy.int64_t ILAKE = 4
cdef public numpy.int64_t SEALED = 5
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
@cython.final
cdef class ControlParameters:
    cdef public double area
    cdef public numpy.int64_t nmbzones
    cdef public numpy.int64_t sclass
    cdef public numpy.int64_t[:] zonetype
    cdef public double[:] zonearea
    cdef public double psi
    cdef public double[:] zonez
    cdef public double[:] pcorr
    cdef public double[:] pcalt
    cdef public double[:] rfcf
    cdef public double[:] sfcf
    cdef public double[:] tcorr
    cdef public double[:] tcalt
    cdef public double[:] icmax
    cdef public double[:] sfdist
    cdef public double[:] smax
    cdef public double[:,:] sred
    cdef public double[:] tt
    cdef public double[:] ttint
    cdef public double[:] dttm
    cdef public double[:] cfmax
    cdef public double[:] cfvar
    cdef public double[:] gmelt
    cdef public double[:] gvar
    cdef public double[:] cfr
    cdef public double[:] whc
    cdef public double[:] fc
    cdef public double[:] beta
    cdef public double[:] h1
    cdef public double[:] tab1
    cdef public double[:] tvs1
    cdef public double[:] h2
    cdef public double[:] tab2
    cdef public double[:] tvs2
    cdef public double k4
    cdef public double gamma
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] doy
    cdef public double[:] relzoneareas
    cdef public double rellandarea
    cdef public double rellowerzonearea
    cdef public double[:,:] zonearearatios
    cdef public numpy.int64_t[:] indiceszonez
    cdef public double z
    cdef public numpy.int64_t[:,:] sredorder
    cdef public numpy.int64_t[:] sredend
    cdef public numpy.int64_t srednumber
    cdef public double[:] ttm
    cdef public double qfactor
@cython.final
cdef class FixedParameters:
    cdef public double pi
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double[:] tc
    cdef public numpy.int64_t _tc_ndim
    cdef public numpy.int64_t _tc_length
    cdef public numpy.int64_t _tc_length_0
    cdef public bint _tc_ramflag
    cdef public double[:,:] _tc_array
    cdef public bint _tc_diskflag_reading
    cdef public bint _tc_diskflag_writing
    cdef public double[:] _tc_ncarray
    cdef public double[:] fracrain
    cdef public numpy.int64_t _fracrain_ndim
    cdef public numpy.int64_t _fracrain_length
    cdef public numpy.int64_t _fracrain_length_0
    cdef public bint _fracrain_ramflag
    cdef public double[:,:] _fracrain_array
    cdef public bint _fracrain_diskflag_reading
    cdef public bint _fracrain_diskflag_writing
    cdef public double[:] _fracrain_ncarray
    cdef public double[:] rfc
    cdef public numpy.int64_t _rfc_ndim
    cdef public numpy.int64_t _rfc_length
    cdef public numpy.int64_t _rfc_length_0
    cdef public bint _rfc_ramflag
    cdef public double[:,:] _rfc_array
    cdef public bint _rfc_diskflag_reading
    cdef public bint _rfc_diskflag_writing
    cdef public double[:] _rfc_ncarray
    cdef public double[:] sfc
    cdef public numpy.int64_t _sfc_ndim
    cdef public numpy.int64_t _sfc_length
    cdef public numpy.int64_t _sfc_length_0
    cdef public bint _sfc_ramflag
    cdef public double[:,:] _sfc_array
    cdef public bint _sfc_diskflag_reading
    cdef public bint _sfc_diskflag_writing
    cdef public double[:] _sfc_ncarray
    cdef public double[:] cfact
    cdef public numpy.int64_t _cfact_ndim
    cdef public numpy.int64_t _cfact_length
    cdef public numpy.int64_t _cfact_length_0
    cdef public bint _cfact_ramflag
    cdef public double[:,:] _cfact_array
    cdef public bint _cfact_diskflag_reading
    cdef public bint _cfact_diskflag_writing
    cdef public double[:] _cfact_ncarray
    cdef public double[:,:] swe
    cdef public numpy.int64_t _swe_ndim
    cdef public numpy.int64_t _swe_length
    cdef public numpy.int64_t _swe_length_0
    cdef public numpy.int64_t _swe_length_1
    cdef public bint _swe_ramflag
    cdef public double[:,:,:] _swe_array
    cdef public bint _swe_diskflag_reading
    cdef public bint _swe_diskflag_writing
    cdef public double[:] _swe_ncarray
    cdef public double[:] gact
    cdef public numpy.int64_t _gact_ndim
    cdef public numpy.int64_t _gact_length
    cdef public numpy.int64_t _gact_length_0
    cdef public bint _gact_ramflag
    cdef public double[:,:] _gact_array
    cdef public bint _gact_diskflag_reading
    cdef public bint _gact_diskflag_writing
    cdef public double[:] _gact_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double[:] pc
    cdef public numpy.int64_t _pc_ndim
    cdef public numpy.int64_t _pc_length
    cdef public numpy.int64_t _pc_length_0
    cdef public bint _pc_ramflag
    cdef public double[:,:] _pc_array
    cdef public bint _pc_diskflag_reading
    cdef public bint _pc_diskflag_writing
    cdef public double[:] _pc_ncarray
    cdef public double[:] ei
    cdef public numpy.int64_t _ei_ndim
    cdef public numpy.int64_t _ei_length
    cdef public numpy.int64_t _ei_length_0
    cdef public bint _ei_ramflag
    cdef public double[:,:] _ei_array
    cdef public bint _ei_diskflag_reading
    cdef public bint _ei_diskflag_writing
    cdef public double[:] _ei_ncarray
    cdef public double[:] tf
    cdef public numpy.int64_t _tf_ndim
    cdef public numpy.int64_t _tf_length
    cdef public numpy.int64_t _tf_length_0
    cdef public bint _tf_ramflag
    cdef public double[:,:] _tf_array
    cdef public bint _tf_diskflag_reading
    cdef public bint _tf_diskflag_writing
    cdef public double[:] _tf_ncarray
    cdef public double[:] spl
    cdef public numpy.int64_t _spl_ndim
    cdef public numpy.int64_t _spl_length
    cdef public numpy.int64_t _spl_length_0
    cdef public bint _spl_ramflag
    cdef public double[:,:] _spl_array
    cdef public bint _spl_diskflag_reading
    cdef public bint _spl_diskflag_writing
    cdef public double[:] _spl_ncarray
    cdef public double[:] wcl
    cdef public numpy.int64_t _wcl_ndim
    cdef public numpy.int64_t _wcl_length
    cdef public numpy.int64_t _wcl_length_0
    cdef public bint _wcl_ramflag
    cdef public double[:,:] _wcl_array
    cdef public bint _wcl_diskflag_reading
    cdef public bint _wcl_diskflag_writing
    cdef public double[:] _wcl_ncarray
    cdef public double[:] spg
    cdef public numpy.int64_t _spg_ndim
    cdef public numpy.int64_t _spg_length
    cdef public numpy.int64_t _spg_length_0
    cdef public bint _spg_ramflag
    cdef public double[:,:] _spg_array
    cdef public bint _spg_diskflag_reading
    cdef public bint _spg_diskflag_writing
    cdef public double[:] _spg_ncarray
    cdef public double[:] wcg
    cdef public numpy.int64_t _wcg_ndim
    cdef public numpy.int64_t _wcg_length
    cdef public numpy.int64_t _wcg_length_0
    cdef public bint _wcg_ramflag
    cdef public double[:,:] _wcg_array
    cdef public bint _wcg_diskflag_reading
    cdef public bint _wcg_diskflag_writing
    cdef public double[:] _wcg_ncarray
    cdef public double[:] glmelt
    cdef public numpy.int64_t _glmelt_ndim
    cdef public numpy.int64_t _glmelt_length
    cdef public numpy.int64_t _glmelt_length_0
    cdef public bint _glmelt_ramflag
    cdef public double[:,:] _glmelt_array
    cdef public bint _glmelt_diskflag_reading
    cdef public bint _glmelt_diskflag_writing
    cdef public double[:] _glmelt_ncarray
    cdef public double[:,:] melt
    cdef public numpy.int64_t _melt_ndim
    cdef public numpy.int64_t _melt_length
    cdef public numpy.int64_t _melt_length_0
    cdef public numpy.int64_t _melt_length_1
    cdef public bint _melt_ramflag
    cdef public double[:,:,:] _melt_array
    cdef public bint _melt_diskflag_reading
    cdef public bint _melt_diskflag_writing
    cdef public double[:] _melt_ncarray
    cdef public double[:,:] refr
    cdef public numpy.int64_t _refr_ndim
    cdef public numpy.int64_t _refr_length
    cdef public numpy.int64_t _refr_length_0
    cdef public numpy.int64_t _refr_length_1
    cdef public bint _refr_ramflag
    cdef public double[:,:,:] _refr_array
    cdef public bint _refr_diskflag_reading
    cdef public bint _refr_diskflag_writing
    cdef public double[:] _refr_ncarray
    cdef public double[:] in_
    cdef public numpy.int64_t _in__ndim
    cdef public numpy.int64_t _in__length
    cdef public numpy.int64_t _in__length_0
    cdef public bint _in__ramflag
    cdef public double[:,:] _in__array
    cdef public bint _in__diskflag_reading
    cdef public bint _in__diskflag_writing
    cdef public double[:] _in__ncarray
    cdef public double[:] r
    cdef public numpy.int64_t _r_ndim
    cdef public numpy.int64_t _r_length
    cdef public numpy.int64_t _r_length_0
    cdef public bint _r_ramflag
    cdef public double[:,:] _r_array
    cdef public bint _r_diskflag_reading
    cdef public bint _r_diskflag_writing
    cdef public double[:] _r_ncarray
    cdef public double[:] sr
    cdef public numpy.int64_t _sr_ndim
    cdef public numpy.int64_t _sr_length
    cdef public numpy.int64_t _sr_length_0
    cdef public bint _sr_ramflag
    cdef public double[:,:] _sr_array
    cdef public bint _sr_diskflag_reading
    cdef public bint _sr_diskflag_writing
    cdef public double[:] _sr_ncarray
    cdef public double[:] ea
    cdef public numpy.int64_t _ea_ndim
    cdef public numpy.int64_t _ea_length
    cdef public numpy.int64_t _ea_length_0
    cdef public bint _ea_ramflag
    cdef public double[:,:] _ea_array
    cdef public bint _ea_diskflag_reading
    cdef public bint _ea_diskflag_writing
    cdef public double[:] _ea_ncarray
    cdef public double[:] qvs1
    cdef public numpy.int64_t _qvs1_ndim
    cdef public numpy.int64_t _qvs1_length
    cdef public numpy.int64_t _qvs1_length_0
    cdef public bint _qvs1_ramflag
    cdef public double[:,:] _qvs1_array
    cdef public bint _qvs1_diskflag_reading
    cdef public bint _qvs1_diskflag_writing
    cdef public double[:] _qvs1_ncarray
    cdef public double[:] qab1
    cdef public numpy.int64_t _qab1_ndim
    cdef public numpy.int64_t _qab1_length
    cdef public numpy.int64_t _qab1_length_0
    cdef public bint _qab1_ramflag
    cdef public double[:,:] _qab1_array
    cdef public bint _qab1_diskflag_reading
    cdef public bint _qab1_diskflag_writing
    cdef public double[:] _qab1_ncarray
    cdef public double[:] qvs2
    cdef public numpy.int64_t _qvs2_ndim
    cdef public numpy.int64_t _qvs2_length
    cdef public numpy.int64_t _qvs2_length_0
    cdef public bint _qvs2_ramflag
    cdef public double[:,:] _qvs2_array
    cdef public bint _qvs2_diskflag_reading
    cdef public bint _qvs2_diskflag_writing
    cdef public double[:] _qvs2_ncarray
    cdef public double[:] qab2
    cdef public numpy.int64_t _qab2_ndim
    cdef public numpy.int64_t _qab2_length
    cdef public numpy.int64_t _qab2_length_0
    cdef public bint _qab2_ramflag
    cdef public double[:,:] _qab2_array
    cdef public bint _qab2_diskflag_reading
    cdef public bint _qab2_diskflag_writing
    cdef public double[:] _qab2_ncarray
    cdef public double[:] el
    cdef public numpy.int64_t _el_ndim
    cdef public numpy.int64_t _el_length
    cdef public numpy.int64_t _el_length_0
    cdef public bint _el_ramflag
    cdef public double[:,:] _el_array
    cdef public bint _el_diskflag_reading
    cdef public bint _el_diskflag_writing
    cdef public double[:] _el_ncarray
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
    cdef public double inrc
    cdef public numpy.int64_t _inrc_ndim
    cdef public numpy.int64_t _inrc_length
    cdef public bint _inrc_ramflag
    cdef public double[:] _inrc_array
    cdef public bint _inrc_diskflag_reading
    cdef public bint _inrc_diskflag_writing
    cdef public double[:] _inrc_ncarray
    cdef public bint _inrc_outputflag
    cdef double *_inrc_outputpointer
    cdef public double outrc
    cdef public numpy.int64_t _outrc_ndim
    cdef public numpy.int64_t _outrc_length
    cdef public bint _outrc_ramflag
    cdef public double[:] _outrc_array
    cdef public bint _outrc_diskflag_reading
    cdef public bint _outrc_diskflag_writing
    cdef public double[:] _outrc_ncarray
    cdef public bint _outrc_outputflag
    cdef double *_outrc_outputpointer
    cdef public double rt
    cdef public numpy.int64_t _rt_ndim
    cdef public numpy.int64_t _rt_length
    cdef public bint _rt_ramflag
    cdef public double[:] _rt_array
    cdef public bint _rt_diskflag_reading
    cdef public bint _rt_diskflag_writing
    cdef public double[:] _rt_ncarray
    cdef public bint _rt_outputflag
    cdef double *_rt_outputpointer
    cdef public double qt
    cdef public numpy.int64_t _qt_ndim
    cdef public numpy.int64_t _qt_length
    cdef public bint _qt_ramflag
    cdef public double[:] _qt_array
    cdef public bint _qt_diskflag_reading
    cdef public bint _qt_diskflag_writing
    cdef public double[:] _qt_ncarray
    cdef public bint _qt_outputflag
    cdef double *_qt_outputpointer
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
    cdef public bint _ic_ramflag
    cdef public double[:,:] _ic_array
    cdef public bint _ic_diskflag_reading
    cdef public bint _ic_diskflag_writing
    cdef public double[:] _ic_ncarray
    cdef public double[:,:] sp
    cdef public numpy.int64_t _sp_ndim
    cdef public numpy.int64_t _sp_length
    cdef public numpy.int64_t _sp_length_0
    cdef public numpy.int64_t _sp_length_1
    cdef public bint _sp_ramflag
    cdef public double[:,:,:] _sp_array
    cdef public bint _sp_diskflag_reading
    cdef public bint _sp_diskflag_writing
    cdef public double[:] _sp_ncarray
    cdef public double[:,:] wc
    cdef public numpy.int64_t _wc_ndim
    cdef public numpy.int64_t _wc_length
    cdef public numpy.int64_t _wc_length_0
    cdef public numpy.int64_t _wc_length_1
    cdef public bint _wc_ramflag
    cdef public double[:,:,:] _wc_array
    cdef public bint _wc_diskflag_reading
    cdef public bint _wc_diskflag_writing
    cdef public double[:] _wc_ncarray
    cdef public double[:] sm
    cdef public numpy.int64_t _sm_ndim
    cdef public numpy.int64_t _sm_length
    cdef public numpy.int64_t _sm_length_0
    cdef public bint _sm_ramflag
    cdef public double[:,:] _sm_array
    cdef public bint _sm_diskflag_reading
    cdef public bint _sm_diskflag_writing
    cdef public double[:] _sm_ncarray
    cdef public double[:] bw1
    cdef public numpy.int64_t _bw1_ndim
    cdef public numpy.int64_t _bw1_length
    cdef public numpy.int64_t _bw1_length_0
    cdef public bint _bw1_ramflag
    cdef public double[:,:] _bw1_array
    cdef public bint _bw1_diskflag_reading
    cdef public bint _bw1_diskflag_writing
    cdef public double[:] _bw1_ncarray
    cdef public double[:] bw2
    cdef public numpy.int64_t _bw2_ndim
    cdef public numpy.int64_t _bw2_length
    cdef public numpy.int64_t _bw2_length_0
    cdef public bint _bw2_ramflag
    cdef public double[:,:] _bw2_array
    cdef public bint _bw2_diskflag_reading
    cdef public bint _bw2_diskflag_writing
    cdef public double[:] _bw2_ncarray
    cdef public double lz
    cdef public numpy.int64_t _lz_ndim
    cdef public numpy.int64_t _lz_length
    cdef public bint _lz_ramflag
    cdef public double[:] _lz_array
    cdef public bint _lz_diskflag_reading
    cdef public bint _lz_diskflag_writing
    cdef public double[:] _lz_ncarray
    cdef public bint _lz_outputflag
    cdef double *_lz_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class AideSequences:
    cdef public double[:] spe
    cdef public numpy.int64_t _spe_ndim
    cdef public numpy.int64_t _spe_length
    cdef public numpy.int64_t _spe_length_0
    cdef public double[:] wce
    cdef public numpy.int64_t _wce_ndim
    cdef public numpy.int64_t _wce_length
    cdef public numpy.int64_t _wce_length_0
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
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface aetmodel
    cdef public numpy.npy_bool aetmodel_is_mainmodel
    cdef public numpy.int64_t aetmodel_typeid
    cdef public masterinterface.MasterInterface rconcmodel
    cdef public numpy.npy_bool rconcmodel_is_mainmodel
    cdef public numpy.int64_t rconcmodel_typeid
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
    cpdef inline void calc_tc_v1(self) noexcept nogil
    cpdef inline void calc_fracrain_v1(self) noexcept nogil
    cpdef inline void calc_rfc_sfc_v1(self) noexcept nogil
    cpdef inline void calc_pc_v1(self) noexcept nogil
    cpdef inline void calc_tf_ic_v1(self) noexcept nogil
    cpdef inline void calc_sp_wc_v1(self) noexcept nogil
    cpdef inline void calc_spl_wcl_sp_wc_v1(self) noexcept nogil
    cpdef inline void calc_spg_wcg_sp_wc_v1(self) noexcept nogil
    cpdef inline void calc_cfact_v1(self) noexcept nogil
    cpdef inline void calc_melt_sp_wc_v1(self) noexcept nogil
    cpdef inline void calc_refr_sp_wc_v1(self) noexcept nogil
    cpdef inline void calc_in_wc_v1(self) noexcept nogil
    cpdef inline void calc_swe_v1(self) noexcept nogil
    cpdef inline void calc_sr_v1(self) noexcept nogil
    cpdef inline void calc_gact_v1(self) noexcept nogil
    cpdef inline void calc_glmelt_in_v1(self) noexcept nogil
    cpdef inline void calc_ei_ic_v1(self) noexcept nogil
    cpdef inline void calc_r_sm_v1(self) noexcept nogil
    cpdef inline void calc_ea_sm_v1(self) noexcept nogil
    cpdef inline void calc_qab1_qvs1_bw1_v1(self) noexcept nogil
    cpdef inline void calc_qab2_qvs2_bw2_v1(self) noexcept nogil
    cpdef inline void calc_inrc_v3(self) noexcept nogil
    cpdef inline void calc_outrc_v1(self) noexcept nogil
    cpdef inline void calc_lz_v2(self) noexcept nogil
    cpdef inline void calc_el_lz_v1(self) noexcept nogil
    cpdef inline void calc_q1_lz_v1(self) noexcept nogil
    cpdef inline void calc_rt_v2(self) noexcept nogil
    cpdef inline void calc_qt_v1(self) noexcept nogil
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature_v1(self) noexcept nogil
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_ei_ic_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_ea_sm_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_el_lz_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_qab_qvs_bw_v1(self, numpy.int64_t k, double[:] h, double[:] k1, double[:] k2, double[:] s0, double[:] qz, double[:] qa1, double[:] qa2, double t0) noexcept nogil
    cpdef inline void calc_outrc_rconcmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_q_v1(self) noexcept nogil
    cpdef inline void calc_tc(self) noexcept nogil
    cpdef inline void calc_fracrain(self) noexcept nogil
    cpdef inline void calc_rfc_sfc(self) noexcept nogil
    cpdef inline void calc_pc(self) noexcept nogil
    cpdef inline void calc_tf_ic(self) noexcept nogil
    cpdef inline void calc_sp_wc(self) noexcept nogil
    cpdef inline void calc_spl_wcl_sp_wc(self) noexcept nogil
    cpdef inline void calc_spg_wcg_sp_wc(self) noexcept nogil
    cpdef inline void calc_cfact(self) noexcept nogil
    cpdef inline void calc_melt_sp_wc(self) noexcept nogil
    cpdef inline void calc_refr_sp_wc(self) noexcept nogil
    cpdef inline void calc_in_wc(self) noexcept nogil
    cpdef inline void calc_swe(self) noexcept nogil
    cpdef inline void calc_sr(self) noexcept nogil
    cpdef inline void calc_gact(self) noexcept nogil
    cpdef inline void calc_glmelt_in(self) noexcept nogil
    cpdef inline void calc_ei_ic(self) noexcept nogil
    cpdef inline void calc_r_sm(self) noexcept nogil
    cpdef inline void calc_ea_sm(self) noexcept nogil
    cpdef inline void calc_qab1_qvs1_bw1(self) noexcept nogil
    cpdef inline void calc_qab2_qvs2_bw2(self) noexcept nogil
    cpdef inline void calc_inrc(self) noexcept nogil
    cpdef inline void calc_outrc(self) noexcept nogil
    cpdef inline void calc_lz(self) noexcept nogil
    cpdef inline void calc_el_lz(self) noexcept nogil
    cpdef inline void calc_q1_lz(self) noexcept nogil
    cpdef inline void calc_rt(self) noexcept nogil
    cpdef inline void calc_qt(self) noexcept nogil
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature(self) noexcept nogil
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_ei_ic_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_ea_sm_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_el_lz_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_qab_qvs_bw(self, numpy.int64_t k, double[:] h, double[:] k1, double[:] k2, double[:] s0, double[:] qz, double[:] qa1, double[:] qa2, double t0) noexcept nogil
    cpdef inline void calc_outrc_rconcmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_q(self) noexcept nogil
