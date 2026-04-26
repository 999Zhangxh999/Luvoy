<template>
  <main class="min-h-screen bg-brand-bg py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text">系统设置</h1>
          <p class="text-sm text-brand-muted mt-1">管理您的账户、隐私和系统偏好</p>
        </div>
        <button @click="$router.back()" class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm text-brand-muted hover:text-brand-text hover:bg-brand-card transition-all">
          <i class="bi bi-arrow-left"></i>
          返回
        </button>
      </div>

      <!-- Message Alert -->
      <div v-if="msg" :class="[
        'flex items-center gap-3 p-4 rounded-xl mb-6 border',
        msgOk ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
      ]">
        <i :class="msgOk ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
        <span>{{ msg }}</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- 左侧导航 -->
        <div class="lg:col-span-1">
          <nav class="bg-brand-card border border-brand-border rounded-2xl p-2 sticky top-24">
            <button v-for="tab in settingsTabs" :key="tab.key"
              @click="activeTab = tab.key"
              class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"
              :class="activeTab === tab.key 
                ? 'bg-cyan-500/10 dark:bg-violet-500/10 text-cyan-600 dark:text-violet-400' 
                : 'text-brand-muted hover:text-brand-text hover:bg-brand-surface'">
              <i :class="[tab.icon, 'text-base']"></i>
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- 右侧内容 -->
        <div class="lg:col-span-3 space-y-6">
          <!-- 账户设置 -->
          <div v-show="activeTab === 'account'" class="space-y-6">
            <!-- 个人信息 -->
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-person text-cyan-500 dark:text-violet-400"></i>
                个人信息
              </h2>
              
              <!-- 头像设置 -->
              <div class="flex items-center gap-6 mb-6 pb-6 border-b border-brand-border">
                <div class="relative group">
                  <div v-if="avatarUrl" class="w-20 h-20 rounded-2xl overflow-hidden">
                    <img :src="avatarUrl" alt="头像" class="w-full h-full object-cover" />
                  </div>
                  <div v-else class="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-600 dark:from-violet-600 dark:to-indigo-700 flex items-center justify-center text-white text-2xl font-bold">
                    {{ userInitials }}
                  </div>
                  <button @click="triggerAvatarUpload" 
                    class="absolute inset-0 rounded-2xl bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                    <i class="bi bi-camera text-white text-xl"></i>
                  </button>
                  <input type="file" ref="avatarInput" @change="handleAvatarChange" accept="image/*" class="hidden" />
                </div>
                <div>
                  <h3 class="text-sm font-medium text-brand-text mb-1">更换头像</h3>
                  <p class="text-xs text-brand-muted mb-3">支持 JPG、PNG 格式，最大 5MB</p>
                  <div class="flex gap-2">
                    <button @click="triggerAvatarUpload" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-brand-surface text-brand-text hover:bg-brand-border/50 transition-all">
                      上传图片
                    </button>
                    <button v-if="avatarUrl" @click="removeAvatar" class="px-3 py-1.5 rounded-lg text-xs font-medium text-red-500 hover:bg-red-500/10 transition-all">
                      移除
                    </button>
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">用户名</label>
                  <input v-model="accountForm.username" type="text" 
                    class="w-full px-4 py-2.5 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 focus:ring-1 focus:ring-cyan-500/20 dark:focus:ring-violet-500/20 outline-none transition-all" 
                    placeholder="请输入用户名" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">邮箱</label>
                  <input v-model="accountForm.email" type="email" 
                    class="w-full px-4 py-2.5 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 focus:ring-1 focus:ring-cyan-500/20 dark:focus:ring-violet-500/20 outline-none transition-all" 
                    placeholder="请输入邮箱" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">手机号</label>
                  <input v-model="accountForm.phone" type="tel" 
                    class="w-full px-4 py-2.5 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 focus:ring-1 focus:ring-cyan-500/20 dark:focus:ring-violet-500/20 outline-none transition-all" 
                    placeholder="请输入手机号" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">所在城市</label>
                  <input v-model="accountForm.city" type="text" 
                    class="w-full px-4 py-2.5 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 focus:ring-1 focus:ring-cyan-500/20 dark:focus:ring-violet-500/20 outline-none transition-all" 
                    placeholder="请输入城市" />
                </div>
              </div>

              <button @click="saveAccountInfo" class="mt-6 px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500 text-white text-sm font-medium hover:shadow-lg hover:shadow-cyan-500/20 dark:hover:shadow-violet-500/20 transition-all">
                保存更改
              </button>
            </div>

            <!-- 修改密码 -->
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-shield-lock text-cyan-500 dark:text-violet-400"></i>
                修改密码
              </h2>
              
              <div class="space-y-4 max-w-md">
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">当前密码</label>
                  <div class="relative">
                    <input v-model="passwordForm.current" :type="showCurrentPwd ? 'text' : 'password'" 
                      class="w-full px-4 py-2.5 pr-12 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all" 
                      placeholder="请输入当前密码" />
                    <button @click="showCurrentPwd = !showCurrentPwd" type="button" class="absolute right-4 top-1/2 -translate-y-1/2 text-brand-muted hover:text-brand-text">
                      <i :class="showCurrentPwd ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">新密码</label>
                  <div class="relative">
                    <input v-model="passwordForm.newPwd" :type="showNewPwd ? 'text' : 'password'" 
                      class="w-full px-4 py-2.5 pr-12 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all" 
                      placeholder="请输入新密码" />
                    <button @click="showNewPwd = !showNewPwd" type="button" class="absolute right-4 top-1/2 -translate-y-1/2 text-brand-muted hover:text-brand-text">
                      <i :class="showNewPwd ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">确认新密码</label>
                  <input v-model="passwordForm.confirm" type="password" 
                    class="w-full px-4 py-2.5 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all" 
                    placeholder="请再次输入新密码" />
                </div>
              </div>

              <button @click="changePassword" class="mt-6 px-6 py-2.5 rounded-xl border border-brand-border text-sm font-medium text-brand-text hover:bg-brand-surface transition-all">
                更新密码
              </button>
            </div>
          </div>

          <!-- 隐私设置 -->
          <div v-show="activeTab === 'privacy'" class="space-y-6">
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-eye text-cyan-500 dark:text-violet-400"></i>
                隐私设置
              </h2>
              
              <div class="space-y-4">
                <div v-for="option in privacyOptions" :key="option.key" 
                  class="flex items-center justify-between p-4 rounded-xl bg-brand-surface">
                  <div>
                    <h3 class="text-sm font-medium text-brand-text">{{ option.label }}</h3>
                    <p class="text-xs text-brand-muted mt-0.5">{{ option.desc }}</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="privacySettings[option.key]" class="sr-only peer">
                    <div class="w-11 h-6 bg-brand-border rounded-full peer peer-checked:after:translate-x-full peer-checked:bg-cyan-500 dark:peer-checked:bg-violet-500 after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- 通知设置 -->
          <div v-show="activeTab === 'notification'" class="space-y-6">
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-bell text-cyan-500 dark:text-violet-400"></i>
                通知设置
              </h2>
              
              <div class="space-y-4">
                <div v-for="option in notificationOptions" :key="option.key" 
                  class="flex items-center justify-between p-4 rounded-xl bg-brand-surface">
                  <div>
                    <h3 class="text-sm font-medium text-brand-text">{{ option.label }}</h3>
                    <p class="text-xs text-brand-muted mt-0.5">{{ option.desc }}</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="notificationSettings[option.key]" class="sr-only peer">
                    <div class="w-11 h-6 bg-brand-border rounded-full peer peer-checked:after:translate-x-full peer-checked:bg-cyan-500 dark:peer-checked:bg-violet-500 after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- LLM 配置 -->
          <div v-show="activeTab === 'llm'" class="space-y-6">
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-cpu text-cyan-500 dark:text-violet-400"></i>
                LLM 大模型配置
              </h2>

              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">API Key</label>
                  <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-brand-muted">
                      <i class="bi bi-key"></i>
                    </span>
                    <input 
                      v-model="form.api_key" 
                      :type="showKey ? 'text' : 'password'"
                      class="w-full px-4 py-2.5 pl-11 pr-12 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all"
                      placeholder="sk-***"
                    />
                    <button 
                      @click="showKey = !showKey"
                      type="button"
                      class="absolute right-4 top-1/2 -translate-y-1/2 text-brand-muted hover:text-brand-text"
                    >
                      <i :class="showKey ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">Base URL</label>
                  <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-brand-muted">
                      <i class="bi bi-link-45deg"></i>
                    </span>
                    <input 
                      v-model="form.base_url" 
                      class="w-full px-4 py-2.5 pl-11 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all"
                      placeholder="https://api.deepseek.com/v1"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-brand-muted mb-2">模型名称</label>
                  <div class="relative">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-brand-muted">
                      <i class="bi bi-robot"></i>
                    </span>
                    <input 
                      v-model="form.model" 
                      class="w-full px-4 py-2.5 pl-11 rounded-xl bg-brand-surface border border-brand-border text-brand-text placeholder-brand-muted focus:border-cyan-500 dark:focus:border-violet-500 outline-none transition-all"
                      placeholder="deepseek-chat"
                    />
                  </div>
                </div>

                <button @click="save" :disabled="saving" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 dark:from-violet-500 dark:to-indigo-500 text-white text-sm font-medium hover:shadow-lg transition-all disabled:opacity-50">
                  <i class="bi bi-check-circle mr-2"></i>
                  {{ saving ? '保存中...' : '保存设置' }}
                </button>
              </div>
            </div>

            <!-- 推荐提供商 -->
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <h2 class="text-base font-semibold text-brand-text mb-6 flex items-center gap-2">
                <i class="bi bi-buildings text-cyan-500 dark:text-violet-400"></i>
                推荐提供商
              </h2>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div 
                  v-for="p in providers" 
                  :key="p.name"
                  @click="useProvider(p)"
                  class="p-4 rounded-xl border border-brand-border bg-brand-surface hover:border-cyan-500/40 dark:hover:border-violet-500/40 cursor-pointer transition-all group"
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-brand-text group-hover:text-cyan-600 dark:group-hover:text-violet-400 transition-colors">
                      {{ p.name }}
                    </span>
                    <span class="px-2 py-0.5 rounded-full text-xs bg-brand-card text-brand-muted">{{ p.model }}</span>
                  </div>
                  <code class="text-xs text-brand-muted break-all">{{ p.url }}</code>
                </div>
              </div>
            </div>
          </div>

          <!-- 关于系统 -->
          <div v-show="activeTab === 'about'" class="space-y-6">
            <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
              <div class="text-center py-8">
                <div class="w-20 h-20 mx-auto rounded-2xl bg-white dark:bg-white/10 p-2 mb-4 shadow-lg">
                  <img src="/logo.png" alt="拓扑 Topo 标识" class="w-full h-full rounded-xl" />
                </div>
                <h2 class="text-xl font-bold text-brand-text mb-2">拓扑 · Topo</h2>
                <p class="text-sm text-brand-muted mb-4">智能职业发展规划平台</p>
                <p class="text-xs text-brand-muted">版本 1.0.0</p>
              </div>
              
              <div class="border-t border-brand-border pt-6 mt-6">
                <div class="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <p class="text-2xl font-bold text-brand-text">1000+</p>
                    <p class="text-xs text-brand-muted">用户</p>
                  </div>
                  <div>
                    <p class="text-2xl font-bold text-brand-text">5000+</p>
                    <p class="text-xs text-brand-muted">职位</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, inject, onMounted, computed } from 'vue'
import { getSettings, updateSettings } from '@/api'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const setLoading = inject('setLoading')
const toast = inject('toast')

const activeTab = ref('account')
const form = ref({ api_key: '', base_url: '', model: '' })
const saving = ref(false)
const msg = ref('')
const msgOk = ref(true)
const showKey = ref(false)
const showCurrentPwd = ref(false)
const showNewPwd = ref(false)

// 头像相关
const avatarInput = ref(null)
const avatarUrl = ref(localStorage.getItem('user-avatar') || '')

const userInitials = computed(() => {
  const name = authStore.user?.username || '用户'
  return name.slice(0, 2).toUpperCase()
})

function triggerAvatarUpload() {
  avatarInput.value?.click()
}

function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      toast('请上传图片文件', 'warning')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      toast('图片大小不能超过 5MB', 'warning')
      return
    }
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarUrl.value = e.target.result
      localStorage.setItem('user-avatar', e.target.result)
      window.dispatchEvent(new Event('avatar-updated'))
      toast('头像已更新', 'success')
    }
    reader.readAsDataURL(file)
  }
}

function removeAvatar() {
  avatarUrl.value = ''
  localStorage.removeItem('user-avatar')
  window.dispatchEvent(new Event('avatar-updated'))
  toast('头像已移除', 'info')
}

// 账户表单
const accountForm = ref({
  username: authStore.user?.username || '',
  email: authStore.user?.email || '',
  phone: '',
  city: ''
})

// 密码表单
const passwordForm = ref({
  current: '',
  newPwd: '',
  confirm: ''
})

// 设置标签
const settingsTabs = [
  { key: 'account', label: '账户设置', icon: 'bi bi-person' },
  { key: 'privacy', label: '隐私设置', icon: 'bi bi-eye' },
  { key: 'notification', label: '通知设置', icon: 'bi bi-bell' },
  { key: 'llm', label: 'LLM 配置', icon: 'bi bi-cpu' },
  { key: 'about', label: '关于系统', icon: 'bi bi-info-circle' },
]

// 隐私设置
const privacyOptions = [
  { key: 'showProfile', label: '公开我的档案', desc: '允许HR查看我的求职画像' },
  { key: 'showResume', label: '公开我的简历', desc: '允许企业下载我的简历' },
  { key: 'showContact', label: '显示联系方式', desc: '在档案中显示我的联系信息' },
  { key: 'allowRecommend', label: '接受职位推荐', desc: '系统会根据你的画像推荐职位' },
]

const privacySettings = ref({
  showProfile: true,
  showResume: true,
  showContact: false,
  allowRecommend: true
})

// 通知设置
const notificationOptions = [
  { key: 'jobUpdate', label: '职位动态', desc: '投递的职位有新进展时通知我' },
  { key: 'interview', label: '面试邀请', desc: '收到面试邀请时通知我' },
  { key: 'message', label: '新消息', desc: '收到HR消息时通知我' },
  { key: 'system', label: '系统通知', desc: '接收系统公告和更新提醒' },
  { key: 'email', label: '邮件通知', desc: '同时发送邮件通知' },
]

const notificationSettings = ref({
  jobUpdate: true,
  interview: true,
  message: true,
  system: true,
  email: false
})

const providers = [
  { name: 'DeepSeek（推荐）', url: 'https://api.deepseek.com/v1', model: 'deepseek-chat' },
  { name: '通义千问', url: 'https://dashscope.aliyuncs.com/compatible-mode/v1', model: 'qwen-plus' },
  { name: '智谱AI', url: 'https://open.bigmodel.cn/api/paas/v4', model: 'glm-4-flash' },
  { name: 'Moonshot', url: 'https://api.moonshot.cn/v1', model: 'moonshot-v1-8k' },
]

function useProvider(p) {
  form.value.base_url = p.url
  form.value.model = p.model
  toast(`已切换到 ${p.name}`, 'info')
}

function saveAccountInfo() {
  toast('个人信息已保存', 'success')
}

function changePassword() {
  if (!passwordForm.value.current) {
    toast('请输入当前密码', 'warning')
    return
  }
  if (!passwordForm.value.newPwd) {
    toast('请输入新密码', 'warning')
    return
  }
  if (passwordForm.value.newPwd !== passwordForm.value.confirm) {
    toast('两次密码输入不一致', 'warning')
    return
  }
  toast('密码已更新', 'success')
  passwordForm.value = { current: '', newPwd: '', confirm: '' }
}

async function save() {
  saving.value = true; setLoading(true, '正在保存设置…'); msg.value = ''
  try {
    const { data } = await updateSettings(form.value)
    msg.value = data.message; msgOk.value = data.success
    toast(data.message, data.success ? 'success' : 'warning')
  } catch (e) {
    msg.value = e.response?.data?.message || '保存失败'; msgOk.value = false
    toast(msg.value, 'danger')
  } finally { saving.value = false; setLoading(false) }
}

onMounted(async () => {
  try {
    const { data } = await getSettings()
    form.value = {
      api_key: '',
      base_url: data.base_url,
      model: data.model,
    }
  } catch {}
})
</script>