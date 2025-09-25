<template>
  <div class="quant-strategy-generator">
    <NeoBaroqueCard :title="'📈 量化交易策略生成器'" variant="elevated" padding="large">
      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">🎯</span>
          策略需求描述
        </label>
        <textarea
          v-model="strategyInput"
          @input="onInputChange"
          placeholder="请详细描述您希望生成的量化交易策略，例如：基于MACD和RSI的双均线策略、机器学习驱动的趋势跟踪策略等..."
          :disabled="isLoading"
          class="strategy-textarea"
          rows="6"
        ></textarea>
      </div>

      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">📚</span>
          知识库选择
        </label>
        <select
          v-model="selectedKnowledgeBase"
          :disabled="isLoading || knowledgeBases.length === 0"
          class="knowledge-base-select"
        >
          <option value="">默认知识库</option>
          <option
            v-for="kb in knowledgeBases"
            :key="kb.id"
            :value="kb.id"
          >
            {{ kb.name }}
          </option>
        </select>
      </div>

      <div class="button-group">
        <NeoBaroqueButton
          :text="isLoading ? '生成中...' : '生成量化策略'"
          variant="primary"
          icon="📊"
          :disabled="isLoading || !strategyInput.trim()"
          @click="generateStrategy"
          size="large"
        />
        <NeoBaroqueButton
          text="清空"
          variant="secondary"
          icon="🗑️"
          :disabled="isLoading"
          @click="clearForm"
          size="large"
        />
      </div>
    </NeoBaroqueCard>

    <NeoBaroqueCard
      v-if="strategyResult || error"
      :title="'📋 生成的策略代码'"
      variant="elevated"
      padding="large"
      class="result-card"
    >
      <NeoBaroqueLoading
        v-if="isLoading"
        message="✧ 正在生成量化策略，请稍候 ✧"
        center-icon="📊"
        center-variant="gold"
        variant="inline"
        :orbit-radius="50"
      />

      <div v-if="error" class="error">
        <span class="error-icon">⚠</span>
        <p>{{ error }}</p>
      </div>

      <div v-if="strategyResult" class="strategy-result">
        <div class="strategy-meta">
          <div class="meta-item">
            <span class="meta-label">知识库:</span>
            <span class="meta-value">{{ strategyResult.knowledge_base_used || '默认' }}</span>
          </div>
          <div class="meta-item" v-if="strategyResult.implementation_steps">
            <span class="meta-label">实现步骤:</span>
            <span class="meta-value">{{ strategyResult.implementation_steps.substring(0, 100) }}...</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">生成时间:</span>
            <span class="meta-value">{{ new Date().toLocaleString() }}</span>
          </div>
        </div>

        <div v-html="renderedStrategyCode" class="strategy-code"></div>

        <div class="action-buttons">
          <NeoBaroqueButton
            text="复制代码"
            variant="secondary"
            icon="📋"
            @click="copyToClipboard"
            size="small"
          />
          <NeoBaroqueButton
            text="下载代码"
            variant="secondary"
            icon="💾"
            :disabled="isDownloading"
            @click="downloadCode"
            size="small"
          />
        </div>
      </div>
    </NeoBaroqueCard>
  </div>

  <!-- 增强加载组件 -->
  <EnhancedLoading
    v-if="showEnhancedLoading"
    :title="'正在生成量化策略'"
    :message="'AI正在分析您的需求并生成专业策略，请耐心等待...'"
    :center-icon="'📊'"
    :fullscreen="true"
    :show-cancel="true"
    :show-progress="true"
    :progress="Math.round(loadingProgress)"
    :estimated-time="120"
    :show-time="true"
    :tips="strategyTips"
    @cancel="cancelRequest"
  />
</template>

<script>
import { marked } from 'marked'
import { quantApi } from '../utils/axiosConfig'
import hljs from 'highlight.js'
import NeoBaroqueCard from './NeoBaroqueCard.vue'
import NeoBaroqueButton from './NeoBaroqueButton.vue'
import NeoBaroqueLoading from './NeoBaroqueLoading.vue'
import EnhancedLoading from './EnhancedLoading.vue'

// 配置代码高亮
function setupCodeHighlighting() {
  const renderer = new marked.Renderer()

  renderer.code = function({ text: code, lang: language }) {
    const lang = language || 'python'

    try {
      const highlighted = hljs.highlight(code, { language: lang }).value
      return `<pre><code class="hljs language-${lang}">${highlighted}</code></pre>`
    } catch (e) {
      return `<pre><code class="hljs">${escapeHtml(code)}</code></pre>`
    }
  }

  marked.setOptions({
    gfm: true,
    breaks: true,
    headerIds: false,
    renderer: renderer
  })
}

function escapeHtml(html) {
  if (!html) return ''
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

export default {
  name: 'QuantStrategyGenerator',
  components: {
    NeoBaroqueCard,
    NeoBaroqueButton,
    NeoBaroqueLoading,
    EnhancedLoading
  },
  data() {
    return {
      strategyInput: '',
      selectedKnowledgeBase: '',
      strategyResult: null,
      error: null,
      isLoading: false,
      knowledgeBases: [],
      inputTimeout: null,
      showEnhancedLoading: false,
      loadingProgress: 0,
      isDownloading: false, // 防止重复下载
      strategyTips: [
        '量化策略需要详细的参数设置才能获得好的回测结果',
        '建议包含止损、止盈等风险管理措施',
        '不同的市场环境可能需要不同的策略参数',
        '回测时请考虑交易成本和滑点的影响',
        '建议在实盘交易前进行充分的回测验证'
      ]
    }
  },
  computed: {
    renderedStrategyCode() {
      if (!this.strategyResult || !this.strategyResult.content) return ''

      // 直接返回格式化的代码内容，不使用markdown渲染
      return `<pre><code>${escapeHtml(this.strategyResult.content)}</code></pre>`
    }
  },
  methods: {
    async loadKnowledgeBases() {
      try {
        const response = await quantApi.getKnowledgeBases()
        this.knowledgeBases = response.data.knowledge_bases || []
        console.log('[QuantStrategy] Knowledge bases loaded:', this.knowledgeBases.length)
      } catch (err) {
        console.error('[QuantStrategy] Failed to load knowledge bases:', err)
      }
    },

    async generateStrategy() {
      if (!this.strategyInput.trim()) return

      console.log('[QuantStrategy] Generating strategy...')
      this.isLoading = true
      this.showEnhancedLoading = true
      this.error = null
      this.strategyResult = null
      this.loadingProgress = 0

      // 模拟进度更新
      const progressInterval = setInterval(() => {
        if (this.loadingProgress < 90) {
          this.loadingProgress += Math.random() * 10
        }
      }, 2000)

      try {
        const requestData = {
          prompt: this.strategyInput.trim()
        }

        if (this.selectedKnowledgeBase) {
          requestData.knowledge_base_name = this.knowledgeBases.find(kb => kb.id === this.selectedKnowledgeBase)?.name
        }

        const response = await quantApi.generateStrategy(requestData)
        console.log('[QuantStrategy] Strategy generated successfully')
        this.strategyResult = response.data
        this.loadingProgress = 100
      } catch (err) {
        const error = err.response?.data?.error || err.message || '生成策略失败，请重试'
        this.error = error
        console.error('[QuantStrategy] API Error:', err)

        // 特殊处理超时错误
        if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
          this.error = '策略生成超时，可能因为请求过于复杂，请简化需求或稍后重试'
        }
      } finally {
        clearInterval(progressInterval)
        this.isLoading = false
        this.showEnhancedLoading = false
      }
    },

    clearForm() {
      this.strategyInput = ''
      this.selectedKnowledgeBase = ''
      this.strategyResult = null
      this.error = null
    },

    cancelRequest() {
      console.log('[QuantStrategy] Request cancelled by user')
      this.showEnhancedLoading = false
      this.isLoading = false
      this.error = '用户取消了请求'
    },

    async copyToClipboard() {
      if (!this.strategyResult?.content) return

      try {
        await navigator.clipboard.writeText(this.strategyResult.content)
        alert('代码已复制到剪贴板')
      } catch (err) {
        console.error('[QuantStrategy] Copy to clipboard failed:', err)
        alert('复制失败，请手动复制')
      }
    },

    downloadCode() {
      if (!this.strategyResult?.content || this.isDownloading) return

      this.isDownloading = true

      try {
        const blob = new Blob([this.strategyResult.content], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `quant_strategy_${new Date().getTime()}.py`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)

        // 添加下载成功的提示
        console.log('[QuantStrategy] Code downloaded successfully')
      } catch (error) {
        console.error('[QuantStrategy] Download error:', error)
        alert('下载失败，请重试')
      } finally {
        // 重置下载状态
        setTimeout(() => {
          this.isDownloading = false
        }, 1000)
      }
    },

    onInputChange() {
      if (this.inputTimeout) {
        clearTimeout(this.inputTimeout)
      }
      this.inputTimeout = setTimeout(() => {
        console.log('[QuantStrategy] Input changed - length:', this.strategyInput.length)
      }, 500)
    }
  },
  mounted() {
    setupCodeHighlighting()
    this.loadKnowledgeBases()
    console.log('[QuantStrategy] Component mounted')
  }
}
</script>

<style scoped>
.quant-strategy-generator {
  max-width: 1200px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  font-weight: bold;
  color: var(--deep-blue);
  font-size: 1.1rem;
}

.label-icon {
  font-size: 1.3rem;
}

.strategy-textarea {
  width: 100%;
  padding: 15px;
  border: 2px solid var(--light-gray);
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

.strategy-textarea:focus {
  outline: none;
  border-color: var(--primary-gold);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.knowledge-base-select {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid var(--light-gray);
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.3s ease;
}

.knowledge-base-select:focus {
  outline: none;
  border-color: var(--primary-gold);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.button-group {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.result-card {
  animation: fadeIn 0.8s ease-out;
  margin-top: 30px;
}

.strategy-result {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--light-gray);
}

.strategy-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(0, 123, 255, 0.05);
  border-radius: 8px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.meta-label {
  font-weight: bold;
  color: var(--deep-blue);
  font-size: 0.9rem;
}

.meta-value {
  color: var(--text-color);
  font-size: 0.9rem;
  word-break: break-word;
}

.strategy-code {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  border: 1px solid #e9ecef;
  overflow-x: auto;
}

.strategy-code :deep(pre) {
  margin: 0;
  background: transparent;
  padding: 0;
}

.strategy-code :deep(code) {
  background: transparent;
  padding: 0;
  font-size: 0.9rem;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
  }

  .strategy-meta {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>