import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  // Repositório de projeto no GitHub Pages: castrokleber-bit.github.io/ctb/, não a raiz
  // do domínio. Sem isso os assets (JS/CSS/dados) resolvem para a raiz errada em produção.
  base: '/ctb/',
  plugins: [react()],
})
