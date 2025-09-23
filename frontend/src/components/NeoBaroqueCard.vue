<template>
  <div class="neo-baroque-card" :class="cardClass">
    <div class="card-header" v-if="$slots.header || title">
      <slot name="header">
        <h3>{{ title }}</h3>
      </slot>
    </div>

    <div class="card-body">
      <slot></slot>
    </div>

    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>

    <!-- Decorative Elements -->
    <div class="card-corner top-left"></div>
    <div class="card-corner top-right"></div>
    <div class="card-corner bottom-left"></div>
    <div class="card-corner bottom-right"></div>

    <div class="card-ornament left"></div>
    <div class="card-ornament right"></div>
  </div>
</template>

<script>
export default {
  name: 'NeoBaroqueCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'default', // default, elevated, outlined
      validator: (value) => ['default', 'elevated', 'outlined'].includes(value)
    },
    padding: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    cardClass() {
      return [
        `neo-baroque-card--${this.variant}`,
        `neo-baroque-card--padding-${this.padding}`
      ]
    }
  }
}
</script>

<style scoped>
.neo-baroque-card {
  position: relative;
  background: rgba(255, 255, 255, 0.9);
  border-radius: var(--border-radius-ornate);
  overflow: hidden;
  transition: all 0.3s ease;
  border: var(--border-silver);
}

.neo-baroque-card--default {
  box-shadow: var(--shadow-ornate);
}

.neo-baroque-card--elevated {
  box-shadow: var(--shadow-deep);
}

.neo-baroque-card--outlined {
  border: var(--border-gold);
  box-shadow: none;
}

.neo-baroque-card--padding-small {
  padding: 15px;
}

.neo-baroque-card--padding-medium {
  padding: 25px;
}

.neo-baroque-card--padding-large {
  padding: 35px;
}

.neo-baroque-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-deep);
}

.card-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  position: relative;
}

.card-header h3 {
  margin: 0;
  color: var(--deep-blue);
  font-size: 1.5rem;
  font-family: var(--secondary-font);
  position: relative;
  padding-left: 20px;
}

.card-header h3::before {
  content: '✦';
  position: absolute;
  left: 0;
  color: var(--primary-gold);
  font-size: 1.2rem;
}

.card-body {
  color: var(--charcoal);
  line-height: 1.6;
}

.card-footer {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid rgba(212, 175, 55, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

/* Card Corners */
.card-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 2px solid var(--primary-gold);
  opacity: 0.6;
}

.card-corner.top-left {
  top: 10px;
  left: 10px;
  border-right: none;
  border-bottom: none;
  border-radius: var(--border-radius-ornate) 0 0 0;
}

.card-corner.top-right {
  top: 10px;
  right: 10px;
  border-left: none;
  border-bottom: none;
  border-radius: 0 var(--border-radius-ornate) 0 0;
}

.card-corner.bottom-left {
  bottom: 10px;
  left: 10px;
  border-right: none;
  border-top: none;
  border-radius: 0 0 0 var(--border-radius-ornate);
}

.card-corner.bottom-right {
  bottom: 10px;
  right: 10px;
  border-left: none;
  border-top: none;
  border-radius: 0 0 var(--border-radius-ornate) 0;
}

/* Side Ornaments */
.card-ornament {
  position: absolute;
  width: 2px;
  height: 40px;
  background: var(--gold-gradient);
  opacity: 0.4;
}

.card-ornament.left {
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.card-ornament.right {
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

/* Hover Effects */
.neo-baroque-card:hover .card-corner {
  opacity: 1;
  transform: scale(1.1);
}

.neo-baroque-card:hover .card-ornament {
  opacity: 0.6;
  height: 50px;
}

/* Responsive */
@media (max-width: 768px) {
  .neo-baroque-card {
    margin: 10px;
  }

  .card-corner {
    width: 20px;
    height: 20px;
  }

  .card-ornament {
    height: 30px;
  }
}
</style>