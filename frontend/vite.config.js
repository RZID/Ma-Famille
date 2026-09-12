import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// VITE_BASE_PATH=/ma-famille/ for the final domain
// (college.rzidinc.com/ma-famille), "/" for previews and local dev.
export default defineConfig({
  base: process.env.VITE_BASE_PATH || '/',
  plugins: [vue(), tailwindcss()],
  server: {
    port: 5173,
  },
})
