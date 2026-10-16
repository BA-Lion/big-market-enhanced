# big-market-enhanced

基于原 big-market 后端的增强仓库，用于 Bug 修复、业务流程优化和逐步升级。保留原有七模块、`cn.bugstack` 包名及 Maven 坐标 `cn.bugstack:big-market:1.1`。

原项目基线：`7e31b5374f4b889a9ea306d73a5623b1e49c786a`。已导入 382 个受版本控制文件；不包含原 Git 历史。原简介见 [upstream-readme.md](docs/upstream-readme.md)，初始化差异见 [.ai/doc/runtime-and-import.md](.ai/doc/runtime-and-import.md)。

## 当前验证范围

初始化已完成源码完整性和静态配置检查；**尚未完成实际编译、服务启动或业务联调**。离线 Maven 检查因本机未缓存 Boot 父 POM 而受阻。以下是后续可执行的本地准备路径，本次初始化没有执行启动、数据库导入或发布。

## 工程结构

| 模块 | 职责 |
| --- | --- |
| `big-market-app` | Spring Boot 启动、配置装配、资源和测试 |
| `big-market-trigger` | HTTP / Dubbo、MQ 消费和 XXL-Job 入口 |
| `big-market-domain` | 活动、策略、奖品、返利、积分、异步任务领域服务 |
| `big-market-infrastructure` | 仓储实现、MyBatis、Redis、消息和外部网关 |
| `big-market-api` | 对外服务接口与 DTO，独立 POM |
| `big-market-querys` | 查询侧模型和仓储接口（沿用原拼写） |
| `big-market-types` | 公共类型、异常、注解、常量 |
| `docs/dev-ops` | SQL、容器和历史运维资料 |
| `.ai` | 项目画像、约束、任务和验证证据 |

## 本地构建

基线使用 **JDK 8**、Maven 3.8+、UTF-8。Windows 统一通过 `scripts/java8.ps1` 自动选用已安装的 Java 8 和 Maven，保留全局 JDK 17；无需每次新开终端手动切换环境。`.sh` 脚本需要 Git Bash / WSL。无需改包名、改模块名或转换 Java 源文件。

在仓库根目录执行：

```powershell
& .\scripts\java8.ps1 -Action Check
& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B', '-ntp', 'clean', 'package', '-DskipTests')
```

产物为 `big-market-app/target/big-market-app.jar`。`-DskipTests` 跳过执行但仍编译测试；`-Dmaven.test.skip=true` 才会同时跳过测试编译。依赖必须能够从配置的 Maven 仓库下载，包括 db-router 和 business-behavior-monitor SDK。尚未提供 Maven Wrapper，需自行安装 Maven。这里的 java8.ps1 是选择 JDK 和调用已安装 Maven 的项目脚本，不负责下载 Maven。具体安装路径默认值在脚本中；可通过 -JdkHome/-MavenHome 或 BIG_MARKET_JAVA_HOME/BIG_MARKET_MAVEN_HOME 覆盖，优先级为参数、项目变量、默认值。完整步骤见 [Java 8 调用流程](.ai/doc/java8-workflow.md)。

无需中间件的结构检查：

```powershell
python .ai/test/script/validate_harness.py
python .ai/test/script/validate_initialization.py
# Docker Compose 配置解析，不连接守护进程、不启动容器
# 需要 Docker Desktop 提供的 Compose v2+ 或兼容版本
docker compose -f docs/dev-ops/docker-compose-local.yml config --quiet
```

## 本地运行准备

准备 Docker Desktop 的 Linux containers 环境。应用在宿主机运行，使用新增的 local Compose；历史 `docker-compose-environment*.yml` 和 `docker-compose-app.yml` 保留供参考，不是本仓库默认启动入口。

```powershell
# 以下命令会启动中间件，并在全新 MySQL 数据卷内导入示例 SQL
docker compose -f docs/dev-ops/docker-compose-local.yml up -d
# 检查服务状态和 MySQL 初始化日志
docker compose -f docs/dev-ops/docker-compose-local.yml ps
docker compose -f docs/dev-ops/docker-compose-local.yml logs mysql
```

local Compose 绑定本机回环地址，创建项目独立数据卷，包含：

| 服务 | 宿主机端口 | 用途 |
| --- | --- | --- |
| MySQL 8.0.32 | 13306 | big_market、big_market_01、big_market_02、xxl_job |
| Redis 6.2 | 16379 | 缓存、库存、策略装配 |
| RabbitMQ 3.12.9 | 5672 / 15672 | 业务消息 / 管理界面 |
| Elasticsearch 7.17.14 | 9200 | 查询侧；与 JDBC 驱动版本一致 |
| XXL-Job 2.4.1 | 9090 | 调度管理，应用执行器默认 9999 |

MySQL 初始化 SQL 只会在空数据卷首次启动时执行，包含建库、删表及样例数据，勿导入已有业务库。不要通过删除卷来处理普通启动问题。

XXL-Job 管理端在容器中，需要回调宿主机的执行器。Windows Docker Desktop 可这样设置；实际任务运行前，在管理端检查原有任务、执行器组和启用状态：

```powershell
$env:XXL_JOB_EXECUTOR_ADDRESS = 'http://host.docker.internal:9999/'
& .\scripts\java8.ps1 -Action Run
```

只预览而不启动时，执行 `& .\scripts\java8.ps1 -Action Run -DryRun`。脚本前台运行，完成后恢复原 JAVA_HOME、PATH 和工作目录；不修改全局配置。

应用默认监听 `http://localhost:8098`，API 前缀 `/api/v1/raffle/`。可先访问 `/actuator/health` 检查状态。这个地址只有完成上述启动后才可访问，本次未实际访问。

## 配置与凭证

通用配置在 `big-market-app/src/main/resources/application.yml`，默认激活 dev。test/prod 覆盖部署端点并要求显式提供凭证，不再连接原项目机器。部署用的 MySQL URL 要分别指向基础库及两个分库。

| 环境变量 | dev 默认值或说明 |
| --- | --- |
| `SPRING_PROFILES_ACTIVE` / `SERVER_PORT` | dev / 8098（test 8099，prod 8092） |
| `MYSQL_HOST` / `MYSQL_PORT` | 127.0.0.1 / 13306 |
| `MYSQL_USERNAME` / `MYSQL_PASSWORD` | root / 123456，仅本地示例 |
| `MYSQL_DB00_URL` / `MYSQL_DB01_URL` / `MYSQL_DB02_URL` | test/prod 必填，各自完整 JDBC URL |
| `RABBITMQ_HOST` / `RABBITMQ_PORT` | 127.0.0.1 / 5672 |
| `RABBITMQ_USERNAME` / `RABBITMQ_PASSWORD` | admin / admin，仅本地示例 |
| `REDIS_HOST` / `REDIS_PORT` | 127.0.0.1 / 16379；test/prod 默认端口 6379 |
| `ELASTICSEARCH_JDBC_URL` | jdbc:es://http://127.0.0.1:9200 |
| `DUBBO_REGISTRY_ADDRESS` | N/A（本地不依赖 Nacos） |
| `ZOOKEEPER_ENABLE` / `ZOOKEEPER_ADDRESS` | false / 127.0.0.1:2181 |
| `XXL_JOB_ADMIN_ADDRESS` / `XXL_JOB_ACCESS_TOKEN` | 本地 9090/xxl-job-admin / default_token |
| `XXL_JOB_EXECUTOR_ADDRESS` / `XXL_JOB_EXECUTOR_IP` / `XXL_JOB_EXECUTOR_PORT` | 空 / 空 / 9999，注册地址须可被管理端访问 |
| `GATEWAY_API_HOST` / `GATEWAY_APP_ID` / `GATEWAY_APP_TOKEN` | 本地 8091 / big-market / 示例 token；账户奖品需真实兼容网关 |
| `INBOUND_APP_TOKEN` | `chatgpt-data` 调用方的本地示例 token，部署时覆盖 |

可在根目录创建被忽略的 `config/application-dev.yml`，使用标准 Spring 配置键覆盖本地设置。`.env` 由 Docker Compose 使用，`java -jar` **不会自动加载**它；若修改中间件口令，要同步设置当前 PowerShell 的对应环境变量。RedisClientConfig 的密码设置在上游被注释，带密码 Redis 的接入需后续单独修改。

## 测试与联调边界

默认跳过测试执行；原有测试主要是 JUnit 4 + SpringBootTest，依赖中间件，部分会修改数据或使用 CountDownLatch 永久等待。先检查目标测试，再在准备好的环境中选择单个测试，例如：

```powershell
& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B', '-ntp', '-pl', 'big-market-app', '-am', 'test', '-DskipTests=false', '-Dtest=AwardDaoTest', '-Dsurefire.failIfNoSpecifiedTests=false')
```

示例 SQL 的活动 `100401` 已于 2026-10-06 到期，不能直接作为当前抽奖成功的验收数据；`100301` 截止 2034-03-09。实际抽奖前先核实活动、SKU 与策略关系并调用相应 armory 接口。

外部账户调额服务、前端、ES 订单索引和 Canal 同步不属于 local Compose 的完整链路。ES SQL JDBC 使用本地 trial 许可，许可到期及索引准备需另行处理；见 [Elastic 文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/sql-jdbc.html)。`gateway.config.enable` 在现有实现中不能禁用远程发奖，不要用它判断外部奖品是否可用。

## 开发协作

先读 [AGENTS.md](AGENTS.md) 和 [.ai/index.md](.ai/index.md)，项目事实以 [.ai/project.md](.ai/project.md) 为入口。风险、验证限制及后续工作均有索引。

原发布和外部代码审查工作流改为手动触发；内部仍保留上游账号、镜像和第三方服务配置，重新配置前不要执行。构建自己的本地镜像可在打包后执行 `docker build -t big-market-enhanced:local big-market-app`；容器运行需要重新配置宿主机/服务网络地址。

原作者信息和源码版权声明保持原样，根 POM 标注 Apache-2.0；源快照未包含 LICENSE 正文，本次不额外推断或变更授权范围。
