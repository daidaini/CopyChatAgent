import os
import json
import re
import requests
from zhipuai import ZhipuAI

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GLM_API_KEY')
        self.base_url = os.getenv('AI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
        
        if not self.api_key:
            raise ValueError("GLM_API_KEY environment variable is required")
        
        self.client = ZhipuAI(api_key=self.api_key, base_url=self.base_url)
        
        self.system_prompt = """你是一个专业的AI助手，请根据用户的输入生成有价值的内容。
你可以生成以下格式的内容：
1. Markdown格式 - 用于结构化的文档、代码示例等
2. HTML格式 - 用于富文本内容
3. 纯文本格式 - 用于简单的回答

请根据内容类型自动选择最适合的格式，并在返回时明确指明格式类型。
你的回答应该清晰、准确、有帮助。"""

    def generate_content(self, user_input):
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"用户输入：{user_input}\n\n请根据用户输入生成合适的内容，并明确指明格式类型（markdown/html/text）。"}
            ]
            
            response = self.client.chat.completions.create(
                model="glm-4-0520",  # GLM-4.5模型
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