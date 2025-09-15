#!/usr/bin/env python3
"""
Test script for Markdown to HTML conversion
"""
import sys
import os
sys.path.append('backend')

from markdown_converter import MarkdownConverter
from html_manager import HTMLManager
from logger import backend_logger

def test_markdown_conversion():
    print("Testing Markdown to HTML conversion...")

    # Test markdown content
    test_markdown = """# 测试标题

这是一个**Markdown**测试文档。

## 子标题

- 项目1
- 项目2
- 项目3

```python
def hello_world():
    print("Hello, World!")
```

这是一个[链接](https://example.com)。

> 这是一个引用块

### 更多内容

*斜体文本*和**粗体文本**的测试。"""

    # Test conversion
    converter = MarkdownConverter()
    html_content = converter.convert_to_html(test_markdown, "测试文档")

    print(f"Conversion completed. HTML content length: {len(html_content)}")

    # Save to HTML manager
    html_manager = HTMLManager()
    file_info = html_manager.save_html_content(
        content=html_content,
        prompt_type="test_conversion",
        original_input="测试Markdown转换功能"
    )

    if file_info:
        print(f"HTML file saved: {file_info['filename']} (ID: {file_info['file_id']})")
        print(f"File path: {file_info['filepath']}")

        # Verify file exists and has content
        if os.path.exists(file_info['filepath']):
            with open(file_info['filepath'], 'r', encoding='utf-8') as f:
                saved_content = f.read()
            print(f"Saved file content length: {len(saved_content)}")
            print("✅ Markdown conversion test successful!")
        else:
            print("❌ Saved file not found")
    else:
        print("❌ Failed to save HTML file")

    # Test fallback conversion
    print("\nTesting fallback conversion...")
    fallback_html = converter._fallback_conversion(test_markdown, "回退测试")
    print(f"Fallback conversion completed. Length: {len(fallback_html)}")

if __name__ == '__main__':
    test_markdown_conversion()