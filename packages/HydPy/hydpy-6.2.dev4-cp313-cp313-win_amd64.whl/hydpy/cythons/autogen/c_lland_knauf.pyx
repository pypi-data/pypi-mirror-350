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
cdef public numpy.int64_t SIED_D = 1
cdef public numpy.int64_t SIED_L = 2
cdef public numpy.int64_t VERS = 3
cdef public numpy.int64_t ACKER = 4
cdef public numpy.int64_t WEINB = 5
cdef public numpy.int64_t OBSTB = 6
cdef public numpy.int64_t BODEN = 7
cdef public numpy.int64_t GLETS = 8
cdef public numpy.int64_t GRUE_I = 9
cdef public numpy.int64_t FEUCHT = 10
cdef public numpy.int64_t GRUE_E = 11
cdef public numpy.int64_t BAUMB = 12
cdef public numpy.int64_t NADELW = 13
cdef public numpy.int64_t LAUBW = 14
cdef public numpy.int64_t MISCHW = 15
cdef public numpy.int64_t WASSER = 16
cdef public numpy.int64_t FLUSS = 17
cdef public numpy.int64_t SEE = 18
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
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._nied_inputflag:
            self.nied = self._nied_inputpointer[0]
        elif self._nied_diskflag_reading:
            self.nied = self._nied_ncarray[0]
        elif self._nied_ramflag:
            self.nied = self._nied_array[idx]
        if self._teml_inputflag:
            self.teml = self._teml_inputpointer[0]
        elif self._teml_diskflag_reading:
            self.teml = self._teml_ncarray[0]
        elif self._teml_ramflag:
            self.teml = self._teml_array[idx]
        if self._relativehumidity_inputflag:
            self.relativehumidity = self._relativehumidity_inputpointer[0]
        elif self._relativehumidity_diskflag_reading:
            self.relativehumidity = self._relativehumidity_ncarray[0]
        elif self._relativehumidity_ramflag:
            self.relativehumidity = self._relativehumidity_array[idx]
        if self._windspeed_inputflag:
            self.windspeed = self._windspeed_inputpointer[0]
        elif self._windspeed_diskflag_reading:
            self.windspeed = self._windspeed_ncarray[0]
        elif self._windspeed_ramflag:
            self.windspeed = self._windspeed_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._nied_diskflag_writing:
            self._nied_ncarray[0] = self.nied
        if self._nied_ramflag:
            self._nied_array[idx] = self.nied
        if self._teml_diskflag_writing:
            self._teml_ncarray[0] = self.teml
        if self._teml_ramflag:
            self._teml_array[idx] = self.teml
        if self._relativehumidity_diskflag_writing:
            self._relativehumidity_ncarray[0] = self.relativehumidity
        if self._relativehumidity_ramflag:
            self._relativehumidity_array[idx] = self.relativehumidity
        if self._windspeed_diskflag_writing:
            self._windspeed_ncarray[0] = self.windspeed
        if self._windspeed_ramflag:
            self._windspeed_array[idx] = self.windspeed
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "nied":
            self._nied_inputpointer = value.p_value
        if name == "teml":
            self._teml_inputpointer = value.p_value
        if name == "relativehumidity":
            self._relativehumidity_inputpointer = value.p_value
        if name == "windspeed":
            self._windspeed_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._possiblesunshineduration_diskflag_reading:
            self.possiblesunshineduration = self._possiblesunshineduration_ncarray[0]
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._sunshineduration_diskflag_reading:
            self.sunshineduration = self._sunshineduration_ncarray[0]
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._possiblesunshineduration_diskflag_writing:
            self._possiblesunshineduration_ncarray[0] = self.possiblesunshineduration
        if self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._sunshineduration_diskflag_writing:
            self._sunshineduration_ncarray[0] = self.sunshineduration
        if self._sunshineduration_ramflag:
            self._sunshineduration_array[idx] = self.sunshineduration
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._sunshineduration_outputflag:
            self._sunshineduration_outputpointer[0] = self.sunshineduration
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qz_diskflag_reading:
            self.qz = self._qz_ncarray[0]
        elif self._qz_ramflag:
            self.qz = self._qz_array[idx]
        if self._qzh_diskflag_reading:
            self.qzh = self._qzh_ncarray[0]
        elif self._qzh_ramflag:
            self.qzh = self._qzh_array[idx]
        if self._dailysunshineduration_diskflag_reading:
            self.dailysunshineduration = self._dailysunshineduration_ncarray[0]
        elif self._dailysunshineduration_ramflag:
            self.dailysunshineduration = self._dailysunshineduration_array[idx]
        if self._dailypossiblesunshineduration_diskflag_reading:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_ncarray[0]
        elif self._dailypossiblesunshineduration_ramflag:
            self.dailypossiblesunshineduration = self._dailypossiblesunshineduration_array[idx]
        if self._globalradiation_diskflag_reading:
            self.globalradiation = self._globalradiation_ncarray[0]
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._nkor_diskflag_reading:
            k = 0
            for jdx0 in range(self._nkor_length_0):
                self.nkor[jdx0] = self._nkor_ncarray[k]
                k += 1
        elif self._nkor_ramflag:
            for jdx0 in range(self._nkor_length_0):
                self.nkor[jdx0] = self._nkor_array[idx, jdx0]
        if self._tkor_diskflag_reading:
            k = 0
            for jdx0 in range(self._tkor_length_0):
                self.tkor[jdx0] = self._tkor_ncarray[k]
                k += 1
        elif self._tkor_ramflag:
            for jdx0 in range(self._tkor_length_0):
                self.tkor[jdx0] = self._tkor_array[idx, jdx0]
        if self._windspeed2m_diskflag_reading:
            self.windspeed2m = self._windspeed2m_ncarray[0]
        elif self._windspeed2m_ramflag:
            self.windspeed2m = self._windspeed2m_array[idx]
        if self._reducedwindspeed2m_diskflag_reading:
            k = 0
            for jdx0 in range(self._reducedwindspeed2m_length_0):
                self.reducedwindspeed2m[jdx0] = self._reducedwindspeed2m_ncarray[k]
                k += 1
        elif self._reducedwindspeed2m_ramflag:
            for jdx0 in range(self._reducedwindspeed2m_length_0):
                self.reducedwindspeed2m[jdx0] = self._reducedwindspeed2m_array[idx, jdx0]
        if self._saturationvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_ncarray[k]
                k += 1
        elif self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self.saturationvapourpressure[jdx0] = self._saturationvapourpressure_array[idx, jdx0]
        if self._saturationvapourpressuresnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._saturationvapourpressuresnow_length_0):
                self.saturationvapourpressuresnow[jdx0] = self._saturationvapourpressuresnow_ncarray[k]
                k += 1
        elif self._saturationvapourpressuresnow_ramflag:
            for jdx0 in range(self._saturationvapourpressuresnow_length_0):
                self.saturationvapourpressuresnow[jdx0] = self._saturationvapourpressuresnow_array[idx, jdx0]
        if self._actualvapourpressure_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_ncarray[k]
                k += 1
        elif self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self.actualvapourpressure[jdx0] = self._actualvapourpressure_array[idx, jdx0]
        if self._tz_diskflag_reading:
            k = 0
            for jdx0 in range(self._tz_length_0):
                self.tz[jdx0] = self._tz_ncarray[k]
                k += 1
        elif self._tz_ramflag:
            for jdx0 in range(self._tz_length_0):
                self.tz[jdx0] = self._tz_array[idx, jdx0]
        if self._wg_diskflag_reading:
            k = 0
            for jdx0 in range(self._wg_length_0):
                self.wg[jdx0] = self._wg_ncarray[k]
                k += 1
        elif self._wg_ramflag:
            for jdx0 in range(self._wg_length_0):
                self.wg[jdx0] = self._wg_array[idx, jdx0]
        if self._netshortwaveradiationsnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._netshortwaveradiationsnow_length_0):
                self.netshortwaveradiationsnow[jdx0] = self._netshortwaveradiationsnow_ncarray[k]
                k += 1
        elif self._netshortwaveradiationsnow_ramflag:
            for jdx0 in range(self._netshortwaveradiationsnow_length_0):
                self.netshortwaveradiationsnow[jdx0] = self._netshortwaveradiationsnow_array[idx, jdx0]
        if self._netlongwaveradiationsnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._netlongwaveradiationsnow_length_0):
                self.netlongwaveradiationsnow[jdx0] = self._netlongwaveradiationsnow_ncarray[k]
                k += 1
        elif self._netlongwaveradiationsnow_ramflag:
            for jdx0 in range(self._netlongwaveradiationsnow_length_0):
                self.netlongwaveradiationsnow[jdx0] = self._netlongwaveradiationsnow_array[idx, jdx0]
        if self._netradiationsnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._netradiationsnow_length_0):
                self.netradiationsnow[jdx0] = self._netradiationsnow_ncarray[k]
                k += 1
        elif self._netradiationsnow_ramflag:
            for jdx0 in range(self._netradiationsnow_length_0):
                self.netradiationsnow[jdx0] = self._netradiationsnow_array[idx, jdx0]
        if self._nbes_diskflag_reading:
            k = 0
            for jdx0 in range(self._nbes_length_0):
                self.nbes[jdx0] = self._nbes_ncarray[k]
                k += 1
        elif self._nbes_ramflag:
            for jdx0 in range(self._nbes_length_0):
                self.nbes[jdx0] = self._nbes_array[idx, jdx0]
        if self._sbes_diskflag_reading:
            k = 0
            for jdx0 in range(self._sbes_length_0):
                self.sbes[jdx0] = self._sbes_ncarray[k]
                k += 1
        elif self._sbes_ramflag:
            for jdx0 in range(self._sbes_length_0):
                self.sbes[jdx0] = self._sbes_array[idx, jdx0]
        if self._evi_diskflag_reading:
            k = 0
            for jdx0 in range(self._evi_length_0):
                self.evi[jdx0] = self._evi_ncarray[k]
                k += 1
        elif self._evi_ramflag:
            for jdx0 in range(self._evi_length_0):
                self.evi[jdx0] = self._evi_array[idx, jdx0]
        if self._evb_diskflag_reading:
            k = 0
            for jdx0 in range(self._evb_length_0):
                self.evb[jdx0] = self._evb_ncarray[k]
                k += 1
        elif self._evb_ramflag:
            for jdx0 in range(self._evb_length_0):
                self.evb[jdx0] = self._evb_array[idx, jdx0]
        if self._evs_diskflag_reading:
            k = 0
            for jdx0 in range(self._evs_length_0):
                self.evs[jdx0] = self._evs_ncarray[k]
                k += 1
        elif self._evs_ramflag:
            for jdx0 in range(self._evs_length_0):
                self.evs[jdx0] = self._evs_array[idx, jdx0]
        if self._wnied_diskflag_reading:
            k = 0
            for jdx0 in range(self._wnied_length_0):
                self.wnied[jdx0] = self._wnied_ncarray[k]
                k += 1
        elif self._wnied_ramflag:
            for jdx0 in range(self._wnied_length_0):
                self.wnied[jdx0] = self._wnied_array[idx, jdx0]
        if self._tempssurface_diskflag_reading:
            k = 0
            for jdx0 in range(self._tempssurface_length_0):
                self.tempssurface[jdx0] = self._tempssurface_ncarray[k]
                k += 1
        elif self._tempssurface_ramflag:
            for jdx0 in range(self._tempssurface_length_0):
                self.tempssurface[jdx0] = self._tempssurface_array[idx, jdx0]
        if self._actualalbedo_diskflag_reading:
            k = 0
            for jdx0 in range(self._actualalbedo_length_0):
                self.actualalbedo[jdx0] = self._actualalbedo_ncarray[k]
                k += 1
        elif self._actualalbedo_ramflag:
            for jdx0 in range(self._actualalbedo_length_0):
                self.actualalbedo[jdx0] = self._actualalbedo_array[idx, jdx0]
        if self._schmpot_diskflag_reading:
            k = 0
            for jdx0 in range(self._schmpot_length_0):
                self.schmpot[jdx0] = self._schmpot_ncarray[k]
                k += 1
        elif self._schmpot_ramflag:
            for jdx0 in range(self._schmpot_length_0):
                self.schmpot[jdx0] = self._schmpot_array[idx, jdx0]
        if self._schm_diskflag_reading:
            k = 0
            for jdx0 in range(self._schm_length_0):
                self.schm[jdx0] = self._schm_ncarray[k]
                k += 1
        elif self._schm_ramflag:
            for jdx0 in range(self._schm_length_0):
                self.schm[jdx0] = self._schm_array[idx, jdx0]
        if self._gefrpot_diskflag_reading:
            k = 0
            for jdx0 in range(self._gefrpot_length_0):
                self.gefrpot[jdx0] = self._gefrpot_ncarray[k]
                k += 1
        elif self._gefrpot_ramflag:
            for jdx0 in range(self._gefrpot_length_0):
                self.gefrpot[jdx0] = self._gefrpot_array[idx, jdx0]
        if self._gefr_diskflag_reading:
            k = 0
            for jdx0 in range(self._gefr_length_0):
                self.gefr[jdx0] = self._gefr_ncarray[k]
                k += 1
        elif self._gefr_ramflag:
            for jdx0 in range(self._gefr_length_0):
                self.gefr[jdx0] = self._gefr_array[idx, jdx0]
        if self._wlatsnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._wlatsnow_length_0):
                self.wlatsnow[jdx0] = self._wlatsnow_ncarray[k]
                k += 1
        elif self._wlatsnow_ramflag:
            for jdx0 in range(self._wlatsnow_length_0):
                self.wlatsnow[jdx0] = self._wlatsnow_array[idx, jdx0]
        if self._wsenssnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._wsenssnow_length_0):
                self.wsenssnow[jdx0] = self._wsenssnow_ncarray[k]
                k += 1
        elif self._wsenssnow_ramflag:
            for jdx0 in range(self._wsenssnow_length_0):
                self.wsenssnow[jdx0] = self._wsenssnow_array[idx, jdx0]
        if self._wsurf_diskflag_reading:
            k = 0
            for jdx0 in range(self._wsurf_length_0):
                self.wsurf[jdx0] = self._wsurf_ncarray[k]
                k += 1
        elif self._wsurf_ramflag:
            for jdx0 in range(self._wsurf_length_0):
                self.wsurf[jdx0] = self._wsurf_array[idx, jdx0]
        if self._sff_diskflag_reading:
            k = 0
            for jdx0 in range(self._sff_length_0):
                self.sff[jdx0] = self._sff_ncarray[k]
                k += 1
        elif self._sff_ramflag:
            for jdx0 in range(self._sff_length_0):
                self.sff[jdx0] = self._sff_array[idx, jdx0]
        if self._fvg_diskflag_reading:
            k = 0
            for jdx0 in range(self._fvg_length_0):
                self.fvg[jdx0] = self._fvg_ncarray[k]
                k += 1
        elif self._fvg_ramflag:
            for jdx0 in range(self._fvg_length_0):
                self.fvg[jdx0] = self._fvg_array[idx, jdx0]
        if self._wada_diskflag_reading:
            k = 0
            for jdx0 in range(self._wada_length_0):
                self.wada[jdx0] = self._wada_ncarray[k]
                k += 1
        elif self._wada_ramflag:
            for jdx0 in range(self._wada_length_0):
                self.wada[jdx0] = self._wada_array[idx, jdx0]
        if self._qdb_diskflag_reading:
            k = 0
            for jdx0 in range(self._qdb_length_0):
                self.qdb[jdx0] = self._qdb_ncarray[k]
                k += 1
        elif self._qdb_ramflag:
            for jdx0 in range(self._qdb_length_0):
                self.qdb[jdx0] = self._qdb_array[idx, jdx0]
        if self._qib1_diskflag_reading:
            k = 0
            for jdx0 in range(self._qib1_length_0):
                self.qib1[jdx0] = self._qib1_ncarray[k]
                k += 1
        elif self._qib1_ramflag:
            for jdx0 in range(self._qib1_length_0):
                self.qib1[jdx0] = self._qib1_array[idx, jdx0]
        if self._qib2_diskflag_reading:
            k = 0
            for jdx0 in range(self._qib2_length_0):
                self.qib2[jdx0] = self._qib2_ncarray[k]
                k += 1
        elif self._qib2_ramflag:
            for jdx0 in range(self._qib2_length_0):
                self.qib2[jdx0] = self._qib2_array[idx, jdx0]
        if self._qbb_diskflag_reading:
            k = 0
            for jdx0 in range(self._qbb_length_0):
                self.qbb[jdx0] = self._qbb_ncarray[k]
                k += 1
        elif self._qbb_ramflag:
            for jdx0 in range(self._qbb_length_0):
                self.qbb[jdx0] = self._qbb_array[idx, jdx0]
        if self._qkap_diskflag_reading:
            k = 0
            for jdx0 in range(self._qkap_length_0):
                self.qkap[jdx0] = self._qkap_ncarray[k]
                k += 1
        elif self._qkap_ramflag:
            for jdx0 in range(self._qkap_length_0):
                self.qkap[jdx0] = self._qkap_array[idx, jdx0]
        if self._qdgz_diskflag_reading:
            self.qdgz = self._qdgz_ncarray[0]
        elif self._qdgz_ramflag:
            self.qdgz = self._qdgz_array[idx]
        if self._qdgz1_diskflag_reading:
            self.qdgz1 = self._qdgz1_ncarray[0]
        elif self._qdgz1_ramflag:
            self.qdgz1 = self._qdgz1_array[idx]
        if self._qdgz2_diskflag_reading:
            self.qdgz2 = self._qdgz2_ncarray[0]
        elif self._qdgz2_ramflag:
            self.qdgz2 = self._qdgz2_array[idx]
        if self._qigz1_diskflag_reading:
            self.qigz1 = self._qigz1_ncarray[0]
        elif self._qigz1_ramflag:
            self.qigz1 = self._qigz1_array[idx]
        if self._qigz2_diskflag_reading:
            self.qigz2 = self._qigz2_ncarray[0]
        elif self._qigz2_ramflag:
            self.qigz2 = self._qigz2_array[idx]
        if self._qbgz_diskflag_reading:
            self.qbgz = self._qbgz_ncarray[0]
        elif self._qbgz_ramflag:
            self.qbgz = self._qbgz_array[idx]
        if self._qdga1_diskflag_reading:
            self.qdga1 = self._qdga1_ncarray[0]
        elif self._qdga1_ramflag:
            self.qdga1 = self._qdga1_array[idx]
        if self._qdga2_diskflag_reading:
            self.qdga2 = self._qdga2_ncarray[0]
        elif self._qdga2_ramflag:
            self.qdga2 = self._qdga2_array[idx]
        if self._qiga1_diskflag_reading:
            self.qiga1 = self._qiga1_ncarray[0]
        elif self._qiga1_ramflag:
            self.qiga1 = self._qiga1_array[idx]
        if self._qiga2_diskflag_reading:
            self.qiga2 = self._qiga2_ncarray[0]
        elif self._qiga2_ramflag:
            self.qiga2 = self._qiga2_array[idx]
        if self._qbga_diskflag_reading:
            self.qbga = self._qbga_ncarray[0]
        elif self._qbga_ramflag:
            self.qbga = self._qbga_array[idx]
        if self._qah_diskflag_reading:
            self.qah = self._qah_ncarray[0]
        elif self._qah_ramflag:
            self.qah = self._qah_array[idx]
        if self._qa_diskflag_reading:
            self.qa = self._qa_ncarray[0]
        elif self._qa_ramflag:
            self.qa = self._qa_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qz_diskflag_writing:
            self._qz_ncarray[0] = self.qz
        if self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qzh_diskflag_writing:
            self._qzh_ncarray[0] = self.qzh
        if self._qzh_ramflag:
            self._qzh_array[idx] = self.qzh
        if self._dailysunshineduration_diskflag_writing:
            self._dailysunshineduration_ncarray[0] = self.dailysunshineduration
        if self._dailysunshineduration_ramflag:
            self._dailysunshineduration_array[idx] = self.dailysunshineduration
        if self._dailypossiblesunshineduration_diskflag_writing:
            self._dailypossiblesunshineduration_ncarray[0] = self.dailypossiblesunshineduration
        if self._dailypossiblesunshineduration_ramflag:
            self._dailypossiblesunshineduration_array[idx] = self.dailypossiblesunshineduration
        if self._globalradiation_diskflag_writing:
            self._globalradiation_ncarray[0] = self.globalradiation
        if self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._nkor_diskflag_writing:
            k = 0
            for jdx0 in range(self._nkor_length_0):
                self._nkor_ncarray[k] = self.nkor[jdx0]
                k += 1
        if self._nkor_ramflag:
            for jdx0 in range(self._nkor_length_0):
                self._nkor_array[idx, jdx0] = self.nkor[jdx0]
        if self._tkor_diskflag_writing:
            k = 0
            for jdx0 in range(self._tkor_length_0):
                self._tkor_ncarray[k] = self.tkor[jdx0]
                k += 1
        if self._tkor_ramflag:
            for jdx0 in range(self._tkor_length_0):
                self._tkor_array[idx, jdx0] = self.tkor[jdx0]
        if self._windspeed2m_diskflag_writing:
            self._windspeed2m_ncarray[0] = self.windspeed2m
        if self._windspeed2m_ramflag:
            self._windspeed2m_array[idx] = self.windspeed2m
        if self._reducedwindspeed2m_diskflag_writing:
            k = 0
            for jdx0 in range(self._reducedwindspeed2m_length_0):
                self._reducedwindspeed2m_ncarray[k] = self.reducedwindspeed2m[jdx0]
                k += 1
        if self._reducedwindspeed2m_ramflag:
            for jdx0 in range(self._reducedwindspeed2m_length_0):
                self._reducedwindspeed2m_array[idx, jdx0] = self.reducedwindspeed2m[jdx0]
        if self._saturationvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_ncarray[k] = self.saturationvapourpressure[jdx0]
                k += 1
        if self._saturationvapourpressure_ramflag:
            for jdx0 in range(self._saturationvapourpressure_length_0):
                self._saturationvapourpressure_array[idx, jdx0] = self.saturationvapourpressure[jdx0]
        if self._saturationvapourpressuresnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._saturationvapourpressuresnow_length_0):
                self._saturationvapourpressuresnow_ncarray[k] = self.saturationvapourpressuresnow[jdx0]
                k += 1
        if self._saturationvapourpressuresnow_ramflag:
            for jdx0 in range(self._saturationvapourpressuresnow_length_0):
                self._saturationvapourpressuresnow_array[idx, jdx0] = self.saturationvapourpressuresnow[jdx0]
        if self._actualvapourpressure_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_ncarray[k] = self.actualvapourpressure[jdx0]
                k += 1
        if self._actualvapourpressure_ramflag:
            for jdx0 in range(self._actualvapourpressure_length_0):
                self._actualvapourpressure_array[idx, jdx0] = self.actualvapourpressure[jdx0]
        if self._tz_diskflag_writing:
            k = 0
            for jdx0 in range(self._tz_length_0):
                self._tz_ncarray[k] = self.tz[jdx0]
                k += 1
        if self._tz_ramflag:
            for jdx0 in range(self._tz_length_0):
                self._tz_array[idx, jdx0] = self.tz[jdx0]
        if self._wg_diskflag_writing:
            k = 0
            for jdx0 in range(self._wg_length_0):
                self._wg_ncarray[k] = self.wg[jdx0]
                k += 1
        if self._wg_ramflag:
            for jdx0 in range(self._wg_length_0):
                self._wg_array[idx, jdx0] = self.wg[jdx0]
        if self._netshortwaveradiationsnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._netshortwaveradiationsnow_length_0):
                self._netshortwaveradiationsnow_ncarray[k] = self.netshortwaveradiationsnow[jdx0]
                k += 1
        if self._netshortwaveradiationsnow_ramflag:
            for jdx0 in range(self._netshortwaveradiationsnow_length_0):
                self._netshortwaveradiationsnow_array[idx, jdx0] = self.netshortwaveradiationsnow[jdx0]
        if self._netlongwaveradiationsnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._netlongwaveradiationsnow_length_0):
                self._netlongwaveradiationsnow_ncarray[k] = self.netlongwaveradiationsnow[jdx0]
                k += 1
        if self._netlongwaveradiationsnow_ramflag:
            for jdx0 in range(self._netlongwaveradiationsnow_length_0):
                self._netlongwaveradiationsnow_array[idx, jdx0] = self.netlongwaveradiationsnow[jdx0]
        if self._netradiationsnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._netradiationsnow_length_0):
                self._netradiationsnow_ncarray[k] = self.netradiationsnow[jdx0]
                k += 1
        if self._netradiationsnow_ramflag:
            for jdx0 in range(self._netradiationsnow_length_0):
                self._netradiationsnow_array[idx, jdx0] = self.netradiationsnow[jdx0]
        if self._nbes_diskflag_writing:
            k = 0
            for jdx0 in range(self._nbes_length_0):
                self._nbes_ncarray[k] = self.nbes[jdx0]
                k += 1
        if self._nbes_ramflag:
            for jdx0 in range(self._nbes_length_0):
                self._nbes_array[idx, jdx0] = self.nbes[jdx0]
        if self._sbes_diskflag_writing:
            k = 0
            for jdx0 in range(self._sbes_length_0):
                self._sbes_ncarray[k] = self.sbes[jdx0]
                k += 1
        if self._sbes_ramflag:
            for jdx0 in range(self._sbes_length_0):
                self._sbes_array[idx, jdx0] = self.sbes[jdx0]
        if self._evi_diskflag_writing:
            k = 0
            for jdx0 in range(self._evi_length_0):
                self._evi_ncarray[k] = self.evi[jdx0]
                k += 1
        if self._evi_ramflag:
            for jdx0 in range(self._evi_length_0):
                self._evi_array[idx, jdx0] = self.evi[jdx0]
        if self._evb_diskflag_writing:
            k = 0
            for jdx0 in range(self._evb_length_0):
                self._evb_ncarray[k] = self.evb[jdx0]
                k += 1
        if self._evb_ramflag:
            for jdx0 in range(self._evb_length_0):
                self._evb_array[idx, jdx0] = self.evb[jdx0]
        if self._evs_diskflag_writing:
            k = 0
            for jdx0 in range(self._evs_length_0):
                self._evs_ncarray[k] = self.evs[jdx0]
                k += 1
        if self._evs_ramflag:
            for jdx0 in range(self._evs_length_0):
                self._evs_array[idx, jdx0] = self.evs[jdx0]
        if self._wnied_diskflag_writing:
            k = 0
            for jdx0 in range(self._wnied_length_0):
                self._wnied_ncarray[k] = self.wnied[jdx0]
                k += 1
        if self._wnied_ramflag:
            for jdx0 in range(self._wnied_length_0):
                self._wnied_array[idx, jdx0] = self.wnied[jdx0]
        if self._tempssurface_diskflag_writing:
            k = 0
            for jdx0 in range(self._tempssurface_length_0):
                self._tempssurface_ncarray[k] = self.tempssurface[jdx0]
                k += 1
        if self._tempssurface_ramflag:
            for jdx0 in range(self._tempssurface_length_0):
                self._tempssurface_array[idx, jdx0] = self.tempssurface[jdx0]
        if self._actualalbedo_diskflag_writing:
            k = 0
            for jdx0 in range(self._actualalbedo_length_0):
                self._actualalbedo_ncarray[k] = self.actualalbedo[jdx0]
                k += 1
        if self._actualalbedo_ramflag:
            for jdx0 in range(self._actualalbedo_length_0):
                self._actualalbedo_array[idx, jdx0] = self.actualalbedo[jdx0]
        if self._schmpot_diskflag_writing:
            k = 0
            for jdx0 in range(self._schmpot_length_0):
                self._schmpot_ncarray[k] = self.schmpot[jdx0]
                k += 1
        if self._schmpot_ramflag:
            for jdx0 in range(self._schmpot_length_0):
                self._schmpot_array[idx, jdx0] = self.schmpot[jdx0]
        if self._schm_diskflag_writing:
            k = 0
            for jdx0 in range(self._schm_length_0):
                self._schm_ncarray[k] = self.schm[jdx0]
                k += 1
        if self._schm_ramflag:
            for jdx0 in range(self._schm_length_0):
                self._schm_array[idx, jdx0] = self.schm[jdx0]
        if self._gefrpot_diskflag_writing:
            k = 0
            for jdx0 in range(self._gefrpot_length_0):
                self._gefrpot_ncarray[k] = self.gefrpot[jdx0]
                k += 1
        if self._gefrpot_ramflag:
            for jdx0 in range(self._gefrpot_length_0):
                self._gefrpot_array[idx, jdx0] = self.gefrpot[jdx0]
        if self._gefr_diskflag_writing:
            k = 0
            for jdx0 in range(self._gefr_length_0):
                self._gefr_ncarray[k] = self.gefr[jdx0]
                k += 1
        if self._gefr_ramflag:
            for jdx0 in range(self._gefr_length_0):
                self._gefr_array[idx, jdx0] = self.gefr[jdx0]
        if self._wlatsnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._wlatsnow_length_0):
                self._wlatsnow_ncarray[k] = self.wlatsnow[jdx0]
                k += 1
        if self._wlatsnow_ramflag:
            for jdx0 in range(self._wlatsnow_length_0):
                self._wlatsnow_array[idx, jdx0] = self.wlatsnow[jdx0]
        if self._wsenssnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._wsenssnow_length_0):
                self._wsenssnow_ncarray[k] = self.wsenssnow[jdx0]
                k += 1
        if self._wsenssnow_ramflag:
            for jdx0 in range(self._wsenssnow_length_0):
                self._wsenssnow_array[idx, jdx0] = self.wsenssnow[jdx0]
        if self._wsurf_diskflag_writing:
            k = 0
            for jdx0 in range(self._wsurf_length_0):
                self._wsurf_ncarray[k] = self.wsurf[jdx0]
                k += 1
        if self._wsurf_ramflag:
            for jdx0 in range(self._wsurf_length_0):
                self._wsurf_array[idx, jdx0] = self.wsurf[jdx0]
        if self._sff_diskflag_writing:
            k = 0
            for jdx0 in range(self._sff_length_0):
                self._sff_ncarray[k] = self.sff[jdx0]
                k += 1
        if self._sff_ramflag:
            for jdx0 in range(self._sff_length_0):
                self._sff_array[idx, jdx0] = self.sff[jdx0]
        if self._fvg_diskflag_writing:
            k = 0
            for jdx0 in range(self._fvg_length_0):
                self._fvg_ncarray[k] = self.fvg[jdx0]
                k += 1
        if self._fvg_ramflag:
            for jdx0 in range(self._fvg_length_0):
                self._fvg_array[idx, jdx0] = self.fvg[jdx0]
        if self._wada_diskflag_writing:
            k = 0
            for jdx0 in range(self._wada_length_0):
                self._wada_ncarray[k] = self.wada[jdx0]
                k += 1
        if self._wada_ramflag:
            for jdx0 in range(self._wada_length_0):
                self._wada_array[idx, jdx0] = self.wada[jdx0]
        if self._qdb_diskflag_writing:
            k = 0
            for jdx0 in range(self._qdb_length_0):
                self._qdb_ncarray[k] = self.qdb[jdx0]
                k += 1
        if self._qdb_ramflag:
            for jdx0 in range(self._qdb_length_0):
                self._qdb_array[idx, jdx0] = self.qdb[jdx0]
        if self._qib1_diskflag_writing:
            k = 0
            for jdx0 in range(self._qib1_length_0):
                self._qib1_ncarray[k] = self.qib1[jdx0]
                k += 1
        if self._qib1_ramflag:
            for jdx0 in range(self._qib1_length_0):
                self._qib1_array[idx, jdx0] = self.qib1[jdx0]
        if self._qib2_diskflag_writing:
            k = 0
            for jdx0 in range(self._qib2_length_0):
                self._qib2_ncarray[k] = self.qib2[jdx0]
                k += 1
        if self._qib2_ramflag:
            for jdx0 in range(self._qib2_length_0):
                self._qib2_array[idx, jdx0] = self.qib2[jdx0]
        if self._qbb_diskflag_writing:
            k = 0
            for jdx0 in range(self._qbb_length_0):
                self._qbb_ncarray[k] = self.qbb[jdx0]
                k += 1
        if self._qbb_ramflag:
            for jdx0 in range(self._qbb_length_0):
                self._qbb_array[idx, jdx0] = self.qbb[jdx0]
        if self._qkap_diskflag_writing:
            k = 0
            for jdx0 in range(self._qkap_length_0):
                self._qkap_ncarray[k] = self.qkap[jdx0]
                k += 1
        if self._qkap_ramflag:
            for jdx0 in range(self._qkap_length_0):
                self._qkap_array[idx, jdx0] = self.qkap[jdx0]
        if self._qdgz_diskflag_writing:
            self._qdgz_ncarray[0] = self.qdgz
        if self._qdgz_ramflag:
            self._qdgz_array[idx] = self.qdgz
        if self._qdgz1_diskflag_writing:
            self._qdgz1_ncarray[0] = self.qdgz1
        if self._qdgz1_ramflag:
            self._qdgz1_array[idx] = self.qdgz1
        if self._qdgz2_diskflag_writing:
            self._qdgz2_ncarray[0] = self.qdgz2
        if self._qdgz2_ramflag:
            self._qdgz2_array[idx] = self.qdgz2
        if self._qigz1_diskflag_writing:
            self._qigz1_ncarray[0] = self.qigz1
        if self._qigz1_ramflag:
            self._qigz1_array[idx] = self.qigz1
        if self._qigz2_diskflag_writing:
            self._qigz2_ncarray[0] = self.qigz2
        if self._qigz2_ramflag:
            self._qigz2_array[idx] = self.qigz2
        if self._qbgz_diskflag_writing:
            self._qbgz_ncarray[0] = self.qbgz
        if self._qbgz_ramflag:
            self._qbgz_array[idx] = self.qbgz
        if self._qdga1_diskflag_writing:
            self._qdga1_ncarray[0] = self.qdga1
        if self._qdga1_ramflag:
            self._qdga1_array[idx] = self.qdga1
        if self._qdga2_diskflag_writing:
            self._qdga2_ncarray[0] = self.qdga2
        if self._qdga2_ramflag:
            self._qdga2_array[idx] = self.qdga2
        if self._qiga1_diskflag_writing:
            self._qiga1_ncarray[0] = self.qiga1
        if self._qiga1_ramflag:
            self._qiga1_array[idx] = self.qiga1
        if self._qiga2_diskflag_writing:
            self._qiga2_ncarray[0] = self.qiga2
        if self._qiga2_ramflag:
            self._qiga2_array[idx] = self.qiga2
        if self._qbga_diskflag_writing:
            self._qbga_ncarray[0] = self.qbga
        if self._qbga_ramflag:
            self._qbga_array[idx] = self.qbga
        if self._qah_diskflag_writing:
            self._qah_ncarray[0] = self.qah
        if self._qah_ramflag:
            self._qah_array[idx] = self.qah
        if self._qa_diskflag_writing:
            self._qa_ncarray[0] = self.qa
        if self._qa_ramflag:
            self._qa_array[idx] = self.qa
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "qz":
            self._qz_outputpointer = value.p_value
        if name == "qzh":
            self._qzh_outputpointer = value.p_value
        if name == "dailysunshineduration":
            self._dailysunshineduration_outputpointer = value.p_value
        if name == "dailypossiblesunshineduration":
            self._dailypossiblesunshineduration_outputpointer = value.p_value
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
        if name == "windspeed2m":
            self._windspeed2m_outputpointer = value.p_value
        if name == "qdgz":
            self._qdgz_outputpointer = value.p_value
        if name == "qdgz1":
            self._qdgz1_outputpointer = value.p_value
        if name == "qdgz2":
            self._qdgz2_outputpointer = value.p_value
        if name == "qigz1":
            self._qigz1_outputpointer = value.p_value
        if name == "qigz2":
            self._qigz2_outputpointer = value.p_value
        if name == "qbgz":
            self._qbgz_outputpointer = value.p_value
        if name == "qdga1":
            self._qdga1_outputpointer = value.p_value
        if name == "qdga2":
            self._qdga2_outputpointer = value.p_value
        if name == "qiga1":
            self._qiga1_outputpointer = value.p_value
        if name == "qiga2":
            self._qiga2_outputpointer = value.p_value
        if name == "qbga":
            self._qbga_outputpointer = value.p_value
        if name == "qah":
            self._qah_outputpointer = value.p_value
        if name == "qa":
            self._qa_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._qz_outputflag:
            self._qz_outputpointer[0] = self.qz
        if self._qzh_outputflag:
            self._qzh_outputpointer[0] = self.qzh
        if self._dailysunshineduration_outputflag:
            self._dailysunshineduration_outputpointer[0] = self.dailysunshineduration
        if self._dailypossiblesunshineduration_outputflag:
            self._dailypossiblesunshineduration_outputpointer[0] = self.dailypossiblesunshineduration
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._windspeed2m_outputflag:
            self._windspeed2m_outputpointer[0] = self.windspeed2m
        if self._qdgz_outputflag:
            self._qdgz_outputpointer[0] = self.qdgz
        if self._qdgz1_outputflag:
            self._qdgz1_outputpointer[0] = self.qdgz1
        if self._qdgz2_outputflag:
            self._qdgz2_outputpointer[0] = self.qdgz2
        if self._qigz1_outputflag:
            self._qigz1_outputpointer[0] = self.qigz1
        if self._qigz2_outputflag:
            self._qigz2_outputpointer[0] = self.qigz2
        if self._qbgz_outputflag:
            self._qbgz_outputpointer[0] = self.qbgz
        if self._qdga1_outputflag:
            self._qdga1_outputpointer[0] = self.qdga1
        if self._qdga2_outputflag:
            self._qdga2_outputpointer[0] = self.qdga2
        if self._qiga1_outputflag:
            self._qiga1_outputpointer[0] = self.qiga1
        if self._qiga2_outputflag:
            self._qiga2_outputpointer[0] = self.qiga2
        if self._qbga_outputflag:
            self._qbga_outputpointer[0] = self.qbga
        if self._qah_outputflag:
            self._qah_outputpointer[0] = self.qah
        if self._qa_outputflag:
            self._qa_outputpointer[0] = self.qa
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inzp_diskflag_reading:
            k = 0
            for jdx0 in range(self._inzp_length_0):
                self.inzp[jdx0] = self._inzp_ncarray[k]
                k += 1
        elif self._inzp_ramflag:
            for jdx0 in range(self._inzp_length_0):
                self.inzp[jdx0] = self._inzp_array[idx, jdx0]
        if self._wats_diskflag_reading:
            k = 0
            for jdx0 in range(self._wats_length_0):
                self.wats[jdx0] = self._wats_ncarray[k]
                k += 1
        elif self._wats_ramflag:
            for jdx0 in range(self._wats_length_0):
                self.wats[jdx0] = self._wats_array[idx, jdx0]
        if self._waes_diskflag_reading:
            k = 0
            for jdx0 in range(self._waes_length_0):
                self.waes[jdx0] = self._waes_ncarray[k]
                k += 1
        elif self._waes_ramflag:
            for jdx0 in range(self._waes_length_0):
                self.waes[jdx0] = self._waes_array[idx, jdx0]
        if self._esnow_diskflag_reading:
            k = 0
            for jdx0 in range(self._esnow_length_0):
                self.esnow[jdx0] = self._esnow_ncarray[k]
                k += 1
        elif self._esnow_ramflag:
            for jdx0 in range(self._esnow_length_0):
                self.esnow[jdx0] = self._esnow_array[idx, jdx0]
        if self._taus_diskflag_reading:
            k = 0
            for jdx0 in range(self._taus_length_0):
                self.taus[jdx0] = self._taus_ncarray[k]
                k += 1
        elif self._taus_ramflag:
            for jdx0 in range(self._taus_length_0):
                self.taus[jdx0] = self._taus_array[idx, jdx0]
        if self._ebdn_diskflag_reading:
            k = 0
            for jdx0 in range(self._ebdn_length_0):
                self.ebdn[jdx0] = self._ebdn_ncarray[k]
                k += 1
        elif self._ebdn_ramflag:
            for jdx0 in range(self._ebdn_length_0):
                self.ebdn[jdx0] = self._ebdn_array[idx, jdx0]
        if self._bowa_diskflag_reading:
            k = 0
            for jdx0 in range(self._bowa_length_0):
                self.bowa[jdx0] = self._bowa_ncarray[k]
                k += 1
        elif self._bowa_ramflag:
            for jdx0 in range(self._bowa_length_0):
                self.bowa[jdx0] = self._bowa_array[idx, jdx0]
        if self._sdg1_diskflag_reading:
            self.sdg1 = self._sdg1_ncarray[0]
        elif self._sdg1_ramflag:
            self.sdg1 = self._sdg1_array[idx]
        if self._sdg2_diskflag_reading:
            self.sdg2 = self._sdg2_ncarray[0]
        elif self._sdg2_ramflag:
            self.sdg2 = self._sdg2_array[idx]
        if self._sig1_diskflag_reading:
            self.sig1 = self._sig1_ncarray[0]
        elif self._sig1_ramflag:
            self.sig1 = self._sig1_array[idx]
        if self._sig2_diskflag_reading:
            self.sig2 = self._sig2_ncarray[0]
        elif self._sig2_ramflag:
            self.sig2 = self._sig2_array[idx]
        if self._sbg_diskflag_reading:
            self.sbg = self._sbg_ncarray[0]
        elif self._sbg_ramflag:
            self.sbg = self._sbg_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._inzp_diskflag_writing:
            k = 0
            for jdx0 in range(self._inzp_length_0):
                self._inzp_ncarray[k] = self.inzp[jdx0]
                k += 1
        if self._inzp_ramflag:
            for jdx0 in range(self._inzp_length_0):
                self._inzp_array[idx, jdx0] = self.inzp[jdx0]
        if self._wats_diskflag_writing:
            k = 0
            for jdx0 in range(self._wats_length_0):
                self._wats_ncarray[k] = self.wats[jdx0]
                k += 1
        if self._wats_ramflag:
            for jdx0 in range(self._wats_length_0):
                self._wats_array[idx, jdx0] = self.wats[jdx0]
        if self._waes_diskflag_writing:
            k = 0
            for jdx0 in range(self._waes_length_0):
                self._waes_ncarray[k] = self.waes[jdx0]
                k += 1
        if self._waes_ramflag:
            for jdx0 in range(self._waes_length_0):
                self._waes_array[idx, jdx0] = self.waes[jdx0]
        if self._esnow_diskflag_writing:
            k = 0
            for jdx0 in range(self._esnow_length_0):
                self._esnow_ncarray[k] = self.esnow[jdx0]
                k += 1
        if self._esnow_ramflag:
            for jdx0 in range(self._esnow_length_0):
                self._esnow_array[idx, jdx0] = self.esnow[jdx0]
        if self._taus_diskflag_writing:
            k = 0
            for jdx0 in range(self._taus_length_0):
                self._taus_ncarray[k] = self.taus[jdx0]
                k += 1
        if self._taus_ramflag:
            for jdx0 in range(self._taus_length_0):
                self._taus_array[idx, jdx0] = self.taus[jdx0]
        if self._ebdn_diskflag_writing:
            k = 0
            for jdx0 in range(self._ebdn_length_0):
                self._ebdn_ncarray[k] = self.ebdn[jdx0]
                k += 1
        if self._ebdn_ramflag:
            for jdx0 in range(self._ebdn_length_0):
                self._ebdn_array[idx, jdx0] = self.ebdn[jdx0]
        if self._bowa_diskflag_writing:
            k = 0
            for jdx0 in range(self._bowa_length_0):
                self._bowa_ncarray[k] = self.bowa[jdx0]
                k += 1
        if self._bowa_ramflag:
            for jdx0 in range(self._bowa_length_0):
                self._bowa_array[idx, jdx0] = self.bowa[jdx0]
        if self._sdg1_diskflag_writing:
            self._sdg1_ncarray[0] = self.sdg1
        if self._sdg1_ramflag:
            self._sdg1_array[idx] = self.sdg1
        if self._sdg2_diskflag_writing:
            self._sdg2_ncarray[0] = self.sdg2
        if self._sdg2_ramflag:
            self._sdg2_array[idx] = self.sdg2
        if self._sig1_diskflag_writing:
            self._sig1_ncarray[0] = self.sig1
        if self._sig1_ramflag:
            self._sig1_array[idx] = self.sig1
        if self._sig2_diskflag_writing:
            self._sig2_ncarray[0] = self.sig2
        if self._sig2_ramflag:
            self._sig2_array[idx] = self.sig2
        if self._sbg_diskflag_writing:
            self._sbg_ncarray[0] = self.sbg
        if self._sbg_ramflag:
            self._sbg_array[idx] = self.sbg
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "sdg1":
            self._sdg1_outputpointer = value.p_value
        if name == "sdg2":
            self._sdg2_outputpointer = value.p_value
        if name == "sig1":
            self._sig1_outputpointer = value.p_value
        if name == "sig2":
            self._sig2_outputpointer = value.p_value
        if name == "sbg":
            self._sbg_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._sdg1_outputflag:
            self._sdg1_outputpointer[0] = self.sdg1
        if self._sdg2_outputflag:
            self._sdg2_outputpointer[0] = self.sdg2
        if self._sig1_outputflag:
            self._sig1_outputpointer[0] = self.sig1
        if self._sig2_outputflag:
            self._sig2_outputpointer[0] = self.sig2
        if self._sbg_outputflag:
            self._sbg_outputpointer[0] = self.sbg
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
cdef class PegasusESnow(rootutils.PegasusBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_backwardeulererror_v1(x)
@cython.final
cdef class PegasusTempSSurface(rootutils.PegasusBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_energygainsnowsurface_v1(x)
@cython.final
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.aetmodel = None
        self.aetmodel_is_mainmodel = False
        self.radiationmodel = None
        self.radiationmodel_is_mainmodel = False
        self.soilmodel = None
        self.soilmodel_is_mainmodel = False
        self.pegasusesnow = PegasusESnow(self)
        self.pegasustempssurface = PegasusTempSSurface(self)
    def get_aetmodel(self) -> masterinterface.MasterInterface | None:
        return self.aetmodel
    def set_aetmodel(self, aetmodel: masterinterface.MasterInterface | None) -> None:
        self.aetmodel = aetmodel
    def get_radiationmodel(self) -> masterinterface.MasterInterface | None:
        return self.radiationmodel
    def set_radiationmodel(self, radiationmodel: masterinterface.MasterInterface | None) -> None:
        self.radiationmodel = radiationmodel
    def get_soilmodel(self) -> masterinterface.MasterInterface | None:
        return self.soilmodel
    def set_soilmodel(self, soilmodel: masterinterface.MasterInterface | None) -> None:
        self.soilmodel = soilmodel
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
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.reset_reuseflags()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.reset_reuseflags()
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.load_data(idx)
        self.sequences.inputs.load_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.load_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.load_data(idx)
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.save_data(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.save_data(idx)
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._inzp_length_0):
            self.sequences.old_states.inzp[jdx0] = self.sequences.new_states.inzp[jdx0]
        for jdx0 in range(self.sequences.states._wats_length_0):
            self.sequences.old_states.wats[jdx0] = self.sequences.new_states.wats[jdx0]
        for jdx0 in range(self.sequences.states._waes_length_0):
            self.sequences.old_states.waes[jdx0] = self.sequences.new_states.waes[jdx0]
        for jdx0 in range(self.sequences.states._esnow_length_0):
            self.sequences.old_states.esnow[jdx0] = self.sequences.new_states.esnow[jdx0]
        for jdx0 in range(self.sequences.states._taus_length_0):
            self.sequences.old_states.taus[jdx0] = self.sequences.new_states.taus[jdx0]
        for jdx0 in range(self.sequences.states._ebdn_length_0):
            self.sequences.old_states.ebdn[jdx0] = self.sequences.new_states.ebdn[jdx0]
        for jdx0 in range(self.sequences.states._bowa_length_0):
            self.sequences.old_states.bowa[jdx0] = self.sequences.new_states.bowa[jdx0]
        self.sequences.old_states.sdg1 = self.sequences.new_states.sdg1
        self.sequences.old_states.sdg2 = self.sequences.new_states.sdg2
        self.sequences.old_states.sig1 = self.sequences.new_states.sig1
        self.sequences.old_states.sig2 = self.sequences.new_states.sig2
        self.sequences.old_states.sbg = self.sequences.new_states.sbg
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.new2old()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.new2old()
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.process_radiationmodel_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_sunshineduration_v1()
        self.calc_globalradiation_v1()
        self.calc_qzh_v1()
        self.update_loggedsunshineduration_v1()
        self.calc_dailysunshineduration_v1()
        self.update_loggedpossiblesunshineduration_v1()
        self.calc_dailypossiblesunshineduration_v1()
        self.calc_nkor_v1()
        self.calc_tkor_v1()
        self.calc_windspeed2m_v1()
        self.calc_reducedwindspeed2m_v1()
        self.calc_saturationvapourpressure_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_nbes_inzp_v1()
        self.calc_snratio_v1()
        self.calc_sbes_v1()
        self.calc_wats_v1()
        self.calc_wada_waes_v1()
        self.calc_wnied_esnow_v1()
        self.calc_temps_v1()
        self.update_taus_v1()
        self.calc_actualalbedo_v1()
        self.calc_netshortwaveradiationsnow_v1()
        self.calc_rlatm_v1()
        self.calc_tz_v1()
        self.calc_wg_v1()
        self.update_esnow_v1()
        self.calc_schmpot_v2()
        self.calc_schm_wats_v1()
        self.calc_gefrpot_v1()
        self.calc_gefr_wats_v1()
        self.calc_evs_waes_wats_v1()
        self.update_wada_waes_v1()
        self.update_esnow_v2()
        self.calc_evi_inzp_v1()
        self.calc_evb_v1()
        self.update_ebdn_v1()
        self.calc_sff_v1()
        self.calc_fvg_v1()
        self.calc_qkap_v1()
        self.calc_qbb_v1()
        self.calc_qib1_v1()
        self.calc_qib2_v1()
        self.calc_qdb_v1()
        self.update_qdb_v1()
        self.calc_bowa_v1()
        self.calc_qbgz_v1()
        self.calc_qigz1_v1()
        self.calc_qigz2_v1()
        self.calc_qdgz_v1()
        self.calc_qbga_sbg_qbgz_qdgz_v1()
        self.calc_qiga1_sig1_v1()
        self.calc_qiga2_sig2_v1()
        self.calc_qdgz1_qdgz2_v1()
        self.calc_qdga1_sdg1_v1()
        self.calc_qdga2_sdg2_v1()
        self.calc_qah_v1()
        self.calc_qa_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_inlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_inlets()
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.update_inlets()
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.pick_qz_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outlets()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outlets()
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.update_outlets()
        self.pass_qa_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_receivers(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_receivers(idx)
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_senders(idx)
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_senders(idx)
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outputs()
        if (self.radiationmodel is not None) and not self.radiationmodel_is_mainmodel:
            self.radiationmodel.update_outputs()
        if (self.soilmodel is not None) and not self.soilmodel_is_mainmodel:
            self.soilmodel.update_outputs()
    cpdef inline void pick_qz_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx])
    cpdef inline void process_radiationmodel_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_possiblesunshineduration_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
    cpdef inline void calc_sunshineduration_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
    cpdef inline void calc_globalradiation_v1(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_qzh_v1(self) noexcept nogil:
        self.sequences.fluxes.qzh = self.sequences.fluxes.qz / self.parameters.derived.qfactor
    cpdef inline void update_loggedsunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.factors.sunshineduration
    cpdef inline void calc_dailysunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailysunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailysunshineduration = self.sequences.fluxes.dailysunshineduration + (self.sequences.logs.loggedsunshineduration[idx])
    cpdef inline void update_loggedpossiblesunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedpossiblesunshineduration[idx] = (                self.sequences.logs.loggedpossiblesunshineduration[idx - 1]            )
        self.sequences.logs.loggedpossiblesunshineduration[0] = self.sequences.factors.possiblesunshineduration
    cpdef inline void calc_dailypossiblesunshineduration_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailypossiblesunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailypossiblesunshineduration = self.sequences.fluxes.dailypossiblesunshineduration + (self.sequences.logs.loggedpossiblesunshineduration[idx])
    cpdef inline void calc_nkor_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.nkor[k] = self.parameters.control.kg[k] * self.sequences.inputs.nied
    cpdef inline void calc_tkor_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.tkor[k] = self.parameters.control.kt[k] + self.sequences.inputs.teml
    cpdef inline void calc_windspeed2m_v1(self) noexcept nogil:
        self.sequences.fluxes.windspeed2m = self.sequences.inputs.windspeed * (            log(2.0 / self.parameters.fixed.z0)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.z0)        )
    cpdef inline void calc_reducedwindspeed2m_v1(self) noexcept nogil:
        cdef double d_lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (LAUBW, MISCHW, NADELW):
                d_lai = self.parameters.control.lai[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]
                self.sequences.fluxes.reducedwindspeed2m[k] = (                    max(self.parameters.control.p1wind - self.parameters.control.p2wind * d_lai, 0.0) * self.sequences.fluxes.windspeed2m                )
            else:
                self.sequences.fluxes.reducedwindspeed2m[k] = self.sequences.fluxes.windspeed2m
    cpdef inline void calc_saturationvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.saturationvapourpressure[k] = self.return_saturationvapourpressure_v1(                self.sequences.fluxes.tkor[k]            )
    cpdef inline void calc_actualvapourpressure_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.actualvapourpressure[k] = (                self.sequences.fluxes.saturationvapourpressure[k] * self.sequences.inputs.relativehumidity / 100.0            )
    cpdef inline void calc_nbes_inzp_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.nbes[k] = 0.0
                self.sequences.states.inzp[k] = 0.0
            else:
                self.sequences.fluxes.nbes[k] = max(                    self.sequences.fluxes.nkor[k]                    + self.sequences.states.inzp[k]                    - self.parameters.derived.kinz[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]],                    0.0,                )
                self.sequences.states.inzp[k] = self.sequences.states.inzp[k] + (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.nbes[k])
    cpdef inline void calc_snratio_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.fluxes.tkor[k] >= (self.parameters.control.tgr[k] + self.parameters.control.tsp[k] / 2.0):
                self.sequences.aides.snratio[k] = 0.0
            elif self.sequences.fluxes.tkor[k] <= (self.parameters.control.tgr[k] - self.parameters.control.tsp[k] / 2.0):
                self.sequences.aides.snratio[k] = 1.0
            else:
                self.sequences.aides.snratio[k] = (                    (self.parameters.control.tgr[k] + self.parameters.control.tsp[k] / 2.0) - self.sequences.fluxes.tkor[k]                ) / self.parameters.control.tsp[k]
    cpdef inline void calc_sbes_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.sbes[k] = self.sequences.aides.snratio[k] * self.sequences.fluxes.nbes[k]
    cpdef inline void calc_wats_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.wats[k] = 0.0
            else:
                self.sequences.states.wats[k] = self.sequences.states.wats[k] + (self.sequences.fluxes.sbes[k])
    cpdef inline void calc_wada_waes_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.waes[k] = 0.0
                self.sequences.fluxes.wada[k] = self.sequences.fluxes.nbes[k]
            else:
                self.sequences.states.waes[k] = self.sequences.states.waes[k] + (self.sequences.fluxes.nbes[k])
                self.sequences.fluxes.wada[k] = max(self.sequences.states.waes[k] - self.parameters.control.pwmax[k] * self.sequences.states.wats[k], 0.0)
                self.sequences.states.waes[k] = self.sequences.states.waes[k] - (self.sequences.fluxes.wada[k])
    cpdef inline void calc_wnied_esnow_v1(self) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.wnied[k] = 0.0
                self.sequences.states.esnow[k] = 0.0
            else:
                d_ice = self.parameters.fixed.cpeis * self.sequences.fluxes.sbes[k]
                d_water = self.parameters.fixed.cpwasser * (self.sequences.fluxes.nbes[k] - self.sequences.fluxes.sbes[k] - self.sequences.fluxes.wada[k])
                self.sequences.fluxes.wnied[k] = (self.sequences.fluxes.tkor[k] - self.parameters.control.trefn[k]) * (d_ice + d_water)
                self.sequences.states.esnow[k] = self.sequences.states.esnow[k] + (self.sequences.fluxes.wnied[k])
    cpdef inline void calc_temps_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.aides.temps[k] = self.return_temps_v1(k)
    cpdef inline void update_taus_v1(self) noexcept nogil:
        cdef double d_r2
        cdef double d_r1
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0:
                if isnan(self.sequences.states.taus[k]):
                    self.sequences.states.taus[k] = 0.0
                d_r1 = exp(                    5000.0 * (1 / 273.15 - 1.0 / (273.15 + self.sequences.aides.temps[k]))                )
                d_r2 = min(d_r1**10, 1.0)
                self.sequences.states.taus[k] = self.sequences.states.taus[k] * (max(1 - 0.1 * self.sequences.fluxes.sbes[k], 0.0))
                self.sequences.states.taus[k] = self.sequences.states.taus[k] + ((d_r1 + d_r2 + 0.03) / 1e6 * self.parameters.derived.seconds)
            else:
                self.sequences.states.taus[k] = nan
    cpdef inline void calc_actualalbedo_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0.0:
                self.sequences.fluxes.actualalbedo[k] = self.parameters.control.albedo0snow * (                    1.0 - self.parameters.control.snowagingfactor * self.sequences.states.taus[k] / (1.0 + self.sequences.states.taus[k])                )
            else:
                self.sequences.fluxes.actualalbedo[k] = nan
    cpdef inline void calc_netshortwaveradiationsnow_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if isnan(self.sequences.fluxes.actualalbedo[k]):
                self.sequences.fluxes.netshortwaveradiationsnow[k] = 0.0
            else:
                self.sequences.fluxes.netshortwaveradiationsnow[k] = (                    self.parameters.derived.fr[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]                    * (1.0 - self.sequences.fluxes.actualalbedo[k])                    * self.sequences.fluxes.globalradiation                )
    cpdef inline void calc_rlatm_v1(self) noexcept nogil:
        cdef double d_t
        cdef numpy.int64_t k
        cdef double d_common
        cdef double d_rs
        d_rs = self.sequences.fluxes.dailysunshineduration / self.sequences.fluxes.dailypossiblesunshineduration
        d_common = self.parameters.fixed.fratm * self.parameters.fixed.sigma * (1.0 + 0.22 * (1.0 - d_rs) ** 2)
        for k in range(self.parameters.control.nhru):
            d_t = self.sequences.fluxes.tkor[k] + 273.15
            self.sequences.aides.rlatm[k] = d_common * (                d_t**4 * (self.sequences.fluxes.actualvapourpressure[k] / d_t) ** (1.0 / 7.0)            )
    cpdef inline void calc_tz_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.tz[k] = nan
            elif self.sequences.states.ebdn[k] < 0.0:
                self.sequences.fluxes.tz[k] = self.sequences.states.ebdn[k] / (2.0 * self.parameters.fixed.z * self.parameters.fixed.cg)
            elif self.sequences.states.ebdn[k] < self.parameters.derived.heatoffusion[k]:
                self.sequences.fluxes.tz[k] = 0.0
            else:
                self.sequences.fluxes.tz[k] = (self.sequences.states.ebdn[k] - self.parameters.derived.heatoffusion[k]) / (2.0 * self.parameters.fixed.z * self.parameters.fixed.cg)
    cpdef inline void calc_wg_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (FLUSS, SEE, WASSER):
                self.sequences.fluxes.wg[k] = 0.0
            else:
                self.sequences.fluxes.wg[k] = self.return_wg_v1(k)
    cpdef inline void update_esnow_v1(self) noexcept nogil:
        cdef double d_esnow
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0.0:
                self.idx_hru = k
                d_esnow = self.sequences.states.esnow[k]
                self.sequences.states.esnow[k] = self.pegasusesnow.find_x(                    self.return_esnow_v1(k, -30.0),                    self.return_esnow_v1(k, 30.0),                    self.return_esnow_v1(k, -100.0),                    self.return_esnow_v1(k, 100.0),                    0.0,                    1e-8,                    10,                )
                if self.sequences.states.esnow[k] > 0.0:
                    self.sequences.aides.temps[k] = 0.0
                    self.sequences.fluxes.tempssurface[k] = self.return_tempssurface(k)
                    self.sequences.fluxes.wg[k] = self.return_wg_v1(k)
                    self.sequences.states.esnow[k] = d_esnow + self.sequences.fluxes.wg[k] - self.sequences.fluxes.wsurf[k]
            else:
                self.sequences.states.esnow[k] = 0.0
                self.sequences.aides.temps[k] = nan
                self.sequences.fluxes.tempssurface[k] = nan
                self.sequences.fluxes.netlongwaveradiationsnow[k] = 0.0
                self.sequences.fluxes.netradiationsnow[k] = 0.0
                self.sequences.fluxes.saturationvapourpressuresnow[k] = 0.0
                self.sequences.fluxes.wsenssnow[k] = 0.0
                self.sequences.fluxes.wlatsnow[k] = 0.0
                self.sequences.fluxes.wsurf[k] = 0.0
    cpdef inline void calc_schmpot_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0.0:
                self.sequences.fluxes.schmpot[k] = max(self.sequences.states.esnow[k] / self.parameters.fixed.rschmelz, 0.0)
            else:
                self.sequences.fluxes.schmpot[k] = 0.0
    cpdef inline void calc_schm_wats_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.schm[k] = 0.0
            else:
                self.sequences.fluxes.schm[k] = min(self.sequences.fluxes.schmpot[k], self.sequences.states.wats[k])
                self.sequences.states.wats[k] = self.sequences.states.wats[k] - (self.sequences.fluxes.schm[k])
    cpdef inline void calc_gefrpot_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0:
                self.sequences.fluxes.gefrpot[k] = max(-self.sequences.states.esnow[k] / self.parameters.fixed.rschmelz, 0)
            else:
                self.sequences.fluxes.gefrpot[k] = 0.0
    cpdef inline void calc_gefr_wats_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE) or not self.parameters.control.refreezeflag:
                self.sequences.fluxes.gefr[k] = 0.0
            else:
                self.sequences.fluxes.gefr[k] = min(self.sequences.fluxes.gefrpot[k], (self.sequences.states.waes[k] - self.sequences.states.wats[k]))
                self.sequences.states.wats[k] = self.sequences.states.wats[k] + (self.sequences.fluxes.gefr[k])
    cpdef inline void calc_evs_waes_wats_v1(self) noexcept nogil:
        cdef double d_frac
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, SEE, FLUSS) or (self.sequences.states.waes[k] <= 0.0):
                self.sequences.fluxes.evs[k] = 0.0
                self.sequences.states.waes[k] = 0.0
                self.sequences.states.wats[k] = 0.0
            else:
                self.sequences.fluxes.evs[k] = min(self.sequences.fluxes.wlatsnow[k] / self.parameters.fixed.lwe, self.sequences.states.waes[k])
                d_frac = (self.sequences.states.waes[k] - self.sequences.fluxes.evs[k]) / self.sequences.states.waes[k]
                self.sequences.states.waes[k] = self.sequences.states.waes[k] * (d_frac)
                self.sequences.states.wats[k] = self.sequences.states.wats[k] * (d_frac)
    cpdef inline void update_wada_waes_v1(self) noexcept nogil:
        cdef double d_wada_corr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] not in (WASSER, FLUSS, SEE):
                d_wada_corr = max(self.sequences.states.waes[k] - self.parameters.control.pwmax[k] * self.sequences.states.wats[k], 0.0)
                self.sequences.fluxes.wada[k] = self.sequences.fluxes.wada[k] + (d_wada_corr)
                self.sequences.states.waes[k] = self.sequences.states.waes[k] - (d_wada_corr)
    cpdef inline void update_esnow_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE)) or (self.sequences.states.waes[k] <= 0.0):
                self.sequences.states.esnow[k] = 0.0
            else:
                self.sequences.states.esnow[k] = self.sequences.states.esnow[k] + (self.parameters.fixed.rschmelz * (self.sequences.fluxes.gefr[k] - self.sequences.fluxes.schm[k]))
    cpdef inline void calc_evi_inzp_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_evi_inzp_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_evb_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_evb_aetmodel_v1((<masterinterface.MasterInterface>self.aetmodel))
    cpdef inline void update_ebdn_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.ebdn[k] = 0.0
            else:
                self.sequences.states.ebdn[k] = self.sequences.states.ebdn[k] + (self.parameters.control.wg2z[self.parameters.derived.moy[self.idx_sim]] - self.sequences.fluxes.wg[k])
    cpdef inline void calc_sff_v1(self) noexcept nogil:
        cdef double d_sff
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.sff[k] = 0.0
            else:
                d_sff = 1.0 - self.sequences.states.ebdn[k] / (self.parameters.fixed.bowa2z[k] * self.parameters.fixed.rschmelz)
                self.sequences.fluxes.sff[k] = min(max(d_sff, 0.0), 1.0)
    cpdef inline void calc_fvg_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.fvg[k] = 0.0
            else:
                self.sequences.fluxes.fvg[k] = min(self.parameters.control.fvf * self.sequences.fluxes.sff[k] ** self.parameters.control.bsff, 1.0)
    cpdef inline void calc_qkap_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE)) or (self.parameters.control.wmax[k] <= 0.0):
                self.sequences.fluxes.qkap[k] = 0.0
            elif self.sequences.states.bowa[k] <= self.parameters.control.kapgrenz[k, 0]:
                self.sequences.fluxes.qkap[k] = self.parameters.control.kapmax[k]
            elif self.sequences.states.bowa[k] <= self.parameters.control.kapgrenz[k, 1]:
                self.sequences.fluxes.qkap[k] = self.parameters.control.kapmax[k] * (                    1.0                    - (self.sequences.states.bowa[k] - self.parameters.control.kapgrenz[k, 0])                    / (self.parameters.control.kapgrenz[k, 1] - self.parameters.control.kapgrenz[k, 0])                )
            else:
                self.sequences.fluxes.qkap[k] = 0
    cpdef inline void calc_qbb_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (                (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE))                or (self.sequences.states.bowa[k] <= self.parameters.control.pwp[k])                or (self.parameters.control.wmax[k] <= 0.0)            ):
                self.sequences.fluxes.qbb[k] = 0.0
            elif self.sequences.states.bowa[k] <= self.parameters.control.fk[k]:
                if self.parameters.control.rbeta:
                    self.sequences.fluxes.qbb[k] = 0.0
                else:
                    self.sequences.fluxes.qbb[k] = self.parameters.control.beta[k] * (self.sequences.states.bowa[k] - self.parameters.control.pwp[k])
            else:
                self.sequences.fluxes.qbb[k] = (                    self.parameters.control.beta[k]                    * (self.sequences.states.bowa[k] - self.parameters.control.pwp[k])                    * (                        1.0                        + (self.parameters.control.fbeta[k] - 1.0)                        * (self.sequences.states.bowa[k] - self.parameters.control.fk[k])                        / (self.parameters.control.wmax[k] - self.parameters.control.fk[k])                    )                )
    cpdef inline void calc_qib1_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE)) or (                self.sequences.states.bowa[k] <= self.parameters.control.pwp[k]            ):
                self.sequences.fluxes.qib1[k] = 0.0
            else:
                self.sequences.fluxes.qib1[k] = self.parameters.control.dmin[k] * (self.sequences.states.bowa[k] / self.parameters.control.wmax[k])
    cpdef inline void calc_qib2_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (                (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE))                or (self.sequences.states.bowa[k] <= self.parameters.control.fk[k])                or (self.parameters.control.wmax[k] <= self.parameters.control.fk[k])            ):
                self.sequences.fluxes.qib2[k] = 0.0
            else:
                self.sequences.fluxes.qib2[k] = (self.parameters.control.dmax[k] - self.parameters.control.dmin[k]) * (                    (self.sequences.states.bowa[k] - self.parameters.control.fk[k]) / (self.parameters.control.wmax[k] - self.parameters.control.fk[k])                ) ** 1.5
    cpdef inline void calc_qdb_v1(self) noexcept nogil:
        cdef double d_exz
        cdef double d_sfa
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == WASSER:
                self.sequences.fluxes.qdb[k] = 0.0
            elif (self.parameters.control.lnk[k] in (VERS, FLUSS, SEE)) or (self.parameters.control.wmax[k] <= 0.0):
                self.sequences.fluxes.qdb[k] = self.sequences.fluxes.wada[k]
            else:
                if self.sequences.states.bowa[k] < self.parameters.control.wmax[k]:
                    d_sfa = (1.0 - self.sequences.states.bowa[k] / self.parameters.control.wmax[k]) ** (                        1.0 / (self.parameters.control.bsf[k] + 1.0)                    ) - (self.sequences.fluxes.wada[k] / ((self.parameters.control.bsf[k] + 1.0) * self.parameters.control.wmax[k]))
                else:
                    d_sfa = 0.0
                d_exz = self.sequences.states.bowa[k] + self.sequences.fluxes.wada[k] - self.parameters.control.wmax[k]
                self.sequences.fluxes.qdb[k] = d_exz
                if d_sfa > 0.0:
                    self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + (d_sfa ** (self.parameters.control.bsf[k] + 1.0) * self.parameters.control.wmax[k])
                self.sequences.fluxes.qdb[k] = max(self.sequences.fluxes.qdb[k], 0.0)
    cpdef inline void update_qdb_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + (self.sequences.fluxes.fvg[k] * (self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k]))
    cpdef inline void calc_bowa_v1(self) noexcept nogil:
        if self.soilmodel is None:
            self.calc_bowa_default_v1()
        elif self.soilmodel_typeid == 1:
            self.calc_bowa_soilmodel_v1(                (<masterinterface.MasterInterface>self.soilmodel)            )
    cpdef inline void calc_qbgz_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qbgz = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == SEE:
                self.sequences.fluxes.qbgz = self.sequences.fluxes.qbgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.evi[k]))
            elif self.parameters.control.lnk[k] not in (WASSER, FLUSS, VERS):
                self.sequences.fluxes.qbgz = self.sequences.fluxes.qbgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.qbb[k] - self.sequences.fluxes.qkap[k]))
    cpdef inline void calc_qigz1_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qigz1 = 0.0
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qigz1 = self.sequences.fluxes.qigz1 + (self.parameters.control.fhru[k] * self.sequences.fluxes.qib1[k])
    cpdef inline void calc_qigz2_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qigz2 = 0.0
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qigz2 = self.sequences.fluxes.qigz2 + (self.parameters.control.fhru[k] * self.sequences.fluxes.qib2[k])
    cpdef inline void calc_qdgz_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qdgz = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == FLUSS:
                self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.evi[k]))
            elif self.parameters.control.lnk[k] not in (WASSER, SEE):
                self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (self.parameters.control.fhru[k] * self.sequences.fluxes.qdb[k])
    cpdef inline void calc_qbga_sbg_qbgz_qdgz_v1(self) noexcept nogil:
        cdef double qbgz
        cdef double tt
        cdef double c2
        cdef double c1
        cdef double st
        cdef double fraction
        cdef double t
        cdef double excess
        cdef double z
        cdef double s0
        cdef double g2
        cdef double g1
        cdef double sm
        cdef double k
        k = self.parameters.derived.kb
        sm = self.parameters.control.gsbmax * self.parameters.control.volbmax
        g1 = self.parameters.control.gsbgrad1
        g2 = self.parameters.control.gsbgrad2
        s0 = self.sequences.old_states.sbg
        z = self.sequences.fluxes.qbgz
        if s0 > sm:
            excess = s0 - sm
            s0 = sm
        else:
            excess = 0.0
        if k == 0.0:
            self.sequences.new_states.sbg = 0.0
            self.sequences.fluxes.qbga = s0 + self.sequences.fluxes.qbgz
        elif z - s0 / k <= g1:
            if isinf(k):
                self.sequences.new_states.sbg = min(s0 + z, sm)
                self.sequences.fluxes.qbga = 0.0
            else:
                if isinf(sm):
                    t = 1.0
                else:
                    fraction = (k * z - sm) / (k * z - s0)
                    if fraction > 0.0:
                        t = -k * log(fraction)
                    else:
                        t = 1.0
                if t < 1.0:
                    self.sequences.new_states.sbg = sm
                    self.sequences.fluxes.qbga = s0 - sm + t * self.sequences.fluxes.qbgz
                    self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t) * sm / k)
                else:
                    self.sequences.new_states.sbg = self.return_sg_v1(k, s0, z, 1.0)
                    self.sequences.fluxes.qbga = s0 - self.sequences.new_states.sbg + self.sequences.fluxes.qbgz
        elif g2 == 0.0:
            self.sequences.fluxes.qbga = s0 / k
            self.sequences.new_states.sbg = s0
        else:
            if isinf(k) and (g2 > g1):
                self.sequences.fluxes.qbga = 0.0
                self.sequences.new_states.sbg = s0 + g2 / ((g2 - g1) / z + 1.0)
            else:
                st = min(k * (z - g1), sm)
                if g1 == g2:
                    t = min((st - s0) / g1, 1.0)
                    self.sequences.fluxes.qbga = t * (g1 * t + 2.0 * s0) / (2.0 * k)
                else:
                    c1 = (g2 - g1) / (g1 - g2 - z)
                    c2 = (g2 * k * z) / (g1 - g2)
                    t = min(k / c1 * log((st + c2) / (s0 + c2)), 1.0)
                    self.sequences.fluxes.qbga = (s0 + c2) * (                        exp(c1 * t / k) - 1.0                    ) / c1 - c2 * t / k
                if t < 1.0:
                    if st == sm:
                        self.sequences.new_states.sbg = sm
                        self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t) * sm / k)
                    else:
                        fraction = (k * z - sm) / (k * z - st)
                        if fraction > 0.0:
                            tt = -k * log(fraction)
                        else:
                            tt = 1.0
                        if t + tt < 1.0:
                            self.sequences.new_states.sbg = sm
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (st - sm + tt * self.sequences.fluxes.qbgz)
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t - tt) * sm / k)
                        else:
                            self.sequences.new_states.sbg = self.return_sg_v1(k, st, z, 1.0 - t)
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (st - self.sequences.new_states.sbg + (1.0 - t) * self.sequences.fluxes.qbgz)
                elif g1 == g2:
                    self.sequences.new_states.sbg = s0 + g1
                else:
                    self.sequences.new_states.sbg = (s0 + c2) * exp(1.0 / k * c1) - c2
        qbgz = self.sequences.fluxes.qbgz
        self.sequences.fluxes.qbgz = self.sequences.new_states.sbg - s0 + self.sequences.fluxes.qbga
        self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (qbgz - self.sequences.fluxes.qbgz)
        self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (excess)
    cpdef inline void calc_qiga1_sig1_v1(self) noexcept nogil:
        self.sequences.new_states.sig1 = self.return_sg_v1(self.parameters.derived.ki1, self.sequences.old_states.sig1, self.sequences.fluxes.qigz1, 1.0)
        self.sequences.fluxes.qiga1 = self.sequences.old_states.sig1 - self.sequences.new_states.sig1 + self.sequences.fluxes.qigz1
    cpdef inline void calc_qiga2_sig2_v1(self) noexcept nogil:
        self.sequences.new_states.sig2 = self.return_sg_v1(self.parameters.derived.ki2, self.sequences.old_states.sig2, self.sequences.fluxes.qigz2, 1.0)
        self.sequences.fluxes.qiga2 = self.sequences.old_states.sig2 - self.sequences.new_states.sig2 + self.sequences.fluxes.qigz2
    cpdef inline void calc_qdgz1_qdgz2_v1(self) noexcept nogil:
        if self.sequences.fluxes.qdgz > self.parameters.control.a2:
            self.sequences.fluxes.qdgz2 = (self.sequences.fluxes.qdgz - self.parameters.control.a2) ** 2 / (self.sequences.fluxes.qdgz + self.parameters.control.a1 - self.parameters.control.a2)
            self.sequences.fluxes.qdgz1 = self.sequences.fluxes.qdgz - self.sequences.fluxes.qdgz2
        else:
            self.sequences.fluxes.qdgz2 = 0.0
            self.sequences.fluxes.qdgz1 = self.sequences.fluxes.qdgz
    cpdef inline void calc_qdga1_sdg1_v1(self) noexcept nogil:
        self.sequences.new_states.sdg1 = self.return_sg_v1(self.parameters.derived.kd1, self.sequences.old_states.sdg1, self.sequences.fluxes.qdgz1, 1.0)
        self.sequences.fluxes.qdga1 = self.sequences.old_states.sdg1 - self.sequences.new_states.sdg1 + self.sequences.fluxes.qdgz1
    cpdef inline void calc_qdga2_sdg2_v1(self) noexcept nogil:
        self.sequences.new_states.sdg2 = self.return_sg_v1(self.parameters.derived.kd2, self.sequences.old_states.sdg2, self.sequences.fluxes.qdgz2, 1.0)
        self.sequences.fluxes.qdga2 = self.sequences.old_states.sdg2 - self.sequences.new_states.sdg2 + self.sequences.fluxes.qdgz2
    cpdef inline void calc_qah_v1(self) noexcept nogil:
        cdef double d_epw
        cdef numpy.int64_t k
        cdef double d_area
        self.sequences.fluxes.qah = self.sequences.fluxes.qzh + self.sequences.fluxes.qbga + self.sequences.fluxes.qiga1 + self.sequences.fluxes.qiga2 + self.sequences.fluxes.qdga1 + self.sequences.fluxes.qdga2
        if (not self.parameters.control.negq) and (self.sequences.fluxes.qah < 0.0):
            d_area = 0.0
            for k in range(self.parameters.control.nhru):
                if self.parameters.control.lnk[k] in (FLUSS, SEE):
                    d_area = d_area + (self.parameters.control.fhru[k])
            if d_area > 0.0:
                for k in range(self.parameters.control.nhru):
                    if self.parameters.control.lnk[k] in (FLUSS, SEE):
                        self.sequences.fluxes.evi[k] = self.sequences.fluxes.evi[k] + (self.sequences.fluxes.qah / d_area)
            self.sequences.fluxes.qah = 0.0
        d_epw = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == WASSER:
                self.sequences.fluxes.qah = self.sequences.fluxes.qah + (self.parameters.control.fhru[k] * self.sequences.fluxes.nkor[k])
                d_epw = d_epw + (self.parameters.control.fhru[k] * self.sequences.fluxes.evi[k])
        if (self.sequences.fluxes.qah > d_epw) or self.parameters.control.negq:
            self.sequences.fluxes.qah = self.sequences.fluxes.qah - (d_epw)
        elif d_epw > 0.0:
            for k in range(self.parameters.control.nhru):
                if self.parameters.control.lnk[k] == WASSER:
                    self.sequences.fluxes.evi[k] = self.sequences.fluxes.evi[k] * (self.sequences.fluxes.qah / d_epw)
            self.sequences.fluxes.qah = 0.0
    cpdef inline void calc_qa_v1(self) noexcept nogil:
        self.sequences.fluxes.qa = self.parameters.derived.qfactor * self.sequences.fluxes.qah
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.tkor[s]
    cpdef double get_meantemperature_v1(self) noexcept nogil:
        return self.sequences.inputs.teml
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.nkor[s]
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.inzp[k]
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.bowa[k]
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.wats[k] > 0.0:
            return 1.0
        return 0.0
    cpdef double get_snowalbedo_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.actualalbedo[k]
    cpdef inline double return_netlongwaveradiationsnow_v1(self, numpy.int64_t k) noexcept nogil:
        cdef double d_fr
        cdef double d_counter
        cdef double d_temp
        d_temp = self.sequences.fluxes.tkor[k] + 273.15
        d_counter = self.sequences.aides.rlatm[k]
        if self.parameters.control.lnk[k] in (LAUBW, MISCHW, NADELW):
            d_fr = self.parameters.derived.fr[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]
            d_counter = d_fr * d_counter + (1.0 - d_fr) * 0.97 * self.parameters.fixed.sigma * d_temp**4
        return self.parameters.fixed.sigma * (self.sequences.fluxes.tempssurface[k] + 273.15) ** 4 - d_counter
    cpdef inline double return_energygainsnowsurface_v1(self, double tempssurface) noexcept nogil:
        cdef numpy.int64_t k
        k = self.idx_hru
        self.sequences.fluxes.tempssurface[k] = tempssurface
        self.sequences.fluxes.saturationvapourpressuresnow[k] = self.return_saturationvapourpressure_v1(            self.sequences.fluxes.tempssurface[k]        )
        self.sequences.fluxes.wlatsnow[k] = self.return_wlatsnow_v1(k)
        self.sequences.fluxes.wsenssnow[k] = self.return_wsenssnow_v1(k)
        self.sequences.fluxes.netlongwaveradiationsnow[k] = self.return_netlongwaveradiationsnow_v1(k)
        self.sequences.fluxes.netradiationsnow[k] = self.return_netradiation_v1(            self.sequences.fluxes.netshortwaveradiationsnow[k], self.sequences.fluxes.netlongwaveradiationsnow[k]        )
        self.sequences.fluxes.wsurf[k] = self.return_wsurf_v1(k)
        return (            self.sequences.fluxes.wsurf[k] + self.sequences.fluxes.netradiationsnow[k] - self.sequences.fluxes.wsenssnow[k] - self.sequences.fluxes.wlatsnow[k]        )
    cpdef inline double return_saturationvapourpressure_v1(self, double temperature) noexcept nogil:
        return 6.1078 * 2.71828 ** (17.08085 * temperature / (temperature + 234.175))
    cpdef inline double return_netradiation_v1(self, double netshortwaveradiation, double netlongwaveradiation) noexcept nogil:
        return netshortwaveradiation - netlongwaveradiation
    cpdef inline double return_wsenssnow_v1(self, numpy.int64_t k) noexcept nogil:
        return (self.parameters.control.turb0 + self.parameters.control.turb1 * self.sequences.fluxes.reducedwindspeed2m[k]) * (            self.sequences.fluxes.tempssurface[k] - self.sequences.fluxes.tkor[k]        )
    cpdef inline double return_wlatsnow_v1(self, numpy.int64_t k) noexcept nogil:
        return (            (self.parameters.control.turb0 + self.parameters.control.turb1 * self.sequences.fluxes.reducedwindspeed2m[k])            * self.parameters.fixed.psyinv            * (self.sequences.fluxes.saturationvapourpressuresnow[k] - self.sequences.fluxes.actualvapourpressure[k])        )
    cpdef inline double return_wsurf_v1(self, numpy.int64_t k) noexcept nogil:
        if isinf(self.parameters.control.ktschnee):
            return inf
        return self.parameters.control.ktschnee * (self.sequences.aides.temps[k] - self.sequences.fluxes.tempssurface[k])
    cpdef inline double return_temps_v1(self, numpy.int64_t k) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        if self.sequences.states.waes[k] > 0.0:
            d_ice = self.parameters.fixed.cpeis * self.sequences.states.wats[k]
            d_water = self.parameters.fixed.cpwasser * (self.sequences.states.waes[k] - self.sequences.states.wats[k])
            return max(self.sequences.states.esnow[k] / (d_ice + d_water), -273.0)
        return nan
    cpdef inline double return_wg_v1(self, numpy.int64_t k) noexcept nogil:
        cdef double d_temp
        if self.sequences.states.waes[k] > 0.0:
            d_temp = self.sequences.aides.temps[k]
        else:
            d_temp = self.sequences.fluxes.tkor[k]
        return self.parameters.fixed.lambdag * (self.sequences.fluxes.tz[k] - d_temp) / self.parameters.fixed.z
    cpdef inline double return_backwardeulererror_v1(self, double esnow) noexcept nogil:
        cdef double d_esnow_old
        cdef numpy.int64_t k
        k = self.idx_hru
        if self.sequences.states.waes[k] > 0.0:
            d_esnow_old = self.sequences.states.esnow[k]
            self.sequences.states.esnow[k] = esnow
            self.sequences.aides.temps[k] = self.return_temps_v1(k)
            self.sequences.states.esnow[k] = d_esnow_old
            self.return_tempssurface_v1(k)
            self.sequences.fluxes.wg[k] = self.return_wg_v1(k)
            return d_esnow_old - esnow + self.sequences.fluxes.wg[k] - self.sequences.fluxes.wsurf[k]
        return nan
    cpdef inline double return_esnow_v1(self, numpy.int64_t k, double temps) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        d_ice = self.parameters.fixed.cpeis * self.sequences.states.wats[k]
        d_water = self.parameters.fixed.cpwasser * (self.sequences.states.waes[k] - self.sequences.states.wats[k])
        return temps * (d_ice + d_water)
    cpdef inline double return_tempssurface_v1(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.waes[k] > 0.0:
            if isinf(self.parameters.control.ktschnee):
                self.idx_hru = k
                self.return_energygainsnowsurface_v1(self.sequences.aides.temps[k])
                self.sequences.fluxes.wsurf[k] = (                    self.sequences.fluxes.wsenssnow[k] + self.sequences.fluxes.wlatsnow[k] - self.sequences.fluxes.netradiationsnow[k]                )
            else:
                self.idx_hru = k
                self.pegasustempssurface.find_x(-50.0, 0.0, -100.0, 0.0, 0.0, 1e-8, 10)
                self.sequences.fluxes.wsurf[k] = self.sequences.fluxes.wsurf[k] - (self.return_energygainsnowsurface_v1(                    self.sequences.fluxes.tempssurface[k]                ))
        else:
            self.sequences.fluxes.tempssurface[k] = nan
            self.sequences.fluxes.saturationvapourpressuresnow[k] = 0.0
            self.sequences.fluxes.wsenssnow[k] = 0.0
            self.sequences.fluxes.wlatsnow[k] = 0.0
            self.sequences.fluxes.wsurf[k] = 0.0
        return self.sequences.fluxes.tempssurface[k]
    cpdef inline double return_sg_v1(self, double k, double s, double qz, double dt) noexcept nogil:
        if k <= 0.0:
            return 0.0
        if isinf(k):
            return s + qz
        return k * qz - (k * qz - s) * exp(-dt / k)
    cpdef inline void calc_bowa_default_v1(self) noexcept nogil:
        cdef double d_factor
        cdef double d_rvl
        cdef double d_incr
        cdef double d_decr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.states.bowa[k] = 0.0
            else:
                d_decr = self.sequences.fluxes.qbb[k] + self.sequences.fluxes.qib1[k] + self.sequences.fluxes.qib2[k] + self.sequences.fluxes.qdb[k]
                d_incr = self.sequences.fluxes.wada[k] + self.sequences.fluxes.qkap[k]
                if self.sequences.fluxes.evb[k] > 0.0:
                    d_decr = d_decr + (self.sequences.fluxes.evb[k])
                else:
                    d_incr = d_incr - (self.sequences.fluxes.evb[k])
                if d_decr > self.sequences.states.bowa[k] + d_incr:
                    d_rvl = (self.sequences.states.bowa[k] + d_incr) / d_decr
                    if self.sequences.fluxes.evb[k] > 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (d_rvl)
                    self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] * (d_rvl)
                    self.sequences.fluxes.qib1[k] = self.sequences.fluxes.qib1[k] * (d_rvl)
                    self.sequences.fluxes.qib2[k] = self.sequences.fluxes.qib2[k] * (d_rvl)
                    self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] * (d_rvl)
                    self.sequences.states.bowa[k] = 0.0
                else:
                    self.sequences.states.bowa[k] = (self.sequences.states.bowa[k] + d_incr) - d_decr
                    if self.sequences.states.bowa[k] > self.parameters.control.wmax[k]:
                        d_factor = (self.sequences.states.bowa[k] - self.parameters.control.wmax[k]) / d_incr
                        if self.sequences.fluxes.evb[k] < 0.0:
                            self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (d_factor)
                        self.sequences.fluxes.wada[k] = self.sequences.fluxes.wada[k] * (d_factor)
                        self.sequences.fluxes.qkap[k] = self.sequences.fluxes.qkap[k] * (d_factor)
                        self.sequences.states.bowa[k] = self.parameters.control.wmax[k]
    cpdef inline void calc_bowa_soilmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef double removal
        cdef double demand
        cdef double factor
        cdef double addition
        cdef double supply
        cdef double qbb_soilmodel
        cdef double infiltration
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.states.bowa[k] = 0.0
            else:
                submodel.set_initialsurfacewater(k, self.sequences.fluxes.wada[k])
                submodel.set_actualsurfacewater(k, self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k])
                submodel.set_soilwatersupply(k, 0.0)
                submodel.set_soilwaterdemand(k, 0.0)
                submodel.execute_infiltration(k)
                infiltration = submodel.get_infiltration(k)
                self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + ((self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k]) - infiltration)
                qbb_soilmodel = submodel.get_percolation(k)
                supply = self.sequences.fluxes.qkap[k]
                if self.sequences.fluxes.evb[k] < 0.0:
                    supply = supply - (self.sequences.fluxes.evb[k])
                submodel.set_soilwatersupply(k, supply)
                submodel.add_soilwater(k)
                addition = submodel.get_soilwateraddition(k)
                if addition < supply:
                    factor = addition / supply
                    self.sequences.fluxes.qkap[k] = self.sequences.fluxes.qkap[k] * (factor)
                    if self.sequences.fluxes.evb[k] < 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (factor)
                demand = self.sequences.fluxes.qbb[k] + self.sequences.fluxes.qib1[k] + self.sequences.fluxes.qib2[k]
                if self.sequences.fluxes.evb[k] > 0.0:
                    demand = demand + (self.sequences.fluxes.evb[k])
                submodel.set_soilwaterdemand(k, demand)
                submodel.remove_soilwater(k)
                removal = submodel.get_soilwaterremoval(k)
                if removal < demand:
                    factor = removal / demand
                    self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] * (factor)
                    self.sequences.fluxes.qib1[k] = self.sequences.fluxes.qib1[k] * (factor)
                    self.sequences.fluxes.qib2[k] = self.sequences.fluxes.qib2[k] * (factor)
                    if self.sequences.fluxes.evb[k] > 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (factor)
                self.sequences.states.bowa[k] = submodel.get_soilwatercontent(k)
                self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] + (qbb_soilmodel)
    cpdef inline void calc_evi_inzp_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.evi[k] = submodel.get_waterevaporation(k)
                self.sequences.states.inzp[k] = 0.0
            else:
                self.sequences.fluxes.evi[k] = min(submodel.get_interceptionevaporation(k), self.sequences.states.inzp[k])
                self.sequences.states.inzp[k] = self.sequences.states.inzp[k] - (self.sequences.fluxes.evi[k])
    cpdef inline void calc_evb_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.evb[k] = 0.0
            else:
                self.sequences.fluxes.evb[k] = submodel.get_soilevapotranspiration(k)
    cpdef inline void pass_qa_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qa
    cpdef inline void pick_qz(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx])
    cpdef inline void process_radiationmodel(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            (<masterinterface.MasterInterface>self.radiationmodel).process_radiation()
    cpdef inline void calc_possiblesunshineduration(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.possiblesunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_possiblesunshineduration()
    cpdef inline void calc_sunshineduration(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
        elif self.radiationmodel_typeid == 4:
            self.sequences.factors.sunshineduration = (<masterinterface.MasterInterface>self.radiationmodel).get_sunshineduration()
    cpdef inline void calc_globalradiation(self) noexcept nogil:
        if self.radiationmodel_typeid == 1:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
        elif self.radiationmodel_typeid == 4:
            self.sequences.fluxes.globalradiation = (<masterinterface.MasterInterface>self.radiationmodel).get_globalradiation()
    cpdef inline void calc_qzh(self) noexcept nogil:
        self.sequences.fluxes.qzh = self.sequences.fluxes.qz / self.parameters.derived.qfactor
    cpdef inline void update_loggedsunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedsunshineduration[idx] = self.sequences.logs.loggedsunshineduration[idx - 1]
        self.sequences.logs.loggedsunshineduration[0] = self.sequences.factors.sunshineduration
    cpdef inline void calc_dailysunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailysunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailysunshineduration = self.sequences.fluxes.dailysunshineduration + (self.sequences.logs.loggedsunshineduration[idx])
    cpdef inline void update_loggedpossiblesunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedpossiblesunshineduration[idx] = (                self.sequences.logs.loggedpossiblesunshineduration[idx - 1]            )
        self.sequences.logs.loggedpossiblesunshineduration[0] = self.sequences.factors.possiblesunshineduration
    cpdef inline void calc_dailypossiblesunshineduration(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.dailypossiblesunshineduration = 0.0
        for idx in range(self.parameters.derived.nmblogentries):
            self.sequences.fluxes.dailypossiblesunshineduration = self.sequences.fluxes.dailypossiblesunshineduration + (self.sequences.logs.loggedpossiblesunshineduration[idx])
    cpdef inline void calc_nkor(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.nkor[k] = self.parameters.control.kg[k] * self.sequences.inputs.nied
    cpdef inline void calc_tkor(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.tkor[k] = self.parameters.control.kt[k] + self.sequences.inputs.teml
    cpdef inline void calc_windspeed2m(self) noexcept nogil:
        self.sequences.fluxes.windspeed2m = self.sequences.inputs.windspeed * (            log(2.0 / self.parameters.fixed.z0)            / log(self.parameters.control.measuringheightwindspeed / self.parameters.fixed.z0)        )
    cpdef inline void calc_reducedwindspeed2m(self) noexcept nogil:
        cdef double d_lai
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (LAUBW, MISCHW, NADELW):
                d_lai = self.parameters.control.lai[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]
                self.sequences.fluxes.reducedwindspeed2m[k] = (                    max(self.parameters.control.p1wind - self.parameters.control.p2wind * d_lai, 0.0) * self.sequences.fluxes.windspeed2m                )
            else:
                self.sequences.fluxes.reducedwindspeed2m[k] = self.sequences.fluxes.windspeed2m
    cpdef inline void calc_saturationvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.saturationvapourpressure[k] = self.return_saturationvapourpressure_v1(                self.sequences.fluxes.tkor[k]            )
    cpdef inline void calc_actualvapourpressure(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.actualvapourpressure[k] = (                self.sequences.fluxes.saturationvapourpressure[k] * self.sequences.inputs.relativehumidity / 100.0            )
    cpdef inline void calc_nbes_inzp(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.nbes[k] = 0.0
                self.sequences.states.inzp[k] = 0.0
            else:
                self.sequences.fluxes.nbes[k] = max(                    self.sequences.fluxes.nkor[k]                    + self.sequences.states.inzp[k]                    - self.parameters.derived.kinz[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]],                    0.0,                )
                self.sequences.states.inzp[k] = self.sequences.states.inzp[k] + (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.nbes[k])
    cpdef inline void calc_snratio(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.fluxes.tkor[k] >= (self.parameters.control.tgr[k] + self.parameters.control.tsp[k] / 2.0):
                self.sequences.aides.snratio[k] = 0.0
            elif self.sequences.fluxes.tkor[k] <= (self.parameters.control.tgr[k] - self.parameters.control.tsp[k] / 2.0):
                self.sequences.aides.snratio[k] = 1.0
            else:
                self.sequences.aides.snratio[k] = (                    (self.parameters.control.tgr[k] + self.parameters.control.tsp[k] / 2.0) - self.sequences.fluxes.tkor[k]                ) / self.parameters.control.tsp[k]
    cpdef inline void calc_sbes(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.sbes[k] = self.sequences.aides.snratio[k] * self.sequences.fluxes.nbes[k]
    cpdef inline void calc_wats(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.wats[k] = 0.0
            else:
                self.sequences.states.wats[k] = self.sequences.states.wats[k] + (self.sequences.fluxes.sbes[k])
    cpdef inline void calc_wada_waes(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.waes[k] = 0.0
                self.sequences.fluxes.wada[k] = self.sequences.fluxes.nbes[k]
            else:
                self.sequences.states.waes[k] = self.sequences.states.waes[k] + (self.sequences.fluxes.nbes[k])
                self.sequences.fluxes.wada[k] = max(self.sequences.states.waes[k] - self.parameters.control.pwmax[k] * self.sequences.states.wats[k], 0.0)
                self.sequences.states.waes[k] = self.sequences.states.waes[k] - (self.sequences.fluxes.wada[k])
    cpdef inline void calc_wnied_esnow(self) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.wnied[k] = 0.0
                self.sequences.states.esnow[k] = 0.0
            else:
                d_ice = self.parameters.fixed.cpeis * self.sequences.fluxes.sbes[k]
                d_water = self.parameters.fixed.cpwasser * (self.sequences.fluxes.nbes[k] - self.sequences.fluxes.sbes[k] - self.sequences.fluxes.wada[k])
                self.sequences.fluxes.wnied[k] = (self.sequences.fluxes.tkor[k] - self.parameters.control.trefn[k]) * (d_ice + d_water)
                self.sequences.states.esnow[k] = self.sequences.states.esnow[k] + (self.sequences.fluxes.wnied[k])
    cpdef inline void calc_temps(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.aides.temps[k] = self.return_temps_v1(k)
    cpdef inline void update_taus(self) noexcept nogil:
        cdef double d_r2
        cdef double d_r1
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0:
                if isnan(self.sequences.states.taus[k]):
                    self.sequences.states.taus[k] = 0.0
                d_r1 = exp(                    5000.0 * (1 / 273.15 - 1.0 / (273.15 + self.sequences.aides.temps[k]))                )
                d_r2 = min(d_r1**10, 1.0)
                self.sequences.states.taus[k] = self.sequences.states.taus[k] * (max(1 - 0.1 * self.sequences.fluxes.sbes[k], 0.0))
                self.sequences.states.taus[k] = self.sequences.states.taus[k] + ((d_r1 + d_r2 + 0.03) / 1e6 * self.parameters.derived.seconds)
            else:
                self.sequences.states.taus[k] = nan
    cpdef inline void calc_actualalbedo(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0.0:
                self.sequences.fluxes.actualalbedo[k] = self.parameters.control.albedo0snow * (                    1.0 - self.parameters.control.snowagingfactor * self.sequences.states.taus[k] / (1.0 + self.sequences.states.taus[k])                )
            else:
                self.sequences.fluxes.actualalbedo[k] = nan
    cpdef inline void calc_netshortwaveradiationsnow(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if isnan(self.sequences.fluxes.actualalbedo[k]):
                self.sequences.fluxes.netshortwaveradiationsnow[k] = 0.0
            else:
                self.sequences.fluxes.netshortwaveradiationsnow[k] = (                    self.parameters.derived.fr[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]                    * (1.0 - self.sequences.fluxes.actualalbedo[k])                    * self.sequences.fluxes.globalradiation                )
    cpdef inline void calc_rlatm(self) noexcept nogil:
        cdef double d_t
        cdef numpy.int64_t k
        cdef double d_common
        cdef double d_rs
        d_rs = self.sequences.fluxes.dailysunshineduration / self.sequences.fluxes.dailypossiblesunshineduration
        d_common = self.parameters.fixed.fratm * self.parameters.fixed.sigma * (1.0 + 0.22 * (1.0 - d_rs) ** 2)
        for k in range(self.parameters.control.nhru):
            d_t = self.sequences.fluxes.tkor[k] + 273.15
            self.sequences.aides.rlatm[k] = d_common * (                d_t**4 * (self.sequences.fluxes.actualvapourpressure[k] / d_t) ** (1.0 / 7.0)            )
    cpdef inline void calc_tz(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.tz[k] = nan
            elif self.sequences.states.ebdn[k] < 0.0:
                self.sequences.fluxes.tz[k] = self.sequences.states.ebdn[k] / (2.0 * self.parameters.fixed.z * self.parameters.fixed.cg)
            elif self.sequences.states.ebdn[k] < self.parameters.derived.heatoffusion[k]:
                self.sequences.fluxes.tz[k] = 0.0
            else:
                self.sequences.fluxes.tz[k] = (self.sequences.states.ebdn[k] - self.parameters.derived.heatoffusion[k]) / (2.0 * self.parameters.fixed.z * self.parameters.fixed.cg)
    cpdef inline void calc_wg(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (FLUSS, SEE, WASSER):
                self.sequences.fluxes.wg[k] = 0.0
            else:
                self.sequences.fluxes.wg[k] = self.return_wg_v1(k)
    cpdef inline void calc_schmpot(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0.0:
                self.sequences.fluxes.schmpot[k] = max(self.sequences.states.esnow[k] / self.parameters.fixed.rschmelz, 0.0)
            else:
                self.sequences.fluxes.schmpot[k] = 0.0
    cpdef inline void calc_schm_wats(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.schm[k] = 0.0
            else:
                self.sequences.fluxes.schm[k] = min(self.sequences.fluxes.schmpot[k], self.sequences.states.wats[k])
                self.sequences.states.wats[k] = self.sequences.states.wats[k] - (self.sequences.fluxes.schm[k])
    cpdef inline void calc_gefrpot(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.sequences.states.waes[k] > 0:
                self.sequences.fluxes.gefrpot[k] = max(-self.sequences.states.esnow[k] / self.parameters.fixed.rschmelz, 0)
            else:
                self.sequences.fluxes.gefrpot[k] = 0.0
    cpdef inline void calc_gefr_wats(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE) or not self.parameters.control.refreezeflag:
                self.sequences.fluxes.gefr[k] = 0.0
            else:
                self.sequences.fluxes.gefr[k] = min(self.sequences.fluxes.gefrpot[k], (self.sequences.states.waes[k] - self.sequences.states.wats[k]))
                self.sequences.states.wats[k] = self.sequences.states.wats[k] + (self.sequences.fluxes.gefr[k])
    cpdef inline void calc_evs_waes_wats(self) noexcept nogil:
        cdef double d_frac
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, SEE, FLUSS) or (self.sequences.states.waes[k] <= 0.0):
                self.sequences.fluxes.evs[k] = 0.0
                self.sequences.states.waes[k] = 0.0
                self.sequences.states.wats[k] = 0.0
            else:
                self.sequences.fluxes.evs[k] = min(self.sequences.fluxes.wlatsnow[k] / self.parameters.fixed.lwe, self.sequences.states.waes[k])
                d_frac = (self.sequences.states.waes[k] - self.sequences.fluxes.evs[k]) / self.sequences.states.waes[k]
                self.sequences.states.waes[k] = self.sequences.states.waes[k] * (d_frac)
                self.sequences.states.wats[k] = self.sequences.states.wats[k] * (d_frac)
    cpdef inline void update_wada_waes(self) noexcept nogil:
        cdef double d_wada_corr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] not in (WASSER, FLUSS, SEE):
                d_wada_corr = max(self.sequences.states.waes[k] - self.parameters.control.pwmax[k] * self.sequences.states.wats[k], 0.0)
                self.sequences.fluxes.wada[k] = self.sequences.fluxes.wada[k] + (d_wada_corr)
                self.sequences.states.waes[k] = self.sequences.states.waes[k] - (d_wada_corr)
    cpdef inline void calc_evi_inzp(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_evi_inzp_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_evb(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_evb_aetmodel_v1((<masterinterface.MasterInterface>self.aetmodel))
    cpdef inline void update_ebdn(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.states.ebdn[k] = 0.0
            else:
                self.sequences.states.ebdn[k] = self.sequences.states.ebdn[k] + (self.parameters.control.wg2z[self.parameters.derived.moy[self.idx_sim]] - self.sequences.fluxes.wg[k])
    cpdef inline void calc_sff(self) noexcept nogil:
        cdef double d_sff
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.sff[k] = 0.0
            else:
                d_sff = 1.0 - self.sequences.states.ebdn[k] / (self.parameters.fixed.bowa2z[k] * self.parameters.fixed.rschmelz)
                self.sequences.fluxes.sff[k] = min(max(d_sff, 0.0), 1.0)
    cpdef inline void calc_fvg(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.fvg[k] = 0.0
            else:
                self.sequences.fluxes.fvg[k] = min(self.parameters.control.fvf * self.sequences.fluxes.sff[k] ** self.parameters.control.bsff, 1.0)
    cpdef inline void calc_qkap(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE)) or (self.parameters.control.wmax[k] <= 0.0):
                self.sequences.fluxes.qkap[k] = 0.0
            elif self.sequences.states.bowa[k] <= self.parameters.control.kapgrenz[k, 0]:
                self.sequences.fluxes.qkap[k] = self.parameters.control.kapmax[k]
            elif self.sequences.states.bowa[k] <= self.parameters.control.kapgrenz[k, 1]:
                self.sequences.fluxes.qkap[k] = self.parameters.control.kapmax[k] * (                    1.0                    - (self.sequences.states.bowa[k] - self.parameters.control.kapgrenz[k, 0])                    / (self.parameters.control.kapgrenz[k, 1] - self.parameters.control.kapgrenz[k, 0])                )
            else:
                self.sequences.fluxes.qkap[k] = 0
    cpdef inline void calc_qbb(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (                (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE))                or (self.sequences.states.bowa[k] <= self.parameters.control.pwp[k])                or (self.parameters.control.wmax[k] <= 0.0)            ):
                self.sequences.fluxes.qbb[k] = 0.0
            elif self.sequences.states.bowa[k] <= self.parameters.control.fk[k]:
                if self.parameters.control.rbeta:
                    self.sequences.fluxes.qbb[k] = 0.0
                else:
                    self.sequences.fluxes.qbb[k] = self.parameters.control.beta[k] * (self.sequences.states.bowa[k] - self.parameters.control.pwp[k])
            else:
                self.sequences.fluxes.qbb[k] = (                    self.parameters.control.beta[k]                    * (self.sequences.states.bowa[k] - self.parameters.control.pwp[k])                    * (                        1.0                        + (self.parameters.control.fbeta[k] - 1.0)                        * (self.sequences.states.bowa[k] - self.parameters.control.fk[k])                        / (self.parameters.control.wmax[k] - self.parameters.control.fk[k])                    )                )
    cpdef inline void calc_qib1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE)) or (                self.sequences.states.bowa[k] <= self.parameters.control.pwp[k]            ):
                self.sequences.fluxes.qib1[k] = 0.0
            else:
                self.sequences.fluxes.qib1[k] = self.parameters.control.dmin[k] * (self.sequences.states.bowa[k] / self.parameters.control.wmax[k])
    cpdef inline void calc_qib2(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if (                (self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE))                or (self.sequences.states.bowa[k] <= self.parameters.control.fk[k])                or (self.parameters.control.wmax[k] <= self.parameters.control.fk[k])            ):
                self.sequences.fluxes.qib2[k] = 0.0
            else:
                self.sequences.fluxes.qib2[k] = (self.parameters.control.dmax[k] - self.parameters.control.dmin[k]) * (                    (self.sequences.states.bowa[k] - self.parameters.control.fk[k]) / (self.parameters.control.wmax[k] - self.parameters.control.fk[k])                ) ** 1.5
    cpdef inline void calc_qdb(self) noexcept nogil:
        cdef double d_exz
        cdef double d_sfa
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == WASSER:
                self.sequences.fluxes.qdb[k] = 0.0
            elif (self.parameters.control.lnk[k] in (VERS, FLUSS, SEE)) or (self.parameters.control.wmax[k] <= 0.0):
                self.sequences.fluxes.qdb[k] = self.sequences.fluxes.wada[k]
            else:
                if self.sequences.states.bowa[k] < self.parameters.control.wmax[k]:
                    d_sfa = (1.0 - self.sequences.states.bowa[k] / self.parameters.control.wmax[k]) ** (                        1.0 / (self.parameters.control.bsf[k] + 1.0)                    ) - (self.sequences.fluxes.wada[k] / ((self.parameters.control.bsf[k] + 1.0) * self.parameters.control.wmax[k]))
                else:
                    d_sfa = 0.0
                d_exz = self.sequences.states.bowa[k] + self.sequences.fluxes.wada[k] - self.parameters.control.wmax[k]
                self.sequences.fluxes.qdb[k] = d_exz
                if d_sfa > 0.0:
                    self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + (d_sfa ** (self.parameters.control.bsf[k] + 1.0) * self.parameters.control.wmax[k])
                self.sequences.fluxes.qdb[k] = max(self.sequences.fluxes.qdb[k], 0.0)
    cpdef inline void update_qdb(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + (self.sequences.fluxes.fvg[k] * (self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k]))
    cpdef inline void calc_bowa(self) noexcept nogil:
        if self.soilmodel is None:
            self.calc_bowa_default_v1()
        elif self.soilmodel_typeid == 1:
            self.calc_bowa_soilmodel_v1(                (<masterinterface.MasterInterface>self.soilmodel)            )
    cpdef inline void calc_qbgz(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qbgz = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == SEE:
                self.sequences.fluxes.qbgz = self.sequences.fluxes.qbgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.evi[k]))
            elif self.parameters.control.lnk[k] not in (WASSER, FLUSS, VERS):
                self.sequences.fluxes.qbgz = self.sequences.fluxes.qbgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.qbb[k] - self.sequences.fluxes.qkap[k]))
    cpdef inline void calc_qigz1(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qigz1 = 0.0
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qigz1 = self.sequences.fluxes.qigz1 + (self.parameters.control.fhru[k] * self.sequences.fluxes.qib1[k])
    cpdef inline void calc_qigz2(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qigz2 = 0.0
        for k in range(self.parameters.control.nhru):
            self.sequences.fluxes.qigz2 = self.sequences.fluxes.qigz2 + (self.parameters.control.fhru[k] * self.sequences.fluxes.qib2[k])
    cpdef inline void calc_qdgz(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.qdgz = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == FLUSS:
                self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (self.parameters.control.fhru[k] * (self.sequences.fluxes.nkor[k] - self.sequences.fluxes.evi[k]))
            elif self.parameters.control.lnk[k] not in (WASSER, SEE):
                self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (self.parameters.control.fhru[k] * self.sequences.fluxes.qdb[k])
    cpdef inline void calc_qbga_sbg_qbgz_qdgz(self) noexcept nogil:
        cdef double qbgz
        cdef double tt
        cdef double c2
        cdef double c1
        cdef double st
        cdef double fraction
        cdef double t
        cdef double excess
        cdef double z
        cdef double s0
        cdef double g2
        cdef double g1
        cdef double sm
        cdef double k
        k = self.parameters.derived.kb
        sm = self.parameters.control.gsbmax * self.parameters.control.volbmax
        g1 = self.parameters.control.gsbgrad1
        g2 = self.parameters.control.gsbgrad2
        s0 = self.sequences.old_states.sbg
        z = self.sequences.fluxes.qbgz
        if s0 > sm:
            excess = s0 - sm
            s0 = sm
        else:
            excess = 0.0
        if k == 0.0:
            self.sequences.new_states.sbg = 0.0
            self.sequences.fluxes.qbga = s0 + self.sequences.fluxes.qbgz
        elif z - s0 / k <= g1:
            if isinf(k):
                self.sequences.new_states.sbg = min(s0 + z, sm)
                self.sequences.fluxes.qbga = 0.0
            else:
                if isinf(sm):
                    t = 1.0
                else:
                    fraction = (k * z - sm) / (k * z - s0)
                    if fraction > 0.0:
                        t = -k * log(fraction)
                    else:
                        t = 1.0
                if t < 1.0:
                    self.sequences.new_states.sbg = sm
                    self.sequences.fluxes.qbga = s0 - sm + t * self.sequences.fluxes.qbgz
                    self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t) * sm / k)
                else:
                    self.sequences.new_states.sbg = self.return_sg_v1(k, s0, z, 1.0)
                    self.sequences.fluxes.qbga = s0 - self.sequences.new_states.sbg + self.sequences.fluxes.qbgz
        elif g2 == 0.0:
            self.sequences.fluxes.qbga = s0 / k
            self.sequences.new_states.sbg = s0
        else:
            if isinf(k) and (g2 > g1):
                self.sequences.fluxes.qbga = 0.0
                self.sequences.new_states.sbg = s0 + g2 / ((g2 - g1) / z + 1.0)
            else:
                st = min(k * (z - g1), sm)
                if g1 == g2:
                    t = min((st - s0) / g1, 1.0)
                    self.sequences.fluxes.qbga = t * (g1 * t + 2.0 * s0) / (2.0 * k)
                else:
                    c1 = (g2 - g1) / (g1 - g2 - z)
                    c2 = (g2 * k * z) / (g1 - g2)
                    t = min(k / c1 * log((st + c2) / (s0 + c2)), 1.0)
                    self.sequences.fluxes.qbga = (s0 + c2) * (                        exp(c1 * t / k) - 1.0                    ) / c1 - c2 * t / k
                if t < 1.0:
                    if st == sm:
                        self.sequences.new_states.sbg = sm
                        self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t) * sm / k)
                    else:
                        fraction = (k * z - sm) / (k * z - st)
                        if fraction > 0.0:
                            tt = -k * log(fraction)
                        else:
                            tt = 1.0
                        if t + tt < 1.0:
                            self.sequences.new_states.sbg = sm
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (st - sm + tt * self.sequences.fluxes.qbgz)
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + ((1.0 - t - tt) * sm / k)
                        else:
                            self.sequences.new_states.sbg = self.return_sg_v1(k, st, z, 1.0 - t)
                            self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (st - self.sequences.new_states.sbg + (1.0 - t) * self.sequences.fluxes.qbgz)
                elif g1 == g2:
                    self.sequences.new_states.sbg = s0 + g1
                else:
                    self.sequences.new_states.sbg = (s0 + c2) * exp(1.0 / k * c1) - c2
        qbgz = self.sequences.fluxes.qbgz
        self.sequences.fluxes.qbgz = self.sequences.new_states.sbg - s0 + self.sequences.fluxes.qbga
        self.sequences.fluxes.qdgz = self.sequences.fluxes.qdgz + (qbgz - self.sequences.fluxes.qbgz)
        self.sequences.fluxes.qbga = self.sequences.fluxes.qbga + (excess)
    cpdef inline void calc_qiga1_sig1(self) noexcept nogil:
        self.sequences.new_states.sig1 = self.return_sg_v1(self.parameters.derived.ki1, self.sequences.old_states.sig1, self.sequences.fluxes.qigz1, 1.0)
        self.sequences.fluxes.qiga1 = self.sequences.old_states.sig1 - self.sequences.new_states.sig1 + self.sequences.fluxes.qigz1
    cpdef inline void calc_qiga2_sig2(self) noexcept nogil:
        self.sequences.new_states.sig2 = self.return_sg_v1(self.parameters.derived.ki2, self.sequences.old_states.sig2, self.sequences.fluxes.qigz2, 1.0)
        self.sequences.fluxes.qiga2 = self.sequences.old_states.sig2 - self.sequences.new_states.sig2 + self.sequences.fluxes.qigz2
    cpdef inline void calc_qdgz1_qdgz2(self) noexcept nogil:
        if self.sequences.fluxes.qdgz > self.parameters.control.a2:
            self.sequences.fluxes.qdgz2 = (self.sequences.fluxes.qdgz - self.parameters.control.a2) ** 2 / (self.sequences.fluxes.qdgz + self.parameters.control.a1 - self.parameters.control.a2)
            self.sequences.fluxes.qdgz1 = self.sequences.fluxes.qdgz - self.sequences.fluxes.qdgz2
        else:
            self.sequences.fluxes.qdgz2 = 0.0
            self.sequences.fluxes.qdgz1 = self.sequences.fluxes.qdgz
    cpdef inline void calc_qdga1_sdg1(self) noexcept nogil:
        self.sequences.new_states.sdg1 = self.return_sg_v1(self.parameters.derived.kd1, self.sequences.old_states.sdg1, self.sequences.fluxes.qdgz1, 1.0)
        self.sequences.fluxes.qdga1 = self.sequences.old_states.sdg1 - self.sequences.new_states.sdg1 + self.sequences.fluxes.qdgz1
    cpdef inline void calc_qdga2_sdg2(self) noexcept nogil:
        self.sequences.new_states.sdg2 = self.return_sg_v1(self.parameters.derived.kd2, self.sequences.old_states.sdg2, self.sequences.fluxes.qdgz2, 1.0)
        self.sequences.fluxes.qdga2 = self.sequences.old_states.sdg2 - self.sequences.new_states.sdg2 + self.sequences.fluxes.qdgz2
    cpdef inline void calc_qah(self) noexcept nogil:
        cdef double d_epw
        cdef numpy.int64_t k
        cdef double d_area
        self.sequences.fluxes.qah = self.sequences.fluxes.qzh + self.sequences.fluxes.qbga + self.sequences.fluxes.qiga1 + self.sequences.fluxes.qiga2 + self.sequences.fluxes.qdga1 + self.sequences.fluxes.qdga2
        if (not self.parameters.control.negq) and (self.sequences.fluxes.qah < 0.0):
            d_area = 0.0
            for k in range(self.parameters.control.nhru):
                if self.parameters.control.lnk[k] in (FLUSS, SEE):
                    d_area = d_area + (self.parameters.control.fhru[k])
            if d_area > 0.0:
                for k in range(self.parameters.control.nhru):
                    if self.parameters.control.lnk[k] in (FLUSS, SEE):
                        self.sequences.fluxes.evi[k] = self.sequences.fluxes.evi[k] + (self.sequences.fluxes.qah / d_area)
            self.sequences.fluxes.qah = 0.0
        d_epw = 0.0
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] == WASSER:
                self.sequences.fluxes.qah = self.sequences.fluxes.qah + (self.parameters.control.fhru[k] * self.sequences.fluxes.nkor[k])
                d_epw = d_epw + (self.parameters.control.fhru[k] * self.sequences.fluxes.evi[k])
        if (self.sequences.fluxes.qah > d_epw) or self.parameters.control.negq:
            self.sequences.fluxes.qah = self.sequences.fluxes.qah - (d_epw)
        elif d_epw > 0.0:
            for k in range(self.parameters.control.nhru):
                if self.parameters.control.lnk[k] == WASSER:
                    self.sequences.fluxes.evi[k] = self.sequences.fluxes.evi[k] * (self.sequences.fluxes.qah / d_epw)
            self.sequences.fluxes.qah = 0.0
    cpdef inline void calc_qa(self) noexcept nogil:
        self.sequences.fluxes.qa = self.parameters.derived.qfactor * self.sequences.fluxes.qah
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.tkor[s]
    cpdef double get_meantemperature(self) noexcept nogil:
        return self.sequences.inputs.teml
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.nkor[s]
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.inzp[k]
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.bowa[k]
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.wats[k] > 0.0:
            return 1.0
        return 0.0
    cpdef double get_snowalbedo(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.fluxes.actualalbedo[k]
    cpdef inline double return_netlongwaveradiationsnow(self, numpy.int64_t k) noexcept nogil:
        cdef double d_fr
        cdef double d_counter
        cdef double d_temp
        d_temp = self.sequences.fluxes.tkor[k] + 273.15
        d_counter = self.sequences.aides.rlatm[k]
        if self.parameters.control.lnk[k] in (LAUBW, MISCHW, NADELW):
            d_fr = self.parameters.derived.fr[self.parameters.control.lnk[k] - 1, self.parameters.derived.moy[self.idx_sim]]
            d_counter = d_fr * d_counter + (1.0 - d_fr) * 0.97 * self.parameters.fixed.sigma * d_temp**4
        return self.parameters.fixed.sigma * (self.sequences.fluxes.tempssurface[k] + 273.15) ** 4 - d_counter
    cpdef inline double return_energygainsnowsurface(self, double tempssurface) noexcept nogil:
        cdef numpy.int64_t k
        k = self.idx_hru
        self.sequences.fluxes.tempssurface[k] = tempssurface
        self.sequences.fluxes.saturationvapourpressuresnow[k] = self.return_saturationvapourpressure_v1(            self.sequences.fluxes.tempssurface[k]        )
        self.sequences.fluxes.wlatsnow[k] = self.return_wlatsnow_v1(k)
        self.sequences.fluxes.wsenssnow[k] = self.return_wsenssnow_v1(k)
        self.sequences.fluxes.netlongwaveradiationsnow[k] = self.return_netlongwaveradiationsnow_v1(k)
        self.sequences.fluxes.netradiationsnow[k] = self.return_netradiation_v1(            self.sequences.fluxes.netshortwaveradiationsnow[k], self.sequences.fluxes.netlongwaveradiationsnow[k]        )
        self.sequences.fluxes.wsurf[k] = self.return_wsurf_v1(k)
        return (            self.sequences.fluxes.wsurf[k] + self.sequences.fluxes.netradiationsnow[k] - self.sequences.fluxes.wsenssnow[k] - self.sequences.fluxes.wlatsnow[k]        )
    cpdef inline double return_saturationvapourpressure(self, double temperature) noexcept nogil:
        return 6.1078 * 2.71828 ** (17.08085 * temperature / (temperature + 234.175))
    cpdef inline double return_netradiation(self, double netshortwaveradiation, double netlongwaveradiation) noexcept nogil:
        return netshortwaveradiation - netlongwaveradiation
    cpdef inline double return_wsenssnow(self, numpy.int64_t k) noexcept nogil:
        return (self.parameters.control.turb0 + self.parameters.control.turb1 * self.sequences.fluxes.reducedwindspeed2m[k]) * (            self.sequences.fluxes.tempssurface[k] - self.sequences.fluxes.tkor[k]        )
    cpdef inline double return_wlatsnow(self, numpy.int64_t k) noexcept nogil:
        return (            (self.parameters.control.turb0 + self.parameters.control.turb1 * self.sequences.fluxes.reducedwindspeed2m[k])            * self.parameters.fixed.psyinv            * (self.sequences.fluxes.saturationvapourpressuresnow[k] - self.sequences.fluxes.actualvapourpressure[k])        )
    cpdef inline double return_wsurf(self, numpy.int64_t k) noexcept nogil:
        if isinf(self.parameters.control.ktschnee):
            return inf
        return self.parameters.control.ktschnee * (self.sequences.aides.temps[k] - self.sequences.fluxes.tempssurface[k])
    cpdef inline double return_temps(self, numpy.int64_t k) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        if self.sequences.states.waes[k] > 0.0:
            d_ice = self.parameters.fixed.cpeis * self.sequences.states.wats[k]
            d_water = self.parameters.fixed.cpwasser * (self.sequences.states.waes[k] - self.sequences.states.wats[k])
            return max(self.sequences.states.esnow[k] / (d_ice + d_water), -273.0)
        return nan
    cpdef inline double return_wg(self, numpy.int64_t k) noexcept nogil:
        cdef double d_temp
        if self.sequences.states.waes[k] > 0.0:
            d_temp = self.sequences.aides.temps[k]
        else:
            d_temp = self.sequences.fluxes.tkor[k]
        return self.parameters.fixed.lambdag * (self.sequences.fluxes.tz[k] - d_temp) / self.parameters.fixed.z
    cpdef inline double return_backwardeulererror(self, double esnow) noexcept nogil:
        cdef double d_esnow_old
        cdef numpy.int64_t k
        k = self.idx_hru
        if self.sequences.states.waes[k] > 0.0:
            d_esnow_old = self.sequences.states.esnow[k]
            self.sequences.states.esnow[k] = esnow
            self.sequences.aides.temps[k] = self.return_temps_v1(k)
            self.sequences.states.esnow[k] = d_esnow_old
            self.return_tempssurface_v1(k)
            self.sequences.fluxes.wg[k] = self.return_wg_v1(k)
            return d_esnow_old - esnow + self.sequences.fluxes.wg[k] - self.sequences.fluxes.wsurf[k]
        return nan
    cpdef inline double return_esnow(self, numpy.int64_t k, double temps) noexcept nogil:
        cdef double d_water
        cdef double d_ice
        d_ice = self.parameters.fixed.cpeis * self.sequences.states.wats[k]
        d_water = self.parameters.fixed.cpwasser * (self.sequences.states.waes[k] - self.sequences.states.wats[k])
        return temps * (d_ice + d_water)
    cpdef inline double return_tempssurface(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.waes[k] > 0.0:
            if isinf(self.parameters.control.ktschnee):
                self.idx_hru = k
                self.return_energygainsnowsurface_v1(self.sequences.aides.temps[k])
                self.sequences.fluxes.wsurf[k] = (                    self.sequences.fluxes.wsenssnow[k] + self.sequences.fluxes.wlatsnow[k] - self.sequences.fluxes.netradiationsnow[k]                )
            else:
                self.idx_hru = k
                self.pegasustempssurface.find_x(-50.0, 0.0, -100.0, 0.0, 0.0, 1e-8, 10)
                self.sequences.fluxes.wsurf[k] = self.sequences.fluxes.wsurf[k] - (self.return_energygainsnowsurface_v1(                    self.sequences.fluxes.tempssurface[k]                ))
        else:
            self.sequences.fluxes.tempssurface[k] = nan
            self.sequences.fluxes.saturationvapourpressuresnow[k] = 0.0
            self.sequences.fluxes.wsenssnow[k] = 0.0
            self.sequences.fluxes.wlatsnow[k] = 0.0
            self.sequences.fluxes.wsurf[k] = 0.0
        return self.sequences.fluxes.tempssurface[k]
    cpdef inline double return_sg(self, double k, double s, double qz, double dt) noexcept nogil:
        if k <= 0.0:
            return 0.0
        if isinf(k):
            return s + qz
        return k * qz - (k * qz - s) * exp(-dt / k)
    cpdef inline void calc_bowa_default(self) noexcept nogil:
        cdef double d_factor
        cdef double d_rvl
        cdef double d_incr
        cdef double d_decr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.states.bowa[k] = 0.0
            else:
                d_decr = self.sequences.fluxes.qbb[k] + self.sequences.fluxes.qib1[k] + self.sequences.fluxes.qib2[k] + self.sequences.fluxes.qdb[k]
                d_incr = self.sequences.fluxes.wada[k] + self.sequences.fluxes.qkap[k]
                if self.sequences.fluxes.evb[k] > 0.0:
                    d_decr = d_decr + (self.sequences.fluxes.evb[k])
                else:
                    d_incr = d_incr - (self.sequences.fluxes.evb[k])
                if d_decr > self.sequences.states.bowa[k] + d_incr:
                    d_rvl = (self.sequences.states.bowa[k] + d_incr) / d_decr
                    if self.sequences.fluxes.evb[k] > 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (d_rvl)
                    self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] * (d_rvl)
                    self.sequences.fluxes.qib1[k] = self.sequences.fluxes.qib1[k] * (d_rvl)
                    self.sequences.fluxes.qib2[k] = self.sequences.fluxes.qib2[k] * (d_rvl)
                    self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] * (d_rvl)
                    self.sequences.states.bowa[k] = 0.0
                else:
                    self.sequences.states.bowa[k] = (self.sequences.states.bowa[k] + d_incr) - d_decr
                    if self.sequences.states.bowa[k] > self.parameters.control.wmax[k]:
                        d_factor = (self.sequences.states.bowa[k] - self.parameters.control.wmax[k]) / d_incr
                        if self.sequences.fluxes.evb[k] < 0.0:
                            self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (d_factor)
                        self.sequences.fluxes.wada[k] = self.sequences.fluxes.wada[k] * (d_factor)
                        self.sequences.fluxes.qkap[k] = self.sequences.fluxes.qkap[k] * (d_factor)
                        self.sequences.states.bowa[k] = self.parameters.control.wmax[k]
    cpdef inline void calc_bowa_soilmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef double removal
        cdef double demand
        cdef double factor
        cdef double addition
        cdef double supply
        cdef double qbb_soilmodel
        cdef double infiltration
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.states.bowa[k] = 0.0
            else:
                submodel.set_initialsurfacewater(k, self.sequences.fluxes.wada[k])
                submodel.set_actualsurfacewater(k, self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k])
                submodel.set_soilwatersupply(k, 0.0)
                submodel.set_soilwaterdemand(k, 0.0)
                submodel.execute_infiltration(k)
                infiltration = submodel.get_infiltration(k)
                self.sequences.fluxes.qdb[k] = self.sequences.fluxes.qdb[k] + ((self.sequences.fluxes.wada[k] - self.sequences.fluxes.qdb[k]) - infiltration)
                qbb_soilmodel = submodel.get_percolation(k)
                supply = self.sequences.fluxes.qkap[k]
                if self.sequences.fluxes.evb[k] < 0.0:
                    supply = supply - (self.sequences.fluxes.evb[k])
                submodel.set_soilwatersupply(k, supply)
                submodel.add_soilwater(k)
                addition = submodel.get_soilwateraddition(k)
                if addition < supply:
                    factor = addition / supply
                    self.sequences.fluxes.qkap[k] = self.sequences.fluxes.qkap[k] * (factor)
                    if self.sequences.fluxes.evb[k] < 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (factor)
                demand = self.sequences.fluxes.qbb[k] + self.sequences.fluxes.qib1[k] + self.sequences.fluxes.qib2[k]
                if self.sequences.fluxes.evb[k] > 0.0:
                    demand = demand + (self.sequences.fluxes.evb[k])
                submodel.set_soilwaterdemand(k, demand)
                submodel.remove_soilwater(k)
                removal = submodel.get_soilwaterremoval(k)
                if removal < demand:
                    factor = removal / demand
                    self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] * (factor)
                    self.sequences.fluxes.qib1[k] = self.sequences.fluxes.qib1[k] * (factor)
                    self.sequences.fluxes.qib2[k] = self.sequences.fluxes.qib2[k] * (factor)
                    if self.sequences.fluxes.evb[k] > 0.0:
                        self.sequences.fluxes.evb[k] = self.sequences.fluxes.evb[k] * (factor)
                self.sequences.states.bowa[k] = submodel.get_soilwatercontent(k)
                self.sequences.fluxes.qbb[k] = self.sequences.fluxes.qbb[k] + (qbb_soilmodel)
    cpdef inline void calc_evi_inzp_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (WASSER, FLUSS, SEE):
                self.sequences.fluxes.evi[k] = submodel.get_waterevaporation(k)
                self.sequences.states.inzp[k] = 0.0
            else:
                self.sequences.fluxes.evi[k] = min(submodel.get_interceptionevaporation(k), self.sequences.states.inzp[k])
                self.sequences.states.inzp[k] = self.sequences.states.inzp[k] - (self.sequences.fluxes.evi[k])
    cpdef inline void calc_evb_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nhru):
            if self.parameters.control.lnk[k] in (VERS, WASSER, FLUSS, SEE):
                self.sequences.fluxes.evb[k] = 0.0
            else:
                self.sequences.fluxes.evb[k] = submodel.get_soilevapotranspiration(k)
    cpdef inline void pass_qa(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qa
