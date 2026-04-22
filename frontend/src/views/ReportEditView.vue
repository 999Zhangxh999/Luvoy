<template>
  <main v-if="report" class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <router-link 
          :to="`/reports/${studentId}`" 
          class="w-10 h-10 rounded-xl border border-slate-700 flex items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
        >
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div>
          <h1 class="text-2xl font-bold text-slate-100">
            <i class="bi bi-pencil-square mr-2 text-violet-400"></i>编辑报告
          </h1>
          <p class="text-sm text-slate-400">点击章节标签切换编辑内容</p>
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

      <!-- Section Tabs -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button 
          v-for="(sec, idx) in sections" 
          :key="sec.key"
          @click="activeTab = sec.key"
          :class="[
            'inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all',
            activeTab === sec.key 
              ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white shadow-lg shadow-violet-500/25' 
              : 'border border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'
          ]"
        >
          <span :class="[
            'w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold',
            activeTab === sec.key ? 'bg-white/20' : 'bg-slate-700'
          ]">
            {{ idx + 1 }}
          </span>
          {{ sec.label }}
        </button>
      </div>

      <!-- Editor Card -->
      <div v-for="sec in sections" :key="sec.key" v-show="activeTab === sec.key">
        <div class="card overflow-hidden">
          <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700 bg-slate-800/50">
            <span class="font-semibold text-slate-100">
              <i class="bi bi-journal-text mr-2 text-violet-400"></i>{{ sec.label }}
            </span>
            <span class="text-xs text-slate-500">支持 Markdown 语法</span>
          </div>
          <textarea 
            v-model="report[sec.key]" 
            :placeholder="`编辑${sec.label}…`"
            class="w-full bg-transparent border-0 outline-none px-5 py-4 text-slate-300 leading-relaxed resize-y min-h-[400px] font-mono text-sm"
          ></textarea>
          <div class="flex items-center justify-between px-5 py-3 border-t border-slate-700 bg-slate-800/50">
            <span class="text-xs text-slate-500">
              {{ (report[sec.key] || '').length }} 字符
            </span>
            <button 
              @click="saveSection(sec.key)" 
              :disabled="saving"
              class="btn-primary"
            >
              <i class="bi bi-check-circle mr-2"></i>
              {{ saving ? '保存中...' : '保存此章节' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getReport, updateReportSection } from '@/api'

const route = useRoute()
const setLoading = inject('setLoading')
const toast = inject('toast')
const studentId = route.params.studentId

const report = ref(null)
const activeTab = ref('section_self_assessment')
const saving = ref(false)
const msg = ref('')
const msgOk = ref(true)

const sections = [
  { key: 'section_self_assessment', label: '自我评估' },
  { key: 'section_job_exploration', label: '职业探索' },
  { key: 'section_career_goal', label: '职业目标' },
  { key: 'section_career_path', label: '路径规划' },
  { key: 'section_action_plan', label: '行动计划' },
  { key: 'section_evaluation', label: '评估与调整' },
]

async function saveSection(key) {
  saving.value = true; setLoading(true, '正在保存…'); msg.value = ''
  try {
    await updateReportSection(report.value.id, key, report.value[key])
    msg.value = '保存成功'; msgOk.value = true
    toast('章节保存成功', 'success')
  } catch (e) {
    msg.value = e.response?.data?.message || '保存失败'; msgOk.value = false
    toast(msg.value, 'danger')
  } finally { saving.value = false; setLoading(false) }
}

onMounted(async () => {
  try {
    const { data } = await getReport(studentId)
    report.value = data
  } catch {}
})
</script>
