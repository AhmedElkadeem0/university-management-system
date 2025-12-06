<template>
  <v-dialog :model-value="show" @update:model-value="$emit('close')" max-width="600">
    <v-card>
      <v-card-title class="text-h5 bg-primary text-white">
        {{ instructor ? 'Edit Instructor' : 'Add New Instructor' }}
        <v-btn icon="mdi-close" variant="text" @click="$emit('close')" class="float-right"></v-btn>
      </v-card-title>
      
      <v-card-text class="pt-4">
        <v-form ref="formRef" @submit.prevent="handleSubmit">
          <!-- Employee ID (Required for creation, disabled for editing) -->
          <v-text-field
            v-if="!instructor"
            v-model.number="formData.employee_id"
            label="Employee ID *"
            variant="outlined"
            type="number"
            required
            :rules="[v => !!v || 'Employee ID is required', v => v > 0 || 'Must be positive']"
            class="mb-2"
            hint="Unique employee identifier number"
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
            label="Email"
            variant="outlined"
            type="email"
            :rules="[
              v => !v || /.+@.+\..+/.test(v) || 'Email must be valid'
            ]"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model="formData.department"
            label="Department *"
            variant="outlined"
            required
            :rules="[v => !!v || 'Department is required']"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model.number="formData.salary"
            label="Salary ($)"
            variant="outlined"
            type="number"
            min="0"
            :rules="[
              v => v === null || v === '' || v >= 0 || 'Salary cannot be negative'
            ]"
            class="mb-2"
          ></v-text-field>

          <v-card-actions class="px-0 pb-0">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="$emit('close')">Cancel</v-btn>
            <v-btn type="submit" color="primary" variant="flat">
              {{ instructor ? 'Update' : 'Create' }}
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
  instructor: Object
})

const emit = defineEmits(['close', 'save'])

const formRef = ref(null)

const defaultForm = {
  employee_id: null,
  first_name: '',
  last_name: '',
  email: '',
  department: '',
  salary: 50000,
}

const formData = ref({ ...defaultForm })

watch(() => props.show, (newVal) => {
  if (newVal && props.instructor) {
    formData.value = { ...props.instructor }
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