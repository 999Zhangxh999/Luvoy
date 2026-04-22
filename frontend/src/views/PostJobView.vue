<template>
  <div class="post-job">
    <!-- 背景 -->
    <div class="post-bg">
      <div class="bg-glow glow-1"></div>
      <div class="bg-glow glow-2"></div>
    </div>

    <div class="post-container">
      <!-- 头部 -->
      <header class="post-header">
        <router-link to="/job-hub" class="back-btn">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="header-info">
          <h1><i class="bi bi-plus-circle-fill"></i> 发布职位</h1>
          <p>创建职位画像，精准吸引人才</p>
        </div>
      </header>

      <!-- 发布流程 -->
      <div class="step-indicator">
        <div v-for="(step, i) in steps" :key="i" :class="['step', { active: currentStep === i, done: currentStep > i }]">
          <div class="step-dot">
            <i v-if="currentStep > i" class="bi bi-check"></i>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span class="step-label">{{ step }}</span>
        </div>
      </div>

      <!-- 表单内容 -->
      <div class="form-container">
        <!-- Step 1: 基本信息 -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="currentStep === 0" key="step1" class="form-section">
            <h2><i class="bi bi-info-circle"></i> 基本信息</h2>
            
            <div class="form-grid">
              <div class="form-group full">
                <label>职位名称 <span class="required">*</span></label>
                <input v-model="form.title" placeholder="如：高级前端开发工程师" />
              </div>

              <div class="form-group">
                <label>所属部门</label>
                <input v-model="form.department" placeholder="如：技术部" />
              </div>

              <div class="form-group">
                <label>工作城市 <span class="required">*</span></label>
                <select v-model="form.city">
                  <option value="">请选择</option>
                  <option value="北京">北京</option>
                  <option value="上海">上海</option>
                  <option value="深圳">深圳</option>
                  <option value="杭州">杭州</option>
                  <option value="广州">广州</option>
                  <option value="成都">成都</option>
                </select>
              </div>

              <div class="form-group">
                <label>工作经验 <span class="required">*</span></label>
                <select v-model="form.experience">
                  <option value="">请选择</option>
                  <option value="不限">不限</option>
                  <option value="应届生">应届生</option>
                  <option value="1-3年">1-3年</option>
                  <option value="3-5年">3-5年</option>
                  <option value="5-10年">5-10年</option>
                  <option value="10年以上">10年以上</option>
                </select>
              </div>

              <div class="form-group">
                <label>学历要求</label>
                <select v-model="form.education">
                  <option value="">不限</option>
                  <option value="大专">大专</option>
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                  <option value="博士">博士</option>
                </select>
              </div>

              <div class="form-group">
                <label>薪资范围 <span class="required">*</span></label>
                <div class="salary-inputs">
                  <input v-model="form.salaryMin" type="number" placeholder="最低" />
                  <span>-</span>
                  <input v-model="form.salaryMax" type="number" placeholder="最高" />
                  <span>K</span>
                </div>
              </div>

              <div class="form-group">
                <label>招聘人数</label>
                <input v-model="form.headcount" type="number" placeholder="如：3" />
              </div>

              <div class="form-group">
                <label>工作类型</label>
                <select v-model="form.jobType">
                  <option value="全职">全职</option>
                  <option value="兼职">兼职</option>
                  <option value="实习">实习</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Step 2: 职位描述 -->
          <div v-else-if="currentStep === 1" key="step2" class="form-section">
            <h2><i class="bi bi-file-text"></i> 职位描述</h2>

            <div class="form-group">
              <label>职位描述 <span class="required">*</span></label>
              <textarea v-model="form.description" rows="5" placeholder="描述工作内容、职责范围等..."></textarea>
            </div>

            <div class="form-group">
              <label>任职要求 <span class="required">*</span></label>
              <div class="requirement-list">
                <div v-for="(req, i) in form.requirements" :key="i" class="req-item">
                  <input v-model="form.requirements[i]" placeholder="输入一条要求..." />
                  <button class="btn-remove" @click="removeRequirement(i)" v-if="form.requirements.length > 1">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
                <button class="btn-add" @click="addRequirement">
                  <i class="bi bi-plus"></i> 添加要求
                </button>
              </div>
            </div>

            <div class="form-group">
              <label>职位亮点</label>
              <div class="highlights-grid">
                <label v-for="hl in highlightOptions" :key="hl" class="highlight-check">
                  <input type="checkbox" :value="hl" v-model="form.highlights" />
                  <span>{{ hl }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Step 3: 技能画像 -->
          <div v-else-if="currentStep === 2" key="step3" class="form-section">
            <h2><i class="bi bi-lightning"></i> 技能画像</h2>

            <div class="form-group">
              <label>必备技能 <span class="required">*</span></label>
              <div class="skill-input">
                <input v-model="skillInput" placeholder="输入技能名称，按回车添加" @keyup.enter="addSkill('required')" />
                <button @click="addSkill('required')"><i class="bi bi-plus"></i></button>
              </div>
              <div class="skill-tags">
                <span v-for="(skill, i) in form.requiredSkills" :key="skill" class="skill-tag required">
                  {{ skill }}
                  <i class="bi bi-x" @click="removeSkill('required', i)"></i>
                </span>
              </div>
            </div>

            <div class="form-group">
              <label>加分技能</label>
              <div class="skill-input">
                <input v-model="bonusSkillInput" placeholder="输入加分技能" @keyup.enter="addSkill('bonus')" />
                <button @click="addSkill('bonus')"><i class="bi bi-plus"></i></button>
              </div>
              <div class="skill-tags">
                <span v-for="(skill, i) in form.bonusSkills" :key="skill" class="skill-tag bonus">
                  {{ skill }}
                  <i class="bi bi-x" @click="removeSkill('bonus', i)"></i>
                </span>
              </div>
            </div>

            <div class="form-group">
              <label>能力模型配置</label>
              <p class="form-hint">拖动滑块设置各维度权重（总和建议为100）</p>
              <div class="ability-sliders">
                <div v-for="ability in abilities" :key="ability.key" class="ability-slider">
                  <div class="ability-header">
                    <span class="ability-name">{{ ability.name }}</span>
                    <span class="ability-value">{{ form.abilityWeights[ability.key] }}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" 
                    max="100" 
                    v-model="form.abilityWeights[ability.key]"
                  />
                </div>
              </div>
            </div>

            <!-- 画像预览 -->
            <div class="profile-preview">
              <h4><i class="bi bi-hexagon"></i> 岗位画像预览</h4>
              <div class="preview-radar">
                <RadarChart :series="previewRadar" :indicators="radarIndicators" height="200px" />
              </div>
            </div>
          </div>

          <!-- Step 4: 公司信息 -->
          <div v-else-if="currentStep === 3" key="step4" class="form-section">
            <h2><i class="bi bi-building"></i> 公司信息</h2>

            <div class="form-grid">
              <div class="form-group full">
                <label>公司名称 <span class="required">*</span></label>
                <input v-model="form.companyName" placeholder="公司全称" />
              </div>

              <div class="form-group">
                <label>公司规模</label>
                <select v-model="form.companyScale">
                  <option value="">请选择</option>
                  <option value="50人以下">50人以下</option>
                  <option value="50-150人">50-150人</option>
                  <option value="150-500人">150-500人</option>
                  <option value="500-1000人">500-1000人</option>
                  <option value="1000-5000人">1000-5000人</option>
                  <option value="5000人以上">5000人以上</option>
                </select>
              </div>

              <div class="form-group">
                <label>行业领域</label>
                <select v-model="form.industry">
                  <option value="">请选择</option>
                  <option value="互联网">互联网</option>
                  <option value="金融">金融</option>
                  <option value="教育">教育</option>
                  <option value="医疗">医疗</option>
                  <option value="电商">电商</option>
                  <option value="游戏">游戏</option>
                </select>
              </div>

              <div class="form-group">
                <label>融资阶段</label>
                <select v-model="form.funding">
                  <option value="">请选择</option>
                  <option value="未融资">未融资</option>
                  <option value="天使轮">天使轮</option>
                  <option value="A轮">A轮</option>
                  <option value="B轮">B轮</option>
                  <option value="C轮及以上">C轮及以上</option>
                  <option value="已上市">已上市</option>
                </select>
              </div>

              <div class="form-group full">
                <label>公司介绍</label>
                <textarea v-model="form.companyIntro" rows="3" placeholder="简要介绍公司..."></textarea>
              </div>

              <div class="form-group full">
                <label>工作地址</label>
                <input v-model="form.address" placeholder="详细办公地址" />
              </div>
            </div>

            <div class="form-group">
              <label>福利待遇</label>
              <div class="benefits-grid">
                <label v-for="bf in benefitOptions" :key="bf" class="benefit-check">
                  <input type="checkbox" :value="bf" v-model="form.benefits" />
                  <span>{{ bf }}</span>
                </label>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <!-- 底部操作 -->
      <div class="form-actions">
        <button v-if="currentStep > 0" class="btn-prev" @click="prevStep">
          <i class="bi bi-arrow-left"></i> 上一步
        </button>
        <div class="spacer"></div>
        <button v-if="currentStep < steps.length - 1" class="btn-next" @click="nextStep">
          下一步 <i class="bi bi-arrow-right"></i>
        </button>
        <button v-else class="btn-submit" @click="submitJob">
          <i class="bi bi-check-lg"></i> 发布职位
        </button>
      </div>
    </div>

    <!-- 发布成功弹窗 -->
    <transition name="modal-fade">
      <div v-if="showSuccess" class="success-modal" @click.self="closeSuccess">
        <div class="success-content">
          <div class="success-icon">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <h2>发布成功！</h2>
          <p>职位已发布，系统正在为您匹配人才</p>
          <div class="success-stats">
            <div class="stat">
              <span class="num">256</span>
              <span class="label">潜在匹配</span>
            </div>
            <div class="stat">
              <span class="num">85%</span>
              <span class="label">画像完整度</span>
            </div>
          </div>
          <div class="success-actions">
            <router-link to="/talent-market" class="btn-primary">
              <i class="bi bi-people"></i> 浏览人才
            </router-link>
            <router-link to="/job-hub" class="btn-secondary">
              返回首页
            </router-link>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import RadarChart from '@/components/RadarChart.vue'

const router = useRouter()
const toast = inject('toast', null)

// 步骤
const steps = ['基本信息', '职位描述', '技能画像', '公司信息']
const currentStep = ref(0)

// 表单数据
const form = ref({
  title: '',
  department: '',
  city: '',
  experience: '',
  education: '',
  salaryMin: '',
  salaryMax: '',
  headcount: '',
  jobType: '全职',
  description: '',
  requirements: [''],
  highlights: [],
  requiredSkills: [],
  bonusSkills: [],
  abilityWeights: {
    technical: 20,
    communication: 15,
    learning: 20,
    innovation: 15,
    teamwork: 15,
    execution: 15
  },
  companyName: '',
  companyScale: '',
  industry: '',
  funding: '',
  companyIntro: '',
  address: '',
  benefits: []
})

// 技能输入
const skillInput = ref('')
const bonusSkillInput = ref('')

// 能力维度
const abilities = [
  { key: 'technical', name: '技术能力' },
  { key: 'communication', name: '沟通能力' },
  { key: 'learning', name: '学习能力' },
  { key: 'innovation', name: '创新能力' },
  { key: 'teamwork', name: '团队协作' },
  { key: 'execution', name: '执行能力' },
]

// 雷达图配置
const radarIndicators = [
  { name: '技术能力', max: 100 },
  { name: '沟通能力', max: 100 },
  { name: '学习能力', max: 100 },
  { name: '创新能力', max: 100 },
  { name: '团队协作', max: 100 },
  { name: '执行能力', max: 100 },
]

const previewRadar = computed(() => [{
  name: '岗位要求',
  value: [
    form.value.abilityWeights.technical,
    form.value.abilityWeights.communication,
    form.value.abilityWeights.learning,
    form.value.abilityWeights.innovation,
    form.value.abilityWeights.teamwork,
    form.value.abilityWeights.execution
  ],
  areaStyle: { color: 'rgba(139, 92, 246, 0.3)' },
  lineStyle: { color: '#8b5cf6' }
}])

// 选项
const highlightOptions = ['弹性工作', '技术氛围好', '扁平管理', '晋升空间大', '大牛带队', '国际化团队']
const benefitOptions = ['五险一金', '年终奖', '股票期权', '免费班车', '免费三餐', '健身房', '带薪年假', '团建活动']

// 成功弹窗
const showSuccess = ref(false)

// 添加技能
function addSkill(type) {
  const input = type === 'required' ? skillInput : bonusSkillInput
  const skills = type === 'required' ? form.value.requiredSkills : form.value.bonusSkills
  
  if (input.value.trim() && !skills.includes(input.value.trim())) {
    skills.push(input.value.trim())
    if (type === 'required') {
      skillInput.value = ''
    } else {
      bonusSkillInput.value = ''
    }
  }
}

// 移除技能
function removeSkill(type, index) {
  const skills = type === 'required' ? form.value.requiredSkills : form.value.bonusSkills
  skills.splice(index, 1)
}

// 添加要求
function addRequirement() {
  form.value.requirements.push('')
}

// 移除要求
function removeRequirement(index) {
  form.value.requirements.splice(index, 1)
}

// 上一步
function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 下一步
function nextStep() {
  // 简单验证
  if (currentStep.value === 0) {
    if (!form.value.title || !form.value.city || !form.value.experience) {
      toast?.('请填写必填项', 'error')
      return
    }
  }
  
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

// 提交
function submitJob() {
  if (!form.value.companyName) {
    toast?.('请填写公司名称', 'error')
    return
  }
  
  console.log('提交职位:', form.value)
  showSuccess.value = true
}

// 关闭成功弹窗
function closeSuccess() {
  showSuccess.value = false
  router.push('/job-hub')
}
</script>

<style scoped>
.post-job {
  min-height: 100vh;
  padding: 24px;
  position: relative;
}

/* 背景 */
.post-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.12;
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: #8b5cf6;
  left: -150px;
  top: 10%;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: #06b6d4;
  right: -100px;
  bottom: 20%;
}

.post-container {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 头部 */
.post-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
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
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(139, 92, 246, 0.2);
}

.header-info h1 {
  font-size: 26px;
  font-weight: 700;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.header-info h1 i {
  color: #8b5cf6;
}

.header-info p {
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
}

/* 步骤指示器 */
.step-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  position: relative;
}

.step-indicator::before {
  content: '';
  position: absolute;
  top: 16px;
  left: 40px;
  right: 40px;
  height: 2px;
  background: rgba(139, 92, 246, 0.15);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  position: relative;
  z-index: 1;
}

.step-dot {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-brand-card, #1a1a2e);
  border: 2px solid rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-brand-muted, #64748b);
  transition: all 0.3s;
}

.step.active .step-dot {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-color: #8b5cf6;
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
}

.step.done .step-dot {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.step-label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
  transition: color 0.3s;
}

.step.active .step-label {
  color: #a78bfa;
  font-weight: 600;
}

.step.done .step-label {
  color: #34d399;
}

/* 表单容器 */
.form-container {
  background: var(--color-brand-card, #1a1a2e);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  min-height: 400px;
}

.form-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.form-section h2 i {
  color: #8b5cf6;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-brand-text, #e2e8f0);
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 16px;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #8b5cf6;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.salary-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.salary-inputs input {
  flex: 1;
}

.salary-inputs span {
  color: var(--color-brand-muted, #64748b);
}

/* 要求列表 */
.requirement-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.req-item {
  display: flex;
  gap: 10px;
}

.req-item input {
  flex: 1;
  padding: 12px 16px;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  outline: none;
}

.btn-remove {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #f87171;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px dashed rgba(139, 92, 246, 0.3);
  border-radius: 10px;
  font-size: 13px;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add:hover {
  background: rgba(139, 92, 246, 0.15);
}

/* 亮点选择 */
.highlights-grid,
.benefits-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.highlight-check,
.benefit-check {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.highlight-check:has(input:checked),
.benefit-check:has(input:checked) {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}

.highlight-check input,
.benefit-check input {
  display: none;
}

.highlight-check span,
.benefit-check span {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

/* 技能输入 */
.skill-input {
  display: flex;
  gap: 10px;
}

.skill-input input {
  flex: 1;
  padding: 12px 16px;
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 10px;
  font-size: 14px;
  color: var(--color-brand-text, #e2e8f0);
  outline: none;
}

.skill-input button {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.skill-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
}

.skill-tag.required {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.skill-tag.bonus {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.skill-tag i {
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.skill-tag i:hover {
  opacity: 1;
}

/* 能力滑块 */
.ability-sliders {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.ability-slider {
  padding: 14px;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
}

.ability-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.ability-name {
  font-size: 13px;
  color: var(--color-brand-text, #e2e8f0);
}

.ability-value {
  font-size: 14px;
  font-weight: 600;
  color: #a78bfa;
}

.ability-slider input[type="range"] {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: rgba(139, 92, 246, 0.2);
  appearance: none;
  cursor: pointer;
}

.ability-slider input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4);
}

.form-hint {
  font-size: 12px;
  color: var(--color-brand-muted, #64748b);
  margin-bottom: 14px;
}

/* 画像预览 */
.profile-preview {
  margin-top: 24px;
  padding: 20px;
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 16px;
}

.profile-preview h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-brand-text, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.profile-preview h4 i {
  color: #8b5cf6;
}

.preview-radar {
  min-height: 200px;
}

/* 底部操作 */
.form-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.spacer {
  flex: 1;
}

.btn-prev,
.btn-next,
.btn-submit {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-prev {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.btn-prev:hover {
  background: rgba(139, 92, 246, 0.2);
}

.btn-next {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border: none;
  color: white;
}

.btn-next:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.btn-submit {
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
}

/* 动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 成功弹窗 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.success-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 20px;
}

.success-content {
  background: var(--color-brand-surface, #0f0f1a);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px;
  padding: 48px;
  text-align: center;
  max-width: 420px;
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
  animation: success-pop 0.5s ease;
}

@keyframes success-pop {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.success-content h2 {
  font-size: 24px;
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

.success-stats .stat {
  display: flex;
  flex-direction: column;
}

.success-stats .num {
  font-size: 28px;
  font-weight: 700;
  color: #8b5cf6;
}

.success-stats .label {
  font-size: 13px;
  color: var(--color-brand-muted, #64748b);
}

.success-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.success-actions .btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  text-decoration: none;
  transition: all 0.3s;
}

.success-actions .btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
}

.success-actions .btn-secondary {
  padding: 12px 28px;
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  font-size: 14px;
  color: var(--color-brand-muted, #64748b);
  text-decoration: none;
  transition: all 0.2s;
}

.success-actions .btn-secondary:hover {
  border-color: rgba(139, 92, 246, 0.4);
  color: var(--color-brand-text, #e2e8f0);
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .ability-sliders {
    grid-template-columns: 1fr;
  }

  .step-label {
    display: none;
  }
}
</style>
