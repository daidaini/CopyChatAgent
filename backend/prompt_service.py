import os
from logger import ai_service_logger

class PromptService:
    def __init__(self, prompts_dir):
        self.prompts_dir = prompts_dir
        self.default_prompt = """你是一个专业的AI助手，请根据用户的输入生成有价值的内容。
你可以生成以下格式的内容：
1. Markdown格式 - 用于结构化的文档、代码示例等
2. HTML格式 - 用于富文本内容
3. 纯文本格式 - 用于简单的回答

请根据内容类型自动选择最适合的格式，并在返回时明确指明格式类型。
你的回答应该清晰、准确、有帮助。"""

        self.available_prompts = self._load_available_prompts()
        ai_service_logger.info(f"PromptService initialized with {len(self.available_prompts)} prompts")

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

    def get_prompt_content(self, prompt_name):
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

    def get_available_prompts(self):
        """Get list of available prompt types"""
        return list(self.available_prompts.keys())

    def get_default_prompt(self):
        """Get the default system prompt"""
        return self.default_prompt