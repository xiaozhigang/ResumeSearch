"""
基础模型类
"""
from openai import OpenAI
from typing import Dict, Any, Optional
import json
from utils.config_loader import config


class BaseModel:
    """所有模型的基类"""

    def __init__(self):
        """初始化OpenAI客户端"""
        openai_config = config.get_openai_config()
        self.api_key = openai_config.get('api_key')
        self.model = openai_config.get('model', 'gpt-4o')
        self.temperature = openai_config.get('temperature', 0.7)
        self.max_tokens = openai_config.get('max_tokens', 2000)

        if not self.api_key or self.api_key == 'your-openai-api-key-here':
            raise ValueError("请在config/config.yaml中配置有效的OpenAI API密钥")

        self.client = OpenAI(api_key=self.api_key)

    def call_gpt(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        调用GPT模型

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            模型返回的文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"调用GPT模型时发生错误: {e}")
            raise

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        解析JSON格式的响应

        Args:
            response: GPT返回的文本

        Returns:
            解析后的字典
        """
        try:
            # 尝试提取JSON内容（处理markdown代码块的情况）
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                response = response[start:end].strip()

            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print(f"原始响应: {response}")
            raise

    def process(self, *args, **kwargs) -> Dict[str, Any]:
        """
        处理逻辑（子类需要实现）

        Returns:
            处理结果字典
        """
        raise NotImplementedError("子类必须实现process方法")
