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
    cdef public numpy.int64_t nmbsoils
    cdef public numpy.int64_t nmbbins
    cdef public double dt
    cdef public numpy.npy_bool[:] sealed
    cdef public double[:] soilarea
    cdef public double[:] soildepth
    cdef public double[:] residualmoisture
    cdef public double[:] saturationmoisture
    cdef public double[:] saturatedconductivity
    cdef public double[:] poresizedistribution
    cdef public double[:] airentrypotential
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t nmbsubsteps
    cdef public double[:] soilareafraction
    cdef public double[:] effectivecapillarysuction
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public AideSequences aides
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
    cdef public double rainfall
    cdef public numpy.int64_t _rainfall_ndim
    cdef public numpy.int64_t _rainfall_length
    cdef public bint _rainfall_ramflag
    cdef public double[:] _rainfall_array
    cdef public bint _rainfall_diskflag_reading
    cdef public bint _rainfall_diskflag_writing
    cdef public double[:] _rainfall_ncarray
    cdef public bint _rainfall_inputflag
    cdef double *_rainfall_inputpointer
    cdef public double capillaryrise
    cdef public numpy.int64_t _capillaryrise_ndim
    cdef public numpy.int64_t _capillaryrise_length
    cdef public bint _capillaryrise_ramflag
    cdef public double[:] _capillaryrise_array
    cdef public bint _capillaryrise_diskflag_reading
    cdef public bint _capillaryrise_diskflag_writing
    cdef public double[:] _capillaryrise_ncarray
    cdef public bint _capillaryrise_inputflag
    cdef double *_capillaryrise_inputpointer
    cdef public double evaporation
    cdef public numpy.int64_t _evaporation_ndim
    cdef public numpy.int64_t _evaporation_length
    cdef public bint _evaporation_ramflag
    cdef public double[:] _evaporation_array
    cdef public bint _evaporation_diskflag_reading
    cdef public bint _evaporation_diskflag_writing
    cdef public double[:] _evaporation_ncarray
    cdef public bint _evaporation_inputflag
    cdef double *_evaporation_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FluxSequences:
    cdef public double[:] surfacewatersupply
    cdef public numpy.int64_t _surfacewatersupply_ndim
    cdef public numpy.int64_t _surfacewatersupply_length
    cdef public numpy.int64_t _surfacewatersupply_length_0
    cdef public bint _surfacewatersupply_ramflag
    cdef public double[:,:] _surfacewatersupply_array
    cdef public bint _surfacewatersupply_diskflag_reading
    cdef public bint _surfacewatersupply_diskflag_writing
    cdef public double[:] _surfacewatersupply_ncarray
    cdef public double[:] soilwatersupply
    cdef public numpy.int64_t _soilwatersupply_ndim
    cdef public numpy.int64_t _soilwatersupply_length
    cdef public numpy.int64_t _soilwatersupply_length_0
    cdef public bint _soilwatersupply_ramflag
    cdef public double[:,:] _soilwatersupply_array
    cdef public bint _soilwatersupply_diskflag_reading
    cdef public bint _soilwatersupply_diskflag_writing
    cdef public double[:] _soilwatersupply_ncarray
    cdef public double[:] demand
    cdef public numpy.int64_t _demand_ndim
    cdef public numpy.int64_t _demand_length
    cdef public numpy.int64_t _demand_length_0
    cdef public bint _demand_ramflag
    cdef public double[:,:] _demand_array
    cdef public bint _demand_diskflag_reading
    cdef public bint _demand_diskflag_writing
    cdef public double[:] _demand_ncarray
    cdef public double[:] infiltration
    cdef public numpy.int64_t _infiltration_ndim
    cdef public numpy.int64_t _infiltration_length
    cdef public numpy.int64_t _infiltration_length_0
    cdef public bint _infiltration_ramflag
    cdef public double[:,:] _infiltration_array
    cdef public bint _infiltration_diskflag_reading
    cdef public bint _infiltration_diskflag_writing
    cdef public double[:] _infiltration_ncarray
    cdef public double[:] percolation
    cdef public numpy.int64_t _percolation_ndim
    cdef public numpy.int64_t _percolation_length
    cdef public numpy.int64_t _percolation_length_0
    cdef public bint _percolation_ramflag
    cdef public double[:,:] _percolation_array
    cdef public bint _percolation_diskflag_reading
    cdef public bint _percolation_diskflag_writing
    cdef public double[:] _percolation_ncarray
    cdef public double[:] soilwateraddition
    cdef public numpy.int64_t _soilwateraddition_ndim
    cdef public numpy.int64_t _soilwateraddition_length
    cdef public numpy.int64_t _soilwateraddition_length_0
    cdef public bint _soilwateraddition_ramflag
    cdef public double[:,:] _soilwateraddition_array
    cdef public bint _soilwateraddition_diskflag_reading
    cdef public bint _soilwateraddition_diskflag_writing
    cdef public double[:] _soilwateraddition_ncarray
    cdef public double[:] withdrawal
    cdef public numpy.int64_t _withdrawal_ndim
    cdef public numpy.int64_t _withdrawal_length
    cdef public numpy.int64_t _withdrawal_length_0
    cdef public bint _withdrawal_ramflag
    cdef public double[:,:] _withdrawal_array
    cdef public bint _withdrawal_diskflag_reading
    cdef public bint _withdrawal_diskflag_writing
    cdef public double[:] _withdrawal_ncarray
    cdef public double[:] surfacerunoff
    cdef public numpy.int64_t _surfacerunoff_ndim
    cdef public numpy.int64_t _surfacerunoff_length
    cdef public numpy.int64_t _surfacerunoff_length_0
    cdef public bint _surfacerunoff_ramflag
    cdef public double[:,:] _surfacerunoff_array
    cdef public bint _surfacerunoff_diskflag_reading
    cdef public bint _surfacerunoff_diskflag_writing
    cdef public double[:] _surfacerunoff_ncarray
    cdef public double totalinfiltration
    cdef public numpy.int64_t _totalinfiltration_ndim
    cdef public numpy.int64_t _totalinfiltration_length
    cdef public bint _totalinfiltration_ramflag
    cdef public double[:] _totalinfiltration_array
    cdef public bint _totalinfiltration_diskflag_reading
    cdef public bint _totalinfiltration_diskflag_writing
    cdef public double[:] _totalinfiltration_ncarray
    cdef public bint _totalinfiltration_outputflag
    cdef double *_totalinfiltration_outputpointer
    cdef public double totalpercolation
    cdef public numpy.int64_t _totalpercolation_ndim
    cdef public numpy.int64_t _totalpercolation_length
    cdef public bint _totalpercolation_ramflag
    cdef public double[:] _totalpercolation_array
    cdef public bint _totalpercolation_diskflag_reading
    cdef public bint _totalpercolation_diskflag_writing
    cdef public double[:] _totalpercolation_ncarray
    cdef public bint _totalpercolation_outputflag
    cdef double *_totalpercolation_outputpointer
    cdef public double totalsoilwateraddition
    cdef public numpy.int64_t _totalsoilwateraddition_ndim
    cdef public numpy.int64_t _totalsoilwateraddition_length
    cdef public bint _totalsoilwateraddition_ramflag
    cdef public double[:] _totalsoilwateraddition_array
    cdef public bint _totalsoilwateraddition_diskflag_reading
    cdef public bint _totalsoilwateraddition_diskflag_writing
    cdef public double[:] _totalsoilwateraddition_ncarray
    cdef public bint _totalsoilwateraddition_outputflag
    cdef double *_totalsoilwateraddition_outputpointer
    cdef public double totalwithdrawal
    cdef public numpy.int64_t _totalwithdrawal_ndim
    cdef public numpy.int64_t _totalwithdrawal_length
    cdef public bint _totalwithdrawal_ramflag
    cdef public double[:] _totalwithdrawal_array
    cdef public bint _totalwithdrawal_diskflag_reading
    cdef public bint _totalwithdrawal_diskflag_writing
    cdef public double[:] _totalwithdrawal_ncarray
    cdef public bint _totalwithdrawal_outputflag
    cdef double *_totalwithdrawal_outputpointer
    cdef public double totalsurfacerunoff
    cdef public numpy.int64_t _totalsurfacerunoff_ndim
    cdef public numpy.int64_t _totalsurfacerunoff_length
    cdef public bint _totalsurfacerunoff_ramflag
    cdef public double[:] _totalsurfacerunoff_array
    cdef public bint _totalsurfacerunoff_diskflag_reading
    cdef public bint _totalsurfacerunoff_diskflag_writing
    cdef public double[:] _totalsurfacerunoff_ncarray
    cdef public bint _totalsurfacerunoff_outputflag
    cdef double *_totalsurfacerunoff_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double[:,:] moisture
    cdef public numpy.int64_t _moisture_ndim
    cdef public numpy.int64_t _moisture_length
    cdef public numpy.int64_t _moisture_length_0
    cdef public numpy.int64_t _moisture_length_1
    cdef public bint _moisture_ramflag
    cdef public double[:,:,:] _moisture_array
    cdef public bint _moisture_diskflag_reading
    cdef public bint _moisture_diskflag_writing
    cdef public double[:] _moisture_ncarray
    cdef public double[:,:] frontdepth
    cdef public numpy.int64_t _frontdepth_ndim
    cdef public numpy.int64_t _frontdepth_length
    cdef public numpy.int64_t _frontdepth_length_0
    cdef public numpy.int64_t _frontdepth_length_1
    cdef public bint _frontdepth_ramflag
    cdef public double[:,:,:] _frontdepth_array
    cdef public bint _frontdepth_diskflag_reading
    cdef public bint _frontdepth_diskflag_writing
    cdef public double[:] _frontdepth_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class LogSequences:
    cdef public double[:,:] moisturechange
    cdef public numpy.int64_t _moisturechange_ndim
    cdef public numpy.int64_t _moisturechange_length
    cdef public numpy.int64_t _moisturechange_length_0
    cdef public numpy.int64_t _moisturechange_length_1
@cython.final
cdef class AideSequences:
    cdef public double[:] initialsurfacewater
    cdef public numpy.int64_t _initialsurfacewater_ndim
    cdef public numpy.int64_t _initialsurfacewater_length
    cdef public numpy.int64_t _initialsurfacewater_length_0
    cdef public double[:] actualsurfacewater
    cdef public numpy.int64_t _actualsurfacewater_ndim
    cdef public numpy.int64_t _actualsurfacewater_length
    cdef public numpy.int64_t _actualsurfacewater_length_0
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
    cpdef void new2old(self) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef void update_inlets(self) noexcept nogil
    cpdef void update_outlets(self) noexcept nogil
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef void update_outputs(self) noexcept nogil
    cpdef inline void calc_surfacewatersupply_v1(self) noexcept nogil
    cpdef inline void calc_soilwatersupply_v1(self) noexcept nogil
    cpdef inline void calc_demand_v1(self) noexcept nogil
    cpdef inline void perform_garto_v1(self) noexcept nogil
    cpdef inline void calc_totalinfiltration_v1(self) noexcept nogil
    cpdef inline void calc_totalpercolation_v1(self) noexcept nogil
    cpdef inline void calc_totalsoilwateraddition_v1(self) noexcept nogil
    cpdef inline void calc_totalwithdrawal_v1(self) noexcept nogil
    cpdef inline void calc_totalsurfacerunoff_v1(self) noexcept nogil
    cpdef void set_initialsurfacewater_v1(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_actualsurfacewater_v1(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_soilwatersupply_v1(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_soilwaterdemand_v1(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void execute_infiltration_v1(self, numpy.int64_t s) noexcept nogil
    cpdef void add_soilwater_v1(self, numpy.int64_t s) noexcept nogil
    cpdef void remove_soilwater_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_infiltration_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_percolation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwateraddition_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwaterremoval_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwatercontent_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline double return_relativemoisture_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline double return_conductivity_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline double return_capillarydrive_v1(self, numpy.int64_t b1, numpy.int64_t b2, numpy.int64_t s) noexcept nogil
    cpdef inline double return_drydepth_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline numpy.int64_t return_lastactivebin_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline void active_bin_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void percolate_filledbin_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline void shift_front_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void redistribute_front_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void infiltrate_wettingfrontbins_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline void merge_frontdepthovershootings_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline void merge_soildepthovershootings_v1(self, numpy.int64_t s) noexcept nogil
    cpdef inline void water_allbins_v1(self, numpy.int64_t s, double supply) noexcept nogil
    cpdef inline void withdraw_allbins_v1(self, numpy.int64_t s, double demand) noexcept nogil
    cpdef inline void calc_surfacewatersupply(self) noexcept nogil
    cpdef inline void calc_soilwatersupply(self) noexcept nogil
    cpdef inline void calc_demand(self) noexcept nogil
    cpdef inline void perform_garto(self) noexcept nogil
    cpdef inline void calc_totalinfiltration(self) noexcept nogil
    cpdef inline void calc_totalpercolation(self) noexcept nogil
    cpdef inline void calc_totalsoilwateraddition(self) noexcept nogil
    cpdef inline void calc_totalwithdrawal(self) noexcept nogil
    cpdef inline void calc_totalsurfacerunoff(self) noexcept nogil
    cpdef void set_initialsurfacewater(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_actualsurfacewater(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_soilwatersupply(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void set_soilwaterdemand(self, numpy.int64_t s, double v) noexcept nogil
    cpdef void execute_infiltration(self, numpy.int64_t s) noexcept nogil
    cpdef void add_soilwater(self, numpy.int64_t s) noexcept nogil
    cpdef void remove_soilwater(self, numpy.int64_t s) noexcept nogil
    cpdef double get_infiltration(self, numpy.int64_t s) noexcept nogil
    cpdef double get_percolation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwateraddition(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwaterremoval(self, numpy.int64_t s) noexcept nogil
    cpdef double get_soilwatercontent(self, numpy.int64_t s) noexcept nogil
    cpdef inline double return_relativemoisture(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline double return_conductivity(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline double return_capillarydrive(self, numpy.int64_t b1, numpy.int64_t b2, numpy.int64_t s) noexcept nogil
    cpdef inline double return_drydepth(self, numpy.int64_t s) noexcept nogil
    cpdef inline numpy.int64_t return_lastactivebin(self, numpy.int64_t s) noexcept nogil
    cpdef inline void active_bin(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void percolate_filledbin(self, numpy.int64_t s) noexcept nogil
    cpdef inline void shift_front(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void redistribute_front(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil
    cpdef inline void infiltrate_wettingfrontbins(self, numpy.int64_t s) noexcept nogil
    cpdef inline void merge_frontdepthovershootings(self, numpy.int64_t s) noexcept nogil
    cpdef inline void merge_soildepthovershootings(self, numpy.int64_t s) noexcept nogil
    cpdef inline void water_allbins(self, numpy.int64_t s, double supply) noexcept nogil
    cpdef inline void withdraw_allbins(self, numpy.int64_t s, double demand) noexcept nogil
