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
    cdef public double[:] hrualtitude
    cdef public double[:] evapotranspirationfactor
    cdef public double[:] altitudefactor
    cdef public double[:] precipitationfactor
    cdef public double[:] airtemperaturefactor
@cython.final
cdef class DerivedParameters:
    cdef public double[:] hruareafraction
    cdef public double altitude
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
@cython.final
cdef class InputSequences:
    cdef public double normalairtemperature
    cdef public numpy.int64_t _normalairtemperature_ndim
    cdef public numpy.int64_t _normalairtemperature_length
    cdef public bint _normalairtemperature_ramflag
    cdef public double[:] _normalairtemperature_array
    cdef public bint _normalairtemperature_diskflag_reading
    cdef public bint _normalairtemperature_diskflag_writing
    cdef public double[:] _normalairtemperature_ncarray
    cdef public bint _normalairtemperature_inputflag
    cdef double *_normalairtemperature_inputpointer
    cdef public double normalevapotranspiration
    cdef public numpy.int64_t _normalevapotranspiration_ndim
    cdef public numpy.int64_t _normalevapotranspiration_length
    cdef public bint _normalevapotranspiration_ramflag
    cdef public double[:] _normalevapotranspiration_array
    cdef public bint _normalevapotranspiration_diskflag_reading
    cdef public bint _normalevapotranspiration_diskflag_writing
    cdef public double[:] _normalevapotranspiration_ncarray
    cdef public bint _normalevapotranspiration_inputflag
    cdef double *_normalevapotranspiration_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double meanairtemperature
    cdef public numpy.int64_t _meanairtemperature_ndim
    cdef public numpy.int64_t _meanairtemperature_length
    cdef public bint _meanairtemperature_ramflag
    cdef public double[:] _meanairtemperature_array
    cdef public bint _meanairtemperature_diskflag_reading
    cdef public bint _meanairtemperature_diskflag_writing
    cdef public double[:] _meanairtemperature_ncarray
    cdef public bint _meanairtemperature_outputflag
    cdef double *_meanairtemperature_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
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
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface precipmodel
    cdef public numpy.npy_bool precipmodel_is_mainmodel
    cdef public numpy.int64_t precipmodel_typeid
    cdef public masterinterface.MasterInterface tempmodel
    cdef public numpy.npy_bool tempmodel_is_mainmodel
    cdef public numpy.int64_t tempmodel_typeid
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
    cpdef inline void calc_meanairtemperature_v1(self) noexcept nogil
    cpdef inline void calc_precipitation_v1(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v5(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration_v3(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_potentialevapotranspiration_v2(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_meanairtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_meanairtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_precipitation_precipmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_meanairtemperature(self) noexcept nogil
    cpdef inline void calc_precipitation(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void calc_potentialevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanpotentialevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil
