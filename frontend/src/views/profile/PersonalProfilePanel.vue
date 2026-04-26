<template>
  <div class="personal-profile-panel">
    <!-- 顶部统计 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon violet"><i class="bi bi-people-fill"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ students.length }}</span>
          <span class="stat-label">学生档案</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon cyan"><i class="bi bi-person-check-fill"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ profiledCount }}</span>
          <span class="stat-label">已生成画像</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green"><i class="bi bi-trophy-fill"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ avgCompetitiveness }}</span>
          <span class="stat-label">平均竞争力</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange"><i class="bi bi-graph-up-arrow"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ avgCompleteness }}%</span>
          <span class="stat-label">平均完整度</span>
        </div>
      </div>
    </div>

    <div class="main-grid">
      <!-- 左侧: 学生列表 -->
      <div class="student-list-section">
        <div class="section-header">
          <h3><i class="bi bi-person-lines-fill"></i> 学生档案</h3>
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="搜索姓名/专业..." 
            />
          </div>
        </div>

        <div class="filter-bar">
          <button 
            :class="['filter-btn', { active: filterStatus === 'all' }]"
            @click="filterStatus = 'all'"
          >
            全部
          </button>
          <button 
            :class="['filter-btn', { active: filterStatus === 'profiled' }]"
            @click="filterStatus = 'profiled'"
          >
            已画像
          </button>
          <button 
            :class="['filter-btn', { active: filterStatus === 'pending' }]"
            @click="filterStatus = 'pending'"
          >
            待生成
          </button>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="skeleton-card" v-for="i in 3" :key="i"></div>
        </div>

        <div v-else class="student-list">
          <div 
            v-for="student in filteredStudents" 
            :key="student.id"
            :class="['student-card', { active: String(student.id) === String(selectedId) }]"
            @click="selectStudent(student)"
          >
            <div class="student-avatar">
              <span>{{ getInitials(student.name) }}</span>
            </div>
            <div class="student-info">
              <div class="student-name">{{ student.name }}</div>
              <div class="student-meta">
                {{ student.education || '学历未知' }} · {{ student.major || '专业未知' }}
              </div>
              <div class="student-school">{{ student.school || '学校未知' }}</div>
            </div>
            <div class="student-status">
              <span :class="['status-badge', student.has_profile ? 'success' : 'pending']">
                {{ student.has_profile ? '已画像' : '待生成' }}
              </span>
            </div>
          </div>

          <div v-if="!filteredStudents.length" class="empty-state">
            <i class="bi bi-person-x"></i>
            <p>暂无匹配的学生档案</p>
          </div>
        </div>
      </div>

      <!-- 右侧: 画像详情 -->
      <div class="profile-detail-section">
        <template v-if="selectedStudent">
          <!-- 学生基本信息 -->
          <div class="student-header">
            <div class="header-avatar">
              <span>{{ getInitials(selectedStudent.name) }}</span>
              <div class="avatar-glow"></div>
            </div>
            <div class="header-info">
              <h2>{{ selectedStudent.name }}</h2>
              <div class="header-meta">
                <span><i class="bi bi-mortarboard"></i>{{ selectedStudent.education || '学历未知' }}</span>
                <span><i class="bi bi-book"></i>{{ selectedStudent.major || '专业未知' }}</span>
                <span><i class="bi bi-building"></i>{{ selectedStudent.school || '学校未知' }}</span>
              </div>
            </div>
            <div class="header-actions">
              <span :class="['header-badge', profile ? 'success' : 'warning']">
                {{ profile ? '画像已生成' : '待生成画像' }}
              </span>
            </div>
          </div>

          <!-- 未生成画像时 -->
          <div v-if="!profile" class="no-profile-state">
            <div class="no-profile-icon">
              <i class="bi bi-person-gear"></i>
            </div>
            <h3>尚未生成能力画像</h3>
            <p>点击下方按钮，AI将根据简历信息自动生成多维度能力画像</p>
            <button class="btn-generate" :disabled="generating" @click="generateProfile">
              <i :class="['bi', generating ? 'bi-hourglass-split animate-spin' : 'bi-magic']"></i>
              {{ generating ? '生成中...' : '一键生成画像' }}
            </button>
          </div>

          <!-- 已有画像 -->
          <template v-else>
            <!-- 核心指标 -->
            <div class="metrics-row">
              <div class="metric-card primary">
                <div class="metric-ring">
                  <svg viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="8" class="ring-bg" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="8" class="ring-fill"
                      :stroke-dasharray="`${completenessScore * 2.51} 251`"
                      stroke-linecap="round"
                    />
                  </svg>
                  <span class="metric-value">{{ completenessScore }}</span>
                </div>
                <span class="metric-label">画像完整度</span>
              </div>
              <div class="metric-card success">
                <div class="metric-ring">
                  <svg viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="8" class="ring-bg" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="8" class="ring-fill"
                      :stroke-dasharray="`${competitivenessScore * 2.51} 251`"
                      stroke-linecap="round"
                    />
                  </svg>
                  <span class="metric-value">{{ competitivenessScore }}</span>
                </div>
                <span class="metric-label">竞争力评分</span>
              </div>
              <div class="metric-card cyan">
                <div class="metric-big">
                  <span class="big-value">{{ skillCount }}</span>
                  <span class="big-unit">项</span>
                </div>
                <span class="metric-label">技能数量</span>
              </div>
              <div class="metric-card orange">
                <div class="metric-big">
                  <span class="big-value">{{ projectCount + internCount }}</span>
                  <span class="big-unit">项</span>
                </div>
                <span class="metric-label">经历总数</span>
              </div>
            </div>

            <!-- 能力雷达 -->
            <div class="ability-radar-card">
              <div class="card-header">
                <h4><i class="bi bi-radar"></i> 能力雷达图</h4>
                <span class="ability-avg">平均: {{ avgAbility.toFixed(1) }}</span>
              </div>
              <div class="radar-container">
                <RadarChart 
                  :series="radarSeries" 
                  :indicators="radarIndicators" 
                  height="280px" 
                />
              </div>
            </div>

            <!-- 能力详情 -->
            <div class="abilities-detail-card">
              <div class="card-header">
                <h4><i class="bi bi-bar-chart-steps"></i> 能力详情</h4>
              </div>
              <div class="abilities-grid">
                <div v-for="ability in abilitiesDetail" :key="ability.key" class="ability-item">
                  <div class="ability-header">
                    <span class="ability-name">{{ ability.name }}</span>
                    <span :class="['ability-score', ability.level]">{{ ability.value.toFixed(1) }}</span>
                  </div>
                  <div class="ability-bar">
                    <div :class="['bar-fill', ability.level]" :style="{ width: `${ability.value * 10}%` }"></div>
                  </div>
                  <span class="ability-desc">{{ ability.desc }}</span>
                </div>
              </div>
            </div>

            <!-- 技能标签 -->
            <div class="skills-card">
              <div class="card-header">
                <h4><i class="bi bi-code-square"></i> 技能标签</h4>
                <span class="skill-count">{{ skillCount }} 项</span>
              </div>
              <div class="skills-cloud">
                <span 
                  v-for="(skill, idx) in profile.technical_skills || []" 
                  :key="skill"
                  :class="['skill-tag', { highlight: idx < 3 }]"
                >
                  {{ skill }}
                </span>
                <span v-if="!skillCount" class="no-skills">暂无技能标签</span>
              </div>
            </div>

            <!-- 经历概览 -->
            <div class="experience-row">
              <div class="exp-card">
                <div class="exp-header">
                  <i class="bi bi-folder2-open"></i>
                  <span>项目经历</span>
                </div>
                <div class="exp-value">{{ projectCount }}</div>
                <div class="exp-list" v-if="projectCount">
                  <span v-for="(proj, i) in (profile.project_experience || []).slice(0, 2)" :key="i" class="exp-item">
                    {{ proj.name || proj }}
                  </span>
                </div>
              </div>
              <div class="exp-card">
                <div class="exp-header">
                  <i class="bi bi-briefcase"></i>
                  <span>实习经历</span>
                </div>
                <div class="exp-value">{{ internCount }}</div>
                <div class="exp-list" v-if="internCount">
                  <span v-for="(intern, i) in (profile.internship_experience || []).slice(0, 2)" :key="i" class="exp-item">
                    {{ intern.company || intern }}
                  </span>
                </div>
              </div>
              <div class="exp-card">
                <div class="exp-header">
                  <i class="bi bi-patch-check"></i>
                  <span>证书</span>
                </div>
                <div class="exp-value">{{ certCount }}</div>
                <div class="exp-list" v-if="certCount">
                  <span v-for="(cert, i) in (profile.certificates || []).slice(0, 2)" :key="i" class="exp-item">
                    {{ cert }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 操作栏 -->
            <div class="action-bar">
              <button class="btn-secondary" @click="$emit('analyze', profile)">
                <i class="bi bi-graph-up"></i> 深度分析
              </button>
              <router-link :to="`/analysis/compare?student=${selectedStudent.id}`" class="btn-primary">
                <i class="bi bi-arrow-left-right"></i> 去对比
              </router-link>
            </div>
          </template>
        </template>

        <div v-else class="empty-detail">
          <div class="empty-icon">
            <i class="bi bi-person"></i>
          </div>
          <h3>选择一个学生档案</h3>
          <p>从左侧列表中选择学生，查看个人能力画像详情</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import RadarChart from '@/components/RadarChart.vue'

const props = defineProps({
  students: { type: Array, default: () => [] },
  selectedId: { type: [String, Number], default: '' },
  profile: { type: Object, default: null },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['select', 'generate', 'analyze'])

const searchQuery = ref('')
const filterStatus = ref('all')
const generating = ref(false)

// 统计
const profiledCount = computed(() => 
  props.students.filter(s => s.has_profile).length
)

const avgCompetitiveness = computed(() => {
  const profiled = props.students.filter(s => s.competitiveness_score)
  if (!profiled.length) return '-'
  const sum = profiled.reduce((acc, s) => acc + Number(s.competitiveness_score || 0), 0)
  return (sum / profiled.length).toFixed(1)
})

const avgCompleteness = computed(() => {
  const profiled = props.students.filter(s => s.completeness_score)
  if (!profiled.length) return 0
  const sum = profiled.reduce((acc, s) => acc + Number(s.completeness_score || 0), 0)
  return Math.round(sum / profiled.length)
})

// 筛选
const filteredStudents = computed(() => {
  return props.students.filter(student => {
    const matchSearch = !searchQuery.value || 
      student.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      student.major?.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    let matchStatus = true
    if (filterStatus.value === 'profiled') matchStatus = student.has_profile
    else if (filterStatus.value === 'pending') matchStatus = !student.has_profile
    
    return matchSearch && matchStatus
  })
})

// 选中的学生
const selectedStudent = computed(() => 
  props.students.find(s => String(s.id) === String(props.selectedId))
)

// 画像数据
const completenessScore = computed(() => 
  Math.round(Number(props.profile?.completeness_score || 0))
)

const competitivenessScore = computed(() => 
  Math.round(Number(props.profile?.competitiveness_score || 0))
)

const skillCount = computed(() => 
  (props.profile?.technical_skills || []).length
)

const projectCount = computed(() => 
  (props.profile?.project_experience || []).length
)

const internCount = computed(() => 
  (props.profile?.internship_experience || []).length
)

const certCount = computed(() => 
  (props.profile?.certificates || []).length
)

// 能力数据
const abilityMeta = [
  { key: 'innovation_ability', name: '创新能力', desc: '创造性解决问题的能力' },
  { key: 'learning_ability', name: '学习能力', desc: '快速掌握新知识的能力' },
  { key: 'pressure_resistance', name: '抗压能力', desc: '应对压力和挑战的能力' },
  { key: 'communication_skill', name: '沟通能力', desc: '表达和交流的能力' },
  { key: 'teamwork_ability', name: '团队协作', desc: '与他人合作共事的能力' },
  { key: 'internship_ability', name: '实践能力', desc: '动手解决实际问题的能力' }
]

const abilitiesDetail = computed(() => {
  if (!props.profile) return []
  return abilityMeta.map(a => {
    const value = Number(props.profile[a.key] || 0)
    let level = 'low'
    if (value >= 8) level = 'high'
    else if (value >= 6) level = 'medium'
    return { ...a, value, level }
  })
})

const avgAbility = computed(() => {
  if (!abilitiesDetail.value.length) return 0
  const sum = abilitiesDetail.value.reduce((acc, a) => acc + a.value, 0)
  return sum / abilitiesDetail.value.length
})

// 雷达图
const radarIndicators = computed(() => abilityMeta.map(a => a.name))

const radarSeries = computed(() => {
  if (!props.profile) return []
  return [{
    name: '个人能力',
    values: abilityMeta.map(a => Number(props.profile[a.key] || 0)),
    color: '#8b5cf6'
  }]
})

// 方法
function getInitials(name) {
  if (!name) return '?'
  return name.slice(0, 1).toUpperCase()
}

function selectStudent(student) {
  emit('select', String(student.id))
}

function generateProfile() {
  if (!props.selectedId) return
  generating.value = true
  emit('generate', props.selectedId)
  // generating状态由父组件控制
  setTimeout(() => { generating.value = false }, 3000)
}
</script>

<style scoped>
.personal-profile-panel {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 统计行 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-icon.violet { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
.stat-icon.cyan { background: rgba(6, 182, 212, 0.15); color: #06b6d4; }
.stat-icon.green { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.stat-icon.orange { background: rgba(249, 115, 22, 0.15); color: #f97316; }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.stat-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

/* 主网格 */
.main-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

/* 学生列表 */
.student-list-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 20px;
  max-height: 700px;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h3 i {
  color: #8b5cf6;
}

.search-box {
  position: relative;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-brand-muted, #64748b);
  font-size: 14px;
}

.search-box input {
  width: 160px;
  padding: 10px 12px 10px 36px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  color: var(--color-brand-text, #e2e8f0);
  font-size: 13px;
  outline: none;
  transition: all 0.2s;
}

.search-box input:focus {
  border-color: rgba(139, 92, 246, 0.5);
}

.search-box input::placeholder {
  color: var(--color-brand-muted, #64748b);
}

.filter-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: rgba(139, 92, 246, 0.3);
  color: var(--color-brand-text, #e2e8f0);
}

.filter-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-color: transparent;
  color: white;
}

.student-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.student-list::-webkit-scrollbar {
  width: 6px;
}

.student-list::-webkit-scrollbar-track {
  background: rgba(139, 92, 246, 0.05);
  border-radius: 3px;
}

.student-list::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.3);
  border-radius: 3px;
}

.student-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.student-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateX(4px);
}

.student-card.active {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.1));
  border-color: #8b5cf6;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
}

.student-avatar {
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
  flex-shrink: 0;
}

.student-info {
  flex: 1;
  min-width: 0;
}

.student-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.student-meta {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 2px;
}

.student-school {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  opacity: 0.8;
}

.status-badge {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 500;
}

.status-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-badge.pending {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

/* 加载态 */
.loading-state {
  flex: 1;
}

.skeleton-card {
  height: 80px;
  background: linear-gradient(90deg, rgba(139, 92, 246, 0.08) 25%, rgba(139, 92, 246, 0.15) 50%, rgba(139, 92, 246, 0.08) 75%);
  background-size: 200% 100%;
  animation: skeleton 1.5s infinite;
  border-radius: 14px;
  margin-bottom: 10px;
}

@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-brand-muted, #64748b);
}

.empty-state i {
  font-size: 40px;
  margin-bottom: 12px;
}

/* 画像详情区域 */
.profile-detail-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
}

/* 学生头部 */
.student-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 24px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.header-avatar {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: white;
  position: relative;
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  border-radius: 22px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.header-info {
  flex: 1;
}

.header-info h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.header-meta span {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  display: flex;
  align-items: center;
  gap: 6px;
}

.header-meta i {
  color: #8b5cf6;
}

.header-badge {
  font-size: 12px;
  padding: 6px 14px;
  border-radius: 10px;
  font-weight: 500;
}

.header-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.header-badge.warning {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

/* 未生成画像状态 */
.no-profile-state {
  text-align: center;
  padding: 60px 40px;
}

.no-profile-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44px;
  color: #8b5cf6;
  margin: 0 auto 24px;
}

.no-profile-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
}

.no-profile-state p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 28px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.btn-generate {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 指标行 */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .metrics-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.metric-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}

.metric-ring {
  width: 80px;
  height: 80px;
  margin: 0 auto 12px;
  position: relative;
}

.metric-ring svg {
  transform: rotate(-90deg);
}

.ring-bg {
  color: rgba(139, 92, 246, 0.1);
}

.metric-card.primary .ring-fill { color: #8b5cf6; }
.metric-card.success .ring-fill { color: #10b981; }
.metric-card.cyan .ring-fill { color: #06b6d4; }
.metric-card.orange .ring-fill { color: #f97316; }

.metric-value {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.metric-big {
  margin-bottom: 12px;
}

.big-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.big-unit {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-left: 4px;
}

.metric-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

/* 能力雷达卡片 */
.ability-radar-card,
.abilities-detail-card,
.skills-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-header h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h4 i {
  color: #8b5cf6;
}

.ability-avg {
  font-size: 13px;
  color: #a78bfa;
}

.radar-container {
  min-height: 280px;
}

/* 能力详情网格 */
.abilities-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 640px) {
  .abilities-grid {
    grid-template-columns: 1fr;
  }
}

.ability-item {
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.ability-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.ability-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
}

.ability-score {
  font-size: 16px;
  font-weight: 700;
}

.ability-score.high { color: #10b981; }
.ability-score.medium { color: #f59e0b; }
.ability-score.low { color: #ef4444; }

.ability-bar {
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.bar-fill.high { background: linear-gradient(90deg, #10b981, #34d399); }
.bar-fill.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.bar-fill.low { background: linear-gradient(90deg, #ef4444, #f87171); }

.ability-desc {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 技能标签 */
.skill-count {
  font-size: 13px;
  color: #06b6d4;
}

.skills-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-tag {
  padding: 8px 14px;
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 10px;
  font-size: 13px;
  color: #22d3ee;
  transition: all 0.2s;
}

.skill-tag:hover {
  transform: translateY(-2px);
  border-color: rgba(6, 182, 212, 0.4);
}

.skill-tag.highlight {
  background: rgba(249, 115, 22, 0.15);
  border-color: rgba(249, 115, 22, 0.3);
  color: #fb923c;
}

.no-skills {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

/* 经历行 */
.experience-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 640px) {
  .experience-row {
    grid-template-columns: 1fr;
  }
}

.exp-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 14px;
  padding: 18px;
}

.exp-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 10px;
}

.exp-header i {
  color: #8b5cf6;
}

.exp-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
}

.exp-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.exp-item {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 操作栏 */
.action-bar {
  display: flex;
  gap: 14px;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
}

.btn-secondary {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

.btn-secondary:hover {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.5);
}

/* 空详情状态 */
.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
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
  margin-bottom: 20px;
}

.empty-detail h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.empty-detail p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}
</style>
