#!/bin/bash

echo "=================================================="
echo "ResumeSearch - 智能简历分析系统"
echo "=================================================="

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查并安装依赖..."
pip install -q -r requirements.txt

# 检查配置文件
if grep -q "your-openai-api-key-here" config/config.yaml; then
    echo ""
    echo "⚠️  警告: 请先在 config/config.yaml 中配置 OpenAI API Key"
    echo ""
fi

# 启动服务
echo "启动服务..."
echo "=================================================="
python main.py
