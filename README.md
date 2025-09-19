# AI Chat Assistant

一个基于Vue.js和Flask的前后端分离AI聊天应用，支持与BigModel GLM-4.5 API集成，具备智能模型选择功能。

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
- AI集成：BigModel GLM-4.5 API，支持多种输出格式
- **智能模型选择**：根据输入内容自动选择glm-4.5或glm-4.5-air模型
- 响应式设计：简洁现代的用户界面
- 错误处理：完整的错误处理机制
- 内容管理：文件-based的Markdown和HTML内容管理
- 多种输出格式：自动检测和渲染Markdown、HTML、纯文本

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

2. 编辑 `.env` 文件，添加你的BigModel API密钥：
```
GLM_API_KEY=your_actual_api_key_here
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

### GET /api/prompts

获取可用的提示词类型列表。

### HTML文件管理
- `GET /api/html/files` - 获取所有HTML文件列表
- `GET /api/html/files/<file_id>` - 获取指定HTML文件内容
- `DELETE /api/html/files/<file_id>` - 删除指定HTML文件
- `GET /api/html/files/<file_id>/view` - 直接在浏览器中查看HTML文件

## 智能模型选择示例

| 输入内容 | 选择的模型 | 选择原因 |
|---------|-----------|----------|
| "你好" | glm-4.5-air | 简单问候，短输入 |
| "帮我写个python函数" | glm-4.5 | 包含编程关键词 |
| "分析这个问题" | glm-4.5 | 复杂任务词汇 |
| "这是一个超过16个字符的较长输入" | glm-4.5 | 输入长度 > 16字符 |
| "第一点\n第二点" | glm-4.5 | 包含换行符 |
| "天气不错" | glm-4.5-air | 简单陈述，短输入 |

## 使用说明

1. 在前端输入框中输入问题或需求
2. 点击"提交"按钮发送到后端
3. 系统根据输入内容智能选择最适合的GLM模型：
   - **简单输入**（≤16字符）：使用 `glm-4.5-air` 模型
   - **复杂输入**（>16字符）：使用 `glm-4.5` 模型
   - **编程相关**：包含编程关键词时使用 `glm-4.5` 模型
   - **特殊格式**：包含换行符或列表时使用 `glm-4.5` 模型
4. 后端调用BigModel API生成内容
5. 前端根据返回格式自动渲染（Markdown/HTML/纯文本）

## 环境变量

- `GLM_API_KEY`: BigModel API密钥（必需）
- `AI_BASE_URL`: BigModel API基础URL（可选，默认为智谱清言API）
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
- BigModel GLM API (zai-sdk)
- python-dotenv
- 智能模型选择算法

## 开发说明

### 智能模型选择算法
系统根据以下规则自动选择最适合的GLM模型：

1. **基于输入长度**：
   - 输入 > 16字符 → 使用 `glm-4.5`（处理复杂内容）
   - 输入 ≤ 16字符 → 使用 `glm-4.5-air`（快速响应）

2. **基于内容复杂度**：
   - 编程相关（python, 函数, 算法, 数据库等）→ `glm-4.5`
   - 复杂任务（分析, 设计, 优化, 实现等）→ `glm-4.5`

3. **基于格式复杂度**：
   - 包含换行符、列表符号 → `glm-4.5`
   - 纯简单文本 → `glm-4.5-air`

### 扩展AI服务
在 `backend/ai_service.py` 中可以轻松添加对其他AI服务的支持。

### 自定义提示词
- 修改 `ai_service.py` 中的 `default_prompt` 来自定义AI行为
- 在 `prompts/` 目录添加自定义提示词模板

### 添加新格式
在前端 `App.vue` 中添加新的格式处理逻辑，在后端添加对应的检测和清理逻辑。

### 测试功能
运行模型选择功能测试：
```bash
python3 test_model_selection.py
```