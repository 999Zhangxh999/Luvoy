<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <section class="mb-8 rounded-3xl border border-brand-border bg-brand-card p-6 lg:p-8">
        <div class="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 class="mb-2 text-3xl font-bold text-brand-text">职业探索</h1>
            <p class="text-brand-muted">基于岗位画像大盘进行多维筛选，快速定位最契合的职业方向。</p>
          </div>
          <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-violet-400">{{ dashboardStats.totalProfiles }}</div>
              <div class="text-xs text-brand-muted">岗位画像</div>
            </div>
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-cyan-400">{{ dashboardStats.categoryCount }}</div>
              <div class="text-xs text-brand-muted">岗位类别</div>
            </div>
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-emerald-400">{{ dashboardStats.uniqueSkills }}</div>
              <div class="text-xs text-brand-muted">技能词条</div>
            </div>
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-amber-400">{{ dashboardStats.averageSalary }}K</div>
              <div class="text-xs text-brand-muted">平均薪资上限</div>
            </div>
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-pink-400">{{ dashboardStats.highDemandCount }}</div>
              <div class="text-xs text-brand-muted">高需求岗位</div>
            </div>
            <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
              <div class="text-xl font-bold text-blue-400">{{ stats.total_jobs || 0 }}</div>
              <div class="text-xs text-brand-muted">招聘岗位库</div>
            </div>
          </div>
        </div>

        <div class="relative">
          <i class="bi bi-search absolute left-4 top-1/2 -translate-y-1/2 text-brand-muted"></i>
          <input
            v-model="searchQuery"
            class="input-base pl-11 pr-24"
            placeholder="搜索岗位名、类别、技能、关键词..."
            @keyup.enter="handleSearch"
          />
          <button class="btn-primary absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2" @click="handleSearch">检索</button>
        </div>

        <div class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="skill in topSkills.slice(0, 10)"
            :key="skill.name"
            class="rounded-full border px-3 py-1 text-xs transition"
            :class="selectedSkills.includes(skill.name)
              ? 'border-cyan-400 bg-cyan-500/20 text-cyan-300'
              : 'border-brand-border bg-brand-surface text-brand-muted hover:border-cyan-400/40'"
            @click="toggleSkill(skill.name)"
          >
            {{ skill.name }} · {{ skill.count }}
          </button>
        </div>
      </section>

      <section class="grid grid-cols-1 gap-6 lg:grid-cols-4">
        <aside class="space-y-4 lg:col-span-1">
          <div class="card p-4">
            <div class="mb-3 flex items-center justify-between">
              <h3 class="font-semibold text-brand-text">筛选条件</h3>
              <button class="text-xs text-cyan-300" @click="resetFilters">重置</button>
            </div>

            <div class="mb-4">
              <div class="mb-2 text-xs text-brand-muted">岗位类别</div>
              <div class="space-y-1">
                <button
                  v-for="cat in categories"
                  :key="cat.name"
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm transition"
                  :class="selectedCategory === cat.name
                    ? 'bg-violet-600 text-white'
                    : 'bg-brand-surface text-brand-muted hover:bg-brand-card'"
                  @click="selectedCategory = cat.name"
                >
                  <span>{{ cat.name }}</span>
                  <span class="text-xs">{{ cat.count }}</span>
                </button>
              </div>
            </div>

            <div class="mb-4">
              <div class="mb-2 text-xs text-brand-muted">学历要求</div>
              <div class="space-y-1">
                <label v-for="edu in educationOptions" :key="edu" class="flex cursor-pointer items-center gap-2 text-sm text-brand-muted">
                  <input v-model="selectedEducations" :value="edu" type="checkbox" />
                  <span>{{ edu }}</span>
                </label>
              </div>
            </div>

            <div class="mb-4">
              <div class="mb-2 text-xs text-brand-muted">经验要求</div>
              <div class="space-y-1">
                <label v-for="exp in experienceOptions" :key="exp" class="flex cursor-pointer items-center gap-2 text-sm text-brand-muted">
                  <input v-model="selectedExperiences" :value="exp" type="checkbox" />
                  <span>{{ exp }}</span>
                </label>
              </div>
            </div>

            <div class="mb-4">
              <div class="mb-2 flex items-center justify-between text-xs text-brand-muted">
                <span>薪资上限（K）</span>
                <span>{{ salaryMax }}</span>
              </div>
              <input v-model.number="salaryMax" class="w-full accent-violet-500" max="120" min="5" type="range" />
            </div>

            <div>
              <div class="mb-2 flex items-center justify-between text-xs text-brand-muted">
                <span>能力均分下限</span>
                <span>{{ minAbility }}</span>
              </div>
              <input v-model.number="minAbility" class="w-full accent-cyan-500" max="10" min="0" step="0.5" type="range" />
            </div>
          </div>

          <div class="card p-4">
            <h3 class="mb-3 font-semibold text-brand-text">探索洞察</h3>
            <div class="space-y-3 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-brand-muted">筛选后岗位数</span>
                <span class="text-violet-300">{{ filteredProfiles.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-brand-muted">筛选后平均能力</span>
                <span class="text-cyan-300">{{ filteredAbilityAvg }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-brand-muted">筛选后平均薪资上限</span>
                <span class="text-emerald-300">{{ filteredSalaryAvg }}K</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-brand-muted">高匹配权重岗位</span>
                <span class="text-amber-300">{{ highSkillWeightCount }}</span>
              </div>
            </div>
          </div>
        </aside>

        <section class="space-y-4 lg:col-span-3">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="text-sm text-brand-muted">
              共 <span class="font-semibold text-violet-300">{{ filteredProfiles.length }}</span> 条画像，当前第 {{ currentPage }} / {{ totalPages }} 页
            </div>
            <div class="flex items-center gap-2">
              <select v-model="sortBy" class="input-base w-44 py-2 text-sm">
                <option value="demand">按需求热度</option>
                <option value="salary">按薪资上限</option>
                <option value="ability">按能力均分</option>
                <option value="name">按岗位名称</option>
              </select>
              <button class="rounded-lg p-2" :class="viewMode === 'grid' ? 'bg-violet-600 text-white' : 'bg-brand-surface text-brand-muted'" @click="viewMode = 'grid'">
                <i class="bi bi-grid-3x3-gap"></i>
              </button>
              <button class="rounded-lg p-2" :class="viewMode === 'list' ? 'bg-violet-600 text-white' : 'bg-brand-surface text-brand-muted'" @click="viewMode = 'list'">
                <i class="bi bi-list"></i>
              </button>
            </div>
          </div>

          <div v-if="loading" class="py-16 text-center text-brand-muted">
            <i class="bi bi-hourglass-split mr-2 animate-spin"></i>加载岗位画像中...
          </div>

          <div v-else-if="paginatedProfiles.length === 0" class="card py-16 text-center text-brand-muted">
            未找到符合条件的岗位画像
          </div>

          <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 gap-4 xl:grid-cols-2">
            <article
              v-for="profile in paginatedProfiles"
              :key="profile.id"
              class="card cursor-pointer p-4"
              @click="openDetail(profile)"
            >
              <div class="mb-3 flex items-start justify-between gap-3">
                <div>
                  <h3 class="font-semibold text-brand-text">{{ profile.position_name }}</h3>
                  <p class="text-xs text-brand-muted">{{ profile.category || '未分类' }} · {{ profile.level || '层级未知' }}</p>
                </div>
                <div class="text-right">
                  <div class="text-sm font-semibold text-emerald-300">{{ profile.salary_range || '面议' }}</div>
                  <div class="text-xs text-brand-muted">热度 {{ profile.demandScore }}</div>
                </div>
              </div>

              <div class="mb-3 grid grid-cols-3 gap-2">
                <div v-for="ability in getAbilities(profile)" :key="ability.short" class="rounded-lg bg-brand-surface p-2 text-center">
                  <div class="text-sm font-bold" :class="abilityColorClass(ability.value)">{{ ability.value.toFixed(1) }}</div>
                  <div class="text-[11px] text-brand-muted">{{ ability.short }}</div>
                </div>
              </div>

              <div class="mb-3 flex flex-wrap gap-1">
                <span v-for="skill in (profile.technical_skills || []).slice(0, 6)" :key="skill" class="badge-cyan text-xs">{{ skill }}</span>
              </div>

              <div class="grid grid-cols-2 gap-2 text-xs text-brand-muted">
                <div>学历：{{ profile.education_req || '不限' }}</div>
                <div>经验：{{ profile.experience_req || '不限' }}</div>
              </div>
            </article>
          </div>

          <div v-else class="space-y-3">
            <article
              v-for="profile in paginatedProfiles"
              :key="profile.id"
              class="card cursor-pointer p-4"
              @click="openDetail(profile)"
            >
              <div class="mb-2 flex items-start justify-between gap-4">
                <div>
                  <h3 class="font-semibold text-brand-text">{{ profile.position_name }}</h3>
                  <p class="text-xs text-brand-muted">{{ profile.category || '未分类' }} · {{ profile.level || '层级未知' }}</p>
                </div>
                <div class="text-right">
                  <div class="text-sm font-semibold text-emerald-300">{{ profile.salary_range || '面议' }}</div>
                  <div class="text-xs text-brand-muted">能力均分 {{ profile.abilityAvg.toFixed(1) }}</div>
                </div>
              </div>

              <div class="mb-2 text-sm text-brand-muted line-clamp-2">{{ profile.summary || '暂无岗位摘要' }}</div>
              <div class="mb-2 flex flex-wrap gap-1">
                <span v-for="skill in (profile.technical_skills || []).slice(0, 8)" :key="skill" class="badge-cyan text-xs">{{ skill }}</span>
              </div>
              <div class="grid grid-cols-4 gap-2 text-xs text-brand-muted">
                <div>基础 {{ ((profile.weight_basic || 0) * 100).toFixed(0) }}%</div>
                <div>技能 {{ ((profile.weight_skill || 0) * 100).toFixed(0) }}%</div>
                <div>素养 {{ ((profile.weight_quality || 0) * 100).toFixed(0) }}%</div>
                <div>潜力 {{ ((profile.weight_potential || 0) * 100).toFixed(0) }}%</div>
              </div>
            </article>
          </div>

          <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 pt-2">
            <button class="btn-secondary px-3 py-2" :disabled="currentPage === 1" @click="currentPage = Math.max(1, currentPage - 1)">
              <i class="bi bi-chevron-left"></i>
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              class="h-9 w-9 rounded-lg text-sm"
              :class="page === currentPage ? 'bg-violet-600 text-white' : 'bg-brand-surface text-brand-muted'"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
            <button class="btn-secondary px-3 py-2" :disabled="currentPage === totalPages" @click="currentPage = Math.min(totalPages, currentPage + 1)">
              <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </section>
      </section>
    </div>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="selectedProfile" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div class="max-h-[90vh] w-full max-w-5xl overflow-y-auto rounded-2xl border border-brand-border bg-brand-card">
            <div class="sticky top-0 z-10 flex items-start justify-between border-b border-brand-border bg-brand-card p-5">
              <div>
                <h2 class="text-2xl font-bold text-brand-text">{{ selectedProfile.position_name }}</h2>
                <p class="text-sm text-brand-muted">{{ selectedProfile.category || '未分类' }} · {{ selectedProfile.level || '层级未知' }} · {{ selectedProfile.salary_range || '面议' }}</p>
              </div>
              <button class="text-brand-muted hover:text-brand-text" @click="selectedProfile = null">
                <i class="bi bi-x-lg text-xl"></i>
              </button>
            </div>

            <div class="space-y-5 p-5">
              <div>
                <h3 class="mb-2 text-sm font-semibold text-brand-text">岗位概述</h3>
                <p class="text-sm leading-6 text-brand-muted">{{ selectedProfile.summary || '暂无岗位概述' }}</p>
              </div>

              <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
                  <div class="text-lg font-bold text-violet-400">{{ ((selectedProfile.weight_basic || 0) * 100).toFixed(0) }}%</div>
                  <div class="text-xs text-brand-muted">基础权重</div>
                </div>
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
                  <div class="text-lg font-bold text-cyan-400">{{ ((selectedProfile.weight_skill || 0) * 100).toFixed(0) }}%</div>
                  <div class="text-xs text-brand-muted">技能权重</div>
                </div>
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
                  <div class="text-lg font-bold text-emerald-400">{{ ((selectedProfile.weight_quality || 0) * 100).toFixed(0) }}%</div>
                  <div class="text-xs text-brand-muted">素养权重</div>
                </div>
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-center">
                  <div class="text-lg font-bold text-amber-400">{{ ((selectedProfile.weight_potential || 0) * 100).toFixed(0) }}%</div>
                  <div class="text-xs text-brand-muted">潜力权重</div>
                </div>
              </div>

              <div>
                <h3 class="mb-2 text-sm font-semibold text-brand-text">能力要求</h3>
                <div class="grid grid-cols-2 gap-2 md:grid-cols-3">
                  <div v-for="ability in getAbilities(selectedProfile)" :key="ability.short" class="rounded-lg border border-brand-border bg-brand-surface p-2">
                    <div class="flex items-center justify-between text-sm">
                      <span class="text-brand-muted">{{ ability.name }}</span>
                      <span class="font-semibold" :class="abilityColorClass(ability.value)">{{ ability.value.toFixed(1) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 class="mb-2 text-sm font-semibold text-brand-text">技能与证书要求</h3>
                <div class="mb-3 flex flex-wrap gap-1">
                  <span v-for="skill in (selectedProfile.technical_skills || [])" :key="skill" class="badge-cyan text-xs">{{ skill }}</span>
                </div>
                <div class="flex flex-wrap gap-1">
                  <span v-for="cert in (selectedProfile.certificates || [])" :key="cert" class="badge text-xs">{{ cert }}</span>
                  <span v-if="!(selectedProfile.certificates || []).length" class="text-xs text-brand-muted">暂无证书要求</span>
                </div>
              </div>

              <div class="grid grid-cols-1 gap-3 md:grid-cols-3">
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-sm text-brand-muted">
                  学历要求：<span class="text-brand-text">{{ selectedProfile.education_req || '不限' }}</span>
                </div>
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-sm text-brand-muted">
                  经验要求：<span class="text-brand-text">{{ selectedProfile.experience_req || '不限' }}</span>
                </div>
                <div class="rounded-xl border border-brand-border bg-brand-surface p-3 text-sm text-brand-muted">
                  需求热度：<span class="text-brand-text">{{ selectedProfile.demandScore }}</span>
                </div>
              </div>
            </div>

            <div class="sticky bottom-0 grid grid-cols-1 gap-3 border-t border-brand-border bg-brand-card p-5 md:grid-cols-3">
              <router-link class="btn-secondary text-center" to="/resume" @click="selectedProfile = null">
                <i class="bi bi-file-earmark-person mr-2"></i>去简历中心建档
              </router-link>
              <router-link class="btn-secondary text-center" to="/analysis" @click="selectedProfile = null">
                <i class="bi bi-bar-chart mr-2"></i>去画像分析对比
              </router-link>
              <router-link class="btn-primary text-center" to="/planning" @click="selectedProfile = null">
                <i class="bi bi-signpost-split mr-2"></i>去规划中心落地
              </router-link>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue'
import { getJobProfiles, getStats } from '@/api'

const toast = inject('toast', null)

const loading = ref(true)
const stats = ref({})
const profiles = ref([])

const searchQuery = ref('')
const selectedCategory = ref('全部')
const selectedEducations = ref([])
const selectedExperiences = ref([])
const selectedSkills = ref([])
const salaryMax = ref(50)
const minAbility = ref(0)
const sortBy = ref('demand')
const viewMode = ref('grid')
const currentPage = ref(1)
const pageSize = 8

const selectedProfile = ref(null)

function parseSalaryMax(salaryRange) {
  if (!salaryRange) return 0
  const nums = String(salaryRange).match(/\d+(?:\.\d+)?/g)
  if (!nums?.length) return 0
  return Math.max(...nums.map(Number))
}

function normalizeProfiles(items) {
  return (items || []).map((profile) => {
    const skills = Array.isArray(profile.technical_skills) ? profile.technical_skills : []
    const abilities = [
      Number(profile.innovation_ability) || 0,
      Number(profile.learning_ability) || 0,
      Number(profile.pressure_resistance) || 0,
      Number(profile.communication_skill) || 0,
      Number(profile.teamwork_ability) || 0,
      Number(profile.internship_ability) || 0,
    ]
    const abilityAvg = abilities.reduce((sum, n) => sum + n, 0) / abilities.length
    const salaryUpper = parseSalaryMax(profile.salary_range)
    const demandScore = Math.round(abilityAvg * 10 + skills.length * 2 + salaryUpper / 2)

    return {
      ...profile,
      technical_skills: skills,
      abilities,
      abilityAvg,
      salaryUpper,
      demandScore,
    }
  })
}

const normalizedProfiles = computed(() => normalizeProfiles(profiles.value))

const categories = computed(() => {
  const map = new Map()
  normalizedProfiles.value.forEach((item) => {
    const key = item.category || '未分类'
    map.set(key, (map.get(key) || 0) + 1)
  })
  const rows = Array.from(map.entries()).map(([name, count]) => ({ name, count }))
  rows.sort((a, b) => b.count - a.count)
  return [{ name: '全部', count: normalizedProfiles.value.length }, ...rows]
})

const educationOptions = computed(() => {
  const set = new Set(normalizedProfiles.value.map((p) => p.education_req).filter(Boolean))
  return set.size ? Array.from(set) : ['不限', '大专', '本科', '硕士', '博士']
})

const experienceOptions = computed(() => {
  const set = new Set(normalizedProfiles.value.map((p) => p.experience_req).filter(Boolean))
  return set.size ? Array.from(set) : ['不限', '应届', '1-3年', '3-5年', '5年以上']
})

const topSkills = computed(() => {
  const map = new Map()
  normalizedProfiles.value.forEach((profile) => {
    profile.technical_skills.forEach((skill) => {
      map.set(skill, (map.get(skill) || 0) + 1)
    })
  })
  return Array.from(map.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
})

function matchAny(sourceText, selectedOptions) {
  if (!selectedOptions.length) return true
  const text = String(sourceText || '').toLowerCase()
  return selectedOptions.some((opt) => text.includes(String(opt).toLowerCase()))
}

const filteredProfiles = computed(() => {
  let rows = [...normalizedProfiles.value]

  const keyword = searchQuery.value.trim().toLowerCase()
  if (keyword) {
    rows = rows.filter((profile) => {
      const target = [
        profile.position_name,
        profile.category,
        profile.level,
        profile.summary,
        profile.technical_skills.join(' '),
      ]
        .join(' ')
        .toLowerCase()
      return target.includes(keyword)
    })
  }

  if (selectedCategory.value !== '全部') {
    rows = rows.filter((profile) => (profile.category || '未分类') === selectedCategory.value)
  }

  rows = rows.filter((profile) => matchAny(profile.education_req, selectedEducations.value))
  rows = rows.filter((profile) => matchAny(profile.experience_req, selectedExperiences.value))

  if (selectedSkills.value.length) {
    rows = rows.filter((profile) => selectedSkills.value.every((skill) => profile.technical_skills.includes(skill)))
  }

  rows = rows.filter((profile) => profile.salaryUpper <= salaryMax.value || profile.salaryUpper === 0)
  rows = rows.filter((profile) => profile.abilityAvg >= minAbility.value)

  rows.sort((a, b) => {
    if (sortBy.value === 'salary') return b.salaryUpper - a.salaryUpper
    if (sortBy.value === 'ability') return b.abilityAvg - a.abilityAvg
    if (sortBy.value === 'name') return String(a.position_name || '').localeCompare(String(b.position_name || ''))
    return b.demandScore - a.demandScore
  })

  return rows
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredProfiles.value.length / pageSize)))

const paginatedProfiles = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProfiles.value.slice(start, start + pageSize)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i += 1) pages.push(i)
  return pages
})

const dashboardStats = computed(() => {
  const totalProfiles = normalizedProfiles.value.length
  const uniqueSkills = topSkills.value.length
  const categoryCount = categories.value.length - 1
  const averageSalary = totalProfiles
    ? Math.round(
        normalizedProfiles.value.reduce((sum, item) => sum + item.salaryUpper, 0) /
          totalProfiles,
      )
    : 0
  const highDemandCount = normalizedProfiles.value.filter((item) => item.demandScore >= 85).length

  return {
    totalProfiles,
    uniqueSkills,
    categoryCount,
    averageSalary,
    highDemandCount,
  }
})

const filteredAbilityAvg = computed(() => {
  if (!filteredProfiles.value.length) return '0.0'
  const avg =
    filteredProfiles.value.reduce((sum, item) => sum + item.abilityAvg, 0) /
    filteredProfiles.value.length
  return avg.toFixed(1)
})

const filteredSalaryAvg = computed(() => {
  if (!filteredProfiles.value.length) return 0
  const avg =
    filteredProfiles.value.reduce((sum, item) => sum + item.salaryUpper, 0) /
    filteredProfiles.value.length
  return Math.round(avg)
})

const highSkillWeightCount = computed(() => {
  return filteredProfiles.value.filter((item) => Number(item.weight_skill || 0) >= 0.3).length
})

function abilityColorClass(value) {
  if (value >= 8) return 'text-emerald-400'
  if (value >= 6) return 'text-cyan-400'
  if (value >= 4) return 'text-amber-400'
  return 'text-red-400'
}

function getAbilities(profile) {
  return [
    { name: '创新能力', short: '创新', value: Number(profile.innovation_ability) || 0 },
    { name: '学习能力', short: '学习', value: Number(profile.learning_ability) || 0 },
    { name: '抗压能力', short: '抗压', value: Number(profile.pressure_resistance) || 0 },
    { name: '沟通能力', short: '沟通', value: Number(profile.communication_skill) || 0 },
    { name: '团队协作', short: '团队', value: Number(profile.teamwork_ability) || 0 },
    { name: '实践能力', short: '实践', value: Number(profile.internship_ability) || 0 },
  ]
}

function handleSearch() {
  currentPage.value = 1
}

function toggleSkill(skillName) {
  const index = selectedSkills.value.indexOf(skillName)
  if (index >= 0) {
    selectedSkills.value.splice(index, 1)
  } else {
    selectedSkills.value.push(skillName)
  }
  currentPage.value = 1
}

function resetFilters() {
  selectedCategory.value = '全部'
  selectedEducations.value = []
  selectedExperiences.value = []
  selectedSkills.value = []
  salaryMax.value = 50
  minAbility.value = 0
  sortBy.value = 'demand'
  searchQuery.value = ''
  currentPage.value = 1
}

function openDetail(profile) {
  selectedProfile.value = profile
  document.body.style.overflow = 'hidden'
}

watch(selectedProfile, (value) => {
  if (!value) {
    document.body.style.overflow = ''
  }
})

watch(
  [searchQuery, selectedCategory, selectedEducations, selectedExperiences, selectedSkills, salaryMax, minAbility, sortBy],
  () => {
    currentPage.value = 1
  },
  { deep: true },
)

async function loadData() {
  loading.value = true
  try {
    const [profilesRes, statsRes] = await Promise.all([getJobProfiles(), getStats()])
    profiles.value = profilesRes.data?.profiles || []
    stats.value = statsRes.data || {}
  } catch (error) {
    toast?.(error?.response?.data?.message || '职业探索数据加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>
