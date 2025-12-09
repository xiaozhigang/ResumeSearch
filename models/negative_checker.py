"""
负面舆情检索模块（模型4）
功能：检索候选人是否有负面舆情信息
"""
import json
import os
from typing import Dict, Any

import requests
from serpapi import GoogleSearch

from .base_model import BaseModel
from utils.config_loader import config


class NegativeChecker(BaseModel):
    """负面舆情检索器"""

    def __init__(self):
        super().__init__()
        self.negative_config = config.get_negative_check_config()
        self.google_config = config.get_google_config()
        self.search_keywords = self.negative_config.get('search_keywords', [])

        self.system_prompt = f"""你是一个专业的背景调查专家。
你的任务是根据候选人的个人信息，分析是否存在负面舆情。

负面舆情包括但不限于：
{chr(10).join([f"- {keyword}相关信息" for keyword in self.search_keywords])}

分析方法：
1. 基于候选人姓名、工作经历等信息
2. 模拟深度搜索（Deep Research）
3. 分析可能存在的负面信息风险

注意：这是基于已有信息的推理分析，实际使用时需要接入真实的搜索引擎API。

返回JSON格式：
{{
    "has_negative_info": true/false,
    "risk_level": "high/medium/low/none",
    "findings": [
        {{
            "category": "负面类别",
            "description": "具体描述",
            "source": "信息来源",
            "confidence": "high/medium/low"
        }}
    ],
    "summary": "总结说明",
    "recommendation": "建议"
}}
"""

    def web_search(self, query):

        # client = serpapi.Client(api_key="c74d00d0bc23536544bd49f64e4a1e37acb76095bbafbc998872d509a6582c36")
        # result = client.search({
        #     "engine": "google",
        #     "q": query
        # })
        # print(json.dumps(result, indent=2, ensure_ascii=False))
        # return result

        search = GoogleSearch({
            "q": query,
            "location": "Austin,Texas",
            "api_key": self.google_config.get('api_key')
        })
        return search.get_dict()


        # url = "https://serpapi.com/search"
        # headers = {"Ocp-Apim-Subscription-Key": "c74d00d0bc23536544bd49f64e4a1e37acb76095bbafbc998872d509a6582c36"}
        # params = {"q": query, "mkt": "zh-CN"}
        # return requests.get(url, headers=headers, params=params).json()


    def process(self, personal_info: Dict[str, Any], work_experience: list) -> Dict[str, Any]:
        """
        检索负面舆情

        Args:
            personal_info: 个人信息
            work_experience: 工作经历

        Returns:
            检索结果
        """
        name = personal_info.get('name', '未知')
        companies = [exp.get('company', '') for exp in work_experience]
        print("=" * 50)
        print("【模型4】开始检索负面舆情...")
        query = f"员工 {name}, {', '.join(companies)}"
        search_results = self.web_search(query)

        print("=" * 50)

        try:


            user_prompt = f"""候选人信息：
姓名: {name}
工作过的公司: {', '.join(companies)}

根据下面的搜索结果总结合分析员工有没有劣质舆论。
{search_results}"""

            response = self.call_gpt(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt
            )

            result = self.parse_json_response(response)

            has_negative = result.get('has_negative_info', False)
            risk_level = result.get('risk_level', 'none')

            print(f"✓ 负面舆情检索完成")
            print(f"  - 是否有负面信息: {'是' if has_negative else '否'}")
            print(f"  - 风险等级: {risk_level}")

            return {
                "success": True,
                "data": result,
                "message": "负面舆情检索完成"
            }

        except Exception as e:
            print(f"✗ 负面舆情检索失败: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"负面舆情检索失败: {str(e)}"
            }
