<template>
  <div class="forum-page">
    <!-- 背景 -->
    <div class="page-background">
      <div class="bg-gradient left"></div>
      <div class="bg-gradient right"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- 头部 -->
    <header class="forum-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="bi bi-chat-square-quote-fill"></i>
            求职交流广场
          </h1>
          <p class="page-desc">分享经验、交流心得、发现机会</p>
        </div>
        <button class="btn-publish" @click="showPublishModal = true">
          <i class="bi bi-plus-lg"></i>
          <span>发布帖子</span>
        </button>
      </div>
      
      <!-- 统计和筛选 -->
      <div class="header-bar">
        <div class="stats-info">
          <span class="stat">
            <i class="bi bi-file-text"></i>
            共 <strong>{{ totalPosts }}</strong> 条帖子
          </span>
          <span class="stat online">
            <span class="online-dot"></span>
            <strong>{{ onlineUsers }}</strong> 人在线
          </span>
        </div>
        
        <div class="filter-tabs">
          <button v-for="tab in filterTabs" :key="tab.value"
            :class="['filter-tab', { active: activeFilter === tab.value }]"
            @click="activeFilter = tab.value">
            {{ tab.label }}
          </button>
        </div>
      </div>
    </header>

    <!-- 帖子列表 -->
    <div class="forum-content">
      <div class="posts-list">
        <TransitionGroup name="post">
          <div v-for="post in filteredPosts" :key="post.id" 
            class="post-card"
            :class="{ 'pinned': post.pinned }"
            @click="openPostDetail(post)">
            
            <!-- 头像 -->
            <div class="post-avatar" :style="{ background: post.avatarColor }">
              {{ post.avatarText }}
              <span v-if="post.online" class="avatar-status"></span>
            </div>
            
            <!-- 主体 -->
            <div class="post-body">
              <!-- 用户信息行 -->
              <div class="post-user">
                <span class="user-name">{{ post.userName }}</span>
                <span :class="['user-role', post.role]">
                  <i :class="post.role === 'seeker' ? 'bi bi-mortarboard-fill' : 'bi bi-briefcase-fill'"></i>
                  {{ post.role === 'seeker' ? '求职' : '招聘' }}
                </span>
                <span v-if="post.pinned" class="tag pinned">
                  <i class="bi bi-pin-angle-fill"></i>
                  置顶
                </span>
                <span v-if="post.hot" class="tag hot">
                  <i class="bi bi-fire"></i>
                  热门
                </span>
              </div>
              
              <!-- 标题 -->
              <h3 class="post-title">{{ post.title }}</h3>
              
              <!-- 内容摘要 -->
              <p class="post-content">{{ post.content }}</p>
              
              <!-- 标签 -->
              <div class="post-tags">
                <span v-if="post.location" class="tag location">
                  <i class="bi bi-geo-alt"></i>
                  {{ post.location }}
                </span>
                <span v-if="post.salary" class="tag salary">
                  <i class="bi bi-currency-yen"></i>
                  {{ post.salary }}
                </span>
                <span v-for="tag in post.skills" :key="tag" class="tag skill">{{ tag }}</span>
              </div>
            </div>
            
            <!-- 互动数据 -->
            <div class="post-stats">
              <div class="stat-item likes" @click.stop="toggleLike(post)">
                <i :class="post.liked ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
                <span>{{ post.likes }}</span>
                <span class="label">点赞</span>
              </div>
              <div class="stat-item comments">
                <i class="bi bi-chat-dots"></i>
                <span>{{ post.comments }}</span>
                <span class="label">评论</span>
              </div>
              <div class="stat-time">{{ post.timeAgo }}</div>
            </div>
          </div>
        </TransitionGroup>
        
        <!-- 加载更多 -->
        <div class="load-more" v-if="hasMore">
          <button class="btn-load" @click="loadMore" :disabled="loading">
            <i class="bi bi-arrow-down-circle" :class="{ 'loading': loading }"></i>
            {{ loading ? '加载中...' : '加载更多' }}
          </button>
        </div>
        
        <!-- 空状态 -->
        <div v-if="filteredPosts.length === 0" class="empty-state">
          <i class="bi bi-chat-square-text"></i>
          <p>暂无帖子，来发布第一条吧！</p>
          <button class="btn-publish-sm" @click="showPublishModal = true">
            <i class="bi bi-plus-lg"></i>
            发布帖子
          </button>
        </div>
      </div>
      
      <!-- 右侧边栏 -->
      <aside class="sidebar">
        <!-- 我的信息 -->
        <div class="sidebar-card my-profile">
          <div class="profile-header">
            <div class="my-avatar" :style="{ background: myProfile.avatarColor }">
              {{ myProfile.avatarText }}
            </div>
            <div class="my-info">
              <h4>{{ myProfile.name }}</h4>
              <span :class="['my-role', myProfile.role]">
                {{ myProfile.role === 'seeker' ? '求职者' : 'HR' }}
              </span>
            </div>
          </div>
          <div class="profile-stats">
            <div class="profile-stat">
              <strong>{{ myProfile.posts }}</strong>
              <span>帖子</span>
            </div>
            <div class="profile-stat">
              <strong>{{ myProfile.likes }}</strong>
              <span>获赞</span>
            </div>
            <div class="profile-stat">
              <strong>{{ myProfile.followers }}</strong>
              <span>关注</span>
            </div>
          </div>
        </div>
        
        <!-- 热门话题 -->
        <div class="sidebar-card hot-topics">
          <h3 class="card-title">
            <i class="bi bi-fire"></i>
            热门话题
          </h3>
          <div class="topic-list">
            <div v-for="(topic, index) in hotTopics" :key="topic.name" 
              class="topic-item"
              @click="searchTopic(topic.name)">
              <span class="topic-rank" :class="getRankClass(index)">{{ index + 1 }}</span>
              <span class="topic-name">{{ topic.name }}</span>
              <span class="topic-count">{{ topic.count }}讨论</span>
            </div>
          </div>
        </div>
        
        <!-- 活跃用户 -->
        <div class="sidebar-card active-users">
          <h3 class="card-title">
            <i class="bi bi-star-fill"></i>
            活跃用户
          </h3>
          <div class="user-list">
            <div v-for="user in activeUsers" :key="user.id" class="user-item">
              <div class="user-avatar" :style="{ background: user.avatarColor }">
                {{ user.avatarText }}
              </div>
              <div class="user-info">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-desc">{{ user.desc }}</span>
              </div>
              <button class="btn-follow" :class="{ following: user.following }" @click="toggleFollow(user)">
                {{ user.following ? '已关注' : '关注' }}
              </button>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- 发帖弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showPublishModal" class="modal-overlay" @click.self="showPublishModal = false">
          <div class="publish-modal">
            <div class="modal-header">
              <h3>
                <i class="bi bi-pencil-square"></i>
                发布新帖子
              </h3>
              <button class="btn-close" @click="showPublishModal = false">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
            
            <div class="modal-body">
              <!-- 身份选择 -->
              <div class="form-group">
                <label>发布身份</label>
                <div class="role-select">
                  <button :class="['role-btn', { active: newPost.role === 'seeker' }]" 
                    @click="newPost.role = 'seeker'">
                    <i class="bi bi-mortarboard-fill"></i>
                    求职者
                  </button>
                  <button :class="['role-btn', { active: newPost.role === 'hr' }]" 
                    @click="newPost.role = 'hr'">
                    <i class="bi bi-briefcase-fill"></i>
                    HR/招聘
                  </button>
                </div>
              </div>
              
              <!-- 标题 -->
              <div class="form-group">
                <label>帖子标题</label>
                <input type="text" v-model="newPost.title" 
                  placeholder="请输入标题，让更多人看到你"
                  maxlength="50">
                <span class="char-count">{{ newPost.title.length }}/50</span>
              </div>
              
              <!-- 内容 -->
              <div class="form-group">
                <label>帖子内容</label>
                <textarea v-model="newPost.content"
                  placeholder="分享你的求职经验、招聘需求或职场心得..."
                  rows="6"
                  maxlength="1000"></textarea>
                <span class="char-count">{{ newPost.content.length }}/1000</span>
              </div>
              
              <!-- 地点 -->
              <div class="form-row">
                <div class="form-group half">
                  <label>地点（可选）</label>
                  <input type="text" v-model="newPost.location" placeholder="如：北京">
                </div>
                <div class="form-group half">
                  <label>薪资（可选）</label>
                  <input type="text" v-model="newPost.salary" placeholder="如：20-35K">
                </div>
              </div>
              
              <!-- 技能标签 -->
              <div class="form-group">
                <label>技能标签（最多5个）</label>
                <div class="tags-input">
                  <span v-for="(tag, index) in newPost.skills" :key="index" class="input-tag">
                    {{ tag }}
                    <i class="bi bi-x" @click="removeTag(index)"></i>
                  </span>
                  <input v-if="newPost.skills.length < 5"
                    type="text" 
                    v-model="tagInput"
                    placeholder="输入后按回车添加"
                    @keydown.enter.prevent="addTag">
                </div>
              </div>
            </div>
            
            <div class="modal-footer">
              <button class="btn-cancel" @click="showPublishModal = false">取消</button>
              <button class="btn-submit" @click="submitPost" :disabled="!canSubmit">
                <i class="bi bi-send"></i>
                发布帖子
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 帖子详情弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDetailModal" class="modal-overlay" @click.self="showDetailModal = false">
          <div class="detail-modal">
            <div class="modal-header">
              <div class="detail-user">
                <div class="detail-avatar" :style="{ background: selectedPost?.avatarColor }">
                  {{ selectedPost?.avatarText }}
                </div>
                <div class="detail-user-info">
                  <span class="user-name">{{ selectedPost?.userName }}</span>
                  <span :class="['user-role', selectedPost?.role]">
                    {{ selectedPost?.role === 'seeker' ? '求职' : '招聘' }}
                  </span>
                  <span class="post-time">{{ selectedPost?.timeAgo }}</span>
                </div>
              </div>
              <button class="btn-close" @click="showDetailModal = false">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
            
            <div class="modal-body detail-body">
              <h2 class="detail-title">{{ selectedPost?.title }}</h2>
              <p class="detail-content">{{ selectedPost?.fullContent || selectedPost?.content }}</p>
              
              <div class="detail-tags" v-if="selectedPost">
                <span v-if="selectedPost.location" class="tag location">
                  <i class="bi bi-geo-alt"></i>
                  {{ selectedPost.location }}
                </span>
                <span v-if="selectedPost.salary" class="tag salary">
                  <i class="bi bi-currency-yen"></i>
                  {{ selectedPost.salary }}
                </span>
                <span v-for="tag in selectedPost.skills" :key="tag" class="tag skill">{{ tag }}</span>
              </div>
              
              <div class="detail-actions">
                <button class="action-btn" :class="{ active: selectedPost?.liked }" @click="toggleLike(selectedPost)">
                  <i :class="selectedPost?.liked ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
                  {{ selectedPost?.likes }} 点赞
                </button>
                <button class="action-btn">
                  <i class="bi bi-bookmark"></i>
                  收藏
                </button>
                <button class="action-btn">
                  <i class="bi bi-share"></i>
                  分享
                </button>
              </div>
              
              <!-- 评论区 -->
              <div class="comments-section">
                <h4>评论 ({{ selectedPost?.comments }})</h4>
                <div class="comment-input">
                  <input type="text" v-model="commentText" placeholder="发表你的看法...">
                  <button class="btn-comment" @click="submitComment">发送</button>
                </div>
                <div class="comments-list">
                  <div v-for="comment in postComments" :key="comment.id" class="comment-item">
                    <div class="comment-avatar" :style="{ background: comment.avatarColor }">
                      {{ comment.avatarText }}
                    </div>
                    <div class="comment-content">
                      <div class="comment-header">
                        <span class="comment-name">{{ comment.userName }}</span>
                        <span class="comment-time">{{ comment.timeAgo }}</span>
                      </div>
                      <p class="comment-text">{{ comment.content }}</p>
                      <div class="comment-actions">
                        <button @click="likeComment(comment)">
                          <i :class="comment.liked ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
                          {{ comment.likes }}
                        </button>
                        <button>
                          <i class="bi bi-reply"></i>
                          回复
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="showToast" class="toast" :class="toastType">
        <i :class="toastIcon"></i>
        {{ toastMessage }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

// 状态
const activeFilter = ref('latest')
const showPublishModal = ref(false)
const showDetailModal = ref(false)
const selectedPost = ref(null)
const loading = ref(false)
const hasMore = ref(true)
const tagInput = ref('')
const commentText = ref('')

// Toast
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')
const toastIcon = computed(() => {
  return toastType.value === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'
})

// 统计
const totalPosts = ref(156)
const onlineUsers = ref(127)

// 筛选标签
const filterTabs = [
  { label: '最新', value: 'latest' },
  { label: '热门', value: 'hot' },
  { label: '求职', value: 'seeker' },
  { label: '招聘', value: 'hr' },
]

// 新帖子
const newPost = reactive({
  role: 'seeker',
  title: '',
  content: '',
  location: '',
  salary: '',
  skills: []
})

const canSubmit = computed(() => newPost.title.trim() && newPost.content.trim())

// 我的资料
const myProfile = reactive({
  name: '张三',
  avatarText: '张',
  avatarColor: '#8b5cf6',
  role: 'seeker',
  posts: 12,
  likes: 234,
  followers: 56
})

// 帖子数据
const posts = ref([
  {
    id: 1,
    userName: '李明',
    avatarText: '李',
    avatarColor: '#f59e0b',
    role: 'seeker',
    pinned: true,
    hot: false,
    online: true,
    title: '3年Java后端寻求后端开发/架构师岗位',
    content: '本人985计算机硕士，3年Java后端开发经验。⚡ 核心技术栈：熟悉 Spring Cloud 微服务架构、精通 MySQL、Redis 性能优化 • 有大规模分布式系统实战经验 ⚡ 项目经验：主导过电商平台交...',
    fullContent: `本人985计算机硕士，3年Java后端开发经验。

⚡ 核心技术栈：
• 熟悉 Spring Cloud 微服务架构
• 精通 MySQL、Redis 性能优化
• 有大规模分布式系统实战经验

⚡ 项目经验：
• 主导过电商平台交易系统重构，QPS提升300%
• 负责用户中心服务，服务千万级用户

期望城市：北京、上海、杭州
期望薪资：25-35K

欢迎HR私信交流！`,
    location: '北京',
    salary: null,
    skills: ['Java', 'Spring', 'MySQL'],
    likes: 89,
    comments: 23,
    timeAgo: '2小时前',
    liked: false
  },
  {
    id: 2,
    userName: '字节跳动 HR',
    avatarText: '字',
    avatarColor: '#4f46e5',
    role: 'hr',
    pinned: true,
    hot: true,
    online: true,
    title: '急招！高级前端工程师 30-60K·16薪',
    content: '【职位描述】我们是字节跳动商业化产品技术团队，负责抖音/头条的商业变现系统。⚡ 岗位职责：负责广告投放平台的架构设计与开发 • 推动前端工程化、组件化建设 • 解决复杂技术问题，提升团队...',
    fullContent: `【职位描述】
我们是字节跳动商业化产品技术团队，负责抖音/头条的商业变现系统。

⚡ 岗位职责：
• 负责广告投放平台的架构设计与开发
• 推动前端工程化、组件化建设
• 解决复杂技术问题，提升团队技术能力

⚡ 任职要求：
• 5年以上前端开发经验
• 精通 Vue/React，有大型项目经验
• 熟悉前端工程化、性能优化

⚡ 我们提供：
• 有竞争力的薪资 30-60K·16薪
• 弹性工作制
• 丰厚的餐补、交通补贴

坐标：北京-海淀区
欢迎投递简历或私信咨询！`,
    location: '北京',
    salary: '30-60K·16薪',
    skills: ['React', 'Vue', 'TypeScript'],
    likes: 156,
    comments: 45,
    timeAgo: '1小时前',
    liked: true
  },
  {
    id: 3,
    userName: '王芳',
    avatarText: '王',
    avatarColor: '#10b981',
    role: 'seeker',
    pinned: false,
    hot: true,
    online: false,
    title: '5年产品经理，寻求产品总监/高级PM',
    content: '大家好，我是王芳，5年互联网产品经验。⚡ 个人亮点：从0到1搭建过3款产品，累计用户超500万 • 擅长用户增长策略，曾主导项目增长200% • 跨部门协调能力强，推动多个重大项目落地 ⚡ 成功...',
    location: '上海',
    salary: null,
    skills: ['产品规划', '用户增长', '数据分析'],
    likes: 234,
    comments: 67,
    timeAgo: '3小时前',
    liked: false
  },
  {
    id: 4,
    userName: '腾讯云团队',
    avatarText: '腾',
    avatarColor: '#06b6d4',
    role: 'hr',
    pinned: false,
    hot: false,
    online: true,
    title: '【深圳】云原生架构师 40-80K',
    content: '腾讯云正在寻找优秀的云原生架构师加入我们！负责腾讯云容器服务（TKE）的架构设计和技术演进，打造行业领先的云原生平台...',
    location: '深圳',
    salary: '40-80K',
    skills: ['Kubernetes', 'Docker', 'Go'],
    likes: 178,
    comments: 32,
    timeAgo: '5小时前',
    liked: false
  },
  {
    id: 5,
    userName: '小红',
    avatarText: '小',
    avatarColor: '#ec4899',
    role: 'seeker',
    pinned: false,
    hot: false,
    online: true,
    title: '应届生求职：数据分析/算法方向',
    content: '2024届应届硕士，人工智能专业。在校期间参与过多个机器学习项目，熟悉Python数据分析全栈，有实习经验。希望找一份数据分析或算法工程师的工作...',
    location: '杭州',
    salary: null,
    skills: ['Python', '机器学习', 'SQL'],
    likes: 45,
    comments: 12,
    timeAgo: '1天前',
    liked: false
  }
])

// 评论数据
const postComments = ref([
  { id: 1, userName: '用户A', avatarText: 'A', avatarColor: '#8b5cf6', content: '这个职位很感兴趣，已投递！', likes: 12, timeAgo: '30分钟前', liked: false },
  { id: 2, userName: '用户B', avatarText: 'B', avatarColor: '#f59e0b', content: '请问有Python相关的岗位吗？', likes: 5, timeAgo: '1小时前', liked: true },
])

// 热门话题
const hotTopics = [
  { name: '#春招经验分享', count: 1234 },
  { name: '#大厂面经', count: 892 },
  { name: '#转行程序员', count: 756 },
  { name: '#薪资谈判技巧', count: 543 },
  { name: '#远程办公', count: 421 }
]

// 活跃用户
const activeUsers = ref([
  { id: 1, name: '面试官老王', avatarText: '王', avatarColor: '#4f46e5', desc: '10年HR经验', following: false },
  { id: 2, name: '程序员小李', avatarText: '李', avatarColor: '#10b981', desc: '阿里P7', following: true },
  { id: 3, name: '产品张姐', avatarText: '张', avatarColor: '#f59e0b', desc: '美团产品总监', following: false },
])

// 过滤帖子
const filteredPosts = computed(() => {
  let result = [...posts.value]
  
  if (activeFilter.value === 'hot') {
    result = result.filter(p => p.hot || p.likes > 100)
  } else if (activeFilter.value === 'seeker') {
    result = result.filter(p => p.role === 'seeker')
  } else if (activeFilter.value === 'hr') {
    result = result.filter(p => p.role === 'hr')
  }
  
  // 置顶排前面
  result.sort((a, b) => {
    if (a.pinned && !b.pinned) return -1
    if (!a.pinned && b.pinned) return 1
    return 0
  })
  
  return result
})

// 点赞
function toggleLike(post) {
  if (!post) return
  post.liked = !post.liked
  post.likes += post.liked ? 1 : -1
  showToastMessage(post.liked ? '已点赞' : '已取消点赞', 'success')
}

// 打开详情
function openPostDetail(post) {
  selectedPost.value = post
  showDetailModal.value = true
}

// 加载更多
function loadMore() {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    hasMore.value = false
  }, 1000)
}

// 添加标签
function addTag() {
  const tag = tagInput.value.trim()
  if (tag && newPost.skills.length < 5 && !newPost.skills.includes(tag)) {
    newPost.skills.push(tag)
  }
  tagInput.value = ''
}

function removeTag(index) {
  newPost.skills.splice(index, 1)
}

// 发布帖子
function submitPost() {
  if (!canSubmit.value) return
  
  const post = {
    id: Date.now(),
    userName: myProfile.name,
    avatarText: myProfile.avatarText,
    avatarColor: myProfile.avatarColor,
    role: newPost.role,
    pinned: false,
    hot: false,
    online: true,
    title: newPost.title,
    content: newPost.content.slice(0, 150) + '...',
    fullContent: newPost.content,
    location: newPost.location || null,
    salary: newPost.salary || null,
    skills: [...newPost.skills],
    likes: 0,
    comments: 0,
    timeAgo: '刚刚',
    liked: false
  }
  
  posts.value.unshift(post)
  totalPosts.value++
  
  // 重置表单
  newPost.title = ''
  newPost.content = ''
  newPost.location = ''
  newPost.salary = ''
  newPost.skills = []
  
  showPublishModal.value = false
  showToastMessage('帖子发布成功！', 'success')
}

// 发表评论
function submitComment() {
  if (!commentText.value.trim() || !selectedPost.value) return
  
  postComments.value.unshift({
    id: Date.now(),
    userName: myProfile.name,
    avatarText: myProfile.avatarText,
    avatarColor: myProfile.avatarColor,
    content: commentText.value,
    likes: 0,
    timeAgo: '刚刚',
    liked: false
  })
  
  selectedPost.value.comments++
  commentText.value = ''
  showToastMessage('评论成功', 'success')
}

// 评论点赞
function likeComment(comment) {
  comment.liked = !comment.liked
  comment.likes += comment.liked ? 1 : -1
}

// 关注
function toggleFollow(user) {
  user.following = !user.following
  showToastMessage(user.following ? '关注成功' : '已取消关注', 'success')
}

// 搜索话题
function searchTopic(topic) {
  showToastMessage(`搜索话题：${topic}`, 'success')
}

// 排名样式
function getRankClass(index) {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return ''
}

// Toast
function showToastMessage(message, type = 'success') {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => showToast.value = false, 2000)
}
</script>

<style scoped>
.forum-page {
  min-height: 100vh;
  padding: 24px;
  position: relative;
}

/* 背景 */
.page-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-gradient {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
}

.bg-gradient.left {
  left: -200px;
  top: -100px;
  background: var(--forum-glow-left, #8b5cf6);
}

.bg-gradient.right {
  right: -200px;
  bottom: -100px;
  background: var(--forum-glow-right, #06b6d4);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* 头部 */
.forum-header {
  max-width: 1200px;
  margin: 0 auto 24px;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.page-title i {
  font-size: 32px;
  color: #8b5cf6;
}

.page-desc {
  font-size: 15px;
  color: var(--color-brand-muted, #64748b);
}

.btn-publish {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}

.btn-publish:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
}

.stats-info {
  display: flex;
  gap: 24px;
}

.stats-info .stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

.stats-info .stat i {
  font-size: 16px;
}

.stats-info .stat strong {
  color: var(--color-brand-text, #e2e8f0);
}

.stats-info .stat.online {
  color: #10b981;
}

.online-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.filter-tabs {
  display: flex;
  gap: 6px;
}

.filter-tab {
  padding: 8px 18px;
  background: transparent;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  color: var(--color-brand-text, #e2e8f0);
  background: rgba(139, 92, 246, 0.1);
}

.filter-tab.active {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
}

/* 内容区 */
.forum-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

@media (max-width: 1024px) {
  .forum-content { grid-template-columns: 1fr; }
  .sidebar { display: none; }
}

/* 帖子列表 */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 18px;
  padding: 22px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateX(4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.post-card.pinned {
  border-color: rgba(139, 92, 246, 0.25);
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), transparent);
}

.post-avatar {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
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
  background: #10b981;
  border: 3px solid var(--color-brand-card, #1a1a2e);
  border-radius: 50%;
}

.post-body {
  min-width: 0;
}

.post-user {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.user-role {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.user-role.seeker {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.user-role.hr {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.user-role i {
  font-size: 10px;
}

.post-user .tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.tag.pinned {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.tag.hot {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.post-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 10px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-content {
  font-size: 14px;
  color: var(--color-brand-muted, #94a3b8);
  line-height: 1.7;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.post-tags .tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 8px;
  font-size: 12px;
  color: var(--color-brand-muted, #94a3b8);
}

.post-tags .tag.location {
  color: #f59e0b;
}

.post-tags .tag.salary {
  color: #10b981;
  font-weight: 600;
}

.post-tags .tag.skill {
  color: #a78bfa;
}

.post-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  min-width: 70px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 8px;
  border-radius: 10px;
  transition: all 0.2s;
}

.stat-item:hover {
  background: rgba(139, 92, 246, 0.1);
}

.stat-item i {
  font-size: 18px;
  color: var(--color-brand-muted, #64748b);
}

.stat-item.likes:hover i,
.stat-item.likes .bi-heart-fill {
  color: #f43f5e;
}

.stat-item span:first-of-type {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.stat-item .label {
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

.stat-time {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 加载更多 */
.load-more {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.btn-load {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  font-size: 14px;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-load:hover:not(:disabled) {
  background: rgba(139, 92, 246, 0.2);
}

.btn-load:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-load i.loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state i {
  font-size: 64px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 20px;
}

.btn-publish-sm {
  padding: 10px 20px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: white;
  cursor: pointer;
}

/* TransitionGroup */
.post-enter-active,
.post-leave-active {
  transition: all 0.4s ease;
}

.post-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.post-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 侧边栏 */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  padding: 20px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 16px;
}

.card-title i {
  color: #f59e0b;
}

/* 我的资料卡片 */
.profile-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}

.my-avatar {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: white;
}

.my-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.my-role {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 12px;
}

.my-role.seeker {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.my-role.hr {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 14px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.profile-stat {
  text-align: center;
}

.profile-stat strong {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.profile-stat span {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 热门话题 */
.topic-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.topic-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.topic-item:hover {
  background: rgba(139, 92, 246, 0.1);
}

.topic-rank {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  background: rgba(139, 92, 246, 0.1);
  color: var(--color-brand-muted, #64748b);
}

.topic-rank.gold {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.topic-rank.silver {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: white;
}

.topic-rank.bronze {
  background: linear-gradient(135deg, #f97316, #ea580c);
  color: white;
}

.topic-name {
  flex: 1;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.topic-count {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

/* 活跃用户 */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.user-item .user-info {
  flex: 1;
  min-width: 0;
}

.user-item .user-name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 2px;
}

.user-desc {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.btn-follow {
  padding: 6px 14px;
  background: rgba(139, 92, 246, 0.15);
  border: none;
  border-radius: 8px;
  font-size: 12px;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-follow:hover {
  background: rgba(139, 92, 246, 0.25);
}

.btn-follow.following {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: var(--color-brand-muted, #64748b);
}

/* 弹窗遮罩 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

/* 发帖弹窗 */
.publish-modal {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.modal-header h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.modal-header h3 i {
  color: #8b5cf6;
}

.btn-close {
  padding: 8px;
  background: transparent;
  border: none;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  transition: all 0.2s;
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.08);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--color-brand-muted, #64748b);
}

.char-count {
  position: absolute;
  right: 12px;
  bottom: 12px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-group.half {
  flex: 1;
}

.role-select {
  display: flex;
  gap: 12px;
}

.role-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
}

.role-btn:hover {
  border-color: rgba(139, 92, 246, 0.3);
}

.role-btn.active {
  background: rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
  color: #a78bfa;
}

.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 12px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  min-height: 48px;
}

.input-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(139, 92, 246, 0.15);
  border-radius: 8px;
  font-size: 13px;
  color: #a78bfa;
}

.input-tag i {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.input-tag i:hover {
  opacity: 1;
}

.tags-input input {
  flex: 1;
  min-width: 100px;
  padding: 4px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.btn-cancel {
  padding: 12px 24px;
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  border-color: rgba(139, 92, 246, 0.4);
  color: var(--color-brand-text, #e2e8f0);
}

.btn-submit {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 详情弹窗 */
.detail-modal {
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.detail-user {
  display: flex;
  align-items: center;
  gap: 14px;
}

.detail-avatar {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.detail-user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-user-info .user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.detail-user-info .post-time {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.detail-body {
  padding: 0 24px 24px;
}

.detail-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 16px;
  line-height: 1.5;
}

.detail-content {
  font-size: 15px;
  color: var(--color-brand-muted, #94a3b8);
  line-height: 1.8;
  margin-bottom: 20px;
  white-space: pre-wrap;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.detail-tags .tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 10px;
  font-size: 13px;
}

.detail-actions {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: rgba(139, 92, 246, 0.1);
  border: none;
  border-radius: 10px;
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  color: var(--color-brand-text, #e2e8f0);
}

.action-btn.active {
  color: #f43f5e;
}

.action-btn.active i {
  color: #f43f5e;
}

/* 评论区 */
.comments-section {
  margin-top: 20px;
}

.comments-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 16px;
}

.comment-input {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.comment-input input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
}

.comment-input input:focus {
  outline: none;
  border-color: #8b5cf6;
}

.btn-comment {
  padding: 12px 20px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-comment:hover {
  transform: translateY(-2px);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 300px;
  overflow-y: auto;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.comment-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
}

.comment-time {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.comment-text {
  font-size: 14px;
  color: var(--color-brand-muted, #94a3b8);
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-actions {
  display: flex;
  gap: 16px;
}

.comment-actions button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: transparent;
  border: none;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.comment-actions button:hover {
  background: rgba(139, 92, 246, 0.1);
  color: var(--color-brand-text, #e2e8f0);
}

.comment-actions button .bi-heart-fill {
  color: #f43f5e;
}

/* 弹窗动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .publish-modal,
.modal-enter-from .detail-modal,
.modal-leave-to .publish-modal,
.modal-leave-to .detail-modal {
  transform: translateY(20px) scale(0.95);
}

/* Toast */
.toast {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 14px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  z-index: 1100;
}

.toast.success i {
  color: #10b981;
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

/* ===== Light Mode Overrides ===== */
:global(html.light) .forum-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1 {
  background: #0891b2;
  opacity: 0.05;
}

:global(html.light) .glow-2 {
  background: #06b6d4;
  opacity: 0.04;
}

:global(html.light) .forum-header h1 {
  color: #0c4a6e;
}

:global(html.light) .forum-header p {
  color: #64748b;
}

:global(html.light) .header-stats {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .stat-item .stat-value {
  color: #0891b2;
}

:global(html.light) .stat-item .stat-label {
  color: #64748b;
}

:global(html.light) .section-title h2 {
  color: #0c4a6e;
}

:global(html.light) .category-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .category-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 8px 24px rgba(8, 145, 178, 0.1);
}

:global(html.light) .category-icon {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .category-name {
  color: #0c4a6e;
}

:global(html.light) .category-meta {
  color: #64748b;
}

:global(html.light) .tabs-bar {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .tab-btn {
  color: #64748b;
}

:global(html.light) .tab-btn.active {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .filter-bar {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .search-box {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .search-box input {
  color: #0c4a6e;
}

:global(html.light) .filter-select {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .btn-create {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .post-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .post-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .avatar-circle {
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .author-name {
  color: #0c4a6e;
}

:global(html.light) .post-time {
  color: #64748b;
}

:global(html.light) .post-title {
  color: #0c4a6e;
}

:global(html.light) .post-content {
  color: #475569;
}

:global(html.light) .post-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .stat-btn {
  color: #64748b;
}

:global(html.light) .stat-btn:hover {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .stat-btn.liked {
  color: #dc2626;
}

:global(html.light) .pinned-badge {
  background: rgba(234, 179, 8, 0.15);
  color: #ca8a04;
}

:global(html.light) .hot-badge {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
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

:global(html.light) .btn-submit {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .detail-modal .modal-content {
  background: #ffffff;
}

:global(html.light) .detail-header {
  background: rgba(8, 145, 178, 0.03);
  border-bottom-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .detail-title {
  color: #0c4a6e;
}

:global(html.light) .detail-body {
  color: #475569;
}

:global(html.light) .reply-item {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.08);
}

:global(html.light) .reply-content {
  color: #475569;
}

:global(html.light) .reply-input-area textarea {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
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

:global(html.light) .toast {
  background: #ffffff;
  border-color: rgba(16, 185, 129, 0.3);
  color: #0c4a6e;
  box-shadow: 0 10px 40px rgba(8, 145, 178, 0.15);
}
</style>
