<template>
  <span class="neo-baroque-icon" :class="iconClass">
    <span class="icon-content">
      <span class="icon-symbol">{{ symbol }}</span>
      <span class="icon-glow" v-if="glow"></span>
      <span class="icon-sparkle" v-if="sparkle"></span>
    </span>
  </span>
</template>

<script>
export default {
  name: 'NeoBaroqueIcon',
  props: {
    symbol: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large, xlarge
      validator: (value) => ['small', 'medium', 'large', 'xlarge'].includes(value)
    },
    variant: {
      type: String,
      default: 'gold', // gold, silver, ruby, emerald, sapphire, royal
      validator: (value) => ['gold', 'silver', 'ruby', 'emerald', 'sapphire', 'royal'].includes(value)
    },
    glow: {
      type: Boolean,
      default: false
    },
    sparkle: {
      type: Boolean,
      default: false
    },
    animated: {
      type: Boolean,
      default: false
    },
    rotate: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    iconClass() {
      return [
        `neo-baroque-icon--${this.size}`,
        `neo-baroque-icon--${this.variant}`,
        {
          'neo-baroque-icon--glow': this.glow,
          'neo-baroque-icon--sparkle': this.sparkle,
          'neo-baroque-icon--animated': this.animated,
          'neo-baroque-icon--rotate': this.rotate
        }
      ]
    }
  }
}
</script>

<style scoped>
.neo-baroque-icon {
  position: relative;
  display: inline-block;
  vertical-align: middle;
}

.icon-content {
  position: relative;
  display: block;
  text-align: center;
  line-height: 1;
}

.icon-symbol {
  position: relative;
  z-index: 2;
  display: block;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

/* Size Variations */
.neo-baroque-icon--small .icon-symbol {
  font-size: 1rem;
}

.neo-baroque-icon--medium .icon-symbol {
  font-size: 1.5rem;
}

.neo-baroque-icon--large .icon-symbol {
  font-size: 2rem;
}

.neo-baroque-icon--xlarge .icon-symbol {
  font-size: 2.5rem;
}

/* Color Variations */
.neo-baroque-icon--gold .icon-symbol {
  color: var(--primary-gold);
}

.neo-baroque-icon--silver .icon-symbol {
  color: var(--silver);
}

.neo-baroque-icon--ruby .icon-symbol {
  color: var(--ruby-red);
}

.neo-baroque-icon--emerald .icon-symbol {
  color: var(--emerald-green);
}

.neo-baroque-icon--sapphire .icon-symbol {
  color: var(--sapphire-blue);
}

.neo-baroque-icon--royal .icon-symbol {
  color: var(--royal-purple);
}

/* Glow Effect */
.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150%;
  height: 150%;
  background: radial-gradient(circle, currentColor 0%, transparent 70%);
  opacity: 0.6;
  border-radius: 50%;
  z-index: 1;
  filter: blur(8px);
}

.neo-baroque-icon--glow .icon-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.2); }
}

/* Sparkle Effect */
.icon-sparkle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 3;
  pointer-events: none;
}

.icon-sparkle::before,
.icon-sparkle::after {
  content: '✦';
  position: absolute;
  font-size: 0.5em;
  color: var(--primary-gold);
  opacity: 0;
  animation: sparkle 3s ease-in-out infinite;
}

.icon-sparkle::before {
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 0s;
}

.icon-sparkle::after {
  bottom: -10px;
  right: -10px;
  transform: rotate(45deg);
  animation-delay: 1.5s;
}

.neo-baroque-icon--sparkle .icon-sparkle::before,
.neo-baroque-icon--sparkle .icon-sparkle::after {
  opacity: 1;
}

@keyframes sparkle {
  0%, 100% { opacity: 0; transform: translateX(-50%) scale(0.5) rotate(0deg); }
  50% { opacity: 1; transform: translateX(-50%) scale(1) rotate(180deg); }
}

/* Animated Effect */
.neo-baroque-icon--animated {
  animation: icon-float 3s ease-in-out infinite;
}

@keyframes icon-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

/* Rotate Effect */
.neo-baroque-icon--rotate {
  animation: icon-rotate 4s linear infinite;
}

@keyframes icon-rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hover Effects */
.neo-baroque-icon:hover .icon-symbol {
  transform: scale(1.1);
  filter: brightness(1.2);
}

.neo-baroque-icon:hover .icon-glow {
  opacity: 0.8;
  transform: translate(-50%, -50%) scale(1.3);
}

/* Interactive Click Effect */
.neo-baroque-icon:active .icon-symbol {
  transform: scale(0.95);
}

/* Accessibility */
.neo-baroque-icon:focus {
  outline: 2px solid var(--primary-gold);
  outline-offset: 2px;
  border-radius: 50%;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .neo-baroque-icon--animated,
  .neo-baroque-icon--rotate,
  .icon-sparkle::before,
  .icon-sparkle::after {
    animation: none;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .icon-symbol {
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
  }

  .icon-glow {
    opacity: 0.8;
  }
}
</style>