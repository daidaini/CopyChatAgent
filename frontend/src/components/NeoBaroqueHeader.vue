<template>
  <header class="neo-baroque-header" :class="headerClass">
    <div class="header-decoration left">
      <NeoBaroqueIcon
        v-for="(icon, index) in leftIcons"
        :key="`left-${index}`"
        :symbol="icon.symbol"
        :size="icon.size"
        :variant="icon.variant"
        :glow="icon.glow"
        :sparkle="icon.sparkle"
        :animated="icon.animated"
        :rotate="icon.rotate"
        class="decoration-icon"
      />
    </div>

    <div class="header-content">
      <NeoBaroqueIcon
        v-if="mainIcon"
        :symbol="mainIcon"
        size="xlarge"
        :variant="mainVariant"
        :glow="true"
        :sparkle="true"
        :animated="true"
        class="main-icon"
      />
      <h1 class="header-title">
        <span class="title-icon" v-if="titlePrefixIcon">
          <NeoBaroqueIcon
            :symbol="titlePrefixIcon"
            size="medium"
            :variant="titleIconVariant"
            :glow="true"
          />
        </span>
        <span class="title-text">{{ title }}</span>
        <span class="title-icon" v-if="titleSuffixIcon">
          <NeoBaroqueIcon
            :symbol="titleSuffixIcon"
            size="medium"
            :variant="titleIconVariant"
            :glow="true"
          />
        </span>
      </h1>
      <p v-if="subtitle" class="header-subtitle">{{ subtitle }}</p>
    </div>

    <div class="header-decoration right">
      <NeoBaroqueIcon
        v-for="(icon, index) in rightIcons"
        :key="`right-${index}`"
        :symbol="icon.symbol"
        :size="icon.size"
        :variant="icon.variant"
        :glow="icon.glow"
        :sparkle="icon.sparkle"
        :animated="icon.animated"
        :rotate="icon.rotate"
        class="decoration-icon"
      />
    </div>

    <!-- Ornamental Dividers -->
    <div class="header-divider left"></div>
    <div class="header-divider right"></div>

    <!-- Floating Ornaments -->
    <div class="floating-ornament top-left">❦</div>
    <div class="floating-ornament top-right">❅</div>
    <div class="floating-ornament bottom-left">✧</div>
    <div class="floating-ornament bottom-right">❈</div>
  </header>
</template>

<script>
import NeoBaroqueIcon from './NeoBaroqueIcon.vue'

export default {
  name: 'NeoBaroqueHeader',
  components: {
    NeoBaroqueIcon
  },
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    },
    mainIcon: {
      type: String,
      default: '✦'
    },
    mainVariant: {
      type: String,
      default: 'gold'
    },
    titlePrefixIcon: {
      type: String,
      default: ''
    },
    titleSuffixIcon: {
      type: String,
      default: ''
    },
    titleIconVariant: {
      type: String,
      default: 'gold'
    },
    variant: {
      type: String,
      default: 'default', // default, compact, ornate
      validator: (value) => ['default', 'compact', 'ornate'].includes(value)
    },
    alignment: {
      type: String,
      default: 'center', // left, center, right
      validator: (value) => ['left', 'center', 'right'].includes(value)
    }
  },
  computed: {
    headerClass() {
      return [
        `neo-baroque-header--${this.variant}`,
        `neo-baroque-header--${this.alignment}`
      ]
    },
    leftIcons() {
      return [
        { symbol: '❦', size: 'large', variant: 'gold', glow: true, animated: true },
        { symbol: '✧', size: 'medium', variant: 'silver', sparkle: true, rotate: true }
      ]
    },
    rightIcons() {
      return [
        { symbol: '❅', size: 'medium', variant: 'sapphire', sparkle: true, animated: true },
        { symbol: '❈', size: 'large', variant: 'emerald', glow: true, rotate: true }
      ]
    }
  }
}
</script>

<style scoped>
.neo-baroque-header {
  position: relative;
  text-align: center;
  padding: 40px 20px;
  margin: 20px 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(244, 228, 193, 0.2) 100%);
  border-radius: var(--border-radius-ornate);
  border: var(--border-silver);
  overflow: hidden;
}

.neo-baroque-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gold-gradient);
}

.neo-baroque-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gold-gradient);
}

/* Header Variations */
.neo-baroque-header--compact {
  padding: 20px;
  margin: 10px 0;
}

.neo-baroque-header--ornate {
  padding: 60px 20px;
  margin: 30px 0;
  border: var(--border-gold);
}

.neo-baroque-header--ornate::before,
.neo-baroque-header--ornate::after {
  height: 5px;
}

/* Alignment Variations */
.neo-baroque-header--left {
  text-align: left;
}

.neo-baroque-header--right {
  text-align: right;
}

/* Header Content */
.header-content {
  position: relative;
  z-index: 2;
}

.main-icon {
  margin-bottom: 15px;
}

.header-title {
  font-family: var(--decorative-font);
  font-size: 3rem;
  color: var(--deep-blue);
  margin: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.title-text {
  position: relative;
}

.title-text::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 2px;
  background: var(--gold-gradient);
  border-radius: 1px;
}

.neo-baroque-header--left .title-text::after {
  left: 0;
  transform: none;
}

.neo-baroque-header--right .title-text::after {
  left: auto;
  right: 0;
  transform: none;
}

.title-icon {
  display: flex;
  align-items: center;
}

.header-subtitle {
  font-family: var(--secondary-font);
  font-size: 1.2rem;
  color: var(--sapphire-blue);
  margin-top: 15px;
  opacity: 0.9;
  font-style: italic;
}

/* Header Decorations */
.header-decoration {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1;
}

.header-decoration.left {
  left: 20px;
}

.header-decoration.right {
  right: 20px;
}

.decoration-icon {
  opacity: 0.8;
  transition: all 0.3s ease;
}

.neo-baroque-header:hover .decoration-icon {
  opacity: 1;
  transform: scale(1.1);
}

/* Header Dividers */
.header-divider {
  position: absolute;
  top: 20px;
  width: 2px;
  height: calc(100% - 40px);
  background: linear-gradient(to bottom, var(--primary-gold), transparent, var(--primary-gold));
  opacity: 0.3;
}

.header-divider.left {
  left: 60px;
}

.header-divider.right {
  right: 60px;
}

/* Floating Ornaments */
.floating-ornament {
  position: absolute;
  font-size: 1.5rem;
  color: var(--primary-gold);
  opacity: 0.3;
  animation: float 6s ease-in-out infinite;
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
  pointer-events: none;
}

.floating-ornament.top-left {
  top: 10px;
  left: 10px;
  animation-delay: 0s;
}

.floating-ornament.top-right {
  top: 10px;
  right: 10px;
  animation-delay: 1s;
}

.floating-ornament.bottom-left {
  bottom: 10px;
  left: 10px;
  animation-delay: 2s;
}

.floating-ornament.bottom-right {
  bottom: 10px;
  right: 10px;
  animation-delay: 3s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

/* Compact Mode Adjustments */
.neo-baroque-header--compact .header-title {
  font-size: 2rem;
}

.neo-baroque-header--compact .header-subtitle {
  font-size: 1rem;
}

.neo-baroque-header--compact .decoration-icon {
  transform: scale(0.8);
}

.neo-baroque-header--compact .floating-ornament {
  font-size: 1rem;
}

/* Ornate Mode Enhancements */
.neo-baroque-header--ornate .header-title {
  font-size: 4rem;
}

.neo-baroque-header--ornate .header-subtitle {
  font-size: 1.5rem;
}

.neo-baroque-header--ornate .floating-ornament {
  font-size: 2rem;
  animation-duration: 8s;
}

/* Responsive Design */
@media (max-width: 768px) {
  .neo-baroque-header {
    padding: 30px 15px;
    margin: 15px 0;
  }

  .neo-baroque-header--compact {
    padding: 15px;
  }

  .neo-baroque-header--ornate {
    padding: 40px 15px;
  }

  .header-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 10px;
  }

  .neo-baroque-header--ornate .header-title {
    font-size: 2.5rem;
  }

  .header-subtitle {
    font-size: 1rem;
  }

  .header-decoration {
    display: none;
  }

  .header-divider {
    display: none;
  }

  .floating-ornament {
    font-size: 1rem;
  }

  .neo-baroque-header--ornate .floating-ornament {
    font-size: 1.2rem;
  }
}

/* Accessibility */
.neo-baroque-header:focus-within {
  outline: 3px solid var(--primary-gold);
  outline-offset: 2px;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .neo-baroque-header {
    border: var(--border-gold);
    background: rgba(255, 255, 255, 0.3);
  }

  .floating-ornament {
    opacity: 0.8;
  }

  .header-title {
    color: var(--charcoal);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }
}
</style>