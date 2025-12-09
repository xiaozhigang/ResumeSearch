"""
API路由
"""
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any
import traceback

from models.resume_parser import ResumeParser
from models.big_company_checker import BigCompanyChecker
from models.ipo_checker import IPOChecker
from models.negative_checker import NegativeChecker
from models.report_generator import ReportGenerator
from utils.config_loader import config


app = Flask(__name__)


def create_app():
    """创建Flask应用"""
    return app


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "ResumeSearch API is running"
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    简历分析接口

    请求体:
    {
        "job_description": "职位描述",
        "exploration_direction": "探索方向",
        "resume": "简历内容"
    }

    返回:
    {
        "success": true/false,
        "data": {...},
        "message": "..."
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "请求体不能为空"
            }), 400

        job_description = data.get('job_description', '')
        exploration_direction = data.get('exploration_direction', '')
        resume_text = data.get('resume', '')

        # 验证必填字段
        if not job_description or not exploration_direction or not resume_text:
            return jsonify({
                "success": False,
                "message": "job_description, exploration_direction 和 resume 字段为必填项"
            }), 400

        print("\n" + "=" * 80)
        print("开始分析简历...")
        print("=" * 80)

        # 步骤1: 解析简历
        parser = ResumeParser()
        parse_result = parser.process(resume_text)

        if not parse_result['success']:
            return jsonify(parse_result), 500

        resume_data = parse_result['data']
        personal_info = resume_data.get('personal_info', {})
        work_experience = resume_data.get('work_experience', [])

        # 步骤2-4: 并发执行三个判断模块
        print("\n并发执行分析模块...")

        concurrent_config = config.get_concurrent_config()
        max_workers = concurrent_config.get('max_workers', 3)

        big_company_result = None
        ipo_result = None
        negative_result = None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_big_company = executor.submit(
                BigCompanyChecker().process,
                work_experience
            )
            future_ipo = executor.submit(
                IPOChecker().process,
                work_experience
            )
            future_negative = executor.submit(
                NegativeChecker().process,
                personal_info,
                work_experience
            )

            # 收集结果
            futures = {
                'big_company': future_big_company,
                'ipo': future_ipo,
                'negative': future_negative
            }

            for name, future in futures.items():
                try:
                    result = future.result()
                    if name == 'big_company':
                        big_company_result = result['data']
                    elif name == 'ipo':
                        ipo_result = result['data']
                    elif name == 'negative':
                        negative_result = result['data']
                except Exception as e:
                    print(f"模块 {name} 执行失败: {e}")
                    return jsonify({
                        "success": False,
                        "message": f"模块 {name} 执行失败: {str(e)}"
                    }), 500

        # 步骤5: 生成最终报告
        generator = ReportGenerator()
        report_result = generator.process(
            job_description=job_description,
            exploration_direction=exploration_direction,
            resume_data=resume_data,
            big_company_result=big_company_result,
            ipo_result=ipo_result,
            negative_result=negative_result
        )

        if not report_result['success']:
            return jsonify(report_result), 500

        print("\n" + "=" * 80)
        print("分析完成！")
        print("=" * 80 + "\n")

        # 返回完整结果
        return jsonify({
            "success": True,
            "data": {
                "resume_info": resume_data,
                "big_company_analysis": big_company_result,
                "ipo_analysis": ipo_result,
                "negative_analysis": negative_result,
                "final_report": report_result['data']
            },
            "message": "简历分析完成"
        })

    except Exception as e:
        print(f"\n错误: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": f"服务器内部错误: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        "success": False,
        "message": "接口不存在"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        "success": False,
        "message": "服务器内部错误"
    }), 500
