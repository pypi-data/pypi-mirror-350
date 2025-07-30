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
    cdef public DerivedParameters derived
@cython.final
cdef class DerivedParameters:
    cdef public double seconds
@cython.final
cdef class Sequences:
    cdef public FactorSequences factors
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
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_sim
    cdef public numpy.npy_bool threading
    cdef public double timeleft
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public interfaceutils.SubmodelsProperty channelmodels
    cdef public interfaceutils.SubmodelsProperty routingmodels
    cdef public interfaceutils.SubmodelsProperty storagemodels
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
    cpdef inline void calc_maxtimesteps_v1(self) noexcept nogil
    cpdef inline void calc_timestep_v1(self) noexcept nogil
    cpdef inline void send_timestep_v1(self) noexcept nogil
    cpdef inline void calc_discharges_v1(self) noexcept nogil
    cpdef inline void update_storages_v1(self) noexcept nogil
    cpdef inline void calc_maxtimesteps(self) noexcept nogil
    cpdef inline void calc_timestep(self) noexcept nogil
    cpdef inline void send_timestep(self) noexcept nogil
    cpdef inline void calc_discharges(self) noexcept nogil
    cpdef inline void update_storages(self) noexcept nogil
