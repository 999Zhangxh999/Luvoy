<template>
  <div class="about-page">
    
    <!-- 左右布局容器 -->
    <div class="about-layout">
      
      <!-- 左侧目录导航 -->
      <aside class="about-sidebar">
        <div class="sidebar-header">
          <i class="bi bi-book"></i>
          <span>目录导航</span>
        </div>
        <nav class="sidebar-nav">
          <a v-for="(section, idx) in sections" :key="section.id"
             :class="['nav-item', { active: currentSection === idx }]"
             @click="currentSection = idx">
            <i :class="section.icon"></i>
            <span>{{ section.title }}</span>
          </a>
        </nav>
        <div class="sidebar-footer">
          <span class="progress-text">{{ currentSection + 1 }} / {{ sections.length }}</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: ((currentSection + 1) / sections.length * 100) + '%' }"></div>
          </div>
        </div>
      </aside>

      <!-- 移动端目录切换按钮 -->
      <button class="mobile-nav-toggle" @click="mobileNavOpen = !mobileNavOpen">
        <i class="bi bi-list"></i>
      </button>

      <!-- 移动端目录抽屉 -->
      <Transition name="drawer">
        <div v-if="mobileNavOpen" class="mobile-nav-overlay" @click="mobileNavOpen = false">
          <div class="mobile-nav-drawer" @click.stop>
            <div class="drawer-header">
              <span><i class="bi bi-book"></i> 目录导航</span>
              <button @click="mobileNavOpen = false"><i class="bi bi-x-lg"></i></button>
            </div>
            <nav class="drawer-nav">
              <a v-for="(section, idx) in sections" :key="section.id"
                 :class="['nav-item', { active: currentSection === idx }]"
                 @click="currentSection = idx; mobileNavOpen = false">
                <i :class="section.icon"></i>
                <span>{{ section.title }}</span>
              </a>
            </nav>
          </div>
        </div>
      </Transition>

      <!-- 右侧内容区 -->
      <main class="about-content">
        <!-- 内容头部：标题+翻页 -->
        <div class="content-header">
          <div class="header-title">
            <span class="section-badge"><i :class="sections[currentSection].icon"></i> {{ sections[currentSection].badge }}</span>
            <h1>{{ sections[currentSection].title }}</h1>
          </div>
          <div class="header-nav">
            <button class="nav-btn" @click="prevSection" :disabled="currentSection === 0">
              <i class="bi bi-chevron-left"></i> 上一节
            </button>
            <button class="nav-btn" @click="nextSection" :disabled="currentSection === sections.length - 1">
              下一节 <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="content-body">
          
          <!-- 0. 项目介绍 -->
          <div v-show="currentSection === 0" class="content-pane">
            <div class="intro-hero">
              <div class="hero-bg-mini">
                <div class="hero-circle c1"></div>
                <div class="hero-circle c2"></div>
              </div>
              <div class="intro-content">
                <span class="intro-badge">中国大学生服务外包创新创业大赛 · A13</span>
                <h2 class="intro-title">律途 · Luvoy<br><span class="gradient-text">Life's Unique Voyage</span></h2>
                <p class="intro-desc">
                  融合多智能体架构与大语言模型技术，为大学生提供从岗位认知、能力评估到个性化职业导航的全链路智能服务。
                </p>
                <div class="intro-tags">
                  <span v-for="t in heroTags" :key="t" class="intro-tag">{{ t }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 1. 八大核心功能 -->
          <div v-show="currentSection === 1" class="content-pane">
            <p class="pane-desc">覆盖从岗位认知到职业规划的完整闭环（点击查看详情）</p>
            <div class="features-grid">
              <div v-for="(f, i) in features" :key="f.title" class="feature-item clickable"
                   @click="showFeatureDetail(f)">
                <div class="feature-num">{{ String(i + 1).padStart(2, '0') }}</div>
                <div class="feature-body">
                  <div class="feature-icon"><i :class="f.icon"></i></div>
                  <h6>{{ f.title }} <i class="bi bi-arrow-right-circle ms-1 detail-arrow"></i></h6>
                  <p>{{ f.desc }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. 核心技术 -->
          <div v-show="currentSection === 2" class="content-pane">
            <div class="tech-grid-compact">
              <div v-for="tech in techs" :key="tech.title" class="tech-card-compact">
                <div class="tech-icon-sm" :style="{ background: tech.gradient }">
                  <i :class="tech.icon"></i>
                </div>
                <div class="tech-info">
                  <h6>{{ tech.title }}</h6>
                  <p>{{ tech.desc }}</p>
                  <div class="tech-tags-sm">
                    <span v-for="tag in tech.tags" :key="tag">{{ tag }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. 系统架构 -->
          <div v-show="currentSection === 3" class="content-pane">
            <div class="arch-diagram-compact">
              <div class="arch-row">
                <div class="arch-layer-compact layer-frontend">
                  <div class="layer-head"><i class="bi bi-window"></i> 展示层</div>
                  <div class="layer-nodes">
                    <span>Vue 3 SPA</span><span>ECharts</span><span>响应式UI</span>
                  </div>
                </div>
                <div class="arch-connector"><i class="bi bi-arrow-right"></i></div>
                <div class="arch-layer-compact layer-backend">
                  <div class="layer-head"><i class="bi bi-server"></i> 服务层</div>
                  <div class="layer-nodes">
                    <span>Flask API</span><span>SQLAlchemy</span><span>Gunicorn</span>
                  </div>
                </div>
              </div>
              <div class="arch-row-center">
                <i class="bi bi-arrow-down"></i> RESTful API · Nginx
              </div>
              <div class="arch-row">
                <div class="arch-layer-compact layer-ai">
                  <div class="layer-head"><i class="bi bi-robot"></i> AI Agent层</div>
                  <div class="layer-agents">
                    <div class="agent-mini"><i class="bi bi-cpu"></i> 岗位分析</div>
                    <div class="agent-mini"><i class="bi bi-file-person"></i> 简历解析</div>
                    <div class="agent-mini"><i class="bi bi-link"></i> 匹配引擎</div>
                    <div class="agent-mini"><i class="bi bi-journal"></i> 报告生成</div>
                  </div>
                </div>
                <div class="arch-connector"><i class="bi bi-arrow-right"></i></div>
                <div class="arch-layer-compact layer-llm">
                  <div class="layer-head"><i class="bi bi-stars"></i> 模型层</div>
                  <div class="layer-nodes">
                    <span>DeepSeek</span><span>通义千问</span><span>智谱AI</span><span>Moonshot</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 4. 技术指标 -->
          <div v-show="currentSection === 4" class="content-pane">
            <div class="stats-grid-compact">
              <div v-for="s in stats" :key="s.label" class="stat-card">
                <div class="stat-num" :style="{ color: s.color }">{{ s.value }}</div>
                <div class="stat-info">
                  <strong>{{ s.label }}</strong>
                  <span>{{ s.desc }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 5. 技术栈 -->
          <div v-show="currentSection === 5" class="content-pane">
            <div class="stack-grid">
              <div v-for="row in stackRows" :key="row.layer" class="stack-card">
                <div class="stack-head" :style="{ background: row.gradient }">
                  <i :class="row.icon"></i> {{ row.layer }}
                </div>
                <div class="stack-body">
                  <span v-for="t in row.techs" :key="t" class="stack-item">{{ t }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 6. 项目信息 -->
          <div v-show="currentSection === 6" class="content-pane">
            <div class="info-cards">
              <div class="info-card">
                <i class="bi bi-trophy"></i>
                <h5>赛题信息</h5>
                <p>中国大学生服务外包创新创业大赛</p>
                <span class="badge badge-soft-primary">A13 · 基于AI的大学生职业规划智能体</span>
              </div>
              <div class="info-card">
                <i class="bi bi-code-square"></i>
                <h5>开源协议</h5>
                <p>MIT License</p>
                <span class="badge badge-soft-success">代码完全开源</span>
              </div>
              <div class="info-card">
                <i class="bi bi-box-seam"></i>
                <h5>部署方式</h5>
                <p>Docker Compose 一键部署</p>
                <span class="badge badge-soft-info">容器化 · 高可用</span>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>

    <!-- 功能详情模态框 -->
    <Teleport to="body">
      <div v-if="showModal" class="detail-modal-overlay" @click.self="closeModal">
        <div class="detail-modal anim-fade-in-up">
          <button class="modal-close" @click="closeModal"><i class="bi bi-x-lg"></i></button>
          <div class="modal-header">
            <div class="modal-icon" :style="{ background: currentFeature.gradient || 'linear-gradient(135deg, #0EA5E9, #06B6D4)' }">
              <i :class="currentFeature.icon"></i>
            </div>
            <h3>{{ currentFeature.title }}</h3>
            <p class="modal-subtitle">{{ currentFeature.desc }}</p>
          </div>
          <div class="modal-body">
            <div class="detail-section" v-for="(section, idx) in currentFeature.details" :key="idx">
              <h5><i :class="section.icon"></i> {{ section.title }}</h5>
              <p v-html="section.content"></p>
              <ul v-if="section.list">
                <li v-for="(item, i) in section.list" :key="i">
                  <strong v-if="item.label">{{ item.label }}：</strong>{{ item.text }}
                </li>
              </ul>
            </div>
            <div class="detail-tags" v-if="currentFeature.tags">
              <span v-for="tag in currentFeature.tags" :key="tag" class="detail-tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const heroTags = ['多Agent架构', '大语言模型', '智能匹配', '个性化规划', 'Docker部署', '响应式设计']

// 模态框状态
const showModal = ref(false)
const currentFeature = ref({})

// 导航状态
const currentSection = ref(0)
const mobileNavOpen = ref(false)

const sections = [
  { id: 'intro', title: '项目介绍', badge: 'Introduction', icon: 'bi bi-info-circle' },
  { id: 'features', title: '八大核心功能', badge: 'Features', icon: 'bi bi-grid' },
  { id: 'tech', title: '核心技术亮点', badge: 'Technology', icon: 'bi bi-cpu' },
  { id: 'arch', title: '系统架构设计', badge: 'Architecture', icon: 'bi bi-diagram-3' },
  { id: 'stats', title: '技术指标', badge: 'Metrics', icon: 'bi bi-speedometer2' },
  { id: 'stack', title: '完整技术栈', badge: 'Tech Stack', icon: 'bi bi-stack' },
  { id: 'info', title: '项目信息', badge: 'Project', icon: 'bi bi-trophy' }
]

const prevSection = () => {
  if (currentSection.value > 0) {
    currentSection.value--
  }
}

const nextSection = () => {
  if (currentSection.value < sections.length - 1) {
    currentSection.value++
  }
}

const showFeatureDetail = (feature) => {
  currentFeature.value = feature
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  document.body.style.overflow = ''
}

const techs = [
  {
    title: '多Agent智能协同',
    icon: 'bi bi-robot',
    gradient: 'linear-gradient(135deg, #0EA5E9, #06B6D4)',
    desc: '四大AI Agent各司其职——岗位分析、简历解析、人岗匹配、报告生成，通过Prompt工程实现多Agent协同推理。',
    tags: ['Agent编排', 'Prompt Engineering', 'JSON Schema'],
  },
  {
    title: 'LLM统一接入层',
    icon: 'bi bi-plug',
    gradient: 'linear-gradient(135deg, #10B981, #059669)',
    desc: '基于OpenAI兼容协议封装统一LLM客户端，运行时一键切换DeepSeek、通义千问、智谱AI等国产大模型。',
    tags: ['OpenAI Compatible', '模型热切换', '容错降级'],
  },
  {
    title: '四维人岗匹配算法',
    icon: 'bi bi-link-45deg',
    gradient: 'linear-gradient(135deg, #F59E0B, #D97706)',
    desc: '从基础条件、技能匹配、综合素质、发展潜力四个维度构建加权匹配模型，结合AI语义理解进行深度分析。',
    tags: ['加权评分', '语义匹配', '雷达图可视化'],
  },
  {
    title: '智能简历解析',
    icon: 'bi bi-file-earmark-text',
    gradient: 'linear-gradient(135deg, #EF4444, #DC2626)',
    desc: '支持PDF/DOCX格式简历上传，AI自动提取个人信息、教育背景、技能特长、项目经验等结构化数据。',
    tags: ['PDF解析', 'DOCX解析', 'NER提取'],
  },
  {
    title: '职业图谱引擎',
    icon: 'bi bi-diagram-3',
    gradient: 'linear-gradient(135deg, #8B5CF6, #6D28D9)',
    desc: '利用LLM自动构建岗位间的晋升路径与转岗关系，形成可交互的职业发展知识图谱。',
    tags: ['知识图谱', 'ECharts Graph', '路径推荐'],
  },
  {
    title: '容器化工程实践',
    icon: 'bi bi-box-seam',
    gradient: 'linear-gradient(135deg, #06B6D4, #0891B2)',
    desc: 'Docker Compose编排前后端服务，Nginx反向代理、Gunicorn多Worker、Volume数据持久化，一键生产部署。',
    tags: ['Docker', 'Nginx', 'Gunicorn', 'CI/CD'],
  },
]

const features = [
  { 
    icon: 'bi bi-database', 
    title: '岗位数据管理', 
    desc: '9000+真实岗位数据导入，支持分页搜索、行业筛选、薪资浏览',
    gradient: 'linear-gradient(135deg, #0EA5E9, #06B6D4)',
    tags: ['数据导入', '分页搜索', '多维筛选', 'RESTful API'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '岗位数据管理模块是整个系统的数据基础层，负责管理来自真实招聘平台的海量岗位信息。系统支持批量导入JSON格式的岗位数据，并提供高效的检索和筛选功能。'
      },
      {
        icon: 'bi bi-list-check',
        title: '核心功能',
        list: [
          { label: '批量导入', text: '支持JSON格式岗位数据批量导入，单次可处理上万条记录' },
          { label: '智能搜索', text: '支持岗位名称、公司名称、地址等多字段模糊搜索' },
          { label: '多维筛选', text: '按行业类别、薪资范围、公司规模等维度筛选' },
          { label: '分页浏览', text: '高性能分页加载，支持自定义每页显示数量' }
        ]
      },
      {
        icon: 'bi bi-gear',
        title: '技术实现',
        content: '基于<strong>Flask-SQLAlchemy</strong>实现ORM映射，使用<strong>SQLite</strong>作为轻量级数据库。后端提供RESTful API接口，前端通过Axios进行异步数据请求，实现流畅的用户交互体验。'
      }
    ]
  },
  { 
    icon: 'bi bi-cpu', 
    title: 'AI岗位画像', 
    desc: '大模型自动分析岗位关键技能、能力要求、权重分配',
    gradient: 'linear-gradient(135deg, #10B981, #059669)',
    tags: ['LLM分析', '结构化提取', '能力模型', 'JSON Schema'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: 'AI岗位画像模块利用大语言模型（LLM）对原始岗位描述进行深度分析，自动提取结构化的岗位能力要求，生成标准化的岗位画像数据。'
      },
      {
        icon: 'bi bi-list-check',
        title: '提取维度',
        list: [
          { label: '技术技能', text: '编程语言、框架、工具等硬性技能要求' },
          { label: '软技能评分', text: '创新能力、学习能力、抗压能力、沟通能力、团队协作、实践能力（1-10分）' },
          { label: '基础要求', text: '学历要求、工作经验、证书要求等' },
          { label: '权重分配', text: '基础要求、技能匹配、综合素质、发展潜力四个维度的权重' }
        ]
      },
      {
        icon: 'bi bi-robot',
        title: 'Agent工作流程',
        content: '① 接收原始岗位数据 → ② 构建分析Prompt → ③ 调用LLM进行推理 → ④ 解析JSON响应 → ⑤ 校验并存储结构化画像。整个过程自动化完成，单个岗位分析约需10-15秒。'
      }
    ]
  },
  { 
    icon: 'bi bi-diagram-3', 
    title: '职业发展图谱', 
    desc: 'AI构建岗位晋升路径与转岗关系可视化',
    gradient: 'linear-gradient(135deg, #8B5CF6, #6D28D9)',
    tags: ['知识图谱', 'ECharts', '路径规划', 'AI生成'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '职业发展图谱模块利用AI自动分析岗位之间的关联关系，构建包含晋升路径和横向转岗路径的职业发展知识图谱，帮助学生了解职业发展方向。'
      },
      {
        icon: 'bi bi-list-check',
        title: '图谱类型',
        list: [
          { label: '垂直晋升', text: '如：初级开发 → 中级开发 → 高级开发 → 技术专家/架构师' },
          { label: '横向转岗', text: '如：后端开发 ↔ 全栈开发 ↔ 技术管理' },
          { label: '跨领域发展', text: '如：开发工程师 → 产品经理 → 创业CEO' }
        ]
      },
      {
        icon: 'bi bi-bar-chart',
        title: '可视化展示',
        content: '采用<strong>ECharts Graph</strong>图表进行可视化展示，支持节点拖拽、缩放、点击查看详情等交互操作。每条路径包含所需技能补充、转换难度、预计年限等信息。'
      }
    ]
  },
  { 
    icon: 'bi bi-person-plus', 
    title: '学生信息管理', 
    desc: '手动录入或PDF/DOCX简历上传，自动解析',
    gradient: 'linear-gradient(135deg, #EF4444, #DC2626)',
    tags: ['简历上传', '自动解析', 'PDF/DOCX', 'NER提取'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '学生信息管理模块支持两种数据录入方式：手动填写表单或上传简历文件。系统可自动解析PDF/DOCX格式的简历，提取关键信息填充到学生档案中。'
      },
      {
        icon: 'bi bi-list-check',
        title: '信息字段',
        list: [
          { label: '基本信息', text: '姓名、性别、年龄、联系方式、所在城市' },
          { label: '教育背景', text: '学校、专业、学历、GPA、在校时间' },
          { label: '技能特长', text: '编程语言、框架工具、证书资质' },
          { label: '项目经验', text: '项目名称、角色、技术栈、成果描述' },
          { label: '实习经历', text: '公司、岗位、工作内容、时间段' }
        ]
      },
      {
        icon: 'bi bi-file-earmark-text',
        title: '简历解析技术',
        content: '使用<strong>PyPDF2</strong>和<strong>python-docx</strong>库提取文档文本，然后通过<strong>LLM</strong>进行智能语义解析，自动识别并提取结构化信息，准确率高达90%以上。'
      }
    ]
  },
  { 
    icon: 'bi bi-radar', 
    title: 'AI学生画像', 
    desc: '六维能力雷达图：创新、学习、抗压、沟通、协作、实践',
    gradient: 'linear-gradient(135deg, #F59E0B, #D97706)',
    tags: ['能力评估', '雷达图', 'AI分析', '六维模型'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: 'AI学生画像模块基于学生档案信息，利用大语言模型进行综合能力评估，生成六维能力雷达图，直观展示学生的能力分布情况。'
      },
      {
        icon: 'bi bi-list-check',
        title: '六维能力模型',
        list: [
          { label: '创新能力', text: '评估学生的创造性思维、问题解决能力、创新项目经历' },
          { label: '学习能力', text: '评估学习速度、知识吸收能力、自主学习习惯' },
          { label: '抗压能力', text: '评估面对压力和挑战时的心理素质和应对能力' },
          { label: '沟通能力', text: '评估表达能力、倾听能力、跨部门协作沟通能力' },
          { label: '团队协作', text: '评估团队合作精神、领导力、冲突处理能力' },
          { label: '实践能力', text: '评估动手能力、项目实战经验、实习表现' }
        ]
      },
      {
        icon: 'bi bi-bar-chart',
        title: '可视化展示',
        content: '使用<strong>ECharts Radar</strong>图表绘制六维雷达图，每个维度评分范围1-10分。同时生成文字版能力总结，为后续人岗匹配提供数据支撑。'
      }
    ]
  },
  { 
    icon: 'bi bi-link-45deg', 
    title: '人岗智能匹配', 
    desc: '基础/技能/素质/潜力四维加权匹配+仪表盘可视化',
    gradient: 'linear-gradient(135deg, #06B6D4, #0891B2)',
    tags: ['四维匹配', '加权算法', '仪表盘', 'AI推荐'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '人岗智能匹配模块是系统的核心功能，将学生画像与岗位画像进行多维度对比分析，计算匹配度评分，并给出详细的匹配分析报告。'
      },
      {
        icon: 'bi bi-list-check',
        title: '四维匹配模型',
        list: [
          { label: '基础条件', text: '学历、专业、工作经验等硬性条件匹配（权重约20%）' },
          { label: '技能匹配', text: '技术栈、工具、证书等专业技能匹配（权重约35%）' },
          { label: '综合素质', text: '软技能六维度与岗位要求的吻合程度（权重约25%）' },
          { label: '发展潜力', text: '学习能力、成长空间、职业规划契合度（权重约20%）' }
        ]
      },
      {
        icon: 'bi bi-speedometer2',
        title: '可视化展示',
        content: '使用<strong>ECharts Gauge</strong>仪表盘展示总体匹配度，配合四维度柱状图、差距分析表格、AI建议等，全方位展示匹配结果。支持一键选择多个岗位进行批量匹配比较。'
      }
    ]
  },
  { 
    icon: 'bi bi-journal-text', 
    title: '职业规划报告', 
    desc: 'AI生成六章定制化报告，支持在线编辑、AI润色、多格式导出',
    gradient: 'linear-gradient(135deg, #EC4899, #DB2777)',
    tags: ['AI生成', '在线编辑', 'Markdown', '多格式导出'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '职业规划报告模块根据学生画像和匹配结果，利用AI自动生成个性化的职业规划报告，包含六个章节的详细内容，支持在线编辑和多格式导出。'
      },
      {
        icon: 'bi bi-list-check',
        title: '报告六章结构',
        list: [
          { label: '第一章', text: '个人能力分析 - 基于六维模型的能力评估与解读' },
          { label: '第二章', text: '职业兴趣探索 - 性格特点与职业倾向分析' },
          { label: '第三章', text: '目标岗位分析 - 匹配岗位的详细要求解读' },
          { label: '第四章', text: '差距分析 - 当前能力与目标要求的差距识别' },
          { label: '第五章', text: '提升计划 - 针对性的能力提升建议与资源推荐' },
          { label: '第六章', text: '行动路线图 - 分阶段的职业发展行动计划' }
        ]
      },
      {
        icon: 'bi bi-pencil-square',
        title: '编辑与导出',
        content: '支持<strong>Markdown</strong>格式在线编辑，可逐章节AI润色优化。导出格式包括：HTML网页版（可打印PDF）、Markdown源文件。所有报告自动保存，可随时查看历史版本。'
      }
    ]
  },
  { 
    icon: 'bi bi-gear', 
    title: '灵活模型配置', 
    desc: '运行时切换DeepSeek/通义千问/智谱/Moonshot等LLM',
    gradient: 'linear-gradient(135deg, #6366F1, #4F46E5)',
    tags: ['模型切换', 'OpenAI兼容', '参数调节', '热更新'],
    details: [
      {
        icon: 'bi bi-info-circle',
        title: '功能概述',
        content: '系统设计了统一的LLM接入层，基于OpenAI兼容协议，支持在运行时动态切换不同的大语言模型，无需重启服务即可生效。'
      },
      {
        icon: 'bi bi-list-check',
        title: '支持的模型',
        list: [
          { label: 'DeepSeek', text: '国产高性价比大模型，推理能力强，价格实惠' },
          { label: '通义千问', text: '阿里云大模型，中文理解能力出色' },
          { label: '智谱AI', text: 'GLM系列模型，GLM-4-Flash完全免费' },
          { label: 'Moonshot', text: 'Kimi大模型，长文本处理能力强' },
          { label: 'OpenAI', text: '支持GPT-4o-mini等模型（需科学上网）' }
        ]
      },
      {
        icon: 'bi bi-sliders',
        title: '可配置参数',
        content: '可在设置页面配置：<strong>API Key</strong>（密钥）、<strong>Base URL</strong>（接口地址）、<strong>Model</strong>（模型名称）、<strong>Temperature</strong>（创造性参数）、<strong>Max Tokens</strong>（最大输出长度）。修改后立即生效，无需重启。'
      }
    ]
  },
]

const stats = [
  { value: '9,178', label: '岗位数据', desc: '真实招聘岗位', color: '#4F46E5' },
  { value: '25+', label: 'API接口', desc: 'RESTful设计', color: '#10B981' },
  { value: '4', label: 'AI Agent', desc: '多智能体协同', color: '#F59E0B' },
  { value: '6', label: '能力维度', desc: '雷达图评估', color: '#EF4444' },
  { value: '12', label: '前端页面', desc: '响应式设计', color: '#8B5CF6' },
  { value: '4', label: 'LLM支持', desc: '模型热切换', color: '#06B6D4' },
]

const stackRows = [
  { layer: '前端', icon: 'bi bi-window', gradient: 'linear-gradient(135deg, #4F46E5, #7C3AED)', techs: ['Vue 3.5', 'Vue Router 4', 'Vite 6', 'Bootstrap 5', 'ECharts 5', 'Axios', 'Marked'] },
  { layer: '后端', icon: 'bi bi-server', gradient: 'linear-gradient(135deg, #10B981, #059669)', techs: ['Python 3.11', 'Flask 3.1', 'SQLAlchemy', 'SQLite', 'Gunicorn', 'Flask-CORS'] },
  { layer: 'AI', icon: 'bi bi-robot', gradient: 'linear-gradient(135deg, #F59E0B, #D97706)', techs: ['OpenAI SDK', 'Prompt Engineering', 'JSON Schema', 'Multi-Agent'] },
  { layer: '部署', icon: 'bi bi-cloud', gradient: 'linear-gradient(135deg, #06B6D4, #0891B2)', techs: ['Docker', 'Docker Compose', 'Nginx', 'Alpine Linux'] },
  { layer: '工具', icon: 'bi bi-tools', gradient: 'linear-gradient(135deg, #8B5CF6, #6D28D9)', techs: ['PyPDF2', 'python-docx', 'Markdown', 'pandas', 'python-dotenv'] },
]
</script>

<style scoped>
/* ===== About Layout ===== */
.about-page {
  min-height: calc(100vh - 80px);
}

.about-layout {
  display: flex;
  gap: 0;
  min-height: calc(100vh - 100px);
}

/* ===== Left Sidebar ===== */
.about-sidebar {
  width: 260px;
  flex-shrink: 0;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 80px;
  height: fit-content;
  max-height: calc(100vh - 100px);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.sidebar-header i {
  font-size: 1.25rem;
  color: var(--primary);
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sidebar-nav .nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.sidebar-nav .nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.sidebar-nav .nav-item.active {
  background: var(--primary);
  color: #fff;
}

.sidebar-nav .nav-item i {
  font-size: 1.1rem;
  width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 1rem;
}

.progress-text {
  font-size: 0.78rem;
  color: var(--text-muted);
  display: block;
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 4px;
  background: var(--bg-hover);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary-gradient);
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* ===== Mobile Nav Toggle ===== */
.mobile-nav-toggle {
  display: none;
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
  z-index: 1000;
  transition: all 0.2s ease;
}

.mobile-nav-toggle:hover {
  transform: scale(1.05);
}

/* ===== Mobile Drawer ===== */
.mobile-nav-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 2000;
}

.mobile-nav-drawer {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 280px;
  max-width: 85vw;
  background: var(--bg-card);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  border-bottom: 1px solid var(--border);
}

.drawer-header span {
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.drawer-header button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--bg-hover);
  color: var(--text-secondary);
  cursor: pointer;
}

.drawer-nav {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  overflow-y: auto;
}

.drawer-nav .nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.drawer-nav .nav-item:hover {
  background: var(--bg-hover);
}

.drawer-nav .nav-item.active {
  background: var(--primary);
  color: #fff;
}

/* Drawer transition */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.25s ease;
}

.drawer-enter-active .mobile-nav-drawer,
.drawer-leave-active .mobile-nav-drawer {
  transition: transform 0.25s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from .mobile-nav-drawer,
.drawer-leave-to .mobile-nav-drawer {
  transform: translateX(-100%);
}

/* ===== Right Content ===== */
.about-content {
  flex: 1;
  min-width: 0;
  margin-left: 1.5rem;
  display: flex;
  flex-direction: column;
}

.content-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  margin-bottom: 1rem;
}

.header-title h1 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0.375rem 0 0;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: var(--bg-hover);
  color: var(--primary);
  font-weight: 600;
  font-size: 0.75rem;
  padding: 0.2rem 0.75rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.content-body {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
}

.content-pane {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.pane-desc {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 1.25rem;
}

/* ===== Intro Pane (项目介绍) ===== */
.intro-hero {
  position: relative;
  padding: 3rem 2rem;
  text-align: center;
  overflow: hidden;
  border-radius: 16px;
  background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
  color: #fff;
}

.hero-bg-mini {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.hero-bg-mini .hero-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  animation: float 8s ease-in-out infinite;
}

.hero-bg-mini .c1 { width: 300px; height: 300px; background: #818CF8; top: -80px; right: -60px; }
.hero-bg-mini .c2 { width: 200px; height: 200px; background: #A78BFA; bottom: -60px; left: -40px; animation-delay: -3s; }

.intro-content {
  position: relative;
  z-index: 1;
  max-width: 650px;
  margin: 0 auto;
}

.intro-badge {
  display: inline-block;
  background: rgba(255,255,255,.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 9999px;
  padding: 0.375rem 1.25rem;
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.intro-title {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.gradient-text {
  background: linear-gradient(135deg, #A78BFA, #38BDF8, #34D399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.intro-desc {
  font-size: 1rem;
  line-height: 1.7;
  opacity: 0.85;
  max-width: 550px;
  margin: 0 auto 1.25rem;
}

.intro-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.intro-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.15);
  font-size: 0.78rem;
  font-weight: 500;
}

/* ===== Pane Subtitle ===== */
.pane-subtitle {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 1.25rem;
}

/* ===== Sections ===== */
.about-section { margin-bottom: 2rem; }
.section-header { text-align: center; margin-bottom: 2rem; }
.section-header h2 { font-size: 1.75rem; font-weight: 800; margin: 0.5rem 0 0.25rem; }
.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: var(--bg-hover);
  color: var(--primary);
  font-weight: 600;
  font-size: 0.8rem;
  padding: 0.25rem 0.875rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Tech Grid Compact */
.tech-grid-compact {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1rem;
}

.tech-card-compact {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-hover);
  border-radius: 12px;
  border: 1px solid var(--border);
}

.tech-icon-sm {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.tech-info h6 {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.tech-info p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.tech-tags-sm {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tech-tags-sm span {
  padding: 0.15rem 0.5rem;
  font-size: 0.68rem;
  font-weight: 600;
  border-radius: 5px;
  background: var(--bg-card);
  color: var(--text-muted);
}

/* Architecture Compact */
.arch-diagram-compact {
  max-width: 100%;
}

.arch-row {
  display: flex;
  gap: 1rem;
  align-items: stretch;
  margin-bottom: 0.5rem;
}

.arch-row-center {
  text-align: center;
  padding: 0.5rem;
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 500;
}

.arch-connector {
  display: flex;
  align-items: center;
  color: var(--text-muted);
  font-size: 1.25rem;
}

.arch-layer-compact {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid;
}

.arch-layer-compact.layer-frontend { border-color: rgba(79,70,229,.2); }
.arch-layer-compact.layer-backend { border-color: rgba(16,185,129,.2); }
.arch-layer-compact.layer-ai { border-color: rgba(245,158,11,.2); }
.arch-layer-compact.layer-llm { border-color: rgba(139,92,246,.2); }

.layer-head {
  padding: 0.625rem 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.layer-frontend .layer-head { background: rgba(79,70,229,.1); color: #4F46E5; }
.layer-backend .layer-head { background: rgba(16,185,129,.1); color: #059669; }
.layer-ai .layer-head { background: rgba(245,158,11,.1); color: #D97706; }
.layer-llm .layer-head { background: rgba(139,92,246,.1); color: #7C3AED; }

.layer-nodes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  padding: 0.75rem;
  background: var(--bg-card);
}

.layer-nodes span {
  padding: 0.25rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
  background: var(--bg-hover);
  color: var(--text-secondary);
}

.layer-agents {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  padding: 0.75rem;
  background: var(--bg-card);
}

.agent-mini {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(245,158,11,.08);
  border-radius: 8px;
  color: #D97706;
}

.agent-mini i {
  font-size: 0.9rem;
}

/* Stats Compact */
.stats-grid-compact {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #1E1B4B, #312E81);
  border-radius: 12px;
}

.stat-num {
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1;
  color: #fff;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-info strong {
  font-size: 0.85rem;
  color: #E2E8F0;
}

.stat-info span {
  font-size: 0.72rem;
  color: rgba(255,255,255,.6);
}

/* Stack Grid */
.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.stack-card {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-card);
}

.stack-head {
  padding: 0.625rem 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stack-body {
  padding: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.stack-item {
  padding: 0.2rem 0.5rem;
  font-size: 0.72rem;
  font-weight: 600;
  border-radius: 5px;
  background: var(--bg-hover);
  color: var(--text-secondary);
}

/* ===== Tech Grid ===== */
.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}
.tech-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.75rem;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.tech-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.tech-icon {
  width: 48px; height: 48px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
.tech-card h5 { font-weight: 700; margin-bottom: 0.5rem; }
.tech-card p { color: var(--text-secondary); font-size: 0.88rem; line-height: 1.6; margin-bottom: 0.75rem; }
.tech-tags { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.tech-tags span {
  padding: 0.2rem 0.6rem;
  font-size: 0.72rem;
  font-weight: 600;
  border-radius: 6px;
  background: var(--bg-hover);
  color: var(--text-muted);
}

/* ===== Architecture ===== */
.arch-section { }
.arch-diagram {
  max-width: 860px;
  margin: 0 auto;
}
.arch-layer { margin-bottom: 0.25rem; }
.layer-label {
  font-size: 0.72rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--text-muted); margin-bottom: 0.5rem;
  padding-left: 0.25rem;
}
.layer-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 0.5rem;
}
.arch-node {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex; align-items: center; gap: 0.5rem;
  border: 1px solid;
}
.layer-frontend .arch-node { background: rgba(79,70,229,.06); border-color: rgba(79,70,229,.15); color: #4F46E5; }
.layer-backend .arch-node { background: rgba(16,185,129,.06); border-color: rgba(16,185,129,.15); color: #059669; }
.layer-ai .arch-node { background: rgba(245,158,11,.06); border-color: rgba(245,158,11,.15); color: #D97706; }
.layer-llm .arch-node { background: rgba(139,92,246,.06); border-color: rgba(139,92,246,.15); color: #7C3AED; }

.agent-node {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.125rem;
  padding: 1rem;
}
.agent-node i { font-size: 1.25rem; margin-bottom: 0.25rem; }
.agent-node span { font-weight: 700; }
.agent-node small { font-size: 0.72rem; font-weight: 400; opacity: 0.7; }

.arch-arrow {
  text-align: center;
  padding: 0.625rem 0;
  color: var(--text-muted);
  font-size: 0.78rem;
  font-weight: 500;
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
}
.arch-arrow i { font-size: 1rem; }

/* ===== Features ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.feature-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  transition: border-color 0.2s ease;
}
.feature-item:hover { border-color: var(--primary-light); }
.feature-num {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--primary);
  opacity: 0.2;
  line-height: 1;
  flex-shrink: 0;
}
.feature-icon { color: var(--primary); font-size: 1.25rem; margin-bottom: 0.375rem; }
.feature-body h6 { font-weight: 700; margin-bottom: 0.25rem; }
.feature-body p { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; margin: 0; }

/* ===== Stats ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}
.stat-item {
  text-align: center;
  padding: 1.25rem 0.5rem;
  border-radius: 14px;
  background: var(--bg-hover);
  border: 1px solid var(--border);
}
.stat-value { font-size: 1.75rem; font-weight: 800; line-height: 1; }
.stat-label { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-top: 0.5rem; }
.stat-desc { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.125rem; }

/* ===== Stack Table ===== */
.stack-table { max-width: 800px; margin: 0 auto; }
.stack-row {
  display: flex;
  align-items: stretch;
  margin-bottom: 0.75rem;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-card);
}
.stack-layer {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  color: #fff; font-weight: 700; font-size: 0.85rem;
  min-width: 100px;
  flex-shrink: 0;
}
.stack-techs {
  display: flex; flex-wrap: wrap; gap: 0.375rem;
  padding: 0.75rem 1rem;
  align-items: center;
}
.stack-tech {
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  background: var(--bg-hover);
  color: var(--text-secondary);
}

/* ===== Project Info ===== */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.25rem;
}
.info-card {
  text-align: center;
  padding: 2rem 1.5rem;
  border-radius: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  transition: transform 0.2s ease;
}
.info-card:hover { transform: translateY(-2px); }
.info-card i { font-size: 2rem; color: var(--primary); margin-bottom: 0.75rem; display: block; }
.info-card h5 { font-weight: 700; margin-bottom: 0.375rem; }
.info-card p { font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 0.75rem; }

/* ===== Responsive ===== */
@media (max-width: 992px) {
  .about-sidebar {
    display: none;
  }
  
  .mobile-nav-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .mobile-nav-overlay {
    display: block;
  }
  
  .about-content {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .intro-hero {
    padding: 2rem 1rem;
  }
  
  .intro-title {
    font-size: 1.5rem;
  }
  
  .intro-desc {
    font-size: 0.88rem;
  }
  
  .intro-tags {
    gap: 0.375rem;
  }
  
  .intro-tag {
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
  }
  
  .features-grid { grid-template-columns: 1fr; }
  .tech-grid { grid-template-columns: 1fr; }
  .layer-content { grid-template-columns: repeat(2, 1fr); }
  .stats-grid { grid-template-columns: repeat(3, 1fr); }
  .stats-section { padding: 2rem 1rem; margin-left: -0.5rem; margin-right: -0.5rem; }
  .stack-row { flex-direction: column; }
  .stack-layer { min-width: auto; padding: 0.625rem 1rem; }
  .tech-grid-compact { grid-template-columns: 1fr; }
  .arch-row { flex-direction: column; gap: 0.5rem; }
  .arch-connector { 
    justify-content: center; 
    transform: rotate(90deg); 
    padding: 0.5rem; 
  }
  .stats-grid-compact { grid-template-columns: repeat(2, 1fr); }
  .stack-grid { grid-template-columns: 1fr; }
  .layer-agents { grid-template-columns: 1fr; }
  .info-cards { grid-template-columns: 1fr; }
  
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .header-nav {
    width: 100%;
    justify-content: space-between;
  }
  
  .nav-btn {
    flex: 1;
    justify-content: center;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(3deg); }
}

/* ===== Detail Modal ===== */
.detail-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.detail-modal {
  background: var(--bg-card);
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  z-index: 10000;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--bg-hover);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10;
}
.modal-close:hover {
  background: var(--primary);
  color: #fff;
}

.modal-header {
  padding: 2rem 2rem 1.5rem;
  text-align: center;
  border-bottom: 1px solid var(--border);
}

.modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #fff;
  margin: 0 auto 1rem;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin: 0;
}

.modal-body {
  padding: 1.5rem 2rem 2rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section:last-of-type {
  margin-bottom: 1rem;
}

.detail-section h5 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-section h5 i {
  font-size: 1.1rem;
}

.detail-section p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.7;
  margin: 0;
}

.detail-section ul {
  list-style: none;
  padding: 0;
  margin: 0.75rem 0 0;
}

.detail-section li {
  position: relative;
  padding: 0.5rem 0 0.5rem 1.25rem;
  font-size: 0.88rem;
  color: var(--text-secondary);
  border-left: 2px solid var(--primary-light);
  margin-bottom: 0.25rem;
}

.detail-section li::before {
  content: '';
  position: absolute;
  left: -5px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background: var(--primary);
  border-radius: 50%;
}

.detail-section li strong {
  color: var(--text-primary);
  font-weight: 600;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.detail-tag {
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  background: var(--bg-hover);
  color: var(--primary);
  border: 1px solid var(--primary-light);
}

/* Clickable feature item */
.feature-item.clickable {
  cursor: pointer;
}

.feature-item.clickable:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}

.detail-arrow {
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  font-size: 0.9rem;
}

.feature-item.clickable:hover .detail-arrow {
  opacity: 1;
  transform: translateX(3px);
}

@media (max-width: 768px) {
  .detail-modal {
    max-height: 90vh;
    border-radius: 16px 16px 0 0;
    margin-top: auto;
  }
  
  .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .modal-body {
    padding: 1rem 1.5rem 1.5rem;
  }
  
  .modal-icon {
    width: 52px;
    height: 52px;
    font-size: 1.5rem;
  }
  
  .modal-header h3 {
    font-size: 1.25rem;
  }
}
</style>

<!-- 全局样式：模态框 (Teleport 到 body，需要非 scoped) -->
<style>
.detail-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.detail-modal {
  background: #fff;
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  z-index: 100000;
}

.detail-modal .modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #F1F5F9;
  color: #64748B;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10;
}
.detail-modal .modal-close:hover {
  background: #4F46E5;
  color: #fff;
}

.detail-modal .modal-header {
  padding: 2rem 2rem 1.5rem;
  text-align: center;
  border-bottom: 1px solid #E2E8F0;
}

.detail-modal .modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #fff;
  margin: 0 auto 1rem;
}

.detail-modal .modal-header h3 {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #1E293B;
}

.detail-modal .modal-subtitle {
  color: #64748B;
  font-size: 0.95rem;
  margin: 0;
}

.detail-modal .modal-body {
  padding: 1.5rem 2rem 2rem;
}

.detail-modal .detail-section {
  margin-bottom: 1.5rem;
}

.detail-modal .detail-section:last-of-type {
  margin-bottom: 1rem;
}

.detail-modal .detail-section h5 {
  font-size: 1rem;
  font-weight: 700;
  color: #4F46E5;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-modal .detail-section h5 i {
  font-size: 1.1rem;
}

.detail-modal .detail-section p {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.7;
  margin-bottom: 0.75rem;
}

.detail-modal .detail-section ul {
  margin: 0;
  padding-left: 1.25rem;
}

.detail-modal .detail-section li {
  color: #475569;
  font-size: 0.88rem;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.detail-modal .detail-section li strong {
  color: #1E293B;
}

.detail-modal .detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #E2E8F0;
}

.detail-modal .detail-tag {
  padding: 0.375rem 0.875rem;
  background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
  color: #4338CA;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
}

.anim-fade-in-up {
  animation: fadeInUpModal 0.3s ease both;
}

@keyframes fadeInUpModal {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .detail-modal {
    max-height: 90vh;
    border-radius: 16px 16px 0 0;
    margin-top: auto;
  }
  
  .detail-modal .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .detail-modal .modal-body {
    padding: 1rem 1.5rem 1.5rem;
  }
  
  .detail-modal .modal-icon {
    width: 52px;
    height: 52px;
    font-size: 1.5rem;
  }
  
  .detail-modal .modal-header h3 {
    font-size: 1.25rem;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .about-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2,
:global(html.light) .glow-3 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }
:global(html.light) .glow-3 { background: #0e7490; }

:global(html.light) .about-header h1 {
  color: #0c4a6e;
}

:global(html.light) .about-header p {
  color: #64748b;
}

:global(html.light) .section-title {
  color: #0c4a6e;
}

:global(html.light) .feature-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .feature-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 8px 32px rgba(8, 145, 178, 0.1);
}

:global(html.light) .feature-icon {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .feature-title {
  color: #0c4a6e;
}

:global(html.light) .feature-desc {
  color: #64748b;
}

:global(html.light) .tech-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .tech-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .tech-icon {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .tech-name {
  color: #0c4a6e;
}

:global(html.light) .tech-desc {
  color: #64748b;
}

:global(html.light) .team-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .team-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .member-avatar {
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .member-name {
  color: #0c4a6e;
}

:global(html.light) .member-role {
  color: #0891b2;
}

:global(html.light) .member-bio {
  color: #64748b;
}

:global(html.light) .stat-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .stat-value {
  color: #0891b2;
}

:global(html.light) .stat-label {
  color: #64748b;
}

:global(html.light) .contact-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .contact-title {
  color: #0c4a6e;
}

:global(html.light) .contact-text {
  color: #64748b;
}

:global(html.light) .contact-link {
  color: #0891b2;
}

:global(html.light) .modal-overlay {
  background: rgba(0, 0, 0, 0.3);
}

:global(html.light) .detail-modal {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .modal-header h3 {
  color: #0c4a6e;
}

:global(html.light) .close-btn {
  color: #64748b;
}

:global(html.light) .close-btn:hover {
  background: rgba(8, 145, 178, 0.1);
  color: #0891b2;
}

:global(html.light) .modal-body {
  color: #475569;
}

:global(html.light) .btn-primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-secondary {
  background: rgba(8, 145, 178, 0.08);
  border-color: rgba(8, 145, 178, 0.2);
  color: #64748b;
}

:global(html.light) .btn-secondary:hover {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}
</style>
