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
    cdef public double catchmentarea
    cdef public numpy.int64_t nmbsegments
    cdef public double length
    cdef public double bottomslope
@cython.final
cdef class DerivedParameters:
    cdef public double seconds
    cdef public double segmentlength
@cython.final
cdef class SolverParameters:
    cdef public double tolerancewaterdepth
    cdef public double tolerancedischarge
    cdef public double tolerancenegativeinflow
    cdef public numpy.int64_t nmbruns
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FactorSequences factors
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
cdef class FactorSequences:
    cdef public double[:] referencewaterdepth
    cdef public numpy.int64_t _referencewaterdepth_ndim
    cdef public numpy.int64_t _referencewaterdepth_length
    cdef public numpy.int64_t _referencewaterdepth_length_0
    cdef public bint _referencewaterdepth_ramflag
    cdef public double[:,:] _referencewaterdepth_array
    cdef public bint _referencewaterdepth_diskflag_reading
    cdef public bint _referencewaterdepth_diskflag_writing
    cdef public double[:] _referencewaterdepth_ncarray
    cdef public double[:] wettedarea
    cdef public numpy.int64_t _wettedarea_ndim
    cdef public numpy.int64_t _wettedarea_length
    cdef public numpy.int64_t _wettedarea_length_0
    cdef public bint _wettedarea_ramflag
    cdef public double[:,:] _wettedarea_array
    cdef public bint _wettedarea_diskflag_reading
    cdef public bint _wettedarea_diskflag_writing
    cdef public double[:] _wettedarea_ncarray
    cdef public double[:] surfacewidth
    cdef public numpy.int64_t _surfacewidth_ndim
    cdef public numpy.int64_t _surfacewidth_length
    cdef public numpy.int64_t _surfacewidth_length_0
    cdef public bint _surfacewidth_ramflag
    cdef public double[:,:] _surfacewidth_array
    cdef public bint _surfacewidth_diskflag_reading
    cdef public bint _surfacewidth_diskflag_writing
    cdef public double[:] _surfacewidth_ncarray
    cdef public double[:] celerity
    cdef public numpy.int64_t _celerity_ndim
    cdef public numpy.int64_t _celerity_length
    cdef public numpy.int64_t _celerity_length_0
    cdef public bint _celerity_ramflag
    cdef public double[:,:] _celerity_array
    cdef public bint _celerity_diskflag_reading
    cdef public bint _celerity_diskflag_writing
    cdef public double[:] _celerity_ncarray
    cdef public double[:] correctingfactor
    cdef public numpy.int64_t _correctingfactor_ndim
    cdef public numpy.int64_t _correctingfactor_length
    cdef public numpy.int64_t _correctingfactor_length_0
    cdef public bint _correctingfactor_ramflag
    cdef public double[:,:] _correctingfactor_array
    cdef public bint _correctingfactor_diskflag_reading
    cdef public bint _correctingfactor_diskflag_writing
    cdef public double[:] _correctingfactor_ncarray
    cdef public double[:] coefficient1
    cdef public numpy.int64_t _coefficient1_ndim
    cdef public numpy.int64_t _coefficient1_length
    cdef public numpy.int64_t _coefficient1_length_0
    cdef public bint _coefficient1_ramflag
    cdef public double[:,:] _coefficient1_array
    cdef public bint _coefficient1_diskflag_reading
    cdef public bint _coefficient1_diskflag_writing
    cdef public double[:] _coefficient1_ncarray
    cdef public double[:] coefficient2
    cdef public numpy.int64_t _coefficient2_ndim
    cdef public numpy.int64_t _coefficient2_length
    cdef public numpy.int64_t _coefficient2_length_0
    cdef public bint _coefficient2_ramflag
    cdef public double[:,:] _coefficient2_array
    cdef public bint _coefficient2_diskflag_reading
    cdef public bint _coefficient2_diskflag_writing
    cdef public double[:] _coefficient2_ncarray
    cdef public double[:] coefficient3
    cdef public numpy.int64_t _coefficient3_ndim
    cdef public numpy.int64_t _coefficient3_length
    cdef public numpy.int64_t _coefficient3_length_0
    cdef public bint _coefficient3_ramflag
    cdef public double[:,:] _coefficient3_array
    cdef public bint _coefficient3_diskflag_reading
    cdef public bint _coefficient3_diskflag_writing
    cdef public double[:] _coefficient3_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double inflow
    cdef public numpy.int64_t _inflow_ndim
    cdef public numpy.int64_t _inflow_length
    cdef public bint _inflow_ramflag
    cdef public double[:] _inflow_array
    cdef public bint _inflow_diskflag_reading
    cdef public bint _inflow_diskflag_writing
    cdef public double[:] _inflow_ncarray
    cdef public bint _inflow_outputflag
    cdef double *_inflow_outputpointer
    cdef public double[:] referencedischarge
    cdef public numpy.int64_t _referencedischarge_ndim
    cdef public numpy.int64_t _referencedischarge_length
    cdef public numpy.int64_t _referencedischarge_length_0
    cdef public bint _referencedischarge_ramflag
    cdef public double[:,:] _referencedischarge_array
    cdef public bint _referencedischarge_diskflag_reading
    cdef public bint _referencedischarge_diskflag_writing
    cdef public double[:] _referencedischarge_ncarray
    cdef public double outflow
    cdef public numpy.int64_t _outflow_ndim
    cdef public numpy.int64_t _outflow_length
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
    cdef public double[:] courantnumber
    cdef public numpy.int64_t _courantnumber_ndim
    cdef public numpy.int64_t _courantnumber_length
    cdef public numpy.int64_t _courantnumber_length_0
    cdef public bint _courantnumber_ramflag
    cdef public double[:,:] _courantnumber_array
    cdef public bint _courantnumber_diskflag_reading
    cdef public bint _courantnumber_diskflag_writing
    cdef public double[:] _courantnumber_ncarray
    cdef public double[:] reynoldsnumber
    cdef public numpy.int64_t _reynoldsnumber_ndim
    cdef public numpy.int64_t _reynoldsnumber_length
    cdef public numpy.int64_t _reynoldsnumber_length_0
    cdef public bint _reynoldsnumber_ramflag
    cdef public double[:,:] _reynoldsnumber_array
    cdef public bint _reynoldsnumber_diskflag_reading
    cdef public bint _reynoldsnumber_diskflag_writing
    cdef public double[:] _reynoldsnumber_ncarray
    cdef public double[:] discharge
    cdef public numpy.int64_t _discharge_ndim
    cdef public numpy.int64_t _discharge_length
    cdef public numpy.int64_t _discharge_length_0
    cdef public bint _discharge_ramflag
    cdef public double[:,:] _discharge_array
    cdef public bint _discharge_diskflag_reading
    cdef public bint _discharge_diskflag_writing
    cdef public double[:] _discharge_ncarray
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
cdef class PegasusReferenceWaterDepth(rootutils.PegasusBase):
    cdef public Model model
    cpdef double apply_method0(self, double x)  noexcept nogil
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_segment
    cdef public numpy.int64_t idx_run
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface wqmodel
    cdef public numpy.npy_bool wqmodel_is_mainmodel
    cdef public numpy.int64_t wqmodel_typeid
    cdef public PegasusReferenceWaterDepth pegasusreferencewaterdepth
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
    cpdef inline void pick_inflow_v1(self) noexcept nogil
    cpdef inline void adjust_inflow_v1(self) noexcept nogil
    cpdef inline void update_discharge_v1(self) noexcept nogil
    cpdef inline void calc_referencedischarge_v1(self) noexcept nogil
    cpdef inline void calc_referencewaterdepth_v1(self) noexcept nogil
    cpdef inline void calc_wettedarea_surfacewidth_celerity_v1(self) noexcept nogil
    cpdef inline void calc_correctingfactor_v1(self) noexcept nogil
    cpdef inline void calc_courantnumber_v1(self) noexcept nogil
    cpdef inline void calc_reynoldsnumber_v1(self) noexcept nogil
    cpdef inline void calc_coefficient1_coefficient2_coefficient3_v1(self) noexcept nogil
    cpdef inline void calc_discharge_v2(self) noexcept nogil
    cpdef inline double return_discharge_crosssectionmodel_v1(self, masterinterface.MasterInterface wqmodel, double waterdepth) noexcept nogil
    cpdef inline void calc_wettedarea_surfacewidth_celerity_crosssectionmodel_v1(self, masterinterface.MasterInterface wqmodel) noexcept nogil
    cpdef inline double return_referencedischargeerror_v1(self, double waterdepth) noexcept nogil
    cpdef inline void calc_outflow_v1(self) noexcept nogil
    cpdef inline void pass_outflow_v1(self) noexcept nogil
    cpdef inline void pick_inflow(self) noexcept nogil
    cpdef inline void adjust_inflow(self) noexcept nogil
    cpdef inline void update_discharge(self) noexcept nogil
    cpdef inline void calc_referencedischarge(self) noexcept nogil
    cpdef inline void calc_referencewaterdepth(self) noexcept nogil
    cpdef inline void calc_wettedarea_surfacewidth_celerity(self) noexcept nogil
    cpdef inline void calc_correctingfactor(self) noexcept nogil
    cpdef inline void calc_courantnumber(self) noexcept nogil
    cpdef inline void calc_reynoldsnumber(self) noexcept nogil
    cpdef inline void calc_coefficient1_coefficient2_coefficient3(self) noexcept nogil
    cpdef inline void calc_discharge(self) noexcept nogil
    cpdef inline double return_discharge_crosssectionmodel(self, masterinterface.MasterInterface wqmodel, double waterdepth) noexcept nogil
    cpdef inline void calc_wettedarea_surfacewidth_celerity_crosssectionmodel(self, masterinterface.MasterInterface wqmodel) noexcept nogil
    cpdef inline double return_referencedischargeerror(self, double waterdepth) noexcept nogil
    cpdef inline void calc_outflow(self) noexcept nogil
    cpdef inline void pass_outflow(self) noexcept nogil
