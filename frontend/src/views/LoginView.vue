<template>
  <div class="login-page min-h-screen relative overflow-hidden" style="background: transparent !important; position: fixed; inset: 0;">
    <!-- 黑夜模式背景 -->
    <div ref="darkBgRef" class="login-dark-bg absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" :style="{ opacity: isDark ? '1' : '0', pointerEvents: isDark ? 'auto' : 'none', zIndex: 5 }">
      <!-- 动画网格 -->
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PHBhdGggZD0iTTM2IDM0djItaC0ydi0yaC00djJoLTJ2LTJoLTR2Mmgtdi0yaC00djJoLTJ2LTJoLTZ2MmgtMnYtMmgtNHYyaC0ydi0yaC02djJoLTJ2LTJoLTR2MmgtMnYtMmgtNnYyaC0ydi0yaC00djJoLTJ2LTJoLTZ2MmgtMnYtMmgtNHYyaC0ydi0yaC02djJoLTJ2LTJoLTR2MmgtMnYtMmgtNnYyaC0ydi0yaC00djJoLTJ2LTIiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-40"></div>
      
      <!-- 光晕效果 -->
      <div class="absolute top-1/4 -left-1/4 w-[500px] h-[500px] bg-purple-500/50 rounded-full blur-[120px] animate-glow"></div>
      <div class="absolute bottom-1/4 -right-1/4 w-[500px] h-[500px] bg-cyan-500/50 rounded-full blur-[120px] animate-glow" style="animation-delay: 2s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-violet-500/40 rounded-full blur-[150px] animate-pulse-slow"></div>
      
      <!-- 额外光点 -->
      <div class="absolute top-[10%] right-[30%] w-40 h-40 bg-pink-500/30 rounded-full blur-[80px] animate-glow" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-[20%] left-[20%] w-32 h-32 bg-blue-500/30 rounded-full blur-[60px] animate-glow" style="animation-delay: 3s;"></div>
      
      <!-- 固定位置的浮动粒子 -->
      <div class="absolute top-[5%] left-[15%] w-2 h-2 bg-violet-400/70 rounded-full animate-float-random"></div>
      <div class="absolute top-[8%] left-[45%] w-2.5 h-2.5 bg-cyan-400/60 rounded-full animate-float-random" style="animation-delay: 1s;"></div>
      <div class="absolute top-[12%] right-[20%] w-1.5 h-1.5 bg-white/50 rounded-full animate-float-random" style="animation-delay: 2s;"></div>
      <div class="absolute top-[18%] left-[30%] w-3 h-3 bg-pink-400/50 rounded-full animate-float-random" style="animation-delay: 0.5s;"></div>
      <div class="absolute top-[25%] right-[35%] w-2 h-2 bg-violet-400/70 rounded-full animate-float-random" style="animation-delay: 1.5s;"></div>
      <div class="absolute top-[32%] left-[8%] w-2.5 h-2.5 bg-cyan-400/60 rounded-full animate-float-random" style="animation-delay: 2.5s;"></div>
      <div class="absolute top-[38%] right-[12%] w-1.5 h-1.5 bg-white/50 rounded-full animate-float-random" style="animation-delay: 3s;"></div>
      <div class="absolute top-[45%] left-[55%] w-3 h-3 bg-pink-400/50 rounded-full animate-float-random" style="animation-delay: 0.8s;"></div>
      <div class="absolute top-[52%] right-[45%] w-2 h-2 bg-violet-400/70 rounded-full animate-float-random" style="animation-delay: 1.8s;"></div>
      <div class="absolute top-[58%] left-[22%] w-2.5 h-2.5 bg-cyan-400/60 rounded-full animate-float-random" style="animation-delay: 2.8s;"></div>
      <div class="absolute top-[65%] right-[28%] w-1.5 h-1.5 bg-white/50 rounded-full animate-float-random" style="animation-delay: 3.5s;"></div>
      <div class="absolute top-[72%] left-[38%] w-3 h-3 bg-pink-400/50 rounded-full animate-float-random" style="animation-delay: 0.3s;"></div>
      <div class="absolute top-[78%] right-[8%] w-2 h-2 bg-violet-400/70 rounded-full animate-float-random" style="animation-delay: 1.3s;"></div>
      <div class="absolute top-[85%] left-[65%] w-2.5 h-2.5 bg-cyan-400/60 rounded-full animate-float-random" style="animation-delay: 2.3s;"></div>
      <div class="absolute bottom-[8%] right-[55%] w-1.5 h-1.5 bg-white/50 rounded-full animate-float-random" style="animation-delay: 3.3s;"></div>
      <div class="absolute top-[15%] right-[5%] w-2 h-2 bg-violet-400/70 rounded-full animate-float-random" style="animation-delay: 4s;"></div>
      <div class="absolute top-[42%] left-[3%] w-2.5 h-2.5 bg-cyan-400/60 rounded-full animate-float-random" style="animation-delay: 4.5s;"></div>
      <div class="absolute bottom-[25%] left-[50%] w-3 h-3 bg-pink-400/50 rounded-full animate-float-random" style="animation-delay: 5s;"></div>
      
      <!-- 动态线条 -->
      <svg class="absolute inset-0 w-full h-full opacity-20">
        <defs>
          <linearGradient id="line-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#7c3aed;stop-opacity:0" />
            <stop offset="50%" style="stop-color:#06b6d4;stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:0" />
          </linearGradient>
        </defs>
        <line x1="0" y1="30%" x2="100%" y2="70%" stroke="url(#line-gradient)" stroke-width="2" class="animate-line-move" />
        <line x1="100%" y1="20%" x2="0" y2="80%" stroke="url(#line-gradient)" stroke-width="2" class="animate-line-move" style="animation-delay: 3s;" />
        <line x1="50%" y1="0" x2="50%" y2="100%" stroke="url(#line-gradient)" stroke-width="2" class="animate-line-move" style="animation-delay: 6s;" />
      </svg>
      
      <!-- 浮动几何形状 -->
      <div class="absolute top-20 left-[10%] w-24 h-24 border-2 border-violet-500/40 rounded-lg rotate-45 animate-float-spin"></div>
      <div class="absolute bottom-32 right-[15%] w-20 h-20 border-2 border-cyan-500/40 rounded-full animate-float-spin" style="animation-delay: 2s;"></div>
      <div class="absolute top-[60%] left-[5%] w-16 h-16 border-2 border-purple-500/40 transform rotate-12 animate-float-spin" style="animation-delay: 4s;"></div>
      <div class="absolute top-[20%] right-[8%] w-28 h-28 border-2 border-indigo-500/30 rounded-2xl animate-float-spin" style="animation-delay: 1s;"></div>
    </div>

    <!-- 白天模式背景 -->
    <div ref="lightBgRef" class="login-light-bg absolute inset-0" :style="{ 
      opacity: isDark ? '0' : '1', 
      pointerEvents: isDark ? 'none' : 'auto', 
      background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 40%, #ecfeff 100%)',
      zIndex: 5
    }">
      <!-- 网格点阵背景 - 更淡 -->
      <div class="absolute inset-0" style="background-image: radial-gradient(circle, rgba(14,165,233,0.15) 1.5px, transparent 1.5px); background-size: 35px 35px;"></div>
      <!-- 大装饰球 - 降低透明度 -->
      <div class="absolute -top-20 -right-20 w-[500px] h-[500px] rounded-full animate-float-slow" style="background: radial-gradient(circle, rgba(6,182,212,0.35) 0%, rgba(20,184,166,0.15) 50%, transparent 80%);"></div>
      <div class="absolute -bottom-32 -left-20 w-[450px] h-[450px] rounded-full animate-float-slow" style="background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, rgba(14,165,233,0.12) 50%, transparent 80%); animation-delay: 2s;"></div>
      <div class="absolute top-1/3 left-1/2 -translate-x-1/2 w-[350px] h-[350px] rounded-full animate-blob" style="background: radial-gradient(circle, rgba(45,212,191,0.25) 0%, rgba(34,211,238,0.1) 50%, transparent 75%); animation-delay: 4s;"></div>
      <!-- 中型漂浮球 - 更柔和 -->
      <div class="absolute top-[12%] left-[10%] w-40 h-40 rounded-full animate-float-slow" style="background: rgba(6,182,212,0.2); box-shadow: 0 0 80px rgba(6,182,212,0.25);"></div>
      <div class="absolute top-[55%] right-[8%] w-32 h-32 rounded-full animate-float-slow" style="background: rgba(59,130,246,0.18); box-shadow: 0 0 70px rgba(59,130,246,0.2); animation-delay: 1.5s;"></div>
      <!-- 闪烁光点 - box-shadow更柔和 -->
      <div class="absolute top-[8%] left-[28%] w-5 h-5 rounded-full animate-twinkle" style="background: white; box-shadow: 0 0 25px rgba(6,182,212,0.6);"></div>
      <div class="absolute top-[18%] right-[32%] w-4 h-4 rounded-full animate-twinkle" style="background: white; box-shadow: 0 0 22px rgba(20,184,166,0.5); animation-delay: 0.8s;"></div>
      <div class="absolute top-[28%] left-[48%] w-5 h-5 rounded-full animate-twinkle" style="background: white; box-shadow: 0 0 25px rgba(6,182,212,0.5); animation-delay: 1.6s;"></div>
      <div class="absolute top-[48%] left-[12%] w-4 h-4 rounded-full animate-twinkle" style="background: white; box-shadow: 0 0 22px rgba(59,130,246,0.5); animation-delay: 2.4s;"></div>
      <!-- 浮动气泡 - 更透明 -->
      <div class="absolute top-[6%] left-[42%] w-10 h-10 rounded-full animate-float-light-random" style="background: rgba(6,182,212,0.25); border: 1.5px solid rgba(255,255,255,0.6);"></div>
      <div class="absolute top-[20%] left-[18%] w-12 h-12 rounded-full animate-float-light-random" style="background: rgba(20,184,166,0.2); border: 1.5px solid rgba(255,255,255,0.5); animation-delay: 1s;"></div>
      <div class="absolute top-[58%] right-[32%] w-8 h-8 rounded-full animate-float-light-random" style="background: rgba(6,182,212,0.28); border: 1.5px solid rgba(255,255,255,0.6); animation-delay: 0.5s;"></div>
      <div class="absolute top-[68%] left-[28%] w-11 h-11 rounded-full animate-float-light-random" style="background: rgba(52,211,153,0.2); border: 1.5px solid rgba(255,255,255,0.5); animation-delay: 1.5s;"></div>
      <!-- 波浪 - 更柔和 -->
      <svg class="absolute bottom-0 left-0 w-full h-40" preserveAspectRatio="none" viewBox="0 0 1440 120">
        <path fill="rgba(6,182,212,0.25)" d="M0,40L60,45C120,50,240,60,360,65C480,70,600,70,720,60C840,50,960,30,1080,25C1200,20,1320,30,1380,35L1440,40L1440,120L1380,120C1320,120,1200,120,1080,120C960,120,840,120,720,120C600,120,480,120,360,120C240,120,120,120,60,120L0,120Z" class="animate-wave"></path>
        <path fill="rgba(14,165,233,0.18)" d="M0,70L60,65C120,60,240,50,360,50C480,50,600,60,720,70C840,80,960,90,1080,85C1200,80,1320,60,1380,50L1440,40L1440,120L1380,120C1320,120,1200,120,1080,120C960,120,840,120,720,120C600,120,480,120,360,120C240,120,120,120,60,120L0,120Z" class="animate-wave" style="animation-delay: 1s;"></path>
      </svg>
      <!-- 边框形状 - 更淡 -->
      <div class="absolute top-14 left-[4%] w-20 h-20 border-2 border-cyan-400/40 rounded-2xl rotate-12 animate-float-spin-light"></div>
      <div class="absolute bottom-48 right-[6%] w-16 h-16 border-2 border-teal-400/40 rounded-full animate-float-spin-light" style="animation-delay: 1.5s;"></div>
    </div>

    <!-- 主题切换按钮 -->
    <button 
      @click="toggleTheme"
      class="absolute top-6 right-6 w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 z-20"
      :class="isDark 
        ? 'bg-white/10 backdrop-blur-xl border border-white/20 text-white hover:bg-white/20' 
        : 'bg-white/80 backdrop-blur-xl border border-cyan-200 text-cyan-600 hover:bg-white shadow-lg'"
    >
      <i :class="isDark ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill'" class="text-xl"></i>
    </button>
    
    <!-- 内容容器 -->
    <div class="relative flex items-center justify-center p-4" style="z-index: 10; min-height: 100vh; background: transparent !important;">
      <div class="w-full max-w-lg">
        <!-- Logo 区域 -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 rounded-3xl mb-6 shadow-2xl transform hover:scale-105 transition-transform bg-white/80 dark:bg-white/10 p-2.5"
               :class="isDark ? 'shadow-purple-500/30' : 'shadow-cyan-500/30'">
            <img src="/luvoy-main-20260404.svg" alt="律途 Luvoy 标识" class="w-full h-full rounded-2xl" />
          </div>
          <h1 class="text-4xl font-bold mb-3 tracking-tight"
              :class="isDark ? 'text-white' : 'text-slate-800'">律途 · Luvoy</h1>
          <p :class="isDark ? 'text-white/60' : 'text-slate-500'" class="text-lg">Life's Unique Voyage</p>
        </div>

        <!-- 登录卡片 -->
        <div class="rounded-3xl border p-8 shadow-2xl transition-all duration-300"
             :class="isDark 
               ? 'bg-white/10 backdrop-blur-2xl border-white/20 shadow-black/20' 
               : 'bg-white/90 backdrop-blur-xl border-cyan-100 shadow-cyan-500/10'">
          <!-- 表单标题 -->
          <div class="text-center mb-8">
            <h2 class="text-2xl font-semibold mb-2"
                :class="isDark ? 'text-white' : 'text-slate-800'">欢迎回来</h2>
            <p :class="isDark ? 'text-white/50' : 'text-slate-500'" class="text-sm">登录您的账户继续使用</p>
          </div>

          <!-- 登录表单 -->
          <form @submit.prevent="handleLogin" class="space-y-5">
            <!-- 用户名 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">用户名 / 邮箱</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-violet-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-person-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-violet-400' : 'text-slate-400 group-focus-within:text-cyan-500'"></i>
                  <input 
                    v-model="form.username"
                    type="text" 
                    placeholder="请输入用户名或邮箱"
                    class="w-full pl-12 pr-4 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20'"
                  >
                </div>
              </div>
            </div>

            <!-- 密码 -->
            <div class="space-y-2">
              <label class="text-sm font-medium block"
                     :class="isDark ? 'text-white/70' : 'text-slate-600'">密码</label>
              <div class="relative group">
                <div v-if="isDark" class="absolute inset-0 bg-gradient-to-r from-violet-500 to-cyan-500 rounded-xl opacity-0 group-focus-within:opacity-100 blur transition-opacity -m-0.5"></div>
                <div class="relative">
                  <i class="bi bi-lock-fill absolute left-4 top-1/2 -translate-y-1/2 transition-colors"
                     :class="isDark ? 'text-white/40 group-focus-within:text-violet-400' : 'text-slate-400 group-focus-within:text-cyan-500'"></i>
                  <input 
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'" 
                    placeholder="请输入密码"
                    class="w-full pl-12 pr-14 py-4 rounded-xl transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:bg-white/10 focus:border-transparent' 
                      : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20'"
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

            <!-- 记住我 & 忘记密码/注册 -->
            <div class="flex items-center justify-between text-sm">
              <label class="flex items-center gap-2 cursor-pointer group">
                <div class="relative">
                  <input 
                    v-model="form.remember"
                    type="checkbox" 
                    class="sr-only peer"
                  >
                  <div class="w-5 h-5 rounded-md border transition-all"
                       :class="isDark 
                         ? 'border-white/20 bg-white/5 peer-checked:bg-violet-500 peer-checked:border-violet-500' 
                         : 'border-slate-300 bg-white peer-checked:bg-cyan-500 peer-checked:border-cyan-500'"></div>
                  <i class="bi bi-check absolute inset-0 flex items-center justify-center text-white opacity-0 peer-checked:opacity-100 transition-opacity"></i>
                </div>
                <span :class="isDark ? 'text-white/60 group-hover:text-white/80' : 'text-slate-500 group-hover:text-slate-700'" class="transition-colors">记住我</span>
              </label>
              <div class="flex items-center gap-3">
                <router-link to="/register" :class="isDark ? 'text-violet-400 hover:text-violet-300' : 'text-cyan-600 hover:text-cyan-700'" class="transition-colors">注册</router-link>
                <span :class="isDark ? 'text-white/30' : 'text-slate-300'">|</span>
                <a href="#" :class="isDark ? 'text-violet-400 hover:text-violet-300' : 'text-cyan-600 hover:text-cyan-700'" class="transition-colors">忘记密码？</a>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-if="error" class="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-red-500 text-sm text-center">
              <i class="bi bi-exclamation-circle mr-2"></i>{{ error }}
            </div>

            <!-- 登录按钮 -->
            <button 
              type="submit"
              :disabled="loading"
              class="w-full py-4 rounded-xl font-semibold text-white transition-all duration-300
                     hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed
                     relative overflow-hidden group"
              :class="isDark 
                ? 'bg-gradient-to-r from-violet-600 via-purple-600 to-cyan-600 hover:from-violet-500 hover:via-purple-500 hover:to-cyan-500 shadow-lg shadow-violet-500/30 hover:shadow-xl hover:shadow-violet-500/40' 
                : 'bg-gradient-to-r from-cyan-500 via-teal-500 to-blue-500 hover:from-cyan-400 hover:via-teal-400 hover:to-blue-400 shadow-lg shadow-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/40'"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              <span v-if="!loading" class="relative flex items-center justify-center gap-2">
                <i class="bi bi-box-arrow-in-right"></i>
                登录
              </span>
              <span v-else class="relative flex items-center justify-center gap-2">
                <i class="bi bi-arrow-repeat animate-spin"></i>
                登录中...
              </span>
            </button>

            <!-- 游客模式按钮 -->
            <button 
              type="button"
              @click="skipLogin"
              class="w-full py-4 rounded-xl font-semibold text-white transition-all duration-300
                     hover:-translate-y-0.5 active:translate-y-0
                     relative overflow-hidden group"
              :class="isDark 
                ? 'bg-gradient-to-r from-pink-500/80 via-rose-500/80 to-orange-500/80 hover:from-pink-400 hover:via-rose-400 hover:to-orange-400 shadow-lg shadow-pink-500/25 hover:shadow-xl hover:shadow-pink-500/35' 
                : 'bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-indigo-400 hover:via-purple-400 hover:to-pink-400 shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40'"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
              <span class="relative flex items-center justify-center gap-2">
                <i class="bi bi-rocket-takeoff"></i>
                游客模式，立即体验
              </span>
            </button>
          </form>

          <!-- 分隔线 -->
          <div class="relative my-8">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t" :class="isDark ? 'border-white/10' : 'border-slate-200'"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4" :class="isDark ? 'bg-transparent text-white/40' : 'bg-white/90 text-slate-400'">或者使用</span>
            </div>
          </div>

          <!-- 第三方登录 -->
          <div class="grid grid-cols-3 gap-4">
            <button class="flex items-center justify-center py-3 rounded-xl border transition-all duration-300 group"
                    :class="isDark 
                      ? 'bg-white/5 border-white/10 text-white hover:bg-white/10 hover:border-white/20' 
                      : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-cyan-300'">
              <i class="bi bi-github text-xl group-hover:scale-110 transition-transform"></i>
            </button>
            <button class="flex items-center justify-center py-3 rounded-xl border transition-all duration-300 group"
                    :class="isDark 
                      ? 'bg-white/5 border-white/10 text-white hover:bg-white/10 hover:border-white/20' 
                      : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-cyan-300'">
              <i class="bi bi-google text-xl group-hover:scale-110 transition-transform"></i>
            </button>
            <button class="flex items-center justify-center py-3 rounded-xl border transition-all duration-300 group"
                    :class="isDark 
                      ? 'bg-white/5 border-white/10 text-green-400 hover:bg-green-500/10 hover:border-green-500/30' 
                      : 'bg-white border-slate-200 text-green-500 hover:bg-green-50 hover:border-green-300'">
              <i class="bi bi-wechat text-xl group-hover:scale-110 transition-transform"></i>
            </button>
          </div>

          <!-- 注册按钮 -->
          <div class="mt-6">
            <p class="text-center mb-3" :class="isDark ? 'text-white/50' : 'text-slate-500'">还没有账号？</p>
            <router-link 
              to="/register" 
              class="w-full py-4 rounded-xl font-semibold text-white transition-all duration-300
                     hover:-translate-y-0.5 active:translate-y-0
                     relative overflow-hidden group flex items-center justify-center gap-2"
              :class="isDark 
                ? 'bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 hover:from-emerald-400 hover:via-teal-400 hover:to-cyan-400 shadow-lg shadow-emerald-500/25 hover:shadow-xl hover:shadow-emerald-500/35' 
                : 'bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 hover:from-emerald-400 hover:via-teal-400 hover:to-cyan-400 shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40'"
            >
              <i class="bi bi-person-plus"></i>
              立即注册
            </router-link>
          </div>
        </div>

        <!-- 底部信息 -->
        <p class="text-center text-sm mt-8" :class="isDark ? 'text-white/30' : 'text-slate-400'">
          登录即表示您同意我们的
          <a href="#" :class="isDark ? 'text-white/50 hover:text-white/70' : 'text-slate-500 hover:text-slate-700'" class="transition-colors">服务条款</a>
          和
          <a href="#" :class="isDark ? 'text-white/50 hover:text-white/70' : 'text-slate-500 hover:text-slate-700'" class="transition-colors">隐私政策</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/themeStore'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const themeStore = useThemeStore()
const { theme } = storeToRefs(themeStore)
const authStore = useAuthStore()

// 背景元素refs
const darkBgRef = ref(null)
const lightBgRef = ref(null)

const form = ref({
  username: '',
  password: '',
  remember: false,
})

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const isDark = computed(() => theme.value === 'dark')

// 使用watch直接操纵DOM
watch(theme, (newTheme) => {
  if (darkBgRef.value && lightBgRef.value) {
    if (newTheme === 'dark') {
      darkBgRef.value.style.opacity = '1'
      darkBgRef.value.style.pointerEvents = 'auto'
      lightBgRef.value.style.opacity = '0'
      lightBgRef.value.style.pointerEvents = 'none'
    } else {
      darkBgRef.value.style.opacity = '0'
      darkBgRef.value.style.pointerEvents = 'none'
      lightBgRef.value.style.opacity = '1'
      lightBgRef.value.style.pointerEvents = 'auto'
    }
  }
}, { immediate: true })

// 确保初始化时背景正确
onMounted(() => {
  if (darkBgRef.value && lightBgRef.value) {
    const currentTheme = theme.value
    if (currentTheme === 'dark') {
      darkBgRef.value.style.opacity = '1'
      darkBgRef.value.style.pointerEvents = 'auto'
      lightBgRef.value.style.opacity = '0'
      lightBgRef.value.style.pointerEvents = 'none'
    } else {
      darkBgRef.value.style.opacity = '0'
      darkBgRef.value.style.pointerEvents = 'none'
      lightBgRef.value.style.opacity = '1'
      lightBgRef.value.style.pointerEvents = 'auto'
    }
  }
})

function toggleTheme() {
  themeStore.toggleTheme()
}

async function handleLogin() {
  error.value = ''
  
  if (!form.value.username || !form.value.password) {
    error.value = '请填写用户名和密码'
    return
  }
  
  loading.value = true
  
  try {
    await authStore.login(form.value.username, form.value.password, form.value.remember)
    router.push('/')
  } catch (e) {
    error.value = e.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}

// 跳过登录，以游客模式进入
function skipLogin() {
  localStorage.setItem('luvoy-guest', 'true')
  router.push('/')
}

onMounted(() => {
  if (authStore.isLoggedIn) {
    router.push('/')
  }
})
</script>

<style scoped>
/* 基础浮动动画 */
@keyframes float-random {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0.7;
  }
  25% {
    transform: translateY(-30px) translateX(20px);
    opacity: 1;
  }
  50% {
    transform: translateY(-10px) translateX(-10px);
    opacity: 0.85;
  }
  75% {
    transform: translateY(-40px) translateX(5px);
    opacity: 0.9;
  }
}

@keyframes float-light-random {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.7;
  }
  25% {
    transform: translateY(-25px) translateX(15px) scale(1.1);
    opacity: 1;
  }
  50% {
    transform: translateY(-40px) translateX(-10px) scale(0.9);
    opacity: 0.8;
  }
  75% {
    transform: translateY(-15px) translateX(25px) scale(1.2);
    opacity: 0.95;
  }
}

/* 缓慢浮动 */
@keyframes float-slow {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  50% {
    transform: translateY(-30px) translateX(20px);
  }
}

/* 光晕呼吸效果 */
@keyframes glow {
  0%, 100% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

/* 慢速脉冲 */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.6;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.9;
    transform: translate(-50%, -50%) scale(1.05);
  }
}

/* Blob 变形动画 */
@keyframes blob {
  0%, 100% {
    transform: translateY(0) scale(1);
    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  }
  25% {
    transform: translateY(-10px) scale(1.02);
    border-radius: 50% 60% 70% 40% / 50% 60% 30% 60%;
  }
  50% {
    transform: translateY(5px) scale(0.98);
    border-radius: 40% 70% 60% 50% / 40% 50% 60% 50%;
  }
  75% {
    transform: translateY(-5px) scale(1.01);
    border-radius: 70% 40% 50% 60% / 70% 40% 60% 40%;
  }
}

/* 渐变移动 */
@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* 线条移动 */
@keyframes line-move {
  0% {
    stroke-dasharray: 0 1000;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 500 1000;
    stroke-dashoffset: -250;
  }
  100% {
    stroke-dasharray: 0 1000;
    stroke-dashoffset: -1000;
  }
}

/* 浮动旋转 - 暗色模式 */
@keyframes float-spin {
  0%, 100% {
    transform: translateY(0) rotate(45deg);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-25px) rotate(90deg);
    opacity: 0.9;
  }
}

/* 浮动旋转 - 亮色模式 */
@keyframes float-spin-light {
  0%, 100% {
    transform: translateY(0) rotate(12deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-20px) rotate(25deg);
    opacity: 1;
  }
}

/* 波浪动画 */
@keyframes wave {
  0% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-25px);
  }
  100% {
    transform: translateX(0);
  }
}

/* 动画类 */
.animate-float-random {
  animation: float-random ease-in-out infinite;
}

.animate-float-light-random {
  animation: float-light-random ease-in-out infinite;
}

.animate-float-slow {
  animation: float-slow 8s ease-in-out infinite;
}

.animate-glow {
  animation: glow 4s ease-in-out infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 6s ease-in-out infinite;
}

.animate-blob {
  animation: blob 12s ease-in-out infinite;
}

.animate-gradient-shift {
  background-size: 200% 200%;
  animation: gradient-shift 8s ease infinite;
}

.animate-line-move {
  animation: line-move 8s ease-in-out infinite;
}

.animate-float-spin {
  animation: float-spin 8s ease-in-out infinite;
}

.animate-float-spin-light {
  animation: float-spin-light 7s ease-in-out infinite;
}

.animate-wave {
  animation: wave 6s ease-in-out infinite;
}

/* 闪烁星星 */
@keyframes twinkle {
  0%, 100% {
    opacity: 0.6;
    transform: scale(0.9);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

.animate-twinkle {
  animation: twinkle 3s ease-in-out infinite;
}

/* 流动光带 */
@keyframes light-flow {
  0% {
    transform: translateX(-50%) rotate(-5deg);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(50%) rotate(-5deg);
    opacity: 0;
  }
}

.animate-light-flow {
  animation: light-flow 10s ease-in-out infinite;
}
</style>
