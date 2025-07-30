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
cdef public numpy.int64_t FIELD = 1
cdef public numpy.int64_t FOREST = 2
cdef public numpy.int64_t GLACIER = 3
cdef public numpy.int64_t ILAKE = 4
cdef public numpy.int64_t SEALED = 5
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
cdef class InputSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._p_inputflag:
            self.p = self._p_inputpointer[0]
        elif self._p_diskflag_reading:
            self.p = self._p_ncarray[0]
        elif self._p_ramflag:
            self.p = self._p_array[idx]
        if self._t_inputflag:
            self.t = self._t_inputpointer[0]
        elif self._t_diskflag_reading:
            self.t = self._t_ncarray[0]
        elif self._t_ramflag:
            self.t = self._t_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._p_diskflag_writing:
            self._p_ncarray[0] = self.p
        if self._p_ramflag:
            self._p_array[idx] = self.p
        if self._t_diskflag_writing:
            self._t_ncarray[0] = self.t
        if self._t_ramflag:
            self._t_array[idx] = self.t
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "p":
            self._p_inputpointer = value.p_value
        if name == "t":
            self._t_inputpointer = value.p_value
@cython.final
cdef class FactorSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._tc_diskflag_reading:
            k = 0
            for jdx0 in range(self._tc_length_0):
                self.tc[jdx0] = self._tc_ncarray[k]
                k += 1
        elif self._tc_ramflag:
            for jdx0 in range(self._tc_length_0):
                self.tc[jdx0] = self._tc_array[idx, jdx0]
        if self._fracrain_diskflag_reading:
            k = 0
            for jdx0 in range(self._fracrain_length_0):
                self.fracrain[jdx0] = self._fracrain_ncarray[k]
                k += 1
        elif self._fracrain_ramflag:
            for jdx0 in range(self._fracrain_length_0):
                self.fracrain[jdx0] = self._fracrain_array[idx, jdx0]
        if self._rfc_diskflag_reading:
            k = 0
            for jdx0 in range(self._rfc_length_0):
                self.rfc[jdx0] = self._rfc_ncarray[k]
                k += 1
        elif self._rfc_ramflag:
            for jdx0 in range(self._rfc_length_0):
                self.rfc[jdx0] = self._rfc_array[idx, jdx0]
        if self._sfc_diskflag_reading:
            k = 0
            for jdx0 in range(self._sfc_length_0):
                self.sfc[jdx0] = self._sfc_ncarray[k]
                k += 1
        elif self._sfc_ramflag:
            for jdx0 in range(self._sfc_length_0):
                self.sfc[jdx0] = self._sfc_array[idx, jdx0]
        if self._cfact_diskflag_reading:
            k = 0
            for jdx0 in range(self._cfact_length_0):
                self.cfact[jdx0] = self._cfact_ncarray[k]
                k += 1
        elif self._cfact_ramflag:
            for jdx0 in range(self._cfact_length_0):
                self.cfact[jdx0] = self._cfact_array[idx, jdx0]
        if self._swe_diskflag_reading:
            k = 0
            for jdx0 in range(self._swe_length_0):
                for jdx1 in range(self._swe_length_1):
                    self.swe[jdx0, jdx1] = self._swe_ncarray[k]
                    k += 1
        elif self._swe_ramflag:
            for jdx0 in range(self._swe_length_0):
                for jdx1 in range(self._swe_length_1):
                    self.swe[jdx0, jdx1] = self._swe_array[idx, jdx0, jdx1]
        if self._gact_diskflag_reading:
            k = 0
            for jdx0 in range(self._gact_length_0):
                self.gact[jdx0] = self._gact_ncarray[k]
                k += 1
        elif self._gact_ramflag:
            for jdx0 in range(self._gact_length_0):
                self.gact[jdx0] = self._gact_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._tc_diskflag_writing:
            k = 0
            for jdx0 in range(self._tc_length_0):
                self._tc_ncarray[k] = self.tc[jdx0]
                k += 1
        if self._tc_ramflag:
            for jdx0 in range(self._tc_length_0):
                self._tc_array[idx, jdx0] = self.tc[jdx0]
        if self._fracrain_diskflag_writing:
            k = 0
            for jdx0 in range(self._fracrain_length_0):
                self._fracrain_ncarray[k] = self.fracrain[jdx0]
                k += 1
        if self._fracrain_ramflag:
            for jdx0 in range(self._fracrain_length_0):
                self._fracrain_array[idx, jdx0] = self.fracrain[jdx0]
        if self._rfc_diskflag_writing:
            k = 0
            for jdx0 in range(self._rfc_length_0):
                self._rfc_ncarray[k] = self.rfc[jdx0]
                k += 1
        if self._rfc_ramflag:
            for jdx0 in range(self._rfc_length_0):
                self._rfc_array[idx, jdx0] = self.rfc[jdx0]
        if self._sfc_diskflag_writing:
            k = 0
            for jdx0 in range(self._sfc_length_0):
                self._sfc_ncarray[k] = self.sfc[jdx0]
                k += 1
        if self._sfc_ramflag:
            for jdx0 in range(self._sfc_length_0):
                self._sfc_array[idx, jdx0] = self.sfc[jdx0]
        if self._cfact_diskflag_writing:
            k = 0
            for jdx0 in range(self._cfact_length_0):
                self._cfact_ncarray[k] = self.cfact[jdx0]
                k += 1
        if self._cfact_ramflag:
            for jdx0 in range(self._cfact_length_0):
                self._cfact_array[idx, jdx0] = self.cfact[jdx0]
        if self._swe_diskflag_writing:
            k = 0
            for jdx0 in range(self._swe_length_0):
                for jdx1 in range(self._swe_length_1):
                    self._swe_ncarray[k] = self.swe[jdx0, jdx1]
                    k += 1
        if self._swe_ramflag:
            for jdx0 in range(self._swe_length_0):
                for jdx1 in range(self._swe_length_1):
                    self._swe_array[idx, jdx0, jdx1] = self.swe[jdx0, jdx1]
        if self._gact_diskflag_writing:
            k = 0
            for jdx0 in range(self._gact_length_0):
                self._gact_ncarray[k] = self.gact[jdx0]
                k += 1
        if self._gact_ramflag:
            for jdx0 in range(self._gact_length_0):
                self._gact_array[idx, jdx0] = self.gact[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._pc_diskflag_reading:
            k = 0
            for jdx0 in range(self._pc_length_0):
                self.pc[jdx0] = self._pc_ncarray[k]
                k += 1
        elif self._pc_ramflag:
            for jdx0 in range(self._pc_length_0):
                self.pc[jdx0] = self._pc_array[idx, jdx0]
        if self._ei_diskflag_reading:
            k = 0
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_ncarray[k]
                k += 1
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_array[idx, jdx0]
        if self._tf_diskflag_reading:
            k = 0
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_ncarray[k]
                k += 1
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_array[idx, jdx0]
        if self._spl_diskflag_reading:
            k = 0
            for jdx0 in range(self._spl_length_0):
                self.spl[jdx0] = self._spl_ncarray[k]
                k += 1
        elif self._spl_ramflag:
            for jdx0 in range(self._spl_length_0):
                self.spl[jdx0] = self._spl_array[idx, jdx0]
        if self._wcl_diskflag_reading:
            k = 0
            for jdx0 in range(self._wcl_length_0):
                self.wcl[jdx0] = self._wcl_ncarray[k]
                k += 1
        elif self._wcl_ramflag:
            for jdx0 in range(self._wcl_length_0):
                self.wcl[jdx0] = self._wcl_array[idx, jdx0]
        if self._spg_diskflag_reading:
            k = 0
            for jdx0 in range(self._spg_length_0):
                self.spg[jdx0] = self._spg_ncarray[k]
                k += 1
        elif self._spg_ramflag:
            for jdx0 in range(self._spg_length_0):
                self.spg[jdx0] = self._spg_array[idx, jdx0]
        if self._wcg_diskflag_reading:
            k = 0
            for jdx0 in range(self._wcg_length_0):
                self.wcg[jdx0] = self._wcg_ncarray[k]
                k += 1
        elif self._wcg_ramflag:
            for jdx0 in range(self._wcg_length_0):
                self.wcg[jdx0] = self._wcg_array[idx, jdx0]
        if self._glmelt_diskflag_reading:
            k = 0
            for jdx0 in range(self._glmelt_length_0):
                self.glmelt[jdx0] = self._glmelt_ncarray[k]
                k += 1
        elif self._glmelt_ramflag:
            for jdx0 in range(self._glmelt_length_0):
                self.glmelt[jdx0] = self._glmelt_array[idx, jdx0]
        if self._melt_diskflag_reading:
            k = 0
            for jdx0 in range(self._melt_length_0):
                for jdx1 in range(self._melt_length_1):
                    self.melt[jdx0, jdx1] = self._melt_ncarray[k]
                    k += 1
        elif self._melt_ramflag:
            for jdx0 in range(self._melt_length_0):
                for jdx1 in range(self._melt_length_1):
                    self.melt[jdx0, jdx1] = self._melt_array[idx, jdx0, jdx1]
        if self._refr_diskflag_reading:
            k = 0
            for jdx0 in range(self._refr_length_0):
                for jdx1 in range(self._refr_length_1):
                    self.refr[jdx0, jdx1] = self._refr_ncarray[k]
                    k += 1
        elif self._refr_ramflag:
            for jdx0 in range(self._refr_length_0):
                for jdx1 in range(self._refr_length_1):
                    self.refr[jdx0, jdx1] = self._refr_array[idx, jdx0, jdx1]
        if self._in__diskflag_reading:
            k = 0
            for jdx0 in range(self._in__length_0):
                self.in_[jdx0] = self._in__ncarray[k]
                k += 1
        elif self._in__ramflag:
            for jdx0 in range(self._in__length_0):
                self.in_[jdx0] = self._in__array[idx, jdx0]
        if self._r_diskflag_reading:
            k = 0
            for jdx0 in range(self._r_length_0):
                self.r[jdx0] = self._r_ncarray[k]
                k += 1
        elif self._r_ramflag:
            for jdx0 in range(self._r_length_0):
                self.r[jdx0] = self._r_array[idx, jdx0]
        if self._sr_diskflag_reading:
            k = 0
            for jdx0 in range(self._sr_length_0):
                self.sr[jdx0] = self._sr_ncarray[k]
                k += 1
        elif self._sr_ramflag:
            for jdx0 in range(self._sr_length_0):
                self.sr[jdx0] = self._sr_array[idx, jdx0]
        if self._ea_diskflag_reading:
            k = 0
            for jdx0 in range(self._ea_length_0):
                self.ea[jdx0] = self._ea_ncarray[k]
                k += 1
        elif self._ea_ramflag:
            for jdx0 in range(self._ea_length_0):
                self.ea[jdx0] = self._ea_array[idx, jdx0]
        if self._dp_diskflag_reading:
            k = 0
            for jdx0 in range(self._dp_length_0):
                self.dp[jdx0] = self._dp_ncarray[k]
                k += 1
        elif self._dp_ramflag:
            for jdx0 in range(self._dp_length_0):
                self.dp[jdx0] = self._dp_array[idx, jdx0]
        if self._el_diskflag_reading:
            k = 0
            for jdx0 in range(self._el_length_0):
                self.el[jdx0] = self._el_ncarray[k]
                k += 1
        elif self._el_ramflag:
            for jdx0 in range(self._el_length_0):
                self.el[jdx0] = self._el_array[idx, jdx0]
        if self._rs_diskflag_reading:
            k = 0
            for jdx0 in range(self._rs_length_0):
                self.rs[jdx0] = self._rs_ncarray[k]
                k += 1
        elif self._rs_ramflag:
            for jdx0 in range(self._rs_length_0):
                self.rs[jdx0] = self._rs_array[idx, jdx0]
        if self._ri_diskflag_reading:
            k = 0
            for jdx0 in range(self._ri_length_0):
                self.ri[jdx0] = self._ri_ncarray[k]
                k += 1
        elif self._ri_ramflag:
            for jdx0 in range(self._ri_length_0):
                self.ri[jdx0] = self._ri_array[idx, jdx0]
        if self._gr1_diskflag_reading:
            k = 0
            for jdx0 in range(self._gr1_length_0):
                self.gr1[jdx0] = self._gr1_ncarray[k]
                k += 1
        elif self._gr1_ramflag:
            for jdx0 in range(self._gr1_length_0):
                self.gr1[jdx0] = self._gr1_array[idx, jdx0]
        if self._rg1_diskflag_reading:
            k = 0
            for jdx0 in range(self._rg1_length_0):
                self.rg1[jdx0] = self._rg1_ncarray[k]
                k += 1
        elif self._rg1_ramflag:
            for jdx0 in range(self._rg1_length_0):
                self.rg1[jdx0] = self._rg1_array[idx, jdx0]
        if self._gr2_diskflag_reading:
            self.gr2 = self._gr2_ncarray[0]
        elif self._gr2_ramflag:
            self.gr2 = self._gr2_array[idx]
        if self._rg2_diskflag_reading:
            self.rg2 = self._rg2_ncarray[0]
        elif self._rg2_ramflag:
            self.rg2 = self._rg2_array[idx]
        if self._gr3_diskflag_reading:
            self.gr3 = self._gr3_ncarray[0]
        elif self._gr3_ramflag:
            self.gr3 = self._gr3_array[idx]
        if self._rg3_diskflag_reading:
            self.rg3 = self._rg3_ncarray[0]
        elif self._rg3_ramflag:
            self.rg3 = self._rg3_array[idx]
        if self._inrc_diskflag_reading:
            self.inrc = self._inrc_ncarray[0]
        elif self._inrc_ramflag:
            self.inrc = self._inrc_array[idx]
        if self._outrc_diskflag_reading:
            self.outrc = self._outrc_ncarray[0]
        elif self._outrc_ramflag:
            self.outrc = self._outrc_array[idx]
        if self._rt_diskflag_reading:
            self.rt = self._rt_ncarray[0]
        elif self._rt_ramflag:
            self.rt = self._rt_array[idx]
        if self._qt_diskflag_reading:
            self.qt = self._qt_ncarray[0]
        elif self._qt_ramflag:
            self.qt = self._qt_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        cdef numpy.int64_t k
        if self._pc_diskflag_writing:
            k = 0
            for jdx0 in range(self._pc_length_0):
                self._pc_ncarray[k] = self.pc[jdx0]
                k += 1
        if self._pc_ramflag:
            for jdx0 in range(self._pc_length_0):
                self._pc_array[idx, jdx0] = self.pc[jdx0]
        if self._ei_diskflag_writing:
            k = 0
            for jdx0 in range(self._ei_length_0):
                self._ei_ncarray[k] = self.ei[jdx0]
                k += 1
        if self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self._ei_array[idx, jdx0] = self.ei[jdx0]
        if self._tf_diskflag_writing:
            k = 0
            for jdx0 in range(self._tf_length_0):
                self._tf_ncarray[k] = self.tf[jdx0]
                k += 1
        if self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self._tf_array[idx, jdx0] = self.tf[jdx0]
        if self._spl_diskflag_writing:
            k = 0
            for jdx0 in range(self._spl_length_0):
                self._spl_ncarray[k] = self.spl[jdx0]
                k += 1
        if self._spl_ramflag:
            for jdx0 in range(self._spl_length_0):
                self._spl_array[idx, jdx0] = self.spl[jdx0]
        if self._wcl_diskflag_writing:
            k = 0
            for jdx0 in range(self._wcl_length_0):
                self._wcl_ncarray[k] = self.wcl[jdx0]
                k += 1
        if self._wcl_ramflag:
            for jdx0 in range(self._wcl_length_0):
                self._wcl_array[idx, jdx0] = self.wcl[jdx0]
        if self._spg_diskflag_writing:
            k = 0
            for jdx0 in range(self._spg_length_0):
                self._spg_ncarray[k] = self.spg[jdx0]
                k += 1
        if self._spg_ramflag:
            for jdx0 in range(self._spg_length_0):
                self._spg_array[idx, jdx0] = self.spg[jdx0]
        if self._wcg_diskflag_writing:
            k = 0
            for jdx0 in range(self._wcg_length_0):
                self._wcg_ncarray[k] = self.wcg[jdx0]
                k += 1
        if self._wcg_ramflag:
            for jdx0 in range(self._wcg_length_0):
                self._wcg_array[idx, jdx0] = self.wcg[jdx0]
        if self._glmelt_diskflag_writing:
            k = 0
            for jdx0 in range(self._glmelt_length_0):
                self._glmelt_ncarray[k] = self.glmelt[jdx0]
                k += 1
        if self._glmelt_ramflag:
            for jdx0 in range(self._glmelt_length_0):
                self._glmelt_array[idx, jdx0] = self.glmelt[jdx0]
        if self._melt_diskflag_writing:
            k = 0
            for jdx0 in range(self._melt_length_0):
                for jdx1 in range(self._melt_length_1):
                    self._melt_ncarray[k] = self.melt[jdx0, jdx1]
                    k += 1
        if self._melt_ramflag:
            for jdx0 in range(self._melt_length_0):
                for jdx1 in range(self._melt_length_1):
                    self._melt_array[idx, jdx0, jdx1] = self.melt[jdx0, jdx1]
        if self._refr_diskflag_writing:
            k = 0
            for jdx0 in range(self._refr_length_0):
                for jdx1 in range(self._refr_length_1):
                    self._refr_ncarray[k] = self.refr[jdx0, jdx1]
                    k += 1
        if self._refr_ramflag:
            for jdx0 in range(self._refr_length_0):
                for jdx1 in range(self._refr_length_1):
                    self._refr_array[idx, jdx0, jdx1] = self.refr[jdx0, jdx1]
        if self._in__diskflag_writing:
            k = 0
            for jdx0 in range(self._in__length_0):
                self._in__ncarray[k] = self.in_[jdx0]
                k += 1
        if self._in__ramflag:
            for jdx0 in range(self._in__length_0):
                self._in__array[idx, jdx0] = self.in_[jdx0]
        if self._r_diskflag_writing:
            k = 0
            for jdx0 in range(self._r_length_0):
                self._r_ncarray[k] = self.r[jdx0]
                k += 1
        if self._r_ramflag:
            for jdx0 in range(self._r_length_0):
                self._r_array[idx, jdx0] = self.r[jdx0]
        if self._sr_diskflag_writing:
            k = 0
            for jdx0 in range(self._sr_length_0):
                self._sr_ncarray[k] = self.sr[jdx0]
                k += 1
        if self._sr_ramflag:
            for jdx0 in range(self._sr_length_0):
                self._sr_array[idx, jdx0] = self.sr[jdx0]
        if self._ea_diskflag_writing:
            k = 0
            for jdx0 in range(self._ea_length_0):
                self._ea_ncarray[k] = self.ea[jdx0]
                k += 1
        if self._ea_ramflag:
            for jdx0 in range(self._ea_length_0):
                self._ea_array[idx, jdx0] = self.ea[jdx0]
        if self._dp_diskflag_writing:
            k = 0
            for jdx0 in range(self._dp_length_0):
                self._dp_ncarray[k] = self.dp[jdx0]
                k += 1
        if self._dp_ramflag:
            for jdx0 in range(self._dp_length_0):
                self._dp_array[idx, jdx0] = self.dp[jdx0]
        if self._el_diskflag_writing:
            k = 0
            for jdx0 in range(self._el_length_0):
                self._el_ncarray[k] = self.el[jdx0]
                k += 1
        if self._el_ramflag:
            for jdx0 in range(self._el_length_0):
                self._el_array[idx, jdx0] = self.el[jdx0]
        if self._rs_diskflag_writing:
            k = 0
            for jdx0 in range(self._rs_length_0):
                self._rs_ncarray[k] = self.rs[jdx0]
                k += 1
        if self._rs_ramflag:
            for jdx0 in range(self._rs_length_0):
                self._rs_array[idx, jdx0] = self.rs[jdx0]
        if self._ri_diskflag_writing:
            k = 0
            for jdx0 in range(self._ri_length_0):
                self._ri_ncarray[k] = self.ri[jdx0]
                k += 1
        if self._ri_ramflag:
            for jdx0 in range(self._ri_length_0):
                self._ri_array[idx, jdx0] = self.ri[jdx0]
        if self._gr1_diskflag_writing:
            k = 0
            for jdx0 in range(self._gr1_length_0):
                self._gr1_ncarray[k] = self.gr1[jdx0]
                k += 1
        if self._gr1_ramflag:
            for jdx0 in range(self._gr1_length_0):
                self._gr1_array[idx, jdx0] = self.gr1[jdx0]
        if self._rg1_diskflag_writing:
            k = 0
            for jdx0 in range(self._rg1_length_0):
                self._rg1_ncarray[k] = self.rg1[jdx0]
                k += 1
        if self._rg1_ramflag:
            for jdx0 in range(self._rg1_length_0):
                self._rg1_array[idx, jdx0] = self.rg1[jdx0]
        if self._gr2_diskflag_writing:
            self._gr2_ncarray[0] = self.gr2
        if self._gr2_ramflag:
            self._gr2_array[idx] = self.gr2
        if self._rg2_diskflag_writing:
            self._rg2_ncarray[0] = self.rg2
        if self._rg2_ramflag:
            self._rg2_array[idx] = self.rg2
        if self._gr3_diskflag_writing:
            self._gr3_ncarray[0] = self.gr3
        if self._gr3_ramflag:
            self._gr3_array[idx] = self.gr3
        if self._rg3_diskflag_writing:
            self._rg3_ncarray[0] = self.rg3
        if self._rg3_ramflag:
            self._rg3_array[idx] = self.rg3
        if self._inrc_diskflag_writing:
            self._inrc_ncarray[0] = self.inrc
        if self._inrc_ramflag:
            self._inrc_array[idx] = self.inrc
        if self._outrc_diskflag_writing:
            self._outrc_ncarray[0] = self.outrc
        if self._outrc_ramflag:
            self._outrc_array[idx] = self.outrc
        if self._rt_diskflag_writing:
            self._rt_ncarray[0] = self.rt
        if self._rt_ramflag:
            self._rt_array[idx] = self.rt
        if self._qt_diskflag_writing:
            self._qt_ncarray[0] = self.qt
        if self._qt_ramflag:
            self._qt_array[idx] = self.qt
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "gr2":
            self._gr2_outputpointer = value.p_value
        if name == "rg2":
            self._rg2_outputpointer = value.p_value
        if name == "gr3":
            self._gr3_outputpointer = value.p_value
        if name == "rg3":
            self._rg3_outputpointer = value.p_value
        if name == "inrc":
            self._inrc_outputpointer = value.p_value
        if name == "outrc":
            self._outrc_outputpointer = value.p_value
        if name == "rt":
            self._rt_outputpointer = value.p_value
        if name == "qt":
            self._qt_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._gr2_outputflag:
            self._gr2_outputpointer[0] = self.gr2
        if self._rg2_outputflag:
            self._rg2_outputpointer[0] = self.rg2
        if self._gr3_outputflag:
            self._gr3_outputpointer[0] = self.gr3
        if self._rg3_outputflag:
            self._rg3_outputpointer[0] = self.rg3
        if self._inrc_outputflag:
            self._inrc_outputpointer[0] = self.inrc
        if self._outrc_outputflag:
            self._outrc_outputpointer[0] = self.outrc
        if self._rt_outputflag:
            self._rt_outputpointer[0] = self.rt
        if self._qt_outputflag:
            self._qt_outputpointer[0] = self.qt
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
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
                for jdx1 in range(self._sp_length_1):
                    self.sp[jdx0, jdx1] = self._sp_ncarray[k]
                    k += 1
        elif self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                for jdx1 in range(self._sp_length_1):
                    self.sp[jdx0, jdx1] = self._sp_array[idx, jdx0, jdx1]
        if self._wc_diskflag_reading:
            k = 0
            for jdx0 in range(self._wc_length_0):
                for jdx1 in range(self._wc_length_1):
                    self.wc[jdx0, jdx1] = self._wc_ncarray[k]
                    k += 1
        elif self._wc_ramflag:
            for jdx0 in range(self._wc_length_0):
                for jdx1 in range(self._wc_length_1):
                    self.wc[jdx0, jdx1] = self._wc_array[idx, jdx0, jdx1]
        if self._sm_diskflag_reading:
            k = 0
            for jdx0 in range(self._sm_length_0):
                self.sm[jdx0] = self._sm_ncarray[k]
                k += 1
        elif self._sm_ramflag:
            for jdx0 in range(self._sm_length_0):
                self.sm[jdx0] = self._sm_array[idx, jdx0]
        if self._suz_diskflag_reading:
            k = 0
            for jdx0 in range(self._suz_length_0):
                self.suz[jdx0] = self._suz_ncarray[k]
                k += 1
        elif self._suz_ramflag:
            for jdx0 in range(self._suz_length_0):
                self.suz[jdx0] = self._suz_array[idx, jdx0]
        if self._sg1_diskflag_reading:
            k = 0
            for jdx0 in range(self._sg1_length_0):
                self.sg1[jdx0] = self._sg1_ncarray[k]
                k += 1
        elif self._sg1_ramflag:
            for jdx0 in range(self._sg1_length_0):
                self.sg1[jdx0] = self._sg1_array[idx, jdx0]
        if self._sg2_diskflag_reading:
            self.sg2 = self._sg2_ncarray[0]
        elif self._sg2_ramflag:
            self.sg2 = self._sg2_array[idx]
        if self._sg3_diskflag_reading:
            self.sg3 = self._sg3_ncarray[0]
        elif self._sg3_ramflag:
            self.sg3 = self._sg3_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
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
                for jdx1 in range(self._sp_length_1):
                    self._sp_ncarray[k] = self.sp[jdx0, jdx1]
                    k += 1
        if self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                for jdx1 in range(self._sp_length_1):
                    self._sp_array[idx, jdx0, jdx1] = self.sp[jdx0, jdx1]
        if self._wc_diskflag_writing:
            k = 0
            for jdx0 in range(self._wc_length_0):
                for jdx1 in range(self._wc_length_1):
                    self._wc_ncarray[k] = self.wc[jdx0, jdx1]
                    k += 1
        if self._wc_ramflag:
            for jdx0 in range(self._wc_length_0):
                for jdx1 in range(self._wc_length_1):
                    self._wc_array[idx, jdx0, jdx1] = self.wc[jdx0, jdx1]
        if self._sm_diskflag_writing:
            k = 0
            for jdx0 in range(self._sm_length_0):
                self._sm_ncarray[k] = self.sm[jdx0]
                k += 1
        if self._sm_ramflag:
            for jdx0 in range(self._sm_length_0):
                self._sm_array[idx, jdx0] = self.sm[jdx0]
        if self._suz_diskflag_writing:
            k = 0
            for jdx0 in range(self._suz_length_0):
                self._suz_ncarray[k] = self.suz[jdx0]
                k += 1
        if self._suz_ramflag:
            for jdx0 in range(self._suz_length_0):
                self._suz_array[idx, jdx0] = self.suz[jdx0]
        if self._sg1_diskflag_writing:
            k = 0
            for jdx0 in range(self._sg1_length_0):
                self._sg1_ncarray[k] = self.sg1[jdx0]
                k += 1
        if self._sg1_ramflag:
            for jdx0 in range(self._sg1_length_0):
                self._sg1_array[idx, jdx0] = self.sg1[jdx0]
        if self._sg2_diskflag_writing:
            self._sg2_ncarray[0] = self.sg2
        if self._sg2_ramflag:
            self._sg2_array[idx] = self.sg2
        if self._sg3_diskflag_writing:
            self._sg3_ncarray[0] = self.sg3
        if self._sg3_ramflag:
            self._sg3_array[idx] = self.sg3
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "sg2":
            self._sg2_outputpointer = value.p_value
        if name == "sg3":
            self._sg3_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._sg2_outputflag:
            self._sg2_outputpointer[0] = self.sg2
        if self._sg3_outputflag:
            self._sg3_outputpointer[0] = self.sg3
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
cdef class Model(masterinterface.MasterInterface):
    def __init__(self):
        super().__init__()
        self.aetmodel = None
        self.aetmodel_is_mainmodel = False
        self.rconcmodel = None
        self.rconcmodel_is_mainmodel = False
    def get_aetmodel(self) -> masterinterface.MasterInterface | None:
        return self.aetmodel
    def set_aetmodel(self, aetmodel: masterinterface.MasterInterface | None) -> None:
        self.aetmodel = aetmodel
    def get_rconcmodel(self) -> masterinterface.MasterInterface | None:
        return self.rconcmodel
    def set_rconcmodel(self, rconcmodel: masterinterface.MasterInterface | None) -> None:
        self.rconcmodel = rconcmodel
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
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.load_data(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.factors.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.save_data(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        cdef numpy.int64_t jdx0, jdx1
        for jdx0 in range(self.sequences.states._ic_length_0):
            self.sequences.old_states.ic[jdx0] = self.sequences.new_states.ic[jdx0]
        for jdx0 in range(self.sequences.states._sp_length_0):
            for jdx1 in range(self.sequences.states._sp_length_1):
                self.sequences.old_states.sp[jdx0,jdx1] = self.sequences.new_states.sp[jdx0,jdx1]
        for jdx0 in range(self.sequences.states._wc_length_0):
            for jdx1 in range(self.sequences.states._wc_length_1):
                self.sequences.old_states.wc[jdx0,jdx1] = self.sequences.new_states.wc[jdx0,jdx1]
        for jdx0 in range(self.sequences.states._sm_length_0):
            self.sequences.old_states.sm[jdx0] = self.sequences.new_states.sm[jdx0]
        for jdx0 in range(self.sequences.states._suz_length_0):
            self.sequences.old_states.suz[jdx0] = self.sequences.new_states.suz[jdx0]
        for jdx0 in range(self.sequences.states._sg1_length_0):
            self.sequences.old_states.sg1[jdx0] = self.sequences.new_states.sg1[jdx0]
        self.sequences.old_states.sg2 = self.sequences.new_states.sg2
        self.sequences.old_states.sg3 = self.sequences.new_states.sg3
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.new2old()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.calc_tc_v1()
        self.calc_fracrain_v1()
        self.calc_rfc_sfc_v1()
        self.calc_pc_v1()
        self.calc_tf_ic_v1()
        self.calc_sp_wc_v1()
        self.calc_spl_wcl_sp_wc_v1()
        self.calc_spg_wcg_sp_wc_v1()
        self.calc_cfact_v1()
        self.calc_melt_sp_wc_v1()
        self.calc_refr_sp_wc_v1()
        self.calc_in_wc_v1()
        self.calc_swe_v1()
        self.calc_sr_v1()
        self.calc_gact_v1()
        self.calc_glmelt_in_v1()
        self.calc_ei_ic_v1()
        self.calc_r_sm_v1()
        self.calc_ea_sm_v1()
        self.calc_suz_v1()
        self.calc_dp_suz_v1()
        self.calc_rs_ri_suz_v1()
        self.calc_gr1_v1()
        self.calc_rg1_sg1_v1()
        self.calc_gr2_gr3_v1()
        self.calc_rg2_sg2_v1()
        self.calc_rg3_sg3_v1()
        self.calc_el_sg2_sg3_v1()
        self.calc_inrc_v2()
        self.calc_outrc_v1()
        self.calc_rt_v1()
        self.calc_qt_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_inlets()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_inlets()
        cdef numpy.int64_t i
    cpdef void update_outlets(self) noexcept nogil:
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outlets()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_outlets()
        self.pass_q_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_receivers(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_senders(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.aetmodel is not None) and not self.aetmodel_is_mainmodel:
            self.aetmodel.update_outputs()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_outputs()
    cpdef inline void calc_tc_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.factors.tc[k] = self.sequences.inputs.t + self.parameters.control.tcorr[k] - self.parameters.control.tcalt[k] * (self.parameters.control.zonez[k] - self.parameters.derived.z)
    cpdef inline void calc_fracrain_v1(self) noexcept nogil:
        cdef double d_dt
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            d_dt = self.parameters.control.ttint[k] / 2.0
            if self.sequences.factors.tc[k] >= (self.parameters.control.tt[k] + d_dt):
                self.sequences.factors.fracrain[k] = 1.0
            elif self.sequences.factors.tc[k] <= (self.parameters.control.tt[k] - d_dt):
                self.sequences.factors.fracrain[k] = 0.0
            else:
                self.sequences.factors.fracrain[k] = (self.sequences.factors.tc[k] - (self.parameters.control.tt[k] - d_dt)) / self.parameters.control.ttint[k]
    cpdef inline void calc_rfc_sfc_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.factors.rfc[k] = self.sequences.factors.fracrain[k] * self.parameters.control.rfcf[k]
            self.sequences.factors.sfc[k] = (1.0 - self.sequences.factors.fracrain[k]) * self.parameters.control.sfcf[k]
    cpdef inline void calc_pc_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.pc[k] = self.sequences.inputs.p * (1.0 + self.parameters.control.pcalt[k] * (self.parameters.control.zonez[k] - self.parameters.derived.z))
            if self.sequences.fluxes.pc[k] <= 0.0:
                self.sequences.fluxes.pc[k] = 0.0
            else:
                self.sequences.fluxes.pc[k] = self.sequences.fluxes.pc[k] * (self.parameters.control.pcorr[k] * (self.sequences.factors.rfc[k] + self.sequences.factors.sfc[k]))
    cpdef inline void calc_tf_ic_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, SEALED):
                self.sequences.fluxes.tf[k] = max(self.sequences.fluxes.pc[k] - (self.parameters.control.icmax[k] - self.sequences.states.ic[k]), 0.0)
                self.sequences.states.ic[k] = self.sequences.states.ic[k] + (self.sequences.fluxes.pc[k] - self.sequences.fluxes.tf[k])
            else:
                self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc[k]
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_sp_wc_v1(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_snow
        cdef double d_rain
        cdef double d_denom
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                d_denom = self.sequences.factors.rfc[k] + self.sequences.factors.sfc[k]
                if d_denom > 0.0:
                    d_rain = self.sequences.fluxes.tf[k] * self.sequences.factors.rfc[k] / d_denom
                    d_snow = self.sequences.fluxes.tf[k] * self.sequences.factors.sfc[k] / d_denom
                    for c in range(self.parameters.control.sclass):
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] + (self.parameters.control.sfdist[c] * d_rain)
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] + (self.parameters.control.sfdist[c] * d_snow)
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_spl_wcl_sp_wc_v1(self) noexcept nogil:
        cdef double d_excess_wc
        cdef double d_excess_sp
        cdef double d_excess
        cdef double d_snow
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.spl[k] = 0.0
            self.sequences.fluxes.wcl[k] = 0.0
            if self.parameters.control.zonetype[k] == ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
            elif not isinf(self.parameters.control.smax[k]):
                for c in range(self.parameters.control.sclass):
                    d_snow = self.sequences.states.sp[c, k] + self.sequences.states.wc[c, k]
                    d_excess = d_snow - self.parameters.control.smax[k]
                    if d_excess > 0.0:
                        d_excess_sp = d_excess * self.sequences.states.sp[c, k] / d_snow
                        d_excess_wc = d_excess * self.sequences.states.wc[c, k] / d_snow
                        self.sequences.fluxes.spl[k] = self.sequences.fluxes.spl[k] + (d_excess_sp / self.parameters.control.sclass)
                        self.sequences.fluxes.wcl[k] = self.sequences.fluxes.wcl[k] + (d_excess_wc / self.parameters.control.sclass)
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] - (d_excess_sp)
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] - (d_excess_wc)
    cpdef inline void calc_spg_wcg_sp_wc_v1(self) noexcept nogil:
        cdef double d_excess_liquid_land
        cdef double d_excess_frozen_land
        cdef double d_delta_wc_zone
        cdef double d_delta_sp_zone
        cdef double d_fraction_gain_class
        cdef double d_excess_liquid_zone_actual
        cdef double d_excess_frozen_zone_actual
        cdef double d_fraction_gain_zone
        cdef double d_gain_max_cum
        cdef double d_excess_total_zone
        cdef double d_excess_liquid_zone
        cdef double d_excess_frozen_zone
        cdef double d_excess_liquid_basin
        cdef double d_excess_frozen_basin
        cdef double d_factor_excess
        cdef double d_factor_gain
        cdef double d_fraction_gain
        cdef double d_gain_max
        cdef double d_gain_pot
        cdef double d_gain_total
        cdef double d_gain_liquid
        cdef double d_gain_frozen
        cdef double d_f
        cdef numpy.int64_t t
        cdef numpy.int64_t f
        cdef numpy.int64_t c
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.spg[i] = 0.0
            self.sequences.fluxes.wcg[i] = 0.0
            self.sequences.aides.spe[i] = 0.0
            self.sequences.aides.wce[i] = 0.0
            if self.parameters.control.zonetype[i] == ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, i] = 0.0
                    self.sequences.states.wc[c, i] = 0.0
        for i in range(self.parameters.derived.srednumber):
            f, t = self.parameters.derived.sredorder[i, 0], self.parameters.derived.sredorder[i, 1]
            d_f = self.parameters.derived.zonearearatios[f, t] * self.parameters.control.sred[f, t]
            d_gain_frozen = d_f * (self.sequences.fluxes.spl[f] + self.sequences.aides.spe[f])
            d_gain_liquid = d_f * (self.sequences.fluxes.wcl[f] + self.sequences.aides.wce[f])
            d_gain_total = d_gain_frozen + d_gain_liquid
            for c in range(self.parameters.control.sclass):
                d_gain_pot = self.parameters.control.sfdist[c] * d_gain_total
                if d_gain_pot > 0.0:
                    d_gain_max = self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t]
                    d_fraction_gain = min(d_gain_max / d_gain_pot, 1.0)
                    d_factor_gain = d_fraction_gain * self.parameters.control.sfdist[c]
                    self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_factor_gain * d_gain_frozen / self.parameters.control.sclass)
                    self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_factor_gain * d_gain_liquid / self.parameters.control.sclass)
                    self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_factor_gain * d_gain_frozen)
                    self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_factor_gain * d_gain_liquid)
                    d_factor_excess = (1.0 - d_fraction_gain) * self.parameters.control.sfdist[c]
                    self.sequences.aides.spe[t] = self.sequences.aides.spe[t] + (d_factor_excess * d_gain_frozen / self.parameters.control.sclass)
                    self.sequences.aides.wce[t] = self.sequences.aides.wce[t] + (d_factor_excess * d_gain_liquid / self.parameters.control.sclass)
        d_excess_frozen_basin, d_excess_liquid_basin = 0.0, 0.0
        for i in range(self.parameters.control.nmbzones):
            if self.parameters.derived.sredend[i]:
                d_excess_frozen_basin = d_excess_frozen_basin + (self.parameters.derived.relzoneareas[i] * (self.sequences.aides.spe[i] + self.sequences.fluxes.spl[i]))
                d_excess_liquid_basin = d_excess_liquid_basin + (self.parameters.derived.relzoneareas[i] * (self.sequences.aides.wce[i] + self.sequences.fluxes.wcl[i]))
        if (d_excess_frozen_basin + d_excess_liquid_basin) <= 0.0:
            return
        for i in range(self.parameters.control.nmbzones):
            t = self.parameters.derived.indiceszonez[i]
            if self.parameters.control.zonetype[t] == ILAKE:
                continue
            d_excess_frozen_zone = d_excess_frozen_basin / self.parameters.derived.relzoneareas[t]
            d_excess_liquid_zone = d_excess_liquid_basin / self.parameters.derived.relzoneareas[t]
            d_excess_total_zone = d_excess_frozen_zone + d_excess_liquid_zone
            d_gain_max_cum = 0.0
            for c in range(self.parameters.control.sclass):
                d_gain_max_cum = d_gain_max_cum + (self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t])
            if d_gain_max_cum <= 0.0:
                continue
            d_fraction_gain_zone = min(                d_gain_max_cum / self.parameters.control.sclass / d_excess_total_zone, 1.0            )
            d_excess_frozen_zone_actual = d_fraction_gain_zone * d_excess_frozen_zone
            d_excess_liquid_zone_actual = d_fraction_gain_zone * d_excess_liquid_zone
            for c in range(self.parameters.control.sclass):
                d_fraction_gain_class = (                    self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t]                ) / d_gain_max_cum
                d_delta_sp_zone = d_fraction_gain_class * d_excess_frozen_zone_actual
                d_delta_wc_zone = d_fraction_gain_class * d_excess_liquid_zone_actual
                self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_delta_sp_zone)
                self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_delta_wc_zone)
                self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_delta_sp_zone * self.parameters.control.sclass)
                self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_delta_wc_zone * self.parameters.control.sclass)
            d_excess_frozen_basin = d_excess_frozen_basin - (d_excess_frozen_zone_actual * self.parameters.derived.relzoneareas[t])
            d_excess_liquid_basin = d_excess_liquid_basin - (d_excess_liquid_zone_actual * self.parameters.derived.relzoneareas[t])
            if (d_excess_frozen_basin + d_excess_liquid_basin) <= 0.0:
                return
        d_excess_frozen_land = d_excess_frozen_basin / self.parameters.derived.rellandarea
        d_excess_liquid_land = d_excess_liquid_basin / self.parameters.derived.rellandarea
        for t in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[t] != ILAKE:
                self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_excess_frozen_land)
                self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_excess_liquid_land)
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_excess_frozen_land)
                    self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_excess_liquid_land)
        return
    cpdef inline void calc_cfact_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double d_factor
        d_factor = 0.5 * sin(            2 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] + 1) / 366 - 1.39        )
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.factors.cfact[k] = max(self.parameters.control.cfmax[k] + d_factor * self.parameters.control.cfvar[k], 0.0)
            else:
                self.sequences.factors.cfact[k] = 0.0
    cpdef inline void calc_melt_sp_wc_v1(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_potmelt
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.factors.tc[k] > self.parameters.derived.ttm[k]:
                    d_potmelt = self.sequences.factors.cfact[k] * (self.sequences.factors.tc[k] - self.parameters.derived.ttm[k])
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.melt[c, k] = min(d_potmelt, self.sequences.states.sp[c, k])
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] - (self.sequences.fluxes.melt[c, k])
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] + (self.sequences.fluxes.melt[c, k])
                else:
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.melt[c, k] = 0.0
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.fluxes.melt[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_refr_sp_wc_v1(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_potrefr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.factors.tc[k] < self.parameters.derived.ttm[k]:
                    d_potrefr = self.parameters.control.cfr[k] * self.parameters.control.cfmax[k] * (self.parameters.derived.ttm[k] - self.sequences.factors.tc[k])
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.refr[c, k] = min(d_potrefr, self.sequences.states.wc[c, k])
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] + (self.sequences.fluxes.refr[c, k])
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] - (self.sequences.fluxes.refr[c, k])
                else:
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.refr[c, k] = 0.0
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.fluxes.refr[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_in_wc_v1(self) noexcept nogil:
        cdef double d_wc_old
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.in_[k] = 0.0
            if self.parameters.control.zonetype[k] != ILAKE:
                for c in range(self.parameters.control.sclass):
                    d_wc_old = self.sequences.states.wc[c, k]
                    self.sequences.states.wc[c, k] = min(d_wc_old, self.parameters.control.whc[k] * self.sequences.states.sp[c, k])
                    self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + ((d_wc_old - self.sequences.states.wc[c, k]) / self.parameters.control.sclass)
            else:
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.tf[k]
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.wc[c, k] = 0.0
    cpdef inline void calc_swe_v1(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.factors.swe[c, k] = self.sequences.states.sp[c, k] + self.sequences.states.wc[c, k]
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.factors.swe[c, k] = 0.0
    cpdef inline void calc_sr_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == SEALED:
                self.sequences.fluxes.sr[k] = self.sequences.fluxes.in_[k]
            else:
                self.sequences.fluxes.sr[k] = 0.0
    cpdef inline void calc_gact_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double d_factor
        d_factor = 0.5 * sin(            2 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] + 1) / 366 - 1.39        )
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == GLACIER:
                self.sequences.factors.gact[k] = max(self.parameters.control.gmelt[k] + d_factor * self.parameters.control.gvar[k], 0.0)
            else:
                self.sequences.factors.gact[k] = 0.0
    cpdef inline void calc_glmelt_in_v1(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_glmeltpot
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.glmelt[k] = 0.0
            if (self.parameters.control.zonetype[k] == GLACIER) and (self.sequences.factors.tc[k] > self.parameters.derived.ttm[k]):
                d_glmeltpot = self.sequences.factors.gact[k] / self.parameters.control.sclass * (self.sequences.factors.tc[k] - self.parameters.derived.ttm[k])
                for c in range(self.parameters.control.sclass):
                    if self.sequences.states.sp[c, k] <= 0.0:
                        self.sequences.fluxes.glmelt[k] = self.sequences.fluxes.glmelt[k] + (d_glmeltpot)
                        self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + (d_glmeltpot)
    cpdef inline void calc_ei_ic_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_ei_ic_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_r_sm_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k] * (self.sequences.states.sm[k] / self.parameters.control.fc[k]) ** self.parameters.control.beta[k]
                    self.sequences.fluxes.r[k] = max(self.sequences.fluxes.r[k], self.sequences.states.sm[k] + self.sequences.fluxes.in_[k] - self.parameters.control.fc[k])
                else:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.in_[k] - self.sequences.fluxes.r[k])
            else:
                self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_ea_sm_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_ea_sm_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_suz_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.states.suz[k] = self.sequences.states.suz[k] + (self.sequences.fluxes.r[k])
            else:
                self.sequences.states.suz[k] = 0.0
    cpdef inline void calc_dp_suz_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.dp[k] = min(self.sequences.states.suz[k], self.parameters.control.percmax)
                self.sequences.states.suz[k] = self.sequences.states.suz[k] - (self.sequences.fluxes.dp[k])
            else:
                self.sequences.fluxes.dp[k] = 0.0
                self.sequences.states.suz[k] = 0.0
    cpdef inline void calc_rs_ri_suz_v1(self) noexcept nogil:
        cdef double d_f
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                if self.sequences.states.suz[k] > self.parameters.control.sgr[k]:
                    self.sequences.fluxes.rs[k] = (self.sequences.states.suz[k] - self.parameters.control.sgr[k]) * (1.0 - self.parameters.derived.w0[k])
                else:
                    self.sequences.fluxes.rs[k] = 0.0
                self.sequences.fluxes.ri[k] = self.sequences.states.suz[k] * (1.0 - self.parameters.derived.w1[k])
                self.sequences.states.suz[k] = self.sequences.states.suz[k] - (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k])
                if self.sequences.states.suz[k] < 0.0:
                    d_f = 1.0 - self.sequences.states.suz[k] / (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k])
                    self.sequences.fluxes.rs[k] = self.sequences.fluxes.rs[k] * (d_f)
                    self.sequences.fluxes.ri[k] = self.sequences.fluxes.ri[k] * (d_f)
                    self.sequences.states.suz[k] = 0.0
            else:
                self.sequences.states.suz[k] = 0.0
                self.sequences.fluxes.rs[k] = 0.0
                self.sequences.fluxes.ri[k] = 0.0
    cpdef inline void calc_gr1_v1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.gr1[k] = min(self.sequences.fluxes.dp[k], (self.parameters.control.sg1max[k] - self.sequences.states.sg1[k]) / self.parameters.control.k2[k])
                self.sequences.fluxes.gr1[k] = self.sequences.fluxes.gr1[k] - (max(self.sequences.states.sg1[k] + self.sequences.fluxes.gr1[k] - self.parameters.control.sg1max[k], 0.0))
            else:
                self.sequences.states.sg1[k] = 0.0
                self.sequences.fluxes.gr1[k] = 0.0
    cpdef inline void calc_rg1_sg1_v1(self) noexcept nogil:
        cdef double d_sg1
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                d_sg1 = self.sequences.states.sg1[k]
                self.sequences.states.sg1[k] = (                    self.parameters.derived.w2[k] * d_sg1 + (1.0 - self.parameters.derived.w2[k]) * self.parameters.control.k2[k] * self.sequences.fluxes.gr1[k]                )
                self.sequences.fluxes.rg1[k] = d_sg1 + self.sequences.fluxes.gr1[k] - self.sequences.states.sg1[k]
            else:
                self.sequences.states.sg1[k] = 0.0
                self.sequences.fluxes.rg1[k] = 0.0
    cpdef inline void calc_gr2_gr3_v1(self) noexcept nogil:
        cdef double d_total
        cdef double d_weight
        cdef numpy.int64_t k
        self.sequences.fluxes.gr2 = 0.0
        self.sequences.fluxes.gr3 = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == SEALED:
                continue
            d_weight = self.parameters.derived.relzoneareas[k] / self.parameters.derived.rellowerzonearea
            if self.parameters.control.zonetype[k] == ILAKE:
                d_total = d_weight * self.sequences.fluxes.pc[k]
            else:
                d_total = d_weight * (self.sequences.fluxes.dp[k] - self.sequences.fluxes.gr1[k])
            self.sequences.fluxes.gr2 = self.sequences.fluxes.gr2 + (self.parameters.fixed.fsg * d_total)
            self.sequences.fluxes.gr3 = self.sequences.fluxes.gr3 + ((1.0 - self.parameters.fixed.fsg) * d_total)
    cpdef inline void calc_rg2_sg2_v1(self) noexcept nogil:
        cdef double d_add
        cdef double d_w3
        cdef double d_k3
        cdef double d_gr2
        cdef double d_sg2
        d_sg2 = self.sequences.states.sg2
        d_gr2 = self.sequences.fluxes.gr2
        d_k3 = self.parameters.control.k3
        d_w3 = self.parameters.derived.w3
        if d_sg2 < 0.0 < d_gr2:
            d_add = min(-self.sequences.states.sg2, d_gr2)
            d_k3 = d_k3 * (d_gr2 / d_add)
            d_w3 = exp(-1.0 / d_k3)
            d_sg2 = d_sg2 + (d_add)
            d_gr2 = d_gr2 - (d_add)
        if d_sg2 >= 0.0:
            self.sequences.states.sg2 = d_w3 * d_sg2 + (1.0 - d_w3) * d_k3 * d_gr2
            self.sequences.fluxes.rg2 = d_sg2 + d_gr2 - self.sequences.states.sg2
        else:
            self.sequences.states.sg2 = d_sg2
            self.sequences.fluxes.rg2 = 0.0
    cpdef inline void calc_rg3_sg3_v1(self) noexcept nogil:
        cdef double d_add
        cdef double d_w4
        cdef double d_k4
        cdef double d_gr3
        cdef double d_sg3
        d_sg3 = self.sequences.states.sg3
        d_gr3 = self.sequences.fluxes.gr3
        d_k4 = self.parameters.derived.k4
        d_w4 = self.parameters.derived.w4
        if d_sg3 < 0.0 < d_gr3:
            d_add = min(-self.sequences.states.sg3, d_gr3)
            d_k4 = d_k4 * (d_gr3 / d_add)
            d_w4 = exp(-1.0 / d_k4)
            d_sg3 = d_sg3 + (d_add)
            d_gr3 = d_gr3 - (d_add)
        if d_sg3 >= 0.0:
            self.sequences.states.sg3 = d_w4 * d_sg3 + (1.0 - d_w4) * d_k4 * d_gr3
            self.sequences.fluxes.rg3 = d_sg3 + d_gr3 - self.sequences.states.sg3
        else:
            self.sequences.states.sg3 = d_sg3
            self.sequences.fluxes.rg3 = 0.0
    cpdef inline void calc_el_sg2_sg3_v1(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_el_sg2_sg3_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_inrc_v2(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.inrc = self.parameters.derived.rellowerzonearea * (self.sequences.fluxes.rg2 + self.sequences.fluxes.rg3)
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.inrc = self.sequences.fluxes.inrc + (self.parameters.derived.relzoneareas[k] * (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k] + self.sequences.fluxes.rg1[k]))
            elif self.parameters.control.zonetype[k] == SEALED:
                self.sequences.fluxes.inrc = self.sequences.fluxes.inrc + (self.parameters.derived.relzoneareas[k] * self.sequences.fluxes.r[k])
    cpdef inline void calc_outrc_v1(self) noexcept nogil:
        if self.rconcmodel is None:
            self.sequences.fluxes.outrc = self.sequences.fluxes.inrc
        elif self.rconcmodel_typeid == 1:
            self.calc_outrc_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel)            )
    cpdef inline void calc_rt_v1(self) noexcept nogil:
        self.sequences.fluxes.rt = self.sequences.fluxes.outrc
    cpdef inline void calc_qt_v1(self) noexcept nogil:
        self.sequences.fluxes.qt = self.parameters.derived.qfactor * self.sequences.fluxes.rt
    cpdef double get_temperature_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.factors.tc[s]
    cpdef double get_meantemperature_v1(self) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_precipitation_v1(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.pc[s]
    cpdef double get_interceptedwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.ic[k]
    cpdef double get_soilwater_v1(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.sm[k]
    cpdef double get_snowcover_v1(self, numpy.int64_t k) noexcept nogil:
        cdef numpy.int64_t c
        cdef double snowcovered
        snowcovered = 0.0
        for c in range(self.parameters.control.sclass):
            snowcovered = snowcovered + (self.sequences.states.sp[c, k] > 0.0)
        return snowcovered / self.parameters.control.sclass
    cpdef inline void calc_ei_ic_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, SEALED):
                self.sequences.fluxes.ei[k] = min(submodel.get_interceptionevaporation(k), self.sequences.states.ic[k])
                self.sequences.states.ic[k] = self.sequences.states.ic[k] - (self.sequences.fluxes.ei[k])
            else:
                self.sequences.fluxes.ei[k] = 0.0
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_ea_sm_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.ea[k] = min(submodel.get_soilevapotranspiration(k), self.sequences.states.sm[k])
                self.sequences.states.sm[k] = self.sequences.states.sm[k] - (self.sequences.fluxes.ea[k])
                if self.sequences.states.sm[k] > self.parameters.control.fc[k]:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.r[k] + (self.sequences.states.sm[k] - self.parameters.control.fc[k])
                    self.sequences.states.sm[k] = self.parameters.control.fc[k]
            else:
                self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_el_sg2_sg3_aetmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef double weight
        cdef numpy.int64_t k
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == ILAKE:
                self.sequences.fluxes.el[k] = submodel.get_waterevaporation(k)
                weight = self.parameters.derived.relzoneareas[k] / self.parameters.derived.rellowerzonearea
                self.sequences.states.sg2 = self.sequences.states.sg2 - (self.parameters.fixed.fsg * weight * self.sequences.fluxes.el[k])
                self.sequences.states.sg3 = self.sequences.states.sg3 - ((1.0 - self.parameters.fixed.fsg) * weight * self.sequences.fluxes.el[k])
            else:
                self.sequences.fluxes.el[k] = 0.0
    cpdef inline void calc_outrc_rconcmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.set_inflow(self.sequences.fluxes.inrc)
        submodel.determine_outflow()
        self.sequences.fluxes.outrc = submodel.get_outflow()
    cpdef inline void pass_q_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qt
    cpdef inline void calc_tc(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.factors.tc[k] = self.sequences.inputs.t + self.parameters.control.tcorr[k] - self.parameters.control.tcalt[k] * (self.parameters.control.zonez[k] - self.parameters.derived.z)
    cpdef inline void calc_fracrain(self) noexcept nogil:
        cdef double d_dt
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            d_dt = self.parameters.control.ttint[k] / 2.0
            if self.sequences.factors.tc[k] >= (self.parameters.control.tt[k] + d_dt):
                self.sequences.factors.fracrain[k] = 1.0
            elif self.sequences.factors.tc[k] <= (self.parameters.control.tt[k] - d_dt):
                self.sequences.factors.fracrain[k] = 0.0
            else:
                self.sequences.factors.fracrain[k] = (self.sequences.factors.tc[k] - (self.parameters.control.tt[k] - d_dt)) / self.parameters.control.ttint[k]
    cpdef inline void calc_rfc_sfc(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.factors.rfc[k] = self.sequences.factors.fracrain[k] * self.parameters.control.rfcf[k]
            self.sequences.factors.sfc[k] = (1.0 - self.sequences.factors.fracrain[k]) * self.parameters.control.sfcf[k]
    cpdef inline void calc_pc(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.pc[k] = self.sequences.inputs.p * (1.0 + self.parameters.control.pcalt[k] * (self.parameters.control.zonez[k] - self.parameters.derived.z))
            if self.sequences.fluxes.pc[k] <= 0.0:
                self.sequences.fluxes.pc[k] = 0.0
            else:
                self.sequences.fluxes.pc[k] = self.sequences.fluxes.pc[k] * (self.parameters.control.pcorr[k] * (self.sequences.factors.rfc[k] + self.sequences.factors.sfc[k]))
    cpdef inline void calc_tf_ic(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, SEALED):
                self.sequences.fluxes.tf[k] = max(self.sequences.fluxes.pc[k] - (self.parameters.control.icmax[k] - self.sequences.states.ic[k]), 0.0)
                self.sequences.states.ic[k] = self.sequences.states.ic[k] + (self.sequences.fluxes.pc[k] - self.sequences.fluxes.tf[k])
            else:
                self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc[k]
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_sp_wc(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_snow
        cdef double d_rain
        cdef double d_denom
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                d_denom = self.sequences.factors.rfc[k] + self.sequences.factors.sfc[k]
                if d_denom > 0.0:
                    d_rain = self.sequences.fluxes.tf[k] * self.sequences.factors.rfc[k] / d_denom
                    d_snow = self.sequences.fluxes.tf[k] * self.sequences.factors.sfc[k] / d_denom
                    for c in range(self.parameters.control.sclass):
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] + (self.parameters.control.sfdist[c] * d_rain)
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] + (self.parameters.control.sfdist[c] * d_snow)
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_spl_wcl_sp_wc(self) noexcept nogil:
        cdef double d_excess_wc
        cdef double d_excess_sp
        cdef double d_excess
        cdef double d_snow
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.spl[k] = 0.0
            self.sequences.fluxes.wcl[k] = 0.0
            if self.parameters.control.zonetype[k] == ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
            elif not isinf(self.parameters.control.smax[k]):
                for c in range(self.parameters.control.sclass):
                    d_snow = self.sequences.states.sp[c, k] + self.sequences.states.wc[c, k]
                    d_excess = d_snow - self.parameters.control.smax[k]
                    if d_excess > 0.0:
                        d_excess_sp = d_excess * self.sequences.states.sp[c, k] / d_snow
                        d_excess_wc = d_excess * self.sequences.states.wc[c, k] / d_snow
                        self.sequences.fluxes.spl[k] = self.sequences.fluxes.spl[k] + (d_excess_sp / self.parameters.control.sclass)
                        self.sequences.fluxes.wcl[k] = self.sequences.fluxes.wcl[k] + (d_excess_wc / self.parameters.control.sclass)
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] - (d_excess_sp)
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] - (d_excess_wc)
    cpdef inline void calc_spg_wcg_sp_wc(self) noexcept nogil:
        cdef double d_excess_liquid_land
        cdef double d_excess_frozen_land
        cdef double d_delta_wc_zone
        cdef double d_delta_sp_zone
        cdef double d_fraction_gain_class
        cdef double d_excess_liquid_zone_actual
        cdef double d_excess_frozen_zone_actual
        cdef double d_fraction_gain_zone
        cdef double d_gain_max_cum
        cdef double d_excess_total_zone
        cdef double d_excess_liquid_zone
        cdef double d_excess_frozen_zone
        cdef double d_excess_liquid_basin
        cdef double d_excess_frozen_basin
        cdef double d_factor_excess
        cdef double d_factor_gain
        cdef double d_fraction_gain
        cdef double d_gain_max
        cdef double d_gain_pot
        cdef double d_gain_total
        cdef double d_gain_liquid
        cdef double d_gain_frozen
        cdef double d_f
        cdef numpy.int64_t t
        cdef numpy.int64_t f
        cdef numpy.int64_t c
        cdef numpy.int64_t i
        for i in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.spg[i] = 0.0
            self.sequences.fluxes.wcg[i] = 0.0
            self.sequences.aides.spe[i] = 0.0
            self.sequences.aides.wce[i] = 0.0
            if self.parameters.control.zonetype[i] == ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, i] = 0.0
                    self.sequences.states.wc[c, i] = 0.0
        for i in range(self.parameters.derived.srednumber):
            f, t = self.parameters.derived.sredorder[i, 0], self.parameters.derived.sredorder[i, 1]
            d_f = self.parameters.derived.zonearearatios[f, t] * self.parameters.control.sred[f, t]
            d_gain_frozen = d_f * (self.sequences.fluxes.spl[f] + self.sequences.aides.spe[f])
            d_gain_liquid = d_f * (self.sequences.fluxes.wcl[f] + self.sequences.aides.wce[f])
            d_gain_total = d_gain_frozen + d_gain_liquid
            for c in range(self.parameters.control.sclass):
                d_gain_pot = self.parameters.control.sfdist[c] * d_gain_total
                if d_gain_pot > 0.0:
                    d_gain_max = self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t]
                    d_fraction_gain = min(d_gain_max / d_gain_pot, 1.0)
                    d_factor_gain = d_fraction_gain * self.parameters.control.sfdist[c]
                    self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_factor_gain * d_gain_frozen / self.parameters.control.sclass)
                    self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_factor_gain * d_gain_liquid / self.parameters.control.sclass)
                    self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_factor_gain * d_gain_frozen)
                    self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_factor_gain * d_gain_liquid)
                    d_factor_excess = (1.0 - d_fraction_gain) * self.parameters.control.sfdist[c]
                    self.sequences.aides.spe[t] = self.sequences.aides.spe[t] + (d_factor_excess * d_gain_frozen / self.parameters.control.sclass)
                    self.sequences.aides.wce[t] = self.sequences.aides.wce[t] + (d_factor_excess * d_gain_liquid / self.parameters.control.sclass)
        d_excess_frozen_basin, d_excess_liquid_basin = 0.0, 0.0
        for i in range(self.parameters.control.nmbzones):
            if self.parameters.derived.sredend[i]:
                d_excess_frozen_basin = d_excess_frozen_basin + (self.parameters.derived.relzoneareas[i] * (self.sequences.aides.spe[i] + self.sequences.fluxes.spl[i]))
                d_excess_liquid_basin = d_excess_liquid_basin + (self.parameters.derived.relzoneareas[i] * (self.sequences.aides.wce[i] + self.sequences.fluxes.wcl[i]))
        if (d_excess_frozen_basin + d_excess_liquid_basin) <= 0.0:
            return
        for i in range(self.parameters.control.nmbzones):
            t = self.parameters.derived.indiceszonez[i]
            if self.parameters.control.zonetype[t] == ILAKE:
                continue
            d_excess_frozen_zone = d_excess_frozen_basin / self.parameters.derived.relzoneareas[t]
            d_excess_liquid_zone = d_excess_liquid_basin / self.parameters.derived.relzoneareas[t]
            d_excess_total_zone = d_excess_frozen_zone + d_excess_liquid_zone
            d_gain_max_cum = 0.0
            for c in range(self.parameters.control.sclass):
                d_gain_max_cum = d_gain_max_cum + (self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t])
            if d_gain_max_cum <= 0.0:
                continue
            d_fraction_gain_zone = min(                d_gain_max_cum / self.parameters.control.sclass / d_excess_total_zone, 1.0            )
            d_excess_frozen_zone_actual = d_fraction_gain_zone * d_excess_frozen_zone
            d_excess_liquid_zone_actual = d_fraction_gain_zone * d_excess_liquid_zone
            for c in range(self.parameters.control.sclass):
                d_fraction_gain_class = (                    self.parameters.control.smax[t] - self.sequences.states.sp[c, t] - self.sequences.states.wc[c, t]                ) / d_gain_max_cum
                d_delta_sp_zone = d_fraction_gain_class * d_excess_frozen_zone_actual
                d_delta_wc_zone = d_fraction_gain_class * d_excess_liquid_zone_actual
                self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_delta_sp_zone)
                self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_delta_wc_zone)
                self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_delta_sp_zone * self.parameters.control.sclass)
                self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_delta_wc_zone * self.parameters.control.sclass)
            d_excess_frozen_basin = d_excess_frozen_basin - (d_excess_frozen_zone_actual * self.parameters.derived.relzoneareas[t])
            d_excess_liquid_basin = d_excess_liquid_basin - (d_excess_liquid_zone_actual * self.parameters.derived.relzoneareas[t])
            if (d_excess_frozen_basin + d_excess_liquid_basin) <= 0.0:
                return
        d_excess_frozen_land = d_excess_frozen_basin / self.parameters.derived.rellandarea
        d_excess_liquid_land = d_excess_liquid_basin / self.parameters.derived.rellandarea
        for t in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[t] != ILAKE:
                self.sequences.fluxes.spg[t] = self.sequences.fluxes.spg[t] + (d_excess_frozen_land)
                self.sequences.fluxes.wcg[t] = self.sequences.fluxes.wcg[t] + (d_excess_liquid_land)
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.sp[c, t] = self.sequences.states.sp[c, t] + (d_excess_frozen_land)
                    self.sequences.states.wc[c, t] = self.sequences.states.wc[c, t] + (d_excess_liquid_land)
        return
    cpdef inline void calc_cfact(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double d_factor
        d_factor = 0.5 * sin(            2 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] + 1) / 366 - 1.39        )
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.factors.cfact[k] = max(self.parameters.control.cfmax[k] + d_factor * self.parameters.control.cfvar[k], 0.0)
            else:
                self.sequences.factors.cfact[k] = 0.0
    cpdef inline void calc_melt_sp_wc(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_potmelt
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.factors.tc[k] > self.parameters.derived.ttm[k]:
                    d_potmelt = self.sequences.factors.cfact[k] * (self.sequences.factors.tc[k] - self.parameters.derived.ttm[k])
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.melt[c, k] = min(d_potmelt, self.sequences.states.sp[c, k])
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] - (self.sequences.fluxes.melt[c, k])
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] + (self.sequences.fluxes.melt[c, k])
                else:
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.melt[c, k] = 0.0
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.fluxes.melt[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_refr_sp_wc(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_potrefr
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.factors.tc[k] < self.parameters.derived.ttm[k]:
                    d_potrefr = self.parameters.control.cfr[k] * self.parameters.control.cfmax[k] * (self.parameters.derived.ttm[k] - self.sequences.factors.tc[k])
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.refr[c, k] = min(d_potrefr, self.sequences.states.wc[c, k])
                        self.sequences.states.sp[c, k] = self.sequences.states.sp[c, k] + (self.sequences.fluxes.refr[c, k])
                        self.sequences.states.wc[c, k] = self.sequences.states.wc[c, k] - (self.sequences.fluxes.refr[c, k])
                else:
                    for c in range(self.parameters.control.sclass):
                        self.sequences.fluxes.refr[c, k] = 0.0
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.fluxes.refr[c, k] = 0.0
                    self.sequences.states.wc[c, k] = 0.0
                    self.sequences.states.sp[c, k] = 0.0
    cpdef inline void calc_in_wc(self) noexcept nogil:
        cdef double d_wc_old
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.in_[k] = 0.0
            if self.parameters.control.zonetype[k] != ILAKE:
                for c in range(self.parameters.control.sclass):
                    d_wc_old = self.sequences.states.wc[c, k]
                    self.sequences.states.wc[c, k] = min(d_wc_old, self.parameters.control.whc[k] * self.sequences.states.sp[c, k])
                    self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + ((d_wc_old - self.sequences.states.wc[c, k]) / self.parameters.control.sclass)
            else:
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.tf[k]
                for c in range(self.parameters.control.sclass):
                    self.sequences.states.wc[c, k] = 0.0
    cpdef inline void calc_swe(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                for c in range(self.parameters.control.sclass):
                    self.sequences.factors.swe[c, k] = self.sequences.states.sp[c, k] + self.sequences.states.wc[c, k]
            else:
                for c in range(self.parameters.control.sclass):
                    self.sequences.factors.swe[c, k] = 0.0
    cpdef inline void calc_sr(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == SEALED:
                self.sequences.fluxes.sr[k] = self.sequences.fluxes.in_[k]
            else:
                self.sequences.fluxes.sr[k] = 0.0
    cpdef inline void calc_gact(self) noexcept nogil:
        cdef numpy.int64_t k
        cdef double d_factor
        d_factor = 0.5 * sin(            2 * self.parameters.fixed.pi * (self.parameters.derived.doy[self.idx_sim] + 1) / 366 - 1.39        )
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == GLACIER:
                self.sequences.factors.gact[k] = max(self.parameters.control.gmelt[k] + d_factor * self.parameters.control.gvar[k], 0.0)
            else:
                self.sequences.factors.gact[k] = 0.0
    cpdef inline void calc_glmelt_in(self) noexcept nogil:
        cdef numpy.int64_t c
        cdef double d_glmeltpot
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.glmelt[k] = 0.0
            if (self.parameters.control.zonetype[k] == GLACIER) and (self.sequences.factors.tc[k] > self.parameters.derived.ttm[k]):
                d_glmeltpot = self.sequences.factors.gact[k] / self.parameters.control.sclass * (self.sequences.factors.tc[k] - self.parameters.derived.ttm[k])
                for c in range(self.parameters.control.sclass):
                    if self.sequences.states.sp[c, k] <= 0.0:
                        self.sequences.fluxes.glmelt[k] = self.sequences.fluxes.glmelt[k] + (d_glmeltpot)
                        self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + (d_glmeltpot)
    cpdef inline void calc_ei_ic(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_ei_ic_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_r_sm(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k] * (self.sequences.states.sm[k] / self.parameters.control.fc[k]) ** self.parameters.control.beta[k]
                    self.sequences.fluxes.r[k] = max(self.sequences.fluxes.r[k], self.sequences.states.sm[k] + self.sequences.fluxes.in_[k] - self.parameters.control.fc[k])
                else:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.in_[k] - self.sequences.fluxes.r[k])
            else:
                self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_ea_sm(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_ea_sm_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_suz(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.states.suz[k] = self.sequences.states.suz[k] + (self.sequences.fluxes.r[k])
            else:
                self.sequences.states.suz[k] = 0.0
    cpdef inline void calc_dp_suz(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.dp[k] = min(self.sequences.states.suz[k], self.parameters.control.percmax)
                self.sequences.states.suz[k] = self.sequences.states.suz[k] - (self.sequences.fluxes.dp[k])
            else:
                self.sequences.fluxes.dp[k] = 0.0
                self.sequences.states.suz[k] = 0.0
    cpdef inline void calc_rs_ri_suz(self) noexcept nogil:
        cdef double d_f
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                if self.sequences.states.suz[k] > self.parameters.control.sgr[k]:
                    self.sequences.fluxes.rs[k] = (self.sequences.states.suz[k] - self.parameters.control.sgr[k]) * (1.0 - self.parameters.derived.w0[k])
                else:
                    self.sequences.fluxes.rs[k] = 0.0
                self.sequences.fluxes.ri[k] = self.sequences.states.suz[k] * (1.0 - self.parameters.derived.w1[k])
                self.sequences.states.suz[k] = self.sequences.states.suz[k] - (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k])
                if self.sequences.states.suz[k] < 0.0:
                    d_f = 1.0 - self.sequences.states.suz[k] / (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k])
                    self.sequences.fluxes.rs[k] = self.sequences.fluxes.rs[k] * (d_f)
                    self.sequences.fluxes.ri[k] = self.sequences.fluxes.ri[k] * (d_f)
                    self.sequences.states.suz[k] = 0.0
            else:
                self.sequences.states.suz[k] = 0.0
                self.sequences.fluxes.rs[k] = 0.0
                self.sequences.fluxes.ri[k] = 0.0
    cpdef inline void calc_gr1(self) noexcept nogil:
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.gr1[k] = min(self.sequences.fluxes.dp[k], (self.parameters.control.sg1max[k] - self.sequences.states.sg1[k]) / self.parameters.control.k2[k])
                self.sequences.fluxes.gr1[k] = self.sequences.fluxes.gr1[k] - (max(self.sequences.states.sg1[k] + self.sequences.fluxes.gr1[k] - self.parameters.control.sg1max[k], 0.0))
            else:
                self.sequences.states.sg1[k] = 0.0
                self.sequences.fluxes.gr1[k] = 0.0
    cpdef inline void calc_rg1_sg1(self) noexcept nogil:
        cdef double d_sg1
        cdef numpy.int64_t k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                d_sg1 = self.sequences.states.sg1[k]
                self.sequences.states.sg1[k] = (                    self.parameters.derived.w2[k] * d_sg1 + (1.0 - self.parameters.derived.w2[k]) * self.parameters.control.k2[k] * self.sequences.fluxes.gr1[k]                )
                self.sequences.fluxes.rg1[k] = d_sg1 + self.sequences.fluxes.gr1[k] - self.sequences.states.sg1[k]
            else:
                self.sequences.states.sg1[k] = 0.0
                self.sequences.fluxes.rg1[k] = 0.0
    cpdef inline void calc_gr2_gr3(self) noexcept nogil:
        cdef double d_total
        cdef double d_weight
        cdef numpy.int64_t k
        self.sequences.fluxes.gr2 = 0.0
        self.sequences.fluxes.gr3 = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == SEALED:
                continue
            d_weight = self.parameters.derived.relzoneareas[k] / self.parameters.derived.rellowerzonearea
            if self.parameters.control.zonetype[k] == ILAKE:
                d_total = d_weight * self.sequences.fluxes.pc[k]
            else:
                d_total = d_weight * (self.sequences.fluxes.dp[k] - self.sequences.fluxes.gr1[k])
            self.sequences.fluxes.gr2 = self.sequences.fluxes.gr2 + (self.parameters.fixed.fsg * d_total)
            self.sequences.fluxes.gr3 = self.sequences.fluxes.gr3 + ((1.0 - self.parameters.fixed.fsg) * d_total)
    cpdef inline void calc_rg2_sg2(self) noexcept nogil:
        cdef double d_add
        cdef double d_w3
        cdef double d_k3
        cdef double d_gr2
        cdef double d_sg2
        d_sg2 = self.sequences.states.sg2
        d_gr2 = self.sequences.fluxes.gr2
        d_k3 = self.parameters.control.k3
        d_w3 = self.parameters.derived.w3
        if d_sg2 < 0.0 < d_gr2:
            d_add = min(-self.sequences.states.sg2, d_gr2)
            d_k3 = d_k3 * (d_gr2 / d_add)
            d_w3 = exp(-1.0 / d_k3)
            d_sg2 = d_sg2 + (d_add)
            d_gr2 = d_gr2 - (d_add)
        if d_sg2 >= 0.0:
            self.sequences.states.sg2 = d_w3 * d_sg2 + (1.0 - d_w3) * d_k3 * d_gr2
            self.sequences.fluxes.rg2 = d_sg2 + d_gr2 - self.sequences.states.sg2
        else:
            self.sequences.states.sg2 = d_sg2
            self.sequences.fluxes.rg2 = 0.0
    cpdef inline void calc_rg3_sg3(self) noexcept nogil:
        cdef double d_add
        cdef double d_w4
        cdef double d_k4
        cdef double d_gr3
        cdef double d_sg3
        d_sg3 = self.sequences.states.sg3
        d_gr3 = self.sequences.fluxes.gr3
        d_k4 = self.parameters.derived.k4
        d_w4 = self.parameters.derived.w4
        if d_sg3 < 0.0 < d_gr3:
            d_add = min(-self.sequences.states.sg3, d_gr3)
            d_k4 = d_k4 * (d_gr3 / d_add)
            d_w4 = exp(-1.0 / d_k4)
            d_sg3 = d_sg3 + (d_add)
            d_gr3 = d_gr3 - (d_add)
        if d_sg3 >= 0.0:
            self.sequences.states.sg3 = d_w4 * d_sg3 + (1.0 - d_w4) * d_k4 * d_gr3
            self.sequences.fluxes.rg3 = d_sg3 + d_gr3 - self.sequences.states.sg3
        else:
            self.sequences.states.sg3 = d_sg3
            self.sequences.fluxes.rg3 = 0.0
    cpdef inline void calc_el_sg2_sg3(self) noexcept nogil:
        if self.aetmodel_typeid == 1:
            self.calc_el_sg2_sg3_aetmodel_v1(                (<masterinterface.MasterInterface>self.aetmodel)            )
    cpdef inline void calc_inrc(self) noexcept nogil:
        cdef numpy.int64_t k
        self.sequences.fluxes.inrc = self.parameters.derived.rellowerzonearea * (self.sequences.fluxes.rg2 + self.sequences.fluxes.rg3)
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, GLACIER):
                self.sequences.fluxes.inrc = self.sequences.fluxes.inrc + (self.parameters.derived.relzoneareas[k] * (self.sequences.fluxes.rs[k] + self.sequences.fluxes.ri[k] + self.sequences.fluxes.rg1[k]))
            elif self.parameters.control.zonetype[k] == SEALED:
                self.sequences.fluxes.inrc = self.sequences.fluxes.inrc + (self.parameters.derived.relzoneareas[k] * self.sequences.fluxes.r[k])
    cpdef inline void calc_outrc(self) noexcept nogil:
        if self.rconcmodel is None:
            self.sequences.fluxes.outrc = self.sequences.fluxes.inrc
        elif self.rconcmodel_typeid == 1:
            self.calc_outrc_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel)            )
    cpdef inline void calc_rt(self) noexcept nogil:
        self.sequences.fluxes.rt = self.sequences.fluxes.outrc
    cpdef inline void calc_qt(self) noexcept nogil:
        self.sequences.fluxes.qt = self.parameters.derived.qfactor * self.sequences.fluxes.rt
    cpdef double get_temperature(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.factors.tc[s]
    cpdef double get_meantemperature(self) noexcept nogil:
        return self.sequences.inputs.t
    cpdef double get_precipitation(self, numpy.int64_t s) noexcept nogil:
        return self.sequences.fluxes.pc[s]
    cpdef double get_interceptedwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.ic[k]
    cpdef double get_soilwater(self, numpy.int64_t k) noexcept nogil:
        return self.sequences.states.sm[k]
    cpdef double get_snowcover(self, numpy.int64_t k) noexcept nogil:
        cdef numpy.int64_t c
        cdef double snowcovered
        snowcovered = 0.0
        for c in range(self.parameters.control.sclass):
            snowcovered = snowcovered + (self.sequences.states.sp[c, k] > 0.0)
        return snowcovered / self.parameters.control.sclass
    cpdef inline void calc_ei_ic_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_interceptionevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST, SEALED):
                self.sequences.fluxes.ei[k] = min(submodel.get_interceptionevaporation(k), self.sequences.states.ic[k])
                self.sequences.states.ic[k] = self.sequences.states.ic[k] - (self.sequences.fluxes.ei[k])
            else:
                self.sequences.fluxes.ei[k] = 0.0
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_ea_sm_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef numpy.int64_t k
        submodel.determine_soilevapotranspiration()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.ea[k] = min(submodel.get_soilevapotranspiration(k), self.sequences.states.sm[k])
                self.sequences.states.sm[k] = self.sequences.states.sm[k] - (self.sequences.fluxes.ea[k])
                if self.sequences.states.sm[k] > self.parameters.control.fc[k]:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.r[k] + (self.sequences.states.sm[k] - self.parameters.control.fc[k])
                    self.sequences.states.sm[k] = self.parameters.control.fc[k]
            else:
                self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_el_sg2_sg3_aetmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        cdef double weight
        cdef numpy.int64_t k
        submodel.determine_waterevaporation()
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == ILAKE:
                self.sequences.fluxes.el[k] = submodel.get_waterevaporation(k)
                weight = self.parameters.derived.relzoneareas[k] / self.parameters.derived.rellowerzonearea
                self.sequences.states.sg2 = self.sequences.states.sg2 - (self.parameters.fixed.fsg * weight * self.sequences.fluxes.el[k])
                self.sequences.states.sg3 = self.sequences.states.sg3 - ((1.0 - self.parameters.fixed.fsg) * weight * self.sequences.fluxes.el[k])
            else:
                self.sequences.fluxes.el[k] = 0.0
    cpdef inline void calc_outrc_rconcmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.set_inflow(self.sequences.fluxes.inrc)
        submodel.determine_outflow()
        self.sequences.fluxes.outrc = submodel.get_outflow()
    cpdef inline void pass_q(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qt
