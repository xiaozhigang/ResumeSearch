# 快速开始指南

## 1. 配置OpenAI API Key

编辑 `config/config.yaml` 文件，将 `your-openai-api-key-here` 替换为您的真实API Key：

```yaml
openai:
  api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # 替换为你的真实API Key
```

## 2. 启动服务

```bash
./start.sh
```

启动后会看到类似输出：

```
==================================================
ResumeSearch - 智能简历分析系统
==================================================

服务启动配置:
  - Host: 0.0.0.0
  - Port: 8000
  - Debug: True

可用接口:
  - GET  http://0.0.0.0:8000/health
  - POST http://0.0.0.0:8000/api/analyze
==================================================
```

## 3. 测试API

打开新的终端窗口，运行测试脚本：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python example_request.py
```

## 4. 使用curl测试

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Java架构师，要求5年以上经验",
    "exploration_direction": "1. 大厂背景 2. 上市经历 3. 无负面舆情",
    "resume": "姓名：张三\n工作经历：字节跳动（2020-至今）Java架构师"
  }'
```

## 5. 自定义配置

编辑 `config/config.yaml` 可以自定义：

- 大厂列表
- 员工人数阈值
- 服务端口
- 并发数量
- 负面舆情检索关键词

## 常见问题

### Q1: 启动时提示找不到模块？
A: 确保在虚拟环境中运行，先执行 `source venv/bin/activate`

### Q2: API调用失败？
A: 检查 `config/config.yaml` 中的 OpenAI API Key 是否正确配置

### Q3: 响应很慢？
A: 正常现象，完整分析需要调用5次GPT-4o，大约需要30-60秒

### Q4: 如何停止服务？
A: 在终端中按 `Ctrl+C`

## 下一步

- 查看完整文档：[README.md](README.md)
- 修改配置文件：`config/config.yaml`
- 查看示例代码：`example_request.py`
- 自定义探索方向和职位描述
