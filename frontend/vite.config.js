import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api_v1': {
        target: 'http://localhost:1234',
        changeOrigin: true,
      },
    },
  },
})
