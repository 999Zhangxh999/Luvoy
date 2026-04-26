<template>
  <div class="applications-view">
    <!-- 背景 -->
    <div class="app-bg">
      <div class="bg-glow glow-1"></div>
      <div class="bg-glow glow-2"></div>
    </div>

    <div class="app-container">
      <!-- 头部 -->
      <header class="app-header">
        <router-link to="/job-hub" class="back-btn">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="header-info">
          <h1><i class="bi bi-send-check-fill"></i> {{ isHR ? '收到的申请' : '投递记录' }}</h1>
          <p>{{ isHR ? '管理来自求职者的申请' : '追踪您的投递状态' }}</p>
        </div>
        <div class="header-stats">
          <div class="stat-pill" v-for="stat in headerStats" :key="stat.label">
            <span class="stat-num">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </header>

      <!-- 标签页 -->
      <div class="tabs-bar">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          :class="['tab-btn', { active: currentTab === tab.key }]"
          @click="currentTab = tab.key"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
          <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- 筛选 & 搜索 -->
      <div class="filter-bar">
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input v-model="searchQuery" :placeholder="isHR ? '搜索求职者姓名、技能...' : '搜索公司、职位...'" />
        </div>
        <div class="filter-group">
          <select v-model="filters.time">
            <option value="">全部时间</option>
            <option value="today">今天</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
          </select>
        </div>
        <div class="filter-group">
          <select v-model="filters.sort">
            <option value="latest">最新优先</option>
            <option value="match">匹配度优先</option>
          </select>
        </div>
      </div>

      <!-- 列表 -->
      <div class="applications-list">
        <transition-group name="list" tag="div" class="list-content">
          <div 
            v-for="item in filteredList" 
            :key="item.id"
            :class="['application-card', item.status]"
          >
            <!-- 头像 & 基本信息 -->
            <div class="card-main">
              <div class="card-avatar" :style="{ background: item.avatarColor }">
                {{ item.avatarText }}
              </div>
              <div class="card-info">
                <div class="info-header">
                  <h3>{{ item.title }}</h3>
                  <span :class="['status-badge', item.status]">
                    <i :class="statusIcon(item.status)"></i>
                    {{ statusLabel(item.status) }}
                  </span>
                </div>
                <p class="info-subtitle">{{ item.subtitle }}</p>
                <div class="info-meta">
                  <span><i class="bi bi-clock"></i> {{ item.time }}</span>
                  <span v-if="item.matchScore"><i class="bi bi-bullseye"></i> 匹配度 {{ item.matchScore }}%</span>
                </div>
              </div>
            </div>

            <!-- 技能标签 -->
            <div class="card-skills">
              <span v-for="skill in item.skills.slice(0, 4)" :key="skill" class="skill-tag">
                {{ skill }}
              </span>
              <span v-if="item.skills.length > 4" class="skill-more">+{{ item.skills.length - 4 }}</span>
            </div>

            <!-- 匹配度条 -->
            <div v-if="item.matchScore" class="match-bar-wrapper">
              <div class="match-bar">
                <div class="match-fill" :style="{ width: `${item.matchScore}%` }" :class="getMatchClass(item.matchScore)"></div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="card-actions">
              <template v-if="isHR">
                <button v-if="item.status === 'pending'" class="btn-accept" @click="acceptApplication(item)">
                  <i class="bi bi-check-lg"></i> 通过
                </button>
                <button v-if="item.status === 'pending'" class="btn-reject" @click="rejectApplication(item)">
                  <i class="bi bi-x-lg"></i> 拒绝
                </button>
                <button class="btn-chat" @click="openChat(item)">
                  <i class="bi bi-chat-dots"></i> 沟通
                </button>
              </template>
              <template v-else>
                <button v-if="item.status === 'accepted'" class="btn-accept" @click="confirmInterview(item)">
                  <i class="bi bi-calendar-check"></i> 确认面试
                </button>
                <button class="btn-detail" @click="viewDetail(item)">
                  <i class="bi bi-eye"></i> 查看详情
                </button>
                <button v-if="item.status === 'pending'" class="btn-withdraw" @click="withdrawApplication(item)">
                  <i class="bi bi-x-circle"></i> 撤回
                </button>
              </template>
            </div>

            <!-- 时间轴（展开） -->
            <transition name="expand">
              <div v-if="expandedId === item.id" class="card-timeline">
                <div class="timeline-title">进度追踪</div>
                <div class="timeline-items">
                  <div v-for="(event, i) in item.timeline" :key="i" :class="['timeline-item', { done: event.done }]">
                    <div class="timeline-dot">
                      <i v-if="event.done" class="bi bi-check"></i>
                    </div>
                    <div class="timeline-content">
                      <span class="timeline-label">{{ event.label }}</span>
                      <span class="timeline-time">{{ event.time }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </transition>

            <!-- 展开按钮 -->
            <button class="btn-expand" @click="toggleExpand(item.id)">
              <i :class="expandedId === item.id ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
            </button>
          </div>
        </transition-group>

        <!-- 空状态 -->
        <div v-if="!filteredList.length" class="empty-state">
          <i class="bi bi-inbox"></i>
          <h3>暂无记录</h3>
          <p>{{ isHR ? '还没有收到求职者的申请' : '您还没有投递过任何职位' }}</p>
          <router-link :to="isHR ? '/talent-market' : '/job-market'" class="btn-explore">
            {{ isHR ? '浏览人才库' : '浏览职位' }}
          </router-link>
        </div>
      </div>

      <!-- 批量操作栏 -->
      <transition name="slide-up">
        <div v-if="selectedItems.length" class="batch-actions">
          <span class="selected-count">已选择 {{ selectedItems.length }} 项</span>
          <button class="btn-batch accept" @click="batchAccept">
            <i class="bi bi-check-all"></i> 批量通过
          </button>
          <button class="btn-batch reject" @click="batchReject">
            <i class="bi bi-x-lg"></i> 批量拒绝
          </button>
          <button class="btn-cancel" @click="selectedItems = []">取消</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const toast = inject('toast', null)

// 判断角色
const isHR = computed(() => localStorage.getItem('jobHubRole') === 'hr')

// 标签页
const currentTab = ref('all')

const tabs = computed(() => isHR.value ? [
  { key: 'all', label: '全部', icon: 'bi bi-grid', count: 12 },
  { key: 'pending', label: '待处理', icon: 'bi bi-hourglass-split', count: 5 },
  { key: 'accepted', label: '已通过', icon: 'bi bi-check-circle', count: 4 },
  { key: 'rejected', label: '已拒绝', icon: 'bi bi-x-circle', count: 3 },
] : [
  { key: 'all', label: '全部', icon: 'bi bi-grid', count: 8 },
  { key: 'pending', label: '待回复', icon: 'bi bi-hourglass-split', count: 3 },
  { key: 'accepted', label: '已通过', icon: 'bi bi-check-circle', count: 2 },
  { key: 'interview', label: '面试中', icon: 'bi bi-calendar-check', count: 2 },
  { key: 'rejected', label: '已拒绝', icon: 'bi bi-x-circle', count: 1 },
])

// 统计
const headerStats = computed(() => isHR.value ? [
  { label: '今日新增', value: 5 },
  { label: '待处理', value: 8 },
  { label: '本周通过', value: 12 },
] : [
  { label: '投递中', value: 3 },
  { label: '面试邀请', value: 2 },
  { label: '收到offer', value: 1 },
])

// 搜索和筛选
const searchQuery = ref('')
const filters = ref({ time: '', sort: 'latest' })

// 模拟数据
const hrApplications = [
  {
    id: 1,
    title: '张三',
    subtitle: '前端开发工程师 · 3年经验',
    avatarText: '张',
    avatarColor: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
    status: 'pending',
    time: '10分钟前',
    matchScore: 92,
    skills: ['Vue.js', 'React', 'TypeScript', 'Node.js'],
    timeline: [
      { label: '收到简历', time: '今天 14:30', done: true },
      { label: 'HR筛选', time: '进行中', done: false },
      { label: '面试安排', time: '', done: false },
      { label: '发送offer', time: '', done: false },
    ]
  },
  {
    id: 2,
    title: '李四',
    subtitle: 'AI算法工程师 · 应届',
    avatarText: '李',
    avatarColor: 'linear-gradient(135deg, #10b981, #059669)',
    status: 'accepted',
    time: '1小时前',
    matchScore: 88,
    skills: ['Python', 'PyTorch', 'TensorFlow', '机器学习'],
    timeline: [
      { label: '收到简历', time: '今天 10:00', done: true },
      { label: 'HR筛选', time: '今天 11:30', done: true },
      { label: '面试安排', time: '进行中', done: false },
      { label: '发送offer', time: '', done: false },
    ]
  },
  {
    id: 3,
    title: '王五',
    subtitle: '数据分析师 · 2年经验',
    avatarText: '王',
    avatarColor: 'linear-gradient(135deg, #f59e0b, #d97706)',
    status: 'rejected',
    time: '昨天',
    matchScore: 65,
    skills: ['SQL', 'Python', 'Tableau'],
    timeline: [
      { label: '收到简历', time: '昨天 09:00', done: true },
      { label: 'HR筛选', time: '昨天 15:00', done: true },
      { label: '不合适', time: '昨天 15:30', done: true },
    ]
  },
]

const seekerApplications = [
  {
    id: 1,
    title: '字节跳动 - 高级前端工程师',
    subtitle: '上海 · 25-40K · 技术部',
    avatarText: '字',
    avatarColor: 'linear-gradient(135deg, #4f46e5, #6366f1)',
    status: 'accepted',
    time: '今天',
    matchScore: 92,
    skills: ['Vue.js', 'React', 'TypeScript'],
    timeline: [
      { label: '投递简历', time: '3天前', done: true },
      { label: '简历筛选', time: '昨天', done: true },
      { label: '收到面试邀请', time: '今天 10:00', done: true },
      { label: '一面', time: '待安排', done: false },
    ]
  },
  {
    id: 2,
    title: '阿里巴巴 - 数据分析师',
    subtitle: '杭州 · 20-35K',
    avatarText: '阿',
    avatarColor: 'linear-gradient(135deg, #f59e0b, #d97706)',
    status: 'pending',
    time: '2天前',
    matchScore: 85,
    skills: ['Python', 'SQL', '数据分析'],
    timeline: [
      { label: '投递简历', time: '2天前', done: true },
      { label: '简历筛选', time: '进行中', done: false },
    ]
  },
  {
    id: 3,
    title: '腾讯 - 后端开发工程师',
    subtitle: '深圳 · 22-38K',
    avatarText: '腾',
    avatarColor: 'linear-gradient(135deg, #06b6d4, #0891b2)',
    status: 'interview',
    time: '1周前',
    matchScore: 78,
    skills: ['Java', 'Spring', 'MySQL'],
    timeline: [
      { label: '投递简历', time: '1周前', done: true },
      { label: '简历筛选', time: '5天前', done: true },
      { label: '一面', time: '3天前', done: true },
      { label: '二面', time: '明天 14:00', done: false },
    ]
  },
]

const applications = computed(() => isHR.value ? hrApplications : seekerApplications)

// 筛选后的列表
const filteredList = computed(() => {
  let list = [...applications.value]
  
  if (currentTab.value !== 'all') {
    list = list.filter(item => item.status === currentTab.value)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(item => 
      item.title.toLowerCase().includes(q) ||
      item.skills.some(s => s.toLowerCase().includes(q))
    )
  }
  
  if (filters.value.sort === 'match') {
    list.sort((a, b) => b.matchScore - a.matchScore)
  }
  
  return list
})

// 展开状态
const expandedId = ref(null)
const selectedItems = ref([])

function toggleExpand(id) {
  expandedId.value = expandedId.value === id ? null : id
}

// 状态相关
function statusLabel(status) {
  const labels = {
    pending: '待处理',
    accepted: '已通过',
    rejected: '已拒绝',
    interview: '面试中'
  }
  return labels[status] || status
}

function statusIcon(status) {
  const icons = {
    pending: 'bi bi-hourglass-split',
    accepted: 'bi bi-check-circle-fill',
    rejected: 'bi bi-x-circle-fill',
    interview: 'bi bi-calendar-check'
  }
  return icons[status] || 'bi bi-circle'
}

function getMatchClass(score) {
  if (score >= 85) return 'high'
  if (score >= 70) return 'medium'
  return 'low'
}

// 操作
function acceptApplication(item) {
  item.status = 'accepted'
  toast?.(`已通过 ${item.title} 的申请`, 'success')
}

function rejectApplication(item) {
  item.status = 'rejected'
  toast?.(`已拒绝 ${item.title} 的申请`, 'info')
}

function openChat(item) {
  router.push('/messages')
}

function viewDetail(item) {
  toast?.('查看详情', 'info')
}

function withdrawApplication(item) {
  toast?.('已撤回投递', 'info')
}

function confirmInterview(item) {
  toast?.('已确认面试', 'success')
}

function batchAccept() {
  toast?.(`批量通过 ${selectedItems.value.length} 项`, 'success')
  selectedItems.value = []
}

function batchReject() {
  toast?.(`批量拒绝 ${selectedItems.value.length} 项`, 'info')
  selectedItems.value = []
}
</script>

<style scoped>
.applications-view {
  min-height: 100vh;
  padding: 24px;
  position: relative;
}

.app-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: #8b5cf6;
  left: -150px;
  top: 10%;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: #06b6d4;
  right: -100px;
  bottom: 15%;
}

.app-container {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 头部 */
.app-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  text-decoration: none;
}

.header-info {
  flex: 1;
}

.header-info h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-info h1 i { color: #8b5cf6; }

.header-info p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 16px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
}

.stat-num {
  font-size: 20px;
  font-weight: 700;
  color: #a78bfa;
}

.stat-label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 标签页 */
.tabs-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  padding: 6px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 14px;
  overflow-x: auto;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: transparent;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.tab-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.tab-btn:not(.active):hover {
  background: rgba(139, 92, 246, 0.1);
  color: var(--color-brand-text, #e2e8f0);
}

.tab-count {
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  font-size: 12px;
}

.tab-btn:not(.active) .tab-count {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
}

.search-box i { color: #64748b; }

.search-box input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.filter-group select {
  padding: 10px 14px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  color: var(--color-brand-text, #e2e8f0);
  font-size: 14px;
  cursor: pointer;
}

/* 列表 */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 卡片 */
.application-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  padding: 20px;
  position: relative;
  transition: all 0.3s;
}

.application-card:hover {
  border-color: rgba(139, 92, 246, 0.25);
  transform: translateX(4px);
}

.application-card.pending { border-left: 4px solid #f59e0b; }
.application-card.accepted { border-left: 4px solid #10b981; }
.application-card.rejected { border-left: 4px solid #ef4444; }
.application-card.interview { border-left: 4px solid #06b6d4; }

.card-main {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 14px;
}

.card-avatar {
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

.card-info {
  flex: 1;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.info-header h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.status-badge.accepted {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.status-badge.rejected {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.status-badge.interview {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.info-subtitle {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 8px;
}

.info-meta {
  display: flex;
  gap: 16px;
}

.info-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 技能标签 */
.card-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.skill-tag {
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 6px;
  font-size: 12px;
  color: #a78bfa;
}

.skill-more {
  padding: 4px 8px;
  background: rgba(100, 116, 139, 0.1);
  border-radius: 6px;
  font-size: 12px;
  color: #64748b;
}

/* 匹配度条 */
.match-bar-wrapper {
  margin-bottom: 14px;
}

.match-bar {
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

/* 操作按钮 */
.card-actions {
  display: flex;
  gap: 10px;
}

.card-actions button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-accept {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: #34d399;
}

.btn-accept:hover {
  background: rgba(16, 185, 129, 0.25);
}

.btn-reject {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.btn-reject:hover {
  background: rgba(239, 68, 68, 0.2);
}

.btn-chat, .btn-detail {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.btn-chat:hover, .btn-detail:hover {
  background: rgba(139, 92, 246, 0.2);
}

.btn-withdraw {
  background: rgba(100, 116, 139, 0.1);
  border: 1px solid rgba(100, 116, 139, 0.2);
  color: #94a3b8;
}

/* 时间轴 */
.card-timeline {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.timeline-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 14px;
}

.timeline-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-left: 16px;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 24px;
  bottom: -12px;
  width: 2px;
  background: rgba(139, 92, 246, 0.15);
}

.timeline-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #64748b;
  flex-shrink: 0;
}

.timeline-item.done .timeline-dot {
  background: #10b981;
  color: white;
}

.timeline-content {
  display: flex;
  flex: 1;
  justify-content: space-between;
}

.timeline-label {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

.timeline-time {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.btn-expand {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.08);
  border: none;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-expand:hover {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-brand-muted, #64748b);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  margin-bottom: 20px;
}

.btn-explore {
  display: inline-flex;
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-decoration: none;
}

/* 批量操作 */
.batch-actions {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.selected-count {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.btn-batch {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-batch.accept {
  background: #10b981;
  color: white;
}

.btn-batch.reject {
  background: #ef4444;
  color: white;
}

.btn-cancel {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
}

/* 动画 */
.list-enter-active, .list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from, .expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from, .slide-up-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

@media (max-width: 640px) {
  .header-stats { display: none; }
  .filter-bar { flex-wrap: wrap; }
  .card-actions { flex-wrap: wrap; }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .glow-1 {
  background: #0891b2;
  opacity: 0.06;
}

:global(html.light) .glow-2 {
  background: #06b6d4;
  opacity: 0.05;
}

:global(html.light) .back-btn {
  background: rgba(8, 145, 178, 0.1);
  border-color: rgba(8, 145, 178, 0.2);
  color: #0891b2;
}

:global(html.light) .header-info h1 i {
  color: #0891b2;
}

:global(html.light) .stat-pill {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .stat-num {
  color: #0891b2;
}

:global(html.light) .tabs-bar {
  background: rgba(8, 145, 178, 0.05);
}

:global(html.light) .tab-btn {
  background: transparent;
  color: #64748b;
}

:global(html.light) .tab-btn.active {
  background: #ffffff;
  color: #0891b2;
  box-shadow: 0 2px 8px rgba(8, 145, 178, 0.15);
}

:global(html.light) .filter-bar {
  background: rgba(8, 145, 178, 0.04);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .search-box {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .search-box input {
  color: #0c4a6e;
}

:global(html.light) .filter-select {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .application-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .application-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .application-card.pending {
  border-left-color: #d97706;
}

:global(html.light) .application-card.accepted {
  border-left-color: #059669;
}

:global(html.light) .application-card.rejected {
  border-left-color: #dc2626;
}

:global(html.light) .application-card.interview {
  border-left-color: #0891b2;
}

:global(html.light) .app-name {
  color: #0c4a6e;
}

:global(html.light) .status-badge.pending {
  background: rgba(217, 119, 6, 0.12);
  color: #d97706;
}

:global(html.light) .status-badge.accepted {
  background: rgba(5, 150, 105, 0.12);
  color: #059669;
}

:global(html.light) .status-badge.rejected {
  background: rgba(220, 38, 38, 0.12);
  color: #dc2626;
}

:global(html.light) .status-badge.interview {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .app-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .app-tags .tag.secondary {
  background: rgba(100, 116, 139, 0.08);
  color: #64748b;
}

:global(html.light) .action-btn {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .action-btn:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .action-btn.accept {
  background: rgba(5, 150, 105, 0.12);
  color: #059669;
}

:global(html.light) .action-btn.accept:hover {
  background: rgba(5, 150, 105, 0.2);
}

:global(html.light) .action-btn.reject {
  background: rgba(220, 38, 38, 0.08);
  color: #dc2626;
}

:global(html.light) .action-btn.reject:hover {
  background: rgba(220, 38, 38, 0.15);
}

:global(html.light) .action-btn.primary {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .action-btn.primary:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .expand-section {
  background: rgba(8, 145, 178, 0.03);
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .expand-content h4 {
  color: #0c4a6e;
}

:global(html.light) .skill-tag {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .match-bar .label {
  color: #64748b;
}

:global(html.light) .match-bar .track {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .match-bar .percent {
  color: #0891b2;
}

:global(html.light) .empty-state {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .empty-state h3 {
  color: #0c4a6e;
}

:global(html.light) .batch-bar {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
  box-shadow: 0 -4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .batch-info {
  color: #0c4a6e;
}

:global(html.light) .btn-cancel {
  border-color: rgba(8, 145, 178, 0.2);
  color: #64748b;
}

:global(html.light) .btn-cancel:hover {
  background: rgba(8, 145, 178, 0.05);
}
</style>
