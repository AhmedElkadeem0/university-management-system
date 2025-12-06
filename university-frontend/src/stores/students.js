import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { studentsAPI } from '@/services/api' // ✅ FIXED PATH

export const useStudentsStore = defineStore('students', () => {
  const students = ref([])
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    limit: 10,
    totalPages: 1,
    totalResults: 0
  })
  const currentStudent = ref(null)

  // Getters
  const totalStudents = computed(() => pagination.value.totalResults || 0)
  const activeStudents = computed(() => students.value.filter(s => s.is_active))
  const inactiveStudents = computed(() => students.value.filter(s => !s.is_active))

  // Actions
  const fetchStudents = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.getAll(params)
      
      // ✅ FIXED: Backend returns { success, data: [...], pagination: {...} }
      students.value = response.data.data || []
      
      pagination.value = {
        page: response.data.pagination?.page || params.page || 1,
        limit: response.data.pagination?.limit || params.limit || 10,
        totalPages: response.data.pagination?.totalPages || 1,
        totalResults: response.data.pagination?.totalResults || 0
      }

    } catch (err) {
      error.value = 'Failed to fetch students. Please check your backend server.'
      console.error('Error fetching students:', err)
      students.value = []
      pagination.value = { page: 1, limit: 10, totalPages: 1, totalResults: 0 }
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchStudentById = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.getById(id)
      currentStudent.value = response.data.data
    } catch (err) {
      error.value = `Failed to fetch student with ID: ${id}`
      console.error('Error fetching student by ID:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createStudent = async (studentData) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.create(studentData)
      // ✅ FIXED: Backend returns { success, message, data: {...} }
      const newStudent = response.data.data
      
      // Add to front of list
      students.value.unshift(newStudent)
      pagination.value.totalResults += 1
      
      return newStudent
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create student'
      console.error('Error creating student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateStudent = async (id, updateData) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.update(id, updateData)
      // ✅ FIXED: Backend returns { status, message, data: {...} }
      const updatedStudent = response.data.data
      
      const index = students.value.findIndex(s => s._id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent
      }
      
      return updatedStudent
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update student'
      console.error('Error updating student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteStudent = async (id) => {
    loading.value = true
    error.value = null
    try {
      await studentsAPI.delete(id)
      students.value = students.value.filter(s => s._id !== id)
      pagination.value.totalResults -= 1
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete student'
      console.error('Error deleting student:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    students,
    loading,
    error,
    pagination,
    currentStudent,
    totalStudents,
    activeStudents,
    inactiveStudents,
    fetchStudents,
    fetchStudentById,
    createStudent,
    updateStudent,
    deleteStudent,
    clearError
  }
})