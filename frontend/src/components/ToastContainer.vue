<template>
  <teleport to="body">
    <div class="fixed top-20 right-6 z-[8000] flex flex-col gap-2 max-w-sm w-full">
      <transition-group name="toast">
        <div v-for="t in toasts" :key="t.id" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium shadow-card backdrop-blur-xl"
          :class="toastClass[t.type]">
          <i :class="iconMap[t.type]" class="text-base flex-shrink-0"></i>
          <span class="flex-1">{{ t.message }}</span>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { inject } from 'vue'

const toasts = inject('toasts', [])

const iconMap = {
  success: 'bi bi-check-circle-fill',
  danger: 'bi bi-x-circle-fill',
  warning: 'bi bi-exclamation-triangle-fill',
  info: 'bi bi-info-circle-fill',
}

const toastClass = {
  success: 'bg-emerald-500/90 text-white border border-emerald-400/30',
  danger: 'bg-red-500/90 text-white border border-red-400/30',
  warning: 'bg-orange-500/90 text-white border border-orange-400/30',
  info: 'bg-violet-500/90 text-white border border-violet-400/30',
}
</script>

<style scoped>
.toast-enter-active { 
  animation: toastIn 0.35s ease both; 
}
.toast-leave-active { 
  animation: toastOut 0.25s ease both; 
}
.toast-move { 
  transition: transform 0.3s ease; 
}

@keyframes toastIn {
  from { opacity: 0; transform: translateX(60px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes toastOut {
  from { opacity: 1; transform: translateX(0) scale(1); }
  to { opacity: 0; transform: translateX(60px) scale(0.95); }
}

@media (max-width: 576px) {
  .fixed {
    top: auto !important; 
    bottom: 1rem;
    right: 0.75rem !important; 
    left: 0.75rem;
    max-width: 100%;
  }
}
</style>
