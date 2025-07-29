# cython: language_level=3, embedsignature=True
# distutils: language=c++
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

from libcpp.vector cimport vector

from .nnps_base cimport *

#Imports for SpatialHashNNPS
cdef extern from "spatial_hash.h":
    cdef cppclass HashEntry:
        double h_max

        vector[unsigned int] *get_indices() noexcept nogil

    cdef cppclass HashTable:
        HashTable(long long int) except + nogil 
        void add(int, int, int, int, double) noexcept nogil
        HashEntry* get(int, int, int) noexcept nogil

# NNPS using Spatial Hashing algorithm
cdef class SpatialHashNNPS(NNPS):
    ############################################################################
    # Data Attributes
    ############################################################################
    cdef long long int table_size               # Size of hashtable
    cdef double radius_scale2

    cdef HashTable** hashtable
    cdef HashTable* current_hash

    cdef NNPSParticleArrayWrapper dst, src

    ##########################################################################
    # Member functions
    ##########################################################################

    cpdef set_context(self, int src_index, int dst_index)

    cdef void find_nearest_neighbors(self, size_t d_idx, UIntArray nbrs) noexcept nogil

    cdef inline void _add_to_hashtable(self, int hash_id, unsigned int pid, double h,
            int i, int j, int k) noexcept nogil

    cdef inline int _neighbor_boxes(self, int i, int j, int k,
            int* x, int* y, int* z) noexcept nogil

    cpdef _refresh(self)

    cpdef _bin(self, int pa_index, UIntArray indices)

# NNPS using Extended Spatial Hashing algorithm
cdef class ExtendedSpatialHashNNPS(NNPS):
    ############################################################################
    # Data Attributes
    ############################################################################
    cdef long long int table_size               # Size of hashtable
    cdef double radius_scale2

    cdef HashTable** hashtable
    cdef HashTable* current_hash

    cdef NNPSParticleArrayWrapper dst, src

    cdef int H
    cdef double h_sub
    cdef bint approximate

    ##########################################################################
    # Member functions
    ##########################################################################

    cpdef set_context(self, int src_index, int dst_index)

    cdef void find_nearest_neighbors(self, size_t d_idx, UIntArray nbrs) noexcept nogil

    cdef inline int _h_mask_approx(self, int* x, int* y, int* z) noexcept nogil

    cdef inline int _h_mask_exact(self, int* x, int* y, int* z) noexcept nogil

    cdef int _neighbor_boxes(self, int i, int j, int k,
            int* x, int* y, int* z, double h) noexcept nogil

    cdef inline void _add_to_hashtable(self, int hash_id, unsigned int pid, double h,
            int i, int j, int k) noexcept nogil

    cpdef _refresh(self)

    cpdef _bin(self, int pa_index, UIntArray indices)
