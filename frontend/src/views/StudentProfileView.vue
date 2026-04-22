<template>
  <main v-if="student" class="min-h-screen py-20 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <router-link 
          to="/students" 
          class="w-10 h-10 rounded-xl border border-slate-700 flex items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
        >
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500 flex items-center justify-center text-white text-lg font-bold">
            {{ student.name?.[0] }}
          </div>
          <div>
            <h1 class="text-2xl font-bold text-slate-100">{{ student.name }} <span class="text-slate-400 font-normal">的档案</span></h1>
            <p class="text-sm text-slate-400">{{ student.school }} · {{ student.major }}</p>
          </div>
        </div>
      </div>

      <!-- Basic Info Card -->
      <div class="card mb-6">
        <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
          <div class="w-10 h-10 rounded-xl bg-violet-500/20 flex items-center justify-center">
            <i class="bi bi-person text-violet-400 text-lg"></i>
          </div>
          <h2 class="font-semibold text-slate-100">基本信息</h2>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
            <span class="block text-xs text-slate-500 mb-1">学校</span>
            <span class="font-medium text-slate-200">{{ student.school || '-' }}</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
            <span class="block text-xs text-slate-500 mb-1">专业</span>
            <span class="font-medium text-slate-200">{{ student.major || '-' }}</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
            <span class="block text-xs text-slate-500 mb-1">学历</span>
            <span class="font-medium text-slate-200">{{ student.education || '-' }}</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
            <span class="block text-xs text-slate-500 mb-1">年龄</span>
            <span class="font-medium text-slate-200">{{ student.age || '-' }}</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
            <span class="block text-xs text-slate-500 mb-1">期望薪资</span>
            <span class="font-medium text-slate-200">{{ student.salary_expectation || '-' }}</span>
          </div>
        </div>
        <div v-if="student.target_positions?.length" class="mt-4">
          <span class="text-xs text-slate-500 block mb-2">目标岗位</span>
          <div class="flex flex-wrap gap-2">
            <span v-for="t in student.target_positions" :key="t" class="badge">{{ t }}</span>
          </div>
        </div>
      </div>

      <!-- Career Persona Card -->
      <div v-if="quizInsights.items.length || student.career_preference" class="card mb-6">
        <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-700">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
              <i class="bi bi-stars text-cyan-400 text-lg"></i>
            </div>
            <h2 class="font-semibold text-slate-100">职业人格画像</h2>
          </div>
          <span class="badge-cyan text-xs">问卷引导</span>
        </div>

        <div v-if="quizInsights.items.length" class="grid lg:grid-cols-5 gap-6">
          <div class="lg:col-span-3 space-y-4">
            <div class="grid grid-cols-2 gap-3">
              <div v-for="item in quizInsights.items" :key="item.key" class="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span class="block text-xs text-slate-500 mb-1">{{ item.label }}</span>
                <span class="font-medium text-slate-200">{{ item.value }}</span>
              </div>
            </div>
            <div v-if="personaTags.length" class="flex flex-wrap gap-2">
              <span v-for="tag in personaTags" :key="tag" class="px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <i class="bi bi-lightning-charge mr-1"></i>{{ tag }}
              </span>
            </div>
            <p v-if="personaSummary" class="text-sm text-slate-400 leading-relaxed">{{ personaSummary }}</p>
          </div>
          <div class="lg:col-span-2">
            <div class="p-4 rounded-xl border border-slate-700 bg-gradient-to-br from-cyan-500/5 to-violet-500/5">
              <RadarChart
                :indicators="['分析驱动', '创意表达', '协作沟通', '执行落地', '成长潜力']"
                :series="personaRadarData"
                height="200px"
              />
            </div>
          </div>
        </div>

        <div v-if="student.target_positions?.length" class="mt-4 flex items-center gap-2">
          <span class="text-xs text-slate-500">建议岗位:</span>
          <div class="flex flex-wrap gap-2">
            <span v-for="t in student.target_positions" :key="t" class="badge">{{ t }}</span>
          </div>
        </div>
        <p v-if="!quizInsights.items.length && student.career_preference" class="text-slate-400 text-sm leading-relaxed">
          {{ student.career_preference }}
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-3 mb-6">
        <button @click="genProfile" :disabled="busy" class="btn-primary bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500">
          <i class="bi bi-cpu mr-2"></i>{{ profile ? '重新生成画像' : '生成个人画像' }}
        </button>
        <button @click="doMatch" :disabled="busy || !profile" class="btn-primary bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-500 hover:to-violet-500 disabled:opacity-40">
          <i class="bi bi-link-45deg mr-2"></i>开始匹配
        </button>
        <button @click="genReport" :disabled="busy || !profile" class="btn-primary bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-500 hover:to-rose-500 disabled:opacity-40">
          <i class="bi bi-file-earmark-text mr-2"></i>{{ report ? '重新生成报告' : '生成报告' }}
        </button>
        <router-link v-if="report" :to="`/reports/${student.id}`" class="btn-secondary">
          <i class="bi bi-eye mr-2"></i>查看报告
        </router-link>
      </div>

      <!-- Message Alert -->
      <div v-if="msg" :class="[
        'flex items-center gap-3 p-4 rounded-xl mb-6 border',
        msgOk ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
      ]">
        <i :class="msgOk ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
        <span>{{ msg }}</span>
      </div>

      <!-- Profile Cards -->
      <div v-if="profile" class="grid lg:grid-cols-5 gap-6 mb-6">
        <div class="lg:col-span-3">
          <div class="card">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-violet-500/20 flex items-center justify-center">
                <i class="bi bi-person-badge text-violet-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">能力画像</h2>
            </div>

            <!-- Skills -->
            <div class="mb-5">
              <span class="text-xs text-slate-500 block mb-2">技术技能</span>
              <div class="flex flex-wrap gap-2">
                <span v-for="s in profile.technical_skills" :key="s" class="badge">{{ s }}</span>
                <span v-if="!profile.technical_skills?.length" class="text-sm text-slate-500">暂无</span>
              </div>
            </div>
            <div class="mb-5">
              <span class="text-xs text-slate-500 block mb-2">资格证书</span>
              <div class="flex flex-wrap gap-2">
                <span v-for="c in profile.certificates" :key="c" class="px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{{ c }}</span>
                <span v-if="!profile.certificates?.length" class="text-sm text-slate-500">暂无</span>
              </div>
            </div>

            <!-- Progress Bars -->
            <div class="grid grid-cols-2 gap-4 mb-5">
              <div>
                <div class="flex justify-between text-xs mb-2">
                  <span class="text-slate-500">完整度</span>
                  <span class="text-violet-400 font-semibold">{{ profile.completeness_score?.toFixed(0) }}%</span>
                </div>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-violet-600 to-cyan-500" :style="{ width: profile.completeness_score + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs mb-2">
                  <span class="text-slate-500">竞争力</span>
                  <span class="text-amber-400 font-semibold">{{ profile.competitiveness_score?.toFixed(0) }}%</span>
                </div>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-amber-500 to-orange-500" :style="{ width: profile.competitiveness_score + '%' }"></div>
                </div>
              </div>
            </div>

            <!-- Evaluation -->
            <div v-if="profile.overall_evaluation" class="mb-5">
              <span class="text-xs text-slate-500 block mb-2">综合评价</span>
              <p class="text-sm text-slate-300 leading-relaxed">{{ profile.overall_evaluation }}</p>
            </div>

            <!-- Strengths & Weaknesses -->
            <div class="grid md:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                <span class="text-xs text-emerald-400 font-medium block mb-2">
                  <i class="bi bi-check-circle mr-1"></i>优势
                </span>
                <ul class="space-y-1">
                  <li v-for="s in profile.strengths" :key="s" class="text-sm text-slate-300">• {{ s }}</li>
                </ul>
              </div>
              <div class="p-4 rounded-xl bg-red-500/5 border border-red-500/20">
                <span class="text-xs text-red-400 font-medium block mb-2">
                  <i class="bi bi-exclamation-circle mr-1"></i>不足
                </span>
                <ul class="space-y-1">
                  <li v-for="w in profile.weaknesses" :key="w" class="text-sm text-slate-300">• {{ w }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Radar Chart -->
        <div class="lg:col-span-2">
          <div class="card sticky top-24">
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-700">
              <div class="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                <i class="bi bi-radar text-cyan-400 text-lg"></i>
              </div>
              <h2 class="font-semibold text-slate-100">六维能力雷达图</h2>
            </div>
            <RadarChart :series="radarData" height="280px" />
          </div>
        </div>
      </div>

      <!-- Match Results -->
      <div v-if="matches.length" class="card">
        <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-700">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center">
              <i class="bi bi-link-45deg text-pink-400 text-lg"></i>
            </div>
            <h2 class="font-semibold text-slate-100">人岗匹配结果</h2>
          </div>
          <span class="badge">{{ matches.length }} 个岗位</span>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="m in matches" 
            :key="m.id"
            class="p-5 rounded-xl border border-slate-700 bg-slate-800/30 hover:border-slate-600 transition-all"
          >
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-slate-100">{{ m.job_name }}</h3>
                <span class="text-xs text-slate-500">{{ m.job_category }}</span>
              </div>
              <div class="text-right">
                <div :class="[
                  'text-2xl font-bold',
                  m.overall_score >= 80 ? 'text-emerald-400' :
                  m.overall_score >= 60 ? 'text-violet-400' : 'text-amber-400'
                ]">
                  {{ m.overall_score?.toFixed(1) }}
                </div>
                <span class="text-xs text-slate-500">综合得分</span>
              </div>
            </div>
            <div class="space-y-2">
              <div v-for="d in dims(m)" :key="d.label" class="flex items-center gap-2">
                <span class="text-xs text-slate-500 w-8">{{ d.label }}</span>
                <div class="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div class="h-full rounded-full" :style="{ width: d.value+'%', background: d.color }"></div>
                </div>
                <span class="text-xs text-slate-400 w-8 text-right">{{ d.value?.toFixed(0) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getStudentDetail, generateStudentProfile, runMatching, generateReport } from '@/api'
import RadarChart from '@/components/RadarChart.vue'

const route = useRoute()
const setLoading = inject('setLoading')
const toast = inject('toast')

const student = ref(null)
const profile = ref(null)
const matches = ref([])
const report = ref(null)
const busy = ref(false)
const msg = ref('')
const msgOk = ref(true)

const radarData = computed(() => {
  if (!profile.value) return []
  const p = profile.value
  return [{
    name: student.value?.name || '',
    values: [p.innovation_ability, p.learning_ability, p.pressure_resistance,
             p.communication_skill, p.teamwork_ability, p.internship_ability],
  }]
})

const quizInsights = computed(() => {
  const raw = student.value?.career_preference || ''
  const labelMap = {
    '工作风格': '工作风格',
    '兴趣方向': '兴趣方向',
    '团队角色': '团队角色',
    '成长重点': '成长重点',
  }

  const items = []
  const re = /(工作风格|兴趣方向|团队角色|成长重点):\s*([^；\n]+)/g
  let m
  while ((m = re.exec(raw)) !== null) {
    items.push({ key: m[1], label: labelMap[m[1]] || m[1], value: m[2].trim() })
  }

  return { items }
})

const personaAxisMap = {
  work_style: {
    '结构化解决问题': [9, 5, 6, 8, 7],
    '创意驱动产出': [5, 9, 6, 7, 7],
    '推进执行落地': [6, 5, 7, 9, 7],
    '沟通协同服务': [5, 6, 9, 7, 7],
  },
  interest_field: {
    '软件开发': [9, 4, 5, 8, 7],
    '数据与AI': [9, 5, 4, 7, 8],
    '产品与运营': [6, 8, 8, 7, 7],
    '业务与市场': [5, 7, 9, 8, 7],
  },
  team_role: {
    '规划者': [8, 6, 7, 7, 8],
    '搭建者': [7, 6, 6, 9, 8],
    '连接者': [6, 7, 9, 7, 7],
    '优化者': [8, 6, 6, 8, 8],
  },
  growth_focus: {
    '专业深度': [9, 5, 5, 7, 8],
    '综合能力': [7, 7, 8, 7, 8],
    '带团队能力': [6, 7, 9, 7, 8],
    '业务影响力': [7, 7, 8, 9, 8],
  },
}

const personaRadarData = computed(() => {
  if (!quizInsights.value.items.length) return []

  const sum = [0, 0, 0, 0, 0]
  let count = 0

  quizInsights.value.items.forEach((item) => {
    const profile = personaAxisMap[item.key]?.[item.value]
    if (!profile) return
    sum.forEach((_, idx) => {
      sum[idx] += profile[idx]
    })
    count += 1
  })

  if (!count) return []
  return [{
    name: '职业人格',
    values: sum.map((v) => Number((v / count).toFixed(1))),
    color: '#0EA5E9',
  }]
})

const personaTags = computed(() => {
  const tags = []
  const vMap = Object.fromEntries(quizInsights.value.items.map((i) => [i.key, i.value]))

  if (vMap.work_style === '结构化解决问题') tags.push('逻辑分析型')
  if (vMap.work_style === '创意驱动产出') tags.push('创意探索型')
  if (vMap.work_style === '推进执行落地') tags.push('行动执行型')
  if (vMap.work_style === '沟通协同服务') tags.push('协同服务型')

  if (vMap.interest_field) tags.push(`${vMap.interest_field}导向`)
  if (vMap.growth_focus) tags.push(`${vMap.growth_focus}成长`)
  return tags.slice(0, 4)
})

const personaSummary = computed(() => {
  if (!quizInsights.value.items.length) return ''
  const vMap = Object.fromEntries(quizInsights.value.items.map((i) => [i.key, i.value]))
  const style = vMap.work_style || '稳定推进'
  const field = vMap.interest_field || '多方向探索'
  const role = vMap.team_role || '协作支持'
  const growth = vMap.growth_focus || '综合提升'

  return `你在工作中偏向"${style}"，兴趣主线为"${field}"，团队中更适合担任"${role}"角色，未来阶段建议围绕"${growth}"持续投入。该画像可作为岗位筛选和职业路径规划的依据。`
})

function dims(m) {
  return [
    { label: '基础', value: m.basic_score, color: '#7c3aed' },
    { label: '技能', value: m.skill_score, color: '#10B981' },
    { label: '素质', value: m.quality_score, color: '#F59E0B' },
    { label: '潜力', value: m.potential_score, color: '#06b6d4' },
  ]
}

async function load() {
  const { data } = await getStudentDetail(route.params.id)
  student.value = data.student
  profile.value = data.profile
  matches.value = data.match_results
  report.value = data.report
}

async function wrap(fn, loadingMsg) {
  busy.value = true; setLoading(true, loadingMsg); msg.value = ''
  try {
    const { data } = await fn()
    msg.value = data.message
    msgOk.value = data.success !== false
    toast(data.message, data.success !== false ? 'success' : 'danger')
    await load()
  } catch (e) {
    msg.value = e.response?.data?.message || '操作失败'
    msgOk.value = false
    toast(msg.value, 'danger')
  } finally { busy.value = false; setLoading(false) }
}

const genProfile = () => wrap(() => generateStudentProfile(route.params.id), 'AI正在生成个人画像…')
const doMatch = () => wrap(() => runMatching(route.params.id, 5), 'AI正在进行人岗匹配…')
const genReport = () => wrap(() => generateReport(route.params.id), 'AI正在生成职业规划报告…')

onMounted(load)
</script>
