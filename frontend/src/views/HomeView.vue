<template>
  <main class="min-h-screen bg-brand-bg">

    <!-- ═══ Section 1: Hero ═══ -->
    <section class="relative overflow-hidden">
      <div class="absolute inset-0">
        <div class="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-violet-600/8 blur-[120px]"></div>
        <div class="absolute bottom-0 left-1/4 w-[400px] h-[400px] rounded-full bg-cyan-600/6 blur-[100px]"></div>
      </div>

      <div class="relative max-w-4xl mx-auto px-4 pt-24 pb-20 text-center">
        <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-4 py-1.5 text-sm text-violet-300" v-observe-visibility>
          <span class="h-2 w-2 rounded-full bg-violet-400 animate-pulse"></span>
          AI 驱动的职业成长平台
        </div>

        <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-brand-text leading-tight mb-6" v-observe-visibility>
          不只是找<span class="gradient-text">工作</span><br>
          而是成为你想成为的人
        </h1>

        <p class="text-brand-muted text-lg mb-2" v-observe-visibility>
          职业路径图谱 · AI 职业顾问 · 技能雷达分析
        </p>
        <p class="text-brand-muted/70 text-sm mb-10" v-observe-visibility>
          帮你把迷茫期省了，直接告诉你下一步该做什么
        </p>

        <!-- Auth Buttons - 已移至导航栏右上角 -->

        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto mb-8" v-observe-visibility>
          <div class="flex items-center bg-brand-surface border border-brand-border rounded-2xl p-1.5 focus-within:border-violet-500/50 transition-all">
            <i class="bi bi-search text-brand-muted ml-4 mr-3"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索职位、公司或技能..."
              class="flex-1 bg-transparent text-brand-text placeholder-brand-muted text-sm py-3 outline-none"
              @keydown.enter="handleSearch"
            />
            <button @click="handleSearch" class="btn-primary px-6 py-2.5 rounded-xl text-sm">搜索</button>
          </div>
        </div>

        <!-- Quick Tags -->
        <div class="flex flex-wrap justify-center gap-3" v-observe-visibility>
          <button v-for="tag in quickTags" :key="tag" @click="searchQuery = tag; handleSearch()"
            class="px-4 py-1.5 rounded-full border border-brand-border text-sm text-brand-muted hover:border-violet-500/40 hover:text-violet-400 transition-all">
            {{ tag }}
          </button>
        </div>
      </div>
    </section>

    <!-- ═══ Section 2: Stats Bar ═══ -->
    <section class="max-w-6xl mx-auto px-4 -mt-4 mb-16 relative z-10" v-observe-visibility>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <router-link v-for="item in statCards" :key="item.label" :to="item.to || '#'"
          class="bg-brand-card border border-brand-border rounded-xl p-4 text-center relative overflow-hidden group hover:border-violet-500/40 transition-all cursor-pointer">
          <div class="absolute top-0 left-0 right-0 h-0.5 group-hover:h-1 transition-all" :class="item.borderColor"></div>
          <div class="w-10 h-10 mx-auto mb-2 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform" :class="item.bgColor">
            <i :class="[item.icon, item.iconColor]" class="text-lg"></i>
          </div>
          <div class="text-2xl font-bold text-brand-text group-hover:text-violet-300 transition-colors">{{ item.value }}</div>
          <div class="text-xs text-brand-muted mt-0.5">{{ item.label }}</div>
        </router-link>
      </div>
    </section>

    <!-- ═══ Section 3: Features ═══ -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center mb-14" v-observe-visibility>
        <h2 class="text-3xl md:text-4xl font-bold text-brand-text mb-4">不一样的招聘平台</h2>
        <p class="text-brand-muted text-base max-w-xl mx-auto">
          我们替你把重复性劳动干了，让你专注于最重要的决策
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div v-for="feature in features" :key="feature.title" class="card group p-7" v-observe-visibility>
          <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-5" :class="feature.iconBg">
            <i :class="[feature.icon, feature.iconColor]" class="text-xl"></i>
          </div>
          <h3 class="text-xl font-semibold text-brand-text mb-3">{{ feature.title }}</h3>
          <p class="text-brand-muted text-sm leading-relaxed mb-5">{{ feature.desc }}</p>
          <div class="flex items-center justify-between">
            <div class="flex gap-2">
              <span v-for="tag in feature.tags" :key="tag" class="badge text-xs">{{ tag }}</span>
            </div>
            <router-link :to="feature.to" class="text-brand-muted hover:text-violet-400 transition-colors">
              <i class="bi bi-arrow-right"></i>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Horizontal Scroll Extra Features -->
      <div class="overflow-x-auto pb-2 scrollbar-hide" v-observe-visibility>
        <div class="flex gap-4 min-w-max px-1">
          <router-link v-for="extra in extraFeatures" :key="extra.title" :to="extra.to"
            class="card-sm flex items-center gap-4 px-5 py-4 min-w-[260px] group">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0" :class="extra.iconBg">
              <i :class="[extra.icon, extra.iconColor]" class="text-lg"></i>
            </div>
            <div>
              <div class="text-sm font-medium text-brand-text">{{ extra.title }}</div>
              <div class="text-xs text-brand-muted">{{ extra.desc }}</div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══ Section 4: Hot Jobs ═══ -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="flex items-center justify-between mb-8" v-observe-visibility>
        <div class="flex items-center gap-3">
          <div class="w-1 h-7 rounded-full bg-violet-500"></div>
          <h2 class="text-2xl font-bold text-brand-text">热门职位</h2>
        </div>
        <router-link to="/jobs" class="text-sm text-brand-muted hover:text-violet-400 transition-colors flex items-center gap-1">
          查看全部 <i class="bi bi-arrow-right"></i>
        </router-link>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div v-for="(job, index) in hotJobs" :key="job.id || index" 
          class="card p-5 group cursor-pointer hover:border-violet-500/50 transition-all" 
          @click="goToJobDetail(job)"
          v-observe-visibility>
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 rounded-xl flex items-center justify-center text-white font-bold text-sm"
                :style="{ background: logoColors[index % logoColors.length] }">
                {{ job.logo }}
              </div>
              <div>
                <h3 class="font-semibold text-brand-text group-hover:text-violet-300 transition-colors">{{ job.title }}</h3>
                <p class="text-xs text-brand-muted">{{ job.company }}</p>
              </div>
            </div>
            <span v-if="job.hot" class="text-xs px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/20">热门</span>
          </div>

          <div class="text-lg font-bold text-violet-400 mb-3">{{ job.salary }}</div>

          <div class="flex flex-wrap gap-1.5 mb-4">
            <span v-for="skill in job.skills" :key="skill" class="badge-cyan text-xs">{{ skill }}</span>
          </div>

          <div class="flex items-center justify-between text-xs text-brand-muted pt-3 border-t border-brand-border">
            <span>{{ job.location }} · {{ job.experience }}</span>
            <span>{{ job.posted }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ Section 5: CTA + Usage Flow ═══ -->
    <section class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- CTA -->
        <div class="rounded-3xl bg-gradient-to-r from-violet-900/30 via-brand-card to-brand-card border border-brand-border p-10 md:p-14 mb-16" v-observe-visibility>
          <div class="flex items-center gap-2 text-violet-400 text-sm font-medium mb-4">
            <i class="bi bi-lightning-fill"></i>
            职业规划
          </div>
          <h2 class="text-3xl md:text-4xl font-bold text-brand-text mb-4 leading-tight">
            还没确定方向？<br>让 AI 帮你找到下一步
          </h2>
          <p class="text-brand-muted text-sm max-w-2xl mb-8 leading-relaxed">
            填写你的背景，5 分钟内获得：职业方向建议、技能差距分析、3-6 个月成长计划。
            已有 <strong class="text-brand-text">28,000+</strong> 人找到了自己的方向。
          </p>
          <div class="flex flex-wrap gap-4">
            <router-link to="/planning" class="btn-primary flex items-center gap-2">
              开始职业规划 <i class="bi bi-arrow-right"></i>
            </router-link>
            <router-link to="/jobs" class="btn-secondary">
              直接找职位
            </router-link>
          </div>
        </div>

        <!-- Usage Flow -->
        <div class="text-center mb-12" v-observe-visibility>
          <div class="flex items-center justify-center gap-2 text-brand-muted mb-3">
            <i class="bi bi-signpost-2 text-violet-400"></i>
            <span class="font-semibold text-brand-text text-xl">使用流程</span>
          </div>
          <p class="text-brand-muted text-sm">七步完成从数据到报告的完整职业规划</p>
        </div>

        <div class="relative" v-observe-visibility>
          <!-- Connection line -->
          <div class="hidden md:block absolute top-8 left-[8%] right-[8%] h-0.5 bg-gradient-to-r from-violet-500 via-cyan-500 to-pink-500 opacity-30"></div>

          <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-6 md:gap-4">
            <div v-for="(step, i) in flowSteps" :key="step.label" class="text-center group">
              <div class="relative mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-3 transition-transform group-hover:scale-110"
                :class="step.bgColor">
                <i :class="[step.icon, step.iconColor]" class="text-xl"></i>
              </div>
              <div class="text-sm font-medium text-brand-text">{{ step.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ Section 6: Testimonials ═══ -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center mb-12" v-observe-visibility>
        <h2 class="text-3xl font-bold text-brand-text mb-3">他们通过 CareerPlus 找到了方向</h2>
        <p class="text-brand-muted text-sm">真实用户分享</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="testimonial in testimonials" :key="testimonial.name" class="card p-6" v-observe-visibility>
          <div class="flex gap-1 mb-4">
            <i v-for="n in 5" :key="n" class="bi bi-star-fill text-amber-400 text-sm"></i>
          </div>
          <p class="text-brand-muted text-sm leading-relaxed mb-6">"{{ testimonial.quote }}"</p>
          <div>
            <div class="font-semibold text-brand-text">{{ testimonial.name }}</div>
            <div class="text-xs text-brand-muted">{{ testimonial.role }}</div>
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getStats, getJobProfiles } from '@/api'

const router = useRouter()
const toast = inject('toast', null)

const searchQuery = ref('')
const stats = ref({ total_jobs: 0, total_profiles: 0, total_students: 0, total_reports: 0, total_graph_paths: 0 })
const profiles = ref([])

const quickTags = ['前端工程师', '产品经理', '数据分析', 'UI设计', '算法工程师', '运营']

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/jobs', query: { q: searchQuery.value.trim() } })
  }
}

const statCards = computed(() => [
  { label: '岗位数据', value: formatNumber(stats.value.total_jobs), icon: 'bi bi-briefcase', borderColor: 'bg-blue-500', bgColor: 'bg-blue-500/10', iconColor: 'text-blue-400', to: '/jobs' },
  { label: '岗位画像', value: stats.value.total_profiles, icon: 'bi bi-person-badge', borderColor: 'bg-emerald-500', bgColor: 'bg-emerald-500/10', iconColor: 'text-emerald-400', to: '/analysis' },
  { label: '学生档案', value: stats.value.total_students, icon: 'bi bi-mortarboard', borderColor: 'bg-violet-500', bgColor: 'bg-violet-500/10', iconColor: 'text-violet-400', to: '/students' },
  { label: '图谱路径', value: stats.value.total_graph_paths || 0, icon: 'bi bi-diagram-3', borderColor: 'bg-amber-500', bgColor: 'bg-amber-500/10', iconColor: 'text-amber-400', to: '/graph' },
  { label: '规划报告', value: stats.value.total_reports, icon: 'bi bi-file-earmark-text', borderColor: 'bg-rose-500', bgColor: 'bg-rose-500/10', iconColor: 'text-rose-400', to: '/planning' },
])

function formatNumber(n) {
  if (!n) return '0'
  if (n >= 10000) return (n / 1000).toFixed(1) + 'K'
  if (n >= 1000) return n.toLocaleString()
  return String(n)
}

const features = [
  {
    title: '职业路径图谱',
    desc: '可视化展示从当前位置到目标岗位的每一步，清楚知道需要什么技能、积累什么经验。',
    icon: 'bi bi-diagram-3', iconBg: 'bg-violet-500/10', iconColor: 'text-violet-400',
    tags: ['路径规划', '技能图谱'], to: '/graph',
  },
  {
    title: 'AI 职业顾问',
    desc: '告诉 AI 你的背景，它给你最适合的方向、差距分析和 3-6 个月的提升计划。',
    icon: 'bi bi-stars', iconBg: 'bg-cyan-500/10', iconColor: 'text-cyan-400',
    tags: ['智能分析', '个性化'], to: '/career/explore',
  },
  {
    title: '技能雷达分析',
    desc: '直观看到你与目标岗位的技能差距，精准推荐学习资源，少走弯路。',
    icon: 'bi bi-activity', iconBg: 'bg-emerald-500/10', iconColor: 'text-emerald-400',
    tags: ['差距可视化', '学习推荐'], to: '/career/skills',
  },
]

const extraFeatures = [
  { title: '画像分析中心', desc: '多维度岗位与能力对比', icon: 'bi bi-bar-chart', iconBg: 'bg-amber-500/10', iconColor: 'text-amber-400', to: '/analysis' },
  { title: '简历中心', desc: '打磨你的第一印象', icon: 'bi bi-file-earmark-person', iconBg: 'bg-pink-500/10', iconColor: 'text-pink-400', to: '/resume' },
  { title: '行动管理', desc: '任务看板，规划落地', icon: 'bi bi-check2-square', iconBg: 'bg-indigo-500/10', iconColor: 'text-indigo-400', to: '/career/actions' },
  { title: '规划报告', desc: '一键生成完整职业规划', icon: 'bi bi-file-earmark-text', iconBg: 'bg-teal-500/10', iconColor: 'text-teal-400', to: '/planning' },
  { title: '学生管理', desc: '批量建档与画像生成', icon: 'bi bi-people', iconBg: 'bg-orange-500/10', iconColor: 'text-orange-400', to: '/students' },
]

const logoColors = [
  'linear-gradient(135deg, #7c3aed, #6d28d9)',
  'linear-gradient(135deg, #f59e0b, #d97706)',
  'linear-gradient(135deg, #ef4444, #dc2626)',
]

const hotJobs = computed(() => {
  const enriched = (profiles.value || []).map(p => {
    const skills = Array.isArray(p.technical_skills) ? p.technical_skills : []
    return {
      id: p.id,
      title: p.position_name || '未知职位',
      company: p.category || '未知公司',
      logo: (p.position_name || '未')[0],
      salary: p.salary_range || '面议',
      skills: skills.slice(0, 3),
      location: '不限',
      experience: p.education_requirement || '不限',
      posted: '最近',
      hot: true,
    }
  })
  return enriched.slice(0, 3)
})

function goToJobDetail(job) {
  if (job.id) {
    router.push(`/jobs/profiles/${job.id}`)
  }
}

const flowSteps = [
  { label: '导入数据', icon: 'bi bi-cloud-upload', bgColor: 'bg-violet-500/15', iconColor: 'text-violet-400' },
  { label: '岗位画像', icon: 'bi bi-person-badge', bgColor: 'bg-blue-500/15', iconColor: 'text-blue-400' },
  { label: '职业图谱', icon: 'bi bi-diagram-3', bgColor: 'bg-cyan-500/15', iconColor: 'text-cyan-400' },
  { label: '学生建档', icon: 'bi bi-people', bgColor: 'bg-emerald-500/15', iconColor: 'text-emerald-400' },
  { label: '个人画像', icon: 'bi bi-person-bounding-box', bgColor: 'bg-amber-500/15', iconColor: 'text-amber-400' },
  { label: '人岗匹配', icon: 'bi bi-link-45deg', bgColor: 'bg-rose-500/15', iconColor: 'text-rose-400' },
  { label: '规划报告', icon: 'bi bi-file-earmark-text', bgColor: 'bg-pink-500/15', iconColor: 'text-pink-400' },
]

const testimonials = [
  {
    name: '小明',
    role: '应届生 → 前端工程师 · 某独角兽企业',
    quote: '原来完全不知道从哪里下手，职业路径图谱让我清楚地看到了每一步需要什么，三个月后拿到了第一个 offer。',
  },
  {
    name: '晓雯',
    role: '运营 → 产品经理 · 互联网大厂',
    quote: 'AI 顾问帮我分析了从运营转产品的差距，制定了系统的学习计划，半年后成功转型，薪资涨了 60%。',
  },
  {
    name: '阿杰',
    role: '毕业 2 年 → 涨薪 40% · 头部电商',
    quote: '技能雷达告诉我数据分析是最大短板，补齐后简历通过率大幅提升，谈薪也更有底气了。',
  },
]

// Scroll visibility directive
const vObserveVisibility = {
  mounted(el) {
    el.style.opacity = '0'
    el.style.transform = 'translateY(24px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        el.style.opacity = '1'
        el.style.transform = 'translateY(0)'
        observer.disconnect()
      }
    }, { threshold: 0.1 })
    observer.observe(el)
  },
}

async function loadData() {
  try {
    const [statsRes, profilesRes] = await Promise.all([
      getStats(),
      getJobProfiles(),
    ])
    stats.value = { ...stats.value, ...(statsRes.data || {}) }
    profiles.value = profilesRes.data?.profiles || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '数据加载失败', 'danger')
  }
}

onMounted(loadData)
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

/* ═══ 移动端适配 ═══ */
@media (max-width: 768px) {
  /* Hero区域 */
  section:first-of-type .pt-24 {
    padding-top: 5rem;
    padding-bottom: 3rem;
  }
  
  /* 搜索栏优化 */
  section:first-of-type .max-w-2xl .flex {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem;
  }
  
  section:first-of-type .max-w-2xl input {
    padding: 0.75rem;
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  section:first-of-type .max-w-2xl button {
    width: 100%;
    justify-content: center;
  }
  
  /* 快捷标签横向滚动 */
  .flex.flex-wrap.justify-center.gap-3 {
    flex-wrap: nowrap;
    justify-content: flex-start;
    overflow-x: auto;
    padding: 0 1rem 0.5rem;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  
  .flex.flex-wrap.justify-center.gap-3::-webkit-scrollbar {
    display: none;
  }
  
  .flex.flex-wrap.justify-center.gap-3 button {
    flex-shrink: 0;
  }
  
  /* 统计卡片 */
  .grid.grid-cols-2.md\\:grid-cols-5 {
    gap: 0.75rem;
  }
  
  .grid.grid-cols-2.md\\:grid-cols-5 > a {
    padding: 0.75rem;
  }
  
  .grid.grid-cols-2.md\\:grid-cols-5 .text-2xl {
    font-size: 1.25rem;
  }
  
  /* 功能卡片区 */
  .grid.grid-cols-1.md\\:grid-cols-3 {
    gap: 1rem;
  }
  
  .card.group.p-7 {
    padding: 1.25rem;
  }
  
  /* CTA区域 */
  .rounded-3xl.bg-gradient-to-r {
    padding: 1.5rem !important;
    border-radius: 1.25rem;
  }
  
  .rounded-3xl.bg-gradient-to-r h2 {
    font-size: 1.5rem;
    line-height: 1.3;
  }
  
  .rounded-3xl.bg-gradient-to-r .flex.flex-wrap.gap-4 {
    flex-direction: column;
  }
  
  .rounded-3xl.bg-gradient-to-r .flex.flex-wrap.gap-4 a {
    width: 100%;
    justify-content: center;
    text-align: center;
  }
  
  /* 流程步骤 */
  .grid.grid-cols-2.sm\\:grid-cols-4.md\\:grid-cols-7 {
    gap: 1rem;
  }
  
  .grid.grid-cols-2.sm\\:grid-cols-4.md\\:grid-cols-7 .w-16.h-16 {
    width: 3rem;
    height: 3rem;
  }
  
  /* 用户评价卡片 */
  .grid.grid-cols-1.md\\:grid-cols-3.gap-6:last-of-type > div {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  /* 超小屏幕 */
  section:first-of-type .pt-24 {
    padding-top: 4rem;
  }
  
  h1.text-4xl {
    font-size: 1.75rem !important;
  }
  
  .rounded-3xl.bg-gradient-to-r h2 {
    font-size: 1.25rem;
  }
  
  .grid.grid-cols-2.sm\\:grid-cols-4.md\\:grid-cols-7 {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
