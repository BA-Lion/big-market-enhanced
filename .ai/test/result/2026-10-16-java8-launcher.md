---
id: TEST-0002
type: test-result
status: passed
created: 2026-10-16
updated: 2026-10-16
subject: java8-launcher
environment: Windows 11 / Windows PowerShell 5.1.26100.9711 / PowerShell 7.6.5 / Temurin 1.8.0_504 / Maven 3.9.16
revision: f3200cf-plus-java8-launcher-working-tree
executed_at: 2026-10-16T14:11:30Z
executed_by: Codex
related_task: ../../task/current/2026-10-16-java8-launcher.md
related_implementation:
---

# Java 8 入口脚本验证

## 验证目标

验证脚本确实选择 Java 8，参数、目录和退出码正确，且不污染调用者环境。本结果的 passed 只覆盖脚本，不代表完整 Maven 构建或应用已启动。

## 环境与基线

验证日期为 2026-10-16（Asia/Shanghai）。全局 JAVA_HOME 仍指向 Java 17；通过 scripts/java8.ps1 选择用户已安装的 JDK 8。基线提交 f3200cf，本次修改尚未提交。

## 执行命令

```powershell
& .\scripts\java8.ps1 -Action Check
& .\scripts\java8.ps1 -Action Run -JvmArguments @('-Xms256m','-Xmx1g') -ToolArguments @('--server.port=18098') -DryRun
& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B','-ntp','clean','package','-DskipTests') -DryRun
python .ai/test/script/validate_harness.py
python .ai/test/script/validate_initialization.py
git diff --check
```

另在被忽略的 .cache 中生成临时 smoke 脚本和带空格路径的 Maven 替身，分别用 Windows PowerShell 5.1 与 PowerShell 7 执行。替身只回显参数/工作目录/JAVA_HOME 并返回 23，不调用 Maven 构建。失败场景为显式选择 JDK 17、缺失 JDK、缺失 Maven 和缺失 JAR；逐次断言退出码及调用者 JAVA_HOME/PATH/工作目录恢复。跨目录检查从临时目录调用仓库脚本，未在仓库外写入文件。

## 结果摘要

| 检查 | 结果 | 证据摘要 |
| --- | --- | --- |
| 真实工具 Check | passed | 两个 PowerShell 版本下 java/javac 输出 1.8.0_504；Maven 3.9.16 报告使用同一 Java 8 |
| Maven/Run 预览 | passed | Maven 目标参数完整；JVM 参数位于 -jar 前，dev profile 和应用参数位于 JAR 后 |
| 含空格参数及路径 | passed | Maven 替身收到单个参数 -Dprobe=two words；替身路径含空格仍正确执行 |
| 子进程退出码 | passed | 替身返回 23，脚本原样返回 23 |
| JDK/路径/JAR 防护 | passed | JDK 17、缺失 JDK、缺失 Maven、缺失 JAR 均返回 1，没有回退全局 Java，也没有启动应用 |
| 环境及目录恢复 | passed | 成功、预览及失败后 JAVA_HOME/PATH/工作目录均与调用前一致 |
| 任意工作目录 | passed | 从临时目录调用，命令定位仓库根，完成后回到调用目录 |
| 项目结构与文档 | passed | harness、初始化结构检查及 git diff --check 通过 |

## 未执行项

未下载依赖、执行 Maven 编译/测试或启动 JAR；未启动 Docker、中间件或数据库导入；未修改全局环境、执行策略或 Git 提交。

## 失败与残余风险

没有剩余脚本验证失败。完整构建及联调继续由 [PROB-0001](../../problem/2026-10-16-runtime-verification.md) 跟踪。临时 smoke 工件是验证辅助，不是正式业务测试或实际服务。

## 相关记录

- [任务](../../task/current/2026-10-16-java8-launcher.md)
- [AI 调用流程](../../doc/java8-workflow.md)
- [脚本](../../../scripts/java8.ps1)
