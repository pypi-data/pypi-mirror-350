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
cdef class Sequences:
    pass
@cython.final
cdef class InletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._latq_diskflag_reading:
            k = 0
            for jdx0 in range(self._latq_length_0):
                self.latq[jdx0] = self._latq_ncarray[k]
                k += 1
        elif self._latq_ramflag:
            for jdx0 in range(self._latq_length_0):
                self.latq[jdx0] = self._latq_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._latq_diskflag_writing:
            k = 0
            for jdx0 in range(self._latq_length_0):
                self._latq_ncarray[k] = self.latq[jdx0]
                k += 1
        if self._latq_ramflag:
            for jdx0 in range(self._latq_length_0):
                self._latq_array[idx, jdx0] = self.latq[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "latq":
            self._latq_length_0 = length
            self._latq_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._latq_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "latq":
            PyMem_Free(self._latq_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "latq":
            self._latq_pointer[idx] = pointer.p_value
            self._latq_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "latq":
            values = numpy.empty(self.len_latq)
            for idx in range(self.len_latq):
                pointerutils.check0(self._latq_length_0)
                if self._latq_ready[idx] == 0:
                    pointerutils.check1(self._latq_length_0, idx)
                    pointerutils.check2(self._latq_ready, idx)
                values[idx] = self._latq_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "latq":
            for idx in range(self.len_latq):
                pointerutils.check0(self._latq_length_0)
                if self._latq_ready[idx] == 0:
                    pointerutils.check1(self._latq_length_0, idx)
                    pointerutils.check2(self._latq_ready, idx)
                self._latq_pointer[idx][0] = value[idx]
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._timestep_diskflag_reading:
            self.timestep = self._timestep_ncarray[0]
        elif self._timestep_ramflag:
            self.timestep = self._timestep_array[idx]
        if self._waterdepth_diskflag_reading:
            self.waterdepth = self._waterdepth_ncarray[0]
        elif self._waterdepth_ramflag:
            self.waterdepth = self._waterdepth_array[idx]
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._timestep_diskflag_writing:
            self._timestep_ncarray[0] = self.timestep
        if self._timestep_ramflag:
            self._timestep_array[idx] = self.timestep
        if self._waterdepth_diskflag_writing:
            self._waterdepth_ncarray[0] = self.waterdepth
        if self._waterdepth_ramflag:
            self._waterdepth_array[idx] = self.waterdepth
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "timestep":
            self._timestep_outputpointer = value.p_value
        if name == "waterdepth":
            self._waterdepth_outputpointer = value.p_value
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._timestep_outputflag:
            self._timestep_outputpointer[0] = self.timestep
        if self._waterdepth_outputflag:
            self._waterdepth_outputpointer[0] = self.waterdepth
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._lateralflow_diskflag_reading:
            self.lateralflow = self._lateralflow_ncarray[0]
        elif self._lateralflow_ramflag:
            self.lateralflow = self._lateralflow_array[idx]
        if self._netinflow_diskflag_reading:
            self.netinflow = self._netinflow_ncarray[0]
        elif self._netinflow_ramflag:
            self.netinflow = self._netinflow_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._lateralflow_diskflag_writing:
            self._lateralflow_ncarray[0] = self.lateralflow
        if self._lateralflow_ramflag:
            self._lateralflow_array[idx] = self.lateralflow
        if self._netinflow_diskflag_writing:
            self._netinflow_ncarray[0] = self.netinflow
        if self._netinflow_ramflag:
            self._netinflow_array[idx] = self.netinflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "lateralflow":
            self._lateralflow_outputpointer = value.p_value
        if name == "netinflow":
            self._netinflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._lateralflow_outputflag:
            self._lateralflow_outputpointer[0] = self.lateralflow
        if self._netinflow_outputflag:
            self._netinflow_outputpointer[0] = self.netinflow
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
cdef class SenderSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterlevel_length_0):
                self.waterlevel[jdx0] = self._waterlevel_ncarray[k]
                k += 1
        elif self._waterlevel_ramflag:
            for jdx0 in range(self._waterlevel_length_0):
                self.waterlevel[jdx0] = self._waterlevel_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._waterlevel_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterlevel_length_0):
                self._waterlevel_ncarray[k] = self.waterlevel[jdx0]
                k += 1
        if self._waterlevel_ramflag:
            for jdx0 in range(self._waterlevel_length_0):
                self._waterlevel_array[idx, jdx0] = self.waterlevel[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "waterlevel":
            self._waterlevel_length_0 = length
            self._waterlevel_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._waterlevel_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "waterlevel":
            PyMem_Free(self._waterlevel_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "waterlevel":
            self._waterlevel_pointer[idx] = pointer.p_value
            self._waterlevel_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "waterlevel":
            values = numpy.empty(self.len_waterlevel)
            for idx in range(self.len_waterlevel):
                pointerutils.check0(self._waterlevel_length_0)
                if self._waterlevel_ready[idx] == 0:
                    pointerutils.check1(self._waterlevel_length_0, idx)
                    pointerutils.check2(self._waterlevel_ready, idx)
                values[idx] = self._waterlevel_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "waterlevel":
            for idx in range(self.len_waterlevel):
                pointerutils.check0(self._waterlevel_length_0)
                if self._waterlevel_ready[idx] == 0:
                    pointerutils.check1(self._waterlevel_length_0, idx)
                    pointerutils.check2(self._waterlevel_ready, idx)
                self._waterlevel_pointer[idx][0] = value[idx]
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.crosssection = None
        self.crosssection_is_mainmodel = False
        self.routingmodelsdownstream = interfaceutils.SubmodelsProperty()
        self.routingmodelsupstream = interfaceutils.SubmodelsProperty()
    def get_crosssection(self) -> masterinterface.MasterInterface | None:
        return self.crosssection
    def set_crosssection(self, crosssection: masterinterface.MasterInterface | None) -> None:
        self.crosssection = crosssection
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
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.senders.save_data(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.watervolume = self.sequences.new_states.watervolume
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.new2old()
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef void update_inlets(self) noexcept nogil:
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_inlets()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._latq_length_0):
                if self.sequences.inlets._latq_ready[i]:
                    self.sequences.inlets.latq[i] = self.sequences.inlets._latq_pointer[i][0]
                else:
                    self.sequences.inlets.latq[i] = nan
        self.pick_lateralflow_v1()
        self.calc_waterdepth_waterlevel_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_senders(idx)
        self.pass_waterlevel_v1()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.senders._waterlevel_length_0):
                if self.sequences.senders._waterlevel_ready[i]:
                    self.sequences.senders._waterlevel_pointer[i][0] = self.sequences.senders._waterlevel_pointer[i][0] + self.sequences.senders.waterlevel[i]
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outputs()
    cpdef inline void pick_lateralflow_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.lateralflow = 0.0
        for i in range(self.sequences.inlets.len_latq):
            self.sequences.fluxes.lateralflow = self.sequences.fluxes.lateralflow + (self.sequences.inlets.latq[i])
    cpdef inline void calc_waterdepth_waterlevel_v1(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_waterlevel_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef double get_watervolume_v1(self) noexcept nogil:
        return self.sequences.states.watervolume
    cpdef double get_waterlevel_v1(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef void set_timestep_v1(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
    cpdef inline void calc_netinflow_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.netinflow = self.sequences.fluxes.lateralflow
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow + ((<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_discharge())
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow - ((<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_discharge())
        self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow * (self.sequences.factors.timestep / 1e3)
    cpdef inline void update_watervolume_v1(self) noexcept nogil:
        self.sequences.states.watervolume = self.sequences.states.watervolume + (self.sequences.fluxes.netinflow)
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_wettedarea(self.sequences.states.watervolume / self.parameters.control.length)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.waterlevel = submodel.get_waterlevel()
    cpdef inline void pass_waterlevel_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.sequences.senders.len_waterlevel):
            self.sequences.senders.waterlevel[i] = self.sequences.factors.waterlevel
    cpdef inline void pick_lateralflow(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.lateralflow = 0.0
        for i in range(self.sequences.inlets.len_latq):
            self.sequences.fluxes.lateralflow = self.sequences.fluxes.lateralflow + (self.sequences.inlets.latq[i])
    cpdef inline void calc_waterdepth_waterlevel(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_waterlevel_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef double get_watervolume(self) noexcept nogil:
        return self.sequences.states.watervolume
    cpdef double get_waterlevel(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef void set_timestep(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
    cpdef inline void calc_netinflow(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.netinflow = self.sequences.fluxes.lateralflow
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow + ((<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_discharge())
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow - ((<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_discharge())
        self.sequences.fluxes.netinflow = self.sequences.fluxes.netinflow * (self.sequences.factors.timestep / 1e3)
    cpdef inline void update_watervolume(self) noexcept nogil:
        self.sequences.states.watervolume = self.sequences.states.watervolume + (self.sequences.fluxes.netinflow)
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_wettedarea(self.sequences.states.watervolume / self.parameters.control.length)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.waterlevel = submodel.get_waterlevel()
    cpdef inline void pass_waterlevel(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.sequences.senders.len_waterlevel):
            self.sequences.senders.waterlevel[i] = self.sequences.factors.waterlevel
    cpdef void update_storage_v1(self) noexcept nogil:
        self.calc_netinflow_v1()
        self.update_watervolume_v1()
        self.calc_waterdepth_waterlevel_v1()
    cpdef void update_storage(self) noexcept nogil:
        self.calc_netinflow_v1()
        self.update_watervolume_v1()
        self.calc_waterdepth_waterlevel_v1()
