# Engineering Philosophy

Evidence-driven software engineering philosophy for AI-assisted development.

当前稳定版本：**v0.4.0 — Continuous Knowledge Compilation**

v0.4.0 定义持续知识编译协议，并在完整验证、master CI 和发布门禁通过后作为稳定版本发布。

这是一个可独立触发、独立维护、独立评测的通用软件工程方法论 Skill Suite。它帮助 Codex、Cline、OpenClaw 以及其他兼容 Agent Skills 规范的 Agent，在需求澄清、仓库分析、架构演化、实现、评审和发布之间保持可追溯的工程判断。

公开源码仓库地址是 `hugo2lee/engineering-philosophy`。该仓库面向通用软件工程场景，不绑定特定作者、公司、团队或技术栈的工程偏好。

## Core Philosophy

核心原则是：

> Prefer the simplest architecture that preserves meaningful boundaries.

v0.4.0 延续 v0.3.0 的六个判断，并增加一条知识演进约束：

1. 先澄清可观察行为，再讨论实现。
2. 新需求必须与已发布行为、现有契约和当前能力对照，不能因为“新增”二字就重复实现。
3. 先检查现有仓库和可复用能力，再制定计划。
4. 架构来自已证明的变更压力，而不是来自对未来可能性的想象。
5. 业务变化与必要的架构 enabler 通过可运行的 vertical slice 一起演进。
6. 已发布的重要行为冻结为可执行 baseline；未经授权不能悄悄削弱。
7. 从仓库证据编译 Agent 知识，但生成不等于激活，项目经验也不自动晋升为全局规则。

规则统一分为 `MUST`、`SHOULD` 和 `CONDITIONAL`。全局 Skill 不写入某个项目的 Go 版本、数据库、公司目录、分支策略、领域 Aggregate 或测试框架；这些属于项目规则、项目级 Skill 或 ADR。

## Feature Change Lifecycle

对有实际影响的功能变更，推荐按以下顺序推进：

```text
User Request
  -> Requirement Clarification
  -> Requirement Reconciliation
  -> User Decision Gate, when required
  -> Approved Requirement Contract
  -> Repository Analysis
  -> Business Change / Impact Analysis
  -> Architecture Pressure Analysis
  -> Conditional architecture-boundaries / ddd-lite routing
  -> Implementation Plan
  -> Incremental Implementation
  -> TDD / Focused Verification
  -> Release Behavior Baseline
  -> Change Review / Gate 3
  -> CI / Artifact / Release Verification / Gate 4
  -> Version / Tag / Release
```

四个 Gate 是决策保护，不是文档仪式：

- **Gate 1 — Requirement Approved**：行为、非目标、冲突和需要用户决定的事项已经清楚。
- **Gate 2 — Ready for Implementation**：仓库影响面、复用能力、变更压力、架构 enabler、任务依赖和验证条件已明确。
- **Gate 3 — Ready for Review**：实现可运行，相关行为测试为绿，适用 Release Behavior Baseline 已建立，计划/需求偏差已记录，必要时 Feature Change Record 已更新，然后再进行变更审查。
- **Gate 4 — Ready for Release**：验证过的就是将要发布的 artifact，质量闸、部署健康检查和停止/回滚条件齐备。

简单、明确、孤立的修改可以把证据保留在任务或提交中；跨边界、兼容性敏感或发布风险较高的功能，建议创建 `docs/changes/<feature-name>.md`。详细流程见 [Feature Change Lifecycle](skills/engineering-philosophy/references/feature-change-lifecycle.md)，记录模板见 [Feature Change Record](skills/engineering-philosophy/references/feature-change-record.md)。

## Continuous Knowledge Compilation

v0.4.0 定义第二条生命周期：当代码、文档、测试、构建、生成物或运维资料持续变化时，Agent 知识应当被发现、分类、对账、编译、验证、注册和退役。

```text
Repository Evidence
  -> Discovery
  -> Artifact Classification
  -> Canonical Source / Provenance
  -> Knowledge Reconciliation
  -> Reference / Evidence / Decision / Generated Artifact / Skill Candidate
  -> Validation & Redaction
  -> Registration
  -> Candidate / Active / Deprecated / Archived
```

这条流程不要求每个文件都生成 Skill。应优先更新已有知识 owner；重复工作才可能形成项目级 Skill candidate；任何 project-to-global promotion 都必须经过独立证据、eval 和审查。完整协议见 [$knowledge-compilation](skills/knowledge-compilation/SKILL.md) 及其 references。

## Quick Start

普通用户使用 `npx skills` 从公开 GitHub 仓库安装，不需要发布 npm 包。当前公开仓库地址是 `hugo2lee/engineering-philosophy`：

```sh
# 查看所有 Skill
npx skills@latest add hugo2lee/engineering-philosophy --list

# 安装全部 Skill
npx skills@latest add hugo2lee/engineering-philosophy \
  --skill '*' \
  --global \
  --agent codex \
  --agent cline \
  --agent openclaw

# 只安装 architecture-boundaries
npx skills@latest add hugo2lee/engineering-philosophy \
  --skill architecture-boundaries \
  --global \
  --agent codex

# 只给 Codex 安装 ChatGPT Web 规划/执行 workflow
npx skills@latest add hugo2lee/engineering-philosophy \
  --skill chatgpt-plan-execute \
  --global \
  --agent codex
```

`npx skills` 会自动发现仓库中的 `skills/<name>/SKILL.md`，因此不需要创建或发布 npm 包。安装后可以使用 `npx skills ls -g` 查看，使用 `npx skills update -g -y` 更新已安装 Skill。

不同 Agent 的原生/默认全局目录如下：

- Codex：`~/.codex/skills`
- Cline：`~/.agents/skills`
- OpenClaw：`~/.openclaw/skills`

原生 Agent 目录和 `npx skills` 的安装目标是两个概念。当前实测 `npx skills@latest` 在同时指定 `--agent codex --agent cline` 时使用共享的 `~/.agents/skills`，指定 OpenClaw 时使用 `~/.openclaw/skills`；`scripts/smoke-test-npx.sh` 有意验证这一 CLI 行为。维护者的 `scripts/deploy.sh` 是独立的复制部署辅助工具，默认按上面的原生目录分别写入，也可以通过参数传入临时目标。实际安装后请用 `npx skills ls -g` 和对应 Agent 文档确认最终路径。

## Published Skills

维护者验证时区分三个集合：filesystem 中的 Discovered Skill Set、registry 中
`status: active` 的 Published Active Skill Set，以及安装器实际输出的 Installed
Skill Set。候选 Skill 必须留在自动发现的 active path 之外，直到通过晋升门禁。

`v0.4.0` 稳定版本发布了 12 个顶层 Skill；当前 `Unreleased` 工作树新增 `chatgpt-plan-execute`，因此 active registry set 为 13 个。任意 ref 的实际发布集合及数量均以 `skills/registry.yaml` 中的 active set 为准，验证、部署和安装不得硬编码固定 Skill 数量。仓库是发布和验证边界，不是一个必须整体触发的巨大 Skill；每个目录都可以独立调用。

- `engineering-philosophy`：总纲、规则等级、全局/项目边界、生命周期和路由。显式入口，不作为所有请求的必经层。
- `requirement-engineering`：Requirement Contract、现有需求/能力/发布行为对照、冲突分类和用户决策门。
- `change-planning`：仓库影响分析、能力复用、依赖、风险、检查点和可执行 Change Plan。
- `architecture-boundaries`：真实技术边界、Ports and Adapters、DIP、显式 DI、测试缝和架构压力/enabler。
- `ddd-lite`：业务不变量、Entity、Value Object、Aggregate、Domain Service、Domain Event 和 Bounded Context 的条件化选择。
- `incremental-implementation`：Business Value + Just-enough Architecture + Verification 的 vertical slice、兼容迁移和安全排序。
- `test-driven-development`：Red-Green-Refactor、行为测试、回归测试和 Release Behavior Baseline。
- `systematic-debugging`：复现、证据、可证伪假设、最小修复、回归验证和不确定性记录。
- `code-review-and-quality`：Requirement Contract、Change Plan、diff、baseline 和验证证据的 Gate 3 审查。
- `git-workflow-and-versioning`：分支、原子提交、版本、CHANGELOG、Tag 和发布可追溯性。
- `ci-cd-and-automation`：测试/构建质量闸、artifact 身份、部署健康、停止/回滚和 Gate 4。
- `knowledge-compilation`：仓库证据发现、artifact 分类、知识对账、provenance、Skill candidate、验证、注册和退役。它不替代普通功能开发、调试、评审或发布 Skill。
- `chatgpt-plan-execute`：显式 Codex workflow；先从真实仓库编译最小可审计上下文，通过 Codex Chrome Extension 交给 ChatGPT Web 做规划/评审，再由 Codex 校验假设、执行并本地验证。普通编码、规划或评审请求不得隐式上传源码。

`v0.4.0` 稳定版仍不创建 C++ Skill，也不创建独立的安全、可观测性或 ADR Skill。代码示例和语言落地参考集中在 `architecture-boundaries` 下的 Go 与 C++ 参考文件中，不把项目版本或公司约束写进全局 Skill。

## Requirement Reconciliation

每个非平凡的新请求都要与四类现有证据对照：既有需求和决策、已实现能力、公开/内部契约、已发布 baseline。结果分类为：

- `New`
- `Overlap`
- `Duplicate`
- `Compatible Extension`
- `Conflict`
- `Replacement`

当新请求与已发布行为冲突，或两个实现都合理但用户可感知结果不同，必须进入 User Decision Gate。不要把未确认的产品决定伪装成架构决定。

## Evolutionary Architecture

架构推理必须写出：

```text
Business change
    -> demonstrated change pressure
    -> architectural requirement
    -> smallest useful enabler
    -> verification evidence
```

一次未来可能性不足以创建完整插件系统、Factory、接口层或平台。真正的压力可以来自重复变更穿过同一不稳定边界、多个 caller 重复协议转换造成缺陷、旧新路径必须共存，或依赖方向已经阻碍可验证变更。业务不变量和一致性边界则路由到 `ddd-lite`。

## Release Behavior Baseline

重要的已发布行为需要在合适的边界冻结为可执行 baseline：

1. **Service Behavior Baseline**：业务输入/输出、成功/错误语义、状态变化和重要副作用。
2. **Persistence Integration Baseline**：真实存储 adapter 的 Save/Load/Update、事务、约束、映射和迁移行为。
3. **Outbound Contract Baseline**：Port、Adapter 与 provider/protocol 的请求、响应、错误、超时、重试和幂等语义。
4. **Inbound Mapping Baseline**：transport 到 command、结果/错误到 transport 的映射。

Service 测试不能证明真实数据库 adapter；mock 的调用次数不能证明 outbound contract；也不要在每个 transport 重复完整业务测试。baseline 失败且没有授权行为变化时，修实现或测试设置；只有明确授权的行为变化才能同步更新需求、决策、record、baseline、实现和 release notes。

## Feature Change Record

推荐的项目级记录路径是 `docs/changes/<feature-name>.md`，包括：Request、Requirement Clarification、Requirement Reconciliation、Approved Requirement Contract、Repository Analysis、Business Change / Impact Analysis、Architecture Pressure Analysis、Design Decisions、Implementation Plan、Incremental Implementation / Discovery Notes、四类 Release Behavior Baseline、Change Review、Verification 和 Release Traceability。

记录不是第二份代码。它的价值是让实现中的发现、计划偏离、用户决策、验证证据和最终发布 artifact 互相可追溯。完整模板见 [feature-change-record.md](skills/engineering-philosophy/references/feature-change-record.md)。

## Routing

选择拥有当前主要决策的最小 Skill：

| Signal | Primary Skill | 典型协作 |
| --- | --- | --- |
| 需求不清、需求冲突、重复能力或用户决策 | `requirement-engineering` | 明确后进入 `change-planning` |
| 需求已批准，需要仓库影响分析、依赖和风险 | `change-planning` | 大变更进入 `incremental-implementation` |
| 已证明的技术变更压力、DI、Port、Adapter、依赖方向 | `architecture-boundaries` | 发现业务不变量时协作 `ddd-lite` |
| 业务不变量、生命周期、一致性边界 | `ddd-lite` | 技术翻译时协作 `architecture-boundaries` |
| 大型迁移、兼容期、vertical slice 排序 | `incremental-implementation` | 协作 `test-driven-development` |
| 新行为或 baseline 实现 | `test-driven-development` | 实际失败时转 `systematic-debugging` |
| 实际失败、回归、超时或 pipeline 错误 | `systematic-debugging` | 需要回归测试时协作 TDD |
| diff、PR/MR、Gate 3 | `code-review-and-quality` | 发现真实缺陷时转 debugging |
| branch、commit、version、tag、CHANGELOG | `git-workflow-and-versioning` | 发布自动化时协作 CI/CD |
| pipeline、artifact、部署健康、Gate 4 | `ci-cd-and-automation` | 失败时转 debugging |
| 仓库变化需要更新 Agent 知识、分类 artifact、判断是否生成 Skill | `knowledge-compilation` | 发现技术边界时协作 architecture-boundaries；发现业务不变量时协作 ddd-lite |
| 显式要求 Codex 将最小本地仓库上下文交给 ChatGPT Web 做规划/评审，再回来执行 | `chatgpt-plan-execute` | ChatGPT 返回后继续路由到拥有实际工程决策的 focused Skill |
| 项目知识晋升为跨项目/全局规则 | `engineering-philosophy` | `knowledge-compilation` 提供 provenance 和 eval 证据 |

完整的 primary、secondary、forbidden 和升级条件见 [routing-matrix.md](skills/engineering-philosophy/references/routing-matrix.md)。在 Codex 中可以显式调用，例如 `$architecture-boundaries`、`$ddd-lite`、`$requirement-engineering`、`$chatgpt-plan-execute`；其他 Agent 可以根据 description 自动触发 specialist Skill。`chatgpt-plan-execute` 是例外：它跨越源码外发边界，因此必须显式调用，不能根据普通编码请求自动触发。

## Migrating from v0.2.x

v0.3.0 只重命名两个 Skill；v0.4.0 在此基础上新增 `knowledge-compilation`，稳定版本总数为 12。当前 `Unreleased` 的 `chatgpt-plan-execute` 不改变这个历史迁移事实：

| v0.2.x | v0.3.0 |
| --- | --- |
| `spec-driven-development` | `requirement-engineering` |
| `planning-and-task-breakdown` | `change-planning` |

先移除旧 Skill，再从新仓库身份安装：

```sh
npx skills@latest remove spec-driven-development planning-and-task-breakdown \
  --global \
  --yes

npx skills@latest add hugo2lee/engineering-philosophy \
  --skill '*' \
  --global \
  --agent codex \
  --agent cline \
  --yes
```

这里使用的是当前 CLI 已验证的 `remove [skills...] --global --yes` 语法。正式安装目标是 `hugo2lee/engineering-philosophy`；迁移细节见 [v0.3.0 skill rename migration](docs/migrations/v0.3.0-skill-renames.md)。

## Validation

维护者可以运行：

```sh
scripts/validate.sh
scripts/smoke-test-npx.sh
scripts/deploy.sh --dry-run
git diff --check
```

验证器会读取 `skills/registry.yaml`，动态检查 active published Skill set 的标准 frontmatter、`agents/openai.yaml`、metadata version、references 链接、独立 eval、routing eval、30 个 feature lifecycle cases、31 个 knowledge lifecycle cases、registry 一致性、生成 Skill sidecar、JSON Schema fixtures 和文档版本一致性。PyYAML、`jsonschema>=4,<5` 与 Agent Skills reference validator 是验证依赖；例如：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install "PyYAML>=6,<7" "jsonschema>=4,<5" "skills-ref==0.1.1"
scripts/validate.sh
```

GitHub Actions 会在 push 和 pull request 上自动运行 validation、ShellCheck 和临时 HOME 下的 npx discovery/installation smoke test。CI 不会写入维护者机器的 Agent 配置。

## Releases

v0.4.0 is the current stable release:

```text
v0.4.0 — Continuous Knowledge Compilation
```

Stable releases use annotated `vMAJOR.MINOR.PATCH` tags. A pushed stable tag runs the repository validation workflow first, and the GitHub Release is published only after validation succeeds. The released `v0.1.0`, `v0.2.0`, `v0.2.1`, and `v0.3.0` tags remain immutable.

维护者发布后续版本时，可以在已通过 master CI 的最终 release commit 上执行：

```sh
git tag -a vX.Y.Z <release-commit> \
  -m "vX.Y.Z — <release title>"
git push origin vX.Y.Z
```

仓库的 GitHub Actions 会对符合 `vMAJOR.MINOR.PATCH` 的新 Tag 自动执行验证，并在验证成功后创建 Release。发布检查项见 [docs/release-checklist.md](docs/release-checklist.md)。

## Design Principle

> Prefer the simplest architecture that preserves meaningful boundaries.
