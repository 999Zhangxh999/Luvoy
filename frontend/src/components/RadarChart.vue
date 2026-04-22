<template>
  <div ref="chartEl" :style="{ width: width, height: height }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { init, use } from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import { TooltipComponent, RadarComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { graphic } from 'echarts/core'

use([RadarChart, TooltipComponent, RadarComponent, CanvasRenderer])

const props = defineProps({
  indicators: { type: Array, default: () => ['创新能力','学习能力','抗压能力','沟通能力','团队协作','实践能力'] },
  series: { type: Array, default: () => [] },
  width: { type: String, default: '100%' },
  height: { type: String, default: '320px' },
})

const chartEl = ref(null)
let chart = null

const COLORS = ['#7c3aed', '#06b6d4', '#10B981', '#F59E0B', '#EF4444', '#ec4899']

function render() {
  if (!chart) return
  const indicator = props.indicators.map(name => ({ name, max: 10 }))
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { 
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#1e293b',
      textStyle: { color: '#e2e8f0' }
    },
    radar: {
      indicator,
      radius: '65%',
      shape: 'circle',
      splitNumber: 5,
      axisName: { color: '#94a3b8', fontSize: 12, fontWeight: 500 },
      splitArea: { areaStyle: { color: ['rgba(124,58,237,.03)', 'rgba(124,58,237,.08)'] } },
      splitLine: { lineStyle: { color: 'rgba(71,85,105,.4)' } },
      axisLine: { lineStyle: { color: 'rgba(71,85,105,.4)' } },
    },
    series: [{
      type: 'radar',
      data: props.series.map((s, i) => ({
        value: s.values,
        name: s.name,
        symbol: 'circle',
        symbolSize: 6,
        areaStyle: { color: new graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: (s.color || COLORS[i % COLORS.length]) + '50' },
          { offset: 1, color: (s.color || COLORS[i % COLORS.length]) + '10' },
        ]) },
        lineStyle: { width: 2.5, color: s.color || COLORS[i % COLORS.length] },
        itemStyle: { color: s.color || COLORS[i % COLORS.length] },
      })),
    }],
  }, true)
}

let ro = null
onMounted(() => {
  chart = init(chartEl.value, 'dark')
  render()
  ro = new ResizeObserver(() => chart?.resize())
  ro.observe(chartEl.value)
})
onUnmounted(() => { chart?.dispose(); ro?.disconnect() })
watch(() => props.series, render, { deep: true })
</script>
