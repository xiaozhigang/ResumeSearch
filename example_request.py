"""
API调用示例代码
"""
import requests
import json


def test_analyze_api():
    """测试简历分析API"""

    # API地址
    url = "http://localhost:8000/api/analyze"

    # 示例数据
    data = {
        "job_description": """
        职位：Java架构师
        要求：
        - 5年以上Java开发经验
        - 有大型互联网公司工作经验
        - 熟悉微服务架构
        - 有技术团队管理经验
        """,

        "exploration_direction": """
        1. 要求候选人在大厂待过
        2. 要求候选人历史所在公司有经历过从未上市到上市过程
        3. 候选人有没有负面舆情信息
        """,

        "resume": """
        姓名：张三
        联系方式：138****8888
        邮箱：zhangsan@example.com

        教育背景：
        2010-2014 北京大学 计算机科学与技术 本科

        工作经历：

        1. 字节跳动（2018.07 - 至今）
           职位：高级Java架构师
           工作内容：
           - 负责抖音后端核心服务架构设计
           - 带领15人技术团队
           - 优化系统性能，支撑日活3亿用户

        2. 美团（2015.07 - 2018.06）
           职位：Java高级工程师
           工作内容：
           - 参与外卖系统核心模块开发
           - 负责订单系统重构
           - 在职期间美团于2018年9月在港交所上市

        3. 创业公司ABC（2014.07 - 2015.06）
           职位：Java开发工程师
           工作内容：
           - 负责电商平台后端开发
           - 参与系统架构设计
        """
    }

    try:
        print("发送请求到API...")
        print(f"URL: {url}\n")

        response = requests.post(url, json=data, timeout=120)

        print(f"状态码: {response.status_code}")
        print("\n响应结果:")
        print("=" * 80)

        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))

        print("=" * 80)

        if result.get('success'):
            print("\n✓ 分析成功!")
            final_report = result.get('data', {}).get('final_report', {})
            print(f"匹配分数: {final_report.get('match_score', 'N/A')}")
            print(f"最终推荐: {final_report.get('final_recommendation', 'N/A')}")
        else:
            print("\n✗ 分析失败")
            print(f"错误信息: {result.get('message')}")

    except requests.exceptions.ConnectionError:
        print("✗ 连接失败，请确保服务已启动")
        print("运行命令: python main.py")
    except Exception as e:
        print(f"✗ 发生错误: {e}")


def test_health_api():
    """测试健康检查API"""
    url = "http://localhost:8000/health"

    try:
        print("测试健康检查接口...")
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"✗ 健康检查失败: {e}")


if __name__ == '__main__':
    print("=" * 80)
    print("ResumeSearch API 测试")
    print("=" * 80 + "\n")

    # 先测试健康检查
    test_health_api()
    print("\n" + "-" * 80 + "\n")

    # 再测试分析接口
    test_analyze_api()
