<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold mb-3">
          <span class="gradient-text">画像</span>
          <span class="text-brand-text ml-2">分析中心</span>
        </h1>
        <p class="text-brand-muted text-sm md:text-base">多维度解析岗位需求与个人能力，精准定位差距，制定成长策略</p>
      </div>

      <!-- 画像类型切换 -->
      <div class="flex justify-center gap-4 mb-8">
        <button 
          @click="activeTab = 'job'"
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200',
            activeTab === 'job' 
              ? 'btn-primary' 
              : 'bg-brand-card border border-brand-border text-brand-muted hover:text-brand-text hover:border-brand-primary/50'
          ]"
        >
          <i class="bi bi-briefcase"></i>
          岗位画像
        </button>
        <button 
          @click="activeTab = 'user'"
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200',
            activeTab === 'user' 
              ? 'btn-primary' 
              : 'bg-brand-card border border-brand-border text-brand-muted hover:text-brand-text hover:border-brand-primary/50'
          ]"
        >
          <i class="bi bi-person"></i>
          用户能力画像
        </button>
      </div>

      <!-- 筛选栏 -->
      <div class="flex flex-wrap items-center justify-center gap-3 mb-6">
        <button 
          v-for="filter in filterTabs" 
          :key="filter.key"
          @click="activeFilter = filter.key"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-all',
            activeFilter === filter.key 
              ? 'bg-brand-primary/20 text-brand-primary border border-brand-primary/30'
              : 'bg-brand-surface border border-brand-border text-brand-muted hover:text-brand-text'
          ]"
        >
          <i :class="filter.icon" class="mr-1.5"></i>
          {{ filter.label }}
        </button>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div v-for="stat in statsCards" :key="stat.label" 
             class="bg-brand-card border border-brand-border rounded-2xl p-5 text-center hover:border-brand-primary/30 transition-all">
          <div class="text-3xl md:text-4xl font-bold gradient-text mb-1">{{ stat.value }}</div>
          <div class="text-xs text-brand-muted mb-2">{{ stat.label }}</div>
          <div :class="stat.trend > 0 ? 'text-emerald-500' : 'text-red-400'" class="text-xs font-medium">
            <i :class="stat.trend > 0 ? 'bi bi-arrow-up-right' : 'bi bi-arrow-down-right'" class="mr-1"></i>
            {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}% 环比
          </div>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 岗位能力雷达图 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-bullseye text-brand-primary"></i>
              岗位能力雷达
            </h3>
            <span class="badge-cyan text-xs">前端工程师</span>
          </div>
          <div class="h-[280px]">
            <RadarChart :series="radarSeries" :indicators="radarIndicators" height="280px" />
          </div>
        </div>

        <!-- 薪资区间分布 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-currency-dollar text-emerald-400"></i>
              薪资区间分布
            </h3>
            <button class="badge text-xs cursor-pointer hover:bg-brand-primary/30 transition-all">全部数据</button>
          </div>
          <div class="space-y-3">
            <div v-for="item in salaryRanges" :key="item.range" class="flex items-center gap-3">
              <span class="w-16 text-xs text-brand-muted text-right">{{ item.range }}</span>
              <div class="flex-1 h-6 bg-brand-surface rounded-lg overflow-hidden relative">
                <div 
                  class="h-full rounded-lg transition-all duration-500"
                  :class="item.color"
                  :style="{ width: item.percent + '%' }"
                ></div>
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs font-medium text-brand-text">
                  {{ item.percent }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 技能需求热度 & 招聘要求分布 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 技能需求热度 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-fire text-orange-400"></i>
              技能需求热度
            </h3>
            <span class="text-xs text-brand-muted">基于 10,000+ 份 JD 分析</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="skill in skillHotTags" 
              :key="skill.name"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium cursor-pointer transition-all hover:scale-105',
                skill.hot ? 'bg-brand-primary/20 text-brand-primary border border-brand-primary/30' : 'bg-brand-surface text-brand-muted border border-brand-border'
              ]"
            >
              {{ skill.name }}
            </span>
          </div>
          <div class="mt-4 flex flex-wrap gap-4 text-xs text-brand-muted">
            <span class="flex items-center gap-1">
              <span class="w-3 h-3 rounded bg-brand-primary/30"></span> 热门
            </span>
            <span class="flex items-center gap-1">
              <span class="w-3 h-3 rounded bg-cyan-500/30"></span> 主流
            </span>
            <span class="flex items-center gap-1">
              <span class="w-3 h-3 rounded bg-brand-surface"></span> 常见
            </span>
          </div>
        </div>

        <!-- 招聘要求分布 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-pie-chart text-violet-400"></i>
              招聘要求分布
            </h3>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <!-- 学历要求 -->
            <div>
              <div class="text-xs text-brand-muted mb-2">学历要求</div>
              <div class="relative w-24 h-24 mx-auto">
                <svg viewBox="0 0 100 100" class="w-full h-full -rotate-90">
                  <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="20" 
                          class="text-brand-surface" />
                  <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="20"
                          class="text-brand-primary" 
                          :stroke-dasharray="`${68 * 2.2} 220`"
                          stroke-linecap="round" />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-lg font-bold text-brand-primary">68%</span>
                </div>
              </div>
              <div class="mt-2 space-y-1 text-xs">
                <div class="flex justify-between"><span class="text-brand-muted">本科及以上</span><span class="text-brand-text">68%</span></div>
                <div class="flex justify-between"><span class="text-brand-muted">大专</span><span class="text-brand-text">12%</span></div>
                <div class="flex justify-between"><span class="text-brand-muted">硕士优先</span><span class="text-brand-text">18%</span></div>
              </div>
            </div>
            <!-- 经验要求 -->
            <div>
              <div class="text-xs text-brand-muted mb-2">经验要求</div>
              <div class="relative w-24 h-24 mx-auto">
                <svg viewBox="0 0 100 100" class="w-full h-full -rotate-90">
                  <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="20" 
                          class="text-brand-surface" />
                  <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="20"
                          class="text-cyan-500" 
                          :stroke-dasharray="`${18 * 2.2} 220`"
                          stroke-linecap="round" />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-lg font-bold text-cyan-500">18%</span>
                </div>
              </div>
              <div class="mt-2 space-y-1 text-xs">
                <div class="flex justify-between"><span class="text-brand-muted">1-3年</span><span class="text-brand-text">42%</span></div>
                <div class="flex justify-between"><span class="text-brand-muted">3-5年</span><span class="text-brand-text">30%</span></div>
                <div class="flex justify-between"><span class="text-brand-muted">应届生</span><span class="text-brand-text">18%</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 行业分布 & 城市需求 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 所属行业分布 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-building text-brand-primary"></i>
              所属行业分布
            </h3>
          </div>
          <div class="space-y-3">
            <div v-for="item in industryData" :key="item.name" class="flex items-center gap-3">
              <span class="w-16 text-xs text-brand-muted text-right">{{ item.name }}</span>
              <div class="flex-1 h-5 bg-brand-surface rounded-lg overflow-hidden relative">
                <div 
                  class="h-full bg-gradient-to-r from-brand-primary to-brand-accent rounded-lg transition-all duration-500"
                  :style="{ width: item.percent + '%' }"
                ></div>
              </div>
              <span class="w-10 text-xs text-brand-muted text-right">{{ item.percent }}%</span>
            </div>
          </div>
        </div>

        <!-- 城市需求 Top 6 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-brand-text flex items-center gap-2">
              <i class="bi bi-geo-alt text-red-400"></i>
              城市需求 Top 6
            </h3>
          </div>
          <div class="space-y-3">
            <div v-for="item in cityData" :key="item.name" class="flex items-center gap-3">
              <span class="w-10 text-xs text-brand-muted text-right">{{ item.name }}</span>
              <div class="flex-1 h-5 bg-brand-surface rounded-lg overflow-hidden relative">
                <div 
                  class="h-full bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg transition-all duration-500"
                  :style="{ width: item.percent + '%' }"
                ></div>
              </div>
              <span class="w-10 text-xs text-brand-muted text-right">{{ item.percent }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 招聘趋势 -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 mb-8">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-brand-text flex items-center gap-2">
            <i class="bi bi-graph-up text-emerald-400"></i>
            近12个月招聘趋势
          </h3>
          <span class="badge-green text-xs">
            <i class="bi bi-arrow-up-right mr-1"></i>
            热度持续上升
          </span>
        </div>
        <div class="h-[200px] flex items-end justify-between gap-2 pt-4">
          <div 
            v-for="(item, index) in trendData" 
            :key="index"
            class="flex-1 flex flex-col items-center gap-1"
          >
            <div 
              class="w-full bg-gradient-to-t from-brand-primary/80 to-brand-accent rounded-t-lg transition-all duration-300 hover:from-brand-primary hover:to-brand-accent"
              :style="{ height: `${item.value}%` }"
            ></div>
            <span class="text-[10px] text-brand-muted">{{ item.month }}</span>
          </div>
        </div>
      </div>

      <!-- 核心要求卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- 核心技术要求 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-brand-primary/20 flex items-center justify-center">
              <i class="bi bi-code-slash text-brand-primary"></i>
            </div>
            <h3 class="font-semibold text-brand-text">核心技术要求</h3>
          </div>
          <ul class="space-y-2 text-sm text-brand-muted">
            <li class="flex items-start gap-2">
              <i class="bi bi-check-circle text-emerald-400 mt-0.5"></i>
              <span>熟练掌握 Vue3 / React 及其生态</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-check-circle text-emerald-400 mt-0.5"></i>
              <span>TypeScript 有实际开发经验</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-check-circle text-emerald-400 mt-0.5"></i>
              <span>熟悉 Vite/Webpack 构建体系</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-check-circle text-emerald-400 mt-0.5"></i>
              <span>了解性能优化与安全实践</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-check-circle text-emerald-400 mt-0.5"></i>
              <span>有组件库或开源经验优先</span>
            </li>
          </ul>
        </div>

        <!-- 软技能要求 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center">
              <i class="bi bi-people text-cyan-400"></i>
            </div>
            <h3 class="font-semibold text-brand-text">软技能要求</h3>
          </div>
          <ul class="space-y-2 text-sm text-brand-muted">
            <li class="flex items-start gap-2">
              <i class="bi bi-chat-dots text-cyan-400 mt-0.5"></i>
              <span>良好的跨部门沟通协调能力</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-journal-text text-cyan-400 mt-0.5"></i>
              <span>有文档协同与知识分享意识</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-lightbulb text-cyan-400 mt-0.5"></i>
              <span>能独立定位与解决疑难问题</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-person-workspace text-cyan-400 mt-0.5"></i>
              <span>对用户体验有敏锐洞察力</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-book text-cyan-400 mt-0.5"></i>
              <span>主动学习引入新技术框架</span>
            </li>
          </ul>
        </div>

        <!-- 加分项 -->
        <div class="bg-brand-card border border-brand-border rounded-2xl p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center">
              <i class="bi bi-star text-amber-400"></i>
            </div>
            <h3 class="font-semibold text-brand-text">加分项</h3>
          </div>
          <ul class="space-y-2 text-sm text-brand-muted">
            <li class="flex items-start gap-2">
              <i class="bi bi-plus-circle text-amber-400 mt-0.5"></i>
              <span>有开源项目贡献或维护经历</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-plus-circle text-amber-400 mt-0.5"></i>
              <span>参与过亿级PV高并发项目优化</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-plus-circle text-amber-400 mt-0.5"></i>
              <span>了解后端/DevOps/容器化基础</span>
            </li>
            <li class="flex items-start gap-2">
              <i class="bi bi-plus-circle text-amber-400 mt-0.5"></i>
              <span>Node.js 全栈开发经验</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 画像对比入口 -->
      <div class="mt-8 text-center">
        <router-link 
          to="/analysis/compare"
          class="inline-flex items-center gap-2 px-8 py-4 rounded-xl btn-primary text-base"
        >
          <i class="bi bi-arrow-left-right"></i>
          进入画像对比
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import RadarChart from '@/components/RadarChart.vue'

const activeTab = ref('job')
const activeFilter = ref('all')

const filterTabs = [
  { key: 'all', label: '前端工程师', icon: 'bi bi-laptop' },
  { key: 'product', label: '产品经理', icon: 'bi bi-kanban' },
  { key: 'data', label: '数据分析师', icon: 'bi bi-bar-chart-line' },
  { key: 'devops', label: '后端工程师', icon: 'bi bi-server' },
  { key: 'ai', label: 'AI算法工程师', icon: 'bi bi-robot' },
]

const statsCards = ref([
  { label: '在招职位', value: '12.4K', trend: 18 },
  { label: '平均薪资', value: '26K', trend: 12 },
  { label: '岗位竞争比', value: '1:8', trend: 5 },
  { label: '平均招聘周期', value: '21天', trend: 8 },
])

const radarIndicators = ['JavaScript', 'Vue/React', 'TypeScript', '性能优化', 'Node.js']
const radarSeries = ref([
  {
    name: '岗位要求',
    values: [9, 8.5, 7.5, 6.5, 5],
    color: '#7c3aed',
  }
])

const salaryRanges = ref([
  { range: '10-15K', percent: 12, color: 'bg-brand-muted/50' },
  { range: '15-20K', percent: 28, color: 'bg-violet-500' },
  { range: '20-30K', percent: 35, color: 'bg-brand-primary' },
  { range: '30-40K', percent: 18, color: 'bg-cyan-500' },
  { range: '40K+', percent: 7, color: 'bg-emerald-500' },
])

const skillHotTags = ref([
  { name: 'Vue3', hot: true },
  { name: 'React', hot: true },
  { name: 'TypeScript', hot: true },
  { name: 'JavaScript', hot: true },
  { name: 'CSS3', hot: false },
  { name: 'Vite', hot: true },
  { name: 'Webpack', hot: false },
  { name: 'Node.js', hot: false },
  { name: 'Git', hot: false },
  { name: '微前端', hot: false },
  { name: 'Next.js', hot: false },
  { name: '小程序', hot: false },
  { name: 'Tailwind', hot: false },
  { name: 'Three.js', hot: false },
  { name: 'Jest', hot: false },
  { name: 'GraphQL', hot: false },
  { name: 'Docker', hot: false },
  { name: 'CI/CD', hot: false },
])

const industryData = ref([
  { name: '互联网', percent: 45 },
  { name: '金融科技', percent: 18 },
  { name: '电商', percent: 15 },
  { name: '游戏', percent: 10 },
  { name: '教育', percent: 7 },
  { name: '其他', percent: 5 },
])

const cityData = ref([
  { name: '北京', percent: 32 },
  { name: '上海', percent: 28 },
  { name: '深圳', percent: 20 },
  { name: '杭州', percent: 10 },
  { name: '广州', percent: 6 },
  { name: '成都', percent: 4 },
])

const trendData = ref([
  { month: '5月', value: 45 },
  { month: '6月', value: 52 },
  { month: '7月', value: 48 },
  { month: '8月', value: 55 },
  { month: '9月', value: 62 },
  { month: '10月', value: 58 },
  { month: '11月', value: 65 },
  { month: '12月', value: 70 },
  { month: '1月', value: 68 },
  { month: '2月', value: 75 },
  { month: '3月', value: 82 },
  { month: '4月', value: 90 },
])
</script>
