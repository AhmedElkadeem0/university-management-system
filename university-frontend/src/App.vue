<template>
  <v-app>
    <NavBar @toggle-drawer="drawer = !drawer" />
    <SideBar v-model="drawer" />

    <v-main>
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '@/components/layout/NavBar.vue'
import SideBar from '@/components/layout/SideBar.vue'

const drawer = ref(true) // Start open for desktop
</script>