<template>
  <div class="arena-container" :class="{ 'panel-left-open': showPersonalDetail, 'panel-right-open': showJobDetail }">
    <!-- 背景装饰 -->
    <div class="arena-bg">
      <div class="bg-glow left"></div>
      <div class="bg-glow right"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- 左侧个人画像详情面板 -->
    <transition name="panel-slide-left">
      <aside v-if="showPersonalDetail && studentProfile" class="side-panel left-panel">
        <div class="panel-header">
          <h3><i class="bi bi-person-badge"></i> 个人画像</h3>
          <button class="btn-close" @click="showPersonalDetail = false"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="panel-body">
          <!-- 基本信息 -->
          <div class="profile-hero-compact">
            <div class="hero-avatar">{{ selectedStudent?.name?.charAt(0) }}</div>
            <div class="hero-info">
              <h4>{{ selectedStudent?.name }}</h4>
              <p>{{ selectedStudent?.education }} · {{ selectedStudent?.major }}</p>
            </div>
          </div>
          <div class="score-badges">
            <div class="badge-item"><span class="num">{{ studentProfile.completeness_score || 0 }}</span><span class="label">完整度</span></div>
            <div class="badge-item"><span class="num">{{ studentProfile.competitiveness_score || 0 }}</span><span class="label">竞争力</span></div>
          </div>

          <!-- SWOT分析 -->
          <div class="section-block">
            <h5><i class="bi bi-grid-3x3"></i> SWOT 分析</h5>
            <div class="swot-cards">
              <div class="swot-card strength">
                <div class="card-title"><i class="bi bi-shield-check"></i> 优势</div>
                <ul>
                  <li v-for="(s, i) in swotStrengths" :key="i">{{ s }}</li>
                </ul>
              </div>
              <div class="swot-card weakness">
                <div class="card-title"><i class="bi bi-exclamation-diamond"></i> 待提升</div>
                <ul>
                  <li v-for="(w, i) in swotWeaknesses" :key="i">{{ w }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- 能力雷达 -->
          <div class="section-block">
            <h5><i class="bi bi-hexagon"></i> 能力模型</h5>
            <div class="radar-compact">
              <RadarChart :series="personalRadarSeries" :indicators="abilityLabels" height="180px" />
            </div>
          </div>

          <!-- 技能列表 -->
          <div class="section-block">
            <h5><i class="bi bi-lightbulb"></i> 技能清单</h5>
            <div class="skill-chips">
              <span v-for="(skill, i) in allPersonalSkills" :key="i" class="chip">{{ skill }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="panel-footer">
            <button class="btn-panel primary" @click="regenerateProfile" :disabled="generating">
              <i :class="generating ? 'bi bi-hourglass-split animate-spin' : 'bi bi-arrow-repeat'"></i>
              {{ generating ? '生成中...' : '重新生成' }}
            </button>
            <router-link :to="`/students/${selectedStudentId}`" class="btn-panel outline">
              <i class="bi bi-pencil"></i> 编辑
            </router-link>
          </div>
        </div>
      </aside>
    </transition>

    <!-- 主内容区 -->
    <main class="arena-main">
      <!-- 顶部标题 -->
      <header class="arena-header">
        <h1 class="arena-title">
          <span class="icon">⚔️</span>
          <span class="text">画像对决</span>
          <span class="badge">PROFILE ARENA</span>
        </h1>
        <p class="arena-desc">选择个人档案与目标岗位，开启能力深度对比</p>
        <div class="header-actions">
          <button class="action-btn" @click="showPersonalDetail = !showPersonalDetail" :class="{ active: showPersonalDetail }" v-if="studentProfile">
            <i class="bi bi-person-badge"></i> {{ showPersonalDetail ? '收起' : '展开' }}个人画像
          </button>
          <button class="action-btn cyan" @click="showJobDetail = !showJobDetail" :class="{ active: showJobDetail }" v-if="selectedJob">
            <i class="bi bi-briefcase"></i> {{ showJobDetail ? '收起' : '展开' }}岗位画像
          </button>
        </div>
      </header>

      <!-- 角色选择区 -->
      <div class="arena-stage">
      <!-- 左侧：个人画像卡 -->
      <div class="profile-card personal" :class="{ selected: selectedStudent, ready: studentProfile }">
        <div class="card-glow"></div>
        <div class="card-frame">
          <!-- 卡片头部 -->
          <div class="card-top">
            <span class="card-type">CHALLENGER</span>
            <span class="card-label">个人画像</span>
          </div>

          <!-- 选择状态 -->
          <div v-if="!selectedStudent" class="card-empty" @click="showStudentPicker">
            <div class="empty-icon">
              <i class="bi bi-person-plus-fill"></i>
            </div>
            <p>点击选择档案</p>
          </div>

          <!-- 已选择状态 -->
          <div v-else class="card-content">
            <div class="avatar-section">
              <div class="avatar-ring">
                <div class="avatar">
                  {{ selectedStudent.name?.charAt(0) }}
                </div>
              </div>
              <div class="level-badge" v-if="studentProfile">
                Lv.{{ profileLevel }}
              </div>
            </div>

            <h3 class="card-name">{{ selectedStudent.name }}</h3>
            <p class="card-title">{{ selectedStudent.major || '专业未知' }}</p>

            <!-- 能力六边形 -->
            <div class="hex-chart" v-if="studentProfile">
              <HexagonChart :values="personalAbilities" color="#8b5cf6" />
            </div>
            <div v-else class="no-profile">
              <button class="btn-generate" @click="generateProfile" :disabled="generating">
                <i :class="generating ? 'bi bi-hourglass-split animate-spin' : 'bi bi-magic'"></i>
                {{ generating ? '生成中...' : '生成画像' }}
              </button>
            </div>

            <!-- 核心属性条 -->
            <div class="stats-bar" v-if="studentProfile">
              <div class="stat-item">
                <span class="stat-label">学习力</span>
                <div class="stat-track">
                  <div class="stat-fill" :style="{ width: `${studentProfile.learning_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ studentProfile.learning_ability }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">创新力</span>
                <div class="stat-track">
                  <div class="stat-fill" :style="{ width: `${studentProfile.innovation_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ studentProfile.innovation_ability }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">执行力</span>
                <div class="stat-track">
                  <div class="stat-fill" :style="{ width: `${studentProfile.internship_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ studentProfile.internship_ability }}</span>
              </div>
            </div>

            <!-- 技能标签 -->
            <div class="skills-section" v-if="studentProfile">
              <div class="skills-title">
                <i class="bi bi-lightbulb"></i> 核心技能
              </div>
              <div class="skills-cloud">
                <span v-for="(skill, i) in topPersonalSkills" :key="i" class="skill-tag">
                  {{ skill }}
                </span>
              </div>
            </div>

            <button class="btn-change" @click="showStudentPicker">
              <i class="bi bi-arrow-repeat"></i> 更换
            </button>
          </div>
        </div>
      </div>

      <!-- 中间：VS区域 -->
      <div class="vs-zone">
        <div class="vs-connector">
          <div class="connector-line top"></div>
          <div class="vs-circle" :class="{ active: canCompare, matching: matching }">
            <span v-if="!matching">VS</span>
            <i v-else class="bi bi-lightning-charge-fill"></i>
          </div>
          <div class="connector-line bottom"></div>
        </div>
        
        <button 
          class="btn-battle" 
          :disabled="!canCompare || matching"
          @click="startBattle"
        >
          <i :class="matching ? 'bi bi-hourglass-split animate-spin' : 'bi bi-play-fill'"></i>
          <span>{{ matching ? '分析中' : '开始对决' }}</span>
        </button>
      </div>

      <!-- 右侧：岗位画像卡 -->
      <div class="profile-card job" :class="{ selected: selectedJob }">
        <div class="card-glow"></div>
        <div class="card-frame">
          <!-- 卡片头部 -->
          <div class="card-top">
            <span class="card-type">TARGET</span>
            <span class="card-label">岗位画像</span>
          </div>

          <!-- 选择状态 -->
          <div v-if="!selectedJob" class="card-empty" @click="showJobPicker">
            <div class="empty-icon">
              <i class="bi bi-briefcase-fill"></i>
            </div>
            <p>点击选择岗位</p>
          </div>

          <!-- 已选择状态 -->
          <div v-else class="card-content">
            <div class="avatar-section job">
              <div class="avatar-ring">
                <div class="avatar">
                  <i class="bi bi-building"></i>
                </div>
              </div>
              <div class="salary-badge">
                {{ selectedJob.salary_range || '面议' }}
              </div>
            </div>

            <h3 class="card-name">{{ selectedJob.position_name }}</h3>
            <p class="card-title">{{ selectedJob.category || '未分类' }} · {{ selectedJob.level || '不限' }}</p>

            <!-- 能力六边形 -->
            <div class="hex-chart">
              <HexagonChart :values="jobAbilities" color="#06b6d4" />
            </div>

            <!-- 核心属性条 -->
            <div class="stats-bar">
              <div class="stat-item">
                <span class="stat-label">学习力</span>
                <div class="stat-track cyan">
                  <div class="stat-fill" :style="{ width: `${selectedJob.learning_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ selectedJob.learning_ability || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">创新力</span>
                <div class="stat-track cyan">
                  <div class="stat-fill" :style="{ width: `${selectedJob.innovation_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ selectedJob.innovation_ability || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">执行力</span>
                <div class="stat-track cyan">
                  <div class="stat-fill" :style="{ width: `${selectedJob.internship_ability * 10}%` }"></div>
                </div>
                <span class="stat-value">{{ selectedJob.internship_ability || 0 }}</span>
              </div>
            </div>

            <!-- 技能标签 -->
            <div class="skills-section">
              <div class="skills-title">
                <i class="bi bi-tools"></i> 技能要求
              </div>
              <div class="skills-cloud">
                <span v-for="(skill, i) in topJobSkills" :key="i" class="skill-tag">
                  {{ skill }}
                </span>
              </div>
            </div>

            <button class="btn-change" @click="showJobPicker">
              <i class="bi bi-arrow-repeat"></i> 更换
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 查看结果按钮（浮动） -->
    <transition name="fade-scale">
      <button 
        v-if="hasResult && !showResultModal" 
        class="view-result-fab"
        @click="showResultModal = true"
      >
        <i class="bi bi-trophy-fill"></i>
        <span>查看对决结果</span>
        <span class="score-badge">{{ overallScore }}分</span>
      </button>
    </transition>

    <!-- 对决结果弹窗 -->
    <transition name="modal-fade">
      <div v-if="showResultModal && matchResult" class="result-modal" @click.self="showResultModal = false">
        <div class="result-dialog">
          <div class="result-header">
            <h2>
              <i class="bi bi-trophy-fill"></i>
              对决结果
            </h2>
            <button class="btn-close" @click="showResultModal = false">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>

          <div class="result-body">
            <!-- 综合评分 -->
            <div class="score-hero">
              <div class="score-ring" :class="scoreLevel.class">
                <svg viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="54" class="ring-bg" />
                  <circle cx="60" cy="60" r="54" class="ring-fill"
                    :stroke-dasharray="`${overallScore * 3.39} 339`" />
                </svg>
                <div class="score-inner">
                  <span class="score-num">{{ overallScore }}</span>
                  <span class="score-label">匹配度</span>
                </div>
              </div>
              <div class="score-verdict">
                <span class="verdict-tag" :class="scoreLevel.class">{{ scoreLevel.text }}</span>
                <p class="verdict-desc">{{ scoreLevel.desc }}</p>
              </div>
            </div>

            <!-- 维度雷达对比 -->
            <div class="radar-section">
              <h4><i class="bi bi-radar"></i> 能力雷达对比</h4>
              <div class="radar-wrap">
                <RadarChart :series="radarSeries" :indicators="radarIndicators" height="240px" />
              </div>
              <div class="radar-legend">
                <span class="legend personal"><span class="dot"></span>个人能力</span>
                <span class="legend job"><span class="dot"></span>岗位要求</span>
              </div>
            </div>

            <!-- 维度评分条 -->
            <div class="dimension-bars">
              <div v-for="dim in dimensions" :key="dim.key" class="dim-row">
                <span class="dim-name">{{ dim.label }}</span>
                <div class="dim-track">
                  <div class="dim-fill" :class="dim.colorClass" :style="{ width: `${dim.value}%` }"></div>
                </div>
                <span class="dim-value" :class="dim.colorClass">{{ dim.value }}</span>
              </div>
            </div>

            <!-- 技能匹配卡片 -->
            <div class="skill-match-cards">
              <div class="match-card success">
                <div class="card-icon"><i class="bi bi-check-circle-fill"></i></div>
                <div class="card-info">
                  <span class="card-num">{{ matchedSkills.length }}</span>
                  <span class="card-label">已匹配</span>
                </div>
                <div class="card-skills">
                  <span v-for="s in matchedSkills.slice(0, 4)" :key="s">{{ s }}</span>
                  <span v-if="matchedSkills.length > 4" class="more">+{{ matchedSkills.length - 4 }}</span>
                </div>
              </div>

              <div class="match-card warning">
                <div class="card-icon"><i class="bi bi-exclamation-triangle-fill"></i></div>
                <div class="card-info">
                  <span class="card-num">{{ missingSkills.length }}</span>
                  <span class="card-label">待补充</span>
              </div>
              <div class="card-skills">
                <span v-for="s in missingSkills.slice(0, 4)" :key="s">{{ s }}</span>
                <span v-if="missingSkills.length > 4" class="more">+{{ missingSkills.length - 4 }}</span>
              </div>
            </div>

            <div class="match-card info">
              <div class="card-icon"><i class="bi bi-star-fill"></i></div>
              <div class="card-info">
                <span class="card-num">{{ extraSkills.length }}</span>
                <span class="card-label">额外优势</span>
              </div>
              <div class="card-skills">
                <span v-for="s in extraSkills.slice(0, 4)" :key="s">{{ s }}</span>
                <span v-if="extraSkills.length > 4" class="more">+{{ extraSkills.length - 4 }}</span>
              </div>
            </div>
          </div>

          <!-- AI建议 -->
          <div class="ai-advice" v-if="recommendations.length">
            <h4><i class="bi bi-robot"></i> AI 改进建议</h4>
            <ul class="advice-list">
              <li v-for="(rec, i) in recommendations" :key="i">
                <span class="num">{{ i + 1 }}</span>
                <span class="text">{{ rec }}</span>
              </li>
            </ul>
          </div>

          <!-- 操作按钮 -->
          <div class="result-actions">
            <router-link :to="`/reports/${selectedStudentId}`" class="btn primary">
              <i class="bi bi-file-earmark-text"></i> 查看报告
            </router-link>
            <router-link to="/planning" class="btn secondary">
              <i class="bi bi-signpost-split"></i> 规划中心
            </router-link>
            <button class="btn outline" @click="resetBattle">
              <i class="bi bi-arrow-counterclockwise"></i> 重新对决
            </button>
          </div>
        </div>
      </div>
    </div>
    </transition>

    <!-- 学生选择弹窗 -->
    <transition name="modal-fade">
      <div v-if="pickerType === 'student'" class="picker-modal" @click.self="closePicker">
        <div class="picker-content">
          <div class="picker-header">
            <h3><i class="bi bi-person-lines-fill"></i> 选择学生档案</h3>
            <button class="btn-close" @click="closePicker"><i class="bi bi-x-lg"></i></button>
          </div>
          <div class="picker-search">
            <i class="bi bi-search"></i>
            <input v-model="searchQuery" placeholder="搜索姓名或专业..." />
          </div>
          <div class="picker-list">
            <div 
              v-for="s in filteredStudents" 
              :key="s.id" 
              class="picker-item"
              :class="{ active: String(s.id) === String(selectedStudentId) }"
              @click="selectStudent(s)"
            >
              <div class="item-avatar">{{ s.name?.charAt(0) }}</div>
              <div class="item-info">
                <span class="item-name">{{ s.name }}</span>
                <span class="item-meta">{{ s.education }} · {{ s.major }}</span>
              </div>
              <i v-if="String(s.id) === String(selectedStudentId)" class="bi bi-check-circle-fill"></i>
            </div>
            <div v-if="!filteredStudents.length" class="picker-empty">
              暂无匹配的学生档案
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 岗位选择弹窗 -->
    <transition name="modal-fade">
      <div v-if="pickerType === 'job'" class="picker-modal" @click.self="closePicker">
        <div class="picker-content">
          <div class="picker-header">
            <h3><i class="bi bi-briefcase-fill"></i> 选择目标岗位</h3>
            <button class="btn-close" @click="closePicker"><i class="bi bi-x-lg"></i></button>
          </div>
          <div class="picker-search">
            <i class="bi bi-search"></i>
            <input v-model="searchQuery" placeholder="搜索岗位名称..." />
          </div>
          <div class="picker-list">
            <div 
              v-for="j in filteredJobs" 
              :key="j.id" 
              class="picker-item job"
              :class="{ active: String(j.id) === String(selectedJobId) }"
              @click="selectJob(j)"
            >
              <div class="item-avatar job"><i class="bi bi-briefcase"></i></div>
              <div class="item-info">
                <span class="item-name">{{ j.position_name }}</span>
                <span class="item-meta">{{ j.category }} · {{ j.salary_range || '面议' }}</span>
              </div>
              <i v-if="String(j.id) === String(selectedJobId)" class="bi bi-check-circle-fill"></i>
            </div>
            <div v-if="!filteredJobs.length" class="picker-empty">
              暂无匹配的岗位画像
            </div>
          </div>
        </div>
      </div>
    </transition>
    </main>

    <!-- 右侧岗位画像详情面板 -->
    <transition name="panel-slide-right">
      <aside v-if="showJobDetail && selectedJob" class="side-panel right-panel">
        <div class="panel-header">
          <h3><i class="bi bi-briefcase"></i> 岗位画像</h3>
          <button class="btn-close" @click="showJobDetail = false"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="panel-body">
          <!-- 基本信息 -->
          <div class="job-hero-compact">
            <div class="job-logo"><i class="bi bi-building"></i></div>
            <div class="job-info">
              <h4>{{ selectedJob.position_name }}</h4>
              <p>{{ selectedJob.category }} · {{ selectedJob.level || '不限' }}</p>
            </div>
          </div>
          <div class="job-salary-badge">{{ selectedJob.salary_range || '面议' }}</div>

          <!-- 任职要求 -->
          <div class="section-block">
            <h5><i class="bi bi-list-check"></i> 任职要求</h5>
            <div class="req-cards">
              <div class="req-card"><span class="label">学历</span><span class="value">{{ selectedJob.education_req || '不限' }}</span></div>
              <div class="req-card"><span class="label">经验</span><span class="value">{{ selectedJob.experience_req || '不限' }}</span></div>
            </div>
          </div>

          <!-- 能力模型 -->
          <div class="section-block">
            <h5><i class="bi bi-hexagon"></i> 能力模型</h5>
            <div class="radar-compact">
              <RadarChart :series="jobRadarSeries" :indicators="abilityLabels" height="180px" />
            </div>
          </div>

          <!-- 技能要求 -->
          <div class="section-block">
            <h5><i class="bi bi-tools"></i> 技能要求</h5>
            <div class="skill-chips cyan">
              <span v-for="(skill, i) in allJobSkills" :key="i" class="chip">{{ skill }}</span>
            </div>
          </div>

          <!-- 职业路径 -->
          <div class="section-block">
            <h5><i class="bi bi-signpost-split"></i> 职业发展</h5>
            <div class="career-timeline">
              <div class="timeline-item" v-for="(step, i) in careerPathSteps" :key="i" :class="{ current: i === 0 }">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <span class="title">{{ step.title }}</span>
                  <span class="meta">{{ step.years }} · {{ step.salary }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="panel-footer">
            <router-link :to="`/jobs/profiles/${selectedJobId}`" class="btn-panel primary">
              <i class="bi bi-box-arrow-up-right"></i> 完整画像
            </router-link>
            <button class="btn-panel outline" @click="showJobDetail = false; showJobPicker()">
              <i class="bi bi-arrow-repeat"></i> 更换
            </button>
          </div>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import {
  getJobProfiles,
  getStudent,
  getStudents,
  runSingleMatching,
  generateStudentProfile as apiGenerateProfile, 
} from '@/api'
import RadarChart from '@/components/RadarChart.vue'
import HexagonChart from '@/components/charts/HexagonChart.vue'

const toast = inject('toast', null)

// 基础数据
const students = ref([])
const jobProfiles = ref([])
const loading = ref(false)

// 选中状态
const selectedStudentId = ref('')
const selectedJobId = ref('')
const studentProfile = ref(null)
const matchResult = ref(null)

// UI状态
const pickerType = ref(null) // 'student' | 'job' | null
const searchQuery = ref('')
const generating = ref(false)
const matching = ref(false)
const showPersonalDetail = ref(false)
const showJobDetail = ref(false)
const showResultModal = ref(false)

// 是否有对决结果
const hasResult = computed(() => !!matchResult.value)

// 计算属性
const selectedStudent = computed(() => 
  students.value.find(s => String(s.id) === String(selectedStudentId.value))
)

const selectedJob = computed(() => 
  jobProfiles.value.find(j => String(j.id) === String(selectedJobId.value))
)

const canCompare = computed(() => 
  selectedStudentId.value && selectedJobId.value && studentProfile.value
)

const profileLevel = computed(() => {
  if (!studentProfile.value) return 1
  const score = studentProfile.value.competitiveness_score || 0
  return Math.max(1, Math.min(10, Math.ceil(score / 10)))
})

// 能力数据
const abilityKeys = ['learning_ability', 'innovation_ability', 'communication_skill', 'teamwork_ability', 'pressure_resistance', 'internship_ability']
const abilityLabels = ['学习力', '创新力', '沟通力', '协作力', '抗压力', '执行力']

const personalAbilities = computed(() => 
  abilityKeys.map(k => Number(studentProfile.value?.[k] || 0))
)

const jobAbilities = computed(() => 
  abilityKeys.map(k => Number(selectedJob.value?.[k] || 0))
)

// 技能
const topPersonalSkills = computed(() => 
  (studentProfile.value?.technical_skills || []).slice(0, 6)
)

const topJobSkills = computed(() => 
  (selectedJob.value?.technical_skills || []).slice(0, 6)
)

// 搜索过滤
const filteredStudents = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return students.value
  return students.value.filter(s => 
    s.name?.toLowerCase().includes(q) || 
    s.major?.toLowerCase().includes(q)
  )
})

const filteredJobs = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return jobProfiles.value
  return jobProfiles.value.filter(j => 
    j.position_name?.toLowerCase().includes(q) || 
    j.category?.toLowerCase().includes(q)
  )
})

// 匹配结果计算
const overallScore = computed(() => 
  Math.round(Number(matchResult.value?.overall_score || 0))
)

const scoreLevel = computed(() => {
  const score = overallScore.value
  if (score >= 80) return { text: '高度匹配', class: 'high', desc: '你的能力与岗位高度契合，可直接投递' }
  if (score >= 60) return { text: '基本匹配', class: 'medium', desc: '存在一定差距，建议针对性提升' }
  return { text: '需要提升', class: 'low', desc: '差距较大，建议制定系统学习计划' }
})

const dimensions = computed(() => [
  { key: 'basic_score', label: '基础匹配', value: Math.round(Number(matchResult.value?.basic_score || 0)), colorClass: 'violet' },
  { key: 'skill_score', label: '技能匹配', value: Math.round(Number(matchResult.value?.skill_score || 0)), colorClass: 'cyan' },
  { key: 'quality_score', label: '素养匹配', value: Math.round(Number(matchResult.value?.quality_score || 0)), colorClass: 'green' },
  { key: 'potential_score', label: '潜力评估', value: Math.round(Number(matchResult.value?.potential_score || 0)), colorClass: 'orange' }
])

// 雷达图
const radarIndicators = computed(() => abilityLabels)
const radarSeries = computed(() => {
  if (!matchResult.value) return []
  return [
    { name: '个人能力', values: personalAbilities.value, color: '#8b5cf6' },
    { name: '岗位要求', values: jobAbilities.value, color: '#06b6d4' }
  ]
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

const recommendations = computed(() => matchResult.value?.recommendations || [])

// SWOT分析数据
const swotStrengths = computed(() => {
  if (!studentProfile.value) return []
  const abilities = abilityKeys.map((k, i) => ({ label: abilityLabels[i], value: studentProfile.value[k] || 0 }))
  const sorted = [...abilities].sort((a, b) => b.value - a.value)
  return sorted.slice(0, 2).map(a => `${a.label}突出 (${a.value}/10)`)
})

const swotWeaknesses = computed(() => {
  if (!studentProfile.value) return []
  const abilities = abilityKeys.map((k, i) => ({ label: abilityLabels[i], value: studentProfile.value[k] || 0 }))
  const sorted = [...abilities].sort((a, b) => a.value - b.value)
  return sorted.slice(0, 2).map(a => `${a.label}需提升 (${a.value}/10)`)
})

// 个人雷达数据
const personalRadarSeries = computed(() => [{
  name: '个人能力',
  values: personalAbilities.value,
  color: '#8b5cf6'
}])

// 岗位雷达数据
const jobRadarSeries = computed(() => [{
  name: '岗位要求',
  values: jobAbilities.value,
  color: '#06b6d4'
}])

// 完整技能列表
const allPersonalSkills = computed(() => studentProfile.value?.technical_skills || [])
const allJobSkills = computed(() => selectedJob.value?.technical_skills || [])

// 职业路径
const careerPathSteps = computed(() => {
  if (!selectedJob.value) return []
  const baseName = selectedJob.value.position_name || '岗位'
  return [
    { title: baseName, years: '0-2年', salary: selectedJob.value.salary_range || '8-12K' },
    { title: `高级${baseName}`, years: '3-5年', salary: '15-25K' },
    { title: '技术专家/经理', years: '5-8年', salary: '25-40K' },
    { title: '总监/架构师', years: '8年+', salary: '40K+' }
  ]
})

// 方法
function showStudentPicker() {
  searchQuery.value = ''
  pickerType.value = 'student'
}

function showJobPicker() {
  searchQuery.value = ''
  pickerType.value = 'job'
}

function closePicker() {
  pickerType.value = null
}

async function selectStudent(student) {
  selectedStudentId.value = String(student.id)
  studentProfile.value = null
  matchResult.value = null
  closePicker()
  
  try {
    const response = await getStudent(student.id)
    studentProfile.value = response.data?.profile || null
  } catch (error) {
    console.error('Load student profile failed:', error)
  }
}

function selectJob(job) {
  selectedJobId.value = String(job.id)
  matchResult.value = null
  closePicker()
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
    toast?.(error?.response?.data?.message || '画像生成失败', 'danger')
  } finally {
    generating.value = false
  }
}

async function regenerateProfile() {
  if (!selectedStudentId.value || generating.value) return
  generating.value = true
  try {
    const response = await apiGenerateProfile(selectedStudentId.value)
    if (response.data?.success) {
      studentProfile.value = response.data.data
      toast?.('画像重新生成成功！', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '画像重新生成失败', 'danger')
  } finally {
    generating.value = false
  }
}

async function startBattle() {
  if (!canCompare.value || matching.value) return
  matching.value = true
  try {
    const response = await runSingleMatching(selectedStudentId.value, selectedJobId.value)
    if (response.data?.success) {
      matchResult.value = response.data.data
      // 对决完成后自动显示结果弹窗
      showResultModal.value = true
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '对比分析失败', 'danger')
  } finally {
    matching.value = false
  }
}

// 重新对决（清除结果）
function resetBattle() {
  matchResult.value = null
  showResultModal.value = false
}

async function loadData() {
  loading.value = true
  try {
    const [jobsRes, studentsRes] = await Promise.all([
      getJobProfiles(),
      getStudents()
    ])
    jobProfiles.value = jobsRes.data?.profiles || []
    students.value = studentsRes.data || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '数据加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.arena-container {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow-x: hidden;
  background: var(--brand-bg, #050509);
}

/* 三栏布局过渡 */
.arena-container.panel-left-open .arena-main {
  margin-left: 0;
}

.arena-container.panel-right-open .arena-main {
  margin-right: 0;
}

/* 主内容区 */
.arena-main {
  flex: 1;
  padding: 24px;
  transition: margin 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 侧边面板基础 */
.side-panel {
  width: 360px;
  background: var(--color-brand-surface, var(--brand-surface, #0f0f1a));
  border: 1px solid var(--brand-border, rgba(139, 92, 246, 0.15));
  display: flex;
  flex-direction: column;
  z-index: 10;
  flex-shrink: 0;
}

.left-panel {
  border-right: 1px solid var(--brand-border, rgba(139, 92, 246, 0.2));
  background: var(--arena-left-panel-bg, linear-gradient(135deg, rgba(139, 92, 246, 0.02), transparent));
}

.right-panel {
  border-left: 1px solid var(--brand-border, rgba(6, 182, 212, 0.2));
  background: var(--arena-right-panel-bg, linear-gradient(135deg, transparent, rgba(6, 182, 212, 0.02)));
}

/* 面板过渡动画 */
.panel-slide-left-enter-active,
.panel-slide-left-leave-active,
.panel-slide-right-enter-active,
.panel-slide-right-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.panel-slide-left-enter-from,
.panel-slide-left-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.panel-slide-right-enter-from,
.panel-slide-right-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* 面板头部 */
.side-panel .panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
  flex-shrink: 0;
}

.left-panel .panel-header {
  background: rgba(139, 92, 246, 0.05);
}

.right-panel .panel-header {
  background: rgba(6, 182, 212, 0.05);
  border-color: rgba(6, 182, 212, 0.1);
}

.side-panel .panel-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.left-panel .panel-header h3 i {
  color: #8b5cf6;
}

.right-panel .panel-header h3 i {
  color: #06b6d4;
}

/* 面板内容 */
.side-panel .panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 个人画像紧凑Hero */
.profile-hero-compact {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 14px;
  margin-bottom: 12px;
}

.profile-hero-compact .hero-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.profile-hero-compact .hero-info h4 {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.profile-hero-compact .hero-info p {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 分数徽章 */
.score-badges {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.score-badges .badge-item {
  flex: 1;
  text-align: center;
  padding: 10px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 10px;
  border: 1px solid rgba(139, 92, 246, 0.15);
}

.score-badges .badge-item .num {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: #a78bfa;
}

.score-badges .badge-item .label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 区块样式 */
.section-block {
  margin-bottom: 16px;
}

.section-block h5 {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.left-panel .section-block h5 i {
  color: #8b5cf6;
}

.right-panel .section-block h5 i {
  color: #06b6d4;
}

/* SWOT卡片 */
.swot-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.swot-card {
  padding: 12px;
  border-radius: 10px;
}

.swot-card.strength {
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.swot-card.weakness {
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.swot-card .card-title {
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.swot-card.strength .card-title {
  color: #34d399;
}

.swot-card.weakness .card-title {
  color: #fbbf24;
}

.swot-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.swot-card li {
  font-size: 11px;
  color: var(--color-brand-text, #e2e8f0);
  padding: 3px 0;
  padding-left: 10px;
  position: relative;
}

.swot-card li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 3px;
  border-radius: 50%;
}

.swot-card.strength li::before {
  background: #34d399;
}

.swot-card.weakness li::before {
  background: #fbbf24;
}

/* 雷达图紧凑 */
.radar-compact {
  min-height: 180px;
}

/* 技能chips */
.skill-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-chips .chip {
  padding: 5px 10px;
  font-size: 11px;
  border-radius: 6px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.skill-chips.cyan .chip {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

/* 岗位紧凑Hero */
.job-hero-compact {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(6, 182, 212, 0.08);
  border-radius: 14px;
  margin-bottom: 8px;
}

.job-hero-compact .job-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  flex-shrink: 0;
}

.job-hero-compact .job-info h4 {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.job-hero-compact .job-info p {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.job-salary-badge {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.12);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
  margin-bottom: 16px;
}

/* 要求卡片 */
.req-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.req-card {
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  background: rgba(6, 182, 212, 0.05);
  border-radius: 8px;
}

.req-card .label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 2px;
}

.req-card .value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

/* 职业时间线 */
.career-timeline {
  position: relative;
  padding-left: 20px;
}

.career-timeline::before {
  content: '';
  position: absolute;
  left: 5px;
  top: 6px;
  bottom: 6px;
  width: 2px;
  background: linear-gradient(180deg, #06b6d4, #8b5cf6);
}

.timeline-item {
  position: relative;
  padding: 8px 0;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.timeline-item .timeline-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #06b6d4;
  border: 2px solid var(--color-brand-surface, #0f0f1a);
  flex-shrink: 0;
  margin-left: -22px;
  margin-top: 4px;
}

.timeline-item.current .timeline-dot {
  background: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.timeline-item .timeline-content {
  display: flex;
  flex-direction: column;
}

.timeline-item .title {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.timeline-item .meta {
  font-size: 10px;
  color: var(--color-brand-muted, #64748b);
}

/* 面板底部 */
.panel-footer {
  display: flex;
  gap: 8px;
  padding: 14px 16px;
  background: rgba(139, 92, 246, 0.03);
  border-top: 1px solid rgba(139, 92, 246, 0.1);
  flex-shrink: 0;
}

.right-panel .panel-footer {
  background: rgba(6, 182, 212, 0.03);
  border-color: rgba(6, 182, 212, 0.1);
}

.btn-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
}

.btn-panel.primary {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
}

.right-panel .btn-panel.primary {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.btn-panel.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.right-panel .btn-panel.primary:hover {
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-panel.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-panel.outline {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

.right-panel .btn-panel.outline {
  border-color: rgba(6, 182, 212, 0.3);
  color: #22d3ee;
}

.btn-panel.outline:hover {
  background: rgba(139, 92, 246, 0.1);
}

.right-panel .btn-panel.outline:hover {
  background: rgba(6, 182, 212, 0.1);
}

/* 背景 */
.arena-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
}

.bg-glow.left {
  left: -200px;
  top: 20%;
  background: #8b5cf6;
}

.bg-glow.right {
  right: -200px;
  top: 30%;
  background: #06b6d4;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* 标题 */
.arena-header {
  text-align: center;
  margin-bottom: 48px;
  position: relative;
  z-index: 1;
}

.arena-title {
  font-size: 36px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.arena-title .icon {
  font-size: 40px;
}

.arena-title .text {
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.arena-title .badge {
  font-size: 11px;
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 6px;
  color: #a78bfa;
  font-weight: 600;
  letter-spacing: 1px;
}

.arena-desc {
  font-size: 15px;
  color: var(--color-brand-muted, #64748b);
}

/* 舞台布局 */
.arena-stage {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

@media (max-width: 900px) {
  .arena-stage {
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }
}

/* 角色卡片 */
.profile-card {
  width: 340px;
  min-height: 480px;
  position: relative;
  border-radius: 24px;
  transition: all 0.4s ease;
}

.profile-card .card-glow {
  position: absolute;
  inset: -2px;
  border-radius: 26px;
  opacity: 0;
  transition: opacity 0.4s;
}

.profile-card.personal .card-glow {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

.profile-card.job .card-glow {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.profile-card.selected .card-glow,
.profile-card.ready .card-glow {
  opacity: 1;
}

.card-frame {
  position: relative;
  height: 100%;
  background: var(--color-brand-card, #1a1a2e);
  border-radius: 24px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-type {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  padding: 4px 10px;
  border-radius: 4px;
}

.profile-card.personal .card-type {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.profile-card.job .card-type {
  background: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.card-label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 空状态 */
.card-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px dashed rgba(139, 92, 246, 0.3);
  border-radius: 16px;
  margin: 8px 0;
  transition: all 0.3s;
}

.card-empty:hover {
  border-color: rgba(139, 92, 246, 0.6);
  background: rgba(139, 92, 246, 0.05);
}

.empty-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #8b5cf6;
  margin-bottom: 16px;
}

.card-empty p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

/* 卡片内容 */
.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-section {
  position: relative;
  margin-bottom: 12px;
}

.avatar-ring {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  padding: 3px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

.profile-card.job .avatar-ring {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--color-brand-card, #1a1a2e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: #8b5cf6;
}

.profile-card.job .avatar {
  font-size: 24px;
  color: #06b6d4;
}

.level-badge,
.salary-badge {
  position: absolute;
  bottom: -4px;
  right: -8px;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 8px;
}

.level-badge {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.salary-badge {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.card-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.card-title {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 16px;
}

/* 六边形图 */
.hex-chart {
  width: 160px;
  height: 140px;
  margin-bottom: 12px;
}

.no-profile {
  padding: 20px;
}

.btn-generate {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 属性条 */
.stats-bar {
  width: 100%;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.stat-label {
  width: 48px;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.stat-track {
  flex: 1;
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.stat-track.cyan {
  background: rgba(6, 182, 212, 0.1);
}

.stat-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.stat-track.cyan .stat-fill {
  background: linear-gradient(90deg, #06b6d4, #22d3ee);
}

.stat-value {
  width: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #a78bfa;
  text-align: right;
}

/* 技能 */
.skills-section {
  width: 100%;
  margin-bottom: 12px;
}

.skills-title {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.skills-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tag {
  font-size: 11px;
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 6px;
  color: #a78bfa;
}

.profile-card.job .skill-tag {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.btn-change {
  margin-top: auto;
  padding: 8px 16px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  color: #a78bfa;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-change:hover {
  background: rgba(139, 92, 246, 0.2);
}

/* VS区域 */
.vs-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px 0;
}

.vs-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.connector-line {
  width: 2px;
  height: 40px;
  background: linear-gradient(180deg, transparent, rgba(139, 92, 246, 0.3), transparent);
}

.vs-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
  border: 2px solid rgba(139, 92, 246, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  color: #64748b;
  transition: all 0.3s;
}

.vs-circle.active {
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  border-color: transparent;
  color: white;
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
}

.vs-circle.matching {
  animation: pulse 0.8s ease infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.btn-battle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-battle:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.5);
}

.btn-battle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 查看结果浮动按钮 */
.view-result-fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border: none;
  border-radius: 50px;
  color: #1a1a2e;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(251, 191, 36, 0.4);
  transition: all 0.3s;
  z-index: 50;
}

.view-result-fab:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 40px rgba(251, 191, 36, 0.5);
}

.view-result-fab i {
  font-size: 18px;
}

.view-result-fab .score-badge {
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 20px;
  font-size: 13px;
}

/* 淡入缩放动画 */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

/* 结果弹窗 */
.result-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 20px;
}

.result-dialog {
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(251, 191, 36, 0.2);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(245, 158, 11, 0.05));
  border-bottom: 1px solid rgba(251, 191, 36, 0.15);
  flex-shrink: 0;
}

.result-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.result-header h2 i {
  color: #fbbf24;
}

.btn-close {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.1);
  border: none;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-close:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.result-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* 评分区 */
.score-hero {
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 28px;
  padding: 20px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 16px;
}

.score-ring {
  width: 130px;
  height: 130px;
  position: relative;
  flex-shrink: 0;
}

.score-ring svg {
  transform: rotate(-90deg);
}

.ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.1);
  stroke-width: 8;
}

.ring-fill {
  fill: none;
  stroke-width: 8;
  stroke-linecap: round;
  transition: stroke-dasharray 0.8s ease;
}

.score-ring.high .ring-fill { stroke: #10b981; }
.score-ring.medium .ring-fill { stroke: #f59e0b; }
.score-ring.low .ring-fill { stroke: #ef4444; }

.score-inner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-num {
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.score-label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.score-verdict {
  flex: 1;
}

.verdict-tag {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.verdict-tag.high {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.verdict-tag.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.verdict-tag.low {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.verdict-desc {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

/* 雷达图 */
.radar-section {
  margin-bottom: 24px;
}

.radar-section h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.radar-section h4 i {
  color: #8b5cf6;
}

.radar-wrap {
  min-height: 260px;
}

.radar-legend {
  display: flex;
  justify-content: center;
  gap: 28px;
  margin-top: 8px;
}

.legend {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.legend .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend.personal .dot { background: #8b5cf6; }
.legend.job .dot { background: #06b6d4; }

/* 维度条 */
.dimension-bars {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

@media (max-width: 640px) {
  .dimension-bars {
    grid-template-columns: 1fr;
  }
}

.dim-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 10px;
}

.dim-name {
  width: 64px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.dim-track {
  flex: 1;
  height: 8px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.dim-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.dim-fill.violet { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.dim-fill.cyan { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
.dim-fill.green { background: linear-gradient(90deg, #10b981, #34d399); }
.dim-fill.orange { background: linear-gradient(90deg, #f97316, #fb923c); }

.dim-value {
  width: 32px;
  font-size: 14px;
  font-weight: 600;
  text-align: right;
}

.dim-value.violet { color: #a78bfa; }
.dim-value.cyan { color: #22d3ee; }
.dim-value.green { color: #34d399; }
.dim-value.orange { color: #fb923c; }

/* 技能匹配卡 */
.skill-match-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .skill-match-cards {
    grid-template-columns: 1fr;
  }
}

.match-card {
  background: rgba(139, 92, 246, 0.05);
  border-radius: 14px;
  padding: 16px;
}

.match-card .card-icon {
  font-size: 20px;
  margin-bottom: 8px;
}

.match-card.success .card-icon { color: #10b981; }
.match-card.warning .card-icon { color: #f59e0b; }
.match-card.info .card-icon { color: #06b6d4; }

.match-card .card-info {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 10px;
}

.match-card .card-num {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-brand-text, #e2e8f0);
}

.match-card .card-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.match-card .card-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.match-card .card-skills span {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
}

.match-card.success .card-skills span {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.match-card.warning .card-skills span {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.match-card.info .card-skills span {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.match-card .card-skills .more {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

/* AI建议 */
.ai-advice {
  margin-bottom: 24px;
}

.ai-advice h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-advice h4 i {
  color: #fbbf24;
}

.advice-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.advice-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: rgba(245, 158, 11, 0.05);
  border-radius: 10px;
  margin-bottom: 8px;
}

.advice-list .num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.advice-list .text {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  line-height: 1.5;
}

/* 操作按钮 */
.result-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.result-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.result-actions .btn.primary {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
}

.result-actions .btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.result-actions .btn.secondary {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.result-actions .btn.secondary:hover {
  background: rgba(6, 182, 212, 0.25);
}

.result-actions .btn.outline {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

.result-actions .btn.outline:hover {
  background: rgba(139, 92, 246, 0.1);
}

/* 选择弹窗 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .picker-content,
.modal-fade-leave-to .picker-content {
  transform: translateY(20px) scale(0.95);
}

.picker-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.picker-content {
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.picker-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.picker-header h3 i {
  color: #8b5cf6;
}

.picker-search {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.picker-search i {
  color: #64748b;
}

.picker-search input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.picker-search input::placeholder {
  color: #64748b;
}

.picker-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.picker-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.picker-item:hover {
  background: rgba(139, 92, 246, 0.1);
}

.picker-item.active {
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.item-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.item-avatar.job {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.item-meta {
  display: block;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.picker-item i.bi-check-circle-fill {
  color: #10b981;
  font-size: 18px;
}

.picker-empty {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-brand-muted, #64748b);
  font-size: 14px;
}

/* 头部操作按钮 */
.header-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  color: #a78bfa;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
}

.action-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.action-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.action-btn.cyan {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.action-btn.cyan:hover {
  background: rgba(6, 182, 212, 0.2);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
}

.action-btn.cyan.active {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 16px rgba(6, 182, 212, 0.3);
}

/* 不再需要的滑出面板样式，保留用于其他组件 */
.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-panel-enter-from,
.slide-panel-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.detail-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 420px;
  max-width: 90vw;
  height: 100vh;
  background: var(--color-brand-surface, #0f0f1a);
  border-left: 1px solid rgba(139, 92, 246, 0.2);
  z-index: 200;
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 40px rgba(0, 0, 0, 0.3);
}

.detail-panel.personal {
  border-color: rgba(139, 92, 246, 0.3);
}

.detail-panel.job {
  border-color: rgba(6, 182, 212, 0.3);
}

.panel-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  background: rgba(139, 92, 246, 0.05);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.detail-panel.job .panel-header {
  background: rgba(6, 182, 212, 0.05);
  border-color: rgba(6, 182, 212, 0.1);
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-header h3 i {
  color: #8b5cf6;
}

.detail-panel.job .panel-header h3 i {
  color: #06b6d4;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

/* 个人画像Hero迷你版 */
.profile-hero-mini {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 16px;
  margin-bottom: 20px;
}

.hero-avatar {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.hero-info h4 {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.hero-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

/* 岗位画像Hero迷你版 */
.job-hero-mini {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(6, 182, 212, 0.08);
  border-radius: 16px;
  margin-bottom: 20px;
}

.job-hero-mini .hero-avatar {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

/* SWOT迷你 */
.swot-mini {
  margin-bottom: 20px;
}

.swot-mini h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.swot-mini h5 i {
  color: #8b5cf6;
}

.swot-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.swot-item {
  padding: 14px;
  border-radius: 12px;
}

.swot-item.strengths {
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.swot-item.weaknesses {
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.swot-item h6 {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.swot-item.strengths h6 {
  color: #34d399;
}

.swot-item.weaknesses h6 {
  color: #fbbf24;
}

.swot-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.swot-item li {
  font-size: 12px;
  color: var(--color-brand-text, #e2e8f0);
  padding: 4px 0;
  padding-left: 12px;
  position: relative;
}

.swot-item li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
}

.swot-item.strengths li::before {
  background: #34d399;
}

.swot-item.weaknesses li::before {
  background: #fbbf24;
}

/* 雷达图迷你 */
.radar-mini {
  margin-bottom: 20px;
}

.radar-mini h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.radar-mini h5 i {
  color: #8b5cf6;
}

.detail-panel.job .radar-mini h5 i {
  color: #06b6d4;
}

/* 技能列表 */
.skill-list {
  margin-bottom: 20px;
}

.skill-list h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.skill-list h5 i {
  color: #8b5cf6;
}

.detail-panel.job .skill-list h5 i {
  color: #06b6d4;
}

.skill-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-chip {
  padding: 6px 12px;
  font-size: 12px;
  border-radius: 8px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.detail-panel.job .skill-chip {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

/* 岗位要求 */
.job-requirements {
  margin-bottom: 20px;
}

.job-requirements h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.job-requirements h5 i {
  color: #06b6d4;
}

.req-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.req-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(6, 182, 212, 0.05);
  border-radius: 10px;
}

.req-item i {
  color: #06b6d4;
  font-size: 14px;
}

.req-item span {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

/* 职业路径迷你 */
.career-path-mini {
  margin-bottom: 20px;
}

.career-path-mini h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.career-path-mini h5 i {
  color: #06b6d4;
}

.path-timeline {
  position: relative;
  padding-left: 24px;
}

.path-timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #06b6d4, #8b5cf6);
}

.path-step {
  position: relative;
  padding: 12px 0;
}

.path-step::before {
  content: '';
  position: absolute;
  left: -20px;
  top: 16px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #06b6d4;
  border: 2px solid var(--color-brand-surface, #0f0f1a);
}

.path-step.current::before {
  background: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
}

.step-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.step-years {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 面板操作 */
.panel-actions {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  background: rgba(139, 92, 246, 0.05);
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.detail-panel.job .panel-actions {
  background: rgba(6, 182, 212, 0.05);
  border-color: rgba(6, 182, 212, 0.1);
}

.btn-action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-action.primary {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
}

.btn-action.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.btn-action.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-action.secondary {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.btn-action.secondary:hover {
  background: rgba(139, 92, 246, 0.2);
}

.detail-panel.job .btn-action.primary {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.detail-panel.job .btn-action.primary:hover {
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

.detail-panel.job .btn-action.secondary {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.detail-panel.job .btn-action.secondary:hover {
  background: rgba(6, 182, 212, 0.2);
}

/* 详情区块 */
.detail-section {
  margin-bottom: 20px;
}

.detail-section h5 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-section h5 i {
  color: #8b5cf6;
}

.detail-panel.job .detail-section h5 i {
  color: #06b6d4;
}

/* 个人画像hero扩展 */
.hero-scores {
  display: flex;
  gap: 12px;
  margin-left: auto;
}

.hero-scores .score {
  text-align: center;
  padding: 8px 12px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 10px;
}

.hero-scores .score span {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #a78bfa;
}

.hero-scores .score {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 岗位hero */
.job-hero-mini {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(6, 182, 212, 0.08);
  border-radius: 16px;
}

.job-logo {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: white;
  flex-shrink: 0;
}

.job-info h4 {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.job-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.job-salary {
  margin-left: auto;
  font-size: 16px;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 6px 12px;
  border-radius: 8px;
}

/* 要求网格 */
.req-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.req-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(6, 182, 212, 0.05);
  border-radius: 10px;
}

.req-item .label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.req-item .value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

/* SWOT样式调整 */
.swot-mini .swot-label {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.swot-mini .swot-item.strength {
  background: rgba(16, 185, 129, 0.08);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.swot-mini .swot-item.strength .swot-label {
  color: #34d399;
}

.swot-mini .swot-item.weakness {
  background: rgba(245, 158, 11, 0.08);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.swot-mini .swot-item.weakness .swot-label {
  color: #fbbf24;
}

.swot-mini .swot-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.swot-mini .swot-item li {
  font-size: 12px;
  color: var(--color-brand-text, #e2e8f0);
  padding: 4px 0;
  padding-left: 12px;
  position: relative;
}

.swot-mini .swot-item li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
}

.swot-mini .swot-item.strength li::before {
  background: #34d399;
}

.swot-mini .swot-item.weakness li::before {
  background: #fbbf24;
}

/* 职业路径样式 */
.career-path-mini {
  padding-left: 20px;
  position: relative;
}

.career-path-mini::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 6px;
  bottom: 6px;
  width: 2px;
  background: linear-gradient(180deg, #06b6d4, #8b5cf6);
}

.path-step {
  position: relative;
  padding: 10px 0;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.path-step .step-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #06b6d4;
  border: 2px solid var(--color-brand-surface, #0f0f1a);
  flex-shrink: 0;
  margin-left: -25px;
  margin-top: 4px;
}

.path-step.current .step-dot {
  background: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
}

.path-step .step-info {
  display: flex;
  flex-direction: column;
}

.path-step .step-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.path-step .step-meta {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 技能chip青色变体 */
.skill-chip.cyan {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

/* 按钮outline变体 */
.btn-action.outline {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

.btn-action.outline:hover {
  background: rgba(139, 92, 246, 0.1);
}

.detail-panel.job .btn-action.outline {
  border-color: rgba(6, 182, 212, 0.3);
  color: #22d3ee;
}

.detail-panel.job .btn-action.outline:hover {
  background: rgba(6, 182, 212, 0.1);
}

/* 响应式 - 三栏布局 */
@media (max-width: 1200px) {
  .side-panel {
    width: 320px;
  }
}

@media (max-width: 1024px) {
  .arena-container {
    flex-direction: column;
  }
  
  .side-panel {
    width: 100%;
    max-height: 50vh;
    border: none;
    border-bottom: 1px solid rgba(139, 92, 246, 0.15);
  }
  
  .right-panel {
    border-bottom: none;
    border-top: 1px solid rgba(6, 182, 212, 0.15);
    order: 2;
  }
  
  .arena-main {
    order: 1;
  }
  
  .left-panel {
    order: 0;
  }
}

@media (max-width: 640px) {
  .header-actions {
    flex-wrap: wrap;
  }
  
  .action-btn {
    flex: 1;
    min-width: 140px;
    justify-content: center;
  }
  
  .swot-cards {
    grid-template-columns: 1fr;
  }
  
  .req-cards {
    grid-template-columns: 1fr;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .arena-container {
  background: #f0f9ff !important;
}

:global(html.light) .arena-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .bg-glow.left,
:global(html.light) .bg-glow.right {
  opacity: 0.1;
}

:global(html.light) .bg-glow.left { background: #0891b2; }
:global(html.light) .bg-glow.right { background: #06b6d4; }

:global(html.light) .bg-grid {
  background-image: 
    linear-gradient(rgba(8, 145, 178, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(8, 145, 178, 0.03) 1px, transparent 1px);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .arena-header h1 {
  color: #0c4a6e;
}

:global(html.light) .arena-title .text {
  background: linear-gradient(135deg, #0891b2, #06b6d4) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}

:global(html.light) .arena-title .badge {
  background: rgba(8, 145, 178, 0.15);
  border-color: rgba(8, 145, 178, 0.3);
  color: #0891b2;
}

:global(html.light) .arena-header p {
  color: #64748b;
}

:global(html.light) .action-btn {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.2);
  color: #0891b2;
}

:global(html.light) .action-btn:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .action-btn.primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  color: white;
}

:global(html.light) .left-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .panel-title {
  color: #0c4a6e;
}

:global(html.light) .match-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .match-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .match-card.active {
  border-color: #0891b2;
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .match-title {
  color: #0c4a6e;
}

:global(html.light) .match-company {
  color: #64748b;
}

:global(html.light) .match-score {
  color: #0891b2;
}

:global(html.light) .arena-main {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .main-title {
  color: #0c4a6e;
}

:global(html.light) .job-info h3 {
  color: #0c4a6e;
}

:global(html.light) .job-company {
  color: #64748b;
}

:global(html.light) .job-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .score-card {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .score-label {
  color: #64748b;
}

:global(html.light) .score-value {
  color: #0891b2;
}

:global(html.light) .swot-card {
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .swot-card.strength {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}

:global(html.light) .swot-card.weakness {
  background: rgba(239, 68, 68, 0.03);
  border-color: rgba(239, 68, 68, 0.15);
}

:global(html.light) .swot-card.opportunity {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .swot-card.threat {
  background: rgba(245, 158, 11, 0.05);
  border-color: rgba(245, 158, 11, 0.2);
}

:global(html.light) .swot-title {
  color: #0c4a6e;
}

:global(html.light) .swot-items li {
  color: #475569;
}

:global(html.light) .req-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .req-card.matched {
  border-color: rgba(16, 185, 129, 0.3);
}

:global(html.light) .req-card.missing {
  border-color: rgba(239, 68, 68, 0.2);
}

:global(html.light) .req-name {
  color: #0c4a6e;
}

:global(html.light) .req-status.matched {
  color: #059669;
}

:global(html.light) .req-status.missing {
  color: #dc2626;
}

:global(html.light) .right-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .advice-section h4 {
  color: #0c4a6e;
}

:global(html.light) .advice-item {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .advice-item:hover {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .advice-text {
  color: #475569;
}

:global(html.light) .ai-assistant {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .ai-header h4 {
  color: #0c4a6e;
}

:global(html.light) .ai-message {
  background: rgba(8, 145, 178, 0.08);
  color: #475569;
}

:global(html.light) .ai-input input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .ai-input .btn-send {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
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

/* 卡片元素白天模式 */
:global(html.light) .card-frame {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .profile-card.personal .card-glow {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .profile-card.job .card-glow {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

:global(html.light) .profile-card.personal .card-type {
  background: rgba(8, 145, 178, 0.2);
  color: #0891b2;
}

:global(html.light) .profile-card.job .card-type {
  background: rgba(6, 182, 212, 0.2);
  color: #06b6d4;
}

:global(html.light) .card-name {
  color: #0c4a6e;
}

:global(html.light) .card-title {
  color: #64748b;
}

:global(html.light) .card-empty {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.2);
  color: #64748b;
}

:global(html.light) .card-empty:hover {
  border-color: rgba(8, 145, 178, 0.4);
  background: rgba(8, 145, 178, 0.06);
}

:global(html.light) .card-empty .empty-icon i {
  color: #0891b2;
}

:global(html.light) .btn-change {
  background: rgba(8, 145, 178, 0.1);
  border-color: rgba(8, 145, 178, 0.2);
  color: #0891b2;
}

:global(html.light) .btn-change:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .avatar-ring {
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .profile-card.personal .avatar {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .profile-card.job .avatar {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

:global(html.light) .level-badge {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .vs-circle {
  background: rgba(8, 145, 178, 0.1);
  border-color: rgba(8, 145, 178, 0.3);
  color: #0891b2;
}

:global(html.light) .vs-circle.active {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  color: white;
}

:global(html.light) .connector-line {
  background: linear-gradient(to bottom, rgba(8, 145, 178, 0.2), transparent);
}

:global(html.light) .btn-battle {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-battle:disabled {
  background: rgba(8, 145, 178, 0.3);
}
</style>
