import { defineConfig, loadConfigFromFile } from 'vite'
import react from '@vitejs/plugin-react'

//TODO: Initial config, change to loadConfigFromFile
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 9999,
    strictPort: true,
    allowedHosts: ['wayfinder.kryptonguy.tech'],
  },
})