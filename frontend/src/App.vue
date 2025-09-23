<template>
  <div class="container">
    <NeoBaroqueDecorations />

    <NeoBaroqueHeader
      title="AI聊天助手"
      subtitle="✧ 预置不同系统提示词,确认不同聊天效果 ✧"
      :main-icon="'✦'"
      main-variant="gold"
      title-prefix-icon="❦"
      title-suffix-icon="❦"
      title-icon-variant="gold"
      variant="ornate"
      alignment="center"
    />

    <NeoBaroqueCard :title="'✧ 输入区域 ✧'" variant="elevated" padding="large">
      <NeoBaroquePromptSelector
        :available-prompts="availablePrompts"
        :selected-prompt="selectedPromptType"
        :disabled="isLoading"
        @select="onPromptSelect"
      />

      <textarea
        v-model="userInput"
        @input="onInputChange"
        placeholder="请输入您的问题或需求..."
        :disabled="isLoading"
      ></textarea>

      <div class="button-group">
        <NeoBaroqueButton
          :text="isLoading ? '生成中...' : '提交'"
          variant="primary"
          icon="✧"
          :disabled="isLoading || !userInput.trim()"
          @click="handleSubmit"
          size="large"
        />
        <!--NeoBaroqueButton
          text="加载测试文件"
          variant="secondary"
          icon="❅"
          :disabled="isLoading"
          @click="handleTestFile"
          size="large"
        /-->
      </div>
    </NeoBaroqueCard>
    
    <NeoBaroqueCard
      v-if="result || error"
      :title="'❦ 生成结果 ❦'"
      variant="elevated"
      padding="large"
      class="result-card"
    >
      <NeoBaroqueLoading
        v-if="isLoading"
        message="✧ 正在生成内容，请稍候 ✧"
        center-icon="✦"
        center-variant="gold"
        variant="inline"
        :orbit-radius="50"
      />

      <div v-if="error" class="error">
        <span class="error-icon">⚠</span>
        <p>{{ error }}</p>
      </div>

      <div v-if="result" class="result-content">
        <div v-if="result.format === 'markdown'" v-html="renderedMarkdown" class="markdown-content"></div>
        <div v-else-if="result.format === 'html'" v-html="result.content" class="html-content"></div>
        <div v-else class="text-content">{{ result.content }}</div>
      </div>
    </NeoBaroqueCard>
  </div>
</template>

<script>
import { marked } from 'marked'
import axios from 'axios'
import hljs from 'highlight.js'
import NeoBaroqueDecorations from './components/NeoBaroqueDecorations.vue'
import NeoBaroqueCard from './components/NeoBaroqueCard.vue'
import NeoBaroqueButton from './components/NeoBaroqueButton.vue'
import NeoBaroqueHeader from './components/NeoBaroqueHeader.vue'
import NeoBaroqueIcon from './components/NeoBaroqueIcon.vue'
import NeoBaroqueLoading from './components/NeoBaroqueLoading.vue'
import NeoBaroquePromptSelector from './components/NeoBaroquePromptSelector.vue'

// 创建自定义渲染器
const renderer = new marked.Renderer()

// 重写渲染方法以正确处理 SVG
renderer.image = function(href, title, text) {
  let out = `<img src="${href}" alt="${text}"`

  if (title) {
    out += ` title="${title}"`
  }

  return out
}

// 允许原始 HTML 通过
renderer.html = function(html) {
  return html
}


// 配置代码高亮
renderer.code = function({ text: code, lang: language }) {
  const lang = language || 'text'

  try {
    const highlighted = hljs.highlight(code, { language: lang }).value
    return `<pre><code class="hljs language-${lang}">${highlighted}</code></pre>`
  } catch (e) {
    // 如果高亮失败，返回原始代码
    return `<pre><code class="hljs">${escapeHtml(code)}</code></pre>`
  }
}

// HTML转义函数
function escapeHtml(html) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

// 配置 marked 以支持完整的 Markdown 语法（一次性配置，避免覆盖）
marked.setOptions({
  // GitHub Flavored Markdown
  gfm: true,           // 支持 GFM 语法（表格、删除线等）
  breaks: true,        // 自动转换换行符为 <br>
  headerIds: false,    // 不生成header id，避免重复和XSS
  mangle: false,       // 不修改内部属性，保持链接原样
  silent: true,        // 静默模式，减少控制台输出
  pedantic: false,     // 不严格模式，兼容更多语法
  sanitize: false,     // 不清理HTML，允许自定义标签
  smartLists: true,    // 智能列表，自动识别列表类型
  smartypants: false,  // 智能标点，保持原样
  xhtml: false,       // 不强制XHTML兼容
  renderer: renderer   // 自定义渲染器
})

export default {
  name: 'App',
  components: {
    NeoBaroqueDecorations,
    NeoBaroqueCard,
    NeoBaroqueButton,
    NeoBaroqueHeader,
    NeoBaroqueIcon,
    NeoBaroqueLoading,
    NeoBaroquePromptSelector
  },
  data() {
    return {
      userInput: '',
      selectedPromptType: '',
      result: null,
      error: null,
      isLoading: false,
      availablePrompts: [],
      inputTimeout: null
    }
  },
  computed: {
    renderedMarkdown() {
      if (!this.result || this.result.format !== 'markdown') return ''

      // 先处理所有被转义的 HTML 标签
      let content = this.result.content

      console.log('[Frontend] Original content:', content)

      // 智能HTML实体解码 - 只解码完整的SVG标签，避免干扰markdown语法
      // 1. 处理完整的SVG标签
      content = content.replace(/&lt;svg([^&]*?)&gt;([\s\S]*?)&lt;\/svg&gt;/g, (match, attrs, body) => {
        console.log('[Frontend] Found escaped SVG, restoring...')
        return `<svg${attrs}>${body}</svg>`
      })

      // 2. 处理独立的SVG标签（不包含在markdown语法中）
      content = content.replace(/&lt;(svg|path|circle|rect|g|text|title|desc)([^&]*?)&gt;/g, '<$1$2>')
      content = content.replace(/&lt;\/(svg|path|circle|rect|g|text|title|desc)&gt;/g, '</$1>')

      console.log('[Frontend] Content after HTML decoding:', content)

      // 使用 marked 处理
      const html = marked(content)

      console.log('[Frontend] HTML after marked:', html)

      // 后处理：确保 SVG 标签没有被再次转义
      const finalHtml = html.replace(/&lt;svg/g, '<svg').replace(/&lt;\/svg&gt;/g, '</svg>')
                           .replace(/&lt;path/g, '<path').replace(/&lt;\/path&gt;/g, '</path>')
                           .replace(/&lt;circle/g, '<circle').replace(/&lt;\/circle&gt;/g, '</circle>')
                           .replace(/&lt;rect/g, '<rect').replace(/&lt;\/rect&gt;/g, '</rect>')

      console.log('[Frontend] Final HTML:', finalHtml)

      return finalHtml
    }
  },
  methods: {
    async loadPrompts() {
      console.log('[Frontend] Loading prompts...')
      try {
        const response = await axios.get('/api/prompts')
        this.availablePrompts = response.data.prompts || []
        console.log('[Frontend] Prompts loaded successfully:', this.availablePrompts.length)
      } catch (err) {
        console.error('[Frontend] Failed to load prompts:', err)
      }
    },

    getPromptDisplayName(prompt) {
      const displayNames = {
        'learn_word': '📚 单词词源分析',
        'concept_svg': '🎨 禅意概念图解',
        'turmin_argumentative_structure': '🏛️ 图尔敏论证模型',
        'explain_math_concept': '🔢 数学概念原理解析',
        'sugeladi_talk': '🎭 苏格拉底对话',
        'first_principles': '⚡ 第一性原理分析',
        'project_architect': '🏗️ 数字架构师',
        'coding_mentor': '💻 编程概念导师',
        'creative_writer': '✍️ 创意写作大师',
        'logical_thinker': '🧠 逻辑思维训练'
      }
      return displayNames[prompt] || prompt
    },

    getPromptIcon(prompt) {
      const icons = {
        'learn_word': '📖',
        'concept_svg': '🎨',
        'turmin_argumentative_structure': '🏛️',
        'explain_math_concept': '🔢',
        'sugeladi_talk': '🎭',
        'first_principles': '⚡',
        'project_architect': '🏗️',
        'coding_mentor': '💻',
        'creative_writer': '✍️',
        'logical_thinker': '🧠'
      }
      return icons[prompt] || '✧'
    },

    getPromptDescription(prompt) {
      const descriptions = {
        'learn_word': '深度分析单词词源、词根词缀，建立记忆网络',
        'concept_svg': '用极简主义美学解释复杂概念，生成禅意SVG图',
        'turmin_argumentative_structure': '运用图尔敏模型分析论证结构，提升逻辑思维',
        'explain_math_concept': '挖掘数学概念的直觉起源，还原发现时的惊喜',
        'sugeladi_talk': '苏格拉底式对话，通过追问探寻问题的本质',
        'first_principles': '回归本质，从第一性原理重新思考问题',
        'project_architect': '设计完整的技术架构和项目实施路径',
        'coding_mentor': '用生动类比讲解编程概念，降低学习门槛',
        'creative_writer': '激发创作灵感，提供个性化写作指导',
        'logical_thinker': '运用逻辑框架分析问题，推导合理结论'
      }
      return descriptions[prompt] || '专业的AI助手'
    },

    async handleTestFile() {
      console.log('[Frontend] Loading test file...')
      this.isLoading = true
      this.error = null
      this.result = null

      try {
        const requestData = {
          input: 'test',  // 必需字段，但会被忽略
          use_test_file: true
        }

        const response = await axios.post('/api/generate', requestData)
        console.log('[Frontend] Test file loaded successfully - format:', response.data.format, 'source:', response.data.source)
        this.result = response.data
      } catch (err) {
        const error = err.response?.data?.error || err.message || '加载测试文件失败，请重试'
        this.error = error
        console.error('[Frontend] Test file loading error:', err)
      } finally {
        this.isLoading = false
      }
    },

    async handleSubmit() {
      if (!this.userInput.trim()) return

      console.log('[Frontend] Submitting request - prompt type:', this.selectedPromptType)
      this.isLoading = true
      this.error = null
      this.result = null

      try {
        const requestData = {
          input: this.userInput.trim()
        }

        if (this.selectedPromptType) {
          requestData.prompt_type = this.selectedPromptType
        }

        const response = await axios.post('/api/generate', requestData)
        console.log('[Frontend] Request successful - format:', response.data.format, 'original_format:', response.data.original_format)
        this.result = response.data

        // If HTML content was saved (either converted from Markdown or original HTML), navigate to display page
        if (response.data.html_file_info) {
          console.log('[Frontend] HTML content saved, navigating to display page')
          const file_id = response.data.html_file_info.file_id
          // Navigate to HTML display page
          window.open(`/html/${file_id}`, '_blank')
        }
      } catch (err) {
        const error = err.response?.data?.error || err.message || '生成失败，请重试'
        this.error = error
        console.error('[Frontend] API Error:', err)
      } finally {
        this.isLoading = false
      }
    },

    onPromptSelect(promptValue) {
      this.selectedPromptType = promptValue
      console.log('[Frontend] Prompt type changed to:', this.selectedPromptType)
    },

    onInputChange() {
      // Debounce input logging to avoid too many logs
      if (this.inputTimeout) {
        clearTimeout(this.inputTimeout)
      }
      this.inputTimeout = setTimeout(() => {
        console.log('[Frontend] Input changed - length:', this.userInput.length)
      }, 500)
    }
  },

  mounted() {
    console.log('[Frontend] Application mounted')
    this.loadPrompts()
  }
}
</script>

<style>
@import './neo-baroque.css';

.result-card {
  animation: fadeIn 0.8s ease-out;
  margin-top: 30px;
}

.prompt-selector label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-weight: bold;
  color: var(--deep-blue);
  font-size: 1.1rem;
}


.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--primary-gold);
  border-top: 3px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.error-icon {
  font-size: 2rem;
  margin-right: 10px;
  color: var(--ruby-red);
}

.error p {
  margin: 0;
  font-weight: bold;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
