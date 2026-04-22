<template>
  <main class="min-h-screen py-16 px-4 sm:px-6 lg:px-8 animate-fade-up">
    <div class="max-w-7xl mx-auto">
      <!-- Hero Section -->
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold text-white mb-3">
          发现你的 <span class="text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-cyan-400">理想工作</span>
        </h1>
        <p class="text-slate-400 mb-8">{{ total }} 个精选岗位等你探索</p>
        
        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto relative">
          <div class="flex bg-slate-800/80 backdrop-blur-xl rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl shadow-violet-500/10">
            <div class="flex-1 flex items-center px-5">
              <i class="bi bi-search text-violet-400 text-lg"></i>
              <input
                v-model="search"
                type="text"
                placeholder="搜索职位、公司、技能..."
                class="flex-1 bg-transparent border-none py-4 px-4 text-white placeholder:text-slate-500 focus:outline-none"
                @keyup.enter="applyFilters"
              />
            </div>
            <button 
              @click="applyFilters"
              class="px-8 py-4 bg-gradient-to-r from-violet-600 to-violet-500 text-white font-medium hover:from-violet-500 hover:to-violet-400 transition-all"
            >
              搜索
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Filter Tags -->
      <div class="flex flex-wrap justify-center gap-3 mb-8">
        <button 
          v-for="tag in quickTags" 
          :key="tag"
          @click="quickSearch(tag)"
          :class="[
            'px-4 py-2 rounded-full text-sm transition-all duration-200',
            search === tag 
              ? 'bg-violet-600 text-white shadow-lg shadow-violet-500/30' 
              : 'bg-slate-800/50 text-slate-400 border border-slate-700/50 hover:border-violet-500/50 hover:text-violet-300'
          ]"
        >
          {{ tag }}
        </button>
      </div>

      <!-- Filters Bar -->
      <div class="flex items-center justify-between gap-4 mb-6 py-3 px-4 rounded-xl bg-slate-800/30">
        <div class="flex items-center gap-4 flex-wrap">
          <!-- Industry Filter -->
          <div class="relative group">
            <button 
              @click="showIndustryDropdown = !showIndustryDropdown"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-colors"
              :class="industryFilter ? 'bg-violet-600/20 text-violet-300 border border-violet-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-600'"
            >
              <i class="bi bi-building"></i>
              {{ industryFilter || '行业' }}
              <i class="bi bi-chevron-down text-xs"></i>
            </button>
            <div v-if="showIndustryDropdown" class="absolute top-full left-0 mt-2 w-48 py-2 bg-slate-800 rounded-lg border border-slate-700 shadow-xl z-50">
              <button @click="industryFilter = ''; showIndustryDropdown = false; applyFilters()" class="w-full px-4 py-2 text-left text-sm text-slate-400 hover:bg-slate-700/50 hover:text-white">全部行业</button>
              <button v-for="ind in industries" :key="ind" @click="industryFilter = ind; showIndustryDropdown = false; applyFilters()" class="w-full px-4 py-2 text-left text-sm text-slate-400 hover:bg-slate-700/50 hover:text-white">{{ ind }}</button>
            </div>
          </div>

          <!-- City Filter -->
          <div class="relative">
            <button 
              @click="showCityDropdown = !showCityDropdown"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-colors"
              :class="cityFilter ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-600'"
            >
              <i class="bi bi-geo-alt"></i>
              {{ cityFilter || '城市' }}
              <i class="bi bi-chevron-down text-xs"></i>
            </button>
            <div v-if="showCityDropdown" class="absolute top-full left-0 mt-2 w-40 py-2 bg-slate-800 rounded-lg border border-slate-700 shadow-xl z-50">
              <button @click="cityFilter = ''; showCityDropdown = false; applyFilters()" class="w-full px-4 py-2 text-left text-sm text-slate-400 hover:bg-slate-700/50 hover:text-white">全部城市</button>
              <button v-for="city in cities" :key="city" @click="cityFilter = city; showCityDropdown = false; applyFilters()" class="w-full px-4 py-2 text-left text-sm text-slate-400 hover:bg-slate-700/50 hover:text-white">{{ city }}</button>
            </div>
          </div>

          <!-- Salary Filter -->
          <div class="relative">
            <button 
              @click="showSalaryDropdown = !showSalaryDropdown"
              class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-colors"
              :class="selectedSalary && selectedSalary !== '不限' ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-600'"
            >
              <i class="bi bi-cash"></i>
              {{ selectedSalary === '不限' ? '薪资' : selectedSalary }}
              <i class="bi bi-chevron-down text-xs"></i>
            </button>
            <div v-if="showSalaryDropdown" class="absolute top-full left-0 mt-2 w-36 py-2 bg-slate-800 rounded-lg border border-slate-700 shadow-xl z-50">
              <button v-for="range in salaryRanges" :key="range" @click="selectedSalary = range; showSalaryDropdown = false; applyFilters()" class="w-full px-4 py-2 text-left text-sm text-slate-400 hover:bg-slate-700/50 hover:text-white">{{ range }}</button>
            </div>
          </div>

          <!-- Clear Filters -->
          <button v-if="hasActiveFilters" @click="clearAllFilters" class="text-sm text-slate-500 hover:text-violet-400 transition-colors">
            <i class="bi bi-x-circle mr-1"></i>清除筛选
          </button>
        </div>

        <!-- Sort -->
        <div class="flex items-center gap-2 text-sm text-slate-400">
          <span>排序:</span>
          <button 
            @click="sortBy = 'latest'" 
            :class="sortBy === 'latest' ? 'text-violet-400' : 'hover:text-white'"
          >最新</button>
          <span class="text-slate-600">|</span>
          <button 
            @click="sortBy = 'salary'" 
            :class="sortBy === 'salary' ? 'text-violet-400' : 'hover:text-white'"
          >薪资</button>
        </div>
      </div>

      <!-- Job Cards -->
      <div class="grid md:grid-cols-2 gap-4">
        <div
          v-for="j in jobs"
          :key="j.id"
          @click="goToJobDetail(j)"
          class="group relative p-5 rounded-2xl bg-gradient-to-br from-slate-800/80 to-slate-800/40 border border-slate-700/50 hover:border-violet-500/40 hover:shadow-lg hover:shadow-violet-500/10 cursor-pointer transition-all duration-300 hover:-translate-y-1"
        >
          <!-- Top Row -->
          <div class="flex justify-between items-start mb-3">
            <div class="flex-1 min-w-0">
              <h3 class="text-lg font-semibold text-white group-hover:text-violet-300 transition-colors truncate pr-4">
                {{ j.title }}
              </h3>
              <p class="text-sm text-slate-500 mt-1">
                {{ j.company_name || '企业' }}
              </p>
            </div>
            <div class="text-right">
              <div class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
                {{ j.salary_range || '面议' }}
              </div>
            </div>
          </div>

          <!-- Tags Row -->
          <div class="flex flex-wrap items-center gap-2 mb-3">
            <span v-if="j.address" class="inline-flex items-center gap-1 text-xs text-slate-400">
              <i class="bi bi-geo-alt"></i>{{ j.address }}
            </span>
            <span v-if="j.experience" class="px-2 py-0.5 rounded bg-slate-700/50 text-xs text-slate-400">{{ j.experience }}</span>
            <span v-if="j.education" class="px-2 py-0.5 rounded bg-slate-700/50 text-xs text-slate-400">{{ j.education }}</span>
          </div>

          <!-- Bottom Row -->
          <div class="flex items-center justify-between pt-3 border-t border-slate-700/50">
            <div class="flex items-center gap-2">
              <span v-if="j.industry" class="px-2 py-1 rounded-md text-xs bg-violet-500/10 text-violet-300 border border-violet-500/20">
                {{ j.industry }}
              </span>
              <span v-if="j.company_size" class="text-xs text-slate-500">{{ j.company_size }}</span>
            </div>
            <div class="flex items-center text-xs text-slate-500 group-hover:text-violet-400 transition-colors">
              查看详情 <i class="bi bi-arrow-right ml-1"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!jobs.length && !loading" class="text-center py-24">
        <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-slate-800/50 flex items-center justify-center">
          <i class="bi bi-search text-4xl text-slate-600"></i>
        </div>
        <h3 class="text-xl text-slate-300 mb-2">暂无匹配的岗位</h3>
        <p class="text-slate-500">试试其他关键词或筛选条件</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-24">
        <div class="inline-block w-10 h-10 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-slate-400">加载中...</p>
      </div>

      <!-- Pagination -->
      <div v-if="pages > 1 && !loading" class="mt-10 flex items-center justify-center gap-3">
        <button 
          :disabled="page === 1"
          @click="changePage(page - 1)"
          class="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:border-violet-500 hover:text-violet-400 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          <i class="bi bi-chevron-left"></i>
        </button>
        
        <div class="flex gap-2">
          <button
            v-for="p in visiblePages"
            :key="p"
            @click="changePage(p)"
            :class="[
              'w-10 h-10 rounded-xl text-sm font-medium transition-all',
              p === page 
                ? 'bg-gradient-to-r from-violet-600 to-violet-500 text-white shadow-lg shadow-violet-500/30' 
                : 'bg-slate-800 border border-slate-700 text-slate-400 hover:border-violet-500 hover:text-violet-400'
            ]"
          >
            {{ p }}
          </button>
        </div>
        
        <button 
          :disabled="page === pages"
          @click="changePage(page + 1)"
          class="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:border-violet-500 hover:text-violet-400 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          <i class="bi bi-chevron-right"></i>
        </button>
        
        <span class="text-slate-500 text-sm ml-4">第 {{ page }} / {{ pages }} 页</span>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getJobs } from '@/api'

const router = useRouter()
const route = useRoute()

const allJobs = ref([])
const jobs = ref([])
const search = ref('')
const page = ref(1)
const pages = ref(1)
const total = ref(0)
const loading = ref(false)
const sortBy = ref('latest')

// Filter values
const industryFilter = ref('')
const cityFilter = ref('')
const selectedSalary = ref('不限')

// Dropdown states
const showIndustryDropdown = ref(false)
const showCityDropdown = ref(false)
const showSalaryDropdown = ref(false)

// Quick search tags
const quickTags = ['前端开发', '后端开发', '产品经理', '数据分析', 'UI设计', '运营', '人工智能', '测试']

const industries = ['互联网', '电商', '金融', '教育', '医疗', '制造', '计算机软件', 'IT服务', '通信', '人工智能']
const salaryRanges = ['不限', '5K以下', '5-10K', '10-20K', '20-30K', '30K以上']
const cities = ['北京', '上海', '深圳', '杭州', '广州', '成都', '武汉', '南京', '西安', '东莞']

const visiblePages = computed(() => {
  const all = []
  const start = Math.max(1, page.value - 2)
  const end = Math.min(pages.value, page.value + 2)
  for (let i = start; i <= end; i++) all.push(i)
  return all
})

// 是否有活跃筛选条件
const hasActiveFilters = computed(() => {
  return search.value || industryFilter.value || cityFilter.value || (selectedSalary.value && selectedSalary.value !== '不限')
})

// 快速搜索
function quickSearch(tag) {
  search.value = search.value === tag ? '' : tag
  applyFilters()
}

// 点击职位卡片跳转
function goToJobDetail(job) {
  router.push(`/jobs/profiles/${job.id}`)
}

// 解析薪资数值
function parseSalary(salaryStr) {
  if (!salaryStr) return 0
  const match = salaryStr.match(/(\d+(?:\.\d+)?)/g)
  if (match && match.length) {
    const nums = match.map(Number)
    return nums.reduce((a, b) => a + b, 0) / nums.length
  }
  return 0
}

// 薪资筛选判断
function matchSalaryRange(salary, range) {
  if (!range || range === '不限') return true
  const val = parseSalary(salary)
  if (range === '5K以下') return val < 5
  if (range === '5-10K') return val >= 5 && val < 10
  if (range === '10-20K') return val >= 10 && val < 20
  if (range === '20-30K') return val >= 20 && val < 30
  if (range === '30K以上') return val >= 30
  return true
}

// 应用筛选和排序
function applyFilters() {
  // Close all dropdowns
  showIndustryDropdown.value = false
  showCityDropdown.value = false
  showSalaryDropdown.value = false
  
  let filtered = [...allJobs.value]
  
  // 搜索
  if (search.value.trim()) {
    const q = search.value.trim().toLowerCase()
    filtered = filtered.filter(j => 
      (j.title || '').toLowerCase().includes(q) ||
      (j.company_name || '').toLowerCase().includes(q) ||
      (j.address || '').toLowerCase().includes(q) ||
      (j.industry || '').toLowerCase().includes(q) ||
      (j.description || '').toLowerCase().includes(q)
    )
  }
  
  // 行业筛选
  if (industryFilter.value) {
    filtered = filtered.filter(j => 
      (j.industry || '').toLowerCase().includes(industryFilter.value.toLowerCase())
    )
  }
  
  // 城市筛选
  if (cityFilter.value) {
    filtered = filtered.filter(j => 
      (j.address || '').toLowerCase().includes(cityFilter.value.toLowerCase())
    )
  }
  
  // 薪资筛选
  if (selectedSalary.value && selectedSalary.value !== '不限') {
    filtered = filtered.filter(j => matchSalaryRange(j.salary_range, selectedSalary.value))
  }
  
  // 排序
  if (sortBy.value === 'salary') {
    filtered.sort((a, b) => parseSalary(b.salary_range) - parseSalary(a.salary_range))
  }
  
  total.value = filtered.length
  pages.value = Math.max(1, Math.ceil(filtered.length / 20))
  page.value = Math.min(page.value, pages.value)
  
  // 分页
  const start = (page.value - 1) * 20
  jobs.value = filtered.slice(start, start + 20)
}

function clearAllFilters() {
  industryFilter.value = ''
  cityFilter.value = ''
  selectedSalary.value = '不限'
  search.value = ''
  page.value = 1
  applyFilters()
}

// 监听筛选器变化
watch([industryFilter, cityFilter, selectedSalary, sortBy], () => {
  page.value = 1
  applyFilters()
}, { deep: true })

async function loadJobs(p = 1) {
  loading.value = true
  page.value = p
  try {
    const { data } = await getJobs({ page: 1, per_page: 10000, search: '' })
    allJobs.value = data.items || []
    applyFilters()
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  applyFilters()
}

onMounted(() => {
  if (route.query.q) {
    search.value = route.query.q
  }
  loadJobs()
})
</script>
