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
@cython.final
cdef class ControlParameters:
    cdef public numpy.int64_t nmbhru
    cdef public double[:] hruarea
    cdef public double[:] monthfactor
    cdef public numpy.int64_t _monthfactor_entrymin
    cdef public double[:] dampingfactor
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public double[:] hruareafraction
@cython.final
cdef class Sequences:
    cdef public FluxSequences fluxes
    cdef public LogSequences logs
@cython.final
cdef class FluxSequences:
    cdef public double[:] referenceevapotranspiration
    cdef public numpy.int64_t _referenceevapotranspiration_ndim
    cdef public numpy.int64_t _referenceevapotranspiration_length
    cdef public numpy.int64_t _referenceevapotranspiration_length_0
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:,:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_diskflag_reading
    cdef public bint _referenceevapotranspiration_diskflag_writing
    cdef public double[:] _referenceevapotranspiration_ncarray
    cdef public double[:] potentialevapotranspiration
    cdef public numpy.int64_t _potentialevapotranspiration_ndim
    cdef public numpy.int64_t _potentialevapotranspiration_length
    cdef public numpy.int64_t _potentialevapotranspiration_length_0
    cdef public bint _potentialevapotranspiration_ramflag
    cdef public double[:,:] _potentialevapotranspiration_array
    cdef public bint _potentialevapotranspiration_diskflag_reading
    cdef public bint _potentialevapotranspiration_diskflag_writing
    cdef public double[:] _potentialevapotranspiration_ncarray
    cdef public double meanpotentialevapotranspiration
    cdef public numpy.int64_t _meanpotentialevapotranspiration_ndim
    cdef public numpy.int64_t _meanpotentialevapotranspiration_length
    cdef public bint _meanpotentialevapotranspiration_ramflag
    cdef public double[:] _meanpotentialevapotranspiration_array
    cdef public bint _meanpotentialevapotranspiration_diskflag_reading
    cdef public bint _meanpotentialevapotranspiration_diskflag_writing
    cdef public double[:] _meanpotentialevapotranspiration_ncarray
    cdef public bint _meanpotentialevapotranspiration_outputflag
    cdef double *_meanpotentialevapotranspiration_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:,:] loggedpotentialevapotranspiration
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_ndim
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length_0
    cdef public numpy.int64_t _loggedpotentialevapotranspiration_length_1
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface retmodel
    cdef public numpy.npy_bool retmodel_is_mainmodel
    cdef public numpy.int64_t retmodel_typeid
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
    cpdef inline void calc_referenceevapotranspiration_v4(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void update_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_potentialevapotranspiration_v2(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration(self) noexcept nogil
    cpdef inline void update_potentialevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_petmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
