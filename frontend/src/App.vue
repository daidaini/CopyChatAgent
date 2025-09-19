<template>
  <div class="container">
    <h1>提示词创意验证</h1>
    
    <div class="input-section">
      <div class="prompt-selector">
        <label for="prompt-type">提示词类型：</label>
        <select
          id="prompt-type"
          v-model="selectedPromptType"
          @change="onPromptTypeChange"
          :disabled="isLoading"
        >
          <option value=""></option>
          <option v-for="prompt in availablePrompts" :key="prompt" :value="prompt">
            {{ getPromptDisplayName(prompt) }}
          </option>
        </select>
      </div>

      <textarea
        v-model="userInput"
        @input="onInputChange"
        placeholder="请输入您的问题或需求..."
        :disabled="isLoading"
      ></textarea>
      <div class="button-group">
        <button
          class="submit-btn"
          @click="handleSubmit"
          :disabled="isLoading || !userInput.trim()"
        >
          {{ isLoading ? '生成中...' : '提交' }}
        </button>
        <button
          class="test-btn"
          @click="handleTestFile"
          :disabled="isLoading"
        >
          加载测试文件
        </button>
      </div>
    </div>
    
    <div class="result-section" v-if="result || error">
      <div v-if="isLoading" class="loading">
        正在生成内容，请稍候...
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-if="result" class="result-content">
        <div v-if="result.format === 'markdown'" v-html="renderedMarkdown" class="markdown-content"></div>
        <div v-else-if="result.format === 'html'" v-html="result.content" class="html-content"></div>
        <div v-else class="text-content">{{ result.content }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import axios from 'axios'
import hljs from 'highlight.js'

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
        'learn_word': '单词学习帮手',
        'concept_svg': '禅意图形解释概念',
        'turmin_argumentative_structure': '图尔敏式论证',
        'explain_math_concept' : '简单理解数学概念',
        'word_memory_card': '生成单词记忆卡片'
      }
      return displayNames[prompt] || prompt
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

    onPromptTypeChange() {
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
