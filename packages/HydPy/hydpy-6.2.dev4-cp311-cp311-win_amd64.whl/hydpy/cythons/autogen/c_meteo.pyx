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
cdef class FixedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._possiblesunshineduration_inputflag:
            self.possiblesunshineduration = self._possiblesunshineduration_inputpointer[0]
        elif self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._sunshineduration_inputflag:
            self.sunshineduration = self._sunshineduration_inputpointer[0]
        elif self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
        if self._clearskysolarradiation_inputflag:
            self.clearskysolarradiation = self._clearskysolarradiation_inputpointer[0]
        elif self._clearskysolarradiation_diskflag_reading:
            self.clearskysolarradiation = self._clearskysolarradiation_ncarray[0]
        elif self._clearskysolarradiation_ramflag:
            self.clearskysolarradiation = self._clearskysolarradiation_array[idx]
        if self._globalradiation_inputflag:
            self.globalradiation = self._globalradiation_inputpointer[0]
        elif self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._temperature_inputflag:
            self.temperature = self._temperature_inputpointer[0]
        elif self._temperature_diskflag_reading:
            self.temperature = self._temperature_ncarray[0]
        elif self._temperature_ramflag:
            self.temperature = self._temperature_array[idx]
        if self._precipitation_inputflag:
            self.precipitation = self._precipitation_inputpointer[0]
        elif self._precipitation_diskflag_reading:
            self.precipitation = self._precipitation_ncarray[0]
        elif self._precipitation_ramflag:
            self.precipitation = self._precipitation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
        if self._clearskysolarradiation_diskflag_writing:
            self._clearskysolarradiation_ncarray[0] = self.clearskysolarradiation
        if self._clearskysolarradiation_ramflag:
            self._clearskysolarradiation_array[idx] = self.clearskysolarradiation
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._temperature_diskflag_writing:
            self._temperature_ncarray[0] = self.temperature
        if self._temperature_ramflag:
            self._temperature_array[idx] = self.temperature
        if self._precipitation_diskflag_writing:
            self._precipitation_ncarray[0] = self.precipitation
        if self._precipitation_ramflag:
            self._precipitation_array[idx] = self.precipitation
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_inputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_inputpointer = value.p_value
        if name == "clearskysolarradiation":
            self._clearskysolarradiation_inputpointer = value.p_value
        if name == "globalradiation":
            self._globalradiation_inputpointer = value.p_value
        if name == "temperature":
            self._temperature_inputpointer = value.p_value
        if name == "precipitation":
            self._precipitation_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._earthsundistance_diskflag_reading:
            self.earthsundistance = self._earthsundistance_ncarray[0]
        elif self._earthsundistance_ramflag:
            self.earthsundistance = self._earthsundistance_array[idx]
        if self._solardeclination_diskflag_reading:
            self.solardeclination = self._solardeclination_ncarray[0]
        elif self._solardeclination_ramflag:
            self.solardeclination = self._solardeclination_array[idx]
        if self._sunsethourangle_diskflag_reading:
            self.sunsethourangle = self._sunsethourangle_ncarray[0]
        elif self._sunsethourangle_ramflag:
            self.sunsethourangle = self._sunsethourangle_array[idx]
        if self._solartimeangle_diskflag_reading:
            self.solartimeangle = self._solartimeangle_ncarray[0]
        elif self._solartimeangle_ramflag:
            self.solartimeangle = self._solartimeangle_array[idx]
        if self._timeofsunrise_diskflag_reading:
            self.timeofsunrise = self._timeofsunrise_ncarray[0]
        elif self._timeofsunrise_ramflag:
            self.timeofsunrise = self._timeofsunrise_array[idx]
        if self._timeofsunset_diskflag_reading:
            self.timeofsunset = self._timeofsunset_ncarray[0]
        elif self._timeofsunset_ramflag:
            self.timeofsunset = self._timeofsunset_array[idx]
        if self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._dailypossiblesunshineduration_diskflag_reading:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_ncarray[0]
        elif self._dailypossiblesunshineduration_ramflag:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_array[idx]
        if self._unadjustedsunshineduration_diskflag_reading:
            self.unadjustedsunshineduration = self._unadjustedsunshineduration_ncarray[0]
        elif self._unadjustedsunshineduration_ramflag:
            self.unadjustedsunshineduration = self._unadjustedsunshineduration_array[idx]
        if self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
        if self._dailysunshineduration_diskflag_reading:
            self.dailysunshineduration = self._dailysunshineduration_ncarray[0]
        elif self._dailysunshineduration_ramflag:
            self.dailysunshineduration = self._dailysunshineduration_array[idx]
        if self._portiondailyradiation_diskflag_reading:
            self.portiondailyradiation = self._portiondailyradiation_ncarray[0]
        elif self._portiondailyradiation_ramflag:
            self.portiondailyradiation = self._portiondailyradiation_array[idx]
        if self._temperature_diskflag_reading:
            k = 0
            for jdx0 in range(self._temperature_length_0):
                self.temperature[jdx0] = self._temperature_ncarray[k]
                k += 1
        elif self._temperature_ramflag:
            for jdx0 in range(self._temperature_length_0):
                self.temperature[jdx0] = self._temperature_array[idx, jdx0]
        if self._meantemperature_diskflag_reading:
            self.meantemperature = self._meantemperature_ncarray[0]
        elif self._meantemperature_ramflag:
            self.meantemperature = self._meantemperature_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._earthsundistance_diskflag_writing:
            self._earthsundistance_ncarray[0] = self.earthsundistance
        if self._earthsundistance_ramflag:
            self._earthsundistance_array[idx] = self.earthsundistance
        if self._solardeclination_diskflag_writing:
            self._solardeclination_ncarray[0] = self.solardeclination
        if self._solardeclination_ramflag:
            self._solardeclination_array[idx] = self.solardeclination
        if self._sunsethourangle_diskflag_writing:
            self._sunsethourangle_ncarray[0] = self.sunsethourangle
        if self._sunsethourangle_ramflag:
            self._sunsethourangle_array[idx] = self.sunsethourangle
        if self._solartimeangle_diskflag_writing:
            self._solartimeangle_ncarray[0] = self.solartimeangle
        if self._solartimeangle_ramflag:
            self._solartimeangle_array[idx] = self.solartimeangle
        if self._timeofsunrise_diskflag_writing:
            self._timeofsunrise_ncarray[0] = self.timeofsunrise
        if self._timeofsunrise_ramflag:
            self._timeofsunrise_array[idx] = self.timeofsunrise
        if self._timeofsunset_diskflag_writing:
            self._timeofsunset_ncarray[0] = self.timeofsunset
        if self._timeofsunset_ramflag:
            self._timeofsunset_array[idx] = self.timeofsunset
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._dailypossiblesunshineduration_diskflag_writing:
            self._dailypossiblesunshineduration_ncarray[0] = self.dailypossiblesunshineduration
        if self._dailypossiblesunshineduration_ramflag:
            self._dailypossiblesunshineduration_array[idx] = self.dailypossiblesunshineduration
        if self._unadjustedsunshineduration_diskflag_writing:
            self._unadjustedsunshineduration_ncarray[0] = self.unadjustedsunshineduration
        if self._unadjustedsunshineduration_ramflag:
            self._unadjustedsunshineduration_array[idx] = self.unadjustedsunshineduration
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
        if self._dailysunshineduration_diskflag_writing:
            self._dailysunshineduration_ncarray[0] = self.dailysunshineduration
        if self._dailysunshineduration_ramflag:
            self._dailysunshineduration_array[idx] = self.dailysunshineduration
        if self._portiondailyradiation_diskflag_writing:
            self._portiondailyradiation_ncarray[0] = self.portiondailyradiation
        if self._portiondailyradiation_ramflag:
            self._portiondailyradiation_array[idx] = self.portiondailyradiation
        if self._temperature_diskflag_writing:
            k = 0
            for jdx0 in range(self._temperature_length_0):
                self._temperature_ncarray[k] = self.temperature[jdx0]
                k += 1
        if self._temperature_ramflag:
            for jdx0 in range(self._temperature_length_0):
                self._temperature_array[idx, jdx0] = self.temperature[jdx0]
        if self._meantemperature_diskflag_writing:
            self._meantemperature_ncarray[0] = self.meantemperature
        if self._meantemperature_ramflag:
            self._meantemperature_array[idx] = self.meantemperature
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "earthsundistance":
            self._earthsundistance_outputpointer = value.p_value
        if name == "solardeclination":
            self._solardeclination_outputpointer = value.p_value
        if name == "sunsethourangle":
            self._sunsethourangle_outputpointer = value.p_value
        if name == "solartimeangle":
            self._solartimeangle_outputpointer = value.p_value
        if name == "timeofsunrise":
            self._timeofsunrise_outputpointer = value.p_value
        if name == "timeofsunset":
            self._timeofsunset_outputpointer = value.p_value
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "dailypossiblesunshineduration":
            self._dailypossiblesunshineduration_outputpointer = value.p_value
        if name == "unadjustedsunshineduration":
            self._unadjustedsunshineduration_outputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_outputpointer = value.p_value
        if name == "dailysunshineduration":
            self._dailysunshineduration_outputpointer = value.p_value
        if name == "portiondailyradiation":
            self._portiondailyradiation_outputpointer = value.p_value
        if name == "meantemperature":
            self._meantemperature_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._earthsundistance_outputflag:
            self._earthsundistance_outputpointer[0] = self.earthsundistance
        if self._solardeclination_outputflag:
            self._solardeclination_outputpointer[0] = self.solardeclination
        if self._sunsethourangle_outputflag:
            self._sunsethourangle_outputpointer[0] = self.sunsethourangle
        if self._solartimeangle_outputflag:
            self._solartimeangle_outputpointer[0] = self.solartimeangle
        if self._timeofsunrise_outputflag:
            self._timeofsunrise_outputpointer[0] = self.timeofsunrise
        if self._timeofsunset_outputflag:
            self._timeofsunset_outputpointer[0] = self.timeofsunset
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._dailypossiblesunshineduration_outputflag:
            self._dailypossiblesunshineduration_outputpointer[0] = self.dailypossiblesunshineduration
        if self._unadjustedsunshineduration_outputflag:
            self._unadjustedsunshineduration_outputpointer[0] = self.unadjustedsunshineduration
        if self._sunshineduration_outputflag:
            self._sunshineduration_outputpointer[0] = self.sunshineduration
        if self._dailysunshineduration_outputflag:
            self._dailysunshineduration_outputpointer[0] = self.dailysunshineduration
        if self._portiondailyradiation_outputflag:
            self._portiondailyradiation_outputpointer[0] = self.portiondailyradiation
        if self._meantemperature_outputflag:
            self._meantemperature_outputpointer[0] = self.meantemperature
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._extraterrestrialradiation_diskflag_reading:
            self.extraterrestrialradiation = self._extraterrestrialradiation_ncarray[0]
        elif self._extraterrestrialradiation_ramflag:
            self.extraterrestrialradiation = self._extraterrestrialradiation_array[idx]
        if self._clearskysolarradiation_diskflag_reading:
            self.clearskysolarradiation = self._clearskysolarradiation_ncarray[0]
        elif self._clearskysolarradiation_ramflag:
            self.clearskysolarradiation = self._clearskysolarradiation_array[idx]
        if self._unadjustedglobalradiation_diskflag_reading:
            self.unadjustedglobalradiation = self._unadjustedglobalradiation_ncarray[0]
        elif self._unadjustedglobalradiation_ramflag:
            self.unadjustedglobalradiation = self._unadjustedglobalradiation_array[idx]
        if self._dailyglobalradiation_diskflag_reading:
            self.dailyglobalradiation = self._dailyglobalradiation_ncarray[0]
        elif self._dailyglobalradiation_ramflag:
            self.dailyglobalradiation = self._dailyglobalradiation_array[idx]
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._precipitation_diskflag_reading:
            k = 0
            for jdx0 in range(self._precipitation_length_0):
                self.precipitation[jdx0] = self._precipitation_ncarray[k]
                k += 1
        elif self._precipitation_ramflag:
            for jdx0 in range(self._precipitation_length_0):
                self.precipitation[jdx0] = self._precipitation_array[idx, jdx0]
        if self._meanprecipitation_diskflag_reading:
            self.meanprecipitation = self._meanprecipitation_ncarray[0]
        elif self._meanprecipitation_ramflag:
            self.meanprecipitation = self._meanprecipitation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._extraterrestrialradiation_diskflag_writing:
            self._extraterrestrialradiation_ncarray[0] = self.extraterrestrialradiation
        if self._extraterrestrialradiation_ramflag:
            self._extraterrestrialradiation_array[idx] = self.extraterrestrialradiation
        if self._clearskysolarradiation_diskflag_writing:
            self._clearskysolarradiation_ncarray[0] = self.clearskysolarradiation
        if self._clearskysolarradiation_ramflag:
            self._clearskysolarradiation_array[idx] = self.clearskysolarradiation
        if self._unadjustedglobalradiation_diskflag_writing:
            self._unadjustedglobalradiation_ncarray[0] = self.unadjustedglobalradiation
        if self._unadjustedglobalradiation_ramflag:
            self._unadjustedglobalradiation_array[idx] = self.unadjustedglobalradiation
        if self._dailyglobalradiation_diskflag_writing:
            self._dailyglobalradiation_ncarray[0] = self.dailyglobalradiation
        if self._dailyglobalradiation_ramflag:
            self._dailyglobalradiation_array[idx] = self.dailyglobalradiation
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._precipitation_diskflag_writing:
            k = 0
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_ncarray[k] = self.precipitation[jdx0]
                k += 1
        if self._precipitation_ramflag:
            for jdx0 in range(self._precipitation_length_0):
                self._precipitation_array[idx, jdx0] = self.precipitation[jdx0]
        if self._meanprecipitation_diskflag_writing:
            self._meanprecipitation_ncarray[0] = self.meanprecipitation
        if self._meanprecipitation_ramflag:
            self._meanprecipitation_array[idx] = self.meanprecipitation
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "extraterrestrialradiation":
            self._extraterrestrialradiation_outputpointer = value.p_value
        if name == "clearskysolarradiation":
            self._clearskysolarradiation_outputpointer = value.p_value
        if name == "unadjustedglobalradiation":
            self._unadjustedglobalradiation_outputpointer = value.p_value
        if name == "dailyglobalradiation":
            self._dailyglobalradiation_outputpointer = value.p_value
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
        if name == "meanprecipitation":
            self._meanprecipitation_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._extraterrestrialradiation_outputflag:
            self._extraterrestrialradiation_outputpointer[0] = self.extraterrestrialradiation
        if self._clearskysolarradiation_outputflag:
            self._clearskysolarradiation_outputpointer[0] = self.clearskysolarradiation
        if self._unadjustedglobalradiation_outputflag:
            self._unadjustedglobalradiation_outputpointer[0] = self.unadjustedglobalradiation
        if self._dailyglobalradiation_outputflag:
            self._dailyglobalradiation_outputpointer[0] = self.dailyglobalradiation
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._meanprecipitation_outputflag:
            self._meanprecipitation_outputpointer[0] = self.meanprecipitation
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.reset_reuseflags()
        self.load_data(idx)
        self.run()
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
        self.__hydpy_reuse_process_radiation_v1__ = False
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.calc_earthsundistance_v1()
        self.calc_solardeclination_v1()
        self.calc_solardeclination_v2()
        self.calc_sunsethourangle_v1()
        self.calc_solartimeangle_v1()
        self.calc_timeofsunrise_timeofsunset_v1()
        self.calc_dailypossiblesunshineduration_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_possiblesunshineduration_v2()
        self.update_loggedsunshineduration_v1()
        self.calc_dailysunshineduration_v1()
        self.update_loggedglobalradiation_v1()
        self.calc_dailyglobalradiation_v2()
        self.calc_extraterrestrialradiation_v1()
        self.calc_extraterrestrialradiation_v2()
        self.calc_dailysunshineduration_v2()
        self.calc_sunshineduration_v1()
        self.calc_portiondailyradiation_v1()
        self.calc_clearskysolarradiation_v1()
        self.adjust_clearskysolarradiation_v1()
        self.calc_globalradiation_v1()
        self.calc_unadjustedglobalradiation_v1()
        self.calc_unadjustedsunshineduration_v1()
        self.update_loggedunadjustedglobalradiation_v1()
        self.update_loggedunadjustedsunshineduration_v1()
        self.calc_dailyglobalradiation_v1()
        self.calc_globalradiation_v2()
        self.calc_sunshineduration_v2()
        self.calc_temperature_v1()
        self.adjust_temperature_v1()
        self.calc_meantemperature_v1()
        self.calc_precipitation_v1()
        self.adjust_precipitation_v1()
        self.calc_meanprecipitation_v1()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        pass
    cpdef void update_outlets(self) noexcept nogil:
        pass
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i
        pass
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
    cpdef inline void calc_earthsundistance_v1(self) noexcept nogil:
        self.sequences.factors.earthsundistance = 1.0 + 0.033 * cos(            2 * self.parameters.fixed.pi / 366.0 * (self.parameters.derived.doy[self.idx_sim] + 1)        )
    cpdef inline void calc_solardeclination_v1(self) noexcept nogil:
        self.sequences.factors.solardeclination = 0.409 * sin(            2 * self.parameters.fixed.pi / 366 * (self.parameters.derived.doy[self.idx_sim] + 1) - 1.39        )
    cpdef inline void calc_solardeclination_v2(self) noexcept nogil:
        self.sequences.factors.solardeclination = 0.41 * cos(            2.0 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] - 171.0) / 365.0        )
    cpdef inline void calc_sunsethourangle_v1(self) noexcept nogil:
        self.sequences.factors.sunsethourangle = acos(            -tan(self.parameters.derived.latituderad) * tan(self.sequences.factors.solardeclination)        )
    cpdef inline void calc_solartimeangle_v1(self) noexcept nogil:
        cdef double d_time
        cdef double d_sc
        cdef double d_b
        d_b = 2.0 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] - 80.0) / 365.0
        d_sc = (            0.1645 * sin(2.0 * d_b)            - 0.1255 * cos(d_b)            - 0.025 * sin(d_b)        )
        d_time = (            self.parameters.derived.sct[self.idx_sim] + (self.parameters.control.longitude - self.parameters.derived.utclongitude) / 15.0 + d_sc        )
        self.sequences.factors.solartimeangle = self.parameters.fixed.pi / 12.0 * (d_time - 12.0)
    cpdef inline void calc_timeofsunrise_timeofsunset_v1(self) noexcept nogil:
        cdef double d_dt
        self.sequences.factors.timeofsunrise = (12.0 / self.parameters.fixed.pi) * acos(            tan(self.sequences.factors.solardeclination) * tan(self.parameters.derived.latituderad)            + 0.0145            / cos(self.sequences.factors.solardeclination)            / cos(self.parameters.derived.latituderad)        )
        self.sequences.factors.timeofsunset = 24.0 - self.sequences.factors.timeofsunrise
        d_dt = (self.parameters.derived.utclongitude - self.parameters.control.longitude) * 4.0 / 60.0
        self.sequences.factors.timeofsunrise = self.sequences.factors.timeofsunrise + (d_dt)
        self.sequences.factors.timeofsunset = self.sequences.factors.timeofsunset + (d_dt)
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil:
        self.sequences.factors.dailypossiblesunshineduration = self.sequences.factors.timeofsunset - self.sequences.factors.timeofsunrise
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil:
        cdef double d_thresh
        if self.parameters.derived.hours < 24.0:
            if self.sequences.factors.solartimeangle <= 0.0:
                d_thresh = -self.sequences.factors.solartimeangle - self.parameters.fixed.pi * self.parameters.derived.days
            else:
                d_thresh = self.sequences.factors.solartimeangle - self.parameters.fixed.pi * self.parameters.derived.days
            self.sequences.factors.possiblesunshineduration = min(                max(12.0 / self.parameters.fixed.pi * (self.sequences.factors.sunsethourangle - d_thresh), 0.0), self.parameters.derived.hours            )
        else:
            self.sequences.factors.possiblesunshineduration = 24.0 / self.parameters.fixed.pi * self.sequences.factors.sunsethourangle
    cpdef inline void calc_possiblesunshineduration_v2(self) noexcept nogil:
        cdef double d_t1
        cdef double d_t0
        cdef double d_stc
        d_stc = self.parameters.derived.sct[self.idx_sim]
        d_t0 = max((d_stc - self.parameters.derived.hours / 2.0), self.sequences.factors.timeofsunrise)
        d_t1 = min((d_stc + self.parameters.derived.hours / 2.0), self.sequences.factors.timeofsunset)
        self.sequences.factors.possiblesunshineduration = max(d_t1 - d_t0, 0.0)
    cpdef inline void update_loggedsunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.inputs.sunshineduration
    cpdef inline void calc_dailysunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.factors.dailysunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.factors.dailysunshineduration = self.sequences.factors.dailysunshineduration + (self.sequences.logs.loggedsunshineduration[idx])
    cpdef inline void update_loggedglobalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.inputs.globalradiation
    cpdef inline void calc_dailyglobalradiation_v2(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailyglobalradiation = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        self.sequences.fluxes.dailyglobalradiation = self.sequences.fluxes.dailyglobalradiation / (self.parameters.derived.nmblogentries)
    cpdef inline void calc_extraterrestrialradiation_v1(self) noexcept nogil:
        cdef double d_omega2
        cdef double d_omega1
        cdef double d_delta
        if self.parameters.derived.days < 1.0:
            d_delta = self.parameters.fixed.pi * self.parameters.derived.days
            d_omega1 = self.sequences.factors.solartimeangle - d_delta
            d_omega2 = self.sequences.factors.solartimeangle + d_delta
            self.sequences.fluxes.extraterrestrialradiation = max(                (12.0 * self.parameters.fixed.solarconstant / self.parameters.fixed.pi * self.sequences.factors.earthsundistance)                * (                    (                        (d_omega2 - d_omega1)                        * sin(self.parameters.derived.latituderad)                        * sin(self.sequences.factors.solardeclination)                    )                    + (                        cos(self.parameters.derived.latituderad)                        * cos(self.sequences.factors.solardeclination)                        * (sin(d_omega2) - sin(d_omega1))                    )                ),                0.0,            )
        else:
            self.sequences.fluxes.extraterrestrialradiation = (                self.parameters.fixed.solarconstant / self.parameters.fixed.pi * self.sequences.factors.earthsundistance            ) * (                (                    self.sequences.factors.sunsethourangle                    * sin(self.parameters.derived.latituderad)                    * sin(self.sequences.factors.solardeclination)                )                + (                    cos(self.parameters.derived.latituderad)                    * cos(self.sequences.factors.solardeclination)                    * sin(self.sequences.factors.sunsethourangle)                )            )
    cpdef inline void calc_extraterrestrialradiation_v2(self) noexcept nogil:
        cdef double d_sunsethourangle
        d_sunsethourangle = (self.sequences.factors.timeofsunset - self.sequences.factors.timeofsunrise) * self.parameters.fixed.pi / 24.0
        self.sequences.fluxes.extraterrestrialradiation = (            self.parameters.fixed.solarconstant * self.sequences.factors.earthsundistance / self.parameters.fixed.pi        ) * (            d_sunsethourangle            * sin(self.sequences.factors.solardeclination)            * sin(self.parameters.derived.latituderad)            + cos(self.sequences.factors.solardeclination)            * cos(self.parameters.derived.latituderad)            * sin(d_sunsethourangle)        )
    cpdef inline void calc_dailysunshineduration_v2(self) noexcept nogil:
        self.sequences.factors.dailysunshineduration = self.return_sunshineduration_v1(            self.sequences.fluxes.dailyglobalradiation,            self.sequences.fluxes.extraterrestrialradiation,            self.sequences.factors.dailypossiblesunshineduration,        )
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil:
        cdef double d_sd
        cdef numpy.int64_t idx
        if self.sequences.fluxes.extraterrestrialradiation > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            d_sd = (                (self.sequences.inputs.globalradiation / self.sequences.fluxes.extraterrestrialradiation)                - self.parameters.control.angstromconstant[idx]            ) * (self.sequences.factors.possiblesunshineduration / self.parameters.control.angstromfactor[idx])
            self.sequences.factors.sunshineduration = min(max(d_sd, 0.0), self.sequences.factors.possiblesunshineduration)
        else:
            self.sequences.factors.sunshineduration = 0.0
    cpdef inline void calc_portiondailyradiation_v1(self) noexcept nogil:
        cdef double d_temp
        cdef double d_p
        cdef double d_tlp
        cdef double d_dt
        cdef numpy.int64_t i
        cdef double d_fac
        d_fac = 2.0 * self.parameters.fixed.pi / 360.0
        self.sequences.factors.portiondailyradiation = 0.0
        for i in range(2):
            if i:
                d_dt = self.parameters.derived.hours / 2.0
            else:
                d_dt = -self.parameters.derived.hours / 2.0
            d_tlp = (100.0 * d_fac) * (                (self.parameters.derived.sct[self.idx_sim] + d_dt - self.sequences.factors.timeofsunrise)                / (self.sequences.factors.timeofsunset - self.sequences.factors.timeofsunrise)            )
            if d_tlp <= 0.0:
                d_p = 0.0
            elif d_tlp < 100.0 * d_fac:
                d_p = 50.0 - 50.0 * cos(1.8 * d_tlp)
                d_temp = 3.4 * sin(3.6 * d_tlp) ** 2
                if d_tlp <= 50.0 * d_fac:
                    d_p = d_p - (d_temp)
                else:
                    d_p = d_p + (d_temp)
            else:
                d_p = 100.0
            if i:
                self.sequences.factors.portiondailyradiation = self.sequences.factors.portiondailyradiation + (d_p)
            else:
                self.sequences.factors.portiondailyradiation = self.sequences.factors.portiondailyradiation - (d_p)
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void adjust_clearskysolarradiation_v1(self) noexcept nogil:
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation * ((            self.parameters.derived.nmblogentries * self.sequences.factors.portiondailyradiation / 100.0        ))
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        if self.sequences.factors.possiblesunshineduration > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            self.sequences.fluxes.globalradiation = self.sequences.fluxes.extraterrestrialradiation * (                self.parameters.control.angstromconstant[idx]                + self.parameters.control.angstromfactor[idx]                * self.sequences.inputs.sunshineduration                / self.sequences.factors.possiblesunshineduration            )
        else:
            self.sequences.fluxes.globalradiation = 0.0
    cpdef inline void calc_unadjustedglobalradiation_v1(self) noexcept nogil:
        cdef double d_pos
        cdef double d_act
        if self.sequences.factors.possiblesunshineduration > 0.0:
            d_act = self.sequences.inputs.sunshineduration
            d_pos = self.sequences.factors.possiblesunshineduration
        else:
            d_act = self.sequences.factors.dailysunshineduration
            d_pos = self.sequences.factors.dailypossiblesunshineduration
        self.sequences.fluxes.unadjustedglobalradiation = (            self.parameters.derived.nmblogentries * self.sequences.factors.portiondailyradiation / 100.0        ) * self.return_dailyglobalradiation_v1(d_act, d_pos)
    cpdef inline void calc_unadjustedsunshineduration_v1(self) noexcept nogil:
        self.sequences.factors.unadjustedsunshineduration = self.return_sunshineduration_v1(            self.sequences.inputs.globalradiation,            self.sequences.fluxes.extraterrestrialradiation            * self.parameters.derived.nmblogentries            * self.sequences.factors.portiondailyradiation            / 100.0,            self.sequences.factors.possiblesunshineduration,        )
    cpdef inline void update_loggedunadjustedglobalradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedunadjustedglobalradiation[idx] = (                self.sequences.logs.loggedunadjustedglobalradiation[idx - 1]            )
        self.sequences.logs.loggedunadjustedglobalradiation[0] = self.sequences.fluxes.unadjustedglobalradiation
    cpdef inline void update_loggedunadjustedsunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedunadjustedsunshineduration[idx] = (                self.sequences.logs.loggedunadjustedsunshineduration[idx - 1]            )
        self.sequences.logs.loggedunadjustedsunshineduration[0] = self.sequences.factors.unadjustedsunshineduration
    cpdef inline void calc_dailyglobalradiation_v1(self) noexcept nogil:
        self.sequences.fluxes.dailyglobalradiation = self.return_dailyglobalradiation_v1(            self.sequences.factors.dailysunshineduration, self.sequences.factors.dailypossiblesunshineduration        )
    cpdef inline void calc_globalradiation_v2(self) noexcept nogil:
        cdef double d_glob_mean
        cdef numpy.int64_t idx
        cdef double d_glob_sum
        d_glob_sum = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            d_glob_sum = d_glob_sum + (self.sequences.logs.loggedunadjustedglobalradiation[idx])
        d_glob_mean = d_glob_sum / self.parameters.derived.nmblogentries
        self.sequences.fluxes.globalradiation = (            self.sequences.fluxes.unadjustedglobalradiation * self.sequences.fluxes.dailyglobalradiation / d_glob_mean        )
    cpdef inline void calc_sunshineduration_v2(self) noexcept nogil:
        cdef numpy.int64_t idx
        cdef double d_denom
        cdef double d_nom
        d_nom = self.sequences.factors.unadjustedsunshineduration * self.sequences.factors.dailysunshineduration
        if d_nom == 0.0:
            self.sequences.factors.sunshineduration = 0.0
        else:
            d_denom = 0.0
            for idx in range(self.parameters.derived.nmblogentries):
                d_denom = d_denom + (self.sequences.logs.loggedunadjustedsunshineduration[idx])
            self.sequences.factors.sunshineduration = min(d_nom / d_denom, self.sequences.factors.possiblesunshineduration)
    cpdef inline void calc_temperature_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.temperature[k] = self.sequences.inputs.temperature
    cpdef inline void adjust_temperature_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.temperature[k] = self.sequences.factors.temperature[k] + (self.parameters.control.temperatureaddend[k])
    cpdef inline void calc_meantemperature_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.factors.meantemperature = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.factors.meantemperature = self.sequences.factors.meantemperature + (self.parameters.derived.hruareafraction[s] * self.sequences.factors.temperature[s])
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.inputs.precipitation
    cpdef inline void adjust_precipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.fluxes.precipitation[k] * (self.parameters.control.precipitationfactor[k])
    cpdef inline void calc_meanprecipitation_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanprecipitation = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanprecipitation = self.sequences.fluxes.meanprecipitation + (self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.precipitation[s])
    cpdef void determine_temperature_v1(self) noexcept nogil:
        self.run()
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.factors.temperature[s]
    cpdef double get_meantemperature_v1(self) noexcept nogil:
        return self.sequences.factors.meantemperature
    cpdef void determine_precipitation_v1(self) noexcept nogil:
        self.run()
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.precipitation[s]
    cpdef double get_meanprecipitation_v1(self) noexcept nogil:
        return self.sequences.fluxes.meanprecipitation
    cpdef void process_radiation_v1(self) noexcept nogil:
        if not self.__hydpy_reuse_process_radiation_v1__:
            self.run()
            self.__hydpy_reuse_process_radiation_v1__ = True
    cpdef double get_possiblesunshineduration_v1(self) noexcept nogil:
        return self.sequences.factors.possiblesunshineduration
    cpdef double get_possiblesunshineduration_v2(self) noexcept nogil:
        return self.sequences.inputs.possiblesunshineduration
    cpdef double get_sunshineduration_v1(self) noexcept nogil:
        return self.sequences.factors.sunshineduration
    cpdef double get_sunshineduration_v2(self) noexcept nogil:
        return self.sequences.inputs.sunshineduration
    cpdef double get_clearskysolarradiation_v1(self) noexcept nogil:
        return self.sequences.fluxes.clearskysolarradiation
    cpdef double get_clearskysolarradiation_v2(self) noexcept nogil:
        return self.sequences.inputs.clearskysolarradiation
    cpdef double get_globalradiation_v1(self) noexcept nogil:
        return self.sequences.fluxes.globalradiation
    cpdef double get_globalradiation_v2(self) noexcept nogil:
        return self.sequences.inputs.globalradiation
    cpdef inline double return_dailyglobalradiation_v1(self, double sunshineduration, double possiblesunshineduration) noexcept nogil:
        cdef numpy.int64_t idx
        if possiblesunshineduration > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            if (sunshineduration <= 0.0) and (self.parameters.derived.days >= 1.0):
                return self.sequences.fluxes.extraterrestrialradiation * self.parameters.control.angstromalternative[idx]
            return self.sequences.fluxes.extraterrestrialradiation * (                self.parameters.control.angstromconstant[idx]                + self.parameters.control.angstromfactor[idx] * sunshineduration / possiblesunshineduration            )
        return 0.0
    cpdef inline double return_sunshineduration_v1(self, double globalradiation, double extraterrestrialradiation, double possiblesunshineduration) noexcept nogil:
        cdef double d_sd
        cdef numpy.int64_t idx
        if extraterrestrialradiation <= 0.0:
            return possiblesunshineduration
        idx = self.parameters.derived.moy[self.idx_sim]
        d_sd = (possiblesunshineduration / self.parameters.control.angstromfactor[idx]) * (            globalradiation / extraterrestrialradiation - self.parameters.control.angstromconstant[idx]        )
        return min(max(d_sd, 0.0), possiblesunshineduration)
    cpdef inline void calc_earthsundistance(self) noexcept nogil:
        self.sequences.factors.earthsundistance = 1.0 + 0.033 * cos(            2 * self.parameters.fixed.pi / 366.0 * (self.parameters.derived.doy[self.idx_sim] + 1)        )
    cpdef inline void calc_sunsethourangle(self) noexcept nogil:
        self.sequences.factors.sunsethourangle = acos(            -tan(self.parameters.derived.latituderad) * tan(self.sequences.factors.solardeclination)        )
    cpdef inline void calc_solartimeangle(self) noexcept nogil:
        cdef double d_time
        cdef double d_sc
        cdef double d_b
        d_b = 2.0 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] - 80.0) / 365.0
        d_sc = (            0.1645 * sin(2.0 * d_b)            - 0.1255 * cos(d_b)            - 0.025 * sin(d_b)        )
        d_time = (            self.parameters.derived.sct[self.idx_sim] + (self.parameters.control.longitude - self.parameters.derived.utclongitude) / 15.0 + d_sc        )
        self.sequences.factors.solartimeangle = self.parameters.fixed.pi / 12.0 * (d_time - 12.0)
    cpdef inline void calc_timeofsunrise_timeofsunset(self) noexcept nogil:
        cdef double d_dt
        self.sequences.factors.timeofsunrise = (12.0 / self.parameters.fixed.pi) * acos(            tan(self.sequences.factors.solardeclination) * tan(self.parameters.derived.latituderad)            + 0.0145            / cos(self.sequences.factors.solardeclination)            / cos(self.parameters.derived.latituderad)        )
        self.sequences.factors.timeofsunset = 24.0 - self.sequences.factors.timeofsunrise
        d_dt = (self.parameters.derived.utclongitude - self.parameters.control.longitude) * 4.0 / 60.0
        self.sequences.factors.timeofsunrise = self.sequences.factors.timeofsunrise + (d_dt)
        self.sequences.factors.timeofsunset = self.sequences.factors.timeofsunset + (d_dt)
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil:
        self.sequences.factors.dailypossiblesunshineduration = self.sequences.factors.timeofsunset - self.sequences.factors.timeofsunrise
    cpdef inline void update_loggedsunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.inputs.sunshineduration
    cpdef inline void update_loggedglobalradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.inputs.globalradiation
    cpdef inline void calc_portiondailyradiation(self) noexcept nogil:
        cdef double d_temp
        cdef double d_p
        cdef double d_tlp
        cdef double d_dt
        cdef numpy.int64_t i
        cdef double d_fac
        d_fac = 2.0 * self.parameters.fixed.pi / 360.0
        self.sequences.factors.portiondailyradiation = 0.0
        for i in range(2):
            if i:
                d_dt = self.parameters.derived.hours / 2.0
            else:
                d_dt = -self.parameters.derived.hours / 2.0
            d_tlp = (100.0 * d_fac) * (                (self.parameters.derived.sct[self.idx_sim] + d_dt - self.sequences.factors.timeofsunrise)                / (self.sequences.factors.timeofsunset - self.sequences.factors.timeofsunrise)            )
            if d_tlp <= 0.0:
                d_p = 0.0
            elif d_tlp < 100.0 * d_fac:
                d_p = 50.0 - 50.0 * cos(1.8 * d_tlp)
                d_temp = 3.4 * sin(3.6 * d_tlp) ** 2
                if d_tlp <= 50.0 * d_fac:
                    d_p = d_p - (d_temp)
                else:
                    d_p = d_p + (d_temp)
            else:
                d_p = 100.0
            if i:
                self.sequences.factors.portiondailyradiation = self.sequences.factors.portiondailyradiation + (d_p)
            else:
                self.sequences.factors.portiondailyradiation = self.sequences.factors.portiondailyradiation - (d_p)
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void adjust_clearskysolarradiation(self) noexcept nogil:
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation * ((            self.parameters.derived.nmblogentries * self.sequences.factors.portiondailyradiation / 100.0        ))
    cpdef inline void calc_unadjustedglobalradiation(self) noexcept nogil:
        cdef double d_pos
        cdef double d_act
        if self.sequences.factors.possiblesunshineduration > 0.0:
            d_act = self.sequences.inputs.sunshineduration
            d_pos = self.sequences.factors.possiblesunshineduration
        else:
            d_act = self.sequences.factors.dailysunshineduration
            d_pos = self.sequences.factors.dailypossiblesunshineduration
        self.sequences.fluxes.unadjustedglobalradiation = (            self.parameters.derived.nmblogentries * self.sequences.factors.portiondailyradiation / 100.0        ) * self.return_dailyglobalradiation_v1(d_act, d_pos)
    cpdef inline void calc_unadjustedsunshineduration(self) noexcept nogil:
        self.sequences.factors.unadjustedsunshineduration = self.return_sunshineduration_v1(            self.sequences.inputs.globalradiation,            self.sequences.fluxes.extraterrestrialradiation            * self.parameters.derived.nmblogentries            * self.sequences.factors.portiondailyradiation            / 100.0,            self.sequences.factors.possiblesunshineduration,        )
    cpdef inline void update_loggedunadjustedglobalradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedunadjustedglobalradiation[idx] = (                self.sequences.logs.loggedunadjustedglobalradiation[idx - 1]            )
        self.sequences.logs.loggedunadjustedglobalradiation[0] = self.sequences.fluxes.unadjustedglobalradiation
    cpdef inline void update_loggedunadjustedsunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedunadjustedsunshineduration[idx] = (                self.sequences.logs.loggedunadjustedsunshineduration[idx - 1]            )
        self.sequences.logs.loggedunadjustedsunshineduration[0] = self.sequences.factors.unadjustedsunshineduration
    cpdef inline void calc_temperature(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.temperature[k] = self.sequences.inputs.temperature
    cpdef inline void adjust_temperature(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.factors.temperature[k] = self.sequences.factors.temperature[k] + (self.parameters.control.temperatureaddend[k])
    cpdef inline void calc_meantemperature(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.factors.meantemperature = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.factors.meantemperature = self.sequences.factors.meantemperature + (self.parameters.derived.hruareafraction[s] * self.sequences.factors.temperature[s])
    cpdef inline void calc_precipitation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.inputs.precipitation
    cpdef inline void adjust_precipitation(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.precipitation[k] = self.sequences.fluxes.precipitation[k] * (self.parameters.control.precipitationfactor[k])
    cpdef inline void calc_meanprecipitation(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.meanprecipitation = 0.0
        for s in range(self.parameters.control.nmbhru):
            self.sequences.fluxes.meanprecipitation = self.sequences.fluxes.meanprecipitation + (self.parameters.derived.hruareafraction[s] * self.sequences.fluxes.precipitation[s])
    cpdef void determine_temperature(self) noexcept nogil:
        self.run()
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.factors.temperature[s]
    cpdef double get_meantemperature(self) noexcept nogil:
        return self.sequences.factors.meantemperature
    cpdef void determine_precipitation(self) noexcept nogil:
        self.run()
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.precipitation[s]
    cpdef double get_meanprecipitation(self) noexcept nogil:
        return self.sequences.fluxes.meanprecipitation
    cpdef void process_radiation(self) noexcept nogil:
        if not self.__hydpy_reuse_process_radiation_v1__:
            self.run()
            self.__hydpy_reuse_process_radiation_v1__ = True
    cpdef inline double return_dailyglobalradiation(self, double sunshineduration, double possiblesunshineduration) noexcept nogil:
        cdef numpy.int64_t idx
        if possiblesunshineduration > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            if (sunshineduration <= 0.0) and (self.parameters.derived.days >= 1.0):
                return self.sequences.fluxes.extraterrestrialradiation * self.parameters.control.angstromalternative[idx]
            return self.sequences.fluxes.extraterrestrialradiation * (                self.parameters.control.angstromconstant[idx]                + self.parameters.control.angstromfactor[idx] * sunshineduration / possiblesunshineduration            )
        return 0.0
    cpdef inline double return_sunshineduration(self, double globalradiation, double extraterrestrialradiation, double possiblesunshineduration) noexcept nogil:
        cdef double d_sd
        cdef numpy.int64_t idx
        if extraterrestrialradiation <= 0.0:
            return possiblesunshineduration
        idx = self.parameters.derived.moy[self.idx_sim]
        d_sd = (possiblesunshineduration / self.parameters.control.angstromfactor[idx]) * (            globalradiation / extraterrestrialradiation - self.parameters.control.angstromconstant[idx]        )
        return min(max(d_sd, 0.0), possiblesunshineduration)
