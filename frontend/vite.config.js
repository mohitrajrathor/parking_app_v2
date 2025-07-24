import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA(
      {
        registerType: 'autoUpdate',
        manifest: {
          name: 'Parkly: A parking facility management application',
          short_name: 'Parkly',
          start_url: '/',
          display: 'standalone',
          background_color: '#ffffff',
          theme_color: '#002fffff',
          icons: [
            {
              src: '/pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png'
            },
            {
              src: '/pwa-512x512.png',
              sizes: '512x512',
              type: 'image/png'
            }
          ]
        }
      }
    )
  ],
  server: {
    proxy: {
      '/api_v1': {
        target: process.env.VITE_BASE_URL,
        changeOrigin: true,
      },
    },
  },
})
