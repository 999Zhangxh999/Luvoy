<template>
  <div class="min-h-screen bg-brand-bg flex resume-builder-container">
    <!-- ═══ 左侧图标侧边栏（桌面端） ═══ -->
    <div class="w-16 flex-shrink-0 bg-brand-surface border-r border-brand-border flex flex-col items-center py-4 gap-2 desktop-sidebar">
      <button 
        v-for="tab in sidebarTabs" 
        :key="tab.id"
        @click="currentTab = tab.id"
        class="sidebar-icon-btn"
        :class="{ 'active': currentTab === tab.id }"
        :title="tab.name"
      >
        <i :class="tab.icon" class="text-lg"></i>
        <span class="text-[10px] mt-1">{{ tab.name }}</span>
      </button>
      <div class="flex-1"></div>
      <button @click="toggleAI" class="sidebar-icon-btn ai-btn" title="AI助手">
        <span class="text-xl">🤖</span>
        <span class="text-[10px] mt-1">AI助手</span>
      </button>
    </div>

    <!-- ═══ 移动端顶部Tab栏 ═══ -->
    <div class="mobile-tab-bar">
      <button 
        v-for="tab in sidebarTabs" 
        :key="'mobile-'+tab.id"
        @click="currentTab = tab.id"
        class="mobile-tab-btn"
        :class="{ 'active': currentTab === tab.id }"
      >
        <i :class="tab.icon" class="text-base"></i>
        <span class="text-[10px]">{{ tab.name }}</span>
      </button>
      <button @click="toggleAI" class="mobile-tab-btn ai-btn">
        <span class="text-base">🤖</span>
        <span class="text-[10px]">AI</span>
      </button>
    </div>

    <!-- ═══ 主内容区 ═══ -->
    <div class="flex-1 flex flex-col h-screen main-content-area">
      <!-- 顶部工具栏 -->
      <div class="h-12 bg-brand-surface border-b border-brand-border flex items-center justify-end px-4 gap-2 top-toolbar overflow-x-auto">
        <!-- 智能一页 -->
        <button @click="smartOnePage" class="toolbar-item">
          <span class="text-xs">智能一页</span>
        </button>
        
        <!-- 字体选择下拉框 -->
        <div class="toolbar-divider hidden md:block"></div>
        <div class="toolbar-select-wrapper hidden md:flex" @click="showFontMenu = !showFontMenu">
          <span class="text-xs">{{ fontDisplayName }}</span>
          <i class="bi bi-chevron-down text-xs ml-2 text-brand-muted"></i>
          <div v-if="showFontMenu" class="font-dropdown" @click.stop>
            <div 
              v-for="font in fontOptions" 
              :key="font.value"
              @click="selectFont(font)"
              class="font-dropdown-item"
              :class="{ 'active': styleSettings.fontFamily === font.value }"
              :style="{ fontFamily: font.value }"
            >
              {{ font.label }}
            </div>
          </div>
        </div>
        
        <!-- 字号 -->
        <div class="toolbar-item">
          <select v-model.number="styleSettings.fontSize" class="toolbar-inline-select w-12">
            <option v-for="size in [10,11,12,13,14,15,16]" :key="size" :value="size">{{ size }}</option>
          </select>
        </div>
        
        <!-- 主题色选择 -->
        <div class="toolbar-divider"></div>
        <div class="flex items-center gap-1.5">
          <button 
            v-for="color in themeColors" 
            :key="color"
            @click="styleSettings.themeColor = color"
            class="w-5 h-5 rounded-full border-2 transition hover:scale-110"
            :class="styleSettings.themeColor === color ? 'border-white shadow-lg' : 'border-transparent'"
            :style="{ backgroundColor: color }"
          ></button>
        </div>
        
        <!-- 模版样式 -->
        <div class="toolbar-divider"></div>
        <div class="toolbar-select-wrapper" @click="showTemplateMenu = !showTemplateMenu">
          <span class="text-xs">模版样式</span>
          <i class="bi bi-chevron-down text-xs ml-2 text-brand-muted"></i>
          <div v-if="showTemplateMenu" class="toolbar-dropdown" @click.stop>
            <button 
              v-for="tpl in resumeTemplates" 
              :key="tpl.id" 
              @click="applyTemplate(tpl.id)" 
              class="dropdown-item"
              :class="{ 'active': selectedTemplate === tpl.id }"
            >
              <i class="bi bi-check mr-2" v-if="selectedTemplate === tpl.id"></i>
              <span v-else class="w-4 mr-2"></span>
              {{ tpl.name }}
            </button>
          </div>
        </div>
        
        <!-- 模块管理 -->
        <div class="toolbar-select-wrapper hidden md:flex" @click="openModuleManager">
          <span class="text-xs">模块管理</span>
          <i class="bi bi-chevron-down text-xs ml-2 text-brand-muted"></i>
        </div>
        
        <!-- 更多操作 -->
        <div class="toolbar-divider"></div>
        <button @click="showExportMenu = !showExportMenu" class="toolbar-icon-btn relative" title="下载">
          <i class="bi bi-download"></i>
          <div v-if="showExportMenu" class="export-menu">
            <button @click="exportPDF" class="export-item"><i class="bi bi-file-pdf mr-2"></i>导出 PDF</button>
            <button @click="exportWord" class="export-item"><i class="bi bi-file-word mr-2"></i>导出 Word</button>
            <button @click="exportJSON" class="export-item"><i class="bi bi-filetype-json mr-2"></i>导出 JSON</button>
          </div>
        </button>
      </div>

      <!-- 内容区域 -->
      <div class="flex-1 flex overflow-hidden content-flex-area">
        <!-- 中间编辑/内容区 -->
        <div class="w-[420px] md:w-[420px] flex-shrink-0 border-r border-brand-border overflow-y-auto bg-brand-bg edit-panel">
          <!-- 简历编辑 -->
          <div v-if="currentTab === 'edit'" class="p-4">
            <!-- AI诊断卡片 -->
            <div class="ai-diagnosis-card mb-4" @click="runAIDiagnosis">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center">
                  <span class="text-xl">🤖</span>
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-semibold text-white">AI导师专业诊断</h3>
                  <p class="text-xs text-white/70">一键分析简历问题</p>
                </div>
                <button class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-white text-xs">
                  {{ isDiagnosing ? '分析中...' : '检查' }}
                </button>
              </div>
            </div>

            <!-- 完成度 -->
            <div class="mb-4 p-3 rounded-xl bg-brand-surface border border-brand-border">
              <div class="flex items-center justify-between text-xs mb-2">
                <span class="text-brand-muted">简历完成度</span>
                <span :class="completionRate >= 80 ? 'text-emerald-400' : 'text-amber-400'">{{ completionRate }}%</span>
              </div>
              <div class="h-1.5 bg-brand-bg rounded-full overflow-hidden">
                <div class="h-full rounded-full bg-gradient-to-r from-violet-500 to-cyan-500 transition-all" :style="{ width: completionRate + '%' }"></div>
              </div>
            </div>

            <!-- 编辑模块 -->
            <div class="space-y-3">
        <!-- 基本信息 -->
        <EditSection 
          title="基本信息" 
          icon="bi-person" 
          :is-expanded="expandedSection === 'basic'"
          @toggle="toggleSection('basic')"
        >
          <div class="space-y-3">
            <div class="edit-field">
              <label class="edit-label">姓名</label>
              <input v-model="resume.basic.name" class="edit-input" placeholder="请输入姓名" />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="edit-field">
                <label class="edit-label">电话</label>
                <input v-model="resume.basic.phone" class="edit-input" placeholder="手机号码" />
              </div>
              <div class="edit-field">
                <label class="edit-label">邮箱</label>
                <input v-model="resume.basic.email" class="edit-input" placeholder="电子邮箱" />
              </div>
            </div>
            <div class="edit-field">
              <label class="edit-label">头像</label>
              <div class="flex items-center gap-3">
                <div 
                  class="w-16 h-20 rounded-lg bg-brand-surface border border-brand-border overflow-hidden cursor-pointer hover:border-violet-500 transition relative group"
                  @click="triggerAvatarUpload"
                >
                  <img v-if="resume.basic.avatar" :src="resume.basic.avatar" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-brand-muted">
                    <i class="bi bi-person text-2xl"></i>
                  </div>
                  <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition">
                    <i class="bi bi-camera text-white text-lg"></i>
                  </div>
                </div>
                <input ref="avatarInput" type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
                <div class="flex flex-col gap-1">
                  <button @click="triggerAvatarUpload" class="btn-ghost text-sm">上传照片</button>
                  <button v-if="resume.basic.avatar" @click="resume.basic.avatar = ''" class="text-xs text-red-400 hover:text-red-300">移除照片</button>
                </div>
              </div>
            </div>
          </div>
        </EditSection>

        <!-- 教育经历 -->
        <EditSection 
          title="教育经历" 
          icon="bi-mortarboard" 
          :is-expanded="expandedSection === 'education'"
          :has-add="true"
          :has-delete="true"
          @toggle="toggleSection('education')"
          @add="addEducation"
          @delete="clearSection('education')"
        >
          <div v-for="(edu, index) in resume.education" :key="index" class="education-card">
            <!-- 教育经历卡片头部 -->
            <div 
              class="edu-card-header" 
              @click="toggleEduExpand(index)"
            >
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <span class="text-sm font-medium text-brand-text truncate">{{ edu.school || '新教育经历' }}</span>
                <button @click.stop="removeEducation(index)" class="text-brand-muted hover:text-red-400 flex-shrink-0">
                  <i class="bi bi-trash text-sm"></i>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xs text-brand-muted">{{ edu.major || '' }}{{ edu.major && edu.endDate ? ' | ' : '' }}{{ edu.endDate ? '-' + edu.endDate.replace('-', '.') : '' }}</span>
                <i class="bi bi-chevron-down text-brand-muted transition-transform" :class="{ 'rotate-180': expandedEduIndex === index }"></i>
              </div>
            </div>

            <!-- 教育经历详细编辑 -->
            <transition name="expand">
              <div v-show="expandedEduIndex === index" class="edu-card-body">
                <!-- 学校名称 & 校徽 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">学校名称</label>
                  <div class="flex items-center gap-3">
                    <input v-model="edu.school" class="edit-input flex-1" placeholder="如：西南交通大学" />
                    <div class="school-logo-upload" @click="triggerEduLogoUpload(index)">
                      <img v-if="edu.logo" :src="edu.logo" class="w-12 h-12 object-contain" />
                      <i v-else class="bi bi-building text-xl text-brand-muted"></i>
                    </div>
                    <button v-if="edu.logo" @click="edu.logo = ''" class="text-xs text-violet-400 hover:text-violet-300">更换</button>
                  </div>
                  <!-- 校徽大小调节 -->
                  <div v-if="edu.logo" class="flex items-center gap-2 mt-2">
                    <span class="text-xs text-brand-muted">校徽大小</span>
                    <input type="range" :min="24" :max="80" :value="edu.logoSize || 48" @input="edu.logoSize = Number($event.target.value)" class="flex-1 accent-violet-500" />
                    <span class="text-xs text-brand-muted w-8 text-right">{{ edu.logoSize || 48 }}px</span>
                  </div>
                </div>

                <!-- 学校标签 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">学校标签</label>
                  <div class="flex flex-wrap gap-2 mt-2">
                    <button 
                      v-for="tag in schoolTagOptions" 
                      :key="tag"
                      @click="toggleSchoolTag(edu, tag)"
                      class="school-tag-btn"
                      :class="{ 
                        'active-blue': edu.tags?.includes(tag) && tag !== '双一流',
                        'active-orange': edu.tags?.includes(tag) && tag === '双一流'
                      }"
                    >{{ tag }}</button>
                  </div>
                </div>

                <!-- 专业 / 学历 / 全日制 -->
                <div class="grid grid-cols-3 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">专业</label>
                    <input v-model="edu.major" class="edit-input" placeholder="人工智能" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">学历</label>
                    <select v-model="edu.degree" class="edit-input">
                      <option value="本科">本科</option>
                      <option value="硕士">硕士</option>
                      <option value="博士">博士</option>
                      <option value="大专">大专</option>
                    </select>
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">类型</label>
                    <select v-model="edu.fullTime" class="edit-input">
                      <option value="全日制">全日制</option>
                      <option value="非全日制">非全日制</option>
                    </select>
                  </div>
                </div>

                <!-- 学院 / 所在城市 -->
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">学院</label>
                    <input v-model="edu.college" class="edit-input" placeholder="请输入" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">所在城市</label>
                    <input v-model="edu.city" class="edit-input" placeholder="成都" />
                  </div>
                </div>

                <!-- 在读时间 -->
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">入学时间</label>
                    <input v-model="edu.startDate" type="month" class="edit-input" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">毕业时间</label>
                    <input v-model="edu.endDate" type="month" class="edit-input" />
                  </div>
                </div>

                <!-- 富文本描述区域 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">详细描述</label>
                  <RichEditor 
                    v-model="edu.description" 
                    placeholder="• 成绩排名：90.31/100 | GPA:3.83/4.00 排名约前5%  • 英语能力：CET-4 580分"
                  />
                </div>

                <!-- 底部AI功能按钮 -->
                <div class="flex items-center gap-3">
                  <button @click="aiCheckEducation(index)" class="edu-ai-btn secondary">
                    <i class="bi bi-search mr-2"></i>AI智能检查
                  </button>
                  <button @click="polishEducation(index)" class="edu-ai-btn primary">
                    <span class="mr-2">✨</span>简历润色
                  </button>
                </div>
              </div>
            </transition>
          </div>
          <button v-if="!resume.education.length" @click="addEducation" class="add-item-btn">
            <i class="bi bi-plus-circle mr-2"></i>添加一段教育经历
          </button>
        </EditSection>

        <!-- 竞赛经历 -->
        <EditSection 
          title="竞赛经历" 
          icon="bi-trophy" 
          :is-expanded="expandedSection === 'competition'"
          :has-add="true"
          :has-delete="true"
          @toggle="toggleSection('competition')"
          @add="addCompetition"
          @delete="clearSection('competitions')"
        >
          <div v-for="(comp, index) in resume.competitions" :key="index" class="section-card">
            <!-- 竞赛卡片头部 -->
            <div class="section-card-header" @click="toggleCompExpand(index)">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <span class="text-sm font-medium text-brand-text truncate">{{ comp.name || '新竞赛经历' }}</span>
                <button @click.stop="removeCompetition(index)" class="text-brand-muted hover:text-red-400 flex-shrink-0">
                  <i class="bi bi-trash text-sm"></i>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="comp.level" class="text-xs text-brand-muted">{{ comp.level }}</span>
                <i class="bi bi-chevron-down text-brand-muted transition-transform" :class="{ 'rotate-180': expandedCompIndex === index }"></i>
              </div>
            </div>

            <!-- 竞赛详细编辑 -->
            <transition name="expand">
              <div v-show="expandedCompIndex === index" class="section-card-body">
                <div class="grid grid-cols-1 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">竞赛名称</label>
                    <input v-model="comp.name" class="edit-input" placeholder="如：第21届百度之星程序设计大赛" />
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">奖项等级</label>
                    <select v-model="comp.level" class="edit-input">
                      <option value="">选择等级</option>
                      <option value="国家级一等奖">国家级一等奖</option>
                      <option value="国家级二等奖">国家级二等奖</option>
                      <option value="国家级三等奖">国家级三等奖</option>
                      <option value="省级一等奖">省级一等奖</option>
                      <option value="省级二等奖">省级二等奖</option>
                      <option value="省级三等奖">省级三等奖</option>
                      <option value="校级奖项">校级奖项</option>
                    </select>
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">获奖时间</label>
                    <input v-model="comp.date" type="month" class="edit-input" />
                  </div>
                </div>

                <!-- 富文本描述区域 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">详细描述</label>
                  <RichEditor 
                    v-model="comp.description" 
                    placeholder="补充竞赛的详细信息，如参赛作品、技术亮点等..."
                  />
                </div>

                <!-- AI功能按钮 -->
                <div class="flex items-center gap-3">
                  <button @click="aiCheckSection('competition', index)" class="section-ai-btn secondary">
                    <i class="bi bi-search mr-2"></i>AI智能检查
                  </button>
                  <button @click="polishSection('competition', index)" class="section-ai-btn primary">
                    <span class="mr-2">✨</span>简历润色
                  </button>
                </div>
              </div>
            </transition>
          </div>
          <button v-if="!resume.competitions.length" @click="addCompetition" class="add-item-btn">
            <i class="bi bi-plus-circle mr-2"></i>添加一段竞赛经历
          </button>
        </EditSection>

        <!-- 项目经历 -->
        <EditSection 
          title="项目经历" 
          icon="bi-folder" 
          :is-expanded="expandedSection === 'project'"
          :has-add="true"
          :has-delete="true"
          @toggle="toggleSection('project')"
          @add="addProject"
          @delete="clearSection('projects')"
        >
          <div v-for="(proj, index) in resume.projects" :key="index" class="section-card">
            <!-- 项目卡片头部 -->
            <div class="section-card-header" @click="toggleProjExpand(index)">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <span class="text-sm font-medium text-brand-text truncate">{{ proj.name || '新项目经历' }}</span>
                <button @click.stop="removeProject(index)" class="text-brand-muted hover:text-red-400 flex-shrink-0">
                  <i class="bi bi-trash text-sm"></i>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="proj.techStack" class="text-xs text-brand-muted truncate max-w-32">{{ proj.techStack }}</span>
                <i class="bi bi-chevron-down text-brand-muted transition-transform" :class="{ 'rotate-180': expandedProjIndex === index }"></i>
              </div>
            </div>

            <!-- 项目详细编辑 -->
            <transition name="expand">
              <div v-show="expandedProjIndex === index" class="section-card-body">
                <div class="grid grid-cols-1 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">项目名称</label>
                    <input v-model="proj.name" class="edit-input" placeholder="如：QQ-FARM-BOT" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">项目链接</label>
                    <input v-model="proj.link" class="edit-input" placeholder="如：https://github.com/xxx/project" />
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">项目影响力</label>
                    <input v-model="proj.impact" class="edit-input" placeholder="如：GitHub Starred 160+" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">技术栈</label>
                    <input v-model="proj.techStack" class="edit-input" placeholder="如：Node.js + Vue3" />
                  </div>
                </div>

                <!-- 富文本描述区域 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">项目详情</label>
                  <RichEditor 
                    v-model="proj.description" 
                    placeholder="项目背景与目标、你的角色与职责、技术亮点与工程能力..."
                  />
                </div>

                <!-- AI功能按钮 -->
                <div class="flex items-center gap-3">
                  <button @click="aiCheckSection('project', index)" class="section-ai-btn secondary">
                    <i class="bi bi-search mr-2"></i>AI智能检查
                  </button>
                  <button @click="polishSection('project', index)" class="section-ai-btn primary">
                    <span class="mr-2">✨</span>简历润色
                  </button>
                </div>
              </div>
            </transition>
          </div>
          <button v-if="!resume.projects.length" @click="addProject" class="add-item-btn">
            <i class="bi bi-plus-circle mr-2"></i>添加一段项目经历
          </button>
        </EditSection>

        <!-- 荣誉奖项 -->
        <EditSection 
          title="荣誉奖项" 
          icon="bi-award" 
          :is-expanded="expandedSection === 'honors'"
          :has-add="true"
          :has-delete="true"
          @toggle="toggleSection('honors')"
          @add="addHonor"
          @delete="clearSection('honors')"
        >
          <div v-for="(honor, index) in resume.honors" :key="index" class="section-card">
            <!-- 荣誉卡片头部 -->
            <div class="section-card-header" @click="toggleHonorExpand(index)">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <span class="text-sm font-medium text-brand-text truncate">{{ honor.name || '新荣誉奖项' }}</span>
                <button @click.stop="removeHonor(index)" class="text-brand-muted hover:text-red-400 flex-shrink-0">
                  <i class="bi bi-trash text-sm"></i>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="honor.date" class="text-xs text-brand-muted">{{ formatDate(honor.date) }}</span>
                <i class="bi bi-chevron-down text-brand-muted transition-transform" :class="{ 'rotate-180': expandedHonorIndex === index }"></i>
              </div>
            </div>

            <!-- 荣誉详细编辑 -->
            <transition name="expand">
              <div v-show="expandedHonorIndex === index" class="section-card-body">
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">奖项名称</label>
                    <input v-model="honor.name" class="edit-input" placeholder="如：校综合一等奖学金" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">获奖时间</label>
                    <input v-model="honor.date" type="month" class="edit-input" />
                  </div>
                </div>

                <!-- 富文本描述区域 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">详细描述</label>
                  <RichEditor 
                    v-model="honor.description" 
                    placeholder="补充荣誉的详细信息..."
                  />
                </div>

                <!-- AI功能按钮 -->
                <div class="flex items-center gap-3">
                  <button @click="aiCheckSection('honor', index)" class="section-ai-btn secondary">
                    <i class="bi bi-search mr-2"></i>AI智能检查
                  </button>
                  <button @click="polishSection('honor', index)" class="section-ai-btn primary">
                    <span class="mr-2">✨</span>简历润色
                  </button>
                </div>
              </div>
            </transition>
          </div>
          <button v-if="!resume.honors.length" @click="addHonor" class="add-item-btn">
            <i class="bi bi-plus-circle mr-2"></i>添加一段荣誉奖项
          </button>
        </EditSection>

        <!-- 实习/工作经历 -->
        <EditSection 
          title="实习经历" 
          icon="bi-briefcase" 
          :is-expanded="expandedSection === 'work'"
          :has-add="true"
          :has-delete="true"
          @toggle="toggleSection('work')"
          @add="addWork"
          @delete="clearSection('works')"
        >
          <div v-for="(work, index) in resume.works" :key="index" class="section-card">
            <!-- 实习卡片头部 -->
            <div class="section-card-header" @click="toggleWorkExpand(index)">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <span class="text-sm font-medium text-brand-text truncate">{{ work.company || '新实习经历' }}</span>
                <button @click.stop="removeWork(index)" class="text-brand-muted hover:text-red-400 flex-shrink-0">
                  <i class="bi bi-trash text-sm"></i>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="work.position" class="text-xs text-brand-muted">{{ work.position }}</span>
                <i class="bi bi-chevron-down text-brand-muted transition-transform" :class="{ 'rotate-180': expandedWorkIndex === index }"></i>
              </div>
            </div>

            <!-- 实习详细编辑 -->
            <transition name="expand">
              <div v-show="expandedWorkIndex === index" class="section-card-body">
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">公司名称</label>
                    <input v-model="work.company" class="edit-input" placeholder="如：字节跳动" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">职位</label>
                    <input v-model="work.position" class="edit-input" placeholder="如：算法工程师实习生" />
                  </div>
                </div>
                <div class="grid grid-cols-3 gap-3 mb-4">
                  <div class="edit-field">
                    <label class="edit-label">部门</label>
                    <input v-model="work.department" class="edit-input" placeholder="所在部门" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">开始时间</label>
                    <input v-model="work.startDate" type="month" class="edit-input" />
                  </div>
                  <div class="edit-field">
                    <label class="edit-label">结束时间</label>
                    <input v-model="work.endDate" type="month" class="edit-input" />
                  </div>
                </div>

                <!-- 富文本描述区域 -->
                <div class="edit-field mb-4">
                  <label class="edit-label">工作描述</label>
                  <RichEditor 
                    v-model="work.description" 
                    placeholder="使用STAR法则描述工作经历..."
                  />
                </div>

                <!-- AI功能按钮 -->
                <div class="flex items-center gap-3">
                  <button @click="aiCheckSection('work', index)" class="section-ai-btn secondary">
                    <i class="bi bi-search mr-2"></i>AI智能检查
                  </button>
                  <button @click="polishSection('work', index)" class="section-ai-btn primary">
                    <span class="mr-2">✨</span>简历润色
                  </button>
                </div>
              </div>
            </transition>
          </div>
          <button v-if="!resume.works.length" @click="addWork" class="add-item-btn">
            <i class="bi bi-plus-circle mr-2"></i>添加一段实习经历
          </button>
        </EditSection>

        <!-- 技能特长 -->
        <EditSection 
          title="技能特长" 
          icon="bi-tools" 
          :is-expanded="expandedSection === 'skills'"
          :has-delete="true"
          @toggle="toggleSection('skills')"
          @delete="clearSection('skills')"
        >
          <!-- 技能编辑 -->
          <div class="space-y-4">
            <!-- 富文本编辑区域 -->
            <div class="edit-field">
              <label class="edit-label">专业技能与特长</label>
              <RichEditor 
                v-model="resume.skills.professional" 
                placeholder="专业技能：熟练掌握Python、Java等编程语言..."
              />
            </div>

            <!-- AI功能按钮 -->
            <div class="flex items-center gap-3">
              <button @click="aiCheckSection('skills', 0)" class="section-ai-btn secondary">
                <i class="bi bi-search mr-2"></i>AI智能检查
              </button>
              <button @click="polishSection('skills', 0)" class="section-ai-btn primary">
                <span class="mr-2">✨</span>简历润色
              </button>
            </div>
          </div>
        </EditSection>

        <!-- 自定义模块 -->
        <EditSection 
          v-for="(section, index) in resume.customSections"
          :key="'custom-' + index"
          :title="section.title || '自定义模块'" 
          icon="bi-plus-square" 
          :is-expanded="expandedSection === 'custom-' + index"
          @toggle="toggleSection('custom-' + index)"
        >
          <div class="space-y-3">
            <div class="edit-field">
              <label class="edit-label">模块标题</label>
              <div class="flex items-center gap-2">
                <input v-model="section.title" class="edit-input flex-1" placeholder="输入模块标题" />
                <button @click="removeCustomSection(index)" class="text-red-400 hover:text-red-300 p-1">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div class="edit-field">
              <label class="edit-label">模块内容</label>
              <RichEditor v-model="section.content" placeholder="输入模块内容" />
            </div>
            <div class="flex justify-end gap-2 pt-2">
              <button @click="aiCheckSection('custom', index)" class="section-ai-btn secondary">
                <i class="bi bi-check-circle"></i> AI 检查
              </button>
            </div>
          </div>
        </EditSection>

        <!-- 添加自定义模块按钮 -->
        <button @click="addCustomSection" class="w-full mt-4 py-3 border-2 border-dashed border-brand-border rounded-xl text-brand-muted hover:text-brand-text hover:border-violet-500 transition flex items-center justify-center gap-2">
          <i class="bi bi-plus-circle"></i>
          <span>添加自定义模块</span>
        </button>
            </div>
          </div>

          <!-- 简历模板 -->
          <!-- 我的简历列表 -->
          <div v-else-if="currentTab === 'myresumes'" class="p-4">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-brand-text">我的简历</h2>
              <button @click="createNewResume" class="px-3 py-1.5 rounded-lg bg-violet-600 text-white text-xs hover:bg-violet-700 transition">
                <i class="bi bi-plus-lg mr-1"></i>新建
              </button>
            </div>

            <!-- 当前编辑中 -->
            <div class="mb-3 p-3 rounded-xl bg-violet-600/10 border border-violet-500/30">
              <div class="flex items-center gap-2 mb-2">
                <i class="bi bi-pencil-fill text-violet-400 text-xs"></i>
                <span class="text-xs text-violet-400">当前编辑</span>
              </div>
              <div v-if="!isRenamingCurrent" class="flex items-center justify-between">
                <span class="text-sm font-medium text-brand-text truncate">{{ currentResumeName }}</span>
                <div class="flex items-center gap-1">
                  <button @click="isRenamingCurrent = true; renamingName = currentResumeName" class="text-brand-muted hover:text-brand-text p-1" title="重命名">
                    <i class="bi bi-pencil text-xs"></i>
                  </button>
                  <button @click="saveCurrentResumeAs" class="text-brand-muted hover:text-brand-text p-1" title="另存为">
                    <i class="bi bi-save text-xs"></i>
                  </button>
                </div>
              </div>
              <div v-else class="flex items-center gap-2">
                <input v-model="renamingName" class="flex-1 px-2 py-1 rounded bg-brand-bg border border-brand-border text-sm text-brand-text" @keyup.enter="confirmRenameCurrent" />
                <button @click="confirmRenameCurrent" class="text-emerald-400 hover:text-emerald-300"><i class="bi bi-check-lg"></i></button>
                <button @click="isRenamingCurrent = false" class="text-brand-muted hover:text-brand-text"><i class="bi bi-x-lg"></i></button>
              </div>
            </div>

            <!-- 已保存的简历列表 -->
            <div class="space-y-2">
              <div v-if="savedResumeList.length === 0" class="text-center py-8 text-brand-muted text-sm">
                <i class="bi bi-folder2 text-3xl block mb-2"></i>
                暂无已保存的简历
              </div>
              <div 
                v-for="item in savedResumeList" 
                :key="item.id"
                class="p-3 rounded-xl bg-brand-surface border border-brand-border hover:border-violet-500/50 transition group cursor-pointer"
                @click="loadSavedResume(item.id)"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-brand-text truncate">{{ item.name }}</div>
                    <div class="text-xs text-brand-muted mt-0.5">{{ formatSavedTime(item.updatedAt) }}</div>
                  </div>
                  <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
                    <button @click.stop="duplicateResume(item.id)" class="text-brand-muted hover:text-brand-text p-1" title="复制">
                      <i class="bi bi-copy text-xs"></i>
                    </button>
                    <button @click.stop="deleteSavedResume(item.id)" class="text-brand-muted hover:text-red-400 p-1" title="删除">
                      <i class="bi bi-trash text-xs"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="currentTab === 'template'" class="p-4">
            <h2 class="text-lg font-bold text-brand-text mb-4">选择模板</h2>
            <div class="grid grid-cols-2 gap-4">
              <div 
                v-for="tpl in resumeTemplates" 
                :key="tpl.id"
                @click="applyTemplate(tpl.id)"
                class="template-card"
                :class="{ 'selected': selectedTemplate === tpl.id }"
              >
                <div class="template-preview" :style="{ background: tpl.color }">
                  <div class="template-lines"></div>
                </div>
                <div class="template-info">
                  <span class="text-sm font-medium text-brand-text">{{ tpl.name }}</span>
                  <span class="text-xs text-brand-muted">{{ tpl.desc }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- AI导师 -->
          <div v-else-if="currentTab === 'ai'" class="p-4">
            <h2 class="text-lg font-bold text-brand-text mb-4">我的优化报告</h2>
            <div class="text-xs text-brand-muted mb-4">简历专家诊断次数不限制 有任何疑惑可以找大师级简历顾问<span class="text-amber-400">0 次</span></div>
            
            <!-- 目标岗位 -->
            <div class="ai-form-group">
              <label class="ai-form-label">目标岗位</label>
              <input v-model="targetJob.title" class="ai-form-input" placeholder="请填写目标岗位" />
            </div>
            
            <!-- 岗位类别 -->
            <div class="ai-form-group">
              <label class="ai-form-label">岗位类别</label>
              <select v-model="targetJob.category" class="ai-form-input">
                <option value="">请选择</option>
                <option value="tech">技术研发</option>
                <option value="product">产品运营</option>
                <option value="design">设计创意</option>
                <option value="market">市场销售</option>
              </select>
            </div>
            
            <!-- 工作经验 -->
            <div class="ai-form-group">
              <label class="ai-form-label">工作经验</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="exp in experienceOptions" 
                  :key="exp"
                  @click="targetJob.experience = exp"
                  class="exp-tag"
                  :class="{ 'active': targetJob.experience === exp }"
                >{{ exp }}</button>
              </div>
            </div>
            
            <!-- 岗位描述 -->
            <div class="ai-form-group">
              <label class="ai-form-label">岗位描述</label>
              <textarea v-model="targetJob.description" class="ai-form-input min-h-20" placeholder="请填写期望的岗位"></textarea>
            </div>
            
            <!-- 求职状态 -->
            <div class="ai-form-group">
              <label class="ai-form-label">我的求职状态</label>
              <select v-model="targetJob.status" class="ai-form-input">
                <option value="">请选择</option>
                <option value="looking">积极找工作</option>
                <option value="passive">观望机会</option>
                <option value="employed">在职</option>
              </select>
            </div>
            
            <!-- 求职类型 -->
            <div class="ai-form-group">
              <label class="ai-form-label">求职类型</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="type in jobTypes" 
                  :key="type"
                  @click="toggleJobType(type)"
                  class="exp-tag"
                  :class="{ 'active': targetJob.types.includes(type) }"
                >{{ type }}</button>
              </div>
            </div>
            
            <button @click="runAIDiagnosis" class="w-full mt-6 btn-primary py-3 rounded-xl">
              <i class="bi bi-magic mr-2"></i>查看简历得分
            </button>
          </div>

          <!-- 职位推荐 -->
          <div v-else-if="currentTab === 'jobs'" class="p-4">
            <h2 class="text-lg font-bold text-brand-text mb-2">为你推荐的职位</h2>
            <p class="text-xs text-brand-muted mb-4">根据你的简历智能匹配</p>
            
            <div class="space-y-3">
              <div 
                v-for="job in recommendedJobs" 
                :key="job.id"
                class="job-card"
                @click="goToJob(job)"
              >
                <div class="flex items-start justify-between mb-2">
                  <div>
                    <h3 class="text-sm font-semibold text-brand-text">{{ job.title }}</h3>
                    <p class="text-xs text-brand-muted">{{ job.company }}</p>
                  </div>
                  <span class="job-match">匹配度 {{ job.matchRate }}%</span>
                </div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="job-tag">{{ job.location }}</span>
                  <span class="job-tag">{{ job.experience }}</span>
                  <span class="job-tag">{{ job.education }}</span>
                </div>
                <div class="text-sm text-amber-400 font-medium">{{ job.salary }}</div>
                <div class="flex flex-wrap gap-1 mt-2">
                  <span v-for="skill in job.skills" :key="skill" class="skill-tag">{{ skill }}</span>
                </div>
              </div>
            </div>
            
            <button @click="loadMoreJobs" class="w-full mt-4 py-2.5 border border-brand-border rounded-lg text-sm text-brand-muted hover:text-brand-text hover:border-violet-500 transition">
              加载更多职位
            </button>
          </div>
        </div>

        <!-- 右侧预览区 -->
        <div class="flex-1 bg-slate-700/30 overflow-y-auto relative">
          <!-- 缩放控制 -->
          <div class="absolute top-4 right-4 flex items-center gap-2 z-10">
            <button @click="zoomLevel = Math.max(50, zoomLevel - 10)" class="zoom-btn">
              <i class="bi bi-zoom-out"></i>
            </button>
            <span class="text-xs text-brand-muted w-10 text-center">{{ zoomLevel }}%</span>
            <button @click="zoomLevel = Math.min(150, zoomLevel + 10)" class="zoom-btn">
              <i class="bi bi-zoom-in"></i>
            </button>
          </div>

          <div class="p-8">
            <div class="max-w-[210mm] mx-auto">
              <!-- 简历预览卡片 -->
              <div 
                ref="resumePreviewRef"
                class="resume-preview-card" 
                :class="'template-' + selectedTemplate"
                :style="{ 
                  transform: `scale(${zoomLevel / 100})`,
                  fontFamily: styleSettings.fontFamily,
                  fontSize: styleSettings.fontSize + 'px',
                  lineHeight: styleSettings.lineHeight,
                  padding: styleSettings.margin === 'narrow' ? '30px' : styleSettings.margin === 'wide' ? '60px' : '40px',
                  '--theme-color': styleSettings.themeColor
                }"
              >
                <!-- 简历头部 -->
                <div class="resume-header">
                  <div class="flex items-start">
                    <!-- 左侧校徽 -->
                    <div class="w-20 flex-shrink-0">
                      <img v-if="resume.education[0] && resume.education[0].logo" :src="resume.education[0].logo" :style="{ width: (resume.education[0].logoSize || 48) + 'px', height: (resume.education[0].logoSize || 48) + 'px' }" class="object-contain" />
                    </div>
                    <!-- 中间姓名+联系方式 居中 -->
                    <div class="flex-1 text-center">
                      <h1 class="text-2xl font-bold text-slate-800 mb-2">{{ resume.basic.name || '姓名' }}</h1>
                      <div class="flex items-center justify-center gap-4 text-sm text-slate-600">
                        <span v-if="resume.basic.phone">电话：{{ resume.basic.phone }}</span>
                        <span v-if="resume.basic.email">邮箱：{{ resume.basic.email }}</span>
                      </div>
                    </div>
                    <!-- 右侧头像 -->
                    <div class="w-20 flex-shrink-0 flex justify-end">
                      <div v-if="resume.basic.avatar" class="w-20 h-26 rounded overflow-hidden border border-slate-200">
                        <img :src="resume.basic.avatar" class="w-full h-full object-cover" />
                      </div>
                    </div>
                  </div>
                </div>

          <!-- 教育经历 -->
          <div v-if="validEducation.length" class="resume-section">
            <h2 class="resume-section-title">教育经历</h2>
            <div v-for="(edu, idx) in validEducation" :key="idx" class="resume-item">
              <div class="flex items-start justify-between mb-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-800">{{ edu.school }}</span>
                  <template v-if="edu.tags && edu.tags.length">
                    <span v-for="tag in edu.tags" :key="tag" class="px-1.5 py-0.5 rounded text-xs bg-violet-100 text-violet-600">{{ tag }}</span>
                  </template>
                  <span v-else-if="edu.level" class="px-1.5 py-0.5 rounded text-xs bg-violet-100 text-violet-600">{{ edu.level }}</span>
                </div>
                <span class="text-sm text-slate-500">{{ formatDate(edu.startDate) }} - {{ formatDate(edu.endDate) }}</span>
              </div>
              <div v-if="edu.major || edu.degree" class="text-sm text-slate-600 mb-1">
                {{ edu.major }}<template v-if="edu.major && edu.degree"> </template>{{ edu.degree }}
                <template v-if="edu.college">（{{ edu.college }}）</template>
              </div>
              <!-- 优先显示 description，否则显示 ranking/courses -->
              <div v-if="edu.description" class="resume-rich-content text-sm text-slate-600" v-html="edu.description"></div>
              <ul v-else class="resume-list">
                <li v-if="edu.ranking">成绩排名：{{ edu.ranking }}</li>
                <li v-if="edu.courses">主修课程：{{ edu.courses }}</li>
              </ul>
            </div>
          </div>

          <!-- 竞赛经历 -->
          <div v-if="validCompetitions.length" class="resume-section">
            <h2 class="resume-section-title">竞赛经历</h2>
            <ul class="resume-list">
              <li v-for="(comp, idx) in validCompetitions" :key="idx">
                <template v-if="comp.name && comp.level">{{ comp.name }}（{{ comp.level }}）</template>
                <template v-else-if="comp.name">{{ comp.name }}</template>
                <template v-else-if="comp.level">{{ comp.level }}</template>
              </li>
            </ul>
          </div>

          <!-- 项目经历 -->
          <div v-if="validProjects.length" class="resume-section">
            <h2 class="resume-section-title">项目经历</h2>
            <div v-for="(proj, idx) in validProjects" :key="idx" class="resume-item">
              <div class="flex items-start justify-between mb-1">
                <div>
                  <span class="font-semibold text-slate-800">{{ proj.name }}</span>
                  <a v-if="proj.link" :href="proj.link" class="text-xs text-violet-600 ml-2" target="_blank">{{ proj.link }}</a>
                </div>
              </div>
              <div v-if="proj.impact" class="text-sm text-slate-600 mb-1">项目影响力：{{ proj.impact }}</div>
              <div v-if="proj.techStack" class="text-sm text-slate-600 mb-1">技术栈：{{ proj.techStack }}</div>
              <div v-if="proj.engineering" class="text-sm text-slate-600 mb-1">工程能力：{{ proj.engineering }}</div>
              <div v-if="proj.description" class="resume-rich-content text-sm text-slate-600" v-html="proj.description"></div>
            </div>
          </div>

          <!-- 实习经历 -->
          <div v-if="validWorks.length" class="resume-section">
            <h2 class="resume-section-title">实习经历</h2>
            <div v-for="(work, idx) in validWorks" :key="idx" class="resume-item">
              <div class="flex items-start justify-between mb-1">
                <span class="font-semibold text-slate-800">{{ work.company }}<template v-if="work.position"> - {{ work.position }}</template></span>
                <span class="text-sm text-slate-500">{{ formatDate(work.startDate) }}<template v-if="work.endDate"> - {{ formatDate(work.endDate) }}</template></span>
              </div>
              <div v-if="work.description" class="resume-rich-content text-sm text-slate-600" v-html="work.description"></div>
            </div>
          </div>

          <!-- 荣誉奖项 -->
          <div v-if="validHonors.length" class="resume-section">
            <h2 class="resume-section-title">荣誉奖项</h2>
            <ul class="resume-list">
              <li v-for="(honor, idx) in validHonors" :key="idx">{{ honor.name }}</li>
            </ul>
          </div>

          <!-- 技能特长 -->
          <div v-if="resume.skills.professional || resume.skills.language" class="resume-section">
            <h2 class="resume-section-title">技能特长</h2>
            <div v-if="resume.skills.professional" class="resume-rich-content text-sm text-slate-600" v-html="resume.skills.professional"></div>
          </div>

          <!-- 自定义模块 -->
          <div 
            v-for="section in resume.customSections" 
            :key="section.title" 
            class="resume-section"
          >
            <h2 class="resume-section-title">{{ section.title }}</h2>
            <div class="resume-rich-content text-sm text-slate-600" v-html="section.content"></div>
          </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ AI助手悬浮窗 ═══ -->
    <!-- ═══ 可爱机器人AI助手 ═══ -->
    <div 
      class="resume-ai-agent" 
      :class="{ 'is-active': isAIExpanded, 'is-dragging': isDragging }"
      :style="{ right: agentPosX + 'px', bottom: agentPosY + 'px' }"
    >
      <!-- 背景遮罩 -->
      <div v-if="isAIExpanded" class="agent-backdrop" @click="toggleAI"></div>
      
      <!-- 机器人角色 -->
      <div 
        class="agent-wrapper" 
        @click="handleAgentClick"
        @mousedown="startAgentDrag"
        @mouseenter="onAgentHover"
        @mouseleave="onAgentLeave"
      >
        <!-- 脉冲环 -->
        <div class="pulse-ring" v-if="!isAIExpanded && !isDragging"></div>
        <div class="pulse-ring delay" v-if="!isAIExpanded && !isDragging"></div>
        
        <!-- 可爱机器人头像 -->
        <div class="robot-avatar" :class="{ thinking: isAIThinking, speaking: isAISpeaking, happy: isHappy, wave: isWaving }">
          <div class="avatar-glow"></div>
          <div class="avatar-main">
            <div class="antenna-wrap">
              <div class="antenna-stem"></div>
              <div class="antenna-tip" :class="{ active: isAIThinking }"></div>
            </div>
            <div class="face">
              <div class="eyes">
                <div class="eye left" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
                <div class="eye right" :class="eyeState"><div class="pupil"></div><div class="highlight"></div></div>
              </div>
              <div class="mouth" :class="mouthState"></div>
              <div class="cheek left"></div>
              <div class="cheek right"></div>
            </div>
          </div>
          <div class="status-indicator" :class="isAIThinking ? 'thinking' : 'online'">
            <span class="status-text">{{ isAIThinking ? '思考中...' : '在线' }}</span>
          </div>
        </div>
      </div>

      <!-- 闲聊气泡 -->
      <transition name="bubble-pop">
        <div v-if="showIdleBubble && !isAIExpanded" class="idle-bubble" @click="toggleAI">
          <span class="bubble-text">{{ idleBubbleText }}</span>
          <div class="bubble-tail"></div>
        </div>
      </transition>

      <!-- 主交互面板 -->
      <transition name="panel-spring">
        <div v-if="isAIExpanded" class="agent-panel">
          <div class="panel-header">
            <div class="header-left">
              <span class="header-icon">🤖</span>
              <span class="header-title">简历小助手</span>
            </div>
            <button class="close-btn" @click="toggleAI"><i class="bi bi-x-lg"></i></button>
          </div>

          <!-- 对话区域 -->
          <div class="chat-zone" ref="chatContainerRef">
            <div v-for="(msg, idx) in aiMessages" :key="idx" class="chat-message" :class="msg.role">
              <span v-if="msg.role === 'assistant'" class="msg-avatar">🤖</span>
              <div class="msg-content">
                <p class="msg-text">{{ msg.content }}</p>
                <!-- 快捷操作 -->
                <div v-if="msg.actions" class="msg-actions">
                  <button 
                    v-for="action in msg.actions" 
                    :key="action.id" 
                    @click="handleAIAction(action)"
                    class="action-chip"
                  >
                    <i :class="action.icon" class="mr-1"></i>{{ action.label }}
                  </button>
                </div>
              </div>
            </div>
            <div v-if="isAIThinking" class="chat-message assistant typing">
              <span class="msg-avatar">🤖</span>
              <div class="msg-content">
                <div class="typing-dots"><span></span><span></span><span></span></div>
              </div>
            </div>
          </div>

          <!-- 功能网格 -->
          <div class="action-grid" v-if="showAgentMenu">
            <button class="action-card" @click="startResumeGuide">
              <span class="action-icon">📝</span>
              <span class="action-label">开始写简历</span>
            </button>
            <button class="action-card" @click="runAIDiagnosis">
              <span class="action-icon">🔍</span>
              <span class="action-label">诊断简历</span>
            </button>
            <button class="action-card" @click="showAIPolish = true; toggleAI()">
              <span class="action-icon">✨</span>
              <span class="action-label">AI润色</span>
            </button>
            <button class="action-card" @click="askCareerAdvice">
              <span class="action-icon">💡</span>
              <span class="action-label">求职建议</span>
            </button>
          </div>

          <!-- 快捷回复 -->
          <div class="quick-replies-bar">
            <button v-for="reply in quickReplies" :key="reply.id" @click="sendQuickReply(reply)" class="quick-btn">
              <span>{{ reply.icon }}</span>
              <span>{{ reply.text }}</span>
            </button>
          </div>

          <!-- 输入框 -->
          <div class="input-bar">
            <input 
              v-model="aiInput" 
              @keyup.enter="sendAIMessage"
              placeholder="问我任何关于简历的问题..."
              class="chat-input"
            />
            <button @click="sendAIMessage" class="send-btn" :disabled="!aiInput.trim()">
              <i class="bi bi-send-fill"></i>
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- AI诊断弹窗 -->
    <Teleport to="body">
      <transition name="fade">
      <div v-if="showAIDiagnosis" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="showAIDiagnosis = false">
        <div class="diagnosis-modal">
          <div class="modal-header">
            <h2 class="text-lg font-bold text-brand-text flex items-center gap-2">
              <span class="text-xl">🔍</span> AI简历诊断报告
            </h2>
            <button @click="showAIDiagnosis = false" class="text-brand-muted hover:text-brand-text">
              <i class="bi bi-x-lg text-xl"></i>
            </button>
          </div>
          <div class="modal-body">
            <!-- 总体评分 -->
            <div class="diagnosis-score">
              <div class="score-ring">
                <svg viewBox="0 0 100 100" class="w-24 h-24">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="8" class="text-brand-border" />
                  <circle cx="50" cy="50" r="45" fill="none" stroke="url(#scoreGradient)" stroke-width="8" 
                    stroke-linecap="round" :stroke-dasharray="`${diagnosisScore * 2.83} 283`" transform="rotate(-90 50 50)" />
                  <defs>
                    <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stop-color="#7c3aed" />
                      <stop offset="100%" stop-color="#06b6d4" />
                    </linearGradient>
                  </defs>
                </svg>
                <span class="score-num">{{ diagnosisScore }}</span>
              </div>
              <div class="score-info">
                <span class="score-label">简历综合评分</span>
                <span class="score-hint">优化后预计可达 {{ Math.min(98, diagnosisScore + 20) }}+ 分</span>
              </div>
            </div>

            <!-- 问题列表 -->
            <div class="diagnosis-issues">
              <h3 class="text-sm font-semibold text-brand-text mb-3">待优化项 ({{ diagnosisIssues.length }})</h3>
              <div v-if="diagnosisIssues.length === 0" class="text-center py-8 text-brand-muted">
                <i class="bi bi-check-circle text-4xl text-emerald-400 mb-2"></i>
                <p>太棒了！暂无待优化项</p>
              </div>
              <div v-else class="space-y-2">
                <div v-for="(issue, idx) in diagnosisIssues" :key="idx" class="issue-card" :class="issue.severity">
                  <div class="issue-icon">
                    <i :class="issue.icon"></i>
                  </div>
                  <div class="issue-content">
                    <span class="issue-title">{{ issue.title }}</span>
                    <span class="issue-desc">{{ issue.description }}</span>
                  </div>
                  <button @click="applyAISuggestion(issue)" class="issue-fix-btn">
                    <i class="bi bi-magic mr-1"></i>一键优化
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="showAIDiagnosis = false" class="btn-secondary">稍后再说</button>
            <button v-if="diagnosisIssues.length" @click="applyAllSuggestions" class="btn-primary">
              <i class="bi bi-magic mr-2"></i>一键优化全部
            </button>
          </div>
        </div>
      </div>
      </transition>

      <!-- AI润色弹窗 -->
      <transition name="fade">
      <div v-if="showAIPolish" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="showAIPolish = false">
        <div class="diagnosis-modal">
          <div class="modal-header">
            <h2 class="text-lg font-bold text-brand-text flex items-center gap-2">
              <span class="text-xl">✨</span> AI简历润色
            </h2>
            <button @click="showAIPolish = false" class="text-brand-muted hover:text-brand-text">
              <i class="bi bi-x-lg text-xl"></i>
            </button>
          </div>
          <div class="modal-body">
            <p class="text-sm text-brand-muted mb-4">选择你想要优化的模块，AI将帮你润色内容，使描述更专业、更有吸引力。</p>
            
            <div class="space-y-3">
              <div class="polish-option">
                <div class="flex items-center gap-3">
                  <div class="polish-icon bg-violet-500/20 text-violet-400">
                    <i class="bi bi-folder"></i>
                  </div>
                  <div class="flex-1">
                    <span class="text-sm font-medium text-brand-text">项目经历</span>
                    <span class="text-xs text-brand-muted block">优化项目描述，突出技术亮点和成果</span>
                  </div>
                  <button @click="polishSection('projects')" class="btn-sm">
                    <i class="bi bi-magic mr-1"></i>润色
                  </button>
                </div>
              </div>
              
              <div class="polish-option">
                <div class="flex items-center gap-3">
                  <div class="polish-icon bg-blue-500/20 text-blue-400">
                    <i class="bi bi-briefcase"></i>
                  </div>
                  <div class="flex-1">
                    <span class="text-sm font-medium text-brand-text">实习经历</span>
                    <span class="text-xs text-brand-muted block">使用STAR法则优化工作描述</span>
                  </div>
                  <button @click="polishSection('works')" class="btn-sm">
                    <i class="bi bi-magic mr-1"></i>润色
                  </button>
                </div>
              </div>
              
              <div class="polish-option">
                <div class="flex items-center gap-3">
                  <div class="polish-icon bg-emerald-500/20 text-emerald-400">
                    <i class="bi bi-tools"></i>
                  </div>
                  <div class="flex-1">
                    <span class="text-sm font-medium text-brand-text">技能特长</span>
                    <span class="text-xs text-brand-muted block">根据项目经历自动生成专业技能</span>
                  </div>
                  <button @click="polishSection('skills')" class="btn-sm">
                    <i class="bi bi-magic mr-1"></i>润色
                  </button>
                </div>
              </div>
              
              <div class="polish-option">
                <div class="flex items-center gap-3">
                  <div class="polish-icon bg-orange-500/20 text-orange-400">
                    <i class="bi bi-file-text"></i>
                  </div>
                  <div class="flex-1">
                    <span class="text-sm font-medium text-brand-text">全文润色</span>
                    <span class="text-xs text-brand-muted block">一键优化简历所有模块内容</span>
                  </div>
                  <button @click="polishAll" class="btn-primary">
                    <i class="bi bi-magic mr-1"></i>全部润色
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </transition>

      <!-- 模块管理弹窗 -->
      <transition name="fade">
      <div v-if="showModuleManager" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="showModuleManager = false">
        <div class="module-manager-modal">
          <div class="modal-header">
            <h2 class="text-lg font-bold text-brand-text">模块管理</h2>
            <button @click="showModuleManager = false" class="text-brand-muted hover:text-brand-text">
              <i class="bi bi-x-lg text-xl"></i>
            </button>
          </div>
          <div class="modal-body max-h-[70vh] overflow-y-auto">
            <!-- 已有模块 -->
            <div class="mb-6">
              <h3 class="text-sm font-semibold text-brand-text mb-3">已有模块</h3>
              <div class="space-y-2">
                <div 
                  v-for="mod in enabledModules" 
                  :key="mod.id"
                  class="module-item"
                  draggable="true"
                  @dragstart="dragStart($event, mod)"
                  @dragover.prevent
                  @drop="drop($event, mod)"
                >
                  <div class="drag-handle">
                    <i class="bi bi-list"></i>
                  </div>
                  <span class="flex-1 text-sm text-brand-text">{{ mod.name }}</span>
                  <button @click="editModule(mod)" class="module-action-btn">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button @click="removeModule(mod)" class="module-action-btn text-red-400 hover:text-red-300">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 添加模块 -->
            <div>
              <h3 class="text-sm font-semibold text-brand-text mb-3">添加模块</h3>
              <div class="space-y-2">
                <div 
                  v-for="mod in availableModules" 
                  :key="mod.id"
                  @click="addModule(mod)"
                  class="module-item add-module cursor-pointer"
                >
                  <div class="add-icon">
                    <i class="bi bi-plus"></i>
                  </div>
                  <span class="flex-1 text-sm text-brand-text">{{ mod.name }}</span>
                  <span v-if="mod.premium" class="premium-badge">💎</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </transition>

      <!-- Toast 提示 -->
      <div class="fixed top-20 right-6 z-[100] space-y-2">
        <transition-group name="toast">
          <div 
            v-for="toast in toasts" 
            :key="toast.id" 
            class="toast-item"
            :class="toast.type"
          >
            <i :class="toast.type === 'success' ? 'bi bi-check-circle' : toast.type === 'error' ? 'bi bi-x-circle' : 'bi bi-info-circle'" class="mr-2"></i>
            {{ toast.message }}
          </div>
        </transition-group>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import EditSection from '@/components/EditSection.vue'
import RichEditor from '@/components/RichEditor.vue'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const router = useRouter()

// 版式设置
const showStylePanel = ref(false)
const showAIPolish = ref(false)
const styleSettings = reactive({
  fontFamily: "'Source Han Sans', 'Noto Sans SC', sans-serif",
  fontSize: 12,
  lineHeight: 1.5,
  margin: 'normal',
  themeColor: '#2563eb'
})
const themeColors = ['#2563eb', '#7c3aed', '#059669', '#dc2626', '#ea580c', '#0891b2', '#1e293b']

// ═══ 多简历管理 ═══
const currentResumeId = ref('') // 当前编辑的简历ID
const currentResumeName = ref('未命名简历')
const savedResumeList = ref([]) // [{id, name, updatedAt}]
const isRenamingCurrent = ref(false)
const renamingName = ref('')

function loadResumeList() {
  try {
    const list = JSON.parse(localStorage.getItem('luvoy-resume-list') || '[]')
    savedResumeList.value = list
  } catch { savedResumeList.value = [] }
}

function saveResumeList() {
  localStorage.setItem('luvoy-resume-list', JSON.stringify(savedResumeList.value))
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
}

function persistCurrentResume() {
  if (!currentResumeId.value) {
    currentResumeId.value = generateId()
  }
  const data = JSON.parse(JSON.stringify(resume))
  localStorage.setItem('luvoy-resume-' + currentResumeId.value, JSON.stringify(data))
  // 更新列表
  const idx = savedResumeList.value.findIndex(r => r.id === currentResumeId.value)
  const entry = { id: currentResumeId.value, name: currentResumeName.value, updatedAt: Date.now() }
  if (idx >= 0) {
    savedResumeList.value[idx] = entry
  } else {
    savedResumeList.value.unshift(entry)
  }
  saveResumeList()
  localStorage.setItem('luvoy-current-resume-id', currentResumeId.value)
}

function createNewResume() {
  // 先保存当前
  persistCurrentResume()
  // 创建新简历
  currentResumeId.value = generateId()
  currentResumeName.value = '未命名简历'
  const blank = {
    basic: { name: '', phone: '', email: '', avatar: '' },
    education: [{ school: '', level: '', tags: [], major: '', degree: '本科', fullTime: '全日制', college: '', city: '', logo: '', logoSize: 48, startDate: '', endDate: '', ranking: '', courses: '', description: '' }],
    competitions: [{ name: '', level: '', date: '', description: '' }],
    projects: [{ name: '', link: '', impact: '', techStack: '', engineering: '', description: '' }],
    works: [{ company: '', position: '', department: '', startDate: '', endDate: '', description: '' }],
    honors: [{ name: '', date: '', description: '' }],
    skills: { professional: '', language: '', other: '' },
    customSections: []
  }
  Object.assign(resume, blank)
  persistCurrentResume()
  currentTab.value = 'edit'
  showToast('已创建新简历', 'success')
}

function loadSavedResume(id) {
  // 先保存当前
  persistCurrentResume()
  try {
    const data = JSON.parse(localStorage.getItem('luvoy-resume-' + id))
    if (data) {
      Object.assign(resume, data)
      currentResumeId.value = id
      const entry = savedResumeList.value.find(r => r.id === id)
      currentResumeName.value = entry ? entry.name : '未命名简历'
      localStorage.setItem('luvoy-current-resume-id', id)
      currentTab.value = 'edit'
      showToast('已加载简历', 'success')
    }
  } catch { showToast('加载失败', 'error') }
}

function deleteSavedResume(id) {
  if (!confirm('确定要删除这份简历吗？')) return
  localStorage.removeItem('luvoy-resume-' + id)
  savedResumeList.value = savedResumeList.value.filter(r => r.id !== id)
  saveResumeList()
  showToast('已删除', 'info')
}

function duplicateResume(id) {
  try {
    const data = localStorage.getItem('luvoy-resume-' + id)
    if (!data) return
    const newId = generateId()
    const entry = savedResumeList.value.find(r => r.id === id)
    const newName = (entry ? entry.name : '未命名简历') + ' 副本'
    localStorage.setItem('luvoy-resume-' + newId, data)
    savedResumeList.value.unshift({ id: newId, name: newName, updatedAt: Date.now() })
    saveResumeList()
    showToast('已复制', 'success')
  } catch {}
}

function saveCurrentResumeAs() {
  const newId = generateId()
  const data = JSON.parse(JSON.stringify(resume))
  localStorage.setItem('luvoy-resume-' + newId, JSON.stringify(data))
  currentResumeId.value = newId
  currentResumeName.value = currentResumeName.value + ' 副本'
  savedResumeList.value.unshift({ id: newId, name: currentResumeName.value, updatedAt: Date.now() })
  saveResumeList()
  localStorage.setItem('luvoy-current-resume-id', newId)
  showToast('已另存为新简历', 'success')
}

function confirmRenameCurrent() {
  if (renamingName.value.trim()) {
    currentResumeName.value = renamingName.value.trim()
    persistCurrentResume()
  }
  isRenamingCurrent.value = false
}

function formatSavedTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + ' 分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + ' 小时前'
  return d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate()
}

// 简历数据
const resume = reactive({
  basic: {
    name: '张小明',
    phone: '138****8888',
    email: 'zhangxm@example.com',
    avatar: ''
  },
  education: [
    {
      school: '清华大学',
      level: '985',
      tags: ['985', '211', '双一流'],
      major: '计算机科学与技术',
      degree: '本科',
      fullTime: '全日制',
      college: '计算机科学与技术学院',
      city: '北京',
      logo: '',
      logoSize: 48,
      startDate: '2021-09',
      endDate: '2025-06',
      ranking: '88.5/100 | GPA:3.75/4.00 专业前10%',
      courses: '数据结构(95)、算法分析(92)、操作系统(90)、计算机网络(88)、数据库原理(91)、软件工程(89)、人工智能导论(93)、机器学习(90)',
      description: ''
    }
  ],
  competitions: [
    { name: 'ACM国际大学生程序设计竞赛区域赛', level: '银牌', date: '2023-11' },
    { name: '全国大学生数学建模竞赛', level: '国家级二等奖', date: '2023-09' },
    { name: '中国大学生计算机设计大赛', level: '省级一等奖', date: '2024-05' },
    { name: '"挑战杯"全国大学生课外学术科技作品竞赛', level: '省级三等奖', date: '2024-03' }
  ],
  projects: [
    {
      name: 'SmartTask 智能任务管理系统',
      link: 'https://github.com/example/smart-task',
      impact: 'GitHub Star 200+，被多个技术社区推荐，日活用户1000+',
      techStack: 'Vue3 + TypeScript + Node.js + MongoDB',
      engineering: '采用前后端分离架构，实现CI/CD自动化部署，单元测试覆盖率85%+',
      description: '基于AI的智能任务分配与进度追踪系统，支持团队协作和数据可视化分析'
    }
  ],
  works: [],
  honors: [],
  skills: {
    professional: '',
    language: 'CET-6 550分',
    other: ''
  },
  customSections: []
})

// UI状态
const expandedSection = ref('basic')
const expandedEduIndex = ref(0) // 当前展开的教育经历索引
const expandedCompIndex = ref(0) // 当前展开的竞赛经历索引
const expandedProjIndex = ref(0) // 当前展开的项目经历索引
const expandedHonorIndex = ref(-1) // 当前展开的荣誉奖项索引
const expandedWorkIndex = ref(0) // 当前展开的实习经历索引
const selectedTemplate = ref('classic')
const zoomLevel = ref(85)
const autoSaveText = ref('已保存')
const isSaving = ref(false)
const showExportMenu = ref(false)
const showPreviewModal = ref(false)
const isDiagnosing = ref(false)
const avatarInput = ref(null)
const currentTab = ref('edit')
const resumeStyle = ref('simple')
const alignment = ref('left')
const showTitleStyles = ref(false)
const showTemplateMenu = ref(false)
const showModuleManager = ref(false)
const showFontMenu = ref(false)
const resumePreviewRef = ref(null)
const draggedModule = ref(null)

// 字体选项
const fontOptions = [
  { label: '思源黑体', value: "'Source Han Sans', 'Noto Sans SC', sans-serif" },
  { label: '宋体', value: "'SimSun', serif" },
  { label: '思源黑体', value: "'Noto Sans SC', sans-serif" },
  { label: '微软雅黑', value: "'Microsoft YaHei', 'PingFang SC', sans-serif" },
  { label: '楷体', value: "'KaiTi', '楷体', serif" }
]

const fontDisplayName = computed(() => {
  const font = fontOptions.find(f => f.value === styleSettings.fontFamily)
  return font ? font.label : '思源黑体'
})

function selectFont(font) {
  styleSettings.fontFamily = font.value
  showFontMenu.value = false
  showToast(`字体已切换为${font.label}`, 'success')
}

// 模块管理数据
const allModules = ref([
  { id: 'education', name: '教育经历', enabled: true, order: 1 },
  { id: 'honors', name: '荣誉奖项', enabled: true, order: 2 },
  { id: 'competition', name: '竞赛经历', enabled: true, order: 3 },
  { id: 'project', name: '项目经历', enabled: true, order: 4 },
  { id: 'summary', name: '个人总结', enabled: false, order: 5 },
  { id: 'work', name: '实习/工作经历', enabled: false, order: 10 },
  { id: 'organization', name: '社团和组织经历', enabled: false, order: 11 },
  { id: 'other', name: '其他', enabled: false, order: 12 },
  { id: 'research', name: '研究经历', enabled: false, order: 13 },
  { id: 'skills', name: '专业技能', enabled: true, order: 6 },
  { id: 'portfolio', name: '作品集', enabled: false, order: 14, premium: true },
  { id: 'custom', name: '自定义', enabled: false, order: 15 }
])

const enabledModules = computed(() => 
  allModules.value.filter(m => m.enabled).sort((a, b) => a.order - b.order)
)

const availableModules = computed(() => 
  allModules.value.filter(m => !m.enabled)
)

function openModuleManager() {
  showModuleManager.value = true
}

function addModule(mod) {
  mod.enabled = true
  mod.order = enabledModules.value.length + 1
  showToast(`已添加${mod.name}模块`, 'success')
  
  // 如果是自定义模块，添加一个新的自定义section
  if (mod.id === 'custom') {
    addCustomSection()
  }
}

function removeModule(mod) {
  mod.enabled = false
  showToast(`已移除${mod.name}模块`, 'info')
}

function editModule(mod) {
  showModuleManager.value = false
  // 跳转到编辑区并展开对应模块
  currentTab.value = 'edit'
  expandedSection.value = mod.id
}

function dragStart(event, mod) {
  draggedModule.value = mod
}

function drop(event, targetMod) {
  if (!draggedModule.value || draggedModule.value.id === targetMod.id) return
  
  const modules = enabledModules.value
  const fromIndex = modules.findIndex(m => m.id === draggedModule.value.id)
  const toIndex = modules.findIndex(m => m.id === targetMod.id)
  
  // 重新排序
  const temp = draggedModule.value.order
  draggedModule.value.order = targetMod.order
  targetMod.order = temp
  
  draggedModule.value = null
  showToast('模块顺序已调整', 'success')
}

// 工具栏功能
function smartOnePage() {
  // 智能压缩简历到一页 - 调整字体大小、行高和边距
  styleSettings.fontSize = 10
  styleSettings.lineHeight = 1.2
  styleSettings.margin = 'narrow'
  showToast('已优化为一页显示，字体调整为10px', 'success')
}

function setAlignment(align) {
  alignment.value = align
  showToast(`已设置${align === 'left' ? '左对齐' : align === 'center' ? '居中' : '右对齐'}`, 'info')
}

function toggleList() {
  showToast('列表样式已切换', 'info')
}

function toggleBorder() {
  showToast('边框样式已切换', 'info')
}

function toggleStripe() {
  showToast('条纹样式已切换', 'info')
}

// 侧边栏导航
const sidebarTabs = [
  { id: 'myresumes', name: '简历', icon: 'bi bi-folder2-open' },
  { id: 'edit', name: '编辑', icon: 'bi bi-pencil-square' },
  { id: 'template', name: '模板', icon: 'bi bi-grid' },
  { id: 'ai', name: '导师', icon: 'bi bi-robot' },
  { id: 'jobs', name: '职位', icon: 'bi bi-briefcase' }
]

// 简历模板
const resumeTemplates = [
  { id: 'classic', name: '经典简约', desc: '适合大多数岗位', color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  { id: 'modern', name: '现代风格', desc: '科技互联网', color: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)' },
  { id: 'elegant', name: '优雅专业', desc: '金融财务', color: 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)' },
  { id: 'creative', name: '创意设计', desc: '设计创意', color: 'linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)' }
]

// AI表单数据
const targetJob = reactive({
  title: '',
  category: '',
  experience: '',
  description: '',
  status: '',
  types: []
})
const experienceOptions = ['实习生', '应届生', '工作 1-3 年', '工作 4-5 年', '工作6年以上']
const jobTypes = ['非本专业求职', '跨行求职', '央国企求职', '外企求职']

function toggleJobType(type) {
  const idx = targetJob.types.indexOf(type)
  if (idx >= 0) targetJob.types.splice(idx, 1)
  else targetJob.types.push(type)
}

// 职位推荐数据
const recommendedJobs = ref([
  {
    id: 1,
    title: '算法工程师',
    company: '字节跳动',
    location: '北京',
    experience: '应届生',
    education: '本科',
    salary: '25-50K·15薪',
    matchRate: 95,
    skills: ['Python', '机器学习', '深度学习', 'PyTorch']
  },
  {
    id: 2,
    title: '后端开发工程师',
    company: '阿里巴巴',
    location: '杭州',
    experience: '1-3年',
    education: '本科',
    salary: '20-40K·16薪',
    matchRate: 92,
    skills: ['Java', 'Spring', 'MySQL', 'Redis']
  },
  {
    id: 3,
    title: 'AI产品经理',
    company: '腾讯',
    location: '深圳',
    experience: '应届生',
    education: '本科',
    salary: '18-35K·14薪',
    matchRate: 88,
    skills: ['AI', '产品设计', '数据分析']
  }
])

function goToJob(job) {
  router.push({ path: '/jobs', query: { id: job.id } })
}

function loadMoreJobs() {
  showToast('正在加载更多职位...', 'info')
}

function applyTemplate(templateId) {
  selectedTemplate.value = templateId
  showTemplateMenu.value = false
  
  // 根据模板设置不同的主题色和样式
  switch (templateId) {
    case 'classic':
      styleSettings.themeColor = '#667eea'
      styleSettings.fontFamily = "'Source Han Sans', 'Noto Sans SC', sans-serif"
      break
    case 'modern':
      styleSettings.themeColor = '#11998e'
      styleSettings.fontFamily = "'Microsoft YaHei', 'PingFang SC', sans-serif"
      break
    case 'elegant':
      styleSettings.themeColor = '#2193b0'
      styleSettings.fontFamily = "'SimSun', serif"
      break
    case 'creative':
      styleSettings.themeColor = '#ee0979'
      styleSettings.fontFamily = "'Noto Sans SC', sans-serif"
      break
  }
  
  showToast(`已应用「${resumeTemplates.find(t => t.id === templateId)?.name || templateId}」模板`, 'success')
}

// 撤销/重做
const historyStack = ref([])
const historyIndex = ref(-1)
const maxHistory = 50

const canUndo = computed(() => historyIndex.value > 0)
const canRedo = computed(() => historyIndex.value < historyStack.value.length - 1)

// 简历完成度计算
const completionRate = computed(() => {
  let total = 0
  let filled = 0
  
  // 基本信息 (20分)
  total += 20
  if (resume.basic.name) filled += 7
  if (resume.basic.phone) filled += 6
  if (resume.basic.email) filled += 5
  if (resume.basic.avatar) filled += 2
  
  // 教育经历 (20分)
  total += 20
  if (resume.education.length) {
    const edu = resume.education[0]
    if (edu.school) filled += 5
    if (edu.major) filled += 5
    if (edu.degree) filled += 3
    if (edu.ranking) filled += 4
    if (edu.courses) filled += 3
  }
  
  // 项目经历 (25分)
  total += 25
  if (resume.projects.length) {
    filled += 10
    const proj = resume.projects[0]
    if (proj.description) filled += 8
    if (proj.techStack) filled += 4
    if (proj.impact) filled += 3
  }
  
  // 竞赛经历 (15分)
  total += 15
  if (resume.competitions.length) {
    filled += Math.min(15, resume.competitions.length * 5)
  }
  
  // 技能特长 (10分)
  total += 10
  if (resume.skills.professional) filled += 5
  if (resume.skills.language) filled += 3
  if (resume.skills.other) filled += 2
  
  // 实习经历 (10分)
  total += 10
  if (resume.works.length) {
    filled += Math.min(10, resume.works.length * 5)
  }
  
  return Math.round((filled / total) * 100)
})

// 过滤掉空的竞赛经历
const validCompetitions = computed(() => {
  return resume.competitions.filter(comp => comp.name || comp.level)
})

// 过滤掉空的荣誉奖项
const validHonors = computed(() => {
  return resume.honors.filter(honor => honor.name)
})

// 过滤掉空的实习经历
const validWorks = computed(() => {
  return resume.works.filter(work => work.company || work.position)
})

// 过滤掉空的教育经历
const validEducation = computed(() => {
  return resume.education.filter(edu => edu.school || edu.major)
})

// 过滤掉空的项目经历
const validProjects = computed(() => {
  return resume.projects.filter(proj => proj.name)
})

const templates = [
  { id: 'classic', name: '经典简约' },
  { id: 'modern', name: '现代风格' },
  { id: 'elegant', name: '优雅专业' }
]

// AI助手状态
const isAIExpanded = ref(false)
const isAIThinking = ref(false)
const isAISpeaking = ref(false)
const aiInput = ref('')
const chatContainerRef = ref(null)
const showAIDiagnosis = ref(false)
const isHappy = ref(false)
const isWaving = ref(false)
const isDragging = ref(false)
const showIdleBubble = ref(false)
const idleBubbleText = ref('')
const showAgentMenu = ref(true)
const eyeState = ref('normal')
const mouthState = ref('normal')

// 拖拽相关
const agentPosX = ref(28)
const agentPosY = ref(28)
const agentDragStart = { x: 0, y: 0, posX: 0, posY: 0 }
let agentDragMoved = false

// 拖拽功能
function startAgentDrag(e) {
  if (isAIExpanded.value) return
  
  agentDragMoved = false
  agentDragStart.x = e.clientX
  agentDragStart.y = e.clientY
  agentDragStart.posX = agentPosX.value
  agentDragStart.posY = agentPosY.value
  
  document.addEventListener('mousemove', onAgentDrag)
  document.addEventListener('mouseup', endAgentDrag)
}

function onAgentDrag(e) {
  const dx = agentDragStart.x - e.clientX // 注意方向反转因为用的是right
  const dy = agentDragStart.y - e.clientY // 注意方向反转因为用的是bottom
  
  if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
    agentDragMoved = true
    isDragging.value = true
  }
  
  // 计算新位置，限制在视口内
  const newX = Math.max(10, Math.min(window.innerWidth - 100, agentDragStart.posX + dx))
  const newY = Math.max(10, Math.min(window.innerHeight - 100, agentDragStart.posY + dy))
  
  agentPosX.value = newX
  agentPosY.value = newY
}

function endAgentDrag() {
  document.removeEventListener('mousemove', onAgentDrag)
  document.removeEventListener('mouseup', endAgentDrag)
  
  setTimeout(() => {
    isDragging.value = false
  }, 50)
}

// 表情动作
function onAgentHover() {
  if (!isAIExpanded.value && !isDragging.value) {
    eyeState.value = 'happy'
    isHappy.value = true
    mouthState.value = 'smile'
  }
}

function onAgentLeave() {
  if (!isAIExpanded.value) {
    eyeState.value = 'normal'
    isHappy.value = false
    mouthState.value = 'normal'
  }
}

function showWaveAnimation() {
  isWaving.value = true
  isHappy.value = true
  eyeState.value = 'happy'
  mouthState.value = 'smile'
  setTimeout(() => {
    isWaving.value = false
    isHappy.value = false
    eyeState.value = 'normal'
    mouthState.value = 'normal'
  }, 1500)
}

// 闲聊气泡文案
const idleBubbles = [
  '简历写好了吗？我来帮你看看~',
  '点我优化简历，提升通过率！',
  '有什么问题随时问我哦 💬',
  '发现简历可以改进的地方！',
  '让我帮你打造一份完美简历 ✨',
  '简历写作有技巧，我来教你！',
  '准备好投递简历了吗？🚀'
]

// 定时显示闲聊气泡
let idleBubbleTimer = null
function startIdleBubble() {
  idleBubbleTimer = setInterval(() => {
    if (!isAIExpanded.value) {
      idleBubbleText.value = idleBubbles[Math.floor(Math.random() * idleBubbles.length)]
      showIdleBubble.value = true
      setTimeout(() => {
        showIdleBubble.value = false
      }, 5000)
    }
  }, 15000)
}

function handleAgentClick() {
  // 如果是拖拽操作就不触发点击
  if (!agentDragMoved && !isAIExpanded.value) {
    toggleAI()
  }
}

// 开始写简历引导
function startResumeGuide() {
  showAgentMenu.value = false
  aiMessages.value.push({
    role: 'assistant',
    content: '好的，让我们一步步来完善你的简历！🎯\n\n首先，请确认一下你的基本信息是否填写完整？\n\n姓名、电话、邮箱是必填项，头像可以让简历更加专业哦~',
    actions: [
      { id: 'check-basic', icon: 'bi bi-person', label: '去填写基本信息' },
      { id: 'next-step', icon: 'bi bi-arrow-right', label: '已填好，下一步' }
    ]
  })
  nextTick(scrollToBottom)
}

// 求职建议
function askCareerAdvice() {
  showAgentMenu.value = false
  aiMessages.value.push({
    role: 'assistant',
    content: '关于求职，给你几点关键建议：\n\n📝 简历篇\n1. 突出与岗位相关的经历\n2. 用数据量化成果（提升30%、节省2小时等）\n3. 简历控制在一页以内\n\n📧 投递篇\n1. 针对不同岗位定制简历\n2. 邮件标题格式：姓名-学校-应聘岗位\n3. 最佳投递时间：周二至周四上午\n\n💼 面试篇\n1. 提前了解公司和岗位\n2. 准备好自我介绍和项目介绍\n3. 准备几个问面试官的问题\n\n需要更详细的建议吗？',
    actions: [
      { id: 'resume-tips', icon: 'bi bi-file-text', label: '简历技巧' },
      { id: 'interview-tips', icon: 'bi bi-chat', label: '面试技巧' }
    ]
  })
  nextTick(scrollToBottom)
}

const aiMessages = ref([
  {
    role: 'assistant',
    content: '嗨！我是你的简历小助手 🤖\n\n有什么关于简历的问题都可以问我！\n我可以帮你：\n• 分析诊断简历\n• AI优化润色\n• 提供求职建议\n\n选择下方功能开始吧~'
  }
])

const quickReplies = ref([
  { id: 'check', icon: '🔍', text: '检查简历' },
  { id: 'optimize', icon: '✨', text: '全面优化' },
  { id: 'tips', icon: '💡', text: '投递建议' },
  { id: 'match', icon: '🎯', text: '岗位匹配' }
])

// 诊断数据
const diagnosisScore = ref(78)
const diagnosisIssues = ref([
  { 
    icon: 'bi bi-exclamation-triangle', 
    severity: 'warning',
    title: '技能特长未填写', 
    description: '缺少专业技能描述会降低HR筛选通过率',
    field: 'skills'
  },
  { 
    icon: 'bi bi-info-circle', 
    severity: 'info',
    title: '项目经历可以更详细', 
    description: '建议使用STAR法则描述项目中的具体贡献',
    field: 'projects'
  }
])

// Toast 提示
const toasts = ref([])
function showToast(message, type = 'success') {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3000)
}

// 方法
function toggleSection(section) {
  expandedSection.value = expandedSection.value === section ? '' : section
}

// 教育经历卡片展开/收起
function toggleEduExpand(index) {
  expandedEduIndex.value = expandedEduIndex.value === index ? -1 : index
}
function toggleCompExpand(index) {
  expandedCompIndex.value = expandedCompIndex.value === index ? -1 : index
}
function toggleProjExpand(index) {
  expandedProjIndex.value = expandedProjIndex.value === index ? -1 : index
}
function toggleHonorExpand(index) {
  expandedHonorIndex.value = expandedHonorIndex.value === index ? -1 : index
}
function toggleWorkExpand(index) {
  expandedWorkIndex.value = expandedWorkIndex.value === index ? -1 : index
}

function aiCheckSection(section, index) {
  showToast('正在分析内容...', 'info')
  setTimeout(() => {
    showToast('内容良好，无需修改', 'success')
  }, 1500)
}

// AI检查教育经历
function aiCheckEducation(index) {
  showToast('正在分析教育经历...', 'info')
  setTimeout(() => {
    showToast('教育经历内容良好，无需修改', 'success')
  }, 1500)
}

// 教育经历润色
function polishEducation(index) {
  showToast('正在润色教育经历...', 'info')
  setTimeout(() => {
    const edu = resume.education[index]
    if (!edu.description && (edu.ranking || edu.courses)) {
      // 自动生成描述内容
      let desc = ''
      if (edu.ranking) desc += `• 成绩排名：${edu.ranking}\n`
      if (edu.courses) desc += `• 主修课程：${edu.courses}`
      edu.description = desc
    }
    showToast('教育经历已优化', 'success')
    saveToHistory()
  }, 1500)
}

function addEducation() {
  resume.education.push({
    school: '', level: '', tags: [], major: '', degree: '本科',
    fullTime: '全日制', college: '', city: '', logo: '', logoSize: 48,
    startDate: '', endDate: '', ranking: '', courses: '', description: ''
  })
  expandedSection.value = 'education'
  saveToHistory()
}

// 校徽上传
const eduLogoInputs = ref({})
function triggerEduLogoUpload(index) {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => handleEduLogoUpload(e, index)
  input.click()
}

function handleEduLogoUpload(e, index) {
  const file = e.target.files[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    showToast('请上传图片文件', 'error')
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    showToast('图片大小不能超过 2MB', 'error')
    return
  }
  const reader = new FileReader()
  reader.onload = (ev) => {
    resume.education[index].logo = ev.target.result
    saveToHistory()
    showToast('校徽上传成功', 'success')
  }
  reader.readAsDataURL(file)
}

// 学校标签切换
const schoolTagOptions = ['985', '211', '双一流', 'C9']
function toggleSchoolTag(edu, tag) {
  if (!edu.tags) edu.tags = []
  const idx = edu.tags.indexOf(tag)
  if (idx >= 0) {
    edu.tags.splice(idx, 1)
  } else {
    edu.tags.push(tag)
  }
  // 同步 level 字段（取第一个 tag 作为主要层次）
  edu.level = edu.tags[0] || ''
}

function removeEducation(index) {
  resume.education.splice(index, 1)
  saveToHistory()
}

function addCompetition() {
  resume.competitions.push({ name: '', level: '', date: '' })
  expandedSection.value = 'competition'
  saveToHistory()
}

function removeCompetition(index) {
  resume.competitions.splice(index, 1)
  saveToHistory()
}

function addProject() {
  resume.projects.push({
    name: '', link: '', impact: '', techStack: '', engineering: '', description: ''
  })
  expandedSection.value = 'project'
  saveToHistory()
}

function removeProject(index) {
  resume.projects.splice(index, 1)
  saveToHistory()
}

function addHonor() {
  resume.honors.push({ name: '', date: '' })
  expandedSection.value = 'honors'
  saveToHistory()
}

function removeHonor(index) {
  resume.honors.splice(index, 1)
  saveToHistory()
}

function addWork() {
  resume.works.push({
    company: '', position: '', department: '', startDate: '', endDate: '', description: ''
  })
  expandedSection.value = 'work'
  saveToHistory()
}

function removeWork(index) {
  resume.works.splice(index, 1)
  saveToHistory()
}

// 清空整个模块
function clearSection(sectionKey) {
  switch (sectionKey) {
    case 'education':
      resume.education.splice(0, resume.education.length)
      break
    case 'competitions':
      resume.competitions.splice(0, resume.competitions.length)
      break
    case 'projects':
      resume.projects.splice(0, resume.projects.length)
      break
    case 'honors':
      resume.honors.splice(0, resume.honors.length)
      break
    case 'works':
      resume.works.splice(0, resume.works.length)
      break
    case 'skills':
      resume.skills.professional = ''
      resume.skills.language = ''
      resume.skills.other = ''
      break
  }
  saveToHistory()
  const nameMap = {
    education: '教育经历',
    competitions: '竞赛经历',
    projects: '项目经历',
    honors: '荣誉奖项',
    works: '实习经历',
    skills: '技能特长'
  }
  showToast(`已清空「${nameMap[sectionKey] || sectionKey}」`, 'info')
}

// 自定义模块管理
function addCustomSection() {
  resume.customSections.push({
    title: '',
    content: ''
  })
  expandedSection.value = 'custom-' + (resume.customSections.length - 1)
  saveToHistory()
  showToast('已添加自定义模块', 'success')
}

function removeCustomSection(index) {
  resume.customSections.splice(index, 1)
  saveToHistory()
  showToast('已删除自定义模块', 'info')
}

function formatDate(date) {
  if (!date) return ''
  const [year, month] = date.split('-')
  return `${year}年${month}月`
}

// 历史记录管理
function saveToHistory() {
  const state = JSON.stringify(resume)
  // 如果当前不在历史末尾，删除后面的记录
  if (historyIndex.value < historyStack.value.length - 1) {
    historyStack.value = historyStack.value.slice(0, historyIndex.value + 1)
  }
  historyStack.value.push(state)
  if (historyStack.value.length > maxHistory) {
    historyStack.value.shift()
  }
  historyIndex.value = historyStack.value.length - 1
}

function undo() {
  if (!canUndo.value) return
  historyIndex.value--
  const state = JSON.parse(historyStack.value[historyIndex.value])
  Object.assign(resume, state)
  showToast('已撤销', 'info')
}

function redo() {
  if (!canRedo.value) return
  historyIndex.value++
  const state = JSON.parse(historyStack.value[historyIndex.value])
  Object.assign(resume, state)
  showToast('已重做', 'info')
}

function saveResume() {
  isSaving.value = true
  autoSaveText.value = '保存中...'
  
  setTimeout(() => {
    persistCurrentResume()
    isSaving.value = false
    autoSaveText.value = '已保存'
    showToast('简历已保存', 'success')
  }, 300)
}

function exportPDF() {
  showExportMenu.value = false
  showToast('正在生成 PDF...', 'info')
  
  const previewCard = document.querySelector('.resume-preview-card')
  if (!previewCard) {
    showToast('无法找到简历预览元素', 'error')
    return
  }
  
  // 临时重置缩放和设置一页所需样式
  const originalTransform = previewCard.style.transform
  const originalFontSize = previewCard.style.fontSize
  const originalLineHeight = previewCard.style.lineHeight
  const originalPadding = previewCard.style.padding
  
  // 强制单页设置
  previewCard.style.transform = 'scale(1)'
  previewCard.style.fontSize = '10px'
  previewCard.style.lineHeight = '1.2'
  previewCard.style.padding = '25px'
  
  // 等待样式应用
  setTimeout(() => {
    html2canvas(previewCard, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      height: 297 * 3.78, // A4高度 297mm 转换为像素 (约1122px)
      windowHeight: 297 * 3.78
    }).then(canvas => {
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      })
      
      const pageWidth = 210
      const pageHeight = 297
      
      // 计算图片在A4页面上的尺寸，强制缩放到一页
      const imgWidth = pageWidth
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      
      // 如果图片高度超过一页，则缩放以适应
      let finalWidth = imgWidth
      let finalHeight = imgHeight
      
      if (imgHeight > pageHeight) {
        const scale = pageHeight / imgHeight
        finalWidth = imgWidth * scale
        finalHeight = pageHeight
      }
      
      // 居中放置
      const xOffset = (pageWidth - finalWidth) / 2
      const yOffset = 0
      
      pdf.addImage(imgData, 'PNG', xOffset, yOffset, finalWidth, finalHeight)
      
      const fileName = `简历_${resume.basic.name || '未命名'}_${new Date().toLocaleDateString().replace(/\//g, '-')}.pdf`
      pdf.save(fileName)
      
      // 恢复原始样式
      previewCard.style.transform = originalTransform
      previewCard.style.fontSize = originalFontSize
      previewCard.style.lineHeight = originalLineHeight
      previewCard.style.padding = originalPadding
      
      showToast('PDF 导出成功（单页）', 'success')
    }).catch(err => {
      console.error('PDF导出失败:', err)
      previewCard.style.transform = originalTransform
      previewCard.style.fontSize = originalFontSize
      previewCard.style.lineHeight = originalLineHeight
      previewCard.style.padding = originalPadding
      showToast('PDF 导出失败', 'error')
    })
  }, 100)
}

function exportWord() {
  showExportMenu.value = false
  showToast('正在生成 Word 文档...', 'info')
  setTimeout(() => {
    showToast('Word 导出成功', 'success')
  }, 1500)
}

function exportJSON() {
  showExportMenu.value = false
  const dataStr = JSON.stringify(resume, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `简历_${resume.basic.name || '未命名'}_${new Date().toLocaleDateString()}.json`
  a.click()
  URL.revokeObjectURL(url)
  showToast('JSON 导出成功', 'success')
}

function importFromFile() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json,.pdf,.docx'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    if (file.name.endsWith('.json')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result)
          Object.assign(resume, data)
          saveToHistory()
          showToast('简历导入成功', 'success')
        } catch {
          showToast('文件格式错误', 'error')
        }
      }
      reader.readAsText(file)
    } else {
      showToast('正在解析简历文件...', 'info')
      // TODO: 实现PDF/Word解析
    }
  }
  input.click()
}

function useTemplate() {
  showToast('模板功能开发中...', 'info')
}

// 头像上传
function triggerAvatarUpload() {
  avatarInput.value?.click()
}

function handleAvatarUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    showToast('请上传图片文件', 'error')
    return
  }
  
  if (file.size > 5 * 1024 * 1024) {
    showToast('图片大小不能超过 5MB', 'error')
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    resume.basic.avatar = e.target.result
    saveToHistory()
    showToast('头像上传成功', 'success')
  }
  reader.readAsDataURL(file)
}

// AI诊断
function runAIDiagnosis() {
  isDiagnosing.value = true
  
  setTimeout(() => {
    isDiagnosing.value = false
    
    // 重新计算诊断结果
    const issues = []
    let score = 100
    
    if (!resume.skills.professional) {
      issues.push({
        icon: 'bi bi-exclamation-triangle',
        severity: 'warning',
        title: '技能特长未填写',
        description: '缺少专业技能描述会降低HR筛选通过率',
        field: 'skills'
      })
      score -= 10
    }
    
    if (resume.projects.length === 0) {
      issues.push({
        icon: 'bi bi-exclamation-circle',
        severity: 'error',
        title: '缺少项目经历',
        description: '项目经历是展示实践能力的关键',
        field: 'projects'
      })
      score -= 15
    } else if (resume.projects.some(p => !p.description || p.description.length < 50)) {
      issues.push({
        icon: 'bi bi-info-circle',
        severity: 'info',
        title: '项目描述可以更详细',
        description: '建议使用STAR法则描述项目中的具体贡献',
        field: 'projects'
      })
      score -= 5
    }
    
    if (resume.works.length === 0) {
      issues.push({
        icon: 'bi bi-info-circle',
        severity: 'info',
        title: '暂无实习经历',
        description: '实习经历能大幅提升简历竞争力',
        field: 'work'
      })
      score -= 8
    }
    
    if (!resume.basic.avatar) {
      issues.push({
        icon: 'bi bi-person',
        severity: 'info',
        title: '建议添加证件照',
        description: '专业的证件照能提升第一印象',
        field: 'basic'
      })
      score -= 2
    }
    
    diagnosisScore.value = Math.max(0, score)
    diagnosisIssues.value = issues
    showAIDiagnosis.value = true
  }, 1500)
}

// AI助手方法
function toggleAI() {
  isAIExpanded.value = !isAIExpanded.value
}

async function sendAIMessage() {
  if (!aiInput.value.trim()) return
  
  const userMsg = aiInput.value.trim()
  aiMessages.value.push({ role: 'user', content: userMsg })
  aiInput.value = ''
  
  isAIThinking.value = true
  await nextTick()
  scrollToBottom()
  
  // 模拟AI响应
  setTimeout(() => {
    isAIThinking.value = false
    aiMessages.value.push({
      role: 'assistant',
      content: generateAIResponse(userMsg)
    })
    nextTick(scrollToBottom)
  }, 1500)
}

function sendQuickReply(reply) {
  aiMessages.value.push({ role: 'user', content: reply.text })
  
  isAIThinking.value = true
  
  setTimeout(() => {
    isAIThinking.value = false
    let response = ''
    let actions = []
    
    switch (reply.id) {
      case 'check':
        response = `我来帮你检查一下简历...\n\n${resume.basic.name ? '✅' : '⚠️'} 基本信息${resume.basic.name ? '完整' : '不完整'}\n${resume.education.length ? '✅' : '⚠️'} 教育经历${resume.education.length ? '已填写' : '未填写'}\n${resume.skills.professional ? '✅' : '⚠️'} 技能特长${resume.skills.professional ? '已填写' : '未填写'}\n${resume.works.length ? '✅' : '⚠️'} 实习经历${resume.works.length ? '已填写' : '为空'}\n\n当前完成度 ${completionRate.value}%`
        if (!resume.skills.professional || !resume.works.length) {
          actions = [
            { id: 'add-skills', icon: 'bi bi-tools', label: '补充技能' },
            { id: 'add-work', icon: 'bi bi-briefcase', label: '添加实习' }
          ]
        }
        break
      case 'optimize':
        response = '好的，我来帮你全面优化简历！\n\n📝 优化建议：\n1. 项目描述增加量化数据\n2. 竞赛经历标注含金量\n3. 添加与目标岗位相关的技能\n\n需要我帮你逐一优化吗？'
        actions = [
          { id: 'auto-optimize', icon: 'bi bi-magic', label: '一键优化' }
        ]
        break
      case 'tips':
        response = '关于简历投递，这里有几点建议：\n\n🎯 针对不同岗位定制简历重点\n📧 邮件标题格式：姓名-学校-应聘岗位\n⏰ 最佳投递时间：周二至周四上午\n📎 PDF格式更通用\n\n需要我帮你针对特定岗位优化简历吗？'
        break
      case 'match':
        response = '根据你的背景，以下岗位匹配度较高：\n\n🔥 算法工程师（匹配度95%）\n🔥 后端开发工程师（匹配度92%）\n🔥 AI产品经理（匹配度88%）\n\n要我帮你针对这些岗位优化简历吗？'
        actions = [
          { id: 'target-algo', icon: 'bi bi-cpu', label: '算法工程师' },
          { id: 'target-backend', icon: 'bi bi-code-slash', label: '后端开发' }
        ]
        break
    }
    
    aiMessages.value.push({ role: 'assistant', content: response, actions })
    nextTick(scrollToBottom)
  }, 1200)
}

function handleAIAction(action) {
  showAgentMenu.value = false
  switch (action.id) {
    case 'check-basic':
      currentTab.value = 'edit'
      expandedSection.value = 'basic'
      toggleAI()
      break
    case 'next-step':
      aiMessages.value.push({
        role: 'assistant',
        content: '很好！基本信息已完善 ✅\n\n接下来，让我们看看你的教育经历。\n\n对于校招来说，教育经历很重要！建议填写：\n• 学校、专业、学历\n• GPA/排名（如果优秀的话）\n• 主修课程（与目标岗位相关的）',
        actions: [
          { id: 'check-education', icon: 'bi bi-mortarboard', label: '填写教育经历' },
          { id: 'next-project', icon: 'bi bi-arrow-right', label: '已填好，下一步' }
        ]
      })
      break
    case 'check-education':
      currentTab.value = 'edit'
      expandedSection.value = 'education'
      toggleAI()
      break
    case 'next-project':
      aiMessages.value.push({
        role: 'assistant',
        content: '教育经历完成！✅\n\n现在是重头戏——项目经历！\n\n这是简历中最能展示你能力的部分。建议：\n• 2-3个高质量项目即可\n• 用数据量化成果\n• 描述技术栈和你的贡献\n\n需要我帮你润色项目描述吗？',
        actions: [
          { id: 'optimize-project', icon: 'bi bi-magic', label: '润色项目描述' },
          { id: 'check-project', icon: 'bi bi-folder', label: '自己填写' }
        ]
      })
      break
    case 'check-project':
      currentTab.value = 'edit'
      expandedSection.value = 'project'
      toggleAI()
      break
    case 'resume-tips':
      aiMessages.value.push({
        role: 'assistant',
        content: '📝 简历撰写技巧：\n\n1. 一页原则 - 应届生简历不超过一页\n\n2. 量化成果 - 用数字说话\n   ❌ 负责项目开发\n   ✅ 独立开发XX系统，提升效率30%\n\n3. 关键词匹配 - 简历要包含JD中的关键词\n\n4. 倒序原则 - 最新的经历放最前面\n\n5. 突出重点 - 与岗位最相关的经历详写\n\n需要我帮你检查简历是否符合这些原则吗？',
        actions: [
          { id: 'check', icon: 'bi bi-search', label: '检查我的简历' }
        ]
      })
      break
    case 'interview-tips':
      aiMessages.value.push({
        role: 'assistant',
        content: '💼 面试技巧分享：\n\n自我介绍（1-2分钟）\n• 学历背景\n• 核心技能和经历\n• 为什么想加入\n\n项目介绍\n• 项目背景和目标\n• 你负责什么\n• 遇到什么难题，如何解决\n• 最终成果\n\n常见问题\n• 为什么选择我司？\n• 你的优缺点是什么？\n• 职业规划是什么？\n\n面试官问你"有什么问题"时\n可以问：\n• 团队的技术栈\n• 新人的培养计划\n• 部门的业务方向'
      })
      break
    case 'add-skills':
      expandedSection.value = 'skills'
      currentTab.value = 'edit'
      toggleAI()
      aiMessages.value.push({
        role: 'assistant',
        content: '我已经帮你定位到技能特长模块。\n\n💡 建议填写：\n1. 编程语言：Python、Java、C++等\n2. 框架工具：PyTorch、TensorFlow、Vue等\n3. 专业技能：机器学习、深度学习、数据结构等\n\n要我根据你的项目经历自动生成技能列表吗？',
        actions: [{ id: 'auto-skills', icon: 'bi bi-magic', label: '自动生成技能' }]
      })
      break
    case 'add-work':
      expandedSection.value = 'work'
      currentTab.value = 'edit'
      addWork()
      aiMessages.value.push({
        role: 'assistant',
        content: '已为你添加实习经历模块。\n\n📝 填写建议：\n1. 公司和职位要准确\n2. 使用STAR法则描述工作内容\n3. 突出你的贡献和成果\n\n如果还没有实习经历，可以填写校内项目或志愿服务经历。'
      })
      break
    case 'optimize-project':
      expandedSection.value = 'project'
      aiMessages.value.push({
        role: 'assistant',
        content: '我来帮你优化项目经历描述！\n\n你的 QQ-FARM-BOT 项目很不错，建议优化为：\n\n研究方向：自动化工具开发、实时系统设计\n方法创新：基于事件驱动的任务调度架构\n核心成果：GitHub 160+ Stars，被多个社区转载\n\n需要我帮你更新描述吗？',
        actions: [{ id: 'apply-project-opt', icon: 'bi bi-check', label: '应用优化' }]
      })
      break
    case 'auto-skills':
      resume.skills.professional = '熟练掌握Python、Java、JavaScript、C++等编程语言；精通机器学习、深度学习算法；熟悉PyTorch、TensorFlow等深度学习框架；熟悉Vue.js、Node.js等Web开发技术栈；具备良好的数据结构与算法基础'
      saveToHistory()
      showToast('技能已自动生成', 'success')
      aiMessages.value.push({
        role: 'assistant',
        content: '✅ 已根据你的项目经历自动生成技能特长描述！\n\n你可以在左侧编辑区查看并调整。'
      })
      break
    case 'auto-optimize':
      applyAllSuggestions()
      break
    case 'apply-project-opt':
      if (resume.projects.length > 0) {
        resume.projects[0].description = '基于Node.js + Vue3技术栈开发的多账号农场自动化管理系统。\n\n• 设计并实现事件驱动的任务调度引擎，支持多账号并发任务管理\n• 构建实时日志系统与可视化控制台，提升运维效率\n• 项目获得GitHub 160+ Stars，被多个技术社区推荐转载'
        saveToHistory()
        showToast('项目描述已优化', 'success')
      }
      aiMessages.value.push({
        role: 'assistant',
        content: '✅ 项目描述已优化！使用了更专业的描述方式和量化数据。'
      })
      break
  }
  nextTick(scrollToBottom)
}

function generateAIResponse(userMsg) {
  const lowerMsg = userMsg.toLowerCase()
  
  if (lowerMsg.includes('项目')) {
    return '关于项目经历，建议你：\n\n1. 用数据量化成果（如：提升30%效率）\n2. 突出技术难点和解决方案\n3. 说明你在团队中的角色\n\n需要我帮你优化具体的项目描述吗？'
  }
  if (lowerMsg.includes('技能') || lowerMsg.includes('skill')) {
    return `根据你的教育背景和项目经历，建议补充以下技能：\n\n编程语言：Python、Java、JavaScript\n开发框架：Vue、Node.js、PyTorch\n专业技能：机器学习、数据结构与算法\n\n要我帮你自动生成技能描述吗？`
  }
  if (lowerMsg.includes('实习') || lowerMsg.includes('工作')) {
    return '关于实习经历：\n\n如果有实习经历，建议使用STAR法则描述：\nS-情境：当时的背景\nT-任务：你的职责\nA-行动：你做了什么\nR-结果：取得的成果\n\n如果暂无实习，可以突出项目经历和竞赛经历。'
  }
  if (lowerMsg.includes('薪资') || lowerMsg.includes('工资')) {
    return '根据你的背景（211本科+AI专业+竞赛经历），预估薪资范围：\n\n🏠 一线城市：18-30K/月\n🏙️ 新一线城市：15-25K/月\n📍 二线城市：12-20K/月\n\n具体薪资取决于岗位类型和公司规模。'
  }
  
  return '好的，我已经记录下你的需求。还有什么我可以帮助你的吗？😊\n\n你可以问我：\n• 如何优化简历\n• 投递建议\n• 岗位匹配\n• 薪资预估'
}

function scrollToBottom() {
  if (chatContainerRef.value) {
    chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight
  }
}

function applyAISuggestion(issue) {
  expandedSection.value = issue.field
  showAIDiagnosis.value = false
  
  // 展开AI助手并给出建议
  isAIExpanded.value = true
  aiMessages.value.push({
    role: 'assistant',
    content: `我来帮你优化"${issue.title}"这个问题！\n\n${issue.description}\n\n让我为你生成优化建议...`
  })
}

function applyAllSuggestions() {
  showAIDiagnosis.value = false
  isAIExpanded.value = true
  isAIThinking.value = true
  
  setTimeout(() => {
    isAIThinking.value = false
    
    // 自动优化
    if (!resume.skills.professional) {
      resume.skills.professional = '熟练掌握Python、Java、C++等编程语言；精通机器学习、深度学习算法；熟悉PyTorch、TensorFlow框架；具备良好的数据结构与算法基础'
    }
    
    // 优化项目描述
    if (resume.projects.length > 0 && (!resume.projects[0].description || resume.projects[0].description.length < 100)) {
      resume.projects[0].description = '基于Node.js + Vue3技术栈开发的多账号农场自动化管理系统。\n\n• 设计并实现事件驱动的任务调度引擎，支持多账号并发任务管理\n• 构建实时日志系统与可视化控制台，提升运维效率\n• 项目获得GitHub 160+ Stars，被多个技术社区推荐转载'
    }
    
    saveToHistory()
    
    aiMessages.value.push({
      role: 'assistant',
      content: '✅ 一键优化完成！\n\n已为你完成以下优化：\n• 生成技能特长描述\n• 优化项目经历描述\n\n请查看左侧编辑区的变化，确认后点击保存即可！'
    })
    
    showToast('一键优化完成', 'success')
    nextTick(scrollToBottom)
  }, 2000)
}

// AI润色功能
function polishSection(section) {
  showAIPolish.value = false
  showToast('正在AI润色...', 'info')
  
  setTimeout(() => {
    switch (section) {
      case 'projects':
        if (resume.projects.length > 0) {
          resume.projects.forEach((proj, idx) => {
            if (proj.name && (!proj.description || proj.description.length < 100)) {
              proj.description = `基于${proj.techStack || '全栈技术'}开发的${proj.name}。\n\n• 采用模块化架构设计，实现高内聚低耦合的代码组织\n• ${proj.impact ? '项目' + proj.impact : '具备良好的用户体验和性能表现'}\n• ${proj.engineering || '完整交付生产级别代码，包含完善的测试与文档'}`
            }
          })
        }
        showToast('项目经历润色完成', 'success')
        break
      case 'works':
        if (resume.works.length > 0) {
          resume.works.forEach(work => {
            if (work.company && (!work.description || work.description.length < 50)) {
              work.description = `在${work.department || '技术部门'}担任${work.position || '技术岗位'}，主要负责：\n\n• 【背景】承担核心业务模块的开发与维护工作\n• 【任务】负责需求分析、技术方案设计与实现\n• 【行动】主导代码评审，推动团队代码规范建设\n• 【成果】按时高质量完成多个重要项目交付`
            }
          })
        }
        showToast('实习经历润色完成', 'success')
        break
      case 'skills':
        if (!resume.skills.professional) {
          const techStack = resume.projects
            .map(p => p.techStack)
            .filter(Boolean)
            .join('、')
          resume.skills.professional = `熟练掌握${techStack || 'Python、Java、JavaScript等编程语言'}；具备扎实的数据结构与算法基础；熟悉机器学习、深度学习相关技术；具备良好的代码规范意识和团队协作能力`
        }
        showToast('技能特长润色完成', 'success')
        break
    }
    saveToHistory()
  }, 1500)
}

function polishAll() {
  showAIPolish.value = false
  showToast('正在全面润色简历...', 'info')
  
  setTimeout(() => {
    polishSection('skills')
    setTimeout(() => {
      polishSection('projects')
      setTimeout(() => {
        polishSection('works')
        showToast('全部润色完成！', 'success')
      }, 500)
    }, 500)
  }, 1000)
}

// 键盘快捷键
function handleKeydown(e) {
  // Ctrl+S 保存
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    saveResume()
  }
  // Ctrl+Z 撤销
  if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
    e.preventDefault()
    undo()
  }
  // Ctrl+Y 或 Ctrl+Shift+Z 重做
  if ((e.ctrlKey && e.key === 'y') || (e.ctrlKey && e.shiftKey && e.key === 'z')) {
    e.preventDefault()
    redo()
  }
}

// 点击外部关闭下拉菜单
function handleClickOutside(e) {
  // 导出菜单
  if (showExportMenu.value && !e.target.closest('.export-menu') && !e.target.closest('[class*="bi-download"]')) {
    showExportMenu.value = false
  }
  // 字体菜单
  if (showFontMenu.value && !e.target.closest('.font-dropdown') && !e.target.closest('.toolbar-select-wrapper')) {
    showFontMenu.value = false
  }
  // 模板菜单
  if (showTemplateMenu.value && !e.target.closest('.toolbar-dropdown')) {
    showTemplateMenu.value = false
  }
}

// 初始化
onMounted(() => {
  // 加载简历列表
  loadResumeList()
  
  // 恢复上次编辑的简历
  const lastId = localStorage.getItem('luvoy-current-resume-id')
  if (lastId) {
    try {
      const data = JSON.parse(localStorage.getItem('luvoy-resume-' + lastId))
      if (data) {
        Object.assign(resume, data)
        currentResumeId.value = lastId
        const entry = savedResumeList.value.find(r => r.id === lastId)
        currentResumeName.value = entry ? entry.name : '未命名简历'
      }
    } catch {}
  }
  // 兼容旧单简历数据迁移
  if (!currentResumeId.value) {
    const oldSaved = localStorage.getItem('luvoy-resume')
    if (oldSaved) {
      try { Object.assign(resume, JSON.parse(oldSaved)) } catch {}
    }
    currentResumeId.value = generateId()
    currentResumeName.value = resume.basic.name ? resume.basic.name + '的简历' : '未命名简历'
    persistCurrentResume()
  }
  
  // 初始化历史记录
  saveToHistory()
  
  // 绑定快捷键
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('click', handleClickOutside)
  
  // 启动闲聊气泡
  startIdleBubble()
  
  // 初始显示一次气泡
  setTimeout(() => {
    if (!isAIExpanded.value) {
      idleBubbleText.value = '嗨！需要帮你写简历吗？点我开始~'
      showIdleBubble.value = true
      setTimeout(() => { showIdleBubble.value = false }, 5000)
    }
  }, 3000)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('click', handleClickOutside)
  if (idleBubbleTimer) clearInterval(idleBubbleTimer)
})

// 自动保存（防抖）
let autoSaveTimer = null
watch(resume, () => {
  isSaving.value = true
  autoSaveText.value = '保存中...'
  clearTimeout(autoSaveTimer)
  autoSaveTimer = setTimeout(() => {
    persistCurrentResume()
    isSaving.value = false
    autoSaveText.value = '已保存'
  }, 1000)
}, { deep: true })
</script>

<style scoped>
/* ═══ 侧边栏 ═══ */
.sidebar-icon-btn {
  @apply w-12 h-14 flex flex-col items-center justify-center rounded-xl text-brand-muted 
         hover:bg-brand-bg hover:text-brand-text transition cursor-pointer;
}
.sidebar-icon-btn.active {
  @apply bg-violet-600/20 text-violet-400;
}
.sidebar-icon-btn.ai-btn {
  @apply hover:bg-orange-500/20 hover:text-orange-400;
}

/* ═══ 工具栏 ═══ */
.toolbar-item {
  @apply flex items-center px-2.5 py-1.5 rounded-lg bg-brand-bg border border-brand-border text-xs text-brand-text
         hover:border-violet-500 transition cursor-pointer relative;
}
.toolbar-icon-btn {
  @apply w-8 h-8 rounded-lg bg-brand-bg border border-brand-border text-brand-muted
         hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center;
}
.toolbar-icon-btn.active {
  @apply bg-violet-600 border-violet-600 text-white;
}
.toolbar-divider {
  @apply w-px h-6 bg-brand-border mx-1;
}
.toolbar-inline-select {
  @apply bg-transparent text-xs text-brand-text outline-none cursor-pointer appearance-none pr-4;
}
.toolbar-dropdown {
  @apply absolute top-full left-0 mt-1 w-32 bg-brand-card border border-brand-border rounded-lg shadow-xl z-50 overflow-hidden;
}
.dropdown-item {
  @apply w-full px-3 py-2 text-left text-xs text-brand-text hover:bg-brand-surface transition;
}
.new-badge {
  @apply absolute -top-1 -right-1 px-1 py-0.5 text-[8px] bg-orange-500 text-white rounded font-bold;
}
.toolbar-select {
  @apply px-2 py-1 rounded-lg bg-brand-bg border border-brand-border text-xs text-brand-text
         focus:border-violet-500 focus:outline-none cursor-pointer;
}
.toolbar-btn {
  @apply w-7 h-7 rounded-lg bg-brand-bg border border-brand-border text-brand-muted text-sm
         hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center
         disabled:opacity-30 disabled:cursor-not-allowed;
}
.zoom-btn {
  @apply w-8 h-8 rounded-lg backdrop-blur border border-brand-border text-brand-muted
         hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center;
  background: rgba(30, 41, 59, 0.8);
}

/* ═══ 模板卡片 ═══ */
.template-card {
  @apply p-3 rounded-xl bg-brand-surface cursor-pointer transition;
  border: 2px solid transparent;
}
.template-card:hover {
  border-color: #3b82f6;
}
.template-card.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
.template-preview {
  @apply h-32 rounded-lg mb-3 relative overflow-hidden;
}
.template-lines {
  @apply absolute inset-4;
  background: repeating-linear-gradient(
    180deg,
    rgba(255,255,255,0.3) 0px,
    rgba(255,255,255,0.3) 4px,
    transparent 4px,
    transparent 12px
  );
}
.template-info {
  @apply flex flex-col gap-0.5;
}

/* ═══ AI表单 ═══ */
.ai-form-group {
  @apply mb-4;
}
.ai-form-label {
  @apply block text-xs text-brand-muted mb-2;
}
.ai-form-input {
  @apply w-full px-3 py-2 rounded-lg bg-brand-bg border border-brand-border text-sm text-brand-text
         placeholder-brand-muted focus:border-violet-500 focus:outline-none transition;
}
.exp-tag {
  @apply px-3 py-1.5 rounded-lg bg-brand-bg border border-brand-border text-xs text-brand-muted
         hover:border-violet-500 hover:text-violet-400 transition cursor-pointer;
}
.exp-tag.active {
  @apply bg-violet-600 border-violet-600 text-white;
}

/* ═══ 职位推荐卡片 ═══ */
.job-card {
  @apply p-4 rounded-xl bg-brand-surface border border-brand-border cursor-pointer transition
         hover:border-violet-500 hover:shadow-lg;
}
.job-match {
  @apply px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs;
}
.job-tag {
  @apply px-2 py-0.5 rounded-full bg-brand-bg text-brand-muted text-xs;
}
.skill-tag {
  @apply px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-400 text-xs;
}

/* ═══ 快捷操作按钮 ═══ */
.quick-action-btn {
  @apply px-3 py-2 rounded-lg bg-brand-surface border border-brand-border text-sm text-brand-muted
         hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center;
}
.ai-polish-btn {
  @apply bg-gradient-to-r from-violet-600 to-purple-600 border-0 text-white hover:from-violet-500 hover:to-purple-500;
}

/* ═══ 版式设置面板 ═══ */
.style-panel {
  @apply bg-brand-surface rounded-xl border border-brand-border overflow-hidden;
}
.style-panel-header {
  @apply flex items-center justify-between px-4 py-3 border-b border-brand-border;
}
.style-panel-body {
  @apply p-4 space-y-4;
}
.style-row {
  @apply flex items-center justify-between;
}
.style-label {
  @apply text-xs text-brand-muted;
}
.style-select {
  @apply px-3 py-1.5 rounded-lg bg-brand-bg border border-brand-border text-sm text-brand-text
         focus:border-violet-500 focus:outline-none cursor-pointer;
}
.style-btn {
  @apply w-7 h-7 rounded-lg bg-brand-bg border border-brand-border text-brand-text text-sm
         hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center;
}

/* 下滑动画 */
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from, .slide-down-leave-to {
  transform: translateY(-10px);
  opacity: 0;
  max-height: 0;
}
.slide-down-enter-to, .slide-down-leave-from {
  max-height: 300px;
}

/* ═══ 导出菜单 ═══ */
.export-menu {
  @apply absolute top-full right-0 mt-1 w-40 bg-brand-card border border-brand-border rounded-lg 
         shadow-xl overflow-hidden z-50;
}
.export-item {
  @apply w-full px-3 py-2 text-left text-sm text-brand-text hover:bg-brand-surface transition
         flex items-center;
}

/* ═══ AI诊断卡片 ═══ */
.ai-diagnosis-card {
  @apply rounded-xl p-4 cursor-pointer transition-all;
  background: linear-gradient(135deg, #f97316, #ea580c);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.3);
}
.ai-diagnosis-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(249, 115, 22, 0.4);
}

/* ═══ 编辑区样式 ═══ */
.edit-field {
  @apply space-y-1;
}
.edit-label {
  @apply text-xs text-brand-muted block;
}
.edit-input {
  @apply w-full px-3 py-2 rounded-lg bg-brand-bg border border-brand-border text-sm text-brand-text 
         placeholder-brand-muted focus:border-violet-500 focus:outline-none transition;
}
.add-item-btn {
  @apply w-full py-3 rounded-lg border-2 border-dashed border-brand-border text-brand-muted 
         text-sm hover:border-violet-500 hover:text-violet-400 transition flex items-center justify-center;
}

/* ═══ 教育经历卡片新样式 ═══ */
.education-card {
  @apply rounded-xl bg-brand-bg border border-brand-border mb-3 overflow-hidden;
}
.edu-card-header {
  @apply flex items-center justify-between px-4 py-3 cursor-pointer 
         hover:bg-slate-800/30 transition select-none;
}
.edu-card-body {
  @apply px-4 pb-4 border-t border-brand-border pt-4;
}
.school-logo-upload {
  @apply w-14 h-14 rounded-lg bg-brand-surface border border-brand-border flex items-center justify-center 
         cursor-pointer hover:border-violet-500 transition overflow-hidden;
}
.school-tag-btn {
  @apply px-4 py-1.5 rounded-full border border-brand-border text-sm text-brand-muted
         hover:border-violet-500 hover:text-violet-400 transition cursor-pointer;
}
.school-tag-btn.active-blue {
  @apply bg-blue-600 border-blue-600 text-white;
}
.school-tag-btn.active-orange {
  @apply bg-orange-500 border-orange-500 text-white;
}
.edu-ai-btn {
  @apply flex-1 py-2.5 rounded-lg text-sm flex items-center justify-center transition;
}
.edu-ai-btn.secondary {
  @apply bg-brand-surface border border-brand-border text-brand-muted hover:text-brand-text hover:border-violet-500;
}
.edu-ai-btn.primary {
  @apply bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500;
}

/* ═══ 通用版块卡片样式 ═══ */
.section-card {
  @apply rounded-xl bg-brand-bg border border-brand-border mb-3 overflow-hidden;
}
.section-card-header {
  @apply flex items-center justify-between px-4 py-3 cursor-pointer 
         hover:bg-slate-800/30 transition select-none;
}
.section-card-body {
  @apply px-4 pb-4 border-t border-brand-border pt-4;
}
.section-ai-btn {
  @apply flex-1 py-2.5 rounded-lg text-sm flex items-center justify-center transition;
}
.section-ai-btn.secondary {
  @apply bg-brand-surface border border-brand-border text-brand-muted hover:text-brand-text hover:border-violet-500;
}
.section-ai-btn.primary {
  @apply bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500;
}

.education-item, .project-item, .work-item {
  @apply p-4 rounded-xl bg-brand-bg border border-brand-border mb-3;
}
.competition-item {
  @apply p-3 rounded-lg bg-brand-bg border border-brand-border mb-2;
}
.honor-item {
  @apply mb-2;
}

/* ═══ 简历预览 ═══ */
.resume-preview-card {
  @apply bg-white rounded-lg shadow-2xl origin-top;
  min-height: 297mm;
  font-family: 'Source Han Sans', 'Noto Sans SC', sans-serif;
  --theme-color: #2563eb;
}
.resume-header {
  @apply pb-4 mb-4;
  border-bottom: 2px solid var(--theme-color);
}
.resume-section {
  @apply mb-5;
}
.resume-section-title {
  @apply text-base font-bold pb-2 mb-3;
  color: var(--theme-color);
  border-bottom: 1px solid #e2e8f0;
}
.resume-item {
  @apply mb-3;
}
.resume-list {
  @apply text-sm text-slate-600 space-y-1 list-none pl-0;
}
.resume-list li {
  @apply flex items-start gap-2;
}
.resume-list li::before {
  content: '•';
  color: var(--theme-color);
  @apply flex-shrink-0;
}

/* ═══ 富文本预览渲染 ═══ */
.resume-rich-content :deep(ul) {
  @apply list-none pl-0 space-y-0.5;
}
.resume-rich-content :deep(ul li) {
  @apply flex items-start gap-2;
}
.resume-rich-content :deep(ul li::before) {
  content: '•';
  color: var(--theme-color);
  @apply flex-shrink-0;
}
.resume-rich-content :deep(ol) {
  @apply list-decimal pl-5 space-y-0.5;
}
.resume-rich-content :deep(b),
.resume-rich-content :deep(strong) {
  @apply font-semibold;
}
.resume-rich-content :deep(a) {
  color: var(--theme-color);
  text-decoration: underline;
}
.resume-rich-content :deep(br + br) {
  @apply hidden;
}

/* ═══ 可爱机器人AI Agent ═══ */
.resume-ai-agent {
  position: fixed;
  z-index: 40;
  font-family: 'Inter', -apple-system, sans-serif;
  transition: none;
}
.resume-ai-agent.is-dragging {
  cursor: grabbing;
  user-select: none;
}
.agent-backdrop {
  position: fixed;
  inset: 0;
  z-index: -1;
}
.agent-wrapper {
  position: relative;
  cursor: grab;
}
.resume-ai-agent.is-dragging .agent-wrapper {
  cursor: grabbing;
}
.resume-ai-agent.is-active .agent-wrapper {
  cursor: pointer;
}

/* 脉冲环动画 */
.pulse-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.4);
  animation: pulse 2s ease-out infinite;
}
.pulse-ring.delay { animation-delay: 1s; }
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.8); opacity: 0; }
}

/* 机器人头像 */
.robot-avatar {
  width: 72px;
  height: 72px;
  position: relative;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.robot-avatar:hover { transform: scale(1.08); }
.robot-avatar.happy { animation: bounce 0.5s ease; }
.robot-avatar.wave { animation: wave 0.8s ease; }

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
@keyframes wave {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

.avatar-glow {
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.35) 0%, transparent 70%);
  filter: blur(8px);
  animation: glow-pulse 3s ease-in-out infinite;
}
@keyframes glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

.avatar-main { 
  width: 100%; 
  height: 100%; 
  position: relative; 
}

/* 天线 */
.antenna-wrap {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.antenna-stem {
  width: 4px;
  height: 10px;
  background: linear-gradient(to bottom, #a78bfa, #8b5cf6);
  border-radius: 2px;
}
.antenna-tip {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #34d399, #10b981);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
  animation: glow-soft 2s ease-in-out infinite;
}
.antenna-tip.active {
  animation: blink-fast 0.4s ease-in-out infinite;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.7);
}
@keyframes glow-soft {
  0%, 100% { box-shadow: 0 0 8px rgba(16, 185, 129, 0.5); }
  50% { box-shadow: 0 0 16px rgba(16, 185, 129, 0.8); }
}
@keyframes blink-fast {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* 机器人脸部 */
.face {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(145deg, #fef3c7, #fde68a);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 -4px 12px rgba(0, 0, 0, 0.05), inset 0 4px 8px rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

.eyes {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 16px;
}
.eye {
  width: 14px;
  height: 14px;
  background: #1e293b;
  border-radius: 50%;
  position: relative;
  transition: all 0.15s ease;
}
.eye.blink { height: 3px; border-radius: 3px; }
.eye.happy { height: 8px; border-radius: 8px 8px 50% 50%; }
.pupil {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  background: #1e293b;
  border-radius: 50%;
}
.eye.blink .pupil, .eye.happy .pupil { display: none; }
.highlight {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
}
.eye.blink .highlight, .eye.happy .highlight { display: none; }

.mouth {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 8px;
  background: #1e293b;
  border-radius: 0 0 16px 16px;
  transition: all 0.2s ease;
}
.mouth.speaking { animation: talk 0.25s ease-in-out infinite; }
.mouth.smile { width: 20px; height: 10px; border-radius: 0 0 20px 20px; }
@keyframes talk {
  0%, 100% { height: 8px; }
  50% { height: 14px; border-radius: 50%; }
}

.cheek {
  position: absolute;
  width: 10px;
  height: 6px;
  background: rgba(251, 113, 133, 0.5);
  border-radius: 50%;
  top: 36px;
}
.cheek.left { left: 8px; }
.cheek.right { right: 8px; }

/* 状态指示器 */
.status-indicator {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.9);
  padding: 3px 10px;
  border-radius: 10px;
  white-space: nowrap;
}
.status-indicator .status-text { font-size: 10px; font-weight: 500; color: #10b981; }
.status-indicator.thinking .status-text { color: #f59e0b; }

/* 闲聊气泡 */
.idle-bubble {
  position: absolute;
  bottom: 20px;
  right: 85px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  padding: 10px 16px;
  border-radius: 16px 16px 4px 16px;
  color: white;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
  cursor: pointer;
  animation: float 3s ease-in-out infinite;
  white-space: nowrap;
  max-width: 240px;
}
.bubble-tail {
  display: none;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
.bubble-pop-enter-active { animation: pop-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.bubble-pop-leave-active { animation: pop-out 0.3s ease; }
@keyframes pop-in {
  0% { transform: scale(0) translateY(10px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes pop-out {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0; }
}

/* 主交互面板 */
.agent-panel {
  @apply absolute w-96 rounded-2xl overflow-hidden;
  background: #0f172a;
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  bottom: 90px;
  right: 0;
}
.panel-spring-enter-active { animation: panel-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.panel-spring-leave-active { animation: panel-out 0.2s ease-in; }
@keyframes panel-in {
  0% { transform: scale(0.8) translateY(20px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes panel-out {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.9) translateY(10px); opacity: 0; }
}
.panel-header {
  @apply flex items-center justify-between px-4 py-3;
  background: rgba(30, 41, 59, 0.8);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}
.header-left {
  @apply flex items-center gap-2;
}
.header-icon {
  @apply text-xl;
}
.header-title {
  @apply text-sm font-semibold text-white;
}
.close-btn {
  @apply w-7 h-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-slate-700/50 transition;
}

/* 对话区域 */
.chat-zone {
  @apply h-64 overflow-y-auto p-4 space-y-3;
}
.chat-message {
  @apply flex gap-2;
}
.chat-message.user {
  @apply flex-row-reverse;
}
.msg-avatar {
  @apply w-7 h-7 rounded-full flex items-center justify-center text-sm flex-shrink-0;
  background: linear-gradient(135deg, #7c3aed, #06b6d4);
}
.msg-content {
  @apply max-w-[80%];
}
.msg-text {
  @apply px-3 py-2 rounded-xl text-sm whitespace-pre-wrap;
}
.chat-message.assistant .msg-text {
  background: rgba(30, 41, 59, 0.8);
  color: #e2e8f0;
}
.chat-message.user .msg-text {
  background: #7c3aed;
  color: white;
}
.msg-actions {
  @apply flex flex-wrap gap-1.5 mt-2;
}
.action-chip {
  @apply px-2.5 py-1 rounded-lg text-xs transition cursor-pointer;
  background: rgba(124, 58, 237, 0.2);
  color: #a78bfa;
}
.action-chip:hover {
  background: rgba(124, 58, 237, 0.3);
}
.chat-message.typing .msg-text {
  background: rgba(30, 41, 59, 0.8);
}
.typing-dots {
  @apply flex gap-1 py-1;
}
.typing-dots span {
  @apply w-2 h-2 rounded-full bg-violet-400;
  animation: typing-dot 1.4s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-dot {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
  30% { transform: translateY(-3px); opacity: 1; }
}

/* 功能网格 */
.action-grid {
  @apply grid grid-cols-2 gap-2 px-4 pb-3;
}
.action-card {
  @apply flex flex-col items-center justify-center gap-1 py-3 rounded-xl transition cursor-pointer;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
}
.action-card:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(124, 58, 237, 0.5);
}
.action-icon {
  @apply text-xl;
}
.action-label {
  @apply text-xs text-slate-300;
}

/* 快捷回复 */
.quick-replies-bar {
  @apply flex flex-wrap gap-2 px-4 py-2;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}
.quick-btn {
  @apply flex items-center gap-1 px-3 py-1.5 rounded-full text-xs text-slate-300 transition cursor-pointer;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
}
.quick-btn:hover {
  border-color: rgba(124, 58, 237, 0.5);
  color: #a78bfa;
}

/* 输入框 */
.input-bar {
  @apply flex gap-2 p-3;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}
.chat-input {
  @apply flex-1 px-3 py-2 rounded-lg text-sm text-white placeholder-slate-400 outline-none;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
}
.chat-input:focus {
  border-color: rgba(124, 58, 237, 0.5);
}
.send-btn {
  @apply w-9 h-9 rounded-lg flex items-center justify-center text-white transition;
  background: #7c3aed;
}
.send-btn:hover {
  background: #6d28d9;
}
.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ═══ 诊断弹窗 ═══ */
.diagnosis-modal {
  @apply w-full max-w-lg bg-brand-card rounded-2xl border border-brand-border overflow-hidden;
}
.modal-header {
  @apply flex items-center justify-between px-5 py-4 border-b border-brand-border;
}
.modal-body {
  @apply p-5;
}
.modal-footer {
  @apply flex items-center justify-end gap-3 px-5 py-4 border-t border-brand-border;
}

.diagnosis-score {
  @apply flex items-center gap-5 p-4 rounded-xl bg-brand-surface mb-5;
}
.score-ring {
  @apply relative;
}
.score-num {
  @apply absolute inset-0 flex items-center justify-center text-2xl font-bold text-brand-text;
}
.score-info {
  @apply flex flex-col;
}
.score-label {
  @apply text-sm font-medium text-brand-text;
}
.score-hint {
  @apply text-xs text-emerald-400;
}

.diagnosis-issues {
  @apply space-y-2;
}
.issue-card {
  @apply flex items-center gap-3 p-3 rounded-xl bg-brand-surface border border-brand-border;
}
.issue-card.warning {
  @apply border-orange-500/30;
}
.issue-card.info {
  @apply border-blue-500/30;
}
.issue-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0;
}
.issue-card.warning .issue-icon {
  @apply bg-orange-500/20 text-orange-400;
}
.issue-card.info .issue-icon {
  @apply bg-blue-500/20 text-blue-400;
}
.issue-content {
  @apply flex-1 min-w-0;
}
.issue-title {
  @apply block text-sm font-medium text-brand-text;
}
.issue-desc {
  @apply block text-xs text-brand-muted;
}
.issue-fix-btn {
  @apply px-3 py-1.5 rounded-lg bg-violet-600 text-white text-xs hover:bg-violet-700 transition flex-shrink-0;
}

/* ═══ AI润色面板 ═══ */
.polish-option {
  @apply p-4 rounded-xl bg-brand-surface border border-brand-border;
}
.polish-icon {
  @apply w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0;
}
.btn-sm {
  @apply px-3 py-1.5 rounded-lg bg-brand-bg border border-brand-border text-sm text-brand-text
         hover:border-violet-500 hover:text-violet-400 transition;
}
.btn-primary {
  @apply px-4 py-2 rounded-lg bg-violet-600 text-white text-sm hover:bg-violet-700 transition;
}
.btn-secondary {
  @apply px-4 py-2 rounded-lg bg-brand-surface border border-brand-border text-sm text-brand-text
         hover:border-violet-500 transition;
}

/* ═══ 动画 ═══ */
.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s ease;
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ═══ Toast 提示 ═══ */
.toast-item {
  @apply px-4 py-3 rounded-lg shadow-xl flex items-center text-sm font-medium;
  min-width: 200px;
}
.toast-item.success {
  @apply bg-emerald-500 text-white;
}
.toast-item.error {
  @apply bg-red-500 text-white;
}
.toast-item.info {
  @apply bg-blue-500 text-white;
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  transform: translateX(100px);
  opacity: 0;
}
.toast-leave-to {
  transform: translateX(100px);
  opacity: 0;
}

/* ═══ 严重等级样式 ═══ */
.issue-card.error {
  @apply border-red-500/30;
}
.issue-card.error .issue-icon {
  @apply bg-red-500/20 text-red-400;
}

/* ═══ 字体下拉框 ═══ */
.toolbar-select-wrapper {
  @apply flex items-center px-3 py-1.5 rounded-lg bg-brand-bg border border-brand-border text-xs text-brand-text
         hover:border-blue-500 transition cursor-pointer relative;
}
.font-dropdown {
  @apply absolute top-full left-0 mt-1 w-36 bg-brand-card border border-brand-border rounded-lg shadow-xl z-50 overflow-hidden;
}
.font-dropdown-item {
  @apply w-full px-4 py-2.5 text-left text-sm text-brand-text hover:bg-brand-surface transition cursor-pointer;
}
.font-dropdown-item.active {
  @apply bg-blue-500/20 text-blue-400;
}

/* ═══ 模块管理弹窗 ═══ */
.module-manager-modal {
  @apply w-full max-w-md bg-brand-card rounded-2xl border border-brand-border overflow-hidden;
}
.module-item {
  @apply flex items-center gap-3 px-4 py-3 rounded-lg bg-brand-surface border border-brand-border;
}
.module-item.add-module {
  @apply cursor-pointer hover:border-blue-500 transition;
}
.drag-handle {
  @apply w-6 h-6 flex items-center justify-center text-brand-muted cursor-move;
}
.add-icon {
  @apply w-6 h-6 flex items-center justify-center text-brand-muted;
}
.module-action-btn {
  @apply w-7 h-7 rounded-lg bg-brand-bg flex items-center justify-center text-brand-muted
         hover:text-brand-text transition;
}
.premium-badge {
  @apply text-sm;
}

/* ═══ 模板样式变体 ═══ */
.resume-preview-card.template-classic .resume-section-title {
  color: var(--theme-color);
  border-bottom-color: var(--theme-color);
}
.resume-preview-card.template-classic .resume-header {
  border-bottom-color: var(--theme-color);
}

.resume-preview-card.template-modern .resume-section-title {
  color: var(--theme-color);
  border-bottom: none;
  padding-bottom: 8px;
}
.resume-preview-card.template-modern .resume-header {
  border-bottom: 3px solid var(--theme-color);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.resume-preview-card.template-elegant .resume-section-title {
  color: var(--theme-color);
  border-bottom: 2px solid var(--theme-color);
  font-family: 'SimSun', serif;
  letter-spacing: 2px;
}
.resume-preview-card.template-elegant .resume-header {
  border-bottom: 2px double var(--theme-color);
  padding-bottom: 16px;
}

.resume-preview-card.template-creative .resume-section-title {
  color: var(--theme-color);
  border-bottom: none;
  position: relative;
  padding-left: 16px;
}
.resume-preview-card.template-creative .resume-section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--theme-color);
  border-radius: 2px;
}
.resume-preview-card.template-creative .resume-header {
  border-bottom: none;
  padding: 24px;
  border-radius: 16px;
}

/* ═══ 下拉菜单通用样式 ═══ */
.toolbar-dropdown .dropdown-item.active {
  @apply bg-blue-500/20 text-blue-400;
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .builder-bg {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
}

:global(html.light) .glow-1,
:global(html.light) .glow-2 {
  opacity: 0.04;
}

:global(html.light) .glow-1 { background: #0891b2; }
:global(html.light) .glow-2 { background: #06b6d4; }

:global(html.light) .builder-header h1 {
  color: #0c4a6e;
}

:global(html.light) .builder-header p {
  color: #64748b;
}

:global(html.light) .toolbar {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .toolbar-btn {
  background: rgba(8, 145, 178, 0.06);
  border-color: rgba(8, 145, 178, 0.15);
  color: #64748b;
}

:global(html.light) .toolbar-btn:hover {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .toolbar-btn.active {
  background: rgba(8, 145, 178, 0.15);
  color: #0891b2;
  border-color: rgba(8, 145, 178, 0.3);
}

:global(html.light) .toolbar-dropdown {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .toolbar-dropdown .dropdown-item {
  color: #64748b;
}

:global(html.light) .toolbar-dropdown .dropdown-item:hover {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .toolbar-dropdown .dropdown-item.active {
  background: rgba(8, 145, 178, 0.12);
  color: #0891b2;
}

:global(html.light) .editor-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .section-card {
  background: rgba(8, 145, 178, 0.02);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .section-card:hover {
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .section-header h3 {
  color: #0c4a6e;
}

:global(html.light) .section-content {
  color: #475569;
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

:global(html.light) .preview-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .resume-preview-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.08);
}

:global(html.light) .resume-header h1 {
  color: #0c4a6e;
}

:global(html.light) .resume-section-title {
  color: #0891b2;
  border-bottom-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .resume-content {
  color: #475569;
}

:global(html.light) .skill-tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .template-selector {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .template-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .template-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .template-card.selected {
  border-color: #0891b2;
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .template-name {
  color: #0c4a6e;
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

:global(html.light) .ai-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .ai-header h4 {
  color: #0c4a6e;
}

:global(html.light) .ai-suggestion {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .ai-suggestion:hover {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .ai-text {
  color: #475569;
}

:global(html.light) .empty-state {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .empty-state h3 {
  color: #0c4a6e;
}

:global(html.light) .empty-state p {
  color: #64748b;
}

/* ═══ 移动端适配 ═══ */
.mobile-tab-bar {
  display: none;
}

@media (max-width: 768px) {
  /* 隐藏桌面侧边栏，显示移动端Tab栏 */
  .desktop-sidebar {
    display: none !important;
  }
  
  .mobile-tab-bar {
    display: flex;
    position: fixed;
    top: 64px; /* NavBar高度 */
    left: 0;
    right: 0;
    z-index: 100;
    background: var(--brand-surface, #1a1a2e);
    border-bottom: 1px solid var(--brand-border, #333);
    padding: 6px 8px;
    gap: 4px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  
  .mobile-tab-bar::-webkit-scrollbar {
    display: none;
  }
  
  .mobile-tab-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 56px;
    padding: 6px 10px;
    border-radius: 10px;
    color: var(--brand-muted, #888);
    background: transparent;
    border: none;
    transition: all 0.2s;
    flex-shrink: 0;
  }
  
  .mobile-tab-btn.active {
    background: rgba(139, 92, 246, 0.2);
    color: #a78bfa;
  }
  
  .mobile-tab-btn.ai-btn {
    margin-left: auto;
  }
  
  /* 主内容区适配 */
  .resume-builder-container {
    flex-direction: column;
    padding-top: 116px; /* NavBar(64px) + 移动端Tab栏高度(52px) */
    padding-bottom: 72px; /* 底部导航高度 */
  }
  
  .main-content-area {
    height: auto;
    min-height: calc(100vh - 52px - 72px);
  }
  
  /* 顶部工具栏简化 */
  .top-toolbar {
    height: auto;
    min-height: 44px;
    padding: 6px 10px;
    flex-wrap: nowrap;
    justify-content: flex-start;
    gap: 6px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  
  .top-toolbar::-webkit-scrollbar {
    display: none;
  }
  
  .toolbar-divider {
    display: none;
  }
  
  .toolbar-item {
    flex-shrink: 0;
    padding: 6px 10px;
  }
  
  .toolbar-select-wrapper {
    flex-shrink: 0;
  }
  
  /* 内容区域改为垂直布局 */
  .content-flex-area {
    flex-direction: column;
  }
  
  /* 编辑面板全宽 */
  .edit-panel {
    width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid var(--brand-border, #333);
  }
  
  /* 预览区适配 */
  .preview-panel,
  .flex-1.p-6.overflow-auto {
    min-height: 60vh;
    padding: 12px !important;
  }
  
  /* 简历预览卡片缩放 */
  .resume-preview-card {
    transform: scale(0.65);
    transform-origin: top center;
  }
  
  /* AI诊断卡片 */
  .ai-diagnosis-card {
    padding: 12px;
  }
  
  /* 编辑表单适配 */
  .edit-input,
  .edit-textarea {
    font-size: 16px !important; /* 防止iOS缩放 */
  }
  
  /* 模块卡片 */
  .grid.grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  /* AI机器人位置调整 - 避开底部导航 */
  .resume-ai-agent {
    bottom: 90px !important; /* 底部导航栏高度 + 间距 */
  }
  
  /* AI面板移动端适配 */
  .agent-panel {
    width: calc(100vw - 32px) !important;
    max-width: 320px;
    right: 8px !important;
    max-height: calc(100vh - 180px);
  }
  
  /* 机器人头像缩小 */
  .robot-avatar {
    transform: scale(0.85);
  }
  
  /* 脉冲环缩小 */
  .pulse-ring {
    width: 80px !important;
    height: 80px !important;
  }
}

@media (max-width: 480px) {
  .mobile-tab-btn {
    min-width: 48px;
    padding: 4px 8px;
  }
  
  .mobile-tab-btn span {
    font-size: 9px;
  }
  
  .toolbar-item {
    padding: 4px 8px;
  }
  
  .resume-preview-card {
    transform: scale(0.5);
  }
}
</style>
