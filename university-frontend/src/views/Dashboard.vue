<template>
  <div>
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-h3 font-weight-bold text-white mb-2 page-title">
        University Management Dashboard
      </h1>
      <p class="text-h6 text-purple-lighten-2">
        System-wide performance metrics and recent activities overview.
      </p>
    </div>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="white"
          size="64"
        ></v-progress-circular>
        <p class="text-white mt-4">Loading dashboard data...</p>
      </v-col>
    </v-row>

    <!-- Stats Grid -->
    <v-row v-else class="mb-6">
      <!-- Total Students -->
      <v-col cols="12" sm="6" lg="3">
        <v-card color="blue darken-1" class="pa-4" elevation="4">
          <v-row align="center">
            <v-col cols="auto">
              <v-avatar color="blue lighten-1" size="56">
                <v-icon size="32" color="white">mdi-account-group</v-icon>
              </v-avatar>
            </v-col>
            <v-col>
              <div class="text-h4 font-weight-bold text-white">
                {{ stats.totalStudents }}
              </div>
              <div class="text-subtitle-1 text-blue-lighten-4">
                Total Students
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Active Students -->
      <v-col cols="12" sm="6" lg="3">
        <v-card color="green darken-1" class="pa-4" elevation="4">
          <v-row align="center">
            <v-col cols="auto">
              <v-avatar color="green lighten-1" size="56">
                <v-icon size="32" color="white">mdi-check-circle</v-icon>
              </v-avatar>
            </v-col>
            <v-col>
              <div class="text-h4 font-weight-bold text-white">
                {{ stats.activeStudents }}
              </div>
              <div class="text-subtitle-1 text-green-lighten-4">
                Active Students
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Total Instructors -->
      <v-col cols="12" sm="6" lg="3">
        <v-card color="purple darken-1" class="pa-4" elevation="4">
          <v-row align="center">
            <v-col cols="auto">
              <v-avatar color="purple lighten-1" size="56">
                <v-icon size="32" color="white">mdi-account-tie</v-icon>
              </v-avatar>
            </v-col>
            <v-col>
              <div class="text-h4 font-weight-bold text-white">
                {{ stats.totalInstructors }}
              </div>
              <div class="text-subtitle-1 text-purple-lighten-4">
                Total Instructors
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Total Courses -->
      <v-col cols="12" sm="6" lg="3">
        <v-card color="orange darken-1" class="pa-4" elevation="4">
          <v-row align="center">
            <v-col cols="auto">
              <v-avatar color="orange lighten-1" size="56">
                <v-icon size="32" color="white">mdi-book-open-page-variant</v-icon>
              </v-avatar>
            </v-col>
            <v-col>
              <div class="text-h4 font-weight-bold text-white">
                {{ stats.totalCourses }}
              </div>
              <div class="text-subtitle-1 text-orange-lighten-4">
                Total Courses
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Activity & Quick Actions -->
    <v-row>
      <!-- Recent Students List -->
      <v-col cols="12" lg="8">
        <v-card elevation="4">
          <v-card-title class="bg-primary text-white">
            <v-icon class="mr-2">mdi-clock-outline</v-icon>
            Recent Students (Last {{ recentStudents.length }})
          </v-card-title>

          <v-card-text class="pa-0">
            <v-list v-if="recentStudents.length > 0" lines="two">
              <v-list-item
                v-for="student in recentStudents"
                :key="student._id"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" size="40">
                    <span class="text-white font-weight-bold">
                      {{ student.first_name[0] }}{{ student.last_name[0] }}
                    </span>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium">
                  {{ student.first_name }} {{ student.last_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ student.email }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-chip
                    :color="student.is_active ? 'success' : 'error'"
                    size="small"
                    label
                  >
                    {{ student.is_active ? 'Active' : 'Inactive' }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>

            <div v-else class="text-center pa-8 text-grey">
              No recent student records found.
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Sidebar: Quick Actions & Top Courses -->
      <v-col cols="12" lg="4">
        <!-- Quick Actions -->
        <v-card elevation="4" class="mb-4">
          <v-card-title class="bg-secondary text-white">
            <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
            Quick Actions
          </v-card-title>
          <v-card-text class="pa-4">
            <v-btn
              :to="{ name: 'Students' }"
              color="primary"
              block
              size="large"
              class="mb-3"
              prepend-icon="mdi-account-school"
            >
              Manage Students
            </v-btn>
            <v-btn
              :to="{ name: 'Instructors' }"
              color="primary"
              block
              size="large"
              class="mb-3"
              prepend-icon="mdi-account-tie"
            >
              Manage Instructors
            </v-btn>
            <v-btn
              :to="{ name: 'Courses' }"
              color="primary"
              block
              size="large"
              prepend-icon="mdi-book-open-variant"
            >
              Manage Courses
            </v-btn>
          </v-card-text>
        </v-card>

        <!-- Top Courses -->
        <v-card elevation="4" class="mb-4">
          <v-card-title class="bg-accent text-white">
            <v-icon class="mr-2">mdi-star</v-icon>
            Top Courses
          </v-card-title>
          <v-card-text class="pa-0">
            <v-list v-if="topCourses.length > 0" density="compact">
              <v-list-item
                v-for="course in topCourses"
                :key="course._id"
              >
                <template v-slot:prepend>
                  <v-chip color="primary" size="small" label>
                    {{ course.course_code }}
                  </v-chip>
                </template>
                <v-list-item-title>
                  {{ course.title }}
                </v-list-item-title>
              </v-list-item>
            </v-list>

            <div v-else class="text-center pa-6 text-grey">
              No course records available.
            </div>
          </v-card-text>
        </v-card>

        <!-- Refresh Button -->
        <v-btn
          @click="loadDashboardData"
          :loading="loading"
          color="info"
          block
          size="large"
          prepend-icon="mdi-refresh"
        >
          Refresh Data
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStudentsStore } from '@/stores/students'
import { useInstructorsStore } from '@/stores/instructors'
import { useCoursesStore } from '@/stores/courses'

const studentsStore = useStudentsStore()
const instructorsStore = useInstructorsStore()
const coursesStore = useCoursesStore()

const loading = ref(false)
const stats = ref({
  totalStudents: 0,
  activeStudents: 0,
  totalInstructors: 0,
  totalCourses: 0,
})

const recentStudents = computed(() => 
  studentsStore.students.slice(0, 5)
)

const topCourses = computed(() => 
  coursesStore.courses.slice(0, 5)
)

const loadDashboardData = async () => {
  loading.value = true
  try {
    const fetchPromises = [
      studentsStore.fetchStudents({ limit: 10 }),
      instructorsStore.fetchInstructors({ limit: 5 }),
      coursesStore.fetchCourses({ limit: 5 }),
    ]
    
    await Promise.all(fetchPromises)

    stats.value = {
      totalStudents: studentsStore.totalStudents,
      activeStudents: studentsStore.activeStudents.length,
      totalInstructors: instructorsStore.totalInstructors,
      totalCourses: coursesStore.totalCourses,
    }

  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.page-title {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
}
</style>