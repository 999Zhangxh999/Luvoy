<template>
  <div class="min-h-screen transition-colors duration-300" :class="[hideNav ? '' : 'bg-brand-bg', { 'capacitor-app': isCapacitorApp }]">
    <NavBar v-if="!hideNav" />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <AppFooter v-if="!hideNav" class="hidden md:block" />
    
    <!-- 移动端底部导航 -->
    <MobileBottomNav v-if="!hideNav" />
    
    <!-- Loading Overlay -->
    <LoadingOverlay :visible="loading" :message="loadingMsg" />
    
    <!-- Toast Container -->
    <ToastContainer />
    
    <!-- Back to top button -->
    <button 
      v-show="showTop && !hideNav" 
      @click="scrollTop"
      class="fixed bottom-20 md:bottom-8 right-4 md:right-8 w-10 h-10 md:w-12 md:h-12 rounded-xl bg-brand-card border border-brand-border
             flex items-center justify-center text-brand-muted hover:text-cyan-500 dark:hover:text-violet-400 hover:border-cyan-500/40 dark:hover:border-violet-500/40
             transition-all duration-300 shadow-card z-50"
    >
      <i class="bi bi-chevron-up text-lg"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'
import AppFooter from './components/AppFooter.vue'
import MobileBottomNav from './components/MobileBottomNav.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'
import ToastContainer from './components/ToastContainer.vue'
import { useThemeStore } from './stores/themeStore'

const route = useRoute()

// 初始化主题
const themeStore = useThemeStore()

// 检测是否是Capacitor应用
const isCapacitorApp = computed(() => {
  return typeof window !== 'undefined' && window.Capacitor !== undefined
})

// 隐藏导航栏（登录页等）
const hideNav = computed(() => route.meta?.hideNav === true)

const loading = ref(false)
const loadingMsg = ref('')
const showTop = ref(false)

// Toast 系统
const toasts = ref([])
let toastId = 0
function addToast(message, type = 'success', duration = 3500) {
  const id = ++toastId
  toasts.value.push({ id, message, type, visible: true })
  setTimeout(() => {
    const idx = toasts.value.findIndex(t => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }, duration)
}

provide('setLoading', (v, msg = '') => { loading.value = v; loadingMsg.value = msg })
provide('toast', addToast)
provide('toasts', toasts)

function onScroll() { showTop.value = window.scrollY > 300 }
function scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>
