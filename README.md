# Pytest + Requests接口测试

## 一、接口测试基础

1. 定义：对系统间接口（API）进行测试，验证接口的请求参数、响应结果、状态码、性能等是否符合预期。
2. 核心目标
   - 功能验证：接口是否按文档返回正确结果
   - 兼容性：不同参数组合、数据格式的兼容性
   - 安全性：权限控制、敏感数据保护
   - 性能：响应时间、并发处理能力
3. 常用工具
   - 自动化：pytest + requests（Python）
   - 手动调试：Postman、Swagger、curl

## 二、核心工具与环境准备

### **必备库**

```cmd
pip install pytest requests pytest-html pytest-xdist  # 核心库+报告+并行执行
```

## **项目结构**

```plaintext
api-test-framework
├─ api/               # 接口封装层：统一管理 API 定义、请求逻辑
├─ config/            # 配置层：环境配置、全局参数
├─ data/              # 数据层：测试用例数据（JSON/YAML 等）
├─ logs/              # 日志层：记录测试过程、错误信息
├─ reports/           # 报告层：测试报告（Allure/Pytest HTML）
├─ tests/             # 用例层：测试用例组织（按模块/功能拆分）
│  └─ user/           # 业务模块：user 相关用例
├─ utils/             # 工具层：通用工具（断言、配置解析、日志、数据处理）
├─ conftest.py        # 全局 Fixture：pytest 钩子、公共前置/后置
├─ run.py             # 执行入口：触发测试、控制运行流程
└─ requirements.txt   # 依赖管理：项目所需 Python 库
```

**（一）api 目录**

- **作用**：封装接口请求逻辑，把接口的 URL、请求方法（GET/POST 等）、参数规则统一管理。
- **价值**：隔离接口变更影响，比如接口地址、入参格式调整，只需改这里，不用动测试用例。

**（二）config 目录**

- **作用**：存储环境配置（如测试环境 / 生产环境的域名）、全局参数（超时时间、日志级别） 。
- **价值**：通过配置文件快速切换环境、调整参数，不用硬编码在代码里。

**（三）data 目录**

- **作用**：存放测试用例数据，像 JSON 文件存登录、下单等场景的入参、预期结果 。
- **价值**：实现 “数据驱动测试”，新增用例只需加数据文件，不用改代码，方便维护多场景测试。

**（四）logs 目录**

- **作用**：记录测试过程日志，包含请求详情、报错堆栈、执行时间等 。
- **价值**：出问题时，通过日志快速定位是接口请求失败、断言不通过，还是环境问题。

**（五）reports 目录**

- **作用**：存储测试报告（如 HTML 报告、Allure 报告 ），可视化展示用例执行结果、通过率、耗时等。
- **价值**：直观呈现测试结论，方便团队协作（开发看报告定位问题、领导看结果做决策 ）。

**（六）tests 目录**

- **作用**：按业务模块（如 user 模块）组织测试用例，编写断言逻辑，调用 api 层封装的接口执行测试 。
- **价值**：清晰划分测试范围，找用例、维护用例更方便，比如改用户登录用例，就去 `tests/user` 目录找。

**（七）utils 目录**

- **作用**：放通用工具函数，像自定义断言（校验响应时间、特殊字段）、数据读取（解析 JSON/YAML ）、日志封装 。
- **价值**：避免重复造轮子，测试用例、其他模块可直接调用，减少代码冗余。

**（八）关键文件**

- **conftest.py**：定义 pytest 全局 / 局部前置后置逻辑（如初始化接口对象、统一加请求头 ），让测试用例复用环境准备、清理操作。
- **run.py**：测试执行入口，可指定运行参数（跑哪些用例、生成啥报告 ），一键触发测试。
- **requirements.txt**：记录项目依赖的 Python 库（如 pytest、requests ），方便在新环境快速安装依赖，复现项目。

**启动测试**

1. 执行 `run.py` 启动测试，`pytest` 框架接管流程。
2. `conftest.py` 里的 `Fixture` 自动执行，准备测试环境（如初始化接口、加载配置 ）。
3. `tests` 里的用例加载 `data` 数据，调用 `api` 层接口发请求，结合 `utils` 工具做断言。
4. `logs` 记录过程，`reports` 生成可视化结果，完成测试闭环。

这套结构让项目可扩展（新增接口、用例方便 ）、易维护（改配置 / 数据不影响代码 ），适配接口测试从简单到复杂场景需求。



## pytest Fixture

Fixture 是 pytest 框架的核心功能，用于**管理测试用例的前置条件（setup）和后置操作（teardown）**，实现代码复用、测试环境准备与清理等功能。

本质是 “可复用的函数 / 组件”，可以被测试用例或其他 fixture 调用。

### 1.定义 Fixture

用 `@pytest.fixture` 装饰器标记一个函数，即为 fixture：

```python
import pytest

@pytest.fixture
def demo_fixture():
    # 前置操作：如初始化资源、连接数据库、登录等
    print("执行前置操作")
    # 通过 yield 返回数据给测试用例（可选）
    yield "需要传递给用例的数据"
    # 后置操作：如关闭连接、清理数据等（测试用例执行后自动执行）
    print("执行后置操作")
```

### 2. 在测试用例中使用 Fixture

测试函数直接通过**参数名**引用 fixture（无需导入）：

```python
def test_example(demo_fixture):  # 参数名与 fixture 函数名一致
    print(f"接收 fixture 传递的数据：{demo_fixture}")
    assert 1 == 1
```

### 3.核心特性

#### 作用域

通过 `scope` 参数指定 fixture 的生效范围，减少重复执行（提升效率）：

- `scope="function"`：默认值，每个测试用例执行一次（前置 + 后置）。
- `scope="class"`：每个测试类中所有用例共享一次。
- `scope="module"`：每个模块（.py 文件）中所有用例共享一次。
- `scope="package"`：每个包（文件夹）中所有用例共享一次。
- `scope="session"`：整个测试会话（一次 pytest 执行）中所有用例共享一次。

#### 依赖传递：Fixture 之间的调用

Fixture 可以依赖其他 fixture，形成依赖链：

```python
@pytest.fixture
def user_info():
    return {"id": 1, "name": "test"}

@pytest.fixture
def order_info(user_info):  # 依赖 user_info fixture
    return {"order_id": 100, "user": user_info}

def test_order(order_info):
    assert order_info["user"]["name"] == "test"
```

#### 参数化 Fixture：动态生成数据

用 `params` 参数为 fixture 传入多组数据，实现 fixture 自身的参数化：

```python
@pytest.fixture(params=[1, 2, 3])  # 3组参数，fixture 会执行3次
def num_fixture(request):  # 通过 request 参数接收每组数据
    return request.param  # 返回当前参数

def test_num(num_fixture):
    assert num_fixture > 0  # 测试用例会执行3次，分别传入1、2、3
```

#### Fixture 的自动发现机制

- 定义在**测试文件（test_\*.py）** 中的 fixture，仅能被当前文件的用例使用。
- 定义在`conftest.py`文件中的 fixture：
  - 无需导入，可被同一目录及子目录的所有测试文件使用。
  - 用于存放项目级公共 fixture（如登录、数据库连接等），是 pytest 项目的最佳实践。

## pytest参数化数据驱动测试

先准备好一组测试数据（各种失败场景的条件），然后通过框架提供的参数化功能，让同一个测试逻辑自动根据每组数据执行一次。

把数据和测试逻辑分离：我们只需要定义一次测试步骤，框架会自动遍历所有数据，每次用一组数据运行这个测试步骤，相当于自动完成了多轮测试。

这种方式不需要手动写循环，而且每组数据的测试结果会单独呈现，能清晰看到每个场景的执行情况，既简化了代码，又方便定位问题。

相关代码

```python
@pytest.mark.parametrize(
    "fail_case",
    data_handler.load_json_cases("user_api", "user_login_test_cases.json")[1:],
    ids=lambda case: f"fail_{case['case_id']}_{case['title'][:10]}"
)
def test_post_user_login_fail(user_api, fail_case):
    """所有登录失败场景"""
    logger.info(f"执行测试用例: {fail_case['case_id']} - {fail_case['title']}")
    response = user_api.login(
        fail_case["data"]["userAccount"],
        fail_case["data"]["userPassword"]
    )

    assertions.assert_response_code(response, fail_case["expected_status"])
    assertions.assert_response_time(response, 1)

    error_json = response.json()
    error_msg = error_json.get("message", "")
    assertions.assert_equal(error_msg, "请求参数错误", "错误信息不一致")
```

