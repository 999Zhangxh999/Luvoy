<template>
  <div class="deep-analysis">
    <!-- 顶部导航 -->
    <header class="analysis-header">
      <div class="header-content">
        <h1>
          <i class="bi bi-graph-up-arrow"></i>
          深度画像分析
        </h1>
        <div class="header-tabs">
          <button 
            v-for="tab in mainTabs" 
            :key="tab.id"
            :class="['tab-btn', { active: activeMainTab === tab.id }]"
            @click="activeMainTab = tab.id"
          >
            <i :class="tab.icon"></i>
            {{ tab.label }}
          </button>
        </div>
      </div>
    </header>

    <!-- 主体内容 -->
    <main class="analysis-main">
      <!-- ==================== 个人画像深度分析 ==================== -->
      <div v-if="activeMainTab === 'personal'" class="personal-deep">
        <!-- 选择学生 -->
        <div class="select-bar">
          <select v-model="selectedStudentId" @change="loadStudentProfile" class="select-input">
            <option value="">选择学生档案</option>
            <option v-for="s in students" :key="s.id" :value="String(s.id)">
              {{ s.name }} · {{ s.major }}
            </option>
          </select>
          <button v-if="selectedStudentId && !studentProfile" @click="generateProfile" :disabled="generating" class="btn-generate">
            <i :class="generating ? 'bi bi-hourglass-split spin' : 'bi bi-magic'"></i>
            {{ generating ? '生成中...' : '生成画像' }}
          </button>
        </div>

        <div v-if="studentProfile" class="profile-deep-grid">
          <!-- 核心概览卡片 -->
          <div class="overview-card">
            <div class="profile-hero">
              <div class="hero-avatar">
                <span class="avatar-text">{{ selectedStudent?.name?.charAt(0) }}</span>
                <div class="level-ring">
                  <svg viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="46" class="ring-bg" />
                    <circle cx="50" cy="50" r="46" class="ring-fill" :stroke-dasharray="`${profileLevel * 28.9} 289`" />
                  </svg>
                  <span class="level-num">Lv.{{ profileLevel }}</span>
                </div>
              </div>
              <div class="hero-info">
                <h2>{{ selectedStudent?.name }}</h2>
                <p class="subtitle">{{ selectedStudent?.education }} · {{ selectedStudent?.major }}</p>
                <div class="hero-scores">
                  <div class="score-item">
                    <span class="score-value" :class="completenessClass">{{ studentProfile.completeness_score || 0 }}</span>
                    <span class="score-label">完整度</span>
                  </div>
                  <div class="score-item">
                    <span class="score-value" :class="competitivenessClass">{{ studentProfile.competitiveness_score || 0 }}</span>
                    <span class="score-label">竞争力</span>
                  </div>
                  <div class="score-item">
                    <span class="score-value potential">{{ potentialScore }}</span>
                    <span class="score-label">潜力值</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 核心能力雷达 -->
            <div class="core-radar">
              <h4><i class="bi bi-hexagon"></i> 核心能力模型</h4>
              <div class="radar-wrap">
                <RadarChart :series="personalRadarSeries" :indicators="abilityLabels" height="220px" />
              </div>
            </div>
          </div>

          <!-- SWOT分析 -->
          <div class="swot-card">
            <h3><i class="bi bi-grid-3x3-gap"></i> SWOT 分析</h3>
            <div class="swot-grid">
              <div class="swot-item strength">
                <div class="swot-header">
                  <i class="bi bi-shield-check"></i>
                  <span>优势 Strengths</span>
                </div>
                <ul>
                  <li v-for="(item, i) in swotData.strengths" :key="i">{{ item }}</li>
                </ul>
              </div>
              <div class="swot-item weakness">
                <div class="swot-header">
                  <i class="bi bi-exclamation-diamond"></i>
                  <span>劣势 Weaknesses</span>
                </div>
                <ul>
                  <li v-for="(item, i) in swotData.weaknesses" :key="i">{{ item }}</li>
                </ul>
              </div>
              <div class="swot-item opportunity">
                <div class="swot-header">
                  <i class="bi bi-lightbulb"></i>
                  <span>机会 Opportunities</span>
                </div>
                <ul>
                  <li v-for="(item, i) in swotData.opportunities" :key="i">{{ item }}</li>
                </ul>
              </div>
              <div class="swot-item threat">
                <div class="swot-header">
                  <i class="bi bi-shield-exclamation"></i>
                  <span>威胁 Threats</span>
                </div>
                <ul>
                  <li v-for="(item, i) in swotData.threats" :key="i">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- 行业对标 -->
          <div class="benchmark-card">
            <h3><i class="bi bi-bar-chart-line"></i> 行业能力对标</h3>
            <div class="benchmark-chart">
              <div v-for="(item, i) in benchmarkData" :key="i" class="benchmark-row">
                <span class="benchmark-label">{{ item.label }}</span>
                <div class="benchmark-track">
                  <div class="benchmark-avg" :style="{ left: `${item.avg * 10}%` }">
                    <span class="avg-line"></span>
                    <span class="avg-tag">平均</span>
                  </div>
                  <div class="benchmark-fill" :class="item.level" :style="{ width: `${item.value * 10}%` }">
                  </div>
                  <div class="benchmark-marker" :style="{ left: `${item.value * 10}%` }">
                    <span class="marker-dot"></span>
                    <span class="marker-value">{{ item.value }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="benchmark-legend">
              <span class="legend-item"><span class="dot above"></span> 高于平均</span>
              <span class="legend-item"><span class="dot equal"></span> 接近平均</span>
              <span class="legend-item"><span class="dot below"></span> 低于平均</span>
            </div>
          </div>

          <!-- 技能图谱 -->
          <div class="skill-map-card">
            <h3><i class="bi bi-diagram-3"></i> 技能能力图谱</h3>
            <div class="skill-categories">
              <div v-for="cat in skillCategories" :key="cat.name" class="skill-cat">
                <div class="cat-header">
                  <span class="cat-icon" :style="{ background: cat.color }">
                    <i :class="cat.icon"></i>
                  </span>
                  <span class="cat-name">{{ cat.name }}</span>
                  <span class="cat-count">{{ cat.skills.length }} 项</span>
                </div>
                <div class="cat-skills">
                  <div v-for="skill in cat.skills" :key="skill.name" class="skill-item">
                    <span class="skill-name">{{ skill.name }}</span>
                    <div class="skill-bar">
                      <div class="skill-fill" :style="{ width: `${skill.level * 20}%`, background: cat.color }"></div>
                    </div>
                    <span class="skill-level">{{ skill.level }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 发展建议 -->
          <div class="advice-card">
            <h3><i class="bi bi-compass"></i> AI 发展建议</h3>
            <div class="advice-sections">
              <div class="advice-section priority">
                <h4><i class="bi bi-1-circle-fill"></i> 优先提升</h4>
                <div class="advice-items">
                  <div v-for="(item, i) in priorityAdvice" :key="i" class="advice-item">
                    <span class="item-icon"><i class="bi bi-arrow-up-circle"></i></span>
                    <div class="item-content">
                      <span class="item-title">{{ item.title }}</span>
                      <span class="item-desc">{{ item.desc }}</span>
                    </div>
                    <span class="item-impact">+{{ item.impact }}%</span>
                  </div>
                </div>
              </div>
              <div class="advice-section maintain">
                <h4><i class="bi bi-check-circle-fill"></i> 继续保持</h4>
                <div class="advice-tags">
                  <span v-for="(tag, i) in maintainAdvice" :key="i" class="advice-tag">{{ tag }}</span>
                </div>
              </div>
              <div class="advice-section explore">
                <h4><i class="bi bi-stars"></i> 探索方向</h4>
                <div class="explore-paths">
                  <div v-for="(path, i) in explorePaths" :key="i" class="path-card">
                    <div class="path-icon" :style="{ background: path.color }">
                      <i :class="path.icon"></i>
                    </div>
                    <span class="path-name">{{ path.name }}</span>
                    <span class="path-match">{{ path.match }}% 契合</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon"><i class="bi bi-person-bounding-box"></i></div>
          <p>选择学生档案查看深度画像分析</p>
        </div>
      </div>

      <!-- ==================== 岗位画像深度分析 ==================== -->
      <div v-else-if="activeMainTab === 'job'" class="job-deep">
        <div class="select-bar">
          <select v-model="selectedJobId" @change="loadJobDetails" class="select-input">
            <option value="">选择目标岗位</option>
            <option v-for="j in jobProfiles" :key="j.id" :value="String(j.id)">
              {{ j.position_name }} · {{ j.category }}
            </option>
          </select>
        </div>

        <div v-if="selectedJob" class="job-deep-grid">
          <!-- 岗位概览 -->
          <div class="job-overview-card">
            <div class="job-hero">
              <div class="job-logo">
                <i class="bi bi-building"></i>
              </div>
              <div class="job-info">
                <h2>{{ selectedJob.position_name }}</h2>
                <p class="job-meta">{{ selectedJob.category }} · {{ selectedJob.level || '不限' }}</p>
                <div class="job-tags">
                  <span class="tag salary">{{ selectedJob.salary_range || '面议' }}</span>
                  <span class="tag edu">{{ selectedJob.education_req || '学历不限' }}</span>
                  <span class="tag exp">{{ selectedJob.experience_req || '经验不限' }}</span>
                </div>
              </div>
            </div>
            
            <!-- 岗位能力模型 -->
            <div class="job-radar">
              <h4><i class="bi bi-hexagon"></i> 岗位能力模型</h4>
              <div class="radar-wrap">
                <RadarChart :series="jobRadarSeries" :indicators="abilityLabels" height="220px" />
              </div>
            </div>
          </div>

          <!-- 核心要求 -->
          <div class="requirements-card">
            <h3><i class="bi bi-list-check"></i> 核心要求拆解</h3>
            <div class="req-grid">
              <div class="req-section skills">
                <h4><i class="bi bi-cpu"></i> 技术技能</h4>
                <div class="req-items">
                  <div v-for="(skill, i) in jobTechSkills" :key="i" class="req-item">
                    <span class="req-name">{{ skill }}</span>
                    <span class="req-level essential">必备</span>
                  </div>
                </div>
              </div>
              <div class="req-section qualities">
                <h4><i class="bi bi-person-heart"></i> 软性素质</h4>
                <div class="req-items">
                  <div v-for="(q, i) in jobQualities" :key="i" class="req-item">
                    <span class="req-name">{{ q.name }}</span>
                    <div class="req-bar">
                      <div class="req-fill" :style="{ width: `${q.importance * 10}%` }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 市场洞察 -->
          <div class="market-card">
            <h3><i class="bi bi-graph-up"></i> 市场洞察</h3>
            <div class="market-stats">
              <div class="market-stat">
                <div class="stat-icon hot"><i class="bi bi-fire"></i></div>
                <div class="stat-info">
                  <span class="stat-value">{{ marketData.heat }}</span>
                  <span class="stat-label">热度指数</span>
                </div>
              </div>
              <div class="market-stat">
                <div class="stat-icon compete"><i class="bi bi-people"></i></div>
                <div class="stat-info">
                  <span class="stat-value">{{ marketData.competition }}</span>
                  <span class="stat-label">竞争程度</span>
                </div>
              </div>
              <div class="market-stat">
                <div class="stat-icon growth"><i class="bi bi-graph-up-arrow"></i></div>
                <div class="stat-info">
                  <span class="stat-value">{{ marketData.growth }}</span>
                  <span class="stat-label">发展前景</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 职业发展路径 -->
          <div class="career-path-card">
            <h3><i class="bi bi-signpost-split"></i> 职业发展路径</h3>
            <div class="path-timeline">
              <div v-for="(stage, i) in careerPath" :key="i" class="path-stage" :class="{ current: i === 0 }">
                <div class="stage-marker"></div>
                <div class="stage-content">
                  <span class="stage-title">{{ stage.title }}</span>
                  <span class="stage-years">{{ stage.years }}</span>
                  <span class="stage-salary">{{ stage.salary }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="empty-icon"><i class="bi bi-briefcase"></i></div>
          <p>选择目标岗位查看深度岗位分析</p>
        </div>
      </div>

      <!-- ==================== 深度对比分析 ==================== -->
      <div v-else-if="activeMainTab === 'compare'" class="compare-deep">
        <div class="select-bar dual">
          <select v-model="selectedStudentId" @change="loadStudentProfile" class="select-input">
            <option value="">选择个人档案</option>
            <option v-for="s in students" :key="s.id" :value="String(s.id)">{{ s.name }}</option>
          </select>
          <span class="vs-badge">VS</span>
          <select v-model="selectedJobId" @change="loadJobDetails" class="select-input">
            <option value="">选择目标岗位</option>
            <option v-for="j in jobProfiles" :key="j.id" :value="String(j.id)">{{ j.position_name }}</option>
          </select>
          <button 
            v-if="canCompare" 
            @click="runDeepCompare" 
            :disabled="comparing"
            class="btn-compare"
          >
            <i :class="comparing ? 'bi bi-hourglass-split spin' : 'bi bi-lightning-charge'"></i>
            {{ comparing ? '分析中...' : '深度对比' }}
          </button>
        </div>

        <div v-if="compareResult" class="compare-deep-grid">
          <!-- 匹配度仪表盘 -->
          <div class="match-dashboard">
            <div class="match-gauge">
              <svg viewBox="0 0 200 120">
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#1e1e2e" stroke-width="20" />
                <path 
                  d="M 20 100 A 80 80 0 0 1 180 100" 
                  fill="none" 
                  :stroke="matchColor" 
                  stroke-width="20"
                  stroke-linecap="round"
                  :stroke-dasharray="`${overallMatchScore * 2.51} 251`"
                />
              </svg>
              <div class="gauge-value">
                <span class="value">{{ overallMatchScore }}</span>
                <span class="label">综合匹配度</span>
              </div>
            </div>
            <div class="match-verdict">
              <span class="verdict-badge" :class="matchLevel.class">{{ matchLevel.text }}</span>
              <p>{{ matchLevel.desc }}</p>
            </div>
          </div>

          <!-- 维度雷达叠加 -->
          <div class="overlap-radar">
            <h4><i class="bi bi-radar"></i> 能力雷达叠加</h4>
            <RadarChart :series="compareRadarSeries" :indicators="abilityLabels" height="280px" />
            <div class="radar-legend">
              <span class="legend personal"><span class="dot"></span>个人</span>
              <span class="legend job"><span class="dot"></span>岗位</span>
            </div>
          </div>

          <!-- 差距热力图 -->
          <div class="gap-heatmap">
            <h4><i class="bi bi-grid-3x3-gap-fill"></i> 能力差距热力图</h4>
            <div class="heatmap-grid">
              <div 
                v-for="(gap, i) in abilityGaps" 
                :key="i" 
                class="heatmap-cell"
                :class="gap.class"
                :title="`${gap.label}: ${gap.diff > 0 ? '+' : ''}${gap.diff.toFixed(1)}`"
              >
                <span class="cell-label">{{ gap.label }}</span>
                <span class="cell-diff">{{ gap.diff > 0 ? '+' : '' }}{{ gap.diff.toFixed(1) }}</span>
              </div>
            </div>
            <div class="heatmap-scale">
              <span>不足 -3</span>
              <div class="scale-bar"></div>
              <span>超出 +3</span>
            </div>
          </div>

          <!-- 技能匹配矩阵 -->
          <div class="skill-matrix">
            <h4><i class="bi bi-grid"></i> 技能匹配矩阵</h4>
            <div class="matrix-sections">
              <div class="matrix-col matched">
                <div class="col-header"><i class="bi bi-check-circle-fill"></i> 已具备</div>
                <div class="col-skills">
                  <span v-for="s in matchedSkills" :key="s" class="skill-chip">{{ s }}</span>
                </div>
                <div class="col-count">{{ matchedSkills.length }} 项</div>
              </div>
              <div class="matrix-col missing">
                <div class="col-header"><i class="bi bi-x-circle-fill"></i> 待补充</div>
                <div class="col-skills">
                  <span v-for="s in missingSkills" :key="s" class="skill-chip">{{ s }}</span>
                </div>
                <div class="col-count">{{ missingSkills.length }} 项</div>
              </div>
              <div class="matrix-col extra">
                <div class="col-header"><i class="bi bi-plus-circle-fill"></i> 额外优势</div>
                <div class="col-skills">
                  <span v-for="s in extraSkills" :key="s" class="skill-chip">{{ s }}</span>
                </div>
                <div class="col-count">{{ extraSkills.length }} 项</div>
              </div>
            </div>
          </div>

          <!-- 学习路径规划 -->
          <div class="learning-path">
            <h4><i class="bi bi-map"></i> 技能补足路径</h4>
            <div class="path-steps">
              <div v-for="(step, i) in learningPath" :key="i" class="path-step">
                <div class="step-number">{{ i + 1 }}</div>
                <div class="step-content">
                  <span class="step-title">{{ step.title }}</span>
                  <span class="step-duration">{{ step.duration }}</span>
                  <span class="step-method">{{ step.method }}</span>
                </div>
                <div class="step-progress">
                  <div class="progress-fill" :style="{ width: `${step.progress}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI 深度建议 -->
          <div class="ai-deep-advice">
            <h4><i class="bi bi-robot"></i> AI 深度建议</h4>
            <div class="advice-cards">
              <div v-for="(advice, i) in deepAdvice" :key="i" class="deep-advice-card">
                <div class="advice-icon" :style="{ background: advice.color }">
                  <i :class="advice.icon"></i>
                </div>
                <div class="advice-content">
                  <span class="advice-title">{{ advice.title }}</span>
                  <p class="advice-text">{{ advice.text }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state compare">
          <div class="empty-icon"><i class="bi bi-arrows-angle-contract"></i></div>
          <p>选择个人档案和目标岗位，开始深度对比分析</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import {
  getJobProfiles,
  getStudent,
  getStudents,
  runSingleMatching,
  generateStudentProfile as apiGenerateProfile
} from '@/api'
import RadarChart from '@/components/RadarChart.vue'

const toast = inject('toast', null)

// 主Tab
const mainTabs = [
  { id: 'personal', label: '个人画像', icon: 'bi bi-person-fill' },
  { id: 'job', label: '岗位画像', icon: 'bi bi-briefcase-fill' },
  { id: 'compare', label: '深度对比', icon: 'bi bi-arrows-angle-contract' }
]
const activeMainTab = ref('personal')

// 数据
const students = ref([])
const jobProfiles = ref([])
const selectedStudentId = ref('')
const selectedJobId = ref('')
const studentProfile = ref(null)
const compareResult = ref(null)

// 状态
const generating = ref(false)
const comparing = ref(false)

// 能力维度
const abilityKeys = ['learning_ability', 'innovation_ability', 'communication_skill', 'teamwork_ability', 'pressure_resistance', 'internship_ability']
const abilityLabels = ['学习力', '创新力', '沟通力', '协作力', '抗压力', '执行力']

// 计算属性
const selectedStudent = computed(() => students.value.find(s => String(s.id) === selectedStudentId.value))
const selectedJob = computed(() => jobProfiles.value.find(j => String(j.id) === selectedJobId.value))

const profileLevel = computed(() => {
  if (!studentProfile.value) return 1
  return Math.max(1, Math.ceil((studentProfile.value.competitiveness_score || 0) / 10))
})

const completenessClass = computed(() => {
  const score = studentProfile.value?.completeness_score || 0
  if (score >= 80) return 'high'
  if (score >= 60) return 'medium'
  return 'low'
})

const competitivenessClass = computed(() => {
  const score = studentProfile.value?.competitiveness_score || 0
  if (score >= 80) return 'high'
  if (score >= 60) return 'medium'
  return 'low'
})

const potentialScore = computed(() => {
  if (!studentProfile.value) return 0
  const learning = studentProfile.value.learning_ability || 0
  const innovation = studentProfile.value.innovation_ability || 0
  return Math.round((learning * 0.6 + innovation * 0.4) * 10)
})

// 个人雷达数据
const personalRadarSeries = computed(() => [{
  name: '个人能力',
  values: abilityKeys.map(k => Number(studentProfile.value?.[k] || 0)),
  color: '#8b5cf6'
}])

// 岗位雷达数据
const jobRadarSeries = computed(() => [{
  name: '岗位要求', 
  values: abilityKeys.map(k => Number(selectedJob.value?.[k] || 0)),
  color: '#06b6d4'
}])

// 对比雷达数据
const compareRadarSeries = computed(() => [
  { name: '个人能力', values: abilityKeys.map(k => Number(studentProfile.value?.[k] || 0)), color: '#8b5cf6' },
  { name: '岗位要求', values: abilityKeys.map(k => Number(selectedJob.value?.[k] || 0)), color: '#06b6d4' }
])

// SWOT数据
const swotData = computed(() => {
  if (!studentProfile.value) return { strengths: [], weaknesses: [], opportunities: [], threats: [] }
  
  const abilities = abilityKeys.map((k, i) => ({ key: k, label: abilityLabels[i], value: studentProfile.value[k] || 0 }))
  const sorted = [...abilities].sort((a, b) => b.value - a.value)
  
  return {
    strengths: sorted.slice(0, 2).map(a => `${a.label}突出 (${a.value}/10)`),
    weaknesses: sorted.slice(-2).map(a => `${a.label}待提升 (${a.value}/10)`),
    opportunities: ['技术快速迭代带来学习机会', '行业人才缺口大'],
    threats: ['同质化竞争激烈', '技能更新速度快']
  }
})

// 行业对标数据
const benchmarkData = computed(() => {
  if (!studentProfile.value) return []
  return abilityKeys.map((k, i) => {
    const value = studentProfile.value[k] || 0
    const avg = 6.5 // 模拟行业平均
    const diff = value - avg
    return {
      label: abilityLabels[i],
      value,
      avg,
      level: diff > 0.5 ? 'above' : diff < -0.5 ? 'below' : 'equal'
    }
  })
})

// 技能分类
const skillCategories = computed(() => {
  if (!studentProfile.value) return []
  const skills = studentProfile.value.technical_skills || []
  return [
    {
      name: '编程技能',
      icon: 'bi bi-code-slash',
      color: '#8b5cf6',
      skills: skills.slice(0, 3).map(s => ({ name: s, level: Math.floor(Math.random() * 3) + 3 }))
    },
    {
      name: '工具能力',
      icon: 'bi bi-tools',
      color: '#06b6d4', 
      skills: skills.slice(3, 6).map(s => ({ name: s, level: Math.floor(Math.random() * 3) + 2 }))
    },
    {
      name: '软技能',
      icon: 'bi bi-people',
      color: '#10b981',
      skills: [
        { name: '沟通表达', level: Math.ceil((studentProfile.value.communication_skill || 5) / 2) },
        { name: '团队协作', level: Math.ceil((studentProfile.value.teamwork_ability || 5) / 2) }
      ]
    }
  ]
})

// 优先提升建议
const priorityAdvice = computed(() => {
  if (!studentProfile.value) return []
  const abilities = abilityKeys.map((k, i) => ({ key: k, label: abilityLabels[i], value: studentProfile.value[k] || 0 }))
  const sorted = [...abilities].sort((a, b) => a.value - b.value)
  return sorted.slice(0, 2).map(a => ({
    title: a.label,
    desc: `当前 ${a.value}/10，建议通过实践和学习提升`,
    impact: Math.round((10 - a.value) * 5)
  }))
})

const maintainAdvice = computed(() => {
  if (!studentProfile.value) return []
  const abilities = abilityKeys.map((k, i) => ({ key: k, label: abilityLabels[i], value: studentProfile.value[k] || 0 }))
  return abilities.filter(a => a.value >= 7).map(a => a.label)
})

const explorePaths = computed(() => [
  { name: '技术专家', icon: 'bi bi-cpu', color: '#8b5cf6', match: 75 },
  { name: '产品经理', icon: 'bi bi-kanban', color: '#06b6d4', match: 68 },
  { name: '项目管理', icon: 'bi bi-clipboard-check', color: '#10b981', match: 62 }
])

// 岗位相关
const jobTechSkills = computed(() => selectedJob.value?.technical_skills || [])
const jobQualities = computed(() => [
  { name: '责任心', importance: 9 },
  { name: '学习意愿', importance: 8 },
  { name: '抗压能力', importance: 7 },
  { name: '沟通能力', importance: 8 }
])

const marketData = computed(() => ({
  heat: '🔥 高',
  competition: '⚔️ 中等',
  growth: '📈 良好'
}))

const careerPath = computed(() => [
  { title: selectedJob.value?.position_name || '初级岗位', years: '0-2年', salary: selectedJob.value?.salary_range || '8-12K' },
  { title: '高级' + (selectedJob.value?.position_name || '岗位'), years: '3-5年', salary: '15-25K' },
  { title: '技术专家/经理', years: '5-8年', salary: '25-40K' },
  { title: '总监/架构师', years: '8年+', salary: '40K+' }
])

// 对比相关
const canCompare = computed(() => selectedStudentId.value && selectedJobId.value && studentProfile.value)

const overallMatchScore = computed(() => Math.round(compareResult.value?.overall_score || 0))

const matchColor = computed(() => {
  const score = overallMatchScore.value
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#f59e0b'
  return '#ef4444'
})

const matchLevel = computed(() => {
  const score = overallMatchScore.value
  if (score >= 80) return { text: '高度匹配', class: 'high', desc: '你的条件与岗位高度契合，可以直接申请！' }
  if (score >= 60) return { text: '基本匹配', class: 'medium', desc: '存在一些差距，建议针对性提升后申请。' }
  return { text: '需要努力', class: 'low', desc: '与目标岗位差距较大，需要系统学习和提升。' }
})

// 能力差距
const abilityGaps = computed(() => {
  if (!studentProfile.value || !selectedJob.value) return []
  return abilityKeys.map((k, i) => {
    const personal = studentProfile.value[k] || 0
    const job = selectedJob.value[k] || 0
    const diff = personal - job
    let cls = 'neutral'
    if (diff >= 1) cls = 'positive'
    else if (diff <= -1) cls = 'negative'
    return { label: abilityLabels[i], diff, class: cls }
  })
})

// 技能匹配
const targetSkills = computed(() => selectedJob.value?.technical_skills || [])
const personalSkillList = computed(() => studentProfile.value?.technical_skills || [])

const matchedSkills = computed(() => {
  const targets = targetSkills.value.map(s => String(s).toLowerCase())
  return personalSkillList.value.filter(s => {
    const n = String(s).toLowerCase()
    return targets.some(t => n.includes(t) || t.includes(n))
  })
})

const missingSkills = computed(() => {
  const matched = matchedSkills.value.map(s => String(s).toLowerCase())
  return targetSkills.value.filter(s => {
    const n = String(s).toLowerCase()
    return !matched.some(m => m.includes(n) || n.includes(m))
  })
})

const extraSkills = computed(() => {
  const targets = targetSkills.value.map(s => String(s).toLowerCase())
  return personalSkillList.value.filter(s => {
    const n = String(s).toLowerCase()
    return !targets.some(t => n.includes(t) || t.includes(n))
  })
})

// 学习路径
const learningPath = computed(() => {
  return missingSkills.value.slice(0, 3).map((skill, i) => ({
    title: skill,
    duration: `${(i + 1) * 2} 周`,
    method: ['在线课程', '项目实践', '导师指导'][i % 3],
    progress: 0
  }))
})

// 深度建议
const deepAdvice = computed(() => {
  if (!compareResult.value) return []
  return [
    { icon: 'bi bi-book', color: '#8b5cf6', title: '技能提升', text: `优先学习 ${missingSkills.value[0] || '核心技能'}，预计2-4周可入门` },
    { icon: 'bi bi-briefcase', color: '#06b6d4', title: '项目经验', text: '通过开源项目或实习积累实战经验' },
    { icon: 'bi bi-person-check', color: '#10b981', title: '面试准备', text: '针对岗位要求准备技术和行为面试' }
  ]
})

// 方法
async function loadData() {
  try {
    const [jobsRes, studentsRes] = await Promise.all([getJobProfiles(), getStudents()])
    jobProfiles.value = jobsRes.data?.profiles || []
    students.value = studentsRes.data || []
  } catch (error) {
    toast?.('数据加载失败', 'danger')
  }
}

async function loadStudentProfile() {
  if (!selectedStudentId.value) {
    studentProfile.value = null
    return
  }
  try {
    const response = await getStudent(selectedStudentId.value)
    studentProfile.value = response.data?.profile || null
  } catch (error) {
    console.error('Load profile failed:', error)
  }
}

function loadJobDetails() {
  // Job details are already in jobProfiles
}

async function generateProfile() {
  if (!selectedStudentId.value || generating.value) return
  generating.value = true
  try {
    const response = await apiGenerateProfile(selectedStudentId.value)
    if (response.data?.success) {
      studentProfile.value = response.data.data
      toast?.('画像生成成功！', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '生成失败', 'danger')
  } finally {
    generating.value = false
  }
}

async function runDeepCompare() {
  if (!canCompare.value || comparing.value) return
  comparing.value = true
  try {
    const response = await runSingleMatching(selectedStudentId.value, selectedJobId.value)
    if (response.data?.success) {
      compareResult.value = response.data.data
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '对比分析失败', 'danger')
  } finally {
    comparing.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.deep-analysis {
  min-height: 100vh;
  background: var(--color-brand-bg, #0f0f1a);
}

/* Header */
.analysis-header {
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.1) 0%, transparent 100%);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
  padding: 20px 24px;
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(10px);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.header-content h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-content h1 i {
  color: #8b5cf6;
}

.header-tabs {
  display: flex;
  gap: 8px;
}

.tab-btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  background: transparent;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: rgba(139, 92, 246, 0.4);
  color: #a78bfa;
}

.tab-btn.active {
  background: var(--btn-primary-gradient, linear-gradient(135deg, #8b5cf6, #6366f1));
  border-color: transparent;
  color: white;
}

/* Main */
.analysis-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

/* Select Bar */
.select-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.select-bar.dual {
  align-items: center;
}

.select-input {
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  color: var(--color-brand-text, #e2e8f0);
  font-size: 14px;
  min-width: 200px;
  outline: none;
  cursor: pointer;
}

.select-input:focus {
  border-color: rgba(139, 92, 246, 0.5);
}

.vs-badge {
  padding: 6px 12px;
  background: var(--btn-primary-gradient, linear-gradient(135deg, #8b5cf6, #06b6d4));
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  color: white;
}

.btn-generate, .btn-compare {
  padding: 12px 20px;
  background: var(--btn-primary-gradient, linear-gradient(135deg, #8b5cf6, #6366f1));
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-generate:hover:not(:disabled), .btn-compare:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.btn-generate:disabled, .btn-compare:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Grids */
.profile-deep-grid, .job-deep-grid, .compare-deep-grid {
  display: grid;
  gap: 20px;
}

.profile-deep-grid {
  grid-template-columns: repeat(2, 1fr);
}

.job-deep-grid {
  grid-template-columns: repeat(2, 1fr);
}

.compare-deep-grid {
  grid-template-columns: repeat(2, 1fr);
}

@media (max-width: 1024px) {
  .profile-deep-grid, .job-deep-grid, .compare-deep-grid {
    grid-template-columns: 1fr;
  }
}

/* Cards */
.overview-card, .swot-card, .benchmark-card, .skill-map-card, .advice-card,
.job-overview-card, .requirements-card, .market-card, .career-path-card,
.match-dashboard, .overlap-radar, .gap-heatmap, .skill-matrix, .learning-path, .ai-deep-advice {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 16px;
  padding: 20px;
}

.overview-card, .job-overview-card, .match-dashboard {
  grid-column: span 2;
}

@media (max-width: 1024px) {
  .overview-card, .job-overview-card, .match-dashboard {
    grid-column: span 1;
  }
}

/* Card Headers */
.overview-card h3, .swot-card h3, .benchmark-card h3, .skill-map-card h3, .advice-card h3,
.requirements-card h3, .market-card h3, .career-path-card h3,
.overlap-radar h4, .gap-heatmap h4, .skill-matrix h4, .learning-path h4, .ai-deep-advice h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.overview-card h3 i, .swot-card h3 i, .benchmark-card h3 i, .skill-map-card h3 i, .advice-card h3 i,
.requirements-card h3 i, .market-card h3 i, .career-path-card h3 i,
.overlap-radar h4 i, .gap-heatmap h4 i, .skill-matrix h4 i, .learning-path h4 i, .ai-deep-advice h4 i {
  color: #8b5cf6;
}

/* Profile Hero */
.profile-hero {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.hero-avatar {
  position: relative;
}

.avatar-text {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: white;
}

.level-ring {
  position: absolute;
  inset: -6px;
  width: 84px;
  height: 84px;
}

.level-ring svg {
  transform: rotate(-90deg);
}

.level-ring .ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.1);
  stroke-width: 4;
}

.level-ring .ring-fill {
  fill: none;
  stroke: #f59e0b;
  stroke-width: 4;
  stroke-linecap: round;
}

.level-num {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 6px;
  color: white;
}

.hero-info h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.hero-info .subtitle {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 12px;
}

.hero-scores {
  display: flex;
  gap: 20px;
}

.score-item {
  text-align: center;
}

.score-value {
  display: block;
  font-size: 24px;
  font-weight: 800;
}

.score-value.high { color: #10b981; }
.score-value.medium { color: #f59e0b; }
.score-value.low { color: #ef4444; }
.score-value.potential { color: #8b5cf6; }

.score-label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.core-radar h4 {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.core-radar h4 i {
  color: #8b5cf6;
}

.radar-wrap {
  min-height: 220px;
}

/* SWOT */
.swot-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.swot-item {
  padding: 14px;
  border-radius: 12px;
}

.swot-item.strength { background: rgba(16, 185, 129, 0.08); }
.swot-item.weakness { background: rgba(239, 68, 68, 0.08); }
.swot-item.opportunity { background: rgba(6, 182, 212, 0.08); }
.swot-item.threat { background: rgba(245, 158, 11, 0.08); }

.swot-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
}

.swot-item.strength .swot-header { color: #10b981; }
.swot-item.weakness .swot-header { color: #ef4444; }
.swot-item.opportunity .swot-header { color: #06b6d4; }
.swot-item.threat .swot-header { color: #f59e0b; }

.swot-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.swot-item li {
  font-size: 12px;
  color: var(--color-brand-text, #e2e8f0);
  padding: 4px 0;
  border-bottom: 1px solid rgba(139, 92, 246, 0.05);
}

.swot-item li:last-child {
  border-bottom: none;
}

/* Benchmark */
.benchmark-chart {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.benchmark-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.benchmark-label {
  width: 56px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.benchmark-track {
  flex: 1;
  height: 10px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 5px;
  position: relative;
}

.benchmark-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.benchmark-fill.above { background: linear-gradient(90deg, #10b981, #34d399); }
.benchmark-fill.equal { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.benchmark-fill.below { background: linear-gradient(90deg, #ef4444, #f87171); }

.benchmark-avg {
  position: absolute;
  top: -16px;
  transform: translateX(-50%);
}

.avg-line {
  display: block;
  width: 2px;
  height: 26px;
  background: #64748b;
}

.avg-tag {
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  color: #64748b;
  white-space: nowrap;
}

.benchmark-marker {
  position: absolute;
  top: -8px;
  transform: translateX(-50%);
}

.marker-dot {
  display: block;
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid #8b5cf6;
  border-radius: 50%;
}

.marker-value {
  position: absolute;
  top: 14px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.benchmark-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 12px;
}

.legend-item {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-item .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-item .dot.above { background: #10b981; }
.legend-item .dot.equal { background: #f59e0b; }
.legend-item .dot.below { background: #ef4444; }

/* Skill Map */
.skill-categories {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skill-cat {
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.cat-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.cat-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: white;
}

.cat-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.cat-count {
  margin-left: auto;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.cat-skills {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skill-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.skill-name {
  width: 80px;
  font-size: 12px;
  color: var(--color-brand-text, #e2e8f0);
}

.skill-bar {
  flex: 1;
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.skill-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.skill-level {
  width: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #a78bfa;
  text-align: right;
}

/* Advice */
.advice-sections {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.advice-section h4 {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.advice-section.priority h4 i { color: #ef4444; }
.advice-section.maintain h4 i { color: #10b981; }
.advice-section.explore h4 i { color: #8b5cf6; }

.advice-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.advice-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.05);
  border-radius: 10px;
}

.item-icon {
  color: #ef4444;
}

.item-content {
  flex: 1;
}

.item-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.item-desc {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.item-impact {
  font-size: 12px;
  font-weight: 600;
  color: #10b981;
}

.advice-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.advice-tag {
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  font-size: 12px;
  color: #34d399;
}

.explore-paths {
  display: flex;
  gap: 12px;
}

.path-card {
  flex: 1;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
  text-align: center;
}

.path-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  margin: 0 auto 10px;
}

.path-name {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.path-match {
  font-size: 11px;
  color: #10b981;
}

/* Job Cards */
.job-hero {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.job-logo {
  width: 64px;
  height: 64px;
  border-radius: 14px;
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.job-info h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.job-meta {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 10px;
}

.job-tags {
  display: flex;
  gap: 8px;
}

.job-tags .tag {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 6px;
}

.tag.salary { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.tag.edu { background: rgba(139, 92, 246, 0.15); color: #a78bfa; }
.tag.exp { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.job-radar h4 {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.job-radar h4 i {
  color: #06b6d4;
}

/* Requirements */
.req-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 640px) {
  .req-grid {
    grid-template-columns: 1fr;
  }
}

.req-section h4 {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.req-section.skills h4 i { color: #06b6d4; }
.req-section.qualities h4 i { color: #10b981; }

.req-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.req-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 8px;
}

.req-name {
  font-size: 12px;
  color: var(--color-brand-text, #e2e8f0);
}

.req-level {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
}

.req-level.essential {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.req-bar {
  width: 60px;
  height: 4px;
  background: rgba(16, 185, 129, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.req-fill {
  height: 100%;
  background: #10b981;
  border-radius: 2px;
}

/* Market */
.market-stats {
  display: flex;
  gap: 16px;
}

.market-stat {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.stat-icon.hot { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.stat-icon.compete { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.stat-icon.growth { background: rgba(16, 185, 129, 0.15); color: #34d399; }

.stat-info .stat-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.stat-info .stat-label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* Career Path */
.path-timeline {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  padding-left: 20px;
}

.path-timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: linear-gradient(180deg, #8b5cf6, #06b6d4);
}

.path-stage {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 10px;
  position: relative;
}

.path-stage.current {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.stage-marker {
  position: absolute;
  left: -14px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #64748b;
  border: 2px solid var(--color-brand-card, #1a1a2e);
}

.path-stage.current .stage-marker {
  background: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3);
}

.stage-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stage-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.stage-years {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.stage-salary {
  font-size: 12px;
  font-weight: 600;
  color: #10b981;
}

/* Compare */
.match-dashboard {
  display: flex;
  align-items: center;
  gap: 32px;
}

.match-gauge {
  position: relative;
  width: 200px;
  height: 120px;
}

.match-gauge svg {
  width: 100%;
  height: 100%;
}

.gauge-value {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.gauge-value .value {
  display: block;
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gauge-value .label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.match-verdict {
  flex: 1;
}

.verdict-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.verdict-badge.high { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.verdict-badge.medium { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.verdict-badge.low { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.match-verdict p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

.overlap-radar {
  min-height: 340px;
}

.radar-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 12px;
}

.radar-legend .legend {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.radar-legend .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.radar-legend .legend.personal .dot { background: #8b5cf6; }
.radar-legend .legend.job .dot { background: #06b6d4; }

/* Gap Heatmap */
.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 12px;
}

.heatmap-cell {
  padding: 14px;
  border-radius: 10px;
  text-align: center;
}

.heatmap-cell.positive { background: rgba(16, 185, 129, 0.15); }
.heatmap-cell.neutral { background: rgba(245, 158, 11, 0.15); }
.heatmap-cell.negative { background: rgba(239, 68, 68, 0.15); }

.cell-label {
  display: block;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 4px;
}

.cell-diff {
  font-size: 16px;
  font-weight: 700;
}

.heatmap-cell.positive .cell-diff { color: #10b981; }
.heatmap-cell.neutral .cell-diff { color: #f59e0b; }
.heatmap-cell.negative .cell-diff { color: #ef4444; }

.heatmap-scale {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 10px;
  color: var(--color-brand-muted, #64748b);
}

.scale-bar {
  width: 100px;
  height: 6px;
  background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981);
  border-radius: 3px;
}

/* Skill Matrix */
.matrix-sections {
  display: flex;
  gap: 12px;
}

.matrix-col {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  text-align: center;
}

.matrix-col.matched { background: rgba(16, 185, 129, 0.08); }
.matrix-col.missing { background: rgba(239, 68, 68, 0.08); }
.matrix-col.extra { background: rgba(6, 182, 212, 0.08); }

.col-header {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.matrix-col.matched .col-header { color: #10b981; }
.matrix-col.missing .col-header { color: #ef4444; }
.matrix-col.extra .col-header { color: #06b6d4; }

.col-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  min-height: 60px;
}

.skill-chip {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 6px;
}

.matrix-col.matched .skill-chip { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.matrix-col.missing .skill-chip { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.matrix-col.extra .skill-chip { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.col-count {
  margin-top: 10px;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* Learning Path */
.path-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.path-step {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.step-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.step-duration, .step-method {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.step-duration {
  margin-right: 8px;
}

.step-progress {
  width: 60px;
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #10b981;
  border-radius: 3px;
}

/* AI Deep Advice */
.advice-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.deep-advice-card {
  display: flex;
  gap: 14px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.advice-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  flex-shrink: 0;
}

.advice-content {
  flex: 1;
}

.advice-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.advice-text {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #8b5cf6;
  margin: 0 auto 20px;
}

.empty-state p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .analysis-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .analysis-header h1 {
  color: #0c4a6e;
}

:global(html.light) .analysis-header p {
  color: #64748b;
}

:global(html.light) .main-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .section-title {
  color: #0c4a6e;
}

:global(html.light) .tab-btn {
  color: #64748b;
}

:global(html.light) .tab-btn.active {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .stat-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .stat-value {
  color: #0891b2;
}

:global(html.light) .stat-label {
  color: #64748b;
}

:global(html.light) .chart-card {
  background: rgba(8, 145, 178, 0.02);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .chart-title {
  color: #0c4a6e;
}

:global(html.light) .skill-item {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .skill-name {
  color: #0c4a6e;
}

:global(html.light) .skill-level {
  color: #64748b;
}

:global(html.light) .skill-bar {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .insight-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .insight-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .insight-title {
  color: #0c4a6e;
}

:global(html.light) .insight-text {
  color: #475569;
}

:global(html.light) .recommendation-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .recommendation-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .recommendation-title {
  color: #0c4a6e;
}

:global(html.light) .recommendation-desc {
  color: #64748b;
}

:global(html.light) .sidebar-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .sidebar-title {
  color: #0c4a6e;
}

:global(html.light) .progress-item {
  background: rgba(8, 145, 178, 0.03);
}

:global(html.light) .progress-label {
  color: #0c4a6e;
}

:global(html.light) .progress-value {
  color: #0891b2;
}

:global(html.light) .progress-bar {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .advice-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .advice-card:hover {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .advice-title {
  color: #0c4a6e;
}

:global(html.light) .advice-text {
  color: #64748b;
}

:global(html.light) .empty-icon {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .btn-primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-secondary {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.2);
  color: #64748b;
}

:global(html.light) .btn-secondary:hover {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}
</style>
