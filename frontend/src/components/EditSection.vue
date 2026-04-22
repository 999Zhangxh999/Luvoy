<template>
  <div class="edit-section" :class="{ 'is-expanded': isExpanded }">
    <div class="section-header" @click="$emit('toggle')">
      <div class="flex items-center gap-3">
        <div class="section-icon">
          <i :class="icon"></i>
        </div>
        <h3 class="section-title">{{ title }}</h3>
        <span v-if="badge" class="section-badge">{{ badge }}</span>
      </div>
      <div class="flex items-center gap-2">
        <button 
          v-if="hasDelete" 
          @click.stop="$emit('delete')" 
          class="delete-btn"
          title="删除此模块"
        >
          <i class="bi bi-trash"></i>
        </button>
        <button 
          v-if="hasAdd && isExpanded" 
          @click.stop="$emit('add')" 
          class="add-btn"
        >
          <i class="bi bi-plus-lg"></i>
        </button>
        <i class="bi bi-chevron-down section-chevron" :class="{ 'rotate-180': isExpanded }"></i>
      </div>
    </div>
    <transition name="expand">
      <div v-show="isExpanded" class="section-content">
        <slot></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  icon: { type: String, default: 'bi-folder' },
  badge: { type: String, default: '' },
  isExpanded: { type: Boolean, default: false },
  hasAdd: { type: Boolean, default: false },
  hasDelete: { type: Boolean, default: false }
})

defineEmits(['toggle', 'add', 'delete'])
</script>

<style scoped>
.edit-section {
  @apply rounded-xl border border-brand-border bg-brand-surface overflow-hidden transition-all;
}
.edit-section.is-expanded {
  @apply border-violet-500/30;
}

.section-header {
  @apply flex items-center justify-between px-4 py-3 cursor-pointer 
         hover:bg-slate-800/30 transition select-none;
}
.section-icon {
  @apply w-8 h-8 rounded-lg bg-violet-500/15 text-violet-400 flex items-center justify-center;
}
.section-title {
  @apply text-sm font-semibold text-brand-text;
}
.section-badge {
  @apply px-2 py-0.5 rounded-full text-xs bg-emerald-500/20 text-emerald-400;
}
.section-chevron {
  @apply text-brand-muted transition-transform duration-200;
}

.add-btn {
  @apply w-7 h-7 rounded-lg bg-violet-500/20 text-violet-400 flex items-center justify-center
         hover:bg-violet-500/30 transition;
}

.delete-btn {
  @apply w-7 h-7 rounded-lg bg-red-500/10 text-red-400/60 flex items-center justify-center
         hover:bg-red-500/20 hover:text-red-400 transition;
}

.section-content {
  @apply px-4 pb-4;
}

/* 展开动画 */
.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.expand-enter-from, .expand-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.expand-enter-to, .expand-leave-from {
  opacity: 1;
  max-height: 1000px;
}
</style>
