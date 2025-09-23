<template>
  <div class="neo-baroque-decorations">
    <!-- Corner Ornaments -->
    <div class="corner-ornament top-left"></div>
    <div class="corner-ornament top-right"></div>
    <div class="corner-ornament bottom-left"></div>
    <div class="corner-ornament bottom-right"></div>

    <!-- Side Borders -->
    <div class="side-border left"></div>
    <div class="side-border right"></div>

    <!-- Floating Decorative Elements -->
    <div class="floating-element" style="top: 10%; left: 5%;">❦</div>
    <div class="floating-element" style="top: 20%; right: 8%;">❅</div>
    <div class="floating-element" style="bottom: 15%; left: 12%;">✧</div>
    <div class="floating-element" style="bottom: 25%; right: 15%;">❈</div>

    <!-- Animated Particles -->
    <div class="particle" v-for="i in 20" :key="i" :style="getParticleStyle(i)"></div>
  </div>
</template>

<script>
export default {
  name: 'NeoBaroqueDecorations',
  methods: {
    getParticleStyle(index) {
      const size = Math.random() * 4 + 2;
      const duration = Math.random() * 20 + 10;
      const delay = Math.random() * 5;
      const startX = Math.random() * 100;
      const startY = Math.random() * 100;

      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${startX}%`,
        top: `${startY}%`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`,
      };
    }
  }
}
</script>

<style scoped>
.neo-baroque-decorations {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

/* Corner Ornaments */
.corner-ornament {
  position: absolute;
  width: 80px;
  height: 80px;
  border: 3px solid var(--primary-gold);
  opacity: 0.6;
}

.corner-ornament.top-left {
  top: 20px;
  left: 20px;
  border-right: none;
  border-bottom: none;
  border-radius: var(--border-radius-ornate) 0 0 0;
}

.corner-ornament.top-right {
  top: 20px;
  right: 20px;
  border-left: none;
  border-bottom: none;
  border-radius: 0 var(--border-radius-ornate) 0 0;
}

.corner-ornament.bottom-left {
  bottom: 20px;
  left: 20px;
  border-right: none;
  border-top: none;
  border-radius: 0 0 0 var(--border-radius-ornate);
}

.corner-ornament.bottom-right {
  bottom: 20px;
  right: 20px;
  border-left: none;
  border-top: none;
  border-radius: 0 0 var(--border-radius-ornate) 0;
}

/* Side Borders */
.side-border {
  position: absolute;
  width: 2px;
  height: 100px;
  background: var(--gold-gradient);
  opacity: 0.4;
}

.side-border.left {
  left: 50px;
  top: 50%;
  transform: translateY(-50%);
}

.side-border.right {
  right: 50px;
  top: 50%;
  transform: translateY(-50%);
}

/* Floating Elements */
.floating-element {
  position: absolute;
  font-size: 2rem;
  color: var(--primary-gold);
  opacity: 0.3;
  animation: float 6s ease-in-out infinite;
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

/* Animated Particles */
.particle {
  position: absolute;
  background: var(--primary-gold);
  border-radius: 50%;
  opacity: 0.6;
  animation: drift linear infinite;
}

@keyframes drift {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100vh) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .corner-ornament {
    width: 60px;
    height: 60px;
  }

  .floating-element {
    font-size: 1.5rem;
  }

  .side-border {
    height: 60px;
  }
}
</style>