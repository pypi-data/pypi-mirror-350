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


cdef void do_nothing(Model model)  noexcept nogil:
    pass

cpdef get_wrapper():
    cdef CallbackWrapper wrapper = CallbackWrapper()
    wrapper.callback = do_nothing
    return wrapper

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
    pass
@cython.final
cdef class ControlParameters:
    pass
@cython.final
cdef class DerivedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_inputflag:
            self.precipitation = self._precipitation_inputpointer[0]
        elif self._precipitation_diskflag_reading:
            self.precipitation = self._precipitation_ncarray[0]
        elif self._precipitation_ramflag:
            self.precipitation = self._precipitation_array[idx]
        if self._temperature_inputflag:
            self.temperature = self._temperature_inputpointer[0]
        elif self._temperature_diskflag_reading:
            self.temperature = self._temperature_ncarray[0]
        elif self._temperature_ramflag:
            self.temperature = self._temperature_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_diskflag_writing:
            self._precipitation_ncarray[0] = self.precipitation
        if self._precipitation_ramflag:
            self._precipitation_array[idx] = self.precipitation
        if self._temperature_diskflag_writing:
            self._temperature_ncarray[0] = self.temperature
        if self._temperature_ramflag:
            self._temperature_array[idx] = self.temperature
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "precipitation":
            self._precipitation_inputpointer = value.p_value
        if name == "temperature":
            self._temperature_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._relativesoilmoisture_diskflag_reading:
            k = 0
            for jdx0 in range(self._relativesoilmoisture_length_0):
                self.relativesoilmoisture[jdx0] = self._relativesoilmoisture_ncarray[k]
                k += 1
        elif self._relativesoilmoisture_ramflag:
            for jdx0 in range(self._relativesoilmoisture_length_0):
                self.relativesoilmoisture[jdx0] = self._relativesoilmoisture_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._relativesoilmoisture_diskflag_writing:
            k = 0
            for jdx0 in range(self._relativesoilmoisture_length_0):
                self._relativesoilmoisture_ncarray[k] = self.relativesoilmoisture[jdx0]
                k += 1
        if self._relativesoilmoisture_ramflag:
            for jdx0 in range(self._relativesoilmoisture_length_0):
                self._relativesoilmoisture_array[idx, jdx0] = self.relativesoilmoisture[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptionevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._interceptionevaporation_length_0):
                self.interceptionevaporation[jdx0] = self._interceptionevaporation_ncarray[k]
                k += 1
        elif self._interceptionevaporation_ramflag:
            for jdx0 in range(self._interceptionevaporation_length_0):
                self.interceptionevaporation[jdx0] = self._interceptionevaporation_array[idx, jdx0]
        if self._throughfall_diskflag_reading:
            k = 0
            for jdx0 in range(self._throughfall_length_0):
                self.throughfall[jdx0] = self._throughfall_ncarray[k]
                k += 1
        elif self._throughfall_ramflag:
            for jdx0 in range(self._throughfall_length_0):
                self.throughfall[jdx0] = self._throughfall_array[idx, jdx0]
        if self._potentialsnowmelt_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialsnowmelt_length_0):
                self.potentialsnowmelt[jdx0] = self._potentialsnowmelt_ncarray[k]
                k += 1
        elif self._potentialsnowmelt_ramflag:
            for jdx0 in range(self._potentialsnowmelt_length_0):
                self.potentialsnowmelt[jdx0] = self._potentialsnowmelt_array[idx, jdx0]
        if self._snowmelt_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowmelt_length_0):
                self.snowmelt[jdx0] = self._snowmelt_ncarray[k]
                k += 1
        elif self._snowmelt_ramflag:
            for jdx0 in range(self._snowmelt_length_0):
                self.snowmelt[jdx0] = self._snowmelt_array[idx, jdx0]
        if self._ponding_diskflag_reading:
            k = 0
            for jdx0 in range(self._ponding_length_0):
                self.ponding[jdx0] = self._ponding_ncarray[k]
                k += 1
        elif self._ponding_ramflag:
            for jdx0 in range(self._ponding_length_0):
                self.ponding[jdx0] = self._ponding_array[idx, jdx0]
        if self._surfacerunoff_diskflag_reading:
            k = 0
            for jdx0 in range(self._surfacerunoff_length_0):
                self.surfacerunoff[jdx0] = self._surfacerunoff_ncarray[k]
                k += 1
        elif self._surfacerunoff_ramflag:
            for jdx0 in range(self._surfacerunoff_length_0):
                self.surfacerunoff[jdx0] = self._surfacerunoff_array[idx, jdx0]
        if self._percolation_diskflag_reading:
            k = 0
            for jdx0 in range(self._percolation_length_0):
                self.percolation[jdx0] = self._percolation_ncarray[k]
                k += 1
        elif self._percolation_ramflag:
            for jdx0 in range(self._percolation_length_0):
                self.percolation[jdx0] = self._percolation_array[idx, jdx0]
        if self._soilevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self.soilevapotranspiration[jdx0] = self._soilevapotranspiration_ncarray[k]
                k += 1
        elif self._soilevapotranspiration_ramflag:
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self.soilevapotranspiration[jdx0] = self._soilevapotranspiration_array[idx, jdx0]
        if self._lakeevaporation_diskflag_reading:
            k = 0
            for jdx0 in range(self._lakeevaporation_length_0):
                self.lakeevaporation[jdx0] = self._lakeevaporation_ncarray[k]
                k += 1
        elif self._lakeevaporation_ramflag:
            for jdx0 in range(self._lakeevaporation_length_0):
                self.lakeevaporation[jdx0] = self._lakeevaporation_array[idx, jdx0]
        if self._totalevapotranspiration_diskflag_reading:
            k = 0
            for jdx0 in range(self._totalevapotranspiration_length_0):
                self.totalevapotranspiration[jdx0] = self._totalevapotranspiration_ncarray[k]
                k += 1
        elif self._totalevapotranspiration_ramflag:
            for jdx0 in range(self._totalevapotranspiration_length_0):
                self.totalevapotranspiration[jdx0] = self._totalevapotranspiration_array[idx, jdx0]
        if self._capillaryrise_diskflag_reading:
            k = 0
            for jdx0 in range(self._capillaryrise_length_0):
                self.capillaryrise[jdx0] = self._capillaryrise_ncarray[k]
                k += 1
        elif self._capillaryrise_ramflag:
            for jdx0 in range(self._capillaryrise_length_0):
                self.capillaryrise[jdx0] = self._capillaryrise_array[idx, jdx0]
        if self._requiredirrigation_diskflag_reading:
            k = 0
            for jdx0 in range(self._requiredirrigation_length_0):
                self.requiredirrigation[jdx0] = self._requiredirrigation_ncarray[k]
                k += 1
        elif self._requiredirrigation_ramflag:
            for jdx0 in range(self._requiredirrigation_length_0):
                self.requiredirrigation[jdx0] = self._requiredirrigation_array[idx, jdx0]
        if self._cisterninflow_diskflag_reading:
            self.cisterninflow = self._cisterninflow_ncarray[0]
        elif self._cisterninflow_ramflag:
            self.cisterninflow = self._cisterninflow_array[idx]
        if self._cisternoverflow_diskflag_reading:
            self.cisternoverflow = self._cisternoverflow_ncarray[0]
        elif self._cisternoverflow_ramflag:
            self.cisternoverflow = self._cisternoverflow_array[idx]
        if self._cisterndemand_diskflag_reading:
            self.cisterndemand = self._cisterndemand_ncarray[0]
        elif self._cisterndemand_ramflag:
            self.cisterndemand = self._cisterndemand_array[idx]
        if self._cisternextraction_diskflag_reading:
            self.cisternextraction = self._cisternextraction_ncarray[0]
        elif self._cisternextraction_ramflag:
            self.cisternextraction = self._cisternextraction_array[idx]
        if self._internalirrigation_diskflag_reading:
            k = 0
            for jdx0 in range(self._internalirrigation_length_0):
                self.internalirrigation[jdx0] = self._internalirrigation_ncarray[k]
                k += 1
        elif self._internalirrigation_ramflag:
            for jdx0 in range(self._internalirrigation_length_0):
                self.internalirrigation[jdx0] = self._internalirrigation_array[idx, jdx0]
        if self._externalirrigation_diskflag_reading:
            k = 0
            for jdx0 in range(self._externalirrigation_length_0):
                self.externalirrigation[jdx0] = self._externalirrigation_ncarray[k]
                k += 1
        elif self._externalirrigation_ramflag:
            for jdx0 in range(self._externalirrigation_length_0):
                self.externalirrigation[jdx0] = self._externalirrigation_array[idx, jdx0]
        if self._potentialrecharge_diskflag_reading:
            k = 0
            for jdx0 in range(self._potentialrecharge_length_0):
                self.potentialrecharge[jdx0] = self._potentialrecharge_ncarray[k]
                k += 1
        elif self._potentialrecharge_ramflag:
            for jdx0 in range(self._potentialrecharge_length_0):
                self.potentialrecharge[jdx0] = self._potentialrecharge_array[idx, jdx0]
        if self._baseflow_diskflag_reading:
            k = 0
            for jdx0 in range(self._baseflow_length_0):
                self.baseflow[jdx0] = self._baseflow_ncarray[k]
                k += 1
        elif self._baseflow_ramflag:
            for jdx0 in range(self._baseflow_length_0):
                self.baseflow[jdx0] = self._baseflow_array[idx, jdx0]
        if self._actualrecharge_diskflag_reading:
            self.actualrecharge = self._actualrecharge_ncarray[0]
        elif self._actualrecharge_ramflag:
            self.actualrecharge = self._actualrecharge_array[idx]
        if self._delayedrecharge_diskflag_reading:
            self.delayedrecharge = self._delayedrecharge_ncarray[0]
        elif self._delayedrecharge_ramflag:
            self.delayedrecharge = self._delayedrecharge_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptionevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._interceptionevaporation_length_0):
                self._interceptionevaporation_ncarray[k] = self.interceptionevaporation[jdx0]
                k += 1
        if self._interceptionevaporation_ramflag:
            for jdx0 in range(self._interceptionevaporation_length_0):
                self._interceptionevaporation_array[idx, jdx0] = self.interceptionevaporation[jdx0]
        if self._throughfall_diskflag_writing:
            k = 0
            for jdx0 in range(self._throughfall_length_0):
                self._throughfall_ncarray[k] = self.throughfall[jdx0]
                k += 1
        if self._throughfall_ramflag:
            for jdx0 in range(self._throughfall_length_0):
                self._throughfall_array[idx, jdx0] = self.throughfall[jdx0]
        if self._potentialsnowmelt_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialsnowmelt_length_0):
                self._potentialsnowmelt_ncarray[k] = self.potentialsnowmelt[jdx0]
                k += 1
        if self._potentialsnowmelt_ramflag:
            for jdx0 in range(self._potentialsnowmelt_length_0):
                self._potentialsnowmelt_array[idx, jdx0] = self.potentialsnowmelt[jdx0]
        if self._snowmelt_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowmelt_length_0):
                self._snowmelt_ncarray[k] = self.snowmelt[jdx0]
                k += 1
        if self._snowmelt_ramflag:
            for jdx0 in range(self._snowmelt_length_0):
                self._snowmelt_array[idx, jdx0] = self.snowmelt[jdx0]
        if self._ponding_diskflag_writing:
            k = 0
            for jdx0 in range(self._ponding_length_0):
                self._ponding_ncarray[k] = self.ponding[jdx0]
                k += 1
        if self._ponding_ramflag:
            for jdx0 in range(self._ponding_length_0):
                self._ponding_array[idx, jdx0] = self.ponding[jdx0]
        if self._surfacerunoff_diskflag_writing:
            k = 0
            for jdx0 in range(self._surfacerunoff_length_0):
                self._surfacerunoff_ncarray[k] = self.surfacerunoff[jdx0]
                k += 1
        if self._surfacerunoff_ramflag:
            for jdx0 in range(self._surfacerunoff_length_0):
                self._surfacerunoff_array[idx, jdx0] = self.surfacerunoff[jdx0]
        if self._percolation_diskflag_writing:
            k = 0
            for jdx0 in range(self._percolation_length_0):
                self._percolation_ncarray[k] = self.percolation[jdx0]
                k += 1
        if self._percolation_ramflag:
            for jdx0 in range(self._percolation_length_0):
                self._percolation_array[idx, jdx0] = self.percolation[jdx0]
        if self._soilevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self._soilevapotranspiration_ncarray[k] = self.soilevapotranspiration[jdx0]
                k += 1
        if self._soilevapotranspiration_ramflag:
            for jdx0 in range(self._soilevapotranspiration_length_0):
                self._soilevapotranspiration_array[idx, jdx0] = self.soilevapotranspiration[jdx0]
        if self._lakeevaporation_diskflag_writing:
            k = 0
            for jdx0 in range(self._lakeevaporation_length_0):
                self._lakeevaporation_ncarray[k] = self.lakeevaporation[jdx0]
                k += 1
        if self._lakeevaporation_ramflag:
            for jdx0 in range(self._lakeevaporation_length_0):
                self._lakeevaporation_array[idx, jdx0] = self.lakeevaporation[jdx0]
        if self._totalevapotranspiration_diskflag_writing:
            k = 0
            for jdx0 in range(self._totalevapotranspiration_length_0):
                self._totalevapotranspiration_ncarray[k] = self.totalevapotranspiration[jdx0]
                k += 1
        if self._totalevapotranspiration_ramflag:
            for jdx0 in range(self._totalevapotranspiration_length_0):
                self._totalevapotranspiration_array[idx, jdx0] = self.totalevapotranspiration[jdx0]
        if self._capillaryrise_diskflag_writing:
            k = 0
            for jdx0 in range(self._capillaryrise_length_0):
                self._capillaryrise_ncarray[k] = self.capillaryrise[jdx0]
                k += 1
        if self._capillaryrise_ramflag:
            for jdx0 in range(self._capillaryrise_length_0):
                self._capillaryrise_array[idx, jdx0] = self.capillaryrise[jdx0]
        if self._requiredirrigation_diskflag_writing:
            k = 0
            for jdx0 in range(self._requiredirrigation_length_0):
                self._requiredirrigation_ncarray[k] = self.requiredirrigation[jdx0]
                k += 1
        if self._requiredirrigation_ramflag:
            for jdx0 in range(self._requiredirrigation_length_0):
                self._requiredirrigation_array[idx, jdx0] = self.requiredirrigation[jdx0]
        if self._cisterninflow_diskflag_writing:
            self._cisterninflow_ncarray[0] = self.cisterninflow
        if self._cisterninflow_ramflag:
            self._cisterninflow_array[idx] = self.cisterninflow
        if self._cisternoverflow_diskflag_writing:
            self._cisternoverflow_ncarray[0] = self.cisternoverflow
        if self._cisternoverflow_ramflag:
            self._cisternoverflow_array[idx] = self.cisternoverflow
        if self._cisterndemand_diskflag_writing:
            self._cisterndemand_ncarray[0] = self.cisterndemand
        if self._cisterndemand_ramflag:
            self._cisterndemand_array[idx] = self.cisterndemand
        if self._cisternextraction_diskflag_writing:
            self._cisternextraction_ncarray[0] = self.cisternextraction
        if self._cisternextraction_ramflag:
            self._cisternextraction_array[idx] = self.cisternextraction
        if self._internalirrigation_diskflag_writing:
            k = 0
            for jdx0 in range(self._internalirrigation_length_0):
                self._internalirrigation_ncarray[k] = self.internalirrigation[jdx0]
                k += 1
        if self._internalirrigation_ramflag:
            for jdx0 in range(self._internalirrigation_length_0):
                self._internalirrigation_array[idx, jdx0] = self.internalirrigation[jdx0]
        if self._externalirrigation_diskflag_writing:
            k = 0
            for jdx0 in range(self._externalirrigation_length_0):
                self._externalirrigation_ncarray[k] = self.externalirrigation[jdx0]
                k += 1
        if self._externalirrigation_ramflag:
            for jdx0 in range(self._externalirrigation_length_0):
                self._externalirrigation_array[idx, jdx0] = self.externalirrigation[jdx0]
        if self._potentialrecharge_diskflag_writing:
            k = 0
            for jdx0 in range(self._potentialrecharge_length_0):
                self._potentialrecharge_ncarray[k] = self.potentialrecharge[jdx0]
                k += 1
        if self._potentialrecharge_ramflag:
            for jdx0 in range(self._potentialrecharge_length_0):
                self._potentialrecharge_array[idx, jdx0] = self.potentialrecharge[jdx0]
        if self._baseflow_diskflag_writing:
            k = 0
            for jdx0 in range(self._baseflow_length_0):
                self._baseflow_ncarray[k] = self.baseflow[jdx0]
                k += 1
        if self._baseflow_ramflag:
            for jdx0 in range(self._baseflow_length_0):
                self._baseflow_array[idx, jdx0] = self.baseflow[jdx0]
        if self._actualrecharge_diskflag_writing:
            self._actualrecharge_ncarray[0] = self.actualrecharge
        if self._actualrecharge_ramflag:
            self._actualrecharge_array[idx] = self.actualrecharge
        if self._delayedrecharge_diskflag_writing:
            self._delayedrecharge_ncarray[0] = self.delayedrecharge
        if self._delayedrecharge_ramflag:
            self._delayedrecharge_array[idx] = self.delayedrecharge
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "cisterninflow":
            self._cisterninflow_outputpointer = value.p_value
        if name == "cisternoverflow":
            self._cisternoverflow_outputpointer = value.p_value
        if name == "cisterndemand":
            self._cisterndemand_outputpointer = value.p_value
        if name == "cisternextraction":
            self._cisternextraction_outputpointer = value.p_value
        if name == "actualrecharge":
            self._actualrecharge_outputpointer = value.p_value
        if name == "delayedrecharge":
            self._delayedrecharge_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._cisterninflow_outputflag:
            self._cisterninflow_outputpointer[0] = self.cisterninflow
        if self._cisternoverflow_outputflag:
            self._cisternoverflow_outputpointer[0] = self.cisternoverflow
        if self._cisterndemand_outputflag:
            self._cisterndemand_outputpointer[0] = self.cisterndemand
        if self._cisternextraction_outputflag:
            self._cisternextraction_outputpointer[0] = self.cisternextraction
        if self._actualrecharge_outputflag:
            self._actualrecharge_outputpointer[0] = self.actualrecharge
        if self._delayedrecharge_outputflag:
            self._delayedrecharge_outputpointer[0] = self.delayedrecharge
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptedwater_diskflag_reading:
            k = 0
            for jdx0 in range(self._interceptedwater_length_0):
                self.interceptedwater[jdx0] = self._interceptedwater_ncarray[k]
                k += 1
        elif self._interceptedwater_ramflag:
            for jdx0 in range(self._interceptedwater_length_0):
                self.interceptedwater[jdx0] = self._interceptedwater_array[idx, jdx0]
        if self._snowpack_diskflag_reading:
            k = 0
            for jdx0 in range(self._snowpack_length_0):
                self.snowpack[jdx0] = self._snowpack_ncarray[k]
                k += 1
        elif self._snowpack_ramflag:
            for jdx0 in range(self._snowpack_length_0):
                self.snowpack[jdx0] = self._snowpack_array[idx, jdx0]
        if self._soilmoisture_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilmoisture_length_0):
                self.soilmoisture[jdx0] = self._soilmoisture_ncarray[k]
                k += 1
        elif self._soilmoisture_ramflag:
            for jdx0 in range(self._soilmoisture_length_0):
                self.soilmoisture[jdx0] = self._soilmoisture_array[idx, jdx0]
        if self._cisternwater_diskflag_reading:
            self.cisternwater = self._cisternwater_ncarray[0]
        elif self._cisternwater_ramflag:
            self.cisternwater = self._cisternwater_array[idx]
        if self._deepwater_diskflag_reading:
            self.deepwater = self._deepwater_ncarray[0]
        elif self._deepwater_ramflag:
            self.deepwater = self._deepwater_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._interceptedwater_diskflag_writing:
            k = 0
            for jdx0 in range(self._interceptedwater_length_0):
                self._interceptedwater_ncarray[k] = self.interceptedwater[jdx0]
                k += 1
        if self._interceptedwater_ramflag:
            for jdx0 in range(self._interceptedwater_length_0):
                self._interceptedwater_array[idx, jdx0] = self.interceptedwater[jdx0]
        if self._snowpack_diskflag_writing:
            k = 0
            for jdx0 in range(self._snowpack_length_0):
                self._snowpack_ncarray[k] = self.snowpack[jdx0]
                k += 1
        if self._snowpack_ramflag:
            for jdx0 in range(self._snowpack_length_0):
                self._snowpack_array[idx, jdx0] = self.snowpack[jdx0]
        if self._soilmoisture_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilmoisture_length_0):
                self._soilmoisture_ncarray[k] = self.soilmoisture[jdx0]
                k += 1
        if self._soilmoisture_ramflag:
            for jdx0 in range(self._soilmoisture_length_0):
                self._soilmoisture_array[idx, jdx0] = self.soilmoisture[jdx0]
        if self._cisternwater_diskflag_writing:
            self._cisternwater_ncarray[0] = self.cisternwater
        if self._cisternwater_ramflag:
            self._cisternwater_array[idx] = self.cisternwater
        if self._deepwater_diskflag_writing:
            self._deepwater_ncarray[0] = self.deepwater
        if self._deepwater_ramflag:
            self._deepwater_array[idx] = self.deepwater
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "cisternwater":
            self._cisternwater_outputpointer = value.p_value
        if name == "deepwater":
            self._deepwater_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._cisternwater_outputflag:
            self._cisternwater_outputpointer[0] = self.cisternwater
        if self._deepwater_outputflag:
            self._deepwater_outputpointer[0] = self.deepwater
@cython.final
cdef class Model:
    def __init__(self):
        super().__init__()
        self.aetmodel = None
        self.aetmodel_is_mainmodel = False
    def get_aetmodel(self) -> masterinterface.MasterInterface | None:
        return self.aetmodel
    def set_aetmodel(self, aetmodel: masterinterface.MasterInterface | None) -> None:
        self.aetmodel = aetmodel
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.reset_reuseflags()
        self.load_data(idx)
        self.update_inlets()
        self.run()
        self.new2old()
        self.update_outlets()
        self.update_outputs()
    cpdef void simulate_period(self, numpy.int64_t i0, numpy.int64_t i1)  noexcept nogil:
        cdef numpy.int64_t i
        with nogil:
            for i in range(i0, i1):
                self.simulate(i)
                self.update_senders(i)
                self.update_receivers(i)
                self.save_data(i)
    cpdef void reset_reuseflags(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._interceptedwater_length_0):
            self.sequences.old_states.interceptedwater[jdx0] = self.sequences.new_states.interceptedwater[jdx0]
        for jdx0 in range(self.sequences.states._snowpack_length_0):
            self.sequences.old_states.snowpack[jdx0] = self.sequences.new_states.snowpack[jdx0]
        for jdx0 in range(self.sequences.states._soilmoisture_length_0):
            self.sequences.old_states.soilmoisture[jdx0] = self.sequences.new_states.soilmoisture[jdx0]
        self.sequences.old_states.cisternwater = self.sequences.new_states.cisternwater
        self.sequences.old_states.deepwater = self.sequences.new_states.deepwater
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.calc_throughfall_interceptedwater_v1()
        self.calc_interceptionevaporation_interceptedwater_v1()
        self.calc_lakeevaporation_v1()
        self.calc_potentialsnowmelt_v1()
        self.calc_snowmelt_snowpack_v1()
        self.calc_ponding_v1()
        self.calc_surfacerunoff_v1()
        self.calc_relativesoilmoisture_v1()
        self.calc_percolation_v1()
        self.calc_cisterninflow_v1()
        self.calc_cisternoverflow_cisternwater_v1()
        self.calc_soilevapotranspiration_v1()
        self.calc_totalevapotranspiration_v1()
        self.calc_capillaryrise_v1()
        self.calc_capillaryrise_v2()
        self.calc_soilmoisture_v1()
        self.calc_relativesoilmoisture_v1()
        self.calc_requiredirrigation_v1()
        self.calc_cisterndemand_v1()
        self.calc_cisternextraction_cisternwater_v1()
        self.calc_internalirrigation_soilmoisture_v1()
        self.calc_externalirrigation_soilmoisture_v1()
        self.calc_externalirrigation_soilmoisture_v2()
        self.calc_relativesoilmoisture_v1()
        self.calc_potentialrecharge_v1()
        self.calc_potentialrecharge_v2()
        self.calc_baseflow_v1()
        self.calc_actualrecharge_v1()
        self.calc_delayedrecharge_deepwater_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outputs()
    cpdef inline void calc_throughfall_interceptedwater_v1(self) noexcept nogil:
        cdef double ic
        cdef numpy.int64_t k
        cdef numpy.int64_t month
        month = self.parameters.derived.moy[self.idx_sim]
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.states.interceptedwater[k] = 0.0
                self.sequences.fluxes.throughfall[k] = 0.0
            else:
                ic = self.parameters.control.interceptioncapacity[self.parameters.control.landtype[k] - 1, month]
                self.sequences.fluxes.throughfall[k] = max(                    self.sequences.inputs.precipitation + self.sequences.states.interceptedwater[k] - ic, 0.0                )
                self.sequences.states.interceptedwater[k] = self.sequences.states.interceptedwater[k] + (self.sequences.inputs.precipitation - self.sequences.fluxes.throughfall[k])
    cpdef inline void calc_interceptionevaporation_interceptedwater_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_interceptionevaporation_interceptedwater_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_lakeevaporation_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_lakeevaporation_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_potentialsnowmelt_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.landtype[k] == WATER) or (self.sequences.inputs.temperature <= 0.0):
                self.sequences.fluxes.potentialsnowmelt[k] = 0.0
            else:
                self.sequences.fluxes.potentialsnowmelt[k] = self.parameters.control.degreedayfactor[k] * self.sequences.inputs.temperature
    cpdef inline void calc_snowmelt_snowpack_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.snowmelt[k] = 0.0
                self.sequences.states.snowpack[k] = 0.0
            elif self.sequences.inputs.temperature <= 0.0:
                self.sequences.fluxes.snowmelt[k] = 0.0
                self.sequences.states.snowpack[k] = self.sequences.states.snowpack[k] + (self.sequences.fluxes.throughfall[k])
            elif self.sequences.fluxes.potentialsnowmelt[k] < self.sequences.states.snowpack[k]:
                self.sequences.fluxes.snowmelt[k] = self.sequences.fluxes.potentialsnowmelt[k]
                self.sequences.states.snowpack[k] = self.sequences.states.snowpack[k] - (self.sequences.fluxes.snowmelt[k])
            else:
                self.sequences.fluxes.snowmelt[k] = self.sequences.states.snowpack[k]
                self.sequences.states.snowpack[k] = 0.0
    cpdef inline void calc_ponding_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.landtype[k] == WATER) or (self.sequences.inputs.temperature <= 0.0):
                self.sequences.fluxes.ponding[k] = 0.0
            else:
                self.sequences.fluxes.ponding[k] = self.sequences.fluxes.throughfall[k] + self.sequences.fluxes.snowmelt[k]
    cpdef inline void calc_surfacerunoff_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == SEALED:
                self.sequences.fluxes.surfacerunoff[k] = self.sequences.fluxes.ponding[k]
            else:
                self.sequences.fluxes.surfacerunoff[k] = 0.0
    cpdef inline void calc_relativesoilmoisture_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.soiltype[k] == NONE) or (self.parameters.derived.maxsoilwater[k] <= 0.0):
                self.sequences.factors.relativesoilmoisture[k] = 0.0
            else:
                self.sequences.factors.relativesoilmoisture[k] = self.sequences.states.soilmoisture[k] / self.parameters.derived.maxsoilwater[k]
    cpdef inline void calc_percolation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.fluxes.percolation[k] = 0.0
            else:
                self.sequences.fluxes.percolation[k] = (                    self.sequences.fluxes.ponding[k] * self.sequences.factors.relativesoilmoisture[k] ** self.parameters.derived.beta[k]                )
    cpdef inline void calc_cisterninflow_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.cisterninflow = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.cisternsource[k]:
                if self.parameters.control.landtype[k] == SEALED:
                    self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow + (self.parameters.control.zonearea[k] * self.sequences.fluxes.surfacerunoff[k])
                elif self.parameters.control.landtype[k] != WATER:
                    self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow + (self.parameters.control.zonearea[k] * self.sequences.fluxes.percolation[k])
        self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow / (1000.0)
    cpdef inline void calc_cisternoverflow_cisternwater_v1(self) noexcept nogil:
        self.sequences.states.cisternwater = self.sequences.states.cisternwater + (self.sequences.fluxes.cisterninflow)
        if self.sequences.states.cisternwater <= self.parameters.control.cisterncapacity:
            self.sequences.fluxes.cisternoverflow = 0.0
        else:
            self.sequences.fluxes.cisternoverflow = self.sequences.states.cisternwater - self.parameters.control.cisterncapacity
            self.sequences.states.cisternwater = self.parameters.control.cisterncapacity
    cpdef inline void calc_soilevapotranspiration_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_soilevapotranspiration_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_totalevapotranspiration_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.lakeevaporation[k]
            else:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.interceptionevaporation[k]
            if self.parameters.control.soiltype[k] != NONE:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.totalevapotranspiration[k] + (self.sequences.fluxes.soilevapotranspiration[k])
    cpdef inline void calc_capillaryrise_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.soiltype[k] == NONE) or not self.parameters.control.withcapillaryrise:
                self.sequences.fluxes.capillaryrise[k] = 0.0
            else:
                self.sequences.fluxes.capillaryrise[k] = (                    self.parameters.derived.potentialcapillaryrise[k]                    * (1.0 - self.sequences.factors.relativesoilmoisture[k]) ** 3                )
    cpdef inline void calc_capillaryrise_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (                (self.parameters.control.soiltype[k] == NONE)                or self.parameters.control.cisternsource[k]                or not self.parameters.control.withcapillaryrise            ):
                self.sequences.fluxes.capillaryrise[k] = 0.0
            else:
                self.sequences.fluxes.capillaryrise[k] = (                    self.parameters.derived.potentialcapillaryrise[k]                    * (1.0 - self.sequences.factors.relativesoilmoisture[k]) ** 3                )
    cpdef inline void calc_soilmoisture_v1(self) noexcept nogil:
        cdef double delta
        cdef double factor
        cdef double decrease
        cdef double increase
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.new_states.soilmoisture[k] = 0.0
                self.sequences.fluxes.percolation[k] = 0.0
                self.sequences.fluxes.capillaryrise[k] = 0.0
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
            else:
                increase = self.sequences.fluxes.ponding[k] + self.sequences.fluxes.capillaryrise[k]
                decrease = self.sequences.fluxes.percolation[k]
                if self.sequences.fluxes.soilevapotranspiration[k] < 0.0:
                    increase = increase - (self.sequences.fluxes.soilevapotranspiration[k])
                else:
                    decrease = decrease + (self.sequences.fluxes.soilevapotranspiration[k])
                self.sequences.new_states.soilmoisture[k] = self.sequences.old_states.soilmoisture[k] + increase - decrease
                if self.sequences.new_states.soilmoisture[k] < 0.0:
                    factor = (self.sequences.old_states.soilmoisture[k] + increase) / decrease
                    self.sequences.fluxes.percolation[k] = self.sequences.fluxes.percolation[k] * (factor)
                    if self.sequences.fluxes.soilevapotranspiration[k] >= 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * (factor)
                    self.sequences.new_states.soilmoisture[k] = 0.0
                elif self.sequences.new_states.soilmoisture[k] > self.parameters.derived.maxsoilwater[k]:
                    delta = self.sequences.new_states.soilmoisture[k] - self.parameters.derived.maxsoilwater[k]
                    if self.sequences.fluxes.capillaryrise[k] >= delta:
                        self.sequences.fluxes.capillaryrise[k] = self.sequences.fluxes.capillaryrise[k] - (delta)
                        self.sequences.new_states.soilmoisture[k] = self.parameters.derived.maxsoilwater[k]
                    else:
                        self.sequences.new_states.soilmoisture[k] = self.sequences.new_states.soilmoisture[k] - (self.sequences.fluxes.capillaryrise[k])
                        self.sequences.fluxes.capillaryrise[k] = 0.0
                        self.sequences.fluxes.percolation[k] = self.sequences.fluxes.percolation[k] + (self.sequences.new_states.soilmoisture[k] - self.parameters.derived.maxsoilwater[k])
                        self.sequences.new_states.soilmoisture[k] = self.parameters.derived.maxsoilwater[k]
    cpdef inline void calc_requiredirrigation_v1(self) noexcept nogil:
        cdef double sm
        cdef numpy.int64_t l
        cdef numpy.int64_t k
        cdef numpy.int64_t m
        m = self.parameters.derived.moy[self.idx_sim]
        for k in range(self.parameters.control.nmbzones):
            l = self.parameters.control.landtype[k] - 1
            sm = self.sequences.factors.relativesoilmoisture[k]
            if (self.parameters.control.soiltype[k] == NONE) or (sm >= self.parameters.control.irrigationtrigger[l, m]):
                self.sequences.fluxes.requiredirrigation[k] = 0.0
            else:
                self.sequences.fluxes.requiredirrigation[k] = self.parameters.derived.maxsoilwater[k] * (                    self.parameters.control.irrigationtarget[l, m] - sm                )
    cpdef inline void calc_cisterndemand_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.cisterndemand = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] != NONE:
                self.sequences.fluxes.cisterndemand = self.sequences.fluxes.cisterndemand + (self.parameters.control.zonearea[k] * self.sequences.fluxes.requiredirrigation[k])
        self.sequences.fluxes.cisterndemand = self.sequences.fluxes.cisterndemand / (1000.0)
    cpdef inline void calc_cisternextraction_cisternwater_v1(self) noexcept nogil:
        if self.sequences.states.cisternwater > self.sequences.fluxes.cisterndemand:
            self.sequences.fluxes.cisternextraction = self.sequences.fluxes.cisterndemand
            self.sequences.states.cisternwater = self.sequences.states.cisternwater - (self.sequences.fluxes.cisternextraction)
        else:
            self.sequences.fluxes.cisternextraction = self.sequences.states.cisternwater
            self.sequences.states.cisternwater = 0.0
    cpdef inline void calc_internalirrigation_soilmoisture_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double factor
        if self.sequences.fluxes.cisterndemand > 0.0:
            factor = self.sequences.fluxes.cisternextraction / self.sequences.fluxes.cisterndemand
        else:
            factor = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.states.soilmoisture[k] = 0.0
                self.sequences.fluxes.internalirrigation[k] = 0.0
            else:
                self.sequences.fluxes.internalirrigation[k] = factor * self.sequences.fluxes.requiredirrigation[k]
                self.sequences.states.soilmoisture[k] = self.sequences.states.soilmoisture[k] + (self.sequences.fluxes.internalirrigation[k])
    cpdef inline void calc_externalirrigation_soilmoisture_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.states.soilmoisture[k] = 0.0
                self.sequences.fluxes.externalirrigation[k] = 0.0
            elif self.parameters.control.withexternalirrigation:
                self.sequences.fluxes.externalirrigation[k] = self.sequences.fluxes.requiredirrigation[k]
                self.sequences.states.soilmoisture[k] = self.sequences.states.soilmoisture[k] + (self.sequences.fluxes.externalirrigation[k])
            else:
                self.sequences.fluxes.externalirrigation[k] = 0.0
    cpdef inline void calc_externalirrigation_soilmoisture_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.states.soilmoisture[k] = 0.0
                self.sequences.fluxes.externalirrigation[k] = 0.0
            elif self.parameters.control.withexternalirrigation:
                self.sequences.fluxes.externalirrigation[k] = (                    self.sequences.fluxes.requiredirrigation[k] - self.sequences.fluxes.internalirrigation[k]                )
                self.sequences.states.soilmoisture[k] = self.sequences.states.soilmoisture[k] + (self.sequences.fluxes.externalirrigation[k])
            else:
                self.sequences.fluxes.externalirrigation[k] = 0.0
    cpdef inline void calc_potentialrecharge_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == SEALED:
                self.sequences.fluxes.potentialrecharge[k] = 0.0
            elif self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.potentialrecharge[k] = self.sequences.inputs.precipitation - self.sequences.fluxes.lakeevaporation[k]
            else:
                self.sequences.fluxes.potentialrecharge[k] = self.sequences.fluxes.percolation[k] - self.sequences.fluxes.capillaryrise[k]
    cpdef inline void calc_potentialrecharge_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.potentialrecharge[k] = self.sequences.inputs.precipitation - self.sequences.fluxes.lakeevaporation[k]
            elif (self.parameters.control.landtype[k] == SEALED) or self.parameters.control.cisternsource[k]:
                self.sequences.fluxes.potentialrecharge[k] = 0.0
            else:
                self.sequences.fluxes.potentialrecharge[k] = self.sequences.fluxes.percolation[k] - self.sequences.fluxes.capillaryrise[k]
    cpdef inline void calc_baseflow_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == SEALED:
                self.sequences.fluxes.baseflow[k] = 0.0
            else:
                self.sequences.fluxes.baseflow[k] = (1.0 - self.parameters.control.baseflowindex[k]) * max(                    self.sequences.fluxes.potentialrecharge[k], 0.0                )
    cpdef inline void calc_actualrecharge_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.actualrecharge = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] != SEALED:
                self.sequences.fluxes.actualrecharge = self.sequences.fluxes.actualrecharge + (self.parameters.derived.zoneratio[k] * (                    self.sequences.fluxes.potentialrecharge[k] - self.sequences.fluxes.baseflow[k]                ))
    cpdef inline void calc_delayedrecharge_deepwater_v1(self) noexcept nogil:
        if self.parameters.control.rechargedelay > 0.0:
            self.sequences.new_states.deepwater = (self.sequences.fluxes.actualrecharge + self.sequences.old_states.deepwater) * exp(                -1.0 / self.parameters.control.rechargedelay            )
            self.sequences.fluxes.delayedrecharge = self.sequences.fluxes.actualrecharge + self.sequences.old_states.deepwater - self.sequences.new_states.deepwater
        else:
            self.sequences.fluxes.delayedrecharge = self.sequences.old_states.deepwater + self.sequences.fluxes.actualrecharge
            self.sequences.new_states.deepwater = 0.0
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.temperature
    cpdef double get_meantemperature_v1(self) noexcept nogil:
        return self.sequences.inputs.temperature
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.precipitation
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.interceptedwater[k]
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.soilmoisture[k]
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.snowpack[k] > 0.0:
            return 1.0
        return 0.0
    cpdef inline void calc_interceptionevaporation_interceptedwater_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
                self.sequences.states.interceptedwater[k] = 0.0
            else:
                self.sequences.fluxes.interceptionevaporation[k] = min(                    submodel.get_interceptionevaporation(k), self.sequences.states.interceptedwater[k]                )
                self.sequences.states.interceptedwater[k] = self.sequences.states.interceptedwater[k] - (self.sequences.fluxes.interceptionevaporation[k])
    cpdef inline void calc_lakeevaporation_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.lakeevaporation[k] = submodel.get_waterevaporation(k)
            else:
                self.sequences.fluxes.lakeevaporation[k] = 0.0
    cpdef inline void calc_soilevapotranspiration_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = submodel.get_soilevapotranspiration(k)
    cpdef inline void calc_throughfall_interceptedwater(self) noexcept nogil:
        cdef double ic
        cdef numpy.int64_t k
        cdef numpy.int64_t month
        month = self.parameters.derived.moy[self.idx_sim]
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.states.interceptedwater[k] = 0.0
                self.sequences.fluxes.throughfall[k] = 0.0
            else:
                ic = self.parameters.control.interceptioncapacity[self.parameters.control.landtype[k] - 1, month]
                self.sequences.fluxes.throughfall[k] = max(                    self.sequences.inputs.precipitation + self.sequences.states.interceptedwater[k] - ic, 0.0                )
                self.sequences.states.interceptedwater[k] = self.sequences.states.interceptedwater[k] + (self.sequences.inputs.precipitation - self.sequences.fluxes.throughfall[k])
    cpdef inline void calc_interceptionevaporation_interceptedwater(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_interceptionevaporation_interceptedwater_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_lakeevaporation(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_lakeevaporation_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_potentialsnowmelt(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.landtype[k] == WATER) or (self.sequences.inputs.temperature <= 0.0):
                self.sequences.fluxes.potentialsnowmelt[k] = 0.0
            else:
                self.sequences.fluxes.potentialsnowmelt[k] = self.parameters.control.degreedayfactor[k] * self.sequences.inputs.temperature
    cpdef inline void calc_snowmelt_snowpack(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.snowmelt[k] = 0.0
                self.sequences.states.snowpack[k] = 0.0
            elif self.sequences.inputs.temperature <= 0.0:
                self.sequences.fluxes.snowmelt[k] = 0.0
                self.sequences.states.snowpack[k] = self.sequences.states.snowpack[k] + (self.sequences.fluxes.throughfall[k])
            elif self.sequences.fluxes.potentialsnowmelt[k] < self.sequences.states.snowpack[k]:
                self.sequences.fluxes.snowmelt[k] = self.sequences.fluxes.potentialsnowmelt[k]
                self.sequences.states.snowpack[k] = self.sequences.states.snowpack[k] - (self.sequences.fluxes.snowmelt[k])
            else:
                self.sequences.fluxes.snowmelt[k] = self.sequences.states.snowpack[k]
                self.sequences.states.snowpack[k] = 0.0
    cpdef inline void calc_ponding(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.landtype[k] == WATER) or (self.sequences.inputs.temperature <= 0.0):
                self.sequences.fluxes.ponding[k] = 0.0
            else:
                self.sequences.fluxes.ponding[k] = self.sequences.fluxes.throughfall[k] + self.sequences.fluxes.snowmelt[k]
    cpdef inline void calc_surfacerunoff(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == SEALED:
                self.sequences.fluxes.surfacerunoff[k] = self.sequences.fluxes.ponding[k]
            else:
                self.sequences.fluxes.surfacerunoff[k] = 0.0
    cpdef inline void calc_relativesoilmoisture(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.soiltype[k] == NONE) or (self.parameters.derived.maxsoilwater[k] <= 0.0):
                self.sequences.factors.relativesoilmoisture[k] = 0.0
            else:
                self.sequences.factors.relativesoilmoisture[k] = self.sequences.states.soilmoisture[k] / self.parameters.derived.maxsoilwater[k]
    cpdef inline void calc_percolation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.fluxes.percolation[k] = 0.0
            else:
                self.sequences.fluxes.percolation[k] = (                    self.sequences.fluxes.ponding[k] * self.sequences.factors.relativesoilmoisture[k] ** self.parameters.derived.beta[k]                )
    cpdef inline void calc_cisterninflow(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.cisterninflow = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.cisternsource[k]:
                if self.parameters.control.landtype[k] == SEALED:
                    self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow + (self.parameters.control.zonearea[k] * self.sequences.fluxes.surfacerunoff[k])
                elif self.parameters.control.landtype[k] != WATER:
                    self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow + (self.parameters.control.zonearea[k] * self.sequences.fluxes.percolation[k])
        self.sequences.fluxes.cisterninflow = self.sequences.fluxes.cisterninflow / (1000.0)
    cpdef inline void calc_cisternoverflow_cisternwater(self) noexcept nogil:
        self.sequences.states.cisternwater = self.sequences.states.cisternwater + (self.sequences.fluxes.cisterninflow)
        if self.sequences.states.cisternwater <= self.parameters.control.cisterncapacity:
            self.sequences.fluxes.cisternoverflow = 0.0
        else:
            self.sequences.fluxes.cisternoverflow = self.sequences.states.cisternwater - self.parameters.control.cisterncapacity
            self.sequences.states.cisternwater = self.parameters.control.cisterncapacity
    cpdef inline void calc_soilevapotranspiration(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_soilevapotranspiration_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_totalevapotranspiration(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.lakeevaporation[k]
            else:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.interceptionevaporation[k]
            if self.parameters.control.soiltype[k] != NONE:
                self.sequences.fluxes.totalevapotranspiration[k] = self.sequences.fluxes.totalevapotranspiration[k] + (self.sequences.fluxes.soilevapotranspiration[k])
    cpdef inline void calc_soilmoisture(self) noexcept nogil:
        cdef double delta
        cdef double factor
        cdef double decrease
        cdef double increase
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.new_states.soilmoisture[k] = 0.0
                self.sequences.fluxes.percolation[k] = 0.0
                self.sequences.fluxes.capillaryrise[k] = 0.0
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
            else:
                increase = self.sequences.fluxes.ponding[k] + self.sequences.fluxes.capillaryrise[k]
                decrease = self.sequences.fluxes.percolation[k]
                if self.sequences.fluxes.soilevapotranspiration[k] < 0.0:
                    increase = increase - (self.sequences.fluxes.soilevapotranspiration[k])
                else:
                    decrease = decrease + (self.sequences.fluxes.soilevapotranspiration[k])
                self.sequences.new_states.soilmoisture[k] = self.sequences.old_states.soilmoisture[k] + increase - decrease
                if self.sequences.new_states.soilmoisture[k] < 0.0:
                    factor = (self.sequences.old_states.soilmoisture[k] + increase) / decrease
                    self.sequences.fluxes.percolation[k] = self.sequences.fluxes.percolation[k] * (factor)
                    if self.sequences.fluxes.soilevapotranspiration[k] >= 0.0:
                        self.sequences.fluxes.soilevapotranspiration[k] = self.sequences.fluxes.soilevapotranspiration[k] * (factor)
                    self.sequences.new_states.soilmoisture[k] = 0.0
                elif self.sequences.new_states.soilmoisture[k] > self.parameters.derived.maxsoilwater[k]:
                    delta = self.sequences.new_states.soilmoisture[k] - self.parameters.derived.maxsoilwater[k]
                    if self.sequences.fluxes.capillaryrise[k] >= delta:
                        self.sequences.fluxes.capillaryrise[k] = self.sequences.fluxes.capillaryrise[k] - (delta)
                        self.sequences.new_states.soilmoisture[k] = self.parameters.derived.maxsoilwater[k]
                    else:
                        self.sequences.new_states.soilmoisture[k] = self.sequences.new_states.soilmoisture[k] - (self.sequences.fluxes.capillaryrise[k])
                        self.sequences.fluxes.capillaryrise[k] = 0.0
                        self.sequences.fluxes.percolation[k] = self.sequences.fluxes.percolation[k] + (self.sequences.new_states.soilmoisture[k] - self.parameters.derived.maxsoilwater[k])
                        self.sequences.new_states.soilmoisture[k] = self.parameters.derived.maxsoilwater[k]
    cpdef inline void calc_requiredirrigation(self) noexcept nogil:
        cdef double sm
        cdef numpy.int64_t l
        cdef numpy.int64_t k
        cdef numpy.int64_t m
        m = self.parameters.derived.moy[self.idx_sim]
        for k in range(self.parameters.control.nmbzones):
            l = self.parameters.control.landtype[k] - 1
            sm = self.sequences.factors.relativesoilmoisture[k]
            if (self.parameters.control.soiltype[k] == NONE) or (sm >= self.parameters.control.irrigationtrigger[l, m]):
                self.sequences.fluxes.requiredirrigation[k] = 0.0
            else:
                self.sequences.fluxes.requiredirrigation[k] = self.parameters.derived.maxsoilwater[k] * (                    self.parameters.control.irrigationtarget[l, m] - sm                )
    cpdef inline void calc_cisterndemand(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.cisterndemand = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] != NONE:
                self.sequences.fluxes.cisterndemand = self.sequences.fluxes.cisterndemand + (self.parameters.control.zonearea[k] * self.sequences.fluxes.requiredirrigation[k])
        self.sequences.fluxes.cisterndemand = self.sequences.fluxes.cisterndemand / (1000.0)
    cpdef inline void calc_cisternextraction_cisternwater(self) noexcept nogil:
        if self.sequences.states.cisternwater > self.sequences.fluxes.cisterndemand:
            self.sequences.fluxes.cisternextraction = self.sequences.fluxes.cisterndemand
            self.sequences.states.cisternwater = self.sequences.states.cisternwater - (self.sequences.fluxes.cisternextraction)
        else:
            self.sequences.fluxes.cisternextraction = self.sequences.states.cisternwater
            self.sequences.states.cisternwater = 0.0
    cpdef inline void calc_internalirrigation_soilmoisture(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double factor
        if self.sequences.fluxes.cisterndemand > 0.0:
            factor = self.sequences.fluxes.cisternextraction / self.sequences.fluxes.cisterndemand
        else:
            factor = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.states.soilmoisture[k] = 0.0
                self.sequences.fluxes.internalirrigation[k] = 0.0
            else:
                self.sequences.fluxes.internalirrigation[k] = factor * self.sequences.fluxes.requiredirrigation[k]
                self.sequences.states.soilmoisture[k] = self.sequences.states.soilmoisture[k] + (self.sequences.fluxes.internalirrigation[k])
    cpdef inline void calc_baseflow(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == SEALED:
                self.sequences.fluxes.baseflow[k] = 0.0
            else:
                self.sequences.fluxes.baseflow[k] = (1.0 - self.parameters.control.baseflowindex[k]) * max(                    self.sequences.fluxes.potentialrecharge[k], 0.0                )
    cpdef inline void calc_actualrecharge(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.actualrecharge = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] != SEALED:
                self.sequences.fluxes.actualrecharge = self.sequences.fluxes.actualrecharge + (self.parameters.derived.zoneratio[k] * (                    self.sequences.fluxes.potentialrecharge[k] - self.sequences.fluxes.baseflow[k]                ))
    cpdef inline void calc_delayedrecharge_deepwater(self) noexcept nogil:
        if self.parameters.control.rechargedelay > 0.0:
            self.sequences.new_states.deepwater = (self.sequences.fluxes.actualrecharge + self.sequences.old_states.deepwater) * exp(                -1.0 / self.parameters.control.rechargedelay            )
            self.sequences.fluxes.delayedrecharge = self.sequences.fluxes.actualrecharge + self.sequences.old_states.deepwater - self.sequences.new_states.deepwater
        else:
            self.sequences.fluxes.delayedrecharge = self.sequences.old_states.deepwater + self.sequences.fluxes.actualrecharge
            self.sequences.new_states.deepwater = 0.0
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.temperature
    cpdef double get_meantemperature(self) noexcept nogil:
        return self.sequences.inputs.temperature
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.precipitation
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.interceptedwater[k]
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.soilmoisture[k]
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.snowpack[k] > 0.0:
            return 1.0
        return 0.0
    cpdef inline void calc_interceptionevaporation_interceptedwater_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.interceptionevaporation[k] = 0.0
                self.sequences.states.interceptedwater[k] = 0.0
            else:
                self.sequences.fluxes.interceptionevaporation[k] = min(                    submodel.get_interceptionevaporation(k), self.sequences.states.interceptedwater[k]                )
                self.sequences.states.interceptedwater[k] = self.sequences.states.interceptedwater[k] - (self.sequences.fluxes.interceptionevaporation[k])
    cpdef inline void calc_lakeevaporation_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.landtype[k] == WATER:
                self.sequences.fluxes.lakeevaporation[k] = submodel.get_waterevaporation(k)
            else:
                self.sequences.fluxes.lakeevaporation[k] = 0.0
    cpdef inline void calc_soilevapotranspiration_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.soiltype[k] == NONE:
                self.sequences.fluxes.soilevapotranspiration[k] = 0.0
            else:
                self.sequences.fluxes.soilevapotranspiration[k] = submodel.get_soilevapotranspiration(k)
