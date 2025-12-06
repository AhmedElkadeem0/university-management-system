import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSidebarStore = defineStore('sidebar', () => {
  const isDrawerOpen = ref(true) // Match what components expect
  
  const toggleDrawer = () => {
    isDrawerOpen.value = !isDrawerOpen.value
  }

  const openDrawer = () => {
    isDrawerOpen.value = true
  }

  const closeDrawer = () => {
    isDrawerOpen.value = false
  }

  return { 
    isDrawerOpen, 
    toggleDrawer, 
    openDrawer, 
    closeDrawer 
  }
})