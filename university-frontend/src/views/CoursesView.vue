<template>
  <div>
    <!-- Header -->
    <v-row class="mb-6" align="center">
      <v-col>
        <h1 class="text-h3 font-weight-bold text-white page-title">
          Courses Management
        </h1>
        <p class="text-h6 text-purple-lighten-2">
          Manage course records and information
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-plus"
          @click="openCreateModal"
        >
          Add New Course
        </v-btn>
      </v-col>
    </v-row>

    <!-- Search and Filters -->
    <SearchFilters
      :filters="filters"
      context="course"
      @update:filters="handleFiltersUpdate"
      @search="handleSearch"
    />

    <!-- Stats -->
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <StatCard
          title="Total Courses"
          :value="coursesStore.totalCourses"
          icon="mdi-book-open-variant"
          color="primary"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="With Instructor"
          :value="coursesWithInstructor"
          icon="mdi-account-check"
          color="success"
        />
      </v-col>
      <v-col cols="12" md="4">
        <StatCard
          title="Unassigned"
          :value="coursesUnassigned"
          icon="mdi-account-question"
          color="warning"
        />
      </v-col>
    </v-row>

    <!-- Course Data Table -->
    <v-card elevation="4">
      <v-card-title class="bg-primary text-white">
        <v-icon class="mr-2">mdi-table</v-icon>
        Course Records
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="coursesStore.courses"
        :loading="coursesStore.loading"
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
            <v-icon size="64" color="grey">mdi-book-off</v-icon>
            <p class="text-h6 text-grey mt-4">No courses found.</p>
          </div>
        </template>

        <!-- Course Code Column with Chip -->
        <template v-slot:item.course_code="{ item }">
          <v-chip color="primary" label>
            {{ item.course_code }}
          </v-chip>
        </template>

        <!-- Credit Hours with Badge -->
        <template v-slot:item.credit_hours="{ item }">
          <v-chip color="secondary" size="small">
            {{ item.credit_hours }} Credits
          </v-chip>
        </template>

        <!-- Instructor Column -->
        <template v-slot:item.instructor_id="{ item }">
          <v-chip
            v-if="item.instructor_id"
            color="success"
            size="small"
            label
          >
            <v-icon start size="small">mdi-check</v-icon>
            Assigned
          </v-chip>
          <v-chip
            v-else
            color="warning"
            size="small"
            label
          >
            <v-icon start size="small">mdi-alert</v-icon>
            Unassigned
          </v-chip>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-pencil"
            size="small"
            color="primary"
            variant="text"
            @click="handleEditCourse(item)"
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
      :pagination="coursesStore.pagination"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Modal -->
    <CourseFormModal
      :show="showCreateForm || showEditForm"
      :course="editingCourse"
      @close="closeModal"
      @save="handleSaveCourse"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :show="showDeleteConfirm"
      title="Confirm Deletion"
      message="Are you sure you want to delete this course? This will automatically unenroll all students and remove the course from instructor records."
      confirm-text="Delete"
      @close="showDeleteConfirm = false; courseToDeleteId = null"
      @confirm="handleDeleteCourse(courseToDeleteId)"
    />

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="5000"
      location="top"
    >
      {{ coursesStore.error }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useCoursesStore } from '@/stores/courses'
import SearchFilters from '@/components/SearchFilters.vue'
import Pagination from '@/components/Pagination.vue'
import CourseFormModal from '@/components/CourseFormModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import StatCard from '@/components/StatCard.vue'

const coursesStore = useCoursesStore()

const showCreateForm = ref(false)
const showEditForm = ref(false)
const editingCourse = ref(null)
const showDeleteConfirm = ref(false)
const courseToDeleteId = ref(null)
const showError = ref(false)

const filters = ref({
  search: '',
  page: 1,
  limit: 10,
  sortBy: 'course_code',
  sortOrder: 1
})

const headers = [
  { title: 'Course Code', key: 'course_code', align: 'start' },
  { title: 'Title', key: 'title' },
  { title: 'Description', key: 'description' },
  { title: 'Credits', key: 'credit_hours', align: 'center' },
  { title: 'Instructor', key: 'instructor_id', align: 'center' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
]

const coursesWithInstructor = computed(() => {
  return coursesStore.courses.filter(c => c.instructor_id).length
})

const coursesUnassigned = computed(() => {
  return coursesStore.courses.filter(c => !c.instructor_id).length
})

onMounted(() => {
  coursesStore.fetchCourses(filters.value)
})

watch(() => coursesStore.error, (newError) => {
  if (newError) {
    showError.value = true
  }
})

const handleFiltersUpdate = (newFilters) => {
  filters.value = { ...filters.value, ...newFilters, page: 1 }
  coursesStore.fetchCourses(filters.value)
}

const handleSearch = () => {
  filters.value.page = 1
  coursesStore.fetchCourses(filters.value)
}

const handlePageChange = (page) => {
  filters.value.page = page
  coursesStore.fetchCourses(filters.value)
}

const openCreateModal = () => {
  editingCourse.value = null
  showCreateForm.value = true
}

const handleEditCourse = (course) => {
  editingCourse.value = course
  showEditForm.value = true
}

const showConfirmDelete = (courseId) => {
  courseToDeleteId.value = courseId
  showDeleteConfirm.value = true
}

const handleDeleteCourse = async (courseId) => {
  try {
    showDeleteConfirm.value = false
    await coursesStore.deleteCourse(courseId)
    await coursesStore.fetchCourses(filters.value)
  } catch (error) {
    console.error('Failed to delete course:', error)
  }
}

const handleSaveCourse = async (courseData) => {
  try {
    if (editingCourse.value) {
      await coursesStore.updateCourse(editingCourse.value._id, courseData)
    } else {
      await coursesStore.createCourse(courseData)
    }
    closeModal()
    coursesStore.fetchCourses(filters.value)
  } catch (error) {
    console.error('Failed to save course:', error)
  }
}

const closeModal = () => {
  showCreateForm.value = false
  showEditForm.value = false
  editingCourse.value = null
}
</script>

<style scoped>
.page-title {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
}
</style>