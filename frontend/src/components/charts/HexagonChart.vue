<template>
  <div class="hexagon-chart" ref="chartRef">
    <svg :viewBox="`0 0 ${size} ${size}`" class="hex-svg">
      <!-- 背景六边形网格 -->
      <g class="hex-grid">
        <polygon 
          v-for="level in 5" 
          :key="level"
          :points="getHexPoints(level / 5)"
          class="grid-line"
        />
      </g>
      
      <!-- 轴线 -->
      <g class="hex-axes">
        <line 
          v-for="(_, i) in 6" 
          :key="i"
          :x1="center" 
          :y1="center"
          :x2="getAxisEndpoint(i).x"
          :y2="getAxisEndpoint(i).y"
          class="axis-line"
        />
      </g>
      
      <!-- 数据区域 -->
      <polygon 
        :points="dataPoints"
        class="data-area"
        :style="{ fill: color + '30', stroke: color }"
      />
      
      <!-- 数据点 -->
      <g class="data-points">
        <circle 
          v-for="(point, i) in dataPointPositions" 
          :key="i"
          :cx="point.x"
          :cy="point.y"
          r="5"
          :fill="color"
          class="data-dot"
        />
      </g>
      
      <!-- 标签 -->
      <g class="hex-labels">
        <text 
          v-for="(label, i) in labels" 
          :key="i"
          :x="getLabelPosition(i).x"
          :y="getLabelPosition(i).y"
          :text-anchor="getLabelAnchor(i)"
          class="label-text"
        >
          {{ label }}
        </text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  values: {
    type: Array,
    default: () => [0, 0, 0, 0, 0, 0]
  },
  labels: {
    type: Array,
    default: () => ['学习', '创新', '沟通', '协作', '抗压', '执行']
  },
  color: {
    type: String,
    default: '#8b5cf6'
  },
  size: {
    type: Number,
    default: 200
  },
  maxValue: {
    type: Number,
    default: 10
  }
})

const chartRef = ref(null)
const center = computed(() => props.size / 2)
const radius = computed(() => props.size * 0.35)

// 计算六边形顶点
function getHexPoints(scale = 1) {
  const points = []
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 3) * i - Math.PI / 2
    const x = center.value + radius.value * scale * Math.cos(angle)
    const y = center.value + radius.value * scale * Math.sin(angle)
    points.push(`${x},${y}`)
  }
  return points.join(' ')
}

// 计算轴线终点
function getAxisEndpoint(index) {
  const angle = (Math.PI / 3) * index - Math.PI / 2
  return {
    x: center.value + radius.value * Math.cos(angle),
    y: center.value + radius.value * Math.sin(angle)
  }
}

// 计算数据点位置
const dataPointPositions = computed(() => {
  return props.values.map((value, i) => {
    const normalizedValue = Math.min(value, props.maxValue) / props.maxValue
    const angle = (Math.PI / 3) * i - Math.PI / 2
    return {
      x: center.value + radius.value * normalizedValue * Math.cos(angle),
      y: center.value + radius.value * normalizedValue * Math.sin(angle)
    }
  })
})

// 数据区域路径
const dataPoints = computed(() => {
  return dataPointPositions.value.map(p => `${p.x},${p.y}`).join(' ')
})

// 标签位置
function getLabelPosition(index) {
  const angle = (Math.PI / 3) * index - Math.PI / 2
  const labelRadius = radius.value + 18
  return {
    x: center.value + labelRadius * Math.cos(angle),
    y: center.value + labelRadius * Math.sin(angle) + 4
  }
}

// 标签对齐方式
function getLabelAnchor(index) {
  if (index === 0) return 'middle'
  if (index === 3) return 'middle'
  if (index < 3) return 'start'
  return 'end'
}
</script>

<style scoped>
.hexagon-chart {
  width: 100%;
  height: 100%;
}

.hex-svg {
  width: 100%;
  height: 100%;
}

.grid-line {
  fill: none;
  stroke: rgba(139, 92, 246, 0.15);
  stroke-width: 1;
}

.axis-line {
  stroke: rgba(139, 92, 246, 0.2);
  stroke-width: 1;
}

.data-area {
  stroke-width: 2;
  transition: all 0.5s ease;
}

.data-dot {
  transition: all 0.3s ease;
}

.data-dot:hover {
  r: 7;
  filter: drop-shadow(0 0 6px currentColor);
}

.label-text {
  font-size: 10px;
  fill: #64748b;
  font-weight: 500;
}
</style>
