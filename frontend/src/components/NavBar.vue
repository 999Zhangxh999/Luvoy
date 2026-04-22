<template>
  <header class="glass-nav sticky top-0 z-50 transition-all duration-300" :class="{ 'shadow-lg shadow-black/20 dark:shadow-black/20': scrolled }">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2.5 group flex-shrink-0">
          <img src="/luvoy-main-20260404.svg" alt="律途 Luvoy 标识" class="w-9 h-9 rounded-lg shadow-md group-hover:scale-110 transition-transform" />
          <span class="font-bold text-brand-text text-lg tracking-tight">律途 · Luvoy</span>
        </router-link>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center gap-1">
          <router-link v-for="item in navItems" :key="item.path" :to="item.path"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150"
            :class="isActive(item.path) ? 'text-brand-text' : 'text-brand-muted hover:text-brand-text'">
            {{ item.label }}
          </router-link>

        </nav>

        <!-- Right Actions -->
        <div class="flex items-center gap-3">
          <!-- 主题切换按钮 - 已禁用，仅保持黑夜模式 -->
          <!-- <button 
            @click="toggleTheme"
            class="w-9 h-9 flex items-center justify-center rounded-lg text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all"
            :title="themeStore.theme === 'dark' ? '切换到白天模式' : '切换到黑夜模式'"
          >
            <i :class="themeStore.theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars'" class="text-lg"></i>
          </button> -->
          <!-- 通知铃铛 -->
          <div class="relative hidden sm:block" @mouseenter="notifOpen = true" @mouseleave="notifOpen = false">
            <button class="w-9 h-9 flex items-center justify-center rounded-lg text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all relative">
              <i class="bi bi-bell text-lg"></i>
              <span v-if="unreadCount > 0" class="absolute -top-0.5 -right-0.5 w-4 h-4 bg-red-500 rounded-full text-[10px] text-white flex items-center justify-center animate-pulse">{{ unreadCount }}</span>
            </button>
            <transition name="dropdown">
              <div v-if="notifOpen" class="absolute top-full right-0 mt-2 w-80 bg-brand-card border border-brand-border rounded-2xl shadow-2xl overflow-hidden">
                <!-- 通知头部 -->
                <div class="flex items-center justify-between px-4 py-3 border-b border-brand-border">
                  <h3 class="text-sm font-semibold text-brand-text">通知中心</h3>
                  <button class="text-xs text-brand-muted hover:text-cyan-600 dark:hover:text-violet-400 transition-colors">全部已读</button>
                </div>
                <!-- 通知列表 -->
                <div class="max-h-80 overflow-y-auto">
                  <div v-for="notif in notifications" :key="notif.id"
                    class="flex gap-3 p-3 hover:bg-brand-surface transition-all cursor-pointer border-b border-brand-border/50 last:border-0"
                    :class="{ 'bg-cyan-500/5 dark:bg-violet-500/5': !notif.read }">
                    <div class="w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center"
                      :class="notif.bgClass">
                      <i :class="[notif.icon, notif.iconClass]"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm text-brand-text line-clamp-2">{{ notif.content }}</p>
                      <p class="text-xs text-brand-muted mt-1">{{ notif.time }}</p>
                    </div>
                    <div v-if="!notif.read" class="w-2 h-2 rounded-full bg-cyan-500 dark:bg-violet-500 flex-shrink-0 mt-1.5"></div>
                  </div>
                </div>
                <!-- 底部链接 -->
                <router-link to="/notifications" @click="notifOpen = false"
                  class="flex items-center justify-center gap-1 py-3 text-sm text-brand-muted hover:text-brand-text hover:bg-brand-surface transition-all border-t border-brand-border">
                  查看全部通知
                  <i class="bi bi-chevron-right text-xs"></i>
                </router-link>
              </div>
            </transition>
          </div>
          <!-- 用户头像 -->
          <div class="relative" @mouseenter="userOpen = true" @mouseleave="userOpen = false" @click.stop="userOpen = !userOpen">
            <button class="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-teal-600 dark:from-violet-600 dark:to-indigo-700 flex items-center justify-center text-white hover:scale-105 transition-transform ring-2 ring-transparent hover:ring-cyan-500/30 dark:hover:ring-violet-500/30 overflow-hidden">
              <img v-if="userAvatar" :src="userAvatar" alt="头像" class="w-full h-full object-cover" />
              <span v-else-if="authStore.isLoggedIn" class="text-xs font-semibold">{{ authStore.userInitials }}</span>
              <i v-else class="bi bi-person text-sm"></i>
            </button>
            <transition name="dropdown">
              <div v-if="userOpen"
                class="user-dropdown-panel absolute top-full right-0 mt-2 w-72 bg-brand-card border border-brand-border rounded-2xl shadow-2xl overflow-y-auto">
                <!-- 用户信息头部 -->
                <div v-if="authStore.isLoggedIn" class="p-4 bg-gradient-to-br from-cyan-500/10 to-teal-500/10 dark:from-violet-500/10 dark:to-indigo-500/10 border-b border-brand-border">
                  <div class="flex items-center gap-3">
                    <div class="relative">
                      <div class="w-14 h-14 rounded-full bg-gradient-to-br from-cyan-500 to-teal-600 dark:from-violet-600 dark:to-indigo-700 flex items-center justify-center text-white text-lg font-bold shadow-lg overflow-hidden">
                        <img v-if="userAvatar" :src="userAvatar" alt="头像" class="w-full h-full object-cover" />
                        <span v-else>{{ authStore.userInitials }}</span>
                      </div>
                      <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-brand-card flex items-center justify-center">
                        <i class="bi bi-check text-white text-xs"></i>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-base font-bold text-brand-text truncate">{{ authStore.user?.username }}</p>
                      <p class="text-xs text-brand-muted truncate mt-0.5">{{ authStore.user?.email }}</p>
                      <div class="flex items-center gap-2 mt-2">
                        <div class="flex-1 h-1.5 bg-brand-surface rounded-full overflow-hidden">
                          <div class="h-full bg-gradient-to-r from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500 rounded-full" style="width: 75%"></div>
                        </div>
                        <span class="text-[10px] text-brand-muted font-medium">75%</span>
                      </div>
                    </div>
                  </div>
                  <!-- 快捷统计 -->
                  <div class="grid grid-cols-3 gap-2 mt-4">
                    <div class="text-center p-2 rounded-lg bg-brand-card/50 backdrop-blur">
                      <p class="text-lg font-bold text-brand-text">12</p>
                      <p class="text-[10px] text-brand-muted">投递</p>
                    </div>
                    <div class="text-center p-2 rounded-lg bg-brand-card/50 backdrop-blur">
                      <p class="text-lg font-bold text-cyan-600 dark:text-violet-400">5</p>
                      <p class="text-[10px] text-brand-muted">面试</p>
                    </div>
                    <div class="text-center p-2 rounded-lg bg-brand-card/50 backdrop-blur">
                      <p class="text-lg font-bold text-brand-text">8</p>
                      <p class="text-[10px] text-brand-muted">收藏</p>
                    </div>
                  </div>
                </div>
                
                <!-- 个人中心入口 -->
                <div class="p-2 border-b border-brand-border">
                  <router-link to="/user-center" @click="userOpen = false"
                    class="flex items-center gap-3 px-3 py-3 rounded-xl bg-gradient-to-r from-cyan-500/10 to-teal-500/10 dark:from-violet-500/10 dark:to-indigo-500/10 hover:from-cyan-500/20 hover:to-teal-500/20 dark:hover:from-violet-500/20 dark:hover:to-indigo-500/20 transition-all group">
                    <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500 flex items-center justify-center text-white group-hover:scale-110 transition-transform">
                      <i class="bi bi-person-circle text-lg"></i>
                    </div>
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-brand-text">个人中心</p>
                      <p class="text-xs text-brand-muted">查看完整档案</p>
                    </div>
                    <i class="bi bi-chevron-right text-brand-muted group-hover:translate-x-1 transition-transform"></i>
                  </router-link>
                </div>
                
                <!-- 主菜单分组 -->
                <div class="p-2">
                  <!-- 画像与能力 -->
                  <p class="px-3 py-1.5 text-[10px] font-semibold text-brand-muted uppercase tracking-wider">画像与能力</p>
                  <router-link v-for="item in profileMenuItems" :key="item.path" :to="item.path"
                    @click="userOpen = false"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-brand-muted hover:bg-brand-surface hover:text-brand-text transition-all group">
                    <i :class="[item.icon, 'text-base group-hover:scale-110 transition-transform']"></i>
                    <span>{{ item.label }}</span>
                    <span v-if="item.badge" class="ml-auto px-1.5 py-0.5 text-[10px] font-medium rounded bg-cyan-500/20 dark:bg-violet-500/20 text-cyan-600 dark:text-violet-400">{{ item.badge }}</span>
                  </router-link>
                  
                  <!-- 求职管理 -->
                  <p class="px-3 py-1.5 text-[10px] font-semibold text-brand-muted uppercase tracking-wider mt-2">求职管理</p>
                  <router-link v-for="item in jobMenuItems" :key="item.path" :to="item.path"
                    @click="userOpen = false"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-brand-muted hover:bg-brand-surface hover:text-brand-text transition-all group">
                    <i :class="[item.icon, 'text-base group-hover:scale-110 transition-transform']"></i>
                    <span>{{ item.label }}</span>
                    <span v-if="item.badge" class="ml-auto px-1.5 py-0.5 text-[10px] font-medium rounded bg-red-500/20 text-red-500">{{ item.badge }}</span>
                  </router-link>
                  
                  <!-- 系统 -->
                  <p class="px-3 py-1.5 text-[10px] font-semibold text-brand-muted uppercase tracking-wider mt-2">系统</p>
                  <router-link v-for="item in systemMenuItems" :key="item.path" :to="item.path"
                    @click="userOpen = false"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-brand-muted hover:bg-brand-surface hover:text-brand-text transition-all group">
                    <i :class="[item.icon, 'text-base group-hover:scale-110 transition-transform']"></i>
                    <span>{{ item.label }}</span>
                  </router-link>
                </div>
                
                <!-- 登出按钮 -->
                <div class="p-2 border-t border-brand-border">
                  <button v-if="authStore.isLoggedIn"
                    @click="handleLogout"
                    class="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm text-red-500 hover:bg-red-500/10 transition-all group">
                    <i class="bi bi-box-arrow-right text-base group-hover:scale-110 transition-transform"></i>
                    退出登录
                  </button>
                  <router-link v-else to="/login"
                    @click="userOpen = false"
                    class="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm text-cyan-600 dark:text-violet-400 hover:bg-cyan-500/10 dark:hover:bg-violet-500/10 transition-all group">
                    <i class="bi bi-box-arrow-in-right text-base group-hover:scale-110 transition-transform"></i>
                    立即登录
                  </router-link>
                </div>
              </div>
            </transition>
          </div>
          <!-- Mobile Toggle -->
          <button class="md:hidden btn-ghost p-2" @click="mobileOpen = !mobileOpen">
            <i :class="mobileOpen ? 'bi bi-x-lg' : 'bi bi-list'" class="text-lg"></i>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <transition name="slide">
        <div v-if="mobileOpen" class="mobile-menu-panel md:hidden pb-4 border-t border-brand-border mt-2 pt-4 space-y-1">
          <router-link v-for="item in allMobileLinks" :key="item.path" :to="item.path"
            class="flex items-center gap-2 px-4 py-3 rounded-lg text-sm font-medium transition-all"
            :class="isActive(item.path) ? 'bg-cyan-500/10 text-cyan-600 dark:bg-violet-500/10 dark:text-violet-400' : 'text-brand-muted hover:text-brand-text hover:bg-brand-card'"
            @click="mobileOpen = false">
            <i :class="item.icon"></i>
            <span>{{ item.label }}</span>
          </router-link>
          
          <!-- 退出登录按钮 -->
          <div class="pt-3 mt-3 border-t border-brand-border">
            <button v-if="authStore.isLoggedIn"
              @click="handleLogout; mobileOpen = false"
              class="flex items-center gap-2 w-full px-4 py-3 rounded-lg text-sm font-medium text-red-500 hover:bg-red-500/10 transition-all">
              <i class="bi bi-box-arrow-right"></i>
              <span>退出登录</span>
            </button>
            <router-link v-else to="/login"
              @click="mobileOpen = false"
              class="flex items-center gap-2 w-full px-4 py-3 rounded-lg text-sm font-medium text-cyan-600 dark:text-violet-400 hover:bg-cyan-500/10 dark:hover:bg-violet-500/10 transition-all">
              <i class="bi bi-box-arrow-in-right"></i>
              <span>立即登录</span>
            </router-link>
          </div>
        </div>
      </transition>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/themeStore'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const scrolled = ref(false)
const mobileOpen = ref(false)
const userOpen = ref(false)
const notifOpen = ref(false)
const userAvatar = ref('')

// 加载用户头像
function loadUserAvatar() {
  const saved = localStorage.getItem('user-avatar')
  if (saved) {
    userAvatar.value = saved
  }
}

// 通知数据
const unreadCount = ref(3)
const notifications = ref([
  { 
    id: 1, 
    content: '您投递的「前端开发工程师」有新回复，HR已查看您的简历', 
    time: '10分钟前', 
    read: false,
    icon: 'bi bi-envelope-open',
    bgClass: 'bg-cyan-500/10 dark:bg-violet-500/10',
    iconClass: 'text-cyan-600 dark:text-violet-400'
  },
  { 
    id: 2, 
    content: '收到腾讯科技的面试邀请，产品经理岗位', 
    time: '2小时前', 
    read: false,
    icon: 'bi bi-calendar-event',
    bgClass: 'bg-emerald-500/10',
    iconClass: 'text-emerald-600'
  },
  { 
    id: 3, 
    content: '您的Python技能评估已完成，得分 85/100', 
    time: '昨天', 
    read: false,
    icon: 'bi bi-award',
    bgClass: 'bg-amber-500/10',
    iconClass: 'text-amber-600'
  },
  { 
    id: 4, 
    content: '阿里巴巴HR收藏了您的简历', 
    time: '2天前', 
    read: true,
    icon: 'bi bi-heart-fill',
    bgClass: 'bg-rose-500/10',
    iconClass: 'text-rose-500'
  },
])

function toggleTheme() {
  themeStore.toggleTheme()
}

function handleLogout() {
  authStore.logout()
  userOpen.value = false
  router.push('/login')
}

const navItems = [
  { path: '/', label: '首页' },
  { path: '/career/explore', label: '职业探索' },
  { path: '/analysis', label: '画像分析' },
  { path: '/job-hub', label: '求职交流' },
  { path: '/resume', label: '简历中心' },
  { path: '/planning', label: '规划中心' },
]

// 画像与能力菜单
const profileMenuItems = [
  { path: '/career/profile', label: '自我画像', icon: 'bi bi-person-bounding-box' },
  { path: '/career/skills', label: '技能评估', icon: 'bi bi-lightning', badge: '新' },
  { path: '/my-profile', label: '求职画像', icon: 'bi bi-file-earmark-person' },
]

// 求职管理菜单
const jobMenuItems = [
  { path: '/my-applications', label: '投递管理', icon: 'bi bi-send', badge: '3' },
  { path: '/messages', label: '消息中心', icon: 'bi bi-chat-dots' },
  { path: '/career/actions', label: '行动管理', icon: 'bi bi-check2-square' },
]

// 系统菜单
const systemMenuItems = [
  { path: '/students', label: '学生管理', icon: 'bi bi-people' },
  { path: '/settings', label: '系统设置', icon: 'bi bi-gear' },
  { path: '/about', label: '关于我们', icon: 'bi bi-info-circle' },
]

const userMenuItems = [
  ...profileMenuItems,
  ...jobMenuItems,
  ...systemMenuItems,
]

const allMobileLinks = computed(() => [
  { path: '/', label: '首页', icon: 'bi bi-house' },
  { path: '/career/explore', label: '职业探索', icon: 'bi bi-signpost-split' },
  { path: '/analysis', label: '画像分析', icon: 'bi bi-bar-chart' },
  { path: '/job-hub', label: '求职交流', icon: 'bi bi-people-fill' },
  { path: '/resume', label: '简历中心', icon: 'bi bi-file-earmark-person' },
  { path: '/planning', label: '规划中心', icon: 'bi bi-file-earmark-text' },
  ...userMenuItems,
])

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function handleScroll() { scrolled.value = window.scrollY > 20 }

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  loadUserAvatar()
  // 监听头像更新事件
  window.addEventListener('avatar-updated', loadUserAvatar)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('avatar-updated', loadUserAvatar)
})
</script>

<style scoped>
/* 用户下拉面板 - 桌面端 */
.user-dropdown-panel {
  max-height: 600px;
}

/* 移动端菜单面板 */
.mobile-menu-panel {
  max-height: calc(100vh - 64px - 72px); /* 减去导航栏和底部导航 */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 80px; /* 底部留空 */
}

/* 移动端适配 */
@media (max-width: 768px) {
  .user-dropdown-panel {
    position: fixed !important;
    top: 64px !important;
    left: 12px !important;
    right: 12px !important;
    bottom: 80px !important; /* 留出底部导航空间 */
    width: auto !important;
    max-height: none !important;
    z-index: 200;
    border-radius: 16px;
    -webkit-overflow-scrolling: touch;
  }
}
</style>
