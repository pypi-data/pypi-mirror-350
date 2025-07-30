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
cdef class SolverParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class FluxSequences:
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
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "q":
            self._q_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._q_outputflag:
            self._q_outputpointer[0] = self.q
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "s":
            self._s_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._s_outputflag:
            self._s_outputpointer[0] = self.s
@cython.final
cdef class NumConsts:
    pass
@cython.final
cdef class NumVars:
    pass
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.solve()
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
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.s = self.sequences.new_states.s
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
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
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
        self.calc_q_v2()
    cpdef inline void calculate_full_terms(self) noexcept nogil:
        self.calc_s_v1()
    cpdef inline void get_point_states(self) noexcept nogil:
        self.sequences.states.s = self.sequences.states._s_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) noexcept nogil:
        self.sequences.states._s_points[self.numvars.idx_stage] = self.sequences.states.s
    cpdef inline void set_result_states(self) noexcept nogil:
        self.sequences.states._s_results[self.numvars.idx_method] = self.sequences.states.s
    cpdef inline void get_sum_fluxes(self) noexcept nogil:
        self.sequences.fluxes.q = self.sequences.fluxes._q_sum
    cpdef inline void set_point_fluxes(self) noexcept nogil:
        self.sequences.fluxes._q_points[self.numvars.idx_stage] = self.sequences.fluxes.q
    cpdef inline void set_result_fluxes(self) noexcept nogil:
        self.sequences.fluxes._q_results[self.numvars.idx_method] = self.sequences.fluxes.q
    cpdef inline void integrate_fluxes(self) noexcept nogil:
        cdef numpy.int64_t jdx
        self.sequences.fluxes.q = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.q = self.sequences.fluxes.q +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._q_points[jdx]
    cpdef inline void reset_sum_fluxes(self) noexcept nogil:
        self.sequences.fluxes._q_sum = 0.
    cpdef inline void addup_fluxes(self) noexcept nogil:
        self.sequences.fluxes._q_sum = self.sequences.fluxes._q_sum + self.sequences.fluxes.q
    cpdef inline void calculate_error(self) noexcept nogil:
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._q_results[self.numvars.idx_method]-self.sequences.fluxes._q_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._q_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._q_results[self.numvars.idx_method]))
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
    cpdef inline void calc_q_v2(self) noexcept nogil:
        if self.sequences.states.s > 0.0:
            self.sequences.fluxes.q = self.parameters.control.k
        else:
            self.sequences.fluxes.q = 0.0
    cpdef inline void calc_s_v1(self) noexcept nogil:
        self.sequences.new_states.s = self.sequences.old_states.s - self.sequences.fluxes.q
    cpdef inline void calc_q(self) noexcept nogil:
        if self.sequences.states.s > 0.0:
            self.sequences.fluxes.q = self.parameters.control.k
        else:
            self.sequences.fluxes.q = 0.0
    cpdef inline void calc_s(self) noexcept nogil:
        self.sequences.new_states.s = self.sequences.old_states.s - self.sequences.fluxes.q
