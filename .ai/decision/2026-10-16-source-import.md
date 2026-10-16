---
id: DEC-0001
type: decision
status: approved
task: ../task/current/2026-10-16-repository-initialization.md
scope: [repository-initialization]
created: 2026-10-16
updated: 2026-10-16
approved_by: Codex（在用户明确授权的初始化范围内）
architecture_refs: []
supersedes: []
superseded_by:
---

# 保持业务基线的独立源码导入

## 问题与目标

增强仓库尚无源码；原项目包含机器相关配置和依赖混用，直接复制不能形成清晰的本地运行入口。

## 范围

包含完整受版本控制文件的复制、必要构建兼容修正、本地配置与独立 Compose、仓库说明及 `.ai` 实例化。排除业务行为改变、技术栈大版本升级、运行服务、数据迁移和发布。

## 已知事实

- 源码基线：`7e31b5374f4b889a9ea306d73a5623b1e49c786a`；检查时工作树干净。
- Spring Boot 父版本为 2.7.12，Java 编译目标为 8；AMQP starter 被显式覆盖为 3.2.0。
- 已手动创建 `RedissonClient`，业务未使用 Spring Data Redis；原 Redisson starter 3.26.0 引入 spring-data-32。
- API 模块的发布插件目前都在 XML 注释内，不会阻塞普通打包。
- 现有 Compose 的 MySQL 对外端口与 dev 配置不一致，XXL-Job 和 Prometheus 争用 9090；dev/test/prod 有原环境地址。

## 待确认项

依赖实际下载、完整编译、外部 SDK 可用性及中间件联通留待实际构建联调验证。

## 适用的架构约束

初始化前无生效架构记录；本次保存现有模块边界，不引入架构变更。

## 采用方案

1. 复制源 Git 跟踪文件，排除其 Git 元数据、缓存和本地未跟踪产物；本仓库 `.git`、`.ai` 保留。
2. Java 源码及业务资源尽量原样保留；不因仓库名变更重命名 Maven 坐标和包名。
3. AMQP 交由 Boot 2.7.12 管理；Redisson starter 改为同版本核心客户端，复用现有手动配置；Boot 打包插件对齐父版本，测试跳过改为可从命令行覆盖的属性。
4. 通用配置集中在 application.yml，默认 dev，采用本机 Compose 地址和端口并用环境变量覆盖；test/prod 覆盖部署端点和凭证。清除应用配置中的原环境凭证，保留公开的本地示例口令；XML 入口 token 也改为环境变量。
5. 添加精简独立的 local Compose（MySQL、Redis、RabbitMQ、Elasticsearch、XXL-Job），不复用历史远程镜像启动应用。保留旧运维资料供追溯。
6. 原自动发布及外部审查工作流改为手动触发，避免初始化即依赖原作者账号和外部凭证；不执行工作流。
7. 新建 README、忽略规则、Agent 入口、项目画像、架构基线、运行说明、问题与验证记录；此 L1 任务由同一模型实施，不额外创建 implementation。

## 备选方案与取舍

- 原样复制：无法解决环境耦合和依赖混用，不采用。
- 升级 Boot 3 / Java 17：涉及 javax/jakarta 迁移，超出初始化范围，不采用。
- 保留 Redisson starter 并替换 Spring Data 适配层：当前没有使用该集成，直接依赖 core 更贴合已有实现。

## 影响模块

根 POM、app POM、使用 Redisson 的模块 POM、app 运行配置、Docker 入口、开发运维配置与文档。Java 源码不修改。

## 兼容性、安全和数据影响

保持业务契约和现有 SQL。只编写数据库初始化路径，不执行。新开发配置仅面向本机；部署必须独立设置凭证。不导入源仓库提交历史。

## 风险与缓解措施

静态检查不能证明运行成功；在验证记录中列出未执行项，并为实际构建、ES SQL 授权、外部奖品网关和联调建立后续入口。

## 验收标准

与 [任务](../task/current/2026-10-16-repository-initialization.md) 一致；逐文件对比并记录所有导入差异。

## 下沉到 Implementation 的事项

无独立执行模型交接，implementation 不适用。

## 相关记录

- [Spring Boot 2.7.12 依赖管理](https://docs.spring.io/spring-boot/docs/2.7.12/reference/html/dependency-versions.html)
- [Redisson 3.26.0 starter POM](https://github.com/redisson/redisson/blob/redisson-3.26.0/redisson-spring-boot-starter/pom.xml)
