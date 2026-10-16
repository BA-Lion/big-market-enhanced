---
id: DOC-0001
type: module-doc
status: current
scope: [initialization, runtime]
created: 2026-10-16
updated: 2026-10-16
source_paths: [pom.xml, big-market-app/src/main/resources, docs/dev-ops/docker-compose-local.yml]
verified_at_revision: source-7e31b5374f4b889a9ea306d73a5623b1e49c786a-plus-initialization-working-tree
---

# 导入来源、转换和运行边界

## 职责

记录增强仓库与原项目的差异，以及当前可用的运行入口。操作步骤以[根 README](../../README.md)为准；Windows AI 的构建和启动必须使用 [Java 8 调用流程](java8-workflow.md) 中的脚本入口。

## 边界与非职责

本次只完成初始化和静态检查，不声称编译、应用启动、抽奖链路或生产部署已验证。

## 代码入口

- 来源：相邻目录 `../all-big-market/big-market`（相对本仓库根目录）；提交 `7e31b5374f4b889a9ea306d73a5623b1e49c786a`。
- 原 Git 工作树在导入时无修改；复制 382 个 Git 跟踪文件，不导入 `.git`。
- Application：`big-market-app/src/main/java/cn/bugstack/Application.java`。
- 原 README 保存到 [upstream-readme.md](../../docs/upstream-readme.md)。

## 核心数据结构

七个 Maven 模块；MySQL 基础库 `big_market`、分库 `big_market_01` / `big_market_02`；Redis 存储库存、概率装配及缓存；RabbitMQ 用于发奖、返利、库存等事件；Elasticsearch 用于订单查询。

## 接口与行为语义

Java 源码、测试、Mapper XML 和 SQL 原样保留。初始化未修改业务 API、库存算法或账户处理。SQL 示例数据包含活动有效期，实际测试必须选择有效活动并先装配。

## 关键常量和配置

通用配置迁入 `application.yml`，默认 dev；`application-dev.yml` 预留本地覆盖；test/prod 提供部署必须注入的环境变量。Spring 资源不经 Maven 过滤，`${...}` 在运行时解析。

## 依赖关系

AMQP 恢复 Boot 2.7.12 版本管理；Redisson 3.26.0 改为核心依赖，现有 RedisClientConfig 已手动创建客户端，不需要 Spring Data 3.2 适配。Boot 打包插件对齐 2.7.12；Surefire 2.22.2 配合 Vintage 执行原 JUnit 4 测试，默认 skipTests 可覆盖。

## 导入文件变更清单

- `README.md`、`.gitignore`：重写仓库入口及本地文件忽略规则。
- `pom.xml`：移除 AMQP 3.2.0 覆盖、Redisson 改 core、增加 skipTests 默认值、移除重复编码属性。
- app/trigger/infrastructure 的 `pom.xml`：Redisson 改 core；app 另对齐 Boot 插件、Surefire，增加 Vintage，关闭资源过滤。
- app 的 `application.yml` / dev / test / prod：配置归一、宿主机端点、环境变量与凭证替换。
- `spring/spring-config-token.xml`：入口 token 改为环境变量及本地示例默认值。
- app 的 Dockerfile / ActionDockerfile：修正 JAVA_OPTS 与 `-jar` 顺序，基础镜像改为 Temurin Java 8 JRE；build.sh 使用本地镜像名并从脚本目录构建。
- 两个原 `.github/workflows/*.yml`：仅允许手动触发。内部发布目标和外部服务仍是历史配置，使用前必须重新配置。
- 原有其余文件逐字节保留；新增本地 Compose、README、协作入口、换行规范、校验脚本和 `.ai` 项目记录。

## 已知限制

- local Compose 只有核心中间件和任务管理，不含 Canal、Nacos、ZooKeeper、监控及前端；它们的历史配置仍保留。
- ES SQL JDBC 与 ES 服务保持 7.17.14；本地 trial 许可有时限。订单索引需要单独建立或通过 Canal 同步，不能把启动 ES 当成订单查询可用。
- XXL-Job 在容器，应用在宿主机，执行器需注册容器可达的宿主机地址；历史任务有启用项，实际运行前先检查调度配置。
- Retrofit2Config 不使用 enable 开关控制建 Bean，AwardPort 也不根据此开关跳过远程调用；外部账户奖品需要真实的兼容网关。
- dev/test/prod 的应用配置已去除原环境凭证；历史运维和 curl 文件仍是上游资料，不能作为本仓库默认环境直接执行。
- API 模块独立 POM；发布插件已被上游注释，本次未启用或改写。

## 验证来源

- [初始化验证](../test/result/2026-10-16-initialization.md)
- [待验证事项](../problem/2026-10-16-runtime-verification.md)
- [Spring Boot 2.7.12 依赖版本](https://docs.spring.io/spring-boot/docs/2.7.12/reference/html/dependency-versions.html)
- [Redisson starter 3.26.0 POM](https://github.com/redisson/redisson/blob/redisson-3.26.0/redisson-spring-boot-starter/pom.xml)
- [Elastic SQL JDBC](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/sql-jdbc.html)

## 相关记录

- [模块边界](../architecture/2026-10-16-module-baseline.md)
