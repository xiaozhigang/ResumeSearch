# ResumeSearch - 智能简历分析系统

基于ChatGPT-4o的智能简历匹配度分析系统，类似于 [BettaFish](https://github.com/666ghj/BettaFish) 项目。

## 项目简介

ResumeSearch 是一个智能简历分析系统，通过5个ChatGPT-4o模型并发分析简历，评估候选人与职位的匹配度。

### 核心功能

1. **简历解析**：自动提取简历中的个人信息和工作经历
2. **大厂判断**：判断候选人是否有大厂工作经验
3. **上市经历**：分析候选人是否经历过公司上市过程
4. **负面舆情**：检索候选人是否有负面信息
5. **报告生成**：整合所有分析结果，生成专业评估报告

## 项目结构

```
ResumeSearch/
├── config/              # 配置文件目录
│   ├── __init__.py
│   └── config.yaml      # 主配置文件
├── models/              # 模型模块（5个独立模型）
│   ├── __init__.py
│   ├── base_model.py    # 基础模型类
│   ├── resume_parser.py # 模型1：简历解析
│   ├── big_company_checker.py  # 模型2：大厂判断
│   ├── ipo_checker.py   # 模型3：上市经历判断
│   ├── negative_checker.py     # 模型4：负面舆情检索
│   └── report_generator.py     # 模型5：报告整合
├── api/                 # API接口层
│   ├── __init__.py
│   └── routes.py        # Flask路由
├── utils/               # 工具类
│   ├── __init__.py
│   └── config_loader.py # 配置加载器
├── main.py              # 主程序入口
├── example_request.py   # API调用示例
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明
```

## 安装部署

### 方式一：使用启动脚本（推荐）

```bash
# 直接运行启动脚本，会自动创建虚拟环境并安装依赖
./start.sh
```

### 方式二：手动安装

#### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或者
venv\Scripts\activate     # Windows
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置OpenAI API Key

编辑 `config/config.yaml` 文件，填入您的OpenAI API Key：

```yaml
openai:
  api_key: "your-openai-api-key-here"  # 替换为你的API Key
  model: "gpt-4o"
  temperature: 0.7
  max_tokens: 2000
```

#### 4. 配置大厂标准（可选）

在 `config/config.yaml` 中可以自定义大厂判断标准：

```yaml
big_company:
  employee_count_threshold: 1000  # 员工人数阈值
  require_listed: true            # 是否要求上市企业
  known_companies:                # 知名大厂列表
    - "腾讯"
    - "阿里巴巴"
    - "字节跳动"
    # ... 可自行添加
```

## 使用方法

### 启动服务

**方式一：使用启动脚本（推荐）**

```bash
./start.sh
```

**方式二：手动启动**

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动服务
python main.py
```

服务将在 `http://localhost:8000` 启动。

### API接口

#### 1. 健康检查

```bash
GET http://localhost:8000/health
```

#### 2. 简历分析

```bash
POST http://localhost:8000/api/analyze
Content-Type: application/json

{
  "job_description": "职位描述内容",
  "exploration_direction": "探索方向（如：1. 要求在大厂待过 2. 经历过上市 3. 无负面舆情）",
  "resume": "简历文本内容"
}
```

### 使用示例代码测试

```bash
python example_request.py
```

## 技术架构

### 模块设计

系统采用模块化设计，5个模型各司其职：

1. **模型1 - 简历解析器**
   - 提取个人信息
   - 解析工作经历
   - 结构化简历数据

2. **模型2 - 大厂判断器**（并发执行）
   - 分析每段工作经历
   - 判断公司规模和知名度
   - 基于配置的大厂标准

3. **模型3 - 上市经历判断器**（并发执行）
   - 分析在职时间与公司上市时间
   - 判断是否经历上市过程
   - 提供置信度评估

4. **模型4 - 负面舆情检索器**（并发执行）
   - 模拟深度搜索
   - 检测负面信息风险
   - 提供风险等级评估

5. **模型5 - 报告生成器**
   - 整合所有分析结果
   - 计算匹配分数
   - 生成专业评估报告

### 并发处理

模型2、3、4 使用 `ThreadPoolExecutor` 并发执行，提高分析效率。

## 配置说明

### OpenAI配置

```yaml
openai:
  api_key: "your-api-key"     # OpenAI API密钥
  model: "gpt-4o"             # 使用的模型
  temperature: 0.7            # 温度参数（0-1）
  max_tokens: 2000            # 最大token数
```

### API服务配置

```yaml
api:
  host: "0.0.0.0"            # 服务地址
  port: 8000                 # 服务端口
  debug: true                # 调试模式
```

### 并发配置

```yaml
concurrent:
  max_workers: 3             # 最大并发数
  timeout: 60                # 超时时间（秒）
```

## 注意事项

1. **API费用**：本项目使用ChatGPT-4o模型，会产生API调用费用
2. **响应时间**：完整分析一份简历需要调用5次GPT，可能需要30-60秒
3. **API Key安全**：请妥善保管您的OpenAI API Key，不要提交到代码仓库
4. **负面舆情检索**：当前为模拟实现，实际使用建议接入真实搜索引擎API

## 开发计划

- [ ] 接入真实搜索引擎API（负面舆情检索）
- [ ] 支持PDF/Word格式简历直接上传
- [ ] 添加结果缓存机制
- [ ] 支持批量分析
- [ ] 提供Web UI界面

## License

MIT

## 参考项目

- [BettaFish](https://github.com/666ghj/BettaFish)
