# `.ai` 导航索引

## 项目状态

- Harness 状态：`initialized`；项目画像已实例化，无项目占位资料。
- 项目：原 big-market 的优化升级仓库；源码基线导入和静态初始化已完成。
- 项目画像：[project.md](project.md)
- 操作入口：[README](../README.md)；协作入口：[AGENTS.md](../AGENTS.md)
- 当前任务：无进行中的开发任务；等待用户下一步指导。
- 当前限制：实际构建与联调尚未验证，见 PROB-0001；不阻塞静态初始化完成。
- 最后维护：2026-10-16

## 必读架构约束

| 记录 | 状态 | 适用范围 |
| --- | --- | --- |
| [ARCH-0001 模块与数据边界](architecture/2026-10-16-module-baseline.md) | accepted | 全项目；保留 Java/Boot 基线、七模块、路由和业务契约 |

## 当前任务

当前无 active/planned/blocked 任务。

## 已批准的任务方案

当前无待执行方案；初始化方案已随任务完成，列于下方追溯区。

## 可执行的 Implementation

当前无。初始化为同一模型完成的 L1 任务，不需要单独 implementation。

## 未解决问题

| 问题 | 状态 | 影响 | 下一步 |
| --- | --- | --- | --- |
| [PROB-0001 构建与联调待验证](problem/2026-10-16-runtime-verification.md) | open | 缺少实际运行证据 | 实际构建、环境准备和链路验证时处理 |

## 近期验证证据

| 结果 | 状态 | 对象 | 验证时间 |
| --- | --- | --- | --- |
| [TEST-0001 初始化静态验证](test/result/2026-10-16-initialization.md) | partial | 静态检查通过，实际构建运行未验证 | 2026-10-16 |

## 稳定知识入口

| 记录 | 状态 | 适用范围 |
| --- | --- | --- |
| [DOC-0001 来源、转换与运行边界](doc/runtime-and-import.md) | current | 初始化来源、16 个转换文件和本地入口 |
| [ATTN-0001 集成测试边界](attention/integration-test-boundaries.md) | verified | 执行原测试、使用活动数据和外部奖品时 |

`test/experience/` 尚无独立经验记录；模板保留在 `templates/`，不作为项目事实。

## 近期完成记录（仅供追溯）

| 记录 | 状态 | 范围 |
| --- | --- | --- |
| [TASK-0001 导入与初始化](task/current/2026-10-16-repository-initialization.md) | completed | 复制、构建配置、开发入口和项目记忆 |
| [DEC-0001 导入方案](decision/2026-10-16-source-import.md) | approved（任务已完成） | 保持业务基线的独立导入，不作为新任务授权 |

## 校验入口

```text
python .ai/test/script/validate_harness.py
python .ai/test/script/validate_initialization.py --compose
```

导入审计可追加 `--source ../all-big-market/big-market`；仅在原项目仍保持导入基线时使用。脚本不启动服务，不执行 SQL。
