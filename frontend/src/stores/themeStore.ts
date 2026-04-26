import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export type ThemeMode = 'light' | 'dark'

export const useThemeStore = defineStore('theme', () => {
    // 从 localStorage 读取主题，默认黑夜模式
    const stored = localStorage.getItem('topo-theme') as ThemeMode | null
    const theme = ref<ThemeMode>(stored || 'dark')

    // 应用主题到 DOM
    function applyTheme(mode: ThemeMode) {
        const root = document.documentElement
        if (mode === 'dark') {
            root.classList.add('dark')
            root.classList.remove('light')
        } else {
            root.classList.add('light')
            root.classList.remove('dark')
        }
    }

    // 切换主题
    function toggleTheme() {
        theme.value = theme.value === 'dark' ? 'light' : 'dark'
    }

    // 设置主题
    function setTheme(mode: ThemeMode) {
        theme.value = mode
    }

    // 监听主题变化
    watch(theme, (newTheme) => {
        localStorage.setItem('topo-theme', newTheme)
        applyTheme(newTheme)
    }, { immediate: true })

    return {
        theme,
        toggleTheme,
        setTheme,
    }
})