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
    cdef public FixedParameters fixed
@cython.final
cdef class ControlParameters:
    cdef public double lengthupstream
    cdef public double timestepfactor
    cdef public double crestheight
    cdef public double crestwidth
    cdef public double flowcoefficient
@cython.final
cdef class DerivedParameters:
    cdef public double seconds
@cython.final
cdef class FixedParameters:
    cdef public double gravitationalacceleration
@cython.final
cdef class Sequences:
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class FactorSequences:
    cdef public double maxtimestep
    cdef public numpy.int64_t _maxtimestep_ndim
    cdef public numpy.int64_t _maxtimestep_length
    cdef public bint _maxtimestep_ramflag
    cdef public double[:] _maxtimestep_array
    cdef public bint _maxtimestep_diskflag_reading
    cdef public bint _maxtimestep_diskflag_writing
    cdef public double[:] _maxtimestep_ncarray
    cdef public bint _maxtimestep_outputflag
    cdef double *_maxtimestep_outputpointer
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
    cdef public double waterlevelupstream
    cdef public numpy.int64_t _waterlevelupstream_ndim
    cdef public numpy.int64_t _waterlevelupstream_length
    cdef public bint _waterlevelupstream_ramflag
    cdef public double[:] _waterlevelupstream_array
    cdef public bint _waterlevelupstream_diskflag_reading
    cdef public bint _waterlevelupstream_diskflag_writing
    cdef public double[:] _waterlevelupstream_ncarray
    cdef public bint _waterlevelupstream_outputflag
    cdef double *_waterlevelupstream_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double dischargevolume
    cdef public numpy.int64_t _dischargevolume_ndim
    cdef public numpy.int64_t _dischargevolume_length
    cdef public bint _dischargevolume_ramflag
    cdef public double[:] _dischargevolume_array
    cdef public bint _dischargevolume_diskflag_reading
    cdef public bint _dischargevolume_diskflag_writing
    cdef public double[:] _dischargevolume_ncarray
    cdef public bint _dischargevolume_outputflag
    cdef double *_dischargevolume_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double discharge
    cdef public numpy.int64_t _discharge_ndim
    cdef public numpy.int64_t _discharge_length
    cdef public bint _discharge_ramflag
    cdef public double[:] _discharge_array
    cdef public bint _discharge_diskflag_reading
    cdef public bint _discharge_diskflag_writing
    cdef public double[:] _discharge_ncarray
    cdef public bint _discharge_outputflag
    cdef double *_discharge_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class OutletSequences:
    cdef public double[:] longq
    cdef public numpy.int64_t _longq_ndim
    cdef public numpy.int64_t _longq_length
    cdef public numpy.int64_t _longq_length_0
    cdef public bint _longq_ramflag
    cdef public double[:,:] _longq_array
    cdef public bint _longq_diskflag_reading
    cdef public bint _longq_diskflag_writing
    cdef public double[:] _longq_ncarray
    cdef double **_longq_pointer
    cdef public numpy.int64_t len_longq
    cdef public numpy.int64_t[:] _longq_ready
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
    cdef public interfaceutils.SubmodelsProperty routingmodelsupstream
    cdef public masterinterface.MasterInterface storagemodelupstream
    cdef public numpy.npy_bool storagemodelupstream_is_mainmodel
    cdef public numpy.int64_t storagemodelupstream_typeid
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
    cpdef inline void reset_dischargevolume_v1(self) noexcept nogil
    cpdef double get_maxtimestep_v1(self) noexcept nogil
    cpdef double get_discharge_v1(self) noexcept nogil
    cpdef double get_partialdischargedownstream_v1(self, double clientdischarge) noexcept nogil
    cpdef double get_dischargevolume_v1(self) noexcept nogil
    cpdef void set_timestep_v1(self, double timestep) noexcept nogil
    cpdef inline void calc_waterlevelupstream_v1(self) noexcept nogil
    cpdef inline void calc_waterlevel_v3(self) noexcept nogil
    cpdef inline void calc_maxtimestep_v3(self) noexcept nogil
    cpdef inline void calc_discharge_v2(self) noexcept nogil
    cpdef inline void update_dischargevolume_v1(self) noexcept nogil
    cpdef inline void pass_discharge_v1(self) noexcept nogil
    cpdef inline void reset_dischargevolume(self) noexcept nogil
    cpdef double get_maxtimestep(self) noexcept nogil
    cpdef double get_discharge(self) noexcept nogil
    cpdef double get_partialdischargedownstream(self, double clientdischarge) noexcept nogil
    cpdef double get_dischargevolume(self) noexcept nogil
    cpdef void set_timestep(self, double timestep) noexcept nogil
    cpdef inline void calc_waterlevelupstream(self) noexcept nogil
    cpdef inline void calc_waterlevel(self) noexcept nogil
    cpdef inline void calc_maxtimestep(self) noexcept nogil
    cpdef inline void calc_discharge(self) noexcept nogil
    cpdef inline void update_dischargevolume(self) noexcept nogil
    cpdef inline void pass_discharge(self) noexcept nogil
    cpdef void determine_maxtimestep_v3(self) noexcept nogil
    cpdef void determine_discharge_v3(self) noexcept nogil
    cpdef void determine_maxtimestep(self) noexcept nogil
    cpdef void determine_discharge(self) noexcept nogil
