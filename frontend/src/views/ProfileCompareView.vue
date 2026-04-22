<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      
      <!-- 页面标题 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-arrow-left-right text-brand-primary"></i>
            画像对比
          </h1>
          <p class="text-sm text-brand-muted mt-1">学生能力画像与岗位要求双向对比分析</p>
        </div>
        <router-link to="/analysis" class="btn-secondary text-sm">
          <i class="bi bi-arrow-left mr-2"></i>
          返回分析中心
        </router-link>
      </div>

      <!-- 对比选择面板 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 选择学生 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <h2 class="mb-4 text-lg font-semibold text-brand-text flex items-center gap-2">
            <i class="bi bi-person text-brand-primary"></i>
            选择学生档案
          </h2>
          <select v-model="selectedStudentId" class="input-base mb-4">
            <option value="">请选择学生</option>
            <option v-for="student in students" :key="student.id" :value="String(student.id)">
              {{ student.name }} · {{ student.education || '学历未知' }} · {{ student.major || '专业未知' }}
            </option>
          </select>

          <div v-if="selectedStudent" class="rounded-xl border border-brand-border bg-brand-surface p-4">
            <div class="mb-4 flex items-start justify-between gap-3">
              <div>
                <div class="text-lg font-semibold text-brand-text">{{ selectedStudent.name }}</div>
                <div class="text-sm text-brand-muted">{{ selectedStudent.education || '学历未知' }} · {{ selectedStudent.major || '专业未知' }}</div>
                <div class="text-xs text-brand-muted">{{ selectedStudent.school || '学校未知' }}</div>
              </div>
              <div class="flex flex-col items-end gap-1 text-xs">
                <span :class="selectedStudent.has_profile ? 'badge-green' : 'badge'">{{ selectedStudent.has_profile ? '已生成画像' : '待生成画像' }}</span>
                <span class="badge-cyan">历史匹配 {{ selectedStudent.match_count || 0 }}</span>
              </div>
            </div>

            <div v-if="studentProfile" class="grid grid-cols-2 gap-3">
              <div class="rounded-lg border border-brand-border bg-brand-card p-3 text-center">
                <div class="text-lg font-bold text-brand-primary">{{ Number(studentProfile.completeness_score || 0).toFixed(1) }}</div>
                <div class="text-xs text-brand-muted">画像完整度</div>
              </div>
              <div class="rounded-lg border border-brand-border bg-brand-card p-3 text-center">
                <div class="text-lg font-bold text-cyan-400">{{ Number(studentProfile.competitiveness_score || 0).toFixed(1) }}</div>
                <div class="text-xs text-brand-muted">竞争力评分</div>
              </div>
            </div>

            <div v-else class="mt-3 rounded-lg border border-dashed border-brand-border p-4 text-center text-sm text-brand-muted">
              学生尚未生成能力画像
              <button class="btn-primary mt-3" :disabled="generatingProfile" @click="generateStudentProfileData">
                <i class="bi bi-magic mr-2" :class="{ 'animate-spin': generatingProfile }"></i>
                {{ generatingProfile ? '生成中...' : '一键生成画像' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 选择岗位 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <h2 class="mb-4 text-lg font-semibold text-brand-text flex items-center gap-2">
            <i class="bi bi-briefcase text-cyan-400"></i>
            选择目标岗位画像
          </h2>
          <select v-model="selectedJobProfileId" class="input-base mb-4">
            <option value="">请选择岗位画像</option>
            <option v-for="profile in jobProfiles" :key="profile.id" :value="String(profile.id)">
              {{ profile.position_name }} · {{ profile.category || '未分类' }} · {{ profile.level || '层级未知' }}
            </option>
          </select>

          <div v-if="selectedJobProfile" class="rounded-xl border border-brand-border bg-brand-surface p-4">
            <div class="mb-3 flex items-center justify-between gap-3">
              <div>
                <div class="font-semibold text-brand-text">{{ selectedJobProfile.position_name }}</div>
                <div class="text-xs text-brand-muted">{{ selectedJobProfile.category || '未分类' }} · {{ selectedJobProfile.level || '层级未知' }}</div>
              </div>
              <span class="badge-cyan text-xs">{{ selectedJobProfile.salary_range || '薪资未知' }}</span>
            </div>

            <div class="mb-3 grid grid-cols-3 gap-2">
              <div v-for="ability in jobAbilities" :key="ability.name" class="rounded-lg border border-brand-border bg-brand-card p-2 text-center">
                <div class="text-sm font-bold" :class="abilityColorClass(ability.value)">{{ ability.value.toFixed(1) }}</div>
                <div class="text-[11px] text-brand-muted">{{ ability.short }}</div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2 text-xs text-brand-muted">
              <div>学历：{{ selectedJobProfile.education_req || '不限' }}</div>
              <div>经验：{{ selectedJobProfile.experience_req || '不限' }}</div>
              <div>技能数：{{ (selectedJobProfile.technical_skills || []).length }}</div>
              <div>证书数：{{ (selectedJobProfile.certificates || []).length }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 开始对比按钮 -->
      <section v-if="studentProfile && selectedJobProfile" class="mb-8 text-center">
        <button class="btn-primary px-8 py-3 text-base" :disabled="matching" @click="runMatching">
          <i class="bi bi-lightning mr-2" :class="{ 'animate-spin': matching }"></i>
          {{ matching ? '分析中...' : '开始智能对比分析' }}
        </button>
      </section>

      <!-- 对比结果 -->
      <section v-if="matchResult" class="space-y-6">
        <!-- 综合评分 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="mb-5 grid grid-cols-1 gap-4 md:grid-cols-5">
            <div class="md:col-span-1 rounded-2xl border border-brand-border bg-brand-surface p-4 text-center">
              <div class="text-4xl font-bold gradient-text">{{ Number(matchResult.overall_score || 0).toFixed(1) }}</div>
              <div class="text-xs text-brand-muted">综合匹配度</div>
              <div class="mt-2 text-xs" :class="overallLevel.class">{{ overallLevel.text }}</div>
            </div>

            <div class="md:col-span-4 grid grid-cols-2 gap-3 md:grid-cols-4">
              <div v-for="dim in dimensionCards" :key="dim.key" class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
                <div class="mb-1 text-xs text-brand-muted">{{ dim.label }}</div>
                <div class="text-2xl font-bold" :class="dim.color">{{ Number(matchResult[dim.key] || 0).toFixed(1) }}</div>
                <div class="mt-2 h-2 overflow-hidden rounded-full bg-brand-card">
                  <div class="h-full rounded-full" :class="dim.barClass" :style="{ width: `${Math.min(100, Number(matchResult[dim.key] || 0))}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 雷达对比图 -->
          <div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
            <div class="rounded-xl border border-brand-border bg-brand-surface p-4">
              <h3 class="mb-3 font-semibold text-brand-text">能力雷达对比（个人 vs 岗位）</h3>
              <RadarChart :series="studentRadarSeries" :indicators="radarIndicators" height="300px" />
            </div>

            <div class="rounded-xl border border-brand-border bg-brand-surface p-4">
              <h3 class="mb-3 font-semibold text-brand-text">能力差值（个人 - 岗位）</h3>
              <div class="space-y-3">
                <div v-for="item in abilityDiffRows" :key="item.name">
                  <div class="mb-1 flex items-center justify-between text-sm">
                    <span class="text-brand-muted">{{ item.name }}</span>
                    <span :class="item.diff >= 0 ? 'text-emerald-400' : 'text-red-400'">
                      {{ item.diff >= 0 ? '+' : '' }}{{ item.diff.toFixed(1) }}
                    </span>
                  </div>
                  <div class="h-2 overflow-hidden rounded-full bg-brand-card">
                    <div class="h-full rounded-full" :class="item.diff >= 0 ? 'bg-emerald-500' : 'bg-red-500'" :style="{ width: `${Math.min(100, Math.abs(item.diff) * 20)}%` }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 技能对比 -->
        <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <div class="bg-brand-card border border-brand-border rounded-2xl p-4">
            <h3 class="mb-3 font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-check-circle text-emerald-400"></i>
              已匹配技能
            </h3>
            <div class="flex flex-wrap gap-1">
              <span v-for="skill in matchedSkills" :key="skill" class="badge-green text-xs">{{ skill }}</span>
              <span v-if="!matchedSkills.length" class="text-xs text-brand-muted">暂无匹配项</span>
            </div>
          </div>

          <div class="bg-brand-card border border-brand-border rounded-2xl p-4">
            <h3 class="mb-3 font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-exclamation-triangle text-red-400"></i>
              待补技能
            </h3>
            <div class="flex flex-wrap gap-1">
              <span v-for="skill in missingSkills" :key="skill" class="rounded-full border border-red-500/30 bg-red-500/10 px-2 py-1 text-xs text-red-400">{{ skill }}</span>
              <span v-if="!missingSkills.length" class="text-xs text-brand-muted">暂无缺口</span>
            </div>
          </div>

          <div class="bg-brand-card border border-brand-border rounded-2xl p-4">
            <h3 class="mb-3 font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-star text-cyan-400"></i>
              额外优势
            </h3>
            <div class="flex flex-wrap gap-1">
              <span v-for="skill in extraSkills" :key="skill" class="badge-cyan text-xs">{{ skill }}</span>
              <span v-if="!extraSkills.length" class="text-xs text-brand-muted">暂无额外技能</span>
            </div>
          </div>
        </div>

        <!-- AI 建议 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <h3 class="mb-4 font-semibold text-brand-text flex items-center gap-2">
            <i class="bi bi-robot text-brand-primary"></i>
            AI 建议与行动优先级
          </h3>
          <div class="space-y-2">
            <div v-for="(rec, index) in recommendations" :key="`${rec}-${index}`"
                 class="rounded-lg border border-brand-border bg-brand-surface p-3 text-sm text-brand-muted flex items-start gap-3">
              <span class="flex-shrink-0 w-6 h-6 rounded-full bg-brand-primary/20 flex items-center justify-center text-xs text-brand-primary font-medium">{{ index + 1 }}</span>
              <span>{{ rec }}</span>
            </div>
            <div v-if="!recommendations.length" class="text-sm text-brand-muted">暂无建议，匹配结果较稳定。</div>
          </div>
        </div>

        <!-- 操作入口 -->
        <div class="flex flex-wrap justify-center gap-3 pb-4">
          <router-link :to="`/reports/${selectedStudentId}`" class="btn-primary">
            <i class="bi bi-file-earmark-text mr-2"></i>查看完整报告
          </router-link>
          <router-link to="/planning" class="btn-secondary">
            <i class="bi bi-signpost-split mr-2"></i>进入规划中心
          </router-link>
        </div>
      </section>

      <!-- 空状态 -->
      <section v-else class="bg-brand-card border border-brand-border rounded-2xl py-16 text-center text-brand-muted">
        <i class="bi bi-arrow-left-right text-5xl text-brand-primary/50"></i>
        <div class="mt-3 text-lg text-brand-text">选择学生与岗位后开始画像对比</div>
        <div class="mt-1 text-sm">分析结果将自动联动匹配评分、技能差距与后续规划路径。</div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref, watch } from 'vue'
import {
  getJobProfiles,
  getStudent,
  getStudents,
  runSingleMatching,
  generateStudentProfile as apiGenerateProfile,
} from '@/api'
import RadarChart from '@/components/RadarChart.vue'

const toast = inject('toast', null)

const students = ref([])
const jobProfiles = ref([])

const selectedStudentId = ref('')
const selectedJobProfileId = ref('')

const selectedStudent = ref(null)
const studentProfile = ref(null)
const selectedJobProfile = ref(null)

const matchResult = ref(null)

const generatingProfile = ref(false)
const matching = ref(false)
const loadingStudent = ref(false)

const abilityMeta = [
  { key: 'innovation_ability', name: '创新能力', short: '创新' },
  { key: 'learning_ability', name: '学习能力', short: '学习' },
  { key: 'pressure_resistance', name: '抗压能力', short: '抗压' },
  { key: 'communication_skill', name: '沟通能力', short: '沟通' },
  { key: 'teamwork_ability', name: '团队协作', short: '团队' },
  { key: 'internship_ability', name: '实践能力', short: '实践' },
]

const dimensionCards = [
  { key: 'basic_score', label: '基础', color: 'text-brand-primary', barClass: 'bg-brand-primary' },
  { key: 'skill_score', label: '技能', color: 'text-cyan-400', barClass: 'bg-cyan-500' },
  { key: 'quality_score', label: '素养', color: 'text-emerald-400', barClass: 'bg-emerald-500' },
  { key: 'potential_score', label: '潜力', color: 'text-amber-400', barClass: 'bg-amber-500' },
]

const studentAbilities = computed(() => {
  if (!studentProfile.value) return []
  return abilityMeta.map((meta) => ({
    ...meta,
    value: Number(studentProfile.value[meta.key] || 0),
  }))
})

const jobAbilities = computed(() => {
  if (!selectedJobProfile.value) return []
  return abilityMeta.map((meta) => ({
    ...meta,
    value: Number(selectedJobProfile.value[meta.key] || 0),
  }))
})

const abilityDiffRows = computed(() => {
  return abilityMeta.map((meta, index) => {
    const studentValue = Number(studentAbilities.value[index]?.value || 0)
    const jobValue = Number(jobAbilities.value[index]?.value || 0)
    return {
      name: meta.name,
      student: studentValue,
      job: jobValue,
      diff: studentValue - jobValue,
    }
  })
})

const radarIndicators = computed(() => abilityMeta.map((item) => item.name))
const studentRadarSeries = computed(() => {
  return [
    {
      name: '学生能力',
      values: studentAbilities.value.map((item) => Number(item.value || 0)),
      color: 'var(--brand-primary)',
    },
    {
      name: '岗位要求',
      values: jobAbilities.value.map((item) => Number(item.value || 0)),
      color: '#06b6d4',
    },
  ]
})

const targetSkills = computed(() => selectedJobProfile.value?.technical_skills || [])
const studentSkills = computed(() => studentProfile.value?.technical_skills || [])

const matchedSkills = computed(() => {
  const targets = targetSkills.value.map((skill) => String(skill).toLowerCase())
  return studentSkills.value.filter((skill) => {
    const normalized = String(skill).toLowerCase()
    return targets.some((target) => normalized.includes(target) || target.includes(normalized))
  })
})

const missingSkills = computed(() => {
  const matchedLower = matchedSkills.value.map((skill) => String(skill).toLowerCase())
  const explicitMissing = matchResult.value?.skill_gaps || []
  const fromTarget = targetSkills.value.filter((skill) => {
    const normalized = String(skill).toLowerCase()
    return !matchedLower.some((matched) => matched.includes(normalized) || normalized.includes(matched))
  })
  const merged = [...explicitMissing, ...fromTarget]
  return Array.from(new Set(merged))
})

const extraSkills = computed(() => {
  const targetLower = targetSkills.value.map((skill) => String(skill).toLowerCase())
  return studentSkills.value.filter((skill) => {
    const normalized = String(skill).toLowerCase()
    return !targetLower.some((target) => normalized.includes(target) || target.includes(normalized))
  })
})

const recommendations = computed(() => matchResult.value?.recommendations || [])

const overallLevel = computed(() => {
  const score = Number(matchResult.value?.overall_score || 0)
  if (score >= 80) return { text: '高匹配', class: 'text-emerald-400' }
  if (score >= 60) return { text: '中匹配', class: 'text-cyan-400' }
  return { text: '需提升', class: 'text-amber-400' }
})

function abilityColorClass(value) {
  if (value >= 8) return 'text-emerald-400'
  if (value >= 6) return 'text-cyan-400'
  if (value >= 4) return 'text-amber-400'
  return 'text-red-400'
}

watch(
  selectedStudentId,
  async (id) => {
    selectedStudent.value = students.value.find((item) => String(item.id) === String(id)) || null
    studentProfile.value = null
    matchResult.value = null

    if (!id) return

    loadingStudent.value = true
    try {
      const response = await getStudent(id)
      selectedStudent.value = response.data?.student || selectedStudent.value
      studentProfile.value = response.data?.profile || null
    } catch (error) {
      toast?.(error?.response?.data?.message || '加载学生画像失败', 'danger')
    } finally {
      loadingStudent.value = false
    }
  },
  { immediate: false },
)

watch(
  selectedJobProfileId,
  (id) => {
    selectedJobProfile.value =
      jobProfiles.value.find((profile) => String(profile.id) === String(id)) || null
    matchResult.value = null
  },
  { immediate: false },
)

async function generateStudentProfileData() {
  if (!selectedStudentId.value) return
  generatingProfile.value = true
  try {
    const response = await apiGenerateProfile(selectedStudentId.value)
    if (response.data?.success) {
      studentProfile.value = response.data.data
      toast?.('学生画像生成成功', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '学生画像生成失败', 'danger')
  } finally {
    generatingProfile.value = false
  }
}

async function runMatching() {
  if (!selectedStudentId.value || !selectedJobProfileId.value) return
  matching.value = true
  try {
    const response = await runSingleMatching(selectedStudentId.value, selectedJobProfileId.value)
    if (response.data?.success) {
      matchResult.value = response.data.data
      toast?.('画像对比分析完成', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '画像对比分析失败', 'danger')
  } finally {
    matching.value = false
  }
}

async function loadBaseData() {
  try {
    const [studentsResponse, profilesResponse] = await Promise.all([getStudents(), getJobProfiles()])
    students.value = studentsResponse.data || []
    jobProfiles.value = profilesResponse.data?.profiles || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '画像对比数据加载失败', 'danger')
  }
}

onMounted(() => {
  loadBaseData()
})
</script>
