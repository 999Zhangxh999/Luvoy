<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">

      <!-- Page Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-clipboard-data text-violet-400"></i> 规划中心
          </h1>
          <p class="text-sm text-brand-muted mt-1">聚合画像分析与报告生成，形成完整的职业规划闭环</p>
        </div>
        <div class="flex items-center gap-3">
          <select class="input-base w-48 text-sm" @change="onStudentSelect($event.target.value)">
            <option value="">选择规划对象</option>
            <option v-for="s in students" :key="s.id" :value="s.id" :selected="selectedStudent?.id === s.id">{{ s.name || '未命名' }}</option>
          </select>
        </div>
      </div>

      <!-- 5 Progress Steps -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-5 mb-8">
        <div class="flex items-center justify-between">
          <template v-for="(step, i) in stepLabels" :key="i">
            <div class="flex flex-col items-center z-10">
              <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold transition-all',
                stepDone(i) ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/30' : 'bg-brand-surface border-2 border-brand-border text-brand-muted']">
                <i v-if="stepDone(i)" class="bi bi-check-lg"></i>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <p :class="['text-xs mt-2 whitespace-nowrap', stepDone(i) ? 'text-violet-400 font-medium' : 'text-brand-muted']">{{ step }}</p>
            </div>
            <div v-if="i < 4" class="flex-1 h-px mx-2 mt-[-16px]" :class="stepDone(i) ? 'bg-violet-600' : 'bg-brand-border'"></div>
          </template>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!selectedStudent" class="flex flex-col items-center justify-center py-20">
        <div class="w-16 h-16 rounded-2xl bg-brand-surface flex items-center justify-center mb-6">
          <i class="bi bi-signpost-split text-3xl text-brand-muted"></i>
        </div>
        <h2 class="text-lg font-semibold text-brand-text mb-2">请选择规划对象</h2>
        <p class="text-brand-muted text-sm mb-8 text-center max-w-md">选择学生后，系统将自动加载画像、匹配、路径与报告状态</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button v-for="s in students.slice(0, 8)" :key="s.id" @click="selectStudent(s)"
            class="bg-brand-card border border-brand-border rounded-xl p-3 text-left hover:border-violet-500/50 transition-all">
            <div class="font-medium text-brand-text text-sm">{{ s.name || '未命名' }}</div>
            <div class="text-xs text-brand-muted mt-1">{{ s.education || '学历未知' }} · {{ s.major || '专业未知' }}</div>
            <div class="mt-2 flex flex-wrap gap-1">
              <span :class="s.has_profile ? 'badge-green' : 'badge'" class="text-[10px]">{{ s.has_profile ? '有画像' : '无画像' }}</span>
              <span v-if="s.has_report" class="badge-orange text-[10px]">有报告</span>
            </div>
          </button>
        </div>
      </div>

      <template v-else>
        <!-- 4 Report Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <!-- Card: 自我画像 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 rounded-xl bg-violet-600/20 flex items-center justify-center">
                <i class="bi bi-person-badge text-violet-400 text-lg"></i>
              </div>
              <span :class="studentProfile ? 'badge-green' : 'badge'" class="text-xs">{{ studentProfile ? '已生成' : '未生成' }}</span>
            </div>
            <h3 class="font-semibold text-brand-text mb-1">自我画像</h3>
            <p class="text-xs text-brand-muted mb-3">能力评估与优势分析</p>
            <button v-if="!studentProfile" @click="generateProfile" :disabled="generatingProfile" class="btn-primary w-full text-sm">
              <i class="bi bi-magic mr-1" :class="{'animate-spin': generatingProfile}"></i>{{ generatingProfile ? '生成中...' : '生成画像' }}
            </button>
            <div v-else class="grid grid-cols-2 gap-2 text-center">
              <div class="rounded-lg bg-brand-surface p-2">
                <div class="text-sm font-bold text-violet-400">{{ Number(studentProfile.completeness_score || 0).toFixed(1) }}</div>
                <div class="text-[10px] text-brand-muted">完整度</div>
              </div>
              <div class="rounded-lg bg-brand-surface p-2">
                <div class="text-sm font-bold text-cyan-400">{{ Number(studentProfile.competitiveness_score || 0).toFixed(1) }}</div>
                <div class="text-[10px] text-brand-muted">竞争力</div>
              </div>
            </div>
          </div>

          <!-- Card: 人岗匹配 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 rounded-xl bg-cyan-600/20 flex items-center justify-center">
                <i class="bi bi-link-45deg text-cyan-400 text-lg"></i>
              </div>
              <span :class="matchResults.length ? 'badge-cyan' : 'badge'" class="text-xs">{{ matchResults.length ? matchResults.length + ' 条' : '未匹配' }}</span>
            </div>
            <h3 class="font-semibold text-brand-text mb-1">人岗匹配</h3>
            <p class="text-xs text-brand-muted mb-3">与目标岗位精准对比</p>
            <button v-if="!matchResults.length" @click="runMatchingAnalysis" :disabled="runningMatch" class="btn-primary w-full text-sm">
              <i class="bi bi-arrow-clockwise mr-1" :class="{'animate-spin': runningMatch}"></i>{{ runningMatch ? '匹配中...' : '开始匹配' }}
            </button>
            <div v-else-if="topMatchResult" class="text-center">
              <div class="text-2xl font-bold gradient-text">{{ Number(topMatchResult.overall_score || 0).toFixed(1) }}</div>
              <div class="text-xs text-brand-muted">最高匹配 · {{ topMatchResult.job_name }}</div>
            </div>
          </div>

          <!-- Card: 技能评估 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 rounded-xl bg-emerald-600/20 flex items-center justify-center">
                <i class="bi bi-lightning text-emerald-400 text-lg"></i>
              </div>
              <span :class="skillAnalysis ? 'badge-green' : 'badge'" class="text-xs">{{ skillAnalysis ? '匹配率 ' + skillAnalysisMatchRate + '%' : '待分析' }}</span>
            </div>
            <h3 class="font-semibold text-brand-text mb-1">技能评估</h3>
            <p class="text-xs text-brand-muted mb-3">技能差距与补齐建议</p>
            <div v-if="skillAnalysis" class="grid grid-cols-2 gap-2 text-center">
              <div class="rounded-lg bg-brand-surface p-2">
                <div class="text-sm font-bold text-emerald-400">{{ (skillAnalysis.matched || []).length }}</div>
                <div class="text-[10px] text-brand-muted">已匹配</div>
              </div>
              <div class="rounded-lg bg-brand-surface p-2">
                <div class="text-sm font-bold text-red-400">{{ (skillAnalysis.missing || []).length }}</div>
                <div class="text-[10px] text-brand-muted">待补齐</div>
              </div>
            </div>
            <div v-else class="text-xs text-brand-muted text-center py-2">需先完成匹配分析</div>
          </div>

          <!-- Card: 报告 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl p-5">
            <div class="flex items-center justify-between mb-3">
              <div class="w-10 h-10 rounded-xl bg-amber-600/20 flex items-center justify-center">
                <i class="bi bi-file-earmark-text text-amber-400 text-lg"></i>
              </div>
              <span :class="report ? 'badge-orange' : 'badge'" class="text-xs">{{ report ? reportStatusLabel : '未生成' }}</span>
            </div>
            <h3 class="font-semibold text-brand-text mb-1">职业规划</h3>
            <p class="text-xs text-brand-muted mb-3">完整的职业规划报告</p>
            <div v-if="!report" class="flex gap-2">
              <button @click="generateStandardReport" :disabled="!!generatingReport" class="btn-secondary flex-1 text-xs">
                <i class="bi bi-file-text mr-1" :class="{'animate-spin': generatingReport === 'standard'}"></i>标准
              </button>
              <button @click="generateMultiAgentReport" :disabled="!!generatingReport" class="btn-primary flex-1 text-xs">
                <i class="bi bi-robot mr-1" :class="{'animate-spin': generatingReport === 'multi'}"></i>AI
              </button>
            </div>
            <div v-else>
              <router-link :to="`/reports/${selectedStudent.id}`" class="btn-secondary w-full text-xs text-center block">
                <i class="bi bi-eye mr-1"></i>查看报告
              </router-link>
            </div>
          </div>
        </div>

        <!-- Accordion Panels -->
        <div class="space-y-3">
          <!-- Panel: 能力画像详情 -->
          <div v-if="studentProfile" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'profile' ? '' : 'profile'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-person-badge text-violet-400"></i>
                <span class="font-semibold text-brand-text text-sm">能力画像详情</span>
              </div>
              <i :class="activePanel === 'profile' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'profile'" class="p-4 pt-0">
              <div class="grid grid-cols-3 gap-2 mb-4">
                <div v-for="ability in profileAbilities" :key="ability.name"
                  class="rounded-lg border border-brand-border bg-brand-surface p-2 text-center">
                  <div class="text-sm font-bold" :class="abilityColorClass(ability.value)">{{ ability.value.toFixed(1) }}</div>
                  <div class="text-[11px] text-brand-muted">{{ ability.short }}</div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <div class="mb-1 text-xs text-brand-muted">优势标签</div>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="item in (studentProfile.strengths || []).slice(0, 6)" :key="item" class="badge-green text-xs">{{ item }}</span>
                    <span v-if="!(studentProfile.strengths || []).length" class="text-xs text-brand-muted">暂无</span>
                  </div>
                </div>
                <div>
                  <div class="mb-1 text-xs text-brand-muted">待提升</div>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="item in (studentProfile.weaknesses || []).slice(0, 6)" :key="item"
                      class="rounded-full border border-red-500/30 bg-red-500/10 px-2 py-1 text-xs text-red-300">{{ item }}</span>
                    <span v-if="!(studentProfile.weaknesses || []).length" class="text-xs text-brand-muted">暂无</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Panel: 匹配结果 -->
          <div v-if="matchResults.length" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'match' ? '' : 'match'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-link-45deg text-cyan-400"></i>
                <span class="font-semibold text-brand-text text-sm">匹配结果详情</span>
                <span class="badge-cyan text-xs">{{ matchResults.length }} 条</span>
              </div>
              <i :class="activePanel === 'match' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'match'" class="p-4 pt-0 space-y-3">
              <article v-for="match in matchResults" :key="match.id" class="rounded-xl border border-brand-border bg-brand-surface p-3">
                <div class="mb-2 flex items-start justify-between gap-3">
                  <div>
                    <div class="font-medium text-brand-text">{{ match.job_name || '岗位' }}</div>
                    <div class="text-xs text-brand-muted">{{ match.job_category || '未分类' }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-xl font-bold gradient-text">{{ Number(match.overall_score || 0).toFixed(1) }}</div>
                    <div class="text-xs text-brand-muted">匹配度</div>
                  </div>
                </div>
                <div class="grid grid-cols-4 gap-2 text-center text-xs">
                  <div class="rounded-lg border border-brand-border bg-brand-card p-2">
                    <div class="font-semibold text-violet-300">{{ Number(match.basic_score || 0).toFixed(0) }}</div>
                    <div class="text-brand-muted">基础</div>
                  </div>
                  <div class="rounded-lg border border-brand-border bg-brand-card p-2">
                    <div class="font-semibold text-cyan-300">{{ Number(match.skill_score || 0).toFixed(0) }}</div>
                    <div class="text-brand-muted">技能</div>
                  </div>
                  <div class="rounded-lg border border-brand-border bg-brand-card p-2">
                    <div class="font-semibold text-emerald-300">{{ Number(match.quality_score || 0).toFixed(0) }}</div>
                    <div class="text-brand-muted">素养</div>
                  </div>
                  <div class="rounded-lg border border-brand-border bg-brand-card p-2">
                    <div class="font-semibold text-amber-300">{{ Number(match.potential_score || 0).toFixed(0) }}</div>
                    <div class="text-brand-muted">潜力</div>
                  </div>
                </div>
                <div class="mt-2 flex flex-wrap gap-1">
                  <span v-for="gap in (match.skill_gaps || []).slice(0, 6)" :key="gap"
                    class="rounded-full border border-red-500/30 bg-red-500/10 px-2 py-1 text-xs text-red-300">{{ gap }}</span>
                </div>
              </article>
            </div>
          </div>

          <!-- Panel: 能力雷达 -->
          <div v-if="studentProfile && topMatchedJobProfile" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'radar' ? '' : 'radar'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-bullseye text-emerald-400"></i>
                <span class="font-semibold text-brand-text text-sm">能力雷达对照</span>
                <span v-if="topMatchResult" class="badge-cyan text-xs">vs {{ topMatchResult.job_name }}</span>
              </div>
              <i :class="activePanel === 'radar' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'radar'" class="p-4 pt-0">
              <RadarChart :series="radarSeries" :indicators="radarIndicators" height="300px" />
              <div class="mt-3 grid grid-cols-3 gap-2">
                <div v-for="row in abilityDiffRows" :key="row.name" class="rounded-lg border border-brand-border bg-brand-surface p-2 text-center">
                  <div class="text-[11px] text-brand-muted">{{ row.name }}</div>
                  <div :class="row.diff >= 0 ? 'text-emerald-400' : 'text-red-400'" class="text-sm font-semibold">
                    {{ row.diff >= 0 ? '+' : '' }}{{ row.diff.toFixed(1) }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Panel: 技能本体分析 -->
          <div v-if="skillAnalysis" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'skill' ? '' : 'skill'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-tools text-violet-400"></i>
                <span class="font-semibold text-brand-text text-sm">技能本体分析</span>
                <span class="badge-green text-xs">匹配率 {{ skillAnalysisMatchRate }}%</span>
              </div>
              <i :class="activePanel === 'skill' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'skill'" class="p-4 pt-0 space-y-3">
              <div class="grid grid-cols-4 gap-2 text-center">
                <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                  <div class="text-sm font-bold text-emerald-300">{{ (skillAnalysis.matched || []).length }}</div>
                  <div class="text-[11px] text-brand-muted">匹配</div>
                </div>
                <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                  <div class="text-sm font-bold text-red-300">{{ (skillAnalysis.missing || []).length }}</div>
                  <div class="text-[11px] text-brand-muted">缺失</div>
                </div>
                <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                  <div class="text-sm font-bold text-cyan-300">{{ (skillAnalysis.extra || []).length }}</div>
                  <div class="text-[11px] text-brand-muted">额外</div>
                </div>
                <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                  <div class="text-sm font-bold text-violet-300">{{ (skillAnalysis.transferable || []).length }}</div>
                  <div class="text-[11px] text-brand-muted">可迁移</div>
                </div>
              </div>
              <div>
                <div class="mb-1 text-xs text-brand-muted">优先补齐技能</div>
                <div class="flex flex-wrap gap-1">
                  <span v-for="skill in (skillAnalysis.missing || []).slice(0, 8)" :key="skill"
                    class="rounded-full border border-red-500/30 bg-red-500/10 px-2 py-1 text-xs text-red-300">{{ skill }}</span>
                  <span v-if="!(skillAnalysis.missing || []).length" class="text-xs text-brand-muted">暂无</span>
                </div>
              </div>
              <div>
                <div class="mb-1 text-xs text-brand-muted">分类覆盖度</div>
                <div class="space-y-2">
                  <div v-for="row in skillCoverageRows" :key="row.category">
                    <div class="mb-1 flex items-center justify-between text-xs">
                      <span class="text-brand-muted">{{ row.category }}</span>
                      <span class="text-cyan-300">{{ row.coverage }}%</span>
                    </div>
                    <div class="h-2 overflow-hidden rounded-full bg-brand-card">
                      <div class="h-full rounded-full bg-gradient-to-r from-cyan-500 to-violet-500" :style="{ width: row.coverage + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Panel: 职业路径 -->
          <div v-if="careerPaths.length || mdpStrategy" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'path' ? '' : 'path'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-signpost-split text-amber-400"></i>
                <span class="font-semibold text-brand-text text-sm">职业路径与MDP策略</span>
              </div>
              <i :class="activePanel === 'path' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'path'" class="p-4 pt-0">
              <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
                <div class="space-y-3">
                  <article v-for="(path, index) in careerPaths" :key="index" class="rounded-xl border border-brand-border bg-brand-surface p-3">
                    <div class="mb-2 flex items-center justify-between text-xs">
                      <span :class="path.type === 'promotion' ? 'text-emerald-300' : 'text-amber-300'">
                        {{ path.type === 'promotion' ? '晋升' : '转岗' }}
                      </span>
                      <span class="text-brand-muted">{{ path.years }}年 · 难度{{ path.difficulty }}</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-1 text-sm text-brand-text">
                      <template v-for="(node, nodeIndex) in path.nodes" :key="`${node}-${nodeIndex}`">
                        <span class="rounded-lg border border-brand-border bg-brand-card px-2 py-1">{{ node }}</span>
                        <i v-if="nodeIndex < path.nodes.length - 1" class="bi bi-chevron-right text-brand-muted"></i>
                      </template>
                    </div>
                  </article>
                  <div v-if="!careerPaths.length" class="text-xs text-brand-muted text-center py-4">暂无推荐路径</div>
                  <div v-if="reachableGroups.length" class="rounded-xl border border-brand-border bg-brand-surface p-3">
                    <div class="mb-2 text-xs text-brand-muted">N 跳可达岗位</div>
                    <div v-for="group in reachableGroups" :key="group.key" class="mb-2">
                      <div class="mb-1 text-xs text-brand-muted">{{ group.label }}</div>
                      <div class="flex flex-wrap gap-1">
                        <span v-for="position in group.positions.slice(0, 8)" :key="`${group.key}-${position}`" class="badge text-xs">{{ position }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="space-y-3">
                  <div v-if="mdpStrategy" class="rounded-xl border border-brand-border bg-brand-surface p-3">
                    <div class="mb-1 text-xs text-brand-muted">最优下一步</div>
                    <div class="text-base font-semibold text-violet-300">{{ mdpStrategy.optimal_action || '-' }}</div>
                    <div class="mt-1 text-xs text-brand-muted">期望价值 {{ Number(mdpStrategy.expected_value || 0).toFixed(2) }}</div>
                    <div v-if="mdpAlternatives.length" class="mt-2 space-y-1 text-xs">
                      <div v-for="alt in mdpAlternatives.slice(0, 4)" :key="alt.action"
                        class="flex items-center justify-between rounded-lg border border-brand-border bg-brand-card px-2 py-1">
                        <span :class="alt.is_optimal ? 'text-emerald-300' : 'text-brand-muted'">{{ alt.action }}</span>
                        <span class="text-cyan-300">{{ Number(alt.q_value || 0).toFixed(2) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="trajectoryNodes.length" class="rounded-xl border border-brand-border bg-brand-surface p-3">
                    <div class="mb-1 text-xs text-brand-muted">推荐发展轨迹</div>
                    <div class="flex flex-wrap items-center gap-1 text-sm text-brand-text">
                      <template v-for="(node, index) in trajectoryNodes" :key="`${node}-${index}`">
                        <span class="rounded-lg border border-brand-border bg-brand-card px-2 py-1">{{ node }}</span>
                        <i v-if="index < trajectoryNodes.length - 1" class="bi bi-chevron-right text-brand-muted"></i>
                      </template>
                    </div>
                  </div>
                  <div>
                    <div class="mb-1 text-xs text-brand-muted">相似岗位</div>
                    <div class="flex flex-wrap gap-1">
                      <span v-for="item in similarPositionRows.slice(0, 10)" :key="item.name" class="badge-cyan text-xs">
                        {{ item.name }}<template v-if="item.similarity !== null"> · {{ item.similarity.toFixed(3) }}</template>
                      </span>
                      <span v-if="!similarPositionRows.length" class="text-xs text-brand-muted">暂无</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Panel: 报告详情 -->
          <div v-if="report" class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'report' ? '' : 'report'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-file-earmark-text text-amber-400"></i>
                <span class="font-semibold text-brand-text text-sm">报告详情</span>
                <span class="badge-green text-xs">{{ reportStatusLabel }}</span>
              </div>
              <i :class="activePanel === 'report' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'report'" class="p-4 pt-0">
              <div class="rounded-xl border border-brand-border bg-brand-surface p-3 mb-3">
                <div class="mb-2 flex items-center justify-between">
                  <div class="font-medium text-brand-text">{{ report.title || '职业规划报告' }}</div>
                  <span class="text-xs text-brand-muted">{{ formatDate(report.created_at) }}</span>
                </div>
                <div class="grid grid-cols-3 gap-2 text-center">
                  <div v-for="item in reportSections" :key="item.key" class="rounded-lg border border-brand-border bg-brand-card p-2">
                    <div class="text-xs text-brand-muted">{{ item.label }}</div>
                    <div class="text-sm font-semibold text-violet-300">{{ sectionLength(item.key) }}</div>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <router-link :to="`/reports/${selectedStudent.id}`" class="btn-secondary text-center text-sm">
                  <i class="bi bi-eye mr-1"></i>查看
                </router-link>
                <router-link :to="`/reports/${selectedStudent.id}/edit`" class="btn-secondary text-center text-sm">
                  <i class="bi bi-pencil mr-1"></i>编辑
                </router-link>
              </div>
            </div>
          </div>

          <!-- Panel: 行动建议 -->
          <div class="bg-brand-card border border-brand-border rounded-2xl overflow-hidden">
            <button @click="activePanel = activePanel === 'action' ? '' : 'action'"
              class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/50 transition-all">
              <div class="flex items-center gap-3">
                <i class="bi bi-rocket text-cyan-400"></i>
                <span class="font-semibold text-brand-text text-sm">行动建议</span>
                <span class="text-xs text-brand-muted">{{ actionSuggestions.length }} 条</span>
              </div>
              <i :class="activePanel === 'action' ? 'bi-chevron-up' : 'bi-chevron-down'" class="text-brand-muted"></i>
            </button>
            <div v-show="activePanel === 'action'" class="p-4 pt-0 space-y-3">
              <article v-for="(action, index) in actionSuggestions" :key="`${action.title}-${index}`"
                class="rounded-xl border border-brand-border bg-brand-surface p-3">
                <div class="mb-2 flex items-center gap-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg text-white" :style="{ background: action.gradient }">
                    <i :class="action.icon"></i>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-brand-text">{{ action.title }}</div>
                    <div class="text-xs text-brand-muted">{{ action.timeline }}</div>
                  </div>
                </div>
                <p class="mb-2 text-sm text-brand-muted">{{ action.desc }}</p>
                <div class="flex flex-wrap gap-1">
                  <span v-for="tag in action.tags" :key="tag" class="badge text-xs">{{ tag }}</span>
                </div>
              </article>
            </div>
          </div>
        </div>

        <!-- Graph Insights -->
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-6">
          <div class="bg-brand-card border border-brand-border rounded-2xl p-4">
            <div class="mb-3 flex items-center justify-between">
              <h3 class="font-semibold text-brand-text text-sm flex items-center gap-2">
                <i class="bi bi-graph-up text-violet-400"></i>图谱热度 PageRank
              </h3>
              <span class="text-xs text-brand-muted">Top {{ topPositionImportance.length }}</span>
            </div>
            <div v-if="topPositionImportance.length" class="space-y-2">
              <div v-for="(item, index) in topPositionImportance" :key="item.name"
                class="rounded-lg border border-brand-border bg-brand-surface p-2">
                <div class="mb-1 flex items-center justify-between text-sm">
                  <span class="text-brand-text">{{ index + 1 }}. {{ item.name }}</span>
                  <span class="text-cyan-300 text-xs">{{ item.score.toFixed(4) }}</span>
                </div>
                <div class="h-1.5 overflow-hidden rounded-full bg-brand-card">
                  <div class="h-full rounded-full bg-gradient-to-r from-violet-600 to-cyan-500"
                    :style="{ width: `${(item.score / maxPositionScore) * 100}%` }"></div>
                </div>
              </div>
            </div>
            <div v-else class="text-center text-sm text-brand-muted py-4">暂无图谱热度数据</div>
          </div>

          <div class="bg-brand-card border border-brand-border rounded-2xl p-4">
            <div class="mb-3 flex items-center justify-between">
              <h3 class="font-semibold text-brand-text text-sm flex items-center gap-2">
                <i class="bi bi-diagram-3 text-cyan-400"></i>岗位社区洞察
              </h3>
              <span class="text-xs text-brand-muted" v-if="communityMeta.modularity > 0">模块度 {{ communityMeta.modularity.toFixed(3) }}</span>
            </div>
            <div class="mb-3 grid grid-cols-2 gap-2 text-center">
              <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                <div class="text-lg font-bold text-violet-400">{{ communityMeta.num_communities }}</div>
                <div class="text-xs text-brand-muted">社区数量</div>
              </div>
              <div class="rounded-lg border border-brand-border bg-brand-surface p-2">
                <div class="text-lg font-bold text-cyan-400">{{ largestCommunitySize }}</div>
                <div class="text-xs text-brand-muted">最大社区</div>
              </div>
            </div>
            <div v-if="communityPreview.length" class="space-y-2">
              <div v-for="(community, index) in communityPreview" :key="`community-${index}`"
                class="rounded-lg border border-brand-border bg-brand-surface p-2 text-xs">
                <div class="mb-1 text-brand-text">社区 {{ index + 1 }} · {{ community.size }} 岗位</div>
                <div class="text-brand-muted">{{ community.sample.join(' / ') }}</div>
              </div>
            </div>
            <div v-else class="text-center text-xs text-brand-muted py-4">暂无社区聚类结果</div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue'
import RadarChart from '@/components/RadarChart.vue'
import {
  generateAdvancedReport,
  generateReport,
  generateStudentProfile as apiGenerateProfile,
  getCareerMdpStrategy,
  getCareerPaths,
  getCareerTrajectory,
  getGraphJobClusters,
  getGraphPositionImportance,
  getGraphReachable,
  getJobProfiles,
  getPositionClusters,
  getSimilarPositions,
  getSkillAnalysis,
  getStudent,
  getStudents,
  runMatching,
} from '@/api'

const toast = inject('toast', null)

const students = ref([])
const jobProfiles = ref([])

const selectedStudent = ref(null)
const studentProfile = ref(null)
const matchResults = ref([])
const report = ref(null)
const careerPaths = ref([])

const skillAnalysis = ref(null)
const reachableMap = ref({})
const similarPositions = ref([])
const mdpStrategy = ref(null)
const trajectoryPlan = ref(null)

const positionImportance = ref([])
const communityBuckets = ref([])
const communityMeta = ref({ num_communities: 0, modularity: 0 })

const generatingProfile = ref(false)
const runningMatch = ref(false)
const generatingReport = ref('')
const planningLoading = ref(false)
const activePanel = ref('')

const stepLabels = ['自我画像', '职业探索', '技能评估', '路径规划', '报告生成']

function stepDone(index) {
  if (index === 0) return !!studentProfile.value
  if (index === 1) return matchResults.value.length > 0
  if (index === 2) return !!skillAnalysis.value
  if (index === 3) return careerPaths.value.length > 0
  if (index === 4) return !!report.value
  return false
}

function onStudentSelect(id) {
  const student = students.value.find(s => String(s.id) === String(id))
  if (student) selectStudent(student)
}

const reportSections = [
  { key: 'section_self_assessment', label: '自我评估' },
  { key: 'section_job_exploration', label: '职业探索' },
  { key: 'section_career_goal', label: '目标设定' },
  { key: 'section_career_path', label: '路径规划' },
  { key: 'section_action_plan', label: '行动计划' },
  { key: 'section_evaluation', label: '评估调整' },
]

const abilityMeta = [
  { key: 'innovation_ability', name: '创新能力', short: '创新' },
  { key: 'learning_ability', name: '学习能力', short: '学习' },
  { key: 'pressure_resistance', name: '抗压能力', short: '抗压' },
  { key: 'communication_skill', name: '沟通能力', short: '沟通' },
  { key: 'teamwork_ability', name: '团队协作', short: '团队' },
  { key: 'internship_ability', name: '实践能力', short: '实践' },
]

const profileAbilities = computed(() => {
  if (!studentProfile.value) return []
  return abilityMeta.map((meta) => ({
    ...meta,
    value: Number(studentProfile.value[meta.key] || 0),
  }))
})

const topMatchResult = computed(() => {
  if (!matchResults.value.length) return null
  return [...matchResults.value].sort(
    (a, b) => Number(b.overall_score || 0) - Number(a.overall_score || 0),
  )[0]
})

const topMatchedJobProfile = computed(() => {
  const top = topMatchResult.value
  if (!top) return null

  const byId = jobProfiles.value.find(
    (profile) => Number(profile.id) === Number(top.job_profile_id),
  )
  if (byId) return byId

  return (
    jobProfiles.value.find(
      (profile) =>
        String(profile.position_name || '').trim() === String(top.job_name || '').trim(),
    ) || null
  )
})

const targetJobAbilities = computed(() => {
  if (!topMatchedJobProfile.value) return []
  return abilityMeta.map((meta) => ({
    ...meta,
    value: Number(topMatchedJobProfile.value[meta.key] || 0),
  }))
})

const radarIndicators = computed(() => abilityMeta.map((item) => item.name))
const radarSeries = computed(() => [
  {
    name: '学生能力',
    values: profileAbilities.value.map((item) => Number(item.value || 0)),
    color: '#7c3aed',
  },
  {
    name: '岗位要求',
    values: targetJobAbilities.value.map((item) => Number(item.value || 0)),
    color: '#06b6d4',
  },
])

const abilityDiffRows = computed(() =>
  abilityMeta.map((meta, index) => {
    const studentValue = Number(profileAbilities.value[index]?.value || 0)
    const targetValue = Number(targetJobAbilities.value[index]?.value || 0)
    return {
      name: meta.name,
      diff: studentValue - targetValue,
    }
  }),
)

const totalMatchRecords = computed(() =>
  students.value.reduce((sum, student) => sum + Number(student.match_count || 0), 0),
)

const reportCount = computed(() => students.value.filter((student) => student.has_report).length)

const reportStatusLabel = computed(() => {
  const map = {
    draft: '草稿',
    generated: '已生成',
    edited: '已编辑',
    exported: '已导出',
  }
  return map[report.value?.status] || '已生成'
})

const topPositionImportance = computed(() =>
  [...positionImportance.value]
    .sort((a, b) => Number(b.score || 0) - Number(a.score || 0))
    .slice(0, 8),
)

const maxPositionScore = computed(() => {
  if (!topPositionImportance.value.length) return 1
  return Math.max(...topPositionImportance.value.map((item) => Number(item.score || 0)), 1)
})

const communityPreview = computed(() =>
  communityBuckets.value.slice(0, 3).map((group) => ({
    size: group.length,
    sample: group.slice(0, 4),
  })),
)

const largestCommunitySize = computed(() => {
  if (!communityBuckets.value.length) return 0
  return Math.max(...communityBuckets.value.map((group) => group.length))
})

const skillAnalysisMatchRate = computed(() =>
  Math.round(Number(skillAnalysis.value?.match_rate || 0) * 100),
)

const skillCoverageRows = computed(() => {
  const coverage = skillAnalysis.value?.category_coverage || {}
  return Object.entries(coverage)
    .map(([category, detail]) => ({
      category,
      coverage: Math.round(Number(detail.coverage || 0) * 100),
    }))
    .sort((a, b) => b.coverage - a.coverage)
})

const reachableGroups = computed(() => {
  const source = reachableMap.value || {}
  return Object.keys(source)
    .filter((key) => key.startsWith('hop_'))
    .sort()
    .map((key) => {
      const rows = Array.isArray(source[key]) ? source[key] : []
      return {
        key,
        label: key.replace('_', ' ').toUpperCase(),
        positions: rows.map(extractPosition).filter(Boolean),
      }
    })
    .filter((group) => group.positions.length > 0)
})

const similarPositionRows = computed(() =>
  (similarPositions.value || [])
    .map((item) => ({
      name: item.name,
      similarity: item.similarity,
    }))
    .filter((item) => item.name),
)

const mdpAlternatives = computed(() => mdpStrategy.value?.alternative_actions || [])
const trajectoryNodes = computed(() => trajectoryPlan.value?.trajectory || [])

const actionSuggestions = computed(() => {
  const suggestions = []
  const topMatch = topMatchResult.value

  if (topMatch) {
    const gaps = (skillAnalysis.value?.missing || topMatch.skill_gaps || []).slice(0, 3)
    suggestions.push({
      title: '技能补齐计划',
      timeline: '短期（1-2个月）',
      desc: gaps.length
        ? `优先补齐 ${gaps.join('、')}，先修正关键差距再扩大投递面。`
        : '核心技能匹配较好，可转向项目深度和面试表达强化。',
      icon: 'bi bi-tools',
      gradient: 'linear-gradient(135deg, #7C3AED, #5B21B6)',
      tags: gaps.length ? gaps : ['技能巩固', '项目强化'],
    })

    suggestions.push({
      title: '目标岗位推进',
      timeline: '中期（2-4个月）',
      desc: `围绕 ${topMatch.job_name || '目标岗位'} 建立“作品-简历-面试”闭环，提升转化效率。`,
      icon: 'bi bi-briefcase',
      gradient: 'linear-gradient(135deg, #06B6D4, #0891B2)',
      tags: ['岗位画像', '投递节奏', '复盘优化'],
    })
  }

  if (mdpStrategy.value?.optimal_action) {
    suggestions.push({
      title: '策略路径执行',
      timeline: '中长期（4-8个月）',
      desc: `优先朝 ${mdpStrategy.value.optimal_action} 方向积累，按策略轨迹逐步迁移。`,
      icon: 'bi bi-signpost-split',
      gradient: 'linear-gradient(135deg, #10B981, #059669)',
      tags: ['MDP策略', '路径迁移', '长期收益'],
    })
  }

  suggestions.push({
    title: '证据与成果沉淀',
    timeline: '持续进行',
    desc: '将学习成果沉淀为可验证项目、面试案例与报告证据，提升竞争力稳定性。',
    icon: 'bi bi-kanban',
    gradient: 'linear-gradient(135deg, #F59E0B, #D97706)',
    tags: ['项目实战', '成长记录', '能力证明'],
  })

  return suggestions
})

function unwrapData(response) {
  return response?.data?.data ?? response?.data ?? null
}

function extractPosition(item) {
  if (typeof item === 'string') return item
  if (!item || typeof item !== 'object') return ''
  return item.position || item.to_position || item.name || item.action || ''
}

function normalizeImportance(raw) {
  if (!raw) return []

  if (Array.isArray(raw)) {
    return raw
      .map((item) => {
        if (typeof item === 'string') return { name: item, score: 0 }
        return {
          name: item.name || item.position || '',
          score: Number(item.score ?? item.value ?? 0),
        }
      })
      .filter((item) => item.name)
  }

  if (typeof raw === 'object') {
    return Object.entries(raw).map(([name, score]) => ({
      name,
      score: Number(score || 0),
    }))
  }

  return []
}

function normalizeCommunities(raw) {
  if (!raw || typeof raw !== 'object') {
    return {
      communities: [],
      num_communities: 0,
      modularity: 0,
    }
  }

  let communities = []
  if (Array.isArray(raw.communities)) {
    communities = raw.communities.filter((group) => Array.isArray(group))
  } else if (raw.clusters && typeof raw.clusters === 'object') {
    communities = Object.values(raw.clusters).filter((group) => Array.isArray(group))
  }

  return {
    communities,
    num_communities: Number(raw.num_communities || raw.n_clusters || communities.length || 0),
    modularity: Number(raw.modularity || 0),
  }
}

function normalizeSimilar(raw) {
  const rows = raw?.similar_positions || []
  if (!Array.isArray(rows)) return []

  return rows
    .map((item) => {
      if (typeof item === 'string') {
        return { name: item, similarity: null }
      }
      if (!item || typeof item !== 'object') {
        return { name: '', similarity: null }
      }
      return {
        name: item.name || item.position || '',
        similarity: item.similarity !== undefined ? Number(item.similarity) : null,
      }
    })
    .filter((item) => item.name)
}

function mapCareerPaths(pathData) {
  const transfer = pathData?.transfers || []
  const promotionsFrom = pathData?.promotions_from || []
  const promotionsTo = pathData?.promotions_to || []

  return [
    ...promotionsFrom.map((item) => ({
      type: 'promotion',
      years: Number(item.estimated_years || 2),
      nodes: [item.from_position, item.to_position].filter(Boolean),
      difficulty: Number(item.difficulty || 3),
    })),
    ...transfer.map((item) => ({
      type: 'transfer',
      years: Number(item.estimated_years || 1),
      nodes: [item.from_position, item.to_position].filter(Boolean),
      difficulty: Number(item.difficulty || 3),
    })),
    ...promotionsTo.map((item) => ({
      type: 'promotion',
      years: Number(item.estimated_years || 2),
      nodes: [item.from_position, item.to_position].filter(Boolean),
      difficulty: Number(item.difficulty || 3),
    })),
  ]
}

function abilityColorClass(value) {
  if (value >= 8) return 'text-emerald-400'
  if (value >= 6) return 'text-cyan-400'
  if (value >= 4) return 'text-amber-400'
  return 'text-red-400'
}

function formatDate(value) {
  if (!value) return '-'
  return new Date(value).toLocaleString('zh-CN')
}

function sectionLength(key) {
  return (report.value?.[key] || '').length
}

async function loadGlobalInsights() {
  try {
    const [importanceRes, clustersRes, positionClustersRes] = await Promise.allSettled([
      getGraphPositionImportance(),
      getGraphJobClusters(),
      getPositionClusters(5),
    ])

    if (importanceRes.status === 'fulfilled') {
      positionImportance.value = normalizeImportance(unwrapData(importanceRes.value)).sort(
        (a, b) => Number(b.score || 0) - Number(a.score || 0),
      )
    }

    let communityRaw = null
    if (clustersRes.status === 'fulfilled') {
      communityRaw = unwrapData(clustersRes.value)
    }

    let normalized = normalizeCommunities(communityRaw)

    if (!normalized.communities.length && positionClustersRes.status === 'fulfilled') {
      normalized = normalizeCommunities(unwrapData(positionClustersRes.value))
    }

    communityBuckets.value = normalized.communities
    communityMeta.value = {
      num_communities: normalized.num_communities,
      modularity: normalized.modularity,
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '图谱洞察加载失败', 'danger')
  }
}

async function hydrateTopMatchInsights() {
  careerPaths.value = []
  skillAnalysis.value = null
  reachableMap.value = {}
  similarPositions.value = []
  mdpStrategy.value = null
  trajectoryPlan.value = null

  const sid = selectedStudent.value?.id
  const top = topMatchResult.value
  if (!sid || !top) return

  const targetPosition = top.job_name
  const targetJobProfileId = Number(top.job_profile_id || topMatchedJobProfile.value?.id || 0)

  planningLoading.value = true
  try {
    const [pathRes, reachableRes, strategyRes, trajectoryRes, similarRes, skillRes] =
      await Promise.allSettled([
        targetPosition ? getCareerPaths(targetPosition) : Promise.resolve({ data: { data: {} } }),
        targetPosition
          ? getGraphReachable(targetPosition, 2)
          : Promise.resolve({ data: { data: {} } }),
        targetPosition
          ? getCareerMdpStrategy(targetPosition)
          : Promise.resolve({ data: { data: null } }),
        targetPosition
          ? getCareerTrajectory(targetPosition, 5)
          : Promise.resolve({ data: { data: null } }),
        targetPosition
          ? getSimilarPositions(targetPosition, 8)
          : Promise.resolve({ data: { data: { similar_positions: [] } } }),
        targetJobProfileId
          ? getSkillAnalysis(sid, targetJobProfileId)
          : Promise.resolve({ data: { data: null } }),
      ])

    if (pathRes.status === 'fulfilled') {
      const pathData = unwrapData(pathRes.value) || {}
      careerPaths.value = mapCareerPaths(pathData).slice(0, 8)
    }

    if (reachableRes.status === 'fulfilled') {
      reachableMap.value = unwrapData(reachableRes.value) || {}
    }

    if (strategyRes.status === 'fulfilled') {
      const strategy = unwrapData(strategyRes.value)
      mdpStrategy.value = strategy && !strategy.error ? strategy : null
    }

    if (trajectoryRes.status === 'fulfilled') {
      const trajectory = unwrapData(trajectoryRes.value)
      trajectoryPlan.value = trajectory && !trajectory.error ? trajectory : null
    }

    if (similarRes.status === 'fulfilled') {
      similarPositions.value = normalizeSimilar(unwrapData(similarRes.value) || {})
    }

    if (skillRes.status === 'fulfilled') {
      const analysis = unwrapData(skillRes.value)
      skillAnalysis.value = analysis && !analysis.error ? analysis : null
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '规划智能分析失败', 'danger')
  } finally {
    planningLoading.value = false
  }
}

async function selectStudent(student) {
  selectedStudent.value = student
  studentProfile.value = null
  matchResults.value = []
  report.value = null

  try {
    const response = await getStudent(student.id)
    selectedStudent.value = response.data?.student || selectedStudent.value
    studentProfile.value = response.data?.profile || null
    matchResults.value = response.data?.match_results || []
    report.value = response.data?.report || null

    await hydrateTopMatchInsights()
  } catch (error) {
    toast?.(error?.response?.data?.message || '加载学生规划数据失败', 'danger')
  }
}

async function generateProfile() {
  if (!selectedStudent.value) return
  generatingProfile.value = true
  try {
    const response = await apiGenerateProfile(selectedStudent.value.id)
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

async function runMatchingAnalysis() {
  if (!selectedStudent.value) return
  runningMatch.value = true
  try {
    const response = await runMatching(selectedStudent.value.id, 5)
    if (response.data?.success) {
      matchResults.value = response.data.data || []
      toast?.('匹配分析完成', 'success')
      await selectStudent(selectedStudent.value)
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '匹配分析失败', 'danger')
  } finally {
    runningMatch.value = false
  }
}

async function generateStandardReport() {
  if (!selectedStudent.value) return
  generatingReport.value = 'standard'
  try {
    const response = await generateReport(selectedStudent.value.id)
    if (response.data?.success) {
      report.value = response.data.data
      selectedStudent.value.has_report = true
      const row = students.value.find((item) => item.id === selectedStudent.value.id)
      if (row) row.has_report = true
      toast?.('标准报告生成成功', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || '标准报告生成失败', 'danger')
  } finally {
    generatingReport.value = ''
  }
}

async function generateMultiAgentReport() {
  if (!selectedStudent.value) return
  generatingReport.value = 'multi'
  try {
    const response = await generateAdvancedReport(selectedStudent.value.id, true)
    if (response.data?.success) {
      report.value = response.data.data
      selectedStudent.value.has_report = true
      const row = students.value.find((item) => item.id === selectedStudent.value.id)
      if (row) row.has_report = true
      toast?.('Multi-Agent 报告生成成功', 'success')
    }
  } catch (error) {
    toast?.(error?.response?.data?.message || 'Multi-Agent 报告生成失败', 'danger')
  } finally {
    generatingReport.value = ''
  }
}

async function loadStudentsAndProfiles() {
  try {
    const [studentsResponse, profilesResponse] = await Promise.all([
      getStudents(),
      getJobProfiles(),
    ])
    students.value = studentsResponse.data || []
    jobProfiles.value = profilesResponse.data?.profiles || []
  } catch (error) {
    toast?.(error?.response?.data?.message || '加载学生与岗位画像失败', 'danger')
  }
}

onMounted(async () => {
  await Promise.all([loadStudentsAndProfiles(), loadGlobalInsights()])
  if (students.value.length) {
    await selectStudent(students.value[0])
  }
})
</script>
