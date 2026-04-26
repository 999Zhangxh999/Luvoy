<template>
  <div class="min-h-screen relative overflow-hidden transition-colors duration-500">
    <!-- 黑夜模式背景 -->
    <div v-if="isDark" class="absolute inset-0 bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
      <!-- 动画网格 -->
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PHBhdGggZD0iTTM2IDM0djItaC0ydi0yaC00djJoLTJ2LTJoLTR2Mmgtdi0yaC00djJoLTJ2LTJoLTZ2MmgtMnYtMmgtNHYyaC0ydi0yaC02djJoLTJ2LTJoLTR2MmgtMnYtMmgtNnYyaC0ydi0yaC00djJoLTJ2LTJoLTZ2MmgtMnYtMmgtNHYyaC0ydi0yaC02djJoLTJ2LTJoLTR2MmgtMnYtMmgtNnYyaC0ydi0yaC00djJoLTJ2LTIiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30"></div>
      
      <!-- 光晕效果 -->
      <div class="absolute top-1/4 -right-1/4 w-96 h-96 bg-indigo-500/30 rounded-full blur-[120px] animate-pulse"></div>
      <div class="absolute bottom-1/4 -left-1/4 w-96 h-96 bg-cyan-500/30 rounded-full blur-[120px] animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-500/20 rounded-full blur-[150px]"></div>
      
      <!-- 浮动粒子 -->
      <div class="absolute inset-0 overflow-hidden">
        <div v-for="n in 20" :key="'dark-'+n" 
             class="absolute w-1 h-1 bg-white/20 rounded-full animate-float"
             :style="{
               left: `${Math.random() * 100}%`,
               top: `${Math.random() * 100}%`,
               animationDelay: `${Math.random() * 5}s`,
               animationDuration: `${3 + Math.random() * 4}s`
             }"></div>
      </div>
    </div>

    <!-- 白天模式背景 -->
    <div v-else class="absolute inset-0 bg-gradient-to-br from-teal-50 via-cyan-100 to-sky-100">
      <!-- 装饰圆形 -->
      <div class="absolute top-0 left-0 w-[500px] h-[500px] bg-gradient-to-br from-teal-200/50 to-cyan-200/50 rounded-full blur-3xl -translate-y-1/2 -translate-x-1/4"></div>
      <div class="absolute bottom-0 right-0 w-[400px] h-[400px] bg-gradient-to-br from-sky-200/50 to-blue-200/50 rounded-full blur-3xl translate-y-1/2 translate-x-1/4"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-cyan-100/30 to-teal-100/30 rounded-full blur-3xl"></div>
      
      <!-- 浮动装饰 -->
      <div class="absolute inset-0 overflow-hidden">
        <div v-for="n in 15" :key="'light-'+n" 
             class="absolute w-3 h-3 bg-teal-400/20 rounded-full animate-float-light"
             :style="{
               left: `${Math.random() * 100}%`,
               top: `${Math.random() * 100}%`,
               animationDelay: `${Math.random() * 5}s`,
               animationDuration: `${4 + Math.random() * 4}s`
             }"></div>
      </div>
    </div>

    <!-- 主题切换按钮 -->
    <button 
      @click="toggleTheme"
      class="absolute top-6 right-6 w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 z-20"
      :class="isDark 
        ? 'bg-white/10 backdrop-blur-xl border border-white/20 text-white hover:bg-white/20' 
        : 'bg-white/80 backdrop-blur-xl border border-teal-200 text-teal-600 hover:bg-white shadow-lg'"
    >
      <i :class="isDark ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill'" class="text-xl"></i>
    </button>
    
    <!-- 内容容器 -->
    <div class="relative min-h-screen flex items-center justify-center p-4 z-10">
      <div class="w-full max-w-lg">
        <!-- Logo 区域 -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-22 h-22 rounded-3xl mb-6 shadow-2xl transform hover:scale-105 transition-transform bg-white/80 dark:bg-white/10 p-2.5"
               :class="isDark ? 'shadow-indigo-500/30' : 'shadow-teal-500/30'">
            <img src="/logo.png" alt="拓扑 Topo 标识" class="w-full h-full rounded-2xl" />
          </div>
          <h1 class="text-4xl font-bold mb-3 tracking-tight"
              :class="isDark ? 'text-white' : 'text-slate-800'">拓扑 · Topo</h1>
          <p :class="isDark ? 'text-white/60' : 'text-slate-500'" class="text-lg">创建您的账户</p>
        </div>

        <!-- 注册卡片 -->
        <div class="rounded-3xl border p-8 shadow-2xl transition-all duration-300"
             :class="isDark 
               ? 'bg-white/10 backdrop-blur-2xl border-white/20 shadow-black/20' 
               : 'bg-white/90 backdrop-blur-xl border-teal-100 shadow-teal-500/10'">
          <!-- 表单标题 -->
          <div class="text-center mb-8">
            <h2 class="text-2xl font-semibold mb-2"
                :class="isDark ? 'text-white' : 'text-slate-800'">新用户注册</h2>
            <p :class="isDark ? 'text-white/50' : 'text-slate-500'" class="text-sm">填写信息开始您的职业规划之旅</p>
          </div>

          <!-- 注册表单 -->
          <form @submit.prevent="handleRegister" class="space-y-5">
            <!-- 用户名 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">用户名</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-person-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-indigo-400' : 'text-slate-400 group-focus-within:text-teal-500'"></i>
                  <input 
                    v-model="form.username"
                    type="text" 
                    placeholder="输入您的用户名"
                    class="w-full pl-12 pr-4 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20'"
                  >
                </div>
              </div>
            </div>

            <!-- 邮箱 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">电子邮箱</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-envelope-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-indigo-400' : 'text-slate-400 group-focus-within:text-teal-500'"></i>
                  <input 
                    v-model="form.email"
                    type="email" 
                    placeholder="输入您的邮箱"
                    class="w-full pl-12 pr-4 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20'"
                  >
                </div>
              </div>
            </div>

            <!-- 密码 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">密码</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-lock-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-indigo-400' : 'text-slate-400 group-focus-within:text-teal-500'"></i>
                  <input 
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'" 
                    placeholder="设置您的密码 (至少6位)"
                    class="w-full pl-12 pr-14 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20'"
                  >
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-4 top-1/2 -translate-y-1/2 transition-colors"
                    :class="isDark ? 'text-white/40 hover:text-white' : 'text-slate-400 hover:text-slate-600'"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- 确认密码 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">确认密码</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-shield-lock-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-indigo-400' : 'text-slate-400 group-focus-within:text-teal-500'"></i>
                  <input 
                    v-model="form.confirmPassword"
                    :type="showConfirmPassword ? 'text' : 'password'" 
                    placeholder="再次输入密码"
                    class="w-full pl-12 pr-14 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20'"
                  >
                  <button 
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="absolute right-4 top-1/2 -translate-y-1/2 transition-colors"
                    :class="isDark ? 'text-white/40 hover:text-white' : 'text-slate-400 hover:text-slate-600'"
                  >
                    <i :class="showConfirmPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- 服务条款 -->
            <div class="flex items-start gap-3">
              <label class="flex items-start gap-2 cursor-pointer group">
                <div class="relative mt-0.5">
                  <input 
                    v-model="form.agreeTerms"
                    type="checkbox" 
                    class="sr-only peer"
                  >
                  <div class="w-5 h-5 rounded-md border transition-all"
                       :class="isDark 
                         ? 'border-white/20 bg-white/5 peer-checked:bg-indigo-500 peer-checked:border-indigo-500' 
                         : 'border-slate-300 bg-white peer-checked:bg-teal-500 peer-checked:border-teal-500'"></div>
                  <i class="bi bi-check absolute inset-0 flex items-center justify-center text-white opacity-0 peer-checked:opacity-100 transition-opacity"></i>
                </div>
                <span class="text-sm transition-colors" :class="isDark ? 'text-white/60 group-hover:text-white/80' : 'text-slate-500 group-hover:text-slate-700'">
                  我已阅读并同意
                  <a href="#" :class="isDark ? 'text-indigo-400 hover:text-indigo-300' : 'text-teal-600 hover:text-teal-700'">服务条款</a>
                  和
                  <a href="#" :class="isDark ? 'text-indigo-400 hover:text-indigo-300' : 'text-teal-600 hover:text-teal-700'">隐私政策</a>
                </span>
              </label>
            </div>

            <!-- 错误提示 -->
            <div v-if="error" class="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-red-500 text-sm text-center">
              <i class="bi bi-exclamation-circle mr-2"></i>{{ error }}
            </div>

            <!-- 注册按钮 -->
            <button 
              type="submit"
              :disabled="loading"
              class="w-full py-4 rounded-xl font-semibold text-white transition-all duration-300
                     hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed
                     relative overflow-hidden group"
              :class="isDark 
                ? 'bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-600 hover:from-indigo-500 hover:via-purple-500 hover:to-cyan-500 shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40' 
                : 'bg-gradient-to-r from-teal-500 via-cyan-500 to-blue-500 hover:from-teal-400 hover:via-cyan-400 hover:to-blue-400 shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40'"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              <span v-if="!loading" class="relative flex items-center justify-center gap-2">
                <i class="bi bi-person-plus-fill"></i>
                创建账户
              </span>
              <span v-else class="relative flex items-center justify-center gap-2">
                <i class="bi bi-arrow-repeat animate-spin"></i>
                注册中...
              </span>
            </button>
          </form>

          <!-- 登录链接 -->
          <p class="text-center mt-8" :class="isDark ? 'text-white/50' : 'text-slate-500'">
            已有账号？
            <router-link to="/login" :class="isDark ? 'text-indigo-400 hover:text-indigo-300' : 'text-teal-600 hover:text-teal-700'" class="font-medium transition-colors">立即登录</router-link>
          </p>
        </div>

        <!-- 底部信息 -->
        <p class="text-center text-sm mt-8" :class="isDark ? 'text-white/30' : 'text-slate-400'">
          <i class="bi bi-shield-check mr-1"></i>
          您的信息将被安全加密保存
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/themeStore'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false,
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const error = ref('')

const isDark = computed(() => themeStore.theme === 'dark')

function toggleTheme() {
  themeStore.toggleTheme()
}

async function handleRegister() {
  error.value = ''
  
  // 验证
  if (!form.value.username || !form.value.email || !form.value.password) {
    error.value = '请填写所有必填项'
    return
  }
  
  if (form.value.password.length < 6) {
    error.value = '密码至少需要6位字符'
    return
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  if (!form.value.agreeTerms) {
    error.value = '请先同意服务条款'
    return
  }
  
  loading.value = true
  
  try {
    await authStore.register(form.value.username, form.value.email, form.value.password)
    router.push('/')
  } catch (e) {
    error.value = e.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (authStore.isLoggedIn) {
    router.push('/')
  }
})
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0.2;
  }
  50% {
    transform: translateY(-20px) translateX(10px);
    opacity: 0.5;
  }
}

@keyframes float-light {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-30px) translateX(15px) scale(1.2);
    opacity: 0.6;
  }
}

.animate-float {
  animation: float ease-in-out infinite;
}

.animate-float-light {
  animation: float-light ease-in-out infinite;
}
</style>