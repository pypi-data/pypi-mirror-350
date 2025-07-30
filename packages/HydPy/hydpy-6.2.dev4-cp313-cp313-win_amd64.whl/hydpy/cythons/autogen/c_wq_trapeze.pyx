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
cdef class Sequences:
    pass
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterdepth_diskflag_reading:
            self.waterdepth = self._waterdepth_ncarray[0]
        elif self._waterdepth_ramflag:
            self.waterdepth = self._waterdepth_array[idx]
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
        if self._wettedareas_diskflag_reading:
            k = 0
            for jdx0 in range(self._wettedareas_length_0):
                self.wettedareas[jdx0] = self._wettedareas_ncarray[k]
                k += 1
        elif self._wettedareas_ramflag:
            for jdx0 in range(self._wettedareas_length_0):
                self.wettedareas[jdx0] = self._wettedareas_array[idx, jdx0]
        if self._wettedarea_diskflag_reading:
            self.wettedarea = self._wettedarea_ncarray[0]
        elif self._wettedarea_ramflag:
            self.wettedarea = self._wettedarea_array[idx]
        if self._wettedperimeters_diskflag_reading:
            k = 0
            for jdx0 in range(self._wettedperimeters_length_0):
                self.wettedperimeters[jdx0] = self._wettedperimeters_ncarray[k]
                k += 1
        elif self._wettedperimeters_ramflag:
            for jdx0 in range(self._wettedperimeters_length_0):
                self.wettedperimeters[jdx0] = self._wettedperimeters_array[idx, jdx0]
        if self._wettedperimeter_diskflag_reading:
            self.wettedperimeter = self._wettedperimeter_ncarray[0]
        elif self._wettedperimeter_ramflag:
            self.wettedperimeter = self._wettedperimeter_array[idx]
        if self._wettedperimeterderivatives_diskflag_reading:
            k = 0
            for jdx0 in range(self._wettedperimeterderivatives_length_0):
                self.wettedperimeterderivatives[jdx0] = self._wettedperimeterderivatives_ncarray[k]
                k += 1
        elif self._wettedperimeterderivatives_ramflag:
            for jdx0 in range(self._wettedperimeterderivatives_length_0):
                self.wettedperimeterderivatives[jdx0] = self._wettedperimeterderivatives_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterdepth_diskflag_writing:
            self._waterdepth_ncarray[0] = self.waterdepth
        if self._waterdepth_ramflag:
            self._waterdepth_array[idx] = self.waterdepth
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
        if self._wettedareas_diskflag_writing:
            k = 0
            for jdx0 in range(self._wettedareas_length_0):
                self._wettedareas_ncarray[k] = self.wettedareas[jdx0]
                k += 1
        if self._wettedareas_ramflag:
            for jdx0 in range(self._wettedareas_length_0):
                self._wettedareas_array[idx, jdx0] = self.wettedareas[jdx0]
        if self._wettedarea_diskflag_writing:
            self._wettedarea_ncarray[0] = self.wettedarea
        if self._wettedarea_ramflag:
            self._wettedarea_array[idx] = self.wettedarea
        if self._wettedperimeters_diskflag_writing:
            k = 0
            for jdx0 in range(self._wettedperimeters_length_0):
                self._wettedperimeters_ncarray[k] = self.wettedperimeters[jdx0]
                k += 1
        if self._wettedperimeters_ramflag:
            for jdx0 in range(self._wettedperimeters_length_0):
                self._wettedperimeters_array[idx, jdx0] = self.wettedperimeters[jdx0]
        if self._wettedperimeter_diskflag_writing:
            self._wettedperimeter_ncarray[0] = self.wettedperimeter
        if self._wettedperimeter_ramflag:
            self._wettedperimeter_array[idx] = self.wettedperimeter
        if self._wettedperimeterderivatives_diskflag_writing:
            k = 0
            for jdx0 in range(self._wettedperimeterderivatives_length_0):
                self._wettedperimeterderivatives_ncarray[k] = self.wettedperimeterderivatives[jdx0]
                k += 1
        if self._wettedperimeterderivatives_ramflag:
            for jdx0 in range(self._wettedperimeterderivatives_length_0):
                self._wettedperimeterderivatives_array[idx, jdx0] = self.wettedperimeterderivatives[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "waterdepth":
            self._waterdepth_outputpointer = value.p_value
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
        if name == "wettedarea":
            self._wettedarea_outputpointer = value.p_value
        if name == "wettedperimeter":
            self._wettedperimeter_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._waterdepth_outputflag:
            self._waterdepth_outputpointer[0] = self.waterdepth
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
        if self._wettedarea_outputflag:
            self._wettedarea_outputpointer[0] = self.wettedarea
        if self._wettedperimeter_outputflag:
            self._wettedperimeter_outputpointer[0] = self.wettedperimeter
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
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
        pass
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        pass
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
    cpdef double get_waterdepth_v1(self) noexcept nogil:
        return self.sequences.factors.waterdepth
    cpdef double get_waterlevel_v1(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef double get_wettedarea_v1(self) noexcept nogil:
        return self.sequences.factors.wettedarea
    cpdef double get_wettedperimeter_v1(self) noexcept nogil:
        return self.sequences.factors.wettedperimeter
    cpdef inline void set_waterdepth_v1(self, double waterdepth) noexcept nogil:
        self.sequences.factors.waterdepth = waterdepth
    cpdef inline void set_waterlevel_v1(self, double waterlevel) noexcept nogil:
        self.sequences.factors.waterlevel = waterlevel
    cpdef inline void set_wettedarea_v1(self, double wettedarea) noexcept nogil:
        self.sequences.factors.wettedarea = wettedarea
    cpdef inline void calc_waterdepth_v1(self) noexcept nogil:
        self.sequences.factors.waterdepth = max(self.sequences.factors.waterlevel - self.parameters.control.bottomlevels[0], 0.0)
    cpdef inline void calc_waterdepth_v2(self) noexcept nogil:
        cdef double ss
        cdef numpy.int64_t i
        cdef double w
        cdef double d
        cdef double a
        a = self.sequences.factors.wettedarea
        d = 0.0
        w = 0.0
        for i in range(self.parameters.control.nmbtrapezes):
            if a > self.parameters.derived.trapezeareas[i]:
                a = a - (self.parameters.derived.trapezeareas[i])
                d = d + (self.parameters.derived.trapezeheights[i])
                w = w + (self.parameters.control.bottomwidths[i] + self.parameters.derived.slopewidths[i])
            else:
                if a > 0.0:
                    w = w + (self.parameters.control.bottomwidths[i])
                    ss = self.parameters.control.sideslopes[i]
                    if ss > 1e-10:
                        d = d + (((4.0 * ss * a + w**2.0) ** 0.5 - w) / (2.0 * ss))
                    else:
                        d = d + (a / w)
                self.sequences.factors.waterdepth = d
                break
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterdepth + self.parameters.control.bottomlevels[0]
    cpdef inline void calc_wettedareas_v1(self) noexcept nogil:
        cdef double ws
        cdef double ss
        cdef double wb
        cdef double ht
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedareas[i] = 0.0
            else:
                ht = self.parameters.derived.trapezeheights[i]
                wb = self.parameters.control.bottomwidths[i]
                if d < ht:
                    ss = self.parameters.control.sideslopes[i]
                    self.sequences.factors.wettedareas[i] = (wb + ss * d) * d
                else:
                    ws = self.parameters.derived.slopewidths[i]
                    self.sequences.factors.wettedareas[i] = (wb + ws / 2.0) * ht + (wb + ws) * (d - ht)
    cpdef inline void calc_wettedarea_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.factors.wettedarea = 0.0
        for i in range(self.parameters.control.nmbtrapezes):
            self.sequences.factors.wettedarea = self.sequences.factors.wettedarea + (self.sequences.factors.wettedareas[i])
    cpdef inline void calc_wettedperimeters_v1(self) noexcept nogil:
        cdef double ss
        cdef double wb
        cdef double ht
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedperimeters[i] = 0.0
            else:
                ht = self.parameters.derived.trapezeheights[i]
                wb = self.parameters.control.bottomwidths[i]
                ss = self.parameters.control.sideslopes[i]
                if d < ht:
                    self.sequences.factors.wettedperimeters[i] = wb + 2.0 * d * (ss**2.0 + 1.0) ** 0.5
                else:
                    self.sequences.factors.wettedperimeters[i] = (                        wb + 2.0 * ht * (ss**2.0 + 1.0) ** 0.5 + 2.0 * (d - ht)                    )
    cpdef inline void calc_wettedperimeter_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.factors.wettedperimeter = 0.0
        for i in range(self.parameters.control.nmbtrapezes):
            self.sequences.factors.wettedperimeter = self.sequences.factors.wettedperimeter + (self.sequences.factors.wettedperimeters[i])
    cpdef inline void calc_wettedperimeterderivatives_v1(self) noexcept nogil:
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedperimeterderivatives[i] = 0.0
            elif d < self.parameters.derived.trapezeheights[i]:
                self.sequences.factors.wettedperimeterderivatives[i] = self.parameters.derived.perimeterderivatives[i]
            else:
                self.sequences.factors.wettedperimeterderivatives[i] = 2.0
    cpdef double get_waterdepth(self) noexcept nogil:
        return self.sequences.factors.waterdepth
    cpdef double get_waterlevel(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef double get_wettedarea(self) noexcept nogil:
        return self.sequences.factors.wettedarea
    cpdef double get_wettedperimeter(self) noexcept nogil:
        return self.sequences.factors.wettedperimeter
    cpdef inline void set_waterdepth(self, double waterdepth) noexcept nogil:
        self.sequences.factors.waterdepth = waterdepth
    cpdef inline void set_waterlevel(self, double waterlevel) noexcept nogil:
        self.sequences.factors.waterlevel = waterlevel
    cpdef inline void set_wettedarea(self, double wettedarea) noexcept nogil:
        self.sequences.factors.wettedarea = wettedarea
    cpdef inline void calc_waterlevel(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterdepth + self.parameters.control.bottomlevels[0]
    cpdef inline void calc_wettedareas(self) noexcept nogil:
        cdef double ws
        cdef double ss
        cdef double wb
        cdef double ht
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedareas[i] = 0.0
            else:
                ht = self.parameters.derived.trapezeheights[i]
                wb = self.parameters.control.bottomwidths[i]
                if d < ht:
                    ss = self.parameters.control.sideslopes[i]
                    self.sequences.factors.wettedareas[i] = (wb + ss * d) * d
                else:
                    ws = self.parameters.derived.slopewidths[i]
                    self.sequences.factors.wettedareas[i] = (wb + ws / 2.0) * ht + (wb + ws) * (d - ht)
    cpdef inline void calc_wettedarea(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.factors.wettedarea = 0.0
        for i in range(self.parameters.control.nmbtrapezes):
            self.sequences.factors.wettedarea = self.sequences.factors.wettedarea + (self.sequences.factors.wettedareas[i])
    cpdef inline void calc_wettedperimeters(self) noexcept nogil:
        cdef double ss
        cdef double wb
        cdef double ht
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedperimeters[i] = 0.0
            else:
                ht = self.parameters.derived.trapezeheights[i]
                wb = self.parameters.control.bottomwidths[i]
                ss = self.parameters.control.sideslopes[i]
                if d < ht:
                    self.sequences.factors.wettedperimeters[i] = wb + 2.0 * d * (ss**2.0 + 1.0) ** 0.5
                else:
                    self.sequences.factors.wettedperimeters[i] = (                        wb + 2.0 * ht * (ss**2.0 + 1.0) ** 0.5 + 2.0 * (d - ht)                    )
    cpdef inline void calc_wettedperimeter(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.factors.wettedperimeter = 0.0
        for i in range(self.parameters.control.nmbtrapezes):
            self.sequences.factors.wettedperimeter = self.sequences.factors.wettedperimeter + (self.sequences.factors.wettedperimeters[i])
    cpdef inline void calc_wettedperimeterderivatives(self) noexcept nogil:
        cdef double d
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbtrapezes):
            d = self.sequences.factors.waterdepth - self.parameters.derived.bottomdepths[i]
            if d < 0.0:
                self.sequences.factors.wettedperimeterderivatives[i] = 0.0
            elif d < self.parameters.derived.trapezeheights[i]:
                self.sequences.factors.wettedperimeterderivatives[i] = self.parameters.derived.perimeterderivatives[i]
            else:
                self.sequences.factors.wettedperimeterderivatives[i] = 2.0
    cpdef void use_waterdepth_v2(self, double waterdepth) noexcept nogil:
        self.set_waterdepth_v1(waterdepth)
        self.calc_waterlevel_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
    cpdef void use_waterlevel_v2(self, double waterlevel) noexcept nogil:
        self.set_waterlevel_v1(waterlevel)
        self.calc_waterdepth_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
    cpdef void use_wettedarea_v1(self, double wettedarea) noexcept nogil:
        self.set_wettedarea_v1(wettedarea)
        self.calc_waterdepth_v2()
        self.calc_waterlevel_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
    cpdef void use_waterdepth(self, double waterdepth) noexcept nogil:
        self.set_waterdepth_v1(waterdepth)
        self.calc_waterlevel_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
    cpdef void use_waterlevel(self, double waterlevel) noexcept nogil:
        self.set_waterlevel_v1(waterlevel)
        self.calc_waterdepth_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
    cpdef void use_wettedarea(self, double wettedarea) noexcept nogil:
        self.set_wettedarea_v1(wettedarea)
        self.calc_waterdepth_v2()
        self.calc_waterlevel_v1()
        self.calc_wettedareas_v1()
        self.calc_wettedarea_v1()
        self.calc_wettedperimeters_v1()
        self.calc_wettedperimeter_v1()
