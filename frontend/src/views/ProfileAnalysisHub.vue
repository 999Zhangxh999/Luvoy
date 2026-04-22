<template>
  <div class="min-h-screen bg-brand-bg">
    <!-- 顶部标题区 -->
    <div class="profile-header">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center">
          <h1 class="text-3xl md:text-4xl font-bold mb-3 animate-fade-in">
            <span class="gradient-text">画像分析</span>
            <span class="text-brand-text ml-2">中心</span>
          </h1>
          <p class="text-brand-muted text-sm md:text-base max-w-2xl mx-auto">
            多维度解析岗位需求与个人能力，AI智能协助精准定位差距，制定个性化成长策略
          </p>
        </div>

        <!-- Tab导航 -->
        <div class="tab-navigation mt-8">
          <div class="tab-container">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="['tab-item', { active: activeTab === tab.id }]"
            >
              <span class="tab-icon"><i :class="tab.icon"></i></span>
              <span class="tab-label">{{ tab.label }}</span>
              <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
            </button>
          </div>
          <div class="tab-indicator" :style="indicatorStyle"></div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pb-12">
      <transition name="tab-fade" mode="out-in">
        <!-- 岗位画像 -->
        <div v-if="activeTab === 'job'" key="job" class="tab-content">
          <JobProfilePanel 
            :job-profiles="jobProfiles"
            :selected-id="selectedJobId"
            :loading="loadingJobs"
            @select="handleJobSelect"
            @analyze="handleJobAnalyze"
          />
        </div>

        <!-- 个人画像 -->
        <div v-else-if="activeTab === 'personal'" key="personal" class="tab-content">
          <PersonalProfilePanel 
            :students="students"
            :selected-id="selectedStudentId"
            :profile="studentProfile"
            :loading="loadingStudents"
            @select="handleStudentSelect"
            @generate="handleGenerateProfile"
            @analyze="handlePersonalAnalyze"
          />
        </div>

        <!-- 画像对比 -->
        <div v-else-if="activeTab === 'compare'" key="compare" class="tab-content">
          <ProfileComparePanel 
            :students="students"
            :job-profiles="jobProfiles"
            :student-profile="studentProfile"
            :selected-student-id="selectedStudentId"
            :selected-job-id="selectedJobId"
            :match-result="matchResult"
            :matching="matching"
            @select-student="handleStudentSelect"
            @select-job="handleJobSelect"
            @compare="handleCompare"
          />
        </div>
      </transition>
    </div>

    <!-- AI助手 -->
    <ProfileAIAssistant 
      :context-mode="activeTab"
      :job-profile="selectedJobProfile"
      :personal-profile="studentProfile"
      :comparison-result="matchResult"
      :skills="currentSkills"
      @analyze="handleAIAnalyze"
      @improve="handleAIImprove"
      @navigate="handleAINavigate"
      @generateSuggestion="handleAISuggestion"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { inject } from 'vue'
import {
  getJobProfiles,
  getStudent,
  getStudents,
  runSingleMatching,
  generateStudentProfile as apiGenerateProfile,
} from '@/api'
import ProfileAIAssistant from '@/components/ProfileAIAssistant.vue'
import JobProfilePanel from './profile/JobProfilePanel.vue'
import PersonalProfilePanel from './profile/PersonalProfilePanel.vue'
import ProfileComparePanel from './profile/ProfileComparePanel.vue'

const toast = inject('toast', null)

// Tab配置
const tabs = [
  { id: 'job', label: '岗位画像', icon: 'bi bi-briefcase-fill' },
  { id: 'personal', label: '个人画像', icon: 'bi bi-person-fill' },
  { id: 'compare', label: '画像对比', icon: 'bi bi-arrow-left-right', badge: 'AI' }
]

const activeTab = ref('job')

// Tab指示器位置
const indicatorStyle = computed(() => {
  const index = tabs.findIndex(t => t.id === activeTab.value)
  return {
    transform: `translateX(${index * 100}%)`,
    width: `${100 / tabs.length}%`
  }
})

// 数据状态
const jobProfiles = ref([])
const students = ref([])
const selectedJobId = ref('')
const selectedStudentId = ref('')
const studentProfile = ref(null)
const matchResult = ref(null)

const loadingJobs = ref(false)
const loadingStudents = ref(false)
const matching = ref(false)
const generatingProfile = ref(false)

// 计算属性
const selectedJobProfile = computed(() => 
  jobProfiles.value.find(p => String(p.id) === String(selectedJobId.value)) || null
)

const currentSkills = computed(() => {
  if (activeTab.value === 'job') {
    return selectedJobProfile.value?.technical_skills || []
  } else if (activeTab.value === 'personal') {
    return studentProfile.value?.technical_skills || []
  }
  return []
})

// 事件处理
function handleJobSelect(id) {
  selectedJobId.value = id
}

async function handleStudentSelect(id) {
  selectedStudentId.value = id
  studentProfile.value = null
  matchResult.value = null
  
  if (!id) return
  
  try {
    const response = await getStudent(id)
    studentProfile.value = response.data?.profile || null
  } catch (error) {
    toast?.(error?.response?.data?.message || '加载学生画像失败', 'danger')
  }
}

function handleJobAnalyze(data) {
  console.log('Job analyze:', data)
}

function handlePersonalAnalyze(data) {
  console.log('Personal analyze:', data)
}

async function handleGenerateProfile(studentId) {
  if (!studentId) return
  generatingProfile.value = true
  try {
    const response = await apiGenerateProfile(studentId)
    if (response.data?.success) {
      studentProfile.value = response.data.data
      toast?.('学生画像生成成功', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '学生画像生成失败', 'danger')
  } finally {
    generatingProfile.value = false
  }
}

async function handleCompare() {
  if (!selectedStudentId.value || !selectedJobId.value) {
    toast?.('请先选择学生和目标岗位', 'warning')
    return
  }
  
  matching.value = true
  try {
    const response = await runSingleMatching(selectedStudentId.value, selectedJobId.value)
    if (response.data?.success) {
      matchResult.value = response.data.data
      toast?.('画像对比分析完成', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '画像对比分析失败', 'danger')
  } finally {
    matching.value = false
  }
}

// AI事件处理
function handleAIAnalyze(data) {
  console.log('AI analyze:', data)
}

function handleAIImprove(data) {
  console.log('AI improve:', data)
}

function handleAINavigate(data) {
  if (data.target === 'compare') {
    activeTab.value = 'compare'
  }
}

function handleAISuggestion(data) {
  console.log('AI suggestion:', data)
}

// 数据加载
async function loadBaseData() {
  loadingJobs.value = true
  loadingStudents.value = true
  
  try {
    const [jobsRes, studentsRes] = await Promise.all([
      getJobProfiles(),
      getStudents()
    ])
    jobProfiles.value = jobsRes.data?.profiles || []
    students.value = studentsRes.data || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '数据加载失败', 'danger')
  } finally {
    loadingJobs.value = false
    loadingStudents.value = false
  }
}

// 清除对比结果当切换tab
watch(activeTab, (newVal) => {
  if (newVal !== 'compare') {
    matchResult.value = null
  }
})

onMounted(() => {
  loadBaseData()
})
</script>

<style scoped>
.profile-header {
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.08) 0%, transparent 100%);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.gradient-text {
  background: var(--gradient-text-bg, linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #10b981 100%));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Tab导航 */
.tab-navigation {
  position: relative;
  max-width: 480px;
  margin: 0 auto;
}

.tab-container {
  display: flex;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 16px;
  padding: 6px;
  position: relative;
  z-index: 1;
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.tab-item .tab-icon {
  font-size: 16px;
  color: #64748b;
  transition: color 0.3s;
}

.tab-item .tab-label {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  transition: color 0.3s;
}

.tab-item .tab-badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 6px;
  background: var(--btn-primary-gradient, linear-gradient(135deg, #8b5cf6, #06b6d4));
  color: white;
  font-weight: 600;
}

.tab-item.active .tab-icon,
.tab-item.active .tab-label {
  color: white;
}

.tab-item:hover:not(.active) .tab-icon,
.tab-item:hover:not(.active) .tab-label {
  color: #a78bfa;
}

.tab-indicator {
  position: absolute;
  top: 6px;
  left: 6px;
  height: calc(100% - 12px);
  background: var(--btn-primary-gradient, linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%));
  border-radius: 12px;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 0;
  box-shadow: 0 4px 15px rgba(var(--brand-primary-rgb, 139, 92, 246), 0.4);
}

/* Tab内容切换动画 */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: all 0.3s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.tab-content {
  animation: contentFade 0.4s ease-out;
}

@keyframes contentFade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式 */
@media (max-width: 640px) {
  .tab-item .tab-label {
    display: none;
  }
  
  .tab-item .tab-icon {
    font-size: 20px;
  }
  
  .tab-navigation {
    max-width: 200px;
  }
}
</style>
