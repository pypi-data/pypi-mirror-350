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
@cython.final
cdef class ControlParameters:
    cdef public double length
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public SenderSequences senders
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences:
    cdef public double[:] latq
    cdef public numpy.int64_t _latq_ndim
    cdef public numpy.int64_t _latq_length
    cdef public numpy.int64_t _latq_length_0
    cdef public bint _latq_ramflag
    cdef public double[:,:] _latq_array
    cdef public bint _latq_diskflag_reading
    cdef public bint _latq_diskflag_writing
    cdef public double[:] _latq_ncarray
    cdef double **_latq_pointer
    cdef public numpy.int64_t len_latq
    cdef public numpy.int64_t[:] _latq_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class FactorSequences:
    cdef public double timestep
    cdef public numpy.int64_t _timestep_ndim
    cdef public numpy.int64_t _timestep_length
    cdef public bint _timestep_ramflag
    cdef public double[:] _timestep_array
    cdef public bint _timestep_diskflag_reading
    cdef public bint _timestep_diskflag_writing
    cdef public double[:] _timestep_ncarray
    cdef public bint _timestep_outputflag
    cdef double *_timestep_outputpointer
    cdef public double waterdepth
    cdef public numpy.int64_t _waterdepth_ndim
    cdef public numpy.int64_t _waterdepth_length
    cdef public bint _waterdepth_ramflag
    cdef public double[:] _waterdepth_array
    cdef public bint _waterdepth_diskflag_reading
    cdef public bint _waterdepth_diskflag_writing
    cdef public double[:] _waterdepth_ncarray
    cdef public bint _waterdepth_outputflag
    cdef double *_waterdepth_outputpointer
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double lateralflow
    cdef public numpy.int64_t _lateralflow_ndim
    cdef public numpy.int64_t _lateralflow_length
    cdef public bint _lateralflow_ramflag
    cdef public double[:] _lateralflow_array
    cdef public bint _lateralflow_diskflag_reading
    cdef public bint _lateralflow_diskflag_writing
    cdef public double[:] _lateralflow_ncarray
    cdef public bint _lateralflow_outputflag
    cdef double *_lateralflow_outputpointer
    cdef public double netinflow
    cdef public numpy.int64_t _netinflow_ndim
    cdef public numpy.int64_t _netinflow_length
    cdef public bint _netinflow_ramflag
    cdef public double[:] _netinflow_array
    cdef public bint _netinflow_diskflag_reading
    cdef public bint _netinflow_diskflag_writing
    cdef public double[:] _netinflow_ncarray
    cdef public bint _netinflow_outputflag
    cdef double *_netinflow_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double watervolume
    cdef public numpy.int64_t _watervolume_ndim
    cdef public numpy.int64_t _watervolume_length
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
cdef class SenderSequences:
    cdef public double[:] waterlevel
    cdef public numpy.int64_t _waterlevel_ndim
    cdef public numpy.int64_t _waterlevel_length
    cdef public numpy.int64_t _waterlevel_length_0
    cdef public bint _waterlevel_ramflag
    cdef public double[:,:] _waterlevel_array
    cdef public bint _waterlevel_diskflag_reading
    cdef public bint _waterlevel_diskflag_writing
    cdef public double[:] _waterlevel_ncarray
    cdef double **_waterlevel_pointer
    cdef public numpy.int64_t len_waterlevel
    cdef public numpy.int64_t[:] _waterlevel_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface crosssection
    cdef public numpy.npy_bool crosssection_is_mainmodel
    cdef public numpy.int64_t crosssection_typeid
    cdef public interfaceutils.SubmodelsProperty routingmodelsdownstream
    cdef public interfaceutils.SubmodelsProperty routingmodelsupstream
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
    cpdef inline void pick_lateralflow_v1(self) noexcept nogil
    cpdef inline void calc_waterdepth_waterlevel_v1(self) noexcept nogil
    cpdef double get_watervolume_v1(self) noexcept nogil
    cpdef double get_waterlevel_v1(self) noexcept nogil
    cpdef void set_timestep_v1(self, double timestep) noexcept nogil
    cpdef inline void calc_netinflow_v1(self) noexcept nogil
    cpdef inline void update_watervolume_v1(self) noexcept nogil
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_waterlevel_v1(self) noexcept nogil
    cpdef inline void pick_lateralflow(self) noexcept nogil
    cpdef inline void calc_waterdepth_waterlevel(self) noexcept nogil
    cpdef double get_watervolume(self) noexcept nogil
    cpdef double get_waterlevel(self) noexcept nogil
    cpdef void set_timestep(self, double timestep) noexcept nogil
    cpdef inline void calc_netinflow(self) noexcept nogil
    cpdef inline void update_watervolume(self) noexcept nogil
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void pass_waterlevel(self) noexcept nogil
    cpdef void update_storage_v1(self) noexcept nogil
    cpdef void update_storage(self) noexcept nogil
