<template>
  <footer class="border-t border-brand-border bg-brand-surface/80 mt-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12 mb-12">
        <!-- Brand -->
        <div class="md:col-span-4">
          <div class="flex items-center gap-2.5 mb-4">
            <img src="/logo.svg" alt="拓扑 Topo 标识" class="w-10 h-10 rounded-lg shadow-md" />
            <span class="font-bold text-brand-text text-lg tracking-tight">拓扑 · Topo</span>
          </div>
          <p class="text-brand-muted text-sm leading-relaxed max-w-xs">
            Voyage for long-term growth.<br />有目标、有准备地远航每一段职业路。
          </p>
        </div>

        <!-- Link Columns -->
        <div v-for="group in linkGroups" :key="group.title" class="md:col-span-2 md:col-start-auto">
          <h4 class="text-brand-text font-semibold text-sm mb-5">{{ group.title }}</h4>
          <ul class="space-y-3">
            <li v-for="link in group.links" :key="link.label">
              <router-link v-if="link.to" :to="link.to"
                class="text-brand-muted text-sm hover:text-violet-400 transition-colors">
                {{ link.label }}
              </router-link>
              <a v-else href="#" class="text-brand-muted text-sm hover:text-violet-400 transition-colors">
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="border-t border-brand-border pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-brand-muted text-sm">© 2026 拓扑 · Topo · Life's Unique Path</p>
        <p class="text-brand-muted/50 text-xs">Vue 3 + Flask + Tailwind CSS</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const linkGroups = [
  {
    title: '产品功能',
    links: [
      { label: '职位搜索', to: '/jobs' },
      { label: '职业规划', to: '/career/profile' },
      { label: '简历中心', to: '/resume' },
      { label: 'AI 顾问', to: '/career/explore' },
    ],
  },
  {
    title: '关于我们',
    links: [
      { label: '产品介绍', to: '/about' },
      { label: '联系我们', to: undefined },
      { label: '企业合作', to: undefined },
    ],
  },
  {
    title: '求职者',
    links: [
      { label: '注册账号', to: undefined },
      { label: '完善简历', to: '/resume' },
      { label: '面经分享', to: undefined },
    ],
  },
]
</script>