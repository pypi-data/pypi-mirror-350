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
    cdef public numpy.int64_t nmbtrapezes
    cdef public double[:] bottomlevels
    cdef public double[:] bottomwidths
    cdef public double[:] sideslopes
    cdef public double[:] stricklercoefficients
    cdef public double bottomslope
@cython.final
cdef class DerivedParameters:
    cdef public double[:] bottomdepths
    cdef public double[:] trapezeheights
    cdef public double[:] slopewidths
    cdef public double[:] perimeterderivatives
@cython.final
cdef class Sequences:
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
@cython.final
cdef class FactorSequences:
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
    cdef public double[:] wettedareas
    cdef public numpy.int64_t _wettedareas_ndim
    cdef public numpy.int64_t _wettedareas_length
    cdef public numpy.int64_t _wettedareas_length_0
    cdef public bint _wettedareas_ramflag
    cdef public double[:,:] _wettedareas_array
    cdef public bint _wettedareas_diskflag_reading
    cdef public bint _wettedareas_diskflag_writing
    cdef public double[:] _wettedareas_ncarray
    cdef public double wettedarea
    cdef public numpy.int64_t _wettedarea_ndim
    cdef public numpy.int64_t _wettedarea_length
    cdef public bint _wettedarea_ramflag
    cdef public double[:] _wettedarea_array
    cdef public bint _wettedarea_diskflag_reading
    cdef public bint _wettedarea_diskflag_writing
    cdef public double[:] _wettedarea_ncarray
    cdef public bint _wettedarea_outputflag
    cdef double *_wettedarea_outputpointer
    cdef public double[:] wettedperimeters
    cdef public numpy.int64_t _wettedperimeters_ndim
    cdef public numpy.int64_t _wettedperimeters_length
    cdef public numpy.int64_t _wettedperimeters_length_0
    cdef public bint _wettedperimeters_ramflag
    cdef public double[:,:] _wettedperimeters_array
    cdef public bint _wettedperimeters_diskflag_reading
    cdef public bint _wettedperimeters_diskflag_writing
    cdef public double[:] _wettedperimeters_ncarray
    cdef public double[:] wettedperimeterderivatives
    cdef public numpy.int64_t _wettedperimeterderivatives_ndim
    cdef public numpy.int64_t _wettedperimeterderivatives_length
    cdef public numpy.int64_t _wettedperimeterderivatives_length_0
    cdef public bint _wettedperimeterderivatives_ramflag
    cdef public double[:,:] _wettedperimeterderivatives_array
    cdef public bint _wettedperimeterderivatives_diskflag_reading
    cdef public bint _wettedperimeterderivatives_diskflag_writing
    cdef public double[:] _wettedperimeterderivatives_ncarray
    cdef public double[:] surfacewidths
    cdef public numpy.int64_t _surfacewidths_ndim
    cdef public numpy.int64_t _surfacewidths_length
    cdef public numpy.int64_t _surfacewidths_length_0
    cdef public bint _surfacewidths_ramflag
    cdef public double[:,:] _surfacewidths_array
    cdef public bint _surfacewidths_diskflag_reading
    cdef public bint _surfacewidths_diskflag_writing
    cdef public double[:] _surfacewidths_ncarray
    cdef public double surfacewidth
    cdef public numpy.int64_t _surfacewidth_ndim
    cdef public numpy.int64_t _surfacewidth_length
    cdef public bint _surfacewidth_ramflag
    cdef public double[:] _surfacewidth_array
    cdef public bint _surfacewidth_diskflag_reading
    cdef public bint _surfacewidth_diskflag_writing
    cdef public double[:] _surfacewidth_ncarray
    cdef public bint _surfacewidth_outputflag
    cdef double *_surfacewidth_outputpointer
    cdef public double[:] dischargederivatives
    cdef public numpy.int64_t _dischargederivatives_ndim
    cdef public numpy.int64_t _dischargederivatives_length
    cdef public numpy.int64_t _dischargederivatives_length_0
    cdef public bint _dischargederivatives_ramflag
    cdef public double[:,:] _dischargederivatives_array
    cdef public bint _dischargederivatives_diskflag_reading
    cdef public bint _dischargederivatives_diskflag_writing
    cdef public double[:] _dischargederivatives_ncarray
    cdef public double dischargederivative
    cdef public numpy.int64_t _dischargederivative_ndim
    cdef public numpy.int64_t _dischargederivative_length
    cdef public bint _dischargederivative_ramflag
    cdef public double[:] _dischargederivative_array
    cdef public bint _dischargederivative_diskflag_reading
    cdef public bint _dischargederivative_diskflag_writing
    cdef public double[:] _dischargederivative_ncarray
    cdef public bint _dischargederivative_outputflag
    cdef double *_dischargederivative_outputpointer
    cdef public double celerity
    cdef public numpy.int64_t _celerity_ndim
    cdef public numpy.int64_t _celerity_length
    cdef public bint _celerity_ramflag
    cdef public double[:] _celerity_array
    cdef public bint _celerity_diskflag_reading
    cdef public bint _celerity_diskflag_writing
    cdef public double[:] _celerity_ncarray
    cdef public bint _celerity_outputflag
    cdef double *_celerity_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double[:] discharges
    cdef public numpy.int64_t _discharges_ndim
    cdef public numpy.int64_t _discharges_length
    cdef public numpy.int64_t _discharges_length_0
    cdef public bint _discharges_ramflag
    cdef public double[:,:] _discharges_array
    cdef public bint _discharges_diskflag_reading
    cdef public bint _discharges_diskflag_writing
    cdef public double[:] _discharges_ncarray
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
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef double get_wettedarea_v1(self) noexcept nogil
    cpdef double get_surfacewidth_v1(self) noexcept nogil
    cpdef double get_discharge_v1(self) noexcept nogil
    cpdef double get_celerity_v1(self) noexcept nogil
    cpdef inline void set_waterdepth_v1(self, double waterdepth) noexcept nogil
    cpdef inline void set_waterlevel_v1(self, double waterlevel) noexcept nogil
    cpdef inline void calc_waterdepth_v1(self) noexcept nogil
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil
    cpdef inline void calc_wettedareas_v1(self) noexcept nogil
    cpdef inline void calc_wettedarea_v1(self) noexcept nogil
    cpdef inline void calc_wettedperimeters_v1(self) noexcept nogil
    cpdef inline void calc_wettedperimeterderivatives_v1(self) noexcept nogil
    cpdef inline void calc_surfacewidths_v1(self) noexcept nogil
    cpdef inline void calc_surfacewidth_v1(self) noexcept nogil
    cpdef inline void calc_discharges_v1(self) noexcept nogil
    cpdef inline void calc_discharge_v2(self) noexcept nogil
    cpdef inline void calc_dischargederivatives_v1(self) noexcept nogil
    cpdef inline void calc_dischargederivative_v1(self) noexcept nogil
    cpdef inline void calc_celerity_v1(self) noexcept nogil
    cpdef double get_wettedarea(self) noexcept nogil
    cpdef double get_surfacewidth(self) noexcept nogil
    cpdef double get_discharge(self) noexcept nogil
    cpdef double get_celerity(self) noexcept nogil
    cpdef inline void set_waterdepth(self, double waterdepth) noexcept nogil
    cpdef inline void set_waterlevel(self, double waterlevel) noexcept nogil
    cpdef inline void calc_waterdepth(self) noexcept nogil
    cpdef inline void calc_waterlevel(self) noexcept nogil
    cpdef inline void calc_wettedareas(self) noexcept nogil
    cpdef inline void calc_wettedarea(self) noexcept nogil
    cpdef inline void calc_wettedperimeters(self) noexcept nogil
    cpdef inline void calc_wettedperimeterderivatives(self) noexcept nogil
    cpdef inline void calc_surfacewidths(self) noexcept nogil
    cpdef inline void calc_surfacewidth(self) noexcept nogil
    cpdef inline void calc_discharges(self) noexcept nogil
    cpdef inline void calc_discharge(self) noexcept nogil
    cpdef inline void calc_dischargederivatives(self) noexcept nogil
    cpdef inline void calc_dischargederivative(self) noexcept nogil
    cpdef inline void calc_celerity(self) noexcept nogil
    cpdef void use_waterdepth_v1(self, double waterdepth) noexcept nogil
    cpdef void use_waterlevel_v1(self, double waterlevel) noexcept nogil
    cpdef void use_waterdepth(self, double waterdepth) noexcept nogil
    cpdef void use_waterlevel(self, double waterlevel) noexcept nogil
