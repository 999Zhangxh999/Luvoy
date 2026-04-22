<template>
  <div class="flex items-center justify-center gap-4">
    <!-- SVG 圆环 -->
    <div class="relative" :style="{ width: size + 'px', height: size + 'px' }">
      <svg :width="size" :height="size" class="-rotate-90">
        <!-- 背景圆 -->
        <circle
          :cx="size / 2"
          :cy="size / 2"
          :r="radius"
          fill="none"
          :stroke="bgColor"
          :stroke-width="strokeWidth"
        />
        <!-- 进度圆 -->
        <circle
          :cx="size / 2"
          :cy="size / 2"
          :r="radius"
          fill="none"
          :stroke="color"
          :stroke-width="strokeWidth"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="strokeDashoffset"
          class="transition-all duration-700 ease-out"
        />
      </svg>
      <!-- 中心内容 -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-2xl font-bold" :style="{ color }">{{ value }}%</span>
        <span v-if="label" class="text-xs text-brand-muted mt-0.5">{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0,
  },
  size: {
    type: Number,
    default: 120,
  },
  strokeWidth: {
    type: Number,
    default: 8,
  },
  color: {
    type: String,
    default: '#7c3aed',
  },
  bgColor: {
    type: String,
    default: '#1e1e2e',
  },
  label: {
    type: String,
    default: '',
  },
})

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const strokeDashoffset = computed(() => 
  circumference.value - (props.value / 100) * circumference.value
)
</script>
