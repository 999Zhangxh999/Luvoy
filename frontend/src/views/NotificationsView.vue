<template>
  <div class="min-h-screen bg-brand-bg py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- 页面头部 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text">通知中心</h1>
          <p class="text-sm text-brand-muted mt-1">查看所有系统通知和消息提醒</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="markAllRead" 
            class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all">
            <i class="bi bi-check2-all"></i>
            全部已读
          </button>
          <button @click="$router.back()" 
            class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all">
            <i class="bi bi-arrow-left"></i>
            返回
          </button>
        </div>
      </div>

      <!-- 筛选标签 -->
      <div class="flex items-center gap-2 mb-6 overflow-x-auto pb-2">
        <button v-for="filter in filters" :key="filter.key"
          @click="activeFilter = filter.key"
          class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all"
          :class="activeFilter === filter.key 
            ? 'bg-cyan-500 dark:bg-violet-500 text-white' 
            : 'bg-brand-card border border-brand-border text-brand-muted hover:text-brand-text hover:border-cyan-500/50 dark:hover:border-violet-500/50'">
          <i :class="filter.icon"></i>
          {{ filter.label }}
          <span v-if="filter.count" class="px-1.5 py-0.5 rounded-full text-xs"
            :class="activeFilter === filter.key ? 'bg-white/20' : 'bg-brand-surface'">
            {{ filter.count }}
          </span>
        </button>
      </div>

      <!-- 通知列表 -->
      <div class="space-y-3">
        <TransitionGroup name="list">
          <div v-for="notif in filteredNotifications" :key="notif.id"
            class="bg-brand-card border rounded-2xl overflow-hidden transition-all hover:shadow-lg cursor-pointer group"
            :class="notif.read ? 'border-brand-border' : 'border-cyan-500/30 dark:border-violet-500/30 bg-cyan-500/5 dark:bg-violet-500/5'"
            @click="handleNotificationClick(notif)">
            <div class="flex gap-4 p-5">
              <!-- 通知图标 -->
              <div class="w-12 h-12 rounded-xl flex-shrink-0 flex items-center justify-center"
                :class="notif.bgClass">
                <i :class="[notif.icon, 'text-xl', notif.iconClass]"></i>
              </div>
              
              <!-- 通知内容 -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <h3 class="text-sm font-semibold text-brand-text group-hover:text-cyan-600 dark:group-hover:text-violet-400 transition-colors">
                      {{ notif.title }}
                    </h3>
                    <p class="text-sm text-brand-muted mt-1 line-clamp-2">{{ notif.content }}</p>
                  </div>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <span v-if="!notif.read" class="w-2 h-2 rounded-full bg-cyan-500 dark:bg-violet-500 animate-pulse"></span>
                    <span class="text-xs text-brand-muted">{{ notif.time }}</span>
                  </div>
                </div>
                
                <!-- 操作按钮 -->
                <div v-if="notif.actions" class="flex items-center gap-2 mt-3">
                  <button v-for="action in notif.actions" :key="action.label"
                    @click.stop="handleAction(notif, action)"
                    class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                    :class="action.primary 
                      ? 'bg-cyan-500 dark:bg-violet-500 text-white hover:bg-cyan-600 dark:hover:bg-violet-600' 
                      : 'bg-brand-surface text-brand-muted hover:text-brand-text'">
                    <i v-if="action.icon" :class="[action.icon, 'mr-1']"></i>
                    {{ action.label }}
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 关联内容预览 -->
            <div v-if="notif.preview" class="px-5 pb-4">
              <div class="p-3 rounded-xl bg-brand-surface flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-teal-500/20 dark:from-violet-500/20 dark:to-indigo-500/20 flex items-center justify-center text-cyan-600 dark:text-violet-400 font-bold text-sm">
                  {{ notif.preview.company?.charAt(0) || 'J' }}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-brand-text truncate">{{ notif.preview.title }}</p>
                  <p class="text-xs text-brand-muted">{{ notif.preview.company }} · {{ notif.preview.location }}</p>
                </div>
                <span class="text-xs font-medium text-cyan-600 dark:text-violet-400">{{ notif.preview.salary }}</span>
              </div>
            </div>
          </div>
        </TransitionGroup>
        
        <!-- 空状态 -->
        <div v-if="filteredNotifications.length === 0" class="py-16 text-center">
          <div class="w-20 h-20 mx-auto rounded-2xl bg-brand-surface flex items-center justify-center mb-4">
            <i class="bi bi-bell-slash text-3xl text-brand-muted"></i>
          </div>
          <h3 class="text-lg font-semibold text-brand-text mb-2">暂无通知</h3>
          <p class="text-sm text-brand-muted">当前分类下没有通知消息</p>
        </div>
      </div>
      
      <!-- 加载更多 -->
      <div v-if="filteredNotifications.length > 0" class="mt-8 text-center">
        <button class="px-6 py-2.5 rounded-xl border border-brand-border text-sm text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all">
          加载更多
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeFilter = ref('all')

const filters = [
  { key: 'all', label: '全部', icon: 'bi bi-inbox', count: 12 },
  { key: 'unread', label: '未读', icon: 'bi bi-circle-fill', count: 5 },
  { key: 'job', label: '职位相关', icon: 'bi bi-briefcase', count: 6 },
  { key: 'interview', label: '面试邀请', icon: 'bi bi-calendar-event', count: 3 },
  { key: 'system', label: '系统通知', icon: 'bi bi-gear', count: 3 },
]

const notifications = ref([
  {
    id: 1,
    type: 'job',
    title: '您投递的职位有新回复',
    content: '字节跳动HR已查看您的简历，对您的经历非常感兴趣，希望进一步了解。',
    time: '10分钟前',
    read: false,
    icon: 'bi bi-envelope-open',
    bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10',
    iconClass: 'text-cyan-600 dark:text-violet-400',
    actions: [
      { label: '查看详情', primary: true, action: 'view' },
      { label: '发送消息', icon: 'bi bi-chat', action: 'message' },
    ],
    preview: {
      title: '前端开发工程师',
      company: '字节跳动',
      location: '北京',
      salary: '25-40K'
    }
  },
  {
    id: 2,
    type: 'interview',
    title: '收到面试邀请',
    content: '腾讯科技邀请您参加产品经理岗位的视频面试，面试时间：明天下午2:00。',
    time: '2小时前',
    read: false,
    icon: 'bi bi-calendar-check',
    bgClass: 'bg-emerald-500/10',
    iconClass: 'text-emerald-600',
    actions: [
      { label: '接受邀请', primary: true, action: 'accept' },
      { label: '协商时间', action: 'reschedule' },
      { label: '婉拒', action: 'decline' },
    ],
    preview: {
      title: '产品经理',
      company: '腾讯科技',
      location: '深圳',
      salary: '30-50K'
    }
  },
  {
    id: 3,
    type: 'system',
    title: '技能评估已完成',
    content: '您的Python技能评估结果已出炉，得分85/100，已自动更新到您的个人档案。',
    time: '昨天',
    read: false,
    icon: 'bi bi-award',
    bgClass: 'bg-amber-500/10',
    iconClass: 'text-amber-600',
    actions: [
      { label: '查看报告', primary: true, action: 'view' },
    ]
  },
  {
    id: 4,
    type: 'job',
    title: '您的简历被收藏',
    content: '阿里巴巴招聘负责人收藏了您的简历，您的档案曝光度提升了。',
    time: '2天前',
    read: true,
    icon: 'bi bi-heart-fill',
    bgClass: 'bg-rose-500/10',
    iconClass: 'text-rose-500'
  },
  {
    id: 5,
    type: 'system',
    title: '职业规划报告已生成',
    content: '根据您的最新画像数据，系统已为您生成Q4职业规划建议报告，请查阅。',
    time: '3天前',
    read: true,
    icon: 'bi bi-file-earmark-text',
    bgClass: 'bg-indigo-500/10',
    iconClass: 'text-indigo-600',
    actions: [
      { label: '查看报告', primary: true, action: 'view' },
    ]
  },
  {
    id: 6,
    type: 'interview',
    title: '面试结果通知',
    content: '恭喜！您在美团的前端工程师面试已通过，请等待下一轮面试通知。',
    time: '4天前',
    read: true,
    icon: 'bi bi-trophy',
    bgClass: 'bg-emerald-500/10',
    iconClass: 'text-emerald-600',
    preview: {
      title: '前端开发工程师',
      company: '美团',
      location: '北京',
      salary: '30-45K'
    }
  },
  {
    id: 7,
    type: 'job',
    title: '有新的匹配职位',
    content: '根据您的技能画像，系统为您匹配到5个高度契合的职位，快来看看吧！',
    time: '5天前',
    read: true,
    icon: 'bi bi-stars',
    bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10',
    iconClass: 'text-cyan-600 dark:text-violet-400',
    actions: [
      { label: '查看职位', primary: true, action: 'view' },
    ]
  },
  {
    id: 8,
    type: 'system',
    title: '档案完成度提醒',
    content: '您的个人档案完成度为75%，完善更多信息可提升职位匹配精准度。',
    time: '1周前',
    read: true,
    icon: 'bi bi-person-exclamation',
    bgClass: 'bg-amber-500/10',
    iconClass: 'text-amber-600',
    actions: [
      { label: '去完善', primary: true, action: 'complete' },
    ]
  },
])

const filteredNotifications = computed(() => {
  if (activeFilter.value === 'all') return notifications.value
  if (activeFilter.value === 'unread') return notifications.value.filter(n => !n.read)
  return notifications.value.filter(n => n.type === activeFilter.value)
})

function markAllRead() {
  notifications.value.forEach(n => n.read = true)
}

function handleNotificationClick(notif) {
  notif.read = true
  // 根据通知类型跳转到对应页面
  if (notif.type === 'job') {
    router.push('/my-applications')
  } else if (notif.type === 'interview') {
    router.push('/my-applications')
  } else if (notif.type === 'system') {
    // 系统通知可能跳转到不同页面
  }
}

function handleAction(notif, action) {
  notif.read = true
  switch (action.action) {
    case 'view':
      router.push('/my-applications')
      break
    case 'message':
      router.push('/messages')
      break
    case 'accept':
      alert('已接受面试邀请')
      break
    case 'reschedule':
      alert('请在消息中与HR协商时间')
      router.push('/messages')
      break
    case 'decline':
      alert('已婉拒此次面试')
      break
    case 'complete':
      router.push('/my-profile')
      break
  }
}
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
