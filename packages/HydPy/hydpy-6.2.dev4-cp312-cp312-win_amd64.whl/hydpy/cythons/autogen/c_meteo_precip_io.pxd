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
    cdef public double[:] precipitationfactor
@cython.final
cdef class DerivedParameters:
    cdef public double[:] hruareafraction
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
@cython.final
cdef class InputSequences:
    cdef public double precipitation
    cdef public numpy.int64_t _precipitation_ndim
    cdef public numpy.int64_t _precipitation_length
    cdef public bint _precipitation_ramflag
    cdef public double[:] _precipitation_array
    cdef public bint _precipitation_diskflag_reading
    cdef public bint _precipitation_diskflag_writing
    cdef public double[:] _precipitation_ncarray
    cdef public bint _precipitation_inputflag
    cdef double *_precipitation_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FluxSequences:
    cdef public double[:] precipitation
    cdef public numpy.int64_t _precipitation_ndim
    cdef public numpy.int64_t _precipitation_length
    cdef public numpy.int64_t _precipitation_length_0
    cdef public bint _precipitation_ramflag
    cdef public double[:,:] _precipitation_array
    cdef public bint _precipitation_diskflag_reading
    cdef public bint _precipitation_diskflag_writing
    cdef public double[:] _precipitation_ncarray
    cdef public double meanprecipitation
    cdef public numpy.int64_t _meanprecipitation_ndim
    cdef public numpy.int64_t _meanprecipitation_length
    cdef public bint _meanprecipitation_ramflag
    cdef public double[:] _meanprecipitation_array
    cdef public bint _meanprecipitation_diskflag_reading
    cdef public bint _meanprecipitation_diskflag_writing
    cdef public double[:] _meanprecipitation_ncarray
    cdef public bint _meanprecipitation_outputflag
    cdef double *_meanprecipitation_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef inline void calc_precipitation_v1(self) noexcept nogil
    cpdef inline void adjust_precipitation_v1(self) noexcept nogil
    cpdef inline void calc_meanprecipitation_v1(self) noexcept nogil
    cpdef void determine_precipitation_v1(self) noexcept nogil
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meanprecipitation_v1(self) noexcept nogil
    cpdef inline void calc_precipitation(self) noexcept nogil
    cpdef inline void adjust_precipitation(self) noexcept nogil
    cpdef inline void calc_meanprecipitation(self) noexcept nogil
    cpdef void determine_precipitation(self) noexcept nogil
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meanprecipitation(self) noexcept nogil
