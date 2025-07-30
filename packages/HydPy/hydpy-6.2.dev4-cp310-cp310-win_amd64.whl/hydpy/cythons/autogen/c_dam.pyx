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
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
        if self._e_diskflag_reading:
            k = 0
            for jdx0 in range(self._e_length_0):
                self.e[jdx0] = self._e_ncarray[k]
                k += 1
        elif self._e_ramflag:
            for jdx0 in range(self._e_length_0):
                self.e[jdx0] = self._e_array[idx, jdx0]
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
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
        if self._e_diskflag_writing:
            k = 0
            for jdx0 in range(self._e_length_0):
                self._e_ncarray[k] = self.e[jdx0]
                k += 1
        if self._e_ramflag:
            for jdx0 in range(self._e_length_0):
                self._e_array[idx, jdx0] = self.e[jdx0]
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "s":
            self._s_pointer = pointer.p_value
        if name == "r":
            self._r_pointer = pointer.p_value
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "q":
            self._q_length_0 = length
            self._q_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._q_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
        if name == "e":
            self._e_length_0 = length
            self._e_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._e_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "q":
            PyMem_Free(self._q_pointer)
        if name == "e":
            PyMem_Free(self._e_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer[idx] = pointer.p_value
            self._q_ready[idx] = 1
        if name == "e":
            self._e_pointer[idx] = pointer.p_value
            self._e_ready[idx] = 1
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
        if name == "s":
            return self._s_pointer[0]
        if name == "r":
            return self._r_pointer[0]
        if name == "e":
            values = numpy.empty(self.len_e)
            for idx in range(self.len_e):
                pointerutils.check0(self._e_length_0)
                if self._e_ready[idx] == 0:
                    pointerutils.check1(self._e_length_0, idx)
                    pointerutils.check2(self._e_ready, idx)
                values[idx] = self._e_pointer[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "q":
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                self._q_pointer[idx][0] = value[idx]
        if name == "s":
            self._s_pointer[0] = value
        if name == "r":
            self._r_pointer[0] = value
        if name == "e":
            for idx in range(self.len_e):
                pointerutils.check0(self._e_length_0)
                if self._e_ready[idx] == 0:
                    pointerutils.check1(self._e_length_0, idx)
                    pointerutils.check2(self._e_ready, idx)
                self._e_pointer[idx][0] = value[idx]
@cython.final
cdef class ReceiverSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_reading:
            self.q = self._q_ncarray[0]
        elif self._q_ramflag:
            self.q = self._q_array[idx]
        if self._d_diskflag_reading:
            self.d = self._d_ncarray[0]
        elif self._d_ramflag:
            self.d = self._d_array[idx]
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
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
        if self._q_diskflag_writing:
            self._q_ncarray[0] = self.q
        if self._q_ramflag:
            self._q_array[idx] = self.q
        if self._d_diskflag_writing:
            self._d_ncarray[0] = self.d
        if self._d_ramflag:
            self._d_array[idx] = self.d
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
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
        if name == "q":
            self._q_pointer = pointer.p_value
        if name == "d":
            self._d_pointer = pointer.p_value
        if name == "s":
            self._s_pointer = pointer.p_value
        if name == "r":
            self._r_pointer = pointer.p_value
        if name == "owl":
            self._owl_pointer = pointer.p_value
        if name == "rwl":
            self._rwl_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            return self._q_pointer[0]
        if name == "d":
            return self._d_pointer[0]
        if name == "s":
            return self._s_pointer[0]
        if name == "r":
            return self._r_pointer[0]
        if name == "owl":
            return self._owl_pointer[0]
        if name == "rwl":
            return self._rwl_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self._q_pointer[0] = value
        if name == "d":
            self._d_pointer[0] = value
        if name == "s":
            self._s_pointer[0] = value
        if name == "r":
            self._r_pointer[0] = value
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
        if self._effectivewaterleveldifference_diskflag_reading:
            self.effectivewaterleveldifference = self._effectivewaterleveldifference_ncarray[0]
        elif self._effectivewaterleveldifference_ramflag:
            self.effectivewaterleveldifference = self._effectivewaterleveldifference_array[idx]
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
        if self._effectivewaterleveldifference_diskflag_writing:
            self._effectivewaterleveldifference_ncarray[0] = self.effectivewaterleveldifference
        if self._effectivewaterleveldifference_ramflag:
            self._effectivewaterleveldifference_array[idx] = self.effectivewaterleveldifference
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "waterlevel":
            self._waterlevel_outputpointer = value.p_value
        if name == "outerwaterlevel":
            self._outerwaterlevel_outputpointer = value.p_value
        if name == "remotewaterlevel":
            self._remotewaterlevel_outputpointer = value.p_value
        if name == "waterleveldifference":
            self._waterleveldifference_outputpointer = value.p_value
        if name == "effectivewaterleveldifference":
            self._effectivewaterleveldifference_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._waterlevel_outputflag:
            self._waterlevel_outputpointer[0] = self.waterlevel
        if self._outerwaterlevel_outputflag:
            self._outerwaterlevel_outputpointer[0] = self.outerwaterlevel
        if self._remotewaterlevel_outputflag:
            self._remotewaterlevel_outputpointer[0] = self.remotewaterlevel
        if self._waterleveldifference_outputflag:
            self._waterleveldifference_outputpointer[0] = self.waterleveldifference
        if self._effectivewaterleveldifference_outputflag:
            self._effectivewaterleveldifference_outputpointer[0] = self.effectivewaterleveldifference
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
        if self._exchange_diskflag_reading:
            self.exchange = self._exchange_ncarray[0]
        elif self._exchange_ramflag:
            self.exchange = self._exchange_array[idx]
        if self._totalremotedischarge_diskflag_reading:
            self.totalremotedischarge = self._totalremotedischarge_ncarray[0]
        elif self._totalremotedischarge_ramflag:
            self.totalremotedischarge = self._totalremotedischarge_array[idx]
        if self._naturalremotedischarge_diskflag_reading:
            self.naturalremotedischarge = self._naturalremotedischarge_ncarray[0]
        elif self._naturalremotedischarge_ramflag:
            self.naturalremotedischarge = self._naturalremotedischarge_array[idx]
        if self._remotedemand_diskflag_reading:
            self.remotedemand = self._remotedemand_ncarray[0]
        elif self._remotedemand_ramflag:
            self.remotedemand = self._remotedemand_array[idx]
        if self._remotefailure_diskflag_reading:
            self.remotefailure = self._remotefailure_ncarray[0]
        elif self._remotefailure_ramflag:
            self.remotefailure = self._remotefailure_array[idx]
        if self._requiredremoterelease_diskflag_reading:
            self.requiredremoterelease = self._requiredremoterelease_ncarray[0]
        elif self._requiredremoterelease_ramflag:
            self.requiredremoterelease = self._requiredremoterelease_array[idx]
        if self._allowedremoterelief_diskflag_reading:
            self.allowedremoterelief = self._allowedremoterelief_ncarray[0]
        elif self._allowedremoterelief_ramflag:
            self.allowedremoterelief = self._allowedremoterelief_array[idx]
        if self._requiredremotesupply_diskflag_reading:
            self.requiredremotesupply = self._requiredremotesupply_ncarray[0]
        elif self._requiredremotesupply_ramflag:
            self.requiredremotesupply = self._requiredremotesupply_array[idx]
        if self._possibleremoterelief_diskflag_reading:
            self.possibleremoterelief = self._possibleremoterelief_ncarray[0]
        elif self._possibleremoterelief_ramflag:
            self.possibleremoterelief = self._possibleremoterelief_array[idx]
        if self._actualremoterelief_diskflag_reading:
            self.actualremoterelief = self._actualremoterelief_ncarray[0]
        elif self._actualremoterelief_ramflag:
            self.actualremoterelief = self._actualremoterelief_array[idx]
        if self._requiredrelease_diskflag_reading:
            self.requiredrelease = self._requiredrelease_ncarray[0]
        elif self._requiredrelease_ramflag:
            self.requiredrelease = self._requiredrelease_array[idx]
        if self._targetedrelease_diskflag_reading:
            self.targetedrelease = self._targetedrelease_ncarray[0]
        elif self._targetedrelease_ramflag:
            self.targetedrelease = self._targetedrelease_array[idx]
        if self._actualrelease_diskflag_reading:
            self.actualrelease = self._actualrelease_ncarray[0]
        elif self._actualrelease_ramflag:
            self.actualrelease = self._actualrelease_array[idx]
        if self._missingremoterelease_diskflag_reading:
            self.missingremoterelease = self._missingremoterelease_ncarray[0]
        elif self._missingremoterelease_ramflag:
            self.missingremoterelease = self._missingremoterelease_array[idx]
        if self._actualremoterelease_diskflag_reading:
            self.actualremoterelease = self._actualremoterelease_ncarray[0]
        elif self._actualremoterelease_ramflag:
            self.actualremoterelease = self._actualremoterelease_array[idx]
        if self._flooddischarge_diskflag_reading:
            self.flooddischarge = self._flooddischarge_ncarray[0]
        elif self._flooddischarge_ramflag:
            self.flooddischarge = self._flooddischarge_array[idx]
        if self._freedischarge_diskflag_reading:
            self.freedischarge = self._freedischarge_ncarray[0]
        elif self._freedischarge_ramflag:
            self.freedischarge = self._freedischarge_array[idx]
        if self._maxforceddischarge_diskflag_reading:
            self.maxforceddischarge = self._maxforceddischarge_ncarray[0]
        elif self._maxforceddischarge_ramflag:
            self.maxforceddischarge = self._maxforceddischarge_array[idx]
        if self._maxfreedischarge_diskflag_reading:
            self.maxfreedischarge = self._maxfreedischarge_ncarray[0]
        elif self._maxfreedischarge_ramflag:
            self.maxfreedischarge = self._maxfreedischarge_array[idx]
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
        if self._exchange_diskflag_writing:
            self._exchange_ncarray[0] = self.exchange
        if self._exchange_ramflag:
            self._exchange_array[idx] = self.exchange
        if self._totalremotedischarge_diskflag_writing:
            self._totalremotedischarge_ncarray[0] = self.totalremotedischarge
        if self._totalremotedischarge_ramflag:
            self._totalremotedischarge_array[idx] = self.totalremotedischarge
        if self._naturalremotedischarge_diskflag_writing:
            self._naturalremotedischarge_ncarray[0] = self.naturalremotedischarge
        if self._naturalremotedischarge_ramflag:
            self._naturalremotedischarge_array[idx] = self.naturalremotedischarge
        if self._remotedemand_diskflag_writing:
            self._remotedemand_ncarray[0] = self.remotedemand
        if self._remotedemand_ramflag:
            self._remotedemand_array[idx] = self.remotedemand
        if self._remotefailure_diskflag_writing:
            self._remotefailure_ncarray[0] = self.remotefailure
        if self._remotefailure_ramflag:
            self._remotefailure_array[idx] = self.remotefailure
        if self._requiredremoterelease_diskflag_writing:
            self._requiredremoterelease_ncarray[0] = self.requiredremoterelease
        if self._requiredremoterelease_ramflag:
            self._requiredremoterelease_array[idx] = self.requiredremoterelease
        if self._allowedremoterelief_diskflag_writing:
            self._allowedremoterelief_ncarray[0] = self.allowedremoterelief
        if self._allowedremoterelief_ramflag:
            self._allowedremoterelief_array[idx] = self.allowedremoterelief
        if self._requiredremotesupply_diskflag_writing:
            self._requiredremotesupply_ncarray[0] = self.requiredremotesupply
        if self._requiredremotesupply_ramflag:
            self._requiredremotesupply_array[idx] = self.requiredremotesupply
        if self._possibleremoterelief_diskflag_writing:
            self._possibleremoterelief_ncarray[0] = self.possibleremoterelief
        if self._possibleremoterelief_ramflag:
            self._possibleremoterelief_array[idx] = self.possibleremoterelief
        if self._actualremoterelief_diskflag_writing:
            self._actualremoterelief_ncarray[0] = self.actualremoterelief
        if self._actualremoterelief_ramflag:
            self._actualremoterelief_array[idx] = self.actualremoterelief
        if self._requiredrelease_diskflag_writing:
            self._requiredrelease_ncarray[0] = self.requiredrelease
        if self._requiredrelease_ramflag:
            self._requiredrelease_array[idx] = self.requiredrelease
        if self._targetedrelease_diskflag_writing:
            self._targetedrelease_ncarray[0] = self.targetedrelease
        if self._targetedrelease_ramflag:
            self._targetedrelease_array[idx] = self.targetedrelease
        if self._actualrelease_diskflag_writing:
            self._actualrelease_ncarray[0] = self.actualrelease
        if self._actualrelease_ramflag:
            self._actualrelease_array[idx] = self.actualrelease
        if self._missingremoterelease_diskflag_writing:
            self._missingremoterelease_ncarray[0] = self.missingremoterelease
        if self._missingremoterelease_ramflag:
            self._missingremoterelease_array[idx] = self.missingremoterelease
        if self._actualremoterelease_diskflag_writing:
            self._actualremoterelease_ncarray[0] = self.actualremoterelease
        if self._actualremoterelease_ramflag:
            self._actualremoterelease_array[idx] = self.actualremoterelease
        if self._flooddischarge_diskflag_writing:
            self._flooddischarge_ncarray[0] = self.flooddischarge
        if self._flooddischarge_ramflag:
            self._flooddischarge_array[idx] = self.flooddischarge
        if self._freedischarge_diskflag_writing:
            self._freedischarge_ncarray[0] = self.freedischarge
        if self._freedischarge_ramflag:
            self._freedischarge_array[idx] = self.freedischarge
        if self._maxforceddischarge_diskflag_writing:
            self._maxforceddischarge_ncarray[0] = self.maxforceddischarge
        if self._maxforceddischarge_ramflag:
            self._maxforceddischarge_array[idx] = self.maxforceddischarge
        if self._maxfreedischarge_diskflag_writing:
            self._maxfreedischarge_ncarray[0] = self.maxfreedischarge
        if self._maxfreedischarge_ramflag:
            self._maxfreedischarge_array[idx] = self.maxfreedischarge
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
        if name == "exchange":
            self._exchange_outputpointer = value.p_value
        if name == "totalremotedischarge":
            self._totalremotedischarge_outputpointer = value.p_value
        if name == "naturalremotedischarge":
            self._naturalremotedischarge_outputpointer = value.p_value
        if name == "remotedemand":
            self._remotedemand_outputpointer = value.p_value
        if name == "remotefailure":
            self._remotefailure_outputpointer = value.p_value
        if name == "requiredremoterelease":
            self._requiredremoterelease_outputpointer = value.p_value
        if name == "allowedremoterelief":
            self._allowedremoterelief_outputpointer = value.p_value
        if name == "requiredremotesupply":
            self._requiredremotesupply_outputpointer = value.p_value
        if name == "possibleremoterelief":
            self._possibleremoterelief_outputpointer = value.p_value
        if name == "actualremoterelief":
            self._actualremoterelief_outputpointer = value.p_value
        if name == "requiredrelease":
            self._requiredrelease_outputpointer = value.p_value
        if name == "targetedrelease":
            self._targetedrelease_outputpointer = value.p_value
        if name == "actualrelease":
            self._actualrelease_outputpointer = value.p_value
        if name == "missingremoterelease":
            self._missingremoterelease_outputpointer = value.p_value
        if name == "actualremoterelease":
            self._actualremoterelease_outputpointer = value.p_value
        if name == "flooddischarge":
            self._flooddischarge_outputpointer = value.p_value
        if name == "freedischarge":
            self._freedischarge_outputpointer = value.p_value
        if name == "maxforceddischarge":
            self._maxforceddischarge_outputpointer = value.p_value
        if name == "maxfreedischarge":
            self._maxfreedischarge_outputpointer = value.p_value
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
        if self._exchange_outputflag:
            self._exchange_outputpointer[0] = self.exchange
        if self._totalremotedischarge_outputflag:
            self._totalremotedischarge_outputpointer[0] = self.totalremotedischarge
        if self._naturalremotedischarge_outputflag:
            self._naturalremotedischarge_outputpointer[0] = self.naturalremotedischarge
        if self._remotedemand_outputflag:
            self._remotedemand_outputpointer[0] = self.remotedemand
        if self._remotefailure_outputflag:
            self._remotefailure_outputpointer[0] = self.remotefailure
        if self._requiredremoterelease_outputflag:
            self._requiredremoterelease_outputpointer[0] = self.requiredremoterelease
        if self._allowedremoterelief_outputflag:
            self._allowedremoterelief_outputpointer[0] = self.allowedremoterelief
        if self._requiredremotesupply_outputflag:
            self._requiredremotesupply_outputpointer[0] = self.requiredremotesupply
        if self._possibleremoterelief_outputflag:
            self._possibleremoterelief_outputpointer[0] = self.possibleremoterelief
        if self._actualremoterelief_outputflag:
            self._actualremoterelief_outputpointer[0] = self.actualremoterelief
        if self._requiredrelease_outputflag:
            self._requiredrelease_outputpointer[0] = self.requiredrelease
        if self._targetedrelease_outputflag:
            self._targetedrelease_outputpointer[0] = self.targetedrelease
        if self._actualrelease_outputflag:
            self._actualrelease_outputpointer[0] = self.actualrelease
        if self._missingremoterelease_outputflag:
            self._missingremoterelease_outputpointer[0] = self.missingremoterelease
        if self._actualremoterelease_outputflag:
            self._actualremoterelease_outputpointer[0] = self.actualremoterelease
        if self._flooddischarge_outputflag:
            self._flooddischarge_outputpointer[0] = self.flooddischarge
        if self._freedischarge_outputflag:
            self._freedischarge_outputpointer[0] = self.freedischarge
        if self._maxforceddischarge_outputflag:
            self._maxforceddischarge_outputpointer[0] = self.maxforceddischarge
        if self._maxfreedischarge_outputflag:
            self._maxfreedischarge_outputpointer[0] = self.maxfreedischarge
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
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._q_diskflag_writing:
            self._q_ncarray[0] = self.q
        if self._q_ramflag:
            self._q_array[idx] = self.q
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self._q_pointer = pointer.p_value
        if name == "s":
            self._s_pointer = pointer.p_value
        if name == "r":
            self._r_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "q":
            return self._q_pointer[0]
        if name == "s":
            return self._s_pointer[0]
        if name == "r":
            return self._r_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self._q_pointer[0] = value
        if name == "s":
            self._s_pointer[0] = value
        if name == "r":
            self._r_pointer[0] = value
@cython.final
cdef class SenderSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._d_diskflag_reading:
            self.d = self._d_ncarray[0]
        elif self._d_ramflag:
            self.d = self._d_array[idx]
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._d_diskflag_writing:
            self._d_ncarray[0] = self.d
        if self._d_ramflag:
            self._d_array[idx] = self.d
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "d":
            self._d_pointer = pointer.p_value
        if name == "s":
            self._s_pointer = pointer.p_value
        if name == "r":
            self._r_pointer = pointer.p_value
    cpdef get_pointervalue(self, str name):
        cdef numpy.int64_t idx
        if name == "d":
            return self._d_pointer[0]
        if name == "s":
            return self._s_pointer[0]
        if name == "r":
            return self._r_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "d":
            self._d_pointer[0] = value
        if name == "s":
            self._s_pointer[0] = value
        if name == "r":
            self._r_pointer[0] = value
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
        self.sequences.senders.save_data(idx)
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
        if not self.threading:
            self.sequences.inlets.s = self.sequences.inlets._s_pointer[0]
        if not self.threading:
            self.sequences.inlets.r = self.sequences.inlets._r_pointer[0]
        if not self.threading:
            for i in range(self.sequences.inlets._e_length_0):
                if self.sequences.inlets._e_ready[i]:
                    self.sequences.inlets.e[i] = self.sequences.inlets._e_pointer[i][0]
                else:
                    self.sequences.inlets.e[i] = nan
        self.calc_precipitation_v1()
        self.calc_adjustedprecipitation_v1()
        self.calc_potentialevaporation_v1()
        self.calc_adjustedevaporation_v1()
        self.calc_actualevaporation_v1()
        self.pic_inflow_v1()
        self.pic_inflow_v2()
        self.calc_naturalremotedischarge_v1()
        self.calc_remotedemand_v1()
        self.calc_remotefailure_v1()
        self.calc_requiredremoterelease_v1()
        self.calc_requiredrelease_v1()
        self.calc_requiredrelease_v2()
        self.calc_targetedrelease_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_outlets()
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_outlets()
        self.pass_outflow_v1()
        self.update_loggedoutflow_v1()
        self.pass_actualremoterelease_v1()
        self.pass_actualremoterelief_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
        if not self.threading:
            self.sequences.outlets._s_pointer[0] = self.sequences.outlets._s_pointer[0] + self.sequences.outlets.s
        if not self.threading:
            self.sequences.outlets._r_pointer[0] = self.sequences.outlets._r_pointer[0] + self.sequences.outlets.r
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_receivers(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_receivers(idx)
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.receivers.q = self.sequences.receivers._q_pointer[0]
        if not self.threading:
            self.sequences.receivers.d = self.sequences.receivers._d_pointer[0]
        if not self.threading:
            self.sequences.receivers.s = self.sequences.receivers._s_pointer[0]
        if not self.threading:
            self.sequences.receivers.r = self.sequences.receivers._r_pointer[0]
        if not self.threading:
            self.sequences.receivers.owl = self.sequences.receivers._owl_pointer[0]
        if not self.threading:
            self.sequences.receivers.rwl = self.sequences.receivers._rwl_pointer[0]
        self.pic_totalremotedischarge_v1()
        self.update_loggedtotalremotedischarge_v1()
        self.pick_loggedouterwaterlevel_v1()
        self.pick_loggedremotewaterlevel_v1()
        self.pic_loggedrequiredremoterelease_v1()
        self.pic_loggedrequiredremoterelease_v2()
        self.pic_exchange_v1()
        self.calc_requiredremoterelease_v2()
        self.pic_loggedallowedremoterelief_v1()
        self.calc_allowedremoterelief_v1()
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.pemodel is not None) and not self.pemodel_is_mainmodel:
            self.pemodel.update_senders(idx)
        if (self.precipmodel is not None) and not self.precipmodel_is_mainmodel:
            self.precipmodel.update_senders(idx)
        self.calc_missingremoterelease_v1()
        self.pass_missingremoterelease_v1()
        self.calc_allowedremoterelief_v2()
        self.pass_allowedremoterelief_v1()
        self.calc_requiredremotesupply_v1()
        self.pass_requiredremotesupply_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.senders._d_pointer[0] = self.sequences.senders._d_pointer[0] + self.sequences.senders.d
        if not self.threading:
            self.sequences.senders._s_pointer[0] = self.sequences.senders._s_pointer[0] + self.sequences.senders.s
        if not self.threading:
            self.sequences.senders._r_pointer[0] = self.sequences.senders._r_pointer[0] + self.sequences.senders.r
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
        self.pic_inflow_v1()
        self.pic_inflow_v2()
        self.calc_waterlevel_v1()
        self.calc_outerwaterlevel_v1()
        self.calc_remotewaterlevel_v1()
        self.calc_waterleveldifference_v1()
        self.calc_effectivewaterleveldifference_v1()
        self.calc_surfacearea_v1()
        self.calc_alloweddischarge_v1()
        self.calc_alloweddischarge_v2()
        self.calc_actualrelease_v1()
        self.calc_actualrelease_v2()
        self.calc_actualrelease_v3()
        self.calc_possibleremoterelief_v1()
        self.calc_actualremoterelief_v1()
        self.calc_actualremoterelease_v1()
        self.update_actualremoterelief_v1()
        self.update_actualremoterelease_v1()
        self.calc_flooddischarge_v1()
        self.calc_maxforceddischarge_v1()
        self.calc_maxfreedischarge_v1()
        self.calc_forceddischarge_v1()
        self.calc_freedischarge_v1()
        self.calc_outflow_v1()
        self.calc_outflow_v2()
        self.calc_outflow_v3()
        self.calc_outflow_v4()
        self.calc_outflow_v5()
    cpdef inline void calculate_full_terms(self) noexcept nogil:
        self.update_watervolume_v1()
        self.update_watervolume_v2()
        self.update_watervolume_v3()
        self.update_watervolume_v4()
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
        self.sequences.fluxes.exchange = self.sequences.fluxes._exchange_sum
        self.sequences.fluxes.possibleremoterelief = self.sequences.fluxes._possibleremoterelief_sum
        self.sequences.fluxes.actualremoterelief = self.sequences.fluxes._actualremoterelief_sum
        self.sequences.fluxes.actualrelease = self.sequences.fluxes._actualrelease_sum
        self.sequences.fluxes.actualremoterelease = self.sequences.fluxes._actualremoterelease_sum
        self.sequences.fluxes.flooddischarge = self.sequences.fluxes._flooddischarge_sum
        self.sequences.fluxes.freedischarge = self.sequences.fluxes._freedischarge_sum
        self.sequences.fluxes.maxforceddischarge = self.sequences.fluxes._maxforceddischarge_sum
        self.sequences.fluxes.maxfreedischarge = self.sequences.fluxes._maxfreedischarge_sum
        self.sequences.fluxes.forceddischarge = self.sequences.fluxes._forceddischarge_sum
        self.sequences.fluxes.outflow = self.sequences.fluxes._outflow_sum
    cpdef inline void set_point_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_points[self.numvars.idx_stage] = self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_points[self.numvars.idx_stage] = self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_points[self.numvars.idx_stage] = self.sequences.fluxes.inflow
        self.sequences.fluxes._exchange_points[self.numvars.idx_stage] = self.sequences.fluxes.exchange
        self.sequences.fluxes._possibleremoterelief_points[self.numvars.idx_stage] = self.sequences.fluxes.possibleremoterelief
        self.sequences.fluxes._actualremoterelief_points[self.numvars.idx_stage] = self.sequences.fluxes.actualremoterelief
        self.sequences.fluxes._actualrelease_points[self.numvars.idx_stage] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._actualremoterelease_points[self.numvars.idx_stage] = self.sequences.fluxes.actualremoterelease
        self.sequences.fluxes._flooddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._freedischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.freedischarge
        self.sequences.fluxes._maxforceddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._maxfreedischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.maxfreedischarge
        self.sequences.fluxes._forceddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.forceddischarge
        self.sequences.fluxes._outflow_points[self.numvars.idx_stage] = self.sequences.fluxes.outflow
    cpdef inline void set_result_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_results[self.numvars.idx_method] = self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_results[self.numvars.idx_method] = self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_results[self.numvars.idx_method] = self.sequences.fluxes.inflow
        self.sequences.fluxes._exchange_results[self.numvars.idx_method] = self.sequences.fluxes.exchange
        self.sequences.fluxes._possibleremoterelief_results[self.numvars.idx_method] = self.sequences.fluxes.possibleremoterelief
        self.sequences.fluxes._actualremoterelief_results[self.numvars.idx_method] = self.sequences.fluxes.actualremoterelief
        self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._actualremoterelease_results[self.numvars.idx_method] = self.sequences.fluxes.actualremoterelease
        self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._freedischarge_results[self.numvars.idx_method] = self.sequences.fluxes.freedischarge
        self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._maxfreedischarge_results[self.numvars.idx_method] = self.sequences.fluxes.maxfreedischarge
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
        self.sequences.fluxes.exchange = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.exchange = self.sequences.fluxes.exchange +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._exchange_points[jdx]
        self.sequences.fluxes.possibleremoterelief = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.possibleremoterelief = self.sequences.fluxes.possibleremoterelief +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._possibleremoterelief_points[jdx]
        self.sequences.fluxes.actualremoterelief = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualremoterelief = self.sequences.fluxes.actualremoterelief +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualremoterelief_points[jdx]
        self.sequences.fluxes.actualrelease = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualrelease_points[jdx]
        self.sequences.fluxes.actualremoterelease = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualremoterelease = self.sequences.fluxes.actualremoterelease +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualremoterelease_points[jdx]
        self.sequences.fluxes.flooddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.flooddischarge = self.sequences.fluxes.flooddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._flooddischarge_points[jdx]
        self.sequences.fluxes.freedischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.freedischarge = self.sequences.fluxes.freedischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._freedischarge_points[jdx]
        self.sequences.fluxes.maxforceddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.maxforceddischarge = self.sequences.fluxes.maxforceddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._maxforceddischarge_points[jdx]
        self.sequences.fluxes.maxfreedischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.maxfreedischarge = self.sequences.fluxes.maxfreedischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._maxfreedischarge_points[jdx]
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
        self.sequences.fluxes._exchange_sum = 0.
        self.sequences.fluxes._possibleremoterelief_sum = 0.
        self.sequences.fluxes._actualremoterelief_sum = 0.
        self.sequences.fluxes._actualrelease_sum = 0.
        self.sequences.fluxes._actualremoterelease_sum = 0.
        self.sequences.fluxes._flooddischarge_sum = 0.
        self.sequences.fluxes._freedischarge_sum = 0.
        self.sequences.fluxes._maxforceddischarge_sum = 0.
        self.sequences.fluxes._maxfreedischarge_sum = 0.
        self.sequences.fluxes._forceddischarge_sum = 0.
        self.sequences.fluxes._outflow_sum = 0.
    cpdef inline void addup_fluxes(self) noexcept nogil:
        self.sequences.fluxes._adjustedprecipitation_sum = self.sequences.fluxes._adjustedprecipitation_sum + self.sequences.fluxes.adjustedprecipitation
        self.sequences.fluxes._actualevaporation_sum = self.sequences.fluxes._actualevaporation_sum + self.sequences.fluxes.actualevaporation
        self.sequences.fluxes._inflow_sum = self.sequences.fluxes._inflow_sum + self.sequences.fluxes.inflow
        self.sequences.fluxes._exchange_sum = self.sequences.fluxes._exchange_sum + self.sequences.fluxes.exchange
        self.sequences.fluxes._possibleremoterelief_sum = self.sequences.fluxes._possibleremoterelief_sum + self.sequences.fluxes.possibleremoterelief
        self.sequences.fluxes._actualremoterelief_sum = self.sequences.fluxes._actualremoterelief_sum + self.sequences.fluxes.actualremoterelief
        self.sequences.fluxes._actualrelease_sum = self.sequences.fluxes._actualrelease_sum + self.sequences.fluxes.actualrelease
        self.sequences.fluxes._actualremoterelease_sum = self.sequences.fluxes._actualremoterelease_sum + self.sequences.fluxes.actualremoterelease
        self.sequences.fluxes._flooddischarge_sum = self.sequences.fluxes._flooddischarge_sum + self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._freedischarge_sum = self.sequences.fluxes._freedischarge_sum + self.sequences.fluxes.freedischarge
        self.sequences.fluxes._maxforceddischarge_sum = self.sequences.fluxes._maxforceddischarge_sum + self.sequences.fluxes.maxforceddischarge
        self.sequences.fluxes._maxfreedischarge_sum = self.sequences.fluxes._maxfreedischarge_sum + self.sequences.fluxes.maxfreedischarge
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
        abserror = fabs(self.sequences.fluxes._exchange_results[self.numvars.idx_method]-self.sequences.fluxes._exchange_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._exchange_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._exchange_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._possibleremoterelief_results[self.numvars.idx_method]-self.sequences.fluxes._possibleremoterelief_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._possibleremoterelief_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._possibleremoterelief_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualremoterelief_results[self.numvars.idx_method]-self.sequences.fluxes._actualremoterelief_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualremoterelief_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualremoterelief_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]-self.sequences.fluxes._actualrelease_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualremoterelease_results[self.numvars.idx_method]-self.sequences.fluxes._actualremoterelease_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualremoterelease_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualremoterelease_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._freedischarge_results[self.numvars.idx_method]-self.sequences.fluxes._freedischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._freedischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._freedischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._maxforceddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._maxfreedischarge_results[self.numvars.idx_method]-self.sequences.fluxes._maxfreedischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._maxfreedischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._maxfreedischarge_results[self.numvars.idx_method]))
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
    cpdef inline void pic_totalremotedischarge_v1(self) noexcept nogil:
        self.sequences.fluxes.totalremotedischarge = self.sequences.receivers.q
    cpdef inline void update_loggedtotalremotedischarge_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedtotalremotedischarge[i] = self.sequences.logs.loggedtotalremotedischarge[i - 1]
        self.sequences.logs.loggedtotalremotedischarge[0] = self.sequences.fluxes.totalremotedischarge
    cpdef inline void pick_loggedouterwaterlevel_v1(self) noexcept nogil:
        self.sequences.logs.loggedouterwaterlevel[0] = self.sequences.receivers.owl
    cpdef inline void pick_loggedremotewaterlevel_v1(self) noexcept nogil:
        self.sequences.logs.loggedremotewaterlevel[0] = self.sequences.receivers.rwl
    cpdef inline void pic_loggedrequiredremoterelease_v1(self) noexcept nogil:
        self.sequences.logs.loggedrequiredremoterelease[0] = self.sequences.receivers.d
    cpdef inline void pic_loggedrequiredremoterelease_v2(self) noexcept nogil:
        self.sequences.logs.loggedrequiredremoterelease[0] = self.sequences.receivers.s
    cpdef inline void pic_exchange_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.exchange = 0.0
        for idx in range(self.sequences.inlets.len_e):
            self.sequences.fluxes.exchange = self.sequences.fluxes.exchange + (self.sequences.inlets.e[idx])
    cpdef inline void calc_requiredremoterelease_v2(self) noexcept nogil:
        self.sequences.fluxes.requiredremoterelease = self.sequences.logs.loggedrequiredremoterelease[0]
    cpdef inline void pic_loggedallowedremoterelief_v1(self) noexcept nogil:
        self.sequences.logs.loggedallowedremoterelief[0] = self.sequences.receivers.r
    cpdef inline void calc_allowedremoterelief_v1(self) noexcept nogil:
        self.sequences.fluxes.allowedremoterelief = self.sequences.logs.loggedallowedremoterelief[0]
    cpdef inline void calc_precipitation_v1(self) noexcept nogil:
        if self.precipmodel is None:
            self.sequences.fluxes.precipitation = 0.0
        elif self.precipmodel_typeid == 2:
            (<masterinterface.MasterInterface>self.precipmodel).determine_precipitation()
            self.sequences.fluxes.precipitation = (<masterinterface.MasterInterface>self.precipmodel).get_precipitation(0)
    cpdef inline void calc_adjustedprecipitation_v1(self) noexcept nogil:
        self.sequences.fluxes.adjustedprecipitation = (            self.parameters.derived.inputfactor * self.parameters.control.correctionprecipitation * self.sequences.fluxes.precipitation        )
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
    cpdef inline void calc_actualevaporation_v1(self) noexcept nogil:
        self.sequences.fluxes.actualevaporation = self.sequences.fluxes.adjustedevaporation * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.thresholdevaporation, self.parameters.derived.smoothparevaporation        )
    cpdef inline void pic_inflow_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void pic_inflow_v2(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.inflow = self.sequences.inlets.s + self.sequences.inlets.r
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.q[idx])
    cpdef inline void calc_naturalremotedischarge_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.naturalremotedischarge = 0.0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge + ((                self.sequences.logs.loggedtotalremotedischarge[idx] - self.sequences.logs.loggedoutflow[idx]            ))
        if self.sequences.fluxes.naturalremotedischarge > 0.0:
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge / (self.parameters.control.nmblogentries)
        else:
            self.sequences.fluxes.naturalremotedischarge = 0.0
    cpdef inline void calc_remotedemand_v1(self) noexcept nogil:
        cdef double d_rdm
        d_rdm = self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]]
        self.sequences.fluxes.remotedemand = max(d_rdm - self.sequences.fluxes.naturalremotedischarge, 0.0)
    cpdef inline void calc_remotefailure_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.remotefailure = 0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure - (self.sequences.logs.loggedtotalremotedischarge[idx])
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure / (self.parameters.control.nmblogentries)
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure + (self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]])
    cpdef inline void calc_requiredremoterelease_v1(self) noexcept nogil:
        self.sequences.fluxes.requiredremoterelease = self.sequences.fluxes.remotedemand + (            smoothutils.smooth_logistic1(                self.sequences.fluxes.remotefailure, self.parameters.derived.remotedischargesmoothpar[self.parameters.derived.toy[self.idx_sim]]            )            * self.parameters.control.remotedischargesafety[self.parameters.derived.toy[self.idx_sim]]        )
    cpdef inline void calc_requiredrelease_v1(self) noexcept nogil:
        self.sequences.fluxes.requiredrelease = self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]]
        self.sequences.fluxes.requiredrelease = self.sequences.fluxes.requiredrelease + smoothutils.smooth_logistic2(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.requiredrelease,            self.parameters.derived.neardischargeminimumsmoothpar2[self.parameters.derived.toy[self.idx_sim]],        )
    cpdef inline void calc_requiredrelease_v2(self) noexcept nogil:
        self.sequences.fluxes.requiredrelease = self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]]
    cpdef inline void calc_targetedrelease_v1(self) noexcept nogil:
        if self.parameters.control.restricttargetedrelease:
            self.sequences.fluxes.targetedrelease = smoothutils.smooth_logistic1(                self.sequences.fluxes.inflow - self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]],                self.parameters.derived.neardischargeminimumsmoothpar1[self.parameters.derived.toy[self.idx_sim]],            )
            self.sequences.fluxes.targetedrelease = (                self.sequences.fluxes.targetedrelease * self.sequences.fluxes.requiredrelease                + (1.0 - self.sequences.fluxes.targetedrelease) * self.sequences.fluxes.inflow            )
        else:
            self.sequences.fluxes.targetedrelease = self.sequences.fluxes.requiredrelease
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
    cpdef inline void calc_effectivewaterleveldifference_v1(self) noexcept nogil:
        cdef double ho
        cdef double hi
        hi = smoothutils.smooth_max1(            self.sequences.factors.waterlevel, self.parameters.control.crestlevel, self.parameters.derived.crestlevelsmoothpar        )
        ho = smoothutils.smooth_max1(            self.sequences.factors.outerwaterlevel, self.parameters.control.crestlevel, self.parameters.derived.crestlevelsmoothpar        )
        self.sequences.factors.effectivewaterleveldifference = hi - ho
    cpdef inline void calc_surfacearea_v1(self) noexcept nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.parameters.control.watervolume2waterlevel.calculate_derivatives(0)
        self.sequences.aides.surfacearea = 1.0 / self.parameters.control.watervolume2waterlevel.output_derivatives[0]
    cpdef inline void calc_alloweddischarge_v1(self) noexcept nogil:
        self.sequences.aides.alloweddischarge = (            self.parameters.control.allowedwaterleveldrop / self.parameters.derived.seconds * self.sequences.aides.surfacearea * 1e6            + self.sequences.fluxes.adjustedprecipitation            + self.sequences.fluxes.inflow            - self.sequences.fluxes.actualevaporation            + self.sequences.fluxes.exchange        )
    cpdef inline void calc_alloweddischarge_v2(self) noexcept nogil:
        self.sequences.aides.alloweddischarge = smoothutils.smooth_min1(            self.parameters.control.allowedwaterleveldrop / self.parameters.derived.seconds * self.sequences.aides.surfacearea * 1e6            + self.sequences.fluxes.inflow,            self.parameters.control.allowedrelease[self.parameters.derived.toy[self.idx_sim]],            self.parameters.derived.dischargesmoothpar,        )
    cpdef inline void calc_actualrelease_v1(self) noexcept nogil:
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.targetedrelease * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelminimumthreshold,            self.parameters.derived.waterlevelminimumsmoothpar,        )
    cpdef inline void calc_actualrelease_v2(self) noexcept nogil:
        self.sequences.fluxes.actualrelease = self.parameters.control.allowedrelease[            self.parameters.derived.toy[self.idx_sim]        ] * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelminimumthreshold,            self.parameters.derived.waterlevelminimumsmoothpar,        )
    cpdef inline void calc_actualrelease_v3(self) noexcept nogil:
        cdef double d_weight
        cdef double d_release2
        cdef double d_neutral
        cdef double d_release1
        cdef double d_upperbound
        cdef double d_factor
        cdef double d_qmax
        cdef double d_qmin
        cdef double d_range
        cdef double d_target
        cdef numpy.int64_t idx_toy
        idx_toy = self.parameters.derived.toy[self.idx_sim]
        d_target = self.parameters.control.targetvolume[idx_toy]
        d_range = max(self.parameters.control.targetrangeabsolute, self.parameters.control.targetrangerelative * d_target)
        d_range = max(d_range, 1e-6)
        d_qmin = self.parameters.control.neardischargeminimumthreshold[idx_toy]
        d_qmax = smoothutils.smooth_max1(            d_qmin, self.sequences.aides.alloweddischarge, self.parameters.derived.dischargesmoothpar        )
        d_factor = smoothutils.smooth_logistic3(            (self.sequences.new_states.watervolume - d_target + d_range) / d_range, self.parameters.derived.volumesmoothparlog2        )
        d_upperbound = smoothutils.smooth_min1(            d_qmax, self.sequences.fluxes.inflow, self.parameters.derived.dischargesmoothpar        )
        d_release1 = (1.0 - d_factor) * d_qmin + d_factor * smoothutils.smooth_max1(            d_qmin, d_upperbound, self.parameters.derived.dischargesmoothpar        )
        d_factor = smoothutils.smooth_logistic3(            (d_target + d_range - self.sequences.new_states.watervolume) / d_range, self.parameters.derived.volumesmoothparlog2        )
        d_neutral = smoothutils.smooth_max1(d_qmin, self.sequences.fluxes.inflow, self.parameters.derived.dischargesmoothpar)
        d_release2 = (1.0 - d_factor) * d_qmax + d_factor * smoothutils.smooth_min1(            d_qmax, d_neutral, self.parameters.derived.dischargesmoothpar        )
        d_weight = smoothutils.smooth_logistic1(            d_target - self.sequences.new_states.watervolume, self.parameters.derived.volumesmoothparlog1        )
        self.sequences.fluxes.actualrelease = d_weight * d_release1 + (1.0 - d_weight) * d_release2
        if self.parameters.derived.volumesmoothparlog1 > 0.0:
            d_weight = exp(                -(((self.sequences.new_states.watervolume - d_target) / self.parameters.derived.volumesmoothparlog1) ** 2)            )
        else:
            d_weight = 0.0
        d_neutral = smoothutils.smooth_max1(            d_upperbound, d_qmin, self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = d_weight * d_neutral + (1.0 - d_weight) * self.sequences.fluxes.actualrelease
        self.sequences.fluxes.actualrelease = smoothutils.smooth_max1(            self.sequences.fluxes.actualrelease, 0.0, self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease * (smoothutils.smooth_logistic1(            self.sequences.new_states.watervolume - self.parameters.control.watervolumeminimumthreshold[idx_toy],            self.parameters.derived.volumesmoothparlog1,        ))
    cpdef inline void calc_possibleremoterelief_v1(self) noexcept nogil:
        self.parameters.control.waterlevel2possibleremoterelief.inputs[0] = self.sequences.factors.waterlevel
        self.parameters.control.waterlevel2possibleremoterelief.calculate_values()
        self.sequences.fluxes.possibleremoterelief = self.parameters.control.waterlevel2possibleremoterelief.outputs[0]
    cpdef inline void calc_actualremoterelief_v1(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelief = self.fix_min1_v1(            self.sequences.fluxes.possibleremoterelief,            self.sequences.fluxes.allowedremoterelief,            self.parameters.control.remoterelieftolerance,            True,        )
    cpdef inline void calc_actualremoterelease_v1(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelease = (            self.sequences.fluxes.requiredremoterelease            * smoothutils.smooth_logistic1(                self.sequences.factors.waterlevel - self.parameters.control.waterlevelminimumremotethreshold,                self.parameters.derived.waterlevelminimumremotesmoothpar,            )        )
    cpdef inline void update_actualremoterelief_v1(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelief = self.fix_min1_v1(            self.sequences.fluxes.actualremoterelief,            self.parameters.control.highestremotedischarge,            self.parameters.derived.highestremotesmoothpar,            False,        )
    cpdef inline void update_actualremoterelease_v1(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelease = self.fix_min1_v1(            self.sequences.fluxes.actualremoterelease,            self.parameters.control.highestremotedischarge - self.sequences.fluxes.actualremoterelief,            self.parameters.derived.highestremotesmoothpar,            False,        )
    cpdef inline void calc_flooddischarge_v1(self) noexcept nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.factors.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_maxforceddischarge_v1(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxforceddischarge.inputs[0] = self.sequences.factors.waterleveldifference
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxforceddischarge.calculate_values(toy)
        self.sequences.fluxes.maxforceddischarge = self.parameters.control.waterleveldifference2maxforceddischarge.outputs[0]
    cpdef inline void calc_maxfreedischarge_v1(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxfreedischarge.inputs[0] = (            self.sequences.factors.effectivewaterleveldifference        )
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxfreedischarge.calculate_values(toy)
        self.sequences.fluxes.maxfreedischarge = self.parameters.control.waterleveldifference2maxfreedischarge.outputs[0]
    cpdef inline void calc_forceddischarge_v1(self) noexcept nogil:
        cdef double r2
        cdef double r1
        r1 = smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelmaximumthreshold,            self.parameters.derived.waterlevelmaximumsmoothpar,        )
        r2 = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        if self.sequences.fluxes.maxforceddischarge >= 0.0:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * r1 * (1.0 - r2)
        else:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * (1.0 - r1) * r2
    cpdef inline void calc_freedischarge_v1(self) noexcept nogil:
        cdef double q_trimmed
        cdef double w
        w = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        q_trimmed = -smoothutils.smooth_logistic2(            -self.sequences.fluxes.maxfreedischarge, self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.freedischarge = w * q_trimmed + (1.0 - w) * self.sequences.fluxes.maxfreedischarge
    cpdef inline void calc_outflow_v1(self) noexcept nogil:
        self.sequences.fluxes.outflow = max(self.sequences.fluxes.actualrelease + self.sequences.fluxes.flooddischarge, 0.0)
    cpdef inline void calc_outflow_v2(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.fix_min1_v1(            self.sequences.fluxes.flooddischarge, self.sequences.aides.alloweddischarge, self.parameters.derived.dischargesmoothpar, False        )
    cpdef inline void calc_outflow_v3(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.fluxes.forceddischarge
    cpdef inline void calc_outflow_v4(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.fluxes.freedischarge
    cpdef inline void calc_outflow_v5(self) noexcept nogil:
        self.sequences.fluxes.outflow = self.sequences.fluxes.freedischarge + self.sequences.fluxes.forceddischarge
    cpdef inline void update_watervolume_v1(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + self.parameters.derived.seconds / 1e6 * (            self.sequences.fluxes.adjustedprecipitation - self.sequences.fluxes.actualevaporation + self.sequences.fluxes.inflow - self.sequences.fluxes.outflow        )
    cpdef inline void update_watervolume_v2(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + self.parameters.derived.seconds / 1e6 * (            self.sequences.fluxes.adjustedprecipitation            - self.sequences.fluxes.actualevaporation            + self.sequences.fluxes.inflow            - self.sequences.fluxes.outflow            - self.sequences.fluxes.actualremoterelease        )
    cpdef inline void update_watervolume_v3(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + (self.parameters.derived.seconds / 1e6) * (            self.sequences.fluxes.adjustedprecipitation            - self.sequences.fluxes.actualevaporation            + self.sequences.fluxes.inflow            - self.sequences.fluxes.outflow            - self.sequences.fluxes.actualremoterelease            - self.sequences.fluxes.actualremoterelief        )
    cpdef inline void update_watervolume_v4(self) noexcept nogil:
        self.sequences.new_states.watervolume = self.sequences.old_states.watervolume + self.parameters.derived.seconds / 1e6 * (            self.sequences.fluxes.adjustedprecipitation            - self.sequences.fluxes.actualevaporation            + self.sequences.fluxes.inflow            - self.sequences.fluxes.outflow            + self.sequences.fluxes.exchange        )
    cpdef inline double fix_min1_v1(self, double input_, double threshold, double smoothpar, numpy.npy_bool relative) noexcept nogil:
        cdef numpy.int64_t _
        cdef double d_result
        if relative:
            smoothpar = smoothpar * (threshold)
        d_result = smoothutils.smooth_min1(input_, threshold, smoothpar)
        for _ in range(5):
            smoothpar = smoothpar / (5.0)
            d_result = smoothutils.smooth_max1(d_result, 0.0, smoothpar)
            smoothpar = smoothpar / (5.0)
            if relative:
                d_result = smoothutils.smooth_min1(d_result, input_, smoothpar)
            else:
                d_result = smoothutils.smooth_min1(d_result, threshold, smoothpar)
        return max(min(d_result, input_, threshold), 0.0)
    cpdef inline void pass_outflow_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
    cpdef inline void update_loggedoutflow_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedoutflow[idx] = self.sequences.logs.loggedoutflow[idx - 1]
        self.sequences.logs.loggedoutflow[0] = self.sequences.fluxes.outflow
    cpdef inline void pass_actualremoterelease_v1(self) noexcept nogil:
        self.sequences.outlets.s = self.sequences.fluxes.actualremoterelease
    cpdef inline void pass_actualremoterelief_v1(self) noexcept nogil:
        self.sequences.outlets.r = self.sequences.fluxes.actualremoterelief
    cpdef inline void calc_missingremoterelease_v1(self) noexcept nogil:
        self.sequences.fluxes.missingremoterelease = max(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.actualrelease, 0.0        )
    cpdef inline void pass_missingremoterelease_v1(self) noexcept nogil:
        self.sequences.senders.d = self.sequences.fluxes.missingremoterelease
    cpdef inline void calc_allowedremoterelief_v2(self) noexcept nogil:
        cdef numpy.int64_t toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.allowedremoterelief = (            smoothutils.smooth_logistic1(                self.parameters.control.waterlevelreliefthreshold[toy] - self.sequences.factors.waterlevel,                self.parameters.derived.waterlevelreliefsmoothpar[toy],            )            * self.parameters.control.highestremoterelief[toy]        )
    cpdef inline void pass_allowedremoterelief_v1(self) noexcept nogil:
        self.sequences.senders.r = self.sequences.fluxes.allowedremoterelief
    cpdef inline void calc_requiredremotesupply_v1(self) noexcept nogil:
        cdef numpy.int64_t toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.requiredremotesupply = (            smoothutils.smooth_logistic1(                self.parameters.control.waterlevelsupplythreshold[toy] - self.sequences.factors.waterlevel,                self.parameters.derived.waterlevelsupplysmoothpar[toy],            )            * self.parameters.control.highestremotesupply[toy]        )
    cpdef inline void pass_requiredremotesupply_v1(self) noexcept nogil:
        self.sequences.senders.s = self.sequences.fluxes.requiredremotesupply
    cpdef inline void pic_totalremotedischarge(self) noexcept nogil:
        self.sequences.fluxes.totalremotedischarge = self.sequences.receivers.q
    cpdef inline void update_loggedtotalremotedischarge(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedtotalremotedischarge[i] = self.sequences.logs.loggedtotalremotedischarge[i - 1]
        self.sequences.logs.loggedtotalremotedischarge[0] = self.sequences.fluxes.totalremotedischarge
    cpdef inline void pick_loggedouterwaterlevel(self) noexcept nogil:
        self.sequences.logs.loggedouterwaterlevel[0] = self.sequences.receivers.owl
    cpdef inline void pick_loggedremotewaterlevel(self) noexcept nogil:
        self.sequences.logs.loggedremotewaterlevel[0] = self.sequences.receivers.rwl
    cpdef inline void pic_exchange(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.exchange = 0.0
        for idx in range(self.sequences.inlets.len_e):
            self.sequences.fluxes.exchange = self.sequences.fluxes.exchange + (self.sequences.inlets.e[idx])
    cpdef inline void pic_loggedallowedremoterelief(self) noexcept nogil:
        self.sequences.logs.loggedallowedremoterelief[0] = self.sequences.receivers.r
    cpdef inline void calc_precipitation(self) noexcept nogil:
        if self.precipmodel is None:
            self.sequences.fluxes.precipitation = 0.0
        elif self.precipmodel_typeid == 2:
            (<masterinterface.MasterInterface>self.precipmodel).determine_precipitation()
            self.sequences.fluxes.precipitation = (<masterinterface.MasterInterface>self.precipmodel).get_precipitation(0)
    cpdef inline void calc_adjustedprecipitation(self) noexcept nogil:
        self.sequences.fluxes.adjustedprecipitation = (            self.parameters.derived.inputfactor * self.parameters.control.correctionprecipitation * self.sequences.fluxes.precipitation        )
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
    cpdef inline void calc_actualevaporation(self) noexcept nogil:
        self.sequences.fluxes.actualevaporation = self.sequences.fluxes.adjustedevaporation * smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.thresholdevaporation, self.parameters.derived.smoothparevaporation        )
    cpdef inline void calc_naturalremotedischarge(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.naturalremotedischarge = 0.0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge + ((                self.sequences.logs.loggedtotalremotedischarge[idx] - self.sequences.logs.loggedoutflow[idx]            ))
        if self.sequences.fluxes.naturalremotedischarge > 0.0:
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge / (self.parameters.control.nmblogentries)
        else:
            self.sequences.fluxes.naturalremotedischarge = 0.0
    cpdef inline void calc_remotedemand(self) noexcept nogil:
        cdef double d_rdm
        d_rdm = self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]]
        self.sequences.fluxes.remotedemand = max(d_rdm - self.sequences.fluxes.naturalremotedischarge, 0.0)
    cpdef inline void calc_remotefailure(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.remotefailure = 0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure - (self.sequences.logs.loggedtotalremotedischarge[idx])
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure / (self.parameters.control.nmblogentries)
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure + (self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]])
    cpdef inline void calc_targetedrelease(self) noexcept nogil:
        if self.parameters.control.restricttargetedrelease:
            self.sequences.fluxes.targetedrelease = smoothutils.smooth_logistic1(                self.sequences.fluxes.inflow - self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]],                self.parameters.derived.neardischargeminimumsmoothpar1[self.parameters.derived.toy[self.idx_sim]],            )
            self.sequences.fluxes.targetedrelease = (                self.sequences.fluxes.targetedrelease * self.sequences.fluxes.requiredrelease                + (1.0 - self.sequences.fluxes.targetedrelease) * self.sequences.fluxes.inflow            )
        else:
            self.sequences.fluxes.targetedrelease = self.sequences.fluxes.requiredrelease
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
    cpdef inline void calc_effectivewaterleveldifference(self) noexcept nogil:
        cdef double ho
        cdef double hi
        hi = smoothutils.smooth_max1(            self.sequences.factors.waterlevel, self.parameters.control.crestlevel, self.parameters.derived.crestlevelsmoothpar        )
        ho = smoothutils.smooth_max1(            self.sequences.factors.outerwaterlevel, self.parameters.control.crestlevel, self.parameters.derived.crestlevelsmoothpar        )
        self.sequences.factors.effectivewaterleveldifference = hi - ho
    cpdef inline void calc_surfacearea(self) noexcept nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.parameters.control.watervolume2waterlevel.calculate_derivatives(0)
        self.sequences.aides.surfacearea = 1.0 / self.parameters.control.watervolume2waterlevel.output_derivatives[0]
    cpdef inline void calc_possibleremoterelief(self) noexcept nogil:
        self.parameters.control.waterlevel2possibleremoterelief.inputs[0] = self.sequences.factors.waterlevel
        self.parameters.control.waterlevel2possibleremoterelief.calculate_values()
        self.sequences.fluxes.possibleremoterelief = self.parameters.control.waterlevel2possibleremoterelief.outputs[0]
    cpdef inline void calc_actualremoterelief(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelief = self.fix_min1_v1(            self.sequences.fluxes.possibleremoterelief,            self.sequences.fluxes.allowedremoterelief,            self.parameters.control.remoterelieftolerance,            True,        )
    cpdef inline void calc_actualremoterelease(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelease = (            self.sequences.fluxes.requiredremoterelease            * smoothutils.smooth_logistic1(                self.sequences.factors.waterlevel - self.parameters.control.waterlevelminimumremotethreshold,                self.parameters.derived.waterlevelminimumremotesmoothpar,            )        )
    cpdef inline void update_actualremoterelief(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelief = self.fix_min1_v1(            self.sequences.fluxes.actualremoterelief,            self.parameters.control.highestremotedischarge,            self.parameters.derived.highestremotesmoothpar,            False,        )
    cpdef inline void update_actualremoterelease(self) noexcept nogil:
        self.sequences.fluxes.actualremoterelease = self.fix_min1_v1(            self.sequences.fluxes.actualremoterelease,            self.parameters.control.highestremotedischarge - self.sequences.fluxes.actualremoterelief,            self.parameters.derived.highestremotesmoothpar,            False,        )
    cpdef inline void calc_flooddischarge(self) noexcept nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.factors.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_maxforceddischarge(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxforceddischarge.inputs[0] = self.sequences.factors.waterleveldifference
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxforceddischarge.calculate_values(toy)
        self.sequences.fluxes.maxforceddischarge = self.parameters.control.waterleveldifference2maxforceddischarge.outputs[0]
    cpdef inline void calc_maxfreedischarge(self) noexcept nogil:
        cdef numpy.int64_t toy
        self.parameters.control.waterleveldifference2maxfreedischarge.inputs[0] = (            self.sequences.factors.effectivewaterleveldifference        )
        toy: int = self.parameters.derived.toy[self.idx_sim]
        self.parameters.control.waterleveldifference2maxfreedischarge.calculate_values(toy)
        self.sequences.fluxes.maxfreedischarge = self.parameters.control.waterleveldifference2maxfreedischarge.outputs[0]
    cpdef inline void calc_forceddischarge(self) noexcept nogil:
        cdef double r2
        cdef double r1
        r1 = smoothutils.smooth_logistic1(            self.sequences.factors.waterlevel - self.parameters.control.waterlevelmaximumthreshold,            self.parameters.derived.waterlevelmaximumsmoothpar,        )
        r2 = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        if self.sequences.fluxes.maxforceddischarge >= 0.0:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * r1 * (1.0 - r2)
        else:
            self.sequences.fluxes.forceddischarge = self.sequences.fluxes.maxforceddischarge * (1.0 - r1) * r2
    cpdef inline void calc_freedischarge(self) noexcept nogil:
        cdef double q_trimmed
        cdef double w
        w = smoothutils.smooth_logistic1(            self.sequences.factors.remotewaterlevel - self.parameters.control.remotewaterlevelmaximumthreshold,            self.parameters.derived.remotewaterlevelmaximumsmoothpar,        )
        q_trimmed = -smoothutils.smooth_logistic2(            -self.sequences.fluxes.maxfreedischarge, self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.freedischarge = w * q_trimmed + (1.0 - w) * self.sequences.fluxes.maxfreedischarge
    cpdef inline double fix_min1(self, double input_, double threshold, double smoothpar, numpy.npy_bool relative) noexcept nogil:
        cdef numpy.int64_t _
        cdef double d_result
        if relative:
            smoothpar = smoothpar * (threshold)
        d_result = smoothutils.smooth_min1(input_, threshold, smoothpar)
        for _ in range(5):
            smoothpar = smoothpar / (5.0)
            d_result = smoothutils.smooth_max1(d_result, 0.0, smoothpar)
            smoothpar = smoothpar / (5.0)
            if relative:
                d_result = smoothutils.smooth_min1(d_result, input_, smoothpar)
            else:
                d_result = smoothutils.smooth_min1(d_result, threshold, smoothpar)
        return max(min(d_result, input_, threshold), 0.0)
    cpdef inline void pass_outflow(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.outflow
    cpdef inline void update_loggedoutflow(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedoutflow[idx] = self.sequences.logs.loggedoutflow[idx - 1]
        self.sequences.logs.loggedoutflow[0] = self.sequences.fluxes.outflow
    cpdef inline void pass_actualremoterelease(self) noexcept nogil:
        self.sequences.outlets.s = self.sequences.fluxes.actualremoterelease
    cpdef inline void pass_actualremoterelief(self) noexcept nogil:
        self.sequences.outlets.r = self.sequences.fluxes.actualremoterelief
    cpdef inline void calc_missingremoterelease(self) noexcept nogil:
        self.sequences.fluxes.missingremoterelease = max(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.actualrelease, 0.0        )
    cpdef inline void pass_missingremoterelease(self) noexcept nogil:
        self.sequences.senders.d = self.sequences.fluxes.missingremoterelease
    cpdef inline void pass_allowedremoterelief(self) noexcept nogil:
        self.sequences.senders.r = self.sequences.fluxes.allowedremoterelief
    cpdef inline void calc_requiredremotesupply(self) noexcept nogil:
        cdef numpy.int64_t toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.requiredremotesupply = (            smoothutils.smooth_logistic1(                self.parameters.control.waterlevelsupplythreshold[toy] - self.sequences.factors.waterlevel,                self.parameters.derived.waterlevelsupplysmoothpar[toy],            )            * self.parameters.control.highestremotesupply[toy]        )
    cpdef inline void pass_requiredremotesupply(self) noexcept nogil:
        self.sequences.senders.s = self.sequences.fluxes.requiredremotesupply
