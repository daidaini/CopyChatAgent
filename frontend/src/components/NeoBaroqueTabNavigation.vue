<template>
  <div class="tab-navigation">
    <div class="tab-buttons">
      <NeoBaroqueButton
        v-for="tab in tabs"
        :key="tab.id"
        :text="tab.label"
        :icon="tab.icon"
        :variant="activeTab === tab.id ? 'primary' : 'secondary'"
        :disabled="isLoading"
        @click="$emit('tab-change', tab.id)"
        size="medium"
        class="tab-button"
      />
    </div>
  </div>
</template>

<script>
import NeoBaroqueButton from './NeoBaroqueButton.vue'

export default {
  name: 'NeoBaroqueTabNavigation',
  components: {
    NeoBaroqueButton
  },
  props: {
    tabs: {
      type: Array,
      required: true,
      default: () => []
    },
    activeTab: {
      type: String,
      required: true
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['tab-change']
}
</script>

<style scoped>
.tab-navigation {
  margin-bottom: 30px;
}

.tab-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.tab-button {
  min-width: 150px;
}

@media (max-width: 768px) {
  .tab-buttons {
    flex-direction: column;
    align-items: center;
  }

  .tab-button {
    width: 100%;
    max-width: 300px;
  }
}
</style>