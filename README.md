# API测试框架

一个功能完善的Python接口测试框架，支持自动化测试、数据驱动、多环境配置等功能。

## 项目特点

- 基于pytest框架，支持丰富的测试用例组织方式
- 完整的HTTP请求封装，支持RESTful API测试
- 多环境配置管理，轻松切换开发、测试、生产环境
- 强大的断言工具，支持响应状态码、响应体、JSON路径等多种断言
- 数据驱动测试，支持从JSON、YAML、CSV文件读取测试数据
- 自动生成测试报告（HTML报告和Allure报告）
- 支持测试用例并行执行，提高测试效率
- 完善的日志系统，便于问题定位
- 内置重试机制，提高测试稳定性
- 支持CI/CD集成

## 环境准备

### 前置条件

- Python 3.8+
- pip（Python包管理工具）

### 安装依赖
pip install -r requirements.txt
### 环境配置

1. 复制环境变量示例文件并修改：
cp .env.example .env
2. 根据需要修改`config`目录下的环境配置文件

## 运行测试

### 基本用法
# 运行所有测试用例
python run.py

# 在指定环境运行测试
python run.py --env test

# 运行冒烟测试用例
python run.py --markers "smoke"

# 运行高优先级用例
python run.py --markers "high"

# 并行执行测试（4个进程）
python run.py --parallel 4

# 生成Allure报告
python run.py --allure
### 查看报告

- HTML报告：`reports/pytest_report.html`
- Allure报告：`reports/allure_report/index.html`（需要先安装Allure）

## 项目结构
api_test_framework/
├── api/                  # 接口封装层
├── config/               # 配置文件
├── data/                 # 测试数据
├── logs/                 # 日志文件
├── reports/              # 测试报告
├── tests/                # 测试用例
│   ├── __init__.py
│   ├── conftest.py       # pytest fixtures
│   └── test_demo.py      # 示例测试用例
├── utils/                # 工具类
├── .env.example          # 环境变量示例
├── .gitignore
├── pytest.ini            # pytest配置
├── requirements.txt      # 依赖包
├── run.py                # 运行入口
└── README.md             # 项目说明
## 扩展指南

### 添加新接口

1. 在`api`目录下创建新的接口类，继承`BaseAPI`
2. 实现接口方法，封装请求细节

### 添加新测试用例

1. 在`tests`目录下创建`test_*.py`文件
2. 使用pytest风格编写测试函数
3. 可使用`conftest.py`中定义的fixture

### 添加测试数据

1. 在`data`目录下添加JSON/YAML/CSV文件
2. 使用`data_handler`工具类读取数据

## CI/CD集成

示例GitHub Actions配置（.github/workflows/test.yml）：
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python run.py --env test --parallel 4 --allure
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/