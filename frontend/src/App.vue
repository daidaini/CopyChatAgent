<template>
  <div class="container">
    <h1>AI Chat Assistant</h1>
    
    <div class="input-section">
      <div class="prompt-selector">
        <label for="prompt-type">提示词类型：</label>
        <select
          id="prompt-type"
          v-model="selectedPromptType"
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
      availablePrompts: []
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
      try {
        const response = await axios.get('/api/prompts')
        this.availablePrompts = response.data.prompts || []
      } catch (err) {
        console.error('Failed to load prompts:', err)
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

        this.result = response.data
      } catch (err) {
        this.error = err.response?.data?.error || err.message || '生成失败，请重试'
        console.error('API Error:', err)
      } finally {
        this.isLoading = false
      }
    }
  },

  mounted() {
    this.loadPrompts()
  }
}
</script>