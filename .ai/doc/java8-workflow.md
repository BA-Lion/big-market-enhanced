---
id: DOC-0002
type: module-doc
status: current
scope: [windows, build, launch]
created: 2026-10-16
updated: 2026-10-16
source_paths: [scripts/java8.ps1]
verified_at_revision: f3200cf-plus-java8-launcher-working-tree
---

# AI 使用 Java 8 的固定调用流程

## 职责

Windows 本地构建、测试和启动应用统一通过 [scripts/java8.ps1](../../scripts/java8.ps1)。脚本自动指定 Java 8，不需要预先执行环境切换，也不依赖全局 java/mvn 的解析结果。

## 边界与非职责

脚本本身不安装 JDK/Maven、不改全局环境、不启动 Docker、不自动构建、不后台启动应用。Check 只检查工具，DryRun 只检查路径和预览参数；Run 才会前台启动应用。脚本存在不代表获得启动服务、迁移或部署的额外授权。

## 代码入口

唯一入口为 scripts/java8.ps1，支持 Check、Maven、Run 三种 Action，默认 Check。用 `&` 调用，不要点源执行。

## 核心数据结构

工具路径优先级：显式 `-JdkHome` / `-MavenHome` 参数 → `BIG_MARKET_JAVA_HOME` / `BIG_MARKET_MAVEN_HOME` 环境变量 → 脚本中用户已确认的本机默认路径。具体机器路径只保存在脚本默认值中，本记录不重复保存。

脚本校验 java.exe、javac.exe、release 文件和 JAVA_VERSION=1.8；路径缺失或版本不符立即失败，禁止静默退回系统 JDK 17。Maven 入口固定为选定目录下 bin/mvn.cmd。

## 接口与行为语义

每次调用临时设置 JAVA_HOME，并将 Java 8 的 bin 放到 PATH 最前；使用所选工具的绝对路径，工作目录固定为仓库根目录。完成或异常后恢复原 JAVA_HOME、PATH 和工作目录，转发被执行程序退出码。

`-ToolArguments` 是参数数组，不是拼接的命令字符串；Maven 用它接收 goals/options，Run 用它接收应用参数。`-JvmArguments` 只对 Run 生效，位于 `-jar` 前；`-JarPath` 相对仓库根解析；`-SpringProfile` 默认 dev。

## AI 必须遵循的调用顺序

1. 阅读当前用户指令、AGENTS、project 和本记录，确认当前授权是检查、构建还是实际启动；本次任务仅授权脚本编写和无服务验证。
2. 首次操作先执行 Check，核实输出中的 Java 和 Maven 版本，失败则修正路径，不绕过脚本使用全局工具。
3. 需要构建时执行 Maven Action；需要测试时同样通过 Maven Action，先读目标测试和数据依赖。
4. 需要实际启动时，先确认依赖环境已准备、JAR 是当前源码构建产物；按本地 Compose 拓扑设置 XXL-Job 回调等环境变量，再用 Run Action。
5. 新任务、新终端或电脑重启后仍直接调用脚本，无需先运行独立的环境初始化命令。每条 Maven/Run 调用都会重新选择 Java 8。
6. 当前只需预览时追加 DryRun，禁止把 DryRun 成功描述为应用已启动。

在仓库根目录使用 PowerShell 执行：

```powershell
# 无服务检查：默认 Action 即 Check
& .\scripts\java8.ps1 -Action Check

# 构建：不会执行测试，但会编译测试
& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B', '-ntp', 'clean', 'package', '-DskipTests')

# 仅预览启动命令；JAR 尚不存在也可预览，不会启动应用
& .\scripts\java8.ps1 -Action Run -DryRun

# 已获得启动授权且环境准备完成后，才执行下列命令
$env:XXL_JOB_EXECUTOR_ADDRESS = 'http://host.docker.internal:9999/'
& .\scripts\java8.ps1 -Action Run

# 按需指定 JVM/应用参数
& .\scripts\java8.ps1 -Action Run -JvmArguments @('-Xms256m', '-Xmx1g') -ToolArguments @('--server.port=18098') -DryRun

# 单个集成测试：先准备隔离数据及依赖服务
& .\scripts\java8.ps1 -Action Maven -ToolArguments @('-B', '-ntp', '-pl', 'big-market-app', '-am', 'test', '-DskipTests=false', '-Dtest=AwardDaoTest', '-Dsurefire.failIfNoSpecifiedTests=false')
```

若 Windows PowerShell 执行策略阻止脚本，可在单独子进程内执行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\java8.ps1 -Action Check`；该参数只作用于该进程，不使用 Set-ExecutionPolicy 修改持久策略。传递数组参数时优先在 PowerShell 内用 `&` 调用；不要把多参数数组作为一个字符串传给 -File。

## 关键常量和配置

环境变量中的普通运行配置（如 MYSQL_PASSWORD、XXL_JOB_EXECUTOR_ADDRESS）会被 Java 子进程继承；脚本只覆盖 JAVA_HOME/PATH。需要切换安装目录时优先使用显式参数或上述项目专用变量，不编辑系统 JAVA_HOME。IDEA 直接运行不会经过脚本，需单独选择项目 SDK/Maven JRE 8。

## 依赖关系

PowerShell 5.1 或兼容的 PowerShell 7、已安装 Windows x64 JDK 8、Maven（Check/Maven 所需）。Run 只要求 JDK 与已打包 JAR，但业务仍依赖中间件。

## 已知限制

脚本按 Windows 可执行文件实现，不用于 Linux/macOS；启动为前台进程，不负责守护或重启。DryRun 会显示传入参数，凭证应通过环境变量传递，不写到命令参数中。

## 验证来源

- [工具及脚本验证](../test/result/2026-10-16-java8-launcher.md)
- [尚未完成的构建联调](../problem/2026-10-16-runtime-verification.md)

## 相关记录

- [项目画像](../project.md)
- [任务](../task/current/2026-10-16-java8-launcher.md)
