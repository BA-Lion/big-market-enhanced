---
id: PROB-0001
type: problem
status: open
severity: medium
scope: [build, integration]
created: 2026-10-16
updated: 2026-10-16
related_tasks: [../task/current/2026-10-16-repository-initialization.md]
related_decisions: [../decision/2026-10-16-source-import.md]
resolved_by:
---

# 实际构建与业务联调尚待验证

## 现象

用户本次仅要求理论可行的初始化，不实际启动。离线 Maven validate 因本地未缓存 Boot 2.7.12 父 POM 无法读取完整 Maven 模型。

## 影响

本次可证明复制完整性和静态配置一致性，不能证明依赖全量可下载、Java 编译和业务运行已通过。此项不阻塞静态初始化验收。

## 复现条件

在缺少父 POM 缓存的环境执行 `mvn -o -B -ntp validate`。

## 已确认事实

- 当前机器 Maven 3.9.16 使用 JDK 17.0.19；没有检测到 JDK 8 安装目录。
- 现有多数测试使用 SpringBootTest，并有数据库写入及永久等待，不适合无中间件环境直接全量执行。
- SQL 活动 100401 的结束日期为 2026-10-06，已早于本次初始化日期；活动 100301 的结束日期为 2034-03-09。保留原始数据，不自行延期活动。
- local Compose 不含 Canal，同步订单到 ES 的链路尚未准备。
- 外部账户奖品依赖独立网关，源码不在仓库内。

## 推断与待确认项

`db-router-spring-boot-starter:1.0.4`、`business-behavior-monitor-sdk:1.1` 等第三方依赖的实际解析及其与现有 Spring 栈的兼容性；ES SQL JDBC 许可；分库路由 Bean 装配；宿主机执行器回调；完整抽奖、返利与发奖链路。

## 已尝试方法

完成源码和配置检查；执行离线 Maven 模型验证，保留明确的环境限制结论，不以 XML 可解析替代编译成功。

## 临时缓解措施

遵循 README 的 Java 8 基线、在线 Maven 打包和 local Compose 路径，按需选择单个测试；使用有效活动并先装配。

## 根因

依赖缓存不足；本任务明确排除实际服务运行。业务联调缺口不是本次发现的已复现业务 Bug。

## 下一步

用户开始实际联调任务后：使用 JDK 8 下载依赖并打包，启动本地中间件，验证上下文启动、装配及抽奖；再单独建立订单索引/Canal 和外部奖品网关。将新问题拆成可复现记录。

## 解决与验证

待实际构建联调后更新；证据见[初始化验证](../test/result/2026-10-16-initialization.md)。
