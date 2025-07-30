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
cdef class DerivedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._timestep_diskflag_reading:
            self.timestep = self._timestep_ncarray[0]
        elif self._timestep_ramflag:
            self.timestep = self._timestep_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._timestep_diskflag_writing:
            self._timestep_ncarray[0] = self.timestep
        if self._timestep_ramflag:
            self._timestep_array[idx] = self.timestep
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "timestep":
            self._timestep_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._timestep_outputflag:
            self._timestep_outputpointer[0] = self.timestep
@cython.final
cdef class Model:
    def __init__(self):
        super().__init__()
        self.channelmodels = interfaceutils.SubmodelsProperty()
        self.routingmodels = interfaceutils.SubmodelsProperty()
        self.storagemodels = interfaceutils.SubmodelsProperty()
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
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).load_data(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.factors.save_data(idx)
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).save_data(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).new2old()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).new2old()
    cpdef inline void run(self) noexcept nogil:
        self.timeleft = self.parameters.derived.seconds
        while True:
            self.calc_maxtimesteps_v1()
            self.calc_timestep_v1()
            self.send_timestep_v1()
            self.calc_discharges_v1()
            self.update_storages_v1()
            if self.timeleft <= 0.0:
                break
            self.new2old()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_inlets()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_outlets()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_outlets()
        cdef numpy.int64_t i
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_receivers(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_senders(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_outputs()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_outputs()
    cpdef inline void calc_maxtimesteps_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).determine_maxtimestep()
    cpdef inline void calc_timestep_v1(self) noexcept nogil:
        cdef double timestep
        cdef numpy.int64_t i
        self.sequences.factors.timestep = inf
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                timestep = (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).get_maxtimestep()
                self.sequences.factors.timestep = min(self.sequences.factors.timestep, timestep)
        if self.sequences.factors.timestep < self.timeleft:
            self.timeleft = self.timeleft - (self.sequences.factors.timestep)
        else:
            self.sequences.factors.timestep = self.timeleft
            self.timeleft = 0.0
    cpdef inline void send_timestep_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).set_timestep(self.sequences.factors.timestep)
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).set_timestep(self.sequences.factors.timestep)
    cpdef inline void calc_discharges_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).determine_discharge()
    cpdef inline void update_storages_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).update_storage()
    cpdef inline void calc_maxtimesteps(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).determine_maxtimestep()
    cpdef inline void calc_timestep(self) noexcept nogil:
        cdef double timestep
        cdef numpy.int64_t i
        self.sequences.factors.timestep = inf
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                timestep = (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).get_maxtimestep()
                self.sequences.factors.timestep = min(self.sequences.factors.timestep, timestep)
        if self.sequences.factors.timestep < self.timeleft:
            self.timeleft = self.timeleft - (self.sequences.factors.timestep)
        else:
            self.sequences.factors.timestep = self.timeleft
            self.timeleft = 0.0
    cpdef inline void send_timestep(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).set_timestep(self.sequences.factors.timestep)
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).set_timestep(self.sequences.factors.timestep)
    cpdef inline void calc_discharges(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).determine_discharge()
    cpdef inline void update_storages(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).update_storage()
