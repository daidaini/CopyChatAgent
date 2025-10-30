import os
from logger import ai_service_logger

class ModelService:
    def __init__(self):
        ai_service_logger.info("ModelService initialized")

        # 从环境变量加载模型配置，如果没有则使用默认值
        self.standard_model = os.getenv('STANDARD_MODEL', 'glm-4.6')
        self.lightweight_model = os.getenv('LIGHTWEIGHT_MODEL', 'glm-4.5-air')

        ai_service_logger.info(f"Model configuration - Standard: {self.standard_model}, Lightweight: {self.lightweight_model}")

    def get_available_models(self):
        """获取可用的模型配置"""
        return {
            'standard': self.standard_model,
            'lightweight': self.lightweight_model,
            'auto': 'auto'  # 自动选择模式
        }

    def select_model(self, user_input, system_prompt, model_type='auto'):
        """
        根据用户输入和指定类型选择GLM模型

        Args:
            user_input: 用户输入文本
            system_prompt: 系统提示词
            model_type: 模型类型 ('auto', 'standard', 'lightweight')

        Returns:
            选择的模型名称
        """
        ai_service_logger.debug(f"Selecting model - type: {model_type}, input_length: {len(user_input)}")

        # 如果明确指定了模型类型
        if model_type == 'standard':
            ai_service_logger.debug(f"Selected standard model: {self.standard_model}")
            return self.standard_model
        elif model_type == 'lightweight':
            ai_service_logger.debug(f"Selected lightweight model: {self.lightweight_model}")
            return self.lightweight_model

        # 自动选择模式（默认行为）
        return self._auto_select_model(user_input, system_prompt)

    def _auto_select_model(self, user_input, system_prompt):
        """
        根据用户输入智能选择模型
        """
        ai_service_logger.debug("Auto-selecting model based on user input analysis")

        input_length = len(user_input.strip())

        # 规则1: 基于输入长度或特殊关键词
        if input_length > 100 or system_prompt.find('lisp') != -1:
            ai_service_logger.debug("Selected standard model based on input length or lisp keyword")
            return self.standard_model

        # 规则2: 基于内容复杂度 - 编程相关
        programming_keywords = [
            '代码', '函数', '算法', 'python', 'javascript', 'java', 'c++', 'html', 'css',
            '编程', '开发', '实现', '调试', 'bug', 'api', '数据库', '框架', 'typescript',
            'react', 'vue', 'angular', 'node', 'express', 'django', 'flask'
        ]

        # 规则3: 基于内容复杂度 - 复杂任务词汇
        complex_task_keywords = [
            '分析', '设计', '优化', '实现', '架构', '方案', '策略', '流程',
            '解释', '说明', '总结', '比较', '对比', '评估', '建议', '翻译',
            '创建', '重构', '部署', '测试', '文档', '教程'
        ]

        # 规则4: 量化交易相关关键词
        quant_trade_keywords = [
            '量化', '交易', '策略', '回测', '风险', '收益', '股票', '期货',
            '算法交易', '投资', '组合', '对冲', '套利', '技术分析'
        ]

        input_lower = user_input.lower()

        # 检查是否包含量化交易关键词
        for keyword in quant_trade_keywords:
            if keyword in input_lower:
                ai_service_logger.debug(f"Selected standard model based on quant trade keyword: {keyword}")
                return self.standard_model

        # 检查是否包含编程关键词
        for keyword in programming_keywords:
            if keyword in input_lower:
                ai_service_logger.debug(f"Selected standard model based on programming keyword: {keyword}")
                return self.standard_model

        # 检查是否包含复杂任务词汇
        for keyword in complex_task_keywords:
            if keyword in input_lower:
                ai_service_logger.debug(f"Selected standard model based on complex task keyword: {keyword}")
                return self.standard_model

        # 规则5: 基于特殊字符和格式（多行、列表等）
        if '\n' in user_input or '•' in user_input or '-' in user_input or user_input.count('。') > 3:
            ai_service_logger.debug("Selected standard model based on special characters or complex formatting")
            return self.standard_model

        # 默认使用轻量级模型
        ai_service_logger.debug(f"Selected lightweight model as default: {self.lightweight_model}")
        return self.lightweight_model

    def validate_model(self, model_name):
        """
        验证模型名称是否有效

        Args:
            model_name: 模型名称

        Returns:
            bool: 是否为有效的模型名称
        """
        valid_models = [self.standard_model, self.lightweight_model]
        is_valid = model_name in valid_models
        ai_service_logger.debug(f"Model validation for '{model_name}': {is_valid}")
        return is_valid