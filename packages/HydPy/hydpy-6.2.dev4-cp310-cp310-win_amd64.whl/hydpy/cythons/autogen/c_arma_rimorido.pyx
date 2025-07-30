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
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qin_diskflag_reading:
            self.qin = self._qin_ncarray[0]
        elif self._qin_ramflag:
            self.qin = self._qin_array[idx]
        if self._qpin_diskflag_reading:
            k = 0
            for jdx0 in range(self._qpin_length_0):
                self.qpin[jdx0] = self._qpin_ncarray[k]
                k += 1
        elif self._qpin_ramflag:
            for jdx0 in range(self._qpin_length_0):
                self.qpin[jdx0] = self._qpin_array[idx, jdx0]
        if self._qma_diskflag_reading:
            k = 0
            for jdx0 in range(self._qma_length_0):
                self.qma[jdx0] = self._qma_ncarray[k]
                k += 1
        elif self._qma_ramflag:
            for jdx0 in range(self._qma_length_0):
                self.qma[jdx0] = self._qma_array[idx, jdx0]
        if self._qar_diskflag_reading:
            k = 0
            for jdx0 in range(self._qar_length_0):
                self.qar[jdx0] = self._qar_ncarray[k]
                k += 1
        elif self._qar_ramflag:
            for jdx0 in range(self._qar_length_0):
                self.qar[jdx0] = self._qar_array[idx, jdx0]
        if self._qpout_diskflag_reading:
            k = 0
            for jdx0 in range(self._qpout_length_0):
                self.qpout[jdx0] = self._qpout_ncarray[k]
                k += 1
        elif self._qpout_ramflag:
            for jdx0 in range(self._qpout_length_0):
                self.qpout[jdx0] = self._qpout_array[idx, jdx0]
        if self._qout_diskflag_reading:
            self.qout = self._qout_ncarray[0]
        elif self._qout_ramflag:
            self.qout = self._qout_array[idx]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._qin_diskflag_writing:
            self._qin_ncarray[0] = self.qin
        if self._qin_ramflag:
            self._qin_array[idx] = self.qin
        if self._qpin_diskflag_writing:
            k = 0
            for jdx0 in range(self._qpin_length_0):
                self._qpin_ncarray[k] = self.qpin[jdx0]
                k += 1
        if self._qpin_ramflag:
            for jdx0 in range(self._qpin_length_0):
                self._qpin_array[idx, jdx0] = self.qpin[jdx0]
        if self._qma_diskflag_writing:
            k = 0
            for jdx0 in range(self._qma_length_0):
                self._qma_ncarray[k] = self.qma[jdx0]
                k += 1
        if self._qma_ramflag:
            for jdx0 in range(self._qma_length_0):
                self._qma_array[idx, jdx0] = self.qma[jdx0]
        if self._qar_diskflag_writing:
            k = 0
            for jdx0 in range(self._qar_length_0):
                self._qar_ncarray[k] = self.qar[jdx0]
                k += 1
        if self._qar_ramflag:
            for jdx0 in range(self._qar_length_0):
                self._qar_array[idx, jdx0] = self.qar[jdx0]
        if self._qpout_diskflag_writing:
            k = 0
            for jdx0 in range(self._qpout_length_0):
                self._qpout_ncarray[k] = self.qpout[jdx0]
                k += 1
        if self._qpout_ramflag:
            for jdx0 in range(self._qpout_length_0):
                self._qpout_array[idx, jdx0] = self.qpout[jdx0]
        if self._qout_diskflag_writing:
            self._qout_ncarray[0] = self.qout
        if self._qout_ramflag:
            self._qout_array[idx] = self.qout
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "qin":
            self._qin_outputpointer = value.p_value
        if name == "qout":
            self._qout_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._qin_outputflag:
            self._qin_outputpointer[0] = self.qin
        if self._qout_outputflag:
            self._qout_outputpointer[0] = self.qout
@cython.final
cdef class LogSequences:
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
cdef class Model:
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
        self.sequences.inlets.load_data(idx)
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.inlets.save_data(idx)
        self.sequences.fluxes.save_data(idx)
        self.sequences.outlets.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.calc_qpin_v1()
        self.update_login_v1()
        self.calc_qma_v1()
        self.calc_qar_v1()
        self.calc_qpout_v1()
        self.update_logout_v1()
        self.calc_qout_v1()
    cpdef void update_inlets(self) noexcept nogil:
        cdef numpy.int64_t i
        if not self.threading:
            for i in range(self.sequences.inlets._q_length_0):
                if self.sequences.inlets._q_ready[i]:
                    self.sequences.inlets.q[i] = self.sequences.inlets._q_pointer[i][0]
                else:
                    self.sequences.inlets.q[i] = nan
        self.pick_q_v1()
    cpdef void update_outlets(self) noexcept nogil:
        self.pass_q_v1()
        cdef numpy.int64_t i
        if not self.threading:
            self.sequences.outlets._q_pointer[0] = self.sequences.outlets._q_pointer[0] + self.sequences.outlets.q
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
            self.sequences.fluxes.update_outputs()
    cpdef inline void pick_q_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qin = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qin = self.sequences.fluxes.qin + (self.sequences.inlets.q[idx])
    cpdef inline void calc_qpin_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb - 1):
            if self.sequences.fluxes.qin < self.parameters.derived.maxq[idx]:
                if idx == 0:
                    self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin
                else:
                    self.sequences.fluxes.qpin[idx] = 0.0
            elif self.sequences.fluxes.qin < self.parameters.derived.maxq[idx + 1]:
                self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin - self.parameters.derived.maxq[idx]
            else:
                self.sequences.fluxes.qpin[idx] = self.parameters.derived.diffq[idx]
        if self.parameters.derived.nmb == 1:
            self.sequences.fluxes.qpin[0] = self.sequences.fluxes.qin
        else:
            self.sequences.fluxes.qpin[self.parameters.derived.nmb - 1] = max(self.sequences.fluxes.qin - self.parameters.derived.maxq[self.parameters.derived.nmb - 1], 0.0)
    cpdef inline void update_login_v1(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ma_order[idx] - 2, -1, -1):
                self.sequences.logs.login[idx, jdx + 1] = self.sequences.logs.login[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            self.sequences.logs.login[idx, 0] = self.sequences.fluxes.qpin[idx]
    cpdef inline void calc_qma_v1(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qma[idx] = 0.0
            for jdx in range(self.parameters.derived.ma_order[idx]):
                self.sequences.fluxes.qma[idx] = self.sequences.fluxes.qma[idx] + (self.parameters.derived.ma_coefs[idx, jdx] * self.sequences.logs.login[idx, jdx])
    cpdef inline void calc_qar_v1(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qar[idx] = 0.0
            for jdx in range(self.parameters.derived.ar_order[idx]):
                self.sequences.fluxes.qar[idx] = self.sequences.fluxes.qar[idx] + (self.parameters.derived.ar_coefs[idx, jdx] * self.sequences.logs.logout[idx, jdx])
    cpdef inline void calc_qpout_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qpout[idx] = self.sequences.fluxes.qma[idx] + self.sequences.fluxes.qar[idx]
    cpdef inline void update_logout_v1(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ar_order[idx] - 2, -1, -1):
                self.sequences.logs.logout[idx, jdx + 1] = self.sequences.logs.logout[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            if self.parameters.derived.ar_order[idx] > 0:
                self.sequences.logs.logout[idx, 0] = self.sequences.fluxes.qpout[idx]
    cpdef inline void calc_qout_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qout = 0.0
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qout = self.sequences.fluxes.qout + (self.sequences.fluxes.qpout[idx])
    cpdef inline void pass_q_v1(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qout
    cpdef inline void pick_q(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qin = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qin = self.sequences.fluxes.qin + (self.sequences.inlets.q[idx])
    cpdef inline void calc_qpin(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb - 1):
            if self.sequences.fluxes.qin < self.parameters.derived.maxq[idx]:
                if idx == 0:
                    self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin
                else:
                    self.sequences.fluxes.qpin[idx] = 0.0
            elif self.sequences.fluxes.qin < self.parameters.derived.maxq[idx + 1]:
                self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin - self.parameters.derived.maxq[idx]
            else:
                self.sequences.fluxes.qpin[idx] = self.parameters.derived.diffq[idx]
        if self.parameters.derived.nmb == 1:
            self.sequences.fluxes.qpin[0] = self.sequences.fluxes.qin
        else:
            self.sequences.fluxes.qpin[self.parameters.derived.nmb - 1] = max(self.sequences.fluxes.qin - self.parameters.derived.maxq[self.parameters.derived.nmb - 1], 0.0)
    cpdef inline void update_login(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ma_order[idx] - 2, -1, -1):
                self.sequences.logs.login[idx, jdx + 1] = self.sequences.logs.login[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            self.sequences.logs.login[idx, 0] = self.sequences.fluxes.qpin[idx]
    cpdef inline void calc_qma(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qma[idx] = 0.0
            for jdx in range(self.parameters.derived.ma_order[idx]):
                self.sequences.fluxes.qma[idx] = self.sequences.fluxes.qma[idx] + (self.parameters.derived.ma_coefs[idx, jdx] * self.sequences.logs.login[idx, jdx])
    cpdef inline void calc_qar(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qar[idx] = 0.0
            for jdx in range(self.parameters.derived.ar_order[idx]):
                self.sequences.fluxes.qar[idx] = self.sequences.fluxes.qar[idx] + (self.parameters.derived.ar_coefs[idx, jdx] * self.sequences.logs.logout[idx, jdx])
    cpdef inline void calc_qpout(self) noexcept nogil:
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qpout[idx] = self.sequences.fluxes.qma[idx] + self.sequences.fluxes.qar[idx]
    cpdef inline void update_logout(self) noexcept nogil:
        cdef numpy.int64_t jdx
        cdef numpy.int64_t idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ar_order[idx] - 2, -1, -1):
                self.sequences.logs.logout[idx, jdx + 1] = self.sequences.logs.logout[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            if self.parameters.derived.ar_order[idx] > 0:
                self.sequences.logs.logout[idx, 0] = self.sequences.fluxes.qpout[idx]
    cpdef inline void calc_qout(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.qout = 0.0
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qout = self.sequences.fluxes.qout + (self.sequences.fluxes.qpout[idx])
    cpdef inline void pass_q(self) noexcept nogil:
        self.sequences.outlets.q = self.sequences.fluxes.qout
