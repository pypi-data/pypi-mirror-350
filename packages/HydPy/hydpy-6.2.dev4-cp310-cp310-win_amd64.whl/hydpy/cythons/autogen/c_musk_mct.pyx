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

cdef public numpy.npy_bool TYPE_CHECKING = False
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
cdef class SolverParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            k = 0
            for jdx0 in range(self._q_length_0):
                self.q[jdx0] = self._q_ncarray[k]
                k += 1
        elif self._q_ramflag:
            for jdx0 in range(self._q_length_0):
                self.q[jdx0] = self._q_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            k = 0
            for jdx0 in range(self._q_length_0):
                self._q_ncarray[k] = self.q[jdx0]
                k += 1
        if self._q_ramflag:
            for jdx0 in range(self._q_length_0):
                self._q_array[idx, jdx0] = self.q[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "q":
            self._q_length_0 = length
            self._q_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._q_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "q":
            PyMem_Free(self._q_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer[idx] = pointer.p_value
            self._q_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            values = numpy.empty(self.len_q)
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                values[idx] = self._q_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "q":
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                self._q_pointer[idx][0] = value[idx]
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._referencewaterdepth_diskflag_reading:
            k = 0
            for jdx0 in range(self._referencewaterdepth_length_0):
                self.referencewaterdepth[jdx0] = self._referencewaterdepth_ncarray[k]
                k += 1
        elif self._referencewaterdepth_ramflag:
            for jdx0 in range(self._referencewaterdepth_length_0):
                self.referencewaterdepth[jdx0] = self._referencewaterdepth_array[idx, jdx0]
        if self._wettedarea_diskflag_reading:
            k = 0
            for jdx0 in range(self._wettedarea_length_0):
                self.wettedarea[jdx0] = self._wettedarea_ncarray[k]
                k += 1
        elif self._wettedarea_ramflag:
            for jdx0 in range(self._wettedarea_length_0):
                self.wettedarea[jdx0] = self._wettedarea_array[idx, jdx0]
        if self._surfacewidth_diskflag_reading:
            k = 0
            for jdx0 in range(self._surfacewidth_length_0):
                self.surfacewidth[jdx0] = self._surfacewidth_ncarray[k]
                k += 1
        elif self._surfacewidth_ramflag:
            for jdx0 in range(self._surfacewidth_length_0):
                self.surfacewidth[jdx0] = self._surfacewidth_array[idx, jdx0]
        if self._celerity_diskflag_reading:
            k = 0
            for jdx0 in range(self._celerity_length_0):
                self.celerity[jdx0] = self._celerity_ncarray[k]
                k += 1
        elif self._celerity_ramflag:
            for jdx0 in range(self._celerity_length_0):
                self.celerity[jdx0] = self._celerity_array[idx, jdx0]
        if self._correctingfactor_diskflag_reading:
            k = 0
            for jdx0 in range(self._correctingfactor_length_0):
                self.correctingfactor[jdx0] = self._correctingfactor_ncarray[k]
                k += 1
        elif self._correctingfactor_ramflag:
            for jdx0 in range(self._correctingfactor_length_0):
                self.correctingfactor[jdx0] = self._correctingfactor_array[idx, jdx0]
        if self._coefficient1_diskflag_reading:
            k = 0
            for jdx0 in range(self._coefficient1_length_0):
                self.coefficient1[jdx0] = self._coefficient1_ncarray[k]
                k += 1
        elif self._coefficient1_ramflag:
            for jdx0 in range(self._coefficient1_length_0):
                self.coefficient1[jdx0] = self._coefficient1_array[idx, jdx0]
        if self._coefficient2_diskflag_reading:
            k = 0
            for jdx0 in range(self._coefficient2_length_0):
                self.coefficient2[jdx0] = self._coefficient2_ncarray[k]
                k += 1
        elif self._coefficient2_ramflag:
            for jdx0 in range(self._coefficient2_length_0):
                self.coefficient2[jdx0] = self._coefficient2_array[idx, jdx0]
        if self._coefficient3_diskflag_reading:
            k = 0
            for jdx0 in range(self._coefficient3_length_0):
                self.coefficient3[jdx0] = self._coefficient3_ncarray[k]
                k += 1
        elif self._coefficient3_ramflag:
            for jdx0 in range(self._coefficient3_length_0):
                self.coefficient3[jdx0] = self._coefficient3_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._referencewaterdepth_diskflag_writing:
            k = 0
            for jdx0 in range(self._referencewaterdepth_length_0):
                self._referencewaterdepth_ncarray[k] = self.referencewaterdepth[jdx0]
                k += 1
        if self._referencewaterdepth_ramflag:
            for jdx0 in range(self._referencewaterdepth_length_0):
                self._referencewaterdepth_array[idx, jdx0] = self.referencewaterdepth[jdx0]
        if self._wettedarea_diskflag_writing:
            k = 0
            for jdx0 in range(self._wettedarea_length_0):
                self._wettedarea_ncarray[k] = self.wettedarea[jdx0]
                k += 1
        if self._wettedarea_ramflag:
            for jdx0 in range(self._wettedarea_length_0):
                self._wettedarea_array[idx, jdx0] = self.wettedarea[jdx0]
        if self._surfacewidth_diskflag_writing:
            k = 0
            for jdx0 in range(self._surfacewidth_length_0):
                self._surfacewidth_ncarray[k] = self.surfacewidth[jdx0]
                k += 1
        if self._surfacewidth_ramflag:
            for jdx0 in range(self._surfacewidth_length_0):
                self._surfacewidth_array[idx, jdx0] = self.surfacewidth[jdx0]
        if self._celerity_diskflag_writing:
            k = 0
            for jdx0 in range(self._celerity_length_0):
                self._celerity_ncarray[k] = self.celerity[jdx0]
                k += 1
        if self._celerity_ramflag:
            for jdx0 in range(self._celerity_length_0):
                self._celerity_array[idx, jdx0] = self.celerity[jdx0]
        if self._correctingfactor_diskflag_writing:
            k = 0
            for jdx0 in range(self._correctingfactor_length_0):
                self._correctingfactor_ncarray[k] = self.correctingfactor[jdx0]
                k += 1
        if self._correctingfactor_ramflag:
            for jdx0 in range(self._correctingfactor_length_0):
                self._correctingfactor_array[idx, jdx0] = self.correctingfactor[jdx0]
        if self._coefficient1_diskflag_writing:
            k = 0
            for jdx0 in range(self._coefficient1_length_0):
                self._coefficient1_ncarray[k] = self.coefficient1[jdx0]
                k += 1
        if self._coefficient1_ramflag:
            for jdx0 in range(self._coefficient1_length_0):
                self._coefficient1_array[idx, jdx0] = self.coefficient1[jdx0]
        if self._coefficient2_diskflag_writing:
            k = 0
            for jdx0 in range(self._coefficient2_length_0):
                self._coefficient2_ncarray[k] = self.coefficient2[jdx0]
                k += 1
        if self._coefficient2_ramflag:
            for jdx0 in range(self._coefficient2_length_0):
                self._coefficient2_array[idx, jdx0] = self.coefficient2[jdx0]
        if self._coefficient3_diskflag_writing:
            k = 0
            for jdx0 in range(self._coefficient3_length_0):
                self._coefficient3_ncarray[k] = self.coefficient3[jdx0]
                k += 1
        if self._coefficient3_ramflag:
            for jdx0 in range(self._coefficient3_length_0):
                self._coefficient3_array[idx, jdx0] = self.coefficient3[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inflow_diskflag_reading:
            self.inflow = self._inflow_ncarray[0]
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._referencedischarge_diskflag_reading:
            k = 0
            for jdx0 in range(self._referencedischarge_length_0):
                self.referencedischarge[jdx0] = self._referencedischarge_ncarray[k]
                k += 1
        elif self._referencedischarge_ramflag:
            for jdx0 in range(self._referencedischarge_length_0):
                self.referencedischarge[jdx0] = self._referencedischarge_array[idx, jdx0]
        if self._outflow_diskflag_reading:
            self.outflow = self._outflow_ncarray[0]
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inflow_diskflag_writing:
            self._inflow_ncarray[0] = self.inflow
        if self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._referencedischarge_diskflag_writing:
            k = 0
            for jdx0 in range(self._referencedischarge_length_0):
                self._referencedischarge_ncarray[k] = self.referencedischarge[jdx0]
                k += 1
        if self._referencedischarge_ramflag:
            for jdx0 in range(self._referencedischarge_length_0):
                self._referencedischarge_array[idx, jdx0] = self.referencedischarge[jdx0]
        if self._outflow_diskflag_writing:
            self._outflow_ncarray[0] = self.outflow
        if self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._courantnumber_diskflag_reading:
            k = 0
            for jdx0 in range(self._courantnumber_length_0):
                self.courantnumber[jdx0] = self._courantnumber_ncarray[k]
                k += 1
        elif self._courantnumber_ramflag:
            for jdx0 in range(self._courantnumber_length_0):
                self.courantnumber[jdx0] = self._courantnumber_array[idx, jdx0]
        if self._reynoldsnumber_diskflag_reading:
            k = 0
            for jdx0 in range(self._reynoldsnumber_length_0):
                self.reynoldsnumber[jdx0] = self._reynoldsnumber_ncarray[k]
                k += 1
        elif self._reynoldsnumber_ramflag:
            for jdx0 in range(self._reynoldsnumber_length_0):
                self.reynoldsnumber[jdx0] = self._reynoldsnumber_array[idx, jdx0]
        if self._discharge_diskflag_reading:
            k = 0
            for jdx0 in range(self._discharge_length_0):
                self.discharge[jdx0] = self._discharge_ncarray[k]
                k += 1
        elif self._discharge_ramflag:
            for jdx0 in range(self._discharge_length_0):
                self.discharge[jdx0] = self._discharge_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._courantnumber_diskflag_writing:
            k = 0
            for jdx0 in range(self._courantnumber_length_0):
                self._courantnumber_ncarray[k] = self.courantnumber[jdx0]
                k += 1
        if self._courantnumber_ramflag:
            for jdx0 in range(self._courantnumber_length_0):
                self._courantnumber_array[idx, jdx0] = self.courantnumber[jdx0]
        if self._reynoldsnumber_diskflag_writing:
            k = 0
            for jdx0 in range(self._reynoldsnumber_length_0):
                self._reynoldsnumber_ncarray[k] = self.reynoldsnumber[jdx0]
                k += 1
        if self._reynoldsnumber_ramflag:
            for jdx0 in range(self._reynoldsnumber_length_0):
                self._reynoldsnumber_array[idx, jdx0] = self.reynoldsnumber[jdx0]
        if self._discharge_diskflag_writing:
            k = 0
            for jdx0 in range(self._discharge_length_0):
                self._discharge_ncarray[k] = self.discharge[jdx0]
                k += 1
        if self._discharge_ramflag:
            for jdx0 in range(self._discharge_length_0):
                self._discharge_array[idx, jdx0] = self.discharge[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class OutletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            self.q = self._q_ncarray[0]
        elif self._q_ramflag:
            self.q = self._q_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            self._q_ncarray[0] = self.q
        if self._q_ramflag:
            self._q_array[idx] = self.q
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            return self._q_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self._q_pointer[0] = value
@cython.final
cdef class PegasusReferenceWaterDepth(rootutils.PegasusBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_referencedischargeerror_v1(x)
@cython.final
cdef class Model:
    def __init__(self):
        super().__init__()
        self.wqmodel = None
        self.wqmodel_is_mainmodel = False
        self.pegasusreferencewaterdepth = PegasusReferenceWaterDepth(self)
    def get_wqmodel(self) -> masterinterface.MasterInterface | None:
        return self.wqmodel
    def set_wqmodel(self, wqmodel: masterinterface.MasterInterface | None) -> None:
        self.wqmodel = wqmodel
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
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._courantnumber_length_0):
            self.sequences.old_states.courantnumber[jdx0] = self.sequences.new_states.courantnumber[jdx0]
        for jdx0 in range(self.sequences.states._reynoldsnumber_length_0):
            self.sequences.old_states.reynoldsnumber[jdx0] = self.sequences.new_states.reynoldsnumber[jdx0]
        for jdx0 in range(self.sequences.states._discharge_length_0):
            self.sequences.old_states.discharge[jdx0] = self.sequences.new_states.discharge[jdx0]
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        cdef numpy.int64_t idx_segment, idx_run
        for idx_segment in range(self.parameters.control.nmbsegments):
            self.idx_segment = idx_segment
            for idx_run in range(self.parameters.solver.nmbruns):
                self.idx_run = idx_run
                self.calc_referencedischarge_v1()
                self.calc_referencewaterdepth_v1()
                self.calc_wettedarea_surfacewidth_celerity_v1()
                self.calc_correctingfactor_v1()
                self.calc_courantnumber_v1()
                self.calc_reynoldsnumber_v1()
                self.calc_coefficient1_coefficient2_coefficient3_v1()
                self.calc_discharge_v2()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.update_inlets()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.pick_inflow_v1()
        self.adjust_inflow_v1()
        self.update_discharge_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.update_outlets()
        self.calc_outflow_v1()
        self.pass_outflow_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
        if (self.wqmodel is not None) and not self.wqmodel_is_mainmodel:
            self.wqmodel.update_outputs()
    cpdef inline void pick_inflow_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void adjust_inflow_v1(self) noexcept nogil:
        if self.sequences.fluxes.inflow < 0.0:
            if self.sequences.fluxes.inflow < self.parameters.solver.tolerancenegativeinflow:
                self.sequences.fluxes.inflow = nan
            else:
                self.sequences.fluxes.inflow = 0.0
    cpdef inline void update_discharge_v1(self) noexcept nogil:
        self.sequences.states.discharge[0] = self.sequences.fluxes.inflow
    cpdef inline void calc_referencedischarge_v1(self) noexcept nogil:
        cdef double est
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.idx_run == 0:
            est = self.sequences.old_states.discharge[i + 1] + self.sequences.new_states.discharge[i] - self.sequences.old_states.discharge[i]
        else:
            est = self.sequences.new_states.discharge[i + 1]
        self.sequences.fluxes.referencedischarge[i] = max((self.sequences.new_states.discharge[i] + est) / 2.0, 0.0)
    cpdef inline void calc_referencewaterdepth_v1(self) noexcept nogil:
        cdef double tol_q
        cdef double mx
        cdef double mn
        cdef double wl
        cdef numpy.int64_t i
        i = self.idx_segment
        wl = self.sequences.factors.referencewaterdepth[i]
        if isnan(wl) or isinf(wl):
            mn = 0.0
            mx = 2.0
        elif wl <= 0.001:
            mn, mx = 0.0, 0.01
        else:
            mn, mx = 0.9 * wl, 1.1 * wl
        tol_q = min(self.parameters.solver.tolerancedischarge, self.sequences.fluxes.referencedischarge[i] / 10.0)
        self.sequences.factors.referencewaterdepth[i] = self.pegasusreferencewaterdepth.find_x(            mn, mx, 0.0, 1000.0, self.parameters.solver.tolerancewaterdepth, tol_q, 100        )
    cpdef inline void calc_wettedarea_surfacewidth_celerity_v1(self) noexcept nogil:
        if self.wqmodel_typeid == 1:
            self.calc_wettedarea_surfacewidth_celerity_crosssectionmodel_v1(                (<masterinterface.MasterInterface>self.wqmodel)            )
    cpdef inline void calc_correctingfactor_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.factors.correctingfactor[i] = 1.0
        else:
            self.sequences.factors.correctingfactor[i] = (                self.sequences.factors.celerity[i] * self.sequences.factors.wettedarea[i] / self.sequences.fluxes.referencedischarge[i]            )
    cpdef inline void calc_courantnumber_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.states.courantnumber[i] = 0.0
        else:
            self.sequences.states.courantnumber[i] = (self.sequences.factors.celerity[i] / self.sequences.factors.correctingfactor[i]) * (                self.parameters.derived.seconds / (1000.0 * self.parameters.derived.segmentlength)            )
    cpdef inline void calc_reynoldsnumber_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.states.reynoldsnumber[i] = 0.0
        else:
            self.sequences.states.reynoldsnumber[i] = self.sequences.fluxes.referencedischarge[i] / (                self.sequences.factors.correctingfactor[i]                * self.sequences.factors.surfacewidth[i]                * self.parameters.control.bottomslope                * self.sequences.factors.celerity[i]                * (1000.0 * self.parameters.derived.segmentlength)            )
    cpdef inline void calc_coefficient1_coefficient2_coefficient3_v1(self) noexcept nogil:
        cdef double f
        cdef numpy.int64_t i
        i = self.idx_segment
        f = 1.0 / (1.0 + self.sequences.new_states.courantnumber[i] + self.sequences.new_states.reynoldsnumber[i])
        self.sequences.factors.coefficient1[i] = (self.sequences.new_states.courantnumber[i] + self.sequences.new_states.reynoldsnumber[i] - 1.0) * f
        if self.sequences.old_states.courantnumber[i] != 0.0:
            f = f * (self.sequences.new_states.courantnumber[i] / self.sequences.old_states.courantnumber[i])
        self.sequences.factors.coefficient2[i] = (1 + self.sequences.old_states.courantnumber[i] - self.sequences.old_states.reynoldsnumber[i]) * f
        self.sequences.factors.coefficient3[i] = (1 - self.sequences.old_states.courantnumber[i] + self.sequences.old_states.reynoldsnumber[i]) * f
    cpdef inline void calc_discharge_v2(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.new_states.discharge[i] == self.sequences.old_states.discharge[i] == self.sequences.old_states.discharge[i + 1]:
            self.sequences.new_states.discharge[i + 1] = self.sequences.new_states.discharge[i]
        else:
            self.sequences.new_states.discharge[i + 1] = (                self.sequences.factors.coefficient1[i] * self.sequences.new_states.discharge[i]                + self.sequences.factors.coefficient2[i] * self.sequences.old_states.discharge[i]                + self.sequences.factors.coefficient3[i] * self.sequences.old_states.discharge[i + 1]            )
        self.sequences.new_states.discharge[i + 1] = max(self.sequences.new_states.discharge[i + 1], 0.0)
    cpdef inline double return_discharge_crosssectionmodel_v1(self, masterinterface.MasterInterface wqmodel, double waterdepth) noexcept nogil:
        wqmodel.use_waterdepth(waterdepth)
        return wqmodel.get_discharge()
    cpdef inline void calc_wettedarea_surfacewidth_celerity_crosssectionmodel_v1(self, masterinterface.MasterInterface wqmodel) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        wqmodel.use_waterdepth(self.sequences.factors.referencewaterdepth[i])
        self.sequences.factors.wettedarea[i] = wqmodel.get_wettedarea()
        self.sequences.factors.surfacewidth[i] = wqmodel.get_surfacewidth()
        self.sequences.factors.celerity[i] = wqmodel.get_celerity()
    cpdef inline double return_referencedischargeerror_v1(self, double waterdepth) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        return (            self.return_discharge_crosssectionmodel_v1(                (<masterinterface.MasterInterface>self.wqmodel), waterdepth            )            - self.sequences.fluxes.referencedischarge[i]        )
    cpdef inline void calc_outflow_v1(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.states.discharge[self.parameters.control.nmbsegments]
    cpdef inline void pass_outflow_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
    cpdef inline void pick_inflow(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void adjust_inflow(self) noexcept nogil:
        if self.sequences.fluxes.inflow < 0.0:
            if self.sequences.fluxes.inflow < self.parameters.solver.tolerancenegativeinflow:
                self.sequences.fluxes.inflow = nan
            else:
                self.sequences.fluxes.inflow = 0.0
    cpdef inline void update_discharge(self) noexcept nogil:
        self.sequences.states.discharge[0] = self.sequences.fluxes.inflow
    cpdef inline void calc_referencedischarge(self) noexcept nogil:
        cdef double est
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.idx_run == 0:
            est = self.sequences.old_states.discharge[i + 1] + self.sequences.new_states.discharge[i] - self.sequences.old_states.discharge[i]
        else:
            est = self.sequences.new_states.discharge[i + 1]
        self.sequences.fluxes.referencedischarge[i] = max((self.sequences.new_states.discharge[i] + est) / 2.0, 0.0)
    cpdef inline void calc_referencewaterdepth(self) noexcept nogil:
        cdef double tol_q
        cdef double mx
        cdef double mn
        cdef double wl
        cdef numpy.int64_t i
        i = self.idx_segment
        wl = self.sequences.factors.referencewaterdepth[i]
        if isnan(wl) or isinf(wl):
            mn = 0.0
            mx = 2.0
        elif wl <= 0.001:
            mn, mx = 0.0, 0.01
        else:
            mn, mx = 0.9 * wl, 1.1 * wl
        tol_q = min(self.parameters.solver.tolerancedischarge, self.sequences.fluxes.referencedischarge[i] / 10.0)
        self.sequences.factors.referencewaterdepth[i] = self.pegasusreferencewaterdepth.find_x(            mn, mx, 0.0, 1000.0, self.parameters.solver.tolerancewaterdepth, tol_q, 100        )
    cpdef inline void calc_wettedarea_surfacewidth_celerity(self) noexcept nogil:
        if self.wqmodel_typeid == 1:
            self.calc_wettedarea_surfacewidth_celerity_crosssectionmodel_v1(                (<masterinterface.MasterInterface>self.wqmodel)            )
    cpdef inline void calc_correctingfactor(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.factors.correctingfactor[i] = 1.0
        else:
            self.sequences.factors.correctingfactor[i] = (                self.sequences.factors.celerity[i] * self.sequences.factors.wettedarea[i] / self.sequences.fluxes.referencedischarge[i]            )
    cpdef inline void calc_courantnumber(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.states.courantnumber[i] = 0.0
        else:
            self.sequences.states.courantnumber[i] = (self.sequences.factors.celerity[i] / self.sequences.factors.correctingfactor[i]) * (                self.parameters.derived.seconds / (1000.0 * self.parameters.derived.segmentlength)            )
    cpdef inline void calc_reynoldsnumber(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.fluxes.referencedischarge[i] == 0.0:
            self.sequences.states.reynoldsnumber[i] = 0.0
        else:
            self.sequences.states.reynoldsnumber[i] = self.sequences.fluxes.referencedischarge[i] / (                self.sequences.factors.correctingfactor[i]                * self.sequences.factors.surfacewidth[i]                * self.parameters.control.bottomslope                * self.sequences.factors.celerity[i]                * (1000.0 * self.parameters.derived.segmentlength)            )
    cpdef inline void calc_coefficient1_coefficient2_coefficient3(self) noexcept nogil:
        cdef double f
        cdef numpy.int64_t i
        i = self.idx_segment
        f = 1.0 / (1.0 + self.sequences.new_states.courantnumber[i] + self.sequences.new_states.reynoldsnumber[i])
        self.sequences.factors.coefficient1[i] = (self.sequences.new_states.courantnumber[i] + self.sequences.new_states.reynoldsnumber[i] - 1.0) * f
        if self.sequences.old_states.courantnumber[i] != 0.0:
            f = f * (self.sequences.new_states.courantnumber[i] / self.sequences.old_states.courantnumber[i])
        self.sequences.factors.coefficient2[i] = (1 + self.sequences.old_states.courantnumber[i] - self.sequences.old_states.reynoldsnumber[i]) * f
        self.sequences.factors.coefficient3[i] = (1 - self.sequences.old_states.courantnumber[i] + self.sequences.old_states.reynoldsnumber[i]) * f
    cpdef inline void calc_discharge(self) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        if self.sequences.new_states.discharge[i] == self.sequences.old_states.discharge[i] == self.sequences.old_states.discharge[i + 1]:
            self.sequences.new_states.discharge[i + 1] = self.sequences.new_states.discharge[i]
        else:
            self.sequences.new_states.discharge[i + 1] = (                self.sequences.factors.coefficient1[i] * self.sequences.new_states.discharge[i]                + self.sequences.factors.coefficient2[i] * self.sequences.old_states.discharge[i]                + self.sequences.factors.coefficient3[i] * self.sequences.old_states.discharge[i + 1]            )
        self.sequences.new_states.discharge[i + 1] = max(self.sequences.new_states.discharge[i + 1], 0.0)
    cpdef inline double return_discharge_crosssectionmodel(self, masterinterface.MasterInterface wqmodel, double waterdepth) noexcept nogil:
        wqmodel.use_waterdepth(waterdepth)
        return wqmodel.get_discharge()
    cpdef inline void calc_wettedarea_surfacewidth_celerity_crosssectionmodel(self, masterinterface.MasterInterface wqmodel) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        wqmodel.use_waterdepth(self.sequences.factors.referencewaterdepth[i])
        self.sequences.factors.wettedarea[i] = wqmodel.get_wettedarea()
        self.sequences.factors.surfacewidth[i] = wqmodel.get_surfacewidth()
        self.sequences.factors.celerity[i] = wqmodel.get_celerity()
    cpdef inline double return_referencedischargeerror(self, double waterdepth) noexcept nogil:
        cdef numpy.int64_t i
        i = self.idx_segment
        return (            self.return_discharge_crosssectionmodel_v1(                (<masterinterface.MasterInterface>self.wqmodel), waterdepth            )            - self.sequences.fluxes.referencedischarge[i]        )
    cpdef inline void calc_outflow(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.states.discharge[self.parameters.control.nmbsegments]
    cpdef inline void pass_outflow(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
