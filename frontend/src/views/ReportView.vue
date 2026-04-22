<template>
  <main v-if="report" class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div class="flex items-center gap-4">
          <router-link 
            :to="`/students/${studentId}`" 
            class="w-10 h-10 rounded-xl border border-slate-700 flex items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
          >
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h1 class="text-2xl font-bold text-slate-100">{{ report.title }}</h1>
            <p v-if="report.updated_at" class="text-sm text-slate-400">{{ report.updated_at }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2 sm:gap-3">
          <button @click="polish" :disabled="busy" class="btn-secondary text-amber-400 border-amber-500/40 hover:bg-amber-500/10">
            <i class="bi bi-magic mr-2"></i>AI润色
          </button>
          <router-link :to="`/reports/${studentId}/edit`" class="btn-secondary">
            <i class="bi bi-pencil mr-2"></i>编辑
          </router-link>
          <div class="relative" ref="dropdownRef">
            <button @click="showExport = !showExport" class="btn-primary">
              <i class="bi bi-download mr-2"></i>导出
              <i class="bi bi-chevron-down ml-1 text-xs"></i>
            </button>
            <div v-if="showExport" class="absolute right-0 top-full mt-2 w-48 bg-slate-800 border border-slate-700 rounded-xl shadow-xl z-10 overflow-hidden">
              <a :href="exportUrl('html')" target="_blank" class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-700 transition-colors">
                <i class="bi bi-filetype-html text-cyan-400"></i>导出 HTML
              </a>
              <a :href="exportUrl('markdown')" target="_blank" class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-700 transition-colors">
                <i class="bi bi-markdown text-violet-400"></i>导出 Markdown
              </a>
            </div>
          </div>
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

      <!-- Report Content -->
      <div class="card">
        <div class="report-content prose prose-invert max-w-none" v-html="reportHtml"></div>
      </div>
    </div>
  </main>

  <!-- Empty State -->
  <main v-else class="min-h-screen py-20 px-4 flex items-center justify-center">
    <div class="text-center">
      <div class="text-6xl mb-4">📄</div>
      <h2 class="text-xl font-semibold text-slate-100 mb-2">暂无报告</h2>
      <p class="text-slate-400 mb-6">请先在学生详情页生成职业规划报告</p>
      <router-link :to="`/students/${studentId}`" class="btn-primary">
        返回学生详情
      </router-link>
    </div>
  </main>
</template>

<script setup>
import { ref, inject, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getReport, polishReport, exportReport } from '@/api'

const route = useRoute()
const setLoading = inject('setLoading')
const toast = inject('toast')
const studentId = route.params.studentId

const report = ref(null)
const reportHtml = ref('')
const busy = ref(false)
const msg = ref('')
const msgOk = ref(true)
const showExport = ref(false)
const dropdownRef = ref(null)

function handleClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    showExport.value = false
  }
}

async function load() {
  try {
    const { data } = await getReport(studentId)
    report.value = data
    reportHtml.value = data.report_html || ''
  } catch {}
}

async function polish() {
  if (!report.value) return
  busy.value = true; setLoading(true, 'AI正在润色报告…'); msg.value = ''
  try {
    const { data } = await polishReport(report.value.id)
    msg.value = data.message; msgOk.value = true
    toast(data.message, 'success')
    await load()
  } catch (e) {
    msg.value = e.response?.data?.message || '润色失败'; msgOk.value = false
    toast(msg.value, 'danger')
  } finally { busy.value = false; setLoading(false) }
}

function exportUrl(fmt) {
  return report.value ? exportReport(report.value.id, fmt) : '#'
}

onMounted(() => {
  load()
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style>
.report-content h1 {
  font-size: 1.6rem;
  font-weight: 700;
  border-bottom: 2px solid #7c3aed;
  padding-bottom: 0.5rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #e2e8f0;
}
.report-content h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #a78bfa;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
.report-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-top: 1rem;
}
.report-content p {
  line-height: 1.8;
  color: #94a3b8;
  margin-bottom: 1rem;
}
.report-content ul, .report-content ol {
  padding-left: 1.5rem;
  color: #94a3b8;
}
.report-content li {
  line-height: 1.7;
  margin-bottom: 0.25rem;
}
.report-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
.report-content th, .report-content td {
  border: 1px solid #1e293b;
  padding: 0.75rem;
  text-align: left;
}
.report-content th {
  background: #1e293b;
  font-weight: 600;
  color: #e2e8f0;
}
.report-content td {
  color: #94a3b8;
}
.report-content blockquote {
  border-left: 4px solid #7c3aed;
  background: rgba(124, 58, 237, 0.1);
  padding: 1rem 1.25rem;
  border-radius: 0 12px 12px 0;
  margin: 1rem 0;
  color: #a78bfa;
}
.report-content code {
  background: #1e293b;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #06b6d4;
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .report-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .report-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .report-header h1 {
  color: #0c4a6e;
}

:global(html.light) .report-meta {
  color: #64748b;
}

:global(html.light) .report-content h1,
:global(html.light) .report-content h2,
:global(html.light) .report-content h3 {
  color: #0c4a6e;
}

:global(html.light) .report-content h2 {
  border-bottom-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .report-content p,
:global(html.light) .report-content li {
  color: #475569;
}

:global(html.light) .report-content strong {
  color: #0c4a6e;
}

:global(html.light) .report-content th,
:global(html.light) .report-content td {
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .report-content th {
  background: rgba(8, 145, 178, 0.08);
  color: #0c4a6e;
}

:global(html.light) .report-content td {
  color: #475569;
}

:global(html.light) .report-content blockquote {
  border-left-color: #0891b2;
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .report-content code {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .btn-back {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .btn-back:hover {
  background: rgba(8, 145, 178, 0.15);
}
</style>
