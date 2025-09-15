import os
import json
import re
import requests
from zai import ZhipuAiClient

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GLM_API_KEY')
        self.base_url = os.getenv('AI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')

        if not self.api_key:
            raise ValueError("GLM_API_KEY environment variable is required")

        self.client = ZhipuAiClient(api_key=self.api_key, base_url=self.base_url)

        # Load default prompt
        self.default_prompt = """你是一个专业的AI助手，请根据用户的输入生成有价值的内容。
你可以生成以下格式的内容：
1. Markdown格式 - 用于结构化的文档、代码示例等
2. HTML格式 - 用于富文本内容
3. 纯文本格式 - 用于简单的回答

请根据内容类型自动选择最适合的格式，并在返回时明确指明格式类型。
你的回答应该清晰、准确、有帮助。"""

        self.available_prompts = self._load_available_prompts()

    def _load_available_prompts(self):
        """Load all available prompt files from the prompts directory"""
        prompts = {}
        if os.path.exists(self.prompts_dir):
            for filename in os.listdir(self.prompts_dir):
                if filename.endswith('.md'):
                    prompt_name = filename[:-3]  # Remove .md extension
                    prompts[prompt_name] = filename
        return prompts

    def _load_prompt_content(self, prompt_name):
        """Load the content of a specific prompt file"""
        if prompt_name not in self.available_prompts:
            return self.default_prompt

        prompt_file = os.path.join(self.prompts_dir, self.available_prompts[prompt_name])
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading prompt {prompt_name}: {e}")
            return self.default_prompt

    def generate_content(self, user_input, prompt_type=None):
        try:
            # Load the appropriate prompt
            if prompt_type and prompt_type in self.available_prompts:
                system_prompt = self._load_prompt_content(prompt_type)
            else:
                system_prompt = self.default_prompt

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model="glm-4.5",  # GLM-4.5模型
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=False
            )
            
            content = response.choices[0].message.content
            format_type = self._detect_format(content)
            
            if format_type != "text":
                clean_content = self._clean_content(content, format_type)
            else:
                clean_content = content.strip()
            
            return {
                "format": format_type,
                "content": clean_content
            }
            
        except Exception as e:
            print(f"Error calling GLM API: {e}")
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
            return "text"
    
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