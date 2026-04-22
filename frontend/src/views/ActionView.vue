<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">

      <!-- ═══ Page Header ═══ -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-check-square-fill text-emerald-400"></i> 行动管理
          </h1>
          <p class="text-sm text-brand-muted mt-1">将职业规划拆解为可执行任务，从"想法"变成"行动"</p>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-brand-muted">{{ taskStats.done }}/{{ taskStats.total }} 完成 · <span class="text-violet-400 font-medium">{{ taskStats.rate }}%</span></span>
          <button @click="showAddModal = true" class="btn-primary text-sm">+ 新建任务</button>
        </div>
      </div>

      <!-- ═══ Category Tabs ═══ -->
      <div class="flex gap-1 mb-8 overflow-x-auto pb-1">
        <button
          v-for="cat in filterTabs" :key="cat.value"
          @click="activeCategory = cat.value"
          :class="[
            'flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm whitespace-nowrap transition-all',
            activeCategory === cat.value
              ? 'bg-violet-600/20 text-violet-300 border border-violet-500/30'
              : 'text-brand-muted hover:text-brand-text hover:bg-brand-surface'
          ]"
        >
          <i :class="cat.icon" class="text-xs"></i>
          {{ cat.label }}（{{ getCategoryCount(cat.value) }}）
        </button>
      </div>

      <!-- ═══ Empty State ═══ -->
      <div v-if="filteredTasks.length === 0 && taskStats.total === 0" class="flex flex-col items-center justify-center py-28">
        <div class="w-16 h-16 rounded-2xl bg-brand-surface flex items-center justify-center mb-6">
          <i class="bi bi-clipboard-check text-3xl text-brand-muted"></i>
        </div>
        <h2 class="text-lg font-semibold text-brand-text mb-2">还没有任务</h2>
        <p class="text-brand-muted text-sm mb-8 text-center max-w-sm">
          你可以手动创建任务，或者根据职业规划自动导入
        </p>
        <div class="flex gap-3">
          <button @click="showAddModal = true" class="btn-primary text-sm">+ 手动创建</button>
          <button @click="importFromRoadmap" class="btn-secondary text-sm flex items-center gap-2">
            <i class="bi bi-clipboard-data"></i> 从规划导入
          </button>
        </div>
      </div>

      <!-- ═══ Task Columns ═══ -->
      <template v-else>
        <!-- Quick Import Bar -->
        <div class="flex flex-wrap gap-3 mb-6" v-if="taskStats.total > 0">
          <button @click="importFromRoadmap" class="btn-ghost text-xs"><i class="bi bi-signpost-split mr-1"></i>从路线图导入</button>
          <button @click="importFromGaps" class="btn-ghost text-xs"><i class="bi bi-graph-down mr-1"></i>从技能差距导入</button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Todo Column -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-3 h-3 rounded-full bg-slate-500"></div>
              <h3 class="font-medium text-brand-text">待开始</h3>
              <span class="text-xs text-brand-muted">({{ todoTasks.length }})</span>
            </div>
            <TransitionGroup name="list" tag="div" class="space-y-3">
              <div v-for="task in todoTasks" :key="task.id" class="bg-brand-card border border-brand-border rounded-xl p-4">
                <div class="flex items-start justify-between mb-2">
                  <span :class="['text-xs px-2 py-0.5 rounded', categoryClass(task.category)]">{{ categoryLabel(task.category) }}</span>
                  <button @click="deleteTask(task.id)" class="text-brand-muted hover:text-red-400"><i class="bi bi-trash text-sm"></i></button>
                </div>
                <h4 class="font-medium text-brand-text mb-2">{{ task.title }}</h4>
                <div v-if="task.relatedSkill" class="flex items-center gap-1 text-xs text-brand-muted mb-3">
                  <i class="bi bi-link-45deg"></i><span>{{ task.relatedSkill }}</span>
                </div>
                <button @click="updateStatus(task.id, 'doing')" class="w-full py-2 rounded-lg text-sm bg-brand-surface text-brand-muted hover:bg-violet-600 hover:text-white transition-all">开始任务</button>
              </div>
            </TransitionGroup>
            <div v-if="todoTasks.length === 0" class="text-center py-8 text-brand-muted">
              <i class="bi bi-inbox text-2xl mb-2 block opacity-50"></i>
              <p class="text-xs">暂无待开始任务</p>
            </div>
          </div>

          <!-- Doing Column -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-3 h-3 rounded-full bg-amber-500"></div>
              <h3 class="font-medium text-brand-text">进行中</h3>
              <span class="text-xs text-brand-muted">({{ doingTasks.length }})</span>
            </div>
            <TransitionGroup name="list" tag="div" class="space-y-3">
              <div v-for="task in doingTasks" :key="task.id" class="bg-brand-card border border-amber-500/30 rounded-xl p-4">
                <div class="flex items-start justify-between mb-2">
                  <span :class="['text-xs px-2 py-0.5 rounded', categoryClass(task.category)]">{{ categoryLabel(task.category) }}</span>
                  <button @click="deleteTask(task.id)" class="text-brand-muted hover:text-red-400"><i class="bi bi-trash text-sm"></i></button>
                </div>
                <h4 class="font-medium text-brand-text mb-2">{{ task.title }}</h4>
                <div class="flex gap-2">
                  <button @click="updateStatus(task.id, 'todo')" class="flex-1 py-2 rounded-lg text-sm bg-brand-surface text-brand-muted hover:bg-slate-600 transition-all">暂停</button>
                  <button @click="updateStatus(task.id, 'done')" class="flex-1 py-2 rounded-lg text-sm bg-emerald-600 text-white hover:bg-emerald-500 transition-all">完成</button>
                </div>
              </div>
            </TransitionGroup>
            <div v-if="doingTasks.length === 0" class="text-center py-8 text-brand-muted">
              <i class="bi bi-hourglass text-2xl mb-2 block opacity-50"></i>
              <p class="text-xs">暂无进行中任务</p>
            </div>
          </div>

          <!-- Done Column -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
              <h3 class="font-medium text-brand-text">已完成</h3>
              <span class="text-xs text-brand-muted">({{ doneTasks.length }})</span>
            </div>
            <TransitionGroup name="list" tag="div" class="space-y-3">
              <div v-for="task in doneTasks" :key="task.id" class="bg-brand-card border border-emerald-500/20 rounded-xl p-4 opacity-75">
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span :class="['text-xs px-2 py-0.5 rounded', categoryClass(task.category)]">{{ categoryLabel(task.category) }}</span>
                    <i class="bi bi-check-circle-fill text-emerald-400"></i>
                  </div>
                  <button @click="deleteTask(task.id)" class="text-brand-muted hover:text-red-400"><i class="bi bi-trash text-sm"></i></button>
                </div>
                <h4 class="font-medium text-brand-text line-through opacity-75">{{ task.title }}</h4>
                <button @click="updateStatus(task.id, 'doing')" class="mt-3 w-full py-2 rounded-lg text-sm bg-brand-surface text-brand-muted hover:bg-violet-600 hover:text-white transition-all">重新开始</button>
              </div>
            </TransitionGroup>
            <div v-if="doneTasks.length === 0" class="text-center py-8 text-brand-muted">
              <i class="bi bi-trophy text-2xl mb-2 block opacity-50"></i>
              <p class="text-xs">暂无已完成任务</p>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- ═══ Add Task Modal ═══ -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showAddModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showAddModal = false">
          <div class="bg-brand-card border border-brand-border rounded-2xl w-full max-w-lg p-6">
            <h3 class="text-lg font-semibold text-brand-text mb-4">添加任务</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm text-brand-muted mb-2">任务标题</label>
                <input v-model="newTask.title" class="input-base" placeholder="如：完成Vue3官方教程">
              </div>
              <div>
                <label class="block text-sm text-brand-muted mb-2">任务分类</label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="cat in taskCategories" :key="cat.value" @click="newTask.category = cat.value"
                    :class="['px-3 py-2 rounded-lg text-sm transition-all', newTask.category === cat.value ? 'bg-violet-600 text-white' : 'bg-brand-surface text-brand-muted border border-brand-border']">
                    <i :class="cat.icon" class="mr-1"></i>{{ cat.label }}
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-sm text-brand-muted mb-2">关联技能（可选）</label>
                <input v-model="newTask.relatedSkill" class="input-base" placeholder="如：TypeScript">
              </div>
              <div>
                <label class="block text-sm text-brand-muted mb-2">资源链接（可选）</label>
                <input v-model="newTask.resourceUrl" class="input-base" placeholder="https://...">
              </div>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="showAddModal = false" class="btn-secondary flex-1">取消</button>
              <button @click="addTask" class="btn-primary flex-1">添加</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useCareerStore, type ActionTask } from '@/stores/careerStore'

const careerStore = useCareerStore()

const showAddModal = ref(false)
const activeCategory = ref('all')

const newTask = reactive({
  title: '',
  category: 'skill' as ActionTask['category'],
  relatedSkill: '',
  resourceUrl: '',
})

const filterTabs = [
  { value: 'all', label: '全部', icon: 'bi bi-grid' },
  { value: 'skill', label: '技能提升', icon: 'bi bi-lightning' },
  { value: 'job', label: '求职', icon: 'bi bi-briefcase' },
  { value: 'interview', label: '面试准备', icon: 'bi bi-chat-dots' },
  { value: 'project', label: '项目实践', icon: 'bi bi-rocket' },
]

const taskCategories = [
  { value: 'skill', label: '技能学习', icon: 'bi bi-book' },
  { value: 'project', label: '项目实战', icon: 'bi bi-code-slash' },
  { value: 'job', label: '求职准备', icon: 'bi bi-briefcase' },
  { value: 'interview', label: '面试复习', icon: 'bi bi-chat-dots' },
]

const taskStats = computed(() => careerStore.taskStats)

const getCategoryCount = (cat: string) => {
  if (cat === 'all') return careerStore.actionTasks.length
  return careerStore.actionTasks.filter(t => t.category === cat).length
}

const filteredTasks = computed(() => {
  if (activeCategory.value === 'all') return careerStore.actionTasks
  return careerStore.actionTasks.filter(t => t.category === activeCategory.value)
})

const todoTasks = computed(() => filteredTasks.value.filter(t => t.status === 'todo'))
const doingTasks = computed(() => filteredTasks.value.filter(t => t.status === 'doing'))
const doneTasks = computed(() => filteredTasks.value.filter(t => t.status === 'done'))

const categoryClass = (cat: string) => {
  const map: Record<string, string> = {
    skill: 'bg-violet-500/10 text-violet-400',
    project: 'bg-emerald-500/10 text-emerald-400',
    job: 'bg-amber-500/10 text-amber-400',
    interview: 'bg-cyan-500/10 text-cyan-400',
  }
  return map[cat] || 'bg-slate-500/10 text-slate-400'
}

const categoryLabel = (cat: string) => {
  const map: Record<string, string> = { skill: '技能', project: '项目', job: '求职', interview: '面试' }
  return map[cat] || cat
}

const addTask = () => {
  if (!newTask.title) return
  careerStore.addTask({
    title: newTask.title,
    category: newTask.category,
    source: 'manual',
    status: 'todo',
    relatedSkill: newTask.relatedSkill || undefined,
    resourceUrl: newTask.resourceUrl || undefined,
  })
  Object.assign(newTask, { title: '', category: 'skill', relatedSkill: '', resourceUrl: '' })
  showAddModal.value = false
}

const updateStatus = (id: string, status: ActionTask['status']) => { careerStore.updateTaskStatus(id, status) }
const deleteTask = (id: string) => { const idx = careerStore.actionTasks.findIndex(t => t.id === id); if (idx >= 0) careerStore.actionTasks.splice(idx, 1) }
const importFromRoadmap = () => { careerStore.importTasksFromRoadmap() }
const importFromGaps = () => { careerStore.importTasksFromGaps() }
</script>

<style scoped>
.list-enter-active, .list-leave-active { transition: all 0.3s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(20px); }
.list-move { transition: transform 0.3s ease; }
</style>
