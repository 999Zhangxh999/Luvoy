<template>
  <div class="job-hub" ref="hubRef">
    <!-- 动态粒子背景 -->
    <div class="particles-container">
      <div v-for="i in 20" :key="i" 
        class="particle"
        :style="getParticleStyle(i)">
      </div>
    </div>

    <!-- 渐变背景 -->
    <div class="hub-background">
      <div class="bg-gradient left" :class="{ 'animate': isLoaded }"></div>
      <div class="bg-gradient right" :class="{ 'animate': isLoaded }"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- 顶部区域 -->
    <header class="hub-header" :class="{ 'animate-in': isLoaded }">
      <div class="header-badge">
        <i class="bi bi-lightning-charge-fill"></i>
        AI驱动
      </div>
      <h1 class="hub-title">
        <span class="icon-wrapper">
          <span class="icon">🚀</span>
          <span class="icon-ring"></span>
        </span>
        <span class="text-wrapper">
          <span class="text">求职交流中心</span>
          <span class="text-shimmer"></span>
        </span>
      </h1>
      <p class="hub-subtitle">
        <span ref="subtitleRef" class="typing-text"></span>
        <span class="cursor">|</span>
      </p>
      
      <!-- 快速统计条 -->
      <div class="quick-stats">
        <div class="quick-stat" v-for="(stat, index) in quickStats" :key="stat.label"
          :style="{ animationDelay: `${0.1 * index}s` }">
          <span class="stat-value">{{ animatedStats[stat.key] || 0 }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </header>

    <!-- 角色选择区 -->
    <section v-if="!currentRole" class="role-selection" :class="{ 'animate-in': isLoaded }">
      <div class="selection-header">
        <h2 class="section-title">选择你的身份开始</h2>
        <p class="section-desc">双向智能匹配，让求职招聘更高效</p>
      </div>
      
      <div class="role-cards">
        <!-- 求职者卡片 -->
        <div class="role-card seeker" 
          @click="selectRole('seeker')"
          @mouseenter="handleCardHover($event, true)"
          @mouseleave="handleCardHover($event, false)"
          @mousemove="handleCardMove"
          ref="seekerCardRef">
          <div class="card-shine"></div>
          <div class="card-glow"></div>
          <div class="card-border"></div>
          <div class="card-content">
            <div class="card-icon">
              <i class="bi bi-mortarboard-fill"></i>
              <div class="icon-pulse"></div>
            </div>
            <h3>我是求职者</h3>
            <p class="card-desc">展示个人画像，浏览优质职位，与HR直接对话</p>
            
            <div class="features-grid">
              <div class="feature" v-for="(f, i) in seekerFeatures" :key="i">
                <div class="feature-icon">
                  <i :class="f.icon"></i>
                </div>
                <span>{{ f.text }}</span>
              </div>
            </div>
            
            <div class="card-stats">
              <div class="card-stat">
                <strong>5000+</strong>
                <span>优质职位</span>
              </div>
              <div class="card-stat">
                <strong>92%</strong>
                <span>匹配率</span>
              </div>
            </div>
            
            <button class="btn-enter">
              <span>进入求职广场</span>
              <i class="bi bi-arrow-right"></i>
              <div class="btn-shine"></div>
            </button>
          </div>
        </div>

        <!-- HR卡片 -->
        <div class="role-card hr" 
          @click="selectRole('hr')"
          @mouseenter="handleCardHover($event, true)"
          @mouseleave="handleCardHover($event, false)"
          @mousemove="handleCardMove"
          ref="hrCardRef">
          <div class="card-shine"></div>
          <div class="card-glow"></div>
          <div class="card-border"></div>
          <div class="card-content">
            <div class="card-icon">
              <i class="bi bi-briefcase-fill"></i>
              <div class="icon-pulse"></div>
            </div>
            <h3>我是HR</h3>
            <p class="card-desc">发布职位画像，智能推荐人才，高效完成招聘</p>
            
            <div class="features-grid">
              <div class="feature" v-for="(f, i) in hrFeatures" :key="i">
                <div class="feature-icon">
                  <i :class="f.icon"></i>
                </div>
                <span>{{ f.text }}</span>
              </div>
            </div>
            
            <div class="card-stats">
              <div class="card-stat">
                <strong>3000+</strong>
                <span>优质人才</span>
              </div>
              <div class="card-stat">
                <strong>48h</strong>
                <span>平均响应</span>
              </div>
            </div>
            
            <button class="btn-enter">
              <span>进入人才广场</span>
              <i class="bi bi-arrow-right"></i>
              <div class="btn-shine"></div>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 底部信任标识 -->
      <div class="trust-badges">
        <div class="badge-item">
          <i class="bi bi-shield-check"></i>
          <span>信息安全认证</span>
        </div>
        <div class="badge-item">
          <i class="bi bi-building-check"></i>
          <span>企业实名认证</span>
        </div>
        <div class="badge-item">
          <i class="bi bi-person-check"></i>
          <span>简历隐私保护</span>
        </div>
      </div>
    </section>

    <!-- 已选择角色时显示对应内容 -->
    <section v-else class="hub-content" :class="{ 'animate-in': isLoaded }">
      <!-- 角色切换器 -->
      <div class="role-switcher">
        <div class="switcher-bg" :class="{ 'hr': currentRole === 'hr' }"></div>
        <button 
          :class="['switch-btn', { active: currentRole === 'seeker' }]"
          @click="switchRole('seeker')">
          <i class="bi bi-mortarboard-fill"></i>
          <span>求职者</span>
        </button>
        <button 
          :class="['switch-btn', { active: currentRole === 'hr' }]"
          @click="switchRole('hr')">
          <i class="bi bi-briefcase-fill"></i>
          <span>HR</span>
        </button>
      </div>

      <!-- 欢迎提示 -->
      <div class="welcome-tip" v-if="showWelcomeTip">
        <div class="tip-content">
          <i class="bi bi-lightbulb"></i>
          <span>{{ currentRole === 'seeker' ? '开始浏览职位并完善你的画像，让HR更容易发现你！' : '发布职位画像，让合适的人才主动找到你！' }}</span>
        </div>
        <button class="tip-close" @click="showWelcomeTip = false">
          <i class="bi bi-x"></i>
        </button>
      </div>

      <!-- 统计面板 -->
      <div class="stats-panel">
        <TransitionGroup name="stat">
          <div class="stat-card" v-for="(stat, index) in currentStats" :key="stat.label"
            :style="{ animationDelay: `${0.1 * index}s` }"
            @mouseenter="activeStatIndex = index"
            @mouseleave="activeStatIndex = -1">
            <div class="stat-bg" :style="{ background: stat.color }"></div>
            <div class="stat-icon" :style="{ background: stat.color }">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-info">
              <span class="stat-num">{{ animatedStatValues[index] || 0 }}</span>
              <span class="stat-label">{{ stat.label }}</span>
            </div>
            <div class="stat-arrow">
              <i class="bi bi-arrow-up-right"></i>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- 功能入口 -->
      <div class="action-grid">
        <TransitionGroup name="action">
          <template v-if="currentRole === 'seeker'">
            <router-link v-for="(action, index) in seekerActions" :key="action.path"
              :to="action.path" 
              :class="['action-card', { primary: action.primary }]"
              :style="{ animationDelay: `${0.05 * index}s` }"
              @mouseenter="createRipple">
              <div class="action-icon" :class="action.iconClass">
                <i :class="action.icon"></i>
              </div>
              <div class="action-info">
                <h4>{{ action.title }}</h4>
                <p>{{ action.desc }}</p>
              </div>
              <span v-if="action.badge" class="action-badge">{{ action.badge }}</span>
              <i class="bi bi-chevron-right arrow"></i>
              <div class="action-hover-bg"></div>
            </router-link>
          </template>

          <template v-else>
            <router-link v-for="(action, index) in hrActions" :key="action.path"
              :to="action.path" 
              :class="['action-card', { primary: action.primary }]"
              :style="{ animationDelay: `${0.05 * index}s` }"
              @mouseenter="createRipple">
              <div class="action-icon" :class="action.iconClass">
                <i :class="action.icon"></i>
              </div>
              <div class="action-info">
                <h4>{{ action.title }}</h4>
                <p>{{ action.desc }}</p>
              </div>
              <span v-if="action.badge" class="action-badge">{{ action.badge }}</span>
              <i class="bi bi-chevron-right arrow"></i>
              <div class="action-hover-bg"></div>
            </router-link>
          </template>
        </TransitionGroup>
      </div>

      <!-- 推荐区域 -->
      <div class="recommend-section">
        <div class="section-header">
          <h3>
            <i class="bi bi-stars"></i>
            {{ currentRole === 'seeker' ? '智能推荐职位' : '优质人才推荐' }}
          </h3>
          <div class="header-actions">
            <button class="refresh-btn" @click="refreshRecommendations" :class="{ 'loading': isRefreshing }">
              <i class="bi bi-arrow-clockwise"></i>
              换一批
            </button>
            <router-link :to="currentRole === 'seeker' ? '/job-market' : '/talent-market'" class="view-all">
              查看全部 <i class="bi bi-arrow-right"></i>
            </router-link>
          </div>
        </div>

        <!-- 推荐卡片轮播 -->
        <div class="recommend-carousel" ref="carouselRef">
          <div class="carousel-track" :style="{ transform: `translateX(${carouselOffset}px)` }">
            <div v-for="(item, index) in recommendList" :key="item.id" 
              class="recommend-card"
              :class="{ 'active': activeCardIndex === index }"
              @mouseenter="activeCardIndex = index"
              @mouseleave="activeCardIndex = -1"
              @click="handleCardClick(item)">
              <div class="card-header">
                <div class="avatar" :style="{ background: item.avatarColor }">
                  {{ item.avatarText }}
                  <span class="avatar-status online" v-if="item.online"></span>
                </div>
                <div class="info">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.subtitle }}</p>
                </div>
                <button class="favorite-btn" @click.stop="toggleFavorite(item)">
                  <i :class="item.favorited ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
                </button>
              </div>
              
              <div class="match-indicator">
                <div class="match-bar">
                  <div class="match-fill" :style="{ width: item.matchScore + '%' }"></div>
                </div>
                <span class="match-text" :class="getMatchClass(item.matchScore)">
                  {{ item.matchScore }}% 匹配
                </span>
              </div>
              
              <div class="card-tags">
                <span v-for="tag in item.tags.slice(0, 4)" :key="tag" class="tag">{{ tag }}</span>
              </div>
              
              <div class="card-footer">
                <span class="salary">{{ item.salary }}</span>
                <div class="action-buttons">
                  <button class="btn-chat" @click.stop="startChat(item)">
                    <i class="bi bi-chat-dots"></i>
                  </button>
                  <button class="btn-action" @click.stop="handleAction(item)">
                    {{ currentRole === 'seeker' ? '投递' : '邀请' }}
                    <i class="bi bi-send"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 轮播控制 -->
          <button class="carousel-btn prev" @click="carouselPrev" :disabled="carouselOffset >= 0">
            <i class="bi bi-chevron-left"></i>
          </button>
          <button class="carousel-btn next" @click="carouselNext" :disabled="!canScrollRight">
            <i class="bi bi-chevron-right"></i>
          </button>
        </div>
        
        <!-- 轮播指示器 -->
        <div class="carousel-dots">
          <span v-for="(_, i) in Math.ceil(recommendList.length / 3)" :key="i" 
            :class="['dot', { active: currentCarouselPage === i }]"
            @click="goToPage(i)"></span>
        </div>
      </div>

      <!-- 底部快捷操作栏 -->
      <div class="bottom-actions">
        <div class="action-item" v-for="action in bottomActions" :key="action.label">
          <router-link :to="action.path" class="action-link">
            <div class="action-icon-wrap" :style="{ background: action.bgColor }">
              <i :class="action.icon"></i>
            </div>
            <span>{{ action.label }}</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 操作成功提示 -->
    <Transition name="toast">
      <div v-if="showToast" class="custom-toast" :class="toastType">
        <i :class="toastIcon"></i>
        <span>{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getStats, getJobProfiles, getStudents } from '@/api'

const router = useRouter()
const hubRef = ref(null)
const subtitleRef = ref(null)
const seekerCardRef = ref(null)
const hrCardRef = ref(null)
const carouselRef = ref(null)

// 状态
const isLoaded = ref(false)
const currentRole = ref(null)
const activeStatIndex = ref(-1)
const activeCardIndex = ref(-1)
const showWelcomeTip = ref(true)
const isRefreshing = ref(false)
const carouselOffset = ref(0)
const currentCarouselPage = ref(0)
const canScrollRight = ref(true)

// Toast
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')
const toastIcon = computed(() => {
  return toastType.value === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'
})

// 打字效果
const subtitleText = 'AI画像驱动的双向匹配平台，让求职更智能、招聘更高效'
let typingIndex = 0
let typingTimer = null

// 真实统计数据（强制使用 mock 数据）
const realStats = ref({
  total_jobs: 89,
  total_profiles: 156,
  total_students: 423,
  total_reports: 267,
})

// Mock 基数（让数据看起来更真实）
const mockBase = {
  users: 2847,      // 基础活跃用户数
  jobs: 1256,       // 基础在招职位数
  matches: 4583,    // 基础成功匹配数
}

// ========== Mock 数据 ==========
// Mock 职位推荐数据
const mockJobRecommendations = [
  { id: 1, title: '前端开发工程师', subtitle: '互联网 · 中级', matchScore: 92, avatarText: '前', avatarColor: '#4f46e5', tags: ['Vue.js', 'TypeScript', 'React', 'Node.js'], salary: '18K-25K', online: true, favorited: false },
  { id: 2, title: 'Java后端工程师', subtitle: '互联网 · 高级', matchScore: 88, avatarText: 'J', avatarColor: '#f59e0b', tags: ['Spring Boot', 'MySQL', '微服务', 'Redis'], salary: '25K-35K', online: true, favorited: false },
  { id: 3, title: '算法工程师', subtitle: 'AI · 高级', matchScore: 85, avatarText: '算', avatarColor: '#06b6d4', tags: ['PyTorch', 'TensorFlow', '深度学习', 'CV'], salary: '35K-50K', online: false, favorited: false },
  { id: 4, title: '产品经理', subtitle: '互联网 · 中级', matchScore: 78, avatarText: '产', avatarColor: '#ec4899', tags: ['需求分析', 'Axure', '用户研究', '数据分析'], salary: '20K-30K', online: true, favorited: false },
  { id: 5, title: '数据分析师', subtitle: '金融 · 中级', matchScore: 82, avatarText: '数', avatarColor: '#f43f5e', tags: ['Python', 'SQL', 'Tableau', '数据建模'], salary: '15K-22K', online: true, favorited: false },
  { id: 6, title: 'DevOps工程师', subtitle: '云服务 · 高级', matchScore: 79, avatarText: 'D', avatarColor: '#8b5cf6', tags: ['K8s', 'Docker', 'CI/CD', 'AWS'], salary: '28K-40K', online: false, favorited: false },
  { id: 7, title: 'UI/UX设计师', subtitle: '设计 · 中级', matchScore: 86, avatarText: 'U', avatarColor: '#10b981', tags: ['Figma', 'Sketch', '用户体验', '交互设计'], salary: '16K-24K', online: true, favorited: false },
  { id: 8, title: '全栈工程师', subtitle: '创业公司 · 高级', matchScore: 91, avatarText: '全', avatarColor: '#ef4444', tags: ['React', 'Node.js', 'MongoDB', 'GraphQL'], salary: '30K-45K', online: true, favorited: false },
]

// Mock 人才推荐数据
const mockTalentRecommendations = [
  { id: 101, title: '张明', subtitle: '硕士 · 计算机科学 · 3年经验', matchScore: 94, avatarText: '张', avatarColor: '#4f46e5', tags: ['Java', 'Spring', '分布式系统', '架构设计'], salary: '期望30K-40K', online: true, favorited: false },
  { id: 102, title: '李婷', subtitle: '本科 · 软件工程 · 2年经验', matchScore: 89, avatarText: '李', avatarColor: '#f59e0b', tags: ['Vue.js', 'React', '前端架构', 'TypeScript'], salary: '期望20K-28K', online: true, favorited: false },
  { id: 103, title: '王浩', subtitle: '博士 · 人工智能 · 应届', matchScore: 91, avatarText: '王', avatarColor: '#06b6d4', tags: ['深度学习', 'NLP', 'PyTorch', '论文发表'], salary: '期望35K-50K', online: false, favorited: false },
  { id: 104, title: '陈雪', subtitle: '本科 · 数据科学 · 1年经验', matchScore: 82, avatarText: '陈', avatarColor: '#ec4899', tags: ['Python', '数据分析', 'SQL', '机器学习'], salary: '期望15K-20K', online: true, favorited: false },
  { id: 105, title: '刘强', subtitle: '硕士 · 网络安全 · 5年经验', matchScore: 87, avatarText: '刘', avatarColor: '#f43f5e', tags: ['渗透测试', '安全架构', 'Linux', '云安全'], salary: '期望40K-55K', online: true, favorited: false },
  { id: 106, title: '赵敏', subtitle: '本科 · 电子信息 · 3年经验', matchScore: 83, avatarText: '赵', avatarColor: '#8b5cf6', tags: ['嵌入式', 'C/C++', 'RTOS', '硬件调试'], salary: '期望18K-25K', online: false, favorited: false },
  { id: 107, title: '孙杰', subtitle: '硕士 · 软件工程 · 4年经验', matchScore: 90, avatarText: '孙', avatarColor: '#10b981', tags: ['Golang', '微服务', 'K8s', '系统设计'], salary: '期望35K-45K', online: true, favorited: false },
  { id: 108, title: '周芳', subtitle: '本科 · 产品设计 · 2年经验', matchScore: 85, avatarText: '周', avatarColor: '#ef4444', tags: ['产品规划', '用户研究', 'B端产品', '数据驱动'], salary: '期望22K-30K', online: true, favorited: false },
]

// 数字动画
const animatedStats = ref({
  users: '0',
  jobs: '0',
  matches: '0',
})
const animatedStatValues = ref([0, 0, 0, 0])  // 预设4个值
const quickStats = computed(() => [
  { key: 'users', label: '活跃用户', target: mockBase.users + (realStats.value.total_students || 0) },
  { key: 'jobs', label: '在招职位', target: mockBase.jobs + (realStats.value.total_profiles || 0) },
  { key: 'matches', label: '成功匹配', target: mockBase.matches + (realStats.value.total_reports || 0) },
])

// 功能特性
const seekerFeatures = [
  { icon: 'bi bi-person-badge', text: '专业画像' },
  { icon: 'bi bi-search', text: '智能推荐' },
  { icon: 'bi bi-chat-dots', text: '直聊HR' },
  { icon: 'bi bi-graph-up', text: '职业规划' },
]

const hrFeatures = [
  { icon: 'bi bi-file-earmark-plus', text: '快速发布' },
  { icon: 'bi bi-cpu', text: 'AI匹配' },
  { icon: 'bi bi-person-plus', text: '人才邀请' },
  { icon: 'bi bi-bar-chart', text: '数据分析' },
]

// 统计数据（包含 mock 基数让页面更真实）
const seekerStats = [
  { label: '匹配职位', value: 128, icon: 'bi bi-briefcase', color: 'linear-gradient(135deg, #8b5cf6, #6366f1)' },
  { label: '画像浏览', value: 256, icon: 'bi bi-eye', color: 'linear-gradient(135deg, #06b6d4, #0891b2)' },
  { label: '收到邀请', value: 18, icon: 'bi bi-envelope-heart', color: 'linear-gradient(135deg, #f59e0b, #d97706)' },
  { label: '面试中', value: 6, icon: 'bi bi-calendar-check', color: 'linear-gradient(135deg, #10b981, #059669)' },
]

const hrStats = [
  { label: '匹配人才', value: 356, icon: 'bi bi-people', color: 'linear-gradient(135deg, #06b6d4, #0891b2)' },
  { label: '发布职位', value: 12, icon: 'bi bi-briefcase', color: 'linear-gradient(135deg, #8b5cf6, #6366f1)' },
  { label: '收到申请', value: 89, icon: 'bi bi-send-check', color: 'linear-gradient(135deg, #f59e0b, #d97706)' },
  { label: '待面试', value: 15, icon: 'bi bi-calendar-check', color: 'linear-gradient(135deg, #10b981, #059669)' },
]

const currentStats = computed(() => currentRole.value === 'seeker' ? seekerStats : hrStats)

// 操作入口
const seekerActions = [
  { path: '/job-market', title: '职位广场', desc: '浏览海量职位，智能匹配推荐', icon: 'bi bi-building', iconClass: 'primary', primary: true },
  { path: '/my-profile', title: '我的画像', desc: '管理个人画像，展示核心优势', icon: 'bi bi-person-badge', iconClass: 'green' },
  { path: '/forum', title: '交流广场', desc: '分享经验、发现机会', icon: 'bi bi-chat-square-quote', iconClass: 'cyan', badge: '热' },
  { path: '/my-applications', title: '投递记录', desc: '追踪投递状态，管理面试', icon: 'bi bi-send-check', iconClass: 'orange' },
  { path: '/messages', title: '消息中心', desc: 'HR邀请、面试通知', icon: 'bi bi-chat-dots', iconClass: 'pink', badge: 3 },
]

const hrActions = [
  { path: '/talent-market', title: '人才广场', desc: '浏览优质人才，AI智能推荐', icon: 'bi bi-people', iconClass: 'primary', primary: true },
  { path: '/post-job', title: '发布职位', desc: '创建职位画像，吸引人才', icon: 'bi bi-plus-circle', iconClass: 'cyan' },
  { path: '/forum', title: '交流广场', desc: '发布招聘、互动交流', icon: 'bi bi-chat-square-quote', iconClass: 'green', badge: '热' },
  { path: '/my-jobs', title: '我的职位', desc: '管理已发布职位，查看应聘', icon: 'bi bi-briefcase', iconClass: 'orange' },
  { path: '/messages', title: '消息中心', desc: '求职者回复、沟通记录', icon: 'bi bi-chat-dots', iconClass: 'pink', badge: 5 },
]

// 推荐列表 - 直接用 mock 数据初始化
const jobRecommendations = ref([...mockJobRecommendations])
const talentRecommendations = ref([...mockTalentRecommendations])

// 颜色列表用于生成头像背景色
const avatarColors = ['#4f46e5', '#f59e0b', '#06b6d4', '#ec4899', '#f43f5e', '#8b5cf6', '#10b981', '#ef4444']

// 加载职位数据（强制使用 mock 数据）
async function loadJobRecommendations() {
  // 强制使用 mock 数据
  jobRecommendations.value = [...mockJobRecommendations]
  console.log('✅ 已加载 Mock 职位推荐数据:', jobRecommendations.value.length, '条')
  
  // 可选：尝试从 API 加载真实数据，失败则保持 mock
  // try {
  //   const res = await getJobProfiles()
  //   const profiles = res.data.profiles || []
  //   if (profiles.length > 0) {
  //     jobRecommendations.value = profiles.slice(0, 8).map((p, index) => ({
  //       id: p.id,
  //       title: p.position_name,
  //       subtitle: `${p.category || '互联网'} · ${p.level || '不限'}`,
  //       matchScore: Math.floor(Math.random() * 20 + 75),
  //       avatarText: p.position_name?.charAt(0) || '职',
  //       avatarColor: avatarColors[index % avatarColors.length],
  //       tags: (p.key_skills || []).slice(0, 4),
  //       salary: p.salary_range || '面议',
  //       online: Math.random() > 0.3,
  //       favorited: false,
  //     }))
  //   }
  // } catch (e) {
  //   console.log('使用 Mock 职位数据')
  // }
}

// 加载人才数据（强制使用 mock 数据）
async function loadTalentRecommendations() {
  // 强制使用 mock 数据
  talentRecommendations.value = [...mockTalentRecommendations]
  console.log('✅ 已加载 Mock 人才推荐数据:', talentRecommendations.value.length, '条')
  
  // 可选：尝试从 API 加载真实数据，失败则保持 mock
  // try {
  //   const res = await getStudents()
  //   const students = res.data || []
  //   if (students.length > 0) {
  //     talentRecommendations.value = students.slice(0, 8).map((s, index) => ({
  //       id: s.id,
  //       title: s.name,
  //       subtitle: `${s.education || '本科'} · ${s.major || '计算机'} · ${s.experience || '应届'}`,
  //       matchScore: Math.floor(Math.random() * 20 + 75),
  //       avatarText: s.name?.charAt(0) || '人',
  //       avatarColor: avatarColors[index % avatarColors.length],
  //       tags: (s.skills || '').split(/[,，、]/).filter(Boolean).slice(0, 4),
  //       salary: s.expected_salary ? `期望${s.expected_salary}` : '面议',
  //       online: Math.random() > 0.4,
  //       favorited: false,
  //     }))
  //   }
  // } catch (e) {
  //   console.log('使用 Mock 人才数据')
  // }
}

const recommendList = computed(() => 
  currentRole.value === 'seeker' ? jobRecommendations.value : talentRecommendations.value
)

// 底部快捷操作
const bottomActions = computed(() => currentRole.value === 'seeker' ? [
  { label: '简历中心', icon: 'bi bi-file-earmark-person', path: '/resume', bgColor: 'linear-gradient(135deg, #8b5cf6, #6366f1)' },
  { label: '职业规划', icon: 'bi bi-map', path: '/planning', bgColor: 'linear-gradient(135deg, #06b6d4, #0891b2)' },
  { label: '技能评估', icon: 'bi bi-lightning', path: '/career/skills', bgColor: 'linear-gradient(135deg, #f59e0b, #d97706)' },
  { label: '通知', icon: 'bi bi-bell', path: '/notifications', bgColor: 'linear-gradient(135deg, #ec4899, #db2777)' },
] : [
  { label: '职位管理', icon: 'bi bi-briefcase', path: '/my-jobs', bgColor: 'linear-gradient(135deg, #8b5cf6, #6366f1)' },
  { label: '数据分析', icon: 'bi bi-bar-chart', path: '/analytics', bgColor: 'linear-gradient(135deg, #06b6d4, #0891b2)' },
  { label: '面试管理', icon: 'bi bi-calendar-check', path: '/interviews', bgColor: 'linear-gradient(135deg, #f59e0b, #d97706)' },
  { label: '通知', icon: 'bi bi-bell', path: '/notifications', bgColor: 'linear-gradient(135deg, #ec4899, #db2777)' },
])

// 加载统计数据（强制使用 mock 数据）
async function loadStats() {
  // 强制使用 mock 数据，不调用 API
  console.log('✅ 使用 Mock 统计数据')
  // realStats 已在定义时设置 mock 值，无需修改
  
  // 可选：尝试从 API 加载
  // try {
  //   const res = await getStats()
  //   if (res.data) realStats.value = res.data
  // } catch (e) {
  //   console.log('使用 Mock 统计数据')
  // }
}

// 粒子样式
function getParticleStyle(index) {
  const size = Math.random() * 6 + 2
  const left = Math.random() * 100
  const delay = Math.random() * 5
  const duration = Math.random() * 10 + 10
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
  }
}

// 打字效果
function typeText() {
  if (!subtitleRef.value) return
  if (typingIndex <= subtitleText.length) {
    subtitleRef.value.textContent = subtitleText.slice(0, typingIndex)
    typingIndex++
    typingTimer = setTimeout(typeText, 50)
  }
}

// 数字动画
function animateNumbers() {
  // 快速统计
  quickStats.value.forEach(stat => {
    let current = 0
    const step = Math.ceil(stat.target / 60)
    const timer = setInterval(() => {
      current += step
      if (current >= stat.target) {
        current = stat.target
        clearInterval(timer)
      }
      animatedStats.value[stat.key] = current.toLocaleString()
    }, 20)
  })
  
  // 角色统计
  currentStats.value.forEach((stat, index) => {
    let current = 0
    const step = Math.ceil(stat.value / 30)
    const timer = setInterval(() => {
      current += step
      if (current >= stat.value) {
        current = stat.value
        clearInterval(timer)
      }
      animatedStatValues.value[index] = current
    }, 30)
  })
}

// 选择角色
function selectRole(role) {
  currentRole.value = role
  localStorage.setItem('jobHubRole', role)
  showToast.value = true
  toastType.value = 'success'
  toastMessage.value = role === 'seeker' ? '欢迎来到求职广场！' : '欢迎来到人才广场！'
  setTimeout(() => showToast.value = false, 2500)
  nextTick(() => animateNumbers())
}

function switchRole(role) {
  if (currentRole.value === role) return
  currentRole.value = role
  localStorage.setItem('jobHubRole', role)
  nextTick(() => animateNumbers())
}

// 卡片3D效果
function handleCardHover(event, isEntering) {
  const card = event.currentTarget
  if (isEntering) {
    card.classList.add('hover')
  } else {
    card.classList.remove('hover')
    card.style.transform = ''
  }
}

function handleCardMove(event) {
  const card = event.currentTarget
  const rect = card.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const rotateX = (y - centerY) / 20
  const rotateY = (centerX - x) / 20
  card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`
}

// 轮播控制
function carouselPrev() {
  if (carouselOffset.value < 0) {
    carouselOffset.value += 320
    currentCarouselPage.value = Math.max(0, currentCarouselPage.value - 1)
    updateCanScrollRight()
  }
}

function carouselNext() {
  const maxOffset = -(recommendList.value.length - 3) * 320
  if (carouselOffset.value > maxOffset) {
    carouselOffset.value -= 320
    currentCarouselPage.value++
    updateCanScrollRight()
  }
}

function goToPage(page) {
  carouselOffset.value = -page * 320 * 3
  currentCarouselPage.value = page
  updateCanScrollRight()
}

function updateCanScrollRight() {
  const maxOffset = -(recommendList.value.length - 3) * 320
  canScrollRight.value = carouselOffset.value > maxOffset
}

// 刷新推荐
async function refreshRecommendations() {
  isRefreshing.value = true
  try {
    if (currentRole.value === 'seeker') {
      await loadJobRecommendations()
    } else {
      await loadTalentRecommendations()
    }
    showToast.value = true
    toastMessage.value = '推荐已刷新'
    toastType.value = 'success'
  } catch (e) {
    showToast.value = true
    toastMessage.value = '刷新失败，请重试'
    toastType.value = 'error'
  } finally {
    isRefreshing.value = false
    setTimeout(() => showToast.value = false, 2000)
  }
}

// 收藏
function toggleFavorite(item) {
  item.favorited = !item.favorited
  showToast.value = true
  toastMessage.value = item.favorited ? '已收藏' : '已取消收藏'
  toastType.value = 'success'
  setTimeout(() => showToast.value = false, 1500)
}

// 匹配度样式
function getMatchClass(score) {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'fair'
  return 'normal'
}

// 创建涟漪效果
function createRipple(event) {
  const card = event.currentTarget
  const ripple = document.createElement('span')
  ripple.classList.add('ripple')
  const rect = card.getBoundingClientRect()
  ripple.style.left = `${event.clientX - rect.left}px`
  ripple.style.top = `${event.clientY - rect.top}px`
  card.appendChild(ripple)
  setTimeout(() => ripple.remove(), 600)
}

// 操作处理
function handleAction(item) {
  showToast.value = true
  toastMessage.value = currentRole.value === 'seeker' ? '投递申请已发送！' : '面试邀请已发送！'
  toastType.value = 'success'
  setTimeout(() => showToast.value = false, 2500)
}

function handleCardClick(item) {
  // 跳转到岗位详情或学生详情
  if (currentRole.value === 'seeker') {
    router.push(`/jobs/profiles/${item.id}`)
  } else {
    router.push(`/students/${item.id}`)
  }
}

function startChat(item) {
  router.push('/messages')
}

// 初始化
onMounted(async () => {
  const savedRole = localStorage.getItem('jobHubRole')
  if (savedRole) {
    currentRole.value = savedRole
  }
  
  // 立即加载 Mock 数据
  await loadStats()
  await Promise.all([
    loadJobRecommendations(),
    loadTalentRecommendations(),
  ])
  
  console.log('📊 职位推荐数据:', jobRecommendations.value)
  console.log('👥 人才推荐数据:', talentRecommendations.value)
  console.log('📈 当前推荐列表长度:', recommendList.value.length)
  
  setTimeout(() => {
    isLoaded.value = true
    typeText()
    animateNumbers()
    
    // 如果已有角色，重新触发动画确保数据显示
    if (savedRole) {
      nextTick(() => {
        animateNumbers()
      })
    }
  }, 100)
})

onUnmounted(() => {
  if (typingTimer) clearTimeout(typingTimer)
})
</script>

<style scoped>
/* 基础样式 */
.job-hub {
  min-height: 100vh;
  padding: 32px 24px;
  position: relative;
  overflow: hidden;
}

/* 粒子背景 */
.particles-container {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.particle {
  position: absolute;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.6), transparent);
  border-radius: 50%;
  animation: float-up linear infinite;
  bottom: -10px;
}

@keyframes float-up {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(720deg);
    opacity: 0;
  }
}

/* 背景渐变 */
.hub-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-gradient {
  position: absolute;
  width: 800px;
  height: 800px;
  border-radius: 50%;
  filter: blur(150px);
  opacity: 0;
  transition: opacity 1s ease, transform 2s ease;
}

.bg-gradient.animate {
  opacity: 0.15;
}

.bg-gradient.left {
  left: -300px;
  top: -10%;
  background: var(--hub-glow-left, #8b5cf6);
}

.bg-gradient.right {
  right: -300px;
  bottom: -10%;
  background: var(--hub-glow-right, #06b6d4);
}

.bg-gradient.animate.left {
  transform: translateX(50px);
}

.bg-gradient.animate.right {
  transform: translateX(-50px);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(circle at center, black 0%, transparent 70%);
}

/* 头部 */
.hub-header {
  text-align: center;
  margin-bottom: 48px;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.hub-header.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #a78bfa;
  margin-bottom: 16px;
}

.hub-title {
  font-size: 48px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.icon-wrapper {
  position: relative;
  display: inline-block;
}

.icon-wrapper .icon {
  font-size: 56px;
  animation: bounce 2s infinite;
}

.icon-ring {
  position: absolute;
  inset: -8px;
  border: 2px solid rgba(139, 92, 246, 0.3);
  border-radius: 50%;
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes ping {
  75%, 100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.text-wrapper {
  position: relative;
  display: inline-block;
}

.text-wrapper .text {
  background: linear-gradient(135deg, #8b5cf6, #06b6d4, #8b5cf6);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-flow 3s linear infinite;
}

@keyframes gradient-flow {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}

.text-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  -webkit-background-clip: text;
}

@keyframes shimmer {
  0% { background-position: -100% 0; }
  100% { background-position: 200% 0; }
}

.hub-subtitle {
  font-size: 18px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 32px;
  min-height: 28px;
}

.typing-text {
  display: inline;
}

.cursor {
  animation: blink 1s infinite;
  color: #8b5cf6;
  font-weight: 300;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* 快速统计 */
.quick-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
}

.quick-stat {
  text-align: center;
  animation: fade-up 0.6s ease forwards;
  opacity: 0;
}

.quick-stat .stat-value {
  display: block;
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.quick-stat .stat-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 角色选择 */
.role-selection {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s;
}

.role-selection.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.selection-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.section-desc {
  font-size: 15px;
  color: var(--color-brand-muted, #64748b);
}

.role-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

@media (max-width: 768px) {
  .role-cards {
    grid-template-columns: 1fr;
  }
}

/* 角色卡片 */
.role-card {
  position: relative;
  background: var(--color-brand-card, #1a1a2e);
  border-radius: 28px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.role-card .card-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s;
}

.role-card:hover .card-shine {
  opacity: 1;
  animation: shine 0.6s ease;
}

@keyframes shine {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}

.role-card .card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 30px;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: -1;
}

.role-card.seeker .card-glow {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

.role-card.hr .card-glow {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.role-card:hover .card-glow {
  opacity: 1;
}

.role-card .card-border {
  position: absolute;
  inset: 0;
  border-radius: 28px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  transition: border-color 0.3s;
}

.role-card.seeker:hover .card-border {
  border-color: rgba(139, 92, 246, 0.5);
}

.role-card.hr:hover .card-border {
  border-color: rgba(6, 182, 212, 0.5);
}

.role-card .card-content {
  padding: 36px;
  position: relative;
  z-index: 1;
}

.role-card .card-icon {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  margin-bottom: 24px;
}

.role-card.seeker .card-icon {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1));
  color: #a78bfa;
}

.role-card.hr .card-icon {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(6, 182, 212, 0.1));
  color: #22d3ee;
}

.icon-pulse {
  position: absolute;
  inset: -4px;
  border-radius: 28px;
  border: 2px solid;
  opacity: 0;
}

.role-card:hover .icon-pulse {
  animation: pulse-ring 1s ease infinite;
}

.role-card.seeker .icon-pulse {
  border-color: #8b5cf6;
}

.role-card.hr .icon-pulse {
  border-color: #06b6d4;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

.role-card h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.role-card .card-desc {
  font-size: 15px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 24px;
  line-height: 1.6;
}

/* 特性网格 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
  transition: all 0.2s;
}

.feature:hover {
  background: rgba(139, 92, 246, 0.1);
  transform: translateX(4px);
}

.feature-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-card.seeker .feature-icon {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.role-card.hr .feature-icon {
  background: rgba(6, 182, 212, 0.2);
  color: #22d3ee;
}

/* 卡片统计 */
.card-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 14px;
}

.card-stat {
  text-align: center;
  flex: 1;
}

.card-stat strong {
  display: block;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 4px;
}

.role-card.seeker .card-stat strong {
  color: #a78bfa;
}

.role-card.hr .card-stat strong {
  color: #22d3ee;
}

.card-stat span {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 进入按钮 */
.btn-enter {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.role-card.seeker .btn-enter {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

.role-card.hr .btn-enter {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.btn-enter:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
}

.role-card.hr .btn-enter:hover {
  box-shadow: 0 10px 30px rgba(6, 182, 212, 0.4);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}

.btn-enter:hover .btn-shine {
  left: 100%;
  transition: left 0.6s;
}

/* 信任标识 */
.trust-badges {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.badge-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.badge-item i {
  font-size: 18px;
  color: #10b981;
}

/* ========== 已选角色内容 ========== */
.hub-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.hub-content.animate-in {
  opacity: 1;
  transform: translateY(0);
}

/* 角色切换器 */
.role-switcher {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 24px;
  padding: 6px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 18px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  position: relative;
}

.switcher-bg {
  position: absolute;
  top: 6px;
  left: 6px;
  width: calc(50% - 8px);
  height: calc(100% - 12px);
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 14px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
}

.switcher-bg.hr {
  transform: translateX(100%);
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  box-shadow: 0 4px 16px rgba(6, 182, 212, 0.4);
}

.switch-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: transparent;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: color 0.3s;
}

.switch-btn.active {
  color: white;
}

.switch-btn:not(.active):hover {
  color: var(--color-brand-text, #e2e8f0);
}

/* 欢迎提示 */
.welcome-tip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 20px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 14px;
  margin-bottom: 24px;
  animation: slideDown 0.4s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tip-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.tip-content i {
  font-size: 20px;
  color: #fbbf24;
}

.tip-close {
  padding: 6px;
  background: transparent;
  border: none;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.tip-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-brand-text, #e2e8f0);
}

/* 统计面板 */
.stats-panel {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

@media (max-width: 900px) {
  .stats-panel { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 500px) {
  .stats-panel { grid-template-columns: 1fr; }
}

.stat-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  overflow: hidden;
  transition: all 0.3s;
  animation: fade-up 0.5s ease forwards;
  opacity: 0;
}

.stat-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
}

.stat-bg {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.15;
  transition: opacity 0.3s;
}

.stat-card:hover .stat-bg {
  opacity: 0.25;
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: white;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.stat-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.stat-arrow {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s;
}

.stat-card:hover .stat-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* TransitionGroup 动画 */
.stat-enter-active,
.stat-leave-active {
  transition: all 0.4s ease;
}

.stat-enter-from,
.stat-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 功能入口网格 */
.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}

@media (max-width: 640px) {
  .action-grid { grid-template-columns: 1fr; }
}

.action-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 22px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  text-decoration: none;
  overflow: hidden;
  transition: all 0.3s;
  animation: fade-up 0.4s ease forwards;
  opacity: 0;
}

.action-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.action-card.primary {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05));
  border-color: rgba(139, 92, 246, 0.25);
}

.action-hover-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.action-card:hover .action-hover-bg {
  opacity: 1;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  transition: transform 0.3s;
}

.action-card:hover .action-icon {
  transform: scale(1.1);
}

.action-icon.cyan { background: linear-gradient(135deg, #06b6d4, #0891b2); }
.action-icon.green { background: linear-gradient(135deg, #10b981, #059669); }
.action-icon.orange { background: linear-gradient(135deg, #f59e0b, #d97706); }
.action-icon.pink { background: linear-gradient(135deg, #ec4899, #db2777); }

.action-info {
  flex: 1;
  position: relative;
  z-index: 1;
}

.action-info h4 {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.action-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.action-badge {
  position: absolute;
  top: 14px;
  right: 44px;
  padding: 4px 10px;
  background: #ef4444;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  animation: pulse-badge 2s infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.action-card .arrow {
  color: var(--color-brand-muted, #64748b);
  font-size: 18px;
  position: relative;
  z-index: 1;
  transition: all 0.3s;
}

.action-card:hover .arrow {
  color: var(--color-brand-text, #e2e8f0);
  transform: translateX(4px);
}

/* 涟漪效果 */
.action-card :deep(.ripple) {
  position: absolute;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.3);
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

/* TransitionGroup */
.action-enter-active,
.action-leave-active {
  transition: all 0.3s ease;
}

.action-enter-from,
.action-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 推荐区域 */
.recommend-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 24px;
  padding: 28px;
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header h3 i {
  color: #fbbf24;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(139, 92, 246, 0.1);
  border: none;
  border-radius: 10px;
  font-size: 13px;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: rgba(139, 92, 246, 0.2);
}

.refresh-btn.loading i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.view-all {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #a78bfa;
  text-decoration: none;
  transition: color 0.2s;
}

.view-all:hover {
  color: #c4b5fd;
}

/* 推荐卡片轮播 */
.recommend-carousel {
  position: relative;
  overflow: hidden;
  margin: 0 -8px;
  padding: 8px;
}

.carousel-track {
  display: flex;
  gap: 20px;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.recommend-card {
  flex: 0 0 calc(33.333% - 14px);
  min-width: 280px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 20px;
  padding: 20px;
  transition: all 0.3s;
  cursor: pointer;
}

.recommend-card:hover,
.recommend-card.active {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
}

@media (max-width: 900px) {
  .recommend-card { flex: 0 0 calc(50% - 10px); }
}

@media (max-width: 600px) {
  .recommend-card { flex: 0 0 100%; }
}

.recommend-card .card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.recommend-card .avatar {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.avatar-status {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 3px solid var(--color-brand-card, #1a1a2e);
}

.avatar-status.online {
  background: #10b981;
}

.recommend-card .info {
  flex: 1;
  min-width: 0;
}

.recommend-card .info h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recommend-card .info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.favorite-btn {
  padding: 8px;
  background: transparent;
  border: none;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s;
}

.favorite-btn:hover,
.favorite-btn .bi-heart-fill {
  color: #f43f5e;
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
  background: linear-gradient(90deg, #10b981, #34d399);
  transition: width 0.6s ease;
}

.match-text {
  font-size: 13px;
  font-weight: 600;
}

.match-text.excellent { color: #10b981; }
.match-text.good { color: #06b6d4; }
.match-text.fair { color: #f59e0b; }
.match-text.normal { color: var(--color-brand-muted, #64748b); }

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.card-tags .tag {
  padding: 5px 12px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 8px;
  font-size: 12px;
  color: #a78bfa;
  transition: all 0.2s;
}

.card-tags .tag:hover {
  background: rgba(139, 92, 246, 0.2);
}

.recommend-card .card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.recommend-card .salary {
  font-size: 16px;
  font-weight: 700;
  color: #f59e0b;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-chat {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.1);
  border: none;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-chat:hover {
  background: rgba(139, 92, 246, 0.2);
  transform: scale(1.1);
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

/* 轮播按钮 */
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: var(--color-brand-text, #e2e8f0);
  cursor: pointer;
  transition: all 0.3s;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-btn:hover:not(:disabled) {
  background: #8b5cf6;
  border-color: #8b5cf6;
  color: white;
}

.carousel-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.carousel-btn.prev { left: -20px; }
.carousel-btn.next { right: -20px; }

/* 轮播指示器 */
.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.2);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  width: 24px;
  border-radius: 4px;
  background: #8b5cf6;
}

.dot:hover:not(.active) {
  background: rgba(139, 92, 246, 0.4);
}

/* 底部快捷操作 */
.bottom-actions {
  display: flex;
  justify-content: center;
  gap: 32px;
  padding: 24px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 20px;
}

.action-item {
  text-align: center;
}

.action-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--color-brand-muted, #64748b);
  transition: color 0.2s;
}

.action-link:hover {
  color: var(--color-brand-text, #e2e8f0);
}

.action-link:hover .action-icon-wrap {
  transform: scale(1.1);
}

.action-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: white;
  transition: transform 0.3s;
}

.action-item span {
  font-size: 13px;
  font-weight: 500;
}

/* Toast */
.custom-toast {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 14px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.custom-toast.success {
  border-color: rgba(16, 185, 129, 0.5);
}

.custom-toast.success i {
  color: #10b981;
}

.custom-toast span {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}

@media (max-width: 768px) {
  .hub-title { font-size: 32px; }
  .quick-stats { gap: 24px; }
  .quick-stat .stat-value { font-size: 22px; }
  .bottom-actions { gap: 20px; flex-wrap: wrap; }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .hub-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2,
:global(html.light) .glow-3 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }
:global(html.light) .glow-3 { background: #0e7490; }

:global(html.light) .hub-header {
  background: rgba(255, 255, 255, 0.8);
  border-bottom-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .hub-title {
  color: #0c4a6e;
}

:global(html.light) .hub-subtitle {
  color: #64748b;
}

:global(html.light) .quick-stat .stat-value {
  color: #0891b2;
}

:global(html.light) .quick-stat .stat-label {
  color: #64748b;
}

:global(html.light) .btn-publish {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .section-header h2 {
  color: #0c4a6e;
}

:global(html.light) .section-header .view-all {
  color: #0891b2;
}

:global(html.light) .filter-tabs {
  background: rgba(8, 145, 178, 0.05);
}

:global(html.light) .filter-tab {
  color: #64748b;
}

:global(html.light) .filter-tab.active {
  background: #ffffff;
  color: #0891b2;
  box-shadow: 0 2px 8px rgba(8, 145, 178, 0.15);
}

:global(html.light) .job-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .job-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);
}

:global(html.light) .company-logo {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .company-info h3 {
  color: #0c4a6e;
}

:global(html.light) .company-name {
  color: #64748b;
}

:global(html.light) .job-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .job-tags .tag.urgent {
  background: rgba(234, 88, 12, 0.1);
  color: #ea580c;
}

:global(html.light) .job-meta span {
  color: #64748b;
}

:global(html.light) .job-salary {
  color: #0891b2;
}

:global(html.light) .job-actions .action-btn {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .job-actions .action-btn:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .job-actions .action-btn.saved {
  background: rgba(234, 179, 8, 0.12);
  color: #ca8a04;
}

:global(html.light) .job-actions .btn-apply {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .match-indicator {
  background: rgba(8, 145, 178, 0.06);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .match-label {
  color: #64748b;
}

:global(html.light) .match-score {
  color: #0891b2;
}

:global(html.light) .match-bar {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .nav-btn {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .nav-btn:hover:not(:disabled) {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .nav-btn:disabled {
  background: rgba(8, 145, 178, 0.03);
  color: #94a3b8;
}

:global(html.light) .page-indicator {
  color: #64748b;
}

:global(html.light) .stats-grid {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .stats-card {
  background: rgba(8, 145, 178, 0.03);
}

:global(html.light) .stats-card h4 {
  color: #64748b;
}

:global(html.light) .stats-card .stat-number {
  color: #0891b2;
}

:global(html.light) .bottom-actions {
  background: rgba(255, 255, 255, 0.9);
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .action-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .action-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .action-icon {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .action-title {
  color: #0c4a6e;
}

:global(html.light) .action-desc {
  color: #64748b;
}

:global(html.light) .modal-overlay {
  background: rgba(0, 0, 0, 0.3);
}

:global(html.light) .modal-content {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .modal-header h3 {
  color: #0c4a6e;
}

:global(html.light) .close-btn {
  color: #64748b;
}

:global(html.light) .close-btn:hover {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .form-group label {
  color: #0c4a6e;
}

:global(html.light) .form-group input,
:global(html.light) .form-group select,
:global(html.light) .form-group textarea {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .form-group input:focus,
:global(html.light) .form-group select:focus,
:global(html.light) .form-group textarea:focus {
  border-color: rgba(8, 145, 178, 0.4);
}

:global(html.light) .range-inputs input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .range-sep {
  color: #64748b;
}

:global(html.light) .tag-input .tags .tag {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .tag-input input {
  color: #0c4a6e;
}

:global(html.light) .btn-cancel {
  background: rgba(8, 145, 178, 0.08);
  color: #64748b;
}

:global(html.light) .btn-publish {
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

:global(html.light) .custom-toast {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.2);
  box-shadow: 0 10px 40px rgba(8, 145, 178, 0.15);
}

:global(html.light) .custom-toast span {
  color: #0c4a6e;
}
</style>
