---
id: ATTN-0001
type: attention
status: verified
scope: [testing, local-development]
created: 2026-10-16
updated: 2026-10-16
evidence: [../test/result/2026-10-16-initialization.md]
---

# 原测试与外部服务的边界

## 触发场景

准备执行 Maven test、复用原示例配置、调试抽奖或外部账户发奖。

## 风险

现有测试多为 JUnit 4 + SpringBootTest，实际连接中间件并写入数据；部分使用无超时的 CountDownLatch.await。样例活动有有效期。`gateway.config.enable` 并未在 Retrofit2Config/AwardPort 中控制远程调用。

## 必须采取的做法

- 先读目标测试及其数据依赖，再选定测试执行；使用隔离开发数据。
- 查验活动有效期、SKU/策略关联和装配状态。
- 启动 XXL-Job 前检查样例任务的启用状态和宿主机回调地址。
- 外部账户奖品需要实际网关，不能把配置 enable=false 当作已禁用调用。

## 禁止做法

不把这些测试当成无需环境的单元测试；不把无限等待当成测试通过；不为通过联调擅自改生产数据或长期延长所有活动。

## 例外条件

后续将某个测试隔离为真正单元测试、增加超时或修复配置开关后，根据对应代码及证据更新适用范围。

## 验证证据

代码检查：RaffleActivityControllerTest、BehaviorRebateServiceTest、AwardServiceTest、Retrofit2Config、AwardPort；SQL：big_market.sql、xxl_job.sql。未执行这些测试。
