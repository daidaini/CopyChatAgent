# API请求与响应格式示例

## 1. 前端到后端的请求

### POST /api/generate

**请求示例：**
```json
{
  "input": "请写一个Python函数来计算斐波那契数列"
}
```

**Headers:**
```
Content-Type: application/json
```

## 2. 后端到前端的响应

### 成功响应 - Markdown格式
```json
{
  "format": "markdown",
  "content": "# 斐波那契数列计算函数\n\n以下是计算斐波那契数列的Python函数：\n\n```python\ndef fibonacci(n):\n    \"\"\"计算斐波那契数列的第n项\"\"\"\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\n# 使用示例\nfor i in range(10):\n    print(f\"F({i}) = {fibonacci(i)}\")\n```\n\n## 优化版本\n\n```python\ndef fibonacci_optimized(n, memo={}):\n    \"\"\"使用记忆化的斐波那契函数\"\"\"\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    \n    memo[n] = fibonacci_optimized(n - 1, memo) + fibonacci_optimized(n - 2, memo)\n    return memo[n]\n```"
}
```

### 成功响应 - HTML格式
```json
{
  "format": "html",
  "content": "<h2>Python Hello World</h2><p>这是一个简单的Python程序：</p><pre><code>print(\"Hello, World!\")</code></pre><p>运行这个程序将输出：<strong>Hello, World!</strong></p>"
}
```

### 成功响应 - 纯文本格式
```json
{
  "format": "text",
  "content": "Hello World程序是最简单的程序之一。在Python中，你只需要使用print函数即可：print('Hello, World!')"
}
```

### 错误响应
```json
{
  "error": "Missing required field: input"
}
```

```json
{
  "error": "Internal server error: API key not configured"
}
```

## 3. 健康检查

### GET /health

**响应：**
```json
{
  "status": "healthy"
}
```

## 4. 前端渲染示例

### Markdown渲染结果
```html
<div class="result-content">
  <h1>斐波那契数列计算函数</h1>
  <p>以下是计算斐波那契数列的Python函数：</p>
  <pre><code>def fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)</code></pre>
</div>
```

### HTML渲染结果
```html
<div class="result-content">
  <h2>Python Hello World</h2>
  <p>这是一个简单的Python程序：</p>
  <pre><code>print("Hello, World!")</code></pre>
  <p>运行这个程序将输出：<strong>Hello, World!</strong></p>
</div>
```

### 纯文本渲染结果
```html
<div class="result-content">
  Hello World程序是最简单的程序之一。在Python中，你只需要使用print函数即可：print('Hello, World!')
</div>
```