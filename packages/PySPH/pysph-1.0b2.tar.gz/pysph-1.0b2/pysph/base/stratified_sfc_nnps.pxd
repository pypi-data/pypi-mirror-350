# cython: language_level=3, embedsignature=True
# distutils: language=c++
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp.pair cimport pair

from .nnps_base cimport *

cdef extern from 'math.h':
    int abs(int) nogil
    double ceil(double) nogil
    double floor(double) nogil
    double fabs(double) nogil
    double fmax(double, double) nogil
    double fmin(double, double) nogil

cdef extern from 'math.h':
    double log(double) nogil
    double log2(double) nogil

cdef extern from "z_order.h":
    ctypedef unsigned int uint32_t
    ctypedef unsigned long long uint64_t
    uint64_t get_key(uint64_t i, uint64_t j, uint64_t k) nogil

    cdef cppclass CompareSortWrapper:
        CompareSortWrapper() except + 
        CompareSortWrapper(uint32_t* current_pids, uint64_t* current_keys,
                int length) except + nogil 
        inline void compare_sort() noexcept nogil

cdef class StratifiedSFCNNPS(NNPS):
    ############################################################################
    # Data Attributes
    ############################################################################
    cdef double radius_scale2
    cdef bint asymmetric

    cdef public int num_levels
    cdef int max_num_bits

    cdef uint64_t* max_keys
    cdef uint64_t current_max_key
    cdef uint64_t max_possible_key

    cdef double interval_size

    cdef uint32_t** pids
    cdef uint32_t* current_pids

    cdef uint64_t** keys
    cdef uint64_t* current_keys

    cdef int*** key_to_idx
    cdef int** current_key_to_idx

    cdef double** cell_sizes
    cdef double* current_cells

    cdef double*** hmax
    cdef double** current_hmax

    cdef int** num_cells
    cdef int* current_num_cells

    cdef vector[int]** nbr_boxes
    cdef vector[int]* current_nbr_boxes

    cdef int*** key_to_nbr_idx
    cdef int** current_key_to_nbr_idx

    cdef int*** key_to_nbr_length
    cdef int** current_key_to_nbr_length

    cdef int* total_mask_len
    cdef int current_mask_len

    cdef NNPSParticleArrayWrapper dst, src

    ##########################################################################
    # Member functions
    ##########################################################################
    cpdef np.ndarray get_keys(self, pa_index)

    cpdef set_context(self, int src_index, int dst_index)

    cdef inline int _get_H(self, double h_q, double h_j)

    cdef inline int get_idx(self, uint64_t key, uint64_t max_key, int* key_to_idx) noexcept nogil

    cdef void _fill_nbr_boxes(self)

    cdef int _neighbor_boxes_func(self, int i, int j, int k, int H,
            int* current_key_to_idx_level, uint64_t max_key,
            double current_cell_size, double* current_hmax_level, 
            vector[int]* nbr_boxes)

    cdef int _neighbor_boxes_asym(self, int i, int j, int k, int H,
            int* current_key_to_idx_level, uint64_t max_key,
            double current_cell_size, double* current_hmax_level,
            vector[int]* nbr_boxes) noexcept nogil

    cdef int _neighbor_boxes_sym(self, int i, int j, int k, int H,
            int* current_key_to_idx_level, uint64_t max_key,
            double current_cell_size, double* current_hmax_level,
            vector[int]* nbr_boxes) noexcept nogil

    cpdef double get_binning_size(self, int interval)

    cpdef int get_number_of_particles(self, int pa_index, int level)

    cpdef get_spatially_ordered_indices(self, int pa_index, LongArray indices)

    cdef void find_nearest_neighbors(self, size_t d_idx, UIntArray nbrs) noexcept nogil

    cdef void fill_array(self, NNPSParticleArrayWrapper pa_wrapper,
            int pa_index, uint32_t* current_pids,
            uint64_t* current_keys, double* current_cells, int* current_num_cells)

    cdef inline int _get_level(self, double h) noexcept nogil

    cpdef _refresh(self)

    cpdef _bin(self, int pa_index, UIntArray indices)
