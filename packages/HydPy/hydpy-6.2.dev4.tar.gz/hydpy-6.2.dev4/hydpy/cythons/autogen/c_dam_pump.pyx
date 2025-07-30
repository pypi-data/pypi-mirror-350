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
cdef class ReceiverSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._owl_diskflag_reading:
            self.owl = self._owl_ncarray[0]
        elif self._owl_ramflag:
            self.owl = self._owl_array[idx]
        if self._rwl_diskflag_reading:
            self.rwl = self._rwl_ncarray[0]
        elif self._rwl_ramflag:
            self.rwl = self._rwl_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._owl_diskflag_writing:
            self._owl_ncarray[0] = self.owl
        if self._owl_ramflag:
            self._owl_array[idx] = self.owl
        if self._rwl_diskflag_writing:
            self._rwl_ncarray[0] = self.rwl
        if self._rwl_ramflag:
            self._rwl_array[idx] = self.rwl
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "owl":
            self._owl_pointer = pointer.p_value
        if name == "rwl":
            self._rwl_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "owl":
            return self._owl_pointer[0]
        if name == "rwl":
            return self._rwl_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "owl":
            self._owl_pointer[0] = value
        if name == "rwl":
            self._rwl_pointer[0] = value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
        if self._outerwaterlevel_diskflag_reading:
            self.outerwaterlevel = self._outerwaterlevel_ncarray[0]
        elif self._outerwaterlevel_ramflag:
            self.outerwaterlevel = self._outerwaterlevel_array[idx]
        if self._remotewaterlevel_diskflag_reading:
            self.remotewaterlevel = self._remotewaterlevel_ncarray[0]
        elif self._remotewaterlevel_ramflag:
            self.remotewaterlevel = self._remotewaterlevel_array[idx]
        if self._waterleveldifference_diskflag_reading:
            self.waterleveldifference = self._waterleveldifference_ncarray[0]
        elif self._waterleveldifference_ramflag:
            self.waterleveldifference = self._waterleveldifference_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
        if self._outerwaterlevel_diskflag_writing:
            self._outerwaterlevel_ncarray[0] = self.outerwaterlevel
        if self._outerwaterlevel_ramflag:
            self._outerwaterlevel_array[idx] = self.outerwaterlevel
        if self._remotewaterlevel_diskflag_writing:
            self._remotewaterlevel_ncarray[0] = self.remotewaterlevel
        if self._remotewaterlevel_ramflag:
            self._remotewaterlevel_array[idx] = self.remotewaterlevel
        if self._waterleveldifference_diskflag_writing:
            self._waterleveldifference_ncarray[0] = self.waterleveldifference
        if self._waterleveldifference_ramflag:
            self._waterleveldifference_array[idx] = self.waterleveldifference
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
        if name == "outerwaterlevel":
            self._outerwaterlevel_outputpointer = value.p_value
        if name == "remotewaterlevel":
            self._remotewaterlevel_outputpointer = value.p_value
        if name == "waterleveldifference":
            self._waterleveldifference_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
        if self._outerwaterlevel_outputflag:
            self._outerwaterlevel_outputpointer[0] = self.outerwaterlevel
        if self._remotewaterlevel_outputflag:
            self._remotewaterlevel_outputpointer[0] = self.remotewaterlevel
        if self._waterleveldifference_outputflag:
            self._waterleveldifference_outputpointer[0] = self.waterleveldifference
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_diskflag_reading:
            self.precipitation = self._precipitation_ncarray[0]
        elif self._precipitation_ramflag:
            self.precipitation = self._precipitation_array[idx]
        if self._adjustedprecipitation_diskflag_reading:
            self.adjustedprecipitation = self._adjustedprecipitation_ncarray[0]
        elif self._adjustedprecipitation_ramflag:
            self.adjustedprecipitation = self._adjustedprecipitation_array[idx]
        if self._potentialevaporation_diskflag_reading:
            self.potentialevaporation = self._potentialevaporation_ncarray[0]
        elif self._potentialevaporation_ramflag:
            self.potentialevaporation = self._potentialevaporation_array[idx]
        if self._adjustedevaporation_diskflag_reading:
            self.adjustedevaporation = self._adjustedevaporation_ncarray[0]
        elif self._adjustedevaporation_ramflag:
            self.adjustedevaporation = self._adjustedevaporation_array[idx]
        if self._actualevaporation_diskflag_reading:
            self.actualevaporation = self._actualevaporation_ncarray[0]
        elif self._actualevaporation_ramflag:
            self.actualevaporation = self._actualevaporation_array[idx]
        if self._inflow_diskflag_reading:
            self.inflow = self._inflow_ncarray[0]
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._maxforceddischarge_diskflag_reading:
            self.maxforceddischarge = self._maxforceddischarge_ncarray[0]
        elif self._maxforceddischarge_ramflag:
            self.maxforceddischarge = self._maxforceddischarge_array[idx]
        if self._forceddischarge_diskflag_reading:
            self.forceddischarge = self._forceddischarge_ncarray[0]
        elif self._forceddischarge_ramflag:
            self.forceddischarge = self._forceddischarge_array[idx]
        if self._outflow_diskflag_reading:
            self.outflow = self._outflow_ncarray[0]
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._precipitation_diskflag_writing:
            self._precipitation_ncarray[0] = self.precipitation
        if self._precipitation_ramflag:
            self._precipitation_array[idx] = self.precipitation
        if self._adjustedprecipitation_diskflag_writing:
            self._adjustedprecipitation_ncarray[0] = self.adjustedprecipitation
        if self._adjustedprecipitation_ramflag:
            self._adjustedprecipitation_array[idx] = self.adjustedprecipitation
        if self._potentialevaporation_diskflag_writing:
            self._potentialevaporation_ncarray[0] = self.potentialevaporation
        if self._potentialevaporation_ramflag:
            self._potentialevaporation_array[idx] = self.potentialevaporation
        if self._adjustedevaporation_diskflag_writing:
            self._adjustedevaporation_ncarray[0] = self.adjustedevaporation
        if self._adjustedevaporation_ramflag:
            self._adjustedevaporation_array[idx] = self.adjustedevaporation
        if self._actualevaporation_diskflag_writing:
            self._actualevaporation_ncarray[0] = self.actualevaporation
        if self._actualevaporation_ramflag:
            self._actualevaporation_array[idx] = self.actualevaporation
        if self._inflow_diskflag_writing:
            self._inflow_ncarray[0] = self.inflow
        if self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._maxforceddischarge_diskflag_writing:
            self._maxforceddischarge_ncarray[0] = self.maxforceddischarge
        if self._maxforceddischarge_ramflag:
            self._maxforceddischarge_array[idx] = self.maxforceddischarge
        if self._forceddischarge_diskflag_writing:
            self._forceddischarge_ncarray[0] = self.forceddischarge
        if self._forceddischarge_ramflag:
            self._forceddischarge_array[idx] = self.forceddischarge
        if self._outflow_diskflag_writing:
            self._outflow_ncarray[0] = self.outflow
        if self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "precipitation":
            self._precipitation_outputpointer = value.p_value
        if name == "adjustedprecipitation":
            self._adjustedprecipitation_outputpointer = value.p_value
        if name == "potentialevaporation":
            self._potentialevaporation_outputpointer = value.p_value
        if name == "adjustedevaporation":
            self._adjustedevaporation_outputpointer = value.p_value
        if name == "actualevaporation":
            self._actualevaporation_outputpointer = value.p_value
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "maxforceddischarge":
            self._maxforceddischarge_outputpointer = value.p_value
        if name == "forceddischarge":
            self._forceddischarge_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._precipitation_outputflag:
            self._precipitation_outputpointer[0] = self.precipitation
        if self._adjustedprecipitation_outputflag:
            self._adjustedprecipitation_outputpointer[0] = self.adjustedprecipitation
        if self._potentialevaporation_outputflag:
            self._potentialevaporation_outputpointer[0] = self.potentialevaporation
        if self._adjustedevaporation_outputflag:
            self._adjustedevaporation_outputpointer[0] = self.adjustedevaporation
        if self._actualevaporation_outputflag:
            self._actualevaporation_outputpointer[0] = self.actualevaporation
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._maxforceddischarge_outputflag:
            self._maxforceddischarge_outputpointer[0] = self.maxforceddischarge
        if self._forceddischarge_outputflag:
            self._forceddischarge_outputpointer[0] = self.forceddischarge
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._watervolume_diskflag_reading:
            self.watervolume = self._watervolume_ncarray[0]
        elif self._watervolume_ramflag:
            self.watervolume = self._watervolume_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._watervolume_diskflag_writing:
            self._watervolume_ncarray[0] = self.watervolume
        if self._watervolume_ramflag:
            self._watervolume_array[idx] = self.watervolume
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "watervolume":
            self._watervolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._watervolume_outputflag:
            self._watervolume_outputpointer[0] = self.watervolume
@cython.final
cdef class LogSequences:
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
cdef class Model:
    def __init__(self):
        super().__init__()
        self.pemodel = None
        self.pemodel_is_mainmodel = False
        self.precipmodel = None
        self.precipmodel_is_mainmodel = False
    def get_pemodel(self) -> masterinterface.MasterInterface | None:
        return self.pemodel
    def set_pemodel(self, pemodel: masterinterface.MasterInterface | None) -> None:
        self.pemodel = pemodel
    def get_precipmodel(self) -> masterinterface.MasterInterface | None:
        return self.precipmodel
    def set_precipmodel(self, precipmodel: masterinterface.MasterInterface | None) -> None:
        self.precipmodel = precipmodel
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.reset_reuseflags()
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
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.reset_reuseflags()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        self.sequences.receivers.load_data(idx)
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.load_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.receivers.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.save_data(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.watervolume = self.sequences.new_states.watervolume
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.new2old()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.new2old()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_inlets()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_inlets()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.calc_precipitation_v1()
        self.calc_potentialevaporation_v1()
        self.calc_adjustedevaporation_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_outlets()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outlets()
        self.calc_waterlevel_v1()
        self.calc_outerwaterlevel_v1()
        self.calc_remotewaterlevel_v1()
        self.pass_outflow_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_receivers(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_receivers(idx)
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.receivers.owl = self.sequences.receivers._owl_pointer[0]
        if not self.threading:
            self.sequences.receivers.rwl = self.sequences.receivers._rwl_pointer[0]
        self.pick_loggedouterwaterlevel_v1()
        self.pick_loggedremotewaterlevel_v1()
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_senders(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_outputs()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outputs()
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
        self.calc_adjustedprecipitation_v1()
        self.pic_inflow_v1()
        self.calc_waterlevel_v1()
        self.calc_outerwaterlevel_v1()
        self.calc_remotewaterlevel_v1()
        self.calc_waterleveldifference_v1()
        self.calc_maxforceddischarge_v1()
        self.calc_forceddischarge_v1()
        self.calc_actualevaporation_v1()
        self.calc_outflow_v3()
    cpdef inline void calculate_full_terms(self) noexcept nogil:
        self.update_watervolume_v1()
    cpdef inline void get_point_states(self) noexcept nogil:
        self.sequences.states.watervolume = self.sequences.states._watervolume_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) noexcept nogil:
        self.sequences.states._watervolume_points[self.numvars.idx_stage] = self.sequences.states.watervolume
    cpdef inline void set_result_states(self) noexcept nogil:
        self.sequences.states._watervolume_results[self.numvars.idx_method] = self.sequences.states.watervolume
    cpdef inline void get_sum_fluxes(self) noexcept nogil:
        self.sequences.fluxes.adjustedprecipitation = self.sequences.fluxes._adjustedprecipitation_sum
        self.sequences.fluxes.actualevaporation = self.sequences.fluxes._actualevaporation_sum
        self.sequences.fluxes.inflow = self.sequences.fluxes._inflow_sum
        self.sequences.fluxes.maxforceddischarge = self.sequences.fluxes._maxforceddischarge_sum
        self.sequences.fluxes.forceddischarge = self.sequences.fluxes._forceddischarge_sum
        self.sequences.fluxes.outflow = self.sequences.fluxes._outflow_sum
    cpdef inline void set_point_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_points[self.numvars.idx_stage] = self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_points[self.numvars.idx_stage] = self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_points[self.numvars.idx_stage] = self.sequences.fluxes.inflow
        self.sequences.fluxes._maxforceddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._forceddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.forceddischarge
        self.sequences.fluxes._outflow_points[self.numvars.idx_stage] = self.sequences.fluxes.outflow
    cpdef inline void set_result_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method] = self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method] = self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_results[self.numvars.idx_method] = self.sequences.fluxes.inflow
        self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._forceddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.forceddischarge
        self.sequences.fluxes._outflow_results[self.numvars.idx_method] = self.sequences.fluxes.outflow
    cpdef inline void integrate_fluxes(self) noexcept nogil:
        cdef numpy.int64_t jdx
        self.sequences.fluxes.adjustedprecipitation = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.adjustedprecipitation = self.sequences.fluxes.adjustedprecipitation +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._adjustedprecipitation_points[jdx]
        self.sequences.fluxes.actualevaporation = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualevaporation = self.sequences.fluxes.actualevaporation +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualevaporation_points[jdx]
        self.sequences.fluxes.inflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._inflow_points[jdx]
        self.sequences.fluxes.maxforceddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.maxforceddischarge = self.sequences.fluxes.maxforceddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._maxforceddischarge_points[jdx]
        self.sequences.fluxes.forceddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.forceddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._forceddischarge_points[jdx]
        self.sequences.fluxes.outflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.outflow = self.sequences.fluxes.outflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._outflow_points[jdx]
    cpdef inline void reset_sum_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_sum = 0.
        self.sequences.fluxes._actualevaporation_sum = 0.
        self.sequences.fluxes._inflow_sum = 0.
        self.sequences.fluxes._maxforceddischarge_sum = 0.
        self.sequences.fluxes._forceddischarge_sum = 0.
        self.sequences.fluxes._outflow_sum = 0.
    cpdef inline void addup_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_sum = self.sequences.fluxes._adjustedprecipitation_sum + self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_sum = self.sequences.fluxes._actualevaporation_sum + self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_sum = self.sequences.fluxes._inflow_sum + self.sequences.fluxes.inflow
        self.sequences.fluxes._maxforceddischarge_sum = self.sequences.fluxes._maxforceddischarge_sum + self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._forceddischarge_sum = self.sequences.fluxes._forceddischarge_sum + self.sequences.fluxes.forceddischarge
        self.sequences.fluxes._outflow_sum = self.sequences.fluxes._outflow_sum + self.sequences.fluxes.outflow
    cpdef inline void calculate_error(self) noexcept nogil:
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method]-self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method]-self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._inflow_results[self.numvars.idx_method]-self.sequences.fluxes._inflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._inflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._inflow_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._forceddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._forceddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._forceddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._forceddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._outflow_results[self.numvars.idx_method]-self.sequences.fluxes._outflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._outflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._outflow_results[self.numvars.idx_method]))
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
    cpdef inline void pick_loggedouterwaterlevel_v1(self) noexcept nogil:
        self.sequences.logs.loggedouterwaterlevel[0] = self.sequences.receivers.owl
    cpdef inline void pick_loggedremotewaterlevel_v1(self) noexcept nogil:
        self.sequences.logs.loggedremotewaterlevel[0] = self.sequences.receivers.rwl
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        if self.precipmodel is None:
            self.sequences.fluxes.precipitation = 0.0
        elif self.precipmodel_typeid == 2:
            (<masterinterface.MasterInterface>self.precipmodel).determine_precipitation()
            self.sequences.fluxes.precipitation = (<masterinterface.MasterInterface>self.precipmodel).get_precipitation(0)
    cpdef inline void calc_potentialevaporation_v1(self) noexcept nogil:
        if self.pemodel is None:
            self.sequences.fluxes.potentialevaporation = 0.0
        elif self.pemodel_typeid == 1:
            (<masterinterface.MasterInterface>self.pemodel).determine_potentialevapotranspiration()
            self.sequences.fluxes.potentialevaporation = (<masterinterface.MasterInterface>self.pemodel).get_potentialevapotranspiration(0)
    cpdef inline void calc_adjustedevaporation_v1(self) noexcept nogil:
        cdef double d_old
        cdef double d_new
        cdef double d_weight
        d_weight = self.parameters.control.weightevaporation
        d_new = self.parameters.derived.inputfactor * self.parameters.control.correctionevaporation * self.sequences.fluxes.potentialevaporation
        d_old = self.sequences.logs.loggedadjustedevaporation[0]
        self.sequences.fluxes.adjustedevaporation = d_weight * d_new + (1.0 - d_weight) * d_old
        self.sequences.logs.loggedadjustedevaporation[0] = self.sequences.fluxes.adjustedevaporation
    cpdef inline void calc_adjustedprecipitation_v1(self) noexcept nogil:
        self.sequences.fluxes.adjustedprecipitation = (            self.parameters.derived.inputfactor * self.parameters.control.correctionprecipitation * self.sequences.fluxes.precipitation        )
    cpdef inline void pic_inflow_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.factors.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_outerwaterlevel_v1(self) noexcept nogil:
        self.sequences.factors.outerwaterlevel = self.sequences.logs.loggedouterwaterlevel[0]
    cpdef inline void calc_remotewaterlevel_v1(self) noexcept nogil:
        self.sequences.factors.remotewaterlevel = self.sequences.logs.loggedremotewaterlevel[0]
    cpdef inline void calc_waterleveldifference_v1(self) noexcept nogil:
        self.sequences.factors.waterleveldifference = self.sequences.factors.waterlevel - self.sequences.factors.outerwaterlevel
    cpdef inline void calc_maxforceddischarge_v1(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxforceddischarge.inputs[0] = self.sequences.factors.waterleveldifference
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxforceddischarge.calculate_values(toy)
        self.sequences.fluxes.maxforceddischarge = self.parameters.control.waterleveldifference2maxforceddischarge.outputs[0]
    cpdef inline void calc_forceddischarge_v1(self) noexcept nogil:
        cdef double r2
        cdef double r1
        r1 = smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelmaximumthreshold,            self.parameters.derived.waterlevelmaximumsmoothpar,        )
        r2 = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        if self.sequences.fluxes.maxforceddischarge >= 0.0:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * r1 * (1.0 - r2)
        else:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * (1.0 - r1) * r2
    cpdef inline void calc_actualevaporation_v1(self) noexcept nogil:
        self.sequences.fluxes.actualevaporation = self.sequences.fluxes.adjustedevaporation * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.thresholdevaporation, self.parameters.derived.smoothparevaporation        )
    cpdef inline void calc_outflow_v3(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.fluxes.forceddischarge
    cpdef inline void update_watervolume_v1(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + self.parameters.derived.seconds / 1e6 * (            self.sequences.fluxes.adjustedprecipitation - self.sequences.fluxes.actualevaporation + self.sequences.fluxes.inflow - self.sequences.fluxes.outflow        )
    cpdef inline void pass_outflow_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
    cpdef inline void pick_loggedouterwaterlevel(self) noexcept nogil:
        self.sequences.logs.loggedouterwaterlevel[0] = self.sequences.receivers.owl
    cpdef inline void pick_loggedremotewaterlevel(self) noexcept nogil:
        self.sequences.logs.loggedremotewaterlevel[0] = self.sequences.receivers.rwl
    cpdef inline void calc_precipitation(self) noexcept nogil:
        if self.precipmodel is None:
            self.sequences.fluxes.precipitation = 0.0
        elif self.precipmodel_typeid == 2:
            (<masterinterface.MasterInterface>self.precipmodel).determine_precipitation()
            self.sequences.fluxes.precipitation = (<masterinterface.MasterInterface>self.precipmodel).get_precipitation(0)
    cpdef inline void calc_potentialevaporation(self) noexcept nogil:
        if self.pemodel is None:
            self.sequences.fluxes.potentialevaporation = 0.0
        elif self.pemodel_typeid == 1:
            (<masterinterface.MasterInterface>self.pemodel).determine_potentialevapotranspiration()
            self.sequences.fluxes.potentialevaporation = (<masterinterface.MasterInterface>self.pemodel).get_potentialevapotranspiration(0)
    cpdef inline void calc_adjustedevaporation(self) noexcept nogil:
        cdef double d_old
        cdef double d_new
        cdef double d_weight
        d_weight = self.parameters.control.weightevaporation
        d_new = self.parameters.derived.inputfactor * self.parameters.control.correctionevaporation * self.sequences.fluxes.potentialevaporation
        d_old = self.sequences.logs.loggedadjustedevaporation[0]
        self.sequences.fluxes.adjustedevaporation = d_weight * d_new + (1.0 - d_weight) * d_old
        self.sequences.logs.loggedadjustedevaporation[0] = self.sequences.fluxes.adjustedevaporation
    cpdef inline void calc_adjustedprecipitation(self) noexcept nogil:
        self.sequences.fluxes.adjustedprecipitation = (            self.parameters.derived.inputfactor * self.parameters.control.correctionprecipitation * self.sequences.fluxes.precipitation        )
    cpdef inline void pic_inflow(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void calc_waterlevel(self) noexcept nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.factors.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_outerwaterlevel(self) noexcept nogil:
        self.sequences.factors.outerwaterlevel = self.sequences.logs.loggedouterwaterlevel[0]
    cpdef inline void calc_remotewaterlevel(self) noexcept nogil:
        self.sequences.factors.remotewaterlevel = self.sequences.logs.loggedremotewaterlevel[0]
    cpdef inline void calc_waterleveldifference(self) noexcept nogil:
        self.sequences.factors.waterleveldifference = self.sequences.factors.waterlevel - self.sequences.factors.outerwaterlevel
    cpdef inline void calc_maxforceddischarge(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxforceddischarge.inputs[0] = self.sequences.factors.waterleveldifference
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxforceddischarge.calculate_values(toy)
        self.sequences.fluxes.maxforceddischarge = self.parameters.control.waterleveldifference2maxforceddischarge.outputs[0]
    cpdef inline void calc_forceddischarge(self) noexcept nogil:
        cdef double r2
        cdef double r1
        r1 = smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelmaximumthreshold,            self.parameters.derived.waterlevelmaximumsmoothpar,        )
        r2 = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        if self.sequences.fluxes.maxforceddischarge >= 0.0:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * r1 * (1.0 - r2)
        else:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * (1.0 - r1) * r2
    cpdef inline void calc_actualevaporation(self) noexcept nogil:
        self.sequences.fluxes.actualevaporation = self.sequences.fluxes.adjustedevaporation * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.thresholdevaporation, self.parameters.derived.smoothparevaporation        )
    cpdef inline void calc_outflow(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.fluxes.forceddischarge
    cpdef inline void update_watervolume(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + self.parameters.derived.seconds / 1e6 * (            self.sequences.fluxes.adjustedprecipitation - self.sequences.fluxes.actualevaporation + self.sequences.fluxes.inflow - self.sequences.fluxes.outflow        )
    cpdef inline void pass_outflow(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
