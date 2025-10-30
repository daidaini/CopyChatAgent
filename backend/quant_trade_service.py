import time
import os
from logger import ai_service_logger
from knowledge_base_service import KnowledgeBaseService
from model_service import ModelService

class QuantTradeService:
    def __init__(self, client, knowledge_base_service):
        self.client = client
        self.knowledge_base_service = knowledge_base_service
        self.model_service = ModelService()
        ai_service_logger.info("QuantTradeService initialized with configurable model support")

    def generate_strategy(self, user_prompt, knowledge_base_name="quant_trade_api_doc", model_type='auto'):
        """Generate quantitative trading strategy using knowledge base"""
        start_time = time.time()
        ai_service_logger.info(f"Starting quantitative trading strategy generation - knowledge_base: {knowledge_base_name}, model_type: {model_type}")

        # Select model for quant trade analysis
        analysis_model = self.model_service.select_model(user_prompt, "量化交易分析", model_type)
        strategy_model = self.model_service.select_model(user_prompt, "量化交易策略生成", model_type)

        ai_service_logger.info(f"Selected models - Analysis: {analysis_model}, Strategy: {strategy_model}")

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
                model=analysis_model,
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
                return self._generate_default_strategy_with_steps(user_prompt, implementation_steps)

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
                return self._generate_default_strategy_with_steps(user_prompt, implementation_steps)

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

    def _generate_default_strategy_with_steps(self, user_prompt, implementation_steps):
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
                model=strategy_model,
                messages=messages,
                temperature=0.7,
                max_tokens=8192,
                stream=False
            )

            content = response.choices[0].message.content
            ai_service_logger.info(f"Generated result: {content}")

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

    def _generate_default_strategy(self, user_prompt):
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
                model=strategy_model,
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