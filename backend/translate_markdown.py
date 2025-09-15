#!/usr/bin/env python3
import os
import sys

from ai_service import AIService

def translate_markdown_file(input_file, output_file):
    try:
        # Read the markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize AI service
        ai_service = AIService()

        # Create translation prompt
        translation_prompt = f"""请将以下Markdown文档翻译成中文。要求：
1. 保持所有Markdown格式（标题、列表、代码块、链接等）
2. 保持图片引用路径不变
3. 专业术语可以保留英文或提供中文翻译
4. 保持文档的结构和可读性
5. 代码示例中的注释也需要翻译

需要翻译的内容：
{content}"""

        # Generate translation
        print("正在翻译文档...")
        result = ai_service.generate_content(translation_prompt)

        # Write the translated content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['content'])

        print(f"翻译完成！已保存到 {output_file}")
        return True

    except Exception as e:
        print(f"翻译过程中出现错误：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python translate_markdown.py <输入文件> <输出文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 不存在")
        sys.exit(1)

    translate_markdown_file(input_file, output_file)