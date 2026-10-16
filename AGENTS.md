# 项目协作入口

开始任务前按顺序阅读：

1. [`.ai/index.md`](.ai/index.md)
2. [`.ai/project.md`](.ai/project.md)
3. [`.ai/readme.md`](.ai/readme.md) 中的风险分级与记录生命周期
4. 索引中与任务相关的架构、方案、问题和验证记录

本仓库用于升级和修复原 big-market 项目。原项目是只读基线，后续修改在本仓库进行。
严格区分代码事实、设计意图、推断和实际验证结果。保持现有 Java 8、Spring Boot 2.7、模块和数据路由边界；升级它们需要单独方案。

Windows 本地执行 Maven、测试或启动后端时，必须通过 `scripts/java8.ps1`，不要直接使用系统 `java` / `mvn`。先运行 `& .\scripts\java8.ps1 -Action Check`；构建使用 `-Action Maven -ToolArguments @(...)`，启动使用 `-Action Run`。完整顺序及预览方式见 [Java 8 调用流程](.ai/doc/java8-workflow.md)。每次调用自动选定 JDK 8，无需预先切换环境；脚本不授予超出当前任务的启动授权。

按 `.ai/readme.md` 分级记录任务。L1 可由同一模型完成，不强制额外 implementation；复杂交接任务必须有已批准的执行契约。仅根据用户当前授权执行启动、迁移或发布；初始化任务已明确不要求实际运行。

不覆盖用户修改，不保存真实凭证，不把依赖服务的集成测试描述成独立单元测试。完成重要修改后更新索引和验证记录。
