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
cdef class InletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._total_diskflag_reading:
            k = 0
            for jdx0 in range(self._total_length_0):
                self.total[jdx0] = self._total_ncarray[k]
                k += 1
        elif self._total_ramflag:
            for jdx0 in range(self._total_length_0):
                self.total[jdx0] = self._total_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._total_diskflag_writing:
            k = 0
            for jdx0 in range(self._total_length_0):
                self._total_ncarray[k] = self.total[jdx0]
                k += 1
        if self._total_ramflag:
            for jdx0 in range(self._total_length_0):
                self._total_array[idx, jdx0] = self.total[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "total":
            self._total_length_0 = length
            self._total_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._total_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "total":
            PyMem_Free(self._total_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "total":
            self._total_pointer[idx] = pointer.p_value
            self._total_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "total":
            values = numpy.empty(self.len_total)
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                values[idx] = self._total_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "total":
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                self._total_pointer[idx][0] = value[idx]
@cython.final
cdef class ReceiverSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
        if self._waterlevels_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_ncarray[k]
                k += 1
        elif self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
        if self._waterlevels_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_ncarray[k] = self.waterlevels[jdx0]
                k += 1
        if self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_array[idx, jdx0] = self.waterlevels[jdx0]
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "waterlevel":
            self._waterlevel_pointer = pointer.p_value
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "waterlevels":
            self._waterlevels_length_0 = length
            self._waterlevels_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._waterlevels_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "waterlevels":
            PyMem_Free(self._waterlevels_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "waterlevels":
            self._waterlevels_pointer[idx] = pointer.p_value
            self._waterlevels_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "waterlevel":
            return self._waterlevel_pointer[0]
        if name == "waterlevels":
            values = numpy.empty(self.len_waterlevels)
            for idx in range(self.len_waterlevels):
                pointerutils.check0(self._waterlevels_length_0)
                if self._waterlevels_ready[idx] == 0:
                    pointerutils.check1(self._waterlevels_length_0, idx)
                    pointerutils.check2(self._waterlevels_ready, idx)
                values[idx] = self._waterlevels_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "waterlevel":
            self._waterlevel_pointer[0] = value
        if name == "waterlevels":
            for idx in range(self.len_waterlevels):
                pointerutils.check0(self._waterlevels_length_0)
                if self._waterlevels_ready[idx] == 0:
                    pointerutils.check1(self._waterlevels_length_0, idx)
                    pointerutils.check2(self._waterlevels_ready, idx)
                self._waterlevels_pointer[idx][0] = value[idx]
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevels_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_ncarray[k]
                k += 1
        elif self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_array[idx, jdx0]
        if self._deltawaterlevel_diskflag_reading:
            self.deltawaterlevel = self._deltawaterlevel_ncarray[0]
        elif self._deltawaterlevel_ramflag:
            self.deltawaterlevel = self._deltawaterlevel_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevels_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_ncarray[k] = self.waterlevels[jdx0]
                k += 1
        if self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_array[idx, jdx0] = self.waterlevels[jdx0]
        if self._deltawaterlevel_diskflag_writing:
            self._deltawaterlevel_ncarray[0] = self.deltawaterlevel
        if self._deltawaterlevel_ramflag:
            self._deltawaterlevel_array[idx] = self.deltawaterlevel
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "deltawaterlevel":
            self._deltawaterlevel_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._deltawaterlevel_outputflag:
            self._deltawaterlevel_outputpointer[0] = self.deltawaterlevel
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._potentialexchange_diskflag_reading:
            self.potentialexchange = self._potentialexchange_ncarray[0]
        elif self._potentialexchange_ramflag:
            self.potentialexchange = self._potentialexchange_array[idx]
        if self._actualexchange_diskflag_reading:
            self.actualexchange = self._actualexchange_ncarray[0]
        elif self._actualexchange_ramflag:
            self.actualexchange = self._actualexchange_array[idx]
        if self._originalinput_diskflag_reading:
            self.originalinput = self._originalinput_ncarray[0]
        elif self._originalinput_ramflag:
            self.originalinput = self._originalinput_array[idx]
        if self._adjustedinput_diskflag_reading:
            self.adjustedinput = self._adjustedinput_ncarray[0]
        elif self._adjustedinput_ramflag:
            self.adjustedinput = self._adjustedinput_array[idx]
        if self._outputs_diskflag_reading:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_ncarray[k]
                k += 1
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._potentialexchange_diskflag_writing:
            self._potentialexchange_ncarray[0] = self.potentialexchange
        if self._potentialexchange_ramflag:
            self._potentialexchange_array[idx] = self.potentialexchange
        if self._actualexchange_diskflag_writing:
            self._actualexchange_ncarray[0] = self.actualexchange
        if self._actualexchange_ramflag:
            self._actualexchange_array[idx] = self.actualexchange
        if self._originalinput_diskflag_writing:
            self._originalinput_ncarray[0] = self.originalinput
        if self._originalinput_ramflag:
            self._originalinput_array[idx] = self.originalinput
        if self._adjustedinput_diskflag_writing:
            self._adjustedinput_ncarray[0] = self.adjustedinput
        if self._adjustedinput_ramflag:
            self._adjustedinput_array[idx] = self.adjustedinput
        if self._outputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self._outputs_ncarray[k] = self.outputs[jdx0]
                k += 1
        if self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "potentialexchange":
            self._potentialexchange_outputpointer = value.p_value
        if name == "actualexchange":
            self._actualexchange_outputpointer = value.p_value
        if name == "originalinput":
            self._originalinput_outputpointer = value.p_value
        if name == "adjustedinput":
            self._adjustedinput_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._potentialexchange_outputflag:
            self._potentialexchange_outputpointer[0] = self.potentialexchange
        if self._actualexchange_outputflag:
            self._actualexchange_outputpointer[0] = self.actualexchange
        if self._originalinput_outputflag:
            self._originalinput_outputpointer[0] = self.originalinput
        if self._adjustedinput_outputflag:
            self._adjustedinput_outputpointer[0] = self.adjustedinput
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class OutletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._exchange_diskflag_reading:
            k = 0
            for jdx0 in range(self._exchange_length_0):
                self.exchange[jdx0] = self._exchange_ncarray[k]
                k += 1
        elif self._exchange_ramflag:
            for jdx0 in range(self._exchange_length_0):
                self.exchange[jdx0] = self._exchange_array[idx, jdx0]
        if self._branched_diskflag_reading:
            k = 0
            for jdx0 in range(self._branched_length_0):
                self.branched[jdx0] = self._branched_ncarray[k]
                k += 1
        elif self._branched_ramflag:
            for jdx0 in range(self._branched_length_0):
                self.branched[jdx0] = self._branched_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._exchange_diskflag_writing:
            k = 0
            for jdx0 in range(self._exchange_length_0):
                self._exchange_ncarray[k] = self.exchange[jdx0]
                k += 1
        if self._exchange_ramflag:
            for jdx0 in range(self._exchange_length_0):
                self._exchange_array[idx, jdx0] = self.exchange[jdx0]
        if self._branched_diskflag_writing:
            k = 0
            for jdx0 in range(self._branched_length_0):
                self._branched_ncarray[k] = self.branched[jdx0]
                k += 1
        if self._branched_ramflag:
            for jdx0 in range(self._branched_length_0):
                self._branched_array[idx, jdx0] = self.branched[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "exchange":
            self._exchange_length_0 = length
            self._exchange_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._exchange_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
        if name == "branched":
            self._branched_length_0 = length
            self._branched_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._branched_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "exchange":
            PyMem_Free(self._exchange_pointer)
        if name == "branched":
            PyMem_Free(self._branched_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "exchange":
            self._exchange_pointer[idx] = pointer.p_value
            self._exchange_ready[idx] = 1
        if name == "branched":
            self._branched_pointer[idx] = pointer.p_value
            self._branched_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "exchange":
            values = numpy.empty(self.len_exchange)
            for idx in range(self.len_exchange):
                pointerutils.check0(self._exchange_length_0)
                if self._exchange_ready[idx] == 0:
                    pointerutils.check1(self._exchange_length_0, idx)
                    pointerutils.check2(self._exchange_ready, idx)
                values[idx] = self._exchange_pointer[idx][0]
            return values
        if name == "branched":
            values = numpy.empty(self.len_branched)
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                values[idx] = self._branched_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "exchange":
            for idx in range(self.len_exchange):
                pointerutils.check0(self._exchange_length_0)
                if self._exchange_ready[idx] == 0:
                    pointerutils.check1(self._exchange_length_0, idx)
                    pointerutils.check2(self._exchange_ready, idx)
                self._exchange_pointer[idx][0] = value[idx]
        if name == "branched":
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                self._branched_pointer[idx][0] = value[idx]
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.update_inlets()
        self.run()
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
        pass
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        self.sequences.receivers.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.receivers.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.update_waterlevels_v1()
        self.calc_deltawaterlevel_v1()
        self.calc_potentialexchange_v1()
        self.calc_actualexchange_v1()
        self.calc_adjustedinput_v1()
        self.calc_outputs_v1()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._total_length_0):
                if self.sequences.inlets._total_ready[i]:
                    self.sequences.inlets.total[i] = self.sequences.inlets._total_pointer[i][0]
                else:
                    self.sequences.inlets.total[i] = nan
        self.pick_originalinput_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_actualexchange_v1()
        self.pass_outputs_v1()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.outlets._exchange_length_0):
                if self.sequences.outlets._exchange_ready[i]:
                    self.sequences.outlets._exchange_pointer[i][0] = self.sequences.outlets._exchange_pointer[i][0] + self.sequences.outlets.exchange[i]
        if not self.threading:
            for i in range(self.sequences.outlets._branched_length_0):
                if self.sequences.outlets._branched_ready[i]:
                    self.sequences.outlets._branched_pointer[i][0] = self.sequences.outlets._branched_pointer[i][0] + self.sequences.outlets.branched[i]
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.receivers.waterlevel = self.sequences.receivers._waterlevel_pointer[0]
        if not self.threading:
            for i in range(self.sequences.receivers._waterlevels_length_0):
                if self.sequences.receivers._waterlevels_ready[i]:
                    self.sequences.receivers.waterlevels[i] = self.sequences.receivers._waterlevels_pointer[i][0]
                else:
                    self.sequences.receivers.waterlevels[i] = nan
        self.pick_loggedwaterlevel_v1()
        self.pic_loggedwaterlevels_v1()
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
    cpdef inline void pick_loggedwaterlevel_v1(self) noexcept nogil:
        self.sequences.logs.loggedwaterlevel[0] = self.sequences.receivers.waterlevel
    cpdef inline void pic_loggedwaterlevels_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(2):
            self.sequences.logs.loggedwaterlevels[idx] = self.sequences.receivers.waterlevels[idx]
    cpdef inline void pick_originalinput_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.originalinput = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.originalinput = self.sequences.fluxes.originalinput + (self.sequences.inlets.total[idx])
    cpdef inline void update_waterlevels_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(2):
            self.sequences.factors.waterlevels[idx] = self.sequences.logs.loggedwaterlevels[idx]
    cpdef inline void calc_deltawaterlevel_v1(self) noexcept nogil:
        cdef double d_wl1
        cdef double d_wl0
        d_wl0 = max(self.sequences.factors.waterlevels[0], self.parameters.control.crestheight)
        d_wl1 = max(self.sequences.factors.waterlevels[1], self.parameters.control.crestheight)
        self.sequences.factors.deltawaterlevel = d_wl0 - d_wl1
    cpdef inline void calc_potentialexchange_v1(self) noexcept nogil:
        cdef double d_sig
        cdef double d_dwl
        if self.sequences.factors.deltawaterlevel >= 0.0:
            d_dwl = self.sequences.factors.deltawaterlevel
            d_sig = 1.0
        else:
            d_dwl = -self.sequences.factors.deltawaterlevel
            d_sig = -1.0
        self.sequences.fluxes.potentialexchange = d_sig * (            self.parameters.control.flowcoefficient * self.parameters.control.crestwidth * d_dwl**self.parameters.control.flowexponent        )
    cpdef inline void calc_actualexchange_v1(self) noexcept nogil:
        if self.sequences.fluxes.potentialexchange >= 0.0:
            self.sequences.fluxes.actualexchange = min(self.sequences.fluxes.potentialexchange, self.parameters.control.allowedexchange)
        else:
            self.sequences.fluxes.actualexchange = max(self.sequences.fluxes.potentialexchange, -self.parameters.control.allowedexchange)
    cpdef inline void calc_adjustedinput_v1(self) noexcept nogil:
        self.sequences.fluxes.adjustedinput = self.sequences.fluxes.originalinput + self.parameters.control.delta[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.adjustedinput = max(self.sequences.fluxes.adjustedinput, self.parameters.control.minimum)
    cpdef inline void calc_outputs_v1(self) noexcept nogil:
        cdef double d_dy
        cdef double d_y0
        cdef double d_dx
        cdef double d_x0
        cdef numpy.int64_t bdx
        cdef double d_x
        cdef numpy.int64_t pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.adjustedinput:
                break
        d_x = self.sequences.fluxes.adjustedinput
        for bdx in range(self.parameters.derived.nmbbranches):
            d_x0 = self.parameters.control.xpoints[pdx - 1]
            d_dx = self.parameters.control.xpoints[pdx] - d_x0
            d_y0 = self.parameters.control.ypoints[bdx, pdx - 1]
            d_dy = self.parameters.control.ypoints[bdx, pdx] - d_y0
            self.sequences.fluxes.outputs[bdx] = (d_x - d_x0) * d_dy / d_dx + d_y0
    cpdef double get_waterlevel_v1(self) noexcept nogil:
        return self.sequences.logs.loggedwaterlevel[0]
    cpdef inline void pass_actualexchange_v1(self) noexcept nogil:
        self.sequences.outlets.exchange[0] = -self.sequences.fluxes.actualexchange
        self.sequences.outlets.exchange[1] = self.sequences.fluxes.actualexchange
    cpdef inline void pass_outputs_v1(self) noexcept nogil:
        cdef numpy.int64_t bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx] = self.sequences.fluxes.outputs[bdx]
    cpdef inline void pick_loggedwaterlevel(self) noexcept nogil:
        self.sequences.logs.loggedwaterlevel[0] = self.sequences.receivers.waterlevel
    cpdef inline void pic_loggedwaterlevels(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(2):
            self.sequences.logs.loggedwaterlevels[idx] = self.sequences.receivers.waterlevels[idx]
    cpdef inline void pick_originalinput(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.originalinput = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.originalinput = self.sequences.fluxes.originalinput + (self.sequences.inlets.total[idx])
    cpdef inline void update_waterlevels(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(2):
            self.sequences.factors.waterlevels[idx] = self.sequences.logs.loggedwaterlevels[idx]
    cpdef inline void calc_deltawaterlevel(self) noexcept nogil:
        cdef double d_wl1
        cdef double d_wl0
        d_wl0 = max(self.sequences.factors.waterlevels[0], self.parameters.control.crestheight)
        d_wl1 = max(self.sequences.factors.waterlevels[1], self.parameters.control.crestheight)
        self.sequences.factors.deltawaterlevel = d_wl0 - d_wl1
    cpdef inline void calc_potentialexchange(self) noexcept nogil:
        cdef double d_sig
        cdef double d_dwl
        if self.sequences.factors.deltawaterlevel >= 0.0:
            d_dwl = self.sequences.factors.deltawaterlevel
            d_sig = 1.0
        else:
            d_dwl = -self.sequences.factors.deltawaterlevel
            d_sig = -1.0
        self.sequences.fluxes.potentialexchange = d_sig * (            self.parameters.control.flowcoefficient * self.parameters.control.crestwidth * d_dwl**self.parameters.control.flowexponent        )
    cpdef inline void calc_actualexchange(self) noexcept nogil:
        if self.sequences.fluxes.potentialexchange >= 0.0:
            self.sequences.fluxes.actualexchange = min(self.sequences.fluxes.potentialexchange, self.parameters.control.allowedexchange)
        else:
            self.sequences.fluxes.actualexchange = max(self.sequences.fluxes.potentialexchange, -self.parameters.control.allowedexchange)
    cpdef inline void calc_adjustedinput(self) noexcept nogil:
        self.sequences.fluxes.adjustedinput = self.sequences.fluxes.originalinput + self.parameters.control.delta[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.adjustedinput = max(self.sequences.fluxes.adjustedinput, self.parameters.control.minimum)
    cpdef inline void calc_outputs(self) noexcept nogil:
        cdef double d_dy
        cdef double d_y0
        cdef double d_dx
        cdef double d_x0
        cdef numpy.int64_t bdx
        cdef double d_x
        cdef numpy.int64_t pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.adjustedinput:
                break
        d_x = self.sequences.fluxes.adjustedinput
        for bdx in range(self.parameters.derived.nmbbranches):
            d_x0 = self.parameters.control.xpoints[pdx - 1]
            d_dx = self.parameters.control.xpoints[pdx] - d_x0
            d_y0 = self.parameters.control.ypoints[bdx, pdx - 1]
            d_dy = self.parameters.control.ypoints[bdx, pdx] - d_y0
            self.sequences.fluxes.outputs[bdx] = (d_x - d_x0) * d_dy / d_dx + d_y0
    cpdef double get_waterlevel(self) noexcept nogil:
        return self.sequences.logs.loggedwaterlevel[0]
    cpdef inline void pass_actualexchange(self) noexcept nogil:
        self.sequences.outlets.exchange[0] = -self.sequences.fluxes.actualexchange
        self.sequences.outlets.exchange[1] = self.sequences.fluxes.actualexchange
    cpdef inline void pass_outputs(self) noexcept nogil:
        cdef numpy.int64_t bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx] = self.sequences.fluxes.outputs[bdx]
