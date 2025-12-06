import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { coursesAPI } from '@/services/api'

export const useCoursesStore = defineStore('courses', () => {
  const courses = ref([])
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    limit: 10,
    totalPages: 1,
    totalResults: 0
  })
  const currentCourse = ref(null)

  // Getters
  const totalCourses = computed(() => pagination.value.totalResults || 0)

  // Actions
  const fetchCourses = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await coursesAPI.getAll(params)
      
      // ✅ FIXED: Backend returns { success, data: [...], pagination: {...} }
      courses.value = response.data.data || []
      
      pagination.value = {
        page: response.data.pagination?.page || params.page || 1,
        limit: response.data.pagination?.limit || params.limit || 10,
        totalPages: response.data.pagination?.totalPages || 1,
        totalResults: response.data.pagination?.total || response.data.pagination?.totalResults || 0
      }
    } catch (err) {
      error.value = 'Failed to fetch courses'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createCourse = async (courseData) => {
    loading.value = true
    error.value = null
    try {
      const response = await coursesAPI.create(courseData)
      // ✅ FIXED: Backend returns { success, message, data: {...} }
      const newCourse = response.data.data
      
      courses.value.unshift(newCourse)
      pagination.value.totalResults += 1
      
      return newCourse
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create course'
      console.error('Error creating course:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCourse = async (id, updateData) => {
    loading.value = true
    error.value = null
    try {
      const response = await coursesAPI.update(id, updateData)
      // ✅ FIXED: Backend returns { success, message, data: {...} }
      const updatedCourse = response.data.data
      
      const index = courses.value.findIndex(c => c._id === id)
      if (index !== -1) {
        courses.value[index] = updatedCourse
      }
      
      return updatedCourse
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update course'
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCourse = async (id) => {
    loading.value = true
    error.value = null
    try {
      await coursesAPI.delete(id)
      courses.value = courses.value.filter(c => c._id !== id)
      pagination.value.totalResults -= 1
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete course'
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
    courses,
    loading,
    error,
    pagination,
    currentCourse,
    totalCourses,
    fetchCourses,
    createCourse,
    updateCourse,
    deleteCourse,
    clearError
  }
})