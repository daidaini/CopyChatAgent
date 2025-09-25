import os
import json
import re
import requests
from zai import ZhipuAiClient
from logger import ai_service_logger
from html_manager import HTMLManager
from file_based_markdown_converter import FileBasedMarkdownConverter
from knowledge_base_service import KnowledgeBaseService
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

        # Initialize knowledge base service with separate LLM client
        self.knowledge_base_service = KnowledgeBaseService(self.api_key, self.base_url)
        ai_service_logger.info("Knowledge base service initialized successfully")

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

    def load_test_markdown_file(self):
        """Load test markdown file content"""
        test_file_path = os.path.join(os.path.dirname(__file__), '../test/test_content.md')
        try:
            with open(test_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return None
        
    def _select_model(self, user_input, system_prompt):
        """
        根据用户输入智能选择GLM模型
        返回: 'glm-4.5' 或 'glm-4.5-air'
        """
        input_length = len(user_input.strip())

        # 规则1: 基于输入长度 或 带lisp字样
        if input_length > 16 or system_prompt.find('lisp') != -1:
            return 'glm-4.5'

        # 规则2: 基于内容复杂度 - 编程相关
        programming_keywords = [
            '代码', '函数', '算法', 'python', 'javascript', 'java', 'c++', 'html', 'css',
            '编程', '开发', '实现', '调试', 'bug', 'api', '数据库', '框架'
        ]

        # 规则3: 基于内容复杂度 - 复杂任务词汇
        complex_task_keywords = [
            '分析', '设计', '优化', '实现', '架构', '方案', '策略', '流程',
            '解释', '说明', '总结', '比较', '对比', '评估', '建议'
        ]

        input_lower = user_input.lower()

        # 检查是否包含编程关键词
        for keyword in programming_keywords:
            if keyword in input_lower:
                return 'glm-4.5'

        # 检查是否包含复杂任务词汇
        for keyword in complex_task_keywords:
            if keyword in input_lower:
                return 'glm-4.5'

        # 规则4: 基于特殊字符和格式
        if '\n' in user_input or '•' in user_input or '-' in user_input:
            return 'glm-4.5'

        # 默认使用轻量级模型
        return 'glm-4.5-air'

    def generate_content(self, user_input, prompt_type=None, use_test_file=False):
        start_time = time.time()
        ai_service_logger.info(f"Starting content generation - prompt_type: {prompt_type}, input_length: {len(user_input)}")
        ai_service_logger.debug(f"User input: {user_input[:100]}...")

        content = ""
        original_format_type = "markdown"
        try:
            if use_test_file:
                content = self.load_test_markdown_file()
                if content:
                    ai_service_logger.info("Using test markdown file content")
                else:
                    ai_service_logger.error("Failed to load test markdown file")
                    return {
                        "format": "text",
                        "content": "抱歉，无法加载测试文件。"
                    }
            else:
                # Load the appropriate prompt
                if prompt_type and prompt_type in self.available_prompts:
                    system_prompt = self._load_prompt_content(prompt_type)
                    ai_service_logger.info(f"Using custom prompt: {prompt_type}")
                else:
                    system_prompt = self.default_prompt
                    ai_service_logger.info("Using default prompt")

                # 智能选择模型
                selected_model = self._select_model(user_input, system_prompt)
                ai_service_logger.info(f"Selected model: {selected_model} based on input analysis")

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
                ai_service_logger.debug("Sending request to GLM API")
                response = self.client.chat.completions.create(
                    model=selected_model,  # 动态选择的模型
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
            display_format = original_format_type

            if original_format_type == "markdown":
                # Always save markdown file first
                markdown_file_info = None
                try:
                    markdown_file_info = self.markdown_converter.save_markdown_file(
                        content,prompt_type,user_input,True
                    )
                    if markdown_file_info:
                        ai_service_logger.info(f"Markdown content saved to file: {markdown_file_info['filename']}")
                    else:
                        ai_service_logger.error("Failed to save markdown file")
                except Exception as save_error:
                    ai_service_logger.error(f"Error saving markdown file: {save_error}")

                needTransToHtml = False
                if content.find('svg') != -1:
                    needTransToHtml = True

                if needTransToHtml:
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
#            ai_service_logger.debug(f"Generated content length: {len(content)}")

            result = {
                "format": display_format,
                "original_format": original_format_type,
                "content": content,
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

    def generate_quant_trade_strategy(self, user_prompt, knowledge_base_name="quant_trade_api_doc"):
        """Generate quantitative trading strategy using knowledge base"""
        start_time = time.time()
        ai_service_logger.info(f"Starting quantitative trading strategy generation - knowledge_base: {knowledge_base_name}")

        implementation_steps = None
        try:
            # Step 1: Analyze user input with GLM-4.5 to extract implementation steps
            analysis_prompt = """你是一个专业的量化交易分析师。请分析用户的需求，并输出实现该量化策略所需的基本步骤。

用户需求：{user_prompt}

请按照以下格式输出步骤：
1. 步骤一：具体描述
2. 步骤二：具体描述
3. 步骤三：具体描述
...

每个步骤应该简洁明了，专注于量化交易策略实现的关键环节。只输出步骤列表，不要添加其他解释。""".format(user_prompt=user_prompt)

            ai_service_logger.info("Step 1: Analyzing user input to extract implementation steps")
            analysis_messages = [
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": user_prompt}
            ]

            analysis_response = self.client.chat.completions.create(
                model="glm-4.5-air",
                messages=analysis_messages,
                temperature=0.5,
                max_tokens=1000,
                stream=False
            )

            implementation_steps = analysis_response.choices[0].message.content
            ai_service_logger.info(f"Extracted implementation steps: {implementation_steps[:200]}...")

            # Step 2: Get knowledge base by name
            knowledge_base = self.knowledge_base_service.get_knowledge_base_by_name(knowledge_base_name)
            if not knowledge_base:
                ai_service_logger.warning(f"Knowledge base '{knowledge_base_name}' not found, using default approach")
                return self._generate_default_quant_strategy_with_steps(user_prompt, implementation_steps)

            knowledge_id = knowledge_base.get('id')

            # Step 3: Use new knowledge retrieval method to generate strategy directly
            ai_service_logger.info("Step 3: Generating strategy using knowledge retrieval with implementation steps")
            strategy_result = self.knowledge_base_service.generate_strategy_with_knowledge_retrieval(
                user_prompt, knowledge_id, implementation_steps
            )

            if strategy_result:
                content = strategy_result['content']
                processing_time = time.time() - start_time
                ai_service_logger.info(f"Successfully generated strategy using knowledge retrieval, length: {len(content)}, processing_time:{processing_time:.2f}s")

                return {
                    "format": "markdown",
                    "content": content,
                    "knowledge_base_used": knowledge_base_name,
                    "implementation_steps": implementation_steps,
                    "source": "knowledge_retrieval",
                    "knowledge_id": knowledge_id
                }
            else:
                ai_service_logger.warning("Knowledge retrieval failed, falling back to traditional approach")
                return self._generate_default_quant_strategy_with_steps(user_prompt, implementation_steps)

        except Exception as e:
            processing_time = time.time() - start_time
            ai_service_logger.error(f"Error generating quantitative trading strategy: {e} - processing_time: {processing_time:.2f}s")

            # Fallback implementation steps if analysis failed
            if not implementation_steps:
                implementation_steps = """1. 步骤一：需求分析和数据收集
   - 分析用户的具体量化交易需求
   - 收集相关的历史市场数据
   - 确定数据源和数据格式

2. 步骤二：技术指标计算
   - 计算所需的技术指标（如移动平均线、RSI、MACD等）
   - 确定指标参数和计算方法
   - 生成交易信号

3. 步骤三：策略实现
   - 编写策略逻辑代码
   - 实现买入和卖出信号
   - 添加风险管理和止盈止损

4. 步骤四：回测和优化
   - 进行历史数据回测
   - 分析策略性能指标
   - 优化策略参数"""

            return {
                "format": "markdown",
                "content": "```python\n# Error generating trading strategy\n# Please try again later\n# Implementation steps were extracted successfully\n```",
                "error": str(e),
                "implementation_steps": implementation_steps,
                "knowledge_base_used": "error_fallback"
            }

    def _generate_default_quant_strategy_with_steps(self, user_prompt, implementation_steps):
        """Generate default quantitative trading strategy with implementation steps when knowledge base is not available"""
        default_system_prompt = """你是一个专业的量化交易策略开发专家。请为用户生成完整的量化交易策略Python代码。

用户需求：{user_prompt}

需要实现的步骤：
{implementation_steps}

要求：
1. 只输出Python代码，不要包含任何解释文字
2. 代码必须是完整的、可运行的
3. 使用markdown代码块格式输出
4. 确保代码符合量化交易的规范和最佳实践
5. 代码需要完整实现上述所有步骤

直接开始输出代码，不要添加任何前言或说明。""".format(user_prompt=user_prompt, implementation_steps=implementation_steps)

        try:
            messages = [
                {"role": "system", "content": default_system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.client.chat.completions.create(
                model="glm-4-0520",
                messages=messages,
                temperature=0.7,
                max_tokens=8192,
                stream=False
            )

            content = response.choices[0].message.content

            ai_service_logger.info(f"Generated result : {content}")

            # Ensure content is in markdown format with code blocks
            if not content.strip().startswith('```python'):
                content = f"```python\n{content}\n```"
            else:
                content = content.replace('```', '```python', 1)

            return {
                "format": "markdown",
                "content": content,
                "knowledge_base_used": "default",
                "implementation_steps": implementation_steps
            }

        except Exception as e:
            ai_service_logger.error(f"Error generating default quant strategy with steps: {e}")
            return {
                "format": "markdown",
                "content": "```python\n# Error generating trading strategy\n# Please check your input and try again\n# Implementation steps were provided\n```",
                "error": str(e),
                "implementation_steps": implementation_steps,
                "knowledge_base_used": "default_error"
            }

    def _generate_default_quant_strategy(self, user_prompt):
        """Generate default quantitative trading strategy when knowledge base is not available"""
        default_system_prompt = """你是一个专业的量化交易策略开发专家。请为用户生成完整的量化交易策略Python代码。

用户需求：{user_prompt}

要求：
1. 只输出Python代码，不要包含任何解释文字
2. 代码必须是完整的、可运行的
3. 使用markdown代码块格式输出
4. 确保代码符合量化交易的规范和最佳实践

直接开始输出代码，不要添加任何前言或说明。""".format(user_prompt=user_prompt)

        try:
            messages = [
                {"role": "system", "content": default_system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.client.chat.completions.create(
                model="glm-4-0520",
                messages=messages,
                temperature=0.7,
                max_tokens=8192,
                stream=False
            )

            content = response.choices[0].message.content

            # Ensure content is in markdown format with code blocks
            if not content.strip().startswith('```python'):
                content = f"```python\n{content}\n```"
            else:
                content = content.replace('```', '```python', 1)

            return {
                "format": "markdown",
                "content": content,
                "knowledge_base_used": "default"
            }

        except Exception as e:
            ai_service_logger.error(f"Error generating default quant strategy: {e}")
            return {
                "format": "markdown",
                "content": "```python\n# Error generating trading strategy\n# Please check your input and try again\n```",
                "error": str(e),
                "knowledge_base_used": "default_error"
            }
