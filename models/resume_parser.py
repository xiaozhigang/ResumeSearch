"""
简历解析模块（模型1）
功能：解析简历信息，提取个人信息和工作经历
"""
from typing import Dict, Any, List
from .base_model import BaseModel


class ResumeParser(BaseModel):
    """简历解析器"""

    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的简历解析专家。
你的任务是从简历文本中提取关键信息。

请提取以下信息：
1. 个人基本信息：姓名、联系方式、教育背景等
2. 工作经历：每段工作经历包括
   - 公司名称
   - 职位
   - 入职时间
   - 离职时间（如果已离职）
   - 工作描述和主要成就

请以JSON格式返回，格式如下：
{
    "personal_info": {
        "name": "姓名",
        "contact": "联系方式",
        "education": "教育背景"
    },
    "work_experience": [
        {
            "company": "公司名称",
            "position": "职位",
            "start_date": "入职时间",
            "end_date": "离职时间或'至今'",
            "description": "工作描述",
            "is_current": true/false
        }
    ]
}
"""

    def process(self, resume_text: str) -> Dict[str, Any]:
        """
        解析简历

        Args:
            resume_text: 简历文本内容

        Returns:
            解析后的简历信息
        """
        print("=" * 50)
        print("【模型1】开始解析简历...")
        print("=" * 50)

        try:
            user_prompt = f"请解析以下简历内容：\n\n{resume_text}"

            response = self.call_gpt(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt
            )

            parsed_data = self.parse_json_response(response)

            print("✓ 简历解析完成")
            print(f"  - 候选人姓名: {parsed_data.get('personal_info', {}).get('name', '未知')}")
            print(f"  - 工作经历数量: {len(parsed_data.get('work_experience', []))}")

            return {
                "success": True,
                "data": parsed_data,
                "message": "简历解析成功"
            }

        except Exception as e:
            print(f"✗ 简历解析失败: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"简历解析失败: {str(e)}"
            }
