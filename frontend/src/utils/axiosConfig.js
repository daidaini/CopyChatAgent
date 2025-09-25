import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000, // 默认30秒超时
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url} - Starting request`)
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API] ${response.config.method.toUpperCase()} ${response.config.url} - Response received`)
    return response
  },
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('[API] Request timeout:', error.config?.url)
      error.message = '请求超时，请稍后重试'
    } else if (error.response) {
      console.error(`[API] HTTP Error ${error.response.status}:`, error.config?.url)
    } else {
      console.error('[API] Network error:', error.message)
    }
    return Promise.reject(error)
  }
)

// 针对不同API的超时配置
export const apiTimeouts = {
  // 普通聊天接口 - 60秒
  chat: 60000,
  // 量化策略生成接口 - 5分钟
  quantStrategy: 300000,
  // 知识库查询接口 - 30秒
  knowledgeBase: 30000,
  // 文件操作接口 - 120秒
  fileOperations: 120000,
  // 默认超时 - 30秒
  default: 30000
}

// 带超时的请求方法
export const api = {
  get: (url, config = {}) => {
    return apiClient.get(url, {
      ...config,
      timeout: config.timeout || apiTimeouts.default
    })
  },

  post: (url, data = {}, config = {}) => {
    return apiClient.post(url, data, {
      ...config,
      timeout: config.timeout || apiTimeouts.default
    })
  },

  put: (url, data = {}, config = {}) => {
    return apiClient.put(url, data, {
      ...config,
      timeout: config.timeout || apiTimeouts.default
    })
  },

  delete: (url, config = {}) => {
    return apiClient.delete(url, {
      ...config,
      timeout: config.timeout || apiTimeouts.default
    })
  }
}

// 专用API方法
export const chatApi = {
  generate: (data) => api.post('/generate', data, { timeout: apiTimeouts.chat }),
  getPrompts: () => api.get('/prompts', { timeout: apiTimeouts.default })
}

export const quantApi = {
  generateStrategy: (data) => api.post('/generate_quant_trade_strategy', data, {
    timeout: apiTimeouts.quantStrategy
  }),
  getKnowledgeBases: () => api.get('/generate_quant_trade_strategy/knowledge_bases', {
    timeout: apiTimeouts.knowledgeBase
  })
}

export const fileApi = {
  getFiles: () => api.get('/html/files', { timeout: apiTimeouts.fileOperations }),
  getFile: (fileId) => api.get(`/html/files/${fileId}`, { timeout: apiTimeouts.fileOperations }),
  deleteFile: (fileId) => api.delete(`/html/files/${fileId}`, { timeout: apiTimeouts.fileOperations }),
  viewFile: (fileId) => api.get(`/html/files/${fileId}/view`, { timeout: apiTimeouts.fileOperations })
}

export default apiClient