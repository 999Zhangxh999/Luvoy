<template>
  <main class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <h1 class="text-3xl font-bold text-slate-100">
          <i class="bi bi-people mr-3 text-violet-400"></i>
          学生档案 <span class="gradient-text">管理</span>
        </h1>
        <router-link to="/students/create" class="btn-primary inline-flex items-center gap-2">
          <i class="bi bi-person-plus"></i>
          新建学生
        </router-link>
      </div>

      <!-- Desktop Table Card -->
      <div class="card hidden lg:block overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-800/50 border-b border-slate-700">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider w-16">#</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">姓名</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">学校</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">专业</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">学历</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase tracking-wider">画像</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase tracking-wider">匹配</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-slate-400 uppercase tracking-wider">报告</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-slate-400 uppercase tracking-wider w-28">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-700/50">
              <tr 
                v-for="s in students" 
                :key="s.id"
                class="hover:bg-slate-800/30 transition-colors"
              >
                <td class="px-4 py-3 text-slate-500">{{ s.id }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                      {{ s.name?.[0] || '?' }}
                    </div>
                    <span class="font-medium text-slate-100">{{ s.name }}</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-slate-400">{{ s.school || '-' }}</td>
                <td class="px-4 py-3 text-slate-400">{{ s.major || '-' }}</td>
                <td class="px-4 py-3">
                  <span class="badge">{{ s.education || '-' }}</span>
                </td>
                <td class="px-4 py-3 text-center">
                  <span 
                    :class="[
                      'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium',
                      s.has_profile 
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                        : 'bg-slate-700/50 text-slate-500'
                    ]"
                  >
                    <span :class="['w-1.5 h-1.5 rounded-full', s.has_profile ? 'bg-emerald-400' : 'bg-slate-500']"></span>
                    {{ s.has_profile ? '已生成' : '未生成' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center">
                  <span class="badge-cyan">{{ s.match_count || 0 }}</span>
                </td>
                <td class="px-4 py-3 text-center">
                  <span 
                    :class="[
                      'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium',
                      s.has_report 
                        ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' 
                        : 'bg-slate-700/50 text-slate-500'
                    ]"
                  >
                    <span :class="['w-1.5 h-1.5 rounded-full', s.has_report ? 'bg-cyan-400' : 'bg-slate-500']"></span>
                    {{ s.has_report ? '已生成' : '未生成' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <router-link 
                      :to="`/students/${s.id}`" 
                      class="px-3 py-1.5 text-xs font-medium text-violet-400 border border-violet-500/40 rounded-lg hover:bg-violet-500/10 transition-colors"
                    >
                      详情
                    </router-link>
                    <button 
                      @click.stop="confirmDelete(s)"
                      class="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      title="删除"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!students.length && !loading">
                <td colspan="9" class="px-4 py-16 text-center">
                  <div class="text-5xl mb-4">👤</div>
                  <p class="text-slate-400 mb-4">暂无学生档案</p>
                  <router-link to="/students/create" class="btn-primary inline-flex items-center gap-2">
                    <i class="bi bi-person-plus"></i>
                    创建第一个学生
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Mobile Card List -->
      <div class="lg:hidden space-y-3">
        <div 
          v-for="s in students" 
          :key="s.id"
          class="card group"
        >
          <div class="flex items-center gap-4">
            <router-link :to="`/students/${s.id}`" class="flex items-center gap-4 flex-1 min-w-0">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500 flex items-center justify-center text-white text-lg font-bold flex-shrink-0">
                {{ s.name?.[0] || '?' }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-semibold text-slate-100 group-hover:text-violet-400 transition-colors">
                  {{ s.name }}
                </div>
                <div class="text-slate-400 text-sm truncate">
                  {{ s.school || '-' }} · {{ s.major || '-' }}
                </div>
                <div class="flex flex-wrap gap-1.5 mt-2">
                  <span v-if="s.has_profile" class="px-2 py-0.5 text-xs rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <i class="bi bi-check-circle mr-1"></i>画像
                  </span>
                  <span v-if="s.has_report" class="px-2 py-0.5 text-xs rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    <i class="bi bi-file-text mr-1"></i>报告
                  </span>
                  <span class="badge-cyan text-xs">{{ s.match_count || 0 }} 匹配</span>
                </div>
              </div>
            </router-link>
            <button 
              @click="confirmDelete(s)"
              class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors flex-shrink-0"
              title="删除"
            >
              <i class="bi bi-trash text-lg"></i>
            </button>
          </div>
        </div>

        <div v-if="!students.length && !loading" class="card text-center py-12">
          <div class="text-5xl mb-4">👤</div>
          <p class="text-slate-400 mb-4">暂无学生档案</p>
          <router-link to="/students/create" class="btn-primary inline-flex items-center gap-2">
            <i class="bi bi-person-plus"></i>
            创建第一个学生
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="card text-center py-16">
        <div class="inline-block w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-slate-400">加载中...</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { getStudents, deleteStudent } from '@/api'

const students = ref([])
const loading = ref(false)
const showToast = inject('showToast')

async function loadStudents() {
  loading.value = true
  try {
    const { data } = await getStudents()
    students.value = data
  } finally {
    loading.value = false
  }
}

async function confirmDelete(s) {
  if (!confirm(`确定要删除学生「${s.name}」吗？\n\n此操作将同时删除该学生的画像、匹配结果和报告，且不可恢复。`)) {
    return
  }
  try {
    const { data } = await deleteStudent(s.id)
    if (data.success) {
      showToast?.(data.message || '删除成功', 'success')
      await loadStudents()
    } else {
      showToast?.(data.message || '删除失败', 'danger')
    }
  } catch (e) {
    showToast?.(e.response?.data?.message || '删除失败', 'danger')
  }
}

onMounted(loadStudents)
</script>
