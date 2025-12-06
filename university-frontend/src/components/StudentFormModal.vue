<template>
  <v-dialog :model-value="show" @update:model-value="$emit('close')" max-width="600">
    <v-card>
      <v-card-title class="text-h5 bg-primary text-white">
        {{ student ? 'Edit Student' : 'Add New Student' }}
        <v-btn icon="mdi-close" variant="text" @click="$emit('close')" class="float-right"></v-btn>
      </v-card-title>
      
      <v-card-text class="pt-4">
        <v-form ref="formRef" @submit.prevent="handleSubmit">
          <!-- Student ID (Required for creation, disabled for editing) -->
          <v-text-field
            v-if="!student"
            v-model.number="formData.student_id"
            label="Student ID *"
            variant="outlined"
            type="number"
            required
            :rules="[v => !!v || 'Student ID is required', v => v > 0 || 'Must be positive']"
            class="mb-2"
            hint="Unique student identifier number"
          ></v-text-field>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.first_name"
                label="First Name *"
                variant="outlined"
                required
                :rules="[v => !!v || 'First name is required']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.last_name"
                label="Last Name *"
                variant="outlined"
                required
                :rules="[v => !!v || 'Last name is required']"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-text-field
            v-model="formData.email"
            label="Email *"
            variant="outlined"
            type="email"
            required
            :rules="[
              v => !!v || 'Email is required',
              v => /.+@.+\..+/.test(v) || 'Email must be valid'
            ]"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model.number="formData.gpa"
            label="GPA"
            variant="outlined"
            type="number"
            step="0.01"
            min="0.0"
            max="4.0"
            :rules="[
              v => v === null || v === '' || (v >= 0 && v <= 4) || 'GPA must be between 0.0 and 4.0'
            ]"
            class="mb-2"
          ></v-text-field>

          <v-checkbox
            v-model="formData.is_active"
            label="Active Student"
            color="primary"
          ></v-checkbox>

          <v-card-actions class="px-0 pb-0">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="$emit('close')">Cancel</v-btn>
            <v-btn type="submit" color="primary" variant="flat">
              {{ student ? 'Update' : 'Create' }}
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
  student: Object
})

const emit = defineEmits(['close', 'save'])

const formRef = ref(null)

const defaultForm = {
  student_id: null,
  first_name: '',
  last_name: '',
  email: '',
  gpa: 0.0,
  is_active: true,
}

const formData = ref({ ...defaultForm })

watch(() => props.show, (newVal) => {
  if (newVal && props.student) {
    formData.value = { ...props.student }
  } else if (newVal) {
    formData.value = { ...defaultForm }
  }
})

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate()
  if (valid) {
    emit('save', formData.value)
  }
}
</script>