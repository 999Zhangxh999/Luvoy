import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 600000, // LLM批量调用最长10分钟
})

// ---- 统计 ----
export const getStats = () => api.get('/stats')

// ---- 岗位 ----
export const getJobs = (params) => api.get('/jobs', { params })
export const getJobDetail = (id) => api.get(`/jobs/${id}`)
export const getJobProfiles = (params) => api.get('/jobs/profiles', { params })
export const getJobProfileDetail = (id) => api.get(`/jobs/profiles/${id}`)
export const analyzeJobs = (count = 10) => api.post('/jobs/analyze', { count })
export const analyzeSingleJob = (id) => api.post(`/jobs/analyze-one/${id}`)

// ---- 图谱 ----
export const getGraphData = () => api.get('/graph/data')
export const buildGraph = () => api.post('/graph/build')
export const getGraphStatistics = () => api.get('/graph/statistics')
export const getCareerPaths = (position) =>
  api.get(`/graph/recommend/${encodeURIComponent(position)}`)

// ---- 学生 ----
export const getStudents = () => api.get('/students')
export const getStudentDetail = (id) => api.get(`/students/${id}`)
export const getStudent = getStudentDetail
export const createStudent = (formData) =>
  api.post('/students', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
export const deleteStudent = (id) => api.delete(`/students/${id}`)
export const generateStudentProfile = (id) =>
  api.post(`/students/${id}/generate-profile`)

// ---- 匹配 ----
export const getMatchResults = (sid) => api.get(`/matching/${sid}`)
export const getMatchingResults = getMatchResults
export const runMatching = (sid, topN = 5) =>
  api.post(`/matching/${sid}/run`, { top_n: topN })
export const matchSingle = (sid, pid) =>
  api.post(`/matching/${sid}/single/${pid}`)
export const runSingleMatching = matchSingle
export const getSkillAnalysis = (sid, pid) =>
  api.get(`/matching/${sid}/skill-analysis`, {
    params: { job_profile_id: pid },
  })

// ---- 报告 ----
export const getReport = (sid) => api.get(`/reports/${sid}`)
export const generateReport = (sid) => api.post(`/reports/${sid}/generate`)
export const generateAdvancedReport = (sid, useMultiAgent = true) =>
  api.post(`/reports/${sid}/generate-advanced`, { use_multi_agent: useMultiAgent })
export const polishReport = (rid) => api.post(`/reports/${rid}/polish`)
export const updateReportSection = (rid, section, content) =>
  api.post(`/reports/${rid}/update-section`, { section, content })
export const exportReport = (rid, fmt) => `/api/reports/${rid}/export/${fmt}`

// ---- 设置 ----
export const getSettings = () => api.get('/settings')
export const updateSettings = (data) => api.post('/settings', data)

// ---- AI对话 ----
export const chatWithAI = (message, context = {}, history = []) =>
  api.post('/chat', { message, context, history })
export const getAlgorithmInfo = () => api.get('/algorithms/info')
export const getGraphPositionImportance = () => api.get('/graph/position-importance')
export const getGraphJobClusters = () => api.get('/graph/job-clusters')
export const getGraphReachable = (position, maxHops = 2) =>
  api.get(`/graph/reachable/${encodeURIComponent(position)}`, {
    params: { max_hops: maxHops },
  })
export const getCareerMdpStrategy = (position) =>
  api.get('/career/mdp-strategy', { params: { position } })
export const getCareerTrajectory = (position, horizon = 5) =>
  api.get('/career/trajectory', {
    params: { position, horizon },
  })
export const getSimilarPositions = (position, topK = 5) =>
  api.get('/positions/similar', {
    params: { position, top_k: topK },
  })
export const getPositionClusters = (nClusters = 5) =>
  api.get('/positions/clusters', {
    params: { n_clusters: nClusters },
  })

export default api
