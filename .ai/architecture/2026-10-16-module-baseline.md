---
id: ARCH-0001
type: architecture
status: accepted
scope: project
created: 2026-10-16
updated: 2026-10-16
owners: [maintainer]
supersedes: []
superseded_by:
sources: [../../pom.xml, ../../big-market-app/src/main/java/cn/bugstack/Application.java]
---

# 导入项目的模块与数据边界

## 背景与问题

本记录保存原项目现有设计边界，作为增强开发基线；不表示已完成全面架构审查。模块关系来自各模块 POM，数据路由来自 application.yml 与仓储实现。

## 决策

维持 Java 8 编译目标、Spring Boot 2.7.12、Maven 七模块结构和 `cn.bugstack` 包名。仓库名改变不要求改变 Maven 坐标。后续升级另行评估兼容性。

## 架构不变量

- MUST：app 负责启动和装配；trigger 提供 HTTP、RPC、MQ 消费和任务入口；domain 保存领域模型、服务及端口。
- MUST：infrastructure 实现领域端口及持久化，querys 保存查询侧模型和仓储接口；api 保存对外接口和 DTO；types 保存公共类型。
- MUST：保留现有接口语义、消息主题和 Mapper namespace，直到对应任务明确批准变更。
- MUST：数据路由维持默认库 db00，业务分库 db01/db02，按 userId 路由，2 库 × 4 表。变更前须评估所有读写路径。
- MUST NOT：未经方案评估改变数据库结构、路由算法、库存扣减、账户额度、积分和发奖幂等语义。
- MUST NOT：在领域模块新增对 app、trigger、infrastructure 的反向模块依赖。

## 系统边界与职责

活动、策略、奖品、返利、积分和异步任务属于本后端；前端与外部账户调额服务未包含在源码仓库内。默认本地入口不使用 Nacos 注册，不启用 ZooKeeper DCC。

## 依赖方向或数据流

- app → trigger、infrastructure。
- trigger → domain、api、querys、types。
- infrastructure → domain、querys（经 domain 传递 types）。
- domain → types；querys → types；api 独立 Maven 模块。
- HTTP/RPC → 领域服务 → 仓储/端口 → MySQL、Redis、RabbitMQ、外部网关；ERP 查询还依赖 Elasticsearch。

## 备选方案与取舍

本次不执行拆服务、模块重命名或 Boot 3 迁移，优先建立可追溯的改进基线。

## 影响

后续任务可在现有模块内修复和优化；触及上述边界时应先提出架构变更和迁移策略。

## 迁移与兼容性

初始化无数据库迁移。SQL 保持原样，应用配置与构建兼容修正见导入方案。

## 验证方式

检查模块 POM、Application、DataSourceConfig、仓储实现和静态校验；实际业务一致性需要独立测试，不由文档声明保证。

## 待确认项

完整事务边界、并发语义及幂等实现需要后续专项审查。

## 相关记录

- [项目画像](../project.md)
- [导入方案](../decision/2026-10-16-source-import.md)
