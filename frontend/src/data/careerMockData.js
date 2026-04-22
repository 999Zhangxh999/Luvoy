// 职业探索模拟数据
// 包含职业列表、晋升/转岗关系、详细画像数据

// 职业类别及颜色
export const careerCategories = [
    { name: '技术开发', color: '#7c3aed' },
    { name: '产品设计', color: '#06b6d4' },
    { name: '数据分析', color: '#10b981' },
    { name: '运营管理', color: '#f59e0b' },
    { name: '市场销售', color: '#ef4444' },
    { name: '人力资源', color: '#ec4899' },
    { name: '财务金融', color: '#8b5cf6' },
    { name: '教育培训', color: '#14b8a6' },
]

// 获取类别颜色
export function getCategoryColor(category) {
    const cat = careerCategories.find(c => c.name === category)
    return cat?.color || '#64748b'
}

// 完整的职业列表
export const mockCareers = [
    // 技术开发类
    { id: 'fe-dev', name: '前端开发工程师', category: '技术开发', level: '初级', salary: '15-25K', demand: '高', promotions: 3, transfers: 4 },
    { id: 'be-dev', name: '后端开发工程师', category: '技术开发', level: '初级', salary: '15-28K', demand: '高', promotions: 3, transfers: 3 },
    { id: 'full-stack', name: '全栈工程师', category: '技术开发', level: '中级', salary: '25-40K', demand: '高', promotions: 2, transfers: 4 },
    { id: 'mobile-dev', name: '移动端开发工程师', category: '技术开发', level: '初级', salary: '18-30K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'devops', name: 'DevOps工程师', category: '技术开发', level: '中级', salary: '25-45K', demand: '高', promotions: 2, transfers: 2 },
    { id: 'tech-lead', name: '技术主管', category: '技术开发', level: '高级', salary: '40-60K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'architect', name: '架构师', category: '技术开发', level: '资深', salary: '50-80K', demand: '中', promotions: 1, transfers: 2 },
    { id: 'cto', name: 'CTO', category: '技术开发', level: '管理', salary: '80-150K', demand: '低', promotions: 0, transfers: 2 },
    { id: 'qa-eng', name: '测试工程师', category: '技术开发', level: '初级', salary: '12-20K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'security-eng', name: '安全工程师', category: '技术开发', level: '中级', salary: '25-45K', demand: '中', promotions: 2, transfers: 2 },

    // 产品设计类
    { id: 'ui-designer', name: 'UI设计师', category: '产品设计', level: '初级', salary: '12-22K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'ux-designer', name: 'UX设计师', category: '产品设计', level: '中级', salary: '18-30K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'product-mgr', name: '产品经理', category: '产品设计', level: '中级', salary: '20-40K', demand: '高', promotions: 3, transfers: 4 },
    { id: 'senior-pm', name: '高级产品经理', category: '产品设计', level: '高级', salary: '35-55K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'product-director', name: '产品总监', category: '产品设计', level: '管理', salary: '50-80K', demand: '低', promotions: 1, transfers: 2 },
    { id: 'visual-designer', name: '视觉设计师', category: '产品设计', level: '初级', salary: '10-18K', demand: '中', promotions: 2, transfers: 2 },
    { id: 'interaction-designer', name: '交互设计师', category: '产品设计', level: '中级', salary: '18-32K', demand: '中', promotions: 2, transfers: 3 },

    // 数据分析类
    { id: 'data-analyst', name: '数据分析师', category: '数据分析', level: '初级', salary: '15-25K', demand: '高', promotions: 3, transfers: 4 },
    { id: 'bi-analyst', name: 'BI分析师', category: '数据分析', level: '中级', salary: '20-35K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'data-scientist', name: '数据科学家', category: '数据分析', level: '高级', salary: '35-60K', demand: '高', promotions: 2, transfers: 2 },
    { id: 'ml-engineer', name: '机器学习工程师', category: '数据分析', level: '高级', salary: '40-70K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'ai-researcher', name: 'AI研究员', category: '数据分析', level: '资深', salary: '50-100K', demand: '中', promotions: 1, transfers: 2 },
    { id: 'data-engineer', name: '数据工程师', category: '数据分析', level: '中级', salary: '25-40K', demand: '高', promotions: 2, transfers: 3 },

    // 运营管理类
    { id: 'ops-specialist', name: '运营专员', category: '运营管理', level: '初级', salary: '8-15K', demand: '高', promotions: 3, transfers: 4 },
    { id: 'content-ops', name: '内容运营', category: '运营管理', level: '初级', salary: '10-18K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'user-ops', name: '用户运营', category: '运营管理', level: '初级', salary: '10-18K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'ops-manager', name: '运营经理', category: '运营管理', level: '中级', salary: '18-30K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'ops-director', name: '运营总监', category: '运营管理', level: '高级', salary: '35-60K', demand: '低', promotions: 1, transfers: 2 },
    { id: 'coo', name: 'COO', category: '运营管理', level: '管理', salary: '60-120K', demand: '低', promotions: 0, transfers: 1 },
    { id: 'project-mgr', name: '项目经理', category: '运营管理', level: '中级', salary: '20-35K', demand: '高', promotions: 2, transfers: 4 },

    // 市场销售类
    { id: 'marketing-specialist', name: '市场专员', category: '市场销售', level: '初级', salary: '8-15K', demand: '高', promotions: 3, transfers: 3 },
    { id: 'brand-manager', name: '品牌经理', category: '市场销售', level: '中级', salary: '18-35K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'marketing-director', name: '市场总监', category: '市场销售', level: '高级', salary: '40-70K', demand: '低', promotions: 1, transfers: 2 },
    { id: 'sales-rep', name: '销售代表', category: '市场销售', level: '初级', salary: '8-20K', demand: '高', promotions: 3, transfers: 2 },
    { id: 'sales-manager', name: '销售经理', category: '市场销售', level: '中级', salary: '20-40K', demand: '中', promotions: 2, transfers: 2 },
    { id: 'bd-manager', name: '商务拓展经理', category: '市场销售', level: '中级', salary: '18-35K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'cmo', name: 'CMO', category: '市场销售', level: '管理', salary: '60-100K', demand: '低', promotions: 0, transfers: 1 },

    // 人力资源类
    { id: 'hr-specialist', name: 'HR专员', category: '人力资源', level: '初级', salary: '8-15K', demand: '中', promotions: 3, transfers: 2 },
    { id: 'recruiter', name: '招聘专员', category: '人力资源', level: '初级', salary: '10-18K', demand: '高', promotions: 2, transfers: 2 },
    { id: 'hrbp', name: 'HRBP', category: '人力资源', level: '中级', salary: '18-35K', demand: '中', promotions: 2, transfers: 2 },
    { id: 'hr-manager', name: '人力资源经理', category: '人力资源', level: '高级', salary: '25-45K', demand: '中', promotions: 1, transfers: 2 },
    { id: 'hr-director', name: 'HRD', category: '人力资源', level: '管理', salary: '40-80K', demand: '低', promotions: 1, transfers: 1 },
    { id: 'training-specialist', name: '培训专员', category: '人力资源', level: '初级', salary: '10-18K', demand: '中', promotions: 2, transfers: 3 },

    // 财务金融类
    { id: 'accountant', name: '会计', category: '财务金融', level: '初级', salary: '8-15K', demand: '高', promotions: 3, transfers: 2 },
    { id: 'financial-analyst', name: '财务分析师', category: '财务金融', level: '中级', salary: '18-35K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'finance-manager', name: '财务经理', category: '财务金融', level: '高级', salary: '30-50K', demand: '中', promotions: 1, transfers: 2 },
    { id: 'cfo', name: 'CFO', category: '财务金融', level: '管理', salary: '60-120K', demand: '低', promotions: 0, transfers: 1 },
    { id: 'investment-analyst', name: '投资分析师', category: '财务金融', level: '中级', salary: '25-50K', demand: '中', promotions: 2, transfers: 2 },
    { id: 'risk-analyst', name: '风控分析师', category: '财务金融', level: '中级', salary: '20-40K', demand: '高', promotions: 2, transfers: 2 },

    // 教育培训类
    { id: 'training-coordinator', name: '培训协调员', category: '教育培训', level: '初级', salary: '8-15K', demand: '中', promotions: 2, transfers: 3 },
    { id: 'curriculum-designer', name: '课程设计师', category: '教育培训', level: '中级', salary: '15-28K', demand: '中', promotions: 2, transfers: 2 },
    { id: 'education-consultant', name: '教育顾问', category: '教育培训', level: '中级', salary: '12-25K', demand: '高', promotions: 2, transfers: 3 },
    { id: 'learning-tech', name: '学习技术专家', category: '教育培训', level: '高级', salary: '25-45K', demand: '中', promotions: 1, transfers: 2 },
]

// 给每个职业添加颜色
export const careersWithColors = mockCareers.map(career => ({
    ...career,
    color: getCategoryColor(career.category),
}))

// 职业关系连接（晋升和转岗）
export const careerLinks = [
    // 技术开发晋升路径
    { source: 'fe-dev', target: 'full-stack', type: 'promotion', years: 2 },
    { source: 'fe-dev', target: 'tech-lead', type: 'promotion', years: 4 },
    { source: 'be-dev', target: 'full-stack', type: 'promotion', years: 2 },
    { source: 'be-dev', target: 'tech-lead', type: 'promotion', years: 4 },
    { source: 'be-dev', target: 'architect', type: 'promotion', years: 6 },
    { source: 'full-stack', target: 'tech-lead', type: 'promotion', years: 2 },
    { source: 'full-stack', target: 'architect', type: 'promotion', years: 4 },
    { source: 'tech-lead', target: 'architect', type: 'promotion', years: 3 },
    { source: 'tech-lead', target: 'cto', type: 'promotion', years: 5 },
    { source: 'architect', target: 'cto', type: 'promotion', years: 3 },
    { source: 'devops', target: 'tech-lead', type: 'promotion', years: 3 },
    { source: 'qa-eng', target: 'tech-lead', type: 'promotion', years: 5 },
    { source: 'security-eng', target: 'architect', type: 'promotion', years: 4 },

    // 技术开发转岗路径
    { source: 'fe-dev', target: 'ui-designer', type: 'transfer' },
    { source: 'fe-dev', target: 'product-mgr', type: 'transfer' },
    { source: 'be-dev', target: 'data-engineer', type: 'transfer' },
    { source: 'be-dev', target: 'devops', type: 'transfer' },
    { source: 'full-stack', target: 'product-mgr', type: 'transfer' },
    { source: 'qa-eng', target: 'devops', type: 'transfer' },
    { source: 'tech-lead', target: 'project-mgr', type: 'transfer' },

    // 产品设计晋升路径
    { source: 'ui-designer', target: 'ux-designer', type: 'promotion', years: 2 },
    { source: 'ui-designer', target: 'visual-designer', type: 'transfer' },
    { source: 'ux-designer', target: 'senior-pm', type: 'promotion', years: 3 },
    { source: 'ux-designer', target: 'interaction-designer', type: 'transfer' },
    { source: 'product-mgr', target: 'senior-pm', type: 'promotion', years: 2 },
    { source: 'senior-pm', target: 'product-director', type: 'promotion', years: 3 },
    { source: 'product-director', target: 'coo', type: 'promotion', years: 4 },
    { source: 'interaction-designer', target: 'ux-designer', type: 'promotion', years: 2 },

    // 产品设计转岗路径
    { source: 'product-mgr', target: 'ops-manager', type: 'transfer' },
    { source: 'product-mgr', target: 'data-analyst', type: 'transfer' },
    { source: 'ux-designer', target: 'product-mgr', type: 'transfer' },

    // 数据分析晋升路径
    { source: 'data-analyst', target: 'bi-analyst', type: 'promotion', years: 2 },
    { source: 'data-analyst', target: 'data-scientist', type: 'promotion', years: 3 },
    { source: 'bi-analyst', target: 'data-scientist', type: 'promotion', years: 2 },
    { source: 'data-scientist', target: 'ai-researcher', type: 'promotion', years: 3 },
    { source: 'data-engineer', target: 'data-scientist', type: 'promotion', years: 3 },
    { source: 'ml-engineer', target: 'ai-researcher', type: 'promotion', years: 2 },

    // 数据分析转岗路径
    { source: 'data-analyst', target: 'product-mgr', type: 'transfer' },
    { source: 'data-analyst', target: 'financial-analyst', type: 'transfer' },
    { source: 'data-engineer', target: 'be-dev', type: 'transfer' },
    { source: 'ml-engineer', target: 'data-scientist', type: 'transfer' },

    // 运营管理晋升路径
    { source: 'ops-specialist', target: 'user-ops', type: 'promotion', years: 1 },
    { source: 'ops-specialist', target: 'content-ops', type: 'transfer' },
    { source: 'content-ops', target: 'ops-manager', type: 'promotion', years: 2 },
    { source: 'user-ops', target: 'ops-manager', type: 'promotion', years: 2 },
    { source: 'ops-manager', target: 'ops-director', type: 'promotion', years: 3 },
    { source: 'ops-director', target: 'coo', type: 'promotion', years: 4 },
    { source: 'project-mgr', target: 'ops-director', type: 'promotion', years: 4 },

    // 运营管理转岗路径
    { source: 'content-ops', target: 'marketing-specialist', type: 'transfer' },
    { source: 'user-ops', target: 'data-analyst', type: 'transfer' },
    { source: 'project-mgr', target: 'product-mgr', type: 'transfer' },

    // 市场销售晋升路径
    { source: 'marketing-specialist', target: 'brand-manager', type: 'promotion', years: 2 },
    { source: 'brand-manager', target: 'marketing-director', type: 'promotion', years: 3 },
    { source: 'marketing-director', target: 'cmo', type: 'promotion', years: 4 },
    { source: 'sales-rep', target: 'sales-manager', type: 'promotion', years: 2 },
    { source: 'sales-manager', target: 'marketing-director', type: 'promotion', years: 4 },
    { source: 'bd-manager', target: 'marketing-director', type: 'promotion', years: 3 },

    // 市场销售转岗路径
    { source: 'marketing-specialist', target: 'content-ops', type: 'transfer' },
    { source: 'bd-manager', target: 'sales-manager', type: 'transfer' },
    { source: 'sales-rep', target: 'bd-manager', type: 'transfer' },

    // 人力资源晋升路径
    { source: 'hr-specialist', target: 'recruiter', type: 'transfer' },
    { source: 'hr-specialist', target: 'hrbp', type: 'promotion', years: 2 },
    { source: 'recruiter', target: 'hrbp', type: 'promotion', years: 2 },
    { source: 'hrbp', target: 'hr-manager', type: 'promotion', years: 3 },
    { source: 'hr-manager', target: 'hr-director', type: 'promotion', years: 4 },
    { source: 'training-specialist', target: 'hr-manager', type: 'promotion', years: 4 },

    // 人力资源转岗路径
    { source: 'training-specialist', target: 'training-coordinator', type: 'transfer' },
    { source: 'recruiter', target: 'bd-manager', type: 'transfer' },

    // 财务金融晋升路径
    { source: 'accountant', target: 'financial-analyst', type: 'promotion', years: 2 },
    { source: 'financial-analyst', target: 'finance-manager', type: 'promotion', years: 3 },
    { source: 'finance-manager', target: 'cfo', type: 'promotion', years: 5 },
    { source: 'investment-analyst', target: 'finance-manager', type: 'promotion', years: 4 },
    { source: 'risk-analyst', target: 'finance-manager', type: 'promotion', years: 4 },

    // 财务金融转岗路径
    { source: 'financial-analyst', target: 'data-analyst', type: 'transfer' },
    { source: 'risk-analyst', target: 'data-analyst', type: 'transfer' },
    { source: 'investment-analyst', target: 'bd-manager', type: 'transfer' },

    // 教育培训晋升路径
    { source: 'training-coordinator', target: 'curriculum-designer', type: 'promotion', years: 2 },
    { source: 'curriculum-designer', target: 'learning-tech', type: 'promotion', years: 3 },
    { source: 'education-consultant', target: 'learning-tech', type: 'promotion', years: 3 },

    // 教育培训转岗路径
    { source: 'curriculum-designer', target: 'product-mgr', type: 'transfer' },
    { source: 'education-consultant', target: 'sales-manager', type: 'transfer' },
    { source: 'training-coordinator', target: 'training-specialist', type: 'transfer' },
]

// 详细的职业画像数据（用于详情页）
export const careerProfiles = {
    'fe-dev': {
        id: 'fe-dev',
        position_name: '前端开发工程师',
        category: '技术开发',
        level: '初级-中级',
        summary: '负责Web应用的前端开发，包括页面布局、交互效果、性能优化等。需要掌握HTML、CSS、JavaScript等核心技术，熟悉主流前端框架。',
        education_req: '本科及以上',
        experience_req: '1-3年',
        salary_range: '15-25K',
        demand: '高',

        // 技能要求
        technical_skills: ['Vue3', 'React', 'TypeScript', 'JavaScript', 'CSS3', 'Vite', 'Webpack', 'Node.js', 'Git', '微信小程序'],
        soft_skills: ['沟通能力', '团队协作', '学习能力', '问题解决'],
        certificates: ['软件设计师', 'Web前端开发证书'],

        // 能力雷达数据
        innovation_ability: 7,
        learning_ability: 9,
        pressure_resistance: 7,
        communication_skill: 6,
        teamwork_ability: 8,
        internship_ability: 8,

        // 权重
        weight_basic: 0.2,
        weight_skill: 0.4,
        weight_quality: 0.2,
        weight_potential: 0.2,

        // 市场数据
        market_data: {
            job_count: 12400,
            avg_salary: 26000,
            competition_ratio: '1:8',
            avg_hire_days: 21,
            salary_distribution: [
                { range: '10-15K', percent: 12 },
                { range: '15-20K', percent: 28 },
                { range: '20-30K', percent: 35 },
                { range: '30-40K', percent: 18 },
                { range: '40K+', percent: 7 },
            ],
            experience_distribution: [
                { range: '应届生', percent: 15 },
                { range: '1-3年', percent: 42 },
                { range: '3-5年', percent: 30 },
                { range: '5年以上', percent: 13 },
            ],
            education_distribution: [
                { range: '大专', percent: 18 },
                { range: '本科', percent: 65 },
                { range: '硕士及以上', percent: 17 },
            ],
            industry_distribution: [
                { name: '互联网', percent: 45 },
                { name: '金融科技', percent: 18 },
                { name: '电商', percent: 15 },
                { name: '游戏', percent: 10 },
                { name: '教育', percent: 7 },
                { name: '其他', percent: 5 },
            ],
            city_distribution: [
                { name: '北京', percent: 32 },
                { name: '上海', percent: 28 },
                { name: '深圳', percent: 20 },
                { name: '杭州', percent: 10 },
                { name: '广州', percent: 6 },
                { name: '成都', percent: 4 },
            ],
            trend_12months: [
                { month: '04', value: 8200 },
                { month: '05', value: 8800 },
                { month: '06', value: 9500 },
                { month: '07', value: 10200 },
                { month: '08', value: 9800 },
                { month: '09', value: 10500 },
                { month: '10', value: 11200 },
                { month: '11', value: 11800 },
                { month: '12', value: 10500 },
                { month: '01', value: 9200 },
                { month: '02', value: 11000 },
                { month: '03', value: 12400 },
            ],
            skill_heat: [
                { name: 'Vue3', heat: 95, growth: 15 },
                { name: 'React', heat: 90, growth: 8 },
                { name: 'TypeScript', heat: 88, growth: 25 },
                { name: 'JavaScript', heat: 85, growth: 2 },
                { name: 'CSS3', heat: 75, growth: 5 },
                { name: 'Vite', heat: 70, growth: 40 },
                { name: 'Webpack', heat: 65, growth: -5 },
                { name: 'Node.js', heat: 60, growth: 10 },
                { name: 'Git', heat: 58, growth: 3 },
                { name: '微信小程序', heat: 55, growth: 8 },
                { name: 'Next.js', heat: 50, growth: 35 },
                { name: 'Tailwind', heat: 48, growth: 45 },
                { name: 'Three.js', heat: 35, growth: 20 },
                { name: 'Jest', heat: 32, growth: 12 },
                { name: 'GraphQL', heat: 28, growth: 15 },
            ],
        },

        // 核心需求描述
        core_requirements: {
            technical: [
                '熟练掌握 Vue3 / React 及其生态',
                'TypeScript 有实际开发经验',
                '熟悉 Vite/Webpack 构建体系',
                '了解性能优化方法论',
                '具备从0到1项目经验优先',
            ],
            soft: [
                '良好的跨部门沟通协调能力',
                '有责任心与较强抗压能力',
                '能独立拆解问题与方案输出',
                '对用户体验有极致追求',
                '主动学习与知识分享意识',
            ],
            bonus: [
                '有开源项目贡献经验',
                '多次担任代码审核官经验',
                '具有跨端开发能力(小程序/RN)',
                '了解服务端渲染SSR/SSG',
                'Node.js 全栈开发能力',
            ],
        },

        // 职业发展路径
        career_path: {
            promotions_from: [
                { to_position: '高级前端工程师', estimated_years: 2, difficulty: 2, description: '深入掌握前端技术，提升架构能力' },
                { to_position: '技术主管', estimated_years: 4, difficulty: 3, description: '具备团队管理能力，技术选型能力' },
                { to_position: '前端架构师', estimated_years: 5, difficulty: 4, description: '主导大型项目架构，制定技术规范' },
            ],
            transfers: [
                { to_position: '全栈工程师', estimated_years: 2, description: '学习后端技术，成为全栈开发者' },
                { to_position: '产品经理', estimated_years: 3, description: '转型产品方向，利用技术背景优势' },
                { to_position: 'UI设计师', estimated_years: 2, description: '结合设计能力，转型设计方向' },
            ],
        },
    },

    'product-mgr': {
        id: 'product-mgr',
        position_name: '产品经理',
        category: '产品设计',
        level: '中级',
        summary: '负责产品全生命周期管理，包括需求分析、产品规划、原型设计、项目跟进等。需要具备良好的用户洞察能力和跨部门协调能力。',
        education_req: '本科及以上',
        experience_req: '2-5年',
        salary_range: '20-40K',
        demand: '高',

        technical_skills: ['Axure', 'Figma', 'SQL', '数据分析', '用户研究', 'A/B测试', 'PRD撰写', '项目管理'],
        soft_skills: ['沟通协调', '逻辑思维', '用户洞察', '商业思维', '抗压能力'],
        certificates: ['PMP', 'NPDP', '产品经理认证'],

        innovation_ability: 8,
        learning_ability: 8,
        pressure_resistance: 8,
        communication_skill: 9,
        teamwork_ability: 9,
        internship_ability: 7,

        weight_basic: 0.15,
        weight_skill: 0.35,
        weight_quality: 0.3,
        weight_potential: 0.2,

        market_data: {
            job_count: 8500,
            avg_salary: 32000,
            competition_ratio: '1:12',
            avg_hire_days: 28,
            salary_distribution: [
                { range: '15-20K', percent: 15 },
                { range: '20-30K', percent: 35 },
                { range: '30-40K', percent: 30 },
                { range: '40-50K', percent: 15 },
                { range: '50K+', percent: 5 },
            ],
            experience_distribution: [
                { range: '1-3年', percent: 25 },
                { range: '3-5年', percent: 40 },
                { range: '5-8年', percent: 25 },
                { range: '8年以上', percent: 10 },
            ],
            education_distribution: [
                { range: '大专', percent: 10 },
                { range: '本科', percent: 70 },
                { range: '硕士及以上', percent: 20 },
            ],
            industry_distribution: [
                { name: '互联网', percent: 50 },
                { name: '金融科技', percent: 15 },
                { name: '电商', percent: 12 },
                { name: '企业服务', percent: 10 },
                { name: '教育', percent: 8 },
                { name: '其他', percent: 5 },
            ],
            city_distribution: [
                { name: '北京', percent: 35 },
                { name: '上海', percent: 25 },
                { name: '深圳', percent: 18 },
                { name: '杭州', percent: 12 },
                { name: '广州', percent: 6 },
                { name: '成都', percent: 4 },
            ],
            trend_12months: [
                { month: '04', value: 6500 },
                { month: '05', value: 7000 },
                { month: '06', value: 7200 },
                { month: '07', value: 7800 },
                { month: '08', value: 7500 },
                { month: '09', value: 8000 },
                { month: '10', value: 8200 },
                { month: '11', value: 8500 },
                { month: '12', value: 7800 },
                { month: '01', value: 7200 },
                { month: '02', value: 8000 },
                { month: '03', value: 8500 },
            ],
            skill_heat: [
                { name: '需求分析', heat: 95, growth: 5 },
                { name: '数据分析', heat: 90, growth: 20 },
                { name: 'Axure', heat: 85, growth: -5 },
                { name: 'Figma', heat: 82, growth: 30 },
                { name: '用户研究', heat: 78, growth: 15 },
                { name: 'SQL', heat: 72, growth: 18 },
                { name: 'A/B测试', heat: 68, growth: 25 },
                { name: 'PRD撰写', heat: 65, growth: 3 },
                { name: '项目管理', heat: 60, growth: 8 },
                { name: 'AI产品', heat: 55, growth: 80 },
            ],
        },

        core_requirements: {
            technical: [
                '熟练使用产品原型工具(Axure/Figma)',
                '具备数据分析能力，熟悉SQL',
                '熟悉用户研究方法论',
                '能够独立完成PRD撰写',
                '有完整的产品0-1经验',
            ],
            soft: [
                '优秀的跨部门沟通协调能力',
                '强逻辑思维与商业敏感度',
                '对用户需求有深刻洞察',
                '能在压力下推动项目进展',
                '具备同理心与责任心',
            ],
            bonus: [
                '有AI/大模型产品经验',
                '具备技术背景',
                '有To B或To C成功产品案例',
                '熟悉敏捷开发流程',
                '有海外产品经验',
            ],
        },

        career_path: {
            promotions_from: [
                { to_position: '高级产品经理', estimated_years: 2, difficulty: 2, description: '负责更复杂的产品线' },
                { to_position: '产品总监', estimated_years: 4, difficulty: 3, description: '管理产品团队，制定产品战略' },
                { to_position: 'COO', estimated_years: 8, difficulty: 5, description: '全面负责公司运营' },
            ],
            transfers: [
                { to_position: '运营经理', estimated_years: 2, description: '转型运营方向' },
                { to_position: '数据分析师', estimated_years: 2, description: '转型数据方向' },
                { to_position: '创业', estimated_years: 5, description: '自主创业' },
            ],
        },
    },

    'data-analyst': {
        id: 'data-analyst',
        position_name: '数据分析师',
        category: '数据分析',
        level: '初级-中级',
        summary: '负责数据的采集、清洗、分析和可视化，为业务决策提供数据支持。需要掌握SQL、Python等工具，具备良好的业务理解能力。',
        education_req: '本科及以上',
        experience_req: '1-3年',
        salary_range: '15-25K',
        demand: '高',

        technical_skills: ['Python', 'SQL', 'Excel', 'Tableau', 'PowerBI', '统计学', '机器学习基础', 'R语言'],
        soft_skills: ['逻辑思维', '业务理解', '沟通表达', '细节把控'],
        certificates: ['数据分析师', 'Google Analytics'],

        innovation_ability: 7,
        learning_ability: 9,
        pressure_resistance: 7,
        communication_skill: 7,
        teamwork_ability: 7,
        internship_ability: 8,

        weight_basic: 0.2,
        weight_skill: 0.4,
        weight_quality: 0.2,
        weight_potential: 0.2,

        market_data: {
            job_count: 9800,
            avg_salary: 22000,
            competition_ratio: '1:10',
            avg_hire_days: 24,
            salary_distribution: [
                { range: '10-15K', percent: 18 },
                { range: '15-20K', percent: 32 },
                { range: '20-30K', percent: 35 },
                { range: '30-40K', percent: 12 },
                { range: '40K+', percent: 3 },
            ],
            experience_distribution: [
                { range: '应届生', percent: 20 },
                { range: '1-3年', percent: 45 },
                { range: '3-5年', percent: 25 },
                { range: '5年以上', percent: 10 },
            ],
            education_distribution: [
                { range: '大专', percent: 12 },
                { range: '本科', percent: 65 },
                { range: '硕士及以上', percent: 23 },
            ],
            industry_distribution: [
                { name: '互联网', percent: 40 },
                { name: '金融', percent: 20 },
                { name: '电商', percent: 15 },
                { name: '咨询', percent: 10 },
                { name: '零售', percent: 8 },
                { name: '其他', percent: 7 },
            ],
            city_distribution: [
                { name: '北京', percent: 30 },
                { name: '上海', percent: 28 },
                { name: '深圳', percent: 18 },
                { name: '杭州', percent: 12 },
                { name: '广州', percent: 7 },
                { name: '成都', percent: 5 },
            ],
            trend_12months: [
                { month: '04', value: 7500 },
                { month: '05', value: 8000 },
                { month: '06', value: 8500 },
                { month: '07', value: 9000 },
                { month: '08', value: 8800 },
                { month: '09', value: 9200 },
                { month: '10', value: 9500 },
                { month: '11', value: 9800 },
                { month: '12', value: 9000 },
                { month: '01', value: 8500 },
                { month: '02', value: 9200 },
                { month: '03', value: 9800 },
            ],
            skill_heat: [
                { name: 'SQL', heat: 98, growth: 5 },
                { name: 'Python', heat: 92, growth: 15 },
                { name: 'Excel', heat: 88, growth: -2 },
                { name: 'Tableau', heat: 75, growth: 10 },
                { name: 'PowerBI', heat: 70, growth: 20 },
                { name: '统计学', heat: 68, growth: 5 },
                { name: '机器学习', heat: 55, growth: 30 },
                { name: 'R语言', heat: 45, growth: -5 },
            ],
        },

        core_requirements: {
            technical: [
                '熟练掌握SQL进行数据查询',
                'Python数据处理(Pandas/NumPy)',
                '熟悉数据可视化工具',
                '掌握基本的统计学知识',
                '了解AB测试方法论',
            ],
            soft: [
                '良好的业务理解能力',
                '严谨的逻辑思维',
                '清晰的数据报告表达',
                '主动发现问题的能力',
                '跨部门沟通协作',
            ],
            bonus: [
                '有机器学习项目经验',
                '熟悉大数据处理(Spark/Hive)',
                '具备行业经验(金融/电商等)',
                '有数据产品化经验',
                '掌握数据治理知识',
            ],
        },

        career_path: {
            promotions_from: [
                { to_position: 'BI分析师', estimated_years: 2, difficulty: 2, description: '深入商业智能领域' },
                { to_position: '数据科学家', estimated_years: 3, difficulty: 4, description: '提升算法和建模能力' },
                { to_position: '数据分析经理', estimated_years: 4, difficulty: 3, description: '带领数据分析团队' },
            ],
            transfers: [
                { to_position: '产品经理', estimated_years: 2, description: '利用数据能力转型产品' },
                { to_position: '数据工程师', estimated_years: 2, description: '转型数据基础设施方向' },
                { to_position: '量化分析师', estimated_years: 3, description: '进入金融量化领域' },
            ],
        },
    },
}

// 获取职业画像详情
export function getCareerProfile(id) {
    return careerProfiles[id] || null
}

// 默认生成所有职业的基础画像
export function getAllCareerProfiles() {
    return mockCareers.map(career => {
        const existingProfile = careerProfiles[career.id]
        if (existingProfile) return existingProfile

        // 生成默认画像
        return {
            id: career.id,
            position_name: career.name,
            category: career.category,
            level: career.level,
            summary: `${career.name}是${career.category}领域的重要岗位，负责相关业务的执行与推进。`,
            education_req: '本科及以上',
            experience_req: '1-3年',
            salary_range: career.salary,
            demand: career.demand,
            technical_skills: ['专业技能1', '专业技能2', '专业技能3'],
            soft_skills: ['沟通能力', '团队协作', '学习能力'],
            certificates: [],
            innovation_ability: 6 + Math.random() * 3,
            learning_ability: 6 + Math.random() * 3,
            pressure_resistance: 6 + Math.random() * 3,
            communication_skill: 6 + Math.random() * 3,
            teamwork_ability: 6 + Math.random() * 3,
            internship_ability: 6 + Math.random() * 3,
            weight_basic: 0.25,
            weight_skill: 0.35,
            weight_quality: 0.2,
            weight_potential: 0.2,
            market_data: {
                job_count: Math.floor(3000 + Math.random() * 10000),
                avg_salary: parseInt(career.salary.split('-')[0]) * 1000 + 5000,
                competition_ratio: '1:' + Math.floor(5 + Math.random() * 10),
                avg_hire_days: Math.floor(15 + Math.random() * 20),
                salary_distribution: [
                    { range: '10-15K', percent: 15 },
                    { range: '15-20K', percent: 30 },
                    { range: '20-30K', percent: 35 },
                    { range: '30-40K', percent: 15 },
                    { range: '40K+', percent: 5 },
                ],
                experience_distribution: [
                    { range: '应届生', percent: 15 },
                    { range: '1-3年', percent: 40 },
                    { range: '3-5年', percent: 30 },
                    { range: '5年以上', percent: 15 },
                ],
                education_distribution: [
                    { range: '大专', percent: 15 },
                    { range: '本科', percent: 65 },
                    { range: '硕士及以上', percent: 20 },
                ],
                industry_distribution: [
                    { name: '互联网', percent: 40 },
                    { name: '金融', percent: 20 },
                    { name: '电商', percent: 15 },
                    { name: '制造', percent: 10 },
                    { name: '教育', percent: 8 },
                    { name: '其他', percent: 7 },
                ],
                city_distribution: [
                    { name: '北京', percent: 30 },
                    { name: '上海', percent: 25 },
                    { name: '深圳', percent: 18 },
                    { name: '杭州', percent: 12 },
                    { name: '广州', percent: 8 },
                    { name: '成都', percent: 7 },
                ],
                trend_12months: Array.from({ length: 12 }, (_, i) => ({
                    month: String((i + 4) % 12 || 12).padStart(2, '0'),
                    value: Math.floor(5000 + Math.random() * 8000),
                })),
                skill_heat: [],
            },
            core_requirements: {
                technical: ['核心技术要求1', '核心技术要求2', '核心技术要求3'],
                soft: ['沟通协调能力', '团队合作精神', '学习能力强'],
                bonus: ['相关行业经验', '项目管理能力'],
            },
            career_path: {
                promotions_from: career.promotions > 0 ? [
                    { to_position: '高级' + career.name, estimated_years: 2, difficulty: 2, description: '晋升到高级岗位' },
                ] : [],
                transfers: career.transfers > 0 ? [
                    { to_position: '相关岗位', estimated_years: 2, description: '横向转岗' },
                ] : [],
            },
        }
    })
}
