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
      <button
        class="submit-btn"
        @click="handleSubmit"
        :disabled="isLoading || !userInput.trim()"
      >
        {{ isLoading ? '生成中...' : '提交' }}
      </button>
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

// 配置 marked 以支持 SVG 和 HTML 标签
marked.setOptions({
  gfm: true,
  breaks: true,
  headerIds: false,
  mangle: false,  // 不要修改内部属性
  silent: true
})

// 创建自定义渲染器
const renderer = new marked.Renderer()

// 重写渲染方法以正确处理 SVG
renderer.image = function(href, title, text) {
  let out = `<img src="${href}" alt="${text}"`

  if (title) {
    out += ` title="${title}"`
  }

  // SVG 特殊处理
  if (href.endsWith('.svg')) {
    out += ` class="svg-image" style="max-width: 100%; height: auto;"`
  }

  out += '>'
  return out
}

// 允许原始 HTML 通过
renderer.html = function(html) {
  return html
}

// 重写列表渲染以避免转义
renderer.list = function(body, ordered, start) {
  const type = ordered ? 'ol' : 'ul'
  const startatt = (ordered && start !== 1) ? (` start="${start}"`) : ''
  return `<${type}${startatt}>\n${body}</${type}>\n`
}

renderer.listitem = function(text) {
  return `<li>${text}</li>\n`
}

marked.setOptions({ renderer })

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

      // 解码 HTML 实体，特别是 SVG 标签
      content = content.replace(/&lt;svg([^&]*?)&gt;([\s\S]*?)&lt;\/svg&gt;/g, (match, attrs, body) => {
        console.log('[Frontend] Found escaped SVG, restoring...')
        return `<svg${attrs}>${body}</svg>`
      })

      // 处理其他常见的 HTML 标签
      content = content.replace(/&lt;([^&]+?)&gt;/g, '<$1>')
      content = content.replace(/&lt;\/([^&]+?)&gt;/g, '</$1>')

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
        'learn_word': '单词学习助手',
        'concept_svg': '结合svg解释概念',
        'turmin_argumentative_structure': '图尔敏论证结构'
      }
      return displayNames[prompt] || prompt
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