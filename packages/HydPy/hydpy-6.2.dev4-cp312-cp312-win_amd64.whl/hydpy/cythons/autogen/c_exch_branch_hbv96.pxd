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
    cdef public double[:] delta
    cdef public numpy.int64_t _delta_entrymin
    cdef public double minimum
    cdef public double[:] xpoints
    cdef public double[:,:] ypoints
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public numpy.int64_t nmbbranches
    cdef public numpy.int64_t nmbpoints
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences:
    cdef public double[:] total
    cdef public numpy.int64_t _total_ndim
    cdef public numpy.int64_t _total_length
    cdef public numpy.int64_t _total_length_0
    cdef public bint _total_ramflag
    cdef public double[:,:] _total_array
    cdef public bint _total_diskflag_reading
    cdef public bint _total_diskflag_writing
    cdef public double[:] _total_ncarray
    cdef double **_total_pointer
    cdef public numpy.int64_t len_total
    cdef public numpy.int64_t[:] _total_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class FluxSequences:
    cdef public double originalinput
    cdef public numpy.int64_t _originalinput_ndim
    cdef public numpy.int64_t _originalinput_length
    cdef public bint _originalinput_ramflag
    cdef public double[:] _originalinput_array
    cdef public bint _originalinput_diskflag_reading
    cdef public bint _originalinput_diskflag_writing
    cdef public double[:] _originalinput_ncarray
    cdef public bint _originalinput_outputflag
    cdef double *_originalinput_outputpointer
    cdef public double adjustedinput
    cdef public numpy.int64_t _adjustedinput_ndim
    cdef public numpy.int64_t _adjustedinput_length
    cdef public bint _adjustedinput_ramflag
    cdef public double[:] _adjustedinput_array
    cdef public bint _adjustedinput_diskflag_reading
    cdef public bint _adjustedinput_diskflag_writing
    cdef public double[:] _adjustedinput_ncarray
    cdef public bint _adjustedinput_outputflag
    cdef double *_adjustedinput_outputpointer
    cdef public double[:] outputs
    cdef public numpy.int64_t _outputs_ndim
    cdef public numpy.int64_t _outputs_length
    cdef public numpy.int64_t _outputs_length_0
    cdef public bint _outputs_ramflag
    cdef public double[:,:] _outputs_array
    cdef public bint _outputs_diskflag_reading
    cdef public bint _outputs_diskflag_writing
    cdef public double[:] _outputs_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class OutletSequences:
    cdef public double[:] branched
    cdef public numpy.int64_t _branched_ndim
    cdef public numpy.int64_t _branched_length
    cdef public numpy.int64_t _branched_length_0
    cdef public bint _branched_ramflag
    cdef public double[:,:] _branched_array
    cdef public bint _branched_diskflag_reading
    cdef public bint _branched_diskflag_writing
    cdef public double[:] _branched_ncarray
    cdef double **_branched_pointer
    cdef public numpy.int64_t len_branched
    cdef public numpy.int64_t[:] _branched_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class Model:
    cdef public numpy.int64_t idx_sim
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
    cpdef inline void pick_originalinput_v1(self) noexcept nogil
    cpdef inline void calc_adjustedinput_v1(self) noexcept nogil
    cpdef inline void calc_outputs_v1(self) noexcept nogil
    cpdef inline void pass_outputs_v1(self) noexcept nogil
    cpdef inline void pick_originalinput(self) noexcept nogil
    cpdef inline void calc_adjustedinput(self) noexcept nogil
    cpdef inline void calc_outputs(self) noexcept nogil
    cpdef inline void pass_outputs(self) noexcept nogil
