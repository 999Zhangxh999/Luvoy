<template>
  <main class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <h1 class="text-3xl font-bold text-slate-100">
          <i class="bi bi-person-badge mr-3 text-violet-400"></i>
          岗位 <span class="gradient-text">画像库</span>
        </h1>
        <div class="flex items-center gap-3">
          <select 
            v-model.number="analyzeCount" 
            class="bg-slate-800 border border-slate-700 text-slate-300 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-violet-500"
          >
            <option :value="5">5个</option>
            <option :value="10">10个</option>
            <option :value="20">20个</option>
          </select>
          <button @click="doAnalyze" :disabled="analyzing" class="btn-primary bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500">
            <i class="bi bi-cpu mr-2"></i>
            {{ analyzing ? '分析中...' : '一键生成' }}
          </button>
        </div>
      </div>

      <!-- Message Alert -->
      <div v-if="msg" :class="[
        'flex items-center gap-3 p-4 rounded-xl mb-6 border',
        msgOk ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
      ]">
        <i :class="msgOk ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
        <span>{{ msg }}</span>
      </div>

      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2 mb-8 pb-6 border-b border-slate-700">
        <button 
          @click="category=''; load()"
          :class="[
            'px-4 py-2 rounded-full text-sm font-medium transition-all',
            category === '' 
              ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white shadow-lg shadow-violet-500/25' 
              : 'border border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'
          ]"
        >
          <i class="bi bi-grid-3x3-gap mr-1"></i>全部
        </button>
        <button 
          v-for="c in categories" 
          :key="c"
          @click="category=c; load()"
          :class="[
            'px-4 py-2 rounded-full text-sm font-medium transition-all',
            category === c 
              ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white shadow-lg shadow-violet-500/25' 
              : 'border border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'
          ]"
        >
          {{ c }}
        </button>
      </div>

      <!-- Profile Cards Grid -->
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div 
          v-for="(p, i) in profiles" 
          :key="p.id"
          class="card group"
          :style="{ animationDelay: (i % 6 * 0.05) + 's' }"
        >
          <div class="flex items-start justify-between mb-3">
            <h3 class="font-semibold text-slate-100 group-hover:text-violet-400 transition-colors leading-tight">
              {{ p.position_name }}
            </h3>
          </div>
          <div class="flex flex-wrap gap-2 mb-3">
            <span class="badge-cyan text-xs">{{ p.category }}</span>
            <span class="px-2.5 py-1 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20">
              {{ p.level }}
            </span>
          </div>
          <p class="text-sm text-slate-400 mb-4 line-clamp-2">{{ p.summary }}</p>
          <div class="flex flex-wrap gap-1.5 mb-4">
            <span 
              v-for="s in (p.technical_skills||[]).slice(0,3)" 
              :key="s"
              class="badge text-xs"
            >
              {{ s }}
            </span>
            <span 
              v-if="(p.technical_skills||[]).length > 3"
              class="px-2 py-0.5 rounded-full text-xs bg-slate-700 text-slate-400"
            >
              +{{ p.technical_skills.length - 3 }}
            </span>
          </div>
          <router-link 
            :to="`/jobs/profiles/${p.id}`" 
            class="block w-full py-2.5 text-center text-sm font-medium text-violet-400 border border-violet-500/40 rounded-xl hover:bg-violet-500/10 transition-colors"
          >
            <i class="bi bi-eye mr-2"></i>查看详情
          </router-link>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!profiles.length" class="card text-center py-16">
        <div class="text-6xl mb-4">📋</div>
        <h2 class="text-xl font-semibold text-slate-100 mb-2">暂无岗位画像</h2>
        <p class="text-slate-400 mb-6">请点击「一键生成」开始AI分析</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { getJobProfiles, analyzeJobs } from '@/api'

const setLoading = inject('setLoading')
const toast = inject('toast')
const profiles = ref([])
const categories = ref([])
const category = ref('')
const analyzing = ref(false)
const analyzeCount = ref(5)
const msg = ref('')
const msgOk = ref(true)

async function load() {
  const { data } = await getJobProfiles({ category: category.value })
  profiles.value = data.profiles
  categories.value = data.categories
}

async function doAnalyze() {
  analyzing.value = true
  setLoading(true, 'AI正在分析岗位画像…')
  msg.value = ''
  try {
    const { data } = await analyzeJobs(analyzeCount.value)
    msg.value = data.message
    msgOk.value = data.success
    toast(data.message, data.success ? 'success' : 'danger')
    await load()
  } catch (e) {
    msg.value = e.response?.data?.message || '分析失败'
    msgOk.value = false
    toast(msg.value, 'danger')
  } finally {
    analyzing.value = false
    setLoading(false)
  }
}

onMounted(load)
</script>
