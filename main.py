"""
ResumeSearch 主程序入口
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.routes import create_app
from utils.config_loader import config


def main():
    """主程序入口"""
    print("=" * 80)
    print("ResumeSearch - 智能简历分析系统")
    print("=" * 80)

    # 获取API配置
    api_config = config.get_api_config()
    host = api_config.get('host', '0.0.0.0')
    port = api_config.get('port', 8000)
    debug = api_config.get('debug', True)

    # 创建Flask应用
    app = create_app()

    print(f"\n服务启动配置:")
    print(f"  - Host: {host}")
    print(f"  - Port: {port}")
    print(f"  - Debug: {debug}")
    print(f"\n可用接口:")
    print(f"  - GET  http://{host}:{port}/health")
    print(f"  - POST http://{host}:{port}/api/analyze")
    print("\n提示: 请确保在 config/config.yaml 中配置了有效的 OpenAI API Key")
    print("=" * 80 + "\n")

    # 启动服务
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
