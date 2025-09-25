from logger import ai_service_logger

class ModelService:
    def __init__(self):
        ai_service_logger.info("ModelService initialized")

    def select_model(self, user_input, system_prompt):
        """
        根据用户输入智能选择GLM模型
        返回: 'glm-4.5' 或 'glm-4.5-air'
        """
        ai_service_logger.debug("Selecting model based on user input")

        input_length = len(user_input.strip())

        # 规则1: 基于输入长度 或 带lisp字样
        if input_length > 16 or system_prompt.find('lisp') != -1:
            ai_service_logger.debug("Selected glm-4.5 based on input length or lisp keyword")
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
                ai_service_logger.debug(f"Selected glm-4.5 based on programming keyword: {keyword}")
                return 'glm-4.5'

        # 检查是否包含复杂任务词汇
        for keyword in complex_task_keywords:
            if keyword in input_lower:
                ai_service_logger.debug(f"Selected glm-4.5 based on complex task keyword: {keyword}")
                return 'glm-4.5'

        # 规则4: 基于特殊字符和格式
        if '\n' in user_input or '•' in user_input or '-' in user_input:
            ai_service_logger.debug("Selected glm-4.5 based on special characters or formatting")
            return 'glm-4.5'

        # 默认使用轻量级模型
        ai_service_logger.debug("Selected glm-4.5-air as default")
        return 'glm-4.5-air'