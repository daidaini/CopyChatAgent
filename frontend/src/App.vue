<template>
  <div class="container">
    <h1>AI Chat Assistant</h1>
    
    <div class="input-section">
      <div class="prompt-selector">
        <label for="prompt-type">提示词类型：</label>
        <select
          id="prompt-type"
          v-model="selectedPromptType"
          @change="onPromptTypeChange"
          :disabled="isLoading"
        >
          <option value="">默认助手</option>
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
        <div v-if="result.format === 'markdown'" v-html="renderedMarkdown"></div>
        <div v-else-if="result.format === 'html'" v-html="result.content"></div>
        <div v-else>{{ result.content }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import axios from 'axios'

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
      return marked(this.result.content)
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
        'learn_word': '单词学习助手'
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
        console.log('[Frontend] Request successful - format:', response.data.format)
        this.result = response.data
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