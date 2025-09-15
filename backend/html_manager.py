import os
import json
import re
import uuid
from datetime import datetime
from logger import backend_logger

class HTMLManager:
    def __init__(self, data_dir='../Data/html_files'):
        self.data_dir = data_dir
        self.metadata_file = os.path.join(data_dir, 'metadata.json')
        self._ensure_directories()
        self._load_metadata()

    def _ensure_directories(self):
        """Ensure the data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
        backend_logger.info(f"HTML data directory: {self.data_dir}")

    def _load_metadata(self):
        """Load existing metadata or create new"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                backend_logger.info(f"Loaded metadata for {len(self.metadata)} HTML files")
            except Exception as e:
                backend_logger.error(f"Error loading metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}
            self._save_metadata()

    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            backend_logger.debug("Metadata saved successfully")
        except Exception as e:
            backend_logger.error(f"Error saving metadata: {e}")

    def is_html_content(self, content):
        """Check if content is HTML format"""
        # Check for HTML tags
        html_patterns = [
            r'<[a-zA-Z][^>]*>.*?</[a-zA-Z][^>]*>',  # Opening and closing tags
            r'<[a-zA-Z][^>]*/>',  # Self-closing tags
            r'<[a-zA-Z][^>]*>',  # Opening tags
            r'&[a-zA-Z]+;',  # HTML entities
        ]

        content_lower = content.lower().strip()

        # Check explicit format declarations
        if ('format: html' in content_lower or '格式：html' in content_lower):
            return True

        # Check for HTML patterns
        for pattern in html_patterns:
            if re.search(pattern, content):
                return True

        return False

    def clean_html_content(self, content):
        """Clean HTML content by removing format declarations"""
        lines = content.split('\n')
        clean_lines = []

        for line in lines:
            line = line.strip()
            # Skip format declaration lines
            if (line.lower().startswith('format:') or
                line.lower().startswith('格式：') or
                line.lower().startswith('here is') or
                line.lower().startswith('以下是')):
                continue
            if line:
                clean_lines.append(line)

        return '\n'.join(clean_lines).strip()

    def save_html_content(self, content, prompt_type=None, original_input=None):
        """Save HTML content to file and return file info"""
        if not self.is_html_content(content):
            backend_logger.warning("Content is not HTML format, not saving")
            return None

        # Clean the content
        clean_content = self.clean_html_content(content)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_id = str(uuid.uuid4())[:8]
        filename = f"html_{timestamp}_{file_id}.html"
        filepath = os.path.join(self.data_dir, filename)

        # Save HTML content to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(clean_content)

            # Create metadata entry
            metadata_entry = {
                'file_id': file_id,
                'filename': filename,
                'filepath': filepath,
                'prompt_type': prompt_type,
                'original_input': original_input,
                'created_at': datetime.now().isoformat(),
                'content_length': len(clean_content)
            }

            self.metadata[file_id] = metadata_entry
            self._save_metadata()

            backend_logger.info(f"HTML content saved: {filename} (ID: {file_id})")
            return metadata_entry

        except Exception as e:
            backend_logger.error(f"Error saving HTML content: {e}")
            return None

    def get_html_file(self, file_id):
        """Get HTML file content and metadata"""
        if file_id not in self.metadata:
            backend_logger.warning(f"HTML file not found: {file_id}")
            return None

        metadata = self.metadata[file_id]
        filepath = metadata['filepath']

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                'metadata': metadata,
                'content': content
            }
        except Exception as e:
            backend_logger.error(f"Error reading HTML file {file_id}: {e}")
            return None

    def get_all_html_files(self):
        """Get list of all HTML files"""
        files = []
        for file_id, metadata in self.metadata.items():
            files.append({
                'file_id': file_id,
                'filename': metadata['filename'],
                'prompt_type': metadata['prompt_type'],
                'created_at': metadata['created_at'],
                'content_length': metadata['content_length'],
                'original_input': metadata.get('original_input', '')[:100] + '...' if len(metadata.get('original_input', '')) > 100 else metadata.get('original_input', '')
            })

        # Sort by creation time (newest first)
        files.sort(key=lambda x: x['created_at'], reverse=True)
        return files

    def delete_html_file(self, file_id):
        """Delete HTML file and its metadata"""
        if file_id not in self.metadata:
            backend_logger.warning(f"HTML file not found for deletion: {file_id}")
            return False

        metadata = self.metadata[file_id]
        filepath = metadata['filepath']

        try:
            # Delete file
            if os.path.exists(filepath):
                os.remove(filepath)

            # Remove from metadata
            del self.metadata[file_id]
            self._save_metadata()

            backend_logger.info(f"HTML file deleted: {file_id}")
            return True

        except Exception as e:
            backend_logger.error(f"Error deleting HTML file {file_id}: {e}")
            return False