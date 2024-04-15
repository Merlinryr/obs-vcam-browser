/// <reference types="vite/client" />
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/ws': {
        target: 'ws://localhost:8000',
        changeOrigin: true, // Allow sending cookies across domains
        secure: false, // Disable security checks for development (not recommended for production)
      },
    },
  },
})