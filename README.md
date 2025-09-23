# AI Chat Assistant

基于Vue.js和Flask的AI聊天应用，集成BigModel GLM-4.5 API，采用新巴洛克数字风格UI设计。

## 🚀 快速开始

### 前端启动
```bash
cd frontend
yarn install
yarn dev
```
访问: http://localhost:3000

### 后端启动
```bash
cd backend
cp .env.example .env
# 编辑.env文件，添加GLM_API_KEY
pip install -r requirements.txt
python app.py
```
后端运行在: http://localhost:5000

## ✨ 核心功能

- **新巴洛克数字风格**: 装饰性强、视觉冲击力大的现代UI设计
- **智能提示词选择**: 10种专业化AI助手模板，涵盖学习、思维、创意、技术等领域
- **多格式输出**: 支持Markdown、HTML、纯文本智能格式检测
- **响应式设计**: 完美适配各种屏幕尺寸
- **实时交互**: 流畅的用户体验和加载状态

## 🎯 提示词类型

| 类别 | 助手类型 | 功能描述 |
|------|----------|----------|
| 📚 学习成长 | 单词词源分析、数学概念解析、编程导师 | 深度学习和技能培养 |
| 🧠 思维训练 | 逻辑思维、第一性原理、图尔敏论证 | 提升分析和推理能力 |
| 🎨 创意表达 | 创意写作、概念图解、苏格拉底对话 | 激发创造力和灵感 |
| 🏗️ 技术架构 | 数字架构师 | 系统设计和技术规划 |

## 🔧 API接口

### 主要接口
- `POST /api/generate` - 生成AI内容
- `GET /api/prompts` - 获取可用提示词
- `GET /health` - 健康检查

### 请求示例
```json
{
  "input": "用户输入",
  "prompt_type": "coding_mentor"
}
```

## 📝 环境变量

```bash
GLM_API_KEY=your_bigmodel_api_key
AI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
FLASK_ENV=development
```

## 🛠️ 技术栈

**前端**: Vue 3 + Vite + NeoBaroque UI + Marked.js
**后端**: Flask + BigModel API + 智能提示词系统
**设计**: 新巴洛克数字风格 + 响应式布局

## 📁 项目结构

```
├── frontend/          # Vue.js前端
│   ├── src/components/  # NeoBaroque组件库
│   └── src/neo-baroque.css  # 样式文件
├── backend/           # Flask后端
├── prompts/           # 提示词模板
└── README.md
```

## 🎨 UI特色

- 装饰性边框和花纹
- 金色渐变和阴影效果
- 动画图标和过渡效果
- 层次分明的信息架构
- 优雅的视觉引导

## 💡 使用提示

1. 选择合适的AI助手类型
2. 输入详细的需求描述
3. 系统自动选择最佳输出格式
4. 享受AI生成的专业内容