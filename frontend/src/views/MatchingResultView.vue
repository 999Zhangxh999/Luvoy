<template>
  <main class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <router-link 
          :to="`/students/${studentId}`" 
          class="w-10 h-10 rounded-xl border border-slate-700 flex items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
        >
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-slate-100">
            <i class="bi bi-link-45deg mr-2 text-pink-400"></i>人岗匹配结果
          </h1>
          <p v-if="results.length" class="text-sm text-slate-400">共 {{ results.length }} 个匹配岗位</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!results.length" class="card text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h2 class="text-xl font-semibold text-slate-100 mb-2">暂无匹配结果</h2>
        <p class="text-slate-400 mb-6">请先在学生详情页执行匹配操作</p>
        <router-link :to="`/students/${studentId}`" class="btn-primary">
          返回学生详情
        </router-link>
      </div>

      <!-- Results Grid -->
      <div class="grid lg:grid-cols-2 gap-6">
        <div 
          v-for="r in results" 
          :key="r.id"
          class="card hover:border-slate-600 transition-all"
        >
          <!-- Header -->
          <div class="flex items-start justify-between mb-5">
            <div>
              <h3 class="text-lg font-semibold text-slate-100">{{ r.job_name || '岗位' }}</h3>
              <span v-if="r.job_category" class="badge-cyan text-xs mt-1 inline-block">{{ r.job_category }}</span>
            </div>
            <div class="text-center">
              <div :class="[
                'text-3xl font-bold',
                r.overall_score >= 80 ? 'text-emerald-400' :
                r.overall_score >= 60 ? 'text-violet-400' : 'text-amber-400'
              ]">
                {{ r.overall_score?.toFixed(1) }}
              </div>
              <span class="text-xs text-slate-500">综合得分</span>
            </div>
          </div>

          <!-- Score Rings -->
          <div class="grid grid-cols-4 gap-3 mb-5">
            <div v-for="g in gauges(r)" :key="g.label" class="text-center">
              <div class="relative w-16 h-16 mx-auto mb-2">
                <svg class="w-full h-full -rotate-90">
                  <circle cx="32" cy="32" r="28" fill="none" stroke="#1e293b" stroke-width="4"/>
                  <circle 
                    cx="32" cy="32" r="28" fill="none" 
                    :stroke="g.color" 
                    stroke-width="4"
                    stroke-linecap="round"
                    :stroke-dasharray="176"
                    :stroke-dashoffset="176 - (g.value / 100) * 176"
                    class="transition-all duration-1000"
                  />
                </svg>
                <span class="absolute inset-0 flex items-center justify-center text-sm font-semibold text-slate-200">
                  {{ g.value?.toFixed(0) }}
                </span>
              </div>
              <span class="text-xs text-slate-500">{{ g.label }}</span>
            </div>
          </div>

          <!-- Skill Gaps -->
          <div v-if="r.skill_gaps?.length" class="mb-4">
            <span class="text-xs font-medium text-slate-400 block mb-2">
              <i class="bi bi-exclamation-triangle mr-1 text-amber-400"></i>技能差距
            </span>
            <div class="flex flex-wrap gap-2">
              <span v-for="g in r.skill_gaps" :key="g" class="px-2.5 py-1 rounded-full text-xs bg-red-500/10 text-red-400 border border-red-500/20">
                {{ g }}
              </span>
            </div>
          </div>

          <!-- Recommendations -->
          <div v-if="r.recommendations?.length">
            <span class="text-xs font-medium text-slate-400 block mb-2">
              <i class="bi bi-lightbulb mr-1 text-cyan-400"></i>提升建议
            </span>
            <ul class="space-y-1">
              <li v-for="rec in r.recommendations" :key="rec" class="text-sm text-slate-400 flex items-start gap-2">
                <span class="text-cyan-400 mt-1">•</span>
                <span>{{ rec }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMatchResults } from '@/api'

const route = useRoute()
const studentId = route.params.studentId
const results = ref([])

function gauges(r) {
  return [
    { label: '基础', value: r.basic_score, color: '#7c3aed' },
    { label: '技能', value: r.skill_score, color: '#10B981' },
    { label: '素质', value: r.quality_score, color: '#F59E0B' },
    { label: '潜力', value: r.potential_score, color: '#06b6d4' },
  ]
}

onMounted(async () => {
  const { data } = await getMatchResults(studentId)
  results.value = data
})
</script>
