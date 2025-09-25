<template>
  <div class="enhanced-loading" :class="{ 'fullscreen': fullscreen }">
    <div class="loading-backdrop" @click="$emit('cancel')"></div>

    <div class="loading-content">
      <!-- 主要加载动画 -->
      <div class="loading-animation">
        <div class="orbit-container">
          <div class="orbit">
            <div class="planet"></div>
          </div>
          <div class="orbit">
            <div class="planet"></div>
          </div>
          <div class="orbit">
            <div class="planet"></div>
          </div>
          <div class="center-star">
            <span class="star-icon">{{ centerIcon }}</span>
          </div>
        </div>
      </div>

      <!-- 加载信息 -->
      <div class="loading-info">
        <h3 class="loading-title">{{ title }}</h3>
        <p class="loading-message">{{ message }}</p>

        <!-- 进度信息 -->
        <div v-if="showProgress" class="progress-section">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: progress + '%' }"
              :class="{ 'progress-animated': !progress }"
            ></div>
          </div>
          <span class="progress-text">{{ progressText }}</span>
        </div>

        <!-- 时间信息 -->
        <div v-if="showTime" class="time-info">
          <span class="elapsed-time">已用时: {{ formatTime(elapsedTime) }}</span>
          <span v-if="estimatedTime" class="estimated-time">预计: {{ formatTime(estimatedTime) }}</span>
        </div>

        <!-- 提示信息 -->
        <div v-if="tips.length > 0" class="loading-tips">
          <span class="tip-icon">💡</span>
          <span class="tip-text">{{ currentTip }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div v-if="showCancel" class="loading-actions">
        <NeoBaroqueButton
          text="取消"
          variant="secondary"
          icon="✕"
          @click="$emit('cancel')"
          size="medium"
        />
      </div>
    </div>
  </div>
</template>

<script>
import NeoBaroqueButton from './NeoBaroqueButton.vue'

export default {
  name: 'EnhancedLoading',
  components: {
    NeoBaroqueButton
  },
  props: {
    title: {
      type: String,
      default: '正在处理'
    },
    message: {
      type: String,
      default: '请稍候...'
    },
    centerIcon: {
      type: String,
      default: '✦'
    },
    fullscreen: {
      type: Boolean,
      default: false
    },
    showCancel: {
      type: Boolean,
      default: false
    },
    showProgress: {
      type: Boolean,
      default: false
    },
    progress: {
      type: Number,
      default: 0
    },
    estimatedTime: {
      type: Number,
      default: null
    },
    showTime: {
      type: Boolean,
      default: true
    },
    tips: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      elapsedTime: 0,
      currentTipIndex: 0,
      timer: null,
      tipTimer: null
    }
  },
  computed: {
    progressText() {
      if (this.progress > 0) {
        return `${this.progress}%`
      }
      return '处理中...'
    },
    currentTip() {
      return this.tips[this.currentTipIndex] || ''
    }
  },
  methods: {
    formatTime(seconds) {
      if (seconds < 60) {
        return `${seconds}秒`
      } else if (seconds < 3600) {
        return `${Math.floor(seconds / 60)}分${seconds % 60}秒`
      } else {
        return `${Math.floor(seconds / 3600)}小时${Math.floor((seconds % 3600) / 60)}分`
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.elapsedTime++
      }, 1000)
    },
    startTipRotation() {
      if (this.tips.length > 1) {
        this.tipTimer = setInterval(() => {
          this.currentTipIndex = (this.currentTipIndex + 1) % this.tips.length
        }, 5000)
      }
    },
    stopTimers() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
      if (this.tipTimer) {
        clearInterval(this.tipTimer)
        this.tipTimer = null
      }
    }
  },
  mounted() {
    if (this.showTime) {
      this.startTimer()
    }
    this.startTipRotation()
  },
  beforeUnmount() {
    this.stopTimers()
  }
}
</script>

<style scoped>
.enhanced-loading {
  position: relative;
  z-index: 9999;
}

.loading-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.fullscreen .loading-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.loading-content {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 2px solid var(--primary-gold);
  max-width: 500px;
  width: 90%;
  text-align: center;
}

.loading-animation {
  margin-bottom: 30px;
}

.orbit-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.orbit {
  position: absolute;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.orbit:nth-child(1) {
  width: 120px;
  height: 120px;
  animation: rotate 4s linear infinite;
}

.orbit:nth-child(2) {
  width: 90px;
  height: 90px;
  animation: rotate 3s linear infinite reverse;
}

.orbit:nth-child(3) {
  width: 60px;
  height: 60px;
  animation: rotate 2s linear infinite;
}

.planet {
  position: absolute;
  width: 8px;
  height: 8px;
  background: var(--primary-gold);
  border-radius: 50%;
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

.center-star {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.star-icon {
  font-size: 2rem;
  animation: pulse 2s ease-in-out infinite;
}

.loading-info {
  margin-bottom: 30px;
}

.loading-title {
  color: var(--deep-blue);
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.loading-message {
  color: var(--text-color);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.progress-section {
  margin: 20px 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-gold), #ffd700);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-animated {
  background: linear-gradient(90deg, var(--primary-gold), #ffd700, var(--primary-gold));
  background-size: 200% 100%;
  animation: shimmer 2s ease-in-out infinite;
}

.progress-text {
  font-size: 0.9rem;
  color: #666;
}

.time-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 20px;
}

.elapsed-time, .estimated-time {
  background: rgba(0, 123, 255, 0.1);
  padding: 5px 10px;
  border-radius: 15px;
}

.loading-tips {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  background: rgba(255, 215, 0, 0.1);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.tip-icon {
  font-size: 1.2rem;
}

.tip-text {
  color: #666;
  font-style: italic;
}

.loading-actions {
  display: flex;
  justify-content: center;
}

@keyframes rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@media (max-width: 768px) {
  .loading-content {
    padding: 30px 20px;
    margin: 20px;
  }

  .time-info {
    flex-direction: column;
    gap: 10px;
  }

  .loading-tips {
    flex-direction: column;
    text-align: center;
  }
}
</style>