import os
import subprocess
import tempfile
import time
from datetime import datetime
from logger import ai_service_logger

class FileBasedMarkdownConverter:
    """File-based Markdown to HTML converter using pandoc"""

    def __init__(self, data_dir="../Data"):
        self.data_dir = data_dir
        self.markdown_dir = os.path.join(data_dir, "markdown")
        self.html_dir = os.path.join(data_dir, "html_files")

        # Create directories if they don't exist
        os.makedirs(self.markdown_dir, exist_ok=True)
        os.makedirs(self.html_dir, exist_ok=True)

        ai_service_logger.info(f"FileBasedMarkdownConverter initialized - markdown_dir: {self.markdown_dir}, html_dir: {self.html_dir}")

    def save_markdown_file(self, content, prompt_type=None, original_input=None):
        """Save markdown content to a file and return file info"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = os.urandom(4).hex()[:8]
            filename = f"markdown_{timestamp}_{random_suffix}.md"
            filepath = os.path.join(self.markdown_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            file_info = {
                'filename': filename,
                'filepath': filepath,
                'prompt_type': prompt_type,
                'original_input': original_input,
                'created_at': datetime.now().isoformat(),
                'size': len(content)
            }

            ai_service_logger.info(f"Markdown file saved: {filename}, size: {len(content)}")
            return file_info

        except Exception as e:
            ai_service_logger.error(f"Error saving markdown file: {e}")
            return None

    def convert_markdown_to_html(self, markdown_file_info, title="AI Generated Content"):
        """Convert markdown file to HTML using pandoc"""
        try:
            markdown_filepath = markdown_file_info['filepath']

            if not os.path.exists(markdown_filepath):
                ai_service_logger.error(f"Markdown file not found: {markdown_filepath}")
                return None

            # Generate HTML filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = os.urandom(4).hex()[:8]
            html_filename = f"html_{timestamp}_{random_suffix}.html"
            html_filepath = os.path.join(self.html_dir, html_filename)

            # Use pandoc to convert
            pandoc_path = "/home/yubo/pkgs/pandoc-3.7.0.2/bin/pandoc"

            cmd = [
                pandoc_path,
                markdown_filepath,
                '-o', html_filepath,
                '--standalone',
                '--metadata', f'title={title}',
                '--from=markdown',
                '--to=html5',
                '--css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css'
            ]

            ai_service_logger.debug(f"Running pandoc command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                # Read the converted HTML content
                with open(html_filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                html_file_info = {
                    'filename': html_filename,
                    'filepath': html_filepath,
                    'title': title,
                    'source_markdown': markdown_file_info['filename'],
                    'prompt_type': markdown_file_info['prompt_type'],
                    'original_input': markdown_file_info['original_input'],
                    'created_at': datetime.now().isoformat(),
                    'size': len(html_content)
                }

                ai_service_logger.info(f"Markdown converted to HTML: {html_filename}, source: {markdown_file_info['filename']}")
                return html_file_info, html_content
            else:
                ai_service_logger.error(f"Pandoc conversion failed: {result.stderr}")
                return None, None

        except subprocess.TimeoutExpired:
            ai_service_logger.error("Pandoc conversion timed out")
            return None, None
        except Exception as e:
            ai_service_logger.error(f"Error converting markdown to HTML: {e}")
            return None, None

    def process_markdown_content(self, content, prompt_type=None, original_input=None, title=None):
        """Complete workflow: save markdown, convert to HTML, return results"""
        if not title:
            title = f"AI Generated Content - {prompt_type or 'Default'}"

        # Step 1: Save markdown file
        markdown_file_info = self.save_markdown_file(content, prompt_type, original_input)
        if not markdown_file_info:
            return None, None

        # Step 2: Convert to HTML
        html_file_info, html_content = self.convert_markdown_to_html(markdown_file_info, title)
        if not html_file_info:
            return markdown_file_info, None

        return markdown_file_info, html_file_info

    def get_markdown_file(self, filename):
        """Get markdown file content"""
        try:
            filepath = os.path.join(self.markdown_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    'filename': filename,
                    'filepath': filepath,
                    'content': content
                }
            return None
        except Exception as e:
            ai_service_logger.error(f"Error reading markdown file {filename}: {e}")
            return None

    def get_all_markdown_files(self):
        """Get list of all markdown files"""
        try:
            files = []
            for filename in os.listdir(self.markdown_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(self.markdown_dir, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
            return sorted(files, key=lambda x: x['created_at'], reverse=True)
        except Exception as e:
            ai_service_logger.error(f"Error listing markdown files: {e}")
            return []