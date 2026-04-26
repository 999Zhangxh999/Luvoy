<template>
  <div class="flex items-center justify-center">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <defs>
        <linearGradient v-for="(item, i) in data" :key="'grad-' + i" :id="'donut-grad-' + i">
          <stop offset="0%" :stop-color="item.color || colors[i % colors.length]" />
          <stop offset="100%" :stop-color="item.colorEnd || item.color || colors[i % colors.length]" stop-opacity="0.7" />
        </linearGradient>
      </defs>

      <!-- 扇区 -->
      <path
        v-for="(item, i) in computedData" :key="i"
        :d="item.path"
        :fill="`url(#donut-grad-${i})`"
        class="transition-all duration-500 hover:opacity-80 cursor-pointer"
        @mouseenter="activeIndex = i"
        @mouseleave="activeIndex = -1"
      />

      <!-- 中心内容 -->
      <circle :cx="cx" :cy="cy" :r="innerRadius" fill="#050509" />
      
      <!-- 中心文字 -->
      <text 
        :x="cx" 
        :y="cy - 8" 
        text-anchor="middle" 
        fill="#e2e8f0" 
        font-size="20" 
        font-weight="bold"
        font-family="Inter, sans-serif"
      >
        {{ activeIndex >= 0 ? data[activeIndex].value + '%' : total }}
      </text>
      <text 
        :x="cx" 
        :y="cy + 12" 
        text-anchor="middle" 
        fill="#64748b" 
        font-size="11"
        font-family="Inter, sans-serif"
      >
        {{ activeIndex >= 0 ? data[activeIndex].label : label }}
      </text>
    </svg>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    // 格式: [{ label: '已完成', value: 60, color: '#7c3aed' }, ...]
  },
  size: {
    type: Number,
    default: 200,
  },
  thickness: {
    type: Number,
    default: 30,
  },
  label: {
    type: String,
    default: '总计',
  },
})

const activeIndex = ref(-1)

const colors = ['#7c3aed', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899']

const cx = props.size / 2
const cy = props.size / 2
const outerRadius = props.size / 2 - 4
const innerRadius = outerRadius - props.thickness

const total = computed(() => props.data.reduce((sum, d) => sum + d.value, 0))

const computedData = computed(() => {
  let startAngle = -Math.PI / 2
  return props.data.map((item) => {
    const angle = (item.value / 100) * Math.PI * 2
    const endAngle = startAngle + angle
    
    const x1 = cx + outerRadius * Math.cos(startAngle)
    const y1 = cy + outerRadius * Math.sin(startAngle)
    const x2 = cx + outerRadius * Math.cos(endAngle)
    const y2 = cy + outerRadius * Math.sin(endAngle)
    const x3 = cx + innerRadius * Math.cos(endAngle)
    const y3 = cy + innerRadius * Math.sin(endAngle)
    const x4 = cx + innerRadius * Math.cos(startAngle)
    const y4 = cy + innerRadius * Math.sin(startAngle)
    
    const largeArc = angle > Math.PI ? 1 : 0
    
    const path = [
      `M ${x1} ${y1}`,
      `A ${outerRadius} ${outerRadius} 0 ${largeArc} 1 ${x2} ${y2}`,
      `L ${x3} ${y3}`,
      `A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${x4} ${y4}`,
      'Z'
    ].join(' ')
    
    startAngle = endAngle
    return { ...item, path }
  })
})
</script>
