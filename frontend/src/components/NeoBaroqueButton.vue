<template>
  <button
    :class="buttonClass"
    :disabled="disabled"
    @click="$emit('click')"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <span class="button-content">
      <span class="button-icon" v-if="icon">{{ icon }}</span>
      <span class="button-text">
        <slot>{{ text }}</slot>
      </span>
    </span>
    <span class="button-ornament left">❦</span>
    <span class="button-ornament right">❦</span>
    <div class="button-shine" v-if="isHovered"></div>
  </button>
</template>

<script>
export default {
  name: 'NeoBaroqueButton',
  props: {
    text: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'primary', // primary, secondary, accent, danger
      validator: (value) => ['primary', 'secondary', 'accent', 'danger'].includes(value)
    },
    icon: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  data() {
    return {
      isHovered: false
    }
  },
  computed: {
    buttonClass() {
      return [
        'neo-baroque-button',
        `neo-baroque-button--${this.variant}`,
        `neo-baroque-button--${this.size}`,
        { 'neo-baroque-button--disabled': this.disabled }
      ]
    }
  }
}
</script>

<style scoped>
.neo-baroque-button {
  position: relative;
  border: none;
  border-radius: var(--border-radius-ornate);
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: bold;
  font-family: var(--secondary-font);
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: var(--shadow-ornate);
  min-width: 120px;
}

.neo-baroque-button--primary {
  background: var(--gold-gradient);
  color: var(--deep-blue);
}

.neo-baroque-button--secondary {
  background: var(--purple-gradient);
  color: white;
}

.neo-baroque-button--accent {
  background: var(--blue-gradient);
  color: white;
}

.neo-baroque-button--danger {
  background: linear-gradient(135deg, #E0115F 0%, #FF1744 50%, #E0115F 100%);
  color: white;
}

.neo-baroque-button--small {
  padding: 10px 20px;
  font-size: 0.9rem;
  min-width: 100px;
}

.neo-baroque-button--medium {
  padding: 15px 30px;
  font-size: 1.1rem;
  min-width: 120px;
}

.neo-baroque-button--large {
  padding: 20px 40px;
  font-size: 1.3rem;
  min-width: 150px;
}

.neo-baroque-button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.neo-baroque-button:hover:not(.neo-baroque-button--disabled) {
  transform: translateY(-3px);
  box-shadow: var(--shadow-deep);
}

.neo-baroque-button:active:not(.neo-baroque-button--disabled) {
  transform: translateY(-1px);
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.button-icon {
  font-size: 1.2em;
}

.button-text {
  position: relative;
  z-index: 2;
}

.button-ornament {
  position: absolute;
  font-size: 1.5rem;
  opacity: 0.6;
  color: inherit;
  pointer-events: none;
  transition: all 0.3s ease;
}

.button-ornament.left {
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
}

.button-ornament.right {
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
}

.neo-baroque-button:hover .button-ornament {
  opacity: 1;
  transform: translateY(-50%) scale(1.2);
}

.button-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  transition: all 0.6s ease;
  pointer-events: none;
}

.neo-baroque-button:hover .button-shine {
  animation: shine 0.6s ease-in-out;
}

@keyframes shine {
  0% {
    transform: translateX(-100%) translateY(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) translateY(100%) rotate(45deg);
  }
}

/* Ripple Effect */
.neo-baroque-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.neo-baroque-button:active::before {
  width: 300px;
  height: 300px;
}

/* Focus State */
.neo-baroque-button:focus {
  outline: 3px solid rgba(212, 175, 55, 0.5);
  outline-offset: 2px;
}

/* Loading State */
.neo-baroque-button--loading {
  position: relative;
  color: transparent;
}

.neo-baroque-button--loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border: 2px solid currentColor;
  border-top: 2px solid transparent;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}
</style>