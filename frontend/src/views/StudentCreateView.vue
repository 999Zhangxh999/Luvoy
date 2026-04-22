<template>
  <main class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-100 mb-2">
          <i class="bi bi-magic text-violet-400 mr-3"></i>
          智能 <span class="gradient-text">问卷建档</span>
        </h1>
        <p class="text-slate-400">
          像做人格测试一样完成档案，系统会自动生成可编辑的简历草稿
        </p>
      </div>

      <!-- Steps Bar -->
      <div class="flex items-center justify-center mb-10">
        <template v-for="(s, idx) in stepsMeta" :key="s.step">
          <div class="flex flex-col items-center relative z-10">
            <div 
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300',
                step > s.step ? 'bg-emerald-500 text-white' :
                step === s.step ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white shadow-lg shadow-violet-500/30' :
                'bg-slate-800 border-2 border-slate-700 text-slate-500'
              ]"
            >
              <i v-if="step > s.step" class="bi bi-check"></i>
              <span v-else>{{ s.step }}</span>
            </div>
            <span 
              :class="[
                'text-xs mt-2 font-medium transition-colors',
                step >= s.step ? 'text-slate-200' : 'text-slate-500'
              ]"
            >
              {{ s.label }}
            </span>
          </div>
          <div 
            v-if="idx < stepsMeta.length - 1"
            :class="[
              'flex-1 h-0.5 mx-3 mb-6 transition-colors',
              step > s.step ? 'bg-emerald-500' : 'bg-slate-700'
            ]"
          ></div>
        </template>
      </div>

      <form @submit.prevent="submit">
        <!-- Step 1: Basic Info -->
        <div v-show="step === 1" class="card">
          <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700">
            <div class="w-10 h-10 rounded-xl bg-violet-500/20 flex items-center justify-center">
              <i class="bi bi-person text-violet-400 text-lg"></i>
            </div>
            <div>
              <h2 class="font-semibold text-slate-100">基础信息</h2>
              <p class="text-sm text-slate-400">填写你的个人基本信息</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">
                姓名 <span class="text-red-400">*</span>
              </label>
              <input v-model="form.name" class="input-base" required placeholder="张三" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">性别</label>
              <select v-model="form.gender" class="input-base">
                <option value="">请选择</option>
                <option>男</option>
                <option>女</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">年龄</label>
              <input v-model.number="form.age" type="number" class="input-base" placeholder="22" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-300 mb-2">学校</label>
              <input v-model="form.school" class="input-base" placeholder="XX大学" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">学历</label>
              <select v-model="form.education" class="input-base">
                <option value="">请选择</option>
                <option>专科</option>
                <option>本科</option>
                <option>硕士</option>
                <option>博士</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-300 mb-2">专业</label>
              <input v-model="form.major" class="input-base" placeholder="计算机科学与技术" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">毕业年份</label>
              <input v-model.number="form.graduation_year" type="number" class="input-base" placeholder="2025" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">期望薪资</label>
              <input v-model="form.salary_expectation" class="input-base" placeholder="8000-12000" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">邮箱</label>
              <input v-model="form.email" type="email" class="input-base" placeholder="name@example.com" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-2">电话</label>
              <input v-model="form.phone" class="input-base" placeholder="138xxxx" />
            </div>
          </div>
        </div>

        <!-- Step 2: Career Quiz -->
        <div v-show="step === 2" class="card">
          <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700">
            <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
              <i class="bi bi-ui-checks-grid text-cyan-400 text-lg"></i>
            </div>
            <div>
              <h2 class="font-semibold text-slate-100">职业人格问卷</h2>
              <p class="text-sm text-slate-400">选择最符合你的选项，系统会自动推断目标岗位</p>
            </div>
          </div>

          <div class="space-y-6">
            <div v-for="q in quizQuestions" :key="q.key" class="p-4 rounded-xl border border-slate-700 bg-slate-800/30">
              <h3 class="font-medium text-slate-200 mb-4">{{ q.title }}</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button
                  v-for="opt in q.options"
                  :key="opt.value"
                  type="button"
                  @click="quizAnswers[q.key] = opt.value"
                  :class="[
                    'p-4 rounded-xl border text-left transition-all duration-200',
                    quizAnswers[q.key] === opt.value 
                      ? 'border-violet-500 bg-violet-500/10 ring-1 ring-violet-500/50' 
                      : 'border-slate-700 bg-slate-800/50 hover:border-slate-600'
                  ]"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <i :class="[opt.icon, quizAnswers[q.key] === opt.value ? 'text-violet-400' : 'text-slate-400']"></i>
                    <span :class="['font-medium', quizAnswers[q.key] === opt.value ? 'text-violet-300' : 'text-slate-200']">
                      {{ opt.label }}
                    </span>
                  </div>
                  <p class="text-xs text-slate-500">{{ opt.desc }}</p>
                </button>
              </div>
            </div>
          </div>

          <!-- Progress & Insights -->
          <div class="mt-6 p-4 rounded-xl border border-slate-700 bg-gradient-to-br from-violet-500/5 to-cyan-500/5">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-medium text-slate-300">
                <i class="bi bi-activity mr-2 text-violet-400"></i>问卷完成进度
              </span>
              <span class="text-sm font-bold text-violet-400">{{ quizCompletion }}/{{ quizQuestions.length }}</span>
            </div>
            <div class="h-2 bg-slate-700 rounded-full overflow-hidden mb-4">
              <div 
                class="h-full bg-gradient-to-r from-violet-600 to-cyan-500 transition-all duration-300"
                :style="{ width: quizProgress + '%' }"
              ></div>
            </div>
            <div>
              <span class="text-sm font-medium text-slate-300 block mb-2">系统推断岗位方向</span>
              <div class="flex flex-wrap gap-2">
                <span v-for="p in inferredPositions" :key="p" class="badge">{{ p }}</span>
                <span v-if="!inferredPositions.length" class="text-sm text-slate-500">先完成2题后显示建议</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Resume -->
        <div v-show="step === 3" class="card">
          <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700">
            <div class="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center">
              <i class="bi bi-file-earmark-richtext text-pink-400 text-lg"></i>
            </div>
            <div>
              <h2 class="font-semibold text-slate-100">简历补充</h2>
              <p class="text-sm text-slate-400">选择方式提交简历内容</p>
            </div>
          </div>

          <!-- Tab Buttons -->
          <div class="flex gap-2 mb-6">
            <button
              v-for="t in tabs"
              :key="t.key"
              type="button"
              @click="tab = t.key"
              :class="[
                'flex-1 py-3 px-4 rounded-xl border text-sm font-medium transition-all flex items-center justify-center gap-2',
                tab === t.key 
                  ? 'border-violet-500 bg-violet-500/10 text-violet-300' 
                  : 'border-slate-700 text-slate-400 hover:border-slate-600'
              ]"
            >
              <i :class="t.icon"></i>
              {{ t.label }}
            </button>
          </div>

          <!-- File Upload -->
          <div v-if="tab === 'file'">
            <div 
              class="border-2 border-dashed border-slate-700 rounded-xl p-10 text-center cursor-pointer hover:border-violet-500/50 hover:bg-violet-500/5 transition-all"
              @click="$refs.fileInput.click()"
              @dragover.prevent
              @drop.prevent="onDrop"
            >
              <i class="bi bi-cloud-arrow-up text-4xl text-violet-400 mb-3 block"></i>
              <p v-if="!resumeFile" class="text-slate-300 mb-1">点击选择文件或拖拽到此处</p>
              <p v-else class="text-emerald-400 font-semibold mb-1">
                <i class="bi bi-check-circle mr-2"></i>{{ resumeFile.name }}
              </p>
              <small class="text-slate-500">支持 PDF / Word / TXT</small>
            </div>
            <input ref="fileInput" type="file" class="hidden" accept=".pdf,.docx,.txt" @change="onFile" />
          </div>

          <!-- Text Input -->
          <div v-else>
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm font-medium text-slate-300">简历文本</label>
              <button 
                v-if="tab === 'quiz'" 
                type="button" 
                @click="applyQuizDraft"
                class="text-xs text-violet-400 hover:text-violet-300 flex items-center gap-1"
              >
                <i class="bi bi-arrow-clockwise"></i>
                重新生成草稿
              </button>
            </div>
            <textarea
              v-model="form.resume_text"
              class="input-base min-h-[260px] resize-none"
              placeholder="在此粘贴或编辑简历内容..."
            ></textarea>
          </div>
        </div>

        <!-- Step 4: Confirm -->
        <div v-show="step === 4" class="card">
          <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center">
              <i class="bi bi-check2-square text-emerald-400 text-lg"></i>
            </div>
            <div>
              <h2 class="font-semibold text-slate-100">确认与创建</h2>
              <p class="text-sm text-slate-400">检查信息并完成创建</p>
            </div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <div class="p-3 rounded-xl border border-slate-700 bg-slate-800/30">
              <span class="block text-xs text-slate-500 mb-1">姓名</span>
              <span class="font-medium text-slate-200">{{ form.name || '-' }}</span>
            </div>
            <div class="p-3 rounded-xl border border-slate-700 bg-slate-800/30">
              <span class="block text-xs text-slate-500 mb-1">专业</span>
              <span class="font-medium text-slate-200">{{ form.major || '-' }}</span>
            </div>
            <div class="p-3 rounded-xl border border-slate-700 bg-slate-800/30">
              <span class="block text-xs text-slate-500 mb-1">目标岗位</span>
              <span class="font-medium text-slate-200 text-sm">{{ form.target_positions || '-' }}</span>
            </div>
            <div class="p-3 rounded-xl border border-slate-700 bg-slate-800/30">
              <span class="block text-xs text-slate-500 mb-1">问卷完成</span>
              <span class="font-medium text-violet-400">{{ quizCompletion }}/{{ quizQuestions.length }}</span>
            </div>
          </div>

          <label class="flex items-start gap-3 p-4 rounded-xl border border-slate-700 bg-slate-800/30 cursor-pointer hover:border-slate-600 transition-colors">
            <input 
              v-model="autoPipeline" 
              type="checkbox"
              class="w-5 h-5 rounded border-slate-600 bg-slate-800 text-violet-500 focus:ring-violet-500/30 mt-0.5"
            />
            <div>
              <span class="font-medium text-slate-200 block">创建后自动执行完整流程</span>
              <span class="text-sm text-slate-400">生成画像 → 人岗匹配 → 生成报告（耗时更久但可直接查看结果）</span>
            </div>
          </label>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex justify-between mt-8">
          <button 
            v-if="step > 1" 
            type="button" 
            @click="step--"
            class="px-6 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 transition-colors"
          >
            <i class="bi bi-arrow-left mr-2"></i>上一步
          </button>
          <div v-else></div>

          <div class="flex gap-3">
            <router-link 
              to="/students" 
              class="px-6 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 transition-colors"
            >
              取消
            </router-link>
            <button 
              v-if="step < 4" 
              type="button" 
              @click="nextStep"
              class="btn-primary"
            >
              下一步 <i class="bi bi-arrow-right ml-2"></i>
            </button>
            <button 
              v-else 
              type="submit" 
              :disabled="submitting"
              class="btn-primary bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500"
            >
              <i class="bi bi-check-circle mr-2"></i>
              {{ submitting ? '处理中...' : '创建完整档案' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </main>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createStudent, generateReport, generateStudentProfile, runMatching } from '@/api'

const router = useRouter()
const setLoading = inject('setLoading')
const toast = inject('toast')

const step = ref(1)
const tab = ref('quiz')
const submitting = ref(false)
const resumeFile = ref(null)
const autoPipeline = ref(true)

const form = ref({
  name: '',
  gender: '',
  age: '',
  school: '',
  major: '',
  education: '',
  graduation_year: '',
  salary_expectation: '',
  email: '',
  phone: '',
  target_positions: '',
  target_cities: '',
  career_preference: '',
  resume_text: '',
})

const stepsMeta = [
  { step: 1, label: '基础信息' },
  { step: 2, label: '职业问卷' },
  { step: 3, label: '简历补充' },
  { step: 4, label: '确认创建' },
]

const tabs = [
  { key: 'quiz', label: '问卷草稿', icon: 'bi bi-stars' },
  { key: 'file', label: '上传文件', icon: 'bi bi-cloud-upload' },
  { key: 'text', label: '手动输入', icon: 'bi bi-pencil-square' },
]

const quizQuestions = [
  {
    key: 'work_style',
    title: '1. 你更喜欢哪种工作方式？',
    options: [
      { value: 'logic', label: '结构化解决问题', desc: '偏分析与系统设计', icon: 'bi bi-diagram-2' },
      { value: 'creative', label: '创意驱动产出', desc: '偏产品与内容创新', icon: 'bi bi-lightbulb' },
      { value: 'execute', label: '推进执行落地', desc: '偏项目推进与运营', icon: 'bi bi-lightning-charge' },
      { value: 'service', label: '沟通协同服务', desc: '偏客户与团队支持', icon: 'bi bi-people' },
    ],
  },
  {
    key: 'interest_field',
    title: '2. 你最感兴趣的方向是？',
    options: [
      { value: 'dev', label: '软件开发', desc: '前后端、工程化、架构', icon: 'bi bi-code-square' },
      { value: 'data', label: '数据与AI', desc: '数据分析、算法、建模', icon: 'bi bi-bar-chart' },
      { value: 'product', label: '产品与运营', desc: '产品设计、增长、策略', icon: 'bi bi-kanban' },
      { value: 'business', label: '业务与市场', desc: '销售、咨询、项目交付', icon: 'bi bi-briefcase' },
    ],
  },
  {
    key: 'team_role',
    title: '3. 团队里你更像哪种角色？',
    options: [
      { value: 'planner', label: '规划者', desc: '制定目标和路径', icon: 'bi bi-signpost' },
      { value: 'builder', label: '搭建者', desc: '快速产出可用方案', icon: 'bi bi-hammer' },
      { value: 'connector', label: '连接者', desc: '跨团队沟通协作', icon: 'bi bi-diagram-3' },
      { value: 'reviewer', label: '优化者', desc: '质量把控与复盘', icon: 'bi bi-clipboard-check' },
    ],
  },
  {
    key: 'growth_focus',
    title: '4. 未来1-2年你最想提升？',
    options: [
      { value: 'depth', label: '专业深度', desc: '成为技术/业务专家', icon: 'bi bi-bullseye' },
      { value: 'breadth', label: '综合能力', desc: '跨领域协同与统筹', icon: 'bi bi-grid-3x3-gap' },
      { value: 'leadership', label: '带团队能力', desc: '组织协调与管理', icon: 'bi bi-people-fill' },
      { value: 'impact', label: '业务影响力', desc: '直接推动结果增长', icon: 'bi bi-graph-up-arrow' },
    ],
  },
]

const quizAnswers = ref({
  work_style: '',
  interest_field: '',
  team_role: '',
  growth_focus: '',
})

const quizCompletion = computed(() => Object.values(quizAnswers.value).filter(Boolean).length)
const quizProgress = computed(() => (quizCompletion.value / quizQuestions.length) * 100)

const answerTextMap = {
  work_style: {
    logic: '结构化解决问题',
    creative: '创意驱动产出',
    execute: '推进执行落地',
    service: '沟通协同服务',
  },
  interest_field: {
    dev: '软件开发',
    data: '数据与AI',
    product: '产品与运营',
    business: '业务与市场',
  },
  team_role: {
    planner: '规划者',
    builder: '搭建者',
    connector: '连接者',
    reviewer: '优化者',
  },
  growth_focus: {
    depth: '专业深度',
    breadth: '综合能力',
    leadership: '带团队能力',
    impact: '业务影响力',
  },
}

function answerText(key) {
  const value = quizAnswers.value[key]
  return answerTextMap[key]?.[value] || '待补充'
}

const inferredPositions = computed(() => {
  const mapping = {
    logic: ['后端开发工程师', '算法工程师'],
    creative: ['产品经理', '内容运营'],
    execute: ['项目运营专员', '实施顾问'],
    service: ['客户成功经理', '人力资源专员'],
    dev: ['前端开发工程师', '后端开发工程师'],
    data: ['数据分析师', 'AI应用工程师'],
    product: ['产品经理', '增长运营'],
    business: ['咨询顾问', '销售运营'],
  }

  const tags = []
  Object.values(quizAnswers.value).forEach((v) => {
    if (mapping[v]) tags.push(...mapping[v])
  })
  return [...new Set(tags)].slice(0, 4)
})

function applyQuizDraft() {
  if (!form.value.target_positions && inferredPositions.value.length) {
    form.value.target_positions = inferredPositions.value.slice(0, 3).join(', ')
  }

  const preferenceLines = [
    `工作风格: ${answerText('work_style')}`,
    `兴趣方向: ${answerText('interest_field')}`,
    `团队角色: ${answerText('team_role')}`,
    `成长重点: ${answerText('growth_focus')}`,
  ]
  form.value.career_preference = preferenceLines.join('；')

  const resumeParts = [
    `${form.value.name || '候选人'}，${form.value.education || '学历待补充'}，${form.value.school || '院校待补充'} ${form.value.major || '专业待补充'}。`,
    `职业兴趣倾向于${answerText('interest_field')}，偏好${answerText('work_style')}型工作方式。`,
    `在团队中更擅长担任${answerText('team_role')}，未来成长重点为${answerText('growth_focus')}。`,
    `目标岗位: ${form.value.target_positions || '待补充'}。`,
    '可补充经历: 请填写项目经历/实习经历/获奖证书等，系统将自动用于画像与匹配分析。',
  ]
  form.value.resume_text = resumeParts.join('\n')
}

function onFile(e) {
  resumeFile.value = e.target.files[0] || null
}

function onDrop(e) {
  resumeFile.value = e.dataTransfer.files[0] || null
}

function validateStep() {
  if (step.value === 1 && !form.value.name) {
    toast('请输入姓名', 'warning')
    return false
  }
  if (step.value === 2 && quizCompletion.value < 2) {
    toast('至少完成2道问卷后再继续', 'warning')
    return false
  }
  if (step.value === 3 && tab.value !== 'file' && !form.value.resume_text?.trim()) {
    toast('请填写或生成简历文本', 'warning')
    return false
  }
  return true
}

function nextStep() {
  if (!validateStep()) return
  if (step.value === 2 && !form.value.resume_text) {
    applyQuizDraft()
  }
  step.value += 1
}

async function submit() {
  if (!form.value.name) {
    toast('请输入姓名', 'warning')
    return
  }
  submitting.value = true
  setLoading(true, autoPipeline.value ? '正在创建并执行完整智能流程...' : '正在创建学生档案并解析简历...')
  try {
    const fd = new FormData()
    for (const [k, v] of Object.entries(form.value)) {
      if (v !== '' && v !== null) fd.append(k, v)
    }
    if (resumeFile.value) fd.append('resume_file', resumeFile.value)

    const { data } = await createStudent(fd)
    if (!data.success) {
      toast(data.message || '创建失败', 'danger')
      return
    }

    const sid = data.data.id
    if (data.warning) {
      toast(data.warning, 'warning')
    }

    if (autoPipeline.value) {
      await generateStudentProfile(sid)
      await runMatching(sid, 5)
      await generateReport(sid)
      toast('建档完成，画像/匹配/报告已自动生成', 'success')
    } else {
      toast('学生档案创建成功', 'success')
    }

    router.push(`/students/${sid}`)
  } catch (e) {
    toast(e.response?.data?.message || '创建失败', 'danger')
  } finally {
    submitting.value = false
    setLoading(false)
  }
}
</script>
