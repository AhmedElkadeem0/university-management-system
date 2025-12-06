<template>
  <v-app-bar app color="white" elevation="2" density="compact" class="text-primary">
    <v-app-bar-nav-icon @click="sidebarStore.toggleDrawer"></v-app-bar-nav-icon>
    <v-toolbar-title class="font-weight-bold">
      University Dashboard
    </v-toolbar-title>
    <v-spacer></v-spacer>
    
    <v-btn icon>
      <v-icon>mdi-bell-outline</v-icon>
    </v-btn>
    <v-avatar color="primary" size="36">
      <span class="white--text text-h6">JD</span>
    </v-avatar>
  </v-app-bar>
</template>

<script setup>
import { useSidebarStore } from '@/stores/sidebar'

const sidebarStore = useSidebarStore()
</script>