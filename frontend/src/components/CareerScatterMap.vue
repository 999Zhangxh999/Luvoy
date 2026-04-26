<template>
  <div 
    class="career-scatter-map" 
    ref="containerRef" 
    @wheel.prevent="handleWheel"
    @mousedown="startDrag"
    @mousemove="onDrag"
    @mouseup="endDrag"
    @mouseleave="endDrag"
    @touchstart.passive="startTouchDrag"
    @touchmove.passive="onTouchDrag"
    @touchend="endDrag"
    :class="{ 'is-dragging': isDragging, 'is-fullscreen': fullscreen }"
  >
    <!-- 动态背景 -->
    <div class="map-background">
      <div class="grid-lines"></div>
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- 顶部导航栏 -->
    <div class="top-bar">
      <div class="top-bar-left">
        <div class="brand">
          <i class="bi bi-stars brand-icon"></i>
          <div class="brand-text">
            <span class="brand-title">职业宇宙</span>
            <span class="brand-subtitle">探索无限可能</span>
          </div>
        </div>
      </div>
      
      <div class="top-bar-center">
        <!-- 搜索框 -->
        <div class="search-box">
          <i class="bi bi-search"></i>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索职业..."
            @focus="showSearchResults = true"
            @blur="hideSearchResults"
          >
          <span v-if="searchQuery" class="search-clear" @mousedown.prevent="searchQuery = ''">
            <i class="bi bi-x"></i>
          </span>
        </div>
        <!-- 搜索结果下拉 -->
        <div v-if="showSearchResults && searchResults.length" class="search-dropdown">
          <div 
            v-for="career in searchResults" 
            :key="career.id"
            class="search-item"
            @mousedown.prevent="focusOnCareer(career)"
          >
            <span class="search-dot" :style="{ backgroundColor: career.color }"></span>
            <span class="search-name">{{ career.name }}</span>
            <span class="search-cat">{{ career.category }}</span>
          </div>
        </div>
      </div>

      <div class="top-bar-right">
        <!-- 统计信息 -->
        <div class="stats-row">
          <div class="stat-chip">
            <span class="stat-value">{{ displayedCareers.length }}</span>
            <span class="stat-label">职位</span>
          </div>
          <div class="stat-chip">
            <span class="stat-value">{{ displayedLinks.length }}</span>
            <span class="stat-label">路径</span>
          </div>
        </div>
        <!-- 缩放控制 -->
        <div class="zoom-controls">
          <button @click="zoomOut" class="zoom-btn" title="缩小">
            <i class="bi bi-dash"></i>
          </button>
          <span class="zoom-value">{{ Math.round(scale * 100) }}%</span>
          <button @click="zoomIn" class="zoom-btn" title="放大">
            <i class="bi bi-plus"></i>
          </button>
        </div>
        <button @click="resetView" class="icon-btn" title="重置视图">
          <i class="bi bi-fullscreen"></i>
        </button>
      </div>
    </div>

    <!-- 左侧类别筛选 -->
    <div class="category-sidebar">
      <button
        @click="clearCategoryFilter"
        class="category-chip"
        :class="{ active: activeCategories.size === 0 }"
      >
        <span class="chip-dot all"></span>
        <span class="chip-label">全部</span>
        <span class="chip-count">{{ allCareers.length }}</span>
      </button>
      <button
        v-for="cat in categoryList"
        :key="cat.name"
        @click="toggleCategory(cat.name)"
        class="category-chip"
        :class="{ active: activeCategories.has(cat.name) }"
        :style="activeCategories.has(cat.name) ? { '--cat-color': cat.color } : {}"
      >
        <span class="chip-dot" :style="{ backgroundColor: cat.color }"></span>
        <span class="chip-label">{{ cat.name }}</span>
        <span class="chip-count">{{ cat.count }}</span>
      </button>
    </div>

    <!-- 可缩放并可拖拽的容器 -->
    <div 
      class="scalable-content" 
      :style="{ 
        transform: `translate(${panX}px, ${panY}px) scale(${scale})`,
        cursor: isDragging ? 'grabbing' : 'grab'
      }"
    >
      <!-- 类别扇形区域 -->
      <svg class="category-sectors" v-if="showSectors">
        <defs>
          <radialGradient v-for="cat in categoryList" :key="'grad-'+cat.name" :id="'sector-grad-'+cat.name.replace(/\s/g, '')">
            <stop offset="0%" :style="`stop-color:${cat.color};stop-opacity:0.12`" />
            <stop offset="100%" :style="`stop-color:${cat.color};stop-opacity:0`" />
          </radialGradient>
        </defs>
        <path
          v-for="sector in categorySectors"
          :key="sector.name"
          :d="sector.path"
          :fill="`url(#sector-grad-${sector.name.replace(/\\s/g, '')})`"
          class="category-sector"
        />
      </svg>

      <!-- 中心探索圆 -->
      <div class="center-circle" :style="centerStyle">
        <div class="center-glow"></div>
        <div class="center-content">
          <i class="bi bi-compass center-icon"></i>
        </div>
      </div>

      <!-- SVG 连接线 -->
      <svg class="connections-svg" ref="svgRef">
        <defs>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#7c3aed;stop-opacity:0.5" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:0.5" />
          </linearGradient>
          <linearGradient id="promotionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#10b981;stop-opacity:0.4" />
            <stop offset="100%" style="stop-color:#34d399;stop-opacity:0.8" />
          </linearGradient>
          <linearGradient id="transferGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:0.4" />
            <stop offset="100%" style="stop-color:#22d3ee;stop-opacity:0.8" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#10b981" opacity="0.7"/>
          </marker>
        </defs>
        <g class="connections-layer">
          <path 
            v-for="(link, i) in visibleLinks" 
            :key="i"
            :d="link.path"
            class="connection-line"
            :class="{ 
              'highlighted': link.highlighted,
              'is-promotion': link.type === 'promotion',
              'is-transfer': link.type === 'transfer'
            }"
            :style="{ 
              stroke: link.type === 'promotion' ? 'url(#promotionGradient)' : 
                      link.type === 'transfer' ? 'url(#transferGradient)' : 
                      'url(#lineGradient)',
              strokeDasharray: link.dashed ? '8,4' : 'none'
            }"
            :marker-end="link.type === 'promotion' ? 'url(#arrowhead)' : ''"
          />
        </g>
      </svg>

      <!-- 职业节点 -->
      <div 
        v-for="(career, index) in visibleCareers" 
        :key="career.id"
        class="career-node"
        :class="{ 
          'is-hovered': hoveredId === career.id,
          'is-related': relatedIds.has(career.id),
          'is-dimmed': hoveredId && hoveredId !== career.id && !relatedIds.has(career.id),
          'is-hot': career.isHot,
          'is-searched': searchedCareer?.id === career.id,
          'is-highlighted': highlightedIds.has(career.id)
        }"
        :style="{ ...getNodeStyle(career), '--color': career.color, '--delay': `${(index % 10) * 0.3}s` }"
        @mouseenter="handleNodeHover(career)"
        @mouseleave="handleNodeLeave"
        @click.stop="handleNodeClick(career)"
        @touchstart.passive="handleNodeHover(career)"
        @touchend.prevent="handleNodeClick(career)"
      >
        <span v-if="career.isHot" class="hot-badge"><i class="bi bi-fire"></i></span>
        <div class="node-body">
          <span class="career-dot"></span>
          <span class="career-name">{{ career.name }}</span>
        </div>
      </div>
    </div>

    <!-- 右侧信息面板 -->
    <transition name="panel-slide">
      <div v-if="tooltip.visible" class="detail-panel">
        <div class="panel-head">
          <span class="panel-dot" :style="{ backgroundColor: tooltip.color }"></span>
          <div class="panel-info">
            <span class="panel-name">{{ tooltip.name }}</span>
            <span class="panel-cat">{{ tooltip.category }}</span>
          </div>
          <span v-if="tooltip.isHot" class="panel-hot"><i class="bi bi-fire"></i></span>
        </div>
        
        <div class="panel-body">
          <div class="panel-stat-row">
            <div class="mini-stat">
              <i class="bi bi-currency-yen"></i>
              <span>{{ tooltip.salary }}</span>
            </div>
          </div>

          <div class="path-section" v-if="hoveredPaths.promotions.length">
            <div class="path-title"><i class="bi bi-graph-up-arrow"></i> 晋升方向</div>
            <div class="path-items">
              <div v-for="(p, i) in hoveredPaths.promotions" :key="'p'+i" class="path-tag promotion">
                <span class="tag-dot" :style="{ backgroundColor: p.color }"></span>
                {{ p.name }}
              </div>
            </div>
          </div>

          <div class="path-section" v-if="hoveredPaths.transfers.length">
            <div class="path-title"><i class="bi bi-shuffle"></i> 转岗方向</div>
            <div class="path-items">
              <div v-for="(p, i) in hoveredPaths.transfers" :key="'t'+i" class="path-tag transfer">
                <span class="tag-dot" :style="{ backgroundColor: p.color }"></span>
                {{ p.name }}
              </div>
            </div>
          </div>

          <div class="skills-section" v-if="tooltip.skills?.length">
            <div class="path-title"><i class="bi bi-stars"></i> 核心技能</div>
            <div class="skill-tags">
              <span v-for="skill in tooltip.skills.slice(0, 4)" :key="skill" class="skill-tag">{{ skill }}</span>
            </div>
          </div>
        </div>

        <div class="panel-foot">
          <i class="bi bi-hand-index"></i> 点击查看详情
        </div>
      </div>
    </transition>

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
      <span class="legend-hint">滚轮缩放 · 拖拽移动 · 点击查看</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  careers: { type: Array, default: () => [] },
  links: { type: Array, default: () => [] },
  categories: { type: Array, default: () => [] },
  fullscreen: { type: Boolean, default: false },
  width: { type: Number, default: 1200 },
  height: { type: Number, default: 800 },
})

const emit = defineEmits(['select', 'showPaths', 'hover'])

const containerRef = ref(null)
const svgRef = ref(null)
const containerWidth = ref(1200)
const containerHeight = ref(800)
const hoveredId = ref(null)
const relatedIds = ref(new Set())

// 搜索相关
const searchQuery = ref('')
const showSearchResults = ref(false)
const searchedCareer = ref(null)

// 类别筛选
const activeCategories = ref(new Set())

// 缩放相关
const scale = ref(1)
const minScale = 0.3
const maxScale = 3

// 平移相关
const panX = ref(0)
const panY = ref(0)
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const panStart = ref({ x: 0, y: 0 })

// 显示控制
const showSectors = ref(true)

// 所有职业（原始数据）
const allCareers = computed(() => props.careers)

// 类别列表
const categoryList = computed(() => {
  if (props.categories.length) return props.categories
  const catMap = new Map()
  props.careers.forEach(career => {
    if (!catMap.has(career.category)) {
      catMap.set(career.category, { name: career.category, color: career.color, count: 0 })
    }
    catMap.get(career.category).count++
  })
  return Array.from(catMap.values())
})

// 筛选后的职业
const displayedCareers = computed(() => {
  let result = props.careers
  if (activeCategories.value.size > 0) {
    result = result.filter(c => activeCategories.value.has(c.category))
  }
  return result
})

// 筛选后的连接
const displayedLinks = computed(() => {
  const ids = new Set(displayedCareers.value.map(c => c.id))
  return props.links.filter(l => ids.has(l.source) && ids.has(l.target))
})

// 搜索结果
const searchResults = computed(() => {
  if (!searchQuery.value.trim()) return []
  const q = searchQuery.value.toLowerCase()
  return props.careers.filter(c => c.name.toLowerCase().includes(q)).slice(0, 8)
})

function hideSearchResults() {
  setTimeout(() => { showSearchResults.value = false }, 150)
}

function focusOnCareer(career) {
  searchedCareer.value = career
  searchQuery.value = ''
  showSearchResults.value = false
  
  // 计算该职业在布局中的位置并移动视图
  const target = visibleCareers.value.find(c => c.id === career.id)
  if (target) {
    panX.value = containerWidth.value / 2 - target.x
    panY.value = containerHeight.value / 2 - target.y
    scale.value = 1.5
  }
  
  // 3秒后取消高亮
  setTimeout(() => { searchedCareer.value = null }, 3000)
}

function toggleCategory(name) {
  const newSet = new Set(activeCategories.value)
  if (newSet.has(name)) {
    newSet.delete(name)
  } else {
    newSet.add(name)
  }
  activeCategories.value = newSet
}

function clearCategoryFilter() {
  activeCategories.value = new Set()
}

function zoomIn() {
  scale.value = Math.min(maxScale, scale.value + 0.2)
}

function zoomOut() {
  scale.value = Math.max(minScale, scale.value - 0.2)
}

function resetView() {
  scale.value = 1
  panX.value = 0
  panY.value = 0
}

function handleWheel(e) {
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  scale.value = Math.min(maxScale, Math.max(minScale, scale.value + delta))
}

function startDrag(e) {
  if (e.target.closest('.career-node') || e.target.closest('.top-bar') || 
      e.target.closest('.category-sidebar') || e.target.closest('.detail-panel') ||
      e.target.closest('.bottom-legend')) return
  isDragging.value = true
  dragStart.value = { x: e.clientX, y: e.clientY }
  panStart.value = { x: panX.value, y: panY.value }
}

function onDrag(e) {
  if (!isDragging.value) return
  const dx = e.clientX - dragStart.value.x
  const dy = e.clientY - dragStart.value.y
  panX.value = panStart.value.x + dx
  panY.value = panStart.value.y + dy
}

function endDrag() {
  isDragging.value = false
}

// 触摸拖拽支持
function startTouchDrag(e) {
  if (e.target.closest('.career-node') || e.target.closest('.top-bar') || 
      e.target.closest('.category-sidebar') || e.target.closest('.detail-panel') ||
      e.target.closest('.bottom-legend')) return
  if (e.touches.length !== 1) return // 只处理单指触摸
  isDragging.value = true
  const touch = e.touches[0]
  dragStart.value = { x: touch.clientX, y: touch.clientY }
  panStart.value = { x: panX.value, y: panY.value }
}

function onTouchDrag(e) {
  if (!isDragging.value || e.touches.length !== 1) return
  const touch = e.touches[0]
  const dx = touch.clientX - dragStart.value.x
  const dy = touch.clientY - dragStart.value.y
  panX.value = panStart.value.x + dx
  panY.value = panStart.value.y + dy
}

const tooltip = ref({
  visible: false,
  name: '',
  category: '',
  color: '',
  salary: '',
  isHot: false,
  skills: [],
})

const centerX = computed(() => containerWidth.value / 2)
const centerY = computed(() => containerHeight.value / 2)
const centerRadius = computed(() => Math.min(containerWidth.value, containerHeight.value) * 0.08)

const centerStyle = computed(() => ({
  width: centerRadius.value * 2 + 'px',
  height: centerRadius.value * 2 + 'px',
  left: centerX.value - centerRadius.value + 'px',
  top: centerY.value - centerRadius.value + 'px',
}))

// 类别扇形区域
const categorySectors = computed(() => {
  const cats = categoryList.value
  if (!cats.length) return []
  
  const cx = centerX.value
  const cy = centerY.value
  const innerR = centerRadius.value + 80
  const outerR = Math.min(containerWidth.value, containerHeight.value) * 0.48
  const anglePerCat = (2 * Math.PI) / cats.length
  
  return cats.map((cat, i) => {
    const startAngle = i * anglePerCat - Math.PI / 2
    const endAngle = startAngle + anglePerCat
    
    const x1 = cx + Math.cos(startAngle) * innerR
    const y1 = cy + Math.sin(startAngle) * innerR
    const x2 = cx + Math.cos(startAngle) * outerR
    const y2 = cy + Math.sin(startAngle) * outerR
    const x3 = cx + Math.cos(endAngle) * outerR
    const y3 = cy + Math.sin(endAngle) * outerR
    const x4 = cx + Math.cos(endAngle) * innerR
    const y4 = cy + Math.sin(endAngle) * innerR
    
    const largeArc = anglePerCat > Math.PI ? 1 : 0
    
    const path = `M ${x1} ${y1} L ${x2} ${y2} A ${outerR} ${outerR} 0 ${largeArc} 1 ${x3} ${y3} L ${x4} ${y4} A ${innerR} ${innerR} 0 ${largeArc} 0 ${x1} ${y1} Z`
    
    return { ...cat, path }
  })
})

// 使用种子随机数生成器确保位置稳定
function seededRandom(seed) {
  const x = Math.sin(seed) * 10000
  return x - Math.floor(x)
}

// 简单的碰撞检测和排斥函数
function applyRepulsion(positions, minDistance = 100) {
  const iterations = 50
  const nodeRadius = 60 // 节点估计半径（包含标签）
  
  for (let iter = 0; iter < iterations; iter++) {
    let moved = false
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j++) {
        const dx = positions[j].x - positions[i].x
        const dy = positions[j].y - positions[i].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        
        if (dist < minDistance && dist > 0) {
          const overlap = (minDistance - dist) / 2
          const nx = dx / dist
          const ny = dy / dist
          
          positions[i].x -= nx * overlap * 0.5
          positions[i].y -= ny * overlap * 0.5
          positions[j].x += nx * overlap * 0.5
          positions[j].y += ny * overlap * 0.5
          moved = true
        }
      }
    }
    if (!moved) break
  }
  return positions
}

// 计算职业节点位置 - 力导向布局避免重叠
const visibleCareers = computed(() => {
  const careers = displayedCareers.value
  if (!careers.length) return []

  const cx = centerX.value
  const cy = centerY.value
  // 扩大分布范围
  const minR = centerRadius.value + 150
  const maxR = Math.min(containerWidth.value, containerHeight.value) * 0.58

  // 按类别分组，获取唯一类别
  const catList = [...new Set(careers.map(c => c.category))]
  const categoryAngles = {}
  const anglePerCategory = (2 * Math.PI) / Math.max(catList.length, 1)

  catList.forEach((cat, i) => {
    // 为每个类别分配一个扇形区域
    const baseAngle = i * anglePerCategory - Math.PI / 2
    categoryAngles[cat] = {
      start: baseAngle,
      end: baseAngle + anglePerCategory,
      index: i,
    }
  })

  // 初始位置计算
  const positions = careers.map((career, idx) => {
    const catInfo = categoryAngles[career.category] || { start: 0, end: Math.PI * 2, index: 0 }
    const careersInCat = careers.filter(c => c.category === career.category)
    const indexInCat = careersInCat.findIndex(c => c.id === career.id)
    const countInCat = careersInCat.length

    // 使用稳定的种子随机数
    const seed = career.id.split('').reduce((a, c) => a + c.charCodeAt(0), 0) + idx

    // 在扇形区域内的角度
    const angleSpan = catInfo.end - catInfo.start
    const baseAngle = catInfo.start + angleSpan * 0.08
    const usableAngle = angleSpan * 0.84

    // 螺旋式分布：同类别节点沿螺旋线排列
    const spiralFactor = indexInCat / Math.max(countInCat - 1, 1)
    const angle = baseAngle + usableAngle * spiralFactor + (seededRandom(seed * 7) - 0.5) * 0.2

    // 半径按螺旋递增
    const radiusRange = maxR - minR
    const r = minR + radiusRange * (0.3 + spiralFactor * 0.7) + (seededRandom(seed * 13) - 0.5) * 40

    return {
      ...career,
      x: cx + Math.cos(angle) * r,
      y: cy + Math.sin(angle) * r,
    }
  })

  // 应用排斥力避免重叠
  return applyRepulsion(positions, 110)
})

// 计算连接线路径
const visibleLinks = computed(() => {
  if (!displayedLinks.value.length || !visibleCareers.value.length) return []

  const careerMap = new Map()
  visibleCareers.value.forEach(c => careerMap.set(c.id, c))

  return displayedLinks.value.map(link => {
    const source = careerMap.get(link.source)
    const target = careerMap.get(link.target)

    if (!source || !target) return null

    // 创建贝塞尔曲线路径
    const midX = (source.x + target.x) / 2
    const midY = (source.y + target.y) / 2
    const dx = target.x - source.x
    const dy = target.y - source.y
    const len = Math.sqrt(dx * dx + dy * dy)
    
    // 控制点偏移
    const offset = len * 0.15
    const controlX = midX + (dy / len) * offset * (Math.random() > 0.5 ? 1 : -1)
    const controlY = midY - (dx / len) * offset * (Math.random() > 0.5 ? 1 : -1)

    const path = `M ${source.x} ${source.y} Q ${controlX} ${controlY} ${target.x} ${target.y}`

    const highlighted = hoveredId.value && 
      (link.source === hoveredId.value || link.target === hoveredId.value)

    return {
      ...link,
      path,
      highlighted,
      color: link.type === 'promotion' ? '#10b981' : link.type === 'transfer' ? '#06b6d4' : null,
      dashed: link.type === 'transfer',
    }
  }).filter(Boolean)
})

function getNodeStyle(career) {
  return {
    left: career.x + 'px',
    top: career.y + 'px',
  }
}

// 悬停时的路径信息
const hoveredPaths = computed(() => {
  if (!hoveredId.value) return { promotions: [], transfers: [] }
  
  const careerMap = new Map()
  visibleCareers.value.forEach(c => careerMap.set(c.id, c))
  
  const promotions = []
  const transfers = []
  
  displayedLinks.value.forEach(link => {
    if (link.source === hoveredId.value || link.target === hoveredId.value) {
      const isSource = link.source === hoveredId.value
      const otherId = isSource ? link.target : link.source
      const otherCareer = careerMap.get(otherId)
      
      if (otherCareer) {
        const pathInfo = {
          name: otherCareer.name,
          direction: isSource ? '→' : '←',
          color: otherCareer.color,
        }
        
        if (link.type === 'promotion') {
          promotions.push(pathInfo)
        } else {
          transfers.push(pathInfo)
        }
      }
    }
  })
  
  return { promotions, transfers }
})

function handleNodeHover(career) {
  hoveredId.value = career.id
  emit('hover', career)
  
  // 找出所有相关的职业ID
  const related = new Set()
  props.links.forEach(link => {
    if (link.source === career.id) related.add(link.target)
    if (link.target === career.id) related.add(link.source)
  })
  relatedIds.value = related

  // 更新信息面板
  tooltip.value = {
    visible: true,
    name: career.name,
    category: career.category,
    color: career.color,
    salary: career.salary || '15-30K',
    promotions: career.promotions || 2,
    transfers: career.transfers || 3,
    isHot: career.isHot || false,
    skills: career.skills || ['沟通能力', '团队协作', '问题解决'],
  }
}

function handleNodeLeave() {
  hoveredId.value = null
  relatedIds.value = new Set()
  tooltip.value.visible = false
  emit('hover', null)
}

function handleNodeClick(career) {
  emit('select', career)
}

// 响应式调整
function updateSize() {
  if (containerRef.value) {
    const rect = containerRef.value.getBoundingClientRect()
    containerWidth.value = rect.width || props.width
    containerHeight.value = rect.height || props.height
  }
}

let resizeObserver = null
onMounted(() => {
  updateSize()
  resizeObserver = new ResizeObserver(updateSize)
  if (containerRef.value) resizeObserver.observe(containerRef.value)
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})

// 高亮的职业ID集合
const highlightedIds = ref(new Set())

// 供外部调用的方法
function searchCareer(keyword) {
  searchQuery.value = keyword
  showSearchResults.value = true
}

function focusOnCareerById(careerId) {
  const career = displayedCareers.value.find(c => c.id === careerId)
  if (career) {
    focusOnCareer(career)
  }
}

function highlightCareers(careerIds) {
  highlightedIds.value = new Set(careerIds || [])
  // 3秒后自动取消高亮
  if (careerIds?.length) {
    setTimeout(() => {
      highlightedIds.value = new Set()
    }, 5000)
  }
}

// 暴露给父组件
defineExpose({
  searchCareer,
  focusOnCareerById,
  focusOnCareer,
  highlightCareers
})
</script>

<style scoped>
/* 基础容器 */
.career-scatter-map {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 100vh;
  overflow: hidden;
  background: #0a0f1a;
}

.career-scatter-map.is-fullscreen {
  position: fixed;
  inset: 0;
}

.career-scatter-map.is-dragging {
  cursor: grabbing !important;
}

:global(html.light) .career-scatter-map {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

/* 动态背景 */
.map-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.grid-lines {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(124, 58, 237, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124, 58, 237, 0.03) 1px, transparent 1px);
  background-size: 80px 80px;
  animation: grid-move 40s linear infinite;
}

:global(html.light) .grid-lines {
  background-image: 
    linear-gradient(rgba(6, 182, 212, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.06) 1px, transparent 1px);
}

@keyframes grid-move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(80px, 80px); }
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  animation: orb-float 25s ease-in-out infinite;
  pointer-events: none;
}

.orb-1 {
  width: 600px;
  height: 600px;
  top: -150px;
  left: -150px;
  background: rgba(124, 58, 237, 0.12);
}

.orb-2 {
  width: 500px;
  height: 500px;
  bottom: -100px;
  right: -100px;
  background: rgba(6, 182, 212, 0.1);
  animation-delay: 8s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  top: 40%;
  left: 40%;
  background: rgba(236, 72, 153, 0.06);
  animation-delay: 15s;
}

:global(html.light) .orb-1 { background: rgba(6, 182, 212, 0.15); }
:global(html.light) .orb-2 { background: rgba(14, 165, 233, 0.12); }
:global(html.light) .orb-3 { background: rgba(45, 212, 191, 0.08); }

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, -30px) scale(1.08); }
  66% { transform: translate(-30px, 40px) scale(0.95); }
}

/* 顶部导航栏 */
.top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: linear-gradient(180deg, rgba(10, 15, 26, 0.95) 0%, rgba(10, 15, 26, 0.8) 70%, transparent 100%);
  backdrop-filter: blur(12px);
}

:global(html.light) .top-bar {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 70%, transparent 100%);
}

.top-bar-left,
.top-bar-center,
.top-bar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  font-size: 24px;
  color: #a78bfa;
  animation: icon-glow 3s ease-in-out infinite;
}

:global(html.light) .brand-icon {
  color: #0891b2;
}

@keyframes icon-glow {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(167, 139, 250, 0.5)); }
  50% { filter: drop-shadow(0 0 16px rgba(167, 139, 250, 0.8)); }
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 16px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: 0.5px;
}

:global(html.light) .brand-title {
  color: #0c4a6e;
}

.brand-subtitle {
  font-size: 10px;
  color: #64748b;
}

/* 搜索框 */
.search-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 280px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 10px;
  padding: 0 12px;
  transition: all 0.2s ease;
}

:global(html.light) .search-box {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.search-box:focus-within {
  border-color: #a78bfa;
  box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
}

:global(html.light) .search-box:focus-within {
  border-color: #0891b2;
  box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.15);
}

.search-box i {
  color: #64748b;
  font-size: 14px;
}

.search-box input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 10px 10px;
  font-size: 13px;
  color: #e2e8f0;
}

:global(html.light) .search-box input {
  color: #1e293b;
}

.search-box input::placeholder {
  color: #64748b;
}

.search-clear {
  cursor: pointer;
  color: #64748b;
  padding: 4px;
}

.search-clear:hover {
  color: #94a3b8;
}

/* 搜索下拉 */
.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 6px;
  background: rgba(15, 23, 42, 0.98);
  border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 12px;
  padding: 6px;
  max-height: 320px;
  overflow-y: auto;
  z-index: 200;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

:global(html.light) .search-dropdown {
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(6, 182, 212, 0.2);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.search-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.search-item:hover {
  background: rgba(124, 58, 237, 0.15);
}

:global(html.light) .search-item:hover {
  background: rgba(6, 182, 212, 0.1);
}

.search-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.search-name {
  flex: 1;
  font-size: 13px;
  color: #e2e8f0;
}

:global(html.light) .search-name {
  color: #1e293b;
}

.search-cat {
  font-size: 11px;
  color: #64748b;
}

/* 统计信息 */
.stats-row {
  display: flex;
  gap: 8px;
}

.stat-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 8px;
}

:global(html.light) .stat-chip {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(6, 182, 212, 0.15);
}

.stat-value {
  font-size: 14px;
  font-weight: 700;
  color: #a78bfa;
}

:global(html.light) .stat-value {
  color: #0891b2;
}

.stat-label {
  font-size: 11px;
  color: #64748b;
}

/* 缩放控制 */
.zoom-controls {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 8px;
  padding: 2px;
}

:global(html.light) .zoom-controls {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(6, 182, 212, 0.15);
}

.zoom-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #94a3b8;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.zoom-btn:hover {
  background: rgba(124, 58, 237, 0.2);
  color: #a78bfa;
}

:global(html.light) .zoom-btn:hover {
  background: rgba(6, 182, 212, 0.15);
  color: #0891b2;
}

.zoom-value {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  min-width: 40px;
  text-align: center;
}

.icon-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(100, 116, 139, 0.2);
  background: rgba(30, 41, 59, 0.6);
  color: #94a3b8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

:global(html.light) .icon-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(6, 182, 212, 0.15);
}

.icon-btn:hover {
  background: rgba(124, 58, 237, 0.2);
  border-color: #a78bfa;
  color: #a78bfa;
}

:global(html.light) .icon-btn:hover {
  background: rgba(6, 182, 212, 0.15);
  border-color: #0891b2;
  color: #0891b2;
}

/* 左侧类别筛选 */
.category-sidebar {
  position: absolute;
  top: 80px;
  left: 16px;
  z-index: 90;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: calc(100vh - 160px);
  overflow-y: auto;
  padding-right: 8px;
}

.category-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

:global(html.light) .category-chip {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(100, 116, 139, 0.15);
}

.category-chip:hover {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(124, 58, 237, 0.3);
}

:global(html.light) .category-chip:hover {
  background: rgba(255, 255, 255, 1);
  border-color: rgba(6, 182, 212, 0.3);
}

.category-chip.active {
  background: var(--cat-color, #a78bfa);
  border-color: transparent;
}

.category-chip.active .chip-label,
.category-chip.active .chip-count {
  color: white;
}

.chip-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.chip-dot.all {
  background: linear-gradient(135deg, #a78bfa, #06b6d4);
}

.chip-label {
  font-size: 12px;
  font-weight: 500;
  color: #e2e8f0;
}

:global(html.light) .chip-label {
  color: #334155;
}

.chip-count {
  font-size: 10px;
  color: #64748b;
  background: rgba(100, 116, 139, 0.2);
  padding: 2px 6px;
  border-radius: 6px;
}

/* 可缩放容器 */
.scalable-content {
  position: relative;
  width: 100%;
  height: 100%;
  transform-origin: center center;
  transition: transform 0.1s ease-out;
}

/* 类别扇形 */
.category-sectors {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.category-sector {
  transition: opacity 0.3s ease;
}

/* 中心圆 */
.center-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
  border: 2px solid rgba(124, 58, 237, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  overflow: hidden;
}

:global(html.light) .center-circle {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(14, 165, 233, 0.15) 100%);
  border: 2px solid rgba(6, 182, 212, 0.5);
}

.center-glow {
  position: absolute;
  inset: -50px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.3) 0%, transparent 70%);
  animation: center-pulse 4s ease-in-out infinite;
}

:global(html.light) .center-glow {
  background: radial-gradient(circle, rgba(6, 182, 212, 0.35) 0%, transparent 70%);
}

@keyframes center-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

.center-content {
  z-index: 1;
}

.center-icon {
  font-size: 32px;
  color: #a78bfa;
  animation: icon-spin 20s linear infinite;
}

:global(html.light) .center-icon {
  color: #0891b2;
}

@keyframes icon-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* SVG连接线 */
.connections-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.connection-line {
  fill: none;
  stroke-width: 2;
  opacity: 0.3;
  transition: all 0.3s ease;
}

.connection-line.is-promotion {
  stroke-width: 2.5;
  opacity: 0.45;
}

.connection-line.is-transfer {
  stroke-width: 2;
  opacity: 0.4;
}

.connection-line.highlighted {
  stroke-width: 4;
  opacity: 1;
  filter: url(#glow);
}

/* 职业节点 */
.career-node {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 10;
  cursor: pointer;
  transition: all 0.25s ease;
}

.career-node:hover,
.career-node.is-hovered {
  z-index: 30;
}

.career-node.is-dimmed {
  opacity: 0.2;
  filter: grayscale(0.6);
}

.career-node.is-related {
  opacity: 1;
  filter: none;
  z-index: 25;
}

.career-node.is-searched {
  z-index: 35;
  animation: searched-pulse 1s ease-in-out 3;
}

@keyframes searched-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.15); }
}

.career-node.is-highlighted {
  z-index: 30;
  animation: highlighted-glow 1.5s ease-in-out infinite;
}

.career-node.is-highlighted .node-body {
  border-color: #fbbf24;
  box-shadow: 0 0 30px rgba(251, 191, 36, 0.5), 0 0 60px rgba(251, 191, 36, 0.3);
}

@keyframes highlighted-glow {
  0%, 100% { 
    filter: brightness(1);
  }
  50% { 
    filter: brightness(1.2);
  }
}

.node-body {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px 8px 12px;
  background: rgba(15, 23, 42, 0.9);
  border: 1.5px solid rgba(124, 58, 237, 0.25);
  border-radius: 24px;
  backdrop-filter: blur(10px);
  transition: all 0.25s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

:global(html.light) .node-body {
  background: rgba(255, 255, 255, 0.95);
  border: 1.5px solid rgba(6, 182, 212, 0.25);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.career-node:hover .node-body,
.career-node.is-hovered .node-body {
  background: rgba(15, 23, 42, 0.98);
  border-color: var(--color);
  box-shadow: 0 0 30px rgba(var(--color), 0.4), 0 8px 30px rgba(0, 0, 0, 0.4);
  transform: scale(1.08);
}

:global(html.light) .career-node:hover .node-body,
:global(html.light) .career-node.is-hovered .node-body {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 25px rgba(6, 182, 212, 0.25), 0 8px 30px rgba(0, 0, 0, 0.15);
}

.career-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--color);
  box-shadow: 0 0 12px var(--color), 0 0 24px var(--color);
  animation: dot-breathe 3s ease-in-out infinite;
  animation-delay: var(--delay);
  flex-shrink: 0;
}

@keyframes dot-breathe {
  0%, 100% { transform: scale(1); box-shadow: 0 0 12px var(--color), 0 0 24px var(--color); }
  50% { transform: scale(1.3); box-shadow: 0 0 18px var(--color), 0 0 36px var(--color); }
}

.career-node:hover .career-dot,
.career-node.is-hovered .career-dot {
  animation: none;
  width: 16px;
  height: 16px;
  box-shadow: 0 0 18px var(--color), 0 0 36px var(--color), 0 0 54px var(--color);
}

.career-name {
  font-size: 13px;
  font-weight: 500;
  color: #e2e8f0;
  white-space: nowrap;
}

:global(html.light) .career-name {
  color: #1e293b;
}

.career-node:hover .career-name,
.career-node.is-hovered .career-name {
  color: #f8fafc;
  font-weight: 600;
}

:global(html.light) .career-node:hover .career-name,
:global(html.light) .career-node.is-hovered .career-name {
  color: #0c4a6e;
}

/* 热门标记 */
.hot-badge {
  position: absolute;
  top: -6px;
  right: -2px;
  color: #f97316;
  font-size: 12px;
  z-index: 10;
  animation: hot-bounce 2s ease-in-out infinite;
}

@keyframes hot-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.career-node.is-hot .node-body {
  border-color: rgba(249, 115, 22, 0.5);
}

/* 右侧详情面板 */
.detail-panel {
  position: absolute;
  top: 80px;
  right: 16px;
  z-index: 90;
  width: 240px;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(124, 58, 237, 0.25);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(16px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
}

:global(html.light) .detail-panel {
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(6, 182, 212, 0.25);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
}

.panel-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid rgba(100, 116, 139, 0.15);
}

.panel-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  box-shadow: 0 0 12px currentColor;
  flex-shrink: 0;
}

.panel-info {
  flex: 1;
  min-width: 0;
}

.panel-name {
  font-size: 15px;
  font-weight: 600;
  color: #f1f5f9;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:global(html.light) .panel-name {
  color: #0c4a6e;
}

.panel-cat {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
  display: block;
}

.panel-hot {
  color: #f97316;
  font-size: 16px;
  animation: hot-bounce 2s ease-in-out infinite;
}

.panel-body {
  padding: 12px 16px;
}

.panel-stat-row {
  display: flex;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(100, 116, 139, 0.1);
}

.mini-stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #a78bfa;
}

:global(html.light) .mini-stat {
  color: #0891b2;
}

.mini-stat i {
  font-size: 14px;
}

.path-section {
  margin-top: 12px;
}

.path-title {
  font-size: 10px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.path-title i {
  font-size: 12px;
  color: #a78bfa;
}

:global(html.light) .path-title i {
  color: #0891b2;
}

.path-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.path-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  background: rgba(100, 116, 139, 0.12);
  border-radius: 8px;
  font-size: 11px;
  color: #e2e8f0;
}

:global(html.light) .path-tag {
  background: rgba(100, 116, 139, 0.08);
  color: #334155;
}

.path-tag.promotion {
  border-left: 3px solid #10b981;
}

.path-tag.transfer {
  border-left: 3px solid #06b6d4;
}

.tag-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.skills-section {
  margin-top: 12px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tag {
  font-size: 10px;
  color: #a78bfa;
  background: rgba(124, 58, 237, 0.12);
  padding: 4px 10px;
  border-radius: 10px;
}

:global(html.light) .skill-tag {
  color: #0891b2;
  background: rgba(6, 182, 212, 0.12);
}

.panel-foot {
  padding: 10px 16px;
  background: rgba(100, 116, 139, 0.08);
  font-size: 10px;
  color: #64748b;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

/* 底部图例 */
.bottom-legend {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 90;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 20px;
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 12px;
  backdrop-filter: blur(12px);
}

:global(html.light) .bottom-legend {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(100, 116, 139, 0.15);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
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
  background-size: 8px 3px;
  background-image: repeating-linear-gradient(90deg, #06b6d4, #06b6d4 4px, transparent 4px, transparent 8px);
}

.legend-divider {
  width: 1px;
  height: 16px;
  background: rgba(100, 116, 139, 0.3);
}

.legend-hint {
  font-size: 10px;
  color: #64748b;
}

/* 面板动画 */
.panel-slide-enter-active,
.panel-slide-leave-active {
  transition: all 0.3s ease;
}

.panel-slide-enter-from,
.panel-slide-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* ═══════════════════════════════════════
   移动端适配样式
   ═══════════════════════════════════════ */

@media (max-width: 768px) {
  /* 顶部导航栏移动端优化 */
  .top-bar {
    padding: 12px 12px !important;
    gap: 8px !important;
    flex-wrap: wrap;
  }
  
  .top-bar-left {
    flex: 0 0 auto;
  }
  
  .brand {
    gap: 8px !important;
    padding: 6px 10px !important;
  }
  
  .brand-icon {
    font-size: 18px !important;
  }
  
  .brand-text {
    display: none !important;
  }
  
  .top-bar-center {
    flex: 1 1 100%;
    order: 3;
    margin-top: 8px;
  }
  
  .search-box {
    width: 100% !important;
    min-width: auto !important;
    max-width: none !important;
  }
  
  .top-bar-right {
    flex: 1 1 auto;
    gap: 6px !important;
    justify-content: flex-end;
  }
  
  .stats-row {
    display: none !important;
  }
  
  .zoom-controls {
    padding: 4px 8px !important;
    gap: 4px !important;
  }
  
  .zoom-value {
    display: none !important;
  }
  
  .zoom-btn {
    width: 28px !important;
    height: 28px !important;
  }
  
  .icon-btn {
    width: 32px !important;
    height: 32px !important;
  }
  
  /* 左侧类别筛选栏移动端隐藏，改为底部显示 */
  .category-sidebar {
    position: fixed !important;
    top: auto !important;
    bottom: 70px !important;
    left: 0 !important;
    right: 0 !important;
    transform: none !important;
    width: 100% !important;
    flex-direction: row !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    padding: 8px 12px !important;
    background: rgba(15, 23, 42, 0.95) !important;
    border-radius: 0 !important;
    border-top: 1px solid rgba(100, 116, 139, 0.2) !important;
    gap: 8px !important;
    scrollbar-width: none;
    -ms-overflow-style: none;
    z-index: 100 !important;
    max-height: none !important;
  }
  
  .category-sidebar::-webkit-scrollbar {
    display: none;
  }
  
  .category-chip {
    flex-shrink: 0 !important;
    padding: 6px 12px !important;
    white-space: nowrap !important;
  }
  
  .chip-label {
    font-size: 11px !important;
  }
  
  .chip-count {
    font-size: 9px !important;
    padding: 1px 5px !important;
  }
  
  /* 详情面板移动端全宽底部显示 */
  .detail-panel {
    position: fixed !important;
    top: auto !important;
    bottom: 130px !important;
    left: 12px !important;
    right: 12px !important;
    width: auto !important;
    max-height: 40vh !important;
    overflow-y: auto !important;
  }
  
  /* 底部图例隐藏 */
  .bottom-legend {
    display: none !important;
  }
  
  /* 节点样式移动端优化 */
  .node-body {
    padding: 6px 12px 6px 10px !important;
    gap: 8px !important;
  }
  
  .career-dot {
    width: 12px !important;
    height: 12px !important;
  }
  
  .career-name {
    font-size: 11px !important;
  }
}

/* 极小屏幕 */
@media (max-width: 480px) {
  .top-bar {
    padding: 8px !important;
  }
  
  .brand {
    padding: 4px 8px !important;
  }
  
  .category-sidebar {
    bottom: 65px !important;
    padding: 6px 8px !important;
  }
  
  .category-chip {
    padding: 4px 10px !important;
  }
  
  .detail-panel {
    bottom: 120px !important;
    left: 8px !important;
    right: 8px !important;
  }
}

/* 白天模式移动端 */
@media (max-width: 768px) {
  :global(html.light) .category-sidebar {
    background: rgba(255, 255, 255, 0.95) !important;
    border-top: 1px solid rgba(6, 182, 212, 0.2) !important;
  }
}
</style>
