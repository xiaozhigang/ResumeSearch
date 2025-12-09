"""
上市经历判断模块（模型3）
功能：判断候选人在职期间公司是否完成上市
"""
from typing import Dict, Any, List
from .base_model import BaseModel


class IPOChecker(BaseModel):
    """上市经历判断器"""

    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的企业上市分析专家。
你的任务是判断候选人在职期间，所在公司是否完成了上市（IPO）。

分析要点：
1. 候选人的在职时间段
2. 公司的上市时间
3. 判断在职期间是否经历了公司上市过程

请基于你的知识库和推理能力进行分析。如果无法确定，请明确说明。

返回JSON格式：
{
    "has_ipo_experience": true/false,
    "ipo_experiences": [
        {
            "company_name": "公司名称",
            "position": "职位",
            "work_period": "在职时间",
            "ipo_date": "上市时间（如果已知）",
            "experienced_ipo": true/false,
            "confidence": "high/medium/low",
            "reason": "判断理由和依据"
        }
    ],
    "summary": "总结说明"
}
"""

    def process(self, work_experience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        判断是否有上市经历

        Args:
            work_experience: 工作经历列表

        Returns:
            判断结果
        """
        print("=" * 50)
        print("【模型3】开始判断上市经历...")
        print("=" * 50)

        try:
            experiences_text = "\n".join([
                f"- {exp.get('company', '未知')}: {exp.get('position', '未知')}\n  在职时间: {exp.get('start_date', '')} - {exp.get('end_date', '')}"
                for exp in work_experience
            ])

            user_prompt = f"""候选人的工作经历如下：
{experiences_text}

请判断候选人在职期间，是否有公司完成了上市（IPO）。
请基于公开信息和已知事实进行分析。"""

            response = self.call_gpt(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt
            )

            result = self.parse_json_response(response)

            has_ipo = result.get('has_ipo_experience', False)
            ipo_companies = [
                exp.get('company_name')
                for exp in result.get('ipo_experiences', [])
                if exp.get('experienced_ipo', False)
            ]

            print(f"✓ 上市经历判断完成")
            print(f"  - 是否有上市经历: {'是' if has_ipo else '否'}")
            if ipo_companies:
                print(f"  - 上市公司列表: {', '.join(ipo_companies)}")

            return {
                "success": True,
                "data": result,
                "message": "上市经历判断完成"
            }

        except Exception as e:
            print(f"✗ 上市经历判断失败: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"上市经历判断失败: {str(e)}"
            }
