<template>
  <div 
    class="profile-ai-assistant" 
    :class="{ 'is-active': isActive, 'is-dragging': isDragging }"
    :style="{ left: posX + 'px', bottom: posY + 'px' }"
  >
    <!-- 背景遮罩 -->
    <div v-if="isActive" class="backdrop" @click="close"></div>
    
    <!-- AI小球 -->
    <div 
      class="ai-avatar-wrapper" 
      @click="handleClick"
      @mousedown="startDrag"
      @mouseenter="onHover" 
      @mouseleave="onLeave"
    >
      <!-- 脉冲环 -->
      <div class="pulse-ring" v-if="!isActive && !isDragging"></div>
      <div class="pulse-ring delay" v-if="!isActive && !isDragging"></div>
      
      <!-- 圆形AI头像 -->
      <div class="ai-avatar" :class="{ thinking: isThinking, speaking: isSpeaking, happy: isHappy }">
        <div class="avatar-glow"></div>
        <div class="avatar-main">
          <div class="face">
            <div class="eyes">
              <div class="eye left" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
              <div class="eye right" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
            </div>
            <div class="mouth" :class="mouthState"></div>
          </div>
        </div>
        <div class="status-badge" :class="contextMode">
          <i :class="contextIcon"></i>
        </div>
      </div>
    </div>

    <!-- 浮动气泡 -->
    <transition name="bubble-pop">
      <div v-if="showIdleBubble && !isActive" class="idle-bubble" @click="toggleActive">
        <span class="bubble-text">{{ idleBubbleText }}</span>
        <div class="bubble-tail"></div>
      </div>
    </transition>

    <!-- 主交互面板 -->
    <transition name="panel-spring">
      <div v-if="isActive" class="main-panel">
        <div class="panel-header">
          <div class="header-title">
            <span class="title-icon">🤖</span>
            <span class="title-text">画像分析助手</span>
            <span class="context-tag" :class="contextMode">{{ contextLabel }}</span>
          </div>
          <button class="close-btn" @click="close"><i class="bi bi-x-lg"></i></button>
        </div>

        <!-- 对话区域 -->
        <div class="chat-zone" ref="chatZoneRef">
          <div v-for="(msg, idx) in chatHistory" :key="idx" class="chat-message" :class="msg.type">
            <span v-if="msg.type === 'ai'" class="msg-avatar">🤖</span>
            <div class="msg-content">
              <p class="msg-text" v-html="msg.text"></p>
              <span class="msg-time">{{ msg.time }}</span>
            </div>
          </div>
          <div v-if="isThinking" class="chat-message ai typing">
            <span class="msg-avatar">🤖</span>
            <div class="msg-content"><div class="typing-dots"><span></span><span></span><span></span></div></div>
          </div>
        </div>

        <!-- 快捷功能卡片 -->
        <div v-if="showQuickActions" class="quick-actions">
          <button 
            v-for="action in contextActions" 
            :key="action.id" 
            class="action-card" 
            :class="action.class"
            @click="handleAction(action)"
          >
            <span class="action-icon">{{ action.icon }}</span>
            <span class="action-label">{{ action.label }}</span>
          </button>
        </div>

        <!-- 分析结果展示 -->
        <div v-if="showAnalysisResult" class="analysis-result">
          <div class="result-header">
            <span class="result-title">{{ analysisTitle }}</span>
            <button class="back-btn" @click="backToMain"><i class="bi bi-arrow-left"></i></button>
          </div>
          <div class="result-content" v-html="analysisContent"></div>
          <div class="result-suggestions" v-if="suggestions.length">
            <div class="suggestions-title">💡 改进建议</div>
            <div v-for="(sug, i) in suggestions" :key="i" class="suggestion-item">
              <span class="sug-num">{{ i + 1 }}</span>
              <span class="sug-text">{{ sug }}</span>
            </div>
          </div>
        </div>

        <!-- 底部输入框 -->
        <div class="chat-input-bar">
          <input 
            v-model="userInput" 
            type="text" 
            :placeholder="inputPlaceholder"
            @keyup.enter="sendUserMessage" 
          />
          <button class="send-btn" @click="sendUserMessage" :disabled="!userInput.trim()">
            <i class="bi bi-send-fill"></i>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  // 当前上下文模式: job / personal / compare
  contextMode: { type: String, default: 'job' },
  // 上下文数据
  jobProfile: { type: Object, default: null },
  personalProfile: { type: Object, default: null },
  comparisonResult: { type: Object, default: null },
  // 技能列表
  skills: { type: Array, default: () => [] },
  // 能力数据
  abilities: { type: Array, default: () => [] }
})

const emit = defineEmits(['analyze', 'improve', 'compare', 'navigate', 'generateSuggestion'])

// 状态
const isActive = ref(false)
const isThinking = ref(false)
const isSpeaking = ref(false)
const isHappy = ref(false)
const eyeState = ref('normal')
const mouthState = ref('normal')

// 面板状态
const showQuickActions = ref(true)
const showAnalysisResult = ref(false)
const analysisTitle = ref('')
const analysisContent = ref('')
const suggestions = ref([])

// 闲聊气泡
const showIdleBubble = ref(false)
const idleBubbleText = ref('')
const idleBubbles = {
  job: [
    '这个岗位要求有点高哦~',
    '让我帮你分析一下岗位画像？',
    '想了解这个岗位的核心能力吗？',
    '点我看看岗位详细解读~',
    '我发现了一些关键技能要求！'
  ],
  personal: [
    '你的画像还可以优化哦~',
    '要不要看看竞争力分析？',
    '我来帮你找出提升方向！',
    '点我看能力成长建议~',
    '发现几个可以加强的地方！'
  ],
  compare: [
    '对比分析结果出来了！',
    '让我帮你分析差距~',
    '想知道如何缩小差距吗？',
    '点我看个性化提升计划！',
    '发现了几个匹配亮点！'
  ]
}

// 拖拽
const posX = ref(28)
const posY = ref(28)
const isDragging = ref(false)
const dragStart = { x: 0, y: 0, posX: 0, posY: 0 }
let dragMoved = false

// 对话
const chatHistory = ref([])
const userInput = ref('')
const chatZoneRef = ref(null)

// 上下文相关
const contextLabel = computed(() => {
  switch (props.contextMode) {
    case 'job': return '岗位画像'
    case 'personal': return '个人画像'
    case 'compare': return '画像对比'
    default: return '画像分析'
  }
})

const contextIcon = computed(() => {
  switch (props.contextMode) {
    case 'job': return 'bi bi-briefcase-fill'
    case 'personal': return 'bi bi-person-fill'
    case 'compare': return 'bi bi-arrow-left-right'
    default: return 'bi bi-bar-chart-fill'
  }
})

const inputPlaceholder = computed(() => {
  switch (props.contextMode) {
    case 'job': return '问我关于岗位要求、技能分析...'
    case 'personal': return '问我关于能力提升、画像优化...'
    case 'compare': return '问我关于差距分析、改进建议...'
    default: return '和我聊聊画像分析...'
  }
})

const contextActions = computed(() => {
  switch (props.contextMode) {
    case 'job':
      return [
        { id: 'explain-job', icon: '📊', label: '讲解岗位画像', class: 'primary' },
        { id: 'skill-analysis', icon: '🎯', label: '技能要求分析', class: 'cyan' },
        { id: 'salary-insight', icon: '💰', label: '薪资洞察', class: 'green' },
        { id: 'similar-jobs', icon: '🔗', label: '相似岗位', class: 'violet' }
      ]
    case 'personal':
      return [
        { id: 'explain-profile', icon: '👤', label: '解读个人画像', class: 'primary' },
        { id: 'strength-analysis', icon: '💪', label: '优势分析', class: 'green' },
        { id: 'weakness-improve', icon: '📈', label: '待提升项', class: 'orange' },
        { id: 'growth-plan', icon: '🚀', label: '成长建议', class: 'cyan' }
      ]
    case 'compare':
      return [
        { id: 'gap-analysis', icon: '📉', label: '差距分析', class: 'primary' },
        { id: 'match-highlight', icon: '✅', label: '匹配亮点', class: 'green' },
        { id: 'improve-priority', icon: '🎯', label: '优先提升', class: 'orange' },
        { id: 'action-plan', icon: '📋', label: '行动计划', class: 'violet' }
      ]
    default:
      return []
  }
})

// AI回复库
const aiResponses = {
  greetings: {
    job: '你好呀！我是画像分析助手~ 🎯\n\n当前我们正在看岗位画像，我可以帮你：\n• 详细解读岗位能力要求\n• 分析核心技能需求\n• 提供薪资参考建议\n\n点击下方卡片或直接问我吧！',
    personal: '嗨！欢迎来到个人画像分析~ 👤\n\n我可以帮你：\n• 解读你的能力画像\n• 分析你的竞争优势\n• 找出可提升的方向\n• 制定成长计划\n\n有什么想了解的？',
    compare: '准备好对比分析了！⚡\n\n我能帮你：\n• 分析个人与岗位的差距\n• 找出你的匹配亮点\n• 确定优先提升项\n• 生成个性化行动计划\n\n开始探索吧！'
  },
  thinking: ['让我分析一下...', '正在整理数据...', '思考中...', '马上就好~'],
  encouragement: ['加油！你的画像在逐步完善 💪', '继续保持，成长可见！✨', '每一步提升都有价值 🌟']
}

// 方法
function randomPick(arr) {
  return Array.isArray(arr) ? arr[Math.floor(Math.random() * arr.length)] : arr
}

function addAIMessage(text) {
  isSpeaking.value = true
  mouthState.value = 'speaking'
  chatHistory.value.push({
    type: 'ai',
    text,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })
  nextTick(() => scrollToBottom())
  setTimeout(() => {
    isSpeaking.value = false
    mouthState.value = 'normal'
  }, 500)
}

function addUserMessage(text) {
  chatHistory.value.push({
    type: 'user',
    text,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })
  nextTick(() => scrollToBottom())
}

function scrollToBottom() {
  if (chatZoneRef.value) {
    chatZoneRef.value.scrollTop = chatZoneRef.value.scrollHeight
  }
}

function toggleActive() {
  isActive.value = !isActive.value
  showIdleBubble.value = false
  
  if (isActive.value) {
    showHappy()
    chatHistory.value = []
    const greeting = aiResponses.greetings[props.contextMode] || aiResponses.greetings.job
    addAIMessage(greeting)
    showQuickActions.value = true
    showAnalysisResult.value = false
  }
}

function close() {
  isActive.value = false
  resetPanel()
}

function resetPanel() {
  showQuickActions.value = true
  showAnalysisResult.value = false
  suggestions.value = []
}

function backToMain() {
  showAnalysisResult.value = false
  showQuickActions.value = true
  addAIMessage('还有什么想了解的吗？点击卡片或直接问我~')
}

function onHover() {
  if (!isActive.value && !isDragging.value) {
    eyeState.value = 'happy'
    isHappy.value = true
    mouthState.value = 'smile'
  }
}

function onLeave() {
  if (!isActive.value) {
    eyeState.value = 'normal'
    isHappy.value = false
    mouthState.value = 'normal'
  }
}

function startDrag(e) {
  if (isActive.value) return
  dragMoved = false
  dragStart.x = e.clientX
  dragStart.y = e.clientY
  dragStart.posX = posX.value
  dragStart.posY = posY.value
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', endDrag)
}

function onDrag(e) {
  const dx = e.clientX - dragStart.x
  const dy = dragStart.y - e.clientY
  if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
    dragMoved = true
    isDragging.value = true
  }
  const newX = Math.max(10, Math.min(window.innerWidth - 100, dragStart.posX + dx))
  const newY = Math.max(10, Math.min(window.innerHeight - 100, dragStart.posY + dy))
  posX.value = newX
  posY.value = newY
}

function endDrag() {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  setTimeout(() => { isDragging.value = false }, 50)
}

function handleClick() {
  if (!dragMoved) toggleActive()
  dragMoved = false
}

function showHappy() {
  isHappy.value = true
  eyeState.value = 'happy'
  mouthState.value = 'smile'
  setTimeout(() => {
    isHappy.value = false
    eyeState.value = 'normal'
    mouthState.value = 'normal'
  }, 1200)
}

function showThinking() {
  isThinking.value = true
}

function hideThinking() {
  isThinking.value = false
}

// 处理快捷操作
function handleAction(action) {
  showQuickActions.value = false
  addAIMessage(randomPick(aiResponses.thinking))
  showThinking()

  setTimeout(() => {
    hideThinking()
    processAction(action.id)
  }, 800)
}

function processAction(actionId) {
  switch (actionId) {
    case 'explain-job':
      explainJobProfile()
      break
    case 'skill-analysis':
      analyzeSkillRequirements()
      break
    case 'salary-insight':
      showSalaryInsight()
      break
    case 'similar-jobs':
      findSimilarJobs()
      break
    case 'explain-profile':
      explainPersonalProfile()
      break
    case 'strength-analysis':
      analyzeStrengths()
      break
    case 'weakness-improve':
      analyzeWeaknesses()
      break
    case 'growth-plan':
      generateGrowthPlan()
      break
    case 'gap-analysis':
      analyzeGaps()
      break
    case 'match-highlight':
      showMatchHighlights()
      break
    case 'improve-priority':
      showImprovePriority()
      break
    case 'action-plan':
      generateActionPlan()
      break
    default:
      addAIMessage('这个功能正在开发中~')
  }
}

// 岗位画像相关
function explainJobProfile() {
  const job = props.jobProfile
  if (!job) {
    addAIMessage('暂无岗位画像数据，请先选择一个岗位~')
    showQuickActions.value = true
    return
  }

  analysisTitle.value = '📊 岗位画像解读'
  analysisContent.value = `
    <div class="profile-summary">
      <div class="summary-header">
        <strong>${job.position_name || '未知岗位'}</strong>
        <span class="category-tag">${job.category || '未分类'}</span>
      </div>
      <div class="summary-grid">
        <div class="grid-item">
          <span class="label">薪资范围</span>
          <span class="value highlight">${job.salary_range || '面议'}</span>
        </div>
        <div class="grid-item">
          <span class="label">学历要求</span>
          <span class="value">${job.education_req || '不限'}</span>
        </div>
        <div class="grid-item">
          <span class="label">经验要求</span>
          <span class="value">${job.experience_req || '不限'}</span>
        </div>
        <div class="grid-item">
          <span class="label">岗位层级</span>
          <span class="value">${job.level || '未知'}</span>
        </div>
      </div>
      <div class="ability-section">
        <div class="section-title">核心能力要求</div>
        <div class="ability-bars">
          ${generateAbilityBars(job)}
        </div>
      </div>
    </div>
  `
  suggestions.value = [
    '关注该岗位的核心技能要求，有针对性地学习',
    '对比薪资范围，评估个人期望是否合理',
    '查看经验要求，规划合适的发展路径'
  ]

  addAIMessage('这是该岗位的详细画像解读 👇')
  showAnalysisResult.value = true
  emit('analyze', { type: 'job-explain', data: job })
}

function generateAbilityBars(profile) {
  const abilities = [
    { key: 'innovation_ability', name: '创新能力', color: 'violet' },
    { key: 'learning_ability', name: '学习能力', color: 'blue' },
    { key: 'pressure_resistance', name: '抗压能力', color: 'green' },
    { key: 'communication_skill', name: '沟通能力', color: 'cyan' },
    { key: 'teamwork_ability', name: '团队协作', color: 'orange' }
  ]

  return abilities.map(ab => {
    const value = Number(profile?.[ab.key] || 0)
    return `
      <div class="ability-bar">
        <span class="ab-name">${ab.name}</span>
        <div class="ab-track">
          <div class="ab-fill ${ab.color}" style="width: ${value * 10}%"></div>
        </div>
        <span class="ab-value">${value.toFixed(1)}</span>
      </div>
    `
  }).join('')
}

function analyzeSkillRequirements() {
  const skills = props.jobProfile?.technical_skills || props.skills || []
  if (!skills.length) {
    addAIMessage('暂无技能数据，请确保已加载岗位画像~')
    showQuickActions.value = true
    return
  }

  analysisTitle.value = '🎯 技能要求分析'
  analysisContent.value = `
    <div class="skill-analysis">
      <div class="skill-cloud">
        ${skills.map((s, i) => `<span class="skill-tag ${i < 3 ? 'hot' : ''}">${s}</span>`).join('')}
      </div>
      <div class="skill-insight">
        <div class="insight-item">
          <i class="bi bi-fire"></i>
          <span>核心技能：${skills.slice(0, 3).join('、')}</span>
        </div>
        <div class="insight-item">
          <i class="bi bi-lightbulb"></i>
          <span>共需掌握 <strong>${skills.length}</strong> 项技能</span>
        </div>
      </div>
    </div>
  `
  suggestions.value = [
    `优先掌握核心技能：${skills[0] || '首要技能'}`,
    '建立技能学习路线图，循序渐进',
    '关注技能的实践应用，不只是理论学习'
  ]

  addAIMessage('这是该岗位的技能要求分析 👇')
  showAnalysisResult.value = true
}

function showSalaryInsight() {
  const job = props.jobProfile
  addAIMessage(`💰 薪资洞察\n\n该岗位薪资范围：<strong>${job?.salary_range || '面议'}</strong>\n\n影响薪资的关键因素：\n• 核心技能掌握程度\n• 项目经验丰富度\n• 行业背景匹配度\n• 团队管理能力\n\n建议做好技能和经验的积累，薪资水平会随之提升！`)
  showQuickActions.value = true
}

function findSimilarJobs() {
  addAIMessage('🔗 相似岗位推荐功能开发中...\n\n稍后会根据当前岗位的能力要求，为你推荐相似的职位选择！')
  showQuickActions.value = true
  emit('navigate', { target: 'similar-jobs' })
}

// 个人画像相关
function explainPersonalProfile() {
  const profile = props.personalProfile
  if (!profile) {
    addAIMessage('暂无个人画像数据，请先上传简历或填写信息~')
    showQuickActions.value = true
    return
  }

  analysisTitle.value = '👤 个人画像解读'
  analysisContent.value = `
    <div class="profile-summary">
      <div class="summary-header">
        <strong>${profile.name || '我的画像'}</strong>
        <span class="score-badge">竞争力 ${Number(profile.competitiveness_score || 0).toFixed(1)}</span>
      </div>
      <div class="summary-grid">
        <div class="grid-item">
          <span class="label">画像完整度</span>
          <span class="value highlight">${Number(profile.completeness_score || 0).toFixed(1)}%</span>
        </div>
        <div class="grid-item">
          <span class="label">技能数量</span>
          <span class="value">${(profile.technical_skills || []).length}</span>
        </div>
        <div class="grid-item">
          <span class="label">项目经历</span>
          <span class="value">${(profile.project_experience || []).length}</span>
        </div>
        <div class="grid-item">
          <span class="label">证书数量</span>
          <span class="value">${(profile.certificates || []).length}</span>
        </div>
      </div>
      <div class="ability-section">
        <div class="section-title">能力分布</div>
        <div class="ability-bars">
          ${generateAbilityBars(profile)}
        </div>
      </div>
    </div>
  `
  
  const completeness = Number(profile.completeness_score || 0)
  suggestions.value = completeness < 80 
    ? ['补充更多项目经历，提升画像完整度', '添加相关证书，增强专业认可', '完善技能标签，便于精准匹配']
    : ['保持画像更新，反映最新能力', '关注行业趋势，补充新兴技能', '定期回顾画像，调整发展方向']

  addAIMessage('这是你的个人画像详细解读 👇')
  showAnalysisResult.value = true
}

function analyzeStrengths() {
  const profile = props.personalProfile
  if (!profile) {
    addAIMessage('请先加载个人画像数据~')
    showQuickActions.value = true
    return
  }

  const abilities = [
    { key: 'innovation_ability', name: '创新能力' },
    { key: 'learning_ability', name: '学习能力' },
    { key: 'pressure_resistance', name: '抗压能力' },
    { key: 'communication_skill', name: '沟通能力' },
    { key: 'teamwork_ability', name: '团队协作' }
  ]

  const sorted = abilities
    .map(a => ({ ...a, value: Number(profile[a.key] || 0) }))
    .sort((a, b) => b.value - a.value)

  const top2 = sorted.slice(0, 2)
  
  addAIMessage(`💪 你的核心优势分析\n\n🥇 ${top2[0].name}：<strong>${top2[0].value.toFixed(1)}</strong> 分\n🥈 ${top2[1].name}：<strong>${top2[1].value.toFixed(1)}</strong> 分\n\n这些是你的竞争亮点！在求职时可以重点展示这些能力，给面试官留下深刻印象~`)
  showQuickActions.value = true
}

function analyzeWeaknesses() {
  const profile = props.personalProfile
  if (!profile) {
    addAIMessage('请先加载个人画像数据~')
    showQuickActions.value = true
    return
  }

  const abilities = [
    { key: 'innovation_ability', name: '创新能力' },
    { key: 'learning_ability', name: '学习能力' },
    { key: 'pressure_resistance', name: '抗压能力' },
    { key: 'communication_skill', name: '沟通能力' },
    { key: 'teamwork_ability', name: '团队协作' }
  ]

  const sorted = abilities
    .map(a => ({ ...a, value: Number(profile[a.key] || 0) }))
    .sort((a, b) => a.value - b.value)

  const bottom2 = sorted.slice(0, 2)
  
  analysisTitle.value = '📈 待提升能力分析'
  analysisContent.value = `
    <div class="weakness-analysis">
      <div class="weakness-items">
        ${bottom2.map((item, i) => `
          <div class="weakness-card">
            <span class="rank">${i + 1}</span>
            <div class="info">
              <span class="name">${item.name}</span>
              <span class="score ${item.value < 5 ? 'low' : 'medium'}">${item.value.toFixed(1)}</span>
            </div>
            <div class="progress">
              <div class="bar" style="width: ${item.value * 10}%"></div>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `
  suggestions.value = [
    `专注提升${bottom2[0].name}，可通过实践项目锻炼`,
    `${bottom2[1].name}可以通过系统学习和刻意练习改进`,
    '设定具体目标，定期检查进步情况'
  ]

  addAIMessage('以下是你可以重点提升的方向 👇')
  showAnalysisResult.value = true
}

function generateGrowthPlan() {
  addAIMessage(`🚀 成长计划建议\n\n基于你的画像分析，建议按以下步骤提升：\n\n<strong>短期（1-3个月）</strong>\n• 完善画像信息，提高完整度\n• 针对薄弱技能进行专项学习\n\n<strong>中期（3-6个月）</strong>\n• 参与实际项目，积累经验\n• 考取相关证书，增强背书\n\n<strong>长期（6-12个月）</strong>\n• 建立个人品牌和影响力\n• 持续迭代和优化能力结构`)
  showQuickActions.value = true
  emit('generateSuggestion', { type: 'growth-plan' })
}

// 对比分析相关
function analyzeGaps() {
  const result = props.comparisonResult
  if (!result) {
    addAIMessage('请先完成画像对比，获取差距数据~')
    showQuickActions.value = true
    return
  }

  const gaps = result.skill_gaps || []
  
  analysisTitle.value = '📉 差距分析报告'
  analysisContent.value = `
    <div class="gap-analysis">
      <div class="overall-score">
        <span class="score">${Number(result.overall_score || 0).toFixed(1)}</span>
        <span class="label">综合匹配度</span>
      </div>
      <div class="gap-details">
        <div class="detail-item">
          <span class="label">基础匹配</span>
          <span class="value">${Number(result.basic_score || 0).toFixed(1)}</span>
        </div>
        <div class="detail-item">
          <span class="label">技能匹配</span>
          <span class="value">${Number(result.skill_score || 0).toFixed(1)}</span>
        </div>
        <div class="detail-item">
          <span class="label">素养匹配</span>
          <span class="value">${Number(result.quality_score || 0).toFixed(1)}</span>
        </div>
      </div>
      ${gaps.length ? `
        <div class="skill-gaps">
          <div class="gaps-title">技能缺口</div>
          <div class="gaps-tags">
            ${gaps.map(g => `<span class="gap-tag">${g}</span>`).join('')}
          </div>
        </div>
      ` : ''}
    </div>
  `
  
  suggestions.value = result.recommendations || [
    '重点补充技能缺口中的核心技能',
    '提升基础匹配度，完善学历和经验',
    '针对性改进能力短板'
  ]

  addAIMessage('这是你与目标岗位的差距分析 👇')
  showAnalysisResult.value = true
}

function showMatchHighlights() {
  const result = props.comparisonResult
  if (!result) {
    addAIMessage('请先完成画像对比~')
    showQuickActions.value = true
    return
  }

  const matched = result.matched_skills || []
  const extra = result.extra_skills || []

  addAIMessage(`✅ 你的匹配亮点\n\n<strong>已匹配技能（${matched.length}项）</strong>\n${matched.length ? matched.map(s => `• ${s}`).join('\n') : '暂无匹配'}\n\n<strong>额外优势技能（${extra.length}项）</strong>\n${extra.length ? extra.map(s => `• ${s}`).join('\n') : '暂无'}`)
  showQuickActions.value = true
}

function showImprovePriority() {
  const result = props.comparisonResult
  if (!result) {
    addAIMessage('请先完成画像对比~')
    showQuickActions.value = true
    return
  }

  const gaps = result.skill_gaps || []
  const priority = gaps.slice(0, 3)

  addAIMessage(`🎯 优先提升项\n\n根据岗位要求和你当前的能力画像，建议优先提升以下技能：\n\n${priority.length ? priority.map((s, i) => `${i + 1}. <strong>${s}</strong>`).join('\n') : '暂无明确的优先项'}\n\n这些技能对于该岗位至关重要，提升后能显著提高匹配度！`)
  showQuickActions.value = true
  emit('improve', { skills: priority })
}

function generateActionPlan() {
  const result = props.comparisonResult
  addAIMessage(`📋 个性化行动计划\n\n基于对比分析结果，为你生成以下行动计划：\n\n<strong>第一步：技能提升</strong>\n• 选择1-2个核心缺口技能\n• 制定学习计划和时间表\n• 通过项目实践巩固学习\n\n<strong>第二步：经验积累</strong>\n• 寻找相关实习或项目机会\n• 参与开源项目或志愿活动\n• 建立作品集展示能力\n\n<strong>第三步：画像更新</strong>\n• 定期更新个人画像\n• 重新进行对比分析\n• 追踪匹配度变化\n\n需要我帮你详细规划某个步骤吗？`)
  showQuickActions.value = true
  emit('generateSuggestion', { type: 'action-plan', data: result })
}

// 用户自由输入
function sendUserMessage() {
  const text = userInput.value.trim()
  if (!text) return
  
  addUserMessage(text)
  userInput.value = ''
  showQuickActions.value = false
  showThinking()

  setTimeout(() => {
    hideThinking()
    processUserInput(text)
  }, 600)
}

function processUserInput(text) {
  const lower = text.toLowerCase()
  
  // 简单意图识别
  if (lower.includes('你好') || lower.includes('hi') || lower.includes('嗨')) {
    const greeting = aiResponses.greetings[props.contextMode]
    addAIMessage(greeting)
  } else if (lower.includes('薪资') || lower.includes('工资') || lower.includes('待遇')) {
    showSalaryInsight()
  } else if (lower.includes('技能') || lower.includes('能力')) {
    if (props.contextMode === 'job') analyzeSkillRequirements()
    else if (props.contextMode === 'personal') analyzeStrengths()
    else analyzeGaps()
  } else if (lower.includes('差距') || lower.includes('对比') || lower.includes('匹配')) {
    analyzeGaps()
  } else if (lower.includes('提升') || lower.includes('改进') || lower.includes('建议')) {
    if (props.contextMode === 'personal') generateGrowthPlan()
    else generateActionPlan()
  } else if (lower.includes('优势') || lower.includes('亮点')) {
    if (props.contextMode === 'compare') showMatchHighlights()
    else analyzeStrengths()
  } else {
    // 默认回复
    addAIMessage(`我理解你想了解"${text}"相关的内容~\n\n目前我可以帮你：${contextActions.value.map(a => a.label).join('、')}\n\n点击上方功能卡片，或换个方式问我吧！`)
  }
  
  showQuickActions.value = true
}

// 闲聊气泡定时器
let idleTimer = null
function startIdleBubble() {
  clearInterval(idleTimer)
  idleTimer = setInterval(() => {
    if (!isActive.value && Math.random() > 0.6) {
      const bubbles = idleBubbles[props.contextMode] || idleBubbles.job
      idleBubbleText.value = randomPick(bubbles)
      showIdleBubble.value = true
      setTimeout(() => { showIdleBubble.value = false }, 4000)
    }
  }, 8000)
}

// 监听上下文变化
watch(() => props.contextMode, () => {
  if (isActive.value) {
    chatHistory.value = []
    const greeting = aiResponses.greetings[props.contextMode]
    addAIMessage(greeting)
    showQuickActions.value = true
    showAnalysisResult.value = false
  }
})

onMounted(() => {
  startIdleBubble()
})

onUnmounted(() => {
  clearInterval(idleTimer)
})
</script>

<style scoped>
.profile-ai-assistant {
  position: fixed;
  z-index: 9999;
  user-select: none;
}

.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
}

/* AI小球 */
.ai-avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.pulse-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.4);
  animation: pulse 2s ease-out infinite;
}

.pulse-ring.delay {
  animation-delay: 1s;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.5); opacity: 0; }
}

.ai-avatar {
  width: 56px;
  height: 56px;
  position: relative;
  transition: transform 0.3s ease;
}

.ai-avatar:hover {
  transform: scale(1.1);
}

.ai-avatar.thinking {
  animation: bob 0.5s ease-in-out infinite;
}

@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.avatar-main {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
  position: relative;
  overflow: hidden;
}

.face {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.eyes {
  display: flex;
  gap: 10px;
}

.eye {
  width: 10px;
  height: 10px;
  background: white;
  border-radius: 50%;
  position: relative;
}

.eye.happy {
  height: 4px;
  border-radius: 4px 4px 0 0;
}

.pupil {
  width: 6px;
  height: 6px;
  background: #1e1b4b;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
}

.eye.happy .pupil {
  display: none;
}

.highlight {
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 5px;
}

.mouth {
  width: 12px;
  height: 6px;
  border: 2px solid white;
  border-top: none;
  border-radius: 0 0 12px 12px;
}

.mouth.smile {
  height: 8px;
}

.mouth.speaking {
  animation: speak 0.3s ease-in-out infinite;
}

@keyframes speak {
  0%, 100% { height: 6px; }
  50% { height: 10px; border-radius: 50%; }
}

.status-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
  border: 2px solid #0f0f23;
}

.status-badge.job { background: #06b6d4; }
.status-badge.personal { background: #8b5cf6; }
.status-badge.compare { background: #10b981; }

/* 浮动气泡 */
.idle-bubble {
  position: absolute;
  bottom: 70px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 16px;
  padding: 10px 16px;
  max-width: 200px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.bubble-text {
  color: #e2e8f0;
  font-size: 13px;
  line-height: 1.4;
}

.bubble-tail {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid #312e81;
}

.bubble-pop-enter-active { animation: bubblePop 0.3s ease-out; }
.bubble-pop-leave-active { animation: bubblePop 0.2s ease-in reverse; }

@keyframes bubblePop {
  0% { opacity: 0; transform: translateX(-50%) scale(0.8) translateY(10px); }
  100% { opacity: 1; transform: translateX(-50%) scale(1) translateY(0); }
}

/* 主面板 */
.main-panel {
  position: absolute;
  bottom: 70px;
  left: -10px;
  width: 380px;
  max-height: 520px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.panel-spring-enter-active { animation: panelSpring 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.panel-spring-leave-active { animation: panelSpring 0.3s ease-in reverse; }

@keyframes panelSpring {
  0% { opacity: 0; transform: scale(0.9) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: rgba(139, 92, 246, 0.1);
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 18px;
}

.title-text {
  font-weight: 600;
  color: #e2e8f0;
  font-size: 15px;
}

.context-tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.context-tag.job { background: rgba(6, 182, 212, 0.2); color: #06b6d4; }
.context-tag.personal { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }
.context-tag.compare { background: rgba(16, 185, 129, 0.2); color: #10b981; }

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #ef4444;
}

/* 对话区域 */
.chat-zone {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 120px;
  max-height: 200px;
}

.chat-message {
  display: flex;
  gap: 8px;
  max-width: 90%;
}

.chat-message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.msg-content {
  background: rgba(139, 92, 246, 0.1);
  border-radius: 12px;
  padding: 10px 14px;
  border: 1px solid rgba(139, 92, 246, 0.15);
}

.chat-message.user .msg-content {
  background: rgba(6, 182, 212, 0.15);
  border-color: rgba(6, 182, 212, 0.2);
}

.msg-text {
  color: #e2e8f0;
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
}

.msg-text :deep(strong) {
  color: #a78bfa;
  font-weight: 600;
}

.msg-time {
  display: block;
  font-size: 10px;
  color: #64748b;
  margin-top: 4px;
  text-align: right;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: #a78bfa;
  border-radius: 50%;
  animation: typing 1.2s ease-in-out infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* 快捷功能卡片 */
.quick-actions {
  padding: 12px 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 10px;
  border-radius: 12px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  background: rgba(139, 92, 246, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  border-color: rgba(139, 92, 246, 0.4);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.action-card.primary { border-color: rgba(139, 92, 246, 0.3); }
.action-card.cyan { border-color: rgba(6, 182, 212, 0.3); }
.action-card.green { border-color: rgba(16, 185, 129, 0.3); }
.action-card.orange { border-color: rgba(249, 115, 22, 0.3); }
.action-card.violet { border-color: rgba(167, 139, 250, 0.3); }

.action-icon {
  font-size: 22px;
}

.action-label {
  font-size: 12px;
  color: #cbd5e1;
  font-weight: 500;
}

/* 分析结果展示 */
.analysis-result {
  padding: 16px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
  max-height: 280px;
  overflow-y: auto;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.result-title {
  font-weight: 600;
  color: #e2e8f0;
  font-size: 14px;
}

.back-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.result-content {
  color: #cbd5e1;
  font-size: 13px;
}

/* 结果内容样式 */
.result-content :deep(.profile-summary) {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  padding: 14px;
}

.result-content :deep(.summary-header) {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.result-content :deep(.summary-header strong) {
  color: #e2e8f0;
  font-size: 15px;
}

.result-content :deep(.category-tag),
.result-content :deep(.score-badge) {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 8px;
  background: rgba(6, 182, 212, 0.2);
  color: #06b6d4;
}

.result-content :deep(.summary-grid) {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}

.result-content :deep(.grid-item) {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-content :deep(.grid-item .label) {
  font-size: 11px;
  color: #64748b;
}

.result-content :deep(.grid-item .value) {
  font-size: 14px;
  color: #e2e8f0;
  font-weight: 500;
}

.result-content :deep(.grid-item .value.highlight) {
  color: #a78bfa;
}

.result-content :deep(.ability-section) {
  margin-top: 12px;
}

.result-content :deep(.section-title) {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 10px;
}

.result-content :deep(.ability-bar) {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.result-content :deep(.ab-name) {
  width: 60px;
  font-size: 11px;
  color: #94a3b8;
}

.result-content :deep(.ab-track) {
  flex: 1;
  height: 6px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.result-content :deep(.ab-fill) {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.result-content :deep(.ab-fill.violet) { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.result-content :deep(.ab-fill.blue) { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.result-content :deep(.ab-fill.green) { background: linear-gradient(90deg, #10b981, #34d399); }
.result-content :deep(.ab-fill.cyan) { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
.result-content :deep(.ab-fill.orange) { background: linear-gradient(90deg, #f97316, #fb923c); }

.result-content :deep(.ab-value) {
  width: 28px;
  font-size: 12px;
  color: #a78bfa;
  text-align: right;
}

/* 技能分析 */
.result-content :deep(.skill-analysis) {
  padding: 10px;
}

.result-content :deep(.skill-cloud) {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.result-content :deep(.skill-tag) {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #cbd5e1;
}

.result-content :deep(.skill-tag.hot) {
  background: rgba(249, 115, 22, 0.15);
  border-color: rgba(249, 115, 22, 0.3);
  color: #fb923c;
}

.result-content :deep(.skill-insight) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-content :deep(.insight-item) {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.result-content :deep(.insight-item i) {
  color: #f97316;
}

/* 差距分析 */
.result-content :deep(.gap-analysis) {
  text-align: center;
}

.result-content :deep(.overall-score) {
  margin-bottom: 16px;
}

.result-content :deep(.overall-score .score) {
  font-size: 40px;
  font-weight: 700;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.result-content :deep(.overall-score .label) {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.result-content :deep(.gap-details) {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 16px;
}

.result-content :deep(.detail-item) {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-content :deep(.detail-item .label) {
  font-size: 11px;
  color: #64748b;
}

.result-content :deep(.detail-item .value) {
  font-size: 18px;
  font-weight: 600;
  color: #a78bfa;
}

.result-content :deep(.skill-gaps) {
  text-align: left;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.result-content :deep(.gaps-title) {
  font-size: 12px;
  color: #ef4444;
  margin-bottom: 8px;
}

.result-content :deep(.gaps-tags) {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.result-content :deep(.gap-tag) {
  padding: 3px 8px;
  border-radius: 8px;
  font-size: 11px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
}

/* 弱项分析 */
.result-content :deep(.weakness-analysis) {
  padding: 10px;
}

.result-content :deep(.weakness-card) {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.15);
  border-radius: 10px;
  margin-bottom: 10px;
}

.result-content :deep(.weakness-card .rank) {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.result-content :deep(.weakness-card .info) {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-content :deep(.weakness-card .name) {
  font-size: 13px;
  color: #e2e8f0;
}

.result-content :deep(.weakness-card .score) {
  font-size: 14px;
  font-weight: 600;
}

.result-content :deep(.weakness-card .score.low) { color: #ef4444; }
.result-content :deep(.weakness-card .score.medium) { color: #f59e0b; }

.result-content :deep(.weakness-card .progress) {
  width: 60px;
  height: 4px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.result-content :deep(.weakness-card .bar) {
  height: 100%;
  background: linear-gradient(90deg, #ef4444, #f87171);
  border-radius: 2px;
}

/* 建议区域 */
.result-suggestions {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.suggestions-title {
  font-size: 13px;
  color: #f59e0b;
  margin-bottom: 10px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
  padding: 8px 10px;
  background: rgba(245, 158, 11, 0.05);
  border-radius: 8px;
}

.sug-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.sug-text {
  font-size: 12px;
  color: #cbd5e1;
  line-height: 1.4;
}

/* 输入框 */
.chat-input-bar {
  display: flex;
  gap: 10px;
  padding: 14px 16px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
  background: rgba(139, 92, 246, 0.03);
}

.chat-input-bar input {
  flex: 1;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  padding: 10px 14px;
  color: #e2e8f0;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}

.chat-input-bar input::placeholder {
  color: #64748b;
}

.chat-input-bar input:focus {
  border-color: rgba(139, 92, 246, 0.5);
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .backdrop {
  background: rgba(0, 0, 0, 0.15);
}

:global(html.light) .pupil {
  background: #0c4a6e;
}

:global(html.light) .status-badge {
  border-color: #ffffff;
}

:global(html.light) .idle-bubble {
  background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
  border-color: rgba(8, 145, 178, 0.3);
  box-shadow: 0 4px 20px rgba(8, 145, 178, 0.15);
}

:global(html.light) .bubble-text {
  color: #0c4a6e;
}

:global(html.light) .bubble-tail {
  border-top-color: #f0f9ff;
}

:global(html.light) .main-panel {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border-color: rgba(8, 145, 178, 0.2);
  box-shadow: 0 10px 40px rgba(8, 145, 178, 0.15);
}

:global(html.light) .panel-header {
  background: rgba(8, 145, 178, 0.08);
  border-bottom-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .title-text {
  color: #0c4a6e;
}

:global(html.light) .context-tag.job {
  background: rgba(6, 182, 212, 0.15);
  color: #0891b2;
}

:global(html.light) .context-tag.personal {
  background: rgba(8, 145, 178, 0.15);
  color: #0891b2;
}

:global(html.light) .context-tag.compare {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

:global(html.light) .close-btn {
  color: #64748b;
}

:global(html.light) .close-btn:hover {
  color: #dc2626;
}

:global(html.light) .msg-avatar {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .msg-content {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .chat-message.user .msg-content {
  background: rgba(6, 182, 212, 0.12);
  border-color: rgba(6, 182, 212, 0.2);
}

:global(html.light) .msg-text {
  color: #1e293b;
}

:global(html.light) .msg-text :deep(strong) {
  color: #0891b2;
}

:global(html.light) .msg-time {
  color: #64748b;
}

:global(html.light) .typing-dots span {
  background: #0891b2;
}

:global(html.light) .quick-actions {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .action-card {
  border-color: rgba(8, 145, 178, 0.2);
  background: rgba(8, 145, 178, 0.03);
}

:global(html.light) .action-card:hover {
  border-color: rgba(8, 145, 178, 0.4);
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.15);
}

:global(html.light) .action-label {
  color: #475569;
}

:global(html.light) .analysis-result {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .result-title {
  color: #0c4a6e;
}

:global(html.light) .back-btn {
  color: #64748b;
}

:global(html.light) .back-btn:hover {
  background: rgba(8, 145, 178, 0.15);
  color: #0891b2;
}

:global(html.light) .result-content {
  color: #475569;
}

:global(html.light) .result-content :deep(.profile-summary) {
  background: rgba(8, 145, 178, 0.04);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .result-content :deep(.summary-header strong) {
  color: #0c4a6e;
}

:global(html.light) .result-content :deep(.category-tag),
:global(html.light) .result-content :deep(.score-badge) {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .result-content :deep(.grid-item .label) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.grid-item .value) {
  color: #0c4a6e;
}

:global(html.light) .result-content :deep(.grid-item .value.highlight) {
  color: #0891b2;
}

:global(html.light) .result-content :deep(.section-title) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.ab-name) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.ab-track) {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .result-content :deep(.ab-value) {
  color: #0891b2;
}

:global(html.light) .result-content :deep(.skill-tag) {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.2);
  color: #475569;
}

:global(html.light) .result-content :deep(.skill-tag.hot) {
  background: rgba(234, 88, 12, 0.1);
  border-color: rgba(234, 88, 12, 0.25);
  color: #ea580c;
}

:global(html.light) .result-content :deep(.insight-item) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.insight-item i) {
  color: #ea580c;
}

:global(html.light) .result-content :deep(.overall-score .label) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.detail-item .label) {
  color: #64748b;
}

:global(html.light) .result-content :deep(.detail-item .value) {
  color: #0891b2;
}

:global(html.light) .result-content :deep(.skill-gaps) {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .result-content :deep(.gaps-title) {
  color: #dc2626;
}

:global(html.light) .result-content :deep(.gap-tag) {
  background: rgba(220, 38, 38, 0.08);
  border-color: rgba(220, 38, 38, 0.2);
  color: #dc2626;
}

:global(html.light) .result-content :deep(.weakness-card) {
  background: rgba(220, 38, 38, 0.04);
  border-color: rgba(220, 38, 38, 0.12);
}

:global(html.light) .result-content :deep(.weakness-card .rank) {
  background: rgba(220, 38, 38, 0.15);
  color: #dc2626;
}

:global(html.light) .result-content :deep(.weakness-card .name) {
  color: #0c4a6e;
}

:global(html.light) .result-content :deep(.weakness-card .progress) {
  background: rgba(220, 38, 38, 0.08);
}

:global(html.light) .result-suggestions {
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .suggestions-title {
  color: #d97706;
}

:global(html.light) .suggestion-item {
  background: rgba(217, 119, 6, 0.06);
}

:global(html.light) .sug-num {
  background: rgba(217, 119, 6, 0.15);
  color: #d97706;
}

:global(html.light) .sug-text {
  color: #475569;
}

:global(html.light) .chat-input-bar {
  border-top-color: rgba(8, 145, 178, 0.1);
  background: rgba(8, 145, 178, 0.02);
}

:global(html.light) .chat-input-bar input {
  background: rgba(8, 145, 178, 0.06);
  border-color: rgba(8, 145, 178, 0.2);
  color: #0c4a6e;
}

:global(html.light) .chat-input-bar input::placeholder {
  color: #64748b;
}

:global(html.light) .chat-input-bar input:focus {
  border-color: rgba(8, 145, 178, 0.5);
}

:global(html.light) .send-btn {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .send-btn:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(8, 145, 178, 0.35);
}
</style>
