<template>
  <v-navigation-drawer
    v-model="sidebarStore.isDrawerOpen"
    app
    permanent
    :rail="!sidebarStore.isDrawerOpen"
    @click.self="sidebarStore.closeDrawer"
    color="primary"
    dark
    class="text-white"
  >
    <!-- Logo/Header -->
    <v-list-item class="py-2" link>
      <template v-slot:prepend>
        <v-icon size="30">mdi-school</v-icon>
      </template>
      <v-list-item-title class="text-h6 font-weight-bold">
        UniPortal
      </v-list-item-title>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Navigation Links -->
    <v-list density="compact" nav>
      <v-list-item
        v-for="route in routes"
        :key="route.path"
        :to="route.path"
        link
        color="secondary"
      >
        <template v-slot:prepend>
          <v-icon>{{ route.meta.icon }}</v-icon>
        </template>
        <v-list-item-title>{{ route.name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'
import { useSidebarStore } from '@/stores/sidebar'
import router from '@/router'

const sidebarStore = useSidebarStore()
const routes = computed(() => router.options.routes.filter(r => r.name !== undefined))
</script>

<style scoped>
/* Styling for a dark/primary sidebar */
.v-navigation-drawer {
    background: linear-gradient(180deg, #673AB7 0%, #764ba2 100%);
}
.v-list-item-title {
    color: white !important;
}
/* Active link styling */
.v-list-item--active {
    background-color: rgba(255, 255, 255, 0.2) !important;
}
</style>