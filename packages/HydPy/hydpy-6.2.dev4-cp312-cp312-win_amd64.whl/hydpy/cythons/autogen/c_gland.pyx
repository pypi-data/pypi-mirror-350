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
        if self._p_inputflag:
            self.p = self._p_inputpointer[0]
        elif self._p_diskflag_reading:
            self.p = self._p_ncarray[0]
        elif self._p_ramflag:
            self.p = self._p_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._p_diskflag_writing:
            self._p_ncarray[0] = self.p
        if self._p_ramflag:
            self._p_array[idx] = self.p
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "p":
            self._p_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._e_diskflag_reading:
            self.e = self._e_ncarray[0]
        elif self._e_ramflag:
            self.e = self._e_array[idx]
        if self._en_diskflag_reading:
            self.en = self._en_ncarray[0]
        elif self._en_ramflag:
            self.en = self._en_array[idx]
        if self._pn_diskflag_reading:
            self.pn = self._pn_ncarray[0]
        elif self._pn_ramflag:
            self.pn = self._pn_array[idx]
        if self._ps_diskflag_reading:
            self.ps = self._ps_ncarray[0]
        elif self._ps_ramflag:
            self.ps = self._ps_array[idx]
        if self._ei_diskflag_reading:
            self.ei = self._ei_ncarray[0]
        elif self._ei_ramflag:
            self.ei = self._ei_array[idx]
        if self._es_diskflag_reading:
            self.es = self._es_ncarray[0]
        elif self._es_ramflag:
            self.es = self._es_array[idx]
        if self._ae_diskflag_reading:
            self.ae = self._ae_ncarray[0]
        elif self._ae_ramflag:
            self.ae = self._ae_array[idx]
        if self._pr_diskflag_reading:
            self.pr = self._pr_ncarray[0]
        elif self._pr_ramflag:
            self.pr = self._pr_array[idx]
        if self._pr9_diskflag_reading:
            self.pr9 = self._pr9_ncarray[0]
        elif self._pr9_ramflag:
            self.pr9 = self._pr9_array[idx]
        if self._pr1_diskflag_reading:
            self.pr1 = self._pr1_ncarray[0]
        elif self._pr1_ramflag:
            self.pr1 = self._pr1_array[idx]
        if self._q10_diskflag_reading:
            self.q10 = self._q10_ncarray[0]
        elif self._q10_ramflag:
            self.q10 = self._q10_array[idx]
        if self._perc_diskflag_reading:
            self.perc = self._perc_ncarray[0]
        elif self._perc_ramflag:
            self.perc = self._perc_array[idx]
        if self._q9_diskflag_reading:
            self.q9 = self._q9_ncarray[0]
        elif self._q9_ramflag:
            self.q9 = self._q9_array[idx]
        if self._q1_diskflag_reading:
            self.q1 = self._q1_ncarray[0]
        elif self._q1_ramflag:
            self.q1 = self._q1_array[idx]
        if self._fd_diskflag_reading:
            self.fd = self._fd_ncarray[0]
        elif self._fd_ramflag:
            self.fd = self._fd_array[idx]
        if self._fr_diskflag_reading:
            self.fr = self._fr_ncarray[0]
        elif self._fr_ramflag:
            self.fr = self._fr_array[idx]
        if self._fr2_diskflag_reading:
            self.fr2 = self._fr2_ncarray[0]
        elif self._fr2_ramflag:
            self.fr2 = self._fr2_array[idx]
        if self._qr_diskflag_reading:
            self.qr = self._qr_ncarray[0]
        elif self._qr_ramflag:
            self.qr = self._qr_array[idx]
        if self._qr2_diskflag_reading:
            self.qr2 = self._qr2_ncarray[0]
        elif self._qr2_ramflag:
            self.qr2 = self._qr2_array[idx]
        if self._qd_diskflag_reading:
            self.qd = self._qd_ncarray[0]
        elif self._qd_ramflag:
            self.qd = self._qd_array[idx]
        if self._qh_diskflag_reading:
            self.qh = self._qh_ncarray[0]
        elif self._qh_ramflag:
            self.qh = self._qh_array[idx]
        if self._qv_diskflag_reading:
            self.qv = self._qv_ncarray[0]
        elif self._qv_ramflag:
            self.qv = self._qv_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._e_diskflag_writing:
            self._e_ncarray[0] = self.e
        if self._e_ramflag:
            self._e_array[idx] = self.e
        if self._en_diskflag_writing:
            self._en_ncarray[0] = self.en
        if self._en_ramflag:
            self._en_array[idx] = self.en
        if self._pn_diskflag_writing:
            self._pn_ncarray[0] = self.pn
        if self._pn_ramflag:
            self._pn_array[idx] = self.pn
        if self._ps_diskflag_writing:
            self._ps_ncarray[0] = self.ps
        if self._ps_ramflag:
            self._ps_array[idx] = self.ps
        if self._ei_diskflag_writing:
            self._ei_ncarray[0] = self.ei
        if self._ei_ramflag:
            self._ei_array[idx] = self.ei
        if self._es_diskflag_writing:
            self._es_ncarray[0] = self.es
        if self._es_ramflag:
            self._es_array[idx] = self.es
        if self._ae_diskflag_writing:
            self._ae_ncarray[0] = self.ae
        if self._ae_ramflag:
            self._ae_array[idx] = self.ae
        if self._pr_diskflag_writing:
            self._pr_ncarray[0] = self.pr
        if self._pr_ramflag:
            self._pr_array[idx] = self.pr
        if self._pr9_diskflag_writing:
            self._pr9_ncarray[0] = self.pr9
        if self._pr9_ramflag:
            self._pr9_array[idx] = self.pr9
        if self._pr1_diskflag_writing:
            self._pr1_ncarray[0] = self.pr1
        if self._pr1_ramflag:
            self._pr1_array[idx] = self.pr1
        if self._q10_diskflag_writing:
            self._q10_ncarray[0] = self.q10
        if self._q10_ramflag:
            self._q10_array[idx] = self.q10
        if self._perc_diskflag_writing:
            self._perc_ncarray[0] = self.perc
        if self._perc_ramflag:
            self._perc_array[idx] = self.perc
        if self._q9_diskflag_writing:
            self._q9_ncarray[0] = self.q9
        if self._q9_ramflag:
            self._q9_array[idx] = self.q9
        if self._q1_diskflag_writing:
            self._q1_ncarray[0] = self.q1
        if self._q1_ramflag:
            self._q1_array[idx] = self.q1
        if self._fd_diskflag_writing:
            self._fd_ncarray[0] = self.fd
        if self._fd_ramflag:
            self._fd_array[idx] = self.fd
        if self._fr_diskflag_writing:
            self._fr_ncarray[0] = self.fr
        if self._fr_ramflag:
            self._fr_array[idx] = self.fr
        if self._fr2_diskflag_writing:
            self._fr2_ncarray[0] = self.fr2
        if self._fr2_ramflag:
            self._fr2_array[idx] = self.fr2
        if self._qr_diskflag_writing:
            self._qr_ncarray[0] = self.qr
        if self._qr_ramflag:
            self._qr_array[idx] = self.qr
        if self._qr2_diskflag_writing:
            self._qr2_ncarray[0] = self.qr2
        if self._qr2_ramflag:
            self._qr2_array[idx] = self.qr2
        if self._qd_diskflag_writing:
            self._qd_ncarray[0] = self.qd
        if self._qd_ramflag:
            self._qd_array[idx] = self.qd
        if self._qh_diskflag_writing:
            self._qh_ncarray[0] = self.qh
        if self._qh_ramflag:
            self._qh_array[idx] = self.qh
        if self._qv_diskflag_writing:
            self._qv_ncarray[0] = self.qv
        if self._qv_ramflag:
            self._qv_array[idx] = self.qv
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "e":
            self._e_outputpointer = value.p_value
        if name == "en":
            self._en_outputpointer = value.p_value
        if name == "pn":
            self._pn_outputpointer = value.p_value
        if name == "ps":
            self._ps_outputpointer = value.p_value
        if name == "ei":
            self._ei_outputpointer = value.p_value
        if name == "es":
            self._es_outputpointer = value.p_value
        if name == "ae":
            self._ae_outputpointer = value.p_value
        if name == "pr":
            self._pr_outputpointer = value.p_value
        if name == "pr9":
            self._pr9_outputpointer = value.p_value
        if name == "pr1":
            self._pr1_outputpointer = value.p_value
        if name == "q10":
            self._q10_outputpointer = value.p_value
        if name == "perc":
            self._perc_outputpointer = value.p_value
        if name == "q9":
            self._q9_outputpointer = value.p_value
        if name == "q1":
            self._q1_outputpointer = value.p_value
        if name == "fd":
            self._fd_outputpointer = value.p_value
        if name == "fr":
            self._fr_outputpointer = value.p_value
        if name == "fr2":
            self._fr2_outputpointer = value.p_value
        if name == "qr":
            self._qr_outputpointer = value.p_value
        if name == "qr2":
            self._qr2_outputpointer = value.p_value
        if name == "qd":
            self._qd_outputpointer = value.p_value
        if name == "qh":
            self._qh_outputpointer = value.p_value
        if name == "qv":
            self._qv_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._e_outputflag:
            self._e_outputpointer[0] = self.e
        if self._en_outputflag:
            self._en_outputpointer[0] = self.en
        if self._pn_outputflag:
            self._pn_outputpointer[0] = self.pn
        if self._ps_outputflag:
            self._ps_outputpointer[0] = self.ps
        if self._ei_outputflag:
            self._ei_outputpointer[0] = self.ei
        if self._es_outputflag:
            self._es_outputpointer[0] = self.es
        if self._ae_outputflag:
            self._ae_outputpointer[0] = self.ae
        if self._pr_outputflag:
            self._pr_outputpointer[0] = self.pr
        if self._pr9_outputflag:
            self._pr9_outputpointer[0] = self.pr9
        if self._pr1_outputflag:
            self._pr1_outputpointer[0] = self.pr1
        if self._q10_outputflag:
            self._q10_outputpointer[0] = self.q10
        if self._perc_outputflag:
            self._perc_outputpointer[0] = self.perc
        if self._q9_outputflag:
            self._q9_outputpointer[0] = self.q9
        if self._q1_outputflag:
            self._q1_outputpointer[0] = self.q1
        if self._fd_outputflag:
            self._fd_outputpointer[0] = self.fd
        if self._fr_outputflag:
            self._fr_outputpointer[0] = self.fr
        if self._fr2_outputflag:
            self._fr2_outputpointer[0] = self.fr2
        if self._qr_outputflag:
            self._qr_outputpointer[0] = self.qr
        if self._qr2_outputflag:
            self._qr2_outputpointer[0] = self.qr2
        if self._qd_outputflag:
            self._qd_outputpointer[0] = self.qd
        if self._qh_outputflag:
            self._qh_outputpointer[0] = self.qh
        if self._qv_outputflag:
            self._qv_outputpointer[0] = self.qv
@cython.final
cdef class StateSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._i_diskflag_reading:
            self.i = self._i_ncarray[0]
        elif self._i_ramflag:
            self.i = self._i_array[idx]
        if self._s_diskflag_reading:
            self.s = self._s_ncarray[0]
        elif self._s_ramflag:
            self.s = self._s_array[idx]
        if self._r_diskflag_reading:
            self.r = self._r_ncarray[0]
        elif self._r_ramflag:
            self.r = self._r_array[idx]
        if self._r2_diskflag_reading:
            self.r2 = self._r2_ncarray[0]
        elif self._r2_ramflag:
            self.r2 = self._r2_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t k
        if self._i_diskflag_writing:
            self._i_ncarray[0] = self.i
        if self._i_ramflag:
            self._i_array[idx] = self.i
        if self._s_diskflag_writing:
            self._s_ncarray[0] = self.s
        if self._s_ramflag:
            self._s_array[idx] = self.s
        if self._r_diskflag_writing:
            self._r_ncarray[0] = self.r
        if self._r_ramflag:
            self._r_array[idx] = self.r
        if self._r2_diskflag_writing:
            self._r2_ncarray[0] = self.r2
        if self._r2_ramflag:
            self._r2_array[idx] = self.r2
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "i":
            self._i_outputpointer = value.p_value
        if name == "s":
            self._s_outputpointer = value.p_value
        if name == "r":
            self._r_outputpointer = value.p_value
        if name == "r2":
            self._r2_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._i_outputflag:
            self._i_outputpointer[0] = self.i
        if self._s_outputflag:
            self._s_outputpointer[0] = self.s
        if self._r_outputflag:
            self._r_outputpointer[0] = self.r
        if self._r2_outputflag:
            self._r2_outputpointer[0] = self.r2
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
cdef class Model:
    def __init__(self):
        super().__init__()
        self.petmodel = None
        self.petmodel_is_mainmodel = False
        self.rconcmodel = None
        self.rconcmodel_is_mainmodel = False
        self.rconcmodel_directflow = None
        self.rconcmodel_directflow_is_mainmodel = False
        self.rconcmodel_routingstore = None
        self.rconcmodel_routingstore_is_mainmodel = False
    def get_petmodel(self) -> masterinterface.MasterInterface | None:
        return self.petmodel
    def set_petmodel(self, petmodel: masterinterface.MasterInterface | None) -> None:
        self.petmodel = petmodel
    def get_rconcmodel(self) -> masterinterface.MasterInterface | None:
        return self.rconcmodel
    def set_rconcmodel(self, rconcmodel: masterinterface.MasterInterface | None) -> None:
        self.rconcmodel = rconcmodel
    def get_rconcmodel_directflow(self) -> masterinterface.MasterInterface | None:
        return self.rconcmodel_directflow
    def set_rconcmodel_directflow(self, rconcmodel_directflow: masterinterface.MasterInterface | None) -> None:
        self.rconcmodel_directflow = rconcmodel_directflow
    def get_rconcmodel_routingstore(self) -> masterinterface.MasterInterface | None:
        return self.rconcmodel_routingstore
    def set_rconcmodel_routingstore(self, rconcmodel_routingstore: masterinterface.MasterInterface | None) -> None:
        self.rconcmodel_routingstore = rconcmodel_routingstore
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
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.reset_reuseflags()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.reset_reuseflags()
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.reset_reuseflags()
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.reset_reuseflags()
    cpdef void load_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.load_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.load_data(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.load_data(idx)
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.load_data(idx)
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inputs.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.states.save_data(idx)
        self.sequences.outlets.save_data(idx)
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.save_data(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.save_data(idx)
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.save_data(idx)
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.save_data(idx)
    cpdef void new2old(self) noexcept nogil:
        self.sequences.old_states.i = self.sequences.new_states.i
        self.sequences.old_states.s = self.sequences.new_states.s
        self.sequences.old_states.r = self.sequences.new_states.r
        self.sequences.old_states.r2 = self.sequences.new_states.r2
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.new2old()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.new2old()
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.new2old()
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.new2old()
    cpdef inline void run(self) noexcept nogil:
        self.calc_ei_v1()
        self.calc_pn_v1()
        self.calc_en_v1()
        self.update_i_v1()
        self.calc_ps_v1()
        self.calc_es_v1()
        self.update_s_v1()
        self.calc_perc_v1()
        self.update_s_v2()
        self.calc_ae_v1()
        self.calc_pr_v1()
        self.calc_pr1_pr9_v1()
        self.calc_q9_v1()
        self.calc_q1_v1()
        self.calc_q10_v1()
        self.calc_q1_q9_v2()
        self.calc_fr_v1()
        self.calc_fr_v2()
        self.update_r_v1()
        self.update_r_v3()
        self.update_r_v2()
        self.calc_qr_v1()
        self.update_r_v3()
        self.calc_fr2_v1()
        self.update_r2_v1()
        self.calc_qr2_r2_v1()
        self.update_r_v2()
        self.calc_fd_v1()
        self.calc_qd_v1()
        self.calc_qh_v1()
        self.calc_qh_v2()
        self.calc_qv_v1()
    cpdef void update_inlets(self) noexcept nogil:
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_inlets()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_inlets()
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.update_inlets()
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.update_inlets()
        cdef numpy.int64_t i
        self.calc_e_v1()
    cpdef void update_outlets(self) noexcept nogil:
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_outlets()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_outlets()
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.update_outlets()
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.update_outlets()
        self.pass_q_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
    cpdef void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_receivers(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_receivers(idx)
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.update_receivers(idx)
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.update_receivers(idx)
        cdef numpy.int64_t i
    cpdef void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_senders(idx)
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_senders(idx)
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.update_senders(idx)
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.update_senders(idx)
        cdef numpy.int64_t i
    cpdef void update_outputs(self) noexcept nogil:
        if not self.threading:
            self.sequences.fluxes.update_outputs()
            self.sequences.states.update_outputs()
        if (self.petmodel is not None) and not self.petmodel_is_mainmodel:
            self.petmodel.update_outputs()
        if (self.rconcmodel is not None) and not self.rconcmodel_is_mainmodel:
            self.rconcmodel.update_outputs()
        if (self.rconcmodel_directflow is not None) and not self.rconcmodel_directflow_is_mainmodel:
            self.rconcmodel_directflow.update_outputs()
        if (self.rconcmodel_routingstore is not None) and not self.rconcmodel_routingstore_is_mainmodel:
            self.rconcmodel_routingstore.update_outputs()
    cpdef inline void calc_e_v1(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_e_petmodel_v1((<masterinterface.MasterInterface>self.petmodel))
    cpdef inline void calc_ei_v1(self) noexcept nogil:
        self.sequences.fluxes.ei = min(self.sequences.fluxes.e, self.sequences.states.i + self.sequences.inputs.p)
    cpdef inline void calc_pn_v1(self) noexcept nogil:
        self.sequences.fluxes.pn = max(self.sequences.inputs.p - (self.parameters.control.imax - self.sequences.states.i) - self.sequences.fluxes.ei, 0.0)
    cpdef inline void calc_en_v1(self) noexcept nogil:
        self.sequences.fluxes.en = max(self.sequences.fluxes.e - self.sequences.fluxes.ei, 0.0)
    cpdef inline void update_i_v1(self) noexcept nogil:
        self.sequences.states.i = self.sequences.states.i + (self.sequences.inputs.p - self.sequences.fluxes.ei - self.sequences.fluxes.pn)
    cpdef inline void calc_ps_v1(self) noexcept nogil:
        self.sequences.fluxes.ps = (            self.parameters.control.x1            * (1.0 - (self.sequences.states.s / self.parameters.control.x1) ** 2.0)            * tanh(self.sequences.fluxes.pn / self.parameters.control.x1)            / (1.0 + self.sequences.states.s / self.parameters.control.x1 * tanh(self.sequences.fluxes.pn / self.parameters.control.x1))        )
    cpdef inline void calc_es_v1(self) noexcept nogil:
        cdef double tre
        cdef double re
        cdef double rs
        rs = self.sequences.states.s / self.parameters.control.x1
        re = self.sequences.fluxes.en / self.parameters.control.x1
        tre = tanh(re)
        self.sequences.fluxes.es = (self.sequences.states.s * (2.0 - rs) * tre) / (1.0 + (1.0 - rs) * tre)
    cpdef inline void update_s_v1(self) noexcept nogil:
        self.sequences.states.s = self.sequences.states.s + (self.sequences.fluxes.ps - self.sequences.fluxes.es)
    cpdef inline void calc_perc_v1(self) noexcept nogil:
        self.sequences.fluxes.perc = self.sequences.states.s * (1.0 - (1.0 + (self.sequences.states.s / self.parameters.control.x1 / self.parameters.derived.beta) ** 4.0) ** -0.25)
    cpdef inline void update_s_v2(self) noexcept nogil:
        self.sequences.states.s = self.sequences.states.s - (self.sequences.fluxes.perc)
    cpdef inline void calc_ae_v1(self) noexcept nogil:
        self.sequences.fluxes.ae = self.sequences.fluxes.ei + self.sequences.fluxes.es
    cpdef inline void calc_pr_v1(self) noexcept nogil:
        self.sequences.fluxes.pr = self.sequences.fluxes.perc + self.sequences.fluxes.pn - self.sequences.fluxes.ps
    cpdef inline void calc_pr1_pr9_v1(self) noexcept nogil:
        self.sequences.fluxes.pr9 = 0.9 * self.sequences.fluxes.pr
        self.sequences.fluxes.pr1 = 0.1 * self.sequences.fluxes.pr
    cpdef inline void calc_q9_v1(self) noexcept nogil:
        if self.rconcmodel_routingstore is None:
            self.sequences.fluxes.q9 = self.sequences.fluxes.pr9
        elif self.rconcmodel_routingstore_typeid == 1:
            self.sequences.fluxes.q9 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel_routingstore),                self.sequences.fluxes.pr9,            )
    cpdef inline void calc_q1_v1(self) noexcept nogil:
        if self.rconcmodel_directflow is None:
            self.sequences.fluxes.q1 = self.sequences.fluxes.pr1
        elif self.rconcmodel_directflow_typeid == 1:
            self.sequences.fluxes.q1 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel_directflow),                self.sequences.fluxes.pr1,            )
    cpdef inline void calc_q10_v1(self) noexcept nogil:
        if self.rconcmodel is None:
            self.sequences.fluxes.q10 = self.sequences.fluxes.pr
        elif self.rconcmodel_typeid == 1:
            self.sequences.fluxes.q10 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel), self.sequences.fluxes.pr            )
    cpdef inline void calc_q1_q9_v2(self) noexcept nogil:
        self.sequences.fluxes.q1 = 0.1 * self.sequences.fluxes.q10
        self.sequences.fluxes.q9 = 0.9 * self.sequences.fluxes.q10
    cpdef inline void calc_fr_v1(self) noexcept nogil:
        self.sequences.fluxes.fr = self.parameters.control.x2 * (self.sequences.states.r / self.parameters.control.x3) ** 3.5
    cpdef inline void calc_fr_v2(self) noexcept nogil:
        self.sequences.fluxes.fr = self.parameters.control.x2 * (self.sequences.states.r / self.parameters.control.x3 - self.parameters.control.x5)
    cpdef inline void update_r_v1(self) noexcept nogil:
        self.sequences.states.r = self.sequences.states.r + (self.sequences.fluxes.q9 + self.sequences.fluxes.fr)
        if self.sequences.states.r < 0.0:
            self.sequences.fluxes.fr = self.sequences.fluxes.fr - (self.sequences.states.r)
            self.sequences.states.r = 0.0
    cpdef inline void update_r_v3(self) noexcept nogil:
        self.sequences.states.r = self.sequences.states.r - (self.sequences.fluxes.qr)
    cpdef inline void update_r_v2(self) noexcept nogil:
        self.sequences.states.r = self.sequences.states.r + (0.6 * self.sequences.fluxes.q9 + self.sequences.fluxes.fr)
        if self.sequences.states.r < 0.0:
            self.sequences.fluxes.fr = self.sequences.fluxes.fr - (self.sequences.states.r)
            self.sequences.states.r = 0.0
    cpdef inline void calc_qr_v1(self) noexcept nogil:
        self.sequences.fluxes.qr = self.sequences.states.r * (1.0 - (1.0 + (self.sequences.states.r / self.parameters.control.x3) ** 4.0) ** -0.25)
    cpdef inline void calc_fr2_v1(self) noexcept nogil:
        self.sequences.fluxes.fr2 = self.sequences.fluxes.fr
    cpdef inline void update_r2_v1(self) noexcept nogil:
        self.sequences.states.r2 = self.sequences.states.r2 + (0.4 * self.sequences.fluxes.q9 + self.sequences.fluxes.fr2)
    cpdef inline void calc_qr2_r2_v1(self) noexcept nogil:
        cdef double ar
        ar = min(max(self.sequences.states.r2 / self.parameters.control.x6, -33.0), 33.0)
        if ar < -7.0:
            self.sequences.fluxes.qr2 = self.parameters.control.x6 * exp(ar)
        elif ar <= 7.0:
            self.sequences.fluxes.qr2 = self.parameters.control.x6 * log(exp(ar) + 1.0)
        else:
            self.sequences.fluxes.qr2 = self.sequences.states.r2 + self.parameters.control.x6 / exp(ar)
        self.sequences.states.r2 = self.sequences.states.r2 - (self.sequences.fluxes.qr2)
    cpdef inline void calc_fd_v1(self) noexcept nogil:
        if (self.sequences.fluxes.q1 + self.sequences.fluxes.fr) <= 0.0:
            self.sequences.fluxes.fd = -self.sequences.fluxes.q1
        else:
            self.sequences.fluxes.fd = self.sequences.fluxes.fr
    cpdef inline void calc_qd_v1(self) noexcept nogil:
        self.sequences.fluxes.qd = max(self.sequences.fluxes.q1 + self.sequences.fluxes.fd, 0.0)
    cpdef inline void calc_qh_v1(self) noexcept nogil:
        self.sequences.fluxes.qh = self.sequences.fluxes.qr + self.sequences.fluxes.qd
    cpdef inline void calc_qh_v2(self) noexcept nogil:
        self.sequences.fluxes.qh = self.sequences.fluxes.qr + self.sequences.fluxes.qr2 + self.sequences.fluxes.qd
    cpdef inline void calc_qv_v1(self) noexcept nogil:
        self.sequences.fluxes.qv = self.sequences.fluxes.qh * self.parameters.derived.qfactor
    cpdef inline void calc_e_petmodel_v1(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.determine_potentialevapotranspiration()
        self.sequences.fluxes.e = submodel.get_potentialevapotranspiration(0)
    cpdef inline double calc_q_rconcmodel_v1(self, masterinterface.MasterInterface submodel, double inflow) noexcept nogil:
        submodel.set_inflow(inflow)
        submodel.determine_outflow()
        return submodel.get_outflow()
    cpdef inline void pass_q_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qv
    cpdef inline void calc_e(self) noexcept nogil:
        if self.petmodel_typeid == 1:
            self.calc_e_petmodel_v1((<masterinterface.MasterInterface>self.petmodel))
    cpdef inline void calc_ei(self) noexcept nogil:
        self.sequences.fluxes.ei = min(self.sequences.fluxes.e, self.sequences.states.i + self.sequences.inputs.p)
    cpdef inline void calc_pn(self) noexcept nogil:
        self.sequences.fluxes.pn = max(self.sequences.inputs.p - (self.parameters.control.imax - self.sequences.states.i) - self.sequences.fluxes.ei, 0.0)
    cpdef inline void calc_en(self) noexcept nogil:
        self.sequences.fluxes.en = max(self.sequences.fluxes.e - self.sequences.fluxes.ei, 0.0)
    cpdef inline void update_i(self) noexcept nogil:
        self.sequences.states.i = self.sequences.states.i + (self.sequences.inputs.p - self.sequences.fluxes.ei - self.sequences.fluxes.pn)
    cpdef inline void calc_ps(self) noexcept nogil:
        self.sequences.fluxes.ps = (            self.parameters.control.x1            * (1.0 - (self.sequences.states.s / self.parameters.control.x1) ** 2.0)            * tanh(self.sequences.fluxes.pn / self.parameters.control.x1)            / (1.0 + self.sequences.states.s / self.parameters.control.x1 * tanh(self.sequences.fluxes.pn / self.parameters.control.x1))        )
    cpdef inline void calc_es(self) noexcept nogil:
        cdef double tre
        cdef double re
        cdef double rs
        rs = self.sequences.states.s / self.parameters.control.x1
        re = self.sequences.fluxes.en / self.parameters.control.x1
        tre = tanh(re)
        self.sequences.fluxes.es = (self.sequences.states.s * (2.0 - rs) * tre) / (1.0 + (1.0 - rs) * tre)
    cpdef inline void calc_perc(self) noexcept nogil:
        self.sequences.fluxes.perc = self.sequences.states.s * (1.0 - (1.0 + (self.sequences.states.s / self.parameters.control.x1 / self.parameters.derived.beta) ** 4.0) ** -0.25)
    cpdef inline void calc_ae(self) noexcept nogil:
        self.sequences.fluxes.ae = self.sequences.fluxes.ei + self.sequences.fluxes.es
    cpdef inline void calc_pr(self) noexcept nogil:
        self.sequences.fluxes.pr = self.sequences.fluxes.perc + self.sequences.fluxes.pn - self.sequences.fluxes.ps
    cpdef inline void calc_pr1_pr9(self) noexcept nogil:
        self.sequences.fluxes.pr9 = 0.9 * self.sequences.fluxes.pr
        self.sequences.fluxes.pr1 = 0.1 * self.sequences.fluxes.pr
    cpdef inline void calc_q9(self) noexcept nogil:
        if self.rconcmodel_routingstore is None:
            self.sequences.fluxes.q9 = self.sequences.fluxes.pr9
        elif self.rconcmodel_routingstore_typeid == 1:
            self.sequences.fluxes.q9 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel_routingstore),                self.sequences.fluxes.pr9,            )
    cpdef inline void calc_q1(self) noexcept nogil:
        if self.rconcmodel_directflow is None:
            self.sequences.fluxes.q1 = self.sequences.fluxes.pr1
        elif self.rconcmodel_directflow_typeid == 1:
            self.sequences.fluxes.q1 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel_directflow),                self.sequences.fluxes.pr1,            )
    cpdef inline void calc_q10(self) noexcept nogil:
        if self.rconcmodel is None:
            self.sequences.fluxes.q10 = self.sequences.fluxes.pr
        elif self.rconcmodel_typeid == 1:
            self.sequences.fluxes.q10 = self.calc_q_rconcmodel_v1(                (<masterinterface.MasterInterface>self.rconcmodel), self.sequences.fluxes.pr            )
    cpdef inline void calc_q1_q9(self) noexcept nogil:
        self.sequences.fluxes.q1 = 0.1 * self.sequences.fluxes.q10
        self.sequences.fluxes.q9 = 0.9 * self.sequences.fluxes.q10
    cpdef inline void calc_qr(self) noexcept nogil:
        self.sequences.fluxes.qr = self.sequences.states.r * (1.0 - (1.0 + (self.sequences.states.r / self.parameters.control.x3) ** 4.0) ** -0.25)
    cpdef inline void calc_fr2(self) noexcept nogil:
        self.sequences.fluxes.fr2 = self.sequences.fluxes.fr
    cpdef inline void update_r2(self) noexcept nogil:
        self.sequences.states.r2 = self.sequences.states.r2 + (0.4 * self.sequences.fluxes.q9 + self.sequences.fluxes.fr2)
    cpdef inline void calc_qr2_r2(self) noexcept nogil:
        cdef double ar
        ar = min(max(self.sequences.states.r2 / self.parameters.control.x6, -33.0), 33.0)
        if ar < -7.0:
            self.sequences.fluxes.qr2 = self.parameters.control.x6 * exp(ar)
        elif ar <= 7.0:
            self.sequences.fluxes.qr2 = self.parameters.control.x6 * log(exp(ar) + 1.0)
        else:
            self.sequences.fluxes.qr2 = self.sequences.states.r2 + self.parameters.control.x6 / exp(ar)
        self.sequences.states.r2 = self.sequences.states.r2 - (self.sequences.fluxes.qr2)
    cpdef inline void calc_fd(self) noexcept nogil:
        if (self.sequences.fluxes.q1 + self.sequences.fluxes.fr) <= 0.0:
            self.sequences.fluxes.fd = -self.sequences.fluxes.q1
        else:
            self.sequences.fluxes.fd = self.sequences.fluxes.fr
    cpdef inline void calc_qd(self) noexcept nogil:
        self.sequences.fluxes.qd = max(self.sequences.fluxes.q1 + self.sequences.fluxes.fd, 0.0)
    cpdef inline void calc_qv(self) noexcept nogil:
        self.sequences.fluxes.qv = self.sequences.fluxes.qh * self.parameters.derived.qfactor
    cpdef inline void calc_e_petmodel(self, masterinterface.MasterInterface submodel) noexcept nogil:
        submodel.determine_potentialevapotranspiration()
        self.sequences.fluxes.e = submodel.get_potentialevapotranspiration(0)
    cpdef inline double calc_q_rconcmodel(self, masterinterface.MasterInterface submodel, double inflow) noexcept nogil:
        submodel.set_inflow(inflow)
        submodel.determine_outflow()
        return submodel.get_outflow()
    cpdef inline void pass_q(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qv
