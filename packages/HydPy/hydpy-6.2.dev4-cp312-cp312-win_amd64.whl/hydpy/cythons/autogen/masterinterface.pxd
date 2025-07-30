# !python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True

cimport numpy

from hydpy.cythons.autogen cimport interfaceutils


cdef class MasterInterface(interfaceutils.BaseInterface):

    cdef void new2old(self)  noexcept nogil

    cdef void determine_interceptionevaporation(self, )  noexcept nogil

    cdef void determine_soilevapotranspiration(self, )  noexcept nogil

    cdef void determine_waterevaporation(self, )  noexcept nogil

    cdef double get_interceptionevaporation(self, numpy.int64_t k)  noexcept nogil

    cdef double get_soilevapotranspiration(self, numpy.int64_t k)  noexcept nogil

    cdef double get_waterevaporation(self, numpy.int64_t k)  noexcept nogil

    cdef double calculate_discharge(self, double waterdepth)  noexcept nogil

    cdef void determine_potentialevapotranspiration(self, )  noexcept nogil

    cdef double get_meanpotentialevapotranspiration(self, )  noexcept nogil

    cdef double get_potentialevapotranspiration(self, numpy.int64_t k)  noexcept nogil

    cdef void determine_potentialinterceptionevaporation(self, )  noexcept nogil

    cdef void determine_potentialsoilevapotranspiration(self, )  noexcept nogil

    cdef void determine_potentialwaterevaporation(self, )  noexcept nogil

    cdef double get_potentialinterceptionevaporation(self, numpy.int64_t k)  noexcept nogil

    cdef double get_potentialsoilevapotranspiration(self, numpy.int64_t k)  noexcept nogil

    cdef double get_potentialwaterevaporation(self, numpy.int64_t k)  noexcept nogil

    cdef double get_precipitation(self, numpy.int64_t k)  noexcept nogil

    cdef void determine_precipitation(self, )  noexcept nogil

    cdef double get_meanprecipitation(self, )  noexcept nogil

    cdef double get_clearskysolarradiation(self, )  noexcept nogil

    cdef double get_globalradiation(self, )  noexcept nogil

    cdef double get_possiblesunshineduration(self, )  noexcept nogil

    cdef double get_sunshineduration(self, )  noexcept nogil

    cdef void process_radiation(self, )  noexcept nogil

    cdef void determine_outflow(self, )  noexcept nogil

    cdef double get_outflow(self, )  noexcept nogil

    cdef void set_inflow(self, double inflow)  noexcept nogil

    cdef double get_celerity(self, )  noexcept nogil

    cdef double get_discharge(self, )  noexcept nogil

    cdef double get_surfacewidth(self, )  noexcept nogil

    cdef double get_wettedarea(self, )  noexcept nogil

    cdef void use_waterdepth(self, double waterdepth)  noexcept nogil

    cdef void use_waterlevel(self, double waterlevel)  noexcept nogil

    cdef double get_waterdepth(self, )  noexcept nogil

    cdef double get_waterlevel(self, )  noexcept nogil

    cdef double get_wettedperimeter(self, )  noexcept nogil

    cdef void use_wettedarea(self, double wettedarea)  noexcept nogil

    cdef void determine_discharge(self, )  noexcept nogil

    cdef void determine_maxtimestep(self, )  noexcept nogil

    cdef double get_dischargevolume(self, )  noexcept nogil

    cdef double get_maxtimestep(self, )  noexcept nogil

    cdef void set_timestep(self, double timestep)  noexcept nogil

    cdef double get_partialdischargeupstream(self, double clientdischarge)  noexcept nogil

    cdef double get_partialdischargedownstream(self, double clientdischarge)  noexcept nogil

    cdef double get_watervolume(self, )  noexcept nogil

    cdef void update_storage(self, )  noexcept nogil

    cdef void add_soilwater(self, numpy.int64_t k)  noexcept nogil

    cdef void execute_infiltration(self, numpy.int64_t k)  noexcept nogil

    cdef double get_infiltration(self, numpy.int64_t k)  noexcept nogil

    cdef double get_percolation(self, numpy.int64_t k)  noexcept nogil

    cdef double get_soilwateraddition(self, numpy.int64_t k)  noexcept nogil

    cdef double get_soilwatercontent(self, numpy.int64_t k)  noexcept nogil

    cdef double get_soilwaterremoval(self, numpy.int64_t k)  noexcept nogil

    cdef void remove_soilwater(self, numpy.int64_t k)  noexcept nogil

    cdef void set_actualsurfacewater(self, numpy.int64_t k, double v)  noexcept nogil

    cdef void set_initialsurfacewater(self, numpy.int64_t k, double v)  noexcept nogil

    cdef void set_soilwaterdemand(self, numpy.int64_t k, double v)  noexcept nogil

    cdef void set_soilwatersupply(self, numpy.int64_t k, double v)  noexcept nogil

    cdef double get_interceptedwater(self, numpy.int64_t k)  noexcept nogil

    cdef double get_snowalbedo(self, numpy.int64_t k)  noexcept nogil

    cdef double get_snowcover(self, numpy.int64_t k)  noexcept nogil

    cdef double get_snowycanopy(self, numpy.int64_t k)  noexcept nogil

    cdef double get_soilwater(self, numpy.int64_t k)  noexcept nogil

    cdef double get_meantemperature(self, )  noexcept nogil

    cdef double get_temperature(self, numpy.int64_t k)  noexcept nogil

    cdef void determine_temperature(self, )  noexcept nogil
