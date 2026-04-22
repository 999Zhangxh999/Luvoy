import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  css: {
    postcss: './postcss.config.js',
  },
  server: {
    host: '127.0.0.1',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: './dist',
    emptyOutDir: true,
    chunkSizeWarningLimit: 700,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return

          if (id.includes('echarts')) return 'vendor-echarts'
          if (id.includes('vue-router')) return 'vendor-router'
          if (id.includes('/vue/') || id.includes('@vue')) return 'vendor-vue'
          if (id.includes('pinia')) return 'vendor-pinia'
          if (id.includes('axios')) return 'vendor-axios'

          return 'vendor-misc'
        },
      },
    },
  },
})
