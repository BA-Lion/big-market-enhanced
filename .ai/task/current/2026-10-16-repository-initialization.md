---
id: TASK-0001
type: task
status: completed
risk_level: L1
created: 2026-10-16
updated: 2026-10-16
owners: [Codex]
decision: ../../decision/2026-10-16-source-import.md
implementation:
problems: [../../problem/2026-10-16-runtime-verification.md]
verification: [../../test/result/2026-10-16-initialization.md]
---

# 导入基线与仓库初始化

## 目标

从相邻原项目导入完整源码、资源、测试和运维资料，建立可独立构建、具备明确本地运行路径的增强仓库，并实例化项目记忆。

## 非目标

不启动应用或容器，不连接外部服务，不执行数据库导入，不进行业务重构或全面依赖升级，不提交或推送 Git。

## 验收标准

- 七个 Maven 模块、SQL、Mapper、配置及测试完整导入，保留当前 Git 和 `.ai`。
- 原 Java 源码保持一致；必要转换有清单和原因。
- README 提供前置条件、构建命令、本地中间件及配置方法。
- `project.md` 无占位资料，Agent 入口与索引可用。
- 完成静态校验，清楚区分静态可行性和实际运行证据。

## 授权与文件边界

用户于 2026-10-16 授权复制原项目、必要转换和仓库初始化。允许修改本仓库的构建、配置、运维和文档；原项目只读，禁止复制其 `.git` 或覆盖本仓库已有 `.ai`。

## 已知约束

保留 Java 8 / Spring Boot 2.7 基线、模块名、包名、API 和分库分表结构；所有服务操作仅写入说明，不实际执行。

## 待确认项

实际联调环境、未来优化范围由用户后续指导。

## 当前阶段

已完成静态范围内的初始化，等待用户下一阶段指导。

## 已完成事项

- 导入 382 个文件，285 个 Java 文件与原项目逐字节一致。
- 完成必要构建兼容转换、环境变量配置及五服务 local Compose。
- 完成 README、忽略规则、换行规范、Agent 入口和项目画像。
- 建立架构基线、来源转换说明、已知问题、测试注意项及验证记录。
- 补齐 test-result 模板的 created/updated 元数据，使其与现有 harness 校验规则一致。
- 静态检查通过；离线 Maven 因依赖缓存不足受阻，未运行实际服务。

## 下一步

等待用户指导实际联调或具体优化任务；后续事项见问题记录，不自行扩大本次范围。

## 阻塞项

无；实际运行不属于本次验收范围。

## 关联记录

- [方案](../../decision/2026-10-16-source-import.md)

- [验证](../../test/result/2026-10-16-initialization.md)
- [待验证问题](../../problem/2026-10-16-runtime-verification.md)
