# AI Chat Assistant with Quantitative Trading

基于Vue.js和Flask的全栈AI聊天应用，集成BigModel GLM-4.5 API，采用新巴洛克数字风格UI设计，支持量化交易策略生成。

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

### 🤖 AI聊天功能
- **新巴洛克数字风格**: 装饰性强、视觉冲击力大的现代UI设计
- **智能提示词选择**: 10种专业化AI助手模板，涵盖学习、思维、创意、技术等领域
- **多格式输出**: 支持Markdown、HTML、纯文本智能格式检测
- **响应式设计**: 完美适配各种屏幕尺寸
- **实时交互**: 流畅的用户体验和加载状态

### 📈 量化交易策略生成
- **AI策略生成**: 基于GLM-4.5的量化交易策略自动生成
- **知识库增强**: 支持专业量化知识库，提升策略专业性
- **代码高亮**: Python代码语法高亮显示
- **一键下载**: 策略代码直接下载为.py文件
- **实现步骤**: 详细的策略实施指导和技术说明

### 🎯 增强用户体验
- **智能超时管理**: 根据操作类型自动调整超时时间
- **轨道动画加载**: 多层旋转行星的精美加载动画
- **进度追踪**: 实时显示操作进度和预计完成时间
- **取消操作**: 支持用户主动取消长时间运行的任务
- **防重复提交**: 完整的状态管理和错误保护机制

## 🎯 提示词类型

| 类别 | 助手类型 | 功能描述 |
|------|----------|----------|
| 📚 学习成长 | 单词词源分析、数学概念解析、编程导师 | 深度学习和技能培养 |
| 🧠 思维训练 | 逻辑思维、第一性原理、图尔敏论证 | 提升分析和推理能力 |
| 🎨 创意表达 | 创意写作、概念图解、苏格拉底对话 | 激发创造力和灵感 |
| 🏗️ 技术架构 | 数字架构师 | 系统设计和技术规划 |

## 🔧 API接口

### AI聊天接口
- `POST /api/generate` - 生成AI内容
- `GET /api/prompts` - 获取可用提示词
- `GET /health` - 健康检查

### 量化交易接口
- `POST /api/generate_quant_trade_strategy` - 生成量化交易策略
- `GET /api/generate_quant_trade_strategy/knowledge_bases` - 获取知识库列表

### 请求示例

#### AI聊天请求
```json
{
  "input": "用户输入",
  "prompt_type": "coding_mentor"
}
```

#### 量化策略请求
```json
{
  "prompt": "基于MACD和RSI的双均线策略",
  "knowledge_base_name": "量化交易知识库"
}
```

## 📝 环境变量

```bash
GLM_API_KEY=your_bigmodel_api_key
AI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
FLASK_ENV=development
```

## 🛠️ 技术栈

**前端技术栈**:
- Vue 3 + Options API
- Vite 4.4.5 构建工具
- NeoBaroque UI 组件库
- Marked.js 5.1.0 (Markdown渲染)
- highlight.js 11.8.0 (代码高亮)
- Axios 1.4.0 (HTTP客户端)

**后端技术栈**:
- Flask 2.3.3 Web框架
- BigModel GLM-4.5 API
- ZhipuAI SDK
- 智能提示词系统
- 知识库服务集成
- 综合日志系统

**特色功能**:
- 轨道动画加载组件
- 智能超时管理系统
- 双标签页架构
- 文件管理和格式检测
- CORS跨域支持

## 📁 项目结构

```
├── frontend/                    # Vue.js前端
│   ├── src/
│   │   ├── components/         # Vue组件
│   │   │   ├── EnhancedLoading.vue        # 轨道动画加载组件
│   │   │   ├── QuantStrategyGenerator.vue # 量化策略生成器
│   │   │   ├── NeoBaroque*.vue            # 新巴洛克UI组件
│   │   │   └── ...
│   │   ├── utils/              # 工具函数
│   │   │   └── axiosConfig.js   # API配置和超时管理
│   │   └── ...
│   ├── test_bug_fixes.html     # UI测试页面
│   └── ...
├── backend/                     # Flask后端
│   ├── ai_service.py           # AI服务核心
│   ├── knowledge_base_service.py # 知识库服务
│   ├── file_based_markdown_converter.py # 文件转换
│   ├── html_manager.py         # HTML管理
│   ├── logger.py               # 日志系统
│   ├── prompts/                # 提示词模板
│   └── ...
├── CLAUDE.md                   # Claude Code指导文档
├── README.md                   # 项目说明文档
└── start_project.sh           # 项目管理脚本
```

## 🎨 UI特色

### 新巴洛克数字风格
- 装饰性边框和花纹
- 金色渐变和阴影效果
- 动画图标和过渡效果
- 层次分明的信息架构
- 优雅的视觉引导

### 轨道动画加载系统
- 多层旋转行星动画
- 中央恒星脉冲效果
- 实时进度条显示
- 时间追踪和预估
- 用户提示轮播
- 全屏模态背景

### 响应式设计
- 移动端优化布局
- 自适应组件大小
- 触摸友好的交互
- 跨浏览器兼容性

## ⚡ 性能特性

### 智能超时管理
- **聊天操作**: 60秒标准超时
- **量化策略**: 5分钟长时间处理
- **知识库查询**: 30秒快速响应
- **文件操作**: 120秒大文件处理
- **动态调整**: 根据操作类型自动优化

### 错误处理和恢复
- 友好的错误提示信息
- 自动重试机制
- 状态恢复功能
- 详细的日志记录

### 代码质量保证
- 防重复提交保护
- 组件状态管理
- 内存泄漏防护
- 性能监控

## 🚀 使用指南

### AI聊天模式
1. 选择合适的AI助手类型（学习、思维、创意、技术等）
2. 输入详细的需求描述
3. 系统自动选择最佳输出格式（Markdown/HTML/文本）
4. 享受AI生成的专业内容

### 量化策略模式
1. 切换到"量化策略"标签页
2. 描述您想要的交易策略（如"基于MACD的趋势跟踪策略"）
3. 可选择相关知识库提升专业性
4. 等待AI生成完整的Python策略代码
5. 查看实现步骤，可直接下载使用

### 🎯 最佳实践
- **详细描述**: 越详细的需求描述，生成的内容越精准
- **知识库选择**: 量化策略时选择合适的知识库能显著提升质量
- **耐心等待**: 复杂策略生成可能需要2-5分钟
- **代码验证**: 下载的策略代码建议在回测环境中验证

## 🔧 开发和测试

### 运行测试
```bash
# UI组件测试
open frontend/test_bug_fixes.html

# 后端功能测试
python test_markdown_conversion.py
python test_logging.py
```

### 项目管理
```bash
./start_project.sh install    # 安装依赖
./start_project.sh start      # 启动服务
./start_project.sh status     # 查看状态
./start_project.sh logs       # 查看日志
```