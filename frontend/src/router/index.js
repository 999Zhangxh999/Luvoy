import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue'), meta: { hideNav: true, public: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue'), meta: { hideNav: true, public: true } },
  { path: '/', name: 'Home', component: () => import('@/views/HomeView.vue') },
  { path: '/jobs', name: 'Jobs', component: () => import('@/views/JobListView.vue') },
  { path: '/jobs/profiles', name: 'JobProfiles', component: () => import('@/views/JobProfilesView.vue') },
  { path: '/jobs/profiles/:id', name: 'JobProfileDetail', component: () => import('@/views/JobProfileDetailView.vue'), props: true },
  { path: '/graph', name: 'Graph', component: () => import('@/views/JobGraphView.vue') },
  { path: '/students', name: 'Students', component: () => import('@/views/StudentListView.vue') },
  { path: '/students/create', name: 'StudentCreate', component: () => import('@/views/StudentCreateView.vue') },
  { path: '/students/:id', name: 'StudentProfile', component: () => import('@/views/StudentProfileView.vue'), props: true },
  { path: '/matching/:studentId', name: 'Matching', component: () => import('@/views/MatchingResultView.vue'), props: true },
  { path: '/reports/:studentId', name: 'Report', component: () => import('@/views/ReportView.vue'), props: true },
  { path: '/reports/:studentId/edit', name: 'ReportEdit', component: () => import('@/views/ReportEditView.vue'), props: true },
  { path: '/settings', name: 'Settings', component: () => import('@/views/SettingsView.vue') },
  { path: '/about', name: 'About', component: () => import('@/views/AboutView.vue') },
  // 职业规划中心（新版）
  { path: '/career/profile', name: 'SelfProfile', component: () => import('@/views/SelfProfileView.vue') },
  { path: '/career/explore', name: 'CareerExplore', component: () => import('@/views/CareerExploreView.vue') },
  { path: '/career/explore/:id', name: 'CareerProfileDetail', component: () => import('@/views/CareerProfileDetailViewNew.vue'), props: true },
  { path: '/career/skills', name: 'SkillAssessment', component: () => import('@/views/SkillAssessmentView.vue') },
  { path: '/career/actions', name: 'ActionPlan', component: () => import('@/views/ActionView.vue') },
  // 核心功能页面
  { path: '/explore', name: 'Explore', component: () => import('@/views/ExploreView.vue') },
  { path: '/analysis', name: 'ProfileAnalysis', component: () => import('@/views/ProfileArenaView.vue') },
  { path: '/resume', name: 'ResumeCenter', component: () => import('@/views/ResumeBuilderView.vue') },
  { path: '/resume/manage', name: 'ResumeManage', component: () => import('@/views/ResumeCenterView.vue') },
  { path: '/planning', name: 'PlanningCenter', component: () => import('@/views/PlanningCenterViewNew.vue') },
  // 求职交流系统
  { path: '/job-hub', name: 'JobHub', component: () => import('@/views/JobHubView.vue') },
  { path: '/talent-market', name: 'TalentMarket', component: () => import('@/views/TalentMarketView.vue') },
  { path: '/job-market', name: 'JobMarket', component: () => import('@/views/JobMarketView.vue') },
  { path: '/messages', name: 'MessageCenter', component: () => import('@/views/MessageCenterView.vue') },
  { path: '/post-job', name: 'PostJob', component: () => import('@/views/PostJobView.vue') },
  { path: '/my-profile', name: 'PublishProfile', component: () => import('@/views/PublishProfileView.vue') },
  { path: '/my-applications', name: 'Applications', component: () => import('@/views/ApplicationsView.vue') },
  { path: '/my-jobs', name: 'MyJobs', component: () => import('@/views/ApplicationsView.vue') },
  { path: '/forum', name: 'Forum', component: () => import('@/views/ForumView.vue') },
  { path: '/user-center', name: 'UserCenter', component: () => import('@/views/UserCenterView.vue') },
  { path: '/notifications', name: 'Notifications', component: () => import('@/views/NotificationsView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的位置（如浏览器后退），则恢复
    if (savedPosition) {
      return savedPosition
    }
    // 否则滚动到顶部
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查本地存储中的token
  const token = localStorage.getItem('topo-token')
  const user = localStorage.getItem('topo-user')
  
  // 如果有token，更新登录状态
  if (token && user) {
    authStore.init()
  }
  
  // 检查是否需要身份验证
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }

  // 同步主题
  const theme = localStorage.getItem('topo-theme') || 'light'
  document.documentElement.setAttribute('data-theme', theme)
})

export default router