# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

"""This module defines the Cython declarations related to module |anntools|."""

cimport numpy


cdef class ANN:

    # required for usage as an "algorithm" by interputils:

    cdef public numpy.int64_t nmb_inputs
    cdef public numpy.int64_t nmb_outputs
    cdef public double[:] inputs
    cdef public double[:] outputs
    cdef public double[:] output_derivatives

    cpdef inline void calculate_values(self) noexcept nogil
    cpdef inline void calculate_derivatives(self, numpy.int64_t idx_input) noexcept nogil

    # algorithm-specific requirements:

    cdef public numpy.int64_t nmb_layers
    cdef public numpy.int64_t[:] nmb_neurons
    cdef public double[:, :] weights_input
    cdef public double[:, :] weights_output
    cdef public double[:, :, :] weights_hidden
    cdef public double[:, :] intercepts_hidden
    cdef public double[:] intercepts_output
    cdef public numpy.int64_t[:, :] activation
    cdef public double[:, :] neurons
    cdef public double[:, :] neuron_derivatives

    cdef inline void apply_activationfunction(self, numpy.int64_t idx_layer, numpy.int64_t idx_neuron, double input_) noexcept nogil
    cdef inline double apply_derivativefunction(self, numpy.int64_t idx_layer, numpy.int64_t idx_neuron, double inner) noexcept nogil
