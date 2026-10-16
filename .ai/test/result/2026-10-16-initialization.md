---
id: TEST-0001
type: test-result
status: partial
created: 2026-10-16
updated: 2026-10-16
subject: repository-initialization
environment: Windows 11 / PowerShell / Maven 3.9.16 / JDK 17.0.19 / Docker Compose 5.1.3
revision: source-7e31b5374f4b889a9ea306d73a5623b1e49c786a-plus-uncommitted-initialization
executed_at: 2026-10-16T13:44:53Z
executed_by: Codex
related_task: ../../task/current/2026-10-16-repository-initialization.md
related_implementation:
---

# 初始化静态验证

## 验证目标

证明导入完整、业务源码未变、仓库入口和静态配置可解析。按用户要求不启动应用或容器，不执行 SQL，不访问旧环境服务。

## 环境与基线

验证日期 2026-10-16（Asia/Shanghai）。原项目提交为 `7e31b5374f4b889a9ea306d73a5623b1e49c786a`，导入前及验证时工作树均干净。增强仓库尚无首次提交，所有变更位于工作树。本机 Python 使用标准库，检查不依赖 PyYAML。

## 执行命令

在仓库根目录运行：

```text
python .ai/test/script/validate_initialization.py --source ../all-big-market/big-market --compose
python .ai/test/script/validate_harness.py
docker compose -f docs/dev-ops/docker-compose-local.yml config --quiet
mvn -o -B -ntp validate
java -version
mvn -v
```

另以 `git -c safe.directory=...` 对原仓库只读检查状态及版本；该参数只对单次命令生效，没有修改全局 Git 设置。

## 结果摘要

| 检查 | 结果 | 证据摘要 |
| --- | --- | --- |
| 完整导入 | passed | 原 Git 跟踪的 382 个文件全部存在；SHA-256 比对允许的 16 个转换文件，其余 366 个逐字节一致 |
| Java 代码 | passed | 285 个 Java 文件（含测试）全部逐字节一致；SQL 和 Mapper 也保持原样 |
| 模块与 XML | passed | 七模块齐全，内部模块依赖可定位，35 个 POM/资源 XML 可解析 |
| 初始化依赖配置 | passed | AMQP 无 3.x 显式覆盖，Redisson 改 core，Boot 插件版本对齐；这些是静态检查，未解析完整依赖树 |
| Spring YAML | passed | 四个 application YAML 通过 Compose 的 YAML 解析器解析（用 x-* 扩展包装并转义 Spring 占位符），无服务启动 |
| 本地 Compose | passed | 配置 schema、五个服务、SQL 绑定路径存在，宿主机端口不重复且仅绑定回环地址 |
| 忽略规则 | passed | Maven 产物、数据、.env、本地覆盖被忽略；.ai、AGENTS 和 SQL 保持可版本控制 |
| Harness | passed | 结构、记录状态和相对链接通过，project 无初始化警告 |
| 离线 Maven 模型验证 | blocked | 本地缺少 Boot 2.7.12 父 POM；offline 模式不能从配置镜像取得它，未进入编译 |
| 工具基线 | partial | 检测到 Maven 3.9.16 / JDK 17.0.19；尚未准备并验证 JDK 8 环境 |

## 未执行项

- 在线下载依赖、完整 Maven 编译/打包、JUnit 测试。
- Docker 镜像拉取、容器启动、数据库初始化。
- Spring 上下文启动、中间件连通、HTTP/RPC、抽奖/发奖/返利/积分链路。
- ES 许可与订单索引、Canal 同步、XXL-Job 回调和外部网关联调。
- Git 提交、推送、CI 和部署。

## 失败与残余风险

离线模型验证受依赖缓存限制，不是编译通过证据。Git 和 Docker CLI 对当前沙箱用户的全局配置读取有权限警告，但本次本地结构和 Compose 解析返回成功；未更改这些全局配置。后续需验证第三方 SDK 解析、旧依赖兼容和实际运行，见 [PROB-0001](../../problem/2026-10-16-runtime-verification.md)。

## 相关记录

- [任务](../../task/current/2026-10-16-repository-initialization.md)
- [方案](../../decision/2026-10-16-source-import.md)
- [转换清单](../../doc/runtime-and-import.md)
