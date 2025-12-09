"""
大厂判断模块（模型2）
功能：判断候选人是否在大厂工作过
"""
from typing import Dict, Any, List
from .base_model import BaseModel
from utils.config_loader import config


class BigCompanyChecker(BaseModel):
    """大厂判断器"""

    def __init__(self):
        super().__init__()
        self.big_company_config = config.get_big_company_config()
        self.known_companies = self.big_company_config.get('known_companies', [])
        self.employee_threshold = self.big_company_config.get('employee_count_threshold', 1000)
        self.require_listed = self.big_company_config.get('require_listed', True)

        self.system_prompt = f"""你是一个专业的企业分析专家。
你的任务是判断候选人是否在大厂工作过。

大厂的判断标准：
1. 员工人数达到{self.employee_threshold}人以上
2. {'必须是上市企业' if self.require_listed else '不要求是否上市'}
3. 或者在以下知名大厂列表中：{', '.join(self.known_companies)}

请分析候选人的工作经历，判断每家公司是否符合大厂标准。

返回JSON格式：
{{
    "has_big_company_experience": true/false,
    "big_companies": [
        {{
            "company_name": "公司名称",
            "is_big_company": true/false,
            "reason": "判断理由",
            "employee_count": "员工人数估计",
            "is_listed": true/false,
            "match_known_list": true/false
        }}
    ],
    "summary": "总结说明"
}}
"""

    def process(self, work_experience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        判断是否有大厂经历

        Args:
            work_experience: 工作经历列表

        Returns:
            判断结果
        """
        print("=" * 50)
        print("【模型2】开始判断大厂经历...")
        print("=" * 50)

        try:
            companies_text = "\n".join([
                f"- {exp.get('company', '未知')}: {exp.get('position', '未知')} ({exp.get('start_date', '')} - {exp.get('end_date', '')})"
                for exp in work_experience
            ])

            user_prompt = f"""候选人的工作经历如下：
{companies_text}

请判断候选人是否有大厂工作经历。"""

            response = self.call_gpt(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt
            )

            result = self.parse_json_response(response)

            has_big_company = result.get('has_big_company_experience', False)
            big_companies = [
                c.get('company_name')
                for c in result.get('big_companies', [])
                if c.get('is_big_company', False)
            ]

            print(f"✓ 大厂判断完成")
            print(f"  - 是否有大厂经历: {'是' if has_big_company else '否'}")
            if big_companies:
                print(f"  - 大厂列表: {', '.join(big_companies)}")

            return {
                "success": True,
                "data": result,
                "message": "大厂判断完成"
            }

        except Exception as e:
            print(f"✗ 大厂判断失败: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"大厂判断失败: {str(e)}"
            }
