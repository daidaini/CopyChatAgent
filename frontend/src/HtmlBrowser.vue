<template>
  <div class="html-browser">
    <div class="header">
      <h1>❅ HTML 文件浏览器 ❅</h1>
      <div class="actions">
        <button class="refresh-btn" @click="loadFiles" :disabled="loading">
          ✧ 刷新 ✧
        </button>
        <button class="back-btn" @click="goBack">
          ✧ 返回主页 ✧
        </button>
      </div>
    </div>

    <div class="content">
      <div v-if="loading" class="loading">
        正在加载 HTML 文件...
      </div>
      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="!loading && !error">
        <div v-if="files.length === 0" class="empty-state">
          <p>暂无 HTML 文件</p>
          <p class="hint">生成 HTML 格式的内容后，文件将显示在这里</p>
        </div>

        <div v-else class="files-grid">
          <div v-for="file in files" :key="file.file_id" class="file-card">
            <div class="file-info">
              <h3>{{ file.filename }}</h3>
              <div class="file-meta">
                <span class="prompt-type">{{ getPromptDisplayName(file.prompt_type) }}</span>
                <span class="created-at">{{ formatTime(file.created_at) }}</span>
              </div>
              <div class="file-preview">
                {{ file.original_input }}
              </div>
              <div class="file-stats">
                <span class="content-length">{{ file.content_length }} 字符</span>
              </div>
            </div>
            <div class="file-actions">
              <button class="view-btn" @click="viewFile(file.file_id)">
                查看
              </button>
              <button class="delete-btn" @click="deleteFile(file.file_id, file.filename)">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HtmlBrowser',
  data() {
    return {
      files: [],
      loading: true,
      error: null
    }
  },
  methods: {
    async loadFiles() {
      console.log('[HtmlBrowser] Loading HTML files')

      this.loading = true
      this.error = null

      try {
        const response = await axios.get('/api/html/files')
        this.files = response.data.files
        console.log(`[HtmlBrowser] Loaded ${this.files.length} HTML files`)
      } catch (err) {
        this.error = err.response?.data?.error || '加载 HTML 文件失败'
        console.error('[HtmlBrowser] Error loading files:', err)
      } finally {
        this.loading = false
      }
    },

    viewFile(fileId) {
      console.log('[HtmlBrowser] Viewing file:', fileId)
      this.$router.push(`/html/${fileId}`)
    },

    async deleteFile(fileId, filename) {
      if (!confirm(`确定要删除文件 "${filename}" 吗？此操作不可恢复。`)) {
        return
      }

      console.log('[HtmlBrowser] Deleting file:', fileId)

      try {
        await axios.delete(`/api/html/files/${fileId}`)
        console.log('[HtmlBrowser] File deleted successfully:', fileId)

        // Reload files list
        this.loadFiles()
      } catch (err) {
        const error = err.response?.data?.error || '删除文件失败'
        console.error('[HtmlBrowser] Error deleting file:', err)
        alert(`删除失败: ${error}`)
      }
    },

    getPromptDisplayName(prompt) {
      const displayNames = {
        'init_prj_prompt': '项目初始化助手',
        'learn_word': '单词学习助手'
      }
      return displayNames[prompt] || prompt || '默认'
    },

    formatTime(timeString) {
      return new Date(timeString).toLocaleString('zh-CN')
    },

    goBack() {
      this.$router.push('/')
    }
  },
  mounted() {
    this.loadFiles()
  }
}
</script>

<style scoped>
@import './neo-baroque.css';

.html-browser {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: var(--primary-font);
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

.actions {
  display: flex;
  gap: 10px;
}

.back-btn, .refresh-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.back-btn:hover, .refresh-btn:hover {
  background: #2980b9;
}

.back-btn:disabled, .refresh-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
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

.empty-state {
  text-align: center;
  padding: 50px;
  color: #666;
}

.empty-state p {
  margin-bottom: 10px;
}

.empty-state .hint {
  font-size: 14px;
  color: #999;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.file-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.2s;
}

.file-card:hover {
  transform: translateY(-2px);
}

.file-info {
  padding: 20px;
}

.file-info h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 16px;
  word-break: break-all;
}

.file-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.prompt-type {
  background: #3498db;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.created-at {
  color: #666;
  font-size: 12px;
}

.file-preview {
  color: #555;
  font-size: 14px;
  margin-bottom: 10px;
  line-height: 1.4;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-length {
  color: #999;
  font-size: 12px;
}

.file-actions {
  display: flex;
  border-top: 1px solid #eee;
}

.file-actions button {
  flex: 1;
  border: none;
  padding: 12px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.view-btn {
  background: #27ae60;
  color: white;
}

.view-btn:hover {
  background: #219a52;
}

.delete-btn {
  background: #e74c3c;
  color: white;
}

.delete-btn:hover {
  background: #c0392b;
}
</style>