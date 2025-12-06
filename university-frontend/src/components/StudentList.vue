<template>
  <v-data-table
    :headers="headers"
    :items="students"
    :loading="loading"
    item-key="_id"
    class="elevation-1"
    :items-per-page="-1"
    hide-default-footer
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Student Records</v-toolbar-title>
      </v-toolbar>
    </template>

    <template v-slot:item.gpa="{ item }">
      <v-chip :color="getGpaColor(item.gpa)" size="small" label>
        {{ item.gpa.toFixed(2) }}
      </v-chip>
    </template>
    
    <template v-slot:item.is_active="{ item }">
      <v-chip :color="item.is_active ? 'success' : 'error'" size="small" label>
        {{ item.is_active ? 'Active' : 'Inactive' }}
      </v-chip>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-btn icon size="small" color="primary" variant="text" @click="$emit('edit', item)">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn icon size="small" color="error" variant="text" @click="confirmDelete(item)">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>
  </v-data-table>
  
  <!-- Custom Confirmation Dialog (Replaces confirm()) -->
  <v-dialog v-model="showConfirmDialog" max-width="400">
    <v-card>
      <v-card-title class="text-h6">Confirm Deletion</v-card-title>
      <v-card-text>
        Are you sure you want to delete student: 
        <strong>{{ studentToDelete?.first_name }} {{ studentToDelete?.last_name }}</strong>?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="showConfirmDialog = false">Cancel</v-btn>
        <v-btn color="error" variant="flat" @click="handleDeleteConfirm">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  students: {
    type: Array,
    required: true
  },
  loading: Boolean
})

const emit = defineEmits(['edit', 'delete'])

const headers = [
  { title: 'ID', key: 'student_id', align: 'start' },
  { title: 'First Name', key: 'first_name' },
  { title: 'Last Name', key: 'last_name' },
  { title: 'Email', key: 'email' },
  { title: 'GPA', key: 'gpa' },
  { title: 'Status', key: 'is_active' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
]

const getGpaColor = (gpa) => {
  if (gpa >= 3.7) return 'primary';
  if (gpa >= 3.0) return 'success';
  if (gpa >= 2.0) return 'warning';
  return 'error';
}

// Confirmation Dialog Logic
const showConfirmDialog = ref(false)
const studentToDelete = ref(null)

const confirmDelete = (student) => {
  studentToDelete.value = student
  showConfirmDialog.value = true
}

const handleDeleteConfirm = () => {
  if (studentToDelete.value) {
    emit('delete', studentToDelete.value._id)
  }
  showConfirmDialog.value = false
  studentToDelete.value = null
}
</script>