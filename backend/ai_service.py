import os
import time
from zai import ZhipuAiClient
from logger import ai_service_logger
from html_manager import HTMLManager
from file_based_markdown_converter import FileBasedMarkdownConverter
from knowledge_base_service import KnowledgeBaseService
from prompt_service import PromptService
from model_service import ModelService
from content_processor import ContentProcessor
from quant_trade_service import QuantTradeService

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

        # Initialize service components
        self.prompt_service = PromptService(self.prompts_dir)
        self.model_service = ModelService()
        self.content_processor = ContentProcessor()
        self.html_manager = HTMLManager()
        self.markdown_converter = FileBasedMarkdownConverter()
        self.knowledge_base_service = KnowledgeBaseService(self.api_key, self.base_url)
        self.quant_trade_service = QuantTradeService(self.client, self.knowledge_base_service)

        ai_service_logger.info("All service components initialized successfully")

    def get_available_prompts(self):
        """Get list of available prompt types"""
        return self.prompt_service.get_available_prompts()

    def load_test_markdown_file(self):
        """Load test markdown file content"""
        test_file_path = os.path.join(os.path.dirname(__file__), '../test/test_content.md')
        try:
            with open(test_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return None

    def generate_content(self, user_input, prompt_type=None, use_test_file=False):
        start_time = time.time()
        ai_service_logger.info(f"Starting content generation - prompt_type: {prompt_type}, input_length: {len(user_input)}")
        ai_service_logger.debug(f"User input: {user_input[:100]}...")

        try:
            # Get content from test file or AI generation
            if use_test_file:
                content = self._get_test_content()
                if content is None:
                    return self._create_error_response("抱歉，无法加载测试文件。")
            else:
                content = self._generate_ai_content(user_input, prompt_type)

            # Process content based on format
            return self._process_generated_content(content, prompt_type, start_time)

        except Exception as e:
            processing_time = time.time() - start_time
            ai_service_logger.error(f"Error calling GLM API: {e} - processing_time: {processing_time:.2f}s")
            return {
                "format": "text",
                "content": f"抱歉，生成内容时出现错误：{str(e)}"
            }

    def _get_test_content(self):
        """Get content from test file"""
        content = self.load_test_markdown_file()
        if content:
            ai_service_logger.info("Using test markdown file content")
            return content
        else:
            ai_service_logger.error("Failed to load test markdown file")
            return None

    def _generate_ai_content(self, user_input, prompt_type):
        """Generate content using AI"""
        # Get the appropriate prompt
        if prompt_type and prompt_type in self.prompt_service.get_available_prompts():
            system_prompt = self.prompt_service.get_prompt_content(prompt_type)
            ai_service_logger.info(f"Using custom prompt: {prompt_type}")
        else:
            system_prompt = self.prompt_service.get_default_prompt()
            ai_service_logger.info("Using default prompt")

        # Select model based on input
        selected_model = self.model_service.select_model(user_input, system_prompt)
        ai_service_logger.info(f"Selected model: {selected_model} based on input analysis")

        # Generate content
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        ai_service_logger.debug("Sending request to GLM API")
        response = self.client.chat.completions.create(
            model=selected_model,
            messages=messages,
            temperature=0.7,
            max_tokens=8192,
            stream=False
        )
        content = response.choices[0].message.content
        ai_service_logger.info(f"Received response content from LLM: {content}")
        return content

    def _process_generated_content(self, content, prompt_type, start_time):
        """Process and format the generated content"""
        # Detect format
        original_format_type = self.content_processor.detect_format(content)

        # Handle file operations and format conversion
        if original_format_type == "markdown":
            result = self._process_markdown_content(content, prompt_type)
        elif original_format_type == "html":
            result = self._process_html_content(content, prompt_type)
        else:
            result = self._create_text_response(content, original_format_type)

        # Log processing time
        processing_time = time.time() - start_time
        ai_service_logger.info(f"Content generation completed successfully - original_format: {original_format_type}, display_format: {result['format']}, processing_time: {processing_time:.2f}s")

        return result

    def _process_markdown_content(self, content, prompt_type):
        """Process markdown content and optionally convert to HTML"""
        html_file_info = None
        display_format = "markdown"
        markdown_file_info = None

        # Save markdown file
        try:
            markdown_file_info = self.markdown_converter.save_markdown_file(
                content, prompt_type, "", True
            )
            if markdown_file_info:
                ai_service_logger.info(f"Markdown content saved to file: {markdown_file_info['filename']}")
            else:
                ai_service_logger.error("Failed to save markdown file")
        except Exception as save_error:
            ai_service_logger.error(f"Error saving markdown file: {save_error}")

        # Check if HTML conversion is needed
        if self.content_processor.should_convert_to_html(content):
            try:
                title = f"结果页面展示 - {prompt_type or 'Default'}"
                html_file_info, html_content = self.markdown_converter.convert_markdown_to_html(
                    markdown_file_info,
                    title
                )
                content = html_content
                display_format = "html"
            except Exception as conversion_error:
                ai_service_logger.error(f"Error in markdown to HTML conversion: {conversion_error}")

        return self._create_content_response(content, "markdown", display_format, html_file_info, markdown_file_info)

    def _process_html_content(self, content, prompt_type):
        """Process HTML content"""
        ai_service_logger.info("HTML content detected, saving to file")
        html_file_info = self.html_manager.save_html_content(
            content, prompt_type, ""
        )
        if html_file_info:
            ai_service_logger.info(f"HTML content saved: {html_file_info['filename']}")
        else:
            ai_service_logger.warning("Failed to save HTML content")

        return self._create_content_response(content, "html", "html", html_file_info)

    def _create_content_response(self, content, original_format, display_format, html_file_info=None, markdown_file_info=None):
        """Create a standardized content response"""
        result = {
            "format": display_format,
            "original_format": original_format,
            "content": content,
            "html_file_info": html_file_info
        }

        if original_format == "markdown" and markdown_file_info:
            result["markdown_file_info"] = markdown_file_info

        return result

    def _create_text_response(self, content, format_type):
        """Create a text response"""
        return {
            "format": format_type,
            "original_format": format_type,
            "content": content
        }

    def _create_error_response(self, error_message):
        """Create an error response"""
        return {
            "format": "text",
            "content": error_message
        }
    
    def get_html_file(self, file_id):
        """Get HTML file content and metadata"""
        return self.html_manager.get_html_file(file_id)

    def get_all_html_files(self):
        """Get list of all HTML files"""
        return self.html_manager.get_all_html_files()

    def delete_html_file(self, file_id):
        """Delete HTML file"""
        return self.html_manager.delete_html_file(file_id)

    def generate_quant_trade_strategy(self, user_prompt, knowledge_base_name="quant_trade_api_doc"):
        """Generate quantitative trading strategy using knowledge base"""
        return self.quant_trade_service.generate_strategy(user_prompt, knowledge_base_name)

    