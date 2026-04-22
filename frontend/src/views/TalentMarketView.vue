<template>
  <div class="talent-market">
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
          <h1><i class="bi bi-people-fill"></i> 人才广场</h1>
          <p>发现优质人才，AI智能匹配推荐</p>
        </div>
      </div>
      <div class="header-right">
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input v-model="searchQuery" placeholder="搜索姓名、技能、专业..." @input="handleSearch" />
        </div>
      </div>
    </header>

    <!-- 筛选器 -->
    <div class="filter-bar">
      <div class="filter-scroll">
        <div class="filter-group">
          <label>专业方向</label>
          <select v-model="filters.major">
            <option value="">全部</option>
            <option value="cs">计算机科学</option>
            <option value="ai">人工智能</option>
            <option value="se">软件工程</option>
            <option value="data">数据科学</option>
            <option value="other">其他</option>
          </select>
        </div>
        <div class="filter-group">
          <label>学历</label>
          <select v-model="filters.education">
            <option value="">全部</option>
            <option value="bachelor">本科</option>
            <option value="master">硕士</option>
            <option value="phd">博士</option>
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
          <label>期望薪资</label>
          <select v-model="filters.salary">
            <option value="">全部</option>
            <option value="0-10">10K以下</option>
            <option value="10-20">10-20K</option>
            <option value="20-30">20-30K</option>
            <option value="30+">30K以上</option>
          </select>
        </div>
        <div class="filter-group">
          <label>排序</label>
          <select v-model="filters.sort">
            <option value="match">匹配度优先</option>
            <option value="new">最新发布</option>
            <option value="score">竞争力评分</option>
          </select>
        </div>
      </div>
      <button class="btn-reset" @click="resetFilters">
        <i class="bi bi-arrow-counterclockwise"></i> 重置
      </button>
    </div>

    <!-- 人才列表 -->
    <div class="talent-grid">
      <div v-for="talent in filteredTalents" :key="talent.id" class="talent-card" @click="viewTalent(talent)">
        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="avatar" :style="{ background: talent.avatarColor }">
            {{ talent.name.charAt(0) }}
          </div>
          <div class="basic-info">
            <h3>{{ talent.name }}</h3>
            <p>{{ talent.education }} · {{ talent.major }}</p>
          </div>
          <div class="match-badge" :class="getMatchClass(talent.matchScore)">
            <span class="score">{{ talent.matchScore }}%</span>
            <span class="label">匹配</span>
          </div>
        </div>

        <!-- 能力雷达（简化版） -->
        <div class="ability-mini">
          <div class="ability-bars">
            <div class="ability-row" v-for="(val, key) in talent.abilities" :key="key">
              <span class="ability-name">{{ abilityLabels[key] }}</span>
              <div class="ability-track">
                <div class="ability-fill" :style="{ width: `${val * 10}%` }"></div>
              </div>
              <span class="ability-val">{{ val }}</span>
            </div>
          </div>
        </div>

        <!-- 技能标签 -->
        <div class="skill-tags">
          <span v-for="skill in talent.skills.slice(0, 5)" :key="skill" class="tag">{{ skill }}</span>
          <span v-if="talent.skills.length > 5" class="tag more">+{{ talent.skills.length - 5 }}</span>
        </div>

        <!-- 期望信息 -->
        <div class="expect-info">
          <span class="expect-item">
            <i class="bi bi-geo-alt"></i>
            {{ talent.expectCity }}
          </span>
          <span class="expect-item">
            <i class="bi bi-currency-dollar"></i>
            {{ talent.expectSalary }}
          </span>
        </div>

        <!-- 操作区 -->
        <div class="card-actions">
          <button class="btn-invite" @click.stop="inviteTalent(talent)">
            <i class="bi bi-envelope-heart"></i> 邀请沟通
          </button>
          <button class="btn-collect" :class="{ active: talent.collected }" @click.stop="toggleCollect(talent)">
            <i :class="talent.collected ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!filteredTalents.length" class="empty-state">
        <i class="bi bi-people"></i>
        <p>暂无匹配的人才</p>
        <button @click="resetFilters">重置筛选条件</button>
      </div>
    </div>

    <!-- 人才详情弹窗 -->
    <transition name="modal-fade">
      <div v-if="selectedTalent" class="talent-modal" @click.self="selectedTalent = null">
        <div class="modal-content">
          <button class="btn-close" @click="selectedTalent = null">
            <i class="bi bi-x-lg"></i>
          </button>

          <!-- 头部信息 -->
          <div class="modal-header">
            <div class="profile-hero">
              <div class="hero-avatar" :style="{ background: selectedTalent.avatarColor }">
                {{ selectedTalent.name.charAt(0) }}
              </div>
              <div class="hero-info">
                <h2>{{ selectedTalent.name }}</h2>
                <p>{{ selectedTalent.education }} · {{ selectedTalent.major }}</p>
                <div class="hero-tags">
                  <span class="hero-tag">{{ selectedTalent.experience }}</span>
                  <span class="hero-tag">{{ selectedTalent.expectCity }}</span>
                </div>
              </div>
              <div class="hero-scores">
                <div class="score-item">
                  <span class="num">{{ selectedTalent.matchScore }}</span>
                  <span class="label">匹配度</span>
                </div>
                <div class="score-item">
                  <span class="num">{{ selectedTalent.competitiveness }}</span>
                  <span class="label">竞争力</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 内容区 -->
          <div class="modal-body">
            <!-- 能力画像 -->
            <section class="detail-section">
              <h4><i class="bi bi-hexagon"></i> 能力画像</h4>
              <div class="radar-area">
                <RadarChart :series="selectedTalentRadar" :indicators="radarIndicators" height="240px" />
              </div>
            </section>

            <!-- 技能清单 -->
            <section class="detail-section">
              <h4><i class="bi bi-lightbulb"></i> 技能清单</h4>
              <div class="skill-list">
                <span v-for="skill in selectedTalent.skills" :key="skill" class="skill-chip">{{ skill }}</span>
              </div>
            </section>

            <!-- 项目经历 -->
            <section class="detail-section">
              <h4><i class="bi bi-folder2-open"></i> 项目经历</h4>
              <div class="project-list">
                <div v-for="proj in selectedTalent.projects" :key="proj.name" class="project-item">
                  <div class="proj-header">
                    <span class="proj-name">{{ proj.name }}</span>
                    <span class="proj-role">{{ proj.role }}</span>
                  </div>
                  <p class="proj-desc">{{ proj.description }}</p>
                </div>
              </div>
            </section>

            <!-- 职业规划 -->
            <section class="detail-section">
              <h4><i class="bi bi-signpost-split"></i> 职业规划</h4>
              <p class="career-plan">{{ selectedTalent.careerPlan }}</p>
            </section>
          </div>

          <!-- 操作区 -->
          <div class="modal-footer">
            <button class="btn-primary" @click="inviteTalent(selectedTalent)">
              <i class="bi bi-envelope-heart"></i> 发送邀请
            </button>
            <button class="btn-secondary" @click="downloadResume(selectedTalent)">
              <i class="bi bi-download"></i> 下载简历
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import RadarChart from '@/components/RadarChart.vue'

const toast = inject('toast', null)

// 搜索和筛选
const searchQuery = ref('')
const filters = ref({
  major: '',
  education: '',
  experience: '',
  salary: '',
  sort: 'match'
})

// 能力标签
const abilityLabels = {
  technical: '技术能力',
  communication: '沟通能力',
  learning: '学习能力',
  innovation: '创新能力',
  teamwork: '团队协作',
  execution: '执行能力'
}

const radarIndicators = [
  { name: '技术能力', max: 10 },
  { name: '沟通能力', max: 10 },
  { name: '学习能力', max: 10 },
  { name: '创新能力', max: 10 },
  { name: '团队协作', max: 10 },
  { name: '执行能力', max: 10 },
]

// 模拟人才数据
const talents = ref([
  {
    id: 1,
    name: '张三',
    education: '本科',
    major: '软件工程',
    experience: '3年经验',
    expectCity: '上海',
    expectSalary: '20-30K',
    matchScore: 95,
    competitiveness: 88,
    avatarColor: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
    abilities: { technical: 9, communication: 7, learning: 8, innovation: 7, teamwork: 8, execution: 8 },
    skills: ['Vue.js', 'React', 'Node.js', 'TypeScript', 'Python', 'MySQL', 'Docker'],
    projects: [
      { name: '电商平台', role: '前端负责人', description: '负责前端架构设计和核心模块开发，优化首屏加载时间50%' },
      { name: '数据可视化系统', role: '全栈开发', description: '基于ECharts实现复杂数据可视化，支持实时数据更新' }
    ],
    careerPlan: '希望在3年内成为技术专家，5年内转型为技术管理，专注于前端工程化和团队建设。',
    collected: false
  },
  {
    id: 2,
    name: '李四',
    education: '硕士',
    major: '人工智能',
    experience: '应届生',
    expectCity: '北京',
    expectSalary: '25-35K',
    matchScore: 88,
    competitiveness: 92,
    avatarColor: 'linear-gradient(135deg, #06b6d4, #0891b2)',
    abilities: { technical: 9, communication: 6, learning: 9, innovation: 9, teamwork: 7, execution: 7 },
    skills: ['Python', 'PyTorch', 'TensorFlow', 'NLP', '深度学习', 'OpenCV'],
    projects: [
      { name: '智能问答系统', role: '算法工程师', description: '基于BERT实现问答匹配，准确率达到92%' },
      { name: '图像识别系统', role: '核心开发', description: '实现工业缺陷检测，检测速度达到100张/秒' }
    ],
    careerPlan: '专注于自然语言处理领域，希望能够参与到前沿AI产品的研发中。',
    collected: true
  },
  {
    id: 3,
    name: '王五',
    education: '本科',
    major: '数据科学',
    experience: '2年经验',
    expectCity: '深圳',
    expectSalary: '18-25K',
    matchScore: 82,
    competitiveness: 75,
    avatarColor: 'linear-gradient(135deg, #f59e0b, #d97706)',
    abilities: { technical: 7, communication: 8, learning: 8, innovation: 6, teamwork: 9, execution: 8 },
    skills: ['Python', 'SQL', 'Tableau', '数据分析', 'Excel', 'PowerBI'],
    projects: [
      { name: '用户行为分析', role: '数据分析师', description: '搭建用户画像系统，提升营销转化率30%' }
    ],
    careerPlan: '希望深耕数据分析领域，向数据产品经理方向发展。',
    collected: false
  },
  {
    id: 4,
    name: '赵六',
    education: '本科',
    major: '计算机科学',
    experience: '1年经验',
    expectCity: '杭州',
    expectSalary: '15-20K',
    matchScore: 78,
    competitiveness: 70,
    avatarColor: 'linear-gradient(135deg, #10b981, #059669)',
    abilities: { technical: 7, communication: 7, learning: 9, innovation: 6, teamwork: 7, execution: 8 },
    skills: ['Java', 'Spring Boot', 'MySQL', 'Redis', 'Vue'],
    projects: [
      { name: '后台管理系统', role: '后端开发', description: '独立完成权限管理和日志模块开发' }
    ],
    careerPlan: '希望成为全栈工程师，对微服务和云原生技术感兴趣。',
    collected: false
  }
])

// 选中的人才
const selectedTalent = ref(null)

// 筛选后的人才列表
const filteredTalents = computed(() => {
  let result = [...talents.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(t => 
      t.name.toLowerCase().includes(query) ||
      t.skills.some(s => s.toLowerCase().includes(query)) ||
      t.major.toLowerCase().includes(query)
    )
  }
  
  if (filters.value.education) {
    const eduMap = { bachelor: '本科', master: '硕士', phd: '博士' }
    result = result.filter(t => t.education === eduMap[filters.value.education])
  }
  
  // 排序
  if (filters.value.sort === 'match') {
    result.sort((a, b) => b.matchScore - a.matchScore)
  } else if (filters.value.sort === 'score') {
    result.sort((a, b) => b.competitiveness - a.competitiveness)
  }
  
  return result
})

// 选中人才的雷达数据
const selectedTalentRadar = computed(() => {
  if (!selectedTalent.value) return []
  const abilities = selectedTalent.value.abilities
  return [{
    name: selectedTalent.value.name,
    value: [
      abilities.technical,
      abilities.communication,
      abilities.learning,
      abilities.innovation,
      abilities.teamwork,
      abilities.execution
    ],
    areaStyle: { color: 'rgba(139, 92, 246, 0.3)' },
    lineStyle: { color: '#8b5cf6' }
  }]
})

// 匹配度等级
function getMatchClass(score) {
  if (score >= 90) return 'high'
  if (score >= 75) return 'medium'
  return 'low'
}

// 重置筛选
function resetFilters() {
  filters.value = {
    major: '',
    education: '',
    experience: '',
    salary: '',
    sort: 'match'
  }
  searchQuery.value = ''
}

// 查看人才详情
function viewTalent(talent) {
  selectedTalent.value = talent
}

// 邀请人才
function inviteTalent(talent) {
  toast?.(`已向 ${talent.name} 发送沟通邀请`, 'success')
}

// 收藏切换
function toggleCollect(talent) {
  talent.collected = !talent.collected
  toast?.(talent.collected ? '已收藏' : '已取消收藏', 'success')
}

// 下载简历
function downloadResume(talent) {
  toast?.(`正在下载 ${talent.name} 的简历...`, 'info')
}

// 搜索处理
function handleSearch() {
  // 可以添加防抖
}
</script>

<style scoped>
.talent-market {
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
  background: var(--talent-glow-left, #06b6d4);
}

.bg-glow.right {
  right: -150px;
  bottom: 20%;
  background: var(--talent-glow-right, #8b5cf6);
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
  color: #06b6d4;
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

/* 人才卡片网格 */
.talent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  position: relative;
  z-index: 1;
}

.talent-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.talent-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.basic-info {
  flex: 1;
  min-width: 0;
}

.basic-info h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.basic-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.match-badge {
  text-align: center;
  padding: 8px 12px;
  border-radius: 12px;
}

.match-badge.high {
  background: rgba(16, 185, 129, 0.15);
}

.match-badge.medium {
  background: rgba(245, 158, 11, 0.15);
}

.match-badge.low {
  background: rgba(239, 68, 68, 0.15);
}

.match-badge .score {
  display: block;
  font-size: 18px;
  font-weight: 700;
}

.match-badge.high .score { color: #34d399; }
.match-badge.medium .score { color: #fbbf24; }
.match-badge.low .score { color: #f87171; }

.match-badge .label {
  font-size: 10px;
  color: var(--color-brand-muted, #64748b);
}

/* 能力条 */
.ability-mini {
  margin-bottom: 14px;
}

.ability-bars {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.ability-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ability-name {
  width: 50px;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.ability-track {
  flex: 1;
  height: 4px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.ability-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 2px;
}

.ability-val {
  width: 16px;
  font-size: 11px;
  font-weight: 600;
  color: #a78bfa;
  text-align: right;
}

/* 技能标签 */
.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.skill-tags .tag {
  padding: 4px 10px;
  background: rgba(6, 182, 212, 0.1);
  border-radius: 6px;
  font-size: 11px;
  color: #22d3ee;
}

.skill-tags .tag.more {
  background: rgba(139, 92, 246, 0.1);
  color: #a78bfa;
}

/* 期望信息 */
.expect-info {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.expect-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.expect-item i {
  color: #64748b;
}

/* 操作区 */
.card-actions {
  display: flex;
  gap: 10px;
}

.btn-invite {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-invite:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-collect {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(236, 72, 153, 0.1);
  border: 1px solid rgba(236, 72, 153, 0.2);
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-collect:hover {
  background: rgba(236, 72, 153, 0.2);
  color: #ec4899;
}

.btn-collect.active {
  background: rgba(236, 72, 153, 0.2);
  color: #ec4899;
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

.talent-modal {
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
  max-width: 700px;
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
}

.profile-hero {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hero-avatar {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: white;
}

.hero-info h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.hero-info > p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 8px;
}

.hero-tags {
  display: flex;
  gap: 8px;
}

.hero-tag {
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 6px;
  font-size: 12px;
  color: #a78bfa;
}

.hero-scores {
  margin-left: auto;
  display: flex;
  gap: 16px;
}

.score-item {
  text-align: center;
  padding: 10px 16px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 12px;
}

.score-item .num {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #a78bfa;
}

.score-item .label {
  font-size: 11px;
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
  min-height: 240px;
}

.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-chip {
  padding: 6px 14px;
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 8px;
  font-size: 13px;
  color: #22d3ee;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-item {
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.proj-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.proj-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.proj-role {
  font-size: 12px;
  padding: 3px 8px;
  background: rgba(139, 92, 246, 0.15);
  border-radius: 6px;
  color: #a78bfa;
}

.proj-desc {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  line-height: 1.5;
}

.career-plan {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  line-height: 1.6;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
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
  background: linear-gradient(135deg, #06b6d4, #0891b2);
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
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.3);
}

.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  color: #a78bfa;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(139, 92, 246, 0.2);
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .market-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .market-header h1 {
  color: #0c4a6e;
}

:global(html.light) .market-header p {
  color: #64748b;
}

:global(html.light) .filter-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .filter-input input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .filter-select {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .talent-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .talent-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);
}

:global(html.light) .talent-name {
  color: #0c4a6e;
}

:global(html.light) .talent-title {
  color: #64748b;
}

:global(html.light) .talent-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .talent-score {
  color: #0891b2;
}

:global(html.light) .talent-meta {
  color: #64748b;
}

:global(html.light) .btn-primary:hover {
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.25);
}

:global(html.light) .btn-secondary {
  background: rgba(8, 145, 178, 0.1);
  border-color: rgba(8, 145, 178, 0.2);
  color: #0891b2;
}

:global(html.light) .btn-secondary:hover {
  background: rgba(8, 145, 178, 0.18);
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
