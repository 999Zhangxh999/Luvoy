<template>
  <div class="career-explore-fullscreen">
    <!-- 全屏地图组件 -->
    <CareerScatterMap
      ref="scatterMapRef"
      :careers="careersWithColors"
      :links="careerLinks"
      :categories="careerCategories"
      :fullscreen="true"
      @select="handleCareerSelect"
      @hover="handleCareerHover"
    />

    <!-- AI 助手 -->
    <CareerAIAssistant
      :careers="careersWithColors"
      :contextCareer="hoveredCareer"
      :careerCount="careersWithColors.length"
      @search="handleAssistantSearch"
      @navigate="handleAssistantNavigate"
      @highlight="handleHighlight"
      @focusCareer="handleFocusCareer"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import CareerScatterMap from '@/components/CareerScatterMap.vue'
import CareerAIAssistant from '@/components/CareerAIAssistant.vue'
import { careersWithColors, careerLinks, careerCategories } from '@/data/careerMockData'

const router = useRouter()
const scatterMapRef = ref(null)
const hoveredCareer = ref(null)

function handleCareerSelect(career) {
  router.push({
    name: 'CareerProfileDetail',
    params: { id: career.id },
  })
}

function handleCareerHover(career) {
  hoveredCareer.value = career
}

function handleAssistantSearch(keyword) {
  if (scatterMapRef.value?.searchCareer) {
    scatterMapRef.value.searchCareer(keyword)
  }
}

function handleAssistantNavigate(careerId) {
  if (scatterMapRef.value?.focusOnCareerById) {
    scatterMapRef.value.focusOnCareerById(careerId)
  }
}

function handleHighlight(careerIds) {
  // 高亮指定的职业节点
  if (scatterMapRef.value?.highlightCareers) {
    scatterMapRef.value.highlightCareers(careerIds)
  }
}

function handleFocusCareer(career) {
  // 聚焦到特定职业
  if (scatterMapRef.value?.focusOnCareer) {
    scatterMapRef.value.focusOnCareer(career)
  }
}
</script>

<style scoped>
.career-explore-fullscreen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>
