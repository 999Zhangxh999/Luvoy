<template>
  <div class="job-profile-panel">
    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon cyan"><i class="bi bi-briefcase-fill"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ jobProfiles.length }}</span>
          <span class="stat-label">岗位画像</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon violet"><i class="bi bi-diagram-3-fill"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ categoryCount }}</span>
          <span class="stat-label">岗位类别</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green"><i class="bi bi-fire"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ avgSkillCount }}</span>
          <span class="stat-label">平均技能数</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange"><i class="bi bi-currency-dollar"></i></div>
        <div class="stat-info">
          <span class="stat-value">{{ avgSalary }}</span>
          <span class="stat-label">平均薪资</span>
        </div>
      </div>
    </div>

    <div class="main-grid">
      <!-- 左侧: 岗位列表 -->
      <div class="job-list-section">
        <div class="section-header">
          <h3><i class="bi bi-list-ul"></i> 岗位画像库</h3>
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="搜索岗位名称..." 
            />
          </div>
        </div>

        <div class="filter-bar">
          <button 
            v-for="cat in categories" 
            :key="cat"
            :class="['filter-btn', { active: activeCategory === cat }]"
            @click="activeCategory = cat"
          >
            {{ cat }}
          </button>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="skeleton-card" v-for="i in 3" :key="i"></div>
        </div>

        <div v-else class="job-list">
          <div 
            v-for="job in filteredJobs" 
            :key="job.id"
            :class="['job-card', { active: String(job.id) === String(selectedId) }]"
            @click="selectJob(job)"
          >
            <div class="job-card-header">
              <span class="job-name">{{ job.position_name }}</span>
              <span class="job-salary">{{ job.salary_range || '面议' }}</span>
            </div>
            <div class="job-card-meta">
              <span class="meta-item"><i class="bi bi-tag"></i>{{ job.category || '未分类' }}</span>
              <span class="meta-item"><i class="bi bi-bar-chart"></i>{{ job.level || '未知' }}</span>
            </div>
            <div class="job-card-skills">
              <span 
                v-for="skill in (job.technical_skills || []).slice(0, 3)" 
                :key="skill" 
                class="skill-tag"
              >{{ skill }}</span>
              <span v-if="(job.technical_skills || []).length > 3" class="skill-more">
                +{{ (job.technical_skills || []).length - 3 }}
              </span>
            </div>
          </div>

          <div v-if="!filteredJobs.length" class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>暂无匹配的岗位画像</p>
          </div>
        </div>
      </div>

      <!-- 右侧: 岗位详情 -->
      <div class="job-detail-section">
        <template v-if="selectedJob">
          <div class="detail-header">
            <div class="detail-title">
              <h2>{{ selectedJob.position_name }}</h2>
              <div class="title-badges">
                <span class="badge-category">{{ selectedJob.category }}</span>
                <span class="badge-level">{{ selectedJob.level }}</span>
              </div>
            </div>
            <div class="detail-salary">
              <span class="salary-label">薪资范围</span>
              <span class="salary-value">{{ selectedJob.salary_range || '面议' }}</span>
            </div>
          </div>

          <!-- 能力雷达 -->
          <div class="ability-radar-card">
            <div class="card-header">
              <h4><i class="bi bi-bullseye"></i> 能力要求雷达</h4>
            </div>
            <div class="radar-container">
              <RadarChart 
                :series="radarSeries" 
                :indicators="radarIndicators" 
                height="280px" 
              />
            </div>
          </div>

          <!-- 基本要求 -->
          <div class="requirements-grid">
            <div class="req-card">
              <span class="req-icon"><i class="bi bi-mortarboard"></i></span>
              <span class="req-label">学历要求</span>
              <span class="req-value">{{ selectedJob.education_req || '不限' }}</span>
            </div>
            <div class="req-card">
              <span class="req-icon"><i class="bi bi-clock-history"></i></span>
              <span class="req-label">经验要求</span>
              <span class="req-value">{{ selectedJob.experience_req || '不限' }}</span>
            </div>
            <div class="req-card">
              <span class="req-icon"><i class="bi bi-tools"></i></span>
              <span class="req-label">技能数量</span>
              <span class="req-value">{{ (selectedJob.technical_skills || []).length }} 项</span>
            </div>
            <div class="req-card">
              <span class="req-icon"><i class="bi bi-award"></i></span>
              <span class="req-label">证书要求</span>
              <span class="req-value">{{ (selectedJob.certificates || []).length }} 项</span>
            </div>
          </div>

          <!-- 技能需求 -->
          <div class="skills-card">
            <div class="card-header">
              <h4><i class="bi bi-lightning"></i> 技能需求</h4>
              <span class="skill-count">{{ (selectedJob.technical_skills || []).length }} 项</span>
            </div>
            <div class="skills-grid">
              <div 
                v-for="(skill, idx) in selectedJob.technical_skills || []" 
                :key="skill"
                :class="['skill-item', { hot: idx < 3 }]"
              >
                <span class="skill-name">{{ skill }}</span>
                <span v-if="idx < 3" class="skill-badge">核心</span>
              </div>
            </div>
          </div>

          <!-- 证书要求 -->
          <div v-if="(selectedJob.certificates || []).length" class="certs-card">
            <div class="card-header">
              <h4><i class="bi bi-patch-check"></i> 证书要求</h4>
            </div>
            <div class="certs-list">
              <span v-for="cert in selectedJob.certificates" :key="cert" class="cert-item">
                {{ cert }}
              </span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-bar">
            <button class="btn-secondary" @click="$emit('analyze', selectedJob)">
              <i class="bi bi-graph-up"></i> 深度分析
            </button>
            <router-link :to="`/analysis/compare?job=${selectedJob.id}`" class="btn-primary">
              <i class="bi bi-arrow-left-right"></i> 去对比
            </router-link>
          </div>
        </template>

        <div v-else class="empty-detail">
          <div class="empty-icon">
            <i class="bi bi-briefcase"></i>
          </div>
          <h3>选择一个岗位画像</h3>
          <p>从左侧列表中选择岗位，查看详细能力要求分析</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import RadarChart from '@/components/RadarChart.vue'

const props = defineProps({
  jobProfiles: { type: Array, default: () => [] },
  selectedId: { type: [String, Number], default: '' },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['select', 'analyze'])

const searchQuery = ref('')
const activeCategory = ref('全部')

// 统计数据
const categoryCount = computed(() => {
  const cats = new Set(props.jobProfiles.map(j => j.category).filter(Boolean))
  return cats.size
})

const avgSkillCount = computed(() => {
  if (!props.jobProfiles.length) return 0
  const total = props.jobProfiles.reduce((sum, j) => sum + (j.technical_skills?.length || 0), 0)
  return Math.round(total / props.jobProfiles.length)
})

const avgSalary = computed(() => {
  // 简单提取薪资数字取平均
  const salaries = props.jobProfiles
    .map(j => {
      const match = (j.salary_range || '').match(/(\d+)/g)
      if (match && match.length >= 2) {
        return (parseInt(match[0]) + parseInt(match[1])) / 2
      }
      return match ? parseInt(match[0]) : 0
    })
    .filter(s => s > 0)
  
  if (!salaries.length) return '未知'
  const avg = Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length)
  return avg >= 10 ? `${avg}K` : `${avg}k`
})

// 类别筛选
const categories = computed(() => {
  const cats = ['全部', ...new Set(props.jobProfiles.map(j => j.category).filter(Boolean))]
  return cats
})

const filteredJobs = computed(() => {
  return props.jobProfiles.filter(job => {
    const matchSearch = !searchQuery.value || 
      job.position_name?.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCategory = activeCategory.value === '全部' || job.category === activeCategory.value
    return matchSearch && matchCategory
  })
})

// 选中的岗位
const selectedJob = computed(() => 
  props.jobProfiles.find(j => String(j.id) === String(props.selectedId))
)

// 雷达图数据
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
  if (!selectedJob.value) return []
  return [{
    name: '岗位要求',
    values: abilityMeta.map(a => Number(selectedJob.value[a.key] || 0)),
    color: '#06b6d4'
  }]
})

// 选择岗位
function selectJob(job) {
  emit('select', String(job.id))
}
</script>

<style scoped>
.job-profile-panel {
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

.stat-icon.cyan { background: rgba(6, 182, 212, 0.15); color: #06b6d4; }
.stat-icon.violet { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
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
  grid-template-columns: 380px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

/* 岗位列表 */
.job-list-section {
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
  width: 180px;
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
  background: rgba(139, 92, 246, 0.12);
}

.search-box input::placeholder {
  color: var(--color-brand-muted, #64748b);
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
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

.job-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.job-list::-webkit-scrollbar {
  width: 6px;
}

.job-list::-webkit-scrollbar-track {
  background: rgba(139, 92, 246, 0.05);
  border-radius: 3px;
}

.job-list::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.3);
  border-radius: 3px;
}

.job-card {
  padding: 16px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 14px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.job-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateX(4px);
}

.job-card.active {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.1));
  border-color: #8b5cf6;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
}

.job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.job-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.job-salary {
  font-size: 13px;
  font-weight: 600;
  color: #10b981;
}

.job-card-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.meta-item {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item i {
  font-size: 11px;
}

.job-card-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tag {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

.skill-more {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(139, 92, 246, 0.1);
  color: #a78bfa;
}

/* 加载态 */
.loading-state {
  flex: 1;
}

.skeleton-card {
  height: 100px;
  background: linear-gradient(90deg, rgba(139, 92, 246, 0.08) 25%, rgba(139, 92, 246, 0.15) 50%, rgba(139, 92, 246, 0.08) 75%);
  background-size: 200% 100%;
  animation: skeleton 1.5s infinite;
  border-radius: 14px;
  margin-bottom: 12px;
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

/* 岗位详情 */
.job-detail-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid var(--color-brand-border, rgba(139, 92, 246, 0.15));
  border-radius: 20px;
  padding: 24px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.detail-title h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
}

.title-badges {
  display: flex;
  gap: 8px;
}

.badge-category {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(6, 182, 212, 0.15);
  color: #06b6d4;
}

.badge-level {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.detail-salary {
  text-align: right;
}

.salary-label {
  display: block;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 4px;
}

.salary-value {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 能力雷达卡片 */
.ability-radar-card {
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

.radar-container {
  min-height: 280px;
}

/* 要求网格 */
.requirements-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .requirements-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.req-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  transition: all 0.2s;
}

.req-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
}

.req-icon {
  font-size: 22px;
  color: #8b5cf6;
  margin-bottom: 8px;
  display: block;
}

.req-label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  display: block;
  margin-bottom: 4px;
}

.req-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

/* 技能卡片 */
.skills-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.skill-count {
  font-size: 13px;
  color: #06b6d4;
  font-weight: 500;
}

.skills-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.15);
  border-radius: 10px;
  transition: all 0.2s;
}

.skill-item:hover {
  border-color: rgba(6, 182, 212, 0.4);
  transform: translateY(-2px);
}

.skill-item.hot {
  background: rgba(249, 115, 22, 0.1);
  border-color: rgba(249, 115, 22, 0.2);
}

.skill-name {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

.skill-badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(249, 115, 22, 0.3);
  color: #fb923c;
  font-weight: 600;
}

/* 证书卡片 */
.certs-card {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.certs-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.cert-item {
  padding: 8px 14px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 10px;
  font-size: 13px;
  color: #34d399;
}

/* 操作栏 */
.action-bar {
  display: flex;
  gap: 14px;
  margin-top: 24px;
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
