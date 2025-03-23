import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@constants': path.resolve(__dirname, './src/constants'),
      '@styles': path.resolve(__dirname, './src/styles'),
    },
  },
  server: {
    port: parseInt(process.env.FRONTEND_PORT || '4550'), // Default our Frontend port to 4550
    host: '0.0.0.0', // Ensure the server is accessible from outside the container
    watch: {
      usePolling: true, // Use polling to detect changes in Docker
    },
  },
});
