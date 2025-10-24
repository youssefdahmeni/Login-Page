import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:9000',  // Ensure this matches backend host
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // Note: Fixed typo from previous '^/api' to '/api'
      }
    }
  }
});