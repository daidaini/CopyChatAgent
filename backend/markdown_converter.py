import subprocess
import tempfile
import os
from logger import backend_logger

class MarkdownConverter:
    def __init__(self):
        self.pandoc_path = "/home/yubo/pkgs/pandoc-3.7.0.2/bin/pandoc"
        backend_logger.info("Markdown converter initialized with pandoc")

    def convert_to_html(self, markdown_content, title="Generated Content"):
        """
        Convert Markdown content to HTML using pandoc
        """
        try:
            backend_logger.info("Converting Markdown to HTML using pandoc")

            # Create temporary files for conversion
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
                md_file.write(markdown_content)
                md_file_path = md_file.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as html_file:
                html_file_path = html_file.name

            # Convert using pandoc with custom styling
            cmd = [
                self.pandoc_path,
                '-s',  # standalone
                '-f', 'markdown',
                '-t', 'html',
                '--metadata=title=' + title,
                '--css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css',
                '--highlight-style=pygments',
                '-o', html_file_path,
                md_file_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                backend_logger.error(f"Pandoc conversion failed: {result.stderr}")
                return self._fallback_conversion(markdown_content, title)

            # Read the generated HTML
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Clean up temporary files
            os.unlink(md_file_path)
            os.unlink(html_file_path)

            backend_logger.info("Markdown to HTML conversion successful")
            return html_content

        except Exception as e:
            backend_logger.error(f"Error in Markdown to HTML conversion: {e}")
            return self._fallback_conversion(markdown_content, title)

    def _fallback_conversion(self, markdown_content, title):
        """
        Fallback conversion using basic string replacement
        """
        backend_logger.info("Using fallback Markdown to HTML conversion")

        # Basic Markdown to HTML conversions
        html_content = markdown_content

        # Headers
        import re
        html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)

        # Bold and italic
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)

        # Code blocks
        html_content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
        html_content = re.sub(r'`(.*?)`', r'<code>\1</code>', html_content)

        # Links
        html_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html_content)

        # Lists (basic)
        html_content = re.sub(r'^- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)

        # Paragraphs
        paragraphs = html_content.split('\n\n')
        html_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                html_paragraphs.append(f'<p>{para}</p>')
            elif para:
                html_paragraphs.append(para)

        # Wrap in basic HTML structure
        final_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    {''.join(html_paragraphs)}
</body>
</html>"""

        return final_html