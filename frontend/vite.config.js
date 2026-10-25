import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    //配置代理(好处是浏览器隐藏了后端地址)
    proxy: {
      // 将/api的请求转到'http://127.0.0.1:8000/api'
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      // 将/api的请求转到'http://127.0.0.1:8000/uploads'
      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
