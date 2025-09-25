import os
import json
import requests
from logger import ai_service_logger
from zai import ZhipuAiClient


class KnowledgeBaseService:
    def __init__(self, api_key, llm_base_url="https://open.bigmodel.cn/api/paas/v4"):
        self.api_key = api_key
        # Knowledge base API URL (different from LLM API)
        self.kb_base_url = "https://open.bigmodel.cn/api/llm-application/open"
        # LLM API URL (for knowledge retrieval tools)
        self.llm_base_url = llm_base_url
        self.headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json',
            'accept': '*/*'
        }
        # Separate client for LLM operations (knowledge retrieval)
        self.llm_client = ZhipuAiClient(api_key=api_key, base_url=llm_base_url)
        ai_service_logger.info("KnowledgeBaseService initialized")
        ai_service_logger.info(f"Knowledge base API URL: {self.kb_base_url}")
        ai_service_logger.info(f"LLM API URL: {self.llm_base_url}")

    def get_knowledge_base_list(self):
        """获取知识库列表"""
        try:
            url = f"{self.kb_base_url}/knowledge"
            ai_service_logger.info(f"Getting knowledge base list from: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            if result.get('code') == 200:
                knowledge_list = result.get('data', {}).get('list', [])
                ai_service_logger.info(f"Successfully retrieved knowledge base list, total: {len(knowledge_list)}")
                return knowledge_list
            else:
                ai_service_logger.error(f"Failed to get knowledge base list: {result.get('message')}")
                return []
        except Exception as e:
            ai_service_logger.error(f"Error getting knowledge base list: {e}")
            return []

    def get_knowledge_base_by_name(self, name):
        """根据名称获取知识库"""
        try:
            knowledge_bases = self.get_knowledge_base_list()
            for kb in knowledge_bases:
                if kb.get('name') == name:
                    ai_service_logger.info(f"Found knowledge base '{name}' with ID: {kb.get('id')}")
                    return kb
            ai_service_logger.warning(f"Knowledge base '{name}' not found")
            return None
        except Exception as e:
            ai_service_logger.error(f"Error getting knowledge base by name: {e}")
            return None

    def search_knowledge_base(self, knowledge_id, query, top_k=5):
        """使用官方工具调用方式搜索知识库内容"""
        try:
            # 构建检索工具
            retrieval_tool = {
                "type": "retrieval",
                "retrieval": {
                    "knowledge_id": knowledge_id,
                    "prompt_template": """从文档
\"\"\"
{{knowledge}}
\"\"\"
中找问题
\"\"\"
{{question}}
\"\"\"
的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。
不要复述问题，直接开始回答。"""
                }
            }

            # 使用LLM客户端工具调用检索知识库
            response = self.llm_client.chat.completions.create(
                model="glm-4.5-air",  # 使用支持工具的模型
                messages=[
                    {"role": "user", "content": query}
                ],
                tools=[retrieval_tool],
                stream=False
            )

            # 解析响应，提取知识库内容
            response_content = response.choices[0].message.content

            # 如果响应中包含知识库信息，我们将其格式化为搜索结果
            search_results = []
            if response_content and "不是来自文档" not in response_content:
                # 如果内容来自文档，创建搜索结果格式
                search_results.append({
                    "content": response_content,
                    "source": "knowledge_base",
                    "knowledge_id": knowledge_id,
                    "score": 1.0  # 默认分数
                })
                ai_service_logger.info(f"Successfully retrieved content from knowledge base {knowledge_id}")
            else:
                ai_service_logger.info(f"No relevant content found in knowledge base {knowledge_id}, using AI knowledge")

            return search_results

        except Exception as e:
            ai_service_logger.error(f"Error searching knowledge base with tools: {e}")
            return []

    def generate_system_prompt_from_knowledge(self, knowledge_results, user_prompt):
        """从知识库内容生成系统提示词"""
        try:
            knowledge_content = ""
            for result in knowledge_results:
                content = result.get('content', '')
                if content:
                    knowledge_content += f"{content}\n\n"

            if not knowledge_content:
                ai_service_logger.warning("No knowledge content found for prompt generation")
                return None

            system_prompt = f"""你是一个专业的量化交易策略开发专家。基于以下知识库内容，为用户生成完整的量化交易策略Python代码。

知识库内容：
{knowledge_content}

用户需求：{user_prompt}

请根据知识库中的量化交易API文档和相关概念，生成满足用户需求的完整量化交易策略代码。

要求：
1. 只输出Python代码(markdown引用代码的格式)，不要包含任何解释文字
2. 代码必须是完整的、可运行的
3. 使用markdown代码块格式输出
4. 确保代码符合量化交易的规范和最佳实践
5. 如果知识库中没有相关信息，请基于你的量化交易知识生成代码

直接开始输出代码，不要添加任何前言或说明。"""

            ai_service_logger.info("Successfully generated system prompt from knowledge base")
            return system_prompt

        except Exception as e:
            ai_service_logger.error(f"Error generating system prompt from knowledge: {e}")
            return None

    def generate_strategy_with_knowledge_retrieval(self, user_prompt, knowledge_id, implementation_steps=None):
        """使用知识库检索工具直接生成量化交易策略"""
        try:
            # 构建检索工具，专门用于量化交易策略生成
            retrieval_tool = {
                "type": "retrieval",
                "retrieval": {
                    "knowledge_id": knowledge_id,
                    "prompt_template": """你是一个专业的量化交易策略开发专家。从文档
\"\"\"
{{knowledge}}
\"\"\"
中找到与用户需求相关的量化交易API、函数、概念或实现方法。

用户需求：{{question}}

如果文档中有相关的API或实现方法，请详细说明如何使用这些API来实现用户的量化交易策略。
如果文档中没有相关信息，请说明需要使用通用的量化交易方法来实现。

重点关注：
1. 数据获取和处理的API
2. 技术指标计算的函数
3. 交易信号生成的方法
4. 回测和风险管理的工具
5. 策略优化的技巧

请提供具体的代码示例和API使用说明。"""
                }
            }

            # 构建系统提示词，包含实现步骤
            system_prompt = """你是一个专业的量化交易策略开发专家。你的任务是根据用户的量化交易需求，结合知识库中的API文档，生成完整的Python量化交易策略代码。

"""

            if implementation_steps:
                system_prompt += f"""基于用户需求分析，需要实现的步骤包括：
{implementation_steps}

请确保生成的代码能够完整实现这些步骤。
"""

            system_prompt += """
请严格按照以下要求：
1. 只输出Python代码，不要包含任何解释文字
2. 代码必须是完整的、可运行的
3. 使用markdown代码块格式输出
4. 优先使用知识库中提供的API和函数
5. 确保代码符合量化交易的规范和最佳实践
6. 包含适当的数据获取、指标计算、信号生成、风险管理等模块

直接开始输出代码，不要添加任何前言或说明。"""

            # 使用LLM客户端工具调用生成策略
            response = self.llm_client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                tools=[retrieval_tool],
                stream=False
            )

            strategy_content = response.choices[0].message.content
           # ai_service_logger.info(f"Successfully generated strategy using knowledge retrieval for knowledge base {knowledge_id}")
            ai_service_logger.info(f"Generated starteyg code: {strategy_content}")

            return {
                "content": strategy_content,
                "knowledge_used": knowledge_id,
                "source": "knowledge_retrieval"
            }

        except Exception as e:
            ai_service_logger.error(f"Error generating strategy with knowledge retrieval: {e}")
            return None