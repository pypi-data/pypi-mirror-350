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
    cdef public numpy.int64_t nmbhru
    cdef public numpy.npy_bool[:] water
    cdef public numpy.npy_bool[:] interception
    cdef public numpy.npy_bool[:] soil
    cdef public double[:] maxsoilwater
    cdef public double[:] dissefactor
@cython.final
cdef class Sequences:
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
@cython.final
cdef class FactorSequences:
    cdef public double[:] interceptedwater
    cdef public numpy.int64_t _interceptedwater_ndim
    cdef public numpy.int64_t _interceptedwater_length
    cdef public numpy.int64_t _interceptedwater_length_0
    cdef public bint _interceptedwater_ramflag
    cdef public double[:,:] _interceptedwater_array
    cdef public bint _interceptedwater_diskflag_reading
    cdef public bint _interceptedwater_diskflag_writing
    cdef public double[:] _interceptedwater_ncarray
    cdef public double[:] soilwater
    cdef public numpy.int64_t _soilwater_ndim
    cdef public numpy.int64_t _soilwater_length
    cdef public numpy.int64_t _soilwater_length_0
    cdef public bint _soilwater_ramflag
    cdef public double[:,:] _soilwater_array
    cdef public bint _soilwater_diskflag_reading
    cdef public bint _soilwater_diskflag_writing
    cdef public double[:] _soilwater_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double[:] potentialinterceptionevaporation
    cdef public numpy.int64_t _potentialinterceptionevaporation_ndim
    cdef public numpy.int64_t _potentialinterceptionevaporation_length
    cdef public numpy.int64_t _potentialinterceptionevaporation_length_0
    cdef public bint _potentialinterceptionevaporation_ramflag
    cdef public double[:,:] _potentialinterceptionevaporation_array
    cdef public bint _potentialinterceptionevaporation_diskflag_reading
    cdef public bint _potentialinterceptionevaporation_diskflag_writing
    cdef public double[:] _potentialinterceptionevaporation_ncarray
    cdef public double[:] potentialsoilevapotranspiration
    cdef public numpy.int64_t _potentialsoilevapotranspiration_ndim
    cdef public numpy.int64_t _potentialsoilevapotranspiration_length
    cdef public numpy.int64_t _potentialsoilevapotranspiration_length_0
    cdef public bint _potentialsoilevapotranspiration_ramflag
    cdef public double[:,:] _potentialsoilevapotranspiration_array
    cdef public bint _potentialsoilevapotranspiration_diskflag_reading
    cdef public bint _potentialsoilevapotranspiration_diskflag_writing
    cdef public double[:] _potentialsoilevapotranspiration_ncarray
    cdef public double[:] potentialwaterevaporation
    cdef public numpy.int64_t _potentialwaterevaporation_ndim
    cdef public numpy.int64_t _potentialwaterevaporation_length
    cdef public numpy.int64_t _potentialwaterevaporation_length_0
    cdef public bint _potentialwaterevaporation_ramflag
    cdef public double[:,:] _potentialwaterevaporation_array
    cdef public bint _potentialwaterevaporation_diskflag_reading
    cdef public bint _potentialwaterevaporation_diskflag_writing
    cdef public double[:] _potentialwaterevaporation_ncarray
    cdef public double[:] waterevaporation
    cdef public numpy.int64_t _waterevaporation_ndim
    cdef public numpy.int64_t _waterevaporation_length
    cdef public numpy.int64_t _waterevaporation_length_0
    cdef public bint _waterevaporation_ramflag
    cdef public double[:,:] _waterevaporation_array
    cdef public bint _waterevaporation_diskflag_reading
    cdef public bint _waterevaporation_diskflag_writing
    cdef public double[:] _waterevaporation_ncarray
    cdef public double[:] interceptionevaporation
    cdef public numpy.int64_t _interceptionevaporation_ndim
    cdef public numpy.int64_t _interceptionevaporation_length
    cdef public numpy.int64_t _interceptionevaporation_length_0
    cdef public bint _interceptionevaporation_ramflag
    cdef public double[:,:] _interceptionevaporation_array
    cdef public bint _interceptionevaporation_diskflag_reading
    cdef public bint _interceptionevaporation_diskflag_writing
    cdef public double[:] _interceptionevaporation_ncarray
    cdef public double[:] soilevapotranspiration
    cdef public numpy.int64_t _soilevapotranspiration_ndim
    cdef public numpy.int64_t _soilevapotranspiration_length
    cdef public numpy.int64_t _soilevapotranspiration_length_0
    cdef public bint _soilevapotranspiration_ramflag
    cdef public double[:,:] _soilevapotranspiration_array
    cdef public bint _soilevapotranspiration_diskflag_reading
    cdef public bint _soilevapotranspiration_diskflag_writing
    cdef public double[:] _soilevapotranspiration_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface intercmodel
    cdef public numpy.npy_bool intercmodel_is_mainmodel
    cdef public numpy.int64_t intercmodel_typeid
    cdef public masterinterface.MasterInterface petmodel
    cdef public numpy.npy_bool petmodel_is_mainmodel
    cdef public numpy.int64_t petmodel_typeid
    cdef public masterinterface.MasterInterface soilwatermodel
    cdef public numpy.npy_bool soilwatermodel_is_mainmodel
    cdef public numpy.int64_t soilwatermodel_typeid
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
    cpdef double get_waterevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_interceptionevaporation_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilevapotranspiration_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation_v3(self) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation_v1(self) noexcept nogil
    cpdef inline void calc_waterevaporation_v2(self) noexcept nogil
    cpdef inline void calc_interceptedwater_v1(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation_v1(self) noexcept nogil
    cpdef inline void calc_soilwater_v1(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration_v2(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_v2(self) noexcept nogil
    cpdef inline void update_soilevapotranspiration_v3(self) noexcept nogil
    cpdef inline void calc_interceptedwater_intercmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilwater_soilwatermodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef double get_waterevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_interceptionevaporation(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilevapotranspiration(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_potentialinterceptionevaporation(self) noexcept nogil
    cpdef inline void calc_potentialwaterevaporation(self) noexcept nogil
    cpdef inline void calc_waterevaporation(self) noexcept nogil
    cpdef inline void calc_interceptedwater(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation(self) noexcept nogil
    cpdef inline void calc_soilwater(self) noexcept nogil
    cpdef inline void calc_potentialsoilevapotranspiration(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration(self) noexcept nogil
    cpdef inline void update_soilevapotranspiration(self) noexcept nogil
    cpdef inline void calc_interceptedwater_intercmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilwater_soilwatermodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef void determine_interceptionevaporation_v1(self) noexcept nogil
    cpdef void determine_soilevapotranspiration_v2(self) noexcept nogil
    cpdef void determine_waterevaporation_v2(self) noexcept nogil
    cpdef void determine_interceptionevaporation(self) noexcept nogil
    cpdef void determine_soilevapotranspiration(self) noexcept nogil
    cpdef void determine_waterevaporation(self) noexcept nogil
