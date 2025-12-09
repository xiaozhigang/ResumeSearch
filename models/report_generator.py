"""
报告整合模块（模型5）
功能：整合所有分析结果，生成最终报告
"""
from typing import Dict, Any
from .base_model import BaseModel
import json


class ReportGenerator(BaseModel):
    """报告生成器"""

    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的人才评估报告专家。
你的任务是整合所有分析结果，生成一份专业的候选人匹配度评估报告。

报告应包含：
1. 候选人基本信息概览
2. 各项评估结果汇总
3. 匹配度分析
4. 优势与风险点
5. 最终推荐意见

请以专业、客观的方式撰写报告。

返回JSON格式：
{
    "candidate_summary": "候选人概况",
    "match_score": 85,
    "evaluation_results": {
        "big_company_experience": {
            "result": "符合/不符合",
            "details": "详细说明"
        },
        "ipo_experience": {
            "result": "符合/不符合",
            "details": "详细说明"
        },
        "negative_info": {
            "result": "无风险/有风险",
            "details": "详细说明"
        }
    },
    "strengths": ["优势1", "优势2"],
    "risks": ["风险1", "风险2"],
    "final_recommendation": "推荐/谨慎推荐/不推荐",
    "recommendation_reason": "推荐理由"
}
"""

    def process(
        self,
        job_description: str,
        exploration_direction: str,
        resume_data: Dict[str, Any],
        big_company_result: Dict[str, Any],
        ipo_result: Dict[str, Any],
        negative_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成最终报告

        Args:
            job_description: 职位描述
            exploration_direction: 探索方向
            resume_data: 简历解析数据
            big_company_result: 大厂判断结果
            ipo_result: 上市经历判断结果
            negative_result: 负面舆情检索结果

        Returns:
            最终报告
        """
        print("=" * 50)
        print("【模型5】开始生成最终报告...")
        print("=" * 50)

        try:
            # 构建用户提示词
            user_prompt = f"""职位描述：
{job_description}

探索方向：
{exploration_direction}

候选人简历信息：
{json.dumps(resume_data, ensure_ascii=False, indent=2)}

大厂经历判断结果：
{json.dumps(big_company_result, ensure_ascii=False, indent=2)}

上市经历判断结果：
{json.dumps(ipo_result, ensure_ascii=False, indent=2)}

负面舆情检索结果：
{json.dumps(negative_result, ensure_ascii=False, indent=2)}

请整合以上所有信息，生成一份专业的候选人匹配度评估报告。"""

            response = self.call_gpt(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                max_tokens=3000
            )

            result = self.parse_json_response(response)

            match_score = result.get('match_score', 0)
            recommendation = result.get('final_recommendation', '未知')

            print(f"✓ 报告生成完成")
            print(f"  - 匹配分数: {match_score}")
            print(f"  - 最终推荐: {recommendation}")

            return {
                "success": True,
                "data": result,
                "message": "报告生成完成"
            }

        except Exception as e:
            print(f"✗ 报告生成失败: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"报告生成失败: {str(e)}"
            }
