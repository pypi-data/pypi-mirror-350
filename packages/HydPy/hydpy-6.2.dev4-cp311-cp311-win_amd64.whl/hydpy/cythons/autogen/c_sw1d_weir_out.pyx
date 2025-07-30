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
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
        if self._waterlevelupstream_diskflag_reading:
            self.waterlevelupstream = self._waterlevelupstream_ncarray[0]
        elif self._waterlevelupstream_ramflag:
            self.waterlevelupstream = self._waterlevelupstream_array[idx]
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
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
        if self._waterlevelupstream_diskflag_writing:
            self._waterlevelupstream_ncarray[0] = self.waterlevelupstream
        if self._waterlevelupstream_ramflag:
            self._waterlevelupstream_array[idx] = self.waterlevelupstream
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "maxtimestep":
            self._maxtimestep_outputpointer = value.p_value
        if name == "timestep":
            self._timestep_outputpointer = value.p_value
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
        if name == "waterlevelupstream":
            self._waterlevelupstream_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._maxtimestep_outputflag:
            self._maxtimestep_outputpointer[0] = self.maxtimestep
        if self._timestep_outputflag:
            self._timestep_outputpointer[0] = self.timestep
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
        if self._waterlevelupstream_outputflag:
            self._waterlevelupstream_outputpointer[0] = self.waterlevelupstream
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dischargevolume_diskflag_reading:
            self.dischargevolume = self._dischargevolume_ncarray[0]
        elif self._dischargevolume_ramflag:
            self.dischargevolume = self._dischargevolume_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dischargevolume_diskflag_writing:
            self._dischargevolume_ncarray[0] = self.dischargevolume
        if self._dischargevolume_ramflag:
            self._dischargevolume_array[idx] = self.dischargevolume
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "dischargevolume":
            self._dischargevolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
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
        self.routingmodelsupstream = interfaceutils.SubmodelsProperty()
        self.storagemodelupstream = None
        self.storagemodelupstream_is_mainmodel = False
    def get_storagemodelupstream(self) -> masterinterface.MasterInterface | None:
        return self.storagemodelupstream
    def set_storagemodelupstream(self, storagemodelupstream: masterinterface.MasterInterface | None) -> None:
        self.storagemodelupstream = storagemodelupstream
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
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
        pass
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.discharge = self.sequences.new_states.discharge
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        self.reset_dischargevolume_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_discharge_v1()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.outlets._longq_length_0):
                if self.sequences.outlets._longq_ready[i]:
                    self.sequences.outlets._longq_pointer[i][0] = self.sequences.outlets._longq_pointer[i][0] + self.sequences.outlets.longq[i]
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
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
    cpdef inline void reset_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = 0.0
    cpdef double get_maxtimestep_v1(self) noexcept nogil:
        return self.sequences.factors.maxtimestep
    cpdef double get_discharge_v1(self) noexcept nogil:
        return self.sequences.states.discharge
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
    cpdef inline void calc_waterlevelupstream_v1(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.waterlevelupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_waterlevel()
    cpdef inline void calc_waterlevel_v3(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterlevelupstream
    cpdef inline void calc_maxtimestep_v3(self) noexcept nogil:
        cdef double cel
        cdef double g
        cdef double c
        cdef double h
        h = self.sequences.factors.waterlevel - self.parameters.control.crestheight
        if h > 0.0:
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            cel = c * (2.0 * g * h) ** 0.5
            self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.control.lengthupstream / cel
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_discharge_v2(self) noexcept nogil:
        cdef double g
        cdef double c
        cdef double w
        cdef double h
        h = self.sequences.factors.waterlevel - self.parameters.control.crestheight
        if h > 0.0:
            w = self.parameters.control.crestwidth
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            self.sequences.states.discharge = w * 2.0 / 3.0 * c * (2.0 * g) ** 0.5 * h ** (3.0 / 2.0)
        else:
            self.sequences.states.discharge = 0.0
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
    cpdef inline void calc_waterlevelupstream(self) noexcept nogil:
        if self.storagemodelupstream_typeid == 1:
            self.sequences.factors.waterlevelupstream = (<masterinterface.MasterInterface>self.storagemodelupstream).get_waterlevel()
    cpdef inline void calc_waterlevel(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterlevelupstream
    cpdef inline void calc_maxtimestep(self) noexcept nogil:
        cdef double cel
        cdef double g
        cdef double c
        cdef double h
        h = self.sequences.factors.waterlevel - self.parameters.control.crestheight
        if h > 0.0:
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            cel = c * (2.0 * g * h) ** 0.5
            self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.control.lengthupstream / cel
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_discharge(self) noexcept nogil:
        cdef double g
        cdef double c
        cdef double w
        cdef double h
        h = self.sequences.factors.waterlevel - self.parameters.control.crestheight
        if h > 0.0:
            w = self.parameters.control.crestwidth
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            self.sequences.states.discharge = w * 2.0 / 3.0 * c * (2.0 * g) ** 0.5 * h ** (3.0 / 2.0)
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
    cpdef void determine_maxtimestep_v3(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterlevel_v3()
        self.calc_maxtimestep_v3()
    cpdef void determine_discharge_v3(self) noexcept nogil:
        self.calc_discharge_v2()
        self.update_dischargevolume_v1()
    cpdef void determine_maxtimestep(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterlevel_v3()
        self.calc_maxtimestep_v3()
    cpdef void determine_discharge(self) noexcept nogil:
        self.calc_discharge_v2()
        self.update_dischargevolume_v1()
