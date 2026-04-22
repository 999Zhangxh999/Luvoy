<template>
  <main v-if="profile" class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <router-link 
          to="/jobs/profiles" 
          class="w-10 h-10 rounded-xl border border-slate-700 flex items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
        >
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-slate-100">{{ profile.position_name }}</h1>
          <div class="flex gap-2 mt-1">
            <span class="badge-cyan text-xs">{{ profile.category }}</span>
            <span class="px-2.5 py-1 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20">
              {{ profile.level }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid lg:grid-cols-5 gap-6">
        <!-- Left Content -->
        <div class="lg:col-span-3 space-y-6">
          <!-- Overview -->
          <div class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-violet-500/20 flex items-center justify-center">
                <i class="bi bi-file-text text-violet-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">岗位概述</h2>
            </div>
            <p class="text-slate-300 leading-relaxed mb-5">{{ profile.summary }}</p>
            <div class="grid grid-cols-3 gap-4">
              <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span class="block text-xs text-slate-500 mb-1">学历要求</span>
                <span class="font-medium text-slate-200">{{ profile.education_req || '-' }}</span>
              </div>
              <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span class="block text-xs text-slate-500 mb-1">经验要求</span>
                <span class="font-medium text-slate-200">{{ profile.experience_req || '-' }}</span>
              </div>
              <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span class="block text-xs text-slate-500 mb-1">薪资范围</span>
                <span class="font-medium text-emerald-400">{{ profile.salary_range || '-' }}</span>
              </div>
            </div>
          </div>

          <!-- Technical Skills -->
          <div class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                <i class="bi bi-code-slash text-cyan-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">技能要求</h2>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="s in profile.technical_skills" :key="s" class="badge">{{ s }}</span>
              <span v-if="!profile.technical_skills?.length" class="text-sm text-slate-500">暂无</span>
            </div>
          </div>

          <!-- Certificates -->
          <div class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center">
                <i class="bi bi-award text-emerald-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">资格证书</h2>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="c in profile.certificates" :key="c" class="px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {{ c }}
              </span>
              <span v-if="!profile.certificates?.length" class="text-sm text-slate-500">暂无</span>
            </div>
          </div>

          <!-- Weights -->
          <div class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center">
                <i class="bi bi-sliders2 text-pink-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">匹配维度权重</h2>
            </div>
            <div class="grid grid-cols-4 gap-4">
              <div v-for="w in weights" :key="w.key" class="text-center">
                <div class="relative w-16 h-16 mx-auto mb-2">
                  <svg class="w-full h-full -rotate-90">
                    <circle cx="32" cy="32" r="28" fill="none" stroke="#1e293b" stroke-width="5"/>
                    <circle 
                      cx="32" cy="32" r="28" fill="none" 
                      :stroke="w.color" 
                      stroke-width="5"
                      stroke-linecap="round"
                      :stroke-dasharray="176"
                      :stroke-dashoffset="176 - (profile[w.key] || 0) * 176"
                      class="transition-all duration-1000"
                    />
                  </svg>
                  <span class="absolute inset-0 flex items-center justify-center text-sm font-bold text-slate-200">
                    {{ ((profile[w.key] || 0) * 100).toFixed(0) }}%
                  </span>
                </div>
                <span class="text-xs text-slate-400">{{ w.label }}</span>
              </div>
            </div>
          </div>

          <!-- Career Path -->
          <div v-if="career" class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center">
                <i class="bi bi-signpost-split text-amber-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">职业发展路径</h2>
            </div>
            
            <!-- Promotions -->
            <div class="mb-6">
              <h3 class="text-sm font-semibold text-emerald-400 mb-3">
                <i class="bi bi-arrow-up-circle mr-2"></i>晋升方向
              </h3>
              <div v-if="career.promotions_from?.length" class="space-y-3">
                <div v-for="p in career.promotions_from" :key="p.id" class="p-4 rounded-xl bg-slate-800/50 border border-slate-700">
                  <div class="flex items-center gap-3 flex-wrap mb-2">
                    <span class="font-medium text-slate-200">→ {{ p.to_position }}</span>
                    <span class="badge text-xs">{{ p.estimated_years }}年</span>
                    <span class="px-2 py-0.5 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      难度 {{ p.difficulty }}/5
                    </span>
                  </div>
                  <p class="text-sm text-slate-400">{{ p.description }}</p>
                </div>
              </div>
              <p v-else class="text-sm text-slate-500">暂无晋升路径</p>
            </div>

            <!-- Transfers -->
            <div>
              <h3 class="text-sm font-semibold text-cyan-400 mb-3">
                <i class="bi bi-arrow-left-right mr-2"></i>转岗方向
              </h3>
              <div v-if="career.transfers?.length" class="space-y-3">
                <div v-for="t in career.transfers" :key="t.id" class="p-4 rounded-xl bg-slate-800/50 border border-slate-700">
                  <div class="flex items-center gap-3 flex-wrap mb-2">
                    <span class="font-medium text-slate-200">→ {{ t.to_position }}</span>
                    <span class="badge text-xs">约{{ t.estimated_years }}年</span>
                  </div>
                  <p class="text-sm text-slate-400">{{ t.description }}</p>
                </div>
              </div>
              <p v-else class="text-sm text-slate-500">暂无转岗路径</p>
            </div>
          </div>
        </div>

        <!-- Right: Radar Chart -->
        <div class="lg:col-span-2">
          <div class="card sticky top-24">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                <i class="bi bi-radar text-cyan-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">软性素质要求</h2>
            </div>
            <RadarChart :series="radarSeries" height="300px" />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getJobProfileDetail } from '@/api'
import RadarChart from '@/components/RadarChart.vue'

const route = useRoute()
const profile = ref(null)
const career = ref(null)

const weights = [
  { key: 'weight_basic', label: '基础要求', color: '#7c3aed' },
  { key: 'weight_skill', label: '职业技能', color: '#10B981' },
  { key: 'weight_quality', label: '职业素养', color: '#F59E0B' },
  { key: 'weight_potential', label: '发展潜力', color: '#06b6d4' },
]

const radarSeries = computed(() => {
  if (!profile.value) return []
  const p = profile.value
  return [{
    name: p.position_name,
    values: [p.innovation_ability, p.learning_ability, p.pressure_resistance,
             p.communication_skill, p.teamwork_ability, p.internship_ability],
  }]
})

onMounted(async () => {
  const { data } = await getJobProfileDetail(route.params.id)
  career.value = data.career_path
  delete data.career_path
  profile.value = data
})
</script>
