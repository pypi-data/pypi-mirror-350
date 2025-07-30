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
    cdef public double[:] coastfactor
    cdef public double[:] evapotranspirationfactor
@cython.final
cdef class DerivedParameters:
    cdef public double[:] hruareafraction
@cython.final
cdef class Sequences:
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
@cython.final
cdef class FactorSequences:
    cdef public double[:] airtemperature
    cdef public numpy.int64_t _airtemperature_ndim
    cdef public numpy.int64_t _airtemperature_length
    cdef public numpy.int64_t _airtemperature_length_0
    cdef public bint _airtemperature_ramflag
    cdef public double[:,:] _airtemperature_array
    cdef public bint _airtemperature_diskflag_reading
    cdef public bint _airtemperature_diskflag_writing
    cdef public double[:] _airtemperature_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double globalradiation
    cdef public numpy.int64_t _globalradiation_ndim
    cdef public numpy.int64_t _globalradiation_length
    cdef public bint _globalradiation_ramflag
    cdef public double[:] _globalradiation_array
    cdef public bint _globalradiation_diskflag_reading
    cdef public bint _globalradiation_diskflag_writing
    cdef public double[:] _globalradiation_ncarray
    cdef public bint _globalradiation_outputflag
    cdef double *_globalradiation_outputpointer
    cdef public double[:] referenceevapotranspiration
    cdef public numpy.int64_t _referenceevapotranspiration_ndim
    cdef public numpy.int64_t _referenceevapotranspiration_length
    cdef public numpy.int64_t _referenceevapotranspiration_length_0
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:,:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_diskflag_reading
    cdef public bint _referenceevapotranspiration_diskflag_writing
    cdef public double[:] _referenceevapotranspiration_ncarray
    cdef public double meanreferenceevapotranspiration
    cdef public numpy.int64_t _meanreferenceevapotranspiration_ndim
    cdef public numpy.int64_t _meanreferenceevapotranspiration_length
    cdef public bint _meanreferenceevapotranspiration_ramflag
    cdef public double[:] _meanreferenceevapotranspiration_array
    cdef public bint _meanreferenceevapotranspiration_diskflag_reading
    cdef public bint _meanreferenceevapotranspiration_diskflag_writing
    cdef public double[:] _meanreferenceevapotranspiration_ncarray
    cdef public bint _meanreferenceevapotranspiration_outputflag
    cdef double *_meanreferenceevapotranspiration_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface radiationmodel
    cdef public numpy.npy_bool radiationmodel_is_mainmodel
    cdef public numpy.int64_t radiationmodel_typeid
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
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil
    cpdef inline void calc_airtemperature_v1(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration_v2(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration_v1(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration_v1(self) noexcept nogil
    cpdef double get_potentialevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_airtemperature_tempmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void process_radiationmodel(self) noexcept nogil
    cpdef inline void calc_globalradiation(self) noexcept nogil
    cpdef inline void calc_airtemperature(self) noexcept nogil
    cpdef inline void calc_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void adjust_referenceevapotranspiration(self) noexcept nogil
    cpdef inline void calc_meanreferenceevapotranspiration(self) noexcept nogil
    cpdef void determine_potentialevapotranspiration(self) noexcept nogil
    cpdef double get_potentialevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef double get_meanpotentialevapotranspiration(self) noexcept nogil
