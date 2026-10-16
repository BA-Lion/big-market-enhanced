---
id: IMP-0000
type: implementation
status: draft
task: ../task/current/YYYY-MM-DD-task.md
decision: ../decision/YYYY-MM-DD-decision.md
architecture_refs: []
scope: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
approved_by:
base_revision:
supersedes: []
superseded_by:
---

# 实施规格

## 1. 执行目标

用可验证的结果描述本次执行完成后系统应达到的状态。

## 2. 执行前必读

- 上游 Decision：
- 相关 Architecture：
- 相关模块文档：
- 相关问题或测试证据：

## 3. 前置条件

- [ ] 上游 decision 状态为 `approved`
- [ ] 基线代码与 `base_revision` 一致或差异已经评估
- [ ] 所有目标文件和符号已经核实存在
- [ ] 所需权限和依赖已经具备

## 4. 修改边界

### 允许修改

| 文件或目录 | 允许的修改 |
| --- | --- |
| TBD | TBD |

### 禁止修改

| 文件或目录 | 原因 |
| --- | --- |
| TBD | TBD |

## 5. 必须保持的不变量

- MUST：
- MUST NOT：

## 6. 详细执行步骤

### Step 1

- 目标文件：
- 目标符号：
- 前置步骤：无
- 修改要求：
- 不得执行：
- 完成判据：

### Step 2

- 目标文件：
- 目标符号：
- 前置步骤：Step 1
- 修改要求：
- 不得执行：
- 完成判据：

## 7. 接口、数据与错误处理

### 接口变化

### 数据结构或迁移

### 错误与边界条件

### 向后兼容要求

## 8. 测试要求

| 测试层级 | 文件或场景 | 预期结果 |
| --- | --- | --- |
| TBD | TBD | TBD |

## 9. 验证命令

按顺序执行；不得用较弱检查替代指定检查。

```text
TBD
```

## 10. 完成标准

- [ ] 所有规定步骤已完成
- [ ] 未修改禁止范围
- [ ] 所有 MUST/MUST NOT 均满足
- [ ] 指定测试和验证命令通过
- [ ] 验证结果已写入 `test/result/`
- [ ] task 和 index 状态已更新

## 11. 停止并升级条件

- 上游设计与代码实际状态冲突。
- 需要修改未授权文件或扩大范围。
- 需要新增生产依赖、迁移数据或执行不可逆操作。
- 指定验证无法运行或失败原因表明方案需要改变。
- 存在无法消除的歧义，继续执行会产生不同产品行为。

## 12. 执行记录

只记录实际偏差、关键发现和阻塞，不复制完整终端输出。

