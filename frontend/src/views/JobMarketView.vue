<template>
  <div class="job-market">
    <!-- 背景 -->
    <div class="market-bg">
      <div class="bg-glow left"></div>
      <div class="bg-glow right"></div>
    </div>

    <!-- 头部 -->
    <header class="market-header">
      <div class="header-left">
        <router-link to="/job-hub" class="back-btn">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="title-area">
          <h1><i class="bi bi-building"></i> 职位广场</h1>
          <p>智能匹配职位，发现理想工作</p>
        </div>
      </div>
      <div class="header-right">
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input v-model="searchQuery" placeholder="搜索职位、公司、技能..." @input="handleSearch" />
        </div>
      </div>
    </header>

    <!-- 筛选器 -->
    <div class="filter-bar">
      <div class="filter-scroll">
        <div class="filter-group">
          <label>行业</label>
          <select v-model="filters.industry">
            <option value="">全部</option>
            <option value="internet">互联网</option>
            <option value="finance">金融</option>
            <option value="education">教育</option>
            <option value="healthcare">医疗</option>
          </select>
        </div>
        <div class="filter-group">
          <label>岗位类型</label>
          <select v-model="filters.category">
            <option value="">全部</option>
            <option value="frontend">前端开发</option>
            <option value="backend">后端开发</option>
            <option value="ai">人工智能</option>
            <option value="data">数据分析</option>
            <option value="product">产品经理</option>
          </select>
        </div>
        <div class="filter-group">
          <label>工作经验</label>
          <select v-model="filters.experience">
            <option value="">全部</option>
            <option value="fresh">应届生</option>
            <option value="1-3">1-3年</option>
            <option value="3-5">3-5年</option>
            <option value="5+">5年以上</option>
          </select>
        </div>
        <div class="filter-group">
          <label>薪资范围</label>
          <select v-model="filters.salary">
            <option value="">全部</option>
            <option value="0-10">10K以下</option>
            <option value="10-20">10-20K</option>
            <option value="20-30">20-30K</option>
            <option value="30-50">30-50K</option>
            <option value="50+">50K以上</option>
          </select>
        </div>
        <div class="filter-group">
          <label>工作城市</label>
          <select v-model="filters.city">
            <option value="">全部</option>
            <option value="beijing">北京</option>
            <option value="shanghai">上海</option>
            <option value="shenzhen">深圳</option>
            <option value="hangzhou">杭州</option>
            <option value="guangzhou">广州</option>
          </select>
        </div>
        <div class="filter-group">
          <label>排序</label>
          <select v-model="filters.sort">
            <option value="match">匹配度优先</option>
            <option value="salary">薪资优先</option>
            <option value="new">最新发布</option>
          </select>
        </div>
      </div>
      <button class="btn-reset" @click="resetFilters">
        <i class="bi bi-arrow-counterclockwise"></i> 重置
      </button>
    </div>

    <!-- 职位列表 -->
    <div class="job-grid">
      <div v-for="job in filteredJobs" :key="job.id" class="job-card" @click="viewJob(job)">
        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="company-logo" :style="{ background: job.logoColor }">
            {{ job.company.charAt(0) }}
          </div>
          <div class="job-info">
            <h3>{{ job.title }}</h3>
            <p>{{ job.company }} · {{ job.city }}</p>
          </div>
          <div class="salary-tag">{{ job.salary }}</div>
        </div>

        <!-- 匹配度指示器 -->
        <div class="match-indicator">
          <div class="match-bar">
            <div class="match-fill" :style="{ width: `${job.matchScore}%` }" :class="getMatchClass(job.matchScore)"></div>
          </div>
          <span class="match-text" :class="getMatchClass(job.matchScore)">匹配度 {{ job.matchScore }}%</span>
        </div>

        <!-- 岗位要求 -->
        <div class="job-requirements">
          <span class="req-item">
            <i class="bi bi-mortarboard"></i>
            {{ job.education }}
          </span>
          <span class="req-item">
            <i class="bi bi-calendar3"></i>
            {{ job.experience }}
          </span>
          <span class="req-item">
            <i class="bi bi-people"></i>
            {{ job.scale }}
          </span>
        </div>

        <!-- 技能标签 -->
        <div class="skill-tags">
          <span v-for="skill in job.skills.slice(0, 4)" :key="skill" class="tag" :class="{ matched: job.matchedSkills?.includes(skill) }">
            <i v-if="job.matchedSkills?.includes(skill)" class="bi bi-check-circle-fill"></i>
            {{ skill }}
          </span>
          <span v-if="job.skills.length > 4" class="tag more">+{{ job.skills.length - 4 }}</span>
        </div>

        <!-- 操作区 -->
        <div class="card-actions">
          <button class="btn-apply" @click.stop="applyJob(job)">
            <i class="bi bi-send"></i> 投递简历
          </button>
          <button class="btn-collect" :class="{ active: job.collected }" @click.stop="toggleCollect(job)">
            <i :class="job.collected ? 'bi bi-star-fill' : 'bi bi-star'"></i>
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!filteredJobs.length" class="empty-state">
        <i class="bi bi-briefcase"></i>
        <p>暂无匹配的职位</p>
        <button @click="resetFilters">重置筛选条件</button>
      </div>
    </div>

    <!-- 职位详情弹窗 -->
    <transition name="modal-fade">
      <div v-if="selectedJob" class="job-modal" @click.self="selectedJob = null">
        <div class="modal-content">
          <button class="btn-close" @click="selectedJob = null">
            <i class="bi bi-x-lg"></i>
          </button>

          <!-- 头部信息 -->
          <div class="modal-header">
            <div class="job-hero">
              <div class="hero-logo" :style="{ background: selectedJob.logoColor }">
                {{ selectedJob.company.charAt(0) }}
              </div>
              <div class="hero-info">
                <h2>{{ selectedJob.title }}</h2>
                <p>{{ selectedJob.company }}</p>
                <div class="hero-meta">
                  <span><i class="bi bi-geo-alt"></i> {{ selectedJob.city }}</span>
                  <span><i class="bi bi-calendar3"></i> {{ selectedJob.experience }}</span>
                  <span><i class="bi bi-mortarboard"></i> {{ selectedJob.education }}</span>
                </div>
              </div>
              <div class="hero-salary">{{ selectedJob.salary }}</div>
            </div>
            <div class="match-hero">
              <div class="match-ring" :class="getMatchClass(selectedJob.matchScore)">
                <svg viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" class="ring-bg" />
                  <circle cx="50" cy="50" r="45" class="ring-fill" 
                    :stroke-dasharray="`${selectedJob.matchScore * 2.83} 283`" />
                </svg>
                <div class="match-inner">
                  <span class="score">{{ selectedJob.matchScore }}%</span>
                  <span class="label">匹配度</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 内容区 -->
          <div class="modal-body">
            <!-- 岗位画像 -->
            <section class="detail-section">
              <h4><i class="bi bi-hexagon"></i> 岗位能力模型</h4>
              <div class="radar-area">
                <RadarChart :series="selectedJobRadar" :indicators="radarIndicators" height="220px" />
              </div>
            </section>

            <!-- 技能匹配 -->
            <section class="detail-section">
              <h4><i class="bi bi-check2-all"></i> 技能匹配分析</h4>
              <div class="skill-match-grid">
                <div class="skill-match-card matched">
                  <div class="card-header">
                    <i class="bi bi-check-circle-fill"></i>
                    <span>已匹配技能</span>
                  </div>
                  <div class="skill-list">
                    <span v-for="skill in selectedJob.matchedSkills" :key="skill" class="skill-item">{{ skill }}</span>
                  </div>
                </div>
                <div class="skill-match-card missing">
                  <div class="card-header">
                    <i class="bi bi-exclamation-circle"></i>
                    <span>待补充技能</span>
                  </div>
                  <div class="skill-list">
                    <span v-for="skill in selectedJob.missingSkills" :key="skill" class="skill-item">{{ skill }}</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- 职位描述 -->
            <section class="detail-section">
              <h4><i class="bi bi-file-text"></i> 职位描述</h4>
              <div class="job-description">
                <p>{{ selectedJob.description }}</p>
              </div>
            </section>

            <!-- 岗位要求 -->
            <section class="detail-section">
              <h4><i class="bi bi-list-check"></i> 任职要求</h4>
              <ul class="requirement-list">
                <li v-for="(req, i) in selectedJob.requirements" :key="i">{{ req }}</li>
              </ul>
            </section>

            <!-- 公司信息 -->
            <section class="detail-section">
              <h4><i class="bi bi-building"></i> 公司信息</h4>
              <div class="company-info">
                <div class="info-row">
                  <span class="label">公司规模</span>
                  <span class="value">{{ selectedJob.scale }}</span>
                </div>
                <div class="info-row">
                  <span class="label">所属行业</span>
                  <span class="value">{{ selectedJob.industry }}</span>
                </div>
                <div class="info-row">
                  <span class="label">融资阶段</span>
                  <span class="value">{{ selectedJob.funding }}</span>
                </div>
              </div>
            </section>
          </div>

          <!-- 操作区 -->
          <div class="modal-footer">
            <button class="btn-primary" @click="applyJob(selectedJob)">
              <i class="bi bi-send"></i> 立即投递
            </button>
            <button class="btn-secondary" @click="toggleCollect(selectedJob)">
              <i :class="selectedJob.collected ? 'bi bi-star-fill' : 'bi bi-star'"></i>
              {{ selectedJob.collected ? '已收藏' : '收藏' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import RadarChart from '@/components/RadarChart.vue'
import { getJobProfiles } from '@/api'

const toast = inject('toast', null)

// 搜索和筛选
const searchQuery = ref('')
const filters = ref({
  industry: '',
  category: '',
  experience: '',
  salary: '',
  city: '',
  sort: 'match'
})

// 加载状态
const loading = ref(true)

// 雷达图配置
const radarIndicators = [
  { name: '技术能力', max: 10 },
  { name: '沟通能力', max: 10 },
  { name: '学习能力', max: 10 },
  { name: '创新能力', max: 10 },
  { name: '团队协作', max: 10 },
  { name: '执行能力', max: 10 },
]

// 颜色列表
const logoColors = [
  'linear-gradient(135deg, #4f46e5, #6366f1)',
  'linear-gradient(135deg, #f59e0b, #d97706)',
  'linear-gradient(135deg, #06b6d4, #0891b2)',
  'linear-gradient(135deg, #10b981, #059669)',
  'linear-gradient(135deg, #ec4899, #db2777)',
  'linear-gradient(135deg, #8b5cf6, #6366f1)',
]

// 职位数据（从API加载）
const jobs = ref([])

// 加载职位数据
async function loadJobs() {
  loading.value = true
  try {
    const res = await getJobProfiles({ category: filters.value.category })
    const profiles = res.data.profiles || []
    jobs.value = profiles.map((p, index) => ({
      id: p.id,
      title: p.position_name,
      company: '智能匹配企业',
      city: '全国',
      salary: p.salary_range || '面议',
      education: p.education_requirement || '本科及以上',
      experience: p.experience_requirement || '不限',
      scale: '1000人以上',
      industry: p.category || '互联网',
      funding: '',
      matchScore: Math.floor(Math.random() * 25 + 70),
      logoColor: logoColors[index % logoColors.length],
      skills: p.key_skills || [],
      matchedSkills: (p.key_skills || []).slice(0, 3),
      missingSkills: (p.key_skills || []).slice(3),
      abilities: {
        technical: p.ability_requirements?.technical_ability || Math.floor(Math.random() * 3 + 7),
        communication: p.ability_requirements?.communication_ability || Math.floor(Math.random() * 3 + 6),
        learning: p.ability_requirements?.learning_ability || Math.floor(Math.random() * 3 + 7),
        innovation: p.ability_requirements?.innovation_ability || Math.floor(Math.random() * 3 + 6),
        teamwork: p.ability_requirements?.teamwork_ability || Math.floor(Math.random() * 3 + 7),
        execution: p.ability_requirements?.execution_ability || Math.floor(Math.random() * 3 + 7),
      },
      description: p.position_description || '暂无描述',
      requirements: p.core_responsibilities || ['暂无要求'],
      collected: false,
      category: p.category,
      level: p.level,
    }))
  } catch (e) {
    console.error('加载职位失败:', e)
    toast?.('加载职位失败', 'error')
  } finally {
    loading.value = false
  }
}

// 选中的职位
const selectedJob = ref(null)

// 筛选后的职位列表
const filteredJobs = computed(() => {
  let result = [...jobs.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(j => 
      j.title.toLowerCase().includes(query) ||
      j.company.toLowerCase().includes(query) ||
      j.skills.some(s => s.toLowerCase().includes(query))
    )
  }
  
  if (filters.value.city) {
    const cityMap = { beijing: '北京', shanghai: '上海', shenzhen: '深圳', hangzhou: '杭州', guangzhou: '广州' }
    result = result.filter(j => j.city === cityMap[filters.value.city])
  }
  
  if (filters.value.category) {
    result = result.filter(j => j.category?.toLowerCase().includes(filters.value.category))
  }
  
  // 排序
  if (filters.value.sort === 'match') {
    result.sort((a, b) => b.matchScore - a.matchScore)
  } else if (filters.value.sort === 'salary') {
    // 简单排序，实际应解析薪资数值
    result.sort((a, b) => parseInt(b.salary) - parseInt(a.salary))
  }
  
  return result
})

// 选中职位的雷达数据
const selectedJobRadar = computed(() => {
  if (!selectedJob.value) return []
  const abilities = selectedJob.value.abilities
  return [{
    name: '岗位要求',
    value: [
      abilities.technical,
      abilities.communication,
      abilities.learning,
      abilities.innovation,
      abilities.teamwork,
      abilities.execution
    ],
    areaStyle: { color: 'rgba(6, 182, 212, 0.3)' },
    lineStyle: { color: '#06b6d4' }
  }]
})

// 匹配度等级
function getMatchClass(score) {
  if (score >= 85) return 'high'
  if (score >= 70) return 'medium'
  return 'low'
}

// 查看职位详情
function viewJob(job) {
  selectedJob.value = job
}

// 投递职位
function applyJob(job) {
  toast?.(`已投递 ${job.company} - ${job.title}`, 'success')
}

// 收藏切换
function toggleCollect(job) {
  job.collected = !job.collected
  toast?.(job.collected ? '已收藏' : '已取消收藏', 'success')
}

// 搜索处理
function handleSearch() {
  // 可以添加防抖
}

// 重置筛选
function resetFilters() {
  filters.value = {
    industry: '',
    category: '',
    experience: '',
    salary: '',
    city: '',
    sort: 'match'
  }
  searchQuery.value = ''
  loadJobs()
}

// 初始化
onMounted(() => {
  loadJobs()
})
</script>

<style scoped>
.job-market {
  min-height: 100vh;
  padding: 20px 24px;
  position: relative;
}

/* 背景 */
.market-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
}

.bg-glow.left {
  left: -150px;
  top: 10%;
  background: #8b5cf6;
}

.bg-glow.right {
  right: -150px;
  bottom: 20%;
  background: #06b6d4;
}

/* 头部 */
.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  text-decoration: none;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(139, 92, 246, 0.2);
}

.title-area h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.title-area h1 i {
  color: #8b5cf6;
}

.title-area p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  min-width: 280px;
}

.search-box i {
  color: #64748b;
}

.search-box input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.search-box input::placeholder {
  color: #64748b;
}

/* 筛选器 */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.filter-scroll {
  display: flex;
  gap: 12px;
  flex: 1;
  overflow-x: auto;
  padding-bottom: 4px;
}

.filter-scroll::-webkit-scrollbar {
  height: 4px;
}

.filter-scroll::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.3);
  border-radius: 2px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
}

.filter-group label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.filter-group select {
  padding: 8px 12px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 8px;
  color: var(--color-brand-text, #e2e8f0);
  font-size: 13px;
  cursor: pointer;
  min-width: 100px;
}

.filter-group select:focus {
  outline: none;
  border-color: #8b5cf6;
}

.btn-reset {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #f87171;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-reset:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* 职位卡片网格 */
.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  position: relative;
  z-index: 1;
}

.job-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.job-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}

.company-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.job-info {
  flex: 1;
  min-width: 0;
}

.job-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.salary-tag {
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.12);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
  flex-shrink: 0;
}

/* 匹配度指示器 */
.match-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.match-bar {
  flex: 1;
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.match-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.match-fill.high { background: linear-gradient(90deg, #10b981, #34d399); }
.match-fill.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.match-fill.low { background: linear-gradient(90deg, #ef4444, #f87171); }

.match-text {
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.match-text.high { color: #34d399; }
.match-text.medium { color: #fbbf24; }
.match-text.low { color: #f87171; }

/* 岗位要求 */
.job-requirements {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
}

.req-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.req-item i {
  font-size: 14px;
}

/* 技能标签 */
.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.skill-tags .tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 6px;
  font-size: 11px;
  color: #a78bfa;
}

.skill-tags .tag.matched {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
}

.skill-tags .tag.matched i {
  font-size: 10px;
}

.skill-tags .tag.more {
  background: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

/* 操作区 */
.card-actions {
  display: flex;
  gap: 10px;
}

.btn-apply {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-apply:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.btn-collect {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-collect:hover {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.btn-collect.active {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--color-brand-muted, #64748b);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 15px;
  margin-bottom: 16px;
}

.empty-state button {
  padding: 10px 20px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  color: #a78bfa;
  cursor: pointer;
}

/* 弹窗 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.job-modal {
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

.modal-content {
  position: relative;
  width: 100%;
  max-width: 750px;
  max-height: 90vh;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.btn-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.1);
  border: none;
  color: #64748b;
  cursor: pointer;
  z-index: 10;
}

.btn-close:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.modal-header {
  padding: 24px;
  background: rgba(139, 92, 246, 0.05);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.job-hero {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.hero-logo {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 700;
  color: white;
}

.hero-info h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.hero-info > p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 8px;
}

.hero-meta {
  display: flex;
  gap: 14px;
}

.hero-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.hero-meta i {
  font-size: 14px;
}

.hero-salary {
  padding: 8px 16px;
  background: rgba(16, 185, 129, 0.12);
  border-radius: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #10b981;
  flex-shrink: 0;
}

.match-hero {
  flex-shrink: 0;
}

.match-ring {
  position: relative;
  width: 80px;
  height: 80px;
}

.match-ring svg {
  transform: rotate(-90deg);
}

.ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.1);
  stroke-width: 6;
}

.ring-fill {
  fill: none;
  stroke-width: 6;
  stroke-linecap: round;
  transition: stroke-dasharray 0.8s ease;
}

.match-ring.high .ring-fill { stroke: #10b981; }
.match-ring.medium .ring-fill { stroke: #f59e0b; }
.match-ring.low .ring-fill { stroke: #ef4444; }

.match-inner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.match-inner .score {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.match-inner .label {
  font-size: 10px;
  color: var(--color-brand-muted, #64748b);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-section h4 i {
  color: #8b5cf6;
}

.radar-area {
  min-height: 220px;
}

/* 技能匹配网格 */
.skill-match-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.skill-match-card {
  padding: 14px;
  border-radius: 12px;
}

.skill-match-card.matched {
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.skill-match-card.missing {
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.15);
}

.skill-match-card .card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.skill-match-card.matched .card-header i { color: #34d399; }
.skill-match-card.missing .card-header i { color: #fbbf24; }

.skill-match-card .card-header span {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.skill-match-card .skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-match-card .skill-item {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
}

.skill-match-card.matched .skill-item {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.skill-match-card.missing .skill-item {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.job-description {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  line-height: 1.6;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.requirement-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.requirement-list li {
  position: relative;
  padding: 8px 0 8px 20px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.requirement-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 14px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #8b5cf6;
}

.company-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.info-row {
  padding: 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 10px;
  text-align: center;
}

.info-row .label {
  display: block;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 4px;
}

.info-row .value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 18px 24px;
  background: rgba(139, 92, 246, 0.03);
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.btn-primary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 12px;
  color: #f59e0b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(245, 158, 11, 0.2);
}

@media (max-width: 640px) {
  .skill-match-grid {
    grid-template-columns: 1fr;
  }
  
  .company-info {
    grid-template-columns: 1fr;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .market-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .market-header h1 {
  color: #0c4a6e;
}

:global(html.light) .market-header p {
  color: #64748b;
}

:global(html.light) .search-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .search-input input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .search-input input::placeholder {
  color: #94a3b8;
}

:global(html.light) .btn-search {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .filter-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.15);
  color: #64748b;
}

:global(html.light) .filter-tags .tag.active {
  background: rgba(8, 145, 178, 0.15);
  border-color: rgba(8, 145, 178, 0.3);
  color: #0891b2;
}

:global(html.light) .content-grid {
  background: transparent;
}

:global(html.light) .job-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .job-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);
}

:global(html.light) .job-card.selected {
  border-color: #0891b2;
  box-shadow: 0 0 0 2px rgba(8, 145, 178, 0.15);
}

:global(html.light) .company-logo {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .job-title {
  color: #0c4a6e;
}

:global(html.light) .company-name {
  color: #64748b;
}

:global(html.light) .job-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .job-tags .tag.match {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
}

:global(html.light) .job-salary {
  color: #0891b2;
}

:global(html.light) .job-meta span {
  color: #64748b;
}

:global(html.light) .detail-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .detail-header h2 {
  color: #0c4a6e;
}

:global(html.light) .detail-company {
  color: #64748b;
}

:global(html.light) .detail-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .info-grid .info-item {
  background: rgba(8, 145, 178, 0.03);
}

:global(html.light) .info-grid .info-label {
  color: #64748b;
}

:global(html.light) .info-grid .info-value {
  color: #0c4a6e;
}

:global(html.light) .info-grid .info-value.salary {
  color: #0891b2;
}

:global(html.light) .section-title {
  color: #0c4a6e;
  border-bottom-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .job-description {
  color: #475569;
}

:global(html.light) .skill-match-item {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .skill-match-item.matched {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}

:global(html.light) .skill-match-item.missing {
  background: rgba(239, 68, 68, 0.03);
  border-color: rgba(239, 68, 68, 0.15);
}

:global(html.light) .skill-name {
  color: #0c4a6e;
}

:global(html.light) .skill-status.matched {
  color: #059669;
}

:global(html.light) .skill-status.missing {
  color: #dc2626;
}

:global(html.light) .company-info-item {
  background: rgba(8, 145, 178, 0.03);
}

:global(html.light) .company-info-item .label {
  color: #64748b;
}

:global(html.light) .company-info-item .value {
  color: #0c4a6e;
}

:global(html.light) .btn-primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-primary:hover {
  box-shadow: 0 6px 20px rgba(8, 145, 178, 0.3);
}

:global(html.light) .btn-secondary {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.2);
  color: #d97706;
}

:global(html.light) .btn-secondary:hover {
  background: rgba(245, 158, 11, 0.18);
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
</style>
