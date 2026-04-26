<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">

      <!-- ═══ Page Header ═══ -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-lightning-fill text-amber-400"></i> 技能评估
          </h1>
          <p class="text-sm text-brand-muted mt-1">对比岗位要求，精准定位差距，制定补强计划</p>
        </div>
        <div v-if="!hasCareerGoal" class="flex items-center gap-3 px-4 py-2 rounded-xl border border-amber-500/30 bg-amber-500/5">
          <i class="bi bi-exclamation-triangle text-amber-400"></i>
          <span class="text-sm text-amber-400">请先选择目标职业</span>
          <router-link to="/career/explore" class="text-sm text-violet-400 hover:text-violet-300 underline">去选择</router-link>
        </div>
        <div v-else class="text-sm text-brand-muted">
          目标：<span class="text-violet-400 font-medium">{{ careerStore.careerGoal.primaryCareerLabel }}</span>
        </div>
      </div>

      <!-- ═══ Empty State ═══ -->
      <div v-if="!hasCareerGoal" class="flex flex-col items-center justify-center py-32">
        <div class="w-20 h-20 rounded-full bg-brand-surface flex items-center justify-center mb-6">
          <i class="bi bi-bullseye text-3xl text-rose-400"></i>
        </div>
        <h2 class="text-xl font-semibold text-brand-text mb-3">还没有选择目标职业</h2>
        <p class="text-brand-muted text-sm mb-8 text-center max-w-md">
          在「职业探索」中选择你的目标方向后，这里将自动生成个性化技能差距分析
        </p>
        <router-link to="/career/explore" class="btn-primary">
          前往职业探索 →
        </router-link>
      </div>

      <!-- ═══ Content (when career goal exists) ═══ -->
      <template v-else>
        <!-- Stats Row -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="card text-center">
            <div class="text-3xl font-bold text-violet-400 mb-1">{{ stats.total }}</div>
            <div class="text-sm text-brand-muted">技能总数</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-emerald-400 mb-1">{{ stats.qualified }}</div>
            <div class="text-sm text-brand-muted">已达标</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-amber-400 mb-1">{{ stats.needsImprove }}</div>
            <div class="text-sm text-brand-muted">待提升</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-red-400 mb-1">{{ stats.majorGap }}</div>
            <div class="text-sm text-brand-muted">重大差距</div>
          </div>
        </div>

        <!-- Radar + Skill List -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div class="card">
            <h2 class="text-lg font-semibold text-brand-text mb-4 flex items-center gap-2">
              <i class="bi bi-hexagon text-violet-400"></i> 技能雷达图
            </h2>
            <div class="aspect-square max-w-md mx-auto">
              <RadarChart v-if="radarData.length > 0" :data="radarData" :max="5" />
              <div v-else class="flex items-center justify-center h-full text-brand-muted"><p>暂无技能数据</p></div>
            </div>
            <div class="flex justify-center gap-6 mt-4">
              <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-violet-500"></div><span class="text-sm text-brand-muted">当前水平</span></div>
              <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-cyan-500"></div><span class="text-sm text-brand-muted">岗位要求</span></div>
            </div>
          </div>

          <div class="card">
            <h2 class="text-lg font-semibold text-brand-text mb-4 flex items-center gap-2">
              <i class="bi bi-list-check text-violet-400"></i> 技能差距详情
            </h2>
            <div class="space-y-3 max-h-96 overflow-y-auto pr-2">
              <div v-for="skill in sortedSkills" :key="skill.skillName" class="bg-brand-surface border border-brand-border rounded-xl p-4">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="font-medium text-brand-text">{{ skill.skillName }}</span>
                    <span class="text-xs text-brand-muted bg-brand-card px-2 py-0.5 rounded">{{ skill.category }}</span>
                  </div>
                  <span :class="['text-xs px-2 py-1 rounded-full', skill.status === 'qualified' ? 'bg-emerald-500/10 text-emerald-400' : skill.status === 'needs_improve' ? 'bg-amber-500/10 text-amber-400' : 'bg-red-500/10 text-red-400']">
                    {{ skill.status === 'qualified' ? '已达标' : skill.status === 'needs_improve' ? '待提升' : '需重点加强' }}
                  </span>
                </div>
                <div class="flex items-center gap-4">
                  <div class="flex-1">
                    <div class="flex justify-between text-xs text-brand-muted mb-1"><span>Lv.{{ skill.userLevel }}</span><span>Lv.{{ skill.requiredLevel }}</span></div>
                    <div class="h-2 bg-brand-card rounded-full overflow-hidden relative">
                      <div class="absolute inset-y-0 left-0 bg-violet-500 rounded-full" :style="{ width: (skill.userLevel / 5 * 100) + '%' }"></div>
                      <div class="absolute inset-y-0 right-0 border-l-2 border-cyan-400" :style="{ right: ((5 - skill.requiredLevel) / 5 * 100) + '%' }"></div>
                    </div>
                  </div>
                  <div class="text-right min-w-[60px]">
                    <span :class="['text-sm font-medium', skill.gap > 0 ? 'text-red-400' : 'text-emerald-400']">
                      {{ skill.gap > 0 ? '-' + skill.gap : '+' + Math.abs(skill.gap) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Suggestions -->
        <div class="card mb-8">
          <h2 class="text-lg font-semibold text-brand-text mb-6 flex items-center gap-2">
            <i class="bi bi-lightbulb text-violet-400"></i> 提升建议
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="(suggestion, i) in suggestions" :key="i" class="bg-brand-surface border border-brand-border rounded-xl p-4">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-lg flex items-center justify-center" :style="{ background: suggestion.gradient }">
                  <i :class="suggestion.icon" class="text-white"></i>
                </div>
                <div>
                  <h3 class="font-medium text-brand-text">{{ suggestion.title }}</h3>
                  <p class="text-xs text-brand-muted">{{ suggestion.subtitle }}</p>
                </div>
              </div>
              <p class="text-sm text-brand-muted mb-3">{{ suggestion.desc }}</p>
              <div class="flex flex-wrap gap-1">
                <span v-for="tag in suggestion.tags" :key="tag" class="badge text-xs">{{ tag }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-center gap-4">
          <router-link to="/career/explore" class="btn-secondary"><i class="bi bi-arrow-left mr-2"></i>返回职业探索</router-link>
          <router-link to="/career/actions" class="btn-primary">生成行动计划<i class="bi bi-arrow-right ml-2"></i></router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCareerStore } from '@/stores/careerStore'
import RadarChart from '@/components/RadarChart.vue'

const careerStore = useCareerStore()

const hasCareerGoal = computed(() => !!careerStore.careerGoal.primaryCareer)

onMounted(() => {
  if (hasCareerGoal.value && careerStore.skillGaps.length === 0) {
    careerStore.generateSkillGaps()
  }
})

const stats = computed(() => {
  const gaps = careerStore.skillGaps
  return {
    total: gaps.length,
    qualified: gaps.filter(g => g.status === 'qualified').length,
    needsImprove: gaps.filter(g => g.status === 'needs_improve').length,
    majorGap: gaps.filter(g => g.status === 'major_gap').length,
  }
})

const sortedSkills = computed(() => {
  return [...careerStore.skillGaps].sort((a, b) => {
    const order = { major_gap: 0, needs_improve: 1, qualified: 2 }
    return order[a.status] - order[b.status]
  })
})

const radarData = computed(() => {
  const gaps = careerStore.skillGaps.slice(0, 6)
  if (gaps.length === 0) return []
  return gaps.map(g => ({ name: g.skillName.split('/')[0], value: g.userLevel, max: 5 }))
})

const suggestions = computed(() => {
  const majorGaps = careerStore.skillGaps.filter(g => g.status === 'major_gap')
  const list = []
  if (majorGaps.length > 0) {
    list.push({
      title: '重点突破', subtitle: `${majorGaps.length}项核心技能待加强`,
      icon: 'bi bi-lightning', gradient: 'linear-gradient(135deg, #EF4444, #DC2626)',
      desc: `建议优先提升${majorGaps.slice(0, 2).map(g => g.skillName).join('、')}等核心技能，这些是岗位的硬性要求。`,
      tags: majorGaps.slice(0, 3).map(g => g.skillName),
    })
  }
  list.push({ title: '系统学习', subtitle: '建立完整知识体系', icon: 'bi bi-book', gradient: 'linear-gradient(135deg, #4F46E5, #7C3AED)', desc: '推荐通过在线课程、技术书籍等方式系统性学习，避免知识碎片化。', tags: ['慕课网', 'Udemy', '极客时间'] })
  list.push({ title: '项目实战', subtitle: '在实践中提升能力', icon: 'bi bi-code-slash', gradient: 'linear-gradient(135deg, #10B981, #059669)', desc: '通过开源项目、个人项目或公司业务实战，将理论知识转化为实际能力。', tags: ['GitHub', '开源贡献', '副业项目'] })
  list.push({ title: '社区交流', subtitle: '向高手学习', icon: 'bi bi-people', gradient: 'linear-gradient(135deg, #06B6D4, #0891B2)', desc: '加入技术社区、参加线下活动，与同行交流学习经验和最佳实践。', tags: ['技术社区', '线下Meetup', '技术大会'] })
  return list
})
</script>
