# Attribution and License Boundaries

本仓库的 Skill 文本、示例和评测案例是面向通用软件工程场景重新编写的原创整理。

设计过程中参考了公开的软件工程思想，包括 Ports and Adapters、Dependency Inversion、务实 DDD、TDD、系统化调试和持续交付实践。本仓库不直接复制上游 Skill 的长篇文本、代码或专有资产。

如果后续加入来自外部项目的实质性文字、代码或资源，必须在合并前：

1. 记录来源链接；
2. 核对原始许可证；
3. 保留必要的版权和许可证声明；
4. 确认其与本仓库现有许可证兼容。

本仓库根目录的 LICENSE 文件是当前法律许可文本，新增内容默认受该许可证约束。

v0.2.0 的格式和分发验证参考了以下公开项目，仅使用其公开规范、命令和兼容性信息，没有复制其 Skill 正文：

- [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)：`SKILL.md` frontmatter、目录结构和 progressive disclosure 约定。该规范项目的相关参考实现采用 Apache-2.0 许可证。
- [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)：标准级 frontmatter validator 的参考实现；其 README 明确说明它是 demonstration/reference library。本仓库只把可安装的 `skills-ref` 命令作为验证工具使用，不把它的实现代码纳入源码。
- [vercel-labs/skills](https://github.com/vercel-labs/skills)：`npx skills` 的公开 CLI 命令和 Agent 目录兼容性说明。该项目采用 MIT 许可证；本仓库没有复制其实现代码。

## ChatGPT Web workflow design references

`chatgpt-plan-execute` 为本仓库独立编写的 workflow Skill。设计时参考了以下公开项目中已经验证过的交接思路，但没有复制其 Skill 正文、脚本或专有资产：

- [Shuvomoy/AutoOPT](https://github.com/Shuvomoy/AutoOPT) 的 `chatgpt-pro-handoff` / `chatgpt-pro-session`：参考 context packaging、manifest、response import 与 persistent conversation/session 的职责拆分。
- [Wangnov/chatgpt-skill](https://github.com/Wangnov/chatgpt-skill) 的 `codex-chatgpt-skill`：参考通过 Codex Chrome Extension 复用用户已认证的 ChatGPT Web / Chrome session，并优先通过可见网页交互完成 handoff。

本仓库在这些公开思路之上重新定义了自己的边界：精确文件选择、secret fail-closed、显式上传授权、repository facts 优先、ChatGPT 作为 planner/reviewer、Codex 作为 explorer/executor/verifier，以及本地可执行验证作为完成条件。
