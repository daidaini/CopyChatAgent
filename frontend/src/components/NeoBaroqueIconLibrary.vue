<template>
  <div class="neo-baroque-icon-library">
    <!-- Icon Categories -->
    <div class="icon-category" v-for="(category, categoryName) in iconCategories" :key="categoryName">
      <h3>{{ category.title }}</h3>
      <div class="icon-grid">
        <div
          v-for="icon in category.icons"
          :key="icon.name"
          class="icon-item"
          @click="$emit('select', icon)"
          @mouseenter="hoveredIcon = icon.name"
          @mouseleave="hoveredIcon = null"
        >
          <NeoBaroqueIcon
            :symbol="icon.symbol"
            :size="hoveredIcon === icon.name ? 'large' : 'medium'"
            :variant="icon.variant"
            :glow="hoveredIcon === icon.name"
            :sparkle="hoveredIcon === icon.name"
            :animated="hoveredIcon === icon.name"
          />
          <span class="icon-name">{{ icon.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NeoBaroqueIcon from './NeoBaroqueIcon.vue'

export default {
  name: 'NeoBaroqueIconLibrary',
  components: {
    NeoBaroqueIcon
  },
  data() {
    return {
      hoveredIcon: null,
      iconCategories: {
        decorative: {
          title: '装饰图标',
          icons: [
            { name: '星芒', symbol: '✦', variant: 'gold' },
            { name: '雪花', symbol: '❅', variant: 'sapphire' },
            { name: '星尘', symbol: '✧', variant: 'silver' },
            { name: '花饰', symbol: '❈', variant: 'emerald' },
            { name: '玫瑰', symbol: '❀', variant: 'ruby' },
            { name: '莲花', symbol: '❁', variant: 'royal' },
            { name: '百合', symbol: '❂', variant: 'gold' },
            { name: '樱吹', symbol: '❃', variant: 'sapphire' }
          ]
        },
        celestial: {
          title: '天体图标',
          icons: [
            { name: '太阳', symbol: '☀', variant: 'gold' },
            { name: '月亮', symbol: '☽', variant: 'silver' },
            { name: '星星', symbol: '⭐', variant: 'gold' },
            { name: '彗星', symbol: '☄', variant: 'sapphire' },
            { name: '云朵', symbol: '☁', variant: 'silver' },
            { name: '雨滴', symbol: '☔', variant: 'sapphire' },
            { name: '闪电', symbol: '⚡', variant: 'gold' },
            { name: '彩虹', symbol: '🌈', variant: 'emerald' }
          ]
        },
        mystical: {
          title: '神秘图标',
          icons: [
            { name: '之眼', symbol: '👁', variant: 'royal' },
            { name: '钥匙', symbol: '🔑', variant: 'gold' },
            { name: '王冠', symbol: '👑', variant: 'gold' },
            { name: '宝石', symbol: '💎', variant: 'sapphire' },
            { name: '蜡烛', symbol: '🕯', variant: 'gold' },
            { name: '镜子', symbol: '🪞', variant: 'silver' },
            { name: '罗盘', symbol: '🧭', variant: 'gold' },
            { name: '沙漏', symbol: '⏳', variant: 'gold' }
          ]
        },
        nature: {
          title: '自然图标',
          icons: [
            { name: '花朵', symbol: '🌸', variant: 'ruby' },
            { name: '叶子', symbol: '🍃', variant: 'emerald' },
            { name: '树木', symbol: '🌳', variant: 'emerald' },
            { name: '山峰', symbol: '⛰', variant: 'sapphire' },
            { name: '海洋', symbol: '🌊', variant: 'sapphire' },
            { name: '火焰', symbol: '🔥', variant: 'ruby' },
            { name: '大地', symbol: '🌍', variant: 'emerald' },
            { name: '星辰', symbol: '✨', variant: 'gold' }
          ]
        },
        wisdom: {
          title: '智慧图标',
          icons: [
            { name: '书籍', symbol: '📚', variant: 'gold' },
            { name: '羽毛笔', symbol: '🪶', variant: 'sapphire' },
            { name: '卷轴', symbol: '📜', variant: 'gold' },
            { name: '墨水瓶', symbol: '🍶', variant: 'sapphire' },
            { name: '眼镜', symbol: '👓', variant: 'silver' },
            { name: '灯泡', symbol: '💡', variant: 'gold' },
            { name: '问号', symbol: '❓', variant: 'gold' },
            { name: '灯', symbol: '🏮', variant: 'gold' }
          ]
        },
        emotion: {
          title: '情感图标',
          icons: [
            { name: '爱心', symbol: '❤', variant: 'ruby' },
            { name: '音乐', symbol: '🎵', variant: 'royal' },
            { name: '面具', symbol: '🎭', variant: 'royal' },
            { name: '星星眼', symbol: '🤩', variant: 'gold' },
            { name: '思考', symbol: '🤔', variant: 'sapphire' },
            { name: '欢呼', symbol: '🎉', variant: 'gold' },
            { name: '祈祷', symbol: '🙏', variant: 'gold' },
            { name: '和平', symbol: '☮', variant: 'emerald' }
          ]
        }
      }
    }
  }
}
</script>

<style scoped>
.neo-baroque-icon-library {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.icon-category {
  margin-bottom: 40px;
}

.icon-category h3 {
  font-family: var(--decorative-font);
  font-size: 1.5rem;
  color: var(--deep-blue);
  margin-bottom: 20px;
  text-align: center;
  position: relative;
}

.icon-category h3::before,
.icon-category h3::after {
  content: '❦';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary-gold);
  font-size: 1.2rem;
}

.icon-category h3::before {
  left: 20px;
}

.icon-category h3::after {
  right: 20px;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--border-radius-ornate);
  border: var(--border-silver);
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border-radius: var(--border-radius-ornate);
  background: rgba(255, 255, 255, 0.8);
  border: var(--border-silver);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.icon-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-gold);
  background: rgba(244, 228, 193, 0.2);
  border-color: var(--primary-gold);
}

.icon-name {
  font-size: 0.9rem;
  color: var(--charcoal);
  font-weight: bold;
  margin-top: 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .icon-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 15px;
    padding: 15px;
  }

  .icon-item {
    padding: 10px;
  }

  .icon-name {
    font-size: 0.8rem;
  }
}

/* Accessibility */
.icon-item:focus {
  outline: 3px solid var(--primary-gold);
  outline-offset: 2px;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .icon-grid {
    background: rgba(255, 255, 255, 0.8);
    border: var(--border-gold);
  }

  .icon-item {
    background: rgba(255, 255, 255, 0.9);
    border: var(--border-gold);
  }
}
</style>