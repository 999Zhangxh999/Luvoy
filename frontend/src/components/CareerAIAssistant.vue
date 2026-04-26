<template>
  <div 
    class="ai-companion" 
    :class="{ 'is-active': isActive, 'is-dragging': isDragging }"
    :style="{ left: posX + 'px', bottom: posY + 'px' }"
  >
    <!-- 背景遮罩 (点击关闭) -->
    <div v-if="isActive" class="backdrop" @click="close"></div>
    
    <!-- 主角色 -->
    <div 
      class="companion-wrapper" 
      @click="handleClick"
      @mousedown="startDrag"
      @mouseenter="onHover" 
      @mouseleave="onLeave"
    >
      <!-- 脉冲环 -->
      <div class="pulse-ring" v-if="!isActive && !isDragging"></div>
      <div class="pulse-ring delay" v-if="!isActive && !isDragging"></div>
      
      <!-- 可爱的圆形机器人 -->
      <div class="robot-avatar" :class="{ thinking: isThinking, speaking: isSpeaking, happy: isHappy, wave: isWaving }">
        <div class="avatar-glow"></div>
        <div class="avatar-main">
          <div class="antenna-wrap">
            <div class="antenna-stem"></div>
            <div class="antenna-tip" :class="{ active: isThinking }"></div>
          </div>
          <div class="face">
            <div class="eyes">
              <div class="eye left" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
              <div class="eye right" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
            </div>
            <div class="mouth" :class="mouthState"></div>
            <div class="cheek left"></div>
            <div class="cheek right"></div>
          </div>
        </div>
        <div class="status-indicator" :class="statusType">
          <span class="status-text">{{ statusText }}</span>
        </div>
      </div>
    </div>

    <!-- 浮动对话气泡 (闲聊) -->
    <transition name="bubble-pop">
      <div v-if="showIdleBubble && !isActive" class="idle-bubble" @click="toggleActive">
        <span class="bubble-text">{{ idleBubbleText }}</span>
        <div class="bubble-tail"></div>
      </div>
    </transition>

    <!-- 主交互面板 -->
    <transition name="panel-spring">
      <div v-if="isActive" class="main-panel" :class="panelMode">
        <div class="panel-header">
          <div class="header-title">
            <span class="title-icon">{{ panelIcon }}</span>
            <span class="title-text">{{ panelTitle }}</span>
          </div>
          <button class="close-btn" @click="close"><i class="bi bi-x-lg"></i></button>
        </div>

        <!-- 对话区域 -->
        <div class="chat-zone" ref="chatZoneRef">
          <div v-for="(msg, idx) in chatHistory" :key="idx" class="chat-message" :class="msg.type">
            <span v-if="msg.type === 'ai'" class="msg-avatar">🤖</span>
            <div class="msg-content">
              <p class="msg-text">{{ msg.text }}</p>
              <span class="msg-time">{{ msg.time }}</span>
            </div>
          </div>
          <div v-if="isThinking" class="chat-message ai typing">
            <span class="msg-avatar">🤖</span>
            <div class="msg-content"><div class="typing-dots"><span></span><span></span><span></span></div></div>
          </div>
        </div>

        <!-- 快捷回复条 -->
        <div v-if="quickReplies.length && !showSearch && !showResults && !showQuiz" class="quick-replies">
          <button v-for="reply in quickReplies" :key="reply.id" class="quick-reply-btn" @click="handleQuickReply(reply)">
            <span class="reply-icon">{{ reply.icon }}</span>
            <span class="reply-text">{{ reply.text }}</span>
          </button>
        </div>

        <!-- 功能网格 -->
        <div v-if="showMainMenu" class="action-grid">
          <button v-for="action in actions" :key="action.id" class="action-card" :class="action.class" @click="doAction(action)">
            <span class="action-icon">{{ action.icon }}</span>
            <span class="action-label">{{ action.label }}</span>
            <span v-if="action.badge" class="action-badge">{{ action.badge }}</span>
          </button>
        </div>

        <!-- 搜索模式 -->
        <div v-if="showSearch" class="search-section">
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input ref="searchInputRef" v-model="searchQuery" type="text" placeholder="输入职业、技能、行业..." @keyup.enter="doSearch" />
            <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''"><i class="bi bi-x"></i></button>
          </div>
          <div class="quick-tags">
            <button v-for="tag in quickTags" :key="tag" class="quick-tag" @click="searchQuery = tag; doSearch()">{{ tag }}</button>
          </div>
          <div class="search-actions">
            <button class="btn-secondary" @click="cancelSearch">取消</button>
            <button class="btn-primary" @click="doSearch" :disabled="!searchQuery.trim()"><i class="bi bi-search"></i> 搜索</button>
          </div>
        </div>

        <!-- 职业测验 -->
        <div v-if="showQuiz" class="quiz-section">
          <div class="quiz-progress">
            <div class="progress-bar" :style="{ width: quizProgress + '%' }"></div>
            <span class="progress-text">{{ quizCurrentIndex + 1 }} / {{ quizQuestions.length }}</span>
          </div>
          <div class="quiz-question">
            <p class="question-text">{{ currentQuizQuestion.text }}</p>
          </div>
          <div class="quiz-options">
            <button v-for="opt in currentQuizQuestion.options" :key="opt.value" class="quiz-option" @click="answerQuiz(opt)">
              <span class="opt-icon">{{ opt.icon }}</span>
              <span class="opt-text">{{ opt.text }}</span>
            </button>
          </div>
        </div>

        <!-- 结果模式 -->
        <div v-if="showResults" class="results-section">
          <div class="results-header">
            <span class="results-title">{{ resultsTitle }}</span>
            <span class="results-count">{{ results.length }} 个结果</span>
          </div>
          <div class="results-list">
            <button v-for="item in results" :key="item.id" class="result-card" @click="selectResult(item)">
              <span class="result-dot" :style="{ '--color': item.color }"></span>
              <div class="result-info">
                <span class="result-name">{{ item.name }}</span>
                <span class="result-meta">{{ item.category }} · {{ item.salary || '薪资面议' }}</span>
              </div>
              <i class="bi bi-arrow-right-circle"></i>
            </button>
          </div>
          <button class="back-btn" @click="backToMenu"><i class="bi bi-arrow-left"></i> 返回</button>
        </div>

        <!-- 底部输入框 -->
        <div v-if="showChatInput" class="chat-input-bar">
          <input v-model="userInput" type="text" placeholder="和小智聊天..." @keyup.enter="sendUserMessage" />
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
  careers: { type: Array, default: () => [] },
  contextCareer: { type: Object, default: null }
})

const emit = defineEmits(['search', 'highlight', 'focusCareer', 'showPaths'])

// 状态
const isActive = ref(false)
const isThinking = ref(false)
const isSpeaking = ref(false)
const isHappy = ref(false)
const isWaving = ref(false)
const eyeState = ref('normal')
const mouthState = ref('normal')
const statusType = ref('online')

// 闲聊气泡
const showIdleBubble = ref(false)
const idleBubbleText = ref('')
const idleBubbles = [
  // 好奇诱导 + 工作话题
  '诶，你知道现在最火的岗位是？',
  '猜猜哪个职业薪资最高？💰',
  '想知道适合你的职业方向吗？',
  '我发现了一些高薪机会...',
  '有个职业测验想给你看~',
  
  // 职业建议引导
  '感觉你很适合产品经理呢',
  '技术岗位最近招人好多！',
  '要不要一起看看数据分析？',
  '听说前端开发很香啊~',
  'AI工程师了解一下？🤖',
  
  // 关心 + 工作引导
  '工作顺利吗？需要换换环境？',
  '想升职加薪？一起聊聊！',
  '职业规划做好了吗？',
  '帮你分析一下职业前景？',
  '来看看有什么好机会~',
  
  // 俏皮 + 工作关联
  '找工作的事，找我就对了！',
  '点我看看热门职位～',
  '在想工作的事？我来帮忙！',
  '新的职业机会在等你哦~',
  '职业探索，从点我开始！✨'
]

// 拖拽相关
const posX = ref(28)
const posY = ref(28)
const isDragging = ref(false)
const dragStart = { x: 0, y: 0, posX: 0, posY: 0 }
let dragMoved = false

// 面板
const panelIcon = ref('🤖')
const panelTitle = ref('小智来啦')
const panelMode = ref('chat')
const showMainMenu = ref(true)
const showSearch = ref(false)
const showResults = ref(false)
const showQuiz = ref(false)
const showChatInput = ref(true)
const searchQuery = ref('')
const searchInputRef = ref(null)
const chatZoneRef = ref(null)
const results = ref([])
const resultsTitle = ref('')
const userInput = ref('')

// 快捷回复
const quickReplies = ref([])
const defaultQuickReplies = [
  { id: 'hi', icon: '👋', text: '你好啊' },
  { id: 'help', icon: '🆘', text: '帮帮我' },
  { id: 'tips', icon: '💡', text: '给点建议' }
]

// 对话历史
const chatHistory = ref([])

// 测验
const quizCurrentIndex = ref(0)
const quizAnswers = ref([])
const quizQuestions = [
  {
    text: '你更喜欢哪种工作环境？',
    options: [
      { icon: '💻', text: '安静独处，专注思考', value: 'introvert' },
      { icon: '👥', text: '团队协作，热闹氛围', value: 'extrovert' },
      { icon: '🏠', text: '灵活远程，自由自在', value: 'flexible' }
    ]
  },
  {
    text: '下面哪个最吸引你？',
    options: [
      { icon: '🎨', text: '创意设计', value: 'creative' },
      { icon: '📊', text: '数据分析', value: 'analytical' },
      { icon: '🤝', text: '沟通交流', value: 'social' },
      { icon: '🔧', text: '动手实践', value: 'practical' }
    ]
  },
  {
    text: '对于薪资和工作平衡，你更看重？',
    options: [
      { icon: '💰', text: '高薪最重要', value: 'money' },
      { icon: '⚖️', text: '平衡最重要', value: 'balance' },
      { icon: '🚀', text: '成长最重要', value: 'growth' }
    ]
  },
  {
    text: '你对技术的态度是？',
    options: [
      { icon: '🤖', text: '超级热爱，想天天接触', value: 'tech-love' },
      { icon: '🙂', text: '工具而已，够用就行', value: 'tech-neutral' },
      { icon: '😅', text: '有点头疼，能少用就少用', value: 'tech-avoid' }
    ]
  }
]
const currentQuizQuestion = computed(() => quizQuestions[quizCurrentIndex.value])
const quizProgress = computed(() => ((quizCurrentIndex.value + 1) / quizQuestions.length) * 100)

// 状态文字
const statusText = computed(() => {
  if (isThinking.value) return '思考中...'
  if (isSpeaking.value) return '说话中'
  return '在线'
})

// 快捷标签
const quickTags = ['产品经理', '前端开发', '数据分析', 'AI工程师', 'UI设计']

// 操作列表
const actions = ref([
  { id: 'search', icon: '🔍', label: '找职业', class: 'primary' },
  { id: 'hot', icon: '🔥', label: '热门推荐', class: 'hot' },
  { id: 'quiz', icon: '📝', label: '职业测验', class: 'quiz', badge: 'New' },
  { id: 'salary', icon: '💰', label: '高薪榜', class: 'salary' },
  { id: 'skills', icon: '🧠', label: '技能分析', class: 'skills' },
  { id: 'random', icon: '🎲', label: '随机探索', class: 'random' }
])

// 时间问候
function getTimeGreeting() {
  const hour = new Date().getHours()
  if (hour < 6) return { greeting: '夜深了还在研究职业？', emoji: '🌙', tip: '注意休息哦~' }
  if (hour < 9) return { greeting: '早上好呀！', emoji: '🌅', tip: '开启元气满满的一天！' }
  if (hour < 12) return { greeting: '上午好！', emoji: '☀️', tip: '今天想探索什么职业？' }
  if (hour < 14) return { greeting: '中午好！', emoji: '🍱', tip: '吃饭了吗？边吃边聊~' }
  if (hour < 18) return { greeting: '下午好！', emoji: '🌤️', tip: '下午茶时间，聊聊职业规划？' }
  if (hour < 22) return { greeting: '晚上好！', emoji: '🌆', tip: '一起看看有什么好机会~' }
  return { greeting: '夜猫子你好！', emoji: '🦉', tip: '深夜思考人生呢？' }
}

// AI回复库
const aiResponses = {
  greetings: [
    '你好呀！今天我们聊点什么？😊',
    '嗨嗨嗨！等你好久啦~',
    '终于来找我啦！有什么可以帮你的？',
    '你好你好！今天想探索什么职业呢？'
  ],
  help: [
    '没问题！我可以帮你：\n🔍 搜索感兴趣的职业\n📝 做职业性格测验\n🔥 看热门职位\n💰 查高薪岗位\n想试试哪个？',
    '当然可以帮你！说说你想了解什么，职业方向、薪资、技能要求都可以问我~',
    '来来来，告诉我你的困惑，我来帮你分析！'
  ],
  tips: [
    '💡 建议：先了解自己的兴趣和优势，再匹配适合的职业方向~',
    '💡 小技巧：可以先做个职业测验，帮你发现潜在的适合方向！',
    '💡 友情提示：不要只看薪资，工作环境和成长空间也很重要哦~',
    '💡 经验之谈：多了解几个方向，可能会发现意想不到的兴趣点！'
  ],
  thinking: [
    '让我想想...',
    '嗯，这个问题有意思...',
    '容我思考一下...',
    '好的，分析中...'
  ],
  found: [
    '找到啦！看看这些：',
    '哇，发现了好多相关的！',
    '来来来，这些你可能感兴趣：',
    '搜到啦！快看看~'
  ],
  notFound: [
    '哎呀，没找到相关的...换个关键词试试？',
    '这个比较冷门呢，要不试试其他词？',
    '暂时没搜到，换个方向看看？'
  ],
  encouragement: [
    '加油！找到理想的职业只是时间问题 💪',
    '相信自己，你一定能找到适合的方向！✨',
    '每一次探索都是成长，继续加油！🌟'
  ],
  farewell: [
    '好的，有问题随时找我哦！👋',
    '拜拜~下次再聊！',
    '去吧去吧，需要我的时候点我~'
  ],
  idle: [
    '还有什么想问的吗？',
    '试试其他功能？',
    '有什么我能帮到的？',
    '想再探索其他职业吗？'
  ],
  quiz: {
    start: '太好了！来做个小测验，帮你发现适合的职业方向~\n准备好了吗？',
    progress: ['不错不错！', '继续继续~', '快完成啦！', '最后一题！']
  }
}

function randomPick(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

// 添加AI消息
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

// 添加用户消息
function addUserMessage(text) {
  chatHistory.value.push({
    type: 'user',
    text,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })
  nextTick(() => scrollToBottom())
}

// 滚动到底部
function scrollToBottom() {
  if (chatZoneRef.value) {
    chatZoneRef.value.scrollTop = chatZoneRef.value.scrollHeight
  }
}

// 切换激活
function toggleActive() {
  isActive.value = !isActive.value
  showIdleBubble.value = false
  
  if (isActive.value) {
    showWave()
    const { greeting, emoji, tip } = getTimeGreeting()
    chatHistory.value = []
    addAIMessage(`${emoji} ${greeting}${tip}`)
    quickReplies.value = defaultQuickReplies
    showMainMenu.value = true
  }
}

// 关闭
function close() {
  isActive.value = false
  resetPanel()
}

// 重置面板
function resetPanel() {
  showSearch.value = false
  showResults.value = false
  showQuiz.value = false
  showMainMenu.value = true
  showChatInput.value = true
  searchQuery.value = ''
  quizCurrentIndex.value = 0
  quizAnswers.value = []
  emit('highlight', [])
}

// 返回菜单
function backToMenu() {
  showSearch.value = false
  showResults.value = false
  showQuiz.value = false
  showMainMenu.value = true
  emit('highlight', [])
  addAIMessage(randomPick(aiResponses.idle))
  quickReplies.value = defaultQuickReplies
}

// 鼠标交互
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

// 拖拽功能
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
  const dy = dragStart.y - e.clientY // 反转y因为bottom是从下往上
  
  if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
    dragMoved = true
    isDragging.value = true
  }
  
  // 计算新位置，限制在视口内
  const newX = Math.max(10, Math.min(window.innerWidth - 100, dragStart.posX + dx))
  const newY = Math.max(10, Math.min(window.innerHeight - 100, dragStart.posY + dy))
  
  posX.value = newX
  posY.value = newY
}

function endDrag() {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  
  setTimeout(() => {
    isDragging.value = false
  }, 50)
}

function handleClick() {
  // 如果是拖拽操作就不触发点击
  if (!dragMoved) {
    toggleActive()
  }
  dragMoved = false
}

// 表情动作
function showWave() {
  isWaving.value = true
  isHappy.value = true
  eyeState.value = 'happy'
  mouthState.value = 'smile'
  setTimeout(() => {
    isWaving.value = false
    isHappy.value = false
    eyeState.value = 'normal'
    mouthState.value = 'normal'
  }, 1500)
}

function showThinking() {
  isThinking.value = true
  statusType.value = 'thinking'
}

function hideThinking() {
  isThinking.value = false
  statusType.value = 'online'
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

// 用户输入消息
function sendUserMessage() {
  const text = userInput.value.trim()
  if (!text) return
  
  addUserMessage(text)
  userInput.value = ''
  quickReplies.value = []
  
  // 简单的意图识别
  showThinking()
  setTimeout(() => {
    hideThinking()
    
    if (text.includes('你好') || text.includes('hi') || text.includes('嗨')) {
      addAIMessage(randomPick(aiResponses.greetings))
    } else if (text.includes('帮') || text.includes('怎么') || text.includes('如何')) {
      addAIMessage(randomPick(aiResponses.help))
    } else if (text.includes('建议') || text.includes('推荐')) {
      addAIMessage(randomPick(aiResponses.tips))
    } else if (text.includes('测验') || text.includes('测试')) {
      addAIMessage(aiResponses.quiz.start)
      setTimeout(() => startQuiz(), 800)
    } else if (text.includes('热门') || text.includes('火')) {
      findHotCareers()
    } else if (text.includes('薪资') || text.includes('工资') || text.includes('钱')) {
      findHighSalary()
    } else if (text.includes('再见') || text.includes('拜拜') || text.includes('bye')) {
      addAIMessage(randomPick(aiResponses.farewell))
    } else {
      // 尝试搜索
      searchQuery.value = text
      addAIMessage(`让我帮你找找"${text}"相关的职业...`)
      setTimeout(() => doSearch(true), 500)
    }
    
    setTimeout(() => {
      if (!showSearch.value && !showResults.value && !showQuiz.value) {
        quickReplies.value = [
          { id: 'more', icon: '🔍', text: '继续探索' },
          { id: 'done', icon: '👋', text: '就这样吧' }
        ]
      }
    }, 1000)
  }, 800)
}

// 执行操作
function doAction(action) {
  quickReplies.value = []
  
  switch (action.id) {
    case 'search':
      showMainMenu.value = false
      showSearch.value = true
      addAIMessage('告诉我你想找什么类型的工作~可以输入职业名、技能或行业哦！')
      nextTick(() => searchInputRef.value?.focus())
      break
    case 'hot':
      findHotCareers()
      break
    case 'quiz':
      addAIMessage(aiResponses.quiz.start)
      setTimeout(() => startQuiz(), 800)
      break
    case 'salary':
      findHighSalary()
      break
    case 'skills':
      analyzeSkills()
      break
    case 'random':
      randomExplore()
      break
  }
}

// 搜索
function doSearch(silent = false) {
  if (!searchQuery.value.trim()) return
  
  if (!silent) {
    addAIMessage(randomPick(aiResponses.thinking))
  }
  showThinking()
  
  setTimeout(() => {
    const q = searchQuery.value.toLowerCase()
    const found = props.careers.filter(c =>
      c.name?.toLowerCase().includes(q) ||
      c.category?.toLowerCase().includes(q) ||
      c.skills?.some(s => s.toLowerCase().includes(q)) ||
      c.industry?.toLowerCase().includes(q)
    )
    
    hideThinking()
    
    if (found.length > 0) {
      showHappy()
      addAIMessage(`${randomPick(aiResponses.found)}找到了 ${found.length} 个相关职位！`)
      results.value = found.slice(0, 10)
      resultsTitle.value = `「${searchQuery.value}」的搜索结果`
      showSearch.value = false
      showMainMenu.value = false
      showResults.value = true
      emit('highlight', found.map(c => c.id))
    } else {
      addAIMessage(randomPick(aiResponses.notFound))
    }
  }, 600)
}

function cancelSearch() {
  showSearch.value = false
  showMainMenu.value = true
  searchQuery.value = ''
  addAIMessage(randomPick(aiResponses.idle))
}

// 热门职位
function findHotCareers() {
  addAIMessage('让我看看最近有什么热门职位... 🔥')
  showThinking()
  showMainMenu.value = false
  
  setTimeout(() => {
    hideThinking()
    const hot = props.careers.filter(c => c.isHot)
    if (hot.length > 0) {
      showHappy()
      addAIMessage(`哇！发现 ${hot.length} 个超火的职位！快来看看~`)
      results.value = hot
      resultsTitle.value = '🔥 热门职位'
      showResults.value = true
      emit('highlight', hot.map(c => c.id))
    } else {
      const recommended = props.careers.slice(0, 6)
      addAIMessage('热门职位暂时没有标记，但我给你推荐这些~')
      results.value = recommended
      resultsTitle.value = '💡 推荐职位'
      showResults.value = true
    }
  }, 600)
}

// 高薪榜
function findHighSalary() {
  addAIMessage('高薪职位来咯！让我帮你排个序... 💰')
  showThinking()
  showMainMenu.value = false
  
  setTimeout(() => {
    hideThinking()
    showHappy()
    const sorted = [...props.careers].sort((a, b) => {
      const getSalary = (s) => {
        if (!s) return 0
        const match = s.match(/(\d+)/)
        return match ? parseInt(match[1]) : 0
      }
      return getSalary(b.salary) - getSalary(a.salary)
    })
    
    addAIMessage('这些是薪资最高的职位，羡慕吧~')
    results.value = sorted.slice(0, 10)
    resultsTitle.value = '💰 高薪榜'
    showResults.value = true
    emit('highlight', sorted.slice(0, 10).map(c => c.id))
  }, 600)
}

// 技能分析
function analyzeSkills() {
  addAIMessage('来看看职场最热门的技能是什么... 🧠')
  showThinking()
  showMainMenu.value = false
  
  setTimeout(() => {
    hideThinking()
    // 统计技能出现频率
    const skillCount = {}
    props.careers.forEach(c => {
      c.skills?.forEach(s => {
        skillCount[s] = (skillCount[s] || 0) + 1
      })
    })
    
    const topSkills = Object.entries(skillCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([skill, count]) => `${skill}（${count}个职位需要）`)
    
    if (topSkills.length > 0) {
      addAIMessage(`📊 热门技能排行：\n${topSkills.map((s, i) => `${i + 1}. ${s}`).join('\n')}\n\n掌握这些技能，找工作更容易哦！`)
    } else {
      addAIMessage('暂时还没有技能数据呢~')
    }
    
    showMainMenu.value = true
    setTimeout(() => {
      quickReplies.value = [
        { id: 'search', icon: '🔍', text: '搜索相关职位' },
        { id: 'back', icon: '🏠', text: '返回主菜单' }
      ]
    }, 500)
  }, 800)
}

// 随机探索
function randomExplore() {
  addAIMessage('让命运帮你选一个吧！🎲')
  
  setTimeout(() => {
    const random = props.careers[Math.floor(Math.random() * props.careers.length)]
    if (random) {
      showHappy()
      addAIMessage(`✨ 随机到了「${random.name}」！\n${random.category ? `属于${random.category}方向，` : ''}${random.salary ? `薪资${random.salary}，` : ''}要不要了解一下？`)
      emit('focusCareer', random)
      emit('highlight', [random.id])
      
      setTimeout(() => {
        quickReplies.value = [
          { id: 'detail', icon: '👀', text: '查看详情' },
          { id: 'another', icon: '🎲', text: '再抽一个' },
          { id: 'back', icon: '🏠', text: '返回' }
        ]
      }, 500)
    }
  }, 500)
}

// 职业测验
function startQuiz() {
  showMainMenu.value = false
  showChatInput.value = false
  showQuiz.value = true
  quizCurrentIndex.value = 0
  quizAnswers.value = []
}

function answerQuiz(opt) {
  quizAnswers.value.push(opt.value)
  
  if (quizCurrentIndex.value < quizQuestions.length - 1) {
    const progressMsg = aiResponses.quiz.progress[Math.min(quizCurrentIndex.value, 3)]
    addAIMessage(progressMsg)
    quizCurrentIndex.value++
  } else {
    finishQuiz()
  }
}

function finishQuiz() {
  showQuiz.value = false
  showChatInput.value = true
  showThinking()
  addAIMessage('分析你的答案中... 🔮')
  
  setTimeout(() => {
    hideThinking()
    showHappy()
    
    // 简单的职业推荐逻辑
    const answers = quizAnswers.value
    let recommendations = []
    
    if (answers.includes('creative')) {
      recommendations.push('UI/UX设计师', '产品经理', '内容创作者')
    }
    if (answers.includes('analytical')) {
      recommendations.push('数据分析师', '商业分析师', '量化研究员')
    }
    if (answers.includes('tech-love')) {
      recommendations.push('软件工程师', 'AI工程师', '全栈开发')
    }
    if (answers.includes('social')) {
      recommendations.push('市场营销', '商务拓展', '人力资源')
    }
    if (answers.includes('money')) {
      recommendations.push('金融分析师', '投资经理', '高级架构师')
    }
    
    if (recommendations.length === 0) {
      recommendations = ['产品经理', '项目经理', '运营专员']
    }
    
    const unique = [...new Set(recommendations)].slice(0, 4)
    addAIMessage(`🎯 根据你的回答，我觉得这些职业方向很适合你：\n\n${unique.map((r, i) => `${i + 1}. ${r}`).join('\n')}\n\n想搜索这些职位吗？`)
    
    showMainMenu.value = true
    setTimeout(() => {
      quickReplies.value = unique.map(r => ({
        id: 'search-' + r,
        icon: '🔍',
        text: `找"${r}"`
      }))
    }, 500)
  }, 1500)
}

// 选择结果
function selectResult(item) {
  showHappy()
  addAIMessage(`好眼光！带你去看看「${item.name}」~`)
  emit('focusCareer', item)
  
  setTimeout(() => close(), 800)
}

// 闲聊气泡定时器
let idleBubbleTimer = null
let blinkTimer = null

onMounted(() => {
  // 闲聊气泡
  idleBubbleTimer = setInterval(() => {
    if (!isActive.value && Math.random() > 0.6) {
      idleBubbleText.value = randomPick(idleBubbles)
      showIdleBubble.value = true
      setTimeout(() => { showIdleBubble.value = false }, 4000)
    }
  }, 8000)
  
  // 眨眼
  blinkTimer = setInterval(() => {
    if (eyeState.value === 'normal' && !isThinking.value) {
      eyeState.value = 'blink'
      setTimeout(() => { eyeState.value = 'normal' }, 150)
    }
  }, 3500)
  
  // 初始延迟显示气泡
  setTimeout(() => {
    if (!isActive.value) {
      idleBubbleText.value = getTimeGreeting().greeting + ' ' + getTimeGreeting().emoji
      showIdleBubble.value = true
      setTimeout(() => { showIdleBubble.value = false }, 5000)
    }
  }, 3000)
})

onUnmounted(() => {
  if (idleBubbleTimer) clearInterval(idleBubbleTimer)
  if (blinkTimer) clearInterval(blinkTimer)
})

// 监听快捷回复的额外处理
watch(quickReplies, () => {
  quickReplies.value.forEach(reply => {
    if (reply.id === 'another') {
      reply.handler = () => randomExplore()
    } else if (reply.id === 'back') {
      reply.handler = () => backToMenu()
    } else if (reply.id?.startsWith('search-')) {
      const keyword = reply.id.replace('search-', '')
      reply.handler = () => {
        searchQuery.value = keyword
        doSearch()
      }
    }
  })
})

// 处理快捷回复
function handleQuickReply(reply) {
  if (reply.handler) {
    addUserMessage(reply.text)
    quickReplies.value = []
    reply.handler()
  } else if (reply.id === 'another') {
    addUserMessage(reply.text)
    quickReplies.value = []
    randomExplore()
  } else if (reply.id === 'back') {
    addUserMessage(reply.text)
    quickReplies.value = []
    backToMenu()
  } else if (reply.id?.startsWith('search-')) {
    const keyword = reply.id.replace('search-', '')
    addUserMessage(reply.text)
    quickReplies.value = []
    searchQuery.value = keyword
    addAIMessage(`好的，帮你搜索"${keyword}"...`)
    setTimeout(() => doSearch(true), 500)
  } else if (reply.id === 'quiz-start') {
    addUserMessage(reply.text)
    quickReplies.value = []
    addAIMessage(aiResponses.quiz.start)
    setTimeout(() => startQuiz(), 800)
  } else if (reply.id === 'explore') {
    addUserMessage(reply.text)
    quickReplies.value = []
    showMainMenu.value = false
    showSearch.value = true
    addAIMessage('告诉我你想找什么类型的工作~')
    nextTick(() => searchInputRef.value?.focus())
  } else if (reply.id === 'more') {
    addUserMessage(reply.text)
    quickReplies.value = []
    showMainMenu.value = true
    addAIMessage('还想探索什么？选一个功能吧~')
  } else if (reply.id === 'done') {
    addUserMessage(reply.text)
    close()
  } else if (reply.id === 'detail') {
    addUserMessage(reply.text)
    // 已经聚焦了，直接关闭让用户看详情
    close()
  } else if (reply.id === 'search') {
    addUserMessage(reply.text)
    quickReplies.value = []
    showMainMenu.value = false
    showSearch.value = true
    addAIMessage('想搜索什么技能或职位呢？')
  } else {
    // 原有逻辑
    addUserMessage(reply.text)
    quickReplies.value = []
    
    setTimeout(() => {
      switch(reply.id) {
        case 'hi':
          addAIMessage(randomPick(aiResponses.greetings))
          break
        case 'help':
          addAIMessage(randomPick(aiResponses.help))
          break
        case 'tips':
          addAIMessage(randomPick(aiResponses.tips))
          break
      }
      setTimeout(() => {
        quickReplies.value = [
          { id: 'quiz-start', icon: '📝', text: '做个测验' },
          { id: 'explore', icon: '🔍', text: '开始找职业' }
        ]
      }, 500)
    }, 400)
  }
}
</script>

<style scoped>
.ai-companion {
  position: fixed;
  z-index: 1000;
  font-family: 'Inter', -apple-system, sans-serif;
  transition: none;
}

.ai-companion.is-dragging {
  cursor: grabbing;
  user-select: none;
}

.companion-wrapper {
  position: relative;
  cursor: grab;
}

.ai-companion.is-dragging .companion-wrapper {
  cursor: grabbing;
}

.ai-companion.is-active .companion-wrapper {
  cursor: pointer;
}

/* 背景遮罩 */
.backdrop {
  position: fixed;
  inset: 0;
  z-index: -1;
}

.pulse-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.4);
  animation: pulse 2s ease-out infinite;
}
.pulse-ring.delay { animation-delay: 1s; }

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.8); opacity: 0; }
}

.robot-avatar {
  width: 72px;
  height: 72px;
  position: relative;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.robot-avatar:hover { transform: scale(1.08); }
.robot-avatar.happy { animation: bounce 0.5s ease; }
.robot-avatar.wave { animation: wave 0.8s ease; }

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
@keyframes wave {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

.avatar-glow {
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.35) 0%, transparent 70%);
  filter: blur(8px);
  animation: glow-pulse 3s ease-in-out infinite;
}
@keyframes glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}
:global(html.light) .avatar-glow {
  background: radial-gradient(circle, rgba(6, 182, 212, 0.4) 0%, transparent 70%);
}

.avatar-main { width: 100%; height: 100%; position: relative; }

.antenna-wrap {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.antenna-stem {
  width: 4px;
  height: 10px;
  background: linear-gradient(to bottom, #a78bfa, #8b5cf6);
  border-radius: 2px;
}
.antenna-tip {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #34d399, #10b981);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
  animation: glow-soft 2s ease-in-out infinite;
}
.antenna-tip.active {
  animation: blink-fast 0.4s ease-in-out infinite;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.7);
}
@keyframes glow-soft {
  0%, 100% { box-shadow: 0 0 8px rgba(16, 185, 129, 0.5); }
  50% { box-shadow: 0 0 16px rgba(16, 185, 129, 0.8); }
}
@keyframes blink-fast {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.face {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(145deg, #fef3c7, #fde68a);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 -4px 12px rgba(0, 0, 0, 0.05), inset 0 4px 8px rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}
:global(html.light) .face {
  background: linear-gradient(145deg, #fef3c7, #fcd34d);
}

.eyes {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 16px;
}
.eye {
  width: 14px;
  height: 14px;
  background: #1e293b;
  border-radius: 50%;
  position: relative;
  transition: all 0.15s ease;
}
.eye.blink { height: 3px; border-radius: 3px; }
.eye.happy { height: 8px; border-radius: 8px 8px 50% 50%; }
.pupil {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  background: #1e293b;
  border-radius: 50%;
}
.eye.blink .pupil, .eye.happy .pupil { display: none; }
.highlight {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
}
.eye.blink .highlight, .eye.happy .highlight { display: none; }

.mouth {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 8px;
  background: #1e293b;
  border-radius: 0 0 16px 16px;
  transition: all 0.2s ease;
}
.mouth.speaking { animation: talk 0.25s ease-in-out infinite; }
.mouth.smile { width: 20px; height: 10px; border-radius: 0 0 20px 20px; }
@keyframes talk {
  0%, 100% { height: 8px; }
  50% { height: 14px; border-radius: 50%; }
}

.cheek {
  position: absolute;
  width: 10px;
  height: 6px;
  background: rgba(251, 113, 133, 0.5);
  border-radius: 50%;
  top: 36px;
}
.cheek.left { left: 8px; }
.cheek.right { right: 8px; }

.status-indicator {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.9);
  padding: 3px 10px;
  border-radius: 10px;
  white-space: nowrap;
}
:global(html.light) .status-indicator {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.status-text { font-size: 10px; font-weight: 500; color: #10b981; }
.status-indicator.thinking .status-text { color: #f59e0b; }

/* 闲聊气泡 */
.idle-bubble {
  position: absolute;
  bottom: 20px;
  left: 85px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  padding: 10px 16px;
  border-radius: 16px 16px 16px 4px;
  color: white;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
  cursor: pointer;
  animation: float 3s ease-in-out infinite;
  white-space: nowrap;
  max-width: 240px;
}
.bubble-tail {
  display: none;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
.bubble-pop-enter-active { animation: pop-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.bubble-pop-leave-active { animation: pop-out 0.3s ease; }
@keyframes pop-in {
  0% { transform: scale(0) translateY(10px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes pop-out {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0; }
}

/* 主面板 */
.main-panel {
  position: absolute;
  bottom: 84px;
  left: 0;
  width: 340px;
  max-height: 520px;
  background: rgba(15, 23, 42, 0.98);
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
}
:global(html.light) .main-panel {
  background: rgba(255, 255, 255, 0.98);
  border-color: rgba(6, 182, 212, 0.25);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.02);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(6, 182, 212, 0.08));
  border-bottom: 1px solid rgba(139, 92, 246, 0.15);
  flex-shrink: 0;
}
:global(html.light) .panel-header {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(14, 165, 233, 0.05));
  border-bottom-color: rgba(6, 182, 212, 0.15);
}
.header-title { display: flex; align-items: center; gap: 8px; }
.title-icon { font-size: 20px; }
.title-text { font-size: 15px; font-weight: 600; color: #f1f5f9; }
:global(html.light) .title-text { color: #0f172a; }
.close-btn {
  width: 30px;
  height: 30px;
  border: none;
  background: rgba(100, 116, 139, 0.15);
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.close-btn:hover { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* 对话区域 */
.chat-zone {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 100px;
  max-height: 180px;
}
.chat-zone::-webkit-scrollbar { width: 4px; }
.chat-zone::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 2px; }

.chat-message {
  display: flex;
  gap: 10px;
  animation: msg-in 0.3s ease;
}
@keyframes msg-in {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.chat-message.user { flex-direction: row-reverse; }
.msg-avatar { font-size: 20px; flex-shrink: 0; }
.msg-content {
  max-width: 80%;
  background: rgba(139, 92, 246, 0.15);
  padding: 10px 14px;
  border-radius: 16px;
  border-top-left-radius: 4px;
}
.chat-message.user .msg-content {
  background: rgba(6, 182, 212, 0.2);
  border-radius: 16px;
  border-top-right-radius: 4px;
}
:global(html.light) .msg-content { background: rgba(139, 92, 246, 0.1); }
:global(html.light) .chat-message.user .msg-content { background: rgba(6, 182, 212, 0.15); }
.msg-text {
  font-size: 14px;
  line-height: 1.5;
  color: #e2e8f0;
  margin: 0;
  white-space: pre-line;
}
:global(html.light) .msg-text { color: #1e293b; }
.msg-time { font-size: 10px; color: #64748b; margin-top: 4px; display: block; }

/* 打字指示器 */
.typing-dots {
  display: flex;
  gap: 4px;
  padding: 4px 0;
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
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40% { transform: translateY(-6px); opacity: 1; }
}

/* 快捷回复 */
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 16px 12px;
  flex-shrink: 0;
}
.quick-reply-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 20px;
  color: #a78bfa;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.quick-reply-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  transform: translateY(-2px);
}
:global(html.light) .quick-reply-btn {
  background: rgba(6, 182, 212, 0.08);
  border-color: rgba(6, 182, 212, 0.25);
  color: #0891b2;
}
.reply-icon { font-size: 14px; }

/* 功能网格 */
.action-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 0 16px 12px;
  flex-shrink: 0;
}
.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  background: rgba(100, 116, 139, 0.1);
  border: 1px solid rgba(100, 116, 139, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}
.action-card:hover {
  transform: translateY(-4px);
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}
:global(html.light) .action-card:hover {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.3);
}
.action-card.primary:hover { border-color: #8b5cf6; }
.action-card.hot:hover { border-color: #f97316; }
.action-card.quiz:hover { border-color: #10b981; }
.action-card.salary:hover { border-color: #eab308; }
.action-card.skills:hover { border-color: #ec4899; }
.action-card.random:hover { border-color: #06b6d4; }
.action-icon { font-size: 24px; }
.action-label { font-size: 12px; font-weight: 500; color: #cbd5e1; }
:global(html.light) .action-label { color: #475569; }
.action-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 8px;
  font-weight: 600;
}

/* 搜索区域 */
.search-section { padding: 0 16px 16px; flex-shrink: 0; }
.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(100, 116, 139, 0.12);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 14px;
  transition: all 0.2s ease;
}
.search-box:focus-within {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.08);
}
:global(html.light) .search-box:focus-within {
  border-color: #0891b2;
  background: rgba(6, 182, 212, 0.05);
}
.search-box i { color: #64748b; font-size: 16px; }
.search-box input {
  flex: 1;
  background: none;
  border: none;
  color: #f1f5f9;
  font-size: 14px;
  outline: none;
}
:global(html.light) .search-box input { color: #1e293b; }
.search-box input::placeholder { color: #64748b; }
.clear-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: rgba(100, 116, 139, 0.2);
  border-radius: 6px;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.clear-btn:hover { background: rgba(100, 116, 139, 0.3); }

.quick-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.quick-tag {
  padding: 6px 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 20px;
  color: #a78bfa;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}
:global(html.light) .quick-tag {
  background: rgba(6, 182, 212, 0.08);
  border-color: rgba(6, 182, 212, 0.2);
  color: #0891b2;
}
.quick-tag:hover { background: rgba(139, 92, 246, 0.2); transform: translateY(-2px); }

.search-actions { display: flex; gap: 10px; margin-top: 14px; }
.btn-secondary {
  flex: 1;
  padding: 10px;
  background: rgba(100, 116, 139, 0.15);
  border: none;
  border-radius: 10px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-secondary:hover { background: rgba(100, 116, 139, 0.25); color: #f1f5f9; }
.btn-primary {
  flex: 1;
  padding: 10px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

/* 测验区域 */
.quiz-section { padding: 0 16px 16px; flex-shrink: 0; }
.quiz-progress {
  height: 6px;
  background: rgba(100, 116, 139, 0.2);
  border-radius: 3px;
  position: relative;
  margin-bottom: 16px;
}
.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #06b6d4);
  border-radius: 3px;
  transition: width 0.4s ease;
}
.progress-text {
  position: absolute;
  right: 0;
  top: 10px;
  font-size: 11px;
  color: #64748b;
}
.quiz-question { margin-bottom: 14px; }
.question-text { font-size: 15px; font-weight: 500; color: #e2e8f0; margin: 0; line-height: 1.5; }
:global(html.light) .question-text { color: #1e293b; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(100, 116, 139, 0.1);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}
.quiz-option:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateX(4px);
}
.opt-icon { font-size: 20px; }
.opt-text { font-size: 14px; color: #e2e8f0; }
:global(html.light) .opt-text { color: #1e293b; }

/* 结果区域 */
.results-section { padding: 0 16px 16px; flex-shrink: 0; }
.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.results-title { font-size: 14px; font-weight: 600; color: #e2e8f0; }
:global(html.light) .results-title { color: #1e293b; }
.results-count { font-size: 12px; color: #64748b; }
.results-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
  padding-right: 4px;
}
.results-list::-webkit-scrollbar { width: 4px; }
.results-list::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 2px; }
.result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(100, 116, 139, 0.08);
  border: 1px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  text-align: left;
}
.result-card:hover {
  background: rgba(139, 92, 246, 0.12);
  border-color: rgba(139, 92, 246, 0.25);
  transform: translateX(4px);
}
:global(html.light) .result-card:hover {
  background: rgba(6, 182, 212, 0.08);
  border-color: rgba(6, 182, 212, 0.25);
}
.result-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color);
  box-shadow: 0 0 10px var(--color);
  flex-shrink: 0;
}
.result-info { flex: 1; min-width: 0; }
.result-name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #f1f5f9;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
:global(html.light) .result-name { color: #1e293b; }
.result-meta { display: block; font-size: 12px; color: #64748b; margin-top: 2px; }
.result-card i { color: #64748b; font-size: 16px; transition: transform 0.2s ease; }
.result-card:hover i { transform: translateX(4px); color: #8b5cf6; }
:global(html.light) .result-card:hover i { color: #0891b2; }
.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 10px;
  background: rgba(100, 116, 139, 0.1);
  border: none;
  border-radius: 10px;
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
  margin-top: 12px;
  transition: all 0.2s ease;
}
.back-btn:hover { background: rgba(100, 116, 139, 0.2); color: #f1f5f9; }

/* 聊天输入框 */
.chat-input-bar {
  display: flex;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.6);
  border-top: 1px solid rgba(100, 116, 139, 0.15);
  flex-shrink: 0;
}
:global(html.light) .chat-input-bar {
  background: rgba(248, 250, 252, 0.8);
  border-top-color: rgba(0, 0, 0, 0.05);
}
.chat-input-bar input {
  flex: 1;
  padding: 10px 14px;
  background: rgba(100, 116, 139, 0.12);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}
.chat-input-bar input:focus {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.08);
}
:global(html.light) .chat-input-bar input {
  color: #1e293b;
  background: white;
  border-color: rgba(0, 0, 0, 0.1);
}
.chat-input-bar input::placeholder { color: #64748b; }
.send-btn {
  width: 42px;
  height: 42px;
  border: none;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  border-radius: 12px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.send-btn:hover:not(:disabled) { transform: scale(1.05); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
.send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* 面板动画 */
.panel-spring-enter-active { animation: panel-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.panel-spring-leave-active { animation: panel-out 0.25s ease; }
@keyframes panel-in {
  0% { opacity: 0; transform: translateY(20px) scale(0.95); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes panel-out {
  0% { opacity: 1; transform: translateY(0) scale(1); }
  100% { opacity: 0; transform: translateY(10px) scale(0.98); }
}

/* ═══════════════════════════════════════
   移动端适配样式
   ═══════════════════════════════════════ */

@media (max-width: 768px) {
  .ai-companion {
    bottom: 140px !important;
    right: 12px !important;
    left: auto !important;
  }
  
  .main-panel {
    position: fixed !important;
    bottom: auto !important;
    top: 60px !important;
    left: 12px !important;
    right: 12px !important;
    width: auto !important;
    max-width: none !important;
    max-height: calc(100vh - 200px) !important;
    border-radius: 16px !important;
  }
  
  .companion-avatar {
    width: 50px !important;
    height: 50px !important;
  }
  
  .panel-header {
    padding: 12px 14px !important;
  }
  
  .panel-title {
    font-size: 15px !important;
  }
  
  .chat-messages {
    padding: 10px 12px !important;
  }
  
  .action-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    padding: 12px !important;
  }
  
  .action-card {
    padding: 12px 10px !important;
  }
  
  .action-icon {
    width: 36px !important;
    height: 36px !important;
  }
  
  .action-label {
    font-size: 11px !important;
  }
  
  .chat-input-bar {
    padding: 10px 12px !important;
  }
  
  .chat-input-bar input {
    padding: 10px 12px !important;
    font-size: 14px !important;
  }
  
  .send-btn {
    width: 40px !important;
    height: 40px !important;
  }
  
  .idle-bubble {
    display: none !important;
  }
}

@media (max-width: 480px) {
  .ai-companion {
    bottom: 130px !important;
    right: 8px !important;
  }
  
  .main-panel {
    left: 8px !important;
    right: 8px !important;
    top: 56px !important;
    max-height: calc(100vh - 180px) !important;
  }
  
  .companion-avatar {
    width: 44px !important;
    height: 44px !important;
  }
  
  .action-grid {
    gap: 6px !important;
    padding: 10px !important;
  }
}
</style>
