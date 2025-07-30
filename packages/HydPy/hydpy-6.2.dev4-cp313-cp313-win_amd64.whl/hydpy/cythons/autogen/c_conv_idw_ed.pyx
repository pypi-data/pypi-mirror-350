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
        if self._inputs_diskflag_reading:
            k = 0
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_ncarray[k]
                k += 1
        elif self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._inputs_length_0):
                self._inputs_ncarray[k] = self.inputs[jdx0]
                k += 1
        if self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self._inputs_array[idx, jdx0] = self.inputs[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "inputs":
            self._inputs_length_0 = length
            self._inputs_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._inputs_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "inputs":
            PyMem_Free(self._inputs_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "inputs":
            self._inputs_pointer[idx] = pointer.p_value
            self._inputs_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "inputs":
            values = numpy.empty(self.len_inputs)
            for idx in range(self.len_inputs):
                pointerutils.check0(self._inputs_length_0)
                if self._inputs_ready[idx] == 0:
                    pointerutils.check1(self._inputs_length_0, idx)
                    pointerutils.check2(self._inputs_ready, idx)
                values[idx] = self._inputs_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "inputs":
            for idx in range(self.len_inputs):
                pointerutils.check0(self._inputs_length_0)
                if self._inputs_ready[idx] == 0:
                    pointerutils.check1(self._inputs_length_0, idx)
                    pointerutils.check2(self._inputs_ready, idx)
                self._inputs_pointer[idx][0] = value[idx]
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inputs_diskflag_reading:
            k = 0
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_ncarray[k]
                k += 1
        elif self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_array[idx, jdx0]
        if self._actualconstant_diskflag_reading:
            self.actualconstant = self._actualconstant_ncarray[0]
        elif self._actualconstant_ramflag:
            self.actualconstant = self._actualconstant_array[idx]
        if self._actualfactor_diskflag_reading:
            self.actualfactor = self._actualfactor_ncarray[0]
        elif self._actualfactor_ramflag:
            self.actualfactor = self._actualfactor_array[idx]
        if self._inputpredictions_diskflag_reading:
            k = 0
            for jdx0 in range(self._inputpredictions_length_0):
                self.inputpredictions[jdx0] = self._inputpredictions_ncarray[k]
                k += 1
        elif self._inputpredictions_ramflag:
            for jdx0 in range(self._inputpredictions_length_0):
                self.inputpredictions[jdx0] = self._inputpredictions_array[idx, jdx0]
        if self._outputpredictions_diskflag_reading:
            k = 0
            for jdx0 in range(self._outputpredictions_length_0):
                self.outputpredictions[jdx0] = self._outputpredictions_ncarray[k]
                k += 1
        elif self._outputpredictions_ramflag:
            for jdx0 in range(self._outputpredictions_length_0):
                self.outputpredictions[jdx0] = self._outputpredictions_array[idx, jdx0]
        if self._inputresiduals_diskflag_reading:
            k = 0
            for jdx0 in range(self._inputresiduals_length_0):
                self.inputresiduals[jdx0] = self._inputresiduals_ncarray[k]
                k += 1
        elif self._inputresiduals_ramflag:
            for jdx0 in range(self._inputresiduals_length_0):
                self.inputresiduals[jdx0] = self._inputresiduals_array[idx, jdx0]
        if self._outputresiduals_diskflag_reading:
            k = 0
            for jdx0 in range(self._outputresiduals_length_0):
                self.outputresiduals[jdx0] = self._outputresiduals_ncarray[k]
                k += 1
        elif self._outputresiduals_ramflag:
            for jdx0 in range(self._outputresiduals_length_0):
                self.outputresiduals[jdx0] = self._outputresiduals_array[idx, jdx0]
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
        if self._inputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._inputs_length_0):
                self._inputs_ncarray[k] = self.inputs[jdx0]
                k += 1
        if self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self._inputs_array[idx, jdx0] = self.inputs[jdx0]
        if self._actualconstant_diskflag_writing:
            self._actualconstant_ncarray[0] = self.actualconstant
        if self._actualconstant_ramflag:
            self._actualconstant_array[idx] = self.actualconstant
        if self._actualfactor_diskflag_writing:
            self._actualfactor_ncarray[0] = self.actualfactor
        if self._actualfactor_ramflag:
            self._actualfactor_array[idx] = self.actualfactor
        if self._inputpredictions_diskflag_writing:
            k = 0
            for jdx0 in range(self._inputpredictions_length_0):
                self._inputpredictions_ncarray[k] = self.inputpredictions[jdx0]
                k += 1
        if self._inputpredictions_ramflag:
            for jdx0 in range(self._inputpredictions_length_0):
                self._inputpredictions_array[idx, jdx0] = self.inputpredictions[jdx0]
        if self._outputpredictions_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputpredictions_length_0):
                self._outputpredictions_ncarray[k] = self.outputpredictions[jdx0]
                k += 1
        if self._outputpredictions_ramflag:
            for jdx0 in range(self._outputpredictions_length_0):
                self._outputpredictions_array[idx, jdx0] = self.outputpredictions[jdx0]
        if self._inputresiduals_diskflag_writing:
            k = 0
            for jdx0 in range(self._inputresiduals_length_0):
                self._inputresiduals_ncarray[k] = self.inputresiduals[jdx0]
                k += 1
        if self._inputresiduals_ramflag:
            for jdx0 in range(self._inputresiduals_length_0):
                self._inputresiduals_array[idx, jdx0] = self.inputresiduals[jdx0]
        if self._outputresiduals_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputresiduals_length_0):
                self._outputresiduals_ncarray[k] = self.outputresiduals[jdx0]
                k += 1
        if self._outputresiduals_ramflag:
            for jdx0 in range(self._outputresiduals_length_0):
                self._outputresiduals_array[idx, jdx0] = self.outputresiduals[jdx0]
        if self._outputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self._outputs_ncarray[k] = self.outputs[jdx0]
                k += 1
        if self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "actualconstant":
            self._actualconstant_outputpointer = value.p_value
        if name == "actualfactor":
            self._actualfactor_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._actualconstant_outputflag:
            self._actualconstant_outputpointer[0] = self.actualconstant
        if self._actualfactor_outputflag:
            self._actualfactor_outputpointer[0] = self.actualfactor
@cython.final
cdef class OutletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
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
        if self._outputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self._outputs_ncarray[k] = self.outputs[jdx0]
                k += 1
        if self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "outputs":
            self._outputs_length_0 = length
            self._outputs_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._outputs_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "outputs":
            PyMem_Free(self._outputs_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "outputs":
            self._outputs_pointer[idx] = pointer.p_value
            self._outputs_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "outputs":
            values = numpy.empty(self.len_outputs)
            for idx in range(self.len_outputs):
                pointerutils.check0(self._outputs_length_0)
                if self._outputs_ready[idx] == 0:
                    pointerutils.check1(self._outputs_length_0, idx)
                    pointerutils.check2(self._outputs_ready, idx)
                values[idx] = self._outputs_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "outputs":
            for idx in range(self.len_outputs):
                pointerutils.check0(self._outputs_length_0)
                if self._outputs_ready[idx] == 0:
                    pointerutils.check1(self._outputs_length_0, idx)
                    pointerutils.check2(self._outputs_ready, idx)
                self._outputs_pointer[idx][0] = value[idx]
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
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.calc_actualconstant_actualfactor_v1()
        self.calc_inputpredictions_v1()
        self.calc_outputpredictions_v1()
        self.calc_inputresiduals_v1()
        self.calc_outputresiduals_v1()
        self.calc_outputs_v3()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._inputs_length_0):
                if self.sequences.inlets._inputs_ready[i]:
                    self.sequences.inlets.inputs[i] = self.sequences.inlets._inputs_pointer[i][0]
                else:
                    self.sequences.inlets.inputs[i] = nan
        self.pick_inputs_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_outputs_v1()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.outlets._outputs_length_0):
                if self.sequences.outlets._outputs_ready[i]:
                    self.sequences.outlets._outputs_pointer[i][0] = self.sequences.outlets._outputs_pointer[i][0] + self.sequences.outlets.outputs[i]
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
            self.sequences.fluxes.update_outputs()
    cpdef inline void pick_inputs_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx]
    cpdef inline void calc_actualconstant_actualfactor_v1(self) noexcept nogil:
        cdef double d_temp
        cdef double d_denominator
        cdef double d_nominator
        cdef double d_mean_inputs
        cdef double d_mean_height
        cdef numpy.int64_t idx
        cdef numpy.int64_t counter
        counter = 0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                counter = counter + (1)
                if counter == self.parameters.control.minnmbinputs:
                    break
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
            return
        d_mean_height = self.return_mean_v1(            self.parameters.control.inputheights, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs        )
        d_mean_inputs = self.return_mean_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs)
        d_nominator = 0.0
        d_denominator = 0.0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                d_temp = self.parameters.control.inputheights[idx] - d_mean_height
                d_nominator = d_nominator + (d_temp * (self.sequences.fluxes.inputs[idx] - d_mean_inputs))
                d_denominator = d_denominator + (d_temp * d_temp)
        if d_denominator > 0.0:
            self.sequences.fluxes.actualfactor = d_nominator / d_denominator
            self.sequences.fluxes.actualconstant = d_mean_inputs - self.sequences.fluxes.actualfactor * d_mean_height
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
        return
    cpdef inline void calc_inputpredictions_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.inputheights[idx]            )
    cpdef inline void calc_outputpredictions_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.outputheights[idx]            )
    cpdef inline void calc_inputresiduals_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputresiduals[idx] = self.sequences.fluxes.inputs[idx] - self.sequences.fluxes.inputpredictions[idx]
    cpdef inline void calc_outputresiduals_v1(self) noexcept nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputresiduals, self.sequences.fluxes.outputresiduals)
    cpdef inline void calc_outputs_v3(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputs[idx] = self.sequences.fluxes.outputpredictions[idx] + self.sequences.fluxes.outputresiduals[idx]
    cpdef inline double return_mean_v1(self, double[:] values, double[:] mask, numpy.int64_t number) noexcept nogil:
        cdef numpy.int64_t idx
        cdef double d_result
        cdef numpy.int64_t counter
        counter = 0
        d_result = 0.0
        for idx in range(number):
            if not isnan(mask[idx]):
                counter = counter + (1)
                d_result = d_result + (values[idx])
        if counter > 0:
            return d_result / counter
        return nan
    cpdef inline void interpolate_inversedistance_v1(self, double[:] inputs, double[:] outputs) noexcept nogil:
        cdef numpy.int64_t idx_in
        cdef numpy.int64_t idx_try
        cdef numpy.int64_t counter_inf
        cdef double d_sumvalues_inf
        cdef double d_sumvalues
        cdef double d_sumweights
        cdef numpy.int64_t idx_out
        for idx_out in range(self.parameters.derived.nmboutputs):
            d_sumweights = 0.0
            d_sumvalues = 0.0
            d_sumvalues_inf = 0.0
            counter_inf = 0
            for idx_try in range(self.parameters.control.maxnmbinputs):
                idx_in = self.parameters.derived.proximityorder[idx_out, idx_try]
                if not isnan(inputs[idx_in]):
                    if isinf(self.parameters.derived.weights[idx_out, idx_try]):
                        d_sumvalues_inf = d_sumvalues_inf + (inputs[idx_in])
                        counter_inf = counter_inf + (1)
                    else:
                        d_sumweights = d_sumweights + (self.parameters.derived.weights[idx_out, idx_try])
                        d_sumvalues = d_sumvalues + (self.parameters.derived.weights[idx_out, idx_try] * inputs[idx_in])
            if counter_inf:
                outputs[idx_out] = d_sumvalues_inf / counter_inf
            elif d_sumweights:
                outputs[idx_out] = d_sumvalues / d_sumweights
            else:
                outputs[idx_out] = nan
    cpdef inline void pass_outputs_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.outlets.outputs[idx] = self.sequences.fluxes.outputs[idx]
    cpdef inline void pick_inputs(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx]
    cpdef inline void calc_actualconstant_actualfactor(self) noexcept nogil:
        cdef double d_temp
        cdef double d_denominator
        cdef double d_nominator
        cdef double d_mean_inputs
        cdef double d_mean_height
        cdef numpy.int64_t idx
        cdef numpy.int64_t counter
        counter = 0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                counter = counter + (1)
                if counter == self.parameters.control.minnmbinputs:
                    break
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
            return
        d_mean_height = self.return_mean_v1(            self.parameters.control.inputheights, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs        )
        d_mean_inputs = self.return_mean_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs)
        d_nominator = 0.0
        d_denominator = 0.0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                d_temp = self.parameters.control.inputheights[idx] - d_mean_height
                d_nominator = d_nominator + (d_temp * (self.sequences.fluxes.inputs[idx] - d_mean_inputs))
                d_denominator = d_denominator + (d_temp * d_temp)
        if d_denominator > 0.0:
            self.sequences.fluxes.actualfactor = d_nominator / d_denominator
            self.sequences.fluxes.actualconstant = d_mean_inputs - self.sequences.fluxes.actualfactor * d_mean_height
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
        return
    cpdef inline void calc_inputpredictions(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.inputheights[idx]            )
    cpdef inline void calc_outputpredictions(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.outputheights[idx]            )
    cpdef inline void calc_inputresiduals(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputresiduals[idx] = self.sequences.fluxes.inputs[idx] - self.sequences.fluxes.inputpredictions[idx]
    cpdef inline void calc_outputresiduals(self) noexcept nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputresiduals, self.sequences.fluxes.outputresiduals)
    cpdef inline void calc_outputs(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputs[idx] = self.sequences.fluxes.outputpredictions[idx] + self.sequences.fluxes.outputresiduals[idx]
    cpdef inline double return_mean(self, double[:] values, double[:] mask, numpy.int64_t number) noexcept nogil:
        cdef numpy.int64_t idx
        cdef double d_result
        cdef numpy.int64_t counter
        counter = 0
        d_result = 0.0
        for idx in range(number):
            if not isnan(mask[idx]):
                counter = counter + (1)
                d_result = d_result + (values[idx])
        if counter > 0:
            return d_result / counter
        return nan
    cpdef inline void interpolate_inversedistance(self, double[:] inputs, double[:] outputs) noexcept nogil:
        cdef numpy.int64_t idx_in
        cdef numpy.int64_t idx_try
        cdef numpy.int64_t counter_inf
        cdef double d_sumvalues_inf
        cdef double d_sumvalues
        cdef double d_sumweights
        cdef numpy.int64_t idx_out
        for idx_out in range(self.parameters.derived.nmboutputs):
            d_sumweights = 0.0
            d_sumvalues = 0.0
            d_sumvalues_inf = 0.0
            counter_inf = 0
            for idx_try in range(self.parameters.control.maxnmbinputs):
                idx_in = self.parameters.derived.proximityorder[idx_out, idx_try]
                if not isnan(inputs[idx_in]):
                    if isinf(self.parameters.derived.weights[idx_out, idx_try]):
                        d_sumvalues_inf = d_sumvalues_inf + (inputs[idx_in])
                        counter_inf = counter_inf + (1)
                    else:
                        d_sumweights = d_sumweights + (self.parameters.derived.weights[idx_out, idx_try])
                        d_sumvalues = d_sumvalues + (self.parameters.derived.weights[idx_out, idx_try] * inputs[idx_in])
            if counter_inf:
                outputs[idx_out] = d_sumvalues_inf / counter_inf
            elif d_sumweights:
                outputs[idx_out] = d_sumvalues / d_sumweights
            else:
                outputs[idx_out] = nan
    cpdef inline void pass_outputs(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.outlets.outputs[idx] = self.sequences.fluxes.outputs[idx]
