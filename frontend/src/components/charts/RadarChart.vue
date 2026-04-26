<template>
  <div class="flex justify-center">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <defs>
        <radialGradient id="radarFill" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.05"/>
        </radialGradient>
        <radialGradient id="radarFill2" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.02"/>
        </radialGradient>
      </defs>

      <!-- 背景网格圆 -->
      <polygon
        v-for="level in [20, 40, 60, 80, 100]" :key="level"
        :points="getPolygonPoints(level)"
        fill="none"
        stroke="#1e1e2e"
        stroke-width="1"
      />

      <!-- 轴线 -->
      <line
        v-for="(axis, i) in data" :key="'axis-' + i"
        :x1="cx" :y1="cy"
        :x2="getPoint(100, i).x" :y2="getPoint(100, i).y"
        stroke="#1e1e2e" stroke-width="1"
      />

      <!-- 对比数据多边形 -->
      <polygon
        v-if="compareData && compareData.length"
        :points="getDataPoints(compareData)"
        fill="url(#radarFill2)"
        stroke="#06b6d4"
        stroke-width="1.5"
        stroke-dasharray="4 3"
        opacity="0.7"
      />

      <!-- 主数据多边形 -->
      <polygon
        :points="getDataPoints(data)"
        fill="url(#radarFill)"
        stroke="#7c3aed"
        stroke-width="2"
      />

      <!-- 数据点 -->
      <circle
        v-for="(d, i) in data" :key="'dot-' + i"
        :cx="getPoint(d.value, i).x"
        :cy="getPoint(d.value, i).y"
        r="4"
        fill="#7c3aed"
        stroke="#050509"
        stroke-width="2"
      />

      <!-- 轴标签 -->
      <text
        v-for="(axis, i) in data" :key="'label-' + i"
        :x="getLabelPoint(i).x"
        :y="getLabelPoint(i).y"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="11"
        fill="#94a3b8"
        font-family="Inter, sans-serif"
      >{{ axis.axis }}</text>

      <!-- 数值标签 -->
      <text
        v-for="(d, i) in data" :key="'val-' + i"
        :x="getValuePoint(d.value, i).x"
        :y="getValuePoint(d.value, i).y"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="9"
        fill="#7c3aed"
        font-weight="bold"
        font-family="Inter, sans-serif"
      >{{ d.value }}</text>
    </svg>
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Array,
    required: true,
    // 格式: [{ axis: 'Vue/React', value: 75 }, ...]
  },
  compareData: {
    type: Array,
    default: () => [],
  },
  size: {
    type: Number,
    default: 280,
  },
})

const cx = props.size / 2
const cy = props.size / 2
const r = props.size * 0.35
const labelR = props.size * 0.47
const n = props.data.length

const angle = (i) => (Math.PI * 2 * i) / n - Math.PI / 2

const getPoint = (val, i) => ({
  x: cx + (r * val / 100) * Math.cos(angle(i)),
  y: cy + (r * val / 100) * Math.sin(angle(i)),
})

const getLabelPoint = (i) => ({
  x: cx + labelR * Math.cos(angle(i)),
  y: cy + labelR * Math.sin(angle(i)),
})

const getValuePoint = (val, i) => ({
  x: cx + (r * val / 100 + 12) * Math.cos(angle(i)),
  y: cy + (r * val / 100 + 12) * Math.sin(angle(i)),
})

const getPolygonPoints = (level) =>
  props.data.map((_, i) => {
    const p = getPoint(level, i)
    return `${p.x},${p.y}`
  }).join(' ')

const getDataPoints = (data) =>
  data.map((d, i) => {
    const p = getPoint(d.value, i)
    return `${p.x},${p.y}`
  }).join(' ')
</script>
