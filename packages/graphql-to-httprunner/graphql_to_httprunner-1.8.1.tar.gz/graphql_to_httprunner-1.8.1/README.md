# GraphQL to HttpRunner

[graphql-to-httprunner](https://pypi.org/project/graphql-to-httprunner)，一个基于GraphQL Schema自动生成HttpRunner测试用例的自动化工具。

## 一、主要功能
1. 支持直接解析GraphQL Schema文件，提取查询操作和类型定义
2. 支持通过内省查询(Introspection Query)自动获取GraphQL Schema
3. 支持为每个查询操作生成对应的HttpRunner测试用例
4. 自动构建GraphQL查询语句，包括字段选择、参数处理、以及默认值生成
5. 自动化生成合适的通用测试断言
6. 一键直接生成GraphQL查询语句列表，方便开发调试
7. 支持API层和用例层测试用例生成，满足HttpRunner分层测试需求
8. 支持测试用例生成时选择全量参数或仅必选参数
9. 支持测试用例生成时是否包含skip关键字，方便用例执行
10. 支持多项目批处理模式、单项目处理模式、单个查询处理模式
11. 支持生成GraphQL查询语句时自动备份和差异对比，方便追踪API变更
12. 支持根据GraphQL查询语句差异报告自动更新测试用例，提升维护效率

## 二、代码结构
项目采用模块化设计，主要包含以下文件：

### 核心模块
- `graphql_to_httprunner/models.py`: 数据模型模块，定义了GraphQL Schema的核心数据结构
  - `GraphQLType`: 表示GraphQL类型，包含字段和实现接口信息
  - `GraphQLSchema`: 表示整个Schema，包含类型、接口和根字段

- `graphql_to_httprunner/parser.py`: 解析器模块，负责解析GraphQL Schema文件
  - `GraphQLSchemaParser`: 解析GraphQL Schema的内容，提取类型、接口、枚举等信息

- `graphql_to_httprunner/introspection.py`: 内省查询模块，通过内省查询获取GraphQL Schema
  - `fetch_schema_from_introspection`: 向GraphQL服务发送内省查询请求，获取Schema

- `graphql_to_httprunner/generator.py`: 生成器模块，负责生成HttpRunner测试用例
  - `HttpRunnerTestCaseGenerator`: 根据Schema生成HttpRunner YAML测试用例，同时支持生成API层和用例层测试用例

- `graphql_to_httprunner/query_generator.py`: 查询语句生成器模块，负责生成GraphQL查询语句列表
  - `GraphQLQueryGenerator`: 根据Schema生成GraphQL查询语句

- `graphql_to_httprunner/report_generator.py`: 查询语句文件差异报告生成模块，用于在GraphQL Schema发生变更时生成详细的差异比较报告
  - `generate_markdown_diff_report`: Markdown格式的差异报告生成
  - `generate_html_diff_report`: HTML格式的差异报告生成

### 工具模块
- `graphql_to_httprunner/main.py`: 程序入口模块，提供命令行界面，协调调用解析器和生成器
- `graphql_to_httprunner/utils.py`: 工具类模块，提供文件备份和差异比较等通用功能
  - `backup_queries_file`: 备份查询语句文件
  - `compare_query_files`: 比较新旧查询语句文件的差异并生成报告
- `graphql_to_httprunner/__main__.py`: 包根目录入口点，允许直接模块运行
- `graphql_to_httprunner/__init__.py`: 包初始化文件，提供模块导入接口
- `__main__.py`: 项目根目录入口点，允许直接运行项目

### 项目结构
```
graphql-schema-to-httprunner/
├── graphql_to_httprunner/        # 主包目录
│   ├── __main__.py               # 主包目录入口点
│   ├── __init__.py               # 包初始化文件
│   ├── models.py                 # 数据模型模块
│   ├── parser.py                 # 解析器模块
│   ├── introspection.py          # 内省查询模块
│   ├── generator.py              # 生成器模块
│   ├── query_generator.py        # 查询语句生成器模块
│   ├── report_generator.py       # 查询语句文件差异报告生成器模块
│   ├── utils.py                  # 工具函数模块
│   └── main.py                   # 命令行入口模块
├── tests/                        # 单元测试目录
├── __main__.py                   # 项目根目录入口点
├── pyproject.toml                # 项目配置文件
├── setup.py                      # 兼容旧式安装的配置文件
├── MANIFEST.in                   # 指定打包时要包含和排查的文件
└── README.md                     # 项目说明文档
```

## 三、安装方法

### 3.1 使用pip安装（推荐）
```bash
# 从PIPY仓库安装
pip install graphql-to-httprunner

# 或者从Git仓库安装
pip install git+https://git.umlife.net/zhangchuzhao/graphql-schema-to-httprunner.git
```

### 3.2 开发模式安装
```bash
# 从本地源码安装
pip install .

# 使用pip开发模式安装
pip install -e .

# 或者使用poetry安装
poetry install
```

## 四、使用方法

### 4.1 命令行使用（推荐）

安装后可以直接使用`gpl2hrun`或`gpl2case`或`graphql2httprunner`或`graphql2testcase`命令：

```bash
# 基于schema.graphql文件生成HttpRunner用例层测试用例
gpl2hrun -f schema.graphql -t -o testcases -u http://your-api-url -d 2

# 基于内省查询URL生成HttpRunner用例层测试用例
gpl2hrun -i http://your-graphql-server/graphql -t -o testcases -u http://your-api-url -d 2

# 基于schema.graphql文件生成HttpRunner API层测试用例
gpl2hrun -f schema.graphql -t --api -o api -u http://your-api-url -d 2

# 基于内省查询URL生成HttpRunner API层测试用例
gpl2hrun -i http://your-graphql-server/graphql -t --api -o api -u project_name -d 2

# 基于schema.graphql文件生成HttpRunner用例层测试用例（仅包含必选参数）
gpl2hrun -f schema.graphql -t -o testcases --required

# 基于schema.graphql文件生成HttpRunner API层测试用例（仅包含必选参数）
gpl2hrun -f schema.graphql -t --api -o api --required

# 基于schema.graphql文件生成HttpRunner API层测试用例（包含关键字参数skip）
gpl2hrun -f schema.graphql -t --api -o api --skip

# 基于schema.graphql文件生成HttpRunner API层测试用例，同时生成引用API的测试用例
gpl2hrun -f schema.graphql -t --api -o api --cite

# 基于schema.graphql文件生成GraphQL查询语句
gpl2hrun -f schema.graphql -q

# 基于schema.graphql文件生成GraphQL查询语句，并默认与旧查询语句文件query.yml进行对比生成差异报告
gpl2hrun -f schema.graphql -q --report

# 基于schema.graphql文件生成GraphQL查询语句，并指定项目名查询语句文件分组标识
gpl2hrun -f schema.graphql -q --project project_name

# 基于内省查询URL生成GraphQL查询语句
gpl2hrun -i http://your-graphql-server/graphql -q -o my.yml -u http://your-api-url -d 2

# 基于内省查询URL生成GraphQL查询语句，并与指定与my.yml进行对比生成差异报告
gpl2hrun -i http://your-graphql-server/graphql -q -o my.yml -u http://your-api-url -d 2

# 使用配置文件批量生成多个项目的HttpRunner测试用例
gpl2hrun -b config.csv -t

# 使用配置文件批量生成多个项目的GraphQL查询语句列表，生成路径默认为query.yaml
gpl2hrun -b config.csv -q

# 使用配置文件批量生成多个项目的GraphQL查询语句列表，并默认与旧查询语句文件query.yaml进行对比生成差异报告
gpl2hrun -b config.csv -q --report

# 使用配置文件批量生成多个项目的GraphQL查询语句列表，生成路径指定为my_query.yaml
gpl2hrun -b config.csv -q --queries-file my_query.yaml

# 使用配置文件批量生成多个项目的GraphQL查询语句列表，并与指定my_query.yaml进行对比生成差异报告
gpl2hrun -b config.csv -q --queries-file my_query.yaml --report

# 根据配置文件和查询语句差异报告自动更新HttpRunner测试用例，查询语句文件默认为query.yaml
gpl2hrun -b config.csv -a

# 根据配置文件和查询语句差异报告自动更新HttpRunner测试用例，查询语句文件指定为my_query.yaml
gpl2hrun -b config.csv -a --queries-file my_query.yaml

# 基于内省查询URL生成操作名称 xxx 的HttpRunner用例层测试用例
gpl2hrun -i http://localhost:8888/graphql -t --query-name xxx

# 基于内省查询URL生成操作名称 xxx 的查询语句
python . -i http://localhost:8888/graphql -q --project swapi --query-name xxx
```

配置文件格式为CSV，包含以下列：
```
project_name,introspection_url,output,base_url,max_depth,required,api,is_cite,is_skip,offline
swapi,http://localhost:8888/graphql,swapi,http://localhost:8888,2,false,false,false,false,false
youcloud,https://example-youcloud.com/graphql,youcloud,youcloud,5,true,true,false,true,false
project3,https://example-project2.com/graphql,project3,project3,6,true,true,true,true,true
```

- `project_name`: 项目名称，用于标识和日志输出
- `introspection_url`: GraphQL内省查询URL
- `output`: 输出目录路径，批量生成GraphQL查询语句时默认为query.yaml
- `base_url`: GraphQL API基础URL
- `max_depth`: GraphQL查询嵌套的最大深度
- `required`: 是否只包含必选参数，值为"true"或"false"
- `api`: 是否生成API层测试用例，值为"true"或"false"
- `is_cite`: 是否生成引用API层的测试用例，值为"true"或"false"
- `is_skip`: 是否生成测试用例是否包含skip关键词，值为"true"或"false"
- `offline`: 项目是否已下线，值为"true"或"false"，批处理时会跳过已下线项目

### 4.2 源码执行使用方式

如果没有通过pip安装，或者需要直接运行源码，可以使用以下方式：

```bash
# 使用根目录的__main__.py入口点（省略模块/指定模块）
python . -f schema.graphql -t -o testcases -u http://your-api-url -d 2
python __main__.py -f schema.graphql -t -o testcases -u http://your-api-url -d 2

# 使用包目录__main__.py入口点
python -m graphql_to_httprunner -f schema.graphql -t -o testcases -u http://your-api-url -d 2

# 使用graphql_to_httprunner/main.py入口点
python -m graphql_to_httprunner.main -f schema.graphql -t -o testcases -u http://your-api-url -d 2
```

### 4.3 代码模块使用方式

```python
from graphql_to_httprunner.parser import GraphQLSchemaParser
from graphql_to_httprunner.generator import HttpRunnerTestCaseGenerator

# 解析GraphQL Schema文件
with open('schema.graphql', 'r') as f:
    schema_content = f.read()
    
parser = GraphQLSchemaParser(schema_content)
schema = parser.parse()

# 生成测试用例
generator = HttpRunnerTestCaseGenerator(schema, base_url="http://your-api-url")
testcase_count = generator.generate_test_cases("testcases")
print(f"已生成{testcase_count}个测试用例")
```

### 4.4 参数说明
```bash
gpl2hrun -h

usage: gpl2hrun [-h] [-V] [-b BATCH] [-f SCHEMA_FILE | -i INTROSPECTION_URL] [-t | -q] [-o OUTPUT] [-u BASE_URL] [-d MAX_DEPTH] [--api] [--required] [-a] [--queries-file QUERIES_FILE]

将GraphQL Schema转换为HttpRunner测试用例或查询语句

optional arguments:
  -h, --help
  -V, --version
  -b BATCH, --batch BATCH
  -f SCHEMA_FILE, --schema-file SCHEMA_FILE
  -i INTROSPECTION_URL, --introspection-url INTROSPECTION_URL
  -t, --testcases
  -q, --queries
  -o OUTPUT, --output OUTPUT
  -u BASE_URL, --base-url BASE_URL
  -d MAX_DEPTH, --max-depth MAX_DEPTH
  --api
  --cite
  --required
  --skip
  --report
  --project
  -a, --auto-update
  --queries-file QUERIES_FILE
  --query-name QUERY_NAME
```

- `-b, --batch`: 批量处理配置文件路径，如 config.csv
- `-f, --schema-file`: GraphQL Schema文件路径
- `-i, --introspection-url`: GraphQL内省查询URL，如 http://localhost:9527/graphql
- `-t, --testcases`: 生成HttpRunner测试用例
- `-q, --queries`: 生成GraphQL查询语句列表
- `--api`: 生成API层测试用例而非用例层测试用例（仅当使用 `-t` 时有效）
- `--cite`: 生成引用API层测试用例（与--api选项一起使用）
- `--required`: 只包含必选参数，默认情况下包含所有参数（仅当使用 `-t` 时有效）
- `--skip`: 生成的测试用例是否包含skip关键词（仅当使用 `-t` 时有效）
- `--report`: 与旧查询语句文件对比生成差异报告（与-q选项一起使用），单项目模式默认与query.yaml对比或通过-o参数指定，批处理模式默认与query.yaml对比或通过--queries-file参数指定
- `-o, --output`: 生成结果输出路径，根据生成类型默认为api、testcases、query.yml三种情况（注意：批模式生成Graphql查询语句时默认为query.yaml，以便适配现有脚本引用方式）
- `-u, --base-url`: API基础URL或项目名，项目名用来作为自定义函数参数生成API基础URL，默认为'http://localhost:8888'
- `-d, --max-depth`: GraphQL查询嵌套的最大深度，默认为2
- `--project`: 指定项目名称，作为生成查询语句文件分组标识，默认为project_name
- `-a, --auto-update`: 根据GraphQL查询语句差异报告自动更新测试用例（需与 `-b` 一起使用）
- `--queries-file`: 查询语句文件输出或获取路径，默认为query.yaml (与-b选项一起使用)
- `--query-name`: 指定要生成的单个查询名称，只生成该查询的测试用例或查询语句

> 注意：
> - 当指定 `-b/--batch` 参数时，工具将进入批处理模式，从配置文件中读取多个项目信息进行批量处理
> - 批处理模式下，可以同时指定 `-t/--testcases` 或 `-q/--queries` 选项来指定生成测试用例或查询语句
> - 单个项目模式下（不使用 `-b/--batch`），必须指定 `-f/--schema-file` 或 `-i/--introspection-url` 选项，且必须指定 `-t/--testcases` 或 `-q/--queries` 选项
> - `-f` 和 `-i` 是互斥参数，只能二选一使用
> - `-t` 和 `-q` 是互斥参数，只能二选一使用
> - 如果使用 `-t` 选项，则 `-o` 参数指定输出目录；如果使用 `-q` 选项，则 `-o` 参数指定输出文件路径
> - `--api` 参数仅在 `-t` 参数存在时有效，用于指定生成API层测试用例
> - `--cite` 参数仅在 `-t`和`--api` 参数存在时有效，用于指定生成引用API层测试用例
> - `--required` 参数仅在 `-t` 参数存在时有效，用于指定只包含必选参数
> - `--skip` 参数仅在 `-t` 参数存在时有效，用于指定生成的测试用例是否包含skip关键词
> - `--report` 参数仅在 `-q` 参数存在时有效，用于与旧查询语句文件对比生成差异报告

### 4.5 执行HttpRunner测试用例
```bash
# 运行用例层测试用例
hrun testcases
# 运行API层测试用例
hrun api
```

### 4.6 打包上传PyPI
```bash
# 打标签（轻量或附注）
git tag v1.0.0 或 git tag -a v1.0.0 -m "发布正式版本 v1.0.0"
# 推送标签(单个或所有)
git push v1.0.0 或 git push --tags
# 本地配置pyproject.toml和pypi token信息
poetry config pypi-token xxx
# 编译打包(更新__init__.py和pyproject.toml中版本号)
poetry build
# 上传发布
poetry publish
```


## 五、注意事项
1. 测试用例中使用$$来转义$符号，以避免与HttpRunner变量语法冲突；
2. HttpRunner接口响应内容引用变量约定为content；
3. 内省查询需要目标GraphQL服务支持标准的内省查询API；
4. 内省查询URL与基础URL不同，分别使用 `-i` 和 `-u` 参数指定；
5. 生成的查询语句列表以YAML格式存储，键为操作名称，值为对应的查询语句；

## 六、查询语句备份与差异对比功能

### 6.1 自动备份功能
当用户执行生成GraphQL查询语句列表任务（使用`-q`参数）时，工具会自动检查是否存在旧的查询语句文件。如果存在，将自动执行以下操作：

1. 将旧文件备份为带时间戳的文件，格式为`文件名.bak.时间戳.扩展名`（例如：`query.yml.bak.20240501123456.yml`）
2. 删除旧的查询语句文件
3. 生成新的查询语句文件
4. 自动执行新旧文件差异对比

这种自动备份机制适用于单项目模式和批处理模式：
- 单项目模式下，备份指定的输出文件，默认为`query.yml`
- 批处理模式下，备份默认`query.yaml`文件

### 6.2 差异对比报告
差异对比功能会自动分析新旧查询语句文件的差异，并生成一份详细的Markdown格式报告和一份详细的HTML格式报告。该报告包含以下信息：

1. **项目级变更**：新增项目、移除项目
2. **查询级变更**：针对每个修改的项目，详细列出新增查询、移除查询和修改查询
3. **详细差异**：对于修改的查询，提供旧值、新值以及详细的文本差异对比

差异报告文件格式为`文件名.时间戳.diff.md`（例如：`query.yml.20240501123456.diff.md`）和`文件名.时间戳.diff.html`（例如：`query.yml.20240501123456.diff.html`）。

### 6.3 差异对比示例

下面是一个Markdown格式差异报告的示例片段：

````markdown
# GraphQL API 变更监测报告
## 旧文件: query.yaml.bak.20240501123456.yaml
## 新文件: query.yaml

## 新增项目
- project_new

## 修改项目
### youcloud
#### 新增查询
- getNewFeature
  ```
  query getNewFeature {
    newFeature {
      id
      name
    }
  }
  ```

#### 修改查询
- getUserInfo
  旧:
  ```
  query getUserInfo {
    user {
      id
      name
    }
  }
  ```
  新:
  ```
  query getUserInfo {
    user {
      id
      name
      email
    }
  }
  ```
  差异详情:
  ```diff
    query getUserInfo {
      user {
        id
        name
  +     email
      }
    }
  ```
````

通过这个差异报告，用户可以清晰地了解随着API升级和迭代，查询语句发生了哪些变化，便于进行API变更管理和测试用例维护。

### 6.4 工具类模块

为了增强代码的可维护性和模块化，项目将文件备份和差异比较功能抽离到了单独的工具类模块(`utils.py`)，主要提供以下功能：

- `backup_queries_file`：负责将现有查询语句文件备份为带时间戳的文件，并删除原文件
- `compare_query_files`：负责比较新旧查询语句文件的差异，并生成详细的Markdown格式差异报告

这些工具函数使项目更加模块化，便于维护和扩展。

## 七、测试用例自动更新功能

随着产品迭代和API变更，GraphQL查询语句会不断更新，导致已生成的HttpRunner测试用例需要手动更新。为了解决这个问题，项目实现了测试用例自动更新功能，能够根据查询语句的差异报告自动更新相应的测试用例文件。

### 7.1 自动更新流程

测试用例自动更新功能的工作流程如下：

1. 备份现有的查询语句文件
2. 根据配置文件重新生成最新的查询语句
3. 比较新旧查询语句文件，生成差异报告
4. 根据差异报告自动处理以下变更:
   - 新增项目：自动生成新项目的所有测试用例
   - 移除项目：自动删除该项目的测试用例目录
   - 修改项目：
     - 新增查询：自动生成新增查询的测试用例
     - 移除查询：自动删除对应的测试用例文件
     - 修改查询：自动更新测试用例中的查询语句

### 7.2 使用方法

使用自动更新功能需要提供配置文件和查询语句文件：

```bash
# 使用默认查询语句文件(query.yaml)
gpl2hrun -b config.csv -a

# 指定查询语句文件
gpl2hrun -b config.csv -a --queries-file custom_queries.yaml
```

### 7.3 注意事项

1. 自动更新功能**必须**与批处理模式(`-b/--batch`)一起使用
2. 配置文件需要包含项目名称、内省查询URL、输出目录等信息
3. 查询语句文件应当包含所有项目的最新查询语句
4. 自动更新过程中如果遇到错误，会尽可能继续处理其他项目和查询
5. 自动更新完成后会输出统计信息，包括新增项目、移除项目、新增查询、移除查询和修改查询的数量
6. 自动更新会保留测试用例中的其他配置和参数值，只更新查询语句部分，不影响已有的自定义配置

### 7.4 工具函数

项目添加了以下工具函数以支持测试用例自动更新功能：

- `find_testcase_files`：查找与指定查询对应的测试用例文件
- `delete_testcase_files`：删除与指定查询对应的测试用例文件
- `update_testcase_query`：更新测试用例文件中的查询语句
- `determine_operation_type`：根据查询语句确定操作类型
- `auto_update_testcases`：根据差异报告自动更新测试用例

通过这些功能，可以大幅提高API测试用例的维护效率，解决GraphQL API变更导致的测试用例失效问题。


## 八、单元测试
项目包含完整的单元测试套件，覆盖所有核心模块功能。

### 8.1 运行测试
```bash
# 安装测试依赖
poetry add -D pytest requests-mock pytest-cov

# 运行所有测试
pytest

# 运行特定模块的测试
pytest tests/test_models.py

# 运行测试并生成覆盖率报告
pytest --cov=graphql_to_httprunner

# 生成HTML格式覆盖率报告
pytest --cov=graphql_to_httprunner --cov-report=html
```
### 8.2 测试文件结构
```
tests/                          # 测试目录
├── conftest.py                # 测试配置文件，定义测试夹具
├── fixtures/                  # 测试数据目录
│   └── schema.graphql        # 测试用的GraphQL Schema
├── test_models.py            # 数据模型测试
├── test_parser.py            # Schema解析器测试
├── test_introspection.py     # 内省查询测试
├── test_generator.py         # 测试用例生成器测试
├── test_query_generator.py   # 查询语句生成器测试
├── test_report_generator.py  # 差异报告生成器测试
└── test_utils.py             # 工具函数测试
```
