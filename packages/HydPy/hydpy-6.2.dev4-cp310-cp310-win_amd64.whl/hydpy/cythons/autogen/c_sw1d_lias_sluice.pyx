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
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._maxtimestep_diskflag_reading:
            self.maxtimestep = self._maxtimestep_ncarray[0]
        elif self._maxtimestep_ramflag:
            self.maxtimestep = self._maxtimestep_array[idx]
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
        if self._waterlevelupstream_diskflag_reading:
            self.waterlevelupstream = self._waterlevelupstream_ncarray[0]
        elif self._waterlevelupstream_ramflag:
            self.waterlevelupstream = self._waterlevelupstream_array[idx]
        if self._waterleveldownstream_diskflag_reading:
            self.waterleveldownstream = self._waterleveldownstream_ncarray[0]
        elif self._waterleveldownstream_ramflag:
            self.waterleveldownstream = self._waterleveldownstream_array[idx]
        if self._watervolumeupstream_diskflag_reading:
            self.watervolumeupstream = self._watervolumeupstream_ncarray[0]
        elif self._watervolumeupstream_ramflag:
            self.watervolumeupstream = self._watervolumeupstream_array[idx]
        if self._watervolumedownstream_diskflag_reading:
            self.watervolumedownstream = self._watervolumedownstream_ncarray[0]
        elif self._watervolumedownstream_ramflag:
            self.watervolumedownstream = self._watervolumedownstream_array[idx]
        if self._wettedarea_diskflag_reading:
            self.wettedarea = self._wettedarea_ncarray[0]
        elif self._wettedarea_ramflag:
            self.wettedarea = self._wettedarea_array[idx]
        if self._wettedperimeter_diskflag_reading:
            self.wettedperimeter = self._wettedperimeter_ncarray[0]
        elif self._wettedperimeter_ramflag:
            self.wettedperimeter = self._wettedperimeter_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._maxtimestep_diskflag_writing:
            self._maxtimestep_ncarray[0] = self.maxtimestep
        if self._maxtimestep_ramflag:
            self._maxtimestep_array[idx] = self.maxtimestep
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
        if self._waterlevelupstream_diskflag_writing:
            self._waterlevelupstream_ncarray[0] = self.waterlevelupstream
        if self._waterlevelupstream_ramflag:
            self._waterlevelupstream_array[idx] = self.waterlevelupstream
        if self._waterleveldownstream_diskflag_writing:
            self._waterleveldownstream_ncarray[0] = self.waterleveldownstream
        if self._waterleveldownstream_ramflag:
            self._waterleveldownstream_array[idx] = self.waterleveldownstream
        if self._watervolumeupstream_diskflag_writing:
            self._watervolumeupstream_ncarray[0] = self.watervolumeupstream
        if self._watervolumeupstream_ramflag:
            self._watervolumeupstream_array[idx] = self.watervolumeupstream
        if self._watervolumedownstream_diskflag_writing:
            self._watervolumedownstream_ncarray[0] = self.watervolumedownstream
        if self._watervolumedownstream_ramflag:
            self._watervolumedownstream_array[idx] = self.watervolumedownstream
        if self._wettedarea_diskflag_writing:
            self._wettedarea_ncarray[0] = self.wettedarea
        if self._wettedarea_ramflag:
            self._wettedarea_array[idx] = self.wettedarea
        if self._wettedperimeter_diskflag_writing:
            self._wettedperimeter_ncarray[0] = self.wettedperimeter
        if self._wettedperimeter_ramflag:
            self._wettedperimeter_array[idx] = self.wettedperimeter
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "maxtimestep":
            self._maxtimestep_outputpointer = value.p_value
        if name == "timestep":
            self._timestep_outputpointer = value.p_value
        if name == "waterdepth":
            self._waterdepth_outputpointer = value.p_value
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
        if name == "waterlevelupstream":
            self._waterlevelupstream_outputpointer = value.p_value
        if name == "waterleveldownstream":
            self._waterleveldownstream_outputpointer = value.p_value
        if name == "watervolumeupstream":
            self._watervolumeupstream_outputpointer = value.p_value
        if name == "watervolumedownstream":
            self._watervolumedownstream_outputpointer = value.p_value
        if name == "wettedarea":
            self._wettedarea_outputpointer = value.p_value
        if name == "wettedperimeter":
            self._wettedperimeter_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._maxtimestep_outputflag:
            self._maxtimestep_outputpointer[0] = self.maxtimestep
        if self._timestep_outputflag:
            self._timestep_outputpointer[0] = self.timestep
        if self._waterdepth_outputflag:
            self._waterdepth_outputpointer[0] = self.waterdepth
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
        if self._waterlevelupstream_outputflag:
            self._waterlevelupstream_outputpointer[0] = self.waterlevelupstream
        if self._waterleveldownstream_outputflag:
            self._waterleveldownstream_outputpointer[0] = self.waterleveldownstream
        if self._watervolumeupstream_outputflag:
            self._watervolumeupstream_outputpointer[0] = self.watervolumeupstream
        if self._watervolumedownstream_outputflag:
            self._watervolumedownstream_outputpointer[0] = self.watervolumedownstream
        if self._wettedarea_outputflag:
            self._wettedarea_outputpointer[0] = self.wettedarea
        if self._wettedperimeter_outputflag:
            self._wettedperimeter_outputpointer[0] = self.wettedperimeter
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dischargeupstream_diskflag_reading:
            self.dischargeupstream = self._dischargeupstream_ncarray[0]
        elif self._dischargeupstream_ramflag:
            self.dischargeupstream = self._dischargeupstream_array[idx]
        if self._dischargedownstream_diskflag_reading:
            self.dischargedownstream = self._dischargedownstream_ncarray[0]
        elif self._dischargedownstream_ramflag:
            self.dischargedownstream = self._dischargedownstream_array[idx]
        if self._dischargevolume_diskflag_reading:
            self.dischargevolume = self._dischargevolume_ncarray[0]
        elif self._dischargevolume_ramflag:
            self.dischargevolume = self._dischargevolume_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dischargeupstream_diskflag_writing:
            self._dischargeupstream_ncarray[0] = self.dischargeupstream
        if self._dischargeupstream_ramflag:
            self._dischargeupstream_array[idx] = self.dischargeupstream
        if self._dischargedownstream_diskflag_writing:
            self._dischargedownstream_ncarray[0] = self.dischargedownstream
        if self._dischargedownstream_ramflag:
            self._dischargedownstream_array[idx] = self.dischargedownstream
        if self._dischargevolume_diskflag_writing:
            self._dischargevolume_ncarray[0] = self.dischargevolume
        if self._dischargevolume_ramflag:
            self._dischargevolume_array[idx] = self.dischargevolume
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "dischargeupstream":
            self._dischargeupstream_outputpointer = value.p_value
        if name == "dischargedownstream":
            self._dischargedownstream_outputpointer = value.p_value
        if name == "dischargevolume":
            self._dischargevolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._dischargeupstream_outputflag:
            self._dischargeupstream_outputpointer[0] = self.dischargeupstream
        if self._dischargedownstream_outputflag:
            self._dischargedownstream_outputpointer[0] = self.dischargedownstream
        if self._dischargevolume_outputflag:
            self._dischargevolume_outputpointer[0] = self.dischargevolume
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._discharge_diskflag_reading:
            self.discharge = self._discharge_ncarray[0]
        elif self._discharge_ramflag:
            self.discharge = self._discharge_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._discharge_diskflag_writing:
            self._discharge_ncarray[0] = self.discharge
        if self._discharge_ramflag:
            self._discharge_array[idx] = self.discharge
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "discharge":
            self._discharge_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._discharge_outputflag:
            self._discharge_outputpointer[0] = self.discharge
@cython.final
cdef class OutletSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._longq_diskflag_reading:
            k = 0
            for jdx0 in range(self._longq_length_0):
                self.longq[jdx0] = self._longq_ncarray[k]
                k += 1
        elif self._longq_ramflag:
            for jdx0 in range(self._longq_length_0):
                self.longq[jdx0] = self._longq_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._longq_diskflag_writing:
            k = 0
            for jdx0 in range(self._longq_length_0):
                self._longq_ncarray[k] = self.longq[jdx0]
                k += 1
        if self._longq_ramflag:
            for jdx0 in range(self._longq_length_0):
                self._longq_array[idx, jdx0] = self.longq[jdx0]
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "longq":
            self._longq_length_0 = length
            self._longq_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._longq_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "longq":
            PyMem_Free(self._longq_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "longq":
            self._longq_pointer[idx] = pointer.p_value
            self._longq_ready[idx] = 1
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "longq":
            values = numpy.empty(self.len_longq)
            for idx in range(self.len_longq):
                pointerutils.check0(self._longq_length_0)
                if self._longq_ready[idx] == 0:
                    pointerutils.check1(self._longq_length_0, idx)
                    pointerutils.check2(self._longq_ready, idx)
                values[idx] = self._longq_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "longq":
            for idx in range(self.len_longq):
                pointerutils.check0(self._longq_length_0)
                if self._longq_ready[idx] == 0:
                    pointerutils.check1(self._longq_length_0, idx)
                    pointerutils.check2(self._longq_ready, idx)
                self._longq_pointer[idx][0] = value[idx]
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.crosssection = None
        self.crosssection_is_mainmodel = False
        self.routingmodelsdownstream = interfaceutils.SubmodelsProperty()
        self.routingmodelsupstream = interfaceutils.SubmodelsProperty()
        self.storagemodeldownstream = None
        self.storagemodeldownstream_is_mainmodel = False
        self.storagemodelupstream = None
        self.storagemodelupstream_is_mainmodel = False
    def get_crosssection(self) -> masterinterface.MasterInterface | None:
        return self.crosssection
    def set_crosssection(self, crosssection: masterinterface.MasterInterface | None) -> None:
        self.crosssection = crosssection
    def get_storagemodeldownstream(self) -> masterinterface.MasterInterface | None:
        return self.storagemodeldownstream
    def set_storagemodeldownstream(self, storagemodeldownstream: masterinterface.MasterInterface | None) -> None:
        self.storagemodeldownstream = storagemodeldownstream
    def get_storagemodelupstream(self) -> masterinterface.MasterInterface | None:
        return self.storagemodelupstream
    def set_storagemodelupstream(self, storagemodelupstream: masterinterface.MasterInterface | None) -> None:
        self.storagemodelupstream = storagemodelupstream
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
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.discharge = self.sequences.new_states.discharge
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.new2old()
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef void update_inlets(self) noexcept nogil:
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_inlets()
        cdef numpy.int64_t i
        self.reset_dischargevolume_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outlets()
        self.pass_discharge_v1()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.outlets._longq_length_0):
                if self.sequences.outlets._longq_ready[i]:
                    self.sequences.outlets._longq_pointer[i][0] = self.sequences.outlets._longq_pointer[i][0] + self.sequences.outlets.longq[i]
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outputs()
    cpdef inline void reset_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = 0.0
    cpdef double get_maxtimestep_v1(self) noexcept nogil:
        return self.sequences.factors.maxtimestep
    cpdef double get_discharge_v1(self) noexcept nogil:
        return self.sequences.states.discharge
    cpdef double get_partialdischargeupstream_v1(self, double clientdischarge) noexcept nogil:
        cdef numpy.int64_t i
        cdef double dischargedownstream
        dischargedownstream = 0.0
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                dischargedownstream = dischargedownstream + (fabs(                    (<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_discharge()                ))
        if dischargedownstream == 0.0:
            return 0.0
        return fabs(self.sequences.states.discharge) * clientdischarge / dischargedownstream
    cpdef double get_partialdischargedownstream_v1(self, double clientdischarge) noexcept nogil:
        cdef numpy.int64_t i
        cdef double dischargeupstream
        dischargeupstream = 0.0
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                dischargeupstream = dischargeupstream + (fabs(                    (<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_discharge()                ))
        if dischargeupstream == 0.0:
            return 0.0
        return fabs(self.sequences.states.discharge) * clientdischarge / dischargeupstream
    cpdef double get_dischargevolume_v1(self) noexcept nogil:
        return self.sequences.fluxes.dischargevolume
    cpdef void set_timestep_v1(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
    cpdef inline void calc_watervolumeupstream_v1(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.watervolumeupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_watervolume()
    cpdef inline void calc_watervolumedownstream_v1(self) noexcept nogil:
        if self.storagemodeldownstream_typeid == 1:
            self.sequences.factors.watervolumedownstream = (<masterinterface.MasterInterface>self.storagemodeldownstream).get_watervolume()
    cpdef inline void calc_waterlevelupstream_v1(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.waterlevelupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_waterlevel()
    cpdef inline void calc_waterleveldownstream_v1(self) noexcept nogil:
        if self.storagemodeldownstream_typeid == 1:
            self.sequences.factors.waterleveldownstream = (<masterinterface.MasterInterface>self.storagemodeldownstream).get_waterlevel()
    cpdef inline void calc_waterlevel_v1(self) noexcept nogil:
        cdef double w
        w = self.parameters.derived.weightupstream
        self.sequences.factors.waterlevel = (            w * self.sequences.factors.waterlevelupstream + (1.0 - w) * self.sequences.factors.waterleveldownstream        )
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
        self.sequences.factors.wettedperimeter = submodel.get_wettedperimeter()
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_v1(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_maxtimestep_v1(self) noexcept nogil:
        if self.sequences.factors.waterdepth > 0.0:
            self.sequences.factors.maxtimestep = (self.parameters.control.timestepfactor * 1000.0 * self.parameters.derived.lengthmin) / (                self.parameters.fixed.gravitationalacceleration * self.sequences.factors.waterdepth            ) ** 0.5
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_dischargeupstream_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.dischargeupstream = 0.0
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                self.sequences.fluxes.dischargeupstream = self.sequences.fluxes.dischargeupstream + ((<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_partialdischargeupstream(self.sequences.states.discharge))
    cpdef inline void calc_dischargedownstream_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.dischargedownstream = 0.0
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                self.sequences.fluxes.dischargedownstream = self.sequences.fluxes.dischargedownstream + ((<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_partialdischargedownstream(self.sequences.states.discharge))
    cpdef inline void calc_discharge_v1(self) noexcept nogil:
        cdef double denominator
        cdef double nominator2
        cdef double nominator1
        cdef double w
        if self.sequences.factors.wettedarea > 0.0:
            w = self.parameters.control.diffusionfactor
            nominator1 = (1.0 - w) * self.sequences.states.discharge + w / 2.0 * (                self.sequences.fluxes.dischargeupstream + self.sequences.fluxes.dischargedownstream            )
            nominator2 = (                self.parameters.fixed.gravitationalacceleration                * self.sequences.factors.wettedarea                * self.sequences.factors.timestep                * (self.sequences.factors.waterlevelupstream - self.sequences.factors.waterleveldownstream)                / (1000.0 * self.parameters.derived.lengthmean)            )
            denominator = 1.0 + (                self.parameters.fixed.gravitationalacceleration                * self.sequences.factors.timestep                / self.parameters.control.stricklercoefficient**2.0                * fabs(self.sequences.states.discharge)                * self.sequences.factors.wettedperimeter ** (4.0 / 3.0)                / self.sequences.factors.wettedarea ** (7.0 / 3.0)            )
            self.sequences.states.discharge = (nominator1 + nominator2) / denominator
        else:
            self.sequences.states.discharge = 0.0
    cpdef inline void update_discharge_v1(self) noexcept nogil:
        cdef double q_min
        cdef double q_max
        if self.sequences.states.discharge > 0.0:
            q_max = 1000.0 * max(self.sequences.factors.watervolumeupstream, 0.0) / self.sequences.factors.timestep
            self.sequences.states.discharge = min(self.sequences.states.discharge, q_max)
        elif self.sequences.states.discharge < 0.0:
            q_min = -1000.0 * max(self.sequences.factors.watervolumedownstream, 0.0) / self.sequences.factors.timestep
            self.sequences.states.discharge = max(self.sequences.states.discharge, q_min)
    cpdef inline void update_discharge_v2(self) noexcept nogil:
        cdef double state_free
        cdef double state_sluice
        cdef double state_closed
        cdef double ht2
        cdef double ht1
        cdef double lt2
        cdef double lt1
        cdef numpy.int64_t toy
        cdef double hd
        cdef double hu
        hu = self.sequences.factors.waterlevelupstream
        hd = self.sequences.factors.waterleveldownstream
        toy = self.parameters.derived.toy[self.idx_sim]
        lt1 = self.parameters.control.bottomlowwaterthreshold[toy]
        lt2 = self.parameters.control.upperlowwaterthreshold[toy]
        ht1 = self.parameters.control.bottomhighwaterthreshold[toy]
        ht2 = self.parameters.control.upperhighwaterthreshold[toy]
        if hu < lt1:
            state_closed = 1.0
        elif hu < lt2:
            state_closed = 1.0 - (hu - lt1) / (lt2 - lt1)
        else:
            state_closed = 0.0
        if hu < ht1:
            state_sluice = 0.0
        elif hu < ht2:
            state_sluice = (hu - ht1) / (ht2 - ht1)
        else:
            state_sluice = 1.0
        state_free = 1.0 - state_closed - state_sluice
        self.sequences.states.discharge = self.sequences.states.discharge * (state_free + (state_sluice if hu > hd else 0.0))
    cpdef inline void update_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.sequences.fluxes.dischargevolume + (self.sequences.factors.timestep * self.sequences.states.discharge)
    cpdef inline void pass_discharge_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        cdef double discharge
        discharge = self.sequences.fluxes.dischargevolume / self.parameters.derived.seconds
        for i in range(self.sequences.outlets.len_longq):
            self.sequences.outlets.longq[i] = discharge
    cpdef inline void reset_dischargevolume(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = 0.0
    cpdef double get_maxtimestep(self) noexcept nogil:
        return self.sequences.factors.maxtimestep
    cpdef double get_discharge(self) noexcept nogil:
        return self.sequences.states.discharge
    cpdef double get_partialdischargeupstream(self, double clientdischarge) noexcept nogil:
        cdef numpy.int64_t i
        cdef double dischargedownstream
        dischargedownstream = 0.0
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                dischargedownstream = dischargedownstream + (fabs(                    (<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_discharge()                ))
        if dischargedownstream == 0.0:
            return 0.0
        return fabs(self.sequences.states.discharge) * clientdischarge / dischargedownstream
    cpdef double get_partialdischargedownstream(self, double clientdischarge) noexcept nogil:
        cdef numpy.int64_t i
        cdef double dischargeupstream
        dischargeupstream = 0.0
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                dischargeupstream = dischargeupstream + (fabs(                    (<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_discharge()                ))
        if dischargeupstream == 0.0:
            return 0.0
        return fabs(self.sequences.states.discharge) * clientdischarge / dischargeupstream
    cpdef double get_dischargevolume(self) noexcept nogil:
        return self.sequences.fluxes.dischargevolume
    cpdef void set_timestep(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
    cpdef inline void calc_watervolumeupstream(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.watervolumeupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_watervolume()
    cpdef inline void calc_watervolumedownstream(self) noexcept nogil:
        if self.storagemodeldownstream_typeid == 1:
            self.sequences.factors.watervolumedownstream = (<masterinterface.MasterInterface>self.storagemodeldownstream).get_watervolume()
    cpdef inline void calc_waterlevelupstream(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.waterlevelupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_waterlevel()
    cpdef inline void calc_waterleveldownstream(self) noexcept nogil:
        if self.storagemodeldownstream_typeid == 1:
            self.sequences.factors.waterleveldownstream = (<masterinterface.MasterInterface>self.storagemodeldownstream).get_waterlevel()
    cpdef inline void calc_waterlevel(self) noexcept nogil:
        cdef double w
        w = self.parameters.derived.weightupstream
        self.sequences.factors.waterlevel = (            w * self.sequences.factors.waterlevelupstream + (1.0 - w) * self.sequences.factors.waterleveldownstream        )
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
        self.sequences.factors.wettedperimeter = submodel.get_wettedperimeter()
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_maxtimestep(self) noexcept nogil:
        if self.sequences.factors.waterdepth > 0.0:
            self.sequences.factors.maxtimestep = (self.parameters.control.timestepfactor * 1000.0 * self.parameters.derived.lengthmin) / (                self.parameters.fixed.gravitationalacceleration * self.sequences.factors.waterdepth            ) ** 0.5
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_dischargeupstream(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.dischargeupstream = 0.0
        for i in range(self.routingmodelsupstream.number):
            if self.routingmodelsupstream.typeids[i] in (1, 2):
                self.sequences.fluxes.dischargeupstream = self.sequences.fluxes.dischargeupstream + ((<masterinterface.MasterInterface>self.routingmodelsupstream.submodels[i]).get_partialdischargeupstream(self.sequences.states.discharge))
    cpdef inline void calc_dischargedownstream(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.dischargedownstream = 0.0
        for i in range(self.routingmodelsdownstream.number):
            if self.routingmodelsdownstream.typeids[i] in (2, 3):
                self.sequences.fluxes.dischargedownstream = self.sequences.fluxes.dischargedownstream + ((<masterinterface.MasterInterface>self.routingmodelsdownstream.submodels[i]).get_partialdischargedownstream(self.sequences.states.discharge))
    cpdef inline void calc_discharge(self) noexcept nogil:
        cdef double denominator
        cdef double nominator2
        cdef double nominator1
        cdef double w
        if self.sequences.factors.wettedarea > 0.0:
            w = self.parameters.control.diffusionfactor
            nominator1 = (1.0 - w) * self.sequences.states.discharge + w / 2.0 * (                self.sequences.fluxes.dischargeupstream + self.sequences.fluxes.dischargedownstream            )
            nominator2 = (                self.parameters.fixed.gravitationalacceleration                * self.sequences.factors.wettedarea                * self.sequences.factors.timestep                * (self.sequences.factors.waterlevelupstream - self.sequences.factors.waterleveldownstream)                / (1000.0 * self.parameters.derived.lengthmean)            )
            denominator = 1.0 + (                self.parameters.fixed.gravitationalacceleration                * self.sequences.factors.timestep                / self.parameters.control.stricklercoefficient**2.0                * fabs(self.sequences.states.discharge)                * self.sequences.factors.wettedperimeter ** (4.0 / 3.0)                / self.sequences.factors.wettedarea ** (7.0 / 3.0)            )
            self.sequences.states.discharge = (nominator1 + nominator2) / denominator
        else:
            self.sequences.states.discharge = 0.0
    cpdef inline void update_dischargevolume(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.sequences.fluxes.dischargevolume + (self.sequences.factors.timestep * self.sequences.states.discharge)
    cpdef inline void pass_discharge(self) noexcept nogil:
        cdef numpy.int64_t i
        cdef double discharge
        discharge = self.sequences.fluxes.dischargevolume / self.parameters.derived.seconds
        for i in range(self.sequences.outlets.len_longq):
            self.sequences.outlets.longq[i] = discharge
    cpdef void determine_maxtimestep_v1(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterleveldownstream_v1()
        self.calc_waterlevel_v1()
        self.calc_waterdepth_wettedarea_wettedperimeter_v1()
        self.calc_dischargeupstream_v1()
        self.calc_dischargedownstream_v1()
        self.calc_maxtimestep_v1()
    cpdef void determine_discharge_v5(self) noexcept nogil:
        self.calc_watervolumeupstream_v1()
        self.calc_watervolumedownstream_v1()
        self.calc_discharge_v1()
        self.update_discharge_v1()
        self.update_discharge_v2()
        self.update_dischargevolume_v1()
    cpdef void determine_maxtimestep(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterleveldownstream_v1()
        self.calc_waterlevel_v1()
        self.calc_waterdepth_wettedarea_wettedperimeter_v1()
        self.calc_dischargeupstream_v1()
        self.calc_dischargedownstream_v1()
        self.calc_maxtimestep_v1()
    cpdef void determine_discharge(self) noexcept nogil:
        self.calc_watervolumeupstream_v1()
        self.calc_watervolumedownstream_v1()
        self.calc_discharge_v1()
        self.update_discharge_v1()
        self.update_discharge_v2()
        self.update_dischargevolume_v1()
