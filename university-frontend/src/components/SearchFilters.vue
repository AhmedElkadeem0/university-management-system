<template>
  <v-card class="pa-4 mb-6" rounded="lg" elevation="2">
    <v-row align="end" justify="start">
      <!-- General Search -->
      <v-col cols="12" md="6" lg="4">
        <v-text-field
          v-model="localFilters.search"
          label="Quick Search"
          density="compact"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          @update:model-value="handleSearchInput"
          clearable
        ></v-text-field>
      </v-col>

      <!-- Min GPA Filter (only for Student context) -->
      <v-col v-if="context === 'student'" cols="6" md="3" lg="2">
        <v-text-field
          v-model="localFilters.gpaFilter"
          label="Min GPA"
          density="compact"
          type="number"
          step="0.1"
          min="0.0"
          max="4.0"
          variant="outlined"
          clearable
        ></v-text-field>
      </v-col>

      <!-- Status Filter (only for Student context) -->
      <v-col v-if="context === 'student'" cols="6" md="3" lg="2">
        <v-select
          v-model="localFilters.statusFilter"
          label="Status"
          density="compact"
          :items="['all', 'active', 'inactive']"
          variant="outlined"
        ></v-select>
      </v-col>

      <!-- Action Buttons -->
      <v-col cols="12" md="6" lg="4" class="d-flex justify-end">
        <v-btn @click="handleSearch" color="primary" class="mr-2" prepend-icon="mdi-filter">
          Apply Filters
        </v-btn>
        <v-btn @click="handleReset" color="secondary" variant="outlined" prepend-icon="mdi-reload">
          Reset
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  filters: {
    type: Object,
    required: true
  },
  // 'student', 'instructor', 'course' to adjust filters
  context: {
    type: String,
    default: 'student'
  }
})

const emit = defineEmits(['update:filters', 'search'])

const localFilters = ref({ ...props.filters })
let searchTimeout = null

// Watch for prop changes and sync with local state
watch(() => props.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })

// Debounced search for general search field
const handleSearchInput = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    emit('update:filters', localFilters.value)
  }, 500)
}

const handleSearch = () => {
  clearTimeout(searchTimeout)
  emit('update:filters', localFilters.value)
}

const handleReset = () => {
  // Reset local filters to initial state, excluding page/limit/sort
  const resetData = {
    search: '',
    gpaFilter: 0.0,
    statusFilter: 'all',
    page: 1,
    limit: props.filters.limit,
    sortBy: props.filters.sortBy,
    sortOrder: props.filters.sortOrder
  }
  localFilters.value = resetData
  emit('update:filters', resetData)
}
</script>