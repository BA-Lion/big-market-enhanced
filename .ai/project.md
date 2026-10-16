---
type: project-profile
status: initialized
updated: 2026-10-16
---

# 项目概况

## 项目目标

- 本仓库 big-market-enhanced 用于基于原 big-market 修复 Bug、优化业务流程并逐步升级，不是原项目学习笔记目录。
- 主要用户：本项目维护者及使用抽奖活动、签到返利、积分兑换、奖品发放和运营查询接口的应用。
- 当前阶段：基线导入与仓库初始化已完成；实际构建、启动及端到端联调尚未验证，下一阶段由用户指导。
- 原始源码来自相邻仓库 `../all-big-market/big-market`（相对本仓库根目录），提交 `7e31b5374f4b889a9ea306d73a5623b1e49c786a`。导入 382 个跟踪文件；保留本仓库独立 Git；初始化已形成提交 f3200cf，后续工具变更以当前工作树为准。
- 来源、转换清单和证据统一保存在 [导入与运行说明](doc/runtime-and-import.md)，不把初始化工作树称作已验证发布版本。

## 技术栈

| 项目 | 当前代码/配置事实 |
| --- | --- |
| Java | 编译目标 Java 8（1.8），UTF-8；本次不升级 Java 大版本 |
| Spring Boot | 2.7.12，Spring MVC、AOP、Actuator；应用入口 cn.bugstack.Application |
| 构建 | Maven 多模块，父坐标 cn.bugstack:big-market:1.1；API 是独立 POM，版本同为 1.1 |
| 持久化 | MyBatis starter 2.1.4、MySQL Connector 8.0.23、HikariCP、db-router starter 1.0.4 |
| 数据库 | local Compose MySQL 8.0.32；基础库 big_market 和 big_market_01 / big_market_02 两分库，路由 2 库 × 4 表 |
| 缓存 | Redisson core 3.26.0，手动创建客户端；local Redis 6.2 |
| 消息 | Spring AMQP 版本由 Boot 2.7.12 管理；local RabbitMQ 3.12.9 |
| RPC/配置 | Dubbo 3.0.9、Nacos client 2.1.0；ZooKeeper/Curator 动态配置，默认关闭；本地 Dubbo registry 为 N/A |
| 查询 | Elasticsearch SQL JDBC 7.17.14；local ES 7.17.14，订单索引与同步需另行准备 |
| 调度 | XXL-Job core/admin 2.4.1，应用 executor 默认端口 9999 |
| 外部服务 | Retrofit 2.9.0；账户调额奖品依赖独立网关，源码不在本仓库 |
| 监控 | Actuator、Micrometer Prometheus、business-behavior-monitor-sdk 1.1；历史运维有 Grafana/Prometheus |
| 测试 | JUnit 4、SpringBootTest；Surefire 2.22.2 与 Vintage，默认跳过执行 |
| 部署 | 可执行 JAR、Java 8 Dockerfile；新增 local Compose 面向宿主机开发，不是生产拓扑 |

## 仓库地图

| 路径 | 职责 | 所有权或修改限制 |
| --- | --- | --- |
| `big-market-app/` | 启动、配置装配、Mapper XML、JUnit 测试 | 修改配置须保持 Bean 所需属性及 profile 完整 |
| `big-market-trigger/` | HTTP/RPC、MQ listener、XXL-Job handler | 接口、主题和任务名变更需明确兼容方案 |
| `big-market-domain/` | activity、strategy、award、rebate、credit、task 领域 | 不反向依赖应用和基础设施模块 |
| `big-market-infrastructure/` | 仓储、DAO/PO、Redis、事件与外部网关 | 保持数据路由、事务和幂等语义 |
| `big-market-api/` | 服务接口及 DTO | 独立 Maven 模块，发布插件未启用 |
| `big-market-querys/` | 查询模型及仓储接口 | 沿用原名称；不顺手重命名 |
| `big-market-types/` | 常量、异常、公共类型和注解 | 变动评估所有依赖模块 |
| `scripts/java8.ps1` | Windows Java 8 的 Check/Maven/Run 统一入口 | AI 本地构建与启动必须通过该入口 |
| `docs/dev-ops/mysql/sql/` | 表结构及种子数据、调度/注册库脚本 | 原始导入基线；不作为生产迁移脚本直接执行 |
| `docs/dev-ops/docker-compose-local.yml` | 推荐的本地中间件入口 | 应用运行在宿主机；不含全部扩展链路 |
| `docs/dev-ops/` 其他文件 | 历史部署、Canal、监控、curl 资料 | 包含旧端点；不可直接当成默认环境 |
| `.github/workflows/` | 原发布和外部代码审查工作流 | 仅手动触发，重新配置目标及凭证后才使用 |
| `.ai/` | 约束、方案、问题、验证和知识 | 遵循 readme 风险分级与模板，不保存凭证 |
| `AGENTS.md`、`README.md` | Agent 入口、面向开发者的准备说明 | 项目事实保持一致，命令以 README 为操作入口 |

## 标准命令

在仓库根目录执行；以下启动和测试命令是操作说明，不代表本次已运行。

**Windows AI 固定入口：[Java 8 调用流程](doc/java8-workflow.md)。每次构建、测试和启动都必须调用 scripts/java8.ps1，不得直接依赖系统 java/mvn。无需事先激活环境；新终端、重启后仍使用同一入口。首次先 Check，再根据授权执行 Maven 或 Run；仅预览时加 DryRun。脚本默认使用用户确认的 JDK 8 和 Maven 安装目录，支持参数或项目专用环境变量覆盖，完成后恢复调用者环境。**

| 用途 | 命令 | 前置条件 |
| --- | --- | --- |
| 工具确认 | `& .\scripts\java8.ps1 -Action Check`、`docker compose version` | Maven 使用 JDK 8 基线 |
| 依赖解析与打包 | `& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B','-ntp','clean','package','-DskipTests')` | Maven 可下载全部依赖；仍会编译测试 |
| 初始化结构检查 | `python .ai/test/script/validate_initialization.py` | Python 3.10+，标准库 |
| 导入逐文件对比 | `python .ai/test/script/validate_initialization.py --source ../all-big-market/big-market` | 原项目仍可只读访问，Git 在 PATH |
| Harness 校验 | `python .ai/test/script/validate_harness.py` | Python 3.10+，标准库 |
| Compose 静态检查 | `docker compose -f docs/dev-ops/docker-compose-local.yml config --quiet` | Compose v2+，不需要启动容器 |
| 启动本地中间件 | `docker compose -f docs/dev-ops/docker-compose-local.yml up -d` | Docker Linux containers；全新卷会自动导入 SQL |
| 预览启动 | `& .\scripts\java8.ps1 -Action Run -DryRun` | 仅检查并显示命令，不要求已有 JAR，不启动应用 |
| 启动应用 | `& .\scripts\java8.ps1 -Action Run` | JDK 8、已打包、MySQL/Redis/MQ/ES 就绪，XXL 回调地址已设置 |
| 单个集成测试 | `& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B','-ntp','-pl','big-market-app','-am','test','-DskipTests=false','-Dtest=AwardDaoTest','-Dsurefire.failIfNoSpecifiedTests=false')` | 中间件与种子数据就绪；先阅读目标测试 |
| 本地镜像构建 | `docker build -t big-market-enhanced:local big-market-app` | 已打包；不自动推送 |
| 格式化 | 尚无统一格式化插件；保持现有 Java 风格，UTF-8，文本换行由 .gitattributes 约束 | 不做无关的全仓格式重排 |
| 静态分析 | 尚未配置 Checkstyle、SpotBugs 或独立 Java 静态分析门禁 | 不把轻量结构脚本描述为 Java 静态分析 |
| 独立单元测试 | 尚未建立与外部服务隔离的独立测试套件 | 现有多数测试属于集成测试或手工实验 |

## 开发约束

- 兼容性目标：维持现有 Maven 坐标、包名、模块名、HTTP API、Dubbo、MQ 主题和任务处理器名称；架构基线见 [ARCH-0001](architecture/2026-10-16-module-baseline.md)。
- Java 工具入口：Windows 使用 scripts/java8.ps1；具体默认安装位置只保存在脚本中。参数 -JdkHome/-MavenHome 优先，其次 BIG_MARKET_JAVA_HOME/BIG_MARKET_MAVEN_HOME，不回退到全局 JDK 17。调用步骤以 [DOC-0002](doc/java8-workflow.md) 为准。
- 文件边界：原仓库只读；所有增强修改落在当前仓库。不复制源 `.git`、不覆盖用户修改；Git 提交、推送和发布按当次授权处理。
- 新增依赖：优先使用当前 Boot 版本管理，检查 Java 8/Boot 2.7 兼容性。生产依赖新增或大版本升级须在任务方案中明确，不为初始化直接迁到 Boot 3。
- 数据变更：分库分表、库存、账户额度、积分、发奖和消息补偿涉及一致性，不可未经评估改变。现有 SQL 是重建及样例脚本，不能充当无损迁移。
- 配置：通用默认值位于 application.yml，默认 dev；test/prod 显式注入端点与凭证。Spring 占位符保留到运行时，不进行 Maven 资源过滤。
- 安全与隐私：dev 仅有公开本地示例口令；部署环境用变量或被忽略的根 config 覆盖，禁止把真实令牌写入代码或 .ai。历史运维资料使用前核实并清理旧环境配置。
- 性能：现有线程池、连接池、缓存和库存算法是基线配置，没有建立性能 SLO 或跑过基准测试；不臆测吞吐或性能收益。
- 工作流：L0/L1/L2/L3 按 [harness](readme.md) 执行；本次初始化 L1，由同一模型实施，无单独 implementation。

## 权威资料入口

| 主题 | 权威位置 | 备注 |
| --- | --- | --- |
| 当前任务与授权 | 用户当前指令、[任务记录](task/current/2026-10-16-repository-initialization.md) | 本次只做静态可行初始化 |
| 产品目标 | 本文项目目标、用户后续指导 | 暂无独立正式 PRD，不补造需求 |
| API 契约 | `big-market-api/src/main/java/cn/bugstack/trigger/api/` 与 `big-market-trigger/src/main/java/cn/bugstack/trigger/http/` | 控制器行为需同时核实 |
| 数据模型 | `docs/dev-ops/mysql/sql/`、domain 模型、DAO/Mapper | 冲突时区分设计与实现，建立问题记录 |
| 部署配置 | application*.yml、local Compose、[README](../README.md) | 历史配置不等于推荐入口 |
| 团队开发规范 | [AGENTS.md](../AGENTS.md)、[readme.md](readme.md)、[模块边界](architecture/2026-10-16-module-baseline.md) | 没有额外已确认团队规范 |
| 导入变更 | [运行与来源](doc/runtime-and-import.md)、[方案](decision/2026-10-16-source-import.md) | 来源提交、转换和边界 |
| 已知问题与验证 | [问题](problem/2026-10-16-runtime-verification.md)、[证据](test/result/2026-10-16-initialization.md) | 静态通过与实际运行分开记录 |

## 专用 Skills 或工具

仓库未安装项目专用 Skill 或插件。不依赖开发者某台机器上的全局 Agent 工具才能构建；使用 Maven、JDK、Docker Compose 和 Python 标准库。仓库提供 harness 与初始化两个轻量校验脚本。

## 已知环境限制

- 当前全局 Java 环境仍为 JDK 17；项目脚本已在 PowerShell 5.1/7 下验证使用 Temurin 1.8.0_504 和 Maven 3.9.16。工具可用不等于完整编译或业务运行通过，见 [TEST-0002](test/result/2026-10-16-java8-launcher.md)。
- 离线 validate 缺少 Boot 2.7.12 父 POM 缓存；实际依赖下载、编译与启动均未完成。
- Compose 解析通过不代表镜像已下载或中间件可用；XXL-Job 的容器到宿主机回调需配置。
- 现有测试可能写数据、依赖固定样例并永久等待，不能未经检查全量运行。
- 活动 100401 已到期；活动有效期、SKU、策略及 Redis 装配均影响联调。
- ES SQL JDBC 需要合适许可；local trial 有时限，索引/Canal 未包含在核心启动路径。
- 前端、外部账户奖品网关不在本仓库；gateway enable 不控制当前远程调用，Redis 密码接入也未启用。
- 本次脚本任务未执行完整构建、服务启动、部署、数据迁移或 Git 提交。
