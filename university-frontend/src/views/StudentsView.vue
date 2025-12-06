<template>
  <div>
    <!-- Header -->
    <v-row class="mb-6" align="center">
      <v-col>
        <h1 class="text-h3 font-weight-bold text-white page-title">
          Students Management
        </h1>
        <p class="text-h6 text-purple-lighten-2">
          Manage student records and information
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-plus"
          @click="openCreateModal"
        >
          Add New Student
        </v-btn>
      </v-col>
    </v-row>

    <!-- Search and Filters -->
    <SearchFilters
      :filters="filters"
      context="student"
      @update:filters="handleFiltersUpdate"
      @search="handleSearch"
    />

    <!-- Stats -->
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <StatCard
          title="Total Students"
          :value="studentsStore.totalStudents"
          icon="mdi-account-group"
          color="primary"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="Active Students"
          :value="studentsStore.activeStudents.length"
          icon="mdi-check-circle"
          color="success"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="Inactive Students"
          :value="studentsStore.inactiveStudents.length"
          icon="mdi-close-circle"
          color="error"
        />
      </v-col>
    </v-row>

    <!-- Student Data Table -->
    <v-card elevation="4">
      <v-card-title class="bg-primary text-white">
        <v-icon class="mr-2">mdi-table</v-icon>
        Student Records
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="studentsStore.students"
        :loading="studentsStore.loading"
        item-key="_id"
        :items-per-page="-1"
        hide-default-footer
      >
        <!-- Loading -->
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>

        <!-- No Data -->
        <template v-slot:no-data>
          <div class="text-center pa-8">
            <v-icon size="64" color="grey">mdi-account-off</v-icon>
            <p class="text-h6 text-grey mt-4">No students found matching your criteria.</p>
          </div>
        </template>

        <!-- GPA Column -->
        <template v-slot:item.gpa="{ item }">
          <v-chip
            :color="getGpaColor(item.gpa)"
            size="small"
            label
          >
            {{ item.gpa ? item.gpa.toFixed(2) : 'N/A' }}
          </v-chip>
        </template>

        <!-- Status Column -->
        <template v-slot:item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            size="small"
            label
          >
            <v-icon start size="small">
              {{ item.is_active ? 'mdi-check' : 'mdi-close' }}
            </v-icon>
            {{ item.is_active ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-pencil"
            size="small"
            color="primary"
            variant="text"
            @click="handleEditStudent(item)"
          ></v-btn>
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            variant="text"
            @click="showConfirmDelete(item._id)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Pagination -->
    <Pagination
      :pagination="studentsStore.pagination"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Modal -->
    <StudentFormModal
      :show="showCreateForm || showEditForm"
      :student="editingStudent"
      @close="closeModal"
      @save="handleSaveStudent"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :show="showDeleteConfirm"
      title="Confirm Deletion"
      message="Are you sure you want to delete this student record? This action cannot be undone."
      confirm-text="Delete"
      @close="showDeleteConfirm = false; studentToDeleteId = null"
      @confirm="handleDeleteStudent(studentToDeleteId)"
    />

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="5000"
      location="top"
    >
      {{ studentsStore.error }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useStudentsStore } from '@/stores/students'
import SearchFilters from '@/components/SearchFilters.vue'
import Pagination from '@/components/Pagination.vue'
import StudentFormModal from '@/components/StudentFormModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import StatCard from '@/components/StatCard.vue'

const studentsStore = useStudentsStore()

const showCreateForm = ref(false)
const showEditForm = ref(false)
const editingStudent = ref(null)
const showDeleteConfirm = ref(false)
const studentToDeleteId = ref(null)
const showError = ref(false)

const filters = ref({
  search: '',
  gpaFilter: null,
  statusFilter: 'all',
  page: 1,
  limit: 10,
  sortBy: 'student_id',
  sortOrder: 1
})

const headers = [
  { title: 'ID', key: 'student_id', align: 'start' },
  { title: 'First Name', key: 'first_name' },
  { title: 'Last Name', key: 'last_name' },
  { title: 'Email', key: 'email' },
  { title: 'GPA', key: 'gpa', align: 'center' },
  { title: 'Status', key: 'is_active', align: 'center' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
]

onMounted(() => {
  studentsStore.fetchStudents(filters.value)
})

watch(() => studentsStore.error, (newError) => {
  if (newError) {
    showError.value = true
  }
})

const handleFiltersUpdate = (newFilters) => {
  filters.value = { ...filters.value, ...newFilters, page: 1 }
  studentsStore.fetchStudents(filters.value)
}

const handleSearch = () => {
  filters.value.page = 1
  studentsStore.fetchStudents(filters.value)
}

const handlePageChange = (page) => {
  filters.value.page = page
  studentsStore.fetchStudents(filters.value)
}

const openCreateModal = () => {
  editingStudent.value = null
  showCreateForm.value = true
}

const handleEditStudent = (student) => {
  editingStudent.value = student
  showEditForm.value = true
}

const showConfirmDelete = (studentId) => {
  studentToDeleteId.value = studentId
  showDeleteConfirm.value = true
}

const handleDeleteStudent = async (studentId) => {
  try {
    showDeleteConfirm.value = false
    await studentsStore.deleteStudent(studentId)
    await studentsStore.fetchStudents(filters.value)
  } catch (error) {
    console.error('Failed to delete student:', error)
  }
}

const handleSaveStudent = async (studentData) => {
  try {
    if (editingStudent.value) {
      await studentsStore.updateStudent(editingStudent.value._id, studentData)
    } else {
      await studentsStore.createStudent(studentData)
    }
    closeModal()
    studentsStore.fetchStudents(filters.value)
  } catch (error) {
    console.error('Failed to save student:', error)
  }
}

const closeModal = () => {
  showCreateForm.value = false
  showEditForm.value = false
  editingStudent.value = null
}

const getGpaColor = (gpa) => {
  if (gpa >= 3.5) return 'success'
  if (gpa >= 3.0) return 'warning'
  return 'error'
}
</script>

<style scoped>
.page-title {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
}
</style>