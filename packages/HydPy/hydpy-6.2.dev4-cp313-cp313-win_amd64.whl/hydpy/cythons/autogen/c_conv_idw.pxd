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
    cdef public double[:,:] inputcoordinates
    cdef public double[:,:] outputcoordinates
    cdef public numpy.int64_t maxnmbinputs
    cdef public double power
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t nmbinputs
    cdef public numpy.int64_t nmboutputs
    cdef public double[:,:] distances
    cdef public numpy.int64_t[:,:] proximityorder
    cdef public double[:,:] weights
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences:
    cdef public double[:] inputs
    cdef public numpy.int64_t _inputs_ndim
    cdef public numpy.int64_t _inputs_length
    cdef public numpy.int64_t _inputs_length_0
    cdef public bint _inputs_ramflag
    cdef public double[:,:] _inputs_array
    cdef public bint _inputs_diskflag_reading
    cdef public bint _inputs_diskflag_writing
    cdef public double[:] _inputs_ncarray
    cdef double **_inputs_pointer
    cdef public numpy.int64_t len_inputs
    cdef public numpy.int64_t[:] _inputs_ready
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline alloc_pointer(self, name, numpy.int64_t length)
    cpdef inline dealloc_pointer(self, name)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx)
    cpdef get_pointervalue(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class FluxSequences:
    cdef public double[:] inputs
    cdef public numpy.int64_t _inputs_ndim
    cdef public numpy.int64_t _inputs_length
    cdef public numpy.int64_t _inputs_length_0
    cdef public bint _inputs_ramflag
    cdef public double[:,:] _inputs_array
    cdef public bint _inputs_diskflag_reading
    cdef public bint _inputs_diskflag_writing
    cdef public double[:] _inputs_ncarray
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
    cdef public double[:] outputs
    cdef public numpy.int64_t _outputs_ndim
    cdef public numpy.int64_t _outputs_length
    cdef public numpy.int64_t _outputs_length_0
    cdef public bint _outputs_ramflag
    cdef public double[:,:] _outputs_array
    cdef public bint _outputs_diskflag_reading
    cdef public bint _outputs_diskflag_writing
    cdef public double[:] _outputs_ncarray
    cdef double **_outputs_pointer
    cdef public numpy.int64_t len_outputs
    cdef public numpy.int64_t[:] _outputs_ready
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
    cpdef inline void pick_inputs_v1(self) noexcept nogil
    cpdef inline void calc_outputs_v2(self) noexcept nogil
    cpdef inline void interpolate_inversedistance_v1(self, double[:] inputs, double[:] outputs) noexcept nogil
    cpdef inline void pass_outputs_v1(self) noexcept nogil
    cpdef inline void pick_inputs(self) noexcept nogil
    cpdef inline void calc_outputs(self) noexcept nogil
    cpdef inline void interpolate_inversedistance(self, double[:] inputs, double[:] outputs) noexcept nogil
    cpdef inline void pass_outputs(self) noexcept nogil
