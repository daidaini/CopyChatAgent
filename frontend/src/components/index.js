// Neo-Baroque Digital Components Library
export { default as NeoBaroqueDecorations } from './NeoBaroqueDecorations.vue'
export { default as NeoBaroqueCard } from './NeoBaroqueCard.vue'
export { default as NeoBaroqueButton } from './NeoBaroqueButton.vue'
export { default as NeoBaroqueHeader } from './NeoBaroqueHeader.vue'
export { default as NeoBaroqueIcon } from './NeoBaroqueIcon.vue'
export { default as NeoBaroqueLoading } from './NeoBaroqueLoading.vue'
export { default as NeoBaroqueIconLibrary } from './NeoBaroqueIconLibrary.vue'

// Component names for global registration
export const components = {
  NeoBaroqueDecorations: () => import('./NeoBaroqueDecorations.vue'),
  NeoBaroqueCard: () => import('./NeoBaroqueCard.vue'),
  NeoBaroqueButton: () => import('./NeoBaroqueButton.vue'),
  NeoBaroqueHeader: () => import('./NeoBaroqueHeader.vue'),
  NeoBaroqueIcon: () => import('./NeoBaroqueIcon.vue'),
  NeoBaroqueLoading: () => import('./NeoBaroqueLoading.vue'),
  NeoBaroqueIconLibrary: () => import('./NeoBaroqueIconLibrary.vue')
}

// Global registration function
export function registerComponents(app) {
  Object.entries(components).forEach(([name, component]) => {
    app.component(name, component)
  })
}