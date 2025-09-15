<template>
  <div class="html-display">
    <div class="header">
      <h1>HTML 内容展示</h1>
      <button class="back-btn" @click="goBack">返回主页</button>
    </div>

    <div class="content-container">
      <div class="html-content" v-if="htmlContent" v-html="htmlContent"></div>
      <div v-if="loading" class="loading">
        正在加载 HTML 内容...
      </div>
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>

    <div class="metadata" v-if="metadata">
      <h3>文件信息</h3>
      <p><strong>文件名:</strong> {{ metadata.filename }}</p>
      <p><strong>提示词类型:</strong> {{ metadata.prompt_type || '默认' }}</p>
      <p><strong>创建时间:</strong> {{ formatTime(metadata.created_at) }}</p>
      <p><strong>内容长度:</strong> {{ metadata.content_length }} 字符</p>
      <p v-if="metadata.original_input"><strong>原始输入:</strong> {{ metadata.original_input }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HtmlDisplay',
  data() {
    return {
      htmlContent: null,
      metadata: null,
      loading: true,
      error: null
    }
  },
  computed: {
    fileId() {
      return this.$route.params.fileId
    }
  },
  methods: {
    async loadHtmlContent() {
      console.log('[HtmlDisplay] Loading HTML content for file:', this.fileId)

      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`/api/html/files/${this.fileId}`)
        this.htmlContent = response.data.content
        this.metadata = response.data.metadata
        console.log('[HtmlDisplay] HTML content loaded successfully')
      } catch (err) {
        this.error = err.response?.data?.error || '加载 HTML 内容失败'
        console.error('[HtmlDisplay] Error loading HTML content:', err)
      } finally {
        this.loading = false
      }
    },

    formatTime(timeString) {
      return new Date(timeString).toLocaleString('zh-CN')
    },

    goBack() {
      this.$router.push('/')
    }
  },
  mounted() {
    this.loadHtmlContent()
  },
  watch: {
    '$route.params.fileId'() {
      this.loadHtmlContent()
    }
  }
}
</script>

<style scoped>
.html-display {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.header h1 {
  color: #2c3e50;
  margin: 0;
}

.back-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.back-btn:hover {
  background: #2980b9;
}

.content-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 30px;
  min-height: 400px;
}

.html-content {
  padding: 30px;
  line-height: 1.6;
}

.html-content :deep(h1), .html-content :deep(h2), .html-content :deep(h3) {
  color: #2c3e50;
  margin-top: 30px;
  margin-bottom: 15px;
}

.html-content :deep(p) {
  margin-bottom: 15px;
}

.html-content :deep(ul), .html-content :deep(ol) {
  margin-bottom: 15px;
  padding-left: 30px;
}

.html-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
}

.html-content :deep(th), .html-content :deep(td) {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.html-content :deep(th) {
  background-color: #f2f2f2;
}

.html-content :deep(code) {
  background-color: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

.html-content :deep(pre) {
  background-color: #f4f4f4;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  margin-bottom: 15px;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #666;
  font-size: 16px;
}

.error {
  text-align: center;
  padding: 50px;
  color: #e74c3c;
  font-size: 16px;
}

.metadata {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 30px;
}

.metadata h3 {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 15px;
}

.metadata p {
  margin-bottom: 8px;
  color: #555;
}

.metadata strong {
  color: #2c3e50;
}
</style>