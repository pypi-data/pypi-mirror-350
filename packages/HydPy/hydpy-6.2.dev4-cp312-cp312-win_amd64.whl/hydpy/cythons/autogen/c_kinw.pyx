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
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qz_diskflag_reading:
            self.qz = self._qz_ncarray[0]
        elif self._qz_ramflag:
            self.qz = self._qz_array[idx]
        if self._qza_diskflag_reading:
            self.qza = self._qza_ncarray[0]
        elif self._qza_ramflag:
            self.qza = self._qza_array[idx]
        if self._qg_diskflag_reading:
            k = 0
            for jdx0 in range(self._qg_length_0):
                self.qg[jdx0] = self._qg_ncarray[k]
                k += 1
        elif self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self.qg[jdx0] = self._qg_array[idx, jdx0]
        if self._qa_diskflag_reading:
            self.qa = self._qa_ncarray[0]
        elif self._qa_ramflag:
            self.qa = self._qa_array[idx]
        if self._dh_diskflag_reading:
            k = 0
            for jdx0 in range(self._dh_length_0):
                self.dh[jdx0] = self._dh_ncarray[k]
                k += 1
        elif self._dh_ramflag:
            for jdx0 in range(self._dh_length_0):
                self.dh[jdx0] = self._dh_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qz_diskflag_writing:
            self._qz_ncarray[0] = self.qz
        if self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qza_diskflag_writing:
            self._qza_ncarray[0] = self.qza
        if self._qza_ramflag:
            self._qza_array[idx] = self.qza
        if self._qg_diskflag_writing:
            k = 0
            for jdx0 in range(self._qg_length_0):
                self._qg_ncarray[k] = self.qg[jdx0]
                k += 1
        if self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self._qg_array[idx, jdx0] = self.qg[jdx0]
        if self._qa_diskflag_writing:
            self._qa_ncarray[0] = self.qa
        if self._qa_ramflag:
            self._qa_array[idx] = self.qa
        if self._dh_diskflag_writing:
            k = 0
            for jdx0 in range(self._dh_length_0):
                self._dh_ncarray[k] = self.dh[jdx0]
                k += 1
        if self._dh_ramflag:
            for jdx0 in range(self._dh_length_0):
                self._dh_array[idx, jdx0] = self.dh[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "qz":
            self._qz_outputpointer = value.p_value
        if name == "qza":
            self._qza_outputpointer = value.p_value
        if name == "qa":
            self._qa_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._qz_outputflag:
            self._qz_outputpointer[0] = self.qz
        if self._qza_outputflag:
            self._qza_outputpointer[0] = self.qza
        if self._qa_outputflag:
            self._qa_outputpointer[0] = self.qa
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._h_diskflag_reading:
            k = 0
            for jdx0 in range(self._h_length_0):
                self.h[jdx0] = self._h_ncarray[k]
                k += 1
        elif self._h_ramflag:
            for jdx0 in range(self._h_length_0):
                self.h[jdx0] = self._h_array[idx, jdx0]
        if self._vg_diskflag_reading:
            k = 0
            for jdx0 in range(self._vg_length_0):
                self.vg[jdx0] = self._vg_ncarray[k]
                k += 1
        elif self._vg_ramflag:
            for jdx0 in range(self._vg_length_0):
                self.vg[jdx0] = self._vg_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._h_diskflag_writing:
            k = 0
            for jdx0 in range(self._h_length_0):
                self._h_ncarray[k] = self.h[jdx0]
                k += 1
        if self._h_ramflag:
            for jdx0 in range(self._h_length_0):
                self._h_array[idx, jdx0] = self.h[jdx0]
        if self._vg_diskflag_writing:
            k = 0
            for jdx0 in range(self._vg_length_0):
                self._vg_ncarray[k] = self.vg[jdx0]
                k += 1
        if self._vg_ramflag:
            for jdx0 in range(self._vg_length_0):
                self._vg_array[idx, jdx0] = self.vg[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class AideSequences:
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
cdef class NumConsts:
    pass
@cython.final
cdef class NumVars:
    pass
@cython.final
cdef class PegasusH(rootutils.PegasusBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_qf_v1(x)
@cython.final
cdef class Model:
    def __init__(self):
        super().__init__()
        self.pegasush = PegasusH(self)
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.update_inlets()
        self.solve()
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
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._h_length_0):
            self.sequences.old_states.h[jdx0] = self.sequences.new_states.h[jdx0]
        for jdx0 in range(self.sequences.states._vg_length_0):
            self.sequences.old_states.vg[jdx0] = self.sequences.new_states.vg[jdx0]
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.pick_q_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_q_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
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
    cpdef inline void solve(self) noexcept nogil:
        cdef numpy.int64_t decrease_dt
        self.numvars.use_relerror = not isnan(            self.parameters.solver.relerrormax        )
        self.numvars.t0, self.numvars.t1 = 0.0, 1.0
        self.numvars.dt_est = 1.0 * self.parameters.solver.reldtmax
        self.numvars.f0_ready = False
        self.reset_sum_fluxes()
        while self.numvars.t0 < self.numvars.t1 - 1e-14:
            self.numvars.last_abserror = inf
            self.numvars.last_relerror = inf
            self.numvars.dt = min(                self.numvars.t1 - self.numvars.t0,                1.0 * self.parameters.solver.reldtmax,                max(self.numvars.dt_est, self.parameters.solver.reldtmin),            )
            if not self.numvars.f0_ready:
                self.calculate_single_terms()
                self.numvars.idx_method = 0
                self.numvars.idx_stage = 0
                self.set_point_fluxes()
                self.set_point_states()
                self.set_result_states()
            for self.numvars.idx_method in range(1, self.numconsts.nmb_methods + 1):
                for self.numvars.idx_stage in range(1, self.numvars.idx_method):
                    self.get_point_states()
                    self.calculate_single_terms()
                    self.set_point_fluxes()
                for self.numvars.idx_stage in range(1, self.numvars.idx_method + 1):
                    self.integrate_fluxes()
                    self.calculate_full_terms()
                    self.set_point_states()
                self.set_result_fluxes()
                self.set_result_states()
                self.calculate_error()
                self.extrapolate_error()
                if self.numvars.idx_method == 1:
                    continue
                if (self.numvars.abserror <= self.parameters.solver.abserrormax) or (                    self.numvars.relerror <= self.parameters.solver.relerrormax                ):
                    self.numvars.dt_est = self.numconsts.dt_increase * self.numvars.dt
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0 + self.numvars.dt
                    self.new2old()
                    break
                decrease_dt = self.numvars.dt > self.parameters.solver.reldtmin
                decrease_dt = decrease_dt and (                    self.numvars.extrapolated_abserror                    > self.parameters.solver.abserrormax                )
                if self.numvars.use_relerror:
                    decrease_dt = decrease_dt and (                        self.numvars.extrapolated_relerror                        > self.parameters.solver.relerrormax                    )
                if decrease_dt:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = self.numvars.dt / self.numconsts.dt_decrease
                    break
                self.numvars.last_abserror = self.numvars.abserror
                self.numvars.last_relerror = self.numvars.relerror
                self.numvars.f0_ready = True
            else:
                if self.numvars.dt <= self.parameters.solver.reldtmin:
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0 + self.numvars.dt
                    self.new2old()
                else:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = self.numvars.dt / self.numconsts.dt_decrease
        self.get_sum_fluxes()
    cpdef inline void calculate_single_terms(self) noexcept nogil:
        self.numvars.nmb_calls = self.numvars.nmb_calls + 1
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_amdh_umdh_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvdh_arvdh_ulvdh_urvdh_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_alvrdh_arvrdh_ulvrdh_urvrdh_v1()
        self.calc_qm_v1()
        self.calc_qmdh_v1()
        self.calc_qm_v2()
        self.calc_qlv_qrv_v1()
        self.calc_qlvdh_qrvdh_v1()
        self.calc_qlv_qrv_v2()
        self.calc_qlvr_qrvr_v1()
        self.calc_qlvrdh_qrvrdh_v1()
        self.calc_qlvr_qrvr_v2()
        self.calc_ag_v1()
        self.calc_qg_v1()
        self.calc_qg_v2()
        self.calc_qa_v1()
        self.calc_wbm_v1()
        self.calc_wblv_wbrv_v1()
        self.calc_wblvr_wbrvr_v1()
        self.calc_wbg_v1()
        self.calc_dh_v1()
    cpdef inline void calculate_full_terms(self) noexcept nogil:
        self.update_h_v1()
        self.update_vg_v1()
    cpdef inline void get_point_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states.h[idx0] = self.sequences.states._h_points[self.numvars.idx_stage][idx0]
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states.vg[idx0] = self.sequences.states._vg_points[self.numvars.idx_stage][idx0]
    cpdef inline void set_point_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states._h_points[self.numvars.idx_stage][idx0] = self.sequences.states.h[idx0]
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states._vg_points[self.numvars.idx_stage][idx0] = self.sequences.states.vg[idx0]
    cpdef inline void set_result_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states._h_results[self.numvars.idx_method][idx0] = self.sequences.states.h[idx0]
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states._vg_results[self.numvars.idx_method][idx0] = self.sequences.states.vg[idx0]
    cpdef inline void get_sum_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes.qza = self.sequences.fluxes._qza_sum
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = self.sequences.fluxes._qg_sum[idx0]
        self.sequences.fluxes.qa = self.sequences.fluxes._qa_sum
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes.dh[idx0] = self.sequences.fluxes._dh_sum[idx0]
    cpdef inline void set_point_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._qza_points[self.numvars.idx_stage] = self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_points[self.numvars.idx_stage] = self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.dh[idx0]
    cpdef inline void set_result_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._qza_results[self.numvars.idx_method] = self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_results[self.numvars.idx_method] = self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.dh[idx0]
    cpdef inline void integrate_fluxes(self) noexcept nogil:
        cdef numpy.int64_t jdx, idx0
        self.sequences.fluxes.qza = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.qza = self.sequences.fluxes.qza +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qza_points[jdx]
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.qg[idx0] = self.sequences.fluxes.qg[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qg_points[jdx, idx0]
        self.sequences.fluxes.qa = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.qa = self.sequences.fluxes.qa +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qa_points[jdx]
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes.dh[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.dh[idx0] = self.sequences.fluxes.dh[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._dh_points[jdx, idx0]
    cpdef inline void reset_sum_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._qza_sum = 0.
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = 0.
        self.sequences.fluxes._qa_sum = 0.
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_sum[idx0] = 0.
    cpdef inline void addup_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._qza_sum = self.sequences.fluxes._qza_sum + self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = self.sequences.fluxes._qg_sum[idx0] + self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_sum = self.sequences.fluxes._qa_sum + self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_sum[idx0] = self.sequences.fluxes._dh_sum[idx0] + self.sequences.fluxes.dh[idx0]
    cpdef inline void calculate_error(self) noexcept nogil:
        cdef numpy.int64_t idx0
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._qza_results[self.numvars.idx_method]-self.sequences.fluxes._qza_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._qza_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._qza_results[self.numvars.idx_method]))
        for idx0 in range(self.sequences.fluxes._qg_length):
            abserror = fabs(self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._qg_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0]))
        abserror = fabs(self.sequences.fluxes._qa_results[self.numvars.idx_method]-self.sequences.fluxes._qa_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._qa_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._qa_results[self.numvars.idx_method]))
        for idx0 in range(self.sequences.fluxes._dh_length):
            abserror = fabs(self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._dh_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0]))
    cpdef inline void extrapolate_error(self) noexcept nogil:
        if self.numvars.abserror <= 0.0:
            self.numvars.extrapolated_abserror = 0.0
            self.numvars.extrapolated_relerror = 0.0
        else:
            if self.numvars.idx_method > 2:
                self.numvars.extrapolated_abserror = exp(                    log(self.numvars.abserror)                    + (                        log(self.numvars.abserror)                        - log(self.numvars.last_abserror)                    )                    * (self.numconsts.nmb_methods - self.numvars.idx_method)                )
            else:
                self.numvars.extrapolated_abserror = -999.9
            if self.numvars.use_relerror:
                if self.numvars.idx_method > 2:
                    if isinf(self.numvars.relerror):
                        self.numvars.extrapolated_relerror = inf
                    else:
                        self.numvars.extrapolated_relerror = exp(                            log(self.numvars.relerror)                            + (                                log(self.numvars.relerror)                                - log(self.numvars.last_relerror)                            )                            * (self.numconsts.nmb_methods - self.numvars.idx_method)                        )
                else:
                    self.numvars.extrapolated_relerror = -999.9
            else:
                self.numvars.extrapolated_relerror = inf
    cpdef inline void pick_q_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx])
    cpdef inline void calc_rhm_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhm[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhmdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhmdh[i] = smoothutils.smooth_logistic2_derivative2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhv_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhv[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp)
    cpdef inline void calc_rhvdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhvdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvr_rhrvr_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvrdh_rhrvrdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_am_um_v1(self) noexcept nogil:
        cdef double d_temp
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            self.sequences.aides.am[i] = d_temp * (self.parameters.control.bm + d_temp * self.parameters.control.bnm) + self.sequences.aides.rhv[i] * (                self.parameters.control.bm + 2.0 * d_temp * self.parameters.control.bnm            )
            self.sequences.aides.um[i] = self.parameters.control.bm + 2.0 * d_temp * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhv[i]
    cpdef inline void calc_amdh_umdh_v1(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.amdh[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + 2.0 * self.parameters.control.bnm * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + 2.0 * self.parameters.control.bnm * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.umdh[i] = 2.0 * d_temp2 * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhvdh[i]
    cpdef inline void calc_alv_arv_ulv_urv_v1(self) noexcept nogil:
        cdef double d_temp
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            self.sequences.aides.alv[i] = d_temp * (self.parameters.control.bv[0] + (d_temp * self.parameters.control.bnv[0] / 2.0)) + self.sequences.aides.rhlvr[                i            ] * (self.parameters.control.bv[0] + d_temp * self.parameters.control.bnv[0])
            self.sequences.aides.ulv[i] = self.parameters.control.bv[0] + d_temp * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvr[i]
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            self.sequences.aides.arv[i] = d_temp * (self.parameters.control.bv[1] + (d_temp * self.parameters.control.bnv[1] / 2.0)) + self.sequences.aides.rhrvr[                i            ] * (self.parameters.control.bv[1] + d_temp * self.parameters.control.bnv[1])
            self.sequences.aides.urv[i] = self.parameters.control.bv[1] + d_temp * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvr[i]
    cpdef inline void calc_alvdh_arvdh_ulvdh_urvdh_v1(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.alvdh[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            self.sequences.aides.ulvdh[i] = d_temp2 * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvrdh[i]
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.arvdh[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
            self.sequences.aides.urvdh[i] = d_temp2 * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_alvr_arvr_ulvr_urvr_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvr[i] = self.sequences.aides.rhlvr[i] ** 2 * self.parameters.control.bnvr[0] / 2.0
            self.sequences.aides.ulvr[i] = self.sequences.aides.rhlvr[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvr[i] = self.sequences.aides.rhrvr[i] ** 2 * self.parameters.control.bnvr[1] / 2.0
            self.sequences.aides.urvr[i] = self.sequences.aides.rhrvr[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_alvrdh_arvrdh_ulvrdh_urvrdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvrdh[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.ulvrdh[i] = self.sequences.aides.rhlvrdh[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvrdh[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.urvrdh[i] = self.sequences.aides.rhrvrdh[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_qm_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.um[i] > 0.0:
                self.sequences.aides.qm[i] = (                    self.parameters.derived.mfm * self.sequences.aides.am[i] ** (5.0 / 3.0) / self.sequences.aides.um[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qm[i] = 0.0
    cpdef inline void calc_qmdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.am[i] > 0.0) and (self.sequences.aides.um[i] > 0.0):
                self.sequences.aides.qmdh[i] = self.parameters.derived.mfm * (                    5.0                    * self.sequences.aides.am[i] ** (2.0 / 3.0)                    * self.sequences.aides.amdh[i]                    / (3.0 * self.sequences.aides.um[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.am[i] ** (5.0 / 3.0)                    * self.sequences.aides.umdh[i]                    / (3.0 * self.sequences.aides.um[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qmdh[i] = 0.0
    cpdef inline void calc_qm_v2(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.amdh[i] > 0.0:
                self.sequences.aides.qm[i] = self.sequences.aides.qmdh[i] / self.sequences.aides.amdh[i] * self.sequences.aides.am[i]
            else:
                self.sequences.aides.qm[i] = 0.0
    cpdef inline void calc_qlv_qrv_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulv[i] > 0.0:
                self.sequences.aides.qlv[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alv[i] ** (5.0 / 3.0) / self.sequences.aides.ulv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlv[i] = 0.0
            if self.sequences.aides.urv[i] > 0:
                self.sequences.aides.qrv[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arv[i] ** (5.0 / 3.0) / self.sequences.aides.urv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrv[i] = 0.0
    cpdef inline void calc_qlvdh_qrvdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.alv[i] > 0.0) and (self.sequences.aides.ulv[i] > 0.0):
                self.sequences.aides.qlvdh[i] = self.parameters.derived.mfv[0] * (                    5.0                    * self.sequences.aides.alv[i] ** (2.0 / 3.0)                    * self.sequences.aides.alvdh[i]                    / (3.0 * self.sequences.aides.ulv[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.alv[i] ** (5.0 / 3.0)                    * self.sequences.aides.ulvdh[i]                    / (3.0 * self.sequences.aides.ulv[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qlvdh[i] = 0.0
            if (self.sequences.aides.arv[i] > 0.0) and (self.sequences.aides.urv[i] > 0.0):
                self.sequences.aides.qrvdh[i] = self.parameters.derived.mfv[1] * (                    5.0                    * self.sequences.aides.arv[i] ** (2.0 / 3.0)                    * self.sequences.aides.arvdh[i]                    / (3.0 * self.sequences.aides.urv[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.arv[i] ** (5.0 / 3.0)                    * self.sequences.aides.urvdh[i]                    / (3.0 * self.sequences.aides.urv[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qrvdh[i] = 0.0
    cpdef inline void calc_qlv_qrv_v2(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.alvdh[i] > 0.0:
                self.sequences.aides.qlv[i] = self.sequences.aides.qlvdh[i] / self.sequences.aides.alvdh[i] * self.sequences.aides.alv[i]
            else:
                self.sequences.aides.qlv[i] = 0.0
            if self.sequences.aides.arvdh[i] > 0.0:
                self.sequences.aides.qrv[i] = self.sequences.aides.qrvdh[i] / self.sequences.aides.arvdh[i] * self.sequences.aides.arv[i]
            else:
                self.sequences.aides.qrv[i] = 0.0
    cpdef inline void calc_qlvr_qrvr_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulvr[i] > 0.0:
                self.sequences.aides.qlvr[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alvr[i] ** (5.0 / 3.0) / self.sequences.aides.ulvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlvr[i] = 0.0
            if self.sequences.aides.urvr[i] > 0.0:
                self.sequences.aides.qrvr[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arvr[i] ** (5.0 / 3.0) / self.sequences.aides.urvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrvr[i] = 0.0
    cpdef inline void calc_qlvrdh_qrvrdh_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.alvr[i] > 0.0) and (self.sequences.aides.ulvr[i] > 0.0):
                self.sequences.aides.qlvrdh[i] = self.parameters.derived.mfv[0] * (                    5.0                    * self.sequences.aides.alvr[i] ** (2.0 / 3.0)                    * self.sequences.aides.alvrdh[i]                    / (3.0 * self.sequences.aides.ulvr[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.alvr[i] ** (5.0 / 3.0)                    * self.sequences.aides.ulvrdh[i]                    / (3.0 * self.sequences.aides.ulvr[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qlvrdh[i] = 0.0
            if (self.sequences.aides.arvr[i] > 0.0) and (self.sequences.aides.urvr[i] > 0.0):
                self.sequences.aides.qrvrdh[i] = self.parameters.derived.mfv[1] * (                    5.0                    * self.sequences.aides.arvr[i] ** (2.0 / 3.0)                    * self.sequences.aides.arvrdh[i]                    / (3.0 * self.sequences.aides.urvr[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.arvr[i] ** (5.0 / 3.0)                    * self.sequences.aides.urvrdh[i]                    / (3.0 * self.sequences.aides.urvr[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qrvrdh[i] = 0.0
    cpdef inline void calc_qlvr_qrvr_v2(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.alvrdh[i] > 0.0:
                self.sequences.aides.qlvr[i] = self.sequences.aides.qlvrdh[i] / self.sequences.aides.alvrdh[i] * self.sequences.aides.alvr[i]
            else:
                self.sequences.aides.qlvr[i] = 0.0
            if self.sequences.aides.arvrdh[i] > 0.0:
                self.sequences.aides.qrvr[i] = self.sequences.aides.qrvrdh[i] / self.sequences.aides.arvrdh[i] * self.sequences.aides.arvr[i]
            else:
                self.sequences.aides.qrvr[i] = 0.0
    cpdef inline void calc_ag_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.ag[i] = self.sequences.aides.am[i] + self.sequences.aides.alv[i] + self.sequences.aides.arv[i] + self.sequences.aides.alvr[i] + self.sequences.aides.arvr[i]
    cpdef inline void calc_qg_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.fluxes.qg[i] = self.sequences.aides.qm[i] + self.sequences.aides.qlv[i] + self.sequences.aides.qrv[i] + self.sequences.aides.qlvr[i] + self.sequences.aides.qrvr[i]
    cpdef inline void calc_qg_v2(self) noexcept nogil:
        cdef double d_v
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.parameters.control.vg2fg.inputs[0] = self.sequences.states.vg[i]
            self.parameters.control.vg2fg.calculate_values()
            d_v = max(self.parameters.control.ek * self.parameters.control.vg2fg.outputs[0], 0.0)
            self.sequences.fluxes.qg[i] = 1000.0 * d_v * self.sequences.states.vg[i] * self.parameters.control.gts / self.parameters.control.laen
    cpdef inline void calc_qa_v1(self) noexcept nogil:
        if self.parameters.control.gts > 0:
            self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
        else:
            self.sequences.fluxes.qa = self.sequences.fluxes.qz
    cpdef inline void calc_wbm_v1(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.wbm[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + self.parameters.control.bnm * 2.0 * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + self.parameters.control.bnm * 2.0 * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.wbm[i] = smoothutils.smooth_max1(self.parameters.fixed.wbmin, self.sequences.aides.wbm[i], self.parameters.fixed.wbreg)
    cpdef inline void calc_wblv_wbrv_v1(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wblv[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2.0 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.wbrv[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2.0 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
    cpdef inline void calc_wblvr_wbrvr_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wblvr[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wbrvr[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_wbg_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wbg[i] = (                self.sequences.aides.wbm[i] + self.sequences.aides.wblv[i] + self.sequences.aides.wbrv[i] + self.sequences.aides.wblvr[i] + self.sequences.aides.wbrvr[i]            )
    cpdef inline void calc_dh_v1(self) noexcept nogil:
        cdef double d_qz
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if i:
                d_qz = self.sequences.fluxes.qg[i - 1]
            else:
                d_qz = self.sequences.fluxes.qz
            self.sequences.fluxes.dh[i] = (d_qz - self.sequences.fluxes.qg[i]) / (1000.0 * self.parameters.control.laen / self.parameters.control.gts * self.sequences.aides.wbg[i])
    cpdef inline void update_h_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.new_states.h[i] = self.sequences.old_states.h[i] + self.parameters.derived.sek * self.sequences.fluxes.dh[i]
    cpdef inline void update_vg_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if i:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qg[i - 1] - self.sequences.fluxes.qg[i]) / 1e6
            else:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qza - self.sequences.fluxes.qg[i]) / 1e6
    cpdef inline double return_qf_v1(self, double h) noexcept nogil:
        cdef double d_error
        cdef double d_qg
        d_qg = self.sequences.fluxes.qg[0]
        self.sequences.states.h[0] = h
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_qm_v1()
        self.calc_qlv_qrv_v1()
        self.calc_qlvr_qrvr_v1()
        self.calc_ag_v1()
        self.calc_qg_v1()
        d_error = self.sequences.fluxes.qg[0] - d_qg
        self.sequences.fluxes.qg[0] = d_qg
        return d_error
    cpdef inline double return_h_v1(self) noexcept nogil:
        return self.pegasush.find_x(0.0, 2.0 * self.parameters.control.hm, -10.0, 1000.0, 0.0, 1e-10, 1000)
    cpdef inline void pass_q_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qa
    cpdef inline void pick_q(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx])
    cpdef inline void calc_rhm(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhm[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhmdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhmdh[i] = smoothutils.smooth_logistic2_derivative2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhv(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhv[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp)
    cpdef inline void calc_rhvdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhvdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvr_rhrvr(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvrdh_rhrvrdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_am_um(self) noexcept nogil:
        cdef double d_temp
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            self.sequences.aides.am[i] = d_temp * (self.parameters.control.bm + d_temp * self.parameters.control.bnm) + self.sequences.aides.rhv[i] * (                self.parameters.control.bm + 2.0 * d_temp * self.parameters.control.bnm            )
            self.sequences.aides.um[i] = self.parameters.control.bm + 2.0 * d_temp * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhv[i]
    cpdef inline void calc_amdh_umdh(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.amdh[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + 2.0 * self.parameters.control.bnm * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + 2.0 * self.parameters.control.bnm * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.umdh[i] = 2.0 * d_temp2 * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhvdh[i]
    cpdef inline void calc_alv_arv_ulv_urv(self) noexcept nogil:
        cdef double d_temp
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            self.sequences.aides.alv[i] = d_temp * (self.parameters.control.bv[0] + (d_temp * self.parameters.control.bnv[0] / 2.0)) + self.sequences.aides.rhlvr[                i            ] * (self.parameters.control.bv[0] + d_temp * self.parameters.control.bnv[0])
            self.sequences.aides.ulv[i] = self.parameters.control.bv[0] + d_temp * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvr[i]
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            self.sequences.aides.arv[i] = d_temp * (self.parameters.control.bv[1] + (d_temp * self.parameters.control.bnv[1] / 2.0)) + self.sequences.aides.rhrvr[                i            ] * (self.parameters.control.bv[1] + d_temp * self.parameters.control.bnv[1])
            self.sequences.aides.urv[i] = self.parameters.control.bv[1] + d_temp * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvr[i]
    cpdef inline void calc_alvdh_arvdh_ulvdh_urvdh(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.alvdh[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            self.sequences.aides.ulvdh[i] = d_temp2 * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvrdh[i]
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.arvdh[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
            self.sequences.aides.urvdh[i] = d_temp2 * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_alvr_arvr_ulvr_urvr(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvr[i] = self.sequences.aides.rhlvr[i] ** 2 * self.parameters.control.bnvr[0] / 2.0
            self.sequences.aides.ulvr[i] = self.sequences.aides.rhlvr[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvr[i] = self.sequences.aides.rhrvr[i] ** 2 * self.parameters.control.bnvr[1] / 2.0
            self.sequences.aides.urvr[i] = self.sequences.aides.rhrvr[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_alvrdh_arvrdh_ulvrdh_urvrdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvrdh[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.ulvrdh[i] = self.sequences.aides.rhlvrdh[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvrdh[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.urvrdh[i] = self.sequences.aides.rhrvrdh[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_qmdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.am[i] > 0.0) and (self.sequences.aides.um[i] > 0.0):
                self.sequences.aides.qmdh[i] = self.parameters.derived.mfm * (                    5.0                    * self.sequences.aides.am[i] ** (2.0 / 3.0)                    * self.sequences.aides.amdh[i]                    / (3.0 * self.sequences.aides.um[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.am[i] ** (5.0 / 3.0)                    * self.sequences.aides.umdh[i]                    / (3.0 * self.sequences.aides.um[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qmdh[i] = 0.0
    cpdef inline void calc_qlvdh_qrvdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.alv[i] > 0.0) and (self.sequences.aides.ulv[i] > 0.0):
                self.sequences.aides.qlvdh[i] = self.parameters.derived.mfv[0] * (                    5.0                    * self.sequences.aides.alv[i] ** (2.0 / 3.0)                    * self.sequences.aides.alvdh[i]                    / (3.0 * self.sequences.aides.ulv[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.alv[i] ** (5.0 / 3.0)                    * self.sequences.aides.ulvdh[i]                    / (3.0 * self.sequences.aides.ulv[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qlvdh[i] = 0.0
            if (self.sequences.aides.arv[i] > 0.0) and (self.sequences.aides.urv[i] > 0.0):
                self.sequences.aides.qrvdh[i] = self.parameters.derived.mfv[1] * (                    5.0                    * self.sequences.aides.arv[i] ** (2.0 / 3.0)                    * self.sequences.aides.arvdh[i]                    / (3.0 * self.sequences.aides.urv[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.arv[i] ** (5.0 / 3.0)                    * self.sequences.aides.urvdh[i]                    / (3.0 * self.sequences.aides.urv[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qrvdh[i] = 0.0
    cpdef inline void calc_qlvrdh_qrvrdh(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if (self.sequences.aides.alvr[i] > 0.0) and (self.sequences.aides.ulvr[i] > 0.0):
                self.sequences.aides.qlvrdh[i] = self.parameters.derived.mfv[0] * (                    5.0                    * self.sequences.aides.alvr[i] ** (2.0 / 3.0)                    * self.sequences.aides.alvrdh[i]                    / (3.0 * self.sequences.aides.ulvr[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.alvr[i] ** (5.0 / 3.0)                    * self.sequences.aides.ulvrdh[i]                    / (3.0 * self.sequences.aides.ulvr[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qlvrdh[i] = 0.0
            if (self.sequences.aides.arvr[i] > 0.0) and (self.sequences.aides.urvr[i] > 0.0):
                self.sequences.aides.qrvrdh[i] = self.parameters.derived.mfv[1] * (                    5.0                    * self.sequences.aides.arvr[i] ** (2.0 / 3.0)                    * self.sequences.aides.arvrdh[i]                    / (3.0 * self.sequences.aides.urvr[i] ** (2.0 / 3.0))                    - 2.0                    * self.sequences.aides.arvr[i] ** (5.0 / 3.0)                    * self.sequences.aides.urvrdh[i]                    / (3.0 * self.sequences.aides.urvr[i] ** (5.0 / 3.0))                )
            else:
                self.sequences.aides.qrvrdh[i] = 0.0
    cpdef inline void calc_ag(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.ag[i] = self.sequences.aides.am[i] + self.sequences.aides.alv[i] + self.sequences.aides.arv[i] + self.sequences.aides.alvr[i] + self.sequences.aides.arvr[i]
    cpdef inline void calc_qa(self) noexcept nogil:
        if self.parameters.control.gts > 0:
            self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
        else:
            self.sequences.fluxes.qa = self.sequences.fluxes.qz
    cpdef inline void calc_wbm(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.wbm[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + self.parameters.control.bnm * 2.0 * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + self.parameters.control.bnm * 2.0 * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.wbm[i] = smoothutils.smooth_max1(self.parameters.fixed.wbmin, self.sequences.aides.wbm[i], self.parameters.fixed.wbreg)
    cpdef inline void calc_wblv_wbrv(self) noexcept nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wblv[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2.0 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.wbrv[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2.0 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
    cpdef inline void calc_wblvr_wbrvr(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wblvr[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wbrvr[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_wbg(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wbg[i] = (                self.sequences.aides.wbm[i] + self.sequences.aides.wblv[i] + self.sequences.aides.wbrv[i] + self.sequences.aides.wblvr[i] + self.sequences.aides.wbrvr[i]            )
    cpdef inline void calc_dh(self) noexcept nogil:
        cdef double d_qz
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if i:
                d_qz = self.sequences.fluxes.qg[i - 1]
            else:
                d_qz = self.sequences.fluxes.qz
            self.sequences.fluxes.dh[i] = (d_qz - self.sequences.fluxes.qg[i]) / (1000.0 * self.parameters.control.laen / self.parameters.control.gts * self.sequences.aides.wbg[i])
    cpdef inline void update_h(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            self.sequences.new_states.h[i] = self.sequences.old_states.h[i] + self.parameters.derived.sek * self.sequences.fluxes.dh[i]
    cpdef inline void update_vg(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.gts):
            if i:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qg[i - 1] - self.sequences.fluxes.qg[i]) / 1e6
            else:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qza - self.sequences.fluxes.qg[i]) / 1e6
    cpdef inline double return_qf(self, double h) noexcept nogil:
        cdef double d_error
        cdef double d_qg
        d_qg = self.sequences.fluxes.qg[0]
        self.sequences.states.h[0] = h
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_qm_v1()
        self.calc_qlv_qrv_v1()
        self.calc_qlvr_qrvr_v1()
        self.calc_ag_v1()
        self.calc_qg_v1()
        d_error = self.sequences.fluxes.qg[0] - d_qg
        self.sequences.fluxes.qg[0] = d_qg
        return d_error
    cpdef inline double return_h(self) noexcept nogil:
        return self.pegasush.find_x(0.0, 2.0 * self.parameters.control.hm, -10.0, 1000.0, 0.0, 1e-10, 1000)
    cpdef inline void pass_q(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qa
