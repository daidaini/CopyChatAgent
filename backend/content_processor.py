import re
from logger import ai_service_logger

class ContentProcessor:
    def __init__(self):
        ai_service_logger.info("ContentProcessor initialized")

    def detect_format(self, content):
        """Detect the format of the content (markdown, html, or text)"""
        ai_service_logger.debug("Detecting content format")

        content_lower = content.lower()

        if ("format: markdown" in content_lower or
            "格式：markdown" in content_lower or
            re.search(r'^#{1,6}\s', content) or
            '```' in content):
            ai_service_logger.debug("Detected markdown format")
            return "markdown"

        elif ("format: html" in content_lower or
              "格式：html" in content_lower or
              '<' in content and '>' in content and re.search(r'<[a-zA-Z][^>]*>', content)):
            ai_service_logger.debug("Detected html format")
            return "html"

        else:
            ai_service_logger.debug("Defaulting to markdown format")
            return "markdown"

    def clean_content(self, content, format_type):
        """Clean content by removing format indicators and headers"""
        ai_service_logger.debug(f"Cleaning content for format: {format_type}")

        lines = content.split('\n')
        clean_lines = []
        skip_next = False

        for line in lines:
            line = line.strip()

            if (line.lower().startswith('format:') or
                line.lower().startswith('格式：') or
                line.lower().startswith('here is') or
                line.lower().startswith('以下是')):
                continue

            if skip_next:
                skip_next = False
                continue

            if line and not line.startswith('#') and not line.startswith('```'):
                clean_lines.append(line)
            elif line.startswith('```'):
                clean_lines.append(line)
            elif line.startswith('#'):
                clean_lines.append(line)

        cleaned_content = '\n'.join(clean_lines).strip()
        ai_service_logger.debug(f"Content cleaned, length: {len(cleaned_content)}")
        return cleaned_content

    def should_convert_to_html(self, content):
        """Determine if markdown content should be converted to HTML"""
        return content.find('svg') != -1