<template>
  <div class="job-graph-fullscreen">
    <!-- 动态背景 -->
    <div class="graph-background">
      <div class="grid-lines"></div>
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- 顶部导航栏 -->
    <div class="top-bar">
      <div class="top-bar-left">
        <div class="brand">
          <i class="bi bi-diagram-3 brand-icon"></i>
          <div class="brand-text">
            <span class="brand-title">职业发展图谱</span>
            <span class="brand-subtitle">探索职业晋升与转岗路径</span>
          </div>
        </div>
      </div>
      
      <div class="top-bar-center">
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input v-model="searchTerm" type="text" placeholder="搜索职位..." @input="updateChart" @focus="searchFocused = true" @blur="setTimeout(() => searchFocused = false, 200)">
          <span v-if="searchTerm" class="search-clear" @click="searchTerm = ''; updateChart()">
            <i class="bi bi-x"></i>
          </span>
          <!-- 搜索下拉结果 -->
          <div v-if="searchFocused && searchResults.length" class="search-dropdown">
            <div v-for="result in searchResults" :key="result" @mousedown="focusOnJob(result); searchTerm = ''" class="search-result-item">
              <i class="bi bi-briefcase"></i>
              <span>{{ result }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="top-bar-right">
        <div class="stats-row">
          <div class="stat-chip">
            <span class="stat-value">{{ promotions.length + transfers.length }}</span>
            <span class="stat-label">路径</span>
          </div>
          <div class="stat-chip promotion">
            <span class="stat-value">{{ promotions.length }}</span>
            <span class="stat-label">晋升</span>
          </div>
          <div class="stat-chip transfer">
            <span class="stat-value">{{ transfers.length }}</span>
            <span class="stat-label">转岗</span>
          </div>
        </div>
        <button @click="doBuild" :disabled="building" class="build-btn">
          <i :class="building ? 'bi bi-arrow-repeat animate-spin' : 'bi bi-cpu'"></i>
          {{ building ? '构建中' : '智能构建' }}
        </button>
      </div>
    </div>

    <!-- 左侧类别筛选 -->
    <div class="category-sidebar">
      <div class="sidebar-section">
        <div class="section-title"><i class="bi bi-star-fill"></i> 我的关注</div>
        <div v-if="favorites.length" class="favorites-list">
          <div v-for="fav in favorites" :key="fav" @click="focusOnJob(fav)" class="fav-item">
            <span class="fav-name">{{ fav }}</span>
            <i class="bi bi-x-lg fav-remove" @click.stop="toggleFavorite(fav)"></i>
          </div>
        </div>
        <div v-else class="empty-favorites">
          <i class="bi bi-star"></i>
          <span>点击节点添加关注</span>
        </div>
        <button v-if="favorites.length" @click="showOnlyFavorites = !showOnlyFavorites; updateChart()" 
          :class="['filter-toggle', { active: showOnlyFavorites }]">
          <i :class="showOnlyFavorites ? 'bi bi-eye-fill' : 'bi bi-eye'"></i>
          {{ showOnlyFavorites ? '显示全部' : '只看关注' }}
        </button>
      </div>

      <div class="sidebar-section">
        <div class="section-title"><i class="bi bi-funnel"></i> 职位类别</div>
        <button @click="clearCategoryFilter" class="category-chip" :class="{ active: selectedCategories.length === 0 }">
          <span class="chip-dot all"></span>
          <span class="chip-label">全部</span>
          <span class="chip-count">{{ nodeCount }}</span>
        </button>
        <button v-for="cat in categories" :key="cat.name" @click="toggleCategory(cat.name)"
          class="category-chip" :class="{ active: selectedCategories.includes(cat.name) }"
          :style="selectedCategories.includes(cat.name) ? { '--cat-color': cat.color } : {}">
          <span class="chip-dot" :style="{ backgroundColor: cat.color }"></span>
          <span class="chip-label">{{ cat.name }}</span>
          <span class="chip-count">{{ cat.count }}</span>
        </button>
      </div>

      <!-- 热门职位 -->
      <div class="sidebar-section" v-if="hotJobs.length">
        <div class="section-title"><i class="bi bi-fire"></i> 热门职位</div>
        <div class="hot-jobs-list">
          <div v-for="(job, idx) in hotJobs" :key="job.name" @click="focusOnJob(job.name)" class="hot-job-item">
            <span class="hot-rank" :class="'rank-' + (idx + 1)">{{ idx + 1 }}</span>
            <span class="hot-name">{{ job.name }}</span>
            <span class="hot-count">{{ job.count }}条</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图谱区域 -->
    <div ref="chartEl" class="chart-container"></div>

    <!-- 空状态 -->
    <div v-if="!hasData" class="empty-state">
      <div class="empty-icon">
        <i class="bi bi-diagram-3"></i>
      </div>
      <h2>暂无图谱数据</h2>
      <p>点击右上角「智能构建」按钮生成职业发展图谱</p>
      <button @click="doBuild" :disabled="building" class="start-btn">
        <i :class="building ? 'bi bi-arrow-repeat animate-spin' : 'bi bi-magic'"></i>
        {{ building ? '正在构建...' : '开始构建' }}
      </button>
    </div>

    <!-- 右侧详情面板 -->
    <transition name="panel-slide">
      <div v-if="selectedNode" class="detail-panel">
        <div class="panel-close" @click="selectedNode = null"><i class="bi bi-x-lg"></i></div>
        <div class="panel-head">
          <span class="panel-dot" :style="{ backgroundColor: selectedNode.color }"></span>
          <div class="panel-info">
            <span class="panel-name">{{ selectedNode.name }}</span>
            <span class="panel-cat">{{ selectedNode.category }}</span>
          </div>
          <button @click="toggleFavorite(selectedNode.name)" :class="['fav-btn', { active: favorites.includes(selectedNode.name) }]">
            <i :class="favorites.includes(selectedNode.name) ? 'bi bi-star-fill' : 'bi bi-star'"></i>
          </button>
        </div>
        
        <div class="panel-body">
          <!-- 职位概览 -->
          <div class="path-section">
            <div class="path-title"><i class="bi bi-info-circle"></i> 职位概览</div>
            <div class="overview-grid">
              <div class="overview-item">
                <span class="ov-value">{{ selectedNode.canPromoteTo?.length || 0 }}</span>
                <span class="ov-label">晋升方向</span>
              </div>
              <div class="overview-item">
                <span class="ov-value">{{ selectedNode.canTransferTo?.length || 0 }}</span>
                <span class="ov-label">转岗方向</span>
              </div>
              <div class="overview-item">
                <span class="ov-value">{{ selectedNode.fromCount || 0 }}</span>
                <span class="ov-label">来源职位</span>
              </div>
            </div>
          </div>

          <div class="path-section" v-if="selectedNode.canPromoteTo?.length">
            <div class="path-title"><i class="bi bi-graph-up-arrow"></i> 晋升方向</div>
            <div class="path-items">
              <div v-for="to in selectedNode.canPromoteTo" :key="to" @click="focusOnJob(to)" class="path-tag promotion">
                <i class="bi bi-arrow-up-right"></i> {{ to }}
              </div>
            </div>
          </div>

          <div class="path-section" v-if="selectedNode.canTransferTo?.length">
            <div class="path-title"><i class="bi bi-shuffle"></i> 转岗方向</div>
            <div class="path-items">
              <div v-for="to in selectedNode.canTransferTo" :key="to" @click="focusOnJob(to)" class="path-tag transfer">
                <i class="bi bi-arrow-left-right"></i> {{ to }}
              </div>
            </div>
          </div>

          <div class="path-section" v-if="selectedNode.fromJobs?.length">
            <div class="path-title"><i class="bi bi-arrow-bar-right"></i> 可来源于</div>
            <div class="path-items">
              <div v-for="from in selectedNode.fromJobs" :key="from.name" @click="focusOnJob(from.name)" 
                :class="['path-tag', from.type === 'promotion' ? 'promotion' : 'transfer']">
                <i :class="from.type === 'promotion' ? 'bi bi-arrow-up' : 'bi bi-arrows-angle-contract'"></i>
                {{ from.name }}
              </div>
            </div>
          </div>

          <div class="path-section" v-if="!selectedNode.canPromoteTo?.length && !selectedNode.canTransferTo?.length && !selectedNode.fromJobs?.length">
            <div class="no-paths">
              <i class="bi bi-info-circle"></i>
              <span>暂无关联路径</span>
            </div>
          </div>
        </div>

        <div class="panel-foot">
          <button @click="viewJobDetail" class="detail-btn">
            <i class="bi bi-box-arrow-up-right"></i> 查看详情
          </button>
        </div>
      </div>
    </transition>

    <!-- 右侧排行榜 -->
    <div class="right-sidebar" v-if="hasData && !selectedNode">
      <div class="sidebar-section">
        <div class="section-title"><i class="bi bi-graph-up-arrow"></i> 晋升热门</div>
        <div class="rank-list" v-if="topPromotionTargets.length">
          <div v-for="(item, idx) in topPromotionTargets" :key="item.name" @click="focusOnJob(item.name)" class="rank-item promotion">
            <span class="rank-badge" :class="'badge-' + (idx + 1)">{{ idx + 1 }}</span>
            <span class="rank-name">{{ item.name }}</span>
            <span class="rank-count">{{ item.count }}人可达</span>
          </div>
        </div>
        <div v-else class="empty-rank">暂无数据</div>
      </div>

      <div class="sidebar-section">
        <div class="section-title"><i class="bi bi-shuffle"></i> 转岗热门</div>
        <div class="rank-list" v-if="topTransferTargets.length">
          <div v-for="(item, idx) in topTransferTargets" :key="item.name" @click="focusOnJob(item.name)" class="rank-item transfer">
            <span class="rank-badge" :class="'badge-' + (idx + 1)">{{ idx + 1 }}</span>
            <span class="rank-name">{{ item.name }}</span>
            <span class="rank-count">{{ item.count }}人可达</span>
          </div>
        </div>
        <div v-else class="empty-rank">暂无数据</div>
      </div>

      <div class="sidebar-section compact">
        <div class="section-title"><i class="bi bi-bar-chart"></i> 数据概览</div>
        <div class="mini-stats">
          <div class="mini-stat">
            <span class="ms-value">{{ nodeCount }}</span>
            <span class="ms-label">职位</span>
          </div>
          <div class="mini-stat promotion">
            <span class="ms-value">{{ promotions.length }}</span>
            <span class="ms-label">晋升</span>
          </div>
          <div class="mini-stat transfer">
            <span class="ms-value">{{ transfers.length }}</span>
            <span class="ms-label">转岗</span>
          </div>
          <div class="mini-stat fav">
            <span class="ms-value">{{ favorites.length }}</span>
            <span class="ms-label">关注</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部图例 -->
    <div class="bottom-legend">
      <div class="legend-item">
        <span class="legend-line promotion"></span>
        <span>晋升路径</span>
      </div>
      <div class="legend-item">
        <span class="legend-line transfer"></span>
        <span>转岗路径</span>
      </div>
      <div class="legend-divider"></div>
      <div class="legend-item">
        <span class="legend-node fav"></span>
        <span>关注职位</span>
      </div>
      <div class="legend-divider"></div>
      <span class="legend-hint">
        <i class="bi bi-mouse2"></i> 滚轮缩放
        <i class="bi bi-hand-index"></i> 拖拽移动
        <i class="bi bi-cursor"></i> 点击查看
      </span>
    </div>

    <!-- 缩放控制 -->
    <div class="zoom-controls">
      <button @click="zoomIn" class="zoom-btn" title="放大"><i class="bi bi-plus-lg"></i></button>
      <button @click="zoomOut" class="zoom-btn" title="缩小"><i class="bi bi-dash-lg"></i></button>
      <button @click="resetView" class="zoom-btn" title="重置"><i class="bi bi-fullscreen"></i></button>
    </div>

    <!-- 消息提示 -->
    <transition name="toast">
      <div v-if="msg" :class="['toast-msg', msgOk ? 'success' : 'error']">
        <i :class="msgOk ? 'bi bi-check-circle-fill' : 'bi bi-x-circle-fill'"></i>
        {{ msg }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { init, use } from 'echarts/core'
import { GraphChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getGraphData, buildGraph, getJobProfiles } from '@/api'

use([GraphChart, TooltipComponent, LegendComponent, CanvasRenderer])

const router = useRouter()
const setLoading = inject('setLoading')
const toast = inject('toast')
const chartEl = ref(null)
let chart = null
let resizeHandler = null

// 用 ref 包裹以实现响应式
const graphDataCache = ref(null)

const promotions = ref([])
const transfers = ref([])
const building = ref(false)
const msg = ref('')
const msgOk = ref(true)
const searchTerm = ref('')
const selectedCategories = ref([])
const selectedNode = ref(null)
const favorites = ref(JSON.parse(localStorage.getItem('jobFavorites') || '[]'))
const showOnlyFavorites = ref(false)
const searchFocused = ref(false)

const hasData = computed(() => promotions.value.length > 0 || transfers.value.length > 0)
const nodeCount = computed(() => graphDataCache.value?.nodes?.length || 0)

const categoryColors = {
  '初级岗位': '#10b981', '中级岗位': '#3b82f6', '高级岗位': '#8b5cf6', '专家/管理': '#f59e0b'
}

const categories = computed(() => {
  if (!graphDataCache.value?.categories) return []
  const catCounts = {}
  graphDataCache.value.nodes?.forEach(node => {
    const catName = graphDataCache.value.categories[node.category]?.name || '其他'
    catCounts[catName] = (catCounts[catName] || 0) + 1
  })
  return graphDataCache.value.categories.map(cat => ({
    name: cat.name,
    color: categoryColors[cat.name] || '#64748b',
    count: catCounts[cat.name] || 0
  }))
})

// 热门职位（连接数最多）
const hotJobs = computed(() => {
  if (!graphDataCache.value?.nodes || !graphDataCache.value?.links) return []
  const connCount = {}
  graphDataCache.value.links.forEach(l => {
    connCount[l.source] = (connCount[l.source] || 0) + 1
    connCount[l.target] = (connCount[l.target] || 0) + 1
  })
  const idToName = {}
  graphDataCache.value.nodes.forEach(n => { idToName[n.id] = n.name })
  return Object.entries(connCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([id, cnt]) => ({ name: idToName[id] || id, count: cnt }))
})

// 晋升热门目标（被晋升最多的职位）
const topPromotionTargets = computed(() => {
  const count = {}
  promotions.value.forEach(p => {
    count[p.to_position] = (count[p.to_position] || 0) + 1
  })
  return Object.entries(count)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, cnt]) => ({ name, count: cnt, type: 'promotion' }))
})

// 转岗热门目标
const topTransferTargets = computed(() => {
  const count = {}
  transfers.value.forEach(t => {
    count[t.to_position] = (count[t.to_position] || 0) + 1
  })
  return Object.entries(count)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, cnt]) => ({ name, count: cnt, type: 'transfer' }))
})

// 搜索结果
const searchResults = computed(() => {
  if (!searchTerm.value || !graphDataCache.value?.nodes) return []
  const term = searchTerm.value.toLowerCase()
  return graphDataCache.value.nodes
    .filter(n => n.name.toLowerCase().includes(term))
    .slice(0, 8)
    .map(n => n.name)
})

function toggleFavorite(jobName) {
  const idx = favorites.value.indexOf(jobName)
  if (idx >= 0) favorites.value.splice(idx, 1)
  else favorites.value.push(jobName)
  localStorage.setItem('jobFavorites', JSON.stringify(favorites.value))
  updateChart()
}

function focusOnJob(jobName) {
  if (!chart) return
  chart.dispatchAction({ type: 'downplay' })
  chart.dispatchAction({ type: 'highlight', name: jobName })
  if (graphDataCache.value) {
    const node = graphDataCache.value.nodes.find(n => n.name === jobName)
    if (node) {
      const catName = graphDataCache.value.categories[node.category]?.name || '未分类'
      const promTo = promotions.value.filter(pr => pr.from_position === jobName).map(pr => pr.to_position)
      const transTo = transfers.value.filter(tr => tr.from_position === jobName).map(tr => tr.to_position)
      selectedNode.value = { name: jobName, category: catName, color: categoryColors[catName] || '#64748b', canPromoteTo: promTo, canTransferTo: transTo }
    }
  }
}

async function viewJobDetail() {
  if (!selectedNode.value?.name) return
  
  try {
    // 先搜索职位画像获取ID
    const { data } = await getJobProfiles({ search: selectedNode.value.name })
    if (data.profiles?.length > 0) {
      // 找到匹配的职位
      const profile = data.profiles.find(p => p.title === selectedNode.value.name) || data.profiles[0]
      const route = router.resolve({ name: 'JobProfileDetail', params: { id: profile.id } })
      window.open(route.href, '_blank')
    } else {
      // 没找到，跳转到搜索页
      const route = router.resolve({ name: 'JobProfiles', query: { search: selectedNode.value.name } })
      window.open(route.href, '_blank')
    }
  } catch (e) {
    // 出错时跳转到搜索页
    const route = router.resolve({ name: 'JobProfiles', query: { search: selectedNode.value.name } })
    window.open(route.href, '_blank')
  }
}

function toggleCategory(catName) {
  const idx = selectedCategories.value.indexOf(catName)
  if (idx >= 0) selectedCategories.value.splice(idx, 1)
  else selectedCategories.value.push(catName)
  updateChart()
}

function clearCategoryFilter() {
  selectedCategories.value = []
  updateChart()
}

function updateChart() {
  if (!graphDataCache.value || !chart) return
  renderChart(graphDataCache.value)
}

function renderChart(graphData) {
  if (!chart) chart = init(chartEl.value, 'dark')
  if (!graphData.nodes?.length) { chart.clear(); return }
  graphDataCache.value = graphData
  
  const idToName = {}
  graphData.nodes.forEach(n => { idToName[n.id] = n.name })
  
  let filteredNodes = [...graphData.nodes]
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    filteredNodes = filteredNodes.filter(n => n.name.toLowerCase().includes(term))
  }
  if (selectedCategories.value.length > 0) {
    filteredNodes = filteredNodes.filter(n => {
      const catName = graphData.categories[n.category]?.name
      return selectedCategories.value.includes(catName)
    })
  }
  if (showOnlyFavorites.value && favorites.value.length > 0) {
    filteredNodes = filteredNodes.filter(n => favorites.value.includes(n.name))
  }
  
  const nodeIds = new Set(filteredNodes.map(n => n.id))
  const filteredLinks = graphData.links
    .filter(l => nodeIds.has(l.source) && nodeIds.has(l.target))
    .map(l => ({
      source: idToName[l.source] || l.source,
      target: idToName[l.target] || l.target,
      type: l.value
    }))
  
  const connCount = {}
  filteredLinks.forEach(l => {
    connCount[l.source] = (connCount[l.source] || 0) + 1
    connCount[l.target] = (connCount[l.target] || 0) + 1
  })
  
  const styledNodes = filteredNodes.map(node => {
    const catName = graphData.categories[node.category]?.name || '其他'
    const color = categoryColors[catName] || '#64748b'
    const conns = connCount[node.name] || 0
    const isFav = favorites.value.includes(node.name)
    const size = isFav ? Math.min(55, 28 + conns * 5) : Math.min(45, 20 + conns * 5)
    
    return {
      name: node.name,
      category: node.category,
      symbolSize: size,
      symbol: isFav ? 'star' : 'circle',
      itemStyle: { 
        color: isFav ? '#fbbf24' : color, 
        borderColor: isFav ? '#f59e0b' : 'rgba(255,255,255,0.2)', 
        borderWidth: isFav ? 3 : 1, 
        shadowColor: isFav ? '#fbbf24' : color, 
        shadowBlur: isFav ? 25 : 15 
      },
      label: { show: true, fontSize: 10, color: '#e2e8f0', distance: 5 }
    }
  })
  
  const styledLinks = filteredLinks.map(l => ({
    source: l.source,
    target: l.target,
    lineStyle: { 
      color: l.type === 'promotion' ? '#10b981' : '#06b6d4', 
      width: 2, 
      curveness: 0.2, 
      opacity: 0.7 
    },
    emphasis: { lineStyle: { width: 4, opacity: 1, shadowBlur: 15, shadowColor: l.type === 'promotion' ? '#10b981' : '#06b6d4' } }
  }))
  
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      show: false
    },
    animation: true,
    animationDuration: 800,
    animationEasing: 'cubicOut',
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      zoom: 0.9,
      categories: graphData.categories.map(c => ({ ...c, itemStyle: { color: categoryColors[c.name] || '#64748b' } })),
      data: styledNodes,
      links: styledLinks,
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 8],
      force: { repulsion: 400, gravity: 0.15, edgeLength: [60, 150], friction: 0.5, layoutAnimation: true },
      emphasis: { focus: 'adjacency', scale: 1.15, blurScope: 'global' },
      blur: { itemStyle: { opacity: 0.1 }, lineStyle: { opacity: 0.05 } }
    }]
  }, true)
  
  chart.off('click')
  chart.on('click', 'series.graph', p => {
    if (p.dataType === 'node') {
      const catName = graphData.categories[p.data.category]?.name || '未分类'
      const promTo = promotions.value.filter(pr => pr.from_position === p.name).map(pr => pr.to_position)
      const transTo = transfers.value.filter(tr => tr.from_position === p.name).map(tr => tr.to_position)
      // 找出可以晋升/转岗到此职位的来源
      const fromProms = promotions.value.filter(pr => pr.to_position === p.name).map(pr => ({ name: pr.from_position, type: 'promotion' }))
      const fromTrans = transfers.value.filter(tr => tr.to_position === p.name).map(tr => ({ name: tr.from_position, type: 'transfer' }))
      const fromJobs = [...fromProms, ...fromTrans]
      selectedNode.value = { 
        name: p.name, 
        category: catName, 
        color: categoryColors[catName] || '#64748b', 
        canPromoteTo: promTo, 
        canTransferTo: transTo,
        fromJobs: fromJobs,
        fromCount: fromJobs.length
      }
      chart.dispatchAction({ type: 'highlight', name: p.name })
    }
  })
}

let currentZoom = 0.9
function zoomIn() { if (chart) { currentZoom = Math.min(currentZoom * 1.3, 3); chart.setOption({ series: [{ zoom: currentZoom }] }) } }
function zoomOut() { if (chart) { currentZoom = Math.max(currentZoom / 1.3, 0.3); chart.setOption({ series: [{ zoom: currentZoom }] }) } }
function resetView() { if (chart) { currentZoom = 0.9; chart.dispatchAction({ type: 'restore' }) } }

async function load() {
  const { data } = await getGraphData()
  promotions.value = data.paths?.promotion_paths || []
  transfers.value = data.paths?.transfer_paths || []
  renderChart(data)
}

async function doBuild() {
  building.value = true
  setLoading(true, 'AI正在构建职业发展图谱…')
  msg.value = ''
  try {
    const { data } = await buildGraph()
    msg.value = data.message
    msgOk.value = data.success
    await load()
    setTimeout(() => { msg.value = '' }, 3000)
  } catch (e) {
    msg.value = e.response?.data?.message || '构建失败'
    msgOk.value = false
    setTimeout(() => { msg.value = '' }, 3000)
  } finally {
    building.value = false
    setLoading(false)
  }
}

onMounted(() => {
  load()
  resizeHandler = () => chart?.resize()
  window.addEventListener('resize', resizeHandler)
})
onUnmounted(() => {
  chart?.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})
</script>

<style scoped>
.job-graph-fullscreen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: var(--job-graph-bg, linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%));
}

/* 动态背景 */
.graph-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-lines {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.3), transparent);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.25), transparent);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.2), transparent);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(-30px, -20px) scale(1.02); }
}

/* 顶部导航栏 */
.top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--graph-topbar-bg, linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.7) 100%));
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--brand-border, rgba(148, 163, 184, 0.1));
  z-index: 100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  font-size: 28px;
  color: var(--brand-primary, #8b5cf6);
  filter: drop-shadow(0 0 8px rgba(var(--brand-primary-rgb, 139, 92, 246), 0.5));
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--brand-text, #e2e8f0) 0%, var(--brand-primary, #8b5cf6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-subtitle {
  font-size: 11px;
  color: var(--brand-muted, #64748b);
}

.search-box {
  position: relative;
  width: 320px;
}

.search-box i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--brand-muted, #64748b);
  font-size: 14px;
}

.search-box input {
  width: 100%;
  padding: 10px 40px 10px 40px;
  border-radius: 12px;
  border: 1px solid var(--brand-border, rgba(148, 163, 184, 0.2));
  background: var(--graph-search-bg, rgba(15, 23, 42, 0.6));
  color: var(--brand-text, #e2e8f0);
  font-size: 14px;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: var(--brand-primary, rgba(139, 92, 246, 0.5));
  background: var(--graph-search-focus-bg, rgba(15, 23, 42, 0.8));
  box-shadow: 0 0 20px rgba(var(--brand-primary-rgb, 139, 92, 246), 0.15);
}

.search-clear {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--brand-muted, #64748b);
  cursor: pointer;
  padding: 4px;
}

/* 搜索下拉结果 */
.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: var(--graph-dropdown-bg, rgba(15, 23, 42, 0.95));
  backdrop-filter: blur(12px);
  border: 1px solid var(--brand-border, rgba(148, 163, 184, 0.2));
  border-radius: 12px;
  overflow: hidden;
  z-index: 200;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s;
  color: #e2e8f0;
  font-size: 13px;
}

.search-result-item:hover {
  background: rgba(139, 92, 246, 0.2);
}

.search-result-item i {
  position: static;
  transform: none;
  color: #8b5cf6;
  font-size: 14px;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stats-row {
  display: flex;
  gap: 8px;
}

.stat-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 14px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.stat-chip.promotion { border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.1); }
.stat-chip.transfer { border-color: rgba(6, 182, 212, 0.3); background: rgba(6, 182, 212, 0.1); }

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #e2e8f0;
}

.stat-chip.promotion .stat-value { color: #10b981; }
.stat-chip.transfer .stat-value { color: #06b6d4; }

.stat-label {
  font-size: 10px;
  color: #64748b;
}

.build-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.build-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
}

.build-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 左侧边栏 */
.category-sidebar {
  position: absolute;
  top: 90px;
  left: 20px;
  width: 200px;
  max-height: calc(100vh - 180px);
  overflow-y: auto;
  z-index: 90;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-section {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 16px;
  padding: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 12px;
}

.section-title i {
  color: #8b5cf6;
}

.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 120px;
  overflow-y: auto;
}

.fav-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.2);
  cursor: pointer;
  transition: all 0.2s;
}

.fav-item:hover {
  background: rgba(251, 191, 36, 0.2);
}

.fav-name {
  font-size: 12px;
  color: #fbbf24;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fav-remove {
  font-size: 10px;
  color: #fbbf24;
  opacity: 0.6;
}

.fav-remove:hover {
  opacity: 1;
}

.empty-favorites {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px;
  color: #64748b;
  font-size: 11px;
}

.empty-favorites i {
  font-size: 20px;
  opacity: 0.5;
}

.filter-toggle {
  width: 100%;
  margin-top: 10px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: transparent;
  color: #94a3b8;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-toggle.active {
  background: rgba(251, 191, 36, 0.15);
  border-color: rgba(251, 191, 36, 0.3);
  color: #fbbf24;
}

.category-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 10px;
  margin-bottom: 6px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.15);
  background: rgba(30, 41, 59, 0.5);
  color: #94a3b8;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-chip:hover {
  background: rgba(148, 163, 184, 0.1);
}

.category-chip.active {
  background: rgba(var(--cat-color-rgb, 139, 92, 246), 0.15);
  border-color: var(--cat-color, #8b5cf6);
  color: var(--cat-color, #8b5cf6);
}

.chip-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.chip-dot.all {
  background: linear-gradient(135deg, #10b981, #3b82f6, #8b5cf6, #f59e0b);
}

.chip-label {
  flex: 1;
  text-align: left;
}

.chip-count {
  font-size: 10px;
  opacity: 0.7;
}

/* 图谱容器 */
.chart-container {
  position: absolute;
  inset: 70px 0 0 0;
  z-index: 10;
}

/* 空状态 */
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 50;
  background: rgba(15, 23, 42, 0.95);
}

.empty-icon {
  width: 100px;
  height: 100px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.1));
  border: 1px solid rgba(139, 92, 246, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon i {
  font-size: 48px;
  color: #8b5cf6;
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

.start-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.start-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 12px 35px rgba(139, 92, 246, 0.4);
}

/* 右侧详情面板 */
.detail-panel {
  position: absolute;
  top: 90px;
  right: 20px;
  width: 280px;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 20px;
  overflow: hidden;
  z-index: 90;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.panel-close {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgba(148, 163, 184, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 10;
}

.panel-close:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.panel-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.1) 0%, transparent 100%);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.panel-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 12px currentColor;
}

.panel-info {
  flex: 1;
  min-width: 0;
}

.panel-name {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.panel-cat {
  font-size: 11px;
  color: #64748b;
}

.fav-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: transparent;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.fav-btn.active {
  background: rgba(251, 191, 36, 0.2);
  border-color: rgba(251, 191, 36, 0.4);
  color: #fbbf24;
}

.panel-body {
  padding: 16px 20px;
  max-height: 300px;
  overflow-y: auto;
}

.path-section {
  margin-bottom: 16px;
}

.path-section:last-child {
  margin-bottom: 0;
}

.path-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 10px;
}

.path-title i {
  font-size: 14px;
}

.path-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.path-tag {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.path-tag.promotion {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.path-tag.promotion:hover {
  background: rgba(16, 185, 129, 0.25);
}

.path-tag.transfer {
  background: rgba(6, 182, 212, 0.15);
  border: 1px solid rgba(6, 182, 212, 0.3);
  color: #06b6d4;
}

.path-tag.transfer:hover {
  background: rgba(6, 182, 212, 0.25);
}

.no-paths {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.05);
  color: #64748b;
  font-size: 12px;
}

.panel-foot {
  padding: 16px 20px;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.detail-btn {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.35);
}

/* 底部图例 */
.bottom-legend {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 12px 24px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 14px;
  z-index: 90;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.legend-line {
  width: 24px;
  height: 3px;
  border-radius: 2px;
}

.legend-line.promotion {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.legend-line.transfer {
  background: linear-gradient(90deg, #06b6d4, #22d3ee);
}

.legend-divider {
  width: 1px;
  height: 20px;
  background: rgba(148, 163, 184, 0.2);
}

.legend-hint {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 11px;
  color: #64748b;
}

.legend-hint i {
  margin-right: 4px;
  color: #8b5cf6;
}

/* 缩放控制 */
.zoom-controls {
  position: absolute;
  bottom: 80px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 90;
}

.zoom-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  color: #94a3b8;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.zoom-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.4);
  color: #8b5cf6;
}

/* Toast消息 */
.toast-msg {
  position: absolute;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 14px;
  z-index: 200;
  animation: slideDown 0.3s ease;
}

.toast-msg.success {
  background: rgba(16, 185, 129, 0.9);
  color: white;
}

.toast-msg.error {
  background: rgba(239, 68, 68, 0.9);
  color: white;
}

@keyframes slideDown {
  from { transform: translateX(-50%) translateY(-20px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}

/* 动画 */
.panel-slide-enter-active,
.panel-slide-leave-active {
  transition: all 0.3s ease;
}

.panel-slide-enter-from,
.panel-slide-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

/* 热门职位 */
.hot-jobs-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hot-job-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  cursor: pointer;
  transition: all 0.2s;
}

.hot-job-item:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}

.hot-rank {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}

.hot-rank.rank-1 {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1e1b4b;
}

.hot-rank.rank-2 {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #1e1b4b;
}

.hot-rank.rank-3 {
  background: linear-gradient(135deg, #cd7f32, #b8860b);
  color: #1e1b4b;
}

.hot-name {
  flex: 1;
  font-size: 11px;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot-count {
  font-size: 10px;
  color: #64748b;
  white-space: nowrap;
}

/* 右下角统计面板 */
.stats-panel {
  position: absolute;
  bottom: 80px;
  left: 20px;
  width: 200px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 16px;
  padding: 16px;
  z-index: 90;
}

.stats-title {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.sg-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  border-radius: 10px;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.sg-item i {
  font-size: 16px;
  color: #8b5cf6;
}

.sg-item.promotion {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.2);
}

.sg-item.promotion i {
  color: #10b981;
}

.sg-item.transfer {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
}

.sg-item.transfer i {
  color: #06b6d4;
}

.sg-item.fav {
  background: rgba(251, 191, 36, 0.1);
  border-color: rgba(251, 191, 36, 0.2);
}

.sg-item.fav i {
  color: #fbbf24;
}

.sg-info {
  display: flex;
  flex-direction: column;
}

.sg-value {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
}

.sg-label {
  font-size: 9px;
  color: #64748b;
}

/* 职位概览网格 */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.overview-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 6px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.08);
}

.ov-value {
  font-size: 20px;
  font-weight: 700;
  color: #8b5cf6;
}

.ov-label {
  font-size: 10px;
  color: #64748b;
  margin-top: 2px;
}

/* 图例节点 */
.legend-node {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.legend-node.fav {
  background: #fbbf24;
  box-shadow: 0 0 8px rgba(251, 191, 36, 0.5);
}

/* 右侧排行榜 */
.right-sidebar {
  position: absolute;
  top: 90px;
  right: 20px;
  width: 220px;
  max-height: calc(100vh - 180px);
  overflow-y: auto;
  z-index: 90;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rank-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.1);
  cursor: pointer;
  transition: all 0.25s ease;
}

.rank-item:hover {
  transform: translateX(-4px);
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.2);
}

.rank-item.promotion:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.3);
}

.rank-item.transfer:hover {
  background: rgba(6, 182, 212, 0.15);
  border-color: rgba(6, 182, 212, 0.3);
}

.rank-badge {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  flex-shrink: 0;
}

.rank-badge.badge-1 {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #1e1b4b;
}

.rank-badge.badge-2 {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #1e1b4b;
}

.rank-badge.badge-3 {
  background: linear-gradient(135deg, #cd7f32, #b8860b);
  color: #1e1b4b;
}

.rank-name {
  flex: 1;
  font-size: 12px;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rank-count {
  font-size: 10px;
  color: #64748b;
  white-space: nowrap;
}

.empty-rank {
  padding: 16px;
  text-align: center;
  color: #64748b;
  font-size: 12px;
}

.sidebar-section.compact {
  padding: 12px;
}

.mini-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.mini-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 4px;
  border-radius: 8px;
  background: rgba(139, 92, 246, 0.1);
}

.mini-stat.promotion {
  background: rgba(16, 185, 129, 0.1);
}

.mini-stat.transfer {
  background: rgba(6, 182, 212, 0.1);
}

.mini-stat.fav {
  background: rgba(251, 191, 36, 0.1);
}

.ms-value {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
}

.mini-stat.promotion .ms-value { color: #10b981; }
.mini-stat.transfer .ms-value { color: #06b6d4; }
.mini-stat.fav .ms-value { color: #fbbf24; }

.ms-label {
  font-size: 9px;
  color: #64748b;
  margin-top: 2px;
}
</style>
