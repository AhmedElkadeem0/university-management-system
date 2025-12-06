<template>
  <div v-if="pagination.totalPages > 1" class="text-center py-4">
    <v-pagination
      :model-value="pagination.page"
      :length="pagination.totalPages"
      :total-visible="7"
      @update:model-value="handlePageChange"
      color="primary"
    ></v-pagination>
    <div class="text-caption mt-2 text-white text-shadow">
      Showing {{ (pagination.page - 1) * pagination.limit + 1 }} - 
      {{ Math.min(pagination.page * pagination.limit, pagination.totalResults) }} 
      of {{ pagination.totalResults }} items
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  pagination: {
    type: Object,
    required: true,
    default: () => ({ page: 1, limit: 10, totalResults: 0, totalPages: 1 })
  }
})

const emit = defineEmits(['page-change'])

const handlePageChange = (newPage) => {
  emit('page-change', newPage)
}
</script>