<template>
  <v-card :color="color" class="pa-4" rounded="lg" elevation="4">
    <v-row align="center">
      <v-col cols="auto">
        <v-avatar :color="iconColor || 'white'" size="48">
          <v-icon size="30" :color="color">{{ icon }}</v-icon>
        </v-avatar>
      </v-col>
      <v-col>
        <div class="text-subtitle-1 text-uppercase font-weight-medium mb-1" :class="`text-${textColor}`">
          {{ title }}
        </div>
        <div class="text-h4 font-weight-bold" :class="`text-${textColor}`">
          {{ value }}
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String, // MDI icon string, e.g., 'mdi-account-group'
  color: {
    type: String,
    default: 'primary'
  },
  iconColor: {
    type: String,
    default: 'white'
  },
  textColor: {
    type: String,
    default: 'white'
  }
})
</script>