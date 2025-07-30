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

cdef public numpy.int64_t SAND = 1
cdef public numpy.int64_t LOAMY_SAND = 2
cdef public numpy.int64_t SANDY_LOAM = 3
cdef public numpy.int64_t SILT_LOAM = 4
cdef public numpy.int64_t LOAM = 5
cdef public numpy.int64_t SANDY_CLAY_LOAM = 6
cdef public numpy.int64_t SILT_CLAY_LOAM = 7
cdef public numpy.int64_t CLAY_LOAM = 8
cdef public numpy.int64_t SANDY_CLAY = 9
cdef public numpy.int64_t SILTY_CLAY = 10
cdef public numpy.int64_t CLAY = 11
cdef public numpy.int64_t SEALED = 12
cdef public numpy.int64_t FIELD = 13
cdef public numpy.int64_t WINE = 14
cdef public numpy.int64_t ORCHARD = 15
cdef public numpy.int64_t SOIL = 16
cdef public numpy.int64_t PASTURE = 17
cdef public numpy.int64_t WETLAND = 18
cdef public numpy.int64_t TREES = 19
cdef public numpy.int64_t CONIFER = 20
cdef public numpy.int64_t DECIDIOUS = 21
cdef public numpy.int64_t MIXED = 22
cdef public numpy.int64_t WATER = 23
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
cdef class SolverParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._t_inputflag:
            self.t = self._t_inputpointer[0]
        elif self._t_diskflag_reading:
            self.t = self._t_ncarray[0]
        elif self._t_ramflag:
            self.t = self._t_array[idx]
        if self._p_inputflag:
            self.p = self._p_inputpointer[0]
        elif self._p_diskflag_reading:
            self.p = self._p_ncarray[0]
        elif self._p_ramflag:
            self.p = self._p_array[idx]
        if self._fxg_inputflag:
            self.fxg = self._fxg_inputpointer[0]
        elif self._fxg_diskflag_reading:
            self.fxg = self._fxg_ncarray[0]
        elif self._fxg_ramflag:
            self.fxg = self._fxg_array[idx]
        if self._fxs_inputflag:
            self.fxs = self._fxs_inputpointer[0]
        elif self._fxs_diskflag_reading:
            self.fxs = self._fxs_ncarray[0]
        elif self._fxs_ramflag:
            self.fxs = self._fxs_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._t_diskflag_writing:
            self._t_ncarray[0] = self.t
        if self._t_ramflag:
            self._t_array[idx] = self.t
        if self._p_diskflag_writing:
            self._p_ncarray[0] = self.p
        if self._p_ramflag:
            self._p_array[idx] = self.p
        if self._fxg_diskflag_writing:
            self._fxg_ncarray[0] = self.fxg
        if self._fxg_ramflag:
            self._fxg_array[idx] = self.fxg
        if self._fxs_diskflag_writing:
            self._fxs_ncarray[0] = self.fxs
        if self._fxs_ramflag:
            self._fxs_array[idx] = self.fxs
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "t":
            self._t_inputpointer = value.p_value
        if name == "p":
            self._p_inputpointer = value.p_value
        if name == "fxg":
            self._fxg_inputpointer = value.p_value
        if name == "fxs":
            self._fxs_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dhs_diskflag_reading:
            self.dhs = self._dhs_ncarray[0]
        elif self._dhs_ramflag:
            self.dhs = self._dhs_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._dhs_diskflag_writing:
            self._dhs_ncarray[0] = self.dhs
        if self._dhs_ramflag:
            self._dhs_array[idx] = self.dhs
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "dhs":
            self._dhs_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._dhs_outputflag:
            self._dhs_outputpointer[0] = self.dhs
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._pc_diskflag_reading:
            self.pc = self._pc_ncarray[0]
        elif self._pc_ramflag:
            self.pc = self._pc_array[idx]
        if self._pe_diskflag_reading:
            k = 0
            for jdx0 in range(self._pe_length_0):
                self.pe[jdx0] = self._pe_ncarray[k]
                k += 1
        elif self._pe_ramflag:
            for jdx0 in range(self._pe_length_0):
                self.pe[jdx0] = self._pe_array[idx, jdx0]
        if self._pet_diskflag_reading:
            k = 0
            for jdx0 in range(self._pet_length_0):
                self.pet[jdx0] = self._pet_ncarray[k]
                k += 1
        elif self._pet_ramflag:
            for jdx0 in range(self._pet_length_0):
                self.pet[jdx0] = self._pet_array[idx, jdx0]
        if self._tf_diskflag_reading:
            k = 0
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_ncarray[k]
                k += 1
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_array[idx, jdx0]
        if self._ei_diskflag_reading:
            k = 0
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_ncarray[k]
                k += 1
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_array[idx, jdx0]
        if self._rf_diskflag_reading:
            k = 0
            for jdx0 in range(self._rf_length_0):
                self.rf[jdx0] = self._rf_ncarray[k]
                k += 1
        elif self._rf_ramflag:
            for jdx0 in range(self._rf_length_0):
                self.rf[jdx0] = self._rf_array[idx, jdx0]
        if self._sf_diskflag_reading:
            k = 0
            for jdx0 in range(self._sf_length_0):
                self.sf[jdx0] = self._sf_ncarray[k]
                k += 1
        elif self._sf_ramflag:
            for jdx0 in range(self._sf_length_0):
                self.sf[jdx0] = self._sf_array[idx, jdx0]
        if self._pm_diskflag_reading:
            k = 0
            for jdx0 in range(self._pm_length_0):
                self.pm[jdx0] = self._pm_ncarray[k]
                k += 1
        elif self._pm_ramflag:
            for jdx0 in range(self._pm_length_0):
                self.pm[jdx0] = self._pm_array[idx, jdx0]
        if self._am_diskflag_reading:
            k = 0
            for jdx0 in range(self._am_length_0):
                self.am[jdx0] = self._am_ncarray[k]
                k += 1
        elif self._am_ramflag:
            for jdx0 in range(self._am_length_0):
                self.am[jdx0] = self._am_array[idx, jdx0]
        if self._ps_diskflag_reading:
            self.ps = self._ps_ncarray[0]
        elif self._ps_ramflag:
            self.ps = self._ps_array[idx]
        if self._pve_diskflag_reading:
            self.pve = self._pve_ncarray[0]
        elif self._pve_ramflag:
            self.pve = self._pve_array[idx]
        if self._pv_diskflag_reading:
            self.pv = self._pv_ncarray[0]
        elif self._pv_ramflag:
            self.pv = self._pv_array[idx]
        if self._pq_diskflag_reading:
            self.pq = self._pq_ncarray[0]
        elif self._pq_ramflag:
            self.pq = self._pq_array[idx]
        if self._etve_diskflag_reading:
            self.etve = self._etve_ncarray[0]
        elif self._etve_ramflag:
            self.etve = self._etve_array[idx]
        if self._etv_diskflag_reading:
            self.etv = self._etv_ncarray[0]
        elif self._etv_ramflag:
            self.etv = self._etv_array[idx]
        if self._es_diskflag_reading:
            self.es = self._es_ncarray[0]
        elif self._es_ramflag:
            self.es = self._es_array[idx]
        if self._et_diskflag_reading:
            self.et = self._et_ncarray[0]
        elif self._et_ramflag:
            self.et = self._et_array[idx]
        if self._gr_diskflag_reading:
            self.gr = self._gr_ncarray[0]
        elif self._gr_ramflag:
            self.gr = self._gr_array[idx]
        if self._fxs_diskflag_reading:
            self.fxs = self._fxs_ncarray[0]
        elif self._fxs_ramflag:
            self.fxs = self._fxs_array[idx]
        if self._fxg_diskflag_reading:
            self.fxg = self._fxg_ncarray[0]
        elif self._fxg_ramflag:
            self.fxg = self._fxg_array[idx]
        if self._cdg_diskflag_reading:
            self.cdg = self._cdg_ncarray[0]
        elif self._cdg_ramflag:
            self.cdg = self._cdg_array[idx]
        if self._fgse_diskflag_reading:
            self.fgse = self._fgse_ncarray[0]
        elif self._fgse_ramflag:
            self.fgse = self._fgse_array[idx]
        if self._fgs_diskflag_reading:
            self.fgs = self._fgs_ncarray[0]
        elif self._fgs_ramflag:
            self.fgs = self._fgs_array[idx]
        if self._fqs_diskflag_reading:
            self.fqs = self._fqs_ncarray[0]
        elif self._fqs_ramflag:
            self.fqs = self._fqs_array[idx]
        if self._rh_diskflag_reading:
            self.rh = self._rh_ncarray[0]
        elif self._rh_ramflag:
            self.rh = self._rh_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._pc_diskflag_writing:
            self._pc_ncarray[0] = self.pc
        if self._pc_ramflag:
            self._pc_array[idx] = self.pc
        if self._pe_diskflag_writing:
            k = 0
            for jdx0 in range(self._pe_length_0):
                self._pe_ncarray[k] = self.pe[jdx0]
                k += 1
        if self._pe_ramflag:
            for jdx0 in range(self._pe_length_0):
                self._pe_array[idx, jdx0] = self.pe[jdx0]
        if self._pet_diskflag_writing:
            k = 0
            for jdx0 in range(self._pet_length_0):
                self._pet_ncarray[k] = self.pet[jdx0]
                k += 1
        if self._pet_ramflag:
            for jdx0 in range(self._pet_length_0):
                self._pet_array[idx, jdx0] = self.pet[jdx0]
        if self._tf_diskflag_writing:
            k = 0
            for jdx0 in range(self._tf_length_0):
                self._tf_ncarray[k] = self.tf[jdx0]
                k += 1
        if self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self._tf_array[idx, jdx0] = self.tf[jdx0]
        if self._ei_diskflag_writing:
            k = 0
            for jdx0 in range(self._ei_length_0):
                self._ei_ncarray[k] = self.ei[jdx0]
                k += 1
        if self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self._ei_array[idx, jdx0] = self.ei[jdx0]
        if self._rf_diskflag_writing:
            k = 0
            for jdx0 in range(self._rf_length_0):
                self._rf_ncarray[k] = self.rf[jdx0]
                k += 1
        if self._rf_ramflag:
            for jdx0 in range(self._rf_length_0):
                self._rf_array[idx, jdx0] = self.rf[jdx0]
        if self._sf_diskflag_writing:
            k = 0
            for jdx0 in range(self._sf_length_0):
                self._sf_ncarray[k] = self.sf[jdx0]
                k += 1
        if self._sf_ramflag:
            for jdx0 in range(self._sf_length_0):
                self._sf_array[idx, jdx0] = self.sf[jdx0]
        if self._pm_diskflag_writing:
            k = 0
            for jdx0 in range(self._pm_length_0):
                self._pm_ncarray[k] = self.pm[jdx0]
                k += 1
        if self._pm_ramflag:
            for jdx0 in range(self._pm_length_0):
                self._pm_array[idx, jdx0] = self.pm[jdx0]
        if self._am_diskflag_writing:
            k = 0
            for jdx0 in range(self._am_length_0):
                self._am_ncarray[k] = self.am[jdx0]
                k += 1
        if self._am_ramflag:
            for jdx0 in range(self._am_length_0):
                self._am_array[idx, jdx0] = self.am[jdx0]
        if self._ps_diskflag_writing:
            self._ps_ncarray[0] = self.ps
        if self._ps_ramflag:
            self._ps_array[idx] = self.ps
        if self._pve_diskflag_writing:
            self._pve_ncarray[0] = self.pve
        if self._pve_ramflag:
            self._pve_array[idx] = self.pve
        if self._pv_diskflag_writing:
            self._pv_ncarray[0] = self.pv
        if self._pv_ramflag:
            self._pv_array[idx] = self.pv
        if self._pq_diskflag_writing:
            self._pq_ncarray[0] = self.pq
        if self._pq_ramflag:
            self._pq_array[idx] = self.pq
        if self._etve_diskflag_writing:
            self._etve_ncarray[0] = self.etve
        if self._etve_ramflag:
            self._etve_array[idx] = self.etve
        if self._etv_diskflag_writing:
            self._etv_ncarray[0] = self.etv
        if self._etv_ramflag:
            self._etv_array[idx] = self.etv
        if self._es_diskflag_writing:
            self._es_ncarray[0] = self.es
        if self._es_ramflag:
            self._es_array[idx] = self.es
        if self._et_diskflag_writing:
            self._et_ncarray[0] = self.et
        if self._et_ramflag:
            self._et_array[idx] = self.et
        if self._gr_diskflag_writing:
            self._gr_ncarray[0] = self.gr
        if self._gr_ramflag:
            self._gr_array[idx] = self.gr
        if self._fxs_diskflag_writing:
            self._fxs_ncarray[0] = self.fxs
        if self._fxs_ramflag:
            self._fxs_array[idx] = self.fxs
        if self._fxg_diskflag_writing:
            self._fxg_ncarray[0] = self.fxg
        if self._fxg_ramflag:
            self._fxg_array[idx] = self.fxg
        if self._cdg_diskflag_writing:
            self._cdg_ncarray[0] = self.cdg
        if self._cdg_ramflag:
            self._cdg_array[idx] = self.cdg
        if self._fgse_diskflag_writing:
            self._fgse_ncarray[0] = self.fgse
        if self._fgse_ramflag:
            self._fgse_array[idx] = self.fgse
        if self._fgs_diskflag_writing:
            self._fgs_ncarray[0] = self.fgs
        if self._fgs_ramflag:
            self._fgs_array[idx] = self.fgs
        if self._fqs_diskflag_writing:
            self._fqs_ncarray[0] = self.fqs
        if self._fqs_ramflag:
            self._fqs_array[idx] = self.fqs
        if self._rh_diskflag_writing:
            self._rh_ncarray[0] = self.rh
        if self._rh_ramflag:
            self._rh_array[idx] = self.rh
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "pc":
            self._pc_outputpointer = value.p_value
        if name == "ps":
            self._ps_outputpointer = value.p_value
        if name == "pve":
            self._pve_outputpointer = value.p_value
        if name == "pv":
            self._pv_outputpointer = value.p_value
        if name == "pq":
            self._pq_outputpointer = value.p_value
        if name == "etve":
            self._etve_outputpointer = value.p_value
        if name == "etv":
            self._etv_outputpointer = value.p_value
        if name == "es":
            self._es_outputpointer = value.p_value
        if name == "et":
            self._et_outputpointer = value.p_value
        if name == "gr":
            self._gr_outputpointer = value.p_value
        if name == "fxs":
            self._fxs_outputpointer = value.p_value
        if name == "fxg":
            self._fxg_outputpointer = value.p_value
        if name == "cdg":
            self._cdg_outputpointer = value.p_value
        if name == "fgse":
            self._fgse_outputpointer = value.p_value
        if name == "fgs":
            self._fgs_outputpointer = value.p_value
        if name == "fqs":
            self._fqs_outputpointer = value.p_value
        if name == "rh":
            self._rh_outputpointer = value.p_value
        if name == "r":
            self._r_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._pc_outputflag:
            self._pc_outputpointer[0] = self.pc
        if self._ps_outputflag:
            self._ps_outputpointer[0] = self.ps
        if self._pve_outputflag:
            self._pve_outputpointer[0] = self.pve
        if self._pv_outputflag:
            self._pv_outputpointer[0] = self.pv
        if self._pq_outputflag:
            self._pq_outputpointer[0] = self.pq
        if self._etve_outputflag:
            self._etve_outputpointer[0] = self.etve
        if self._etv_outputflag:
            self._etv_outputpointer[0] = self.etv
        if self._es_outputflag:
            self._es_outputpointer[0] = self.es
        if self._et_outputflag:
            self._et_outputpointer[0] = self.et
        if self._gr_outputflag:
            self._gr_outputpointer[0] = self.gr
        if self._fxs_outputflag:
            self._fxs_outputpointer[0] = self.fxs
        if self._fxg_outputflag:
            self._fxg_outputpointer[0] = self.fxg
        if self._cdg_outputflag:
            self._cdg_outputpointer[0] = self.cdg
        if self._fgse_outputflag:
            self._fgse_outputpointer[0] = self.fgse
        if self._fgs_outputflag:
            self._fgs_outputpointer[0] = self.fgs
        if self._fqs_outputflag:
            self._fqs_outputpointer[0] = self.fqs
        if self._rh_outputflag:
            self._rh_outputpointer[0] = self.rh
        if self._r_outputflag:
            self._r_outputpointer[0] = self.r
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._ic_diskflag_reading:
            k = 0
            for jdx0 in range(self._ic_length_0):
                self.ic[jdx0] = self._ic_ncarray[k]
                k += 1
        elif self._ic_ramflag:
            for jdx0 in range(self._ic_length_0):
                self.ic[jdx0] = self._ic_array[idx, jdx0]
        if self._sp_diskflag_reading:
            k = 0
            for jdx0 in range(self._sp_length_0):
                self.sp[jdx0] = self._sp_ncarray[k]
                k += 1
        elif self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                self.sp[jdx0] = self._sp_array[idx, jdx0]
        if self._dve_diskflag_reading:
            self.dve = self._dve_ncarray[0]
        elif self._dve_ramflag:
            self.dve = self._dve_array[idx]
        if self._dv_diskflag_reading:
            self.dv = self._dv_ncarray[0]
        elif self._dv_ramflag:
            self.dv = self._dv_array[idx]
        if self._hge_diskflag_reading:
            self.hge = self._hge_ncarray[0]
        elif self._hge_ramflag:
            self.hge = self._hge_array[idx]
        if self._dg_diskflag_reading:
            self.dg = self._dg_ncarray[0]
        elif self._dg_ramflag:
            self.dg = self._dg_array[idx]
        if self._hq_diskflag_reading:
            self.hq = self._hq_ncarray[0]
        elif self._hq_ramflag:
            self.hq = self._hq_array[idx]
        if self._hs_diskflag_reading:
            self.hs = self._hs_ncarray[0]
        elif self._hs_ramflag:
            self.hs = self._hs_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._ic_diskflag_writing:
            k = 0
            for jdx0 in range(self._ic_length_0):
                self._ic_ncarray[k] = self.ic[jdx0]
                k += 1
        if self._ic_ramflag:
            for jdx0 in range(self._ic_length_0):
                self._ic_array[idx, jdx0] = self.ic[jdx0]
        if self._sp_diskflag_writing:
            k = 0
            for jdx0 in range(self._sp_length_0):
                self._sp_ncarray[k] = self.sp[jdx0]
                k += 1
        if self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                self._sp_array[idx, jdx0] = self.sp[jdx0]
        if self._dve_diskflag_writing:
            self._dve_ncarray[0] = self.dve
        if self._dve_ramflag:
            self._dve_array[idx] = self.dve
        if self._dv_diskflag_writing:
            self._dv_ncarray[0] = self.dv
        if self._dv_ramflag:
            self._dv_array[idx] = self.dv
        if self._hge_diskflag_writing:
            self._hge_ncarray[0] = self.hge
        if self._hge_ramflag:
            self._hge_array[idx] = self.hge
        if self._dg_diskflag_writing:
            self._dg_ncarray[0] = self.dg
        if self._dg_ramflag:
            self._dg_array[idx] = self.dg
        if self._hq_diskflag_writing:
            self._hq_ncarray[0] = self.hq
        if self._hq_ramflag:
            self._hq_array[idx] = self.hq
        if self._hs_diskflag_writing:
            self._hs_ncarray[0] = self.hs
        if self._hs_ramflag:
            self._hs_array[idx] = self.hs
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "dve":
            self._dve_outputpointer = value.p_value
        if name == "dv":
            self._dv_outputpointer = value.p_value
        if name == "hge":
            self._hge_outputpointer = value.p_value
        if name == "dg":
            self._dg_outputpointer = value.p_value
        if name == "hq":
            self._hq_outputpointer = value.p_value
        if name == "hs":
            self._hs_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._dve_outputflag:
            self._dve_outputpointer[0] = self.dve
        if self._dv_outputflag:
            self._dv_outputpointer[0] = self.dv
        if self._hge_outputflag:
            self._hge_outputpointer[0] = self.hge
        if self._dg_outputflag:
            self._dg_outputpointer[0] = self.dg
        if self._hq_outputflag:
            self._hq_outputpointer[0] = self.hq
        if self._hs_outputflag:
            self._hs_outputpointer[0] = self.hs
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
cdef class NumConsts:
    pass
@cython.final
cdef class NumVars:
    pass
@cython.final
cdef class PegasusDGEq(rootutils.PegasusBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_errordv_v1(x)
@cython.final
cdef class QuadDVEq_V1(quadutils.QuadBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_dvh_v1(x)
@cython.final
cdef class QuadDVEq_V2(quadutils.QuadBase):
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x)  noexcept nogil:
        return self.model.return_dvh_v2(x)
@cython.final
cdef class Model:
    def __init__(self):
        super().__init__()
        self.dischargemodel = None
        self.dischargemodel_is_mainmodel = False
        self.petmodel = None
        self.petmodel_is_mainmodel = False
        self.waterlevelmodel = None
        self.waterlevelmodel_is_mainmodel = False
        self.pegasusdgeq = PegasusDGEq(self)
        self.quaddveq_v1 = QuadDVEq_V1(self)
        self.quaddveq_v2 = QuadDVEq_V2(self)
    def get_dischargemodel(self) -> masterinterface.MasterInterface | None:
        return self.dischargemodel
    def set_dischargemodel(self, dischargemodel: masterinterface.MasterInterface | None) -> None:
        self.dischargemodel = dischargemodel
    def get_petmodel(self) -> masterinterface.MasterInterface | None:
        return self.petmodel
    def set_petmodel(self, petmodel: masterinterface.MasterInterface | None) -> None:
        self.petmodel = petmodel
    def get_waterlevelmodel(self) -> masterinterface.MasterInterface | None:
        return self.waterlevelmodel
    def set_waterlevelmodel(self, waterlevelmodel: masterinterface.MasterInterface | None) -> None:
        self.waterlevelmodel = waterlevelmodel
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
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.reset_reuseflags()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.reset_reuseflags()
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.load_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.load_data(idx)
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.save_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.save_data(idx)
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0
        for jdx0 in range(self.sequences.states._ic_length_0):
            self.sequences.old_states.ic[jdx0] = self.sequences.new_states.ic[jdx0]
        for jdx0 in range(self.sequences.states._sp_length_0):
            self.sequences.old_states.sp[jdx0] = self.sequences.new_states.sp[jdx0]
        self.sequences.old_states.dve = self.sequences.new_states.dve
        self.sequences.old_states.dv = self.sequences.new_states.dv
        self.sequences.old_states.hge = self.sequences.new_states.hge
        self.sequences.old_states.dg = self.sequences.new_states.dg
        self.sequences.old_states.hq = self.sequences.new_states.hq
        self.sequences.old_states.hs = self.sequences.new_states.hs
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.new2old()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.new2old()
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.new2old()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.update_inlets()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_inlets()
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.update_inlets()
        cdef numpy.int64_t i
        self.calc_pe_pet_v1()
        self.calc_fr_v1()
        self.calc_pm_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.update_outlets()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_outlets()
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.update_outlets()
        self.calc_et_v1()
        self.calc_r_v1()
        self.pass_r_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.update_receivers(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_receivers(idx)
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.update_receivers(idx)
        cdef numpy.int64_t i
        self.pick_hs_v1()
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.update_senders(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_senders(idx)
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.factors.update_outputs()
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.dischargemodel is not None) and not self.dischargemodel_is_mainmodel:
            self.dischargemodel.update_outputs()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_outputs()
        if (self.waterlevelmodel is not None) and not self.waterlevelmodel_is_mainmodel:
            self.waterlevelmodel.update_outputs()
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
        self.calc_fxs_v1()
        self.calc_fxg_v1()
        self.calc_pc_v1()
        self.calc_tf_v1()
        self.calc_ei_v1()
        self.calc_sf_v1()
        self.calc_rf_v1()
        self.calc_am_v1()
        self.calc_ps_v1()
        self.calc_we_w_v1()
        self.calc_pve_pv_v1()
        self.calc_pq_v1()
        self.calc_betae_beta_v1()
        self.calc_etve_etv_v1()
        self.calc_es_v1()
        self.calc_fqs_v1()
        self.calc_fgse_v1()
        self.calc_fgs_v1()
        self.calc_rh_v1()
        self.calc_dveq_v1()
        self.calc_dveq_v2()
        self.calc_dveq_v3()
        self.calc_dveq_v4()
        self.calc_dgeq_v1()
        self.calc_gf_v1()
        self.calc_gr_v1()
        self.calc_cdg_v1()
        self.calc_cdg_v2()
    cpdef inline void calculate_full_terms(self) noexcept nogil:
        self.update_ic_v1()
        self.update_sp_v1()
        self.update_dve_v1()
        self.update_dv_v1()
        self.update_hge_v1()
        self.update_dg_v1()
        self.update_hq_v1()
        self.update_hs_v1()
    cpdef inline void get_point_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states.ic[idx0] = self.sequences.states._ic_points[self.numvars.idx_stage][idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states.sp[idx0] = self.sequences.states._sp_points[self.numvars.idx_stage][idx0]
        self.sequences.states.dve = self.sequences.states._dve_points[self.numvars.idx_stage]
        self.sequences.states.dv = self.sequences.states._dv_points[self.numvars.idx_stage]
        self.sequences.states.hge = self.sequences.states._hge_points[self.numvars.idx_stage]
        self.sequences.states.dg = self.sequences.states._dg_points[self.numvars.idx_stage]
        self.sequences.states.hq = self.sequences.states._hq_points[self.numvars.idx_stage]
        self.sequences.states.hs = self.sequences.states._hs_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states._ic_points[self.numvars.idx_stage][idx0] = self.sequences.states.ic[idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states._sp_points[self.numvars.idx_stage][idx0] = self.sequences.states.sp[idx0]
        self.sequences.states._dve_points[self.numvars.idx_stage] = self.sequences.states.dve
        self.sequences.states._dv_points[self.numvars.idx_stage] = self.sequences.states.dv
        self.sequences.states._hge_points[self.numvars.idx_stage] = self.sequences.states.hge
        self.sequences.states._dg_points[self.numvars.idx_stage] = self.sequences.states.dg
        self.sequences.states._hq_points[self.numvars.idx_stage] = self.sequences.states.hq
        self.sequences.states._hs_points[self.numvars.idx_stage] = self.sequences.states.hs
    cpdef inline void set_result_states(self) noexcept nogil:
        cdef numpy.int64_t idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states._ic_results[self.numvars.idx_method][idx0] = self.sequences.states.ic[idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states._sp_results[self.numvars.idx_method][idx0] = self.sequences.states.sp[idx0]
        self.sequences.states._dve_results[self.numvars.idx_method] = self.sequences.states.dve
        self.sequences.states._dv_results[self.numvars.idx_method] = self.sequences.states.dv
        self.sequences.states._hge_results[self.numvars.idx_method] = self.sequences.states.hge
        self.sequences.states._dg_results[self.numvars.idx_method] = self.sequences.states.dg
        self.sequences.states._hq_results[self.numvars.idx_method] = self.sequences.states.hq
        self.sequences.states._hs_results[self.numvars.idx_method] = self.sequences.states.hs
    cpdef inline void get_sum_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes.pc = self.sequences.fluxes._pc_sum
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes.tf[idx0] = self.sequences.fluxes._tf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes.ei[idx0] = self.sequences.fluxes._ei_sum[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes.rf[idx0] = self.sequences.fluxes._rf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes.sf[idx0] = self.sequences.fluxes._sf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes.am[idx0] = self.sequences.fluxes._am_sum[idx0]
        self.sequences.fluxes.ps = self.sequences.fluxes._ps_sum
        self.sequences.fluxes.pve = self.sequences.fluxes._pve_sum
        self.sequences.fluxes.pv = self.sequences.fluxes._pv_sum
        self.sequences.fluxes.pq = self.sequences.fluxes._pq_sum
        self.sequences.fluxes.etve = self.sequences.fluxes._etve_sum
        self.sequences.fluxes.etv = self.sequences.fluxes._etv_sum
        self.sequences.fluxes.es = self.sequences.fluxes._es_sum
        self.sequences.fluxes.gr = self.sequences.fluxes._gr_sum
        self.sequences.fluxes.fxs = self.sequences.fluxes._fxs_sum
        self.sequences.fluxes.fxg = self.sequences.fluxes._fxg_sum
        self.sequences.fluxes.cdg = self.sequences.fluxes._cdg_sum
        self.sequences.fluxes.fgse = self.sequences.fluxes._fgse_sum
        self.sequences.fluxes.fgs = self.sequences.fluxes._fgs_sum
        self.sequences.fluxes.fqs = self.sequences.fluxes._fqs_sum
        self.sequences.fluxes.rh = self.sequences.fluxes._rh_sum
    cpdef inline void set_point_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._pc_points[self.numvars.idx_stage] = self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_points[self.numvars.idx_stage] = self.sequences.fluxes.ps
        self.sequences.fluxes._pve_points[self.numvars.idx_stage] = self.sequences.fluxes.pve
        self.sequences.fluxes._pv_points[self.numvars.idx_stage] = self.sequences.fluxes.pv
        self.sequences.fluxes._pq_points[self.numvars.idx_stage] = self.sequences.fluxes.pq
        self.sequences.fluxes._etve_points[self.numvars.idx_stage] = self.sequences.fluxes.etve
        self.sequences.fluxes._etv_points[self.numvars.idx_stage] = self.sequences.fluxes.etv
        self.sequences.fluxes._es_points[self.numvars.idx_stage] = self.sequences.fluxes.es
        self.sequences.fluxes._gr_points[self.numvars.idx_stage] = self.sequences.fluxes.gr
        self.sequences.fluxes._fxs_points[self.numvars.idx_stage] = self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_points[self.numvars.idx_stage] = self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_points[self.numvars.idx_stage] = self.sequences.fluxes.cdg
        self.sequences.fluxes._fgse_points[self.numvars.idx_stage] = self.sequences.fluxes.fgse
        self.sequences.fluxes._fgs_points[self.numvars.idx_stage] = self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_points[self.numvars.idx_stage] = self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_points[self.numvars.idx_stage] = self.sequences.fluxes.rh
    cpdef inline void set_result_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._pc_results[self.numvars.idx_method] = self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_results[self.numvars.idx_method] = self.sequences.fluxes.ps
        self.sequences.fluxes._pve_results[self.numvars.idx_method] = self.sequences.fluxes.pve
        self.sequences.fluxes._pv_results[self.numvars.idx_method] = self.sequences.fluxes.pv
        self.sequences.fluxes._pq_results[self.numvars.idx_method] = self.sequences.fluxes.pq
        self.sequences.fluxes._etve_results[self.numvars.idx_method] = self.sequences.fluxes.etve
        self.sequences.fluxes._etv_results[self.numvars.idx_method] = self.sequences.fluxes.etv
        self.sequences.fluxes._es_results[self.numvars.idx_method] = self.sequences.fluxes.es
        self.sequences.fluxes._gr_results[self.numvars.idx_method] = self.sequences.fluxes.gr
        self.sequences.fluxes._fxs_results[self.numvars.idx_method] = self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_results[self.numvars.idx_method] = self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_results[self.numvars.idx_method] = self.sequences.fluxes.cdg
        self.sequences.fluxes._fgse_results[self.numvars.idx_method] = self.sequences.fluxes.fgse
        self.sequences.fluxes._fgs_results[self.numvars.idx_method] = self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_results[self.numvars.idx_method] = self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_results[self.numvars.idx_method] = self.sequences.fluxes.rh
    cpdef inline void integrate_fluxes(self) noexcept nogil:
        cdef numpy.int64_t jdx, idx0
        self.sequences.fluxes.pc = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pc = self.sequences.fluxes.pc +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pc_points[jdx]
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes.tf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.tf[idx0] = self.sequences.fluxes.tf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._tf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes.ei[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.ei[idx0] = self.sequences.fluxes.ei[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._ei_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes.rf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.rf[idx0] = self.sequences.fluxes.rf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._rf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes.sf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.sf[idx0] = self.sequences.fluxes.sf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._sf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes.am[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.am[idx0] = self.sequences.fluxes.am[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._am_points[jdx, idx0]
        self.sequences.fluxes.ps = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.ps = self.sequences.fluxes.ps +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._ps_points[jdx]
        self.sequences.fluxes.pve = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pve = self.sequences.fluxes.pve +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pve_points[jdx]
        self.sequences.fluxes.pv = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pv = self.sequences.fluxes.pv +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pv_points[jdx]
        self.sequences.fluxes.pq = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pq = self.sequences.fluxes.pq +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pq_points[jdx]
        self.sequences.fluxes.etve = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.etve = self.sequences.fluxes.etve +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._etve_points[jdx]
        self.sequences.fluxes.etv = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.etv = self.sequences.fluxes.etv +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._etv_points[jdx]
        self.sequences.fluxes.es = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.es = self.sequences.fluxes.es +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._es_points[jdx]
        self.sequences.fluxes.gr = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.gr = self.sequences.fluxes.gr +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._gr_points[jdx]
        self.sequences.fluxes.fxs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fxs = self.sequences.fluxes.fxs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fxs_points[jdx]
        self.sequences.fluxes.fxg = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fxg = self.sequences.fluxes.fxg +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fxg_points[jdx]
        self.sequences.fluxes.cdg = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.cdg = self.sequences.fluxes.cdg +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._cdg_points[jdx]
        self.sequences.fluxes.fgse = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fgse = self.sequences.fluxes.fgse +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fgse_points[jdx]
        self.sequences.fluxes.fgs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fgs = self.sequences.fluxes.fgs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fgs_points[jdx]
        self.sequences.fluxes.fqs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fqs = self.sequences.fluxes.fqs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fqs_points[jdx]
        self.sequences.fluxes.rh = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.rh = self.sequences.fluxes.rh +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._rh_points[jdx]
    cpdef inline void reset_sum_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._pc_sum = 0.
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_sum[idx0] = 0.
        self.sequences.fluxes._ps_sum = 0.
        self.sequences.fluxes._pve_sum = 0.
        self.sequences.fluxes._pv_sum = 0.
        self.sequences.fluxes._pq_sum = 0.
        self.sequences.fluxes._etve_sum = 0.
        self.sequences.fluxes._etv_sum = 0.
        self.sequences.fluxes._es_sum = 0.
        self.sequences.fluxes._gr_sum = 0.
        self.sequences.fluxes._fxs_sum = 0.
        self.sequences.fluxes._fxg_sum = 0.
        self.sequences.fluxes._cdg_sum = 0.
        self.sequences.fluxes._fgse_sum = 0.
        self.sequences.fluxes._fgs_sum = 0.
        self.sequences.fluxes._fqs_sum = 0.
        self.sequences.fluxes._rh_sum = 0.
    cpdef inline void addup_fluxes(self) noexcept nogil:
        cdef numpy.int64_t idx0
        self.sequences.fluxes._pc_sum = self.sequences.fluxes._pc_sum + self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_sum[idx0] = self.sequences.fluxes._tf_sum[idx0] + self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_sum[idx0] = self.sequences.fluxes._ei_sum[idx0] + self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_sum[idx0] = self.sequences.fluxes._rf_sum[idx0] + self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_sum[idx0] = self.sequences.fluxes._sf_sum[idx0] + self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_sum[idx0] = self.sequences.fluxes._am_sum[idx0] + self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_sum = self.sequences.fluxes._ps_sum + self.sequences.fluxes.ps
        self.sequences.fluxes._pve_sum = self.sequences.fluxes._pve_sum + self.sequences.fluxes.pve
        self.sequences.fluxes._pv_sum = self.sequences.fluxes._pv_sum + self.sequences.fluxes.pv
        self.sequences.fluxes._pq_sum = self.sequences.fluxes._pq_sum + self.sequences.fluxes.pq
        self.sequences.fluxes._etve_sum = self.sequences.fluxes._etve_sum + self.sequences.fluxes.etve
        self.sequences.fluxes._etv_sum = self.sequences.fluxes._etv_sum + self.sequences.fluxes.etv
        self.sequences.fluxes._es_sum = self.sequences.fluxes._es_sum + self.sequences.fluxes.es
        self.sequences.fluxes._gr_sum = self.sequences.fluxes._gr_sum + self.sequences.fluxes.gr
        self.sequences.fluxes._fxs_sum = self.sequences.fluxes._fxs_sum + self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_sum = self.sequences.fluxes._fxg_sum + self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_sum = self.sequences.fluxes._cdg_sum + self.sequences.fluxes.cdg
        self.sequences.fluxes._fgse_sum = self.sequences.fluxes._fgse_sum + self.sequences.fluxes.fgse
        self.sequences.fluxes._fgs_sum = self.sequences.fluxes._fgs_sum + self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_sum = self.sequences.fluxes._fqs_sum + self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_sum = self.sequences.fluxes._rh_sum + self.sequences.fluxes.rh
    cpdef inline void calculate_error(self) noexcept nogil:
        cdef numpy.int64_t idx0
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._pc_results[self.numvars.idx_method]-self.sequences.fluxes._pc_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pc_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pc_results[self.numvars.idx_method]))
        for idx0 in range(self.sequences.fluxes._tf_length):
            abserror = fabs(self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._tf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._ei_length):
            abserror = fabs(self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._ei_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._rf_length):
            abserror = fabs(self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._rf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._sf_length):
            abserror = fabs(self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._sf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._am_length):
            abserror = fabs(self.sequences.fluxes._am_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._am_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._am_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._am_results[self.numvars.idx_method, idx0]))
        abserror = fabs(self.sequences.fluxes._ps_results[self.numvars.idx_method]-self.sequences.fluxes._ps_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._ps_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._ps_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._pve_results[self.numvars.idx_method]-self.sequences.fluxes._pve_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pve_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pve_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._pv_results[self.numvars.idx_method]-self.sequences.fluxes._pv_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pv_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pv_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._pq_results[self.numvars.idx_method]-self.sequences.fluxes._pq_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pq_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pq_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._etve_results[self.numvars.idx_method]-self.sequences.fluxes._etve_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._etve_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._etve_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._etv_results[self.numvars.idx_method]-self.sequences.fluxes._etv_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._etv_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._etv_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._es_results[self.numvars.idx_method]-self.sequences.fluxes._es_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._es_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._es_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._gr_results[self.numvars.idx_method]-self.sequences.fluxes._gr_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._gr_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._gr_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fxs_results[self.numvars.idx_method]-self.sequences.fluxes._fxs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fxs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fxs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fxg_results[self.numvars.idx_method]-self.sequences.fluxes._fxg_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fxg_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fxg_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._cdg_results[self.numvars.idx_method]-self.sequences.fluxes._cdg_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._cdg_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._cdg_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fgse_results[self.numvars.idx_method]-self.sequences.fluxes._fgse_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fgse_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fgse_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fgs_results[self.numvars.idx_method]-self.sequences.fluxes._fgs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fgs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fgs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fqs_results[self.numvars.idx_method]-self.sequences.fluxes._fqs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fqs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fqs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._rh_results[self.numvars.idx_method]-self.sequences.fluxes._rh_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._rh_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._rh_results[self.numvars.idx_method]))
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
    cpdef inline void pick_hs_v1(self) noexcept nogil:
        cdef double hs
        cdef double waterlevel
        if self.waterlevelmodel is None:
            self.sequences.factors.dhs = 0.0
        elif self.waterlevelmodel_typeid == 1:
            waterlevel = (<masterinterface.MasterInterface>self.waterlevelmodel).get_waterlevel()
            hs = 1000.0 * (waterlevel - self.parameters.control.bl)
            self.sequences.factors.dhs = hs - self.sequences.new_states.hs
            self.sequences.old_states.hs = self.sequences.new_states.hs = hs
    cpdef inline void calc_pe_pet_v1(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_pe_pet_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_pe_pet_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_fr_v1(self) noexcept nogil:
        if self.sequences.inputs.t >= (self.parameters.control.tt + self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 1.0
        elif self.sequences.inputs.t <= (self.parameters.control.tt - self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 0.0
        else:
            self.sequences.aides.fr = (self.sequences.inputs.t - (self.parameters.control.tt - self.parameters.control.ti / 2.0)) / self.parameters.control.ti
    cpdef inline void calc_pm_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.pm[k] = self.parameters.control.ddf[k] * smoothutils.smooth_logistic2(                self.sequences.inputs.t - self.parameters.control.ddt, self.parameters.derived.rt2            )
        self.sequences.fluxes.pm[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_fxs_v1(self) noexcept nogil:
        if self.sequences.inputs.fxs == 0.0:
            self.sequences.fluxes.fxs = 0.0
        elif self.parameters.control.nu == 1:
            self.sequences.fluxes.fxs = inf
        else:
            self.sequences.fluxes.fxs = self.sequences.inputs.fxs / self.parameters.derived.asr
    cpdef inline void calc_fxg_v1(self) noexcept nogil:
        cdef double ra
        if self.sequences.inputs.fxg == 0.0:
            self.sequences.fluxes.fxg = 0.0
        else:
            ra = self.parameters.derived.agr
            if ra > 0.0:
                self.sequences.fluxes.fxg = self.sequences.inputs.fxg / ra
            else:
                self.sequences.fluxes.fxg = inf
    cpdef inline void calc_pc_v1(self) noexcept nogil:
        self.sequences.fluxes.pc = self.parameters.control.cp * self.sequences.inputs.p
    cpdef inline void calc_tf_v1(self) noexcept nogil:
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            lai = self.parameters.control.lai[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc * smoothutils.smooth_logistic1(                self.sequences.states.ic[k] - self.parameters.control.ih * lai, self.parameters.derived.rh1            )
        self.sequences.fluxes.tf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_ei_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.ei[k] = self.sequences.fluxes.pe[k] * (smoothutils.smooth_logistic1(self.sequences.states.ic[k], self.parameters.derived.rh1))
        self.sequences.fluxes.ei[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_sf_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.sf[k] = (1.0 - self.sequences.aides.fr) * self.sequences.fluxes.tf[k]
        self.sequences.fluxes.sf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_rf_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.rf[k] = self.sequences.aides.fr * self.sequences.fluxes.tf[k]
        self.sequences.fluxes.rf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_am_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.am[k] = self.sequences.fluxes.pm[k] * smoothutils.smooth_logistic1(self.sequences.states.sp[k], self.parameters.derived.rh1)
        self.sequences.fluxes.am[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_ps_v1(self) noexcept nogil:
        self.sequences.fluxes.ps = self.sequences.fluxes.pc
    cpdef inline void calc_we_w_v1(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.aides.we = 0.5 + 0.5 * cos(                min(max(self.sequences.states.dve, 0.0), self.parameters.control.cwe) * self.parameters.fixed.pi / self.parameters.control.cwe            )
        else:
            self.sequences.aides.we = nan
        if self.parameters.derived.nug:
            self.sequences.aides.w = 0.5 + 0.5 * cos(                min(max(self.sequences.states.dv, 0.0), self.parameters.control.cw) * self.parameters.fixed.pi / self.parameters.control.cw            )
        else:
            self.sequences.aides.w = nan
    cpdef inline void calc_pve_pv_v1(self) noexcept nogil:
        cdef double p
        cdef numpy.int64_t k
        self.sequences.fluxes.pve, self.sequences.fluxes.pv = 0.0, 0.0
        for k in range(self.parameters.derived.nul):
            if self.parameters.control.lt[k] != SEALED:
                p = self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k]
                if self.parameters.control.er[k]:
                    self.sequences.fluxes.pve = self.sequences.fluxes.pve + (p * (1.0 - self.sequences.aides.we) * self.parameters.control.aur[k] / self.parameters.derived.agre)
                else:
                    self.sequences.fluxes.pv = self.sequences.fluxes.pv + (p * (1.0 - self.sequences.aides.w) * self.parameters.control.aur[k] / self.parameters.derived.agr)
    cpdef inline void calc_pq_v1(self) noexcept nogil:
        cdef double pq
        cdef numpy.int64_t k
        self.sequences.fluxes.pq = 0.0
        for k in range(self.parameters.derived.nul):
            pq = self.parameters.control.aur[k] / self.parameters.derived.alr * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k])
            if self.parameters.control.lt[k] != SEALED:
                pq = pq * (self.sequences.aides.we if self.parameters.control.er[k] else self.sequences.aides.w)
            self.sequences.fluxes.pq = self.sequences.fluxes.pq + (pq)
    cpdef inline void calc_betae_beta_v1(self) noexcept nogil:
        cdef double temp
        if self.parameters.derived.nuge:
            temp = self.parameters.control.zeta1 * (self.sequences.states.dve - self.parameters.control.zeta2)
            if temp > 700.0:
                self.sequences.aides.betae = 0.0
            else:
                temp = exp(temp)
                self.sequences.aides.betae = 0.5 + 0.5 * (1.0 - temp) / (1.0 + temp)
        else:
            self.sequences.aides.betae = nan
        if self.parameters.derived.nug:
            temp = self.parameters.control.zeta1 * (self.sequences.states.dv - self.parameters.control.zeta2)
            if temp > 700.0:
                self.sequences.aides.beta = 0.0
            else:
                temp = exp(temp)
                self.sequences.aides.beta = 0.5 + 0.5 * (1.0 - temp) / (1.0 + temp)
        else:
            self.sequences.aides.beta = nan
    cpdef inline void calc_etve_etv_v1(self) noexcept nogil:
        cdef double pet
        cdef numpy.int64_t k
        self.sequences.fluxes.etve, self.sequences.fluxes.etv = 0.0, 0.0
        for k in range(self.parameters.derived.nul):
            if (self.parameters.control.lt[k] != SEALED) and (self.sequences.fluxes.pe[k] > 0.0):
                pet = (self.sequences.fluxes.pe[k] - self.sequences.fluxes.ei[k]) / self.sequences.fluxes.pe[k] * self.sequences.fluxes.pet[k]
                if self.parameters.control.er[k]:
                    self.sequences.fluxes.etve = self.sequences.fluxes.etve + (self.parameters.control.aur[k] / self.parameters.derived.agre * pet * self.sequences.aides.betae)
                else:
                    self.sequences.fluxes.etv = self.sequences.fluxes.etv + (self.parameters.control.aur[k] / self.parameters.derived.agr * pet * self.sequences.aides.beta)
    cpdef inline void calc_es_v1(self) noexcept nogil:
        self.sequences.fluxes.es = self.sequences.fluxes.pe[self.parameters.derived.nul] * smoothutils.smooth_logistic1(self.sequences.states.hs, self.parameters.derived.rh1)
    cpdef inline void calc_fqs_v1(self) noexcept nogil:
        if self.parameters.control.nu > 1:
            self.sequences.fluxes.fqs = self.sequences.states.hq / self.parameters.control.cq
        else:
            self.sequences.fluxes.fqs = 0.0
    cpdef inline void calc_fgse_v1(self) noexcept nogil:
        cdef double hg
        cdef double hge
        if self.parameters.derived.nuge:
            hge = self.sequences.states.hge
            hg = 1000.0 * self.parameters.control.gl - self.sequences.states.dg
            self.sequences.fluxes.fgse = fabs(hge - hg) * (hge - hg) / self.parameters.control.cge
        else:
            self.sequences.fluxes.fgse = 0.0
    cpdef inline void calc_fgs_v1(self) noexcept nogil:
        cdef double conductivity
        cdef double excess
        cdef double contactsurface
        cdef double gradient
        cdef double hs
        cdef double hg
        if self.parameters.derived.nug:
            hg = smoothutils.smooth_logistic2(self.parameters.derived.cd - self.sequences.states.dg, self.parameters.derived.rh2)
            hs = smoothutils.smooth_logistic2(self.sequences.states.hs, self.parameters.derived.rh2)
            gradient = (hg if self.parameters.control.rg else self.parameters.derived.cd - self.sequences.states.dg) - hs
            if self.parameters.control.rg:
                contactsurface = fabs(hg - hs)
            else:
                contactsurface = smoothutils.smooth_max1(hg, hs, self.parameters.derived.rh2)
            excess = smoothutils.smooth_max2(                -self.sequences.states.dg, self.sequences.states.hs - self.parameters.derived.cd, 0.0, self.parameters.derived.rh2            )
            conductivity = (1.0 + self.parameters.control.cgf * excess) / self.parameters.control.cg
            self.sequences.fluxes.fgs = gradient * contactsurface * conductivity
        else:
            self.sequences.fluxes.fgs = 0.0
    cpdef inline void calc_rh_v1(self) noexcept nogil:
        if self.dischargemodel is None:
            self.sequences.fluxes.rh = (                self.parameters.derived.asr * (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)                + self.parameters.derived.alr * self.sequences.fluxes.fqs                + self.parameters.derived.agr * self.sequences.fluxes.fgs            )
        elif self.dischargemodel_typeid == 2:
            self.sequences.fluxes.rh = (<masterinterface.MasterInterface>self.dischargemodel).calculate_discharge(self.sequences.states.hs / 1000.0)
    cpdef inline void calc_dveq_v1(self) noexcept nogil:
        if self.parameters.derived.nug:
            if self.sequences.states.dg < self.parameters.control.psiae:
                self.sequences.aides.dveq = 0.0
            else:
                self.sequences.aides.dveq = self.parameters.control.thetas * (                    self.sequences.states.dg                    - self.sequences.states.dg ** (1.0 - 1.0 / self.parameters.control.b)                    / (1.0 - 1.0 / self.parameters.control.b)                    / self.parameters.control.psiae ** (-1.0 / self.parameters.control.b)                    - self.parameters.control.psiae / (1.0 - self.parameters.control.b)                )
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v2(self) noexcept nogil:
        cdef double t2
        cdef double t1
        cdef double x0
        if self.parameters.derived.nug:
            x0 = -10.0 * self.parameters.control.sh
            if self.sequences.states.dg > self.parameters.control.psiae:
                t1 = self.quaddveq_v1.integrate(x0, self.parameters.control.psiae, 2, 20, 1e-8)
                t2 = self.quaddveq_v1.integrate(self.parameters.control.psiae, self.sequences.states.dg, 2, 20, 1e-8)
                self.sequences.aides.dveq = t1 + t2
            else:
                self.sequences.aides.dveq = self.quaddveq_v1.integrate(x0, self.sequences.states.dg, 2, 20, 1e-8)
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v3(self) noexcept nogil:
        if self.parameters.derived.nug:
            if self.sequences.states.dg < self.parameters.control.psiae:
                self.sequences.aides.dveq = self.parameters.control.thetar * self.sequences.states.dg
            else:
                self.sequences.aides.dveq = (self.parameters.control.thetas - self.parameters.control.thetar) * (                    self.sequences.states.dg                    - self.sequences.states.dg ** (1.0 - 1.0 / self.parameters.control.b)                    / (1.0 - 1.0 / self.parameters.control.b)                    / self.parameters.control.psiae ** (-1.0 / self.parameters.control.b)                    - self.parameters.control.psiae / (1.0 - self.parameters.control.b)                ) + self.parameters.control.thetar * self.sequences.states.dg
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v4(self) noexcept nogil:
        cdef double t2
        cdef double t1
        cdef double x0
        if self.parameters.derived.nug:
            x0 = -10.0 * self.parameters.control.sh
            if self.sequences.states.dg > self.parameters.control.psiae:
                t1 = self.quaddveq_v2.integrate(x0, self.parameters.control.psiae, 2, 20, 1e-8)
                t2 = self.quaddveq_v2.integrate(self.parameters.control.psiae, self.sequences.states.dg, 2, 20, 1e-8)
                self.sequences.aides.dveq = t1 + t2
            else:
                self.sequences.aides.dveq = self.quaddveq_v2.integrate(x0, self.sequences.states.dg, 2, 20, 1e-8)
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dgeq_v1(self) noexcept nogil:
        cdef double error
        if self.sequences.states.dv > 0.0:
            error = self.return_errordv_v1(self.parameters.control.psiae)
            if error <= 0.0:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    self.parameters.control.psiae, 10000.0, self.parameters.control.psiae, 1000000.0, 0.0, 1e-8, 20                )
            else:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    0.0, self.parameters.control.psiae, 0.0, self.parameters.control.psiae, 0.0, 1e-8, 20                )
        else:
            self.sequences.aides.dgeq = 0.0
    cpdef inline void calc_gf_v1(self) noexcept nogil:
        self.sequences.aides.gf = smoothutils.smooth_logistic1(self.sequences.states.dg, self.parameters.derived.rh1) / self.return_dvh_v2(            self.sequences.aides.dgeq - self.sequences.states.dg        )
    cpdef inline void calc_gr_v1(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.fluxes.gr = smoothutils.smooth_logistic2(self.parameters.control.ac - self.sequences.states.dve, self.parameters.derived.rh2)
        else:
            self.sequences.fluxes.gr = 0.0
    cpdef inline void calc_cdg_v1(self) noexcept nogil:
        cdef double target
        if self.parameters.derived.nug:
            target = smoothutils.smooth_min1(self.sequences.aides.dveq, self.sequences.states.dg, self.parameters.derived.rh1)
            self.sequences.fluxes.cdg = (self.sequences.states.dv - target) / self.parameters.control.cv
            if self.parameters.control.dgc:
                self.sequences.fluxes.cdg = self.sequences.fluxes.cdg + ((self.sequences.fluxes.fgs - self.sequences.fluxes.fgse - self.sequences.fluxes.fxg) / self.parameters.control.thetas)
        else:
            self.sequences.fluxes.cdg = 0.0
    cpdef inline void calc_cdg_v2(self) noexcept nogil:
        cdef double cdg_fast
        cdef double cdg_slow
        cdef double target
        if self.parameters.derived.nug:
            target = smoothutils.smooth_min1(self.sequences.aides.dveq, self.sequences.states.dg, self.parameters.derived.rh1)
            cdg_slow = (self.sequences.states.dv - target) / self.parameters.control.cv
            cdg_fast = self.sequences.aides.gf * (self.sequences.fluxes.fgs - self.sequences.fluxes.fgse - self.sequences.fluxes.pv - self.sequences.fluxes.fxg)
            self.sequences.fluxes.cdg = cdg_slow + cdg_fast
        else:
            self.sequences.fluxes.cdg = 0.0
    cpdef inline void update_ic_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.new_states.ic[k] = self.sequences.old_states.ic[k] + (self.sequences.fluxes.pc - self.sequences.fluxes.tf[k] - self.sequences.fluxes.ei[k])
        self.sequences.new_states.ic[self.parameters.derived.nul] = 0
    cpdef inline void update_sp_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.new_states.sp[k] = self.sequences.old_states.sp[k] + (self.sequences.fluxes.sf[k] - self.sequences.fluxes.am[k])
        self.sequences.new_states.sp[self.parameters.derived.nul] = 0
    cpdef inline void update_dve_v1(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.new_states.dve = self.sequences.old_states.dve - (self.sequences.fluxes.pve - self.sequences.fluxes.etve - self.sequences.fluxes.gr)
        else:
            self.sequences.new_states.dve = nan
    cpdef inline void update_dv_v1(self) noexcept nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dv = self.sequences.old_states.dv - (                self.sequences.fluxes.fxg + self.sequences.fluxes.pv - self.sequences.fluxes.etv - self.sequences.fluxes.fgs + self.sequences.fluxes.fgse * self.parameters.derived.agre / self.parameters.derived.agr            )
        else:
            self.sequences.new_states.dv = nan
    cpdef inline void update_hge_v1(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.new_states.hge = self.sequences.old_states.hge + (self.sequences.fluxes.gr - self.sequences.fluxes.fgse) / self.parameters.control.thetas
        else:
            self.sequences.new_states.hge = nan
    cpdef inline void update_dg_v1(self) noexcept nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dg = self.sequences.old_states.dg + self.sequences.fluxes.cdg
        else:
            self.sequences.new_states.dg = nan
    cpdef inline void update_hq_v1(self) noexcept nogil:
        self.sequences.new_states.hq = self.sequences.old_states.hq + (self.sequences.fluxes.pq - self.sequences.fluxes.fqs)
    cpdef inline void update_hs_v1(self) noexcept nogil:
        self.sequences.new_states.hs = (            self.sequences.old_states.hs            + (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)            + (self.parameters.derived.alr * self.sequences.fluxes.fqs + self.parameters.derived.agr * self.sequences.fluxes.fgs - self.sequences.fluxes.rh) / self.parameters.derived.asr        )
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_meantemperature_v1(self) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.pc
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.sp[k] > 0.0:
            return 1.0
        return 0.0
    cpdef inline void calc_pe_pet_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialevapotranspiration()
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.pe[k] = self.sequences.fluxes.pet[k] = submodel.get_potentialevapotranspiration(k)
        self.sequences.fluxes.pe[self.parameters.derived.nul] = submodel.get_potentialevapotranspiration(self.parameters.derived.nul)
        self.sequences.fluxes.pet[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_pe_pet_petmodel_v2(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_potentialinterceptionevaporation()
        submodel.determine_potentialsoilevapotranspiration()
        submodel.determine_potentialwaterevaporation()
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.pe[k] = submodel.get_potentialinterceptionevaporation(k)
            self.sequences.fluxes.pet[k] = submodel.get_potentialsoilevapotranspiration(k)
        self.sequences.fluxes.pe[self.parameters.derived.nul] = submodel.get_potentialwaterevaporation(self.parameters.derived.nul)
        self.sequences.fluxes.pet[self.parameters.derived.nul] = 0.0
    cpdef inline double return_errordv_v1(self, double dg) noexcept nogil:
        cdef double d_delta
        cdef double dg_old
        cdef double dveq_old
        dveq_old = self.sequences.aides.dveq
        dg_old = self.sequences.states.dg
        self.sequences.states.dg = dg
        self.calc_dveq_v3()
        d_delta = self.sequences.aides.dveq - self.sequences.states.dv
        self.sequences.aides.dveq = dveq_old
        self.sequences.states.dg = dg_old
        return d_delta
    cpdef inline double return_dvh_v1(self, double h) noexcept nogil:
        h = smoothutils.smooth_max1(h, self.parameters.control.psiae, self.parameters.derived.rh1)
        return self.parameters.control.thetas * (1.0 - (h / self.parameters.control.psiae) ** (-1.0 / self.parameters.control.b))
    cpdef inline double return_dvh_v2(self, double h) noexcept nogil:
        h = smoothutils.smooth_max1(h, self.parameters.control.psiae, self.parameters.derived.rh1)
        return self.parameters.control.thetar + (            (self.parameters.control.thetas - self.parameters.control.thetar) * (1.0 - (h / self.parameters.control.psiae) ** (-1.0 / self.parameters.control.b))        )
    cpdef inline void calc_et_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double ei
        ei = 0.0
        for k in range(self.parameters.derived.nul):
            ei = ei + (self.parameters.control.aur[k] * self.sequences.fluxes.ei[k])
        self.sequences.fluxes.et = ei + self.parameters.derived.agre * self.sequences.fluxes.etve + self.parameters.derived.agr * self.sequences.fluxes.etv + self.parameters.derived.asr * self.sequences.fluxes.es
    cpdef inline void calc_r_v1(self) noexcept nogil:
        self.sequences.fluxes.r = self.parameters.derived.qf * self.sequences.fluxes.rh
    cpdef inline void pass_r_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.r
    cpdef inline void pick_hs(self) noexcept nogil:
        cdef double hs
        cdef double waterlevel
        if self.waterlevelmodel is None:
            self.sequences.factors.dhs = 0.0
        elif self.waterlevelmodel_typeid == 1:
            waterlevel = (<masterinterface.MasterInterface>self.waterlevelmodel).get_waterlevel()
            hs = 1000.0 * (waterlevel - self.parameters.control.bl)
            self.sequences.factors.dhs = hs - self.sequences.new_states.hs
            self.sequences.old_states.hs = self.sequences.new_states.hs = hs
    cpdef inline void calc_pe_pet(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_pe_pet_petmodel_v1(                (<masterinterface.MasterInterface>self.petmodel)            )
        elif self.petmodel_typeid == 2:
            self.calc_pe_pet_petmodel_v2(                (<masterinterface.MasterInterface>self.petmodel)            )
    cpdef inline void calc_fr(self) noexcept nogil:
        if self.sequences.inputs.t >= (self.parameters.control.tt + self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 1.0
        elif self.sequences.inputs.t <= (self.parameters.control.tt - self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 0.0
        else:
            self.sequences.aides.fr = (self.sequences.inputs.t - (self.parameters.control.tt - self.parameters.control.ti / 2.0)) / self.parameters.control.ti
    cpdef inline void calc_pm(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.pm[k] = self.parameters.control.ddf[k] * smoothutils.smooth_logistic2(                self.sequences.inputs.t - self.parameters.control.ddt, self.parameters.derived.rt2            )
        self.sequences.fluxes.pm[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_fxs(self) noexcept nogil:
        if self.sequences.inputs.fxs == 0.0:
            self.sequences.fluxes.fxs = 0.0
        elif self.parameters.control.nu == 1:
            self.sequences.fluxes.fxs = inf
        else:
            self.sequences.fluxes.fxs = self.sequences.inputs.fxs / self.parameters.derived.asr
    cpdef inline void calc_fxg(self) noexcept nogil:
        cdef double ra
        if self.sequences.inputs.fxg == 0.0:
            self.sequences.fluxes.fxg = 0.0
        else:
            ra = self.parameters.derived.agr
            if ra > 0.0:
                self.sequences.fluxes.fxg = self.sequences.inputs.fxg / ra
            else:
                self.sequences.fluxes.fxg = inf
    cpdef inline void calc_pc(self) noexcept nogil:
        self.sequences.fluxes.pc = self.parameters.control.cp * self.sequences.inputs.p
    cpdef inline void calc_tf(self) noexcept nogil:
        cdef double lai
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            lai = self.parameters.control.lai[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc * smoothutils.smooth_logistic1(                self.sequences.states.ic[k] - self.parameters.control.ih * lai, self.parameters.derived.rh1            )
        self.sequences.fluxes.tf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_ei(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.ei[k] = self.sequences.fluxes.pe[k] * (smoothutils.smooth_logistic1(self.sequences.states.ic[k], self.parameters.derived.rh1))
        self.sequences.fluxes.ei[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_sf(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.sf[k] = (1.0 - self.sequences.aides.fr) * self.sequences.fluxes.tf[k]
        self.sequences.fluxes.sf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_rf(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.rf[k] = self.sequences.aides.fr * self.sequences.fluxes.tf[k]
        self.sequences.fluxes.rf[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_am(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.fluxes.am[k] = self.sequences.fluxes.pm[k] * smoothutils.smooth_logistic1(self.sequences.states.sp[k], self.parameters.derived.rh1)
        self.sequences.fluxes.am[self.parameters.derived.nul] = 0.0
    cpdef inline void calc_ps(self) noexcept nogil:
        self.sequences.fluxes.ps = self.sequences.fluxes.pc
    cpdef inline void calc_we_w(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.aides.we = 0.5 + 0.5 * cos(                min(max(self.sequences.states.dve, 0.0), self.parameters.control.cwe) * self.parameters.fixed.pi / self.parameters.control.cwe            )
        else:
            self.sequences.aides.we = nan
        if self.parameters.derived.nug:
            self.sequences.aides.w = 0.5 + 0.5 * cos(                min(max(self.sequences.states.dv, 0.0), self.parameters.control.cw) * self.parameters.fixed.pi / self.parameters.control.cw            )
        else:
            self.sequences.aides.w = nan
    cpdef inline void calc_pve_pv(self) noexcept nogil:
        cdef double p
        cdef numpy.int64_t k
        self.sequences.fluxes.pve, self.sequences.fluxes.pv = 0.0, 0.0
        for k in range(self.parameters.derived.nul):
            if self.parameters.control.lt[k] != SEALED:
                p = self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k]
                if self.parameters.control.er[k]:
                    self.sequences.fluxes.pve = self.sequences.fluxes.pve + (p * (1.0 - self.sequences.aides.we) * self.parameters.control.aur[k] / self.parameters.derived.agre)
                else:
                    self.sequences.fluxes.pv = self.sequences.fluxes.pv + (p * (1.0 - self.sequences.aides.w) * self.parameters.control.aur[k] / self.parameters.derived.agr)
    cpdef inline void calc_pq(self) noexcept nogil:
        cdef double pq
        cdef numpy.int64_t k
        self.sequences.fluxes.pq = 0.0
        for k in range(self.parameters.derived.nul):
            pq = self.parameters.control.aur[k] / self.parameters.derived.alr * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k])
            if self.parameters.control.lt[k] != SEALED:
                pq = pq * (self.sequences.aides.we if self.parameters.control.er[k] else self.sequences.aides.w)
            self.sequences.fluxes.pq = self.sequences.fluxes.pq + (pq)
    cpdef inline void calc_betae_beta(self) noexcept nogil:
        cdef double temp
        if self.parameters.derived.nuge:
            temp = self.parameters.control.zeta1 * (self.sequences.states.dve - self.parameters.control.zeta2)
            if temp > 700.0:
                self.sequences.aides.betae = 0.0
            else:
                temp = exp(temp)
                self.sequences.aides.betae = 0.5 + 0.5 * (1.0 - temp) / (1.0 + temp)
        else:
            self.sequences.aides.betae = nan
        if self.parameters.derived.nug:
            temp = self.parameters.control.zeta1 * (self.sequences.states.dv - self.parameters.control.zeta2)
            if temp > 700.0:
                self.sequences.aides.beta = 0.0
            else:
                temp = exp(temp)
                self.sequences.aides.beta = 0.5 + 0.5 * (1.0 - temp) / (1.0 + temp)
        else:
            self.sequences.aides.beta = nan
    cpdef inline void calc_etve_etv(self) noexcept nogil:
        cdef double pet
        cdef numpy.int64_t k
        self.sequences.fluxes.etve, self.sequences.fluxes.etv = 0.0, 0.0
        for k in range(self.parameters.derived.nul):
            if (self.parameters.control.lt[k] != SEALED) and (self.sequences.fluxes.pe[k] > 0.0):
                pet = (self.sequences.fluxes.pe[k] - self.sequences.fluxes.ei[k]) / self.sequences.fluxes.pe[k] * self.sequences.fluxes.pet[k]
                if self.parameters.control.er[k]:
                    self.sequences.fluxes.etve = self.sequences.fluxes.etve + (self.parameters.control.aur[k] / self.parameters.derived.agre * pet * self.sequences.aides.betae)
                else:
                    self.sequences.fluxes.etv = self.sequences.fluxes.etv + (self.parameters.control.aur[k] / self.parameters.derived.agr * pet * self.sequences.aides.beta)
    cpdef inline void calc_es(self) noexcept nogil:
        self.sequences.fluxes.es = self.sequences.fluxes.pe[self.parameters.derived.nul] * smoothutils.smooth_logistic1(self.sequences.states.hs, self.parameters.derived.rh1)
    cpdef inline void calc_fqs(self) noexcept nogil:
        if self.parameters.control.nu > 1:
            self.sequences.fluxes.fqs = self.sequences.states.hq / self.parameters.control.cq
        else:
            self.sequences.fluxes.fqs = 0.0
    cpdef inline void calc_fgse(self) noexcept nogil:
        cdef double hg
        cdef double hge
        if self.parameters.derived.nuge:
            hge = self.sequences.states.hge
            hg = 1000.0 * self.parameters.control.gl - self.sequences.states.dg
            self.sequences.fluxes.fgse = fabs(hge - hg) * (hge - hg) / self.parameters.control.cge
        else:
            self.sequences.fluxes.fgse = 0.0
    cpdef inline void calc_fgs(self) noexcept nogil:
        cdef double conductivity
        cdef double excess
        cdef double contactsurface
        cdef double gradient
        cdef double hs
        cdef double hg
        if self.parameters.derived.nug:
            hg = smoothutils.smooth_logistic2(self.parameters.derived.cd - self.sequences.states.dg, self.parameters.derived.rh2)
            hs = smoothutils.smooth_logistic2(self.sequences.states.hs, self.parameters.derived.rh2)
            gradient = (hg if self.parameters.control.rg else self.parameters.derived.cd - self.sequences.states.dg) - hs
            if self.parameters.control.rg:
                contactsurface = fabs(hg - hs)
            else:
                contactsurface = smoothutils.smooth_max1(hg, hs, self.parameters.derived.rh2)
            excess = smoothutils.smooth_max2(                -self.sequences.states.dg, self.sequences.states.hs - self.parameters.derived.cd, 0.0, self.parameters.derived.rh2            )
            conductivity = (1.0 + self.parameters.control.cgf * excess) / self.parameters.control.cg
            self.sequences.fluxes.fgs = gradient * contactsurface * conductivity
        else:
            self.sequences.fluxes.fgs = 0.0
    cpdef inline void calc_rh(self) noexcept nogil:
        if self.dischargemodel is None:
            self.sequences.fluxes.rh = (                self.parameters.derived.asr * (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)                + self.parameters.derived.alr * self.sequences.fluxes.fqs                + self.parameters.derived.agr * self.sequences.fluxes.fgs            )
        elif self.dischargemodel_typeid == 2:
            self.sequences.fluxes.rh = (<masterinterface.MasterInterface>self.dischargemodel).calculate_discharge(self.sequences.states.hs / 1000.0)
    cpdef inline void calc_dgeq(self) noexcept nogil:
        cdef double error
        if self.sequences.states.dv > 0.0:
            error = self.return_errordv_v1(self.parameters.control.psiae)
            if error <= 0.0:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    self.parameters.control.psiae, 10000.0, self.parameters.control.psiae, 1000000.0, 0.0, 1e-8, 20                )
            else:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    0.0, self.parameters.control.psiae, 0.0, self.parameters.control.psiae, 0.0, 1e-8, 20                )
        else:
            self.sequences.aides.dgeq = 0.0
    cpdef inline void calc_gf(self) noexcept nogil:
        self.sequences.aides.gf = smoothutils.smooth_logistic1(self.sequences.states.dg, self.parameters.derived.rh1) / self.return_dvh_v2(            self.sequences.aides.dgeq - self.sequences.states.dg        )
    cpdef inline void calc_gr(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.fluxes.gr = smoothutils.smooth_logistic2(self.parameters.control.ac - self.sequences.states.dve, self.parameters.derived.rh2)
        else:
            self.sequences.fluxes.gr = 0.0
    cpdef inline void update_ic(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.new_states.ic[k] = self.sequences.old_states.ic[k] + (self.sequences.fluxes.pc - self.sequences.fluxes.tf[k] - self.sequences.fluxes.ei[k])
        self.sequences.new_states.ic[self.parameters.derived.nul] = 0
    cpdef inline void update_sp(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.derived.nul):
            self.sequences.new_states.sp[k] = self.sequences.old_states.sp[k] + (self.sequences.fluxes.sf[k] - self.sequences.fluxes.am[k])
        self.sequences.new_states.sp[self.parameters.derived.nul] = 0
    cpdef inline void update_dve(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.new_states.dve = self.sequences.old_states.dve - (self.sequences.fluxes.pve - self.sequences.fluxes.etve - self.sequences.fluxes.gr)
        else:
            self.sequences.new_states.dve = nan
    cpdef inline void update_dv(self) noexcept nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dv = self.sequences.old_states.dv - (                self.sequences.fluxes.fxg + self.sequences.fluxes.pv - self.sequences.fluxes.etv - self.sequences.fluxes.fgs + self.sequences.fluxes.fgse * self.parameters.derived.agre / self.parameters.derived.agr            )
        else:
            self.sequences.new_states.dv = nan
    cpdef inline void update_hge(self) noexcept nogil:
        if self.parameters.derived.nuge:
            self.sequences.new_states.hge = self.sequences.old_states.hge + (self.sequences.fluxes.gr - self.sequences.fluxes.fgse) / self.parameters.control.thetas
        else:
            self.sequences.new_states.hge = nan
    cpdef inline void update_dg(self) noexcept nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dg = self.sequences.old_states.dg + self.sequences.fluxes.cdg
        else:
            self.sequences.new_states.dg = nan
    cpdef inline void update_hq(self) noexcept nogil:
        self.sequences.new_states.hq = self.sequences.old_states.hq + (self.sequences.fluxes.pq - self.sequences.fluxes.fqs)
    cpdef inline void update_hs(self) noexcept nogil:
        self.sequences.new_states.hs = (            self.sequences.old_states.hs            + (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)            + (self.parameters.derived.alr * self.sequences.fluxes.fqs + self.parameters.derived.agr * self.sequences.fluxes.fgs - self.sequences.fluxes.rh) / self.parameters.derived.asr        )
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_meantemperature(self) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.pc
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil:
        if self.sequences.states.sp[k] > 0.0:
            return 1.0
        return 0.0
    cpdef inline double return_errordv(self, double dg) noexcept nogil:
        cdef double d_delta
        cdef double dg_old
        cdef double dveq_old
        dveq_old = self.sequences.aides.dveq
        dg_old = self.sequences.states.dg
        self.sequences.states.dg = dg
        self.calc_dveq_v3()
        d_delta = self.sequences.aides.dveq - self.sequences.states.dv
        self.sequences.aides.dveq = dveq_old
        self.sequences.states.dg = dg_old
        return d_delta
    cpdef inline void calc_et(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double ei
        ei = 0.0
        for k in range(self.parameters.derived.nul):
            ei = ei + (self.parameters.control.aur[k] * self.sequences.fluxes.ei[k])
        self.sequences.fluxes.et = ei + self.parameters.derived.agre * self.sequences.fluxes.etve + self.parameters.derived.agr * self.sequences.fluxes.etv + self.parameters.derived.asr * self.sequences.fluxes.es
    cpdef inline void calc_r(self) noexcept nogil:
        self.sequences.fluxes.r = self.parameters.derived.qf * self.sequences.fluxes.rh
    cpdef inline void pass_r(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.r
