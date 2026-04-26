<template>
  <div class="min-h-screen bg-brand-bg py-8">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">

      <!-- ═══ Page Header ═══ -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-bold text-brand-text flex items-center gap-2">
            <i class="bi bi-rocket-takeoff text-violet-400"></i> 自我画像
          </h1>
          <p class="text-sm text-brand-muted mt-1">完善你的能力档案，解锁精准职业匹配</p>
        </div>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-3">
            <span class="text-xs text-brand-muted">档案完整度</span>
            <div class="w-24 h-1.5 rounded-full bg-brand-surface overflow-hidden">
              <div class="h-full bg-gradient-to-r from-violet-600 to-cyan-500 transition-all duration-500 rounded-full" :style="{ width: completeness + '%' }"></div>
            </div>
            <span class="text-sm font-bold" :class="completeness >= 60 ? 'text-emerald-400' : 'text-violet-400'">{{ completeness }}%</span>
          </div>
          <button
            :class="completeness >= 60 ? 'btn-primary text-xs' : 'px-4 py-2 rounded-xl text-xs border border-brand-border text-brand-muted cursor-not-allowed'"
            :disabled="completeness < 60"
            @click="completeness >= 60 && router.push('/career/explore')"
          >开始匹配（需≥60%）</button>
        </div>
      </div>

      <!-- ═══ Step Tabs ═══ -->
      <div class="flex gap-1 mb-6">
        <button
          v-for="(s, i) in steps" :key="i"
          @click="step = i"
          :class="[
            'flex items-center gap-2 px-4 py-2 rounded-xl text-sm transition-all',
            step === i
              ? 'bg-violet-600/20 text-violet-300 border border-violet-500/30'
              : 'text-brand-muted hover:text-brand-text hover:bg-brand-surface'
          ]"
        >
          <i :class="s.icon" class="text-base"></i>
          {{ s.label }}
        </button>
      </div>

      <!-- ═══ Mode Toggle: 填写 / 查看画像 ═══ -->
      <div class="flex gap-2 mb-6">
        <button
          @click="viewMode = 'edit'"
          :class="[
            'flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all',
            viewMode === 'edit'
              ? 'bg-gradient-to-r from-orange-600 to-orange-500 text-white'
              : 'bg-brand-surface text-brand-muted hover:text-brand-text border border-brand-border'
          ]"
        >
          <i class="bi bi-pencil-square"></i> 填写信息
        </button>
        <button
          @click="viewMode = 'view'"
          :class="[
            'flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all',
            viewMode === 'view'
              ? 'bg-gradient-to-r from-emerald-600 to-emerald-500 text-white'
              : 'bg-brand-surface text-brand-muted hover:text-brand-text border border-brand-border'
          ]"
        >
          <i class="bi bi-eye"></i> 查看画像
        </button>
      </div>

      <!-- ════════════════════════════════════════ -->
      <!-- EDIT MODE                                -->
      <!-- ════════════════════════════════════════ -->
      <template v-if="viewMode === 'edit'">
        <Transition name="fade" mode="out-in">

          <!-- Step 0: 基本信息 -->
          <div v-if="step === 0" key="basic">
            <h2 class="text-lg font-semibold text-brand-text mb-6 flex items-center gap-3">
              <span class="w-7 h-7 rounded-full bg-violet-600 text-white text-xs flex items-center justify-center">1</span>
              基本信息
            </h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div class="lg:col-span-2">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">姓名</label>
                    <input v-model="form.name" type="text" class="input-base" placeholder="你的名字">
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">年龄</label>
                    <input v-model="form.age" type="text" class="input-base" placeholder="如：22">
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">学历</label>
                    <select v-model="form.education" class="input-base">
                      <option value="">请选择</option>
                      <option value="高中">高中</option>
                      <option value="大专">大专</option>
                      <option value="本科">本科</option>
                      <option value="硕士">硕士</option>
                      <option value="博士">博士</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">工作经验</label>
                    <select v-model="form.experience" class="input-base">
                      <option value="">请选择</option>
                      <option value="应届">应届生</option>
                      <option value="1年以下">1年以下</option>
                      <option value="1-3年">1-3年</option>
                      <option value="3-5年">3-5年</option>
                      <option value="5-10年">5-10年</option>
                      <option value="10年以上">10年以上</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">专业</label>
                    <input v-model="form.major" type="text" class="input-base" placeholder="如：计算机科学">
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">院校</label>
                    <input v-model="form.school" type="text" class="input-base" placeholder="如：北京大学">
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">当前城市</label>
                    <input v-model="form.currentCity" type="text" class="input-base" placeholder="如：北京">
                  </div>
                  <div>
                    <label class="block text-sm text-brand-muted mb-2">期望城市</label>
                    <input v-model="targetCityStr" type="text" class="input-base" placeholder="多个城市用逗号分隔">
                  </div>
                </div>
              </div>
              <!-- Info sidebar -->
              <div class="card-sm p-5">
                <h4 class="text-sm font-medium text-brand-text flex items-center gap-2 mb-3">
                  <i class="bi bi-info-circle text-violet-400"></i> 为什么需要这些信息？
                </h4>
                <ul class="space-y-2 text-xs text-brand-muted">
                  <li class="flex items-start gap-2"><span class="text-violet-400 mt-0.5">•</span>学历和专业用于初步职业方向筛选</li>
                  <li class="flex items-start gap-2"><span class="text-violet-400 mt-0.5">•</span>工作经验决定你在路径图中的起点</li>
                  <li class="flex items-start gap-2"><span class="text-violet-400 mt-0.5">•</span>城市信息匹配当地薪资水平和机会</li>
                  <li class="flex items-start gap-2"><span class="text-violet-400 mt-0.5">•</span>所有数据仅用于本地分析，不会上传</li>
                </ul>
              </div>
            </div>
            <div class="mt-8">
              <button @click="step = 1" class="w-full py-3 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 text-white font-medium hover:from-violet-700 hover:to-violet-600 transition-all">
                保存并继续 →
              </button>
            </div>
          </div>

          <!-- Step 1: 工作 & 项目经历 -->
          <div v-else-if="step === 1" key="experience">
            <h2 class="text-lg font-semibold text-brand-text mb-6 flex items-center gap-3">
              <span class="w-7 h-7 rounded-full bg-emerald-600 text-white text-xs flex items-center justify-center">2</span>
              工作 &amp; 项目经历
            </h2>

            <!-- Work Experience -->
            <div class="card mb-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-brand-text flex items-center gap-2">
                  <i class="bi bi-briefcase text-violet-400"></i> 工作经历
                </h3>
                <button @click="showWorkModal = true" class="text-sm text-violet-400 hover:text-violet-300 transition-colors">+ 添加</button>
              </div>
              <div v-if="form.workExperiences.length === 0" class="text-center py-10 text-brand-muted text-sm">
                暂无工作经历，点击「添加」填写
              </div>
              <div v-else class="space-y-3">
                <div v-for="(exp, i) in form.workExperiences" :key="i" class="bg-brand-surface border border-brand-border rounded-xl p-4">
                  <div class="flex justify-between items-start">
                    <div>
                      <h4 class="font-medium text-brand-text">{{ exp.company }}</h4>
                      <p class="text-sm text-brand-muted">{{ exp.role }} · {{ exp.duration }}</p>
                    </div>
                    <button @click="removeWork(i)" class="text-red-400 hover:text-red-300"><i class="bi bi-trash"></i></button>
                  </div>
                  <p v-if="exp.desc" class="text-sm text-brand-muted mt-2">{{ exp.desc }}</p>
                </div>
              </div>
            </div>

            <!-- Project Experience -->
            <div class="card mb-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-brand-text flex items-center gap-2">
                  <i class="bi bi-rocket text-pink-400"></i> 项目经历
                </h3>
                <button @click="showProjectModal = true" class="text-sm text-violet-400 hover:text-violet-300 transition-colors">+ 添加</button>
              </div>
              <div v-if="form.projectExperiences.length === 0" class="text-center py-10 text-brand-muted text-sm">
                暂无项目经历，点击「添加」填写
              </div>
              <div v-else class="space-y-3">
                <div v-for="(proj, i) in form.projectExperiences" :key="i" class="bg-brand-surface border border-brand-border rounded-xl p-4">
                  <div class="flex justify-between items-start mb-2">
                    <div>
                      <h4 class="font-medium text-brand-text">{{ proj.name }}</h4>
                      <p class="text-sm text-brand-muted">{{ proj.role }}</p>
                    </div>
                    <button @click="removeProject(i)" class="text-red-400 hover:text-red-300"><i class="bi bi-trash"></i></button>
                  </div>
                  <div class="flex flex-wrap gap-1 mb-2">
                    <span v-for="t in proj.tech" :key="t" class="badge text-xs">{{ t }}</span>
                  </div>
                  <p v-if="proj.desc" class="text-sm text-brand-muted">{{ proj.desc }}</p>
                </div>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="step = 0" class="flex-1 py-3 rounded-xl border border-brand-border text-brand-muted hover:text-brand-text transition-colors">← 上一步</button>
              <button @click="step = 2" class="flex-1 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 text-white font-medium hover:from-violet-700 hover:to-violet-600 transition-all">保存并继续 →</button>
            </div>
          </div>

          <!-- Step 2: 技术技能 -->
          <div v-else-if="step === 2" key="skills">
            <h2 class="text-lg font-semibold text-brand-text mb-6 flex items-center gap-3">
              <span class="w-7 h-7 rounded-full bg-amber-600 text-white text-xs flex items-center justify-center">3</span>
              技术技能
            </h2>

            <!-- Quick Select -->
            <div class="card mb-6">
              <h3 class="font-medium text-brand-text flex items-center gap-2 mb-4">
                <i class="bi bi-lightning text-amber-400"></i> 快速选择常用技能
              </h3>
              <div class="space-y-4">
                <div v-for="cat in skillCategories" :key="cat.name">
                  <div class="text-xs text-violet-400 mb-2">{{ cat.name }}</div>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="skill in cat.items" :key="skill"
                      @click="toggleQuickSkill(skill, cat.name)"
                      :class="[
                        'px-3 py-1.5 rounded-lg text-sm transition-all',
                        hasSkill(skill)
                          ? 'bg-violet-600 text-white'
                          : 'bg-brand-surface text-brand-muted hover:bg-brand-card border border-brand-border'
                      ]"
                    >{{ skill }}</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- My Skills -->
            <div class="card mb-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-brand-text flex items-center gap-2">
                  <i class="bi bi-collection text-cyan-400"></i> 我的技能（{{ form.skills.length }}项）
                </h3>
                <button @click="showSkillModal = true" class="text-sm text-violet-400 hover:text-violet-300 transition-colors">+ 自定义添加</button>
              </div>
              <div v-if="form.skills.length === 0" class="text-center py-8 text-brand-muted text-sm">
                点击上方标签快速添加技能
              </div>
              <div v-else class="flex flex-wrap gap-2">
                <div v-for="(skill, i) in form.skills" :key="i"
                  class="flex items-center gap-2 bg-brand-surface border border-brand-border rounded-lg px-3 py-1.5 text-sm">
                  <span class="text-brand-text">{{ skill.name }}</span>
                  <span class="text-xs text-brand-muted">{{ skill.category }}</span>
                  <button @click="removeSkill(i)" class="text-red-400 hover:text-red-300 ml-1"><i class="bi bi-x"></i></button>
                </div>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="step = 1" class="flex-1 py-3 rounded-xl border border-brand-border text-brand-muted hover:text-brand-text transition-colors">← 上一步</button>
              <button @click="step = 3" class="flex-1 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 text-white font-medium hover:from-violet-700 hover:to-violet-600 transition-all">保存并继续 →</button>
            </div>
          </div>

          <!-- Step 3: 性格偏好 -->
          <div v-else-if="step === 3" key="personality">
            <h2 class="text-lg font-semibold text-brand-text mb-6 flex items-center gap-3">
              <span class="w-7 h-7 rounded-full bg-pink-600 text-white text-xs flex items-center justify-center">4</span>
              性格偏好
            </h2>

            <!-- Bipolar Trait Sliders -->
            <div class="card mb-6">
              <h3 class="font-medium text-brand-text flex items-center gap-2 mb-6">
                <i class="bi bi-stars text-pink-400"></i> 六维特质自评
              </h3>
              <div class="space-y-5">
                <div v-for="trait in bipolarTraits" :key="trait.left" class="flex items-center gap-4">
                  <span class="w-16 text-right text-sm text-brand-muted flex-shrink-0">{{ trait.left }}</span>
                  <div class="flex-1 flex gap-1">
                    <button
                      v-for="n in 10" :key="n"
                      @click="setBipolarScore(trait.key, n)"
                      :class="[
                        'flex-1 h-8 rounded transition-all',
                        n <= getBipolarScore(trait.key)
                          ? 'bg-violet-500/60 hover:bg-violet-500/80'
                          : 'bg-brand-surface hover:bg-brand-card'
                      ]"
                    ></button>
                  </div>
                  <span class="w-16 text-sm text-brand-muted flex-shrink-0">{{ trait.right }}</span>
                  <span class="w-6 text-right text-sm font-bold text-violet-400">{{ getBipolarScore(trait.key) }}</span>
                </div>
              </div>
            </div>

            <!-- Work Style Tags -->
            <div class="card mb-6">
              <h3 class="font-medium text-brand-text flex items-center gap-2 mb-4">
                <i class="bi bi-palette text-cyan-400"></i> 工作风格偏好（可多选）
              </h3>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="style in workStyles" :key="style"
                  @click="toggleWorkStyle(style)"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm transition-all',
                    form.workStyle.includes(style)
                      ? 'bg-violet-600 text-white'
                      : 'bg-brand-surface text-brand-muted hover:bg-brand-card border border-brand-border'
                  ]"
                >{{ style }}</button>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="step = 2" class="flex-1 py-3 rounded-xl border border-brand-border text-brand-muted hover:text-brand-text transition-colors">← 上一步</button>
              <button @click="saveProfile" class="flex-1 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 text-white font-medium hover:from-violet-700 hover:to-violet-600 transition-all flex items-center justify-center gap-2">
                <i class="bi bi-check-square"></i> 生成我的画像
              </button>
            </div>
          </div>

        </Transition>
      </template>

      <!-- ════════════════════════════════════════ -->
      <!-- VIEW MODE (Profile View - image 17)      -->
      <!-- ════════════════════════════════════════ -->
      <template v-else>
        <!-- Profile Card -->
        <div class="card mb-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-full bg-violet-600/20 border-2 border-violet-500/30 flex items-center justify-center text-2xl">
                <span v-if="form.name" class="text-violet-400 font-bold">{{ form.name[0] }}</span>
                <i v-else class="bi bi-question-lg text-violet-400"></i>
              </div>
              <div>
                <h2 class="text-xl font-bold text-brand-text">{{ form.name || '未填写姓名' }}</h2>
                <div class="flex items-center gap-2 mt-1">
                  <span v-if="!form.name" class="text-xs px-2 py-0.5 rounded bg-orange-500/15 text-orange-400">未填写</span>
                  <span v-else class="text-sm text-brand-muted">{{ form.education || '' }} · {{ form.major || '' }} · {{ form.school || '' }}</span>
                </div>
              </div>
            </div>
            <!-- Completeness circle -->
            <div class="text-center">
              <div class="w-16 h-16 rounded-full border-4 flex items-center justify-center"
                :class="completeness >= 60 ? 'border-emerald-500' : 'border-brand-border'">
                <span class="text-lg font-bold" :class="completeness >= 60 ? 'text-emerald-400' : 'text-brand-muted'">{{ completeness }}%</span>
              </div>
              <span class="text-xs text-brand-muted mt-1">完整度</span>
            </div>
          </div>
        </div>

        <!-- Skills + Radar Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <!-- Skill Tags -->
          <div class="card">
            <h3 class="font-medium text-brand-text flex items-center gap-2 mb-4">
              <i class="bi bi-tag text-amber-400"></i> 技术技能标签
            </h3>
            <div v-if="form.skills.length === 0" class="text-center py-8 text-brand-muted text-sm">
              暂无技能数据，请填写信息
            </div>
            <div v-else class="flex flex-wrap gap-2">
              <span v-for="skill in form.skills" :key="skill.name" class="badge-cyan text-xs">{{ skill.name }}</span>
            </div>
          </div>

          <!-- Radar Chart -->
          <div class="card">
            <h3 class="font-medium text-brand-text flex items-center gap-2 mb-4">
              <i class="bi bi-hexagon text-violet-400"></i> 六维能力雷达
            </h3>
            <div ref="radarChartRef" class="h-52"></div>
            <div class="grid grid-cols-3 gap-3 mt-3 text-center">
              <div v-for="dim in radarDimensions" :key="dim.label">
                <div class="text-xs text-brand-muted">{{ dim.label }}</div>
                <div class="text-sm font-bold" :class="dim.color">{{ dim.value }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Strengths + Improvements -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div class="card border-l-2 border-l-emerald-500">
            <h3 class="font-medium text-brand-text flex items-center gap-2 mb-3">
              <i class="bi bi-check-square text-emerald-400"></i> 个人优势
            </h3>
            <ul v-if="strengths.length > 0" class="space-y-2">
              <li v-for="s in strengths" :key="s" class="flex items-start gap-2 text-sm text-brand-muted">
                <span class="text-emerald-400 mt-0.5">▸</span> {{ s }}
              </li>
            </ul>
            <p v-else class="text-sm text-brand-muted">请先完善个人信息以获得优势分析</p>
          </div>
          <div class="card border-l-2 border-l-amber-500">
            <h3 class="font-medium text-brand-text flex items-center gap-2 mb-3">
              <i class="bi bi-exclamation-triangle text-amber-400"></i> 待提升项
            </h3>
            <ul class="space-y-2">
              <li v-for="item in improvements" :key="item" class="flex items-start gap-2 text-sm text-brand-muted">
                <span class="text-amber-400 mt-0.5">▸</span> {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Competitiveness -->
        <div class="card mb-6">
          <h3 class="font-medium text-brand-text flex items-center gap-2 mb-5">
            <i class="bi bi-graph-up text-violet-400"></i> 综合竞争力评估
          </h3>
          <div class="space-y-4">
            <div v-for="metric in competitiveness" :key="metric.label">
              <div class="flex items-center justify-between text-sm mb-1">
                <span class="text-brand-muted">{{ metric.label }}</span>
                <span :class="metric.color" class="font-semibold">{{ metric.value }}%</span>
              </div>
              <div class="h-2 bg-brand-surface rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-500" :class="metric.barClass" :style="{ width: metric.value + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <button @click="viewMode = 'edit'" class="py-3 rounded-xl border border-brand-border text-brand-muted hover:text-brand-text transition-colors">
            重新完善画像
          </button>
          <router-link to="/career/explore" class="py-3 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 text-white text-center font-medium flex items-center justify-center gap-2">
            <i class="bi bi-rocket"></i> 开始职业探索
          </router-link>
          <router-link to="/planning" class="py-3 rounded-xl border border-brand-border text-brand-muted hover:text-brand-text text-center flex items-center justify-center gap-2 transition-colors">
            <i class="bi bi-file-earmark-text"></i> 生成报告
          </router-link>
        </div>
      </template>
    </div>

    <!-- ═══ Modals ═══ -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showWorkModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showWorkModal = false">
          <div class="bg-brand-card border border-brand-border rounded-2xl w-full max-w-lg p-6">
            <h3 class="text-lg font-semibold text-brand-text mb-4">添加工作经历</h3>
            <div class="space-y-4">
              <input v-model="workForm.company" class="input-base" placeholder="公司名称">
              <input v-model="workForm.role" class="input-base" placeholder="职位名称">
              <input v-model="workForm.duration" class="input-base" placeholder="在职时间，如：2022.03 - 2024.01">
              <textarea v-model="workForm.desc" class="input-base h-24 resize-none" placeholder="工作内容描述"></textarea>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="showWorkModal = false" class="btn-secondary flex-1">取消</button>
              <button @click="addWork" class="btn-primary flex-1">添加</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showProjectModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showProjectModal = false">
          <div class="bg-brand-card border border-brand-border rounded-2xl w-full max-w-lg p-6">
            <h3 class="text-lg font-semibold text-brand-text mb-4">添加项目经历</h3>
            <div class="space-y-4">
              <input v-model="projectForm.name" class="input-base" placeholder="项目名称">
              <input v-model="projectForm.role" class="input-base" placeholder="担任角色">
              <input v-model="projectForm.techStr" class="input-base" placeholder="技术栈（用逗号分隔）">
              <textarea v-model="projectForm.desc" class="input-base h-24 resize-none" placeholder="项目描述"></textarea>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="showProjectModal = false" class="btn-secondary flex-1">取消</button>
              <button @click="addProject" class="btn-primary flex-1">添加</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showSkillModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showSkillModal = false">
          <div class="bg-brand-card border border-brand-border rounded-2xl w-full max-w-lg p-6">
            <h3 class="text-lg font-semibold text-brand-text mb-4">自定义添加技能</h3>
            <div class="space-y-4">
              <input v-model="skillForm.name" class="input-base" placeholder="技能名称，如：Vue.js">
              <select v-model="skillForm.category" class="input-base">
                <option value="">选择分类</option>
                <option v-for="cat in skillCategories" :key="cat.name" :value="cat.name">{{ cat.name }}</option>
              </select>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="showSkillModal = false" class="btn-secondary flex-1">取消</button>
              <button @click="addSkill" class="btn-primary flex-1">添加</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCareerStore } from '@/stores/careerStore'
import * as echarts from 'echarts'

const router = useRouter()
const careerStore = useCareerStore()

const step = ref(0)
const viewMode = ref<'edit' | 'view'>('edit')
const radarChartRef = ref<HTMLElement | null>(null)
let radarChart: echarts.ECharts | null = null

const steps = [
  { label: '基本信息', icon: 'bi bi-person' },
  { label: '经历', icon: 'bi bi-briefcase' },
  { label: '技能', icon: 'bi bi-lightning' },
  { label: '偏好', icon: 'bi bi-hand-thumbs-up' },
]

const skillCategories = [
  { name: '前端', items: ['HTML/CSS', 'JavaScript', 'TypeScript', 'React', 'Vue', 'Next.js'] },
  { name: '后端', items: ['Node.js', 'Python', 'Java', 'Go', 'Spring Boot', 'FastAPI'] },
  { name: '数据库', items: ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQL'] },
  { name: '工具', items: ['Git', 'Docker', 'Linux', 'Webpack', 'Vite', 'Figma'] },
  { name: 'AI/算法', items: ['机器学习', '深度学习', 'PyTorch', 'TensorFlow', 'AIGC'] },
  { name: '软技能', items: ['项目管理', '用户研究', '需求分析', '数据分析', '商业思维'] },
]

const workStyles = ['远程办公', '弹性工时', '团队协作', '独立工作', '快节奏创业', '稳定大厂', '技术驱动', '业务驱动', '扁平管理', '国际化环境']

const bipolarTraits = [
  { key: 'extraversion', left: '内向', right: '外向' },
  { key: 'innovation', left: '稳健', right: '创新' },
  { key: 'planning', left: '规划型', right: '执行型' },
  { key: 'collaboration', left: '独立', right: '协作' },
  { key: 'risk', left: '稳定', right: '冒险' },
  { key: 'focus', left: '宏观', right: '细致' },
]

const form = reactive({
  name: careerStore.userProfile.name || '',
  age: careerStore.userProfile.age || '',
  education: careerStore.userProfile.education || '',
  major: careerStore.userProfile.major || '',
  school: careerStore.userProfile.school || '',
  experience: careerStore.userProfile.experience || '',
  currentCity: careerStore.userProfile.currentCity || '',
  targetCity: [...(careerStore.userProfile.targetCity || [])],
  workExperiences: [...(careerStore.userProfile.workExperiences || [])],
  projectExperiences: [...(careerStore.userProfile.projectExperiences || [])],
  skills: [...(careerStore.userProfile.skills || [])],
  personality: [...(careerStore.userProfile.personality || [])],
  workStyle: [...(careerStore.userProfile.workStyle || [])],
  bipolarScores: { ...(careerStore.userProfile.bipolarScores || {}) } as Record<string, number>,
})

const targetCityStr = computed({
  get: () => form.targetCity.join(', '),
  set: (val: string) => { form.targetCity = val.split(/[,，]/).map(s => s.trim()).filter(Boolean) }
})

const showWorkModal = ref(false)
const showProjectModal = ref(false)
const showSkillModal = ref(false)

const workForm = reactive({ company: '', role: '', duration: '', desc: '' })
const projectForm = reactive({ name: '', role: '', techStr: '', desc: '' })
const skillForm = reactive({ name: '', category: '', level: 3 })

const completeness = computed(() => {
  let score = 0
  if (form.name) score += 10
  if (form.education) score += 10
  if (form.major) score += 10
  if (form.school) score += 10
  if (form.experience) score += 10
  if (form.currentCity) score += 5
  if (form.workExperiences.length > 0) score += 15
  if (form.projectExperiences.length > 0) score += 10
  if (form.skills.length >= 3) score += 15
  if (form.workStyle.length > 0) score += 5
  return score
})

const hasSkill = (name: string) => form.skills.some(s => s.name === name)

const toggleQuickSkill = (name: string, category: string) => {
  const idx = form.skills.findIndex(s => s.name === name)
  if (idx >= 0) {
    form.skills.splice(idx, 1)
  } else {
    form.skills.push({ name, category, level: 3, yearsUsed: 0 })
  }
}

const toggleWorkStyle = (style: string) => {
  const idx = form.workStyle.indexOf(style)
  if (idx >= 0) form.workStyle.splice(idx, 1)
  else form.workStyle.push(style)
}

const getBipolarScore = (key: string) => form.bipolarScores[key] || 5
const setBipolarScore = (key: string, score: number) => { form.bipolarScores[key] = score }

const addWork = () => {
  if (workForm.company && workForm.role) {
    form.workExperiences.push({ ...workForm })
    Object.assign(workForm, { company: '', role: '', duration: '', desc: '' })
    showWorkModal.value = false
  }
}

const removeWork = (i: number) => form.workExperiences.splice(i, 1)

const addProject = () => {
  if (projectForm.name) {
    form.projectExperiences.push({
      name: projectForm.name,
      role: projectForm.role,
      tech: projectForm.techStr.split(/[,，]/).map(s => s.trim()).filter(Boolean),
      desc: projectForm.desc,
    })
    Object.assign(projectForm, { name: '', role: '', techStr: '', desc: '' })
    showProjectModal.value = false
  }
}

const removeProject = (i: number) => form.projectExperiences.splice(i, 1)

const addSkill = () => {
  if (skillForm.name && skillForm.category) {
    form.skills.push({ name: skillForm.name, category: skillForm.category, level: skillForm.level, yearsUsed: 0 })
    Object.assign(skillForm, { name: '', category: '', level: 3 })
    showSkillModal.value = false
  }
}

const removeSkill = (i: number) => form.skills.splice(i, 1)

// Radar data
const radarDimensions = computed(() => {
  const techScore = Math.min(form.skills.length * 10, 100)
  const projectScore = form.projectExperiences.length * 25
  const softScore = form.skills.filter(s => s.category === '软技能').length * 20
  const learnScore = form.education ? (form.education === '硕士' ? 60 : form.education === '博士' ? 80 : 40) : 0
  const collab = (form.bipolarScores['collaboration'] || 5) * 10
  const innovate = (form.bipolarScores['innovation'] || 5) * 10
  return [
    { label: '技术', value: Math.min(techScore, 100), color: 'text-violet-400' },
    { label: '项目经验', value: Math.min(projectScore, 100), color: 'text-cyan-400' },
    { label: '软技能', value: Math.min(softScore, 100), color: 'text-emerald-400' },
    { label: '学习能力', value: Math.min(learnScore, 100), color: 'text-amber-400' },
    { label: '协作能力', value: Math.min(collab, 100), color: 'text-pink-400' },
    { label: '创新能力', value: Math.min(innovate, 100), color: 'text-blue-400' },
  ]
})

const strengths = computed(() => {
  const list: string[] = []
  if (form.skills.length >= 5) list.push('技能储备丰富，覆盖面广')
  if (form.workExperiences.length >= 2) list.push('有丰富的工作经验积累')
  if (form.projectExperiences.length >= 2) list.push('项目经验扎实，实战能力强')
  if (form.education === '硕士' || form.education === '博士') list.push('学历优势明显')
  return list
})

const improvements = computed(() => {
  const list: string[] = []
  if (form.skills.length < 3) list.push('技能广度不足，建议拓展更多技术栈')
  if (form.workExperiences.length === 0) list.push('工作经验尚浅，建议多参与实习或项目')
  if (form.projectExperiences.length === 0) list.push('缺少项目经历，建议积累实战项目')
  if (!form.education) list.push('请补充学历信息以获得更准确的分析')
  if (list.length === 0) list.push('继续保持，可以尝试挑战更高级的目标')
  return list
})

const competitiveness = computed(() => {
  const techDepth = Math.min(form.skills.filter(s => s.category !== '软技能').length * 8, 100)
  const expRich = Math.min(form.workExperiences.length * 20, 100)
  const projectReal = Math.min(form.projectExperiences.length * 15, 100)
  const skillBreadth = Math.min(new Set(form.skills.map(s => s.category)).size * 15, 100)
  const overall = Math.round((techDepth + expRich + projectReal + skillBreadth) / 4)
  return [
    { label: '技术深度', value: techDepth, color: 'text-violet-400', barClass: 'bg-violet-500' },
    { label: '经验丰富度', value: expRich, color: 'text-blue-400', barClass: 'bg-blue-500' },
    { label: '项目实战', value: projectReal, color: 'text-emerald-400', barClass: 'bg-emerald-500' },
    { label: '技能广度', value: skillBreadth, color: 'text-amber-400', barClass: 'bg-amber-500' },
    { label: '综合竞争力', value: overall, color: 'text-brand-text', barClass: 'bg-gradient-to-r from-violet-500 to-cyan-500' },
  ]
})

function renderRadar() {
  if (!radarChartRef.value) return
  if (!radarChart) radarChart = echarts.init(radarChartRef.value)
  const dims = radarDimensions.value
  radarChart.setOption({
    radar: {
      indicator: dims.map(d => ({ name: d.label, max: 100 })),
      shape: 'polygon',
      splitNumber: 4,
      axisName: { color: '#9ca3af', fontSize: 11 },
      splitLine: { lineStyle: { color: '#1e1e2e' } },
      splitArea: { areaStyle: { color: ['transparent'] } },
      axisLine: { lineStyle: { color: '#1e1e2e' } },
    },
    series: [{
      type: 'radar',
      data: [{ value: dims.map(d => d.value), areaStyle: { color: 'rgba(124,58,237,0.2)' } }],
      lineStyle: { color: '#7c3aed', width: 2 },
      itemStyle: { color: '#7c3aed' },
      symbol: 'circle',
      symbolSize: 6,
    }],
  })
}

watch(viewMode, async (mode) => {
  if (mode === 'view') {
    await nextTick()
    renderRadar()
  }
})

const saveProfile = () => {
  careerStore.updateProfile({
    name: form.name,
    age: form.age,
    education: form.education,
    major: form.major,
    school: form.school,
    experience: form.experience,
    currentCity: form.currentCity,
    targetCity: form.targetCity,
    workExperiences: form.workExperiences,
    projectExperiences: form.projectExperiences,
    skills: form.skills,
    personality: form.personality,
    workStyle: form.workStyle,
    bipolarScores: form.bipolarScores,
    completeness: completeness.value,
  })
  viewMode.value = 'view'
}

onMounted(() => {
  if (completeness.value > 0 && careerStore.userProfile.name) {
    viewMode.value = 'view'
    nextTick(() => renderRadar())
  }
})
</script>
