import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { instructorsAPI } from '@/services/api'

export const useInstructorsStore = defineStore('instructors', () => {
  const instructors = ref([])
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({ page: 1, limit: 10, totalResults: 0, totalPages: 1 })
  const currentInstructor = ref(null)

  // Getters
  const totalInstructors = computed(() => pagination.value.totalResults || 0)

  // Actions
  const fetchInstructors = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await instructorsAPI.getAll(params)
      
      // ✅ FIXED: Backend returns { success, data: [...], pagination: {...} }
      instructors.value = response.data.data || []
      
      pagination.value = {
        page: response.data.pagination?.page || params.page || 1,
        limit: response.data.pagination?.limit || params.limit || 10,
        totalPages: response.data.pagination?.totalPages || 1,
        totalResults: response.data.pagination?.totalResults || 0
      }
    } catch (err) {
      error.value = 'Failed to fetch instructors'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createInstructor = async (instructorData) => {
    loading.value = true
    error.value = null
    try {
      const response = await instructorsAPI.create(instructorData)
      // ✅ FIXED: Backend returns { success, message, data: {...} }
      const newInstructor = response.data.data
      
      instructors.value.unshift(newInstructor)
      pagination.value.totalResults += 1
      
      return newInstructor
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create instructor'
      console.error('Error creating instructor:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateInstructor = async (id, updateData) => {
    loading.value = true
    error.value = null
    try {
      const response = await instructorsAPI.update(id, updateData)
      // ✅ FIXED: Backend returns { success, message, data: {...} }
      const updatedInstructor = response.data.data
      
      const index = instructors.value.findIndex(i => i._id === id)
      if (index !== -1) {
        instructors.value[index] = updatedInstructor
      }
      
      return updatedInstructor
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update instructor'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteInstructor = async (id) => {
    loading.value = true
    error.value = null
    try {
      await instructorsAPI.delete(id)
      instructors.value = instructors.value.filter(i => i._id !== id)
      pagination.value.totalResults -= 1
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete instructor'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    instructors,
    loading,
    error,
    pagination,
    currentInstructor,
    totalInstructors,
    fetchInstructors,
    createInstructor,
    updateInstructor,
    deleteInstructor,
    clearError
  }
})