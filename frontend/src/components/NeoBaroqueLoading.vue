<template>
  <div class="neo-baroque-loading" :class="loadingClass">
    <div class="loading-container">
      <div class="loading-orbit">
        <NeoBaroqueIcon
          v-for="(icon, index) in orbitIcons"
          :key="index"
          :symbol="icon.symbol"
          :size="size"
          :variant="icon.variant"
          :glow="true"
          :sparkle="true"
          :animated="true"
          class="orbit-icon"
          :style="{
            animationDelay: `${index * 0.5}s`,
            transform: `rotate(${index * 60}deg) translateX(${orbitRadius}px) rotate(-${index * 60}deg)`
          }"
        />
      </div>

      <div class="loading-center">
        <NeoBaroqueIcon
          :symbol="centerIcon"
          :size="centerSize"
          :variant="centerVariant"
          :glow="true"
          :sparkle="true"
          :rotate="true"
          class="center-icon"
        />
      </div>

      <div class="loading-text">
        <p class="loading-message">{{ message }}</p>
        <div class="loading-dots">
          <span>.</span>
          <span>.</span>
          <span>.</span>
        </div>
      </div>

      <!-- Floating Decorations -->
      <div class="floating-decoration" v-for="(deco, index) in floatingDecorations" :key="index">
        <NeoBaroqueIcon
          :symbol="deco.symbol"
          :size="deco.size"
          :variant="deco.variant"
          :glow="deco.glow"
          :animated="true"
          class="floating-icon"
          :style="{
            animationDelay: `${index * 0.7}s`,
            left: `${deco.position.x}%`,
            top: `${deco.position.y}%`
          }"
        />
      </div>
    </div>
  </div>
</template>

<script>
import NeoBaroqueIcon from './NeoBaroqueIcon.vue'

export default {
  name: 'NeoBaroqueLoading',
  components: {
    NeoBaroqueIcon
  },
  props: {
    message: {
      type: String,
      default: '正在加载中'
    },
    size: {
      type: String,
      default: 'large'
    },
    variant: {
      type: String,
      default: 'default'
    },
    centerIcon: {
      type: String,
      default: '✦'
    },
    centerVariant: {
      type: String,
      default: 'gold'
    },
    centerSize: {
      type: String,
      default: 'xlarge'
    },
    orbitRadius: {
      type: Number,
      default: 60
    }
  },
  computed: {
    loadingClass() {
      return [`neo-baroque-loading--${this.variant}`]
    },
    orbitIcons() {
      return [
        { symbol: '❅', variant: 'sapphire' },
        { symbol: '✧', variant: 'silver' },
        { symbol: '❈', variant: 'emerald' },
        { symbol: '❀', variant: 'ruby' },
        { symbol: '❁', variant: 'royal' },
        { symbol: '❂', variant: 'gold' }
      ]
    },
    floatingDecorations() {
      return [
        { symbol: '✨', variant: 'gold', size: 'small', glow: true, position: { x: 10, y: 20 } },
        { symbol: '⭐', variant: 'silver', size: 'small', glow: true, position: { x: 90, y: 30 } },
        { symbol: '❦', variant: 'emerald', size: 'medium', glow: true, position: { x: 15, y: 80 } },
        { symbol: '❅', variant: 'sapphire', size: 'small', glow: true, position: { x: 85, y: 70 } }
      ]
    }
  }
}
</script>

<style scoped>
.neo-baroque-loading {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 40px;
}

.loading-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 30px;
}

/* Orbit Animation */
.loading-orbit {
  position: relative;
  width: 200px;
  height: 200px;
  animation: orbit-pulse 4s ease-in-out infinite;
}

.orbit-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center;
  animation: orbit-rotate 6s linear infinite;
}

.center-icon {
  animation: center-pulse 2s ease-in-out infinite;
}

/* Loading Text */
.loading-text {
  text-align: center;
  color: var(--deep-blue);
  font-family: var(--secondary-font);
}

.loading-message {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.loading-dots {
  display: flex;
  gap: 5px;
  justify-content: center;
}

.loading-dots span {
  font-size: 1.5rem;
  color: var(--primary-gold);
  animation: dot-bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(1) {
  animation-delay: 0s;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

/* Floating Decorations */
.floating-decoration {
  position: absolute;
  pointer-events: none;
}

.floating-icon {
  animation: float-random 8s ease-in-out infinite;
}

/* Animations */
@keyframes orbit-rotate {
  0% { transform: rotate(0deg) translateX(60px) rotate(0deg); }
  100% { transform: rotate(360deg) translateX(60px) rotate(-360deg); }
}

@keyframes orbit-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes center-pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
}

@keyframes dot-bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
}

@keyframes float-random {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  25% { transform: translateY(-15px) rotate(5deg); }
  50% { transform: translateY(-10px) rotate(-5deg); }
  75% { transform: translateY(-20px) rotate(3deg); }
}

/* Loading Variants */
.neo-baroque-loading--default {
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--border-radius-ornate);
  border: var(--border-silver);
}

.neo-baroque-loading--overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
}

.neo-baroque-loading--inline {
  background: transparent;
  min-height: 100px;
  padding: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .neo-baroque-loading {
    padding: 20px;
  }

  .loading-orbit {
    width: 150px;
    height: 150px;
  }

  .orbit-icon {
    transform: rotate(0deg) translateX(45px) rotate(0deg);
  }

  .loading-message {
    font-size: 1rem;
  }

  .loading-dots span {
    font-size: 1.2rem;
  }
}

/* Accessibility */
.neo-baroque-loading:focus {
  outline: 3px solid var(--primary-gold);
  outline-offset: 2px;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .orbit-icon,
  .center-icon,
  .floating-icon,
  .loading-dots span {
    animation: none;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .neo-baroque-loading--default {
    background: rgba(255, 255, 255, 0.9);
    border: var(--border-gold);
  }

  .loading-message {
    color: var(--charcoal);
  }
}
</style>