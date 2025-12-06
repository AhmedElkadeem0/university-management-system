<template>
  <v-dialog :model-value="show" @update:model-value="$emit('close')" max-width="500">
    <v-card rounded="xl">
      <v-card-title class="text-h5 primary text-white">
        {{ course ? 'Edit Course' : 'Add New Course' }}
        <v-btn icon flat @click="$emit('close')" class="float-right">
          <v-icon color="white">mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pt-4">
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="formData.course_code"
            label="Course Code (e.g., CS101)"
            variant="outlined"
            required
            :disabled="!!course"
            class="mb-2"
          ></v-text-field>
          <v-text-field
            v-model="formData.title"
            label="Title"
            variant="outlined"
            required
            class="mb-2"
          ></v-text-field>
          <v-text-field
            v-model.number="formData.credit_hours"
            label="Credit Hours"
            variant="outlined"
            type="number"
            min="1"
            max="6"
            required
            class="mb-2"
          ></v-text-field>
          <v-text-field
            v-model="formData.instructor_name"
            label="Instructor Name"
            variant="outlined"
            class="mb-2"
          ></v-text-field>
          
          <v-card-actions class="d-flex justify-end pr-0">
            <v-btn variant="text" @click="$emit('close')">Cancel</v-btn>
            <v-btn type="submit" color="primary" variant="flat">
              {{ course ? 'Update' : 'Create' }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  course: Object // course data if in edit mode
})

const emit = defineEmits(['close', 'save'])

const defaultForm = {
  course_code: '',
  title: '',
  credit_hours: 3,
  instructor_name: '',
}

const formData = ref({ ...defaultForm })

watch(() => props.show, (newVal) => {
  if (newVal && props.course) {
    formData.value = { ...props.course }
  } else if (newVal) {
    formData.value = { ...defaultForm }
  }
})

const handleSubmit = () => {
  // Validation can be added here
  emit('save', formData.value)
}
</script>