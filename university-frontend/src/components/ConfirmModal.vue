<template>
  <v-dialog :model-value="show" @update:model-value="$emit('close')" max-width="500">
    <v-card>
      <v-card-title class="text-h5 bg-error text-white d-flex align-center">
        <v-icon class="mr-2" color="white">mdi-alert-circle</v-icon>
        {{ title }}
      </v-card-title>
      
      <v-card-text class="pt-6 pb-4">
        <p class="text-body-1">{{ message }}</p>
      </v-card-text>
      
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn 
          variant="text" 
          @click="$emit('close')"
        >
          Cancel
        </v-btn>
        <v-btn 
          color="error" 
          variant="flat"
          @click="handleConfirm"
        >
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  }
})

const emit = defineEmits(['close', 'confirm'])

const handleConfirm = () => {
  emit('confirm')
  emit('close')
}
</script>