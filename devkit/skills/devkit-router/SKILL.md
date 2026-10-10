---
name: devkit-router
description: Route a software build task to the right devkit skill. Use when starting a new system or feature, when a build task spans more than one stage, or when unsure which skill applies.
---

# devkit router

One skill owns each stage. Pick the row you are in, invoke that skill, and come back
here when the stage changes. Never run two skills from the same row.

## The pipeline

| # | 阶段 | Skill | 产出 |
|---|---|---|---|
| 1 | 把模糊想法变成设计 | `devkit:brainstorming` | `docs/devkit/specs/<date>-<topic>-design.md` |
| 2 | 定项目契约 | `devkit:spec-driven-development` | 技术栈、命令、目录、代码风格、测试策略 |
| 3 | 固定领域词汇与决策 | `devkit:domain-modeling` | `GLOSSARY.md`、`docs/adr/` |
| 4 | 划模块边界 | `devkit:codebase-design` | 深模块与 seam 的划分 |
| 5 | 设计对外接口 | `devkit:api-and-interface-design` | API 契约与版本策略 |
| 6 | 拆实现计划 | `devkit:writing-plans` | `docs/devkit/plans/<feature>-plan.md` |
| 7 | 开隔离工作区 | `devkit:using-git-worktrees` | 独立 worktree 与分支 |
| 8 | 执行计划 | `devkit:executing-plans` 或 `devkit:subagent-driven-development` | 见下方选择规则 |
| 9 | 写每一行代码 | `devkit:test-driven-development` | 先红后绿的测试与实现 |
| 10 | 任何异常 | `devkit:systematic-debugging` | 根因，而非症状补丁 |
| 11 | 前端视觉 | `devkit:frontend-design` | 有主张的视觉方向 |
| 12 | 浏览器端验证 | `devkit:webapp-testing` | Playwright 脚本与证据 |
| 13 | 埋点 | `devkit:observability-and-instrumentation` | 日志、指标、追踪、告警 |
| 14 | 流水线 | `devkit:ci-cd-and-automation` | 质量门禁与部署流水线 |
| 15 | 宣称完成前 | `devkit:verification-before-completion` | 实际跑过的验证命令与输出 |
| 16 | 收到评审意见 | `devkit:receiving-code-review` | 对意见的处理，含何时该反驳 |
| 17 | 上线 | `devkit:shipping-and-launch` | 发布前清单 |
| 18 | 合并收尾 | `devkit:finishing-a-development-branch` | 集成方式的决定 |

第 8 行的选择：任务之间互不依赖且想并行，用 `devkit:subagent-driven-development`；
人在场逐条推进，用 `devkit:executing-plans`。两者都不适用而只是有一堆彼此独立的杂活，
用 `devkit:dispatching-parallel-agents`。

## 不归本套件管的四件事

这四件内置命令已经做得更好，本套件不收同类 skill，不要另找替代：

- 代码评审用 `/code-review`。本套件只收 `devkit:receiving-code-review`，它管的是
  收到意见之后怎么做，和评审本身不重叠。
- 安全审查用 `/security-review`。
- 清理与简化用 `/simplify`。
- 把应用跑起来看效果用 `/run`。

项目第一次成形后，用 `/init` 把约定写进 `CLAUDE.md`。

## 两条硬规则

**阶段不可跳。** 没有第 1 步的设计就不要进第 6 步的计划；没有第 15 步的验证就不要说完成。
觉得"这个太简单不值得走流程"时，这个念头本身就是跳步的信号。

**一个阶段只用一个 skill。** 本套件已经在二十余个候选里为每个阶段选定了唯一一个，
选择依据记在 `README.md`。再引入同类 skill 会让路由变得不确定。
