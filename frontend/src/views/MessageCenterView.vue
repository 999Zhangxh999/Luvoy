<template>
  <div class="message-center">
    <!-- 背景动效 -->
    <div class="msg-background">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-orb orb-3"></div>
    </div>

    <div class="msg-container">
      <!-- 左侧会话列表 -->
      <aside class="conversation-list">
        <div class="list-header">
          <router-link to="/job-hub" class="back-btn">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <h2><i class="bi bi-chat-dots-fill"></i> 消息中心</h2>
        </div>

        <!-- 搜索 -->
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input v-model="searchQuery" placeholder="搜索消息..." />
        </div>

        <!-- 分类标签 -->
        <div class="tab-bar">
          <button 
            v-for="tab in tabs" 
            :key="tab.key"
            :class="['tab-btn', { active: currentTab === tab.key }]"
            @click="currentTab = tab.key"
          >
            <span class="tab-label">{{ tab.label }}</span>
            <span v-if="tab.unread" class="tab-badge">{{ tab.unread }}</span>
          </button>
        </div>

        <!-- 会话列表 -->
        <div class="conversations">
          <div 
            v-for="conv in filteredConversations" 
            :key="conv.id"
            :class="['conv-item', { active: selectedConv?.id === conv.id, unread: conv.unread }]"
            @click="selectConversation(conv)"
          >
            <div class="conv-avatar" :style="{ background: conv.avatarColor }">
              {{ conv.avatarText }}
              <span v-if="conv.online" class="online-dot"></span>
            </div>
            <div class="conv-info">
              <div class="conv-header">
                <span class="conv-name">{{ conv.name }}</span>
                <span class="conv-time">{{ conv.time }}</span>
              </div>
              <div class="conv-preview">
                <span class="conv-badge" :class="conv.type">{{ conv.typeLabel }}</span>
                <span class="conv-text">{{ conv.lastMessage }}</span>
              </div>
            </div>
            <span v-if="conv.unread" class="unread-count">{{ conv.unread }}</span>
          </div>

          <div v-if="!filteredConversations.length" class="no-conversations">
            <i class="bi bi-chat-left-text"></i>
            <p>暂无消息</p>
          </div>
        </div>
      </aside>

      <!-- 右侧聊天区 -->
      <main class="chat-area">
        <template v-if="selectedConv">
          <!-- 聊天头部 -->
          <div class="chat-header">
            <div class="chat-info">
              <div class="chat-avatar" :style="{ background: selectedConv.avatarColor }">
                {{ selectedConv.avatarText }}
              </div>
              <div class="chat-meta">
                <h3>{{ selectedConv.name }}</h3>
                <span class="chat-status" :class="{ online: selectedConv.online }">
                  {{ selectedConv.online ? '在线' : `活跃于${selectedConv.lastActive}` }}
                </span>
              </div>
            </div>
            <div class="chat-actions">
              <button class="action-btn" title="查看画像" @click="viewProfile">
                <i class="bi bi-person-badge"></i>
              </button>
              <button class="action-btn" title="更多选项">
                <i class="bi bi-three-dots-vertical"></i>
              </button>
            </div>
          </div>

          <!-- 相关职位/画像 卡片 -->
          <div v-if="selectedConv.relatedInfo" class="related-card">
            <div class="related-icon">
              <i :class="selectedConv.type === 'invitation' ? 'bi bi-briefcase' : 'bi bi-person-badge'"></i>
            </div>
            <div class="related-info">
              <span class="related-label">{{ selectedConv.type === 'invitation' ? '相关职位' : '相关画像' }}</span>
              <span class="related-title">{{ selectedConv.relatedInfo.title }}</span>
            </div>
            <span class="match-badge">匹配 {{ selectedConv.relatedInfo.matchScore }}%</span>
          </div>

          <!-- 消息列表 -->
          <div class="message-list" ref="messageListRef">
            <div 
              v-for="(msg, index) in currentMessages" 
              :key="index"
              :class="['message', msg.isMine ? 'mine' : 'theirs']"
            >
              <div v-if="!msg.isMine" class="msg-avatar" :style="{ background: selectedConv.avatarColor }">
                {{ selectedConv.avatarText }}
              </div>
              <div class="msg-content">
                <div v-if="msg.type === 'text'" class="msg-bubble">
                  <p>{{ msg.content }}</p>
                  <span class="msg-time">{{ msg.time }}</span>
                </div>
                <div v-else-if="msg.type === 'card'" class="msg-card">
                  <div class="card-header">
                    <i :class="msg.cardIcon"></i>
                    <span>{{ msg.cardTitle }}</span>
                  </div>
                  <div class="card-body">
                    <h4>{{ msg.content }}</h4>
                    <p>{{ msg.cardDesc }}</p>
                  </div>
                  <div class="card-footer">
                    <button class="card-btn" @click="handleCardAction(msg)">
                      {{ msg.cardAction }}
                    </button>
                  </div>
                </div>
                <div v-else-if="msg.type === 'system'" class="msg-system">
                  <i class="bi bi-info-circle"></i>
                  {{ msg.content }}
                </div>
              </div>
            </div>

            <!-- 打字指示器 -->
            <div v-if="isTyping" class="typing-indicator">
              <div class="msg-avatar" :style="{ background: selectedConv.avatarColor }">
                {{ selectedConv.avatarText }}
              </div>
              <div class="typing-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>

          <!-- 快捷回复 -->
          <div class="quick-replies">
            <button 
              v-for="reply in quickReplies" 
              :key="reply"
              class="quick-btn"
              @click="sendQuickReply(reply)"
            >
              {{ reply }}
            </button>
          </div>

          <!-- 输入区 -->
          <div class="chat-input">
            <button class="input-action" title="添加附件">
              <i class="bi bi-paperclip"></i>
            </button>
            <input 
              v-model="inputMessage" 
              placeholder="输入消息..." 
              @keyup.enter="sendMessage"
            />
            <button class="input-action" title="发送表情">
              <i class="bi bi-emoji-smile"></i>
            </button>
            <button 
              class="send-btn" 
              :class="{ active: inputMessage.trim() }"
              :disabled="!inputMessage.trim()"
              @click="sendMessage"
            >
              <i class="bi bi-send-fill"></i>
            </button>
          </div>
        </template>

        <!-- 未选择会话 -->
        <div v-else class="no-chat-selected">
          <div class="empty-icon">
            <i class="bi bi-chat-square-heart"></i>
          </div>
          <h3>开始对话</h3>
          <p>选择一个会话开始交流，或浏览职位/人才开启新对话</p>
          <div class="empty-actions">
            <router-link to="/job-market" class="empty-btn">
              <i class="bi bi-building"></i> 浏览职位
            </router-link>
            <router-link to="/talent-market" class="empty-btn secondary">
              <i class="bi bi-people"></i> 浏览人才
            </router-link>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, inject } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const toast = inject('toast', null)

// 当前标签
const currentTab = ref('all')
const tabs = [
  { key: 'all', label: '全部', unread: 5 },
  { key: 'invitation', label: '邀请', unread: 2 },
  { key: 'application', label: '投递', unread: 3 },
  { key: 'system', label: '系统', unread: 0 },
]

// 搜索
const searchQuery = ref('')

// 会话数据
const conversations = ref([
  {
    id: 1,
    name: '字节跳动HR - 王经理',
    avatarText: '王',
    avatarColor: 'linear-gradient(135deg, #4f46e5, #6366f1)',
    lastMessage: '您好，看了您的简历很匹配我们的岗位，方便聊聊吗？',
    time: '刚刚',
    unread: 2,
    online: true,
    type: 'invitation',
    typeLabel: '邀请',
    relatedInfo: { title: '高级前端开发工程师', matchScore: 92 },
    lastActive: ''
  },
  {
    id: 2,
    name: '阿里巴巴HR - 李总',
    avatarText: '李',
    avatarColor: 'linear-gradient(135deg, #f59e0b, #d97706)',
    lastMessage: '期待您的回复，我们下周可以安排面试',
    time: '10分钟前',
    unread: 1,
    online: false,
    type: 'invitation',
    typeLabel: '邀请',
    relatedInfo: { title: 'AI算法工程师', matchScore: 85 },
    lastActive: '2小时前'
  },
  {
    id: 3,
    name: '腾讯招聘',
    avatarText: '腾',
    avatarColor: 'linear-gradient(135deg, #06b6d4, #0891b2)',
    lastMessage: '您投递的"数据分析师"岗位已进入筛选阶段',
    time: '1小时前',
    unread: 1,
    online: false,
    type: 'application',
    typeLabel: '投递',
    relatedInfo: { title: '数据分析师', matchScore: 88 },
    lastActive: '30分钟前'
  },
  {
    id: 4,
    name: '美团点评',
    avatarText: '美',
    avatarColor: 'linear-gradient(135deg, #10b981, #059669)',
    lastMessage: '感谢投递，我们将尽快处理',
    time: '昨天',
    unread: 0,
    online: false,
    type: 'application',
    typeLabel: '投递',
    relatedInfo: { title: '全栈工程师', matchScore: 78 },
    lastActive: '昨天'
  },
  {
    id: 5,
    name: '系统通知',
    avatarText: '系',
    avatarColor: 'linear-gradient(135deg, #64748b, #475569)',
    lastMessage: '您的画像已更新，新增匹配职位12个',
    time: '2天前',
    unread: 1,
    online: false,
    type: 'system',
    typeLabel: '系统',
    relatedInfo: null,
    lastActive: ''
  }
])

// 选中的会话
const selectedConv = ref(null)

// 消息历史
const messagesMap = ref({
  1: [
    { type: 'system', content: '对话开始于 今天 14:30' },
    { type: 'card', isMine: false, cardIcon: 'bi bi-briefcase', cardTitle: '职位邀请', content: '高级前端开发工程师', cardDesc: '字节跳动 · 上海 · 25-40K', cardAction: '查看职位', time: '14:30' },
    { type: 'text', isMine: false, content: '您好，我是字节跳动的HR王经理。看了您的简历和技能画像，与我们团队需求非常匹配！', time: '14:31' },
    { type: 'text', isMine: false, content: '我们正在招聘高级前端开发工程师，团队技术氛围很好，您有兴趣聊聊吗？', time: '14:32' },
    { type: 'text', isMine: true, content: '您好王经理，感谢关注！我目前确实在看机会', time: '14:35' },
    { type: 'text', isMine: true, content: '方便了解一下具体的项目和团队情况吗？', time: '14:35' },
    { type: 'text', isMine: false, content: '当然可以！我们是抖音核心业务团队，主要负责创作者工具平台的研发...', time: '刚刚' },
  ],
  2: [
    { type: 'system', content: '对话开始于 今天 10:15' },
    { type: 'card', isMine: false, cardIcon: 'bi bi-briefcase', cardTitle: '职位邀请', content: 'AI算法工程师', cardDesc: '阿里巴巴 · 杭州 · 35-60K', cardAction: '查看职位', time: '10:15' },
    { type: 'text', isMine: false, content: '您好！您的AI背景和项目经验非常出色', time: '10:16' },
    { type: 'text', isMine: false, content: '期待您的回复，我们下周可以安排面试', time: '10:17' },
  ],
  3: [
    { type: 'system', content: '您投递了"数据分析师"岗位' },
    { type: 'card', isMine: true, cardIcon: 'bi bi-send', cardTitle: '投递申请', content: '数据分析师', cardDesc: '腾讯 · 深圳 · 20-35K', cardAction: '查看详情', time: '09:00' },
    { type: 'text', isMine: false, content: '收到您的申请，目前正在筛选中', time: '11:30' },
    { type: 'text', isMine: false, content: '您投递的"数据分析师"岗位已进入筛选阶段', time: '1小时前' },
  ]
})

// 当前消息
const currentMessages = computed(() => {
  if (!selectedConv.value) return []
  return messagesMap.value[selectedConv.value.id] || []
})

// 筛选会话
const filteredConversations = computed(() => {
  let list = conversations.value
  
  if (currentTab.value !== 'all') {
    list = list.filter(c => c.type === currentTab.value)
  }
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c => 
      c.name.toLowerCase().includes(q) || 
      c.lastMessage.toLowerCase().includes(q)
    )
  }
  
  return list
})

// 快捷回复
const quickReplies = [
  '好的，谢谢！',
  '请问具体薪资范围？',
  '方便约个时间详聊吗？',
  '我需要考虑一下'
]

// 输入
const inputMessage = ref('')
const isTyping = ref(false)
const messageListRef = ref(null)

// 选择会话
function selectConversation(conv) {
  selectedConv.value = conv
  if (conv.unread) {
    conv.unread = 0
    updateTabUnread()
  }
  scrollToBottom()
}

// 更新标签未读数
function updateTabUnread() {
  tabs.forEach(tab => {
    if (tab.key === 'all') {
      tab.unread = conversations.value.reduce((sum, c) => sum + (c.unread || 0), 0)
    } else {
      tab.unread = conversations.value.filter(c => c.type === tab.key).reduce((sum, c) => sum + (c.unread || 0), 0)
    }
  })
}

// 发送消息
function sendMessage() {
  if (!inputMessage.value.trim() || !selectedConv.value) return
  
  const msg = {
    type: 'text',
    isMine: true,
    content: inputMessage.value,
    time: '刚刚'
  }
  
  if (!messagesMap.value[selectedConv.value.id]) {
    messagesMap.value[selectedConv.value.id] = []
  }
  messagesMap.value[selectedConv.value.id].push(msg)
  
  // 更新会话预览
  selectedConv.value.lastMessage = inputMessage.value
  selectedConv.value.time = '刚刚'
  
  inputMessage.value = ''
  scrollToBottom()
  
  // 模拟对方打字
  simulateTyping()
}

// 快捷回复
function sendQuickReply(reply) {
  inputMessage.value = reply
  sendMessage()
}

// 模拟打字
function simulateTyping() {
  isTyping.value = true
  setTimeout(() => {
    isTyping.value = false
    // 模拟回复
    const replies = [
      '好的，收到您的消息了',
      '没问题，我这边安排一下',
      '非常感谢您的关注！'
    ]
    const randomReply = replies[Math.floor(Math.random() * replies.length)]
    messagesMap.value[selectedConv.value.id].push({
      type: 'text',
      isMine: false,
      content: randomReply,
      time: '刚刚'
    })
    scrollToBottom()
  }, 1500)
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

// 查看画像
function viewProfile() {
  if (selectedConv.value.type === 'invitation') {
    router.push(`/job/${selectedConv.value.id}`)
  } else {
    toast?.('查看详情', 'info')
  }
}

// 卡片操作
function handleCardAction(msg) {
  toast?.(`点击了: ${msg.cardAction}`, 'info')
}
</script>

<style scoped>
.message-center {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景动效 */
.msg-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.1;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: var(--orb-color-1, #8b5cf6);
  left: -100px;
  top: 20%;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: var(--orb-color-2, #06b6d4);
  right: -50px;
  top: 50%;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: var(--orb-color-3, #f59e0b);
  left: 30%;
  bottom: -100px;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(20px, 30px) scale(1.02); }
}

.msg-container {
  display: flex;
  height: 100vh;
  position: relative;
  z-index: 1;
}

/* 左侧会话列表 */
.conversation-list {
  width: 360px;
  flex-shrink: 0;
  background: var(--color-brand-surface, #0f0f1a);
  border-right: 1px solid rgba(139, 92, 246, 0.1);
  display: flex;
  flex-direction: column;
}

.list-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.back-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
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

.list-header h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.list-header h2 i {
  color: #8b5cf6;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 16px 20px;
  padding: 10px 14px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 12px;
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

/* 标签栏 */
.tab-bar {
  display: flex;
  gap: 6px;
  padding: 0 20px 16px;
  overflow-x: auto;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid transparent;
  border-radius: 20px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-btn.active {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

.tab-btn:not(.active):hover {
  background: rgba(139, 92, 246, 0.1);
  color: var(--color-brand-text, #e2e8f0);
}

.tab-badge {
  padding: 2px 7px;
  background: #ef4444;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  color: white;
}

/* 会话列表 */
.conversations {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
}

.conv-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 4px;
}

.conv-item:hover {
  background: rgba(139, 92, 246, 0.08);
}

.conv-item.active {
  background: rgba(139, 92, 246, 0.12);
}

.conv-item.unread {
  background: rgba(139, 92, 246, 0.06);
}

.conv-avatar {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  background: #22c55e;
  border: 2px solid var(--color-brand-surface, #0f0f1a);
  border-radius: 50%;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.conv-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-time {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  flex-shrink: 0;
}

.conv-preview {
  display: flex;
  align-items: center;
  gap: 6px;
}

.conv-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
  flex-shrink: 0;
}

.conv-badge.invitation {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.conv-badge.application {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.conv-badge.system {
  background: rgba(100, 116, 139, 0.15);
  color: #94a3b8;
}

.conv-text {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-count {
  width: 20px;
  height: 20px;
  background: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.no-conversations {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-brand-muted, #64748b);
}

.no-conversations i {
  font-size: 40px;
  margin-bottom: 12px;
  opacity: 0.5;
}

/* 右侧聊天区 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--color-brand-card, #1a1a2e);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
  background: rgba(139, 92, 246, 0.03);
}

.chat-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.chat-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.chat-meta h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.chat-status {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.chat-status.online {
  color: #22c55e;
}

.chat-status.online::before {
  content: '•';
  margin-right: 4px;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.08);
  border: none;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

/* 相关卡片 */
.related-card {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 16px 24px;
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
}

.related-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.related-info {
  flex: 1;
}

.related-label {
  display: block;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 2px;
}

.related-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.match-badge {
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #34d399;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 10px;
  max-width: 75%;
}

.message.mine {
  flex-direction: row-reverse;
  margin-left: auto;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.msg-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.msg-bubble {
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 16px 16px 16px 4px;
  max-width: 100%;
}

.message.mine .msg-bubble {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 16px 16px 4px 16px;
}

.msg-bubble p {
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.message.mine .msg-bubble p {
  color: white;
}

.msg-time {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
  margin-top: 4px;
}

.message.mine .msg-time {
  text-align: right;
  color: rgba(255, 255, 255, 0.7);
}

/* 消息卡片 */
.msg-card {
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 14px;
  overflow: hidden;
  min-width: 240px;
}

.msg-card .card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(139, 92, 246, 0.08);
  font-size: 12px;
  color: #a78bfa;
}

.msg-card .card-body {
  padding: 14px;
}

.msg-card .card-body h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.msg-card .card-body p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.msg-card .card-footer {
  padding: 10px 14px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.card-btn {
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.card-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

/* 系统消息 */
.msg-system {
  align-self: center;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(100, 116, 139, 0.1);
  border-radius: 20px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 16px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: #a78bfa;
  border-radius: 50%;
  animation: typing 1.4s ease-in-out infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}

/* 快捷回复 */
.quick-replies {
  display: flex;
  gap: 8px;
  padding: 12px 24px;
  overflow-x: auto;
  border-top: 1px solid rgba(139, 92, 246, 0.05);
}

.quick-btn {
  padding: 8px 14px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 20px;
  font-size: 13px;
  color: #a78bfa;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}

/* 输入区 */
.chat-input {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: var(--color-brand-surface, #0f0f1a);
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.input-action {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: transparent;
  border: none;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.input-action:hover {
  color: #a78bfa;
  background: rgba(139, 92, 246, 0.1);
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  outline: none;
  transition: border-color 0.2s;
}

.chat-input input:focus {
  border-color: #8b5cf6;
}

.chat-input input::placeholder {
  color: #64748b;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(139, 92, 246, 0.2);
  border: none;
  color: #64748b;
  cursor: not-allowed;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.send-btn.active {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
  cursor: pointer;
}

.send-btn.active:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
}

/* 未选择会话 */
.no-chat-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.empty-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.15));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: #a78bfa;
  margin-bottom: 24px;
}

.no-chat-selected h3 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.no-chat-selected > p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  text-align: center;
  margin-bottom: 24px;
}

.empty-actions {
  display: flex;
  gap: 12px;
}

.empty-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-decoration: none;
  transition: all 0.2s;
}

.empty-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.empty-btn.secondary {
  background: rgba(6, 182, 212, 0.15);
  border: 1px solid rgba(6, 182, 212, 0.3);
  color: #22d3ee;
}

.empty-btn.secondary:hover {
  background: rgba(6, 182, 212, 0.25);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.2);
}

@media (max-width: 768px) {
  .conversation-list {
    width: 100%;
    position: absolute;
    z-index: 10;
    height: 100%;
  }

  .chat-area {
    position: absolute;
    inset: 0;
    z-index: 5;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .message-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .page-header h1 {
  color: #0c4a6e;
}

:global(html.light) .page-header p {
  color: #64748b;
}

:global(html.light) .chat-container {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .conversation-list {
  background: rgba(8, 145, 178, 0.02);
  border-right-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .list-header {
  border-bottom-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .list-header h3 {
  color: #0c4a6e;
}

:global(html.light) .search-box {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .search-box input {
  color: #0c4a6e;
}

:global(html.light) .search-box input::placeholder {
  color: #94a3b8;
}

:global(html.light) .conv-item {
  border-bottom-color: rgba(8, 145, 178, 0.08);
}

:global(html.light) .conv-item:hover {
  background: rgba(8, 145, 178, 0.05);
}

:global(html.light) .conv-item.active {
  background: rgba(8, 145, 178, 0.1);
  border-left-color: #0891b2;
}

:global(html.light) .conv-avatar {
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .conv-name {
  color: #0c4a6e;
}

:global(html.light) .conv-preview {
  color: #64748b;
}

:global(html.light) .conv-time {
  color: #94a3b8;
}

:global(html.light) .unread-badge {
  background: #0891b2;
}

:global(html.light) .chat-header {
  background: rgba(8, 145, 178, 0.03);
  border-bottom-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .chat-avatar {
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .chat-name {
  color: #0c4a6e;
}

:global(html.light) .chat-status {
  color: #64748b;
}

:global(html.light) .header-actions button {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .header-actions button:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .chat-messages {
  background: rgba(8, 145, 178, 0.02);
}

:global(html.light) .message-bubble {
  background: rgba(8, 145, 178, 0.08);
  color: #0c4a6e;
}

:global(html.light) .message.sent .message-bubble {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  color: white;
}

:global(html.light) .message-time {
  color: #94a3b8;
}

:global(html.light) .date-divider span {
  background: rgba(8, 145, 178, 0.08);
  color: #64748b;
}

:global(html.light) .chat-input {
  background: rgba(8, 145, 178, 0.03);
  border-top-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .input-actions button {
  color: #64748b;
}

:global(html.light) .input-actions button:hover {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .input-field input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .input-field input::placeholder {
  color: #94a3b8;
}

:global(html.light) .input-field input:focus {
  border-color: rgba(8, 145, 178, 0.4);
}

:global(html.light) .btn-send {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .empty-chat {
  color: #64748b;
}

:global(html.light) .empty-chat h3 {
  color: #0c4a6e;
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

:global(html.light) .empty-btn {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .empty-btn:hover {
  box-shadow: 0 6px 20px rgba(8, 145, 178, 0.3);
}

:global(html.light) .empty-btn.secondary {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  color: #0891b2;
}

:global(html.light) .empty-btn.secondary:hover {
  background: rgba(6, 182, 212, 0.18);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.15);
}
</style>
