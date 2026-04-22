<template>
  <div class="profile-compare-panel">
    <!-- 双栏选择区 -->
    <div class="selection-grid">
      <!-- 左侧: 选择学生 -->
      <div class="selection-card student">
        <div class="card-header">
          <div class="header-icon student">
            <i class="bi bi-person-fill"></i>
          </div>
          <h3>选择个人画像</h3>
        </div>
        
        <select v-model="studentId" class="select-input" @change="handleStudentChange">
          <option value="">请选择学生档案</option>
          <option v-for="s in students" :key="s.id" :value="String(s.id)">
            {{ s.name }} · {{ s.education || '学历未知' }} · {{ s.major || '专业未知' }}
          </option>
        </select>

        <div v-if="selectedStudent" class="selected-preview">
          <div class="preview-avatar">
            {{ selectedStudent.name?.slice(0, 1) }}
          </div>
          <div class="preview-info">
            <div class="preview-name">{{ selectedStudent.name }}</div>
            <div class="preview-meta">{{ selectedStudent.education }} · {{ selectedStudent.major }}</div>
          </div>
          <div class="preview-status">
            <span :class="['status-tag', studentProfile ? 'ready' : 'pending']">
              {{ studentProfile ? '画像就绪' : '待生成' }}
            </span>
          </div>
        </div>

        <div v-if="studentProfile" class="profile-mini-stats">
          <div class="mini-stat">
            <span class="mini-value">{{ completenessScore }}</span>
            <span class="mini-label">完整度</span>
          </div>
          <div class="mini-stat">
            <span class="mini-value">{{ competitivenessScore }}</span>
            <span class="mini-label">竞争力</span>
          </div>
          <div class="mini-stat">
            <span class="mini-value">{{ studentSkillCount }}</span>
            <span class="mini-label">技能数</span>
          </div>
        </div>
      </div>

      <!-- 中间: 对比箭头 -->
      <div class="compare-arrow">
        <div class="arrow-line"></div>
        <div class="arrow-icon">
          <i class="bi bi-arrow-left-right"></i>
        </div>
        <div class="arrow-line"></div>
      </div>

      <!-- 右侧: 选择岗位 -->
      <div class="selection-card job">
        <div class="card-header">
          <div class="header-icon job">
            <i class="bi bi-briefcase-fill"></i>
          </div>
          <h3>选择目标岗位</h3>
        </div>
        
        <select v-model="jobId" class="select-input" @change="handleJobChange">
          <option value="">请选择岗位画像</option>
          <option v-for="j in jobProfiles" :key="j.id" :value="String(j.id)">
            {{ j.position_name }} · {{ j.category || '未分类' }} · {{ j.salary_range || '薪资面议' }}
          </option>
        </select>

        <div v-if="selectedJob" class="selected-preview">
          <div class="preview-avatar job">
            <i class="bi bi-briefcase"></i>
          </div>
          <div class="preview-info">
            <div class="preview-name">{{ selectedJob.position_name }}</div>
            <div class="preview-meta">{{ selectedJob.category }} · {{ selectedJob.level }}</div>
          </div>
          <div class="preview-salary">
            {{ selectedJob.salary_range || '面议' }}
          </div>
        </div>

        <div v-if="selectedJob" class="profile-mini-stats">
          <div class="mini-stat">
            <span class="mini-value">{{ selectedJob.education_req || '不限' }}</span>
            <span class="mini-label">学历要求</span>
          </div>
          <div class="mini-stat">
            <span class="mini-value">{{ selectedJob.experience_req || '不限' }}</span>
            <span class="mini-label">经验要求</span>
          </div>
          <div class="mini-stat">
            <span class="mini-value">{{ jobSkillCount }}</span>
            <span class="mini-label">技能要求</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 对比按钮 -->
    <div class="compare-action">
      <button 
        class="btn-compare" 
        :disabled="!canCompare || matching"
        @click="startCompare"
      >
        <i :class="['bi', matching ? 'bi-hourglass-split animate-spin' : 'bi-lightning-fill']"></i>
        {{ matching ? '智能分析中...' : '开始智能对比分析' }}
      </button>
      <p v-if="!canCompare" class="compare-hint">
        <i class="bi bi-info-circle"></i>
        请选择学生档案（需已生成画像）和目标岗位后开始对比
      </p>
    </div>

    <!-- 对比结果 -->
    <transition name="result-fade">
      <div v-if="matchResult" class="compare-result">
        <!-- 综合评分 -->
        <div class="overall-score-section">
          <div class="score-ring-wrap">
            <div class="score-ring" :class="overallLevel.class">
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="currentColor" stroke-width="10" class="ring-bg" />
                <circle cx="60" cy="60" r="52" fill="none" stroke="currentColor" stroke-width="10" class="ring-fill"
                  :stroke-dasharray="`${overallScore * 3.27} 327`"
                  stroke-linecap="round"
                />
              </svg>
              <div class="score-value">
                <span class="value">{{ overallScore }}</span>
                <span class="label">综合匹配</span>
              </div>
            </div>
          </div>
          <div class="score-details">
            <div v-for="dim in dimensionScores" :key="dim.key" class="dim-item">
              <div class="dim-header">
                <span class="dim-name">{{ dim.label }}</span>
                <span :class="['dim-value', dim.colorClass]">{{ dim.value }}</span>
              </div>
              <div class="dim-bar">
                <div :class="['dim-fill', dim.colorClass]" :style="{ width: dim.value + '%' }"></div>
              </div>
            </div>
          </div>
          <div class="score-verdict">
            <span :class="['verdict-badge', overallLevel.class]">{{ overallLevel.text }}</span>
            <p class="verdict-desc">{{ overallLevel.desc }}</p>
          </div>
        </div>

        <!-- 雷达对比 -->
        <div class="radar-compare-section">
          <div class="section-header">
            <h4><i class="bi bi-radar"></i> 能力雷达对比</h4>
          </div>
          <div class="radar-container">
            <RadarChart :series="radarSeries" :indicators="radarIndicators" height="320px" />
          </div>
          <div class="radar-legend">
            <span class="legend-item student"><span class="dot"></span> 个人能力</span>
            <span class="legend-item job"><span class="dot"></span> 岗位要求</span>
          </div>
        </div>

        <!-- 能力差值 -->
        <div class="ability-diff-section">
          <div class="section-header">
            <h4><i class="bi bi-bar-chart-steps"></i> 能力差值分析</h4>
            <span class="diff-summary">
              <span class="positive">{{ positiveDiffs }} 项优势</span>
              <span class="separator">|</span>
              <span class="negative">{{ negativeDiffs }} 项待提升</span>
            </span>
          </div>
          <div class="diff-grid">
            <div v-for="item in abilityDiffs" :key="item.name" class="diff-item">
              <div class="diff-name">{{ item.name }}</div>
              <div class="diff-bar-wrap">
                <div class="diff-bar">
                  <div 
                    :class="['diff-fill', item.diff >= 0 ? 'positive' : 'negative']"
                    :style="{ width: `${Math.min(100, Math.abs(item.diff) * 10)}%` }"
                  ></div>
                </div>
                <span :class="['diff-value', item.diff >= 0 ? 'positive' : 'negative']">
                  {{ item.diff >= 0 ? '+' : '' }}{{ item.diff.toFixed(1) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 技能匹配 -->
        <div class="skills-match-section">
          <div class="skills-grid">
            <div class="skill-card matched">
              <div class="skill-card-header">
                <i class="bi bi-check-circle-fill"></i>
                <span>已匹配技能</span>
                <span class="count">{{ matchedSkills.length }}</span>
              </div>
              <div class="skill-tags">
                <span v-for="skill in matchedSkills" :key="skill" class="skill-tag">{{ skill }}</span>
                <span v-if="!matchedSkills.length" class="no-skill">暂无匹配</span>
              </div>
            </div>

            <div class="skill-card missing">
              <div class="skill-card-header">
                <i class="bi bi-exclamation-triangle-fill"></i>
                <span>待补技能</span>
                <span class="count">{{ missingSkills.length }}</span>
              </div>
              <div class="skill-tags">
                <span v-for="skill in missingSkills" :key="skill" class="skill-tag">{{ skill }}</span>
                <span v-if="!missingSkills.length" class="no-skill">无技能缺口</span>
              </div>
            </div>

            <div class="skill-card extra">
              <div class="skill-card-header">
                <i class="bi bi-star-fill"></i>
                <span>额外优势</span>
                <span class="count">{{ extraSkills.length }}</span>
              </div>
              <div class="skill-tags">
                <span v-for="skill in extraSkills" :key="skill" class="skill-tag">{{ skill }}</span>
                <span v-if="!extraSkills.length" class="no-skill">暂无额外技能</span>
              </div>
            </div>
          </div>
        </div>

        <!-- AI建议 -->
        <div v-if="recommendations.length" class="ai-suggestions-section">
          <div class="section-header">
            <h4><i class="bi bi-robot"></i> AI 改进建议</h4>
          </div>
          <div class="suggestions-list">
            <div v-for="(rec, i) in recommendations" :key="i" class="suggestion-item">
              <span class="sug-num">{{ i + 1 }}</span>
              <span class="sug-text">{{ rec }}</span>
            </div>
          </div>
        </div>

        <!-- 操作栏 -->
        <div class="result-actions">
          <button class="btn-secondary" @click="resetCompare">
            <i class="bi bi-arrow-counterclockwise"></i> 重新选择
          </button>
          <router-link :to="`/reports/${selectedStudentId}`" class="btn-primary">
            <i class="bi bi-file-earmark-text"></i> 查看完整报告
          </router-link>
          <router-link to="/planning" class="btn-outline">
            <i class="bi bi-signpost-split"></i> 进入规划中心
          </router-link>
        </div>
      </div>
    </transition>

    <!-- 空状态 -->
    <div v-if="!matchResult" class="empty-result">
      <div class="empty-illustration">
        <div class="illustration-circles">
          <div class="circle left"></div>
          <div class="circle right"></div>
          <div class="arrows">
            <i class="bi bi-arrow-left-right"></i>
          </div>
        </div>
      </div>
      <h3>选择画像开始对比</h3>
      <p>选择学生档案和目标岗位后，AI将自动进行多维度对比分析，<br>帮助你精准定位能力差距，制定提升策略</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import RadarChart from '@/components/RadarChart.vue'

const props = defineProps({
  students: { type: Array, default: () => [] },
  jobProfiles: { type: Array, default: () => [] },
  studentProfile: { type: Object, default: null },
  selectedStudentId: { type: [String, Number], default: '' },
  selectedJobId: { type: [String, Number], default: '' },
  matchResult: { type: Object, default: null },
  matching: { type: Boolean, default: false }
})

const emit = defineEmits(['select-student', 'select-job', 'compare'])

const route = useRoute()

const studentId = ref('')
const jobId = ref('')

// 初始化从props或路由参数
onMounted(() => {
  if (props.selectedStudentId) studentId.value = String(props.selectedStudentId)
  if (props.selectedJobId) jobId.value = String(props.selectedJobId)
  
  // 从路由参数初始化
  if (route.query.student) studentId.value = String(route.query.student)
  if (route.query.job) jobId.value = String(route.query.job)
})

// 同步props变化
watch(() => props.selectedStudentId, (val) => {
  if (val) studentId.value = String(val)
})

watch(() => props.selectedJobId, (val) => {
  if (val) jobId.value = String(val)
})

// 计算属性
const selectedStudent = computed(() => 
  props.students.find(s => String(s.id) === studentId.value)
)

const selectedJob = computed(() => 
  props.jobProfiles.find(j => String(j.id) === jobId.value)
)

const canCompare = computed(() => 
  studentId.value && jobId.value && props.studentProfile
)

// 学生画像指标
const completenessScore = computed(() => 
  Math.round(Number(props.studentProfile?.completeness_score || 0))
)

const competitivenessScore = computed(() => 
  Math.round(Number(props.studentProfile?.competitiveness_score || 0))
)

const studentSkillCount = computed(() => 
  (props.studentProfile?.technical_skills || []).length
)

const jobSkillCount = computed(() => 
  (selectedJob.value?.technical_skills || []).length
)

// 匹配结果数据
const overallScore = computed(() => 
  Math.round(Number(props.matchResult?.overall_score || 0))
)

const overallLevel = computed(() => {
  const score = overallScore.value
  if (score >= 80) return { text: '高度匹配', class: 'high', desc: '你的能力与岗位要求高度契合，可以考虑直接投递申请' }
  if (score >= 60) return { text: '基本匹配', class: 'medium', desc: '存在一定差距，建议针对性提升后再申请' }
  return { text: '需要提升', class: 'low', desc: '与目标岗位差距较大，建议制定系统的能力提升计划' }
})

const dimensionScores = computed(() => [
  { key: 'basic_score', label: '基础匹配', value: Math.round(Number(props.matchResult?.basic_score || 0)), colorClass: 'violet' },
  { key: 'skill_score', label: '技能匹配', value: Math.round(Number(props.matchResult?.skill_score || 0)), colorClass: 'cyan' },
  { key: 'quality_score', label: '素养匹配', value: Math.round(Number(props.matchResult?.quality_score || 0)), colorClass: 'green' },
  { key: 'potential_score', label: '潜力评估', value: Math.round(Number(props.matchResult?.potential_score || 0)), colorClass: 'orange' }
])

// 能力雷达
const abilityMeta = [
  { key: 'innovation_ability', name: '创新能力' },
  { key: 'learning_ability', name: '学习能力' },
  { key: 'pressure_resistance', name: '抗压能力' },
  { key: 'communication_skill', name: '沟通能力' },
  { key: 'teamwork_ability', name: '团队协作' },
  { key: 'internship_ability', name: '实践能力' }
]

const radarIndicators = computed(() => abilityMeta.map(a => a.name))

const radarSeries = computed(() => {
  if (!props.matchResult) return []
  return [
    {
      name: '个人能力',
      values: abilityMeta.map(a => Number(props.studentProfile?.[a.key] || 0)),
      color: '#8b5cf6'
    },
    {
      name: '岗位要求',
      values: abilityMeta.map(a => Number(selectedJob.value?.[a.key] || 0)),
      color: '#06b6d4'
    }
  ]
})

// 能力差值
const abilityDiffs = computed(() => {
  if (!props.studentProfile || !selectedJob.value) return []
  return abilityMeta.map(a => {
    const studentVal = Number(props.studentProfile[a.key] || 0)
    const jobVal = Number(selectedJob.value[a.key] || 0)
    return {
      name: a.name,
      student: studentVal,
      job: jobVal,
      diff: studentVal - jobVal
    }
  })
})

const positiveDiffs = computed(() => 
  abilityDiffs.value.filter(d => d.diff >= 0).length
)

const negativeDiffs = computed(() => 
  abilityDiffs.value.filter(d => d.diff < 0).length
)

// 技能匹配
const targetSkills = computed(() => selectedJob.value?.technical_skills || [])
const studentSkills = computed(() => props.studentProfile?.technical_skills || [])

const matchedSkills = computed(() => {
  const targets = targetSkills.value.map(s => String(s).toLowerCase())
  return studentSkills.value.filter(s => {
    const normalized = String(s).toLowerCase()
    return targets.some(t => normalized.includes(t) || t.includes(normalized))
  })
})

const missingSkills = computed(() => {
  const matchedLower = matchedSkills.value.map(s => String(s).toLowerCase())
  const explicit = props.matchResult?.skill_gaps || []
  const fromTarget = targetSkills.value.filter(s => {
    const normalized = String(s).toLowerCase()
    return !matchedLower.some(m => m.includes(normalized) || normalized.includes(m))
  })
  return [...new Set([...explicit, ...fromTarget])]
})

const extraSkills = computed(() => {
  const targetLower = targetSkills.value.map(s => String(s).toLowerCase())
  return studentSkills.value.filter(s => {
    const normalized = String(s).toLowerCase()
    return !targetLower.some(t => normalized.includes(t) || t.includes(normalized))
  })
})

const recommendations = computed(() => props.matchResult?.recommendations || [])

// 方法
function handleStudentChange() {
  emit('select-student', studentId.value)
}

function handleJobChange() {
  emit('select-job', jobId.value)
}

function startCompare() {
  emit('compare')
}

function resetCompare() {
  studentId.value = ''
  jobId.value = ''
  emit('select-student', '')
  emit('select-job', '')
}
</script>

<style scoped>
.profile-compare-panel {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 选择区域网格 */
.selection-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

@media (max-width: 900px) {
  .selection-grid {
    grid-template-columns: 1fr;
  }
  
  .compare-arrow {
    transform: rotate(90deg);
    margin: 16px auto;
  }
}

.selection-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s ease;
}

.selection-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
}

.selection-card.student:hover {
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.15);
}

.selection-card.job:hover {
  box-shadow: 0 0 30px rgba(6, 182, 212, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}

.header-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.header-icon.student {
  background: rgba(139, 92, 246, 0.15);
  color: #8b5cf6;
}

.header-icon.job {
  background: rgba(6, 182, 212, 0.15);
  color: #06b6d4;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.select-input {
  width: 100%;
  padding: 14px 16px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  color: var(--color-brand-text, #e2e8f0);
  font-size: 14px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%238b8b8b' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 12px;
}

.select-input:focus {
  border-color: rgba(139, 92, 246, 0.5);
}

.selected-preview {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 16px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.preview-avatar {
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

.preview-avatar.job {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  font-size: 16px;
}

.preview-info {
  flex: 1;
}

.preview-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.preview-meta {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.status-tag {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 500;
}

.status-tag.ready {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-tag.pending {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.preview-salary {
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
}

.profile-mini-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 16px;
}

.mini-stat {
  text-align: center;
  padding: 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 10px;
}

.mini-value {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.mini-label {
  display: block;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  margin-top: 4px;
}

/* 对比箭头 */
.compare-arrow {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.arrow-line {
  width: 2px;
  height: 40px;
  background: linear-gradient(180deg, transparent, rgba(139, 92, 246, 0.5), transparent);
}

.arrow-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}

/* 对比按钮 */
.compare-action {
  text-align: center;
  margin-bottom: 32px;
}

.btn-compare {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 40px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-compare:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
}

.btn-compare:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.compare-hint {
  margin-top: 14px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

/* 对比结果 */
.result-fade-enter-active {
  animation: resultFadeIn 0.5s ease;
}

@keyframes resultFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.compare-result {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 综合评分区 */
.overall-score-section {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 32px;
  align-items: center;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 28px;
}

@media (max-width: 900px) {
  .overall-score-section {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.score-ring-wrap {
  display: flex;
  justify-content: center;
}

.score-ring {
  width: 140px;
  height: 140px;
  position: relative;
}

.score-ring svg {
  transform: rotate(-90deg);
}

.ring-bg {
  color: rgba(139, 92, 246, 0.1);
}

.score-ring.high .ring-fill { color: #10b981; }
.score-ring.medium .ring-fill { color: #f59e0b; }
.score-ring.low .ring-fill { color: #ef4444; }

.score-value {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-value .value {
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.score-value .label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.score-details {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.dim-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dim-name {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.dim-value {
  font-size: 14px;
  font-weight: 600;
}

.dim-value.violet { color: #a78bfa; }
.dim-value.cyan { color: #22d3ee; }
.dim-value.green { color: #34d399; }
.dim-value.orange { color: #fb923c; }

.dim-bar {
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.dim-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.dim-fill.violet { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.dim-fill.cyan { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
.dim-fill.green { background: linear-gradient(90deg, #10b981, #34d399); }
.dim-fill.orange { background: linear-gradient(90deg, #f97316, #fb923c); }

.score-verdict {
  text-align: center;
}

.verdict-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
}

.verdict-badge.high {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.verdict-badge.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.verdict-badge.low {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.verdict-desc {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  max-width: 200px;
}

/* 雷达对比区 */
.radar-compare-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h4 i {
  color: #8b5cf6;
}

.radar-container {
  min-height: 320px;
}

.radar-legend {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.legend-item .dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-item.student .dot { background: #8b5cf6; }
.legend-item.job .dot { background: #06b6d4; }

/* 能力差值区 */
.ability-diff-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
}

.diff-summary {
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.diff-summary .positive { color: #10b981; }
.diff-summary .negative { color: #ef4444; }
.diff-summary .separator { color: var(--color-brand-muted, #64748b); }

.diff-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 640px) {
  .diff-grid {
    grid-template-columns: 1fr;
  }
}

.diff-item {
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.diff-name {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 10px;
}

.diff-bar-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.diff-bar {
  flex: 1;
  height: 8px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.diff-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.diff-fill.positive { background: linear-gradient(90deg, #10b981, #34d399); }
.diff-fill.negative { background: linear-gradient(90deg, #ef4444, #f87171); }

.diff-value {
  font-size: 14px;
  font-weight: 600;
  min-width: 40px;
  text-align: right;
}

.diff-value.positive { color: #10b981; }
.diff-value.negative { color: #ef4444; }

/* 技能匹配区 */
.skills-match-section {
  margin-bottom: 8px;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 900px) {
  .skills-grid {
    grid-template-columns: 1fr;
  }
}

.skill-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 16px;
  padding: 20px;
}

.skill-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.skill-card.matched .skill-card-header i { color: #10b981; }
.skill-card.missing .skill-card-header i { color: #ef4444; }
.skill-card.extra .skill-card-header i { color: #06b6d4; }

.skill-card-header .count {
  margin-left: auto;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-card .skill-tag {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
}

.skill-card.matched .skill-tag {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.skill-card.missing .skill-tag {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.skill-card.extra .skill-tag {
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.no-skill {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* AI建议区 */
.ai-suggestions-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px;
  background: rgba(245, 158, 11, 0.05);
  border-radius: 12px;
}

.sug-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.sug-text {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  line-height: 1.5;
}

/* 操作栏 */
.result-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary,
.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
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
}

.btn-outline {
  background: transparent;
  border: 1px solid rgba(6, 182, 212, 0.3);
  color: #22d3ee;
}

.btn-outline:hover {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.5);
}

/* 空状态 */
.empty-result {
  text-align: center;
  padding: 60px 20px;
}

.empty-illustration {
  margin-bottom: 28px;
}

.illustration-circles {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  position: relative;
}

.circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  opacity: 0.8;
}

.circle.left {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(139, 92, 246, 0.1));
  border: 2px dashed rgba(139, 92, 246, 0.4);
  animation: pulse-left 2s ease-in-out infinite;
}

.circle.right {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(6, 182, 212, 0.1));
  border: 2px dashed rgba(6, 182, 212, 0.4);
  animation: pulse-right 2s ease-in-out infinite;
}

@keyframes pulse-left {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(-10px); }
}

@keyframes pulse-right {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(10px); }
}

.arrows {
  position: absolute;
  font-size: 24px;
  color: rgba(139, 92, 246, 0.5);
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.empty-result h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 12px;
}

.empty-result p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  line-height: 1.6;
}
</style>
