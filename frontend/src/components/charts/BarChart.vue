<template>
  <div class="w-full">
    <div v-for="(item, index) in data" :key="index" class="mb-3 last:mb-0">
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm text-brand-text">{{ item.label }}</span>
        <span class="text-sm font-medium" :style="{ color: item.color || '#7c3aed' }">
          {{ item.value }}%
        </span>
      </div>
      <div class="h-2 bg-brand-surface rounded-full overflow-hidden">
        <div 
          class="h-full rounded-full transition-all duration-700 ease-out"
          :style="{ 
            width: item.value + '%', 
            background: item.color || 'linear-gradient(90deg, #7c3aed, #06b6d4)' 
          }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Array,
    required: true,
    // 格式: [{ label: 'Vue/React', value: 75, color: '#7c3aed' }, ...]
  },
})
</script>
