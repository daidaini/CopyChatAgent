// Neo-Baroque Digital Components Library
export { default as NeoBaroqueDecorations } from './NeoBaroqueDecorations.vue'
export { default as NeoBaroqueCard } from './NeoBaroqueCard.vue'
export { default as NeoBaroqueButton } from './NeoBaroqueButton.vue'

// Component names for global registration
export const components = {
  NeoBaroqueDecorations: () => import('./NeoBaroqueDecorations.vue'),
  NeoBaroqueCard: () => import('./NeoBaroqueCard.vue'),
  NeoBaroqueButton: () => import('./NeoBaroqueButton.vue')
}

// Global registration function
export function registerComponents(app) {
  Object.entries(components).forEach(([name, component]) => {
    app.component(name, component)
  })
}