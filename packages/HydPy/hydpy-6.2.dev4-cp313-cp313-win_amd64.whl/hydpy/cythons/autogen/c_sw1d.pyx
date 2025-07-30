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

    cpdef void init_gateheight_callback(self):
        self.gateheight_callback = do_nothing
        cdef CallbackWrapper wrapper = CallbackWrapper()
        wrapper.callback = do_nothing
        self._gateheight_wrapper = wrapper

    cpdef CallbackWrapper get_gateheight_callback(self):
        return self._gateheight_wrapper

    cpdef void set_gateheight_callback(self, CallbackWrapper wrapper):
        self.gateheight_callback = wrapper.callback
        self._gateheight_wrapper = wrapper

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
cdef class InletSequences:
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
        if self._latq_diskflag_reading:
            k = 0
            for jdx0 in range(self._latq_length_0):
                self.latq[jdx0] = self._latq_ncarray[k]
                k += 1
        elif self._latq_ramflag:
            for jdx0 in range(self._latq_length_0):
                self.latq[jdx0] = self._latq_array[idx, jdx0]
        if self._waterlevel_diskflag_reading:
            self.waterlevel = self._waterlevel_ncarray[0]
        elif self._waterlevel_ramflag:
            self.waterlevel = self._waterlevel_array[idx]
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
        if self._latq_diskflag_writing:
            k = 0
            for jdx0 in range(self._latq_length_0):
                self._latq_ncarray[k] = self.latq[jdx0]
                k += 1
        if self._latq_ramflag:
            for jdx0 in range(self._latq_length_0):
                self._latq_array[idx, jdx0] = self.latq[jdx0]
        if self._waterlevel_diskflag_writing:
            self._waterlevel_ncarray[0] = self.waterlevel
        if self._waterlevel_ramflag:
            self._waterlevel_array[idx] = self.waterlevel
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "waterlevel":
            self._waterlevel_pointer = pointer.p_value
    cpdef inline alloc_pointer(self, name, numpy.int64_t length):
        if name == "longq":
            self._longq_length_0 = length
            self._longq_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._longq_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
        if name == "latq":
            self._latq_length_0 = length
            self._latq_ready = numpy.full(length, 0, dtype=numpy.int64)
            self._latq_pointer = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc_pointer(self, name):
        if name == "longq":
            PyMem_Free(self._longq_pointer)
        if name == "latq":
            PyMem_Free(self._latq_pointer)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "longq":
            self._longq_pointer[idx] = pointer.p_value
            self._longq_ready[idx] = 1
        if name == "latq":
            self._latq_pointer[idx] = pointer.p_value
            self._latq_ready[idx] = 1
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
        if name == "latq":
            values = numpy.empty(self.len_latq)
            for idx in range(self.len_latq):
                pointerutils.check0(self._latq_length_0)
                if self._latq_ready[idx] == 0:
                    pointerutils.check1(self._latq_length_0, idx)
                    pointerutils.check2(self._latq_ready, idx)
                values[idx] = self._latq_pointer[idx][0]
            return values
        if name == "waterlevel":
            return self._waterlevel_pointer[0]
    cpdef set_value(self, str name, value):
        if name == "longq":
            for idx in range(self.len_longq):
                pointerutils.check0(self._longq_length_0)
                if self._longq_ready[idx] == 0:
                    pointerutils.check1(self._longq_length_0, idx)
                    pointerutils.check2(self._longq_ready, idx)
                self._longq_pointer[idx][0] = value[idx]
        if name == "latq":
            for idx in range(self.len_latq):
                pointerutils.check0(self._latq_length_0)
                if self._latq_ready[idx] == 0:
                    pointerutils.check1(self._latq_length_0, idx)
                    pointerutils.check2(self._latq_ready, idx)
                self._latq_pointer[idx][0] = value[idx]
        if name == "waterlevel":
            self._waterlevel_pointer[0] = value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
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
        if self._waterlevels_diskflag_reading:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_ncarray[k]
                k += 1
        elif self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self.waterlevels[jdx0] = self._waterlevels_array[idx, jdx0]
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
        cdef numpy.int64_t jdx0
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
        if self._waterlevels_diskflag_writing:
            k = 0
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_ncarray[k] = self.waterlevels[jdx0]
                k += 1
        if self._waterlevels_ramflag:
            for jdx0 in range(self._waterlevels_length_0):
                self._waterlevels_array[idx, jdx0] = self.waterlevels[jdx0]
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
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inflow_diskflag_reading:
            self.inflow = self._inflow_ncarray[0]
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._outflow_diskflag_reading:
            self.outflow = self._outflow_ncarray[0]
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
        if self._lateralflow_diskflag_reading:
            self.lateralflow = self._lateralflow_ncarray[0]
        elif self._lateralflow_ramflag:
            self.lateralflow = self._lateralflow_array[idx]
        if self._netinflow_diskflag_reading:
            self.netinflow = self._netinflow_ncarray[0]
        elif self._netinflow_ramflag:
            self.netinflow = self._netinflow_array[idx]
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
        if self._discharges_diskflag_reading:
            k = 0
            for jdx0 in range(self._discharges_length_0):
                self.discharges[jdx0] = self._discharges_ncarray[k]
                k += 1
        elif self._discharges_ramflag:
            for jdx0 in range(self._discharges_length_0):
                self.discharges[jdx0] = self._discharges_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inflow_diskflag_writing:
            self._inflow_ncarray[0] = self.inflow
        if self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._outflow_diskflag_writing:
            self._outflow_ncarray[0] = self.outflow
        if self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
        if self._lateralflow_diskflag_writing:
            self._lateralflow_ncarray[0] = self.lateralflow
        if self._lateralflow_ramflag:
            self._lateralflow_array[idx] = self.lateralflow
        if self._netinflow_diskflag_writing:
            self._netinflow_ncarray[0] = self.netinflow
        if self._netinflow_ramflag:
            self._netinflow_array[idx] = self.netinflow
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
        if self._discharges_diskflag_writing:
            k = 0
            for jdx0 in range(self._discharges_length_0):
                self._discharges_ncarray[k] = self.discharges[jdx0]
                k += 1
        if self._discharges_ramflag:
            for jdx0 in range(self._discharges_length_0):
                self._discharges_array[idx, jdx0] = self.discharges[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
        if name == "lateralflow":
            self._lateralflow_outputpointer = value.p_value
        if name == "netinflow":
            self._netinflow_outputpointer = value.p_value
        if name == "dischargeupstream":
            self._dischargeupstream_outputpointer = value.p_value
        if name == "dischargedownstream":
            self._dischargedownstream_outputpointer = value.p_value
        if name == "dischargevolume":
            self._dischargevolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
        if self._lateralflow_outputflag:
            self._lateralflow_outputpointer[0] = self.lateralflow
        if self._netinflow_outputflag:
            self._netinflow_outputpointer[0] = self.netinflow
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
        if self._watervolume_diskflag_reading:
            self.watervolume = self._watervolume_ncarray[0]
        elif self._watervolume_ramflag:
            self.watervolume = self._watervolume_array[idx]
        if self._discharge_diskflag_reading:
            self.discharge = self._discharge_ncarray[0]
        elif self._discharge_ramflag:
            self.discharge = self._discharge_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._watervolume_diskflag_writing:
            self._watervolume_ncarray[0] = self.watervolume
        if self._watervolume_ramflag:
            self._watervolume_array[idx] = self.watervolume
        if self._discharge_diskflag_writing:
            self._discharge_ncarray[0] = self.discharge
        if self._discharge_ramflag:
            self._discharge_array[idx] = self.discharge
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "watervolume":
            self._watervolume_outputpointer = value.p_value
        if name == "discharge":
            self._discharge_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._watervolume_outputflag:
            self._watervolume_outputpointer[0] = self.watervolume
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
cdef class Model:
    def __init__(self):
        super().__init__()
        self.channelmodels = interfaceutils.SubmodelsProperty()
        self.crosssection = None
        self.crosssection_is_mainmodel = False
        self.routingmodels = interfaceutils.SubmodelsProperty()
        self.routingmodelsdownstream = interfaceutils.SubmodelsProperty()
        self.routingmodelsupstream = interfaceutils.SubmodelsProperty()
        self.storagemodeldownstream = None
        self.storagemodeldownstream_is_mainmodel = False
        self.storagemodels = interfaceutils.SubmodelsProperty()
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
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).reset_reuseflags()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.reset_reuseflags()
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).reset_reuseflags()
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.reset_reuseflags()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).reset_reuseflags()
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).load_data(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.load_data(idx)
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).load_data(idx)
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.load_data(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).load_data(idx)
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        self.sequences.senders.save_data(idx)
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).save_data(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.save_data(idx)
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).save_data(idx)
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.save_data(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).save_data(idx)
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.watervolume = self.sequences.new_states.watervolume
        self.sequences.old_states.discharge = self.sequences.new_states.discharge
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).new2old()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.new2old()
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).new2old()
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.new2old()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).new2old()
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.timeleft = self.parameters.derived.seconds
        while True:
            self.calc_maxtimesteps_v1()
            self.calc_timestep_v1()
            self.send_timestep_v1()
            self.calc_discharges_v1()
            self.update_storages_v1()
            self.query_waterlevels_v1()
            if self.timeleft <= 0.0:
                break
            self.new2old()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).update_inlets()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_inlets()
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_inlets()
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.update_inlets()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_inlets()
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.update_inlets()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._longq_length_0):
                if self.sequences.inlets._longq_ready[i]:
                    self.sequences.inlets.longq[i] = self.sequences.inlets._longq_pointer[i][0]
                else:
                    self.sequences.inlets.longq[i] = nan
        if not self.threading:
            for i in range(self.sequences.inlets._latq_length_0):
                if self.sequences.inlets._latq_ready[i]:
                    self.sequences.inlets.latq[i] = self.sequences.inlets._latq_pointer[i][0]
                else:
                    self.sequences.inlets.latq[i] = nan
        if not self.threading:
            self.sequences.inlets.waterlevel = self.sequences.inlets._waterlevel_pointer[0]
        self.pick_inflow_v1()
        self.pick_outflow_v1()
        self.pick_lateralflow_v1()
        self.pick_waterleveldownstream_v1()
    cpdef void update_outlets(self) noexcept nogil:
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).update_outlets()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outlets()
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_outlets()
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.update_outlets()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_outlets()
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.update_outlets()
        self.pass_discharge_v1()
        self.pass_waterlevel_v1()
        self.calc_discharges_v2()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.outlets._longq_length_0):
                if self.sequences.outlets._longq_ready[i]:
                    self.sequences.outlets._longq_pointer[i][0] = self.sequences.outlets._longq_pointer[i][0] + self.sequences.outlets.longq[i]
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).update_receivers(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_receivers(idx)
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_receivers(idx)
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.update_receivers(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_receivers(idx)
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).update_senders(idx)
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_senders(idx)
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_senders(idx)
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.update_senders(idx)
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_senders(idx)
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.update_senders(idx)
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
        cdef numpy.int64_t i_submodel
        for i_submodel in range(self.channelmodels.number):
            if self.channelmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.channelmodels.submodels[i_submodel]).update_outputs()
        if (self.crosssection is not None) and not self.crosssection_is_mainmodel:
            self.crosssection.update_outputs()
        for i_submodel in range(self.routingmodels.number):
            if self.routingmodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.routingmodels.submodels[i_submodel]).update_outputs()
        if (self.storagemodeldownstream is not None) and not self.storagemodeldownstream_is_mainmodel:
            self.storagemodeldownstream.update_outputs()
        for i_submodel in range(self.storagemodels.number):
            if self.storagemodels.typeids[i_submodel] > 0:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i_submodel]).update_outputs()
        if (self.storagemodelupstream is not None) and not self.storagemodelupstream_is_mainmodel:
            self.storagemodelupstream.update_outputs()
    cpdef inline void pick_inflow_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.inflow = 0.0
        for i in range(self.sequences.inlets.len_longq):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.longq[i])
    cpdef inline void pick_outflow_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.outflow = 0.0
        for i in range(self.sequences.inlets.len_longq):
            self.sequences.fluxes.outflow = self.sequences.fluxes.outflow + (self.sequences.inlets.longq[i])
    cpdef inline void pick_lateralflow_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.lateralflow = 0.0
        for i in range(self.sequences.inlets.len_latq):
            self.sequences.fluxes.lateralflow = self.sequences.fluxes.lateralflow + (self.sequences.inlets.latq[i])
    cpdef inline void pick_waterleveldownstream_v1(self) noexcept nogil:
        self.sequences.factors.waterleveldownstream = self.sequences.inlets.waterlevel
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
    cpdef inline void query_waterlevels_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                self.sequences.factors.waterlevels[i] = (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).get_waterlevel()
    cpdef void determine_discharge_v2(self) noexcept nogil:
        self.sequences.states.discharge = self.sequences.fluxes.inflow
    cpdef void determine_discharge_v4(self) noexcept nogil:
        self.sequences.states.discharge = self.sequences.fluxes.outflow
    cpdef double get_watervolume_v1(self) noexcept nogil:
        return self.sequences.states.watervolume
    cpdef double get_waterlevel_v1(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef double get_discharge_v1(self) noexcept nogil:
        return self.sequences.states.discharge
    cpdef double get_dischargevolume_v1(self) noexcept nogil:
        return self.sequences.fluxes.dischargevolume
    cpdef double get_maxtimestep_v1(self) noexcept nogil:
        return self.sequences.factors.maxtimestep
    cpdef void set_timestep_v1(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
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
    cpdef inline void calc_maxtimestep_v1(self) noexcept nogil:
        if self.sequences.factors.waterdepth > 0.0:
            self.sequences.factors.maxtimestep = (self.parameters.control.timestepfactor * 1000.0 * self.parameters.derived.lengthmin) / (                self.parameters.fixed.gravitationalacceleration * self.sequences.factors.waterdepth            ) ** 0.5
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_maxtimestep_v2(self) noexcept nogil:
        cdef double cel
        if (self.sequences.fluxes.inflow != 0.0) and (self.sequences.factors.wettedarea > 0.0):
            cel = fabs(5.0 / 3.0 * self.sequences.fluxes.inflow / self.sequences.factors.wettedarea)
            self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.control.lengthdownstream / cel
        else:
            self.sequences.factors.maxtimestep = inf
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
    cpdef inline void calc_maxtimestep_v4(self) noexcept nogil:
        cdef double cel
        if (self.sequences.fluxes.outflow != 0.0) and (self.sequences.factors.wettedarea > 0.0):
            cel = fabs(5.0 / 3.0 * self.sequences.fluxes.outflow / self.sequences.factors.wettedarea)
            self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.control.lengthupstream / cel
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_maxtimestep_v5(self) noexcept nogil:
        cdef double cel
        cdef double ld
        cdef double lu
        cdef double g
        cdef double c
        cdef double h
        self.parameters.control.gateheight_callback(self)
        h = min(self.parameters.control.gateheight, self.sequences.factors.waterlevel) - self.parameters.control.bottomlevel
        if h > 0.0:
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            lu = self.sequences.factors.waterlevelupstream
            ld = self.sequences.factors.waterleveldownstream
            cel = c * h * (2.0 * g * fabs(lu - ld)) ** 0.5
            if cel == 0.0:
                self.sequences.factors.maxtimestep = inf
            else:
                self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.control.lengthupstream / cel
        else:
            self.sequences.factors.maxtimestep = inf
    cpdef inline void calc_maxtimestep_v6(self) noexcept nogil:
        cdef double cel
        if (self.sequences.states.discharge != 0.0) and (self.sequences.factors.wettedarea > 0.0):
            cel = fabs(5.0 / 3.0 * self.sequences.states.discharge / self.sequences.factors.wettedarea)
            self.sequences.factors.maxtimestep = self.parameters.control.timestepfactor * 1000.0 * self.parameters.derived.lengthmin / cel
        else:
            self.sequences.factors.maxtimestep = inf
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
    cpdef inline void calc_waterlevel_v2(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterleveldownstream
    cpdef inline void calc_waterlevel_v3(self) noexcept nogil:
        self.sequences.factors.waterlevel = self.sequences.factors.waterlevelupstream
    cpdef inline void calc_waterlevel_v4(self) noexcept nogil:
        self.sequences.factors.waterlevel = (self.sequences.factors.waterlevelupstream + self.sequences.factors.waterleveldownstream) / 2.0
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_wettedarea(self.sequences.states.watervolume / self.parameters.control.length)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.waterlevel = submodel.get_waterlevel()
    cpdef inline void calc_waterdepth_waterlevel_v1(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_waterlevel_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_waterdepth_wettedarea_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
    cpdef inline void calc_waterdepth_wettedarea_v1(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
        self.sequences.factors.wettedperimeter = submodel.get_wettedperimeter()
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_v1(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
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
    cpdef inline void calc_discharge_v3(self) noexcept nogil:
        cdef double ld
        cdef double lu
        cdef double g
        cdef double c
        cdef double w
        cdef double h
        self.parameters.control.gateheight_callback(self)
        h = min(self.parameters.control.gateheight, self.sequences.factors.waterlevel) - self.parameters.control.bottomlevel
        if h > 0.0:
            w = self.parameters.control.gatewidth
            c = self.parameters.control.flowcoefficient
            g = self.parameters.fixed.gravitationalacceleration
            lu = self.sequences.factors.waterlevelupstream
            ld = self.sequences.factors.waterleveldownstream
            if ld < lu:
                self.sequences.states.discharge = w * c * h * (2.0 * g * (lu - ld)) ** 0.5
            else:
                self.sequences.states.discharge = -w * c * h * (2.0 * g * (ld - lu)) ** 0.5
            self.sequences.states.discharge = self.sequences.states.discharge * (1.0 - smoothutils.filter_norm(lu, ld, self.parameters.control.dampingradius))
        else:
            self.sequences.states.discharge = 0.0
    cpdef inline void calc_discharge_v4(self) noexcept nogil:
        cdef double t2
        cdef double t1
        cdef double hd
        cdef double hu
        hu = self.sequences.factors.waterlevelupstream
        hd = self.sequences.factors.waterleveldownstream
        t1 = self.parameters.control.targetwaterlevel1
        t2 = self.parameters.control.targetwaterlevel2
        if hu < t1:
            self.sequences.states.discharge = 0.0
        else:
            self.parameters.control.gradient2pumpingrate.inputs[0] = hu - hd
            self.parameters.control.gradient2pumpingrate.calculate_values()
            self.sequences.states.discharge = max(self.parameters.control.gradient2pumpingrate.outputs[0], 0.0)
            if hu < t2:
                self.sequences.states.discharge = self.sequences.states.discharge * ((hu - t1) / (t2 - t1))
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
    cpdef inline void reset_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = 0.0
    cpdef inline void update_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.sequences.fluxes.dischargevolume + (self.sequences.factors.timestep * self.sequences.states.discharge)
    cpdef inline void calc_dischargevolume_v1(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.parameters.derived.seconds * self.sequences.fluxes.inflow
    cpdef inline void calc_dischargevolume_v2(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.parameters.derived.seconds * self.sequences.fluxes.outflow
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
    cpdef inline void pass_discharge_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        cdef double discharge
        discharge = self.sequences.fluxes.dischargevolume / self.parameters.derived.seconds
        for i in range(self.sequences.outlets.len_longq):
            self.sequences.outlets.longq[i] = discharge
    cpdef inline void pass_waterlevel_v1(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.sequences.senders.len_waterlevel):
            self.sequences.senders.waterlevel[i] = self.sequences.factors.waterlevel
    cpdef inline void calc_discharges_v2(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.routingmodels.number):
            if self.routingmodels.typeids[i] in (1, 2, 3):
                self.sequences.fluxes.discharges[i] = (                    (<masterinterface.MasterInterface>self.routingmodels.submodels[i]).get_dischargevolume()                    / self.parameters.derived.seconds                )
            else:
                self.sequences.fluxes.discharges[i] = 0.0
    cpdef inline void pick_inflow(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.inflow = 0.0
        for i in range(self.sequences.inlets.len_longq):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow + (self.sequences.inlets.longq[i])
    cpdef inline void pick_outflow(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.outflow = 0.0
        for i in range(self.sequences.inlets.len_longq):
            self.sequences.fluxes.outflow = self.sequences.fluxes.outflow + (self.sequences.inlets.longq[i])
    cpdef inline void pick_lateralflow(self) noexcept nogil:
        cdef numpy.int64_t i
        self.sequences.fluxes.lateralflow = 0.0
        for i in range(self.sequences.inlets.len_latq):
            self.sequences.fluxes.lateralflow = self.sequences.fluxes.lateralflow + (self.sequences.inlets.latq[i])
    cpdef inline void pick_waterleveldownstream(self) noexcept nogil:
        self.sequences.factors.waterleveldownstream = self.sequences.inlets.waterlevel
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
    cpdef inline void update_storages(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).update_storage()
    cpdef inline void query_waterlevels(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.storagemodels.number):
            if self.storagemodels.typeids[i] == 1:
                self.sequences.factors.waterlevels[i] = (<masterinterface.MasterInterface>self.storagemodels.submodels[i]).get_waterlevel()
    cpdef double get_watervolume(self) noexcept nogil:
        return self.sequences.states.watervolume
    cpdef double get_waterlevel(self) noexcept nogil:
        return self.sequences.factors.waterlevel
    cpdef double get_discharge(self) noexcept nogil:
        return self.sequences.states.discharge
    cpdef double get_dischargevolume(self) noexcept nogil:
        return self.sequences.fluxes.dischargevolume
    cpdef double get_maxtimestep(self) noexcept nogil:
        return self.sequences.factors.maxtimestep
    cpdef void set_timestep(self, double timestep) noexcept nogil:
        self.sequences.factors.timestep = timestep
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
    cpdef inline void calc_waterdepth_waterlevel_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_wettedarea(self.sequences.states.watervolume / self.parameters.control.length)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.waterlevel = submodel.get_waterlevel()
    cpdef inline void calc_waterdepth_waterlevel(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_waterlevel_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_waterdepth_wettedarea_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
    cpdef inline void calc_waterdepth_wettedarea(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.use_waterlevel(self.sequences.factors.waterlevel)
        self.sequences.factors.waterdepth = submodel.get_waterdepth()
        self.sequences.factors.wettedarea = submodel.get_wettedarea()
        self.sequences.factors.wettedperimeter = submodel.get_wettedperimeter()
    cpdef inline void calc_waterdepth_wettedarea_wettedperimeter(self) noexcept nogil:
        if self.crosssection_typeid == 2:
            self.calc_waterdepth_wettedarea_wettedperimeter_crosssectionmodel_v2(                (<masterinterface.MasterInterface>self.crosssection)            )
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
    cpdef inline void reset_dischargevolume(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = 0.0
    cpdef inline void update_dischargevolume(self) noexcept nogil:
        self.sequences.fluxes.dischargevolume = self.sequences.fluxes.dischargevolume + (self.sequences.factors.timestep * self.sequences.states.discharge)
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
    cpdef inline void pass_discharge(self) noexcept nogil:
        cdef numpy.int64_t i
        cdef double discharge
        discharge = self.sequences.fluxes.dischargevolume / self.parameters.derived.seconds
        for i in range(self.sequences.outlets.len_longq):
            self.sequences.outlets.longq[i] = discharge
    cpdef inline void pass_waterlevel(self) noexcept nogil:
        cdef numpy.int64_t i
        for i in range(self.sequences.senders.len_waterlevel):
            self.sequences.senders.waterlevel[i] = self.sequences.factors.waterlevel
    cpdef void determine_maxtimestep_v1(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterleveldownstream_v1()
        self.calc_waterlevel_v1()
        self.calc_waterdepth_wettedarea_wettedperimeter_v1()
        self.calc_dischargeupstream_v1()
        self.calc_dischargedownstream_v1()
        self.calc_maxtimestep_v1()
    cpdef void determine_maxtimestep_v2(self) noexcept nogil:
        self.calc_waterleveldownstream_v1()
        self.calc_waterlevel_v2()
        self.calc_waterdepth_wettedarea_v1()
        self.calc_maxtimestep_v2()
    cpdef void determine_maxtimestep_v3(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterlevel_v3()
        self.calc_maxtimestep_v3()
    cpdef void determine_maxtimestep_v4(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterlevel_v3()
        self.calc_waterdepth_wettedarea_v1()
        self.calc_maxtimestep_v4()
    cpdef void determine_maxtimestep_v5(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterlevel_v4()
        self.calc_maxtimestep_v5()
    cpdef void determine_maxtimestep_v6(self) noexcept nogil:
        self.calc_waterlevelupstream_v1()
        self.calc_waterleveldownstream_v1()
        self.calc_waterlevel_v1()
        self.calc_waterdepth_wettedarea_v1()
        self.calc_maxtimestep_v6()
    cpdef void determine_discharge_v1(self) noexcept nogil:
        self.calc_watervolumeupstream_v1()
        self.calc_watervolumedownstream_v1()
        self.calc_discharge_v1()
        self.update_discharge_v1()
        self.update_dischargevolume_v1()
    cpdef void determine_discharge_v3(self) noexcept nogil:
        self.calc_discharge_v2()
        self.update_dischargevolume_v1()
    cpdef void determine_discharge_v5(self) noexcept nogil:
        self.calc_watervolumeupstream_v1()
        self.calc_watervolumedownstream_v1()
        self.calc_discharge_v1()
        self.update_discharge_v1()
        self.update_discharge_v2()
        self.update_dischargevolume_v1()
    cpdef void determine_discharge_v6(self) noexcept nogil:
        self.calc_discharge_v3()
        self.update_dischargevolume_v1()
    cpdef void determine_discharge_v7(self) noexcept nogil:
        self.calc_waterlevel_v3()
        self.calc_discharge_v4()
        self.update_dischargevolume_v1()
    cpdef void update_storage_v1(self) noexcept nogil:
        self.calc_netinflow_v1()
        self.update_watervolume_v1()
        self.calc_waterdepth_waterlevel_v1()
    cpdef void update_storage(self) noexcept nogil:
        self.calc_netinflow_v1()
        self.update_watervolume_v1()
        self.calc_waterdepth_waterlevel_v1()
