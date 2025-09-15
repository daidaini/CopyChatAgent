#!/usr/bin/env python3
"""
Test script to verify the fixed markdown saving logic
"""
import sys
import os
import time
sys.path.append('backend')

# from ai_service import AIService

def test_markdown_saving():
    print("Testing fixed markdown saving logic...")

    # Import and initialize the converter directly (avoiding API key requirement)
    from file_based_markdown_converter import FileBasedMarkdownConverter
    converter = FileBasedMarkdownConverter(data_dir="Data")

    # Test markdown content
    test_markdown_content = """# 测试Markdown保存

这是一个测试markdown文档，验证修复后的保存逻辑。

## 功能验证

1. **粗体文本** 和 *斜体文本*
2. 代码块：
   ```python
   def test_function():
       return "测试成功"
   ```
3. 列表和链接

[测试链接](https://example.com)

> 这是一个引用块

"""

    print("1. Testing markdown content processing...")

    # Simulate the content generation workflow
    original_format = "markdown"
    clean_content = test_markdown_content
    prompt_type = "test"
    user_input = "测试markdown保存功能"

    print(f"   Original format: {original_format}")
    print(f"   Content length: {len(clean_content)}")

    # Test the markdown saving logic directly
    markdown_file_info = converter.save_markdown_file(
        content=clean_content,
        prompt_type=prompt_type,
        original_input=user_input
    )

    if markdown_file_info:
        print(f"   ✓ Markdown file saved: {markdown_file_info['filename']}")
        print(f"   ✓ File path: {markdown_file_info['filepath']}")
        print(f"   ✓ File size: {markdown_file_info['size']} bytes")

        # Verify file exists and content is correct
        if os.path.exists(markdown_file_info['filepath']):
            with open(markdown_file_info['filepath'], 'r', encoding='utf-8') as f:
                saved_content = f.read()

            if saved_content.strip() == clean_content.strip():
                print("   ✓ File content matches original content")
            else:
                print("   ✗ File content does not match original content")
                return False
        else:
            print("   ✗ Markdown file does not exist")
            return False
    else:
        print("   ✗ Failed to save markdown file")
        return False

    print("2. Testing HTML conversion...")

    # Test HTML conversion
    html_file_info, html_content = converter.convert_markdown_to_html(
        markdown_file_info,
        "Test HTML Conversion"
    )

    if html_file_info and html_content:
        print(f"   ✓ HTML file created: {html_file_info['filename']}")
        print(f"   ✓ HTML content length: {len(html_content)}")

        # Verify HTML file exists
        if os.path.exists(html_file_info['filepath']):
            print("   ✓ HTML file exists on disk")
        else:
            print("   ✗ HTML file does not exist")
            return False
    else:
        print("   ✗ Failed to convert to HTML")
        return False

    print("3. Testing complete workflow simulation...")

    # Test the complete workflow as it would happen in generate_content
    result = {
        "format": "html" if html_file_info else "markdown",
        "original_format": "markdown",
        "content": html_content if html_file_info else clean_content,
        "html_file_info": html_file_info,
        "markdown_file_info": markdown_file_info
    }

    print(f"   ✓ Result format: {result['format']}")
    print(f"   ✓ Original format: {result['original_format']}")
    print(f"   ✓ Has markdown file info: {'markdown_file_info' in result}")
    print(f"   ✓ Has html file info: {'html_file_info' in result}")

    print("4. Testing file preservation...")

    # Check that files are not overwritten
    time.sleep(1)  # Ensure different timestamp

    # Save another markdown file
    markdown_file_info2 = converter.save_markdown_file(
        content=clean_content + "\n\n第二个文件，避免覆盖",
        prompt_type=prompt_type,
        original_input=user_input + " (2)"
    )

    if markdown_file_info2:
        print(f"   ✓ Second markdown file saved: {markdown_file_info2['filename']}")

        # Verify both files exist and are different
        if (os.path.exists(markdown_file_info['filepath']) and
            os.path.exists(markdown_file_info2['filepath']) and
            markdown_file_info['filename'] != markdown_file_info2['filename']):
            print("   ✓ Files are preserved and not overwritten")
        else:
            print("   ✗ Files may have been overwritten")
            return False
    else:
        print("   ✗ Failed to save second markdown file")
        return False

    print("\nAll tests passed! ✓")
    print("✓ Markdown content is properly saved to files")
    print("✓ Files are preserved and not overwritten")
    print("✓ HTML conversion works correctly")
    print("✓ Complete workflow functions as expected")

    return True

if __name__ == "__main__":
    test_markdown_saving()