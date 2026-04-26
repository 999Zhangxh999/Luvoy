<template>
  <div ref="el" :style="{ width: width, height: height }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { init, use, graphic } from 'echarts/core'
import { GaugeChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

use([GaugeChart, CanvasRenderer])

const props = defineProps({
  value: { type: Number, default: 0 },
  label: { type: String, default: '' },
  color: { type: String, default: '#4F46E5' },
  width: { type: String, default: '200px' },
  height: { type: String, default: '200px' },
})

const el = ref(null)
let chart = null

function render() {
  if (!chart) return
  chart.setOption({
    series: [{
      type: 'gauge',
      startAngle: 200, endAngle: -20,
      min: 0, max: 100,
      progress: {
        show: true, width: 12,
        itemStyle: {
          color: new graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: props.color + 'AA' },
            { offset: 1, color: props.color },
          ]),
        },
        roundCap: true,
      },
      axisLine: { lineStyle: { width: 12, color: [[1, '#F1F5F9']] }, roundCap: true },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      pointer: { show: false },
      title: {
        show: true, offsetCenter: [0, '72%'],
        fontSize: 12, fontWeight: 500,
        color: '#64748B',
      },
      detail: {
        valueAnimation: true, offsetCenter: [0, '38%'],
        fontSize: 22, fontWeight: 'bold',
        formatter: '{value}',
        color: props.color,
      },
      data: [{ value: props.value, name: props.label }],
    }],
  }, true)
}

let ro = null
onMounted(() => {
  chart = init(el.value)
  render()
  ro = new ResizeObserver(() => chart?.resize())
  ro.observe(el.value)
})
onUnmounted(() => { chart?.dispose(); ro?.disconnect() })
watch(() => props.value, render)
</script>
