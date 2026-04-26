<template>
  <div class="min-h-screen bg-brand-bg">
    <!-- Sticky Header -->
    <div class="sticky top-0 z-30 glass-nav border-b border-brand-border">
      <div class="max-w-6xl mx-auto px-4 lg:px-8 h-14 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button @click="goBack" class="btn-ghost p-2 rounded-lg">
            <i class="bi bi-arrow-left text-lg"></i>
          </button>
          <h1 class="text-lg font-bold text-brand-text">岗位画像</h1>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex bg-brand-surface rounded-lg p-0.5 border border-brand-border">
            <button
              @click="profileMode = 'job'"
              class="px-3 py-1.5 rounded-md text-xs font-medium transition-all"
              :class="profileMode === 'job' ? 'bg-violet-600 text-white' : 'text-brand-muted hover:text-brand-text'"
            >
              岗位画像
            </button>
            <button
              @click="profileMode = 'user'"
              class="px-3 py-1.5 rounded-md text-xs font-medium transition-all"
              :class="profileMode === 'user' ? 'bg-violet-600 text-white' : 'text-brand-muted hover:text-brand-text'"
            >
              个人画像
            </button>
          </div>
          <button @click="startMatching" class="btn-primary px-4 py-2 rounded-lg text-sm">
            <i class="bi bi-lightning mr-1"></i> 开始匹配
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div v-if="profile" class="max-w-6xl mx-auto px-4 lg:px-8 py-6 space-y-6">

      <!-- ═══ Hero Card ═══ -->
      <div class="hero-card">
        <div class="flex items-start gap-5">
          <div class="hero-icon" :class="getIconBg(profile.category)">
            <i :class="getCategoryIcon(profile.category)" class="text-2xl"></i>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3 mb-1 flex-wrap">
              <h2 class="text-xl font-bold text-brand-text truncate">{{ profile.position_name }}</h2>
              <span class="tag-category">{{ profile.category }}</span>
              <span class="tag-level">{{ profile.level || 'P3-P5' }}</span>
              <span v-if="marketData.job_count > 1000" class="tag-hot">🔥 热招</span>
            </div>
            <p class="text-sm text-brand-muted mb-3 line-clamp-2">{{ profile.summary || '暂无描述' }}</p>
            <div class="flex flex-wrap items-center gap-4 text-xs text-brand-muted">
              <span class="flex items-center gap-1"><i class="bi bi-mortarboard"></i> {{ profile.education_req || '本科' }}</span>
              <span class="flex items-center gap-1"><i class="bi bi-clock-history"></i> {{ profile.experience_req || '1-3年' }}</span>
              <span class="flex items-center gap-1"><i class="bi bi-graph-up-arrow"></i> 竞争 {{ marketData.competition_ratio }}</span>
            </div>
          </div>
          <div class="hero-salary">
            <span class="salary-num">{{ formatSalary(marketData.avg_salary) }}</span>
            <span class="salary-sub">平均月薪</span>
          </div>
        </div>
      </div>

      <!-- ═══ A. 核心能力 ═══ -->
      <section class="section-card">
        <h3 class="section-title"><i class="bi bi-stars text-violet-400"></i> 核心能力要求</h3>
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <!-- Radar -->
          <div class="lg:col-span-2">
            <RadarChart :series="radarSeries" :indicators="radarIndicators" height="240px" />
          </div>
          <!-- Top Abilities -->
          <div class="lg:col-span-3 space-y-2.5">
            <div v-for="(ability, i) in topAbilities" :key="ability.name" class="ability-row">
              <span class="ability-rank" :class="'rank-' + (i + 1)">{{ i + 1 }}</span>
              <span class="ability-name flex-shrink-0">{{ ability.name }}</span>
              <div class="ability-bar-track">
                <div class="ability-bar-fill" :style="{ width: ability.value * 10 + '%' }"></div>
              </div>
              <span class="ability-score">{{ ability.value.toFixed(1) }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══ B. 技能 & 岗位要求 ═══ -->
      <section class="section-card">
        <h3 class="section-title"><i class="bi bi-tools text-cyan-400"></i> 技能要求</h3>
        <!-- Skill Tags -->
        <div class="flex flex-wrap gap-2 mb-5">
          <span
            v-for="(skill, i) in profile.technical_skills || []"
            :key="skill"
            class="skill-chip"
            :class="{ 'skill-primary': i < 3 }"
          >
            <i v-if="i < 3" class="bi bi-fire text-amber-400 mr-1 text-xs"></i>{{ skill }}
          </span>
          <span v-if="!(profile.technical_skills || []).length" class="text-sm text-brand-subtle">暂无技能数据</span>
        </div>
        <!-- 3-column requirements -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="req-block">
            <h4 class="req-label"><i class="bi bi-wrench text-violet-400 mr-1.5"></i>技术要求</h4>
            <ul class="req-list">
              <li v-for="(r, i) in profile.core_requirements?.technical || []" :key="i">{{ r }}</li>
            </ul>
          </div>
          <div class="req-block">
            <h4 class="req-label"><i class="bi bi-people text-cyan-400 mr-1.5"></i>软技能</h4>
            <ul class="req-list">
              <li v-for="(r, i) in profile.core_requirements?.soft || []" :key="i">{{ r }}</li>
            </ul>
          </div>
          <div class="req-block">
            <h4 class="req-label"><i class="bi bi-star text-amber-400 mr-1.5"></i>加分项</h4>
            <ul class="req-list">
              <li v-for="(r, i) in profile.core_requirements?.bonus || []" :key="i">{{ r }}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ═══ C. 市场洞察 ═══ -->
      <section class="section-card">
        <h3 class="section-title"><i class="bi bi-bar-chart text-emerald-400"></i> 市场洞察</h3>
        <!-- Stats Row -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-5">
          <div class="stat-mini">
            <span class="stat-num text-violet-400">{{ formatNumber(marketData.job_count) }}</span>
            <span class="stat-desc">在招岗位</span>
          </div>
          <div class="stat-mini">
            <span class="stat-num text-cyan-400">{{ formatSalary(marketData.avg_salary) }}</span>
            <span class="stat-desc">平均薪资</span>
          </div>
          <div class="stat-mini">
            <span class="stat-num text-amber-400">{{ marketData.competition_ratio }}</span>
            <span class="stat-desc">竞争指数</span>
          </div>
          <div class="stat-mini">
            <span class="stat-num text-emerald-400">{{ marketData.avg_hire_days }}天</span>
            <span class="stat-desc">招聘周期</span>
          </div>
        </div>
        <!-- 2-col: salary + trend -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Salary Bars -->
          <div>
            <h4 class="sub-title mb-3">薪资分布</h4>
            <div class="space-y-2">
              <div v-for="(item, i) in marketData.salary_distribution" :key="i" class="salary-row">
                <span class="salary-range">{{ item.range }}</span>
                <div class="salary-track">
                  <div class="salary-fill" :class="getSalaryBarClass(i)" :style="{ width: item.percent + '%' }"></div>
                </div>
                <span class="salary-pct">{{ item.percent }}%</span>
              </div>
            </div>
          </div>
          <!-- Trend Chart -->
          <div>
            <h4 class="sub-title mb-3">近12月趋势</h4>
            <div class="h-40" ref="trendChartRef"></div>
          </div>
        </div>
      </section>

      <!-- ═══ D. 职业发展路径 ═══ -->
      <section class="section-card">
        <h3 class="section-title"><i class="bi bi-signpost-split text-amber-400"></i> 职业发展路径</h3>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Promotions -->
          <div>
            <h4 class="sub-title text-emerald-400 mb-3"><i class="bi bi-arrow-up-circle mr-1"></i>晋升方向</h4>
            <div class="space-y-2.5">
              <div v-for="(p, i) in profile.career_path?.promotions_from || []" :key="i" class="path-card">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-brand-text">→ {{ p.to_position }}</span>
                  <div class="flex items-center gap-2 text-xs">
                    <span class="text-brand-muted">{{ p.estimated_years }}年</span>
                    <span class="text-amber-400">{{ '★'.repeat(p.difficulty) }}</span>
                  </div>
                </div>
                <p class="text-xs text-brand-muted mt-1">{{ p.description }}</p>
              </div>
              <p v-if="!profile.career_path?.promotions_from?.length" class="text-sm text-brand-subtle">暂无数据</p>
            </div>
          </div>
          <!-- Transfers -->
          <div>
            <h4 class="sub-title text-cyan-400 mb-3"><i class="bi bi-arrow-left-right mr-1"></i>转岗方向</h4>
            <div class="space-y-2.5">
              <div v-for="(t, i) in profile.career_path?.transfers || []" :key="i" class="path-card">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-brand-text">→ {{ t.to_position }}</span>
                  <span class="text-xs text-brand-muted">约{{ t.estimated_years }}年</span>
                </div>
                <p class="text-xs text-brand-muted mt-1">{{ t.description }}</p>
              </div>
              <p v-if="!profile.career_path?.transfers?.length" class="text-sm text-brand-subtle">暂无数据</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Actions -->
      <div class="flex items-center justify-center gap-4 py-4">
        <button class="btn-secondary px-6 py-2.5 rounded-lg">
          <i class="bi bi-bookmark mr-2"></i>收藏画像
        </button>
        <button class="btn-primary px-6 py-2.5 rounded-lg" @click="startMatching">
          <i class="bi bi-lightning mr-2"></i>立即匹配分析
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-else class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="w-12 h-12 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-brand-muted">正在加载职业画像...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { init, use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import RadarChart from '@/components/RadarChart.vue'
import { getAllCareerProfiles, getCareerProfile } from '@/data/careerMockData'

use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const route = useRoute()
const router = useRouter()

// State
const profile = ref(null)
const profileMode = ref('job')
const trendChartRef = ref(null)
let trendChart = null

// Computed
const marketData = computed(() => profile.value?.market_data || {
  job_count: 0,
  avg_salary: 0,
  competition_ratio: '-',
  avg_hire_days: 0,
  salary_distribution: [],
  experience_distribution: [],
  education_distribution: [],
  industry_distribution: [],
  city_distribution: [],
  trend_12months: [],
  skill_heat: [],
})

const radarIndicators = ['创新能力', '学习能力', '抗压能力', '沟通能力', '团队协作', '实践能力']

const radarSeries = computed(() => {
  if (!profile.value) return []
  return [{
    name: profile.value.position_name,
    values: [
      profile.value.innovation_ability || 5,
      profile.value.learning_ability || 5,
      profile.value.pressure_resistance || 5,
      profile.value.communication_skill || 5,
      profile.value.teamwork_ability || 5,
      profile.value.internship_ability || 5,
    ],
    color: '#7c3aed',
  }]
})

const topAbilities = computed(() => {
  if (!profile.value) return []
  const abilities = [
    { name: '创新能力', value: profile.value.innovation_ability || 5 },
    { name: '学习能力', value: profile.value.learning_ability || 5 },
    { name: '抗压能力', value: profile.value.pressure_resistance || 5 },
    { name: '沟通能力', value: profile.value.communication_skill || 5 },
    { name: '团队协作', value: profile.value.teamwork_ability || 5 },
    { name: '实践能力', value: profile.value.internship_ability || 5 },
  ]
  return abilities.sort((a, b) => b.value - a.value)
})

// Methods

function formatNumber(num) {
  if (!num) return '0'
  if (num >= 10000) return (num / 10000).toFixed(1) + 'W'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}

function formatSalary(salary) {
  if (!salary) return '-'
  return (salary / 1000).toFixed(0) + 'K'
}

function getSalaryBarClass(index) {
  const classes = [
    'bg-gradient-to-r from-violet-600/60 to-violet-500/60',
    'bg-gradient-to-r from-violet-500 to-violet-400',
    'bg-gradient-to-r from-violet-400 to-cyan-400',
    'bg-gradient-to-r from-cyan-500/80 to-cyan-400/80',
    'bg-gradient-to-r from-cyan-400/60 to-cyan-300/60',
  ]
  return classes[index % classes.length]
}

function goBack() {
  router.back()
}

function startMatching() {
  // TODO: Navigate to matching page
  console.log('Start matching for:', profile.value?.position_name)
}

function initTrendChart() {
  if (!trendChartRef.value || !marketData.value.trend_12months?.length) return
  
  if (trendChart) trendChart.dispose()
  trendChart = init(trendChartRef.value, null, { renderer: 'canvas' })
  
  const data = marketData.value.trend_12months
  
  trendChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#1e293b',
      textStyle: { color: '#e2e8f0', fontSize: 12 },
    },
    grid: {
      left: 40,
      right: 20,
      top: 20,
      bottom: 30,
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.month + '月'),
      axisLine: { lineStyle: { color: '#334155' } },
      axisLabel: { color: '#94a3b8', fontSize: 11 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#1e293b' } },
      axisLine: { show: false },
      axisLabel: { color: '#94a3b8', fontSize: 11 },
    },
    series: [{
      type: 'line',
      data: data.map(d => d.value),
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        color: '#7c3aed',
        width: 2,
      },
      itemStyle: {
        color: '#7c3aed',
        borderColor: '#fff',
        borderWidth: 2,
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(124, 58, 237, 0.3)' },
            { offset: 1, color: 'rgba(124, 58, 237, 0.05)' },
          ],
        },
      },
    }],
  })
}

// Load profile data
onMounted(async () => {
  const id = route.params.id
  
  // Try to load from mock data first
  let profileData = getCareerProfile(id)
  
  // If not found, get from all profiles
  if (!profileData) {
    const allProfiles = getAllCareerProfiles()
    profileData = allProfiles.find(p => p.id === id)
  }
  
  if (profileData) {
    profile.value = profileData
    await nextTick()
    initTrendChart()
  }
})

// Resize chart on window resize
let resizeOb = null
onMounted(() => {
  resizeOb = new ResizeObserver(() => trendChart?.resize())
  if (trendChartRef.value) resizeOb.observe(trendChartRef.value)
})

watch(() => marketData.value.trend_12months, () => {
  nextTick(initTrendChart)
}, { deep: true })

// Hero profile helpers
function getIconBg(category) {
  const map = {
    '产品': 'icon-bg-product',
    '技术': 'icon-bg-tech',
    '设计': 'icon-bg-design',
    '运营': 'icon-bg-ops',
    '数据': 'icon-bg-data',
    '市场': 'icon-bg-marketing',
  }
  for (const key of Object.keys(map)) {
    if (category?.includes(key)) return map[key]
  }
  return 'icon-bg-default'
}

function getCategoryIcon(category) {
  const icons = {
    '产品': 'bi bi-lightbulb',
    '技术': 'bi bi-code-slash',
    '设计': 'bi bi-palette',
    '运营': 'bi bi-graph-up-arrow',
    '数据': 'bi bi-bar-chart-line',
    '市场': 'bi bi-megaphone',
    '人力': 'bi bi-people',
    '财务': 'bi bi-calculator',
    'AI': 'bi bi-robot',
    '算法': 'bi bi-cpu',
  }
  for (const key of Object.keys(icons)) {
    if (category?.includes(key)) return icons[key]
  }
  return 'bi bi-briefcase'
}
</script>

<style scoped>
/* ═══ Hero Card ═══ */
.hero-card {
  @apply rounded-2xl p-5 border border-brand-border bg-brand-surface;
}

.hero-icon {
  @apply w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0 text-white;
}
.icon-bg-product { background: linear-gradient(135deg, #7c3aed, #a855f7); }
.icon-bg-tech { background: linear-gradient(135deg, #3b82f6, #06b6d4); }
.icon-bg-design { background: linear-gradient(135deg, #f43f5e, #ec4899); }
.icon-bg-ops { background: linear-gradient(135deg, #f59e0b, #f97316); }
.icon-bg-data { background: linear-gradient(135deg, #06b6d4, #3b82f6); }
.icon-bg-marketing { background: linear-gradient(135deg, #10b981, #22d3ee); }
.icon-bg-default { background: linear-gradient(135deg, #6366f1, #8b5cf6); }

.tag-category {
  @apply px-2.5 py-0.5 rounded-md text-xs font-medium bg-violet-500/15 text-violet-400 border border-violet-500/20;
}
.tag-level {
  @apply px-2.5 py-0.5 rounded-md text-xs font-medium bg-cyan-500/15 text-cyan-400 border border-cyan-500/20;
}
.tag-hot {
  @apply px-2.5 py-0.5 rounded-md text-xs font-medium bg-rose-500/15 text-rose-400 border border-rose-500/20;
}

.hero-salary {
  @apply flex flex-col items-end flex-shrink-0;
}
.salary-num {
  @apply text-2xl font-bold text-violet-400;
}
.salary-sub {
  @apply text-xs text-brand-muted mt-0.5;
}

/* ═══ Section Card ═══ */
.section-card {
  @apply rounded-2xl p-5 border border-brand-border bg-brand-surface;
}
.section-title {
  @apply text-base font-semibold text-brand-text mb-4 flex items-center gap-2;
}
.sub-title {
  @apply text-sm font-medium text-brand-muted;
}

/* ═══ Ability Rows ═══ */
.ability-row {
  @apply flex items-center gap-3;
}
.ability-rank {
  @apply w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold flex-shrink-0;
  background: rgba(124, 58, 237, 0.1);
  color: #a78bfa;
}
.ability-rank.rank-1 {
  background: rgba(124, 58, 237, 0.25);
  color: #fff;
}
.ability-rank.rank-2 {
  background: rgba(6, 182, 212, 0.2);
  color: #67e8f9;
}
.ability-rank.rank-3 {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}
.ability-name {
  @apply text-sm text-brand-text w-16;
}
.ability-bar-track {
  @apply flex-1 h-2 rounded-full bg-brand-bg overflow-hidden;
}
.ability-bar-fill {
  @apply h-full rounded-full transition-all duration-700;
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
}
.ability-score {
  @apply text-sm font-semibold text-violet-400 w-8 text-right;
}

/* ═══ Skill Chips ═══ */
.skill-chip {
  @apply px-3 py-1.5 rounded-lg text-xs font-medium bg-brand-bg text-brand-muted border border-brand-border transition-all;
}
.skill-chip.skill-primary {
  @apply bg-violet-500/10 text-violet-400 border-violet-500/25;
}

/* ═══ Requirement Blocks ═══ */
.req-block {
  @apply p-4 rounded-xl bg-brand-bg border border-brand-border;
}
.req-label {
  @apply text-sm font-medium text-brand-text mb-3 flex items-center;
}
.req-list {
  @apply space-y-2 text-sm text-brand-muted list-none pl-0;
}
.req-list li {
  @apply flex items-start gap-2;
}
.req-list li::before {
  content: '•';
  @apply text-violet-400 flex-shrink-0 mt-0;
}

/* ═══ Stats Mini ═══ */
.stat-mini {
  @apply flex flex-col items-center p-3 rounded-xl bg-brand-bg border border-brand-border text-center;
}
.stat-num {
  @apply text-lg font-bold;
}
.stat-desc {
  @apply text-xs text-brand-muted mt-0.5;
}

/* ═══ Salary Rows ═══ */
.salary-row {
  @apply flex items-center gap-3;
}
.salary-range {
  @apply text-xs text-brand-muted w-14 flex-shrink-0;
}
.salary-track {
  @apply flex-1 h-5 rounded-full bg-brand-bg overflow-hidden;
}
.salary-fill {
  @apply h-full rounded-full transition-all duration-700;
}
.salary-pct {
  @apply text-xs text-brand-text font-medium w-10 text-right flex-shrink-0;
}

/* ═══ Path Cards ═══ */
.path-card {
  @apply p-3.5 rounded-xl bg-brand-bg border border-brand-border hover:border-violet-500/30 transition;
}
</style>
