<template>
  <div class="planning-journey" :class="{ 'dark-mode': true }">
    <!-- 背景动效（简化版） -->
    <div class="journey-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="particles">
        <div v-for="i in 6" :key="i" class="particle" :style="particleStyle(i)"></div>
      </div>
    </div>

    <!-- 顶部导航 -->
    <header class="journey-header">
      <div class="header-left">
        <router-link to="/" class="back-btn">
          <i class="bi bi-arrow-left"></i>
        </router-link>
        <div class="brand">
          <i class="bi bi-compass text-violet-400"></i>
          <span>职业规划中心</span>
        </div>
      </div>
      <div class="header-center">
        <div class="step-progress">
          <template v-for="(step, i) in stepLabels" :key="i">
            <div class="step-dot" :class="{ active: currentStep >= i, current: currentStep === i }">
              <span class="step-num">{{ i + 1 }}</span>
              <span class="step-label">{{ step }}</span>
            </div>
            <div v-if="i < stepLabels.length - 1" class="step-line" :class="{ filled: currentStep > i }"></div>
          </template>
        </div>
      </div>
      <div class="header-right">
        <button v-if="currentStep > 0" @click="prevStep" class="nav-btn">
          <i class="bi bi-chevron-left"></i> 上一步
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="journey-main">
      <!-- Agent对话区域 -->
      <div class="agent-section">
        <!-- AI助手形象 - 与CareerAIAssistant一致 -->
        <div class="agent-avatar" :class="{ thinking: isThinking, speaking: isSpeaking, happy: isHappy }">
          <!-- 脉冲环 -->
          <div class="pulse-ring" v-if="!isThinking"></div>
          <div class="pulse-ring delay" v-if="!isThinking"></div>
          <div class="avatar-glow"></div>
          <div class="avatar-body">
            <div class="antenna">
              <div class="antenna-tip" :class="{ active: isThinking }"></div>
            </div>
            <div class="face">
              <div class="eyes">
                <div class="eye left" :class="eyeState"><div class="pupil"></div></div>
                <div class="eye right" :class="eyeState"><div class="pupil"></div></div>
              </div>
              <div class="mouth" :class="mouthState"></div>
              <div class="cheeks">
                <div class="cheek left"></div>
                <div class="cheek right"></div>
              </div>
            </div>
          </div>
          <div class="agent-name">
            <span class="status-dot"></span>
            小智
          </div>
        </div>

        <!-- 对话气泡 -->
        <div class="agent-dialogue">
          <transition-group name="message" tag="div" class="messages-container">
            <div v-for="(msg, idx) in visibleMessages" :key="msg.id" class="message" :class="msg.type">
              <div class="message-content">
                <span v-if="msg.typing" class="typing-text">{{ msg.displayText }}<span class="cursor">|</span></span>
                <span v-else>{{ msg.text }}</span>
              </div>
            </div>
          </transition-group>
        </div>
      </div>

      <!-- 交互内容区 -->
      <div class="content-section">
        <transition name="slide-up" mode="out-in">
          <!-- Step 0: 欢迎页 -->
          <div v-if="currentStep === 0" key="welcome" class="step-content welcome-step">
            <div class="welcome-hero">
              <h1 class="hero-title">
                <span class="gradient-text">开启你的</span>
                <br>
                <span class="highlight-text">职业规划之旅</span>
              </h1>
              <p class="hero-subtitle">让AI助手小智陪你一起，发现最适合你的职业方向</p>
            </div>
            <div class="welcome-features">
              <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-text">
                  <h3>智能解析</h3>
                  <p>上传简历，AI快速理解你的背景</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-text">
                  <h3>精准匹配</h3>
                  <p>基于画像的人岗智能匹配</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <div class="feature-text">
                  <h3>路径规划</h3>
                  <p>AI规划你的职业发展路径</p>
                </div>
              </div>
            </div>
            <div class="welcome-actions">
              <button class="primary-btn pulse" @click="startJourney">
                <span class="btn-text">开始规划</span>
                <i class="bi bi-arrow-right"></i>
              </button>
              <button v-if="students.length" class="secondary-btn" @click="showExistingSelector = true">
                <i class="bi bi-people"></i>
                <span>继续已有档案</span>
              </button>
            </div>
          </div>

          <!-- Step 1: 基本信息收集 -->
          <div v-else-if="currentStep === 1" key="info" class="step-content info-step">
            <div class="info-modes">
              <div class="mode-tabs">
                <button :class="{ active: infoMode === 'resume' }" @click="infoMode = 'resume'">
                  <i class="bi bi-file-earmark-text"></i>
                  <span>上传简历</span>
                </button>
                <button :class="{ active: infoMode === 'manual' }" @click="infoMode = 'manual'">
                  <i class="bi bi-pencil-square"></i>
                  <span>手动填写</span>
                </button>
              </div>

              <!-- 简历上传模式 -->
              <div v-if="infoMode === 'resume'" class="resume-upload">
                <div 
                  class="upload-zone" 
                  :class="{ dragging: isDragging, uploaded: selectedFile }"
                  @drop.prevent="handleDrop"
                  @dragover.prevent="isDragging = true"
                  @dragleave="isDragging = false"
                  @click="$refs.fileInput.click()"
                >
                  <input ref="fileInput" type="file" accept=".pdf,.docx,.doc" @change="handleFileSelect" hidden>
                  <template v-if="!selectedFile">
                    <div class="upload-icon">
                      <i class="bi bi-cloud-arrow-up"></i>
                    </div>
                    <h3>拖拽简历文件到这里</h3>
                    <p>或点击选择文件</p>
                    <span class="file-types">支持 PDF / DOCX / DOC 格式</span>
                  </template>
                  <template v-else>
                    <div class="file-preview">
                      <i class="bi bi-file-earmark-check text-emerald-400"></i>
                      <div class="file-info">
                        <span class="file-name">{{ selectedFile.name }}</span>
                        <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
                      </div>
                      <button class="remove-file" @click.stop="selectedFile = null">
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                  </template>
                </div>
                <div class="upload-tip">
                  <i class="bi bi-shield-check text-emerald-400"></i>
                  <span>您的简历将安全保存，仅用于生成职业画像</span>
                </div>
              </div>

              <!-- 手动填写模式 -->
              <div v-if="infoMode === 'manual'" class="manual-form">
                <div class="form-group">
                  <label>你的名字</label>
                  <input v-model="formData.name" type="text" placeholder="请输入你的名字" class="form-input" />
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>最高学历</label>
                    <select v-model="formData.education" class="form-input">
                      <option value="">请选择</option>
                      <option value="大专">大专</option>
                      <option value="本科">本科</option>
                      <option value="硕士">硕士</option>
                      <option value="博士">博士</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>专业方向</label>
                    <input v-model="formData.major" type="text" placeholder="如: 计算机科学与技术" class="form-input" />
                  </div>
                </div>
                <div class="form-group">
                  <label>毕业院校</label>
                  <input v-model="formData.school" type="text" placeholder="请输入你的毕业院校" class="form-input" />
                </div>
                <div class="form-group">
                  <label>技能标签 <span class="hint">（逗号分隔）</span></label>
                  <input v-model="formData.skills" type="text" placeholder="如: Python, 数据分析, 机器学习" class="form-input" />
                </div>
                <div class="form-group">
                  <label>个人简介 <span class="hint">（可选）</span></label>
                  <textarea v-model="formData.summary" rows="3" placeholder="简单介绍一下你自己..." class="form-input"></textarea>
                </div>
              </div>
            </div>

            <div class="step-actions">
              <button class="primary-btn" @click="submitInfo" :disabled="!canSubmitInfo || isProcessing">
                <i v-if="isProcessing" class="bi bi-hourglass-split animate-spin"></i>
                <span>{{ isProcessing ? '正在解析...' : '继续' }}</span>
                <i v-if="!isProcessing" class="bi bi-arrow-right"></i>
              </button>
            </div>
          </div>

          <!-- Step 2: 求职意向 -->
          <div v-else-if="currentStep === 2" key="target" class="step-content target-step">
            <div class="target-questions">
              <!-- 问题1: 期望岗位 -->
              <div class="question-card">
                <div class="question-header">
                  <span class="q-num">Q1</span>
                  <h3>你期望从事什么类型的工作？</h3>
                </div>
                <div class="tag-selector">
                  <button 
                    v-for="tag in positionTags" 
                    :key="tag" 
                    :class="{ selected: selectedPositions.includes(tag) }"
                    @click="toggleTag(selectedPositions, tag)"
                  >
                    {{ tag }}
                  </button>
                </div>
                <input 
                  v-model="customPosition" 
                  type="text" 
                  placeholder="或者输入你想要的岗位名称..." 
                  class="form-input mt-3"
                  @keyup.enter="addCustomPosition"
                />
              </div>

              <!-- 问题2: 期望行业 -->
              <div class="question-card">
                <div class="question-header">
                  <span class="q-num">Q2</span>
                  <h3>你对哪些行业感兴趣？</h3>
                </div>
                <div class="tag-selector">
                  <button 
                    v-for="tag in industryTags" 
                    :key="tag" 
                    :class="{ selected: selectedIndustries.includes(tag) }"
                    @click="toggleTag(selectedIndustries, tag)"
                  >
                    {{ tag }}
                  </button>
                </div>
              </div>

              <!-- 问题3: 对自己的期望 -->
              <div class="question-card">
                <div class="question-header">
                  <span class="q-num">Q3</span>
                  <h3>你在职业发展中最看重什么？</h3>
                </div>
                <div class="priority-cards">
                  <div 
                    v-for="item in priorityOptions" 
                    :key="item.id"
                    class="priority-card"
                    :class="{ selected: selectedPriorities.includes(item.id) }"
                    @click="toggleTag(selectedPriorities, item.id)"
                  >
                    <span class="priority-icon">{{ item.icon }}</span>
                    <span class="priority-label">{{ item.label }}</span>
                    <span class="priority-desc">{{ item.desc }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="step-actions">
              <button class="primary-btn" @click="submitTarget" :disabled="!canSubmitTarget">
                <span>生成职业画像</span>
                <i class="bi bi-magic"></i>
              </button>
            </div>
          </div>

          <!-- Step 3: 生成画像 -->
          <div v-else-if="currentStep === 3" key="profile" class="step-content profile-step">
            <template v-if="generatingProfile">
              <div class="generating-state">
                <div class="ai-working">
                  <div class="working-animation">
                    <div class="ring ring-1"></div>
                    <div class="ring ring-2"></div>
                    <div class="ring ring-3"></div>
                    <div class="center-icon">🤖</div>
                  </div>
                  <h3>小智正在分析你的信息...</h3>
                  <p class="generating-step">{{ generatingStep }}</p>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: generatingProgress + '%' }"></div>
                  </div>
                  <div class="generating-tips">
                    <div class="tip-card">
                      <span class="tip-icon">✨</span>
                      <span class="tip-text">AI 正在从多个维度评估你的能力，请稍候~</span>
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <template v-else-if="studentProfile">
              <div class="profile-result">
                <div class="profile-header">
                  <div class="profile-avatar">
                    <span class="avatar-emoji">👤</span>
                  </div>
                  <div class="profile-info">
                    <h2>{{ selectedStudent?.name || formData.name || '用户' }}</h2>
                    <p>{{ selectedStudent?.education || formData.education }} · {{ selectedStudent?.major || formData.major }}</p>
                  </div>
                  <div class="profile-scores">
                    <div class="score-item">
                      <div class="score-ring">
                        <svg viewBox="0 0 60 60">
                          <circle class="ring-bg" cx="30" cy="30" r="25"></circle>
                          <circle class="ring-fill completeness" cx="30" cy="30" r="25" 
                            :style="{ strokeDashoffset: 157 - (157 * (studentProfile.completeness_score || 0) / 100) }"></circle>
                        </svg>
                        <span class="score-value">{{ Number(studentProfile.completeness_score || 0).toFixed(0) }}</span>
                      </div>
                      <span class="score-label">完整度</span>
                    </div>
                    <div class="score-item">
                      <div class="score-ring">
                        <svg viewBox="0 0 60 60">
                          <circle class="ring-bg" cx="30" cy="30" r="25"></circle>
                          <circle class="ring-fill competitiveness" cx="30" cy="30" r="25"
                            :style="{ strokeDashoffset: 157 - (157 * (studentProfile.competitiveness_score || 0) / 100) }"></circle>
                        </svg>
                        <span class="score-value">{{ Number(studentProfile.competitiveness_score || 0).toFixed(0) }}</span>
                      </div>
                      <span class="score-label">竞争力</span>
                    </div>
                  </div>
                </div>

                <!-- 技能卡片 -->
                <div v-if="studentProfile.technical_skills?.length" class="skills-section">
                  <h4><i class="bi bi-code-slash text-violet-400"></i> 专业技能</h4>
                  <div class="skill-chips">
                    <span v-for="skill in getSkillNames(studentProfile.technical_skills).slice(0, 8)" :key="skill" class="skill-chip">
                      {{ skill }}
                    </span>
                    <span v-if="studentProfile.technical_skills.length > 8" class="skill-chip more">
                      +{{ studentProfile.technical_skills.length - 8 }}
                    </span>
                  </div>
                </div>

                <div class="abilities-radar">
                  <h4><i class="bi bi-radar"></i> 能力雷达</h4>
                  <RadarChart :series="radarSeries" :indicators="radarIndicators" height="280px" />
                </div>

                <div class="profile-tags">
                  <div class="tag-section">
                    <h4><i class="bi bi-star-fill text-amber-400"></i> 核心优势</h4>
                    <div class="tags">
                      <span v-for="s in (studentProfile.strengths || []).slice(0, 6)" :key="s" class="tag success">{{ s }}</span>
                      <span v-if="!studentProfile.strengths?.length" class="empty">暂无</span>
                    </div>
                  </div>
                  <div class="tag-section">
                    <h4><i class="bi bi-arrow-up-circle text-cyan-400"></i> 待提升</h4>
                    <div class="tags">
                      <span v-for="w in (studentProfile.weaknesses || []).slice(0, 6)" :key="w" class="tag warning">{{ w }}</span>
                      <span v-if="!studentProfile.weaknesses?.length" class="empty">暂无</span>
                    </div>
                  </div>
                </div>
                
                <!-- 综合评价 -->
                <div v-if="studentProfile.overall_evaluation" class="evaluation-section">
                  <h4><i class="bi bi-chat-square-text text-cyan-400"></i> AI 综合评价</h4>
                  <p class="evaluation-text">{{ studentProfile.overall_evaluation }}</p>
                </div>
              </div>

              <div class="step-actions">
                <button class="primary-btn" @click="goToMatching">
                  <span>开始人岗匹配</span>
                  <i class="bi bi-link-45deg"></i>
                </button>
              </div>
            </template>
            <template v-else>
              <div class="empty-state-card">
                <i class="bi bi-exclamation-circle text-rose-300"></i>
                <h3>画像生成暂时失败</h3>
                <p>{{ profileError || '请点击重试，或稍后再试。' }}</p>
                <button class="primary-btn" @click="generateProfile" :disabled="generatingProfile">
                  <i class="bi bi-arrow-clockwise"></i>
                  <span>重试生成画像</span>
                </button>
              </div>
            </template>
          </div>

          <!-- Step 4: 人岗匹配 -->
          <div v-else-if="currentStep === 4" key="matching" class="step-content matching-step">
            <template v-if="runningMatch">
              <div class="generating-state">
                <div class="ai-working">
                  <div class="working-animation matching">
                    <div class="match-line"></div>
                    <div class="person-icon">👤</div>
                    <div class="job-icon">💼</div>
                  </div>
                  <h3>正在为你匹配最佳岗位...</h3>
                  <p class="generating-step">{{ matchingStep }}</p>
                  <div class="matching-tips">
                    <div class="tip-card">
                      <span class="tip-icon">💡</span>
                      <span class="tip-text">匹配过程中AI会综合分析你的技能、经验与岗位要求</span>
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <template v-else-if="matchResults.length">
              <div class="match-results">
                <div class="results-header">
                  <div class="results-title">
                    <i class="bi bi-trophy text-amber-400"></i>
                    <h3>匹配结果</h3>
                  </div>
                  <div class="results-meta">
                    <span class="results-count">
                      <i class="bi bi-briefcase"></i>
                      找到 <strong>{{ matchResults.length }}</strong> 个适合你的岗位
                    </span>
                    <span class="results-tip">点击卡片查看详情</span>
                  </div>
                </div>
                
                <div class="results-list">
                  <div 
                    v-for="(match, idx) in matchResults" 
                    :key="match.id" 
                    class="match-card-enhanced"
                    :class="{ 
                      'top-match': idx === 0,
                      'expanded': expandedMatchId === match.id 
                    }"
                    @click="toggleMatchExpand(match.id)"
                  >
                    <!-- 排名徽章 -->
                    <div class="rank-badge" :class="{ 'rank-1': idx === 0, 'rank-2': idx === 1, 'rank-3': idx === 2 }">
                      <span class="rank-num">{{ idx + 1 }}</span>
                      <span v-if="idx === 0" class="rank-label">最佳匹配</span>
                    </div>
                    
                    <!-- 主要信息区 -->
                    <div class="card-main">
                      <div class="job-info">
                        <h4 class="job-title">{{ match.job_name }}</h4>
                        <div class="job-meta">
                          <span class="job-category"><i class="bi bi-folder"></i> {{ match.job_category || '未分类' }}</span>
                          <span v-if="match.job_level" class="job-level"><i class="bi bi-bar-chart-steps"></i> {{ match.job_level }}</span>
                          <span v-if="match.job_salary" class="job-salary"><i class="bi bi-currency-yen"></i> {{ match.job_salary }}</span>
                        </div>
                      </div>
                      
                      <!-- 总分圆形进度 -->
                      <div class="total-score-ring">
                        <svg viewBox="0 0 100 100">
                          <circle class="ring-bg" cx="50" cy="50" r="42"></circle>
                          <circle 
                            class="ring-progress" 
                            cx="50" cy="50" r="42"
                            :style="{ strokeDashoffset: 264 - (264 * (match.overall_score || 0) / 100) }"
                            :class="getScoreClass(match.overall_score)"
                          ></circle>
                        </svg>
                        <div class="score-text">
                          <span class="score-value">{{ Number(match.overall_score || 0).toFixed(0) }}</span>
                          <span class="score-unit">分</span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 四维度评分条 -->
                    <div class="dimension-scores">
                      <div class="score-bar-item">
                        <div class="bar-label">
                          <i class="bi bi-person-badge"></i>
                          <span>基础匹配</span>
                        </div>
                        <div class="bar-track">
                          <div class="bar-fill basic" :style="{ width: (match.basic_score || 0) + '%' }"></div>
                        </div>
                        <span class="bar-value">{{ Number(match.basic_score || 0).toFixed(0) }}</span>
                      </div>
                      <div class="score-bar-item">
                        <div class="bar-label">
                          <i class="bi bi-code-slash"></i>
                          <span>技能匹配</span>
                        </div>
                        <div class="bar-track">
                          <div class="bar-fill skill" :style="{ width: (match.skill_score || 0) + '%' }"></div>
                        </div>
                        <span class="bar-value">{{ Number(match.skill_score || 0).toFixed(0) }}</span>
                      </div>
                      <div class="score-bar-item">
                        <div class="bar-label">
                          <i class="bi bi-heart"></i>
                          <span>素养匹配</span>
                        </div>
                        <div class="bar-track">
                          <div class="bar-fill quality" :style="{ width: (match.quality_score || 0) + '%' }"></div>
                        </div>
                        <span class="bar-value">{{ Number(match.quality_score || 0).toFixed(0) }}</span>
                      </div>
                      <div class="score-bar-item">
                        <div class="bar-label">
                          <i class="bi bi-graph-up-arrow"></i>
                          <span>发展潜力</span>
                        </div>
                        <div class="bar-track">
                          <div class="bar-fill potential" :style="{ width: (match.potential_score || 0) + '%' }"></div>
                        </div>
                        <span class="bar-value">{{ Number(match.potential_score || 0).toFixed(0) }}</span>
                      </div>
                    </div>
                    
                    <!-- 展开详情区 -->
                    <transition name="expand">
                      <div v-if="expandedMatchId === match.id" class="match-expanded-detail">
                        <!-- 技能分析 -->
                        <div v-if="getMatchAnalysis(match, 'matched_skills')?.length || getMatchAnalysis(match, 'missing_skills')?.length" class="skill-analysis">
                          <div class="analysis-section matched-skills" v-if="getMatchAnalysis(match, 'matched_skills')?.length">
                            <h5><i class="bi bi-check-circle text-emerald-400"></i> 已匹配技能</h5>
                            <div class="skill-tags">
                              <span v-for="skill in getMatchAnalysis(match, 'matched_skills').slice(0, 6)" :key="skill" class="skill-tag matched">
                                {{ skill }}
                              </span>
                            </div>
                          </div>
                          <div class="analysis-section missing-skills" v-if="getMatchAnalysis(match, 'missing_skills')?.length">
                            <h5><i class="bi bi-exclamation-circle text-amber-400"></i> 待提升技能</h5>
                            <div class="skill-tags">
                              <span v-for="skill in getMatchAnalysis(match, 'missing_skills').slice(0, 6)" :key="skill" class="skill-tag missing">
                                {{ skill }}
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        <!-- 推荐建议 -->
                        <div v-if="getMatchRecommendations(match)?.length" class="recommendations">
                          <h5><i class="bi bi-lightbulb text-cyan-400"></i> 提升建议</h5>
                          <ul class="recommend-list">
                            <li v-for="(rec, i) in getMatchRecommendations(match).slice(0, 3)" :key="i">
                              {{ rec }}
                            </li>
                          </ul>
                        </div>
                        
                        <!-- 详细分析 -->
                        <div v-if="getMatchAnalysis(match, 'overall_analysis')" class="overall-analysis">
                          <h5><i class="bi bi-file-text text-violet-400"></i> 综合分析</h5>
                          <p>{{ getMatchAnalysis(match, 'overall_analysis') }}</p>
                        </div>
                        
                        <!-- 操作按钮 -->
                        <div class="detail-actions">
                          <button class="action-btn view-profile" @click.stop="viewJobProfile(match.job_profile_id)">
                            <i class="bi bi-eye"></i> 查看岗位详情
                          </button>
                        </div>
                      </div>
                    </transition>
                    
                    <!-- 展开提示 -->
                    <div class="expand-indicator">
                      <i class="bi" :class="expandedMatchId === match.id ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                    </div>
                  </div>
                </div>
              </div>

              <div class="step-actions">
                <button class="secondary-btn" @click="runMatchingAnalysis" :disabled="runningMatch">
                  <i class="bi bi-arrow-repeat"></i>
                  <span>重新匹配</span>
                </button>
                <button class="primary-btn" @click="goToReport">
                  <span>生成规划报告</span>
                  <i class="bi bi-file-earmark-text"></i>
                </button>
              </div>
            </template>
            <template v-else>
              <div class="empty-state-card">
                <i class="bi bi-search text-cyan-300"></i>
                <h3>暂无匹配结果</h3>
                <p>{{ matchError || '可以重试匹配，或先补充画像信息。' }}</p>
                <button class="primary-btn" @click="runMatchingAnalysis" :disabled="runningMatch">
                  <i class="bi bi-arrow-clockwise"></i>
                  <span>重试人岗匹配</span>
                </button>
              </div>
            </template>
          </div>

          <!-- Step 5: 规划报告 -->
          <div v-else-if="currentStep === 5" key="report" class="step-content report-step">
            <template v-if="generatingReport">
              <div class="generating-state">
                <div class="ai-working">
                  <div class="working-animation report">
                    <div class="doc-icon">📄</div>
                    <div class="writing-lines">
                      <div class="line"></div>
                      <div class="line"></div>
                      <div class="line"></div>
                    </div>
                  </div>
                  <h3>AI正在撰写你的职业规划报告...</h3>
                  <p class="generating-step">{{ reportStep }}</p>
                </div>
              </div>
            </template>
            <template v-else-if="report">
              <div class="report-complete-enhanced">
                <!-- 成功头部 -->
                <div class="success-header">
                  <div class="success-icon-wrapper">
                    <div class="success-ring"></div>
                    <div class="success-ring delay"></div>
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                  <h2>🎉 职业规划报告已生成</h2>
                  <p class="success-subtitle">小智为你量身定制了完整的职业发展规划建议</p>
                </div>
                
                <!-- 报告概览卡片 -->
                <div class="report-overview-card">
                  <div class="overview-header">
                    <i class="bi bi-file-earmark-richtext"></i>
                    <span>{{ report.title || '职业生涯发展报告' }}</span>
                  </div>
                  <div class="overview-stats">
                    <div class="stat-item">
                      <span class="stat-value">{{ reportSections.length }}</span>
                      <span class="stat-label">核心章节</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-value">{{ matchResults.length }}</span>
                      <span class="stat-label">推荐岗位</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-value">AI</span>
                      <span class="stat-label">智能分析</span>
                    </div>
                  </div>
                </div>
                
                <!-- 章节预览卡片网格 -->
                <div class="report-sections-grid">
                  <div 
                    v-for="(section, idx) in reportSections" 
                    :key="section.key" 
                    class="section-card"
                    :style="{ animationDelay: (idx * 0.1) + 's' }"
                  >
                    <div class="section-card-header">
                      <div class="section-icon" :class="getSectionColorClass(idx)">
                        <i :class="section.icon"></i>
                      </div>
                      <div class="section-title">
                        <span class="section-num">第 {{ idx + 1 }} 章</span>
                        <h4>{{ section.label }}</h4>
                      </div>
                    </div>
                    <div class="section-preview-text">
                      {{ getReportPreview(section.key) || '内容生成中...' }}
                    </div>
                    <div class="section-card-footer">
                      <span class="preview-hint">
                        <i class="bi bi-eye"></i> 查看完整内容
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- 下一步提示 -->
                <div class="next-steps-card">
                  <div class="next-steps-header">
                    <i class="bi bi-signpost-split text-amber-400"></i>
                    <span>接下来你可以...</span>
                  </div>
                  <div class="next-steps-list">
                    <div class="next-step-item">
                      <div class="step-icon">📖</div>
                      <div class="step-content">
                        <h5>阅读完整报告</h5>
                        <p>深入了解每个章节的详细分析和建议</p>
                      </div>
                    </div>
                    <div class="next-step-item">
                      <div class="step-icon">✏️</div>
                      <div class="step-content">
                        <h5>编辑和优化</h5>
                        <p>根据你的实际情况调整报告内容</p>
                      </div>
                    </div>
                    <div class="next-step-item">
                      <div class="step-icon">📤</div>
                      <div class="step-content">
                        <h5>导出和分享</h5>
                        <p>将报告导出为PDF或分享给他人</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="report-actions-enhanced">
                  <router-link :to="`/reports/${selectedStudent?.id}`" class="action-card primary">
                    <i class="bi bi-eye-fill"></i>
                    <span>查看完整报告</span>
                  </router-link>
                  <router-link :to="`/reports/${selectedStudent?.id}/edit`" class="action-card secondary">
                    <i class="bi bi-pencil-square"></i>
                    <span>编辑报告</span>
                  </router-link>
                  <button class="action-card tertiary" @click="exportReport">
                    <i class="bi bi-download"></i>
                    <span>导出PDF</span>
                  </button>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="empty-state-card">
                <i class="bi bi-file-earmark-x text-amber-300"></i>
                <h3>报告暂未生成</h3>
                <p>{{ reportError || '请重试生成报告。' }}</p>
                <button class="primary-btn" @click="generateReportAsync" :disabled="generatingReport">
                  <i class="bi bi-arrow-clockwise"></i>
                  <span>重试生成报告</span>
                </button>
              </div>
            </template>
          </div>
        </transition>
      </div>
    </main>

    <!-- 已有档案选择弹窗 -->
    <transition name="modal">
      <div v-if="showExistingSelector" class="modal-overlay" @click.self="showExistingSelector = false">
        <div class="modal-content selector-modal">
          <div class="modal-header">
            <h3><i class="bi bi-people"></i> 选择已有档案</h3>
            <button class="close-btn" @click="showExistingSelector = false">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="student-list">
              <div 
                v-for="s in students" 
                :key="s.id" 
                class="student-item"
                @click="selectExistingStudent(s)"
              >
                <div class="student-avatar">{{ (s.name || '?')[0] }}</div>
                <div class="student-info">
                  <span class="student-name">{{ s.name || '未命名' }}</span>
                  <span class="student-meta">{{ s.education || '学历未知' }} · {{ s.major || '专业未知' }}</span>
                </div>
                <div class="student-status">
                  <span v-if="s.has_profile" class="status-tag success">有画像</span>
                  <span v-if="s.has_report" class="status-tag warning">有报告</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, inject, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import RadarChart from '@/components/RadarChart.vue'
import {
  getStudents,
  getStudent,
  createStudent,
  generateStudentProfile as apiGenerateProfile,
  runMatching,
  generateAdvancedReport,
  getJobProfiles,
} from '@/api'

const router = useRouter()
const toast = inject('toast', null)

// ========== 状态 ==========
const currentStep = ref(0)
const students = ref([])
const selectedStudent = ref(null)
const studentProfile = ref(null)
const matchResults = ref([])
const report = ref(null)
const jobProfiles = ref([])

// 步骤标签
const stepLabels = ['开始', '基本信息', '求职意向', '能力画像', '人岗匹配', '规划报告']

// Agent状态
const isThinking = ref(false)
const isSpeaking = ref(false)
const isHappy = ref(false)
const eyeState = ref('normal')
const mouthState = ref('normal')

// 对话消息
const messages = ref([])
const visibleMessages = computed(() => messages.value.slice(-4))

// Step 1: 信息收集
const infoMode = ref('resume')
const selectedFile = ref(null)
const isDragging = ref(false)
const formData = ref({
  name: '',
  education: '',
  major: '',
  school: '',
  skills: '',
  summary: ''
})
const isProcessing = ref(false)

// Step 2: 求职意向
const positionTags = ['产品经理', '前端开发', '后端开发', '数据分析师', 'UI设计师', 'AI工程师', '运营', '市场营销']
const industryTags = ['互联网', '金融', '教育', '医疗', '电商', '游戏', '人工智能', '新能源']
const priorityOptions = [
  { id: 'salary', icon: '💰', label: '高薪酬', desc: '追求更高的收入回报' },
  { id: 'growth', icon: '📈', label: '快成长', desc: '看重学习和晋升空间' },
  { id: 'balance', icon: '⚖️', label: '好平衡', desc: '工作与生活质量兼顾' },
  { id: 'stable', icon: '🏢', label: '稳定性', desc: '偏好稳定的工作环境' }
]
const selectedPositions = ref([])
const selectedIndustries = ref([])
const selectedPriorities = ref([])
const customPosition = ref('')

// Step 3: 生成画像
const generatingProfile = ref(false)
const generatingProgress = ref(0)
const generatingStep = ref('')
const profileError = ref('')

// Step 4: 匹配
const runningMatch = ref(false)
const matchingStep = ref('')
const matchError = ref('')
const expandedMatchId = ref(null)  // 展开的匹配卡片ID

// Step 5: 报告
const generatingReport = ref(false)
const reportStep = ref('')
const reportError = ref('')

// Modal
const showExistingSelector = ref(false)
const submittingTarget = ref(false)

// 雷达图配置
const abilityMeta = [
  { key: 'innovation_ability', name: '创新能力' },
  { key: 'learning_ability', name: '学习能力' },
  { key: 'pressure_resistance', name: '抗压能力' },
  { key: 'communication_skill', name: '沟通能力' },
  { key: 'teamwork_ability', name: '团队协作' },
  { key: 'internship_ability', name: '实践能力' },
]

const radarIndicators = computed(() => abilityMeta.map(item => item.name))
const radarSeries = computed(() => [{
  name: '能力画像',
  values: abilityMeta.map(meta => Number(studentProfile.value?.[meta.key] || 0)),
  color: '#7c3aed',
}])

const reportSections = [
  { key: 'section_self_assessment', label: '自我评估', icon: 'bi bi-person-check' },
  { key: 'section_job_exploration', label: '职业探索', icon: 'bi bi-compass' },
  { key: 'section_career_goal', label: '目标设定', icon: 'bi bi-bullseye' },
  { key: 'section_career_path', label: '路径规划', icon: 'bi bi-signpost-split' },
  { key: 'section_action_plan', label: '行动计划', icon: 'bi bi-list-check' },
]

// ========== 计算属性 ==========
const canSubmitInfo = computed(() => {
  if (infoMode.value === 'resume') {
    return !!selectedFile.value
  }
  return formData.value.name.trim() !== ''
})

const canSubmitTarget = computed(() => {
  return selectedPositions.value.length > 0 || customPosition.value.trim() !== ''
})

// ========== 方法 ==========
function particleStyle(i) {
  const size = 2 + Math.random() * 4
  return {
    width: size + 'px',
    height: size + 'px',
    left: Math.random() * 100 + '%',
    top: Math.random() * 100 + '%',
    animationDelay: Math.random() * 5 + 's',
    animationDuration: (3 + Math.random() * 4) + 's'
  }
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function toggleTag(arr, tag) {
  const idx = arr.indexOf(tag)
  if (idx === -1) {
    arr.push(tag)
  } else {
    arr.splice(idx, 1)
  }
}

function addCustomPosition() {
  const val = customPosition.value.trim()
  if (val && !selectedPositions.value.includes(val)) {
    selectedPositions.value.push(val)
    customPosition.value = ''
  }
}

// 添加AI消息（带打字机效果）
async function addAgentMessage(text, delay = 30) {
  if (!text || !String(text).trim()) {
    return
  }

  const msg = {
    id: Date.now(),
    type: 'agent',
    text,
    displayText: '',
    typing: true
  }
  messages.value.push(msg)
  isSpeaking.value = true
  mouthState.value = 'speaking'

  for (let i = 0; i <= text.length; i++) {
    msg.displayText = text.slice(0, i)
    await new Promise(r => setTimeout(r, delay))
  }
  
  msg.typing = false
  isSpeaking.value = false
  mouthState.value = 'normal'
}

// 开始旅程
async function startJourney() {
  currentStep.value = 1
  await addAgentMessage('你好呀！欢迎来到职业规划中心 👋')
  await new Promise(r => setTimeout(r, 600))
  await addAgentMessage('我是小智，你的专属职业规划助手，很高兴认识你！😊')
  await new Promise(r => setTimeout(r, 500))
  await addAgentMessage('首先，让我了解一下你的基本情况吧~你可以上传简历，或者手动填写信息。')
}

// 文件处理
function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    addAgentMessage(`收到了 "${file.name}"！看起来不错~`)
  }
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file && /\.(pdf|docx?|doc)$/i.test(file.name)) {
    selectedFile.value = file
    addAgentMessage(`收到了 "${file.name}"！看起来不错~`)
  } else {
    toast?.('请上传 PDF 或 Word 格式的简历', 'warning')
  }
}

// 提交基本信息
async function submitInfo() {
  isProcessing.value = true
  
  try {
    await addAgentMessage('好的，让我来解析一下你的信息...')
    
    // 创建学生档案
    const fd = new FormData()
    if (selectedFile.value) {
      // 后端期望字段名为 'resume_file'
      fd.append('resume_file', selectedFile.value)
    }
    fd.append('name', formData.value.name || '新用户')
    fd.append('education', formData.value.education || '')
    fd.append('major', formData.value.major || '')
    fd.append('school', formData.value.school || '')
    fd.append('skills', formData.value.skills || '')
    fd.append('resume_text', formData.value.summary || '')
    
    const res = await createStudent(fd)
    if (res.data?.success) {
      selectedStudent.value = res.data.data || res.data.student
      await loadStudentDetail()
      
      // 检查是否有PDF解析警告
      if (res.data?.warning) {
        toast?.(res.data.warning, 'warning')
        await addAgentMessage('⚠️ 简历文件解析可能不完整，建议检查一下信息是否正确哦~')
      } else {
        isHappy.value = true
        // 根据简历内容给出个性化夸奖
        const userName = formData.value.name || selectedStudent.value?.name || '同学'
        const school = selectedStudent.value?.school || formData.value.school
        const major = selectedStudent.value?.major || formData.value.major
        
        let praiseMsg = `太棒了 ${userName}！你的简历已经成功解析 ✅`
        if (school && major) {
          praiseMsg = `哇！${userName}，${school}${major}专业，背景很不错呢！简历解析完成 ✅`
        } else if (major) {
          praiseMsg = `${userName}，${major}专业背景很扎实！简历解析完成 ✅`
        }
        await addAgentMessage(praiseMsg)
        
        // 根据简历具体内容给出更详细的鼓励（从resume_text读取）
        await new Promise(r => setTimeout(r, 600))
        const detailedPraises = []
        const resumeText = selectedStudent.value?.resume_text || formData.value.summary || ''
        
        // 检测技术关键词并给出鼓励
        const techKeywords = {
          'Python': '看到你会 Python，这是非常热门的编程语言，在数据分析和AI领域大有可为！🐍',
          'Java': '你掌握了 Java，这可是企业级开发的首选语言，市场需求很大！☕',
          'JavaScript': '你会 JavaScript，前端开发必备技能，很实用！',
          'C++': '看到你会 C++，底层开发能力很强呢！',
          'Vue': '你会 Vue.js，前端框架技能很加分！',
          'React': '掌握 React，前端技能非常棒！',
          'Spring': '会用 Spring 框架，Java 后端开发能力很扎实！',
          'MySQL': '熟悉 MySQL 数据库，后端必备技能！',
          'Linux': '会用 Linux，运维和开发都很需要这个技能！',
          '机器学习': '有机器学习经验，AI方向很有前景！🤖',
          '深度学习': '会深度学习，这是AI领域的核心技能！',
          'TensorFlow': '会用 TensorFlow，深度学习框架技能很棒！',
          'PyTorch': '掌握 PyTorch，AI研究和应用都很需要！'
        }
        
        // 查找简历中的技术关键词
        for (const [keyword, praise] of Object.entries(techKeywords)) {
          if (resumeText.toLowerCase().includes(keyword.toLowerCase())) {
            detailedPraises.push(praise)
            break  // 只显示第一个匹配的技能夸奖
          }
        }
        
        // 检测经验亮点
        if (resumeText.includes('项目') || resumeText.includes('开发')) {
          detailedPraises.push('有项目实战经验，这对求职很加分！💪')
        } else if (resumeText.includes('实习')) {
          detailedPraises.push('有实习经历太棒了，这是宝贵的职场经验！')
        } else if (resumeText.includes('比赛') || resumeText.includes('竞赛') || resumeText.includes('获奖')) {
          detailedPraises.push('参加过比赛/获过奖，说明你很有上进心！🏆')
        }
        
        // 检测学历亮点
        const topSchools = ['清华', '北大', '浙大', '复旦', '交大', '中科', '985', '211']
        if (topSchools.some(s => resumeText.includes(s))) {
          detailedPraises.push('名校背景，起点很高呢！🎓')
        }
        
        // 输出最多2条详细鼓励
        for (let i = 0; i < Math.min(2, detailedPraises.length); i++) {
          await addAgentMessage(detailedPraises[i])
          await new Promise(r => setTimeout(r, 400))
        }
        
        setTimeout(() => { isHappy.value = false }, 1500)
      }
      
      await new Promise(r => setTimeout(r, 800))
      currentStep.value = 2
      await addAgentMessage('接下来，告诉我你的求职意向吧~你想从事什么样的工作呢？')
    }
  } catch (err) {
    toast?.(err?.response?.data?.message || '信息提交失败', 'danger')
    await addAgentMessage('😅 哎呀，出了点问题，请稍后重试~')
  } finally {
    isProcessing.value = false
  }
}

// 提交求职意向
async function submitTarget() {
  if (submittingTarget.value || generatingProfile.value) return
  submittingTarget.value = true

  // 更新学生的目标岗位
  const targets = [...selectedPositions.value]
  if (customPosition.value.trim()) {
    targets.push(customPosition.value.trim())
  }
  
  if (selectedStudent.value) {
    selectedStudent.value.target_positions = targets
  }
  
  // 先设置生成状态，避免切换步骤后闪烁失败界面
  generatingProfile.value = true
  profileError.value = ''
  currentStep.value = 3
  
  // 根据选择给出个性化反馈
  if (targets.length > 0) {
    const targetStr = targets.slice(0, 2).join('、')
    await addAgentMessage(`${targetStr}方向很有发展前景呢！好选择 👍`)
    await new Promise(r => setTimeout(r, 500))
  }
  await addAgentMessage('让我来为你生成专属的能力画像... 🔮')
  
  await generateProfile()
  submittingTarget.value = false
}

// 生成画像
async function generateProfile() {
  if (!selectedStudent.value?.id) {
    generatingProfile.value = false
    return
  }
  // 如果不是从submitTarget进入，需要重置状态
  if (!generatingProfile.value) {
    profileError.value = ''
    generatingProfile.value = true
  }
  generatingProgress.value = 0
  
  const steps = [
    { step: '正在分析你的教育背景...', message: '看起来你的学习经历很丰富呢！📚' },
    { step: '正在评估你的技能水平...', message: '你掌握的技能很有竞争力哦！💡' },
    { step: '正在计算能力维度...', message: '正在深入分析你的各项能力，很快就好~' },
    { step: '正在生成优势与建议...', message: '发现了不少亮点呢！让我帮你总结一下 ✨' },
    { step: '即将完成！', message: '' }
  ]
  
  // 模拟进度与互动
  for (let i = 0; i < steps.length; i++) {
    generatingStep.value = steps[i].step
    generatingProgress.value = (i + 1) * 20
    if (i === 0 && steps[i].message) {
      await addAgentMessage(steps[i].message)
    }
    await new Promise(r => setTimeout(r, 700))
    // 中间穿插鼓励
    if (i === 2) {
      await addAgentMessage('你很棒的，相信自己！💪')
    }
  }
  
  try {
    const res = await apiGenerateProfile(selectedStudent.value.id)
    if (res.data?.success) {
      studentProfile.value = res.data.data
      
      isHappy.value = true
      // 根据画像结果给出个性化评价
      const profile = res.data.data
      let compliment = '画像生成完成！来看看你的能力分析吧~ 🎉'
      if (profile.competitiveness_score >= 80) {
        compliment = '哇！你的综合竞争力评分很高呢！非常优秀 🌟'
      } else if (profile.competitiveness_score >= 60) {
        compliment = '画像生成完成！你的能力很全面，继续加油！🎉'
      } else if (profile.strengths?.length > 2) {
        compliment = '画像生成完成！发现了你不少闪光点呢~来看看吧 ✨'
      }
      await addAgentMessage(compliment)
      setTimeout(() => { isHappy.value = false }, 2000)
    } else {
      profileError.value = res.data?.message || '画像生成失败'
      toast?.(profileError.value, 'danger')
      await addAgentMessage('画像生成遇到问题了，我帮你保留了当前信息，请点击重试。')
    }
  } catch (err) {
    profileError.value = err?.response?.data?.message || '画像生成失败'
    toast?.(profileError.value, 'danger')
    await addAgentMessage('画像生成遇到问题了，我帮你保留了当前信息，请点击重试。')
  } finally {
    generatingProfile.value = false
  }
}

// 进入匹配
async function goToMatching() {
  if (runningMatch.value) return
  runningMatch.value = true  // 先设置匹配状态，避免显示空状态闪烁
  matchError.value = ''
  currentStep.value = 4
  await addAgentMessage('接下来，我会根据你的画像，为你匹配最适合的岗位！')
  await runMatchingAnalysis()
}

// 运行匹配
async function runMatchingAnalysis() {
  if (!selectedStudent.value?.id) {
    runningMatch.value = false
    return
  }
  if (!runningMatch.value) {
    // 如果不是从goToMatching进入，需要设置状态
    matchError.value = ''
    runningMatch.value = true
  }
  
  // 更丰富的匹配步骤与互动消息
  const steps = [
    { step: '正在扫描岗位库...', message: '我正在为你搜索全库岗位，这可能需要一点时间~ ☕' },
    { step: '正在计算匹配度...', message: '根据你的技能和经验，逐一评估每个岗位的契合度 🔍' },
    { step: '正在分析技能差距...', message: '分析哪些技能可以锦上添花，为你找到最优路径 🛤️' },
    { step: '正在排序推荐结果...', message: '快完成了！正在为你筛选出最优选择 ✨' }
  ]
  
  for (let i = 0; i < steps.length; i++) {
    matchingStep.value = steps[i].step
    if (i === 0) {
      await addAgentMessage(steps[i].message)
    }
    await new Promise(r => setTimeout(r, 1200))
    // 中间穿插互动
    if (i === 1) {
      await addAgentMessage('你的背景很有亮点呢！相信会有好结果的 💪')
    }
  }
  
  try {
    const res = await runMatching(selectedStudent.value.id, 5)
    if (res.data?.success) {
      matchResults.value = res.data.data || []
      
      if (matchResults.value.length) {
        isHappy.value = true
        // 根据匹配结果给出个性化反馈
        const topMatch = matchResults.value[0]
        const topScore = Number(topMatch?.final_score || topMatch?.score || 0)
        let matchMsg = `太好了！找到了 ${matchResults.value.length} 个很适合你的岗位！🎯`
        if (topScore >= 85) {
          matchMsg = `哇！发现了非常契合你的岗位！最高匹配度达到 ${topScore.toFixed(0)} 分！🌟`
        } else if (topScore >= 70) {
          matchMsg = `找到了 ${matchResults.value.length} 个不错的岗位推荐，来看看哪个最心仪吧！🎯`
        }
        await addAgentMessage(matchMsg)
        setTimeout(() => { isHappy.value = false }, 2000)
      } else {
        await addAgentMessage('暂时没有找到匹配的岗位，你可以尝试调整求职意向~')
      }
    } else {
      matchResults.value = []
      matchError.value = res.data?.message || '匹配分析失败'
      toast?.(matchError.value, 'danger')
      await addAgentMessage('匹配过程遇到问题了，请点击重试人岗匹配。')
    }
  } catch (err) {
    matchResults.value = []
    matchError.value = err?.response?.data?.message || '匹配分析失败'
    toast?.(matchError.value, 'danger')
    await addAgentMessage('匹配过程遇到问题了，请点击重试人岗匹配。')
  } finally {
    runningMatch.value = false
  }
}

function selectMatch(match) {
  // 可以跳转到岗位详情
  router.push(`/jobs/profiles/${match.job_profile_id}`)
}

// 匹配卡片展开切换
function toggleMatchExpand(matchId) {
  if (expandedMatchId.value === matchId) {
    expandedMatchId.value = null
  } else {
    expandedMatchId.value = matchId
  }
}

// 查看岗位详情
function viewJobProfile(profileId) {
  router.push(`/jobs/profiles/${profileId}`)
}

// 获取技能名称列表（处理不同格式的技能数据）
function getSkillNames(skills) {
  if (!skills) return []
  if (typeof skills === 'string') {
    try {
      skills = JSON.parse(skills)
    } catch {
      return [skills]
    }
  }
  if (!Array.isArray(skills)) return []
  return skills.map(s => {
    if (typeof s === 'string') return s
    if (typeof s === 'object' && s !== null) {
      return s.name || s.skill || s.title || JSON.stringify(s)
    }
    return String(s)
  }).filter(Boolean)
}

// 获取分数等级样式
function getScoreClass(score) {
  const s = Number(score || 0)
  if (s >= 80) return 'excellent'
  if (s >= 60) return 'good'
  if (s >= 40) return 'fair'
  return 'poor'
}

// 解析匹配详情分析
function getMatchAnalysis(match, key) {
  if (!match.detail_analysis) return null
  try {
    const analysis = typeof match.detail_analysis === 'string' 
      ? JSON.parse(match.detail_analysis) 
      : match.detail_analysis
    return analysis[key]
  } catch {
    return null
  }
}

// 获取推荐建议
function getMatchRecommendations(match) {
  if (!match.recommendations) return []
  try {
    return typeof match.recommendations === 'string' 
      ? JSON.parse(match.recommendations) 
      : match.recommendations
  } catch {
    return []
  }
}

// 生成报告
async function goToReport() {
  if (generatingReport.value) return
  currentStep.value = 5
  await addAgentMessage('最后一步！我来为你撰写一份完整的职业规划报告 📝')
  await generateReportAsync()
}

async function generateReportAsync() {
  if (!selectedStudent.value?.id) return
  if (generatingReport.value) return
  
  reportError.value = ''
  generatingReport.value = true
  
  const steps = [
    '正在分析自我评估内容...',
    '正在探索职业方向...',
    '正在设定职业目标...',
    '正在规划发展路径...',
    '正在撰写行动建议...',
    '即将完成报告！'
  ]
  
  for (const step of steps) {
    reportStep.value = step
    await new Promise(r => setTimeout(r, 1200))
  }
  
  try {
    const res = await generateAdvancedReport(selectedStudent.value.id, true)
    if (res.data?.success) {
      report.value = res.data.data
      
      isHappy.value = true
      await addAgentMessage('报告已经生成好了！恭喜你完成了整个职业规划流程 🎊')
      setTimeout(() => { isHappy.value = false }, 2000)
    } else {
      report.value = null
      reportError.value = res.data?.message || '报告生成失败'
      toast?.(reportError.value, 'danger')
      await addAgentMessage('报告生成遇到问题了，请点击重试生成报告。')
    }
  } catch (err) {
    report.value = null
    reportError.value = err?.response?.data?.message || '报告生成失败'
    toast?.(reportError.value, 'danger')
    await addAgentMessage('报告生成遇到问题了，请点击重试生成报告。')
  } finally {
    generatingReport.value = false
  }
}

function getReportPreview(key) {
  const content = report.value?.[key] || ''
  return content.slice(0, 100) + (content.length > 100 ? '...' : '')
}

// 获取章节颜色类
function getSectionColorClass(index) {
  const colors = ['violet', 'cyan', 'amber', 'emerald', 'rose']
  return colors[index % colors.length]
}

// 导出报告
function exportReport() {
  if (selectedStudent.value?.id) {
    window.open(`/api/reports/${selectedStudent.value.id}/export/pdf`, '_blank')
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 选择已有学生
async function selectExistingStudent(student) {
  showExistingSelector.value = false
  selectedStudent.value = student
  await loadStudentDetail()
  
  // 根据学生状态跳转到对应步骤
  if (report.value) {
    currentStep.value = 5
    await addAgentMessage(`欢迎回来，${student.name}！你已经有了完整的职业规划报告~ 📋`)
  } else if (matchResults.value.length) {
    currentStep.value = 4
    await addAgentMessage(`欢迎回来，${student.name}！你的匹配结果还在这里~ 🔗`)
  } else if (studentProfile.value) {
    currentStep.value = 3
    await addAgentMessage(`欢迎回来，${student.name}！你的能力画像已经生成了~ 📊`)
  } else {
    currentStep.value = 2
    await addAgentMessage(`欢迎回来，${student.name}！让我们继续完善你的求职意向吧~`)
  }
}

async function loadStudentDetail() {
  if (!selectedStudent.value?.id) return
  
  try {
    const res = await getStudent(selectedStudent.value.id)
    selectedStudent.value = res.data?.student || selectedStudent.value
    studentProfile.value = res.data?.profile || null
    matchResults.value = res.data?.match_results || []
    report.value = res.data?.report || null
  } catch (err) {
    console.error('Failed to load student detail:', err)
  }
}

// 眨眼动画
let blinkTimer = null
onMounted(async () => {
  // 加载学生列表
  try {
    const res = await getStudents()
    students.value = Array.isArray(res.data)
      ? res.data
      : (res.data?.students || res.data?.data || [])
  } catch (err) {
    console.error('Failed to load students:', err)
  }
  
  // 加载岗位画像
  try {
    const res = await getJobProfiles()
    jobProfiles.value = res.data?.data || []
  } catch (err) {
    console.error('Failed to load job profiles:', err)
  }
  
  // 眨眼
  blinkTimer = setInterval(() => {
    if (eyeState.value === 'normal' && !isThinking.value) {
      eyeState.value = 'blink'
      setTimeout(() => { eyeState.value = 'normal' }, 150)
    }
  }, 3500)
  
  // 初始欢迎
  await addAgentMessage('嗨，我是小智，你的AI职业规划助手！ 👋')
  await new Promise(r => setTimeout(r, 800))
  await addAgentMessage('点击「开始规划」，让我们一起探索最适合你的职业方向吧~ ✨')
})
</script>

<style scoped>
/* ========== 基础布局 ========== */
.planning-journey {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: var(--planning-bg, linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%));
  color: var(--brand-text, #e4e4e7);
}

/* 背景动效 */
.journey-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
  will-change: transform;
  animation: float 30s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--orb-primary, #7c3aed) 0%, transparent 70%);
  top: -150px;
  left: -150px;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}

.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(139, 92, 246, 0.5);
  border-radius: 50%;
  will-change: opacity, transform;
  animation: twinkle 4s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0; transform: scale(0); }
  50% { opacity: 0.8; transform: scale(1); }
}

/* ========== 顶部导航 ========== */
.journey-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(15, 15, 26, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  transform: translateX(-2px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.step-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.step-dot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.3s;
}

.step-dot.active .step-num {
  background: linear-gradient(135deg, #7c3aed, #06b6d4);
  border-color: transparent;
  color: white;
}

.step-dot.current .step-num {
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
  transform: scale(1.1);
}

.step-label {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.4);
  white-space: nowrap;
}

.step-dot.active .step-label {
  color: rgba(139, 92, 246, 0.8);
}

.step-line {
  width: 30px;
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1px;
  margin-bottom: 1rem;
  transition: all 0.3s;
}

.step-line.filled {
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
}

.header-right {
  min-width: 120px;
  display: flex;
  justify-content: flex-end;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #a1a1aa;
  font-size: 0.875rem;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* ========== 主内容区 ========== */
.journey-main {
  position: relative;
  z-index: 5;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
  padding: 2rem 3rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Agent区域 - 与CareerAIAssistant一致的机器人样式 */
.agent-section {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.25rem 1.5rem;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 24px;
  border: 1px solid rgba(139, 92, 246, 0.1);
}

.agent-avatar {
  position: relative;
  flex-shrink: 0;
  padding: 8px;
}

/* 脉冲环动画 - 简化版 */
.pulse-ring {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 2px solid rgba(139, 92, 246, 0.3);
  will-change: transform, opacity;
  animation: pulse 3s ease-out infinite;
}

.pulse-ring.delay {
  display: none; /* 移除第二个脉冲环以提升性能 */
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.6); opacity: 0; }
}

.avatar-glow {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.25) 0%, transparent 70%);
  /* 移除filter blur和animation以提升性能 */
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

.avatar-body {
  width: 72px;
  height: 72px;
  position: relative;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.avatar-body:hover {
  transform: scale(1.08);
}

.agent-avatar.happy .avatar-body {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.antenna {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.antenna::before {
  content: '';
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
  margin-top: -2px;
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

/* 可爱的黄色圆脸 */
.face {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(145deg, #fef3c7, #fde68a);
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.15), 
    inset 0 -4px 12px rgba(0, 0, 0, 0.05), 
    inset 0 4px 8px rgba(255, 255, 255, 0.8);
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

.eye.blink {
  height: 3px;
  border-radius: 3px;
}

.eye.happy {
  height: 8px;
  border-radius: 8px 8px 50% 50%;
}

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

.eye.blink .pupil,
.eye.happy .pupil {
  display: none;
}

.eye::after {
  content: '';
  position: absolute;
  top: 3px;
  right: 3px;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
}

.eye.blink::after,
.eye.happy::after {
  display: none;
}

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

.mouth.speaking {
  animation: talk 0.25s ease-in-out infinite;
}

.mouth.smile {
  width: 20px;
  height: 10px;
  border-radius: 0 0 20px 20px;
}

@keyframes talk {
  0%, 100% { height: 8px; }
  50% { height: 14px; border-radius: 50%; }
}

.cheeks {
  position: absolute;
  top: 36px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 8px;
  pointer-events: none;
}

.cheek {
  width: 10px;
  height: 6px;
  background: rgba(251, 113, 133, 0.5);
  border-radius: 50%;
}

.agent-name {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 0.65rem;
  color: #10b981;
  font-weight: 500;
  background: rgba(15, 23, 42, 0.9);
  padding: 3px 10px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.agent-avatar.thinking .agent-name {
  color: #f59e0b;
}

.agent-avatar.thinking .status-dot {
  background: #f59e0b;
}

.agent-avatar.thinking .avatar-body {
  animation: thinking-bob 1s ease-in-out infinite;
}

@keyframes thinking-bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.agent-avatar.happy .cheek {
  background: rgba(251, 113, 133, 0.8);
}

/* 对话气泡 - 更自然的对话风格 */
.agent-dialogue {
  flex: 1;
  max-width: 600px;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  animation: message-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message-content {
  display: inline-block;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.08));
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 20px 20px 20px 6px;
  font-size: 1rem;
  line-height: 1.7;
  max-width: 100%;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.1);
}

.typing-text .cursor {
  color: #7c3aed;
  animation: blink-cursor 0.8s step-end infinite;
}

@keyframes blink-cursor {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* ========== 内容区域 ========== */
.content-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 过渡动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* ========== Step 0: 欢迎页 ========== */
.welcome-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}

.welcome-hero {
  margin-bottom: 3rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.gradient-text {
  background: linear-gradient(135deg, #7c3aed, #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.highlight-text {
  color: white;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: #a1a1aa;
}

.welcome-features {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  transition: all 0.3s;
}

.feature-card:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 2rem;
}

.feature-text h3 {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.feature-text p {
  font-size: 0.875rem;
  color: #71717a;
}

.welcome-actions {
  display: flex;
  gap: 1rem;
}

/* 按钮样式 */
.primary-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  border: none;
  border-radius: 14px;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5);
}

.primary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.primary-btn.pulse {
  animation: btn-pulse 2s ease-in-out infinite;
}

@keyframes btn-pulse {
  0%, 100% { box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4); }
  50% { box-shadow: 0 8px 40px rgba(139, 92, 246, 0.6); }
}

.secondary-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 14px;
  color: #a1a1aa;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-color: rgba(255, 255, 255, 0.25);
}

/* ========== Step 1: 信息收集 ========== */
.info-step {
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
}

.info-modes {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 1.5rem;
}

.mode-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 0.25rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
}

.mode-tabs button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #71717a;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.mode-tabs button.active {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.mode-tabs button:hover:not(.active) {
  color: #a1a1aa;
}

/* 上传区域 */
.upload-zone {
  border: 2px dashed rgba(139, 92, 246, 0.3);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-zone:hover,
.upload-zone.dragging {
  border-color: #7c3aed;
  background: rgba(139, 92, 246, 0.05);
}

.upload-zone.uploaded {
  border-style: solid;
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.upload-icon {
  font-size: 3rem;
  color: #7c3aed;
  margin-bottom: 1rem;
}

.upload-zone h3 {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.upload-zone p {
  color: #71717a;
  margin-bottom: 0.75rem;
}

.file-types {
  font-size: 0.75rem;
  color: #52525b;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-preview i {
  font-size: 2.5rem;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 500;
  display: block;
}

.file-size {
  font-size: 0.875rem;
  color: #71717a;
}

.remove-file {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.3s;
}

.remove-file:hover {
  background: rgba(239, 68, 68, 0.2);
}

.upload-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #71717a;
}

/* 表单 */
.manual-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #a1a1aa;
}

.form-group label .hint {
  font-weight: 400;
  color: #52525b;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-input {
  padding: 0.875rem 1rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.form-input::placeholder {
  color: #52525b;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

select.form-input {
  cursor: pointer;
}

.step-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

/* ========== Step 2: 求职意向 ========== */
.target-step {
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.target-questions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.question-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 1.5rem;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.q-num {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
}

.question-header h3 {
  font-size: 1rem;
  font-weight: 500;
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-selector button {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  color: #a1a1aa;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.tag-selector button:hover {
  border-color: rgba(139, 92, 246, 0.5);
  color: white;
}

.tag-selector button.selected {
  background: rgba(139, 92, 246, 0.2);
  border-color: #7c3aed;
  color: #a78bfa;
}

.priority-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.priority-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.priority-card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
}

.priority-card.selected {
  background: rgba(139, 92, 246, 0.15);
  border-color: #7c3aed;
}

.priority-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.priority-label {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.priority-desc {
  font-size: 0.75rem;
  color: #71717a;
}

/* ========== Step 3 & 4: 生成状态 ========== */
.generating-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-working {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.working-animation {
  position: relative;
  width: 160px;
  height: 160px;
  margin-bottom: 2rem;
}

.ring {
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: #7c3aed;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.ring-2 {
  inset: 15px;
  border-top-color: #06b6d4;
  animation-direction: reverse;
  animation-duration: 1.2s;
}

.ring-3 {
  inset: 30px;
  border-top-color: #10b981;
  animation-duration: 1s;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.center-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3rem;
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.1); }
}

.ai-working h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.generating-step {
  color: #a78bfa;
  margin-bottom: 1.5rem;
}

.progress-bar {
  width: 300px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* 生成/匹配过程提示卡片 */
.generating-tips,
.matching-tips {
  margin-top: 1.5rem;
}

.tip-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  animation: fadeInUp 0.5s ease;
}

.tip-icon {
  font-size: 1.25rem;
}

.tip-text {
  font-size: 0.875rem;
  color: #c4b5fd;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 匹配动画 */
.working-animation.matching {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.person-icon, .job-icon {
  font-size: 3rem;
  animation: float-icon 2s ease-in-out infinite;
}

.job-icon {
  animation-delay: -1s;
}

@keyframes float-icon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.match-line {
  position: absolute;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
  border-radius: 2px;
  animation: pulse-line 1s ease-in-out infinite;
}

@keyframes pulse-line {
  0%, 100% { opacity: 0.3; transform: scaleX(0.8); }
  50% { opacity: 1; transform: scaleX(1.2); }
}

/* 报告动画 */
.working-animation.report {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.doc-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.writing-lines {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.writing-lines .line {
  width: 80px;
  height: 4px;
  background: rgba(139, 92, 246, 0.5);
  border-radius: 2px;
  animation: write-line 1.5s ease-in-out infinite;
}

.writing-lines .line:nth-child(2) {
  width: 60px;
  animation-delay: 0.2s;
}

.writing-lines .line:nth-child(3) {
  width: 70px;
  animation-delay: 0.4s;
}

@keyframes write-line {
  0% { transform: scaleX(0); transform-origin: left; }
  50% { transform: scaleX(1); transform-origin: left; }
  50.01% { transform-origin: right; }
  100% { transform: scaleX(0); transform-origin: right; }
}

/* ========== Step 3: 画像结果 ========== */
.profile-result {
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  margin-bottom: 1.5rem;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.profile-info p {
  color: #71717a;
}

.profile-scores {
  display: flex;
  gap: 2rem;
}

.score-item {
  text-align: center;
}

.score-ring {
  position: relative;
  width: 60px;
  height: 60px;
  margin: 0 auto 0.5rem;
}

.score-ring svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.score-ring .ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.1);
  stroke-width: 5;
}

.score-ring .ring-fill {
  fill: none;
  stroke-width: 5;
  stroke-linecap: round;
  stroke-dasharray: 157;
  transition: stroke-dashoffset 1s ease;
}

.score-ring .ring-fill.completeness {
  stroke: #7c3aed;
}

.score-ring .ring-fill.competitiveness {
  stroke: #10b981;
}

.score-ring .score-value {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a78bfa, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.score-label {
  font-size: 0.75rem;
  color: #71717a;
}

/* 技能卡片 */
.skills-section {
  background: rgba(139, 92, 246, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 16px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.skills-section h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #e4e4e7;
}

.skill-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-chip {
  padding: 0.4rem 0.875rem;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 20px;
  font-size: 0.8rem;
  color: #a78bfa;
  font-weight: 500;
  transition: all 0.3s;
}

.skill-chip:hover {
  background: rgba(139, 92, 246, 0.25);
  transform: translateY(-1px);
}

.skill-chip.more {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #71717a;
}

/* 综合评价 */
.evaluation-section {
  background: rgba(6, 182, 212, 0.05);
  border: 1px solid rgba(6, 182, 212, 0.15);
  border-radius: 16px;
  padding: 1.25rem;
  margin-top: 1.5rem;
}

.evaluation-section h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: #e4e4e7;
}

.evaluation-text {
  font-size: 0.875rem;
  color: #a1a1aa;
  line-height: 1.7;
  margin: 0;
}

.abilities-radar {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.abilities-radar h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #a1a1aa;
}

.profile-tags {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.tag-section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.25rem;
}

.tag-section h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8125rem;
}

.tag.success {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.tag.warning {
  background: rgba(251, 146, 60, 0.15);
  color: #fb923c;
  border: 1px solid rgba(251, 146, 60, 0.3);
}

.empty {
  color: #52525b;
  font-size: 0.875rem;
}

/* ========== Step 4: 匹配结果 ========== */
.match-results {
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.results-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
}

.results-count {
  color: #71717a;
  font-size: 0.875rem;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.match-card {
  display: grid;
  grid-template-columns: 50px 1fr auto auto auto;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.match-card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateX(4px);
}

.match-card.top-match {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
  border-color: rgba(139, 92, 246, 0.3);
}

.match-rank {
  width: 40px;
  height: 40px;
  background: rgba(139, 92, 246, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #a78bfa;
}

.match-card.top-match .match-rank {
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  color: white;
}

.match-info h4 {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.match-category {
  font-size: 0.75rem;
  color: #71717a;
}

.match-score {
  text-align: center;
  padding: 0 1rem;
}

.score-num {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #7c3aed, #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: block;
}

.match-details {
  display: flex;
  gap: 0.75rem;
}

.detail-item {
  text-align: center;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  min-width: 50px;
}

.detail-label {
  font-size: 0.625rem;
  color: #71717a;
  display: block;
}

.detail-value {
  font-weight: 600;
  font-size: 0.875rem;
}

.match-gaps {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.gap-label {
  font-size: 0.75rem;
  color: #71717a;
}

.gap-tag {
  padding: 0.25rem 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  font-size: 0.75rem;
  color: #f87171;
}

/* ========== Step 5: 报告完成 ========== */
.report-complete {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
}

.complete-icon {
  font-size: 5rem;
  color: #10b981;
  margin-bottom: 1.5rem;
  animation: pop-in 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes pop-in {
  0% { transform: scale(0); }
  100% { transform: scale(1); }
}

.report-complete h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.report-complete > p {
  color: #71717a;
  margin-bottom: 2rem;
}

.report-preview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  text-align: left;
}

.preview-section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
}

.section-header i {
  color: #a78bfa;
}

.section-preview {
  font-size: 0.75rem;
  color: #71717a;
  line-height: 1.5;
}

.report-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* ========== Modal ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #1a1a2e;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.modal-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  color: #71717a;
  cursor: pointer;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.modal-body {
  padding: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.student-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.student-item:hover {
  border-color: rgba(139, 92, 246, 0.4);
  background: rgba(139, 92, 246, 0.05);
}

.student-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.student-info {
  flex: 1;
}

.student-name {
  font-weight: 500;
  display: block;
}

.student-meta {
  font-size: 0.75rem;
  color: #71717a;
}

.student-status {
  display: flex;
  gap: 0.5rem;
}

.status-tag {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.625rem;
  font-weight: 500;
}

.status-tag.success {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.status-tag.warning {
  background: rgba(251, 146, 60, 0.15);
  color: #fb923c;
}

/* Modal动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(20px);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .journey-header {
    flex-wrap: wrap;
    padding: 0.75rem 1rem;
  }
  
  .header-center {
    order: 3;
    width: 100%;
    margin-top: 0.75rem;
  }
  
  .step-progress {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .step-label {
    display: none;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .welcome-features {
    flex-direction: column;
    gap: 1rem;
  }
  
  .welcome-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .welcome-actions button {
    width: 100%;
    justify-content: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .priority-cards {
    grid-template-columns: 1fr;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-tags {
    grid-template-columns: 1fr;
  }
  
  .match-card {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .match-rank {
    margin: 0 auto;
  }
  
  .match-details {
    justify-content: center;
  }
  
  .match-gaps {
    justify-content: center;
  }
}

/* 动画工具类 */
.animate-spin {
  animation: spin 1s linear infinite;
}

.mt-3 {
  margin-top: 0.75rem;
}

/* ========== 增强版匹配卡片样式 ========== */
.results-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.results-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.results-title h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.results-meta {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: #a1a1aa;
  font-size: 0.875rem;
}

.results-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.results-count strong {
  color: #a78bfa;
}

.results-tip {
  color: #71717a;
  font-size: 0.75rem;
}

.match-card-enhanced {
  position: relative;
  background: rgba(30, 30, 50, 0.6);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.match-card-enhanced::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.match-card-enhanced:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15);
}

.match-card-enhanced:hover::before {
  opacity: 1;
}

.match-card-enhanced.top-match {
  border-color: rgba(251, 191, 36, 0.4);
  background: rgba(40, 35, 50, 0.7);
}

.match-card-enhanced.top-match::before {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, transparent 50%);
  opacity: 1;
}

.match-card-enhanced.expanded {
  background: rgba(35, 35, 55, 0.8);
}

/* 排名徽章 */
.rank-badge {
  position: absolute;
  top: -1px;
  left: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #52525b, #3f3f46);
  padding: 0.35rem 1rem;
  border-radius: 0 0 10px 10px;
  font-size: 0.75rem;
  font-weight: 600;
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1c1917;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #0f172a;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #d97706, #b45309);
  color: #fffbeb;
}

.rank-label {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 主要信息区 */
.card-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  margin-bottom: 1.25rem;
}

.job-info {
  flex: 1;
}

.job-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #f4f4f5;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.75rem;
  color: #a1a1aa;
}

.job-meta span {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.job-meta i {
  font-size: 0.875rem;
  color: #71717a;
}

/* 总分圆形进度 */
.total-score-ring {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.total-score-ring svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.total-score-ring .ring-bg {
  fill: none;
  stroke: rgba(139, 92, 246, 0.15);
  stroke-width: 6;
}

.total-score-ring .ring-progress {
  fill: none;
  stroke: #7c3aed;
  stroke-width: 6;
  stroke-linecap: round;
  stroke-dasharray: 264;
  transition: stroke-dashoffset 0.8s ease;
}

.total-score-ring .ring-progress.excellent {
  stroke: #10b981;
}

.total-score-ring .ring-progress.good {
  stroke: #7c3aed;
}

.total-score-ring .ring-progress.fair {
  stroke: #f59e0b;
}

.total-score-ring .ring-progress.poor {
  stroke: #ef4444;
}

.score-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-text .score-value {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  background: linear-gradient(135deg, #a78bfa, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.score-text .score-unit {
  font-size: 0.625rem;
  color: #71717a;
  margin-top: 0.125rem;
}

/* 四维度评分条 */
.dimension-scores {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem 1.5rem;
  margin-bottom: 0.5rem;
}

.score-bar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.bar-label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  min-width: 80px;
  font-size: 0.75rem;
  color: #a1a1aa;
}

.bar-label i {
  font-size: 0.875rem;
}

.bar-track {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.8s ease;
}

.bar-fill.basic {
  background: linear-gradient(90deg, #06b6d4, #22d3ee);
}

.bar-fill.skill {
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
}

.bar-fill.quality {
  background: linear-gradient(90deg, #f472b6, #ec4899);
}

.bar-fill.potential {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.bar-value {
  min-width: 24px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: right;
  color: #d4d4d8;
}

/* 展开详情区 */
.match-expanded-detail {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.skill-analysis {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.analysis-section h5 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.75rem 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #e4e4e7;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 500;
}

.skill-tag.matched {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.skill-tag.missing {
  background: rgba(251, 191, 36, 0.1);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.2);
}

.recommendations {
  margin-bottom: 1rem;
}

.recommendations h5 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.75rem 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #e4e4e7;
}

.recommend-list {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.8rem;
  color: #a1a1aa;
  line-height: 1.8;
}

.recommend-list li::marker {
  color: #06b6d4;
}

.overall-analysis {
  margin-bottom: 1rem;
}

.overall-analysis h5 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.75rem 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #e4e4e7;
}

.overall-analysis p {
  margin: 0;
  font-size: 0.8rem;
  color: #a1a1aa;
  line-height: 1.7;
}

.detail-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.action-btn.view-profile {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.action-btn.view-profile:hover {
  background: rgba(139, 92, 246, 0.25);
}

/* 展开指示器 */
.expand-indicator {
  display: flex;
  justify-content: center;
  margin-top: 0.75rem;
  color: #71717a;
  font-size: 1rem;
}

/* 展开动画 */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  margin-top: 0;
  padding-top: 0;
}

/* 步骤操作按钮组 */
.step-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.secondary-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.05);
  color: #a1a1aa;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f4f4f5;
}

.secondary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式增强卡片 */
@media (max-width: 768px) {
  .card-main {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .total-score-ring {
    margin: 0 auto;
  }
  
  .job-meta {
    justify-content: center;
  }
  
  .dimension-scores {
    grid-template-columns: 1fr;
  }
  
  .skill-analysis {
    grid-template-columns: 1fr;
  }
  
  .step-actions {
    flex-direction: column;
  }
}

/* ========== 增强版报告样式 ========== */
.report-complete-enhanced {
  max-width: 900px;
  margin: 0 auto;
}

/* 成功头部 */
.success-header {
  text-align: center;
  margin-bottom: 2rem;
}

.success-icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  margin-bottom: 1.25rem;
}

.success-icon-wrapper i {
  font-size: 3rem;
  color: #10b981;
  z-index: 2;
}

.success-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid rgba(16, 185, 129, 0.3);
  animation: ripple 2s ease-out infinite;
}

.success-ring.delay {
  animation-delay: 1s;
}

@keyframes ripple {
  0% {
    transform: scale(1);
    opacity: 0.6;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.success-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #f4f4f5;
}

.success-subtitle {
  color: #a1a1aa;
  margin: 0;
  font-size: 1rem;
}

/* 报告概览卡片 */
.report-overview-card {
  background: rgba(30, 30, 50, 0.6);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
}

.overview-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #e4e4e7;
}

.overview-header i {
  font-size: 1.25rem;
  color: #a78bfa;
}

.overview-stats {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a78bfa, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 0.75rem;
  color: #71717a;
}

/* 章节预览卡片网格 */
.report-sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-card {
  background: rgba(30, 30, 50, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 1.25rem;
  transition: all 0.3s ease;
  animation: fadeInUp 0.5s ease both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-card:hover {
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.12);
}

.section-card-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 0.875rem;
}

.section-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
}

.section-icon.violet {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.section-icon.cyan {
  background: rgba(6, 182, 212, 0.15);
  color: #22d3ee;
}

.section-icon.amber {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.section-icon.emerald {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.section-icon.rose {
  background: rgba(244, 63, 94, 0.15);
  color: #fb7185;
}

.section-title {
  flex: 1;
}

.section-num {
  display: block;
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #71717a;
  margin-bottom: 0.125rem;
}

.section-title h4 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e4e4e7;
}

.section-preview-text {
  font-size: 0.8rem;
  color: #a1a1aa;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.section-card-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 0.75rem;
}

.preview-hint {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.7rem;
  color: #71717a;
}

.preview-hint i {
  font-size: 0.75rem;
}

/* 下一步提示卡片 */
.next-steps-card {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(6, 182, 212, 0.05));
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.next-steps-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #e4e4e7;
}

.next-steps-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.next-step-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.step-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.step-content h5 {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #e4e4e7;
}

.step-content p {
  margin: 0;
  font-size: 0.75rem;
  color: #a1a1aa;
  line-height: 1.5;
}

/* 操作按钮 */
.report-actions-enhanced {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.action-card.primary {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.action-card.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(139, 92, 246, 0.4);
}

.action-card.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #a1a1aa;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-card.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f4f4f5;
}

.action-card.tertiary {
  background: rgba(6, 182, 212, 0.1);
  color: #22d3ee;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.action-card.tertiary:hover {
  background: rgba(6, 182, 212, 0.2);
}

/* 响应式报告样式 */
@media (max-width: 768px) {
  .next-steps-list {
    grid-template-columns: 1fr;
  }
  
  .report-actions-enhanced {
    flex-direction: column;
  }
  
  .action-card {
    justify-content: center;
  }
  
  .overview-stats {
    flex-direction: column;
    gap: 0.75rem;
  }
}

/* ===== Light Mode Overrides ===== */
:global(html.light) .planning-bg {
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

:global(html.light) .planning-header h1 {
  color: #0c4a6e;
}

:global(html.light) .planning-header p {
  color: #64748b;
}

:global(html.light) .header-stats {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .stat-item .stat-value {
  color: #0891b2;
}

:global(html.light) .stat-item .stat-label {
  color: #64748b;
}

:global(html.light) .phase-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .phase-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
  box-shadow: 0 4px 16px rgba(8, 145, 178, 0.1);
}

:global(html.light) .phase-card.active {
  border-color: #0891b2;
}

:global(html.light) .phase-title {
  color: #0c4a6e;
}

:global(html.light) .phase-desc {
  color: #64748b;
}

:global(html.light) .step-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .step-card:hover {
  border-color: rgba(8, 145, 178, 0.25);
}

:global(html.light) .step-card.completed {
  border-color: rgba(16, 185, 129, 0.3);
}

:global(html.light) .step-card.active {
  border-color: #0891b2;
}

:global(html.light) .step-title {
  color: #0c4a6e;
}

:global(html.light) .step-desc {
  color: #64748b;
}

:global(html.light) .step-tags .tag {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
}

:global(html.light) .progress-section {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .progress-title {
  color: #0c4a6e;
}

:global(html.light) .progress-track {
  background: rgba(8, 145, 178, 0.1);
}

:global(html.light) .progress-text {
  color: #64748b;
}

:global(html.light) .sidebar-card {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.12);
}

:global(html.light) .sidebar-title {
  color: #0c4a6e;
}

:global(html.light) .resource-item {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .resource-item:hover {
  background: rgba(8, 145, 178, 0.08);
}

:global(html.light) .resource-name {
  color: #0c4a6e;
}

:global(html.light) .resource-desc {
  color: #64748b;
}

:global(html.light) .milestone-card {
  background: rgba(8, 145, 178, 0.03);
  border-color: rgba(8, 145, 178, 0.1);
}

:global(html.light) .milestone-title {
  color: #0c4a6e;
}

:global(html.light) .milestone-date {
  color: #64748b;
}

:global(html.light) .ai-panel {
  background: #ffffff;
  border-color: rgba(8, 145, 178, 0.15);
}

:global(html.light) .ai-header h3 {
  color: #0c4a6e;
}

:global(html.light) .ai-message {
  background: rgba(8, 145, 178, 0.05);
  color: #475569;
}

:global(html.light) .ai-input input {
  background: rgba(8, 145, 178, 0.05);
  border-color: rgba(8, 145, 178, 0.15);
  color: #0c4a6e;
}

:global(html.light) .btn-send {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .modal-overlay {
  background: rgba(0, 0, 0, 0.3);
}

:global(html.light) .modal-content {
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

:global(html.light) .btn-primary {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
}

:global(html.light) .btn-secondary {
  background: rgba(8, 145, 178, 0.08);
  color: #64748b;
}

:global(html.light) .action-card {
  background: rgba(8, 145, 178, 0.08);
  color: #0891b2;
  border-color: rgba(8, 145, 178, 0.2);
}

:global(html.light) .action-card:hover {
  background: rgba(8, 145, 178, 0.15);
}

:global(html.light) .action-card.secondary {
  background: rgba(100, 116, 139, 0.08);
  color: #64748b;
  border-color: rgba(100, 116, 139, 0.15);
}

:global(html.light) .action-card.secondary:hover {
  background: rgba(100, 116, 139, 0.12);
  color: #475569;
}

:global(html.light) .action-card.tertiary {
  background: rgba(6, 182, 212, 0.08);
  color: #0891b2;
  border-color: rgba(6, 182, 212, 0.2);
}

:global(html.light) .action-card.tertiary:hover {
  background: rgba(6, 182, 212, 0.15);
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
</style>
