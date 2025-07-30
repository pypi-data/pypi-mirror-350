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
cdef public numpy.int64_t GRASS = 1
cdef public numpy.int64_t DECIDUOUS = 2
cdef public numpy.int64_t CORN = 3
cdef public numpy.int64_t CONIFER = 4
cdef public numpy.int64_t SPRINGWHEAT = 5
cdef public numpy.int64_t WINTERWHEAT = 6
cdef public numpy.int64_t SUGARBEETS = 7
cdef public numpy.int64_t SEALED = 8
cdef public numpy.int64_t WATER = 9
cdef public numpy.int64_t SAND = 10
cdef public numpy.int64_t SAND_COHESIVE = 11
cdef public numpy.int64_t LOAM = 12
cdef public numpy.int64_t CLAY = 13
cdef public numpy.int64_t SILT = 14
cdef public numpy.int64_t PEAT = 15
cdef public numpy.int64_t NONE = 16
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
@cython.final
cdef class ControlParameters:
    cdef public double area
    cdef public numpy.int64_t nmbzones
    cdef public double[:] zonearea
    cdef public numpy.int64_t[:] landtype
    cdef public numpy.int64_t[:] soiltype
    cdef public double[:,:] interceptioncapacity
    cdef public numpy.int64_t _interceptioncapacity_rowmin
    cdef public numpy.int64_t _interceptioncapacity_columnmin
    cdef public double[:] degreedayfactor
    cdef public double[:] availablefieldcapacity
    cdef public double[:] rootingdepth
    cdef public double[:] groundwaterdepth
    cdef public numpy.npy_bool withcapillaryrise
    cdef public double[:] capillarythreshold
    cdef public double[:] capillarylimit
    cdef public double[:,:] irrigationtrigger
    cdef public numpy.int64_t _irrigationtrigger_rowmin
    cdef public numpy.int64_t _irrigationtrigger_columnmin
    cdef public double[:,:] irrigationtarget
    cdef public numpy.int64_t _irrigationtarget_rowmin
    cdef public numpy.int64_t _irrigationtarget_columnmin
    cdef public numpy.npy_bool withexternalirrigation
    cdef public double[:] baseflowindex
    cdef public double rechargedelay
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int64_t[:] moy
    cdef public double[:] zoneratio
    cdef public double[:] soildepth
    cdef public double[:] maxsoilwater
    cdef public double[:] beta
    cdef public double[:] potentialcapillaryrise
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FactorSequences factors
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public StateSequences old_states
    cdef public StateSequences new_states
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
    cdef public double temperature
    cdef public numpy.int64_t _temperature_ndim
    cdef public numpy.int64_t _temperature_length
    cdef public bint _temperature_ramflag
    cdef public double[:] _temperature_array
    cdef public bint _temperature_diskflag_reading
    cdef public bint _temperature_diskflag_writing
    cdef public double[:] _temperature_ncarray
    cdef public bint _temperature_inputflag
    cdef double *_temperature_inputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value)
@cython.final
cdef class FactorSequences:
    cdef public double[:] relativesoilmoisture
    cdef public numpy.int64_t _relativesoilmoisture_ndim
    cdef public numpy.int64_t _relativesoilmoisture_length
    cdef public numpy.int64_t _relativesoilmoisture_length_0
    cdef public bint _relativesoilmoisture_ramflag
    cdef public double[:,:] _relativesoilmoisture_array
    cdef public bint _relativesoilmoisture_diskflag_reading
    cdef public bint _relativesoilmoisture_diskflag_writing
    cdef public double[:] _relativesoilmoisture_ncarray
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class FluxSequences:
    cdef public double[:] interceptionevaporation
    cdef public numpy.int64_t _interceptionevaporation_ndim
    cdef public numpy.int64_t _interceptionevaporation_length
    cdef public numpy.int64_t _interceptionevaporation_length_0
    cdef public bint _interceptionevaporation_ramflag
    cdef public double[:,:] _interceptionevaporation_array
    cdef public bint _interceptionevaporation_diskflag_reading
    cdef public bint _interceptionevaporation_diskflag_writing
    cdef public double[:] _interceptionevaporation_ncarray
    cdef public double[:] throughfall
    cdef public numpy.int64_t _throughfall_ndim
    cdef public numpy.int64_t _throughfall_length
    cdef public numpy.int64_t _throughfall_length_0
    cdef public bint _throughfall_ramflag
    cdef public double[:,:] _throughfall_array
    cdef public bint _throughfall_diskflag_reading
    cdef public bint _throughfall_diskflag_writing
    cdef public double[:] _throughfall_ncarray
    cdef public double[:] potentialsnowmelt
    cdef public numpy.int64_t _potentialsnowmelt_ndim
    cdef public numpy.int64_t _potentialsnowmelt_length
    cdef public numpy.int64_t _potentialsnowmelt_length_0
    cdef public bint _potentialsnowmelt_ramflag
    cdef public double[:,:] _potentialsnowmelt_array
    cdef public bint _potentialsnowmelt_diskflag_reading
    cdef public bint _potentialsnowmelt_diskflag_writing
    cdef public double[:] _potentialsnowmelt_ncarray
    cdef public double[:] snowmelt
    cdef public numpy.int64_t _snowmelt_ndim
    cdef public numpy.int64_t _snowmelt_length
    cdef public numpy.int64_t _snowmelt_length_0
    cdef public bint _snowmelt_ramflag
    cdef public double[:,:] _snowmelt_array
    cdef public bint _snowmelt_diskflag_reading
    cdef public bint _snowmelt_diskflag_writing
    cdef public double[:] _snowmelt_ncarray
    cdef public double[:] ponding
    cdef public numpy.int64_t _ponding_ndim
    cdef public numpy.int64_t _ponding_length
    cdef public numpy.int64_t _ponding_length_0
    cdef public bint _ponding_ramflag
    cdef public double[:,:] _ponding_array
    cdef public bint _ponding_diskflag_reading
    cdef public bint _ponding_diskflag_writing
    cdef public double[:] _ponding_ncarray
    cdef public double[:] surfacerunoff
    cdef public numpy.int64_t _surfacerunoff_ndim
    cdef public numpy.int64_t _surfacerunoff_length
    cdef public numpy.int64_t _surfacerunoff_length_0
    cdef public bint _surfacerunoff_ramflag
    cdef public double[:,:] _surfacerunoff_array
    cdef public bint _surfacerunoff_diskflag_reading
    cdef public bint _surfacerunoff_diskflag_writing
    cdef public double[:] _surfacerunoff_ncarray
    cdef public double[:] percolation
    cdef public numpy.int64_t _percolation_ndim
    cdef public numpy.int64_t _percolation_length
    cdef public numpy.int64_t _percolation_length_0
    cdef public bint _percolation_ramflag
    cdef public double[:,:] _percolation_array
    cdef public bint _percolation_diskflag_reading
    cdef public bint _percolation_diskflag_writing
    cdef public double[:] _percolation_ncarray
    cdef public double[:] soilevapotranspiration
    cdef public numpy.int64_t _soilevapotranspiration_ndim
    cdef public numpy.int64_t _soilevapotranspiration_length
    cdef public numpy.int64_t _soilevapotranspiration_length_0
    cdef public bint _soilevapotranspiration_ramflag
    cdef public double[:,:] _soilevapotranspiration_array
    cdef public bint _soilevapotranspiration_diskflag_reading
    cdef public bint _soilevapotranspiration_diskflag_writing
    cdef public double[:] _soilevapotranspiration_ncarray
    cdef public double[:] lakeevaporation
    cdef public numpy.int64_t _lakeevaporation_ndim
    cdef public numpy.int64_t _lakeevaporation_length
    cdef public numpy.int64_t _lakeevaporation_length_0
    cdef public bint _lakeevaporation_ramflag
    cdef public double[:,:] _lakeevaporation_array
    cdef public bint _lakeevaporation_diskflag_reading
    cdef public bint _lakeevaporation_diskflag_writing
    cdef public double[:] _lakeevaporation_ncarray
    cdef public double[:] totalevapotranspiration
    cdef public numpy.int64_t _totalevapotranspiration_ndim
    cdef public numpy.int64_t _totalevapotranspiration_length
    cdef public numpy.int64_t _totalevapotranspiration_length_0
    cdef public bint _totalevapotranspiration_ramflag
    cdef public double[:,:] _totalevapotranspiration_array
    cdef public bint _totalevapotranspiration_diskflag_reading
    cdef public bint _totalevapotranspiration_diskflag_writing
    cdef public double[:] _totalevapotranspiration_ncarray
    cdef public double[:] capillaryrise
    cdef public numpy.int64_t _capillaryrise_ndim
    cdef public numpy.int64_t _capillaryrise_length
    cdef public numpy.int64_t _capillaryrise_length_0
    cdef public bint _capillaryrise_ramflag
    cdef public double[:,:] _capillaryrise_array
    cdef public bint _capillaryrise_diskflag_reading
    cdef public bint _capillaryrise_diskflag_writing
    cdef public double[:] _capillaryrise_ncarray
    cdef public double[:] requiredirrigation
    cdef public numpy.int64_t _requiredirrigation_ndim
    cdef public numpy.int64_t _requiredirrigation_length
    cdef public numpy.int64_t _requiredirrigation_length_0
    cdef public bint _requiredirrigation_ramflag
    cdef public double[:,:] _requiredirrigation_array
    cdef public bint _requiredirrigation_diskflag_reading
    cdef public bint _requiredirrigation_diskflag_writing
    cdef public double[:] _requiredirrigation_ncarray
    cdef public double[:] externalirrigation
    cdef public numpy.int64_t _externalirrigation_ndim
    cdef public numpy.int64_t _externalirrigation_length
    cdef public numpy.int64_t _externalirrigation_length_0
    cdef public bint _externalirrigation_ramflag
    cdef public double[:,:] _externalirrigation_array
    cdef public bint _externalirrigation_diskflag_reading
    cdef public bint _externalirrigation_diskflag_writing
    cdef public double[:] _externalirrigation_ncarray
    cdef public double[:] potentialrecharge
    cdef public numpy.int64_t _potentialrecharge_ndim
    cdef public numpy.int64_t _potentialrecharge_length
    cdef public numpy.int64_t _potentialrecharge_length_0
    cdef public bint _potentialrecharge_ramflag
    cdef public double[:,:] _potentialrecharge_array
    cdef public bint _potentialrecharge_diskflag_reading
    cdef public bint _potentialrecharge_diskflag_writing
    cdef public double[:] _potentialrecharge_ncarray
    cdef public double[:] baseflow
    cdef public numpy.int64_t _baseflow_ndim
    cdef public numpy.int64_t _baseflow_length
    cdef public numpy.int64_t _baseflow_length_0
    cdef public bint _baseflow_ramflag
    cdef public double[:,:] _baseflow_array
    cdef public bint _baseflow_diskflag_reading
    cdef public bint _baseflow_diskflag_writing
    cdef public double[:] _baseflow_ncarray
    cdef public double actualrecharge
    cdef public numpy.int64_t _actualrecharge_ndim
    cdef public numpy.int64_t _actualrecharge_length
    cdef public bint _actualrecharge_ramflag
    cdef public double[:] _actualrecharge_array
    cdef public bint _actualrecharge_diskflag_reading
    cdef public bint _actualrecharge_diskflag_writing
    cdef public double[:] _actualrecharge_ncarray
    cdef public bint _actualrecharge_outputflag
    cdef double *_actualrecharge_outputpointer
    cdef public double delayedrecharge
    cdef public numpy.int64_t _delayedrecharge_ndim
    cdef public numpy.int64_t _delayedrecharge_length
    cdef public bint _delayedrecharge_ramflag
    cdef public double[:] _delayedrecharge_array
    cdef public bint _delayedrecharge_diskflag_reading
    cdef public bint _delayedrecharge_diskflag_writing
    cdef public double[:] _delayedrecharge_ncarray
    cdef public bint _delayedrecharge_outputflag
    cdef double *_delayedrecharge_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class StateSequences:
    cdef public double[:] interceptedwater
    cdef public numpy.int64_t _interceptedwater_ndim
    cdef public numpy.int64_t _interceptedwater_length
    cdef public numpy.int64_t _interceptedwater_length_0
    cdef public bint _interceptedwater_ramflag
    cdef public double[:,:] _interceptedwater_array
    cdef public bint _interceptedwater_diskflag_reading
    cdef public bint _interceptedwater_diskflag_writing
    cdef public double[:] _interceptedwater_ncarray
    cdef public double[:] snowpack
    cdef public numpy.int64_t _snowpack_ndim
    cdef public numpy.int64_t _snowpack_length
    cdef public numpy.int64_t _snowpack_length_0
    cdef public bint _snowpack_ramflag
    cdef public double[:,:] _snowpack_array
    cdef public bint _snowpack_diskflag_reading
    cdef public bint _snowpack_diskflag_writing
    cdef public double[:] _snowpack_ncarray
    cdef public double[:] soilmoisture
    cdef public numpy.int64_t _soilmoisture_ndim
    cdef public numpy.int64_t _soilmoisture_length
    cdef public numpy.int64_t _soilmoisture_length_0
    cdef public bint _soilmoisture_ramflag
    cdef public double[:,:] _soilmoisture_array
    cdef public bint _soilmoisture_diskflag_reading
    cdef public bint _soilmoisture_diskflag_writing
    cdef public double[:] _soilmoisture_ncarray
    cdef public double deepwater
    cdef public numpy.int64_t _deepwater_ndim
    cdef public numpy.int64_t _deepwater_length
    cdef public bint _deepwater_ramflag
    cdef public double[:] _deepwater_array
    cdef public bint _deepwater_diskflag_reading
    cdef public bint _deepwater_diskflag_writing
    cdef public double[:] _deepwater_ncarray
    cdef public bint _deepwater_outputflag
    cdef double *_deepwater_outputpointer
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value)
    cpdef inline void update_outputs(self) noexcept nogil
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public numpy.npy_bool threading
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public masterinterface.MasterInterface aetmodel
    cdef public numpy.npy_bool aetmodel_is_mainmodel
    cdef public numpy.int64_t aetmodel_typeid
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
    cpdef inline void calc_throughfall_interceptedwater_v1(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation_interceptedwater_v1(self) noexcept nogil
    cpdef inline void calc_lakeevaporation_v1(self) noexcept nogil
    cpdef inline void calc_potentialsnowmelt_v1(self) noexcept nogil
    cpdef inline void calc_snowmelt_snowpack_v1(self) noexcept nogil
    cpdef inline void calc_ponding_v1(self) noexcept nogil
    cpdef inline void calc_surfacerunoff_v1(self) noexcept nogil
    cpdef inline void calc_relativesoilmoisture_v1(self) noexcept nogil
    cpdef inline void calc_percolation_v1(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_totalevapotranspiration_v1(self) noexcept nogil
    cpdef inline void calc_capillaryrise_v1(self) noexcept nogil
    cpdef inline void calc_soilmoisture_v1(self) noexcept nogil
    cpdef inline void calc_requiredirrigation_v1(self) noexcept nogil
    cpdef inline void calc_externalirrigation_soilmoisture_v1(self) noexcept nogil
    cpdef inline void calc_potentialrecharge_v1(self) noexcept nogil
    cpdef inline void calc_baseflow_v1(self) noexcept nogil
    cpdef inline void calc_actualrecharge_v1(self) noexcept nogil
    cpdef inline void calc_delayedrecharge_deepwater_v1(self) noexcept nogil
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature_v1(self) noexcept nogil
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_interceptionevaporation_interceptedwater_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_lakeevaporation_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_throughfall_interceptedwater(self) noexcept nogil
    cpdef inline void calc_interceptionevaporation_interceptedwater(self) noexcept nogil
    cpdef inline void calc_lakeevaporation(self) noexcept nogil
    cpdef inline void calc_potentialsnowmelt(self) noexcept nogil
    cpdef inline void calc_snowmelt_snowpack(self) noexcept nogil
    cpdef inline void calc_ponding(self) noexcept nogil
    cpdef inline void calc_surfacerunoff(self) noexcept nogil
    cpdef inline void calc_relativesoilmoisture(self) noexcept nogil
    cpdef inline void calc_percolation(self) noexcept nogil
    cpdef inline void calc_soilevapotranspiration(self) noexcept nogil
    cpdef inline void calc_totalevapotranspiration(self) noexcept nogil
    cpdef inline void calc_capillaryrise(self) noexcept nogil
    cpdef inline void calc_soilmoisture(self) noexcept nogil
    cpdef inline void calc_requiredirrigation(self) noexcept nogil
    cpdef inline void calc_externalirrigation_soilmoisture(self) noexcept nogil
    cpdef inline void calc_potentialrecharge(self) noexcept nogil
    cpdef inline void calc_baseflow(self) noexcept nogil
    cpdef inline void calc_actualrecharge(self) noexcept nogil
    cpdef inline void calc_delayedrecharge_deepwater(self) noexcept nogil
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil
    cpdef double get_meantemperature(self) noexcept nogil
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil
    cpdef inline void calc_interceptionevaporation_interceptedwater_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_lakeevaporation_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
    cpdef inline void calc_soilevapotranspiration_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil
