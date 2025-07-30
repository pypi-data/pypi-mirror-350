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
        if self._globalradiation_inputflag:
            self.globalradiation = self._globalradiation_inputpointer[0]
        elif self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "globalradiation":
            self._globalradiation_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
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
        if self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
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
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "earthsundistance":
            self._earthsundistance_outputpointer = value.p_value
        if name == "solardeclination":
            self._solardeclination_outputpointer = value.p_value
        if name == "sunsethourangle":
            self._sunsethourangle_outputpointer = value.p_value
        if name == "solartimeangle":
            self._solartimeangle_outputpointer = value.p_value
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._earthsundistance_outputflag:
            self._earthsundistance_outputpointer[0] = self.earthsundistance
        if self._solardeclination_outputflag:
            self._solardeclination_outputpointer[0] = self.solardeclination
        if self._sunsethourangle_outputflag:
            self._sunsethourangle_outputpointer[0] = self.sunsethourangle
        if self._solartimeangle_outputflag:
            self._solartimeangle_outputpointer[0] = self.solartimeangle
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._sunshineduration_outputflag:
            self._sunshineduration_outputpointer[0] = self.sunshineduration
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._extraterrestrialradiation_diskflag_reading:
            self.extraterrestrialradiation = self._extraterrestrialradiation_ncarray[0]
        elif self._extraterrestrialradiation_ramflag:
            self.extraterrestrialradiation = self._extraterrestrialradiation_array[idx]
        if self._clearskysolarradiation_diskflag_reading:
            self.clearskysolarradiation = self._clearskysolarradiation_ncarray[0]
        elif self._clearskysolarradiation_ramflag:
            self.clearskysolarradiation = self._clearskysolarradiation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._extraterrestrialradiation_diskflag_writing:
            self._extraterrestrialradiation_ncarray[0] = self.extraterrestrialradiation
        if self._extraterrestrialradiation_ramflag:
            self._extraterrestrialradiation_array[idx] = self.extraterrestrialradiation
        if self._clearskysolarradiation_diskflag_writing:
            self._clearskysolarradiation_ncarray[0] = self.clearskysolarradiation
        if self._clearskysolarradiation_ramflag:
            self._clearskysolarradiation_array[idx] = self.clearskysolarradiation
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "extraterrestrialradiation":
            self._extraterrestrialradiation_outputpointer = value.p_value
        if name == "clearskysolarradiation":
            self._clearskysolarradiation_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._extraterrestrialradiation_outputflag:
            self._extraterrestrialradiation_outputpointer[0] = self.extraterrestrialradiation
        if self._clearskysolarradiation_outputflag:
            self._clearskysolarradiation_outputpointer[0] = self.clearskysolarradiation
@cython.final
cdef class Model(masterinterface.MasterInterface):
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
        self.calc_sunsethourangle_v1()
        self.calc_solartimeangle_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_extraterrestrialradiation_v1()
        self.calc_clearskysolarradiation_v1()
        self.calc_sunshineduration_v1()
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
    cpdef inline void calc_clearskysolarradiation_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil:
        cdef double d_sd
        cdef numpy.int64_t idx
        if self.sequences.fluxes.extraterrestrialradiation > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            d_sd = (                (self.sequences.inputs.globalradiation / self.sequences.fluxes.extraterrestrialradiation)                - self.parameters.control.angstromconstant[idx]            ) * (self.sequences.factors.possiblesunshineduration / self.parameters.control.angstromfactor[idx])
            self.sequences.factors.sunshineduration = min(max(d_sd, 0.0), self.sequences.factors.possiblesunshineduration)
        else:
            self.sequences.factors.sunshineduration = 0.0
    cpdef void process_radiation_v1(self) noexcept nogil:
        if not self.__hydpy_reuse_process_radiation_v1__:
            self.run()
            self.__hydpy_reuse_process_radiation_v1__ = True
    cpdef double get_possiblesunshineduration_v1(self) noexcept nogil:
        return self.sequences.factors.possiblesunshineduration
    cpdef double get_sunshineduration_v1(self) noexcept nogil:
        return self.sequences.factors.sunshineduration
    cpdef double get_clearskysolarradiation_v1(self) noexcept nogil:
        return self.sequences.fluxes.clearskysolarradiation
    cpdef double get_globalradiation_v2(self) noexcept nogil:
        return self.sequences.inputs.globalradiation
    cpdef inline void calc_earthsundistance(self) noexcept nogil:
        self.sequences.factors.earthsundistance = 1.0 + 0.033 * cos(            2 * self.parameters.fixed.pi / 366.0 * (self.parameters.derived.doy[self.idx_sim] + 1)        )
    cpdef inline void calc_solardeclination(self) noexcept nogil:
        self.sequences.factors.solardeclination = 0.409 * sin(            2 * self.parameters.fixed.pi / 366 * (self.parameters.derived.doy[self.idx_sim] + 1) - 1.39        )
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
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil:
        cdef double d_thresh
        if self.parameters.derived.hours < 24.0:
            if self.sequences.factors.solartimeangle <= 0.0:
                d_thresh = -self.sequences.factors.solartimeangle - self.parameters.fixed.pi * self.parameters.derived.days
            else:
                d_thresh = self.sequences.factors.solartimeangle - self.parameters.fixed.pi * self.parameters.derived.days
            self.sequences.factors.possiblesunshineduration = min(                max(12.0 / self.parameters.fixed.pi * (self.sequences.factors.sunsethourangle - d_thresh), 0.0), self.parameters.derived.hours            )
        else:
            self.sequences.factors.possiblesunshineduration = 24.0 / self.parameters.fixed.pi * self.sequences.factors.sunsethourangle
    cpdef inline void calc_extraterrestrialradiation(self) noexcept nogil:
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
    cpdef inline void calc_clearskysolarradiation(self) noexcept nogil:
        cdef numpy.int64_t idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void calc_sunshineduration(self) noexcept nogil:
        cdef double d_sd
        cdef numpy.int64_t idx
        if self.sequences.fluxes.extraterrestrialradiation > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            d_sd = (                (self.sequences.inputs.globalradiation / self.sequences.fluxes.extraterrestrialradiation)                - self.parameters.control.angstromconstant[idx]            ) * (self.sequences.factors.possiblesunshineduration / self.parameters.control.angstromfactor[idx])
            self.sequences.factors.sunshineduration = min(max(d_sd, 0.0), self.sequences.factors.possiblesunshineduration)
        else:
            self.sequences.factors.sunshineduration = 0.0
    cpdef void process_radiation(self) noexcept nogil:
        if not self.__hydpy_reuse_process_radiation_v1__:
            self.run()
            self.__hydpy_reuse_process_radiation_v1__ = True
    cpdef double get_possiblesunshineduration(self) noexcept nogil:
        return self.sequences.factors.possiblesunshineduration
    cpdef double get_sunshineduration(self) noexcept nogil:
        return self.sequences.factors.sunshineduration
    cpdef double get_clearskysolarradiation(self) noexcept nogil:
        return self.sequences.fluxes.clearskysolarradiation
    cpdef double get_globalradiation(self) noexcept nogil:
        return self.sequences.inputs.globalradiation
