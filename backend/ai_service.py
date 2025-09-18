import os
import json
import re
import requests
from zai import ZhipuAiClient
from logger import ai_service_logger
from html_manager import HTMLManager
from file_based_markdown_converter import FileBasedMarkdownConverter
import time

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GLM_API_KEY')
        self.base_url = os.getenv('AI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')

        ai_service_logger.info("Initializing AIService")
        ai_service_logger.debug(f"API Base URL: {self.base_url}")
        ai_service_logger.debug(f"Prompts directory: {self.prompts_dir}")

        if not self.api_key:
            ai_service_logger.error("GLM_API_KEY environment variable is required")
            raise ValueError("GLM_API_KEY environment variable is required")

        self.client = ZhipuAiClient(api_key=self.api_key, base_url=self.base_url)
        ai_service_logger.info("ZhipuAiClient initialized successfully")

        # Initialize HTML manager
        self.html_manager = HTMLManager()
        ai_service_logger.info("HTML manager initialized successfully")

        # Initialize file-based Markdown converter
        self.markdown_converter = FileBasedMarkdownConverter()
        ai_service_logger.info("File-based Markdown converter initialized successfully")

        # Load default prompt
        self.default_prompt = """你是一个专业的AI助手，请根据用户的输入生成有价值的内容。
你可以生成以下格式的内容：
1. Markdown格式 - 用于结构化的文档、代码示例等
2. HTML格式 - 用于富文本内容
3. 纯文本格式 - 用于简单的回答

请根据内容类型自动选择最适合的格式，并在返回时明确指明格式类型。
你的回答应该清晰、准确、有帮助。"""

        self.available_prompts = self._load_available_prompts()
        ai_service_logger.info(f"Loaded {len(self.available_prompts)} available prompts: {list(self.available_prompts.keys())}")

    def _load_available_prompts(self):
        """Load all available prompt files from the prompts directory"""
        prompts = {}
        ai_service_logger.debug(f"Loading prompts from directory: {self.prompts_dir}")

        if os.path.exists(self.prompts_dir):
            for filename in os.listdir(self.prompts_dir):
                if filename.endswith('.md'):
                    prompt_name = filename[:-3]  # Remove .md extension
                    prompts[prompt_name] = filename
                    ai_service_logger.debug(f"Found prompt: {prompt_name} -> {filename}")
        else:
            ai_service_logger.warning(f"Prompts directory does not exist: {self.prompts_dir}")

        ai_service_logger.info(f"Total prompts loaded: {len(prompts)}")
        return prompts

    def _load_prompt_content(self, prompt_name):
        """Load the content of a specific prompt file"""
        ai_service_logger.debug(f"Loading prompt content for: {prompt_name}")

        if prompt_name not in self.available_prompts:
            ai_service_logger.warning(f"Prompt not found: {prompt_name}, using default")
            return self.default_prompt

        prompt_file = os.path.join(self.prompts_dir, self.available_prompts[prompt_name])
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            ai_service_logger.debug(f"Successfully loaded prompt: {prompt_name}, length: {len(content)}")
            return content
        except Exception as e:
            ai_service_logger.error(f"Error loading prompt {prompt_name}: {e}")
            return self.default_prompt

    def generate_content(self, user_input, prompt_type=None):
        start_time = time.time()
        ai_service_logger.info(f"Starting content generation - prompt_type: {prompt_type}, input_length: {len(user_input)}")
        ai_service_logger.debug(f"User input: {user_input[:100]}...")

        try:
            # Load the appropriate prompt
            if prompt_type and prompt_type in self.available_prompts:
                system_prompt = self._load_prompt_content(prompt_type)
                ai_service_logger.info(f"Using custom prompt: {prompt_type}")
            else:
                system_prompt = self.default_prompt
                ai_service_logger.info("Using default prompt")

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

            ai_service_logger.debug("Sending request to GLM API")
            response = self.client.chat.completions.create(
                model="glm-4.5-air",  # GLM-4.5模型
                messages=messages,
                temperature=0.7,
                max_tokens=8192,
                stream=False
            )

            content = response.choices[0].message.content
            ai_service_logger.info(f"Recved response content from LLM: {content}")
            original_format_type = self._detect_format(content)

            # Handle Markdown to HTML conversion
            html_file_info = None
            display_content = content
            display_format = original_format_type

            if original_format_type == "markdown":
                ai_service_logger.info("Markdown content detected, saving to file and converting to HTML")

                # Always save markdown file first
                markdown_file_info = None
                try:
                    markdown_file_info = self.markdown_converter.save_markdown_file(
                        content,prompt_type,user_input
                    )
                    if markdown_file_info:
                        ai_service_logger.info(f"Markdown content saved to file: {markdown_file_info['filename']}")
                    else:
                        ai_service_logger.error("Failed to save markdown file")
                except Exception as save_error:
                    ai_service_logger.error(f"Error saving markdown file: {save_error}")

                needTransToHtml = False
                #if content.find('svg') != -1:
                 #   needTransToHtml = True

                html_file_info = None
                if needTransToHtml:
                    try:
                        title = f"AI Generated Content - {prompt_type or 'Default'}"
                        html_file_info, html_content = self.markdown_converter.convert_markdown_to_html(
                            markdown_file_info,
                            title
                        )
                        display_format = "html"
                    except Exception as conversion_error:
                        ai_service_logger.error(f"Error in markdown to HTML conversion: {conversion_error}")

            elif original_format_type == "html":
                ai_service_logger.info("HTML content detected, saving to file")
                html_file_info = self.html_manager.save_html_content(
                    content,prompt_type,user_input
                )
                if html_file_info:
                    ai_service_logger.info(f"HTML content saved: {html_file_info['filename']}")
                else:
                    ai_service_logger.warning("Failed to save HTML content")

            processing_time = time.time() - start_time
            ai_service_logger.info(f"Content generation completed successfully - original_format: {original_format_type}, display_format: {display_format}, processing_time: {processing_time:.2f}s")
            ai_service_logger.debug(f"Generated content length: {len(display_content)}")

            result = {
                "format": display_format,
                "original_format": original_format_type,
                "content": display_content,
                "html_file_info": html_file_info
            }

            # Add markdown file info if it exists
            if original_format_type == "markdown" and markdown_file_info:
                result["markdown_file_info"] = markdown_file_info

            return result

        except Exception as e:
            processing_time = time.time() - start_time
            ai_service_logger.error(f"Error calling GLM API: {e} - processing_time: {processing_time:.2f}s")
            return {
                "format": "text",
                "content": f"抱歉，生成内容时出现错误：{str(e)}"
            }
    
    def _detect_format(self, content):
        content_lower = content.lower()
        
        if ("format: markdown" in content_lower or 
            "格式：markdown" in content_lower or
            re.search(r'^#{1,6}\s', content) or
            '```' in content):
            return "markdown"
        
        elif ("format: html" in content_lower or 
              "格式：html" in content_lower or
              '<' in content and '>' in content and re.search(r'<[a-zA-Z][^>]*>', content)):
            return "html"
        
        else:
            return "markdown"
    
    def _clean_content(self, content, format_type):
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
        
        return '\n'.join(clean_lines).strip()

    def get_available_prompts(self):
        """Get list of available prompt types"""
        return list(self.available_prompts.keys())

    def get_html_file(self, file_id):
        """Get HTML file content and metadata"""
        return self.html_manager.get_html_file(file_id)

    def get_all_html_files(self):
        """Get list of all HTML files"""
        return self.html_manager.get_all_html_files()

    def delete_html_file(self, file_id):
        """Delete HTML file"""
        return self.html_manager.delete_html_file(file_id)