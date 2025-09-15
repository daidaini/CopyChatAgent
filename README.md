# AI Chat Assistant

一个基于Vue.js和Flask的前后端分离AI聊天应用，支持与Anthropic API集成。

## 项目结构

```
.
├── frontend/          # Vue.js前端
│   ├── src/
│   │   ├── App.vue   # 主应用组件
│   │   └── main.js   # 入口文件
│   ├── index.html     # HTML模板
│   ├── package.json   # 前端依赖
│   └── vite.config.js # Vite配置
├── backend/           # Flask后端
│   ├── app.py         # Flask应用主文件
│   ├── ai_service.py  # AI服务封装
│   ├── requirements.txt # Python依赖
│   └── .env.example   # 环境变量示例
└── README.md          # 项目说明
```

## 功能特性

- 前端：Vue.js + Vite，支持Markdown和HTML渲染
- 后端：Flask REST API，处理AI生成请求
- AI集成：Anthropic API，支持多种输出格式
- 响应式设计：简洁现代的用户界面
- 错误处理：完整的错误处理机制

## 快速开始

### 前端设置

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:3000 运行

### 后端设置

1. 复制环境变量文件：
```bash
cd backend
cp .env.example .env
```

2. 编辑 `.env` 文件，添加你的Anthropic API密钥：
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

3. 安装依赖并运行：
```bash
pip install -r requirements.txt
python app.py
```

后端将在 http://localhost:5000 运行

## API文档

### POST /api/generate

**请求体：**
```json
{
  "input": "用户输入的文本"
}
```

**响应：**
```json
{
  "format": "markdown|html|text",
  "content": "生成的内容"
}
```

**错误响应：**
```json
{
  "error": "错误信息"
}
```

### GET /health

健康检查接口，返回服务状态。

## 使用说明

1. 在前端输入框中输入问题或需求
2. 点击"提交"按钮发送到后端
3. 后端调用Anthropic API生成内容
4. 前端根据返回格式自动渲染（Markdown/HTML/纯文本）

## 环境变量

- `ANTHROPIC_API_KEY`: Anthropic API密钥（必需）
- `FLASK_ENV`: Flask环境（development/production）
- `FLASK_DEBUG`: Flask调试模式

## 技术栈

### 前端
- Vue.js 3
- Vite
- Axios
- Marked.js (Markdown渲染)
- 现代CSS

### 后端
- Flask
- Flask-CORS
- Anthropic Python SDK
- python-dotenv

## 开发说明

### 扩展AI服务
在 `backend/ai_service.py` 中可以轻松添加对其他AI服务的支持。

### 自定义提示词
修改 `ai_service.py` 中的 `system_prompt` 来自定义AI的行为。

### 添加新格式
在前端 `App.vue` 中添加新的格式处理逻辑，在后端添加对应的检测和清理逻辑。