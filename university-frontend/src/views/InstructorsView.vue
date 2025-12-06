<template>
  <div>
    <!-- Header -->
    <v-row class="mb-6" align="center">
      <v-col>
        <h1 class="text-h3 font-weight-bold text-white page-title">
          Instructors Management
        </h1>
        <p class="text-h6 text-purple-lighten-2">
          Manage instructor records and information
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-plus"
          @click="openCreateModal"
        >
          Add New Instructor
        </v-btn>
      </v-col>
    </v-row>

    <!-- Search and Filters -->
    <SearchFilters
      :filters="filters"
      context="instructor"
      @update:filters="handleFiltersUpdate"
      @search="handleSearch"
    />

    <!-- Stats -->
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <StatCard
          title="Total Instructors"
          :value="instructorsStore.totalInstructors"
          icon="mdi-account-tie"
          color="primary"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="With Courses"
          :value="instructorsWithCourses"
          icon="mdi-book-check"
          color="success"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="Available"
          :value="instructorsAvailable"
          icon="mdi-account-clock"
          color="info"
        />
      </v-col>
    </v-row>

    <!-- Instructor Data Table -->
    <v-card elevation="4">
      <v-card-title class="bg-primary text-white">
        <v-icon class="mr-2">mdi-table</v-icon>
        Instructor Records
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="instructorsStore.instructors"
        :loading="instructorsStore.loading"
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
            <p class="text-h6 text-grey mt-4">No instructors found.</p>
          </div>
        </template>

        <!-- Full Name Column -->
        <template v-slot:item.name="{ item }">
          {{ item.first_name }} {{ item.last_name }}
        </template>

        <!-- Department Column with Chip -->
        <template v-slot:item.department="{ item }">
          <v-chip color="secondary" size="small" label>
            {{ item.department }}
          </v-chip>
        </template>

        <!-- Salary Column with Formatting -->
        <template v-slot:item.salary="{ item }">
          <span class="font-weight-bold">
            {{ item.salary ? `$${item.salary.toLocaleString()}` : 'N/A' }}
          </span>
        </template>

        <!-- Courses Taught Column -->
        <template v-slot:item.courses_taught="{ item }">
          <v-chip-group v-if="item.courses_taught && item.courses_taught.length > 0">
            <v-chip
              v-for="course in item.courses_taught.slice(0, 2)"
              :key="course"
              size="x-small"
              color="info"
              label
            >
              {{ course }}
            </v-chip>
            <v-chip
              v-if="item.courses_taught.length > 2"
              size="x-small"
              color="grey"
              label
            >
              +{{ item.courses_taught.length - 2 }}
            </v-chip>
          </v-chip-group>
          <span v-else class="text-grey">None</span>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-pencil"
            size="small"
            color="primary"
            variant="text"
            @click="handleEditInstructor(item)"
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
      :pagination="instructorsStore.pagination"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Modal -->
    <InstructorFormModal
      :show="showCreateForm || showEditForm"
      :instructor="editingInstructor"
      @close="closeModal"
      @save="handleSaveInstructor"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :show="showDeleteConfirm"
      title="Confirm Deletion"
      message="Are you sure you want to delete this instructor record? All course associations will be removed."
      confirm-text="Delete"
      @close="showDeleteConfirm = false; instructorToDeleteId = null"
      @confirm="handleDeleteInstructor(instructorToDeleteId)"
    />

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="5000"
      location="top"
    >
      {{ instructorsStore.error }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useInstructorsStore } from '@/stores/instructors'
import SearchFilters from '@/components/SearchFilters.vue'
import Pagination from '@/components/Pagination.vue'
import InstructorFormModal from '@/components/InstructorFormModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import StatCard from '@/components/StatCard.vue'

const instructorsStore = useInstructorsStore()

const showCreateForm = ref(false)
const showEditForm = ref(false)
const editingInstructor = ref(null)
const showDeleteConfirm = ref(false)
const instructorToDeleteId = ref(null)
const showError = ref(false)

const filters = ref({
  search: '',
  page: 1,
  limit: 10,
  sortBy: 'employee_id',
  sortOrder: 1
})

const headers = [
  { title: 'Employee ID', key: 'employee_id', align: 'start' },
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Department', key: 'department', align: 'center' },
  { title: 'Salary', key: 'salary', align: 'end' },
  { title: 'Courses Taught', key: 'courses_taught', align: 'center' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
]

const instructorsWithCourses = computed(() => {
  return instructorsStore.instructors.filter(
    i => i.courses_taught && i.courses_taught.length > 0
  ).length
})

const instructorsAvailable = computed(() => {
  return instructorsStore.instructors.filter(
    i => !i.courses_taught || i.courses_taught.length === 0
  ).length
})

onMounted(() => {
  instructorsStore.fetchInstructors(filters.value)
})

watch(() => instructorsStore.error, (newError) => {
  if (newError) {
    showError.value = true
  }
})

const handleFiltersUpdate = (newFilters) => {
  filters.value = { ...filters.value, ...newFilters, page: 1 }
  instructorsStore.fetchInstructors(filters.value)
}

const handleSearch = () => {
  filters.value.page = 1
  instructorsStore.fetchInstructors(filters.value)
}

const handlePageChange = (page) => {
  filters.value.page = page
  instructorsStore.fetchInstructors(filters.value)
}

const openCreateModal = () => {
  editingInstructor.value = null
  showCreateForm.value = true
}

const handleEditInstructor = (instructor) => {
  editingInstructor.value = instructor
  showEditForm.value = true
}

const showConfirmDelete = (instructorId) => {
  instructorToDeleteId.value = instructorId
  showDeleteConfirm.value = true
}

const handleDeleteInstructor = async (instructorId) => {
  try {
    showDeleteConfirm.value = false
    await instructorsStore.deleteInstructor(instructorId)
    await instructorsStore.fetchInstructors(filters.value)
  } catch (error) {
    console.error('Failed to delete instructor:', error)
  }
}

const handleSaveInstructor = async (instructorData) => {
  try {
    if (editingInstructor.value) {
      await instructorsStore.updateInstructor(editingInstructor.value._id, instructorData)
    } else {
      await instructorsStore.createInstructor(instructorData)
    }
    closeModal()
    instructorsStore.fetchInstructors(filters.value)
  } catch (error) {
    console.error('Failed to save instructor:', error)
  }
}

const closeModal = () => {
  showCreateForm.value = false
  showEditForm.value = false
  editingInstructor.value = null
}
</script>

<style scoped>
.page-title {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
}
</style>