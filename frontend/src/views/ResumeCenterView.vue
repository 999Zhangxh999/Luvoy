<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-file-earmark-person text-violet-400"></i> 简历中心
          </h1>
          <p class="text-sm text-brand-muted mt-1">简历上传、快速建档与批量处理</p>
        </div>
        <div class="flex items-center gap-3 flex-wrap">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-brand-surface border border-brand-border">
            <span class="text-violet-400 font-semibold text-sm">{{ stats.total }}</span>
            <span class="text-xs text-brand-muted">学生</span>
          </div>
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-brand-surface border border-brand-border">
            <span class="text-cyan-400 font-semibold text-sm">{{ stats.withProfile }}</span>
            <span class="text-xs text-brand-muted">已画像</span>
          </div>
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-brand-surface border border-brand-border">
            <span class="text-emerald-400 font-semibold text-sm">{{ stats.withMatch }}</span>
            <span class="text-xs text-brand-muted">已匹配</span>
          </div>
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-brand-surface border border-brand-border">
            <span class="text-amber-400 font-semibold text-sm">{{ stats.withReport }}</span>
            <span class="text-xs text-brand-muted">已报告</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 mb-6">
        <div class="card-sm p-4">
          <h3 class="mb-2 text-sm font-semibold text-brand-text">数据覆盖率</h3>
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-brand-muted">画像覆盖</span>
              <span class="text-violet-300">{{ coverage.profileRate }}%</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-brand-muted">匹配覆盖</span>
              <span class="text-cyan-300">{{ coverage.matchRate }}%</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-brand-muted">报告覆盖</span>
              <span class="text-amber-300">{{ coverage.reportRate }}%</span>
            </div>
          </div>
        </div>

        <div class="card-sm p-4">
          <h3 class="mb-2 text-sm font-semibold text-brand-text">学历结构</h3>
          <div class="flex flex-wrap gap-1">
            <span v-for="item in educationDistribution" :key="item.label" class="badge-cyan text-xs">
              {{ item.label }} {{ item.count }}
            </span>
          </div>
        </div>

        <div class="card-sm p-4">
          <h3 class="mb-2 text-sm font-semibold text-brand-text">目标岗位热词</h3>
          <div class="flex flex-wrap gap-1">
            <span v-for="item in topTargetPositions" :key="item.name" class="badge text-xs">
              {{ item.name }} {{ item.count }}
            </span>
          </div>
        </div>
      </div>

      <section class="mb-8 grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div class="card p-5">
          <h2 class="mb-4 text-lg font-semibold text-brand-text">
            <i class="bi bi-cloud-upload mr-2 text-violet-400"></i>上传简历
          </h2>
          <div
            class="cursor-pointer rounded-xl border-2 border-dashed border-brand-border p-8 text-center transition"
            :class="isDragging ? 'border-violet-500 bg-violet-500/5' : 'hover:border-violet-500/40'"
            @click="openFileDialog"
            @dragover.prevent="isDragging = true"
            @dragleave="isDragging = false"
            @drop.prevent="handleDrop"
          >
            <input ref="fileInput" class="hidden" type="file" accept=".pdf,.docx,.doc" @change="handleFileSelect" />
            <i class="bi bi-file-earmark-arrow-up text-4xl text-violet-400"></i>
            <p class="mt-2 text-brand-text">拖拽或点击上传简历文件</p>
            <p class="text-xs text-brand-muted">支持 PDF / DOCX / DOC</p>
          </div>

          <div v-if="selectedFile" class="mt-4 rounded-xl border border-brand-border bg-brand-surface p-3">
            <div class="flex items-center justify-between gap-2">
              <div class="min-w-0">
                <div class="truncate text-sm text-brand-text">{{ selectedFile.name }}</div>
                <div class="text-xs text-brand-muted">{{ formatFileSize(selectedFile.size) }}</div>
              </div>
              <button class="text-brand-muted hover:text-red-400" @click="selectedFile = null">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="card p-5">
          <h2 class="mb-4 text-lg font-semibold text-brand-text">
            <i class="bi bi-person-plus mr-2 text-cyan-400"></i>快速建档
          </h2>
          <div class="space-y-3">
            <input v-model="quickForm.name" class="input-base" placeholder="姓名 *" />
            <div class="grid grid-cols-2 gap-2">
              <select v-model="quickForm.education" class="input-base">
                <option value="">学历</option>
                <option value="大专">大专</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
              <input v-model="quickForm.major" class="input-base" placeholder="专业" />
            </div>
            <input v-model="quickForm.school" class="input-base" placeholder="毕业院校" />
            <input v-model="quickForm.targetPositions" class="input-base" placeholder="目标岗位（逗号分隔）" />
            <textarea v-model="quickForm.resumeText" class="input-base min-h-24" placeholder="可选：补充简历文本内容，便于AI解析"></textarea>
          </div>
        </div>

        <div class="card flex flex-col p-5">
          <h2 class="mb-4 text-lg font-semibold text-brand-text">
            <i class="bi bi-gear mr-2 text-emerald-400"></i>创建策略
          </h2>
          <div class="space-y-2 text-sm text-brand-muted">
            <label class="flex items-center gap-2"><input v-model="createMode" type="radio" value="resume" /> 从简历解析</label>
            <label class="flex items-center gap-2"><input v-model="createMode" type="radio" value="form" /> 仅手动表单</label>
            <label class="flex items-center gap-2"><input v-model="createMode" type="radio" value="quiz" /> 进入问卷建档</label>
          </div>

          <div class="mt-4 rounded-xl border border-brand-border bg-brand-surface p-3 text-xs text-brand-muted">
            创建后可直接在列表执行批量画像生成、批量匹配和批量报告生成。
          </div>

          <div class="mt-auto space-y-2 pt-4">
            <button
              v-if="createMode === 'quiz'"
              class="btn-primary w-full"
              @click="$router.push('/students/create')"
            >
              <i class="bi bi-clipboard-check mr-2"></i>进入问卷建档
            </button>
            <button
              v-else
              class="btn-primary w-full"
              :disabled="creating || (!selectedFile && !quickForm.name)"
              @click="createStudent"
            >
              <i class="bi bi-magic mr-2" :class="{ 'animate-spin': creating }"></i>
              {{ creating ? '创建中...' : '创建学生档案' }}
            </button>
          </div>
        </div>
      </section>

      <section class="card mb-8 p-5">
        <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
          <h2 class="text-xl font-semibold text-brand-text">
            <i class="bi bi-people mr-2 text-violet-400"></i>学生档案库
          </h2>
          <div class="flex flex-wrap items-center gap-2">
            <div class="relative">
              <i class="bi bi-search absolute left-3 top-1/2 -translate-y-1/2 text-brand-muted"></i>
              <input v-model="searchQuery" class="input-base w-56 py-2 pl-9" placeholder="搜索姓名/专业/学校" />
            </div>
            <select v-model="filterStatus" class="input-base w-40 py-2">
              <option value="all">全部状态</option>
              <option value="profile">有画像</option>
              <option value="match">有匹配</option>
              <option value="report">有报告</option>
            </select>
            <select v-model="sortBy" class="input-base w-40 py-2">
              <option value="new">按创建时间</option>
              <option value="match">按匹配数</option>
              <option value="name">按姓名</option>
            </select>
            <!-- 批量删除按钮 -->
            <button
              v-if="selectedStudents.length > 0"
              class="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-red-600 text-white text-xs hover:bg-red-500 transition"
              @click="confirmBatchDelete"
            >
              <i class="bi bi-trash"></i> 删除选中 ({{ selectedStudents.length }})
            </button>
          </div>
        </div>

        <div v-if="loading" class="py-16 text-center text-brand-muted">
          <i class="bi bi-hourglass-split mr-2 animate-spin"></i>加载学生档案中...
        </div>

        <div v-else-if="paginatedStudents.length === 0" class="py-16 text-center text-brand-muted">
          未检索到符合条件的学生档案
        </div>

        <div v-else class="space-y-3">
          <!-- 全选 -->
          <div class="flex items-center gap-2 px-2 text-xs text-brand-muted">
            <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" class="accent-violet-500" />
            <span>全选当前页</span>
          </div>
          <article v-for="student in paginatedStudents" :key="student.id" class="rounded-xl border border-brand-border bg-brand-surface p-4">
            <div class="flex flex-wrap items-start justify-between gap-3">
              <div class="min-w-0 flex-1 flex items-start gap-3">
                <input
                  type="checkbox"
                  :checked="selectedStudents.includes(student.id)"
                  @change="toggleStudentSelect(student.id)"
                  class="mt-1 accent-violet-500"
                />
                <div class="min-w-0 flex-1">
                  <div class="mb-1 flex flex-wrap items-center gap-2">
                    <h3 class="font-semibold text-brand-text">{{ student.name || '未命名' }}</h3>
                    <span class="badge text-xs">{{ student.education || '学历未知' }}</span>
                  </div>
                  <p class="text-sm text-brand-muted">{{ student.major || '专业未知' }} · {{ student.school || '学校未知' }}</p>
                  <p class="mt-1 text-xs text-brand-muted">
                    目标岗位：{{ (student.target_positions || []).join(' / ') || '未填写' }}
                  </p>
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-2 text-xs">
                <span :class="student.has_profile ? 'badge-green' : 'badge'">{{ student.has_profile ? '已有画像' : '无画像' }}</span>
                <span class="badge-cyan">{{ student.match_count || 0 }} 个匹配</span>
                <span v-if="student.has_report" class="badge-orange">已有报告</span>
              </div>
            </div>

            <div class="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-brand-border pt-3">
              <div class="flex items-center gap-2 text-xs text-brand-muted">
                <span>简历文本：{{ (student.resume_text || '').length }} 字</span>
              </div>
              <div class="flex items-center gap-2">
                <router-link :to="`/students/${student.id}`" class="btn-ghost text-xs"><i class="bi bi-eye mr-1"></i>详情</router-link>
                <router-link :to="`/matching/${student.id}`" class="btn-ghost text-xs"><i class="bi bi-link-45deg mr-1"></i>匹配</router-link>
                <router-link :to="`/reports/${student.id}`" class="btn-ghost text-xs"><i class="bi bi-file-text mr-1"></i>报告</router-link>
                <button class="btn-ghost text-xs text-red-400 hover:bg-red-500/10" @click="confirmDelete(student)">
                  <i class="bi bi-trash mr-1"></i>删除
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-if="totalPages > 1" class="mt-4 flex items-center justify-center gap-2">
          <button class="btn-secondary px-3 py-2" :disabled="currentPage === 1" @click="currentPage = Math.max(1, currentPage - 1)">
            <i class="bi bi-chevron-left"></i>
          </button>
          <button
            v-for="page in visiblePages"
            :key="page"
            class="h-9 w-9 rounded-lg text-sm"
            :class="page === currentPage ? 'bg-violet-600 text-white' : 'bg-brand-surface text-brand-muted'"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
          <button class="btn-secondary px-3 py-2" :disabled="currentPage === totalPages" @click="currentPage = Math.min(totalPages, currentPage + 1)">
            <i class="bi bi-chevron-right"></i>
          </button>
        </div>
      </section>

      <section class="card p-5">
        <h2 class="mb-4 text-lg font-semibold text-brand-text">
          <i class="bi bi-lightning mr-2 text-violet-400"></i>批量任务中心
        </h2>

        <div class="mb-4 grid grid-cols-1 gap-3 md:grid-cols-3">
          <button class="btn-secondary" :disabled="Boolean(batchProcessing)" @click="batchGenerateProfiles">
            <i class="bi bi-cpu mr-2" :class="{ 'animate-spin': batchProcessing === 'profile' }"></i>批量生成画像
          </button>
          <button class="btn-secondary" :disabled="Boolean(batchProcessing)" @click="batchRunMatching">
            <i class="bi bi-link-45deg mr-2" :class="{ 'animate-spin': batchProcessing === 'match' }"></i>批量执行匹配
          </button>
          <button class="btn-secondary" :disabled="Boolean(batchProcessing)" @click="batchGenerateReports">
            <i class="bi bi-file-text mr-2" :class="{ 'animate-spin': batchProcessing === 'report' }"></i>批量生成报告
          </button>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
            <div class="text-lg font-bold text-violet-400">{{ pendingBatch.profile }}</div>
            <div class="text-xs text-brand-muted">待生成画像</div>
          </div>
          <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
            <div class="text-lg font-bold text-cyan-400">{{ pendingBatch.match }}</div>
            <div class="text-xs text-brand-muted">待执行匹配</div>
          </div>
          <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
            <div class="text-lg font-bold text-amber-400">{{ pendingBatch.report }}</div>
            <div class="text-xs text-brand-muted">待生成报告</div>
          </div>
        </div>

        <div v-if="batchProgress" class="mt-4 rounded-xl border border-brand-border bg-brand-surface p-3">
          <div class="mb-2 flex items-center justify-between text-sm text-brand-muted">
            <span>{{ batchProgress.message }}</span>
            <span>{{ batchProgress.current }} / {{ batchProgress.total }}</span>
          </div>
          <div class="h-2 overflow-hidden rounded-full bg-brand-card">
            <div class="h-full rounded-full bg-gradient-to-r from-violet-600 to-cyan-500" :style="{ width: `${(batchProgress.current / batchProgress.total) * 100}%` }"></div>
          </div>
        </div>
      </section>
    </div>

    <!-- ═══ 可爱机器人AI助手（职业探索风格） ═══ -->
    <div
      class="rc-ai-agent"
      :class="{ 'is-active': aiActive, 'is-dragging': aiDragging }"
      :style="{ left: aiPosX + 'px', bottom: aiPosY + 'px' }"
    >
      <div v-if="aiActive" class="rc-backdrop" @click="aiActive = false"></div>

      <!-- 机器人角色 -->
      <div
        class="rc-agent-wrapper"
        @click="handleRobotClick"
        @mousedown="startRobotDrag"
        @mouseenter="robotEye = 'happy'; robotMouth = 'smile'"
        @mouseleave="robotEye = 'normal'; robotMouth = 'normal'"
      >
        <div class="rc-pulse" v-if="!aiActive && !aiDragging"></div>
        <div class="rc-pulse rc-delay" v-if="!aiActive && !aiDragging"></div>

        <div class="rc-robot" :class="{ thinking: aiThinking, happy: robotEye === 'happy' }">
          <div class="rc-glow"></div>
          <div class="rc-avatar-main">
            <div class="rc-antenna-wrap">
              <div class="rc-antenna-stem"></div>
              <div class="rc-antenna-tip" :class="{ active: aiThinking }"></div>
            </div>
            <div class="rc-face">
              <div class="rc-eyes">
                <div class="rc-eye left" :class="robotEye"><div class="rc-pupil"></div><div class="rc-hl"></div></div>
                <div class="rc-eye right" :class="robotEye"><div class="rc-pupil"></div><div class="rc-hl"></div></div>
              </div>
              <div class="rc-mouth" :class="robotMouth"></div>
              <div class="rc-cheek left"></div>
              <div class="rc-cheek right"></div>
            </div>
          </div>
          <div class="rc-status" :class="{ thinking: aiThinking }">
            <span class="rc-status-text">{{ aiThinking ? '思考中...' : '在线' }}</span>
          </div>
        </div>
      </div>

      <!-- 闲聊气泡 -->
      <transition name="rc-bubble-pop">
        <div v-if="showBubble && !aiActive" class="rc-idle-bubble" @click="aiActive = true; showBubble = false">
          <span>{{ bubbleText }}</span>
        </div>
      </transition>

      <!-- 主交互面板 -->
      <transition name="rc-panel-spring">
        <div v-if="aiActive" class="rc-panel">
          <div class="rc-panel-header">
            <div class="flex items-center gap-2">
              <span class="text-xl">🤖</span>
              <span class="text-sm font-semibold text-white">简历中心小智</span>
            </div>
            <button class="rc-close-btn" @click="aiActive = false"><i class="bi bi-x-lg"></i></button>
          </div>

          <!-- 对话区域 -->
          <div class="rc-chat-zone" ref="chatZoneRef">
            <div v-for="(msg, idx) in chatHistory" :key="idx" class="rc-chat-msg" :class="msg.role">
              <span v-if="msg.role === 'assistant'" class="rc-msg-avatar">🤖</span>
              <div class="rc-msg-content">
                <p class="rc-msg-text">{{ msg.content }}</p>
                <div v-if="msg.actions && msg.actions.length" class="rc-msg-actions">
                  <button
                    v-for="action in msg.actions"
                    :key="action.id"
                    class="rc-action-chip"
                    @click="handleAgentAction(action)"
                  >
                    <i v-if="action.icon" :class="action.icon" class="mr-1"></i>{{ action.label }}
                  </button>
                </div>
              </div>
            </div>
            <div v-if="aiThinking" class="rc-chat-msg assistant typing">
              <span class="rc-msg-avatar">🤖</span>
              <div class="rc-msg-content">
                <div class="rc-typing"><span></span><span></span><span></span></div>
              </div>
            </div>
          </div>

          <!-- 功能网格 -->
          <div v-if="showMenu" class="rc-action-grid">
            <button class="rc-action-card" @click="doAgentAction('analyze')">
              <span class="text-xl">📊</span>
              <span class="text-xs text-slate-300">数据分析</span>
            </button>
            <button class="rc-action-card" @click="doAgentAction('advice')">
              <span class="text-xl">💡</span>
              <span class="text-xs text-slate-300">求职建议</span>
            </button>
            <button class="rc-action-card" @click="doAgentAction('batch')">
              <span class="text-xl">⚡</span>
              <span class="text-xs text-slate-300">批量操作</span>
            </button>
            <button class="rc-action-card" @click="doAgentAction('delete-guide')">
              <span class="text-xl">🗑️</span>
              <span class="text-xs text-slate-300">清理档案</span>
            </button>
          </div>

          <!-- 快捷回复 -->
          <div class="rc-quick-bar">
            <button v-for="qr in quickReplies" :key="qr.id" class="rc-quick-btn" @click="handleQuickReply(qr)">
              <span>{{ qr.icon }}</span><span>{{ qr.text }}</span>
            </button>
          </div>

          <!-- 输入框 -->
          <div class="rc-input-bar">
            <input
              v-model="aiInput"
              type="text"
              placeholder="问我任何问题..."
              @keyup.enter="sendMessage"
            />
            <button class="rc-send-btn" @click="sendMessage" :disabled="!aiInput.trim()">
              <i class="bi bi-send-fill"></i>
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- 删除确认弹窗 -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div class="w-full max-w-md rounded-2xl border border-brand-border bg-brand-card p-6">
            <div class="mb-5 text-center">
              <div class="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-red-500/10 text-red-400">
                <i class="bi bi-exclamation-triangle text-2xl"></i>
              </div>
              <h3 class="mb-1 text-lg font-semibold text-brand-text">确认删除学生档案</h3>
              <p class="text-sm text-brand-muted">将删除 {{ deleteTarget.name }} 及其画像、匹配和报告数据。</p>
            </div>
            <div class="flex gap-2">
              <button class="btn-secondary flex-1" @click="deleteTarget = null">取消</button>
              <button class="flex-1 rounded-xl bg-red-600 py-2 text-sm font-semibold text-white hover:bg-red-500" :disabled="deleting" @click="executeDelete">
                {{ deleting ? '删除中...' : '确认删除' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- 批量删除确认弹窗 -->
      <Transition name="fade">
        <div v-if="showBatchDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div class="w-full max-w-md rounded-2xl border border-brand-border bg-brand-card p-6">
            <div class="mb-5 text-center">
              <div class="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-red-500/10 text-red-400">
                <i class="bi bi-trash text-2xl"></i>
              </div>
              <h3 class="mb-1 text-lg font-semibold text-brand-text">批量删除确认</h3>
              <p class="text-sm text-brand-muted">即将删除 {{ selectedStudents.length }} 名学生的全部数据（画像、匹配、报告），不可恢复。</p>
            </div>
            <div class="flex gap-2">
              <button class="btn-secondary flex-1" @click="showBatchDeleteModal = false">取消</button>
              <button class="flex-1 rounded-xl bg-red-600 py-2 text-sm font-semibold text-white hover:bg-red-500" :disabled="batchDeleting" @click="executeBatchDelete">
                {{ batchDeleting ? '删除中...' : '确认删除' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, inject, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  chatWithAI,
  createStudent as apiCreateStudent,
  deleteStudent,
  generateReport,
  generateStudentProfile,
  getStudents,
  runMatching,
} from '@/api'

const router = useRouter()
const toast = inject('toast', null)

const loading = ref(true)
const creating = ref(false)
const deleting = ref(false)
const students = ref([])

const searchQuery = ref('')
const filterStatus = ref('all')
const sortBy = ref('new')

const currentPage = ref(1)
const pageSize = 8

const isDragging = ref(false)
const selectedFile = ref(null)
const fileInput = ref(null)

const createMode = ref('resume')
const quickForm = reactive({
  name: '',
  education: '',
  major: '',
  school: '',
  targetPositions: '',
  resumeText: '',
})

const deleteTarget = ref(null)
const batchProcessing = ref(null)
const batchProgress = ref(null)

// ═══ 批量选择 & 删除 ═══
const selectedStudents = ref([])
const showBatchDeleteModal = ref(false)
const batchDeleting = ref(false)

const isAllSelected = computed(() => {
  if (paginatedStudents.value.length === 0) return false
  return paginatedStudents.value.every((s) => selectedStudents.value.includes(s.id))
})

function toggleStudentSelect(id) {
  const idx = selectedStudents.value.indexOf(id)
  if (idx >= 0) selectedStudents.value.splice(idx, 1)
  else selectedStudents.value.push(id)
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    const pageIds = paginatedStudents.value.map((s) => s.id)
    selectedStudents.value = selectedStudents.value.filter((id) => !pageIds.includes(id))
  } else {
    const pageIds = paginatedStudents.value.map((s) => s.id)
    const merged = new Set([...selectedStudents.value, ...pageIds])
    selectedStudents.value = [...merged]
  }
}

function confirmBatchDelete() {
  if (selectedStudents.value.length === 0) return
  showBatchDeleteModal.value = true
}

async function executeBatchDelete() {
  batchDeleting.value = true
  let success = 0
  for (const id of selectedStudents.value) {
    try {
      await deleteStudent(id)
      success++
    } catch (e) {
      console.error(e)
    }
  }
  toast?.(`成功删除 ${success} 条档案`, 'success')
  selectedStudents.value = []
  showBatchDeleteModal.value = false
  batchDeleting.value = false
  await loadStudents()
}

// ═══ AI 机器人助手 ═══
const aiActive = ref(false)
const aiThinking = ref(false)
const aiDragging = ref(false)
const aiInput = ref('')
const chatZoneRef = ref(null)
const robotEye = ref('normal')
const robotMouth = ref('normal')
const showMenu = ref(true)
const showBubble = ref(false)
const bubbleText = ref('')

const aiPosX = ref(28)
const aiPosY = ref(28)
const dragStart = { x: 0, y: 0, px: 0, py: 0 }
let dragMoved = false

const chatHistory = ref([
  {
    role: 'assistant',
    content: '嗨！我是简历中心的AI助手小智 🤖\n\n我可以帮你：\n• 分析学生数据\n• 提供求职建议\n• 指导批量操作\n• 清理无用档案\n\n选择下方功能或直接输入问题~',
  },
])

const quickReplies = ref([
  { id: 'status', icon: '📊', text: '当前状态' },
  { id: 'tips', icon: '💡', text: '给点建议' },
  { id: 'help', icon: '🆘', text: '怎么用' },
])

const idleBubbles = [
  '有新档案需要处理吗？🤔',
  '点我帮你分析数据~',
  '需要我帮忙清理旧档案吗？',
  '批量操作了解一下？⚡',
  '简历管理有问题？找我！',
  '我可以帮你优化工作流 ✨',
]

let bubbleTimer = null

function startBubbleTimer() {
  bubbleTimer = setInterval(() => {
    if (!aiActive.value) {
      bubbleText.value = idleBubbles[Math.floor(Math.random() * idleBubbles.length)]
      showBubble.value = true
      setTimeout(() => { showBubble.value = false }, 5000)
    }
  }, 18000)
}

// 拖拽
function startRobotDrag(e) {
  if (aiActive.value) return
  dragMoved = false
  dragStart.x = e.clientX
  dragStart.y = e.clientY
  dragStart.px = aiPosX.value
  dragStart.py = aiPosY.value
  document.addEventListener('mousemove', onRobotDrag)
  document.addEventListener('mouseup', endRobotDrag)
}

function onRobotDrag(e) {
  const dx = e.clientX - dragStart.x
  const dy = dragStart.y - e.clientY
  if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
    dragMoved = true
    aiDragging.value = true
  }
  aiPosX.value = Math.max(10, Math.min(window.innerWidth - 100, dragStart.px + dx))
  aiPosY.value = Math.max(10, Math.min(window.innerHeight - 100, dragStart.py + dy))
}

function endRobotDrag() {
  document.removeEventListener('mousemove', onRobotDrag)
  document.removeEventListener('mouseup', endRobotDrag)
  setTimeout(() => { aiDragging.value = false }, 50)
}

function handleRobotClick() {
  if (!dragMoved) {
    aiActive.value = !aiActive.value
    showBubble.value = false
  }
  dragMoved = false
}

function scrollChat() {
  nextTick(() => {
    if (chatZoneRef.value) chatZoneRef.value.scrollTop = chatZoneRef.value.scrollHeight
  })
}

function addAIMsg(content, actions) {
  chatHistory.value.push({ role: 'assistant', content, actions })
  scrollChat()
}

function addUserMsg(content) {
  chatHistory.value.push({ role: 'user', content })
  scrollChat()
}

// 真正调用后端LLM的对话
async function callAI(message) {
  aiThinking.value = true
  scrollChat()
  try {
    const context = {
      student_count: stats.value.total,
      profile_count: stats.value.withProfile,
      match_count: stats.value.withMatch,
    }
    const history = chatHistory.value.slice(-12).map((m) => ({
      role: m.role,
      content: m.content,
    }))
    const res = await chatWithAI(message, context, history)
    aiThinking.value = false
    if (res.data?.success) {
      addAIMsg(res.data.reply)
    } else {
      addAIMsg('抱歉，AI暂时无法回复，请稍后再试 😅')
    }
  } catch (e) {
    aiThinking.value = false
    addAIMsg('网络错误，请检查后端服务是否运行 🔌')
  }
}

async function sendMessage() {
  const text = aiInput.value.trim()
  if (!text) return
  addUserMsg(text)
  aiInput.value = ''
  showMenu.value = false
  await callAI(text)
}

function handleQuickReply(qr) {
  switch (qr.id) {
    case 'status':
      doAgentAction('analyze')
      break
    case 'tips':
      addUserMsg('给点求职建议')
      callAI('根据当前学生档案数据，给我一些简历管理和求职方面的建议')
      break
    case 'help':
      addAIMsg(
        '📖 使用指南：\n\n1️⃣ 上传简历文件或手动填写信息创建学生档案\n2️⃣ 在档案列表中可以查看详情、匹配岗位、生成报告\n3️⃣ 批量任务中心可一键生成画像/匹配/报告\n4️⃣ 勾选多个档案后可批量删除\n5️⃣ 有问题随时问我！',
      )
      break
    default:
      addUserMsg(qr.text)
      callAI(qr.text)
  }
}

function doAgentAction(type) {
  showMenu.value = false
  switch (type) {
    case 'analyze': {
      const s = stats.value
      const c = coverage.value
      addAIMsg(
        `📊 当前数据概览：\n\n👥 总学生数：${s.total}\n✅ 已画像：${s.withProfile}（${c.profileRate}%）\n🔗 已匹配：${s.withMatch}（${c.matchRate}%）\n📄 已报告：${s.withReport}（${c.reportRate}%）\n\n${
          c.profileRate < 50
            ? '⚠️ 画像覆盖率较低，建议执行批量生成画像'
            : c.matchRate < 50
              ? '💡 建议执行批量匹配提升覆盖率'
              : '🎉 数据覆盖率不错！'
        }`,
        [
          { id: 'batch-profile', icon: 'bi bi-cpu', label: '批量画像' },
          { id: 'batch-match', icon: 'bi bi-link-45deg', label: '批量匹配' },
        ],
      )
      break
    }
    case 'advice':
      addUserMsg('给我一些求职建议')
      callAI('基于当前数据，给出简历优化和求职的具体建议')
      break
    case 'batch':
      addAIMsg(
        `⚡ 批量操作指南：\n\n📋 待生成画像：${pendingBatch.value.profile} 人\n🔗 待执行匹配：${pendingBatch.value.match} 人\n📄 待生成报告：${pendingBatch.value.report} 人\n\n点击下方按钮快速执行：`,
        [
          { id: 'batch-profile', icon: 'bi bi-cpu', label: '批量画像' },
          { id: 'batch-match', icon: 'bi bi-link-45deg', label: '批量匹配' },
          { id: 'batch-report', icon: 'bi bi-file-text', label: '批量报告' },
        ],
      )
      break
    case 'delete-guide': {
      const noProfile = students.value.filter((s) => !s.has_profile).length
      addAIMsg(
        `🗑️ 档案清理助手：\n\n当前有 ${noProfile} 名学生无画像数据。\n\n你可以：\n• 勾选列表中的学生，点击"删除选中"批量删除\n• 使用下方按钮一键选中所有无画像的学生\n\n⚠️ 删除操作不可恢复，请谨慎操作！`,
        [{ id: 'select-no-profile', icon: 'bi bi-check-all', label: '选中无画像学生' }],
      )
      break
    }
  }
}

function handleAgentAction(action) {
  switch (action.id) {
    case 'batch-profile':
      batchGenerateProfiles()
      addAIMsg('已启动批量画像生成 ⚙️ 请在页面下方查看进度')
      break
    case 'batch-match':
      batchRunMatching()
      addAIMsg('已启动批量匹配 🔗 请在页面下方查看进度')
      break
    case 'batch-report':
      batchGenerateReports()
      addAIMsg('已启动批量报告生成 📄 请在页面下方查看进度')
      break
    case 'select-no-profile':
      selectedStudents.value = students.value.filter((s) => !s.has_profile).map((s) => s.id)
      addAIMsg(`已选中 ${selectedStudents.value.length} 名无画像学生，你可以在列表上方点击"删除选中"按钮执行批量删除。`)
      break
  }
}

// ═══ 原有逻辑 ═══
const stats = computed(() => {
  const list = students.value
  return {
    total: list.length,
    withProfile: list.filter((item) => item.has_profile).length,
    withMatch: list.filter((item) => Number(item.match_count || 0) > 0).length,
    withReport: list.filter((item) => item.has_report).length,
  }
})

const coverage = computed(() => {
  const total = stats.value.total || 1
  return {
    profileRate: Math.round((stats.value.withProfile / total) * 100),
    matchRate: Math.round((stats.value.withMatch / total) * 100),
    reportRate: Math.round((stats.value.withReport / total) * 100),
  }
})

const educationDistribution = computed(() => {
  const map = new Map()
  students.value.forEach((student) => {
    const key = student.education || '未知'
    map.set(key, (map.get(key) || 0) + 1)
  })
  return Array.from(map.entries())
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count)
})

const topTargetPositions = computed(() => {
  const map = new Map()
  students.value.forEach((student) => {
    ;(student.target_positions || []).forEach((position) => {
      map.set(position, (map.get(position) || 0) + 1)
    })
  })
  return Array.from(map.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 12)
})

const filteredStudents = computed(() => {
  let rows = [...students.value]

  const keyword = searchQuery.value.trim().toLowerCase()
  if (keyword) {
    rows = rows.filter((student) => {
      const text = [
        student.name,
        student.major,
        student.school,
        (student.target_positions || []).join(' '),
      ]
        .join(' ')
        .toLowerCase()
      return text.includes(keyword)
    })
  }

  if (filterStatus.value === 'profile') {
    rows = rows.filter((student) => student.has_profile)
  } else if (filterStatus.value === 'match') {
    rows = rows.filter((student) => Number(student.match_count || 0) > 0)
  } else if (filterStatus.value === 'report') {
    rows = rows.filter((student) => student.has_report)
  }

  rows.sort((a, b) => {
    if (sortBy.value === 'name') return String(a.name || '').localeCompare(String(b.name || ''))
    if (sortBy.value === 'match') return Number(b.match_count || 0) - Number(a.match_count || 0)
    return Number(b.id || 0) - Number(a.id || 0)
  })

  return rows
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredStudents.value.length / pageSize)))

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredStudents.value.slice(start, start + pageSize)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let page = start; page <= end; page += 1) pages.push(page)
  return pages
})

const pendingBatch = computed(() => ({
  profile: students.value.filter((student) => !student.has_profile).length,
  match: students.value.filter((student) => student.has_profile && Number(student.match_count || 0) === 0).length,
  report: students.value.filter((student) => student.has_profile && !student.has_report).length,
}))

function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function openFileDialog() {
  fileInput.value?.click()
}

function handleDrop(event) {
  isDragging.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) selectedFile.value = file
}

function handleFileSelect(event) {
  const file = event.target.files?.[0]
  if (file) selectedFile.value = file
}

async function createStudent() {
  if (!selectedFile.value && !quickForm.name) return

  creating.value = true
  try {
    const formData = new FormData()

    if (selectedFile.value) {
      formData.append('resume_file', selectedFile.value)
    }

    if (quickForm.name) formData.append('name', quickForm.name)
    if (quickForm.education) formData.append('education', quickForm.education)
    if (quickForm.major) formData.append('major', quickForm.major)
    if (quickForm.school) formData.append('school', quickForm.school)
    if (quickForm.targetPositions) formData.append('target_positions', quickForm.targetPositions)
    if (quickForm.resumeText) formData.append('resume_text', quickForm.resumeText)

    const response = await apiCreateStudent(formData)
    if (response.data?.success) {
      toast?.('学生档案创建成功', 'success')
      await loadStudents()

      selectedFile.value = null
      Object.assign(quickForm, {
        name: '',
        education: '',
        major: '',
        school: '',
        targetPositions: '',
        resumeText: '',
      })

      router.push(`/students/${response.data.data.id}`)
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '创建学生档案失败', 'danger')
  } finally {
    creating.value = false
  }
}

function confirmDelete(student) {
  deleteTarget.value = student
}

async function executeDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await deleteStudent(deleteTarget.value.id)
    toast?.('学生档案删除成功', 'success')
    deleteTarget.value = null
    await loadStudents()
  } catch (error) {
    toast?.(error?.response?.data?.message || '删除学生档案失败', 'danger')
  } finally {
    deleting.value = false
  }
}

async function runBatch(type, targets, action, message) {
  if (!targets.length) {
    toast?.(`暂无可${message}的数据`, 'info')
    return
  }

  batchProcessing.value = type
  batchProgress.value = {
    message: `${message}中...`,
    current: 0,
    total: targets.length,
  }

  for (let index = 0; index < targets.length; index += 1) {
    try {
      await action(targets[index].id)
    } catch (error) {
      console.error(error)
    }
    batchProgress.value.current = index + 1
  }

  await loadStudents()
  batchProcessing.value = null
  batchProgress.value = null
  toast?.(`${message}完成`, 'success')
}

async function batchGenerateProfiles() {
  const targets = students.value.filter((student) => !student.has_profile)
  await runBatch('profile', targets, generateStudentProfile, '批量生成画像')
}

async function batchRunMatching() {
  const targets = students.value.filter(
    (student) => student.has_profile && Number(student.match_count || 0) === 0,
  )
  await runBatch('match', targets, (id) => runMatching(id, 5), '批量执行匹配')
}

async function batchGenerateReports() {
  const targets = students.value.filter((student) => student.has_profile && !student.has_report)
  await runBatch('report', targets, generateReport, '批量生成报告')
}

async function loadStudents() {
  loading.value = true
  try {
    const response = await getStudents()
    students.value = response.data || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '加载学生档案失败', 'danger')
  } finally {
    loading.value = false
  }
}

watch(
  [searchQuery, filterStatus, sortBy],
  () => {
    currentPage.value = 1
  },
  { deep: true },
)

onMounted(() => {
  loadStudents()
  startBubbleTimer()
  setTimeout(() => {
    if (!aiActive.value) {
      bubbleText.value = '嗨！需要帮你管理简历吗？点我开始~'
      showBubble.value = true
      setTimeout(() => { showBubble.value = false }, 5000)
    }
  }, 3000)
})

onUnmounted(() => {
  if (bubbleTimer) clearInterval(bubbleTimer)
})
</script>

<style scoped>
/* ═══ 可爱机器人AI助手 - 与职业探索页同风格 ═══ */
.rc-ai-agent {
  position: fixed;
  z-index: 1000;
  font-family: 'Inter', -apple-system, sans-serif;
}
.rc-ai-agent.is-dragging { cursor: grabbing; user-select: none; }
.rc-backdrop { position: fixed; inset: 0; z-index: -1; }
.rc-agent-wrapper { position: relative; cursor: grab; }
.rc-ai-agent.is-dragging .rc-agent-wrapper { cursor: grabbing; }
.rc-ai-agent.is-active .rc-agent-wrapper { cursor: pointer; }

/* 脉冲 */
.rc-pulse {
  position: absolute; inset: -8px; border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.4);
  animation: rc-pulse 2s ease-out infinite;
}
.rc-pulse.rc-delay { animation-delay: 1s; }
@keyframes rc-pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.8); opacity: 0; }
}

/* 机器人 */
.rc-robot {
  width: 72px; height: 72px; position: relative;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.rc-robot:hover { transform: scale(1.08); }
.rc-robot.happy { animation: rc-bounce 0.5s ease; }
@keyframes rc-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.rc-glow {
  position: absolute; inset: -12px; border-radius: 50%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.35) 0%, transparent 70%);
  filter: blur(8px);
  animation: rc-glow-pulse 3s ease-in-out infinite;
}
@keyframes rc-glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}
.rc-avatar-main { width: 100%; height: 100%; position: relative; }

/* 天线 */
.rc-antenna-wrap {
  position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center;
}
.rc-antenna-stem { width: 4px; height: 10px; background: linear-gradient(to bottom, #a78bfa, #8b5cf6); border-radius: 2px; }
.rc-antenna-tip {
  width: 10px; height: 10px; border-radius: 50%;
  background: linear-gradient(135deg, #34d399, #10b981);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
  animation: rc-glow-soft 2s ease-in-out infinite;
}
.rc-antenna-tip.active {
  animation: rc-blink 0.4s ease-in-out infinite;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.7);
}
@keyframes rc-glow-soft {
  0%, 100% { box-shadow: 0 0 8px rgba(16, 185, 129, 0.5); }
  50% { box-shadow: 0 0 16px rgba(16, 185, 129, 0.8); }
}
@keyframes rc-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* 脸 */
.rc-face {
  width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(145deg, #fef3c7, #fde68a);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15), inset 0 -4px 12px rgba(0,0,0,0.05), inset 0 4px 8px rgba(255,255,255,0.8);
  position: relative; overflow: hidden;
}
.rc-eyes { position: absolute; top: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 16px; }
.rc-eye {
  width: 14px; height: 14px; background: #1e293b; border-radius: 50%;
  position: relative; transition: all 0.15s ease;
}
.rc-eye.happy { height: 8px; border-radius: 8px 8px 50% 50%; }
.rc-pupil { position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 6px; height: 6px; background: #1e293b; border-radius: 50%; }
.rc-eye.happy .rc-pupil { display: none; }
.rc-hl { position: absolute; top: 3px; right: 3px; width: 4px; height: 4px; background: white; border-radius: 50%; }
.rc-eye.happy .rc-hl { display: none; }
.rc-mouth {
  position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
  width: 16px; height: 8px; background: #1e293b; border-radius: 0 0 16px 16px;
  transition: all 0.2s ease;
}
.rc-mouth.smile { width: 20px; height: 10px; border-radius: 0 0 20px 20px; }
.rc-cheek { position: absolute; width: 10px; height: 6px; background: rgba(251,113,133,0.5); border-radius: 50%; top: 36px; }
.rc-cheek.left { left: 8px; }
.rc-cheek.right { right: 8px; }

/* 状态 */
.rc-status {
  position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%);
  background: rgba(15,23,42,0.9); padding: 3px 10px; border-radius: 10px; white-space: nowrap;
}
.rc-status-text { font-size: 10px; font-weight: 500; color: #10b981; }
.rc-status.thinking .rc-status-text { color: #f59e0b; }

/* 闲聊气泡 */
.rc-idle-bubble {
  position: absolute; bottom: 20px; left: 85px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  padding: 10px 16px; border-radius: 16px 16px 16px 4px;
  color: white; font-size: 13px; font-weight: 500;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
  cursor: pointer; animation: rc-float 3s ease-in-out infinite;
  white-space: nowrap; max-width: 240px;
}
@keyframes rc-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
.rc-bubble-pop-enter-active { animation: rc-pop-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.rc-bubble-pop-leave-active { animation: rc-pop-out 0.3s ease; }
@keyframes rc-pop-in {
  0% { transform: scale(0) translateY(10px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes rc-pop-out {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0; }
}

/* 面板 */
.rc-panel {
  position: absolute; width: 384px; border-radius: 16px; overflow: hidden;
  background: #0f172a; border: 1px solid rgba(148,163,184,0.2);
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  bottom: 90px; left: 0;
}
.rc-panel-spring-enter-active { animation: rc-panel-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.rc-panel-spring-leave-active { animation: rc-panel-out 0.2s ease-in; }
@keyframes rc-panel-in {
  0% { transform: scale(0.8) translateY(20px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes rc-panel-out {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.9) translateY(10px); opacity: 0; }
}
.rc-panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; background: rgba(30,41,59,0.8);
  border-bottom: 1px solid rgba(148,163,184,0.1);
}
.rc-close-btn {
  width: 28px; height: 28px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #94a3b8; transition: all 0.2s;
}
.rc-close-btn:hover { color: white; background: rgba(51,65,85,0.5); }

/* 对话区 */
.rc-chat-zone { height: 256px; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.rc-chat-msg { display: flex; gap: 8px; }
.rc-chat-msg.user { flex-direction: row-reverse; }
.rc-msg-avatar {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; font-size: 14px;
  background: linear-gradient(135deg, #7c3aed, #06b6d4);
}
.rc-msg-content { max-width: 80%; }
.rc-msg-text { padding: 8px 12px; border-radius: 12px; font-size: 13px; white-space: pre-wrap; }
.rc-chat-msg.assistant .rc-msg-text { background: rgba(30,41,59,0.8); color: #e2e8f0; }
.rc-chat-msg.user .rc-msg-text { background: #7c3aed; color: white; }
.rc-msg-actions { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.rc-action-chip {
  padding: 4px 10px; border-radius: 8px; font-size: 12px; cursor: pointer;
  background: rgba(124,58,237,0.2); color: #a78bfa; transition: background 0.2s;
}
.rc-action-chip:hover { background: rgba(124,58,237,0.3); }
.rc-typing { display: flex; gap: 4px; padding: 4px 0; }
.rc-typing span {
  width: 8px; height: 8px; border-radius: 50%; background: #a78bfa;
  animation: rc-typing-dot 1.4s infinite;
}
.rc-typing span:nth-child(2) { animation-delay: 0.2s; }
.rc-typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes rc-typing-dot {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
  30% { transform: translateY(-3px); opacity: 1; }
}

/* 功能网格 */
.rc-action-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; padding: 0 16px 12px; }
.rc-action-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 4px; padding: 12px; border-radius: 12px; cursor: pointer;
  background: rgba(30,41,59,0.5); border: 1px solid rgba(148,163,184,0.1);
  transition: all 0.2s;
}
.rc-action-card:hover { background: rgba(30,41,59,0.8); border-color: rgba(124,58,237,0.5); }

/* 快捷回复 */
.rc-quick-bar {
  display: flex; flex-wrap: wrap; gap: 8px; padding: 8px 16px;
  border-top: 1px solid rgba(148,163,184,0.1);
}
.rc-quick-btn {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 12px; border-radius: 20px; font-size: 12px;
  color: #cbd5e1; cursor: pointer;
  background: rgba(30,41,59,0.5); border: 1px solid rgba(148,163,184,0.1);
  transition: all 0.2s;
}
.rc-quick-btn:hover { border-color: rgba(124,58,237,0.5); color: #a78bfa; }

/* 输入框 */
.rc-input-bar {
  display: flex; gap: 8px; padding: 12px;
  border-top: 1px solid rgba(148,163,184,0.1);
}
.rc-input-bar input {
  flex: 1; padding: 8px 12px; border-radius: 8px; font-size: 13px;
  color: white; background: rgba(30,41,59,0.5);
  border: 1px solid rgba(148,163,184,0.1); outline: none;
}
.rc-input-bar input::placeholder { color: #64748b; }
.rc-input-bar input:focus { border-color: rgba(124,58,237,0.5); }
.rc-send-btn {
  width: 36px; height: 36px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: white; background: #7c3aed; transition: background 0.2s;
}
.rc-send-btn:hover { background: #6d28d9; }
.rc-send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* ===== Light Mode Overrides ===== */
:global(html.light) .rc-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .rc-glow-1,
:global(html.light) .rc-glow-2 {
  opacity: 0.04;
}

:global(html.light) .rc-glow-1 { background: #0891b2; }
:global(html.light) .rc-glow-2 { background: #06b6d4; }

:global(html.light) .rc-header h1 {
  color: #0c4a6e;
}

:global(html.light) .rc-header p {
  color: #64748b;
}

:global(html.light) .rc-stat-value {
  color: #0891b2;
}

:global(html.light) .rc-stat-label {
  color: #64748b;
}

:global(html.light) .rc-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .rc-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .rc-name {
  color: #0c4a6e;
}

:global(html.light) .rc-meta {
  color: #64748b;
}

:global(html.light) .rc-score {
  color: #0891b2;
}

:global(html.light) .rc-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .rc-action-card {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .rc-action-card:hover {
  background: rgba(8, 145, 178, 0.1);
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .rc-action-card i {
  color: #0891b2;
}

:global(html.light) .rc-action-card span {
  color: #64748b;
}

:global(html.light) .rc-quick-bar {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .rc-quick-btn {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.1);
  color: #64748b;
}

:global(html.light) .rc-quick-btn:hover {
  border-color: rgba(8, 145, 178, 0.3);
  color: #0891b2;
}

:global(html.light) .rc-input-bar {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .rc-input-bar input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .rc-input-bar input::placeholder {
  color: #94a3b8;
}

:global(html.light) .rc-input-bar input:focus {
  border-color: rgba(8, 145, 178, 0.4);
}

:global(html.light) .rc-send-btn {
  background: #0891b2;
}

:global(html.light) .rc-send-btn:hover {
  background: #0e7490;
}

:global(html.light) .empty-state {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .empty-state h3 {
  color: #0c4a6e;
}

:global(html.light) .empty-state p {
  color: #64748b;
}
</style>
