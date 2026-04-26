<template>
  <teleport to="body">
    <transition name="overlay">
      <div v-if="visible" class="fixed inset-0 z-[9999] bg-black/60 backdrop-blur-md flex items-center justify-center">
        <div class="bg-brand-card border border-brand-border rounded-2xl p-8 text-center shadow-card animate-fade-in">
          <div class="relative w-16 h-16 mx-auto mb-4">
            <div class="absolute inset-0 border-2 border-brand-border border-t-violet-500 rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center text-2xl text-violet-400">
              <i class="bi bi-robot"></i>
            </div>
          </div>
          <p class="text-brand-text text-sm font-medium mb-3">{{ message || 'AI 智能体正在处理中…' }}</p>
          <div class="flex justify-center gap-1.5">
            <span v-for="i in 3" :key="i" 
              class="w-1.5 h-1.5 rounded-full bg-violet-500 animate-pulse"
              :style="{ animationDelay: `${i * 0.15}s` }"></span>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
defineProps({
  visible: { type: Boolean, default: false },
  message: { type: String, default: '' },
})
</script>

<style scoped>
.overlay-enter-active { transition: opacity 0.25s ease; }
.overlay-leave-active { transition: opacity 0.2s ease; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
</style>
