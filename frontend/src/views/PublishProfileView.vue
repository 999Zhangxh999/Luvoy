<template>
  <div class="publish-profile">
    <!-- 背景 -->
    <div class="profile-bg">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-grid"></div>
    </div>

    <div class="profile-container">
      <!-- 头部 -->
      <header class="profile-header">
        <router-link to="/job-hub" class="back-btn">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="header-info">
          <h1><i class="bi bi-person-badge-fill"></i> 我的画像</h1>
          <p>打造专属职业名片，展示核心竞争力</p>
        </div>
        <div class="header-actions">
          <button class="btn-preview" @click="showPreview = true">
            <i class="bi bi-eye"></i> 预览
          </button>
        </div>
      </header>

      <!-- 画像完成度 -->
      <div class="completion-card">
        <div class="completion-ring">
          <svg viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="42" class="ring-bg" />
            <circle cx="50" cy="50" r="42" class="ring-fill" 
              :stroke-dasharray="`${completionPercent * 2.64} 264`" />
          </svg>
          <div class="ring-inner">
            <span class="percent">{{ completionPercent }}%</span>
            <span class="label">完成度</span>
          </div>
        </div>
        <div class="completion-info">
          <h3>让HR更快找到你</h3>
          <p>完善画像信息可提升 <strong>3倍</strong> 曝光率</p>
          <div class="completion-tips">
            <span v-for="tip in incompleteTips" :key="tip" class="tip-tag">
              <i class="bi bi-plus-circle"></i> {{ tip }}
            </span>
          </div>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="profile-main">
        <!-- 左侧表单 -->
        <div class="form-area">
          <!-- 基本信息 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-person"></i> 基本信息</h2>
              <span v-if="sections.basic.complete" class="complete-badge">
                <i class="bi bi-check-circle-fill"></i>
              </span>
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label>姓名 <span class="req">*</span></label>
                <input v-model="form.name" placeholder="您的姓名" />
              </div>
              <div class="form-group">
                <label>手机号 <span class="req">*</span></label>
                <input v-model="form.phone" placeholder="联系电话" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input v-model="form.email" placeholder="电子邮箱" />
              </div>
              <div class="form-group">
                <label>所在城市</label>
                <select v-model="form.city">
                  <option value="">请选择</option>
                  <option value="北京">北京</option>
                  <option value="上海">上海</option>
                  <option value="深圳">深圳</option>
                  <option value="杭州">杭州</option>
                  <option value="广州">广州</option>
                </select>
              </div>
            </div>
          </section>

          <!-- 教育背景 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-mortarboard"></i> 教育背景</h2>
              <span v-if="sections.education.complete" class="complete-badge">
                <i class="bi bi-check-circle-fill"></i>
              </span>
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label>最高学历 <span class="req">*</span></label>
                <select v-model="form.education">
                  <option value="">请选择</option>
                  <option value="大专">大专</option>
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                  <option value="博士">博士</option>
                </select>
              </div>
              <div class="form-group">
                <label>学校名称</label>
                <input v-model="form.school" placeholder="毕业院校" />
              </div>
              <div class="form-group">
                <label>专业</label>
                <input v-model="form.major" placeholder="所学专业" />
              </div>
              <div class="form-group">
                <label>毕业年份</label>
                <select v-model="form.graduationYear">
                  <option value="">请选择</option>
                  <option v-for="y in graduationYears" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
            </div>
          </section>

          <!-- 求职意向 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-briefcase"></i> 求职意向</h2>
              <span v-if="sections.intention.complete" class="complete-badge">
                <i class="bi bi-check-circle-fill"></i>
              </span>
            </div>

            <div class="form-grid">
              <div class="form-group full">
                <label>期望岗位 <span class="req">*</span></label>
                <input v-model="form.expectedJob" placeholder="如：前端开发工程师" />
              </div>
              <div class="form-group">
                <label>期望薪资</label>
                <div class="salary-range">
                  <input v-model="form.salaryMin" type="number" placeholder="最低" />
                  <span>-</span>
                  <input v-model="form.salaryMax" type="number" placeholder="最高" />
                  <span>K</span>
                </div>
              </div>
              <div class="form-group">
                <label>工作年限</label>
                <select v-model="form.workYears">
                  <option value="">请选择</option>
                  <option value="应届生">应届生</option>
                  <option value="1-3年">1-3年</option>
                  <option value="3-5年">3-5年</option>
                  <option value="5-10年">5-10年</option>
                  <option value="10年以上">10年以上</option>
                </select>
              </div>
              <div class="form-group">
                <label>期望城市</label>
                <select v-model="form.expectedCity" multiple class="multi-select">
                  <option value="北京">北京</option>
                  <option value="上海">上海</option>
                  <option value="深圳">深圳</option>
                  <option value="杭州">杭州</option>
                  <option value="广州">广州</option>
                  <option value="成都">成都</option>
                </select>
              </div>
            </div>
          </section>

          <!-- 技能标签 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-lightning"></i> 技能标签</h2>
              <span v-if="sections.skills.complete" class="complete-badge">
                <i class="bi bi-check-circle-fill"></i>
              </span>
            </div>

            <div class="form-group">
              <label>核心技能 <span class="req">*</span></label>
              <div class="skill-input">
                <input v-model="skillInput" placeholder="输入技能，按回车添加" @keyup.enter="addSkill" />
                <button @click="addSkill"><i class="bi bi-plus"></i></button>
              </div>
              <div class="skill-tags">
                <span v-for="(skill, i) in form.skills" :key="skill" class="skill-tag">
                  {{ skill }}
                  <i class="bi bi-x" @click="removeSkill(i)"></i>
                </span>
              </div>
              <p class="form-hint">推荐添加 5-10 个技能标签</p>
            </div>

            <div class="recommended-skills">
              <span class="rec-label">热门技能推荐：</span>
              <button 
                v-for="skill in recommendedSkills" 
                :key="skill"
                class="rec-skill"
                @click="addRecommendedSkill(skill)"
                :disabled="form.skills.includes(skill)"
              >
                {{ skill }}
              </button>
            </div>
          </section>

          <!-- 能力画像 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-hexagon"></i> 能力画像</h2>
            </div>

            <p class="form-hint">根据自我评估调整各项能力分值（1-10分）</p>

            <div class="ability-grid">
              <div v-for="ability in abilities" :key="ability.key" class="ability-card">
                <div class="ability-info">
                  <span class="ability-icon">{{ ability.icon }}</span>
                  <span class="ability-name">{{ ability.name }}</span>
                </div>
                <div class="ability-slider">
                  <input 
                    type="range" 
                    min="1" 
                    max="10" 
                    v-model="form.abilities[ability.key]"
                  />
                  <span class="ability-value">{{ form.abilities[ability.key] }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- 自我介绍 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-chat-quote"></i> 自我介绍</h2>
            </div>

            <div class="form-group">
              <label>一句话介绍</label>
              <input v-model="form.tagline" placeholder="用一句话精炼概括您的优势" maxlength="50" />
              <span class="char-count">{{ form.tagline.length }}/50</span>
            </div>

            <div class="form-group">
              <label>详细介绍</label>
              <textarea v-model="form.introduction" rows="5" placeholder="介绍您的工作经历、技能特长、项目成就等..."></textarea>
            </div>
          </section>

          <!-- 项目经历 -->
          <section class="form-section">
            <div class="section-header">
              <h2><i class="bi bi-folder"></i> 项目经历</h2>
              <button class="btn-add-project" @click="addProject">
                <i class="bi bi-plus"></i> 添加项目
              </button>
            </div>

            <div v-if="form.projects.length === 0" class="empty-projects">
              <i class="bi bi-folder-plus"></i>
              <p>添加项目经历展示您的实战能力</p>
              <button @click="addProject">添加第一个项目</button>
            </div>

            <div v-for="(project, i) in form.projects" :key="i" class="project-card">
              <div class="project-header">
                <span class="project-num">项目 {{ i + 1 }}</span>
                <button class="btn-remove" @click="removeProject(i)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
              <div class="project-form">
                <div class="form-group">
                  <label>项目名称</label>
                  <input v-model="project.name" placeholder="项目名称" />
                </div>
                <div class="form-group">
                  <label>担任角色</label>
                  <input v-model="project.role" placeholder="如：核心开发" />
                </div>
                <div class="form-group full">
                  <label>项目描述</label>
                  <textarea v-model="project.description" rows="3" placeholder="项目简介及您的贡献..."></textarea>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 右侧实时预览 -->
        <aside class="preview-sidebar">
          <div class="preview-card">
            <div class="card-header">
              <span class="preview-tag">实时预览</span>
            </div>
            
            <div class="card-avatar">
              <div class="avatar-circle">
                {{ form.name ? form.name.charAt(0) : '?' }}
              </div>
              <div class="avatar-info">
                <h3>{{ form.name || '未填写姓名' }}</h3>
                <p>{{ form.expectedJob || '期望岗位' }}</p>
              </div>
            </div>

            <div v-if="form.tagline" class="card-tagline">
              "{{ form.tagline }}"
            </div>

            <div class="card-meta">
              <span v-if="form.education"><i class="bi bi-mortarboard"></i> {{ form.education }}</span>
              <span v-if="form.workYears"><i class="bi bi-calendar3"></i> {{ form.workYears }}</span>
              <span v-if="form.city"><i class="bi bi-geo-alt"></i> {{ form.city }}</span>
            </div>

            <div v-if="form.skills.length" class="card-skills">
              <span v-for="skill in form.skills.slice(0, 6)" :key="skill" class="skill-chip">
                {{ skill }}
              </span>
              <span v-if="form.skills.length > 6" class="skill-more">+{{ form.skills.length - 6 }}</span>
            </div>

            <div class="card-radar">
              <RadarChart :series="previewRadar" :indicators="radarIndicators" height="180px" />
            </div>

            <div v-if="form.salaryMin && form.salaryMax" class="card-salary">
              期望薪资：{{ form.salaryMin }}-{{ form.salaryMax }}K
            </div>
          </div>

          <button class="btn-publish" @click="publishProfile">
            <i class="bi bi-rocket-takeoff"></i> 发布画像
          </button>
        </aside>
      </div>
    </div>

    <!-- 发布成功弹窗 -->
    <transition name="modal-fade">
      <div v-if="showSuccess" class="success-modal" @click.self="showSuccess = false">
        <div class="success-content">
          <div class="success-icon">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <h2>画像发布成功！</h2>
          <p>您的画像已上线，正在为您匹配合适的职位</p>
          <div class="success-stats">
            <div class="stat">
              <span class="num">128</span>
              <span class="label">潜在匹配</span>
            </div>
            <div class="stat">
              <span class="num">{{ completionPercent }}%</span>
              <span class="label">画像完整度</span>
            </div>
          </div>
          <div class="success-actions">
            <router-link to="/job-market" class="btn-primary">
              <i class="bi bi-building"></i> 浏览职位
            </router-link>
            <router-link to="/job-hub" class="btn-secondary">返回首页</router-link>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import RadarChart from '@/components/RadarChart.vue'

const toast = inject('toast', null)

// 表单数据
const form = ref({
  name: '',
  phone: '',
  email: '',
  city: '',
  education: '',
  school: '',
  major: '',
  graduationYear: '',
  expectedJob: '',
  salaryMin: '',
  salaryMax: '',
  workYears: '',
  expectedCity: [],
  skills: [],
  abilities: {
    technical: 7,
    communication: 6,
    learning: 8,
    innovation: 6,
    teamwork: 7,
    execution: 7
  },
  tagline: '',
  introduction: '',
  projects: []
})

// 技能输入
const skillInput = ref('')

// 能力维度
const abilities = [
  { key: 'technical', name: '技术能力', icon: '💻' },
  { key: 'communication', name: '沟通能力', icon: '💬' },
  { key: 'learning', name: '学习能力', icon: '📚' },
  { key: 'innovation', name: '创新能力', icon: '💡' },
  { key: 'teamwork', name: '团队协作', icon: '🤝' },
  { key: 'execution', name: '执行能力', icon: '⚡' },
]

// 推荐技能
const recommendedSkills = ['Vue.js', 'React', 'Python', 'Java', 'SQL', 'TypeScript', '数据分析', '机器学习']

// 毕业年份
const graduationYears = Array.from({ length: 15 }, (_, i) => 2024 - i)

// 雷达图
const radarIndicators = [
  { name: '技术', max: 10 },
  { name: '沟通', max: 10 },
  { name: '学习', max: 10 },
  { name: '创新', max: 10 },
  { name: '协作', max: 10 },
  { name: '执行', max: 10 },
]

const previewRadar = computed(() => [{
  name: '能力画像',
  value: [
    form.value.abilities.technical,
    form.value.abilities.communication,
    form.value.abilities.learning,
    form.value.abilities.innovation,
    form.value.abilities.teamwork,
    form.value.abilities.execution
  ],
  areaStyle: { color: 'rgba(139, 92, 246, 0.3)' },
  lineStyle: { color: '#8b5cf6' }
}])

// 完成度计算
const sections = computed(() => ({
  basic: { complete: !!form.value.name && !!form.value.phone },
  education: { complete: !!form.value.education },
  intention: { complete: !!form.value.expectedJob },
  skills: { complete: form.value.skills.length >= 3 }
}))

const completionPercent = computed(() => {
  let score = 0
  if (form.value.name) score += 10
  if (form.value.phone) score += 10
  if (form.value.education) score += 10
  if (form.value.school) score += 5
  if (form.value.expectedJob) score += 15
  if (form.value.workYears) score += 10
  if (form.value.skills.length >= 3) score += 15
  if (form.value.tagline) score += 10
  if (form.value.introduction) score += 10
  if (form.value.projects.length > 0) score += 5
  return Math.min(score, 100)
})

const incompleteTips = computed(() => {
  const tips = []
  if (!form.value.name) tips.push('完善姓名')
  if (!form.value.expectedJob) tips.push('填写期望岗位')
  if (form.value.skills.length < 3) tips.push('添加更多技能')
  if (!form.value.introduction) tips.push('完善自我介绍')
  return tips.slice(0, 3)
})

// 添加技能
function addSkill() {
  if (skillInput.value.trim() && !form.value.skills.includes(skillInput.value.trim())) {
    form.value.skills.push(skillInput.value.trim())
    skillInput.value = ''
  }
}

function addRecommendedSkill(skill) {
  if (!form.value.skills.includes(skill)) {
    form.value.skills.push(skill)
  }
}

function removeSkill(index) {
  form.value.skills.splice(index, 1)
}

// 项目
function addProject() {
  form.value.projects.push({ name: '', role: '', description: '' })
}

function removeProject(index) {
  form.value.projects.splice(index, 1)
}

// 发布
const showSuccess = ref(false)
const showPreview = ref(false)

function publishProfile() {
  if (!form.value.name || !form.value.phone || !form.value.expectedJob) {
    toast?.('请填写必要信息（姓名、电话、期望岗位）', 'error')
    return
  }
  showSuccess.value = true
}
</script>

<style scoped>
.publish-profile {
  min-height: 100vh;
  padding: 24px;
  position: relative;
}

/* 背景 */
.profile-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: #8b5cf6;
  left: -150px;
  top: 5%;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: #06b6d4;
  right: -100px;
  bottom: 10%;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 头部 */
.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  text-decoration: none;
}

.header-info {
  flex: 1;
}

.header-info h1 {
  font-size: 26px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-info h1 i { color: #8b5cf6; }

.header-info p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

.btn-preview {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  color: #a78bfa;
  font-size: 14px;
  cursor: pointer;
}

/* 完成度卡片 */
.completion-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.05));
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 18px;
  margin-bottom: 24px;
}

.completion-ring {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.completion-ring svg {
  transform: rotate(-90deg);
}

.ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.15);
  stroke-width: 6;
}

.ring-fill {
  fill: none;
  stroke: #8b5cf6;
  stroke-width: 6;
  stroke-linecap: round;
  transition: stroke-dasharray 0.5s ease;
}

.ring-inner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.ring-inner .percent {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
}

.ring-inner .label {
  font-size: 10px;
  color: var(--color-brand-muted, #64748b);
}

.completion-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 4px;
}

.completion-info p {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 10px;
}

.completion-info strong { color: #f59e0b; }

.completion-tips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tip-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 20px;
  font-size: 12px;
  color: #f59e0b;
}

/* 主内容布局 */
.profile-main {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
}

@media (max-width: 1024px) {
  .profile-main {
    grid-template-columns: 1fr;
  }
  .preview-sidebar { display: none; }
}

/* 表单区 */
.form-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 18px;
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.section-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h2 i { color: #8b5cf6; }

.complete-badge {
  color: #10b981;
  font-size: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.full { grid-column: 1 / -1; }

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
}

.req { color: #ef4444; }

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 14px;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  outline: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #8b5cf6;
}

.salary-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.salary-range input { flex: 1; }

.multi-select {
  height: 80px;
}

/* 技能输入 */
.skill-input {
  display: flex;
  gap: 10px;
}

.skill-input input { flex: 1; }

.skill-input button {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  color: white;
  cursor: pointer;
  font-size: 18px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.skill-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(139, 92, 246, 0.15);
  border-radius: 8px;
  font-size: 13px;
  color: #a78bfa;
}

.skill-tag i {
  cursor: pointer;
  opacity: 0.7;
}

.skill-tag i:hover { opacity: 1; }

.form-hint {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-top: 8px;
}

.recommended-skills {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(139, 92, 246, 0.1);
}

.rec-label {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.rec-skill {
  padding: 4px 10px;
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
  border-radius: 16px;
  font-size: 12px;
  color: #22d3ee;
  cursor: pointer;
}

.rec-skill:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 能力画像 */
.ability-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.ability-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.ability-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 90px;
}

.ability-icon { font-size: 18px; }

.ability-name {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

.ability-slider {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ability-slider input[type="range"] {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: rgba(139, 92, 246, 0.2);
  appearance: none;
  cursor: pointer;
}

.ability-slider input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  cursor: pointer;
}

.ability-value {
  min-width: 24px;
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  color: #a78bfa;
}

/* 自我介绍 */
.char-count {
  align-self: flex-end;
  font-size: 11px;
  color: var(--color-brand-muted, #64748b);
}

/* 项目 */
.btn-add-project {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 8px;
  font-size: 13px;
  color: #a78bfa;
  cursor: pointer;
}

.empty-projects {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-brand-muted, #64748b);
}

.empty-projects i {
  font-size: 40px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-projects button {
  margin-top: 12px;
  padding: 10px 20px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px dashed rgba(139, 92, 246, 0.3);
  border-radius: 10px;
  color: #a78bfa;
  cursor: pointer;
}

.project-card {
  padding: 16px;
  background: rgba(139, 92, 246, 0.03);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 14px;
  margin-top: 14px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.project-num {
  font-size: 13px;
  font-weight: 600;
  color: #a78bfa;
}

.btn-remove {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #f87171;
  cursor: pointer;
}

.project-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

/* 预览侧边栏 */
.preview-sidebar {
  position: sticky;
  top: 24px;
  height: fit-content;
}

.preview-card {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.preview-tag {
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.15);
  border-radius: 20px;
  font-size: 11px;
  color: #a78bfa;
}

.card-avatar {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.avatar-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: white;
}

.avatar-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
}

.avatar-info p {
  font-size: 13px;
  color: #a78bfa;
}

.card-tagline {
  font-size: 13px;
  font-style: italic;
  color: var(--color-brand-muted, #64748b);
  padding: 10px 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 10px;
  margin-bottom: 16px;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.card-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
}

.card-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.skill-chip {
  padding: 4px 10px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 6px;
  font-size: 11px;
  color: #a78bfa;
}

.skill-more {
  padding: 4px 8px;
  background: rgba(100, 116, 139, 0.1);
  border-radius: 6px;
  font-size: 11px;
  color: #64748b;
}

.card-radar {
  min-height: 180px;
  margin-bottom: 16px;
}

.card-salary {
  text-align: center;
  padding: 10px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #34d399;
}

.btn-publish {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-publish:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
}

/* 成功弹窗 */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.3s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.success-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.success-content {
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px;
  padding: 48px;
  text-align: center;
  max-width: 400px;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: #34d399;
  animation: pop 0.5s ease;
}

@keyframes pop {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.success-content h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  margin-bottom: 8px;
}

.success-content > p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 24px;
}

.success-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 32px;
}

.success-stats .stat { display: flex; flex-direction: column; }
.success-stats .num { font-size: 28px; font-weight: 700; color: #8b5cf6; }
.success-stats .label { font-size: 13px; color: var(--color-brand-muted, #64748b); }

.success-actions { display: flex; flex-direction: column; gap: 12px; }

.success-actions .btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  text-decoration: none;
}

.success-actions .btn-secondary {
  padding: 12px;
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  text-decoration: none;
}

@media (max-width: 640px) {
  .form-grid, .ability-grid, .project-form {
    grid-template-columns: 1fr;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .publish-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .publish-header h1 {
  color: #0c4a6e;
}

:global(html.light) .publish-header p {
  color: #64748b;
}

:global(html.light) .step-indicator {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .step-item.active .step-num {
  background: #0891b2;
}

:global(html.light) .step-item.completed .step-num {
  background: #059669;
}

:global(html.light) .step-label {
  color: #64748b;
}

:global(html.light) .step-item.active .step-label {
  color: #0891b2;
}

:global(html.light) .form-section {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .section-title {
  color: #0c4a6e;
}

:global(html.light) .form-group label {
  color: #0c4a6e;
}

:global(html.light) .form-group input,
:global(html.light) .form-group select,
:global(html.light) .form-group textarea {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .form-group input:focus,
:global(html.light) .form-group select:focus,
:global(html.light) .form-group textarea:focus {
  border-color: rgba(8, 145, 178, 0.4);
}

:global(html.light) .skill-tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .ability-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .ability-name {
  color: #0c4a6e;
}

:global(html.light) .progress-track {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .project-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .project-title {
  color: #0c4a6e;
}

:global(html.light) .project-desc {
  color: #64748b;
}

:global(html.light) .btn-next {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-prev {
  background: rgba(8, 145, 178, 0.08);
  color: #64748b;
}

:global(html.light) .btn-prev:hover {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .success-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .success-icon {
  background: rgba(16, 185, 129, 0.1);
}

:global(html.light) .success-title {
  color: #0c4a6e;
}

:global(html.light) .success-desc {
  color: #64748b;
}

:global(html.light) .success-stats .num {
  color: #0891b2;
}

:global(html.light) .success-actions .btn-primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .success-actions .btn-secondary {
  border-color: rgba(8, 145, 178, 0.2);
  color: #64748b;
}

:global(html.light) .success-actions .btn-secondary:hover {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}
</style>
