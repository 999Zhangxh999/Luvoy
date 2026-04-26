<template>
  <div class="min-h-screen bg-brand-bg py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <!-- 页面头部 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text">个人中心</h1>
          <p class="text-sm text-brand-muted mt-1">管理您的账户、画像和求职活动</p>
        </div>
        <button @click="$router.back()" class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all">
          <i class="bi bi-arrow-left"></i>
          返回
        </button>
      </div>

      <!-- 主内容区 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧 - 用户信息卡片 -->
        <div class="lg:col-span-1 space-y-6">
          <!-- 个人信息卡片 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <!-- 封面背景 -->
            <div class="h-24 bg-gradient-to-br from-cyan-500 via-teal-500 to-emerald-500 dark:from-violet-600 dark:via-indigo-600 dark:to-purple-600 relative">
              <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgY3g9IjIwIiBjeT0iMjAiIHI9IjIiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPjwvZz48L3N2Zz4=')] opacity-50"></div>
              <button class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/20 backdrop-blur flex items-center justify-center text-white hover:bg-white/30 transition-all">
                <i class="bi bi-camera text-sm"></i>
              </button>
            </div>
            
            <!-- 头像和基本信息 -->
            <div class="px-6 pb-6">
              <div class="relative -mt-12 mb-4 group">
                <!-- 头像容器 -->
                <div class="relative w-24 h-24 cursor-pointer" @click="triggerAvatarUpload">
                  <div v-if="avatarUrl" class="w-24 h-24 rounded-2xl overflow-hidden shadow-xl border-4 border-brand-card">
                    <img :src="avatarUrl" alt="头像" class="w-full h-full object-cover" />
                  </div>
                  <div v-else class="w-24 h-24 rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-600 dark:from-violet-600 dark:to-indigo-700 flex items-center justify-center text-white text-3xl font-bold shadow-xl border-4 border-brand-card">
                    {{ userInitials }}
                  </div>
                  <!-- 悬浮蒙层 -->
                  <div class="absolute inset-0 rounded-2xl bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <div class="text-center text-white">
                      <i class="bi bi-camera text-xl"></i>
                      <p class="text-xs mt-1">更换头像</p>
                    </div>
                  </div>
                </div>
                <!-- 在线状态 -->
                <div class="absolute -bottom-1 -right-1 w-7 h-7 bg-green-500 rounded-lg border-2 border-brand-card flex items-center justify-center">
                  <i class="bi bi-check text-white text-sm"></i>
                </div>
                <!-- 隐藏的文件输入 -->
                <input type="file" ref="avatarInput" @change="handleAvatarChange" accept="image/*" class="hidden" />
              </div>
              
              <h2 class="text-xl font-bold text-brand-text">{{ userName }}</h2>
              <p class="text-sm text-brand-muted mt-1">{{ userEmail }}</p>
              
              <!-- 标签 -->
              <div class="flex flex-wrap gap-2 mt-4">
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-cyan-500/10 dark:bg-violet-500/10 text-cyan-600 dark:text-violet-400">
                  求职中
                </span>
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-brand-surface text-brand-muted">
                  应届生
                </span>
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-brand-surface text-brand-muted">
                  计算机专业
                </span>
              </div>
              
              <!-- 完成度进度 -->
              <div class="mt-6 p-4 rounded-xl bg-brand-surface">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-brand-text">档案完成度</span>
                  <span class="text-sm font-bold text-cyan-600 dark:text-violet-400">{{ completionPercent }}%</span>
                </div>
                <div class="h-2 bg-brand-card rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500 rounded-full transition-all duration-500"
                    :style="{ width: completionPercent + '%' }"></div>
                </div>
                <p class="text-xs text-brand-muted mt-2">
                  <i class="bi bi-info-circle mr-1"></i>
                  完善档案可提升匹配精准度
                </p>
              </div>
              
              <!-- 编辑资料按钮 -->
              <button @click="$router.push('/settings')" class="w-full mt-4 py-2.5 rounded-xl border border-brand-border text-sm font-medium text-brand-text hover:bg-brand-surface transition-all flex items-center justify-center gap-2">
                <i class="bi bi-pencil"></i>
                编辑资料
              </button>
            </div>
          </div>
          
          <!-- 快捷操作 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <h3 class="text-sm font-semibold text-brand-text mb-4">快捷操作</h3>
            <div class="grid grid-cols-2 gap-3">
              <button v-for="action in quickActions" :key="action.label"
                @click="$router.push(action.path)"
                class="p-3 rounded-xl bg-brand-surface hover:bg-brand-border/50 transition-all text-center group">
                <div class="w-10 h-10 mx-auto rounded-xl flex items-center justify-center mb-2 transition-all"
                  :class="action.bgClass">
                  <i :class="[action.icon, 'text-lg', action.iconClass]"></i>
                </div>
                <span class="text-xs font-medium text-brand-muted group-hover:text-brand-text transition-colors">{{ action.label }}</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 右侧 - 主内容区 -->
        <div class="lg:col-span-2 space-y-6">
          <!-- 数据统计卡片 -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div v-for="stat in stats" :key="stat.label"
              class="bg-brand-card border border-brand-border rounded-2xl p-4 hover:border-cyan-500/30 dark:hover:border-violet-500/30 transition-all cursor-pointer group"
              @click="$router.push(stat.path)">
              <div class="flex items-center justify-between mb-3">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center"
                  :class="stat.bgClass">
                  <i :class="[stat.icon, 'text-lg', stat.iconClass]"></i>
                </div>
                <i class="bi bi-arrow-right text-brand-muted opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all"></i>
              </div>
              <p class="text-2xl font-bold text-brand-text">{{ stat.value }}</p>
              <p class="text-xs text-brand-muted mt-1">{{ stat.label }}</p>
            </div>
          </div>
          
          <!-- 标签页切换 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <div class="flex border-b border-brand-border">
              <button v-for="tab in tabs" :key="tab.key"
                @click="activeTab = tab.key"
                class="flex-1 px-4 py-3.5 text-sm font-medium transition-all relative"
                :class="activeTab === tab.key ? 'text-brand-text' : 'text-brand-muted hover:text-brand-text'">
                <i :class="[tab.icon, 'mr-1.5']"></i>
                {{ tab.label }}
                <span v-if="tab.badge" class="ml-1.5 px-1.5 py-0.5 text-[10px] rounded-full"
                  :class="activeTab === tab.key ? 'bg-cyan-500 dark:bg-violet-500 text-white' : 'bg-brand-surface text-brand-muted'">
                  {{ tab.badge }}
                </span>
                <div v-if="activeTab === tab.key" class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500"></div>
              </button>
            </div>
            
            <!-- 最近动态内容 -->
            <div v-if="activeTab === 'activity'" class="p-5">
              <div class="space-y-4">
                <div v-for="(activity, index) in activities" :key="index"
                  class="flex gap-4 p-4 rounded-xl bg-brand-surface hover:bg-brand-border/30 transition-all cursor-pointer group">
                  <div class="w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center"
                    :class="activity.bgClass">
                    <i :class="[activity.icon, 'text-base', activity.iconClass]"></i>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-brand-text group-hover:text-cyan-600 dark:group-hover:text-violet-400 transition-colors">
                      {{ activity.title }}
                    </p>
                    <p class="text-xs text-brand-muted mt-1">{{ activity.desc }}</p>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <p class="text-xs text-brand-muted">{{ activity.time }}</p>
                    <span v-if="activity.status" class="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-medium"
                      :class="activity.statusClass">{{ activity.status }}</span>
                  </div>
                </div>
              </div>
              <button class="w-full mt-4 py-2.5 text-sm text-brand-muted hover:text-brand-text transition-colors flex items-center justify-center gap-1">
                查看更多动态
                <i class="bi bi-chevron-down"></i>
              </button>
            </div>
            
            <!-- 收藏职位内容 -->
            <div v-if="activeTab === 'favorites'" class="p-5">
              <div class="space-y-3">
                <div v-for="job in favoriteJobs" :key="job.id"
                  class="flex items-center gap-4 p-4 rounded-xl bg-brand-surface hover:bg-brand-border/30 transition-all cursor-pointer group">
                  <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500/20 to-teal-500/20 dark:from-violet-500/20 dark:to-indigo-500/20 flex items-center justify-center text-cyan-600 dark:text-violet-400 font-bold">
                    {{ job.company.charAt(0) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-brand-text group-hover:text-cyan-600 dark:group-hover:text-violet-400 transition-colors truncate">{{ job.title }}</p>
                    <p class="text-xs text-brand-muted mt-0.5">{{ job.company }} · {{ job.location }}</p>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <p class="text-sm font-semibold text-cyan-600 dark:text-violet-400">{{ job.salary }}</p>
                    <p class="text-xs text-brand-muted">{{ job.match }}% 匹配</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 技能标签内容 -->
            <div v-if="activeTab === 'skills'" class="p-5">
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in skills" :key="skill.name"
                  class="px-3 py-1.5 rounded-full text-sm font-medium transition-all cursor-pointer"
                  :class="skill.level === 'expert' ? 'bg-cyan-500/20 dark:bg-violet-500/20 text-cyan-600 dark:text-violet-400' : 
                         skill.level === 'proficient' ? 'bg-emerald-500/20 text-emerald-600' : 
                         'bg-brand-surface text-brand-muted hover:bg-brand-border/50'">
                  {{ skill.name }}
                  <i v-if="skill.level === 'expert'" class="bi bi-star-fill ml-1 text-xs"></i>
                </span>
              </div>
              <button @click="$router.push('/career/skills')" class="mt-6 w-full py-2.5 rounded-xl border border-dashed border-brand-border text-sm text-brand-muted hover:border-cyan-500/50 dark:hover:border-violet-500/50 hover:text-brand-text transition-all flex items-center justify-center gap-2">
                <i class="bi bi-plus-lg"></i>
                添加更多技能
              </button>
            </div>
          </div>
          
          <!-- 推荐职位 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-base font-semibold text-brand-text">
                <i class="bi bi-stars text-cyan-500 dark:text-violet-400 mr-2"></i>
                为你推荐
              </h3>
              <button @click="$router.push('/job-market')" class="text-sm text-brand-muted hover:text-brand-text transition-colors flex items-center gap-1">
                查看更多
                <i class="bi bi-chevron-right text-xs"></i>
              </button>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="rec in recommendations" :key="rec.id"
                class="p-4 rounded-xl bg-brand-surface hover:bg-brand-border/30 transition-all cursor-pointer group border border-transparent hover:border-cyan-500/20 dark:hover:border-violet-500/20">
                <div class="flex items-start gap-3">
                  <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-teal-500/20 dark:from-violet-500/20 dark:to-indigo-500/20 flex items-center justify-center text-cyan-600 dark:text-violet-400 font-bold text-sm flex-shrink-0">
                    {{ rec.company.charAt(0) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-brand-text group-hover:text-cyan-600 dark:group-hover:text-violet-400 transition-colors truncate">{{ rec.title }}</p>
                    <p class="text-xs text-brand-muted mt-0.5">{{ rec.company }}</p>
                    <div class="flex items-center gap-2 mt-2">
                      <span class="text-xs font-medium text-cyan-600 dark:text-violet-400">{{ rec.salary }}</span>
                      <span class="w-1 h-1 rounded-full bg-brand-muted"></span>
                      <span class="text-xs text-brand-muted">{{ rec.location }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center justify-between mt-3 pt-3 border-t border-brand-border">
                  <div class="flex items-center gap-1">
                    <div class="w-16 h-1.5 rounded-full bg-brand-card overflow-hidden">
                      <div class="h-full rounded-full"
                        :class="rec.match >= 80 ? 'bg-green-500' : rec.match >= 60 ? 'bg-cyan-500 dark:bg-violet-500' : 'bg-amber-500'"
                        :style="{ width: rec.match + '%' }"></div>
                    </div>
                    <span class="text-xs font-medium" :class="rec.match >= 80 ? 'text-green-500' : rec.match >= 60 ? 'text-cyan-600 dark:text-violet-400' : 'text-amber-500'">{{ rec.match }}%</span>
                  </div>
                  <button class="px-3 py-1 rounded-lg text-xs font-medium bg-cyan-500/10 dark:bg-violet-500/10 text-cyan-600 dark:text-violet-400 hover:bg-cyan-500/20 dark:hover:bg-violet-500/20 transition-all">
                    投递
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

const userName = computed(() => authStore.user?.username || '用户')
const userEmail = computed(() => authStore.user?.email || 'user@example.com')
const userInitials = computed(() => {
  const name = userName.value
  return name.slice(0, 2).toUpperCase()
})

// 头像相关
const avatarInput = ref(null)
const avatarUrl = ref(localStorage.getItem('user-avatar') || '')

function triggerAvatarUpload() {
  avatarInput.value?.click()
}

function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请上传图片文件')
      return
    }
    // 验证文件大小 (最大 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('图片大小不能超过 5MB')
      return
    }
    // 创建本地预览URL
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarUrl.value = e.target.result
      // 保存到localStorage
      localStorage.setItem('user-avatar', e.target.result)
      // 通知其他组件头像已更新
      window.dispatchEvent(new Event('avatar-updated'))
    }
    reader.readAsDataURL(file)
  }
}

const completionPercent = ref(75)
const activeTab = ref('activity')

const stats = [
  { label: '职位投递', value: 12, icon: 'bi bi-send', bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10', iconClass: 'text-cyan-600 dark:text-violet-400', path: '/my-applications' },
  { label: '面试邀请', value: 5, icon: 'bi bi-calendar-check', bgClass: 'bg-emerald-500/10', iconClass: 'text-emerald-600', path: '/my-applications' },
  { label: '收藏职位', value: 8, icon: 'bi bi-heart', bgClass: 'bg-rose-500/10', iconClass: 'text-rose-500', path: '/job-market' },
  { label: '浏览记录', value: 42, icon: 'bi bi-eye', bgClass: 'bg-amber-500/10', iconClass: 'text-amber-600', path: '/job-market' },
]

const tabs = [
  { key: 'activity', label: '最近动态', icon: 'bi bi-activity', badge: '5' },
  { key: 'favorites', label: '收藏职位', icon: 'bi bi-heart' },
  { key: 'skills', label: '技能标签', icon: 'bi bi-tags' },
]

const quickActions = [
  { label: '完善画像', icon: 'bi bi-person-plus', path: '/my-profile', bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10', iconClass: 'text-cyan-600 dark:text-violet-400' },
  { label: '发布简历', icon: 'bi bi-file-earmark-arrow-up', path: '/resume', bgClass: 'bg-emerald-500/10', iconClass: 'text-emerald-600' },
  { label: '浏览职位', icon: 'bi bi-briefcase', path: '/job-market', bgClass: 'bg-amber-500/10', iconClass: 'text-amber-600' },
  { label: '消息中心', icon: 'bi bi-chat-dots', path: '/messages', bgClass: 'bg-rose-500/10', iconClass: 'text-rose-500' },
]

const activities = [
  { 
    title: '您投递的「前端开发工程师」有新回复', 
    desc: '字节跳动 · HR已查看您的简历', 
    time: '10分钟前',
    icon: 'bi bi-envelope-open',
    bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10',
    iconClass: 'text-cyan-600 dark:text-violet-400',
    status: '待处理',
    statusClass: 'bg-amber-500/20 text-amber-600'
  },
  { 
    title: '收到面试邀请', 
    desc: '腾讯科技 · 产品经理岗位', 
    time: '2小时前',
    icon: 'bi bi-calendar-event',
    bgClass: 'bg-emerald-500/10',
    iconClass: 'text-emerald-600',
    status: '面试中',
    statusClass: 'bg-emerald-500/20 text-emerald-600'
  },
  { 
    title: '技能评估已完成', 
    desc: 'Python技能评估得分 85/100', 
    time: '昨天',
    icon: 'bi bi-award',
    bgClass: 'bg-amber-500/10',
    iconClass: 'text-amber-600'
  },
  { 
    title: '简历被收藏', 
    desc: '阿里巴巴HR收藏了您的简历', 
    time: '2天前',
    icon: 'bi bi-heart-fill',
    bgClass: 'bg-rose-500/10',
    iconClass: 'text-rose-500'
  },
  { 
    title: '职业规划报告生成', 
    desc: '您的Q4职业规划报告已生成', 
    time: '3天前',
    icon: 'bi bi-file-text',
    bgClass: 'bg-indigo-500/10',
    iconClass: 'text-indigo-600'
  },
]

const favoriteJobs = [
  { id: 1, title: '前端开发工程师', company: '字节跳动', location: '北京', salary: '25-40K', match: 92 },
  { id: 2, title: '全栈开发工程师', company: '腾讯科技', location: '深圳', salary: '30-50K', match: 85 },
  { id: 3, title: 'Vue.js开发', company: '阿里巴巴', location: '杭州', salary: '20-35K', match: 88 },
]

const skills = [
  { name: 'JavaScript', level: 'expert' },
  { name: 'Vue.js', level: 'expert' },
  { name: 'TypeScript', level: 'proficient' },
  { name: 'React', level: 'proficient' },
  { name: 'Node.js', level: 'proficient' },
  { name: 'Python', level: 'intermediate' },
  { name: 'SQL', level: 'intermediate' },
  { name: 'Git', level: 'proficient' },
  { name: 'Docker', level: 'intermediate' },
  { name: 'Linux', level: 'intermediate' },
]

const recommendations = [
  { id: 1, title: '高级前端开发', company: '美团', salary: '35-55K', location: '北京', match: 94 },
  { id: 2, title: 'Vue开发工程师', company: '小红书', salary: '25-40K', location: '上海', match: 89 },
  { id: 3, title: '前端技术专家', company: '拼多多', salary: '50-80K', location: '上海', match: 78 },
  { id: 4, title: 'Web开发工程师', company: '网易', salary: '20-35K', location: '杭州', match: 82 },
]
</script>

<style scoped>
/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
