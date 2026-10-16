---
id: TASK-0002
type: task
status: completed
risk_level: L1
created: 2026-10-16
updated: 2026-10-16
owners: [Codex]
decision:
implementation:
problems: []
verification: [../../test/result/2026-10-16-java8-launcher.md]
---

# 固定 Java 8 的项目命令入口

## 目标

用户明确允许在 scripts 内编写指定已安装 JDK 8 的脚本，并要求在 .ai 中记录 AI 调用流程。脚本每次操作自动选择 Java 8 和当前 Maven，免去新开终端后手工切换。

## 非目标

不修改系统/用户全局环境变量，不启动应用或中间件，不实际下载依赖或构建，不修改业务代码。

## 验收标准

- 提供 Check、Maven、Run 入口；统一指定 JDK 8，拒绝其他主版本。
- 支持参数/项目专用环境变量覆盖路径，默认值采用用户已确认的安装位置。
- 从任意工作目录调用均定位仓库根目录，保留参数边界和子进程退出码。
- 成功、失败及 DryRun 后均恢复调用者环境和工作目录。
- .ai/project、索引和 AGENTS 明确指向调用流程，README 示例一致。
- 不实际启动项目，通过检查、预览及失败路径验证脚本。

## 授权与文件边界

用户本次授权 scripts 下脚本及 .ai 流程说明；同步维护根协作入口和开发说明。仅修改启动工具及关联文档，不改原项目、系统配置、Maven 配置或业务源码。

## 已知约束

遵循 [ARCH-0001](../../architecture/2026-10-16-module-baseline.md) 的 Java 8 基线。L1 单一模型直接执行；调用方式已由用户明确，无需独立 decision/implementation。

## 待确认项

无；实际服务运行继续留在后续任务。

## 当前阶段

脚本及调用记忆已完成，未实际构建或启动项目。

## 已完成事项

- 实现 scripts/java8.ps1 的 Check、Maven、Run、DryRun 和路径覆盖。
- 在 PowerShell 5.1/7 验证真实工具、失败路径、参数边界、退出码及环境/目录恢复。
- 更新 AGENTS、project、README、索引和当前运行问题说明；加入持久 AI 调用流程和验证证据。

## 下一步

后续 AI 执行 Windows 本地构建和启动时，按 DOC-0002 通过脚本操作；等待用户下一阶段指导。

## 阻塞项

无。

## 关联记录

- [调用流程](../../doc/java8-workflow.md)
- [验证](../../test/result/2026-10-16-java8-launcher.md)
