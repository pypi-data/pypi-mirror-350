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
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._rainfall_inputflag:
            self.rainfall = self._rainfall_inputpointer[0]
        elif self._rainfall_diskflag_reading:
            self.rainfall = self._rainfall_ncarray[0]
        elif self._rainfall_ramflag:
            self.rainfall = self._rainfall_array[idx]
        if self._capillaryrise_inputflag:
            self.capillaryrise = self._capillaryrise_inputpointer[0]
        elif self._capillaryrise_diskflag_reading:
            self.capillaryrise = self._capillaryrise_ncarray[0]
        elif self._capillaryrise_ramflag:
            self.capillaryrise = self._capillaryrise_array[idx]
        if self._evaporation_inputflag:
            self.evaporation = self._evaporation_inputpointer[0]
        elif self._evaporation_diskflag_reading:
            self.evaporation = self._evaporation_ncarray[0]
        elif self._evaporation_ramflag:
            self.evaporation = self._evaporation_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._rainfall_diskflag_writing:
            self._rainfall_ncarray[0] = self.rainfall
        if self._rainfall_ramflag:
            self._rainfall_array[idx] = self.rainfall
        if self._capillaryrise_diskflag_writing:
            self._capillaryrise_ncarray[0] = self.capillaryrise
        if self._capillaryrise_ramflag:
            self._capillaryrise_array[idx] = self.capillaryrise
        if self._evaporation_diskflag_writing:
            self._evaporation_ncarray[0] = self.evaporation
        if self._evaporation_ramflag:
            self._evaporation_array[idx] = self.evaporation
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "rainfall":
            self._rainfall_inputpointer = value.p_value
        if name == "capillaryrise":
            self._capillaryrise_inputpointer = value.p_value
        if name == "evaporation":
            self._evaporation_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._surfacewatersupply_diskflag_reading:
            k = 0
            for jdx0 in range(self._surfacewatersupply_length_0):
                self.surfacewatersupply[jdx0] = self._surfacewatersupply_ncarray[k]
                k += 1
        elif self._surfacewatersupply_ramflag:
            for jdx0 in range(self._surfacewatersupply_length_0):
                self.surfacewatersupply[jdx0] = self._surfacewatersupply_array[idx, jdx0]
        if self._soilwatersupply_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilwatersupply_length_0):
                self.soilwatersupply[jdx0] = self._soilwatersupply_ncarray[k]
                k += 1
        elif self._soilwatersupply_ramflag:
            for jdx0 in range(self._soilwatersupply_length_0):
                self.soilwatersupply[jdx0] = self._soilwatersupply_array[idx, jdx0]
        if self._demand_diskflag_reading:
            k = 0
            for jdx0 in range(self._demand_length_0):
                self.demand[jdx0] = self._demand_ncarray[k]
                k += 1
        elif self._demand_ramflag:
            for jdx0 in range(self._demand_length_0):
                self.demand[jdx0] = self._demand_array[idx, jdx0]
        if self._infiltration_diskflag_reading:
            k = 0
            for jdx0 in range(self._infiltration_length_0):
                self.infiltration[jdx0] = self._infiltration_ncarray[k]
                k += 1
        elif self._infiltration_ramflag:
            for jdx0 in range(self._infiltration_length_0):
                self.infiltration[jdx0] = self._infiltration_array[idx, jdx0]
        if self._percolation_diskflag_reading:
            k = 0
            for jdx0 in range(self._percolation_length_0):
                self.percolation[jdx0] = self._percolation_ncarray[k]
                k += 1
        elif self._percolation_ramflag:
            for jdx0 in range(self._percolation_length_0):
                self.percolation[jdx0] = self._percolation_array[idx, jdx0]
        if self._soilwateraddition_diskflag_reading:
            k = 0
            for jdx0 in range(self._soilwateraddition_length_0):
                self.soilwateraddition[jdx0] = self._soilwateraddition_ncarray[k]
                k += 1
        elif self._soilwateraddition_ramflag:
            for jdx0 in range(self._soilwateraddition_length_0):
                self.soilwateraddition[jdx0] = self._soilwateraddition_array[idx, jdx0]
        if self._withdrawal_diskflag_reading:
            k = 0
            for jdx0 in range(self._withdrawal_length_0):
                self.withdrawal[jdx0] = self._withdrawal_ncarray[k]
                k += 1
        elif self._withdrawal_ramflag:
            for jdx0 in range(self._withdrawal_length_0):
                self.withdrawal[jdx0] = self._withdrawal_array[idx, jdx0]
        if self._surfacerunoff_diskflag_reading:
            k = 0
            for jdx0 in range(self._surfacerunoff_length_0):
                self.surfacerunoff[jdx0] = self._surfacerunoff_ncarray[k]
                k += 1
        elif self._surfacerunoff_ramflag:
            for jdx0 in range(self._surfacerunoff_length_0):
                self.surfacerunoff[jdx0] = self._surfacerunoff_array[idx, jdx0]
        if self._totalinfiltration_diskflag_reading:
            self.totalinfiltration = self._totalinfiltration_ncarray[0]
        elif self._totalinfiltration_ramflag:
            self.totalinfiltration = self._totalinfiltration_array[idx]
        if self._totalpercolation_diskflag_reading:
            self.totalpercolation = self._totalpercolation_ncarray[0]
        elif self._totalpercolation_ramflag:
            self.totalpercolation = self._totalpercolation_array[idx]
        if self._totalsoilwateraddition_diskflag_reading:
            self.totalsoilwateraddition = self._totalsoilwateraddition_ncarray[0]
        elif self._totalsoilwateraddition_ramflag:
            self.totalsoilwateraddition = self._totalsoilwateraddition_array[idx]
        if self._totalwithdrawal_diskflag_reading:
            self.totalwithdrawal = self._totalwithdrawal_ncarray[0]
        elif self._totalwithdrawal_ramflag:
            self.totalwithdrawal = self._totalwithdrawal_array[idx]
        if self._totalsurfacerunoff_diskflag_reading:
            self.totalsurfacerunoff = self._totalsurfacerunoff_ncarray[0]
        elif self._totalsurfacerunoff_ramflag:
            self.totalsurfacerunoff = self._totalsurfacerunoff_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._surfacewatersupply_diskflag_writing:
            k = 0
            for jdx0 in range(self._surfacewatersupply_length_0):
                self._surfacewatersupply_ncarray[k] = self.surfacewatersupply[jdx0]
                k += 1
        if self._surfacewatersupply_ramflag:
            for jdx0 in range(self._surfacewatersupply_length_0):
                self._surfacewatersupply_array[idx, jdx0] = self.surfacewatersupply[jdx0]
        if self._soilwatersupply_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilwatersupply_length_0):
                self._soilwatersupply_ncarray[k] = self.soilwatersupply[jdx0]
                k += 1
        if self._soilwatersupply_ramflag:
            for jdx0 in range(self._soilwatersupply_length_0):
                self._soilwatersupply_array[idx, jdx0] = self.soilwatersupply[jdx0]
        if self._demand_diskflag_writing:
            k = 0
            for jdx0 in range(self._demand_length_0):
                self._demand_ncarray[k] = self.demand[jdx0]
                k += 1
        if self._demand_ramflag:
            for jdx0 in range(self._demand_length_0):
                self._demand_array[idx, jdx0] = self.demand[jdx0]
        if self._infiltration_diskflag_writing:
            k = 0
            for jdx0 in range(self._infiltration_length_0):
                self._infiltration_ncarray[k] = self.infiltration[jdx0]
                k += 1
        if self._infiltration_ramflag:
            for jdx0 in range(self._infiltration_length_0):
                self._infiltration_array[idx, jdx0] = self.infiltration[jdx0]
        if self._percolation_diskflag_writing:
            k = 0
            for jdx0 in range(self._percolation_length_0):
                self._percolation_ncarray[k] = self.percolation[jdx0]
                k += 1
        if self._percolation_ramflag:
            for jdx0 in range(self._percolation_length_0):
                self._percolation_array[idx, jdx0] = self.percolation[jdx0]
        if self._soilwateraddition_diskflag_writing:
            k = 0
            for jdx0 in range(self._soilwateraddition_length_0):
                self._soilwateraddition_ncarray[k] = self.soilwateraddition[jdx0]
                k += 1
        if self._soilwateraddition_ramflag:
            for jdx0 in range(self._soilwateraddition_length_0):
                self._soilwateraddition_array[idx, jdx0] = self.soilwateraddition[jdx0]
        if self._withdrawal_diskflag_writing:
            k = 0
            for jdx0 in range(self._withdrawal_length_0):
                self._withdrawal_ncarray[k] = self.withdrawal[jdx0]
                k += 1
        if self._withdrawal_ramflag:
            for jdx0 in range(self._withdrawal_length_0):
                self._withdrawal_array[idx, jdx0] = self.withdrawal[jdx0]
        if self._surfacerunoff_diskflag_writing:
            k = 0
            for jdx0 in range(self._surfacerunoff_length_0):
                self._surfacerunoff_ncarray[k] = self.surfacerunoff[jdx0]
                k += 1
        if self._surfacerunoff_ramflag:
            for jdx0 in range(self._surfacerunoff_length_0):
                self._surfacerunoff_array[idx, jdx0] = self.surfacerunoff[jdx0]
        if self._totalinfiltration_diskflag_writing:
            self._totalinfiltration_ncarray[0] = self.totalinfiltration
        if self._totalinfiltration_ramflag:
            self._totalinfiltration_array[idx] = self.totalinfiltration
        if self._totalpercolation_diskflag_writing:
            self._totalpercolation_ncarray[0] = self.totalpercolation
        if self._totalpercolation_ramflag:
            self._totalpercolation_array[idx] = self.totalpercolation
        if self._totalsoilwateraddition_diskflag_writing:
            self._totalsoilwateraddition_ncarray[0] = self.totalsoilwateraddition
        if self._totalsoilwateraddition_ramflag:
            self._totalsoilwateraddition_array[idx] = self.totalsoilwateraddition
        if self._totalwithdrawal_diskflag_writing:
            self._totalwithdrawal_ncarray[0] = self.totalwithdrawal
        if self._totalwithdrawal_ramflag:
            self._totalwithdrawal_array[idx] = self.totalwithdrawal
        if self._totalsurfacerunoff_diskflag_writing:
            self._totalsurfacerunoff_ncarray[0] = self.totalsurfacerunoff
        if self._totalsurfacerunoff_ramflag:
            self._totalsurfacerunoff_array[idx] = self.totalsurfacerunoff
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "totalinfiltration":
            self._totalinfiltration_outputpointer = value.p_value
        if name == "totalpercolation":
            self._totalpercolation_outputpointer = value.p_value
        if name == "totalsoilwateraddition":
            self._totalsoilwateraddition_outputpointer = value.p_value
        if name == "totalwithdrawal":
            self._totalwithdrawal_outputpointer = value.p_value
        if name == "totalsurfacerunoff":
            self._totalsurfacerunoff_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._totalinfiltration_outputflag:
            self._totalinfiltration_outputpointer[0] = self.totalinfiltration
        if self._totalpercolation_outputflag:
            self._totalpercolation_outputpointer[0] = self.totalpercolation
        if self._totalsoilwateraddition_outputflag:
            self._totalsoilwateraddition_outputpointer[0] = self.totalsoilwateraddition
        if self._totalwithdrawal_outputflag:
            self._totalwithdrawal_outputpointer[0] = self.totalwithdrawal
        if self._totalsurfacerunoff_outputflag:
            self._totalsurfacerunoff_outputpointer[0] = self.totalsurfacerunoff
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._moisture_diskflag_reading:
            k = 0
            for jdx0 in range(self._moisture_length_0):
                for jdx1 in range(self._moisture_length_1):
                    self.moisture[jdx0, jdx1] = self._moisture_ncarray[k]
                    k += 1
        elif self._moisture_ramflag:
            for jdx0 in range(self._moisture_length_0):
                for jdx1 in range(self._moisture_length_1):
                    self.moisture[jdx0, jdx1] = self._moisture_array[idx, jdx0, jdx1]
        if self._frontdepth_diskflag_reading:
            k = 0
            for jdx0 in range(self._frontdepth_length_0):
                for jdx1 in range(self._frontdepth_length_1):
                    self.frontdepth[jdx0, jdx1] = self._frontdepth_ncarray[k]
                    k += 1
        elif self._frontdepth_ramflag:
            for jdx0 in range(self._frontdepth_length_0):
                for jdx1 in range(self._frontdepth_length_1):
                    self.frontdepth[jdx0, jdx1] = self._frontdepth_array[idx, jdx0, jdx1]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._moisture_diskflag_writing:
            k = 0
            for jdx0 in range(self._moisture_length_0):
                for jdx1 in range(self._moisture_length_1):
                    self._moisture_ncarray[k] = self.moisture[jdx0, jdx1]
                    k += 1
        if self._moisture_ramflag:
            for jdx0 in range(self._moisture_length_0):
                for jdx1 in range(self._moisture_length_1):
                    self._moisture_array[idx, jdx0, jdx1] = self.moisture[jdx0, jdx1]
        if self._frontdepth_diskflag_writing:
            k = 0
            for jdx0 in range(self._frontdepth_length_0):
                for jdx1 in range(self._frontdepth_length_1):
                    self._frontdepth_ncarray[k] = self.frontdepth[jdx0, jdx1]
                    k += 1
        if self._frontdepth_ramflag:
            for jdx0 in range(self._frontdepth_length_0):
                for jdx1 in range(self._frontdepth_length_1):
                    self._frontdepth_array[idx, jdx0, jdx1] = self.frontdepth[jdx0, jdx1]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class LogSequences:
    pass
@cython.final
cdef class AideSequences:
    pass
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.load_data(idx)
        self.run()
        self.new2old()
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
        self.sequences.inputs.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        for jdx0 in range(self.sequences.states._moisture_length_0):
            for jdx1 in range(self.sequences.states._moisture_length_1):
                self.sequences.old_states.moisture[jdx0,jdx1] = self.sequences.new_states.moisture[jdx0,jdx1]
        for jdx0 in range(self.sequences.states._frontdepth_length_0):
            for jdx1 in range(self.sequences.states._frontdepth_length_1):
                self.sequences.old_states.frontdepth[jdx0,jdx1] = self.sequences.new_states.frontdepth[jdx0,jdx1]
    cpdef inline void run(self) noexcept nogil:
        self.calc_surfacewatersupply_v1()
        self.calc_soilwatersupply_v1()
        self.calc_demand_v1()
        self.perform_garto_v1()
        self.calc_totalinfiltration_v1()
        self.calc_totalpercolation_v1()
        self.calc_totalsoilwateraddition_v1()
        self.calc_totalwithdrawal_v1()
        self.calc_totalsurfacerunoff_v1()
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
    cpdef inline void calc_surfacewatersupply_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.surfacewatersupply[s] = self.sequences.inputs.rainfall
    cpdef inline void calc_soilwatersupply_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.soilwatersupply[s] = self.sequences.inputs.capillaryrise
    cpdef inline void calc_demand_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.demand[s] = self.sequences.inputs.evaporation
    cpdef inline void perform_garto_v1(self) noexcept nogil:
        cdef numpy.int64_t _
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.percolation[s] = 0.0
            self.sequences.fluxes.infiltration[s] = 0.0
            self.sequences.fluxes.soilwateraddition[s] = 0.0
            if self.parameters.control.sealed[s]:
                if self.sequences.fluxes.demand[s] < self.sequences.fluxes.surfacewatersupply[s]:
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.demand[s]
                    self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacewatersupply[s] - self.sequences.fluxes.demand[s]
                else:
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.surfacewatersupply[s]
                    self.sequences.fluxes.surfacerunoff[s] = 0.0
            else:
                self.sequences.aides.initialsurfacewater[s] = self.parameters.control.dt * self.sequences.fluxes.surfacewatersupply[s]
                self.sequences.fluxes.withdrawal[s] = 0.0
                self.sequences.fluxes.surfacerunoff[s] = 0.0
                for _ in range(self.parameters.derived.nmbsubsteps):
                    self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.initialsurfacewater[s]
                    self.percolate_filledbin_v1(s)
                    self.infiltrate_wettingfrontbins_v1(s)
                    self.sequences.fluxes.infiltration[s] = self.sequences.fluxes.infiltration[s] + ((                        self.sequences.aides.initialsurfacewater[s] - self.sequences.aides.actualsurfacewater[s]                    ))
                    self.merge_frontdepthovershootings_v1(s)
                    self.merge_soildepthovershootings_v1(s)
                    self.water_allbins_v1(s, self.parameters.control.dt * self.sequences.fluxes.soilwatersupply[s])
                    self.withdraw_allbins_v1(s, self.parameters.control.dt * self.sequences.fluxes.demand[s])
                    self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacerunoff[s] + (self.sequences.aides.actualsurfacewater[s])
    cpdef inline void calc_totalinfiltration_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalinfiltration = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalinfiltration = self.sequences.fluxes.totalinfiltration + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.infiltration[s])
    cpdef inline void calc_totalpercolation_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalpercolation = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalpercolation = self.sequences.fluxes.totalpercolation + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.percolation[s])
    cpdef inline void calc_totalsoilwateraddition_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalsoilwateraddition = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalsoilwateraddition = self.sequences.fluxes.totalsoilwateraddition + ((                self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.soilwateraddition[s]            ))
    cpdef inline void calc_totalwithdrawal_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalwithdrawal = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalwithdrawal = self.sequences.fluxes.totalwithdrawal + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.withdrawal[s])
    cpdef inline void calc_totalsurfacerunoff_v1(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalsurfacerunoff = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalsurfacerunoff = self.sequences.fluxes.totalsurfacerunoff + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.surfacerunoff[s])
    cpdef void set_initialsurfacewater_v1(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.aides.initialsurfacewater[s] = self.parameters.control.dt * v
    cpdef void set_actualsurfacewater_v1(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.aides.actualsurfacewater[s] = self.parameters.control.dt * v
    cpdef void set_soilwatersupply_v1(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.fluxes.soilwatersupply[s] = v
    cpdef void set_soilwaterdemand_v1(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.fluxes.demand[s] = v
    cpdef void execute_infiltration_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t _
        cdef double initialactualsurfacewater
        initialactualsurfacewater = self.sequences.aides.actualsurfacewater[s]
        self.sequences.fluxes.infiltration[s] = 0.0
        self.sequences.fluxes.percolation[s] = 0.0
        self.sequences.fluxes.surfacerunoff[s] = 0.0
        for _ in range(self.parameters.derived.nmbsubsteps):
            self.sequences.aides.actualsurfacewater[s] = initialactualsurfacewater
            self.percolate_filledbin_v1(s)
            self.infiltrate_wettingfrontbins_v1(s)
            self.sequences.fluxes.infiltration[s] = self.sequences.fluxes.infiltration[s] + (initialactualsurfacewater - self.sequences.aides.actualsurfacewater[s])
            self.merge_frontdepthovershootings_v1(s)
            self.merge_soildepthovershootings_v1(s)
            self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacerunoff[s] + (self.sequences.aides.actualsurfacewater[s])
        self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef void add_soilwater_v1(self, numpy.int64_t s) noexcept nogil:
        self.sequences.fluxes.soilwateraddition[s] = 0.0
        self.water_allbins_v1(s, self.sequences.fluxes.soilwatersupply[s])
    cpdef void remove_soilwater_v1(self, numpy.int64_t s) noexcept nogil:
        self.sequences.aides.actualsurfacewater[s] = 0.0
        self.sequences.fluxes.withdrawal[s] = 0.0
        self.withdraw_allbins_v1(s, self.sequences.fluxes.demand[s])
    cpdef double get_infiltration_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.infiltration[s]
    cpdef double get_percolation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.percolation[s]
    cpdef double get_soilwateraddition_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.soilwateraddition[s]
    cpdef double get_soilwaterremoval_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.withdrawal[s]
    cpdef double get_soilwatercontent_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        cdef double wc
        if self.parameters.control.sealed[s]:
            return 0.0
        wc = self.parameters.control.soildepth[s] * self.sequences.states.moisture[0, s]
        for b in range(1, self.parameters.control.nmbbins):
            if self.sequences.states.moisture[b, s] == self.sequences.states.moisture[0, s]:
                break
            wc = wc + (self.sequences.states.frontdepth[b, s] * (self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]))
        return wc
    cpdef inline double return_relativemoisture_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double moisture
        moisture = min(self.sequences.states.moisture[b, s], self.parameters.control.saturationmoisture[s])
        moisture = max(moisture, self.parameters.control.residualmoisture[s])
        return (moisture - self.parameters.control.residualmoisture[s]) / (            self.parameters.control.saturationmoisture[s] - self.parameters.control.residualmoisture[s]        )
    cpdef inline double return_conductivity_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        return self.parameters.control.saturatedconductivity[s] * (            self.return_relativemoisture_v1(b, s)            ** (3.0 + 2.0 / self.parameters.control.poresizedistribution[s])        )
    cpdef inline double return_capillarydrive_v1(self, numpy.int64_t b1, numpy.int64_t b2, numpy.int64_t s) noexcept nogil:
        cdef double subtrahend
        cdef double exp
        exp = 1.0 / self.parameters.control.poresizedistribution[s] + 3.0
        if self.sequences.states.moisture[b2, s] < self.parameters.control.saturationmoisture[s]:
            subtrahend = self.return_relativemoisture_v1(b2, s) ** exp
        else:
            subtrahend = 3.0 * self.parameters.control.poresizedistribution[s] + 2.0
        return (            self.parameters.control.airentrypotential[s]            * (subtrahend - self.return_relativemoisture_v1(b1, s) ** exp)            / (3.0 * self.parameters.control.poresizedistribution[s] + 1.0)        )
    cpdef inline double return_drydepth_v1(self, numpy.int64_t s) noexcept nogil:
        cdef double tau
        if self.sequences.states.moisture[0, s] < self.parameters.control.saturationmoisture[s]:
            tau = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                / (self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[0, s])            )
            return 0.5 * (                tau + (tau**2 + 4.0 * tau * self.parameters.derived.effectivecapillarysuction[s]) ** 0.5            )
        return inf
    cpdef inline numpy.int64_t return_lastactivebin_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        for b in range(self.parameters.control.nmbbins - 1, 0, -1):
            if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                return b
        return 0
    cpdef inline void active_bin_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double potinfiltration
        cdef double deltamoisture
        cdef double conductivity
        cdef double drydepth
        drydepth = self.return_drydepth_v1(s)
        conductivity = self.return_conductivity_v1(b, s)
        self.sequences.logs.moisturechange[b + 1, s] = (            self.sequences.aides.actualsurfacewater[s] - self.parameters.control.dt * 2.0 * conductivity        ) / drydepth
        if self.sequences.logs.moisturechange[b + 1, s] < 0.0:
            self.sequences.logs.moisturechange[b + 1, s] = (                self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[b, s]            )
        if self.sequences.logs.moisturechange[b + 1, s] > 0.0:
            self.sequences.states.moisture[b + 1, s] = min(                self.sequences.states.moisture[b, s] + self.sequences.logs.moisturechange[b + 1, s],                self.parameters.control.saturationmoisture[s],            )
            deltamoisture = self.sequences.states.moisture[b + 1, s] - self.sequences.states.moisture[b, s]
            potinfiltration = min(                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (self.parameters.derived.effectivecapillarysuction[s] / drydepth + 1.0),                self.parameters.control.soildepth[s] * deltamoisture,            )
            if self.sequences.aides.actualsurfacewater[s] > potinfiltration:
                self.sequences.states.frontdepth[b + 1, s] = potinfiltration / deltamoisture
                self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
            else:
                self.sequences.states.frontdepth[b + 1, s] = self.sequences.aides.actualsurfacewater[s] / deltamoisture
                self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef inline void percolate_filledbin_v1(self, numpy.int64_t s) noexcept nogil:
        cdef double potinfiltration
        self.sequences.states.frontdepth[0, s] = self.parameters.control.soildepth[s]
        potinfiltration = self.parameters.control.dt * self.return_conductivity_v1(0, s)
        if potinfiltration < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + (potinfiltration)
        else:
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + (self.sequences.aides.actualsurfacewater[s])
            self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef inline void shift_front_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double available
        cdef double deltamoisture_bb
        cdef double required
        cdef double deltamoisture_b
        cdef double drive
        cdef double cond2
        cdef double cond1
        cdef double frontshift
        cdef double drydepth
        cdef numpy.int64_t b_last
        b_last = self.return_lastactivebin_v1(s)
        drydepth = self.return_drydepth_v1(s)
        if self.sequences.states.frontdepth[b, s] < drydepth:
            frontshift = drydepth
        else:
            cond1 = self.return_conductivity_v1(b - 1, s)
            cond2 = self.return_conductivity_v1(b, s)
            drive = self.return_capillarydrive_v1(0, b_last, s)
            frontshift = (                self.parameters.control.dt * (cond2 - cond1) / (self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s])            ) * (1.0 + (drive + self.sequences.aides.initialsurfacewater[s]) / self.sequences.states.frontdepth[b, s])
        frontshift = min(frontshift, self.parameters.control.soildepth[s] - self.sequences.states.frontdepth[b, s])
        deltamoisture_b = self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]
        required = frontshift * deltamoisture_b
        if required < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (frontshift)
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (required)
        else:
            required = required - (self.sequences.aides.actualsurfacewater[s])
            self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (self.sequences.aides.actualsurfacewater[s] / deltamoisture_b)
            self.sequences.aides.actualsurfacewater[s] = 0.0
            for b_last in range(b_last, b, -1):
                deltamoisture_bb = (                    self.sequences.states.moisture[b_last, s] - self.sequences.states.moisture[b_last - 1, s]                )
                available = deltamoisture_bb * self.sequences.states.frontdepth[b_last, s]
                if available < required:
                    required = required - (available)
                    self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (available / deltamoisture_b)
                    self.sequences.states.frontdepth[b_last, s] = 0.0
                    self.sequences.states.moisture[b_last, s] = self.sequences.states.moisture[0, s]
                    self.sequences.logs.moisturechange[b_last, s] = 0.0
                else:
                    self.sequences.states.frontdepth[b_last, s] = self.sequences.states.frontdepth[b_last, s] - (required / deltamoisture_bb)
                    self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (required / deltamoisture_b)
                    break
    cpdef inline void redistribute_front_v1(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double volume
        cdef double initialcontent
        cdef double drydepth
        cdef double potinfiltration
        cdef double factor
        cdef double capillarydrive
        cdef double conductivity
        if self.sequences.states.frontdepth[b, s] > 0.0:
            conductivity = self.return_conductivity_v1(b, s)
            capillarydrive = self.return_capillarydrive_v1(b - 1, b, s)
            factor = 1.0 if self.sequences.aides.actualsurfacewater[s] > 0.0 else 1.7
            self.sequences.logs.moisturechange[b, s] = (self.parameters.control.dt / self.sequences.states.frontdepth[b, s]) * (                max(self.sequences.aides.actualsurfacewater[s], 0.0) / self.parameters.control.dt                - conductivity                - (factor * self.parameters.control.saturatedconductivity[s] * capillarydrive)                / self.sequences.states.frontdepth[b, s]            )
            potinfiltration = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (1.0 + self.parameters.derived.effectivecapillarysuction[s] / self.sequences.states.frontdepth[b, s])            )
        else:
            drydepth = self.return_drydepth_v1(s)
            conductivity = self.return_conductivity_v1(b - 1, s)
            self.sequences.logs.moisturechange[b, s] = (                self.sequences.aides.actualsurfacewater[s] - self.parameters.control.dt * conductivity            ) / drydepth
            potinfiltration = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (1.0 + self.parameters.derived.effectivecapillarysuction[s] / drydepth)            )
        initialcontent = self.sequences.states.frontdepth[b, s] * (            self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]        )
        self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] + (self.sequences.logs.moisturechange[b, s])
        self.sequences.states.moisture[b, s] = min(self.sequences.states.moisture[b, s], self.parameters.control.saturationmoisture[s])
        self.sequences.states.moisture[b, s] = max(self.sequences.states.moisture[b, s], self.sequences.states.moisture[b - 1, s])
        if self.sequences.aides.actualsurfacewater[s] > potinfiltration:
            volume = potinfiltration + initialcontent
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
        else:
            volume = self.sequences.aides.actualsurfacewater[s] + initialcontent
            self.sequences.aides.actualsurfacewater[s] = 0.0
        if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[b - 1, s]:
            self.sequences.states.frontdepth[b, s] = volume / (                self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]            )
        else:
            if b > 1:
                self.sequences.states.frontdepth[b - 1, s] = self.sequences.states.frontdepth[b - 1, s] + (volume / (                    self.sequences.states.moisture[b - 1, s] - self.sequences.states.moisture[b - 2, s]                ))
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
            elif b == 1:
                self.sequences.states.moisture[0, s] = self.sequences.states.moisture[0, s] + (volume / self.parameters.control.soildepth[s])
                for bb in range(1, self.parameters.control.nmbbins):
                    self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[0, s]
            self.sequences.states.frontdepth[b, s] = 0.0
            self.sequences.logs.moisturechange[b, s] = 0.0
    cpdef inline void infiltrate_wettingfrontbins_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        for b in range(1, self.parameters.control.nmbbins):
            if self.sequences.states.moisture[0, s] >= self.parameters.control.saturationmoisture[s]:
                break
            if self.sequences.states.moisture[b, s] >= self.parameters.control.saturationmoisture[s]:
                if self.sequences.aides.initialsurfacewater[s] < self.parameters.control.dt * self.parameters.control.saturatedconductivity[s]:
                    self.redistribute_front_v1(b, s)
                else:
                    self.shift_front_v1(b, s)
                break
            if b == self.parameters.control.nmbbins - 1:
                self.redistribute_front_v1(b, s)
                break
            if self.sequences.states.moisture[0, s] < self.sequences.states.moisture[b, s] < self.sequences.states.moisture[b + 1, s]:
                self.sequences.logs.moisturechange[b, s] = 0.0
                self.shift_front_v1(b, s)
            elif (                (self.sequences.aides.initialsurfacewater[s] > self.parameters.control.dt * self.parameters.control.saturatedconductivity[s])                and (self.sequences.logs.moisturechange[b, s] < 0.0)                and (self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s])            ):
                self.active_bin_v1(b, s)
                break
            else:
                self.redistribute_front_v1(b, s)
                break
    cpdef inline void merge_frontdepthovershootings_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double content_lastbin
        cdef double content_thisbin
        cdef numpy.int64_t b
        b = self.parameters.control.nmbbins - 1
        while b > 1:
            if (self.sequences.states.frontdepth[b, s] >= self.sequences.states.frontdepth[b - 1, s]) and (                self.sequences.states.moisture[b, s] > self.sequences.states.moisture[b - 1, s]            ):
                content_thisbin = self.sequences.states.frontdepth[b, s] * (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]                )
                content_lastbin = self.sequences.states.frontdepth[b - 1, s] * (                    self.sequences.states.moisture[b - 1, s] - self.sequences.states.moisture[b - 2, s]                )
                self.sequences.states.frontdepth[b - 1, s] = (content_thisbin + content_lastbin) / (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 2, s]                )
                self.sequences.states.moisture[b - 1, s] = self.sequences.states.moisture[b, s]
                self.sequences.states.frontdepth[b, s] = 0.0
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
                self.sequences.logs.moisturechange[b - 1, s] = 0.0
                self.sequences.logs.moisturechange[b, s] = 0.0
                for bb in range(b + 1, self.parameters.control.nmbbins):
                    if self.sequences.states.moisture[bb, s] > self.sequences.states.moisture[0, s]:
                        self.sequences.states.moisture[bb - 1, s] = self.sequences.states.moisture[bb, s]
                        self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[0, s]
                        self.sequences.states.frontdepth[bb - 1, s] = self.sequences.states.frontdepth[bb, s]
                        self.sequences.states.frontdepth[bb, s] = 0.0
                        self.sequences.logs.moisturechange[bb - 1, s] = self.sequences.logs.moisturechange[bb, s]
                        self.sequences.logs.moisturechange[bb, s] = 0.0
                b = b + (1)
            b = b - (1)
    cpdef inline void merge_soildepthovershootings_v1(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        while (self.sequences.states.frontdepth[1, s] >= self.parameters.control.soildepth[s]) and (            self.sequences.states.moisture[1, s] > self.sequences.states.moisture[0, s]        ):
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + ((self.sequences.states.frontdepth[1, s] - self.parameters.control.soildepth[s]) * (                self.sequences.states.moisture[1, s] - self.sequences.states.moisture[0, s]            ))
            self.sequences.states.frontdepth[1, s] = 0.0
            self.sequences.logs.moisturechange[1, s] = 0.0
            self.sequences.states.moisture[0, s] = self.sequences.states.moisture[1, s]
            for b in range(2, self.parameters.control.nmbbins):
                if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                    self.sequences.states.frontdepth[b - 1, s] = self.sequences.states.frontdepth[b, s]
                    self.sequences.logs.moisturechange[b - 1, s] = self.sequences.logs.moisturechange[b, s]
                    self.sequences.states.moisture[b - 1, s] = self.sequences.states.moisture[b, s]
                    self.sequences.states.frontdepth[b, s] = 0.0
                    self.sequences.logs.moisturechange[b, s] = 0.0
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
    cpdef inline void water_allbins_v1(self, numpy.int64_t s, double supply) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double initmoisture
        cdef double freecontent
        cdef double freedepth
        cdef numpy.int64_t b
        cdef numpy.int64_t bl
        cdef double rest
        if supply <= 0.0:
            return
        rest = supply
        bl = self.return_lastactivebin_v1(s)
        for b in range(bl):
            freedepth = self.parameters.control.soildepth[s] - self.sequences.states.frontdepth[b + 1, s]
            freecontent = freedepth * (                self.sequences.states.moisture[b + 1, s] - self.sequences.states.moisture[b, s]            )
            if rest <= freecontent:
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply)
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] + (rest / freedepth)
                rest = 0.0
                initmoisture = self.sequences.states.moisture[b, s]
                break
            rest = rest - (freecontent)
            self.sequences.states.frontdepth[b + 1, s] = self.parameters.control.soildepth[s]
            initmoisture = self.sequences.states.moisture[b + 1, s]
        if rest > 0.0:
            freecontent = self.parameters.control.soildepth[s] * (                self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[bl, s]            )
            if rest <= freecontent:
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply)
                self.sequences.states.moisture[bl, s] = self.sequences.states.moisture[bl, s] + (rest / self.parameters.control.soildepth[s])
            else:
                rest = rest - (freecontent)
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply - rest)
                self.sequences.states.moisture[bl, s] = self.parameters.control.saturationmoisture[s]
            initmoisture = self.sequences.states.moisture[bl, s]
        for b in range(self.parameters.control.nmbbins):
            if self.sequences.states.moisture[b, s] <= initmoisture:
                self.sequences.states.moisture[b, s] = initmoisture
        for b in range(bl):
            while (self.sequences.states.moisture[b, s] == self.sequences.states.moisture[b + 1, s]) and (                self.sequences.states.frontdepth[b + 1, s] > 0.0            ):
                self.sequences.states.frontdepth[b + 1] = self.sequences.states.frontdepth[b]
                for bb in range(b, self.parameters.control.nmbbins - 1):
                    self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[bb + 1, s]
                    self.sequences.states.frontdepth[bb, s] = self.sequences.states.frontdepth[bb + 1, s]
                    self.sequences.logs.moisturechange[bb, s] = self.sequences.logs.moisturechange[bb + 1, s]
                self.sequences.states.moisture[self.parameters.control.nmbbins - 1, s] = self.sequences.states.moisture[0, s]
                self.sequences.states.frontdepth[self.parameters.control.nmbbins - 1, s] = 0.0
                self.sequences.logs.moisturechange[self.parameters.control.nmbbins - 1, s] = 0.0
        self.sequences.logs.moisturechange[0, s] = 0.0
        return
    cpdef inline void withdraw_allbins_v1(self, numpy.int64_t s, double demand) noexcept nogil:
        cdef double available
        cdef numpy.int64_t b
        if demand <= 0.0:
            return
        if demand < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (demand)
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
            return
        demand = demand - (self.sequences.aides.actualsurfacewater[s])
        self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (self.sequences.aides.actualsurfacewater[s])
        self.sequences.aides.actualsurfacewater[s] = 0.0
        for b in range(self.parameters.control.nmbbins - 1, 0, -1):
            if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                available = self.sequences.states.frontdepth[b, s] * (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]                )
                if demand <= available:
                    self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] - (demand / self.sequences.states.frontdepth[b, s])
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
                    return
                self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (available)
                demand = demand - (available)
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
                self.sequences.states.frontdepth[b, s] = 0.0
        if self.sequences.states.moisture[0, s] <= self.parameters.control.residualmoisture[s]:
            return
        available = self.parameters.control.soildepth[s] * (self.sequences.states.moisture[0, s] - self.parameters.control.residualmoisture[s])
        if demand <= available:
            self.sequences.states.moisture[0, s] = self.sequences.states.moisture[0, s] - (demand / self.parameters.control.soildepth[s])
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
        else:
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (available)
            self.sequences.states.moisture[0, s] = self.parameters.control.residualmoisture[s]
        return
    cpdef inline void calc_surfacewatersupply(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.surfacewatersupply[s] = self.sequences.inputs.rainfall
    cpdef inline void calc_soilwatersupply(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.soilwatersupply[s] = self.sequences.inputs.capillaryrise
    cpdef inline void calc_demand(self) noexcept nogil:
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.demand[s] = self.sequences.inputs.evaporation
    cpdef inline void perform_garto(self) noexcept nogil:
        cdef numpy.int64_t _
        cdef numpy.int64_t s
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.percolation[s] = 0.0
            self.sequences.fluxes.infiltration[s] = 0.0
            self.sequences.fluxes.soilwateraddition[s] = 0.0
            if self.parameters.control.sealed[s]:
                if self.sequences.fluxes.demand[s] < self.sequences.fluxes.surfacewatersupply[s]:
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.demand[s]
                    self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacewatersupply[s] - self.sequences.fluxes.demand[s]
                else:
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.surfacewatersupply[s]
                    self.sequences.fluxes.surfacerunoff[s] = 0.0
            else:
                self.sequences.aides.initialsurfacewater[s] = self.parameters.control.dt * self.sequences.fluxes.surfacewatersupply[s]
                self.sequences.fluxes.withdrawal[s] = 0.0
                self.sequences.fluxes.surfacerunoff[s] = 0.0
                for _ in range(self.parameters.derived.nmbsubsteps):
                    self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.initialsurfacewater[s]
                    self.percolate_filledbin_v1(s)
                    self.infiltrate_wettingfrontbins_v1(s)
                    self.sequences.fluxes.infiltration[s] = self.sequences.fluxes.infiltration[s] + ((                        self.sequences.aides.initialsurfacewater[s] - self.sequences.aides.actualsurfacewater[s]                    ))
                    self.merge_frontdepthovershootings_v1(s)
                    self.merge_soildepthovershootings_v1(s)
                    self.water_allbins_v1(s, self.parameters.control.dt * self.sequences.fluxes.soilwatersupply[s])
                    self.withdraw_allbins_v1(s, self.parameters.control.dt * self.sequences.fluxes.demand[s])
                    self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacerunoff[s] + (self.sequences.aides.actualsurfacewater[s])
    cpdef inline void calc_totalinfiltration(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalinfiltration = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalinfiltration = self.sequences.fluxes.totalinfiltration + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.infiltration[s])
    cpdef inline void calc_totalpercolation(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalpercolation = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalpercolation = self.sequences.fluxes.totalpercolation + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.percolation[s])
    cpdef inline void calc_totalsoilwateraddition(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalsoilwateraddition = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalsoilwateraddition = self.sequences.fluxes.totalsoilwateraddition + ((                self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.soilwateraddition[s]            ))
    cpdef inline void calc_totalwithdrawal(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalwithdrawal = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalwithdrawal = self.sequences.fluxes.totalwithdrawal + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.withdrawal[s])
    cpdef inline void calc_totalsurfacerunoff(self) noexcept nogil:
        cdef numpy.int64_t s
        self.sequences.fluxes.totalsurfacerunoff = 0.0
        for s in range(self.parameters.control.nmbsoils):
            self.sequences.fluxes.totalsurfacerunoff = self.sequences.fluxes.totalsurfacerunoff + (self.parameters.derived.soilareafraction[s] * self.sequences.fluxes.surfacerunoff[s])
    cpdef void set_initialsurfacewater(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.aides.initialsurfacewater[s] = self.parameters.control.dt * v
    cpdef void set_actualsurfacewater(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.aides.actualsurfacewater[s] = self.parameters.control.dt * v
    cpdef void set_soilwatersupply(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.fluxes.soilwatersupply[s] = v
    cpdef void set_soilwaterdemand(self, numpy.int64_t s, double v) noexcept nogil:
        self.sequences.fluxes.demand[s] = v
    cpdef void execute_infiltration(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t _
        cdef double initialactualsurfacewater
        initialactualsurfacewater = self.sequences.aides.actualsurfacewater[s]
        self.sequences.fluxes.infiltration[s] = 0.0
        self.sequences.fluxes.percolation[s] = 0.0
        self.sequences.fluxes.surfacerunoff[s] = 0.0
        for _ in range(self.parameters.derived.nmbsubsteps):
            self.sequences.aides.actualsurfacewater[s] = initialactualsurfacewater
            self.percolate_filledbin_v1(s)
            self.infiltrate_wettingfrontbins_v1(s)
            self.sequences.fluxes.infiltration[s] = self.sequences.fluxes.infiltration[s] + (initialactualsurfacewater - self.sequences.aides.actualsurfacewater[s])
            self.merge_frontdepthovershootings_v1(s)
            self.merge_soildepthovershootings_v1(s)
            self.sequences.fluxes.surfacerunoff[s] = self.sequences.fluxes.surfacerunoff[s] + (self.sequences.aides.actualsurfacewater[s])
        self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef void add_soilwater(self, numpy.int64_t s) noexcept nogil:
        self.sequences.fluxes.soilwateraddition[s] = 0.0
        self.water_allbins_v1(s, self.sequences.fluxes.soilwatersupply[s])
    cpdef void remove_soilwater(self, numpy.int64_t s) noexcept nogil:
        self.sequences.aides.actualsurfacewater[s] = 0.0
        self.sequences.fluxes.withdrawal[s] = 0.0
        self.withdraw_allbins_v1(s, self.sequences.fluxes.demand[s])
    cpdef double get_infiltration(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.infiltration[s]
    cpdef double get_percolation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.percolation[s]
    cpdef double get_soilwateraddition(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.soilwateraddition[s]
    cpdef double get_soilwaterremoval(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.withdrawal[s]
    cpdef double get_soilwatercontent(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        cdef double wc
        if self.parameters.control.sealed[s]:
            return 0.0
        wc = self.parameters.control.soildepth[s] * self.sequences.states.moisture[0, s]
        for b in range(1, self.parameters.control.nmbbins):
            if self.sequences.states.moisture[b, s] == self.sequences.states.moisture[0, s]:
                break
            wc = wc + (self.sequences.states.frontdepth[b, s] * (self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]))
        return wc
    cpdef inline double return_relativemoisture(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double moisture
        moisture = min(self.sequences.states.moisture[b, s], self.parameters.control.saturationmoisture[s])
        moisture = max(moisture, self.parameters.control.residualmoisture[s])
        return (moisture - self.parameters.control.residualmoisture[s]) / (            self.parameters.control.saturationmoisture[s] - self.parameters.control.residualmoisture[s]        )
    cpdef inline double return_conductivity(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        return self.parameters.control.saturatedconductivity[s] * (            self.return_relativemoisture_v1(b, s)            ** (3.0 + 2.0 / self.parameters.control.poresizedistribution[s])        )
    cpdef inline double return_capillarydrive(self, numpy.int64_t b1, numpy.int64_t b2, numpy.int64_t s) noexcept nogil:
        cdef double subtrahend
        cdef double exp
        exp = 1.0 / self.parameters.control.poresizedistribution[s] + 3.0
        if self.sequences.states.moisture[b2, s] < self.parameters.control.saturationmoisture[s]:
            subtrahend = self.return_relativemoisture_v1(b2, s) ** exp
        else:
            subtrahend = 3.0 * self.parameters.control.poresizedistribution[s] + 2.0
        return (            self.parameters.control.airentrypotential[s]            * (subtrahend - self.return_relativemoisture_v1(b1, s) ** exp)            / (3.0 * self.parameters.control.poresizedistribution[s] + 1.0)        )
    cpdef inline double return_drydepth(self, numpy.int64_t s) noexcept nogil:
        cdef double tau
        if self.sequences.states.moisture[0, s] < self.parameters.control.saturationmoisture[s]:
            tau = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                / (self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[0, s])            )
            return 0.5 * (                tau + (tau**2 + 4.0 * tau * self.parameters.derived.effectivecapillarysuction[s]) ** 0.5            )
        return inf
    cpdef inline numpy.int64_t return_lastactivebin(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        for b in range(self.parameters.control.nmbbins - 1, 0, -1):
            if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                return b
        return 0
    cpdef inline void active_bin(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double potinfiltration
        cdef double deltamoisture
        cdef double conductivity
        cdef double drydepth
        drydepth = self.return_drydepth_v1(s)
        conductivity = self.return_conductivity_v1(b, s)
        self.sequences.logs.moisturechange[b + 1, s] = (            self.sequences.aides.actualsurfacewater[s] - self.parameters.control.dt * 2.0 * conductivity        ) / drydepth
        if self.sequences.logs.moisturechange[b + 1, s] < 0.0:
            self.sequences.logs.moisturechange[b + 1, s] = (                self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[b, s]            )
        if self.sequences.logs.moisturechange[b + 1, s] > 0.0:
            self.sequences.states.moisture[b + 1, s] = min(                self.sequences.states.moisture[b, s] + self.sequences.logs.moisturechange[b + 1, s],                self.parameters.control.saturationmoisture[s],            )
            deltamoisture = self.sequences.states.moisture[b + 1, s] - self.sequences.states.moisture[b, s]
            potinfiltration = min(                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (self.parameters.derived.effectivecapillarysuction[s] / drydepth + 1.0),                self.parameters.control.soildepth[s] * deltamoisture,            )
            if self.sequences.aides.actualsurfacewater[s] > potinfiltration:
                self.sequences.states.frontdepth[b + 1, s] = potinfiltration / deltamoisture
                self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
            else:
                self.sequences.states.frontdepth[b + 1, s] = self.sequences.aides.actualsurfacewater[s] / deltamoisture
                self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef inline void percolate_filledbin(self, numpy.int64_t s) noexcept nogil:
        cdef double potinfiltration
        self.sequences.states.frontdepth[0, s] = self.parameters.control.soildepth[s]
        potinfiltration = self.parameters.control.dt * self.return_conductivity_v1(0, s)
        if potinfiltration < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + (potinfiltration)
        else:
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + (self.sequences.aides.actualsurfacewater[s])
            self.sequences.aides.actualsurfacewater[s] = 0.0
    cpdef inline void shift_front(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef double available
        cdef double deltamoisture_bb
        cdef double required
        cdef double deltamoisture_b
        cdef double drive
        cdef double cond2
        cdef double cond1
        cdef double frontshift
        cdef double drydepth
        cdef numpy.int64_t b_last
        b_last = self.return_lastactivebin_v1(s)
        drydepth = self.return_drydepth_v1(s)
        if self.sequences.states.frontdepth[b, s] < drydepth:
            frontshift = drydepth
        else:
            cond1 = self.return_conductivity_v1(b - 1, s)
            cond2 = self.return_conductivity_v1(b, s)
            drive = self.return_capillarydrive_v1(0, b_last, s)
            frontshift = (                self.parameters.control.dt * (cond2 - cond1) / (self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s])            ) * (1.0 + (drive + self.sequences.aides.initialsurfacewater[s]) / self.sequences.states.frontdepth[b, s])
        frontshift = min(frontshift, self.parameters.control.soildepth[s] - self.sequences.states.frontdepth[b, s])
        deltamoisture_b = self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]
        required = frontshift * deltamoisture_b
        if required < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (frontshift)
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (required)
        else:
            required = required - (self.sequences.aides.actualsurfacewater[s])
            self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (self.sequences.aides.actualsurfacewater[s] / deltamoisture_b)
            self.sequences.aides.actualsurfacewater[s] = 0.0
            for b_last in range(b_last, b, -1):
                deltamoisture_bb = (                    self.sequences.states.moisture[b_last, s] - self.sequences.states.moisture[b_last - 1, s]                )
                available = deltamoisture_bb * self.sequences.states.frontdepth[b_last, s]
                if available < required:
                    required = required - (available)
                    self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (available / deltamoisture_b)
                    self.sequences.states.frontdepth[b_last, s] = 0.0
                    self.sequences.states.moisture[b_last, s] = self.sequences.states.moisture[0, s]
                    self.sequences.logs.moisturechange[b_last, s] = 0.0
                else:
                    self.sequences.states.frontdepth[b_last, s] = self.sequences.states.frontdepth[b_last, s] - (required / deltamoisture_bb)
                    self.sequences.states.frontdepth[b, s] = self.sequences.states.frontdepth[b, s] + (required / deltamoisture_b)
                    break
    cpdef inline void redistribute_front(self, numpy.int64_t b, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double volume
        cdef double initialcontent
        cdef double drydepth
        cdef double potinfiltration
        cdef double factor
        cdef double capillarydrive
        cdef double conductivity
        if self.sequences.states.frontdepth[b, s] > 0.0:
            conductivity = self.return_conductivity_v1(b, s)
            capillarydrive = self.return_capillarydrive_v1(b - 1, b, s)
            factor = 1.0 if self.sequences.aides.actualsurfacewater[s] > 0.0 else 1.7
            self.sequences.logs.moisturechange[b, s] = (self.parameters.control.dt / self.sequences.states.frontdepth[b, s]) * (                max(self.sequences.aides.actualsurfacewater[s], 0.0) / self.parameters.control.dt                - conductivity                - (factor * self.parameters.control.saturatedconductivity[s] * capillarydrive)                / self.sequences.states.frontdepth[b, s]            )
            potinfiltration = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (1.0 + self.parameters.derived.effectivecapillarysuction[s] / self.sequences.states.frontdepth[b, s])            )
        else:
            drydepth = self.return_drydepth_v1(s)
            conductivity = self.return_conductivity_v1(b - 1, s)
            self.sequences.logs.moisturechange[b, s] = (                self.sequences.aides.actualsurfacewater[s] - self.parameters.control.dt * conductivity            ) / drydepth
            potinfiltration = (                self.parameters.control.dt                * self.parameters.control.saturatedconductivity[s]                * (1.0 + self.parameters.derived.effectivecapillarysuction[s] / drydepth)            )
        initialcontent = self.sequences.states.frontdepth[b, s] * (            self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]        )
        self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] + (self.sequences.logs.moisturechange[b, s])
        self.sequences.states.moisture[b, s] = min(self.sequences.states.moisture[b, s], self.parameters.control.saturationmoisture[s])
        self.sequences.states.moisture[b, s] = max(self.sequences.states.moisture[b, s], self.sequences.states.moisture[b - 1, s])
        if self.sequences.aides.actualsurfacewater[s] > potinfiltration:
            volume = potinfiltration + initialcontent
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (potinfiltration)
        else:
            volume = self.sequences.aides.actualsurfacewater[s] + initialcontent
            self.sequences.aides.actualsurfacewater[s] = 0.0
        if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[b - 1, s]:
            self.sequences.states.frontdepth[b, s] = volume / (                self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]            )
        else:
            if b > 1:
                self.sequences.states.frontdepth[b - 1, s] = self.sequences.states.frontdepth[b - 1, s] + (volume / (                    self.sequences.states.moisture[b - 1, s] - self.sequences.states.moisture[b - 2, s]                ))
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
            elif b == 1:
                self.sequences.states.moisture[0, s] = self.sequences.states.moisture[0, s] + (volume / self.parameters.control.soildepth[s])
                for bb in range(1, self.parameters.control.nmbbins):
                    self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[0, s]
            self.sequences.states.frontdepth[b, s] = 0.0
            self.sequences.logs.moisturechange[b, s] = 0.0
    cpdef inline void infiltrate_wettingfrontbins(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        for b in range(1, self.parameters.control.nmbbins):
            if self.sequences.states.moisture[0, s] >= self.parameters.control.saturationmoisture[s]:
                break
            if self.sequences.states.moisture[b, s] >= self.parameters.control.saturationmoisture[s]:
                if self.sequences.aides.initialsurfacewater[s] < self.parameters.control.dt * self.parameters.control.saturatedconductivity[s]:
                    self.redistribute_front_v1(b, s)
                else:
                    self.shift_front_v1(b, s)
                break
            if b == self.parameters.control.nmbbins - 1:
                self.redistribute_front_v1(b, s)
                break
            if self.sequences.states.moisture[0, s] < self.sequences.states.moisture[b, s] < self.sequences.states.moisture[b + 1, s]:
                self.sequences.logs.moisturechange[b, s] = 0.0
                self.shift_front_v1(b, s)
            elif (                (self.sequences.aides.initialsurfacewater[s] > self.parameters.control.dt * self.parameters.control.saturatedconductivity[s])                and (self.sequences.logs.moisturechange[b, s] < 0.0)                and (self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s])            ):
                self.active_bin_v1(b, s)
                break
            else:
                self.redistribute_front_v1(b, s)
                break
    cpdef inline void merge_frontdepthovershootings(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double content_lastbin
        cdef double content_thisbin
        cdef numpy.int64_t b
        b = self.parameters.control.nmbbins - 1
        while b > 1:
            if (self.sequences.states.frontdepth[b, s] >= self.sequences.states.frontdepth[b - 1, s]) and (                self.sequences.states.moisture[b, s] > self.sequences.states.moisture[b - 1, s]            ):
                content_thisbin = self.sequences.states.frontdepth[b, s] * (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]                )
                content_lastbin = self.sequences.states.frontdepth[b - 1, s] * (                    self.sequences.states.moisture[b - 1, s] - self.sequences.states.moisture[b - 2, s]                )
                self.sequences.states.frontdepth[b - 1, s] = (content_thisbin + content_lastbin) / (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 2, s]                )
                self.sequences.states.moisture[b - 1, s] = self.sequences.states.moisture[b, s]
                self.sequences.states.frontdepth[b, s] = 0.0
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
                self.sequences.logs.moisturechange[b - 1, s] = 0.0
                self.sequences.logs.moisturechange[b, s] = 0.0
                for bb in range(b + 1, self.parameters.control.nmbbins):
                    if self.sequences.states.moisture[bb, s] > self.sequences.states.moisture[0, s]:
                        self.sequences.states.moisture[bb - 1, s] = self.sequences.states.moisture[bb, s]
                        self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[0, s]
                        self.sequences.states.frontdepth[bb - 1, s] = self.sequences.states.frontdepth[bb, s]
                        self.sequences.states.frontdepth[bb, s] = 0.0
                        self.sequences.logs.moisturechange[bb - 1, s] = self.sequences.logs.moisturechange[bb, s]
                        self.sequences.logs.moisturechange[bb, s] = 0.0
                b = b + (1)
            b = b - (1)
    cpdef inline void merge_soildepthovershootings(self, numpy.int64_t s) noexcept nogil:
        cdef numpy.int64_t b
        while (self.sequences.states.frontdepth[1, s] >= self.parameters.control.soildepth[s]) and (            self.sequences.states.moisture[1, s] > self.sequences.states.moisture[0, s]        ):
            self.sequences.fluxes.percolation[s] = self.sequences.fluxes.percolation[s] + ((self.sequences.states.frontdepth[1, s] - self.parameters.control.soildepth[s]) * (                self.sequences.states.moisture[1, s] - self.sequences.states.moisture[0, s]            ))
            self.sequences.states.frontdepth[1, s] = 0.0
            self.sequences.logs.moisturechange[1, s] = 0.0
            self.sequences.states.moisture[0, s] = self.sequences.states.moisture[1, s]
            for b in range(2, self.parameters.control.nmbbins):
                if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                    self.sequences.states.frontdepth[b - 1, s] = self.sequences.states.frontdepth[b, s]
                    self.sequences.logs.moisturechange[b - 1, s] = self.sequences.logs.moisturechange[b, s]
                    self.sequences.states.moisture[b - 1, s] = self.sequences.states.moisture[b, s]
                    self.sequences.states.frontdepth[b, s] = 0.0
                    self.sequences.logs.moisturechange[b, s] = 0.0
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
    cpdef inline void water_allbins(self, numpy.int64_t s, double supply) noexcept nogil:
        cdef numpy.int64_t bb
        cdef double initmoisture
        cdef double freecontent
        cdef double freedepth
        cdef numpy.int64_t b
        cdef numpy.int64_t bl
        cdef double rest
        if supply <= 0.0:
            return
        rest = supply
        bl = self.return_lastactivebin_v1(s)
        for b in range(bl):
            freedepth = self.parameters.control.soildepth[s] - self.sequences.states.frontdepth[b + 1, s]
            freecontent = freedepth * (                self.sequences.states.moisture[b + 1, s] - self.sequences.states.moisture[b, s]            )
            if rest <= freecontent:
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply)
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] + (rest / freedepth)
                rest = 0.0
                initmoisture = self.sequences.states.moisture[b, s]
                break
            rest = rest - (freecontent)
            self.sequences.states.frontdepth[b + 1, s] = self.parameters.control.soildepth[s]
            initmoisture = self.sequences.states.moisture[b + 1, s]
        if rest > 0.0:
            freecontent = self.parameters.control.soildepth[s] * (                self.parameters.control.saturationmoisture[s] - self.sequences.states.moisture[bl, s]            )
            if rest <= freecontent:
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply)
                self.sequences.states.moisture[bl, s] = self.sequences.states.moisture[bl, s] + (rest / self.parameters.control.soildepth[s])
            else:
                rest = rest - (freecontent)
                self.sequences.fluxes.soilwateraddition[s] = self.sequences.fluxes.soilwateraddition[s] + (supply - rest)
                self.sequences.states.moisture[bl, s] = self.parameters.control.saturationmoisture[s]
            initmoisture = self.sequences.states.moisture[bl, s]
        for b in range(self.parameters.control.nmbbins):
            if self.sequences.states.moisture[b, s] <= initmoisture:
                self.sequences.states.moisture[b, s] = initmoisture
        for b in range(bl):
            while (self.sequences.states.moisture[b, s] == self.sequences.states.moisture[b + 1, s]) and (                self.sequences.states.frontdepth[b + 1, s] > 0.0            ):
                self.sequences.states.frontdepth[b + 1] = self.sequences.states.frontdepth[b]
                for bb in range(b, self.parameters.control.nmbbins - 1):
                    self.sequences.states.moisture[bb, s] = self.sequences.states.moisture[bb + 1, s]
                    self.sequences.states.frontdepth[bb, s] = self.sequences.states.frontdepth[bb + 1, s]
                    self.sequences.logs.moisturechange[bb, s] = self.sequences.logs.moisturechange[bb + 1, s]
                self.sequences.states.moisture[self.parameters.control.nmbbins - 1, s] = self.sequences.states.moisture[0, s]
                self.sequences.states.frontdepth[self.parameters.control.nmbbins - 1, s] = 0.0
                self.sequences.logs.moisturechange[self.parameters.control.nmbbins - 1, s] = 0.0
        self.sequences.logs.moisturechange[0, s] = 0.0
        return
    cpdef inline void withdraw_allbins(self, numpy.int64_t s, double demand) noexcept nogil:
        cdef double available
        cdef numpy.int64_t b
        if demand <= 0.0:
            return
        if demand < self.sequences.aides.actualsurfacewater[s]:
            self.sequences.aides.actualsurfacewater[s] = self.sequences.aides.actualsurfacewater[s] - (demand)
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
            return
        demand = demand - (self.sequences.aides.actualsurfacewater[s])
        self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (self.sequences.aides.actualsurfacewater[s])
        self.sequences.aides.actualsurfacewater[s] = 0.0
        for b in range(self.parameters.control.nmbbins - 1, 0, -1):
            if self.sequences.states.moisture[b, s] > self.sequences.states.moisture[0, s]:
                available = self.sequences.states.frontdepth[b, s] * (                    self.sequences.states.moisture[b, s] - self.sequences.states.moisture[b - 1, s]                )
                if demand <= available:
                    self.sequences.states.moisture[b, s] = self.sequences.states.moisture[b, s] - (demand / self.sequences.states.frontdepth[b, s])
                    self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
                    return
                self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (available)
                demand = demand - (available)
                self.sequences.states.moisture[b, s] = self.sequences.states.moisture[0, s]
                self.sequences.states.frontdepth[b, s] = 0.0
        if self.sequences.states.moisture[0, s] <= self.parameters.control.residualmoisture[s]:
            return
        available = self.parameters.control.soildepth[s] * (self.sequences.states.moisture[0, s] - self.parameters.control.residualmoisture[s])
        if demand <= available:
            self.sequences.states.moisture[0, s] = self.sequences.states.moisture[0, s] - (demand / self.parameters.control.soildepth[s])
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (demand)
        else:
            self.sequences.fluxes.withdrawal[s] = self.sequences.fluxes.withdrawal[s] + (available)
            self.sequences.states.moisture[0, s] = self.parameters.control.residualmoisture[s]
        return
