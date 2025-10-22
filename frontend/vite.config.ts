import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiBase = env.VITE_API_BASE_URL || 'http://localhost:8000';
  return {
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
      proxy: {
        // Optional: in case assets or direct calls made without baseURL
        '/api': {
          target: apiBase,
          changeOrigin: true
        },
        '/ws': {
          target: apiBase.replace('http', 'ws'),
          ws: true,
          changeOrigin: true
        }
      }
    },
    build: {
      sourcemap: true
    }
  };
});
