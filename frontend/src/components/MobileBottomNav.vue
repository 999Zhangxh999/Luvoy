<template>
  <nav class="mobile-bottom-nav" v-if="showNav">
    <div class="nav-items">
      <router-link 
        v-for="item in navItems" 
        :key="item.path" 
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
      >
        <i :class="item.icon"></i>
        <span>{{ item.label }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 不显示底部导航的页面
const hiddenRoutes = ['/login', '/register']

const showNav = computed(() => {
  return !hiddenRoutes.includes(route.path) && !route.meta?.hideNav
})

const navItems = [
  { path: '/', label: '首页', icon: 'bi bi-house' },
  { path: '/career/explore', label: '探索', icon: 'bi bi-compass' },
  { path: '/planning', label: '规划', icon: 'bi bi-signpost-2' },
  { path: '/job-hub', label: '求职', icon: 'bi bi-briefcase' },
  { path: '/resume', label: '简历', icon: 'bi bi-file-person' },
  { path: '/user-center', label: '我的', icon: 'bi bi-person-circle' },
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--brand-card);
  border-top: 1px solid var(--brand-border);
  padding-bottom: env(safe-area-inset-bottom, 0px);
  z-index: 100;
  display: none;
}

@media (max-width: 768px) {
  .mobile-bottom-nav {
    display: block;
  }
}

.nav-items {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  padding: 8px 0;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4px 6px;
  color: var(--brand-muted);
  text-decoration: none;
  transition: all 0.2s ease;
  min-width: 48px;
  flex: 1;
  max-width: 64px;
  border-radius: 10px;
}

.nav-item:active {
  transform: scale(0.95);
  background: var(--brand-surface);
}

.nav-item.active {
  color: var(--brand-primary);
}

.nav-item.active i {
  transform: scale(1.1);
}

.nav-item i {
  font-size: 20px;
  margin-bottom: 2px;
  transition: transform 0.2s ease;
}

.nav-item span {
  font-size: 9px;
  font-weight: 500;
  margin-top: 1px;
}

/* 深色模式 */
.dark .mobile-bottom-nav {
  background: rgba(18, 18, 28, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 亮色模式 */
:global(html.light) .mobile-bottom-nav {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-color: #e0f2fe !important;
}

:global(html.light) .nav-item.active {
  color: #0891b2;
}
</style>
