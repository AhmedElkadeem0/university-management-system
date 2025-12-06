import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import StudentsView from '@/views/StudentsView.vue'
import InstructorsView from '@/views/InstructorsView.vue'
import CoursesView from '@/views/CoursesView.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { icon: 'mdi-view-dashboard' }
  },
  {
    path: '/students',
    name: 'Students',
    component: StudentsView,
    meta: { icon: 'mdi-account-school' }
  },
  {
    path: '/instructors',
    name: 'Instructors',
    component: InstructorsView,
    meta: { icon: 'mdi-account-tie' }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: CoursesView,
    meta: { icon: 'mdi-book-open-variant' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router