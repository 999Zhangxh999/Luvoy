import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// ===== 类型定义 =====
export interface UserProfile {
  // 基本信息
  name: string
  age: string
  education: string
  major: string
  school: string
  experience: string // 年限
  currentCity: string
  targetCity: string[]
  // 经历
  workExperiences: WorkExperience[]
  projectExperiences: ProjectExperience[]
  // 技能
  skills: Skill[]
  // 性格偏好
  personality: PersonalityTrait[]
  workStyle: string[]
  // 完整度
  completeness: number
}

export interface WorkExperience {
  company: string
  role: string
  duration: string
  desc: string
}

export interface ProjectExperience {
  name: string
  role: string
  tech: string[]
  desc: string
}

export interface Skill {
  name: string
  category: string
  level: number // 1-5
  yearsUsed: number
}

export interface PersonalityTrait {
  trait: string
  score: number // 1-10
}

export interface CareerGoal {
  primaryCareer: string
  primaryCareerLabel: string
  alternativeCareers: string[]
  targetYears: number
  targetLevel: string
  currentStage: string
  // AI生成的路径
  roadmap: CareerRoadmap | null
}

export interface CareerRoadmap {
  stages: RoadmapStage[]
  transfers: TransferPath[]
  industryData: IndustryData
}

export interface RoadmapStage {
  level: string
  yearRange: string
  salary: string
  coreSkills: string[]
  keyMilestone: string
  description: string
}

export interface TransferPath {
  target: string
  difficulty: 'low' | 'mid' | 'high'
  migrableSkills: string[]
  gapSkills: string[]
  bestTiming: string
  afterPath: string
}

export interface IndustryData {
  trend: number[] // 12个月数据
  topCities: { city: string; demand: number }[]
  companyTypes: { type: string; percent: number }[]
  outlook: string
}

export interface SkillGap {
  skillName: string
  category: string
  userLevel: number
  requiredLevel: number
  gap: number
  status: 'qualified' | 'needs_improve' | 'major_gap'
  priority: number
}

export interface ActionTask {
  id: string
  title: string
  category: 'skill' | 'job' | 'interview' | 'project'
  source: 'roadmap' | 'skill_gap' | 'manual'
  status: 'todo' | 'doing' | 'done'
  relatedSkill?: string
  resourceUrl?: string
  dueDate?: string
  createdAt: string
}

// ===== Store =====
export const useCareerStore = defineStore('career', () => {
  // 用户画像
  const userProfile = ref<UserProfile>({
    name: '',
    age: '',
    education: '',
    major: '',
    school: '',
    experience: '',
    currentCity: '',
    targetCity: [],
    workExperiences: [],
    projectExperiences: [],
    skills: [],
    personality: [],
    workStyle: [],
    completeness: 0,
  })

  // 职业目标
  const careerGoal = ref<CareerGoal>({
    primaryCareer: '',
    primaryCareerLabel: '',
    alternativeCareers: [],
    targetYears: 5,
    targetLevel: '',
    currentStage: '',
    roadmap: null,
  })

  // 技能差距
  const skillGaps = ref<SkillGap[]>([])

  // 行动任务
  const actionTasks = ref<ActionTask[]>([])

  // 当前活跃模块（用于流程引导）
  const activeModule = ref<1 | 2 | 3 | 4 | 5>(1)

  // 计算完整度
  const computedCompleteness = computed(() => {
    const p = userProfile.value
    let score = 0
    if (p.name) score += 10
    if (p.education) score += 10
    if (p.major) score += 10
    if (p.school) score += 10
    if (p.experience) score += 10
    if (p.currentCity) score += 5
    if (p.workExperiences.length > 0) score += 15
    if (p.projectExperiences.length > 0) score += 10
    if (p.skills.length >= 3) score += 15
    if (p.personality.length > 0) score += 5
    return score
  })

  // 更新画像
  function updateProfile(data: Partial<UserProfile>) {
    userProfile.value = { ...userProfile.value, ...data }
    userProfile.value.completeness = computedCompleteness.value
  }

  // 设置职业目标
  function setCareerGoal(goal: Partial<CareerGoal>) {
    careerGoal.value = { ...careerGoal.value, ...goal }
  }

  // 生成技能差距（基于职业目标）
  function generateSkillGaps() {
    const career = careerGoal.value.primaryCareer
    const userSkills = userProfile.value.skills

    const careerRequirements: Record<string, { name: string; category: string; required: number }[]> = {
      frontend: [
        { name: 'HTML/CSS', category: '基础', required: 4 },
        { name: 'JavaScript', category: '基础', required: 5 },
        { name: 'TypeScript', category: '进阶', required: 4 },
        { name: 'React/Vue', category: '框架', required: 5 },
        { name: '工程化工具', category: '工程', required: 3 },
        { name: '性能优化', category: '进阶', required: 4 },
        { name: '跨端开发', category: '进阶', required: 3 },
        { name: '设计还原', category: '协作', required: 3 },
        { name: '代码规范', category: '工程', required: 4 },
        { name: 'Node.js基础', category: '后端', required: 2 },
      ],
      product: [
        { name: '需求分析', category: '核心', required: 5 },
        { name: '原型设计', category: '核心', required: 4 },
        { name: '用户研究', category: '核心', required: 4 },
        { name: '数据分析', category: '进阶', required: 4 },
        { name: '项目管理', category: '协作', required: 4 },
        { name: '商业思维', category: '进阶', required: 3 },
        { name: 'SQL查询', category: '工具', required: 3 },
        { name: 'Axure/Figma', category: '工具', required: 4 },
        { name: '竞品分析', category: '核心', required: 4 },
        { name: '跨部门协作', category: '协作', required: 4 },
      ],
      data: [
        { name: 'Python', category: '编程', required: 5 },
        { name: 'SQL', category: '数据库', required: 5 },
        { name: '数据可视化', category: '展现', required: 4 },
        { name: '机器学习', category: '算法', required: 4 },
        { name: '统计学', category: '数学', required: 4 },
        { name: 'Pandas/NumPy', category: '工具', required: 4 },
        { name: 'A/B测试', category: '进阶', required: 3 },
        { name: '业务理解', category: '软技能', required: 4 },
        { name: '数据清洗', category: '基础', required: 4 },
        { name: '报告撰写', category: '软技能', required: 3 },
      ],
      backend: [
        { name: 'Java/Go/Python', category: '编程', required: 5 },
        { name: '数据库设计', category: '数据库', required: 5 },
        { name: 'RESTful API', category: '接口', required: 5 },
        { name: '微服务架构', category: '架构', required: 4 },
        { name: 'Redis缓存', category: '中间件', required: 4 },
        { name: '消息队列', category: '中间件', required: 3 },
        { name: '容器化/Docker', category: '运维', required: 3 },
        { name: '系统设计', category: '架构', required: 4 },
        { name: '安全防护', category: '进阶', required: 3 },
        { name: '高并发处理', category: '进阶', required: 4 },
      ],
      ai: [
        { name: 'Python', category: '编程', required: 5 },
        { name: '深度学习', category: '算法', required: 5 },
        { name: 'PyTorch/TF', category: '框架', required: 4 },
        { name: '数学基础', category: '数学', required: 4 },
        { name: 'NLP/CV方向', category: '方向', required: 4 },
        { name: '模型调优', category: '进阶', required: 4 },
        { name: 'MLOps', category: '工程', required: 3 },
        { name: '论文阅读', category: '研究', required: 3 },
        { name: '数据处理', category: '基础', required: 4 },
        { name: 'AIGC工具', category: '新兴', required: 3 },
      ],
    }

    const requirements = careerRequirements[career] || careerRequirements['frontend']

    const gaps: SkillGap[] = requirements.map((req, idx) => {
      const userSkill = userSkills.find(s =>
        s.name.toLowerCase().includes(req.name.toLowerCase().split('/')[0])
      )
      const userLevel = userSkill?.level || Math.floor(Math.random() * 3) + 1
      const gap = req.required - userLevel

      return {
        skillName: req.name,
        category: req.category,
        userLevel,
        requiredLevel: req.required,
        gap,
        status: gap <= 0 ? 'qualified' : gap <= 1 ? 'needs_improve' : 'major_gap',
        priority: idx + 1,
      }
    })

    skillGaps.value = gaps
  }

  // 添加行动任务
  function addTask(task: Omit<ActionTask, 'id' | 'createdAt'>) {
    actionTasks.value.push({
      ...task,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
    })
  }

  // 批量导入任务
  function importTasksFromRoadmap() {
    const stages = careerGoal.value.roadmap?.stages || []
    stages.slice(0, 3).forEach((stage, i) => {
      stage.coreSkills.slice(0, 2).forEach(skill => {
        addTask({
          title: `掌握${skill}（${stage.level}阶段）`,
          category: 'skill',
          source: 'roadmap',
          status: i === 0 ? 'doing' : 'todo',
          relatedSkill: skill,
        })
      })
    })
  }

  function importTasksFromGaps() {
    const topGaps = skillGaps.value
      .filter(g => g.status !== 'qualified')
      .sort((a, b) => b.gap - a.gap)
      .slice(0, 5)

    topGaps.forEach(gap => {
      addTask({
        title: `提升${gap.skillName}（差距${gap.gap}级）`,
        category: 'skill',
        source: 'skill_gap',
        status: 'todo',
        relatedSkill: gap.skillName,
      })
    })
  }

  function updateTaskStatus(id: string, status: ActionTask['status']) {
    const task = actionTasks.value.find(t => t.id === id)
    if (task) task.status = status
  }

  // 任务统计
  const taskStats = computed(() => {
    const total = actionTasks.value.length
    const done = actionTasks.value.filter(t => t.status === 'done').length
    const doing = actionTasks.value.filter(t => t.status === 'doing').length
    const todo = actionTasks.value.filter(t => t.status === 'todo').length
    return { total, done, doing, todo, rate: total ? Math.round((done / total) * 100) : 0 }
  })

  return {
    userProfile,
    careerGoal,
    skillGaps,
    actionTasks,
    activeModule,
    computedCompleteness,
    taskStats,
    updateProfile,
    setCareerGoal,
    generateSkillGaps,
    addTask,
    importTasksFromRoadmap,
    importTasksFromGaps,
    updateTaskStatus,
  }
})
