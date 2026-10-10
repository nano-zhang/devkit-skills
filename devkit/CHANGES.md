# 对上游原文的改动清单

收录以原文为准。以下是全部改动，每条都是为了让这套 skill 在脱离原仓库后仍然自洽。
上游升级时，重新复制再重放这几条即可。

## 1. 命名空间改写

obra 的 skill 之间用 `superpowers:<name>` 互相引用。收录后插件名为 `devkit`，
全部改写为 `devkit:<name>`。涉及 writing-plans、executing-plans、
subagent-driven-development、systematic-debugging 四个 SKILL.md 和
test-driven-development/writing-good-tests.md。

## 2. 指向未收录 skill 的引用

| 原引用 | 处理 | 位置 |
|---|---|---|
| `superpowers:requesting-code-review` | 改为内置 `/code-review` 命令 | executing-plans、subagent-driven-development |
| `../requesting-code-review/code-reviewer.md` | 该 skill 的 SKILL.md 不收录，但这份 reviewer 子 agent 提示词模板是派发流程真正需要的文件，原文收进 `references/code-reviewer.md`，五处链接改指过去 | executing-plans、subagent-driven-development |
| `superpowers:writing-skills` | 删除该括注，保留原句 | test-driven-development/writing-good-tests.md |
| `../using-superpowers/references/` | 删除该路径，保留"无 subagent 工具时走内联执行"的条件 | executing-plans |

## 3. 产物路径

`docs/superpowers/` 改为 `docs/devkit/`，`.superpowers/` 改为 `.devkit/`。
markdown 与 scripts 同步改，共 12 个文件。
`brainstorming/scripts/server.cjs` 里的上游品牌 URL 不在改写范围内，保持原样。

## 4. 删除的文件

| 文件 | 原因 |
|---|---|
| systematic-debugging/CREATION-LOG.md、test-academic.md、test-pressure-1..3.md | 上游写这个 skill 时的过程产物，与使用无关 |
| codebase-design/agents/、domain-modeling/agents/ | 只含 `openai.yaml`，是其他 harness 的适配文件 |

## 5. 新增的文件

| 文件 | 内容 |
|---|---|
| skills/devkit-router/SKILL.md | 本套件自己编写的路由表 |
| skills/test-driven-development/seams-and-mocking.md | mattpocock `engineering/tdd` 的 Seams 与 Anti-patterns 两节，加 tests.md、mocking.md 原文 |
| skills/systematic-debugging/building-a-feedback-loop.md | mattpocock `engineering/diagnosing-bugs` 的 Phase 1 原文 |
| skills/systematic-debugging/hitl-loop.template.sh | 上一份文件引用的脚本，同源 |

两个主文件各加了一行指向新参考文件的指针，位置在 `## The Iron Law` 之前。
不加指针这两份文件不会被读到。
