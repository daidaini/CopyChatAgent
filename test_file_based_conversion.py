#!/usr/bin/env python3
"""
Test script for file-based markdown conversion
"""
import sys
import os
sys.path.append('backend')

from file_based_markdown_converter import FileBasedMarkdownConverter

def test_file_based_conversion():
    print("Testing file-based markdown conversion...")

    # Initialize converter
    converter = FileBasedMarkdownConverter(data_dir="Data")

    # Test markdown content
    test_markdown = """# Test Markdown File

This is a test markdown file to verify the file-based conversion pipeline.

## Features Tested

1. **Bold text** and *italic text*
2. Code blocks:
   ```python
   def hello():
       print("Hello, World!")
   ```
3. Lists and tables

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

> This is a blockquote

[Link to example](https://example.com)

"""

    # Test the complete workflow
    print("1. Testing markdown file saving...")
    markdown_info = converter.save_markdown_file(test_markdown, "test", "Test input")
    if markdown_info:
        print(f"   ✓ Markdown file saved: {markdown_info['filename']}")
    else:
        print("   ✗ Failed to save markdown file")
        return False

    print("2. Testing markdown to HTML conversion...")
    html_info, html_content = converter.convert_markdown_to_html(markdown_info, "Test HTML")
    if html_info and html_content:
        print(f"   ✓ HTML file created: {html_info['filename']}")
        print(f"   ✓ HTML content length: {len(html_content)}")
    else:
        print("   ✗ Failed to convert markdown to HTML")
        return False

    print("3. Testing complete workflow...")
    markdown_info2, html_info2 = converter.process_markdown_content(
        test_markdown, "test", "Test input", "Complete Test"
    )
    if html_info2:
        print(f"   ✓ Complete workflow successful")
        print(f"   ✓ Markdown: {markdown_info2['filename']}")
        print(f"   ✓ HTML: {html_info2['filename']}")
    else:
        print("   ✗ Complete workflow failed")
        return False

    print("4. Testing file listing...")
    markdown_files = converter.get_all_markdown_files()
    print(f"   ✓ Found {len(markdown_files)} markdown files")

    print("\nAll tests passed! ✓")
    return True

if __name__ == "__main__":
    test_file_based_conversion()