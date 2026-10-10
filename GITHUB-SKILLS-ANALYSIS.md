# GitHub Skill 仓库调研与分析

调研时间：2026-10-09
目录：`/Users/jingzhong.zhang/jz/code/github/skill`
样本：GitHub 上 skill 相关仓库，按 star 排序取头部，克隆 10 个，删除 1 个注水仓库后留 9 个

复现脚本（均可重跑）：

```bash
python3 -I tools/survey.py repos      # 每仓库 skill 清单 + frontmatter
python3 -I tools/crossrepo.py repos   # 规模、字段使用、渐进式披露
python3 -I tools/topics.py repos      # 主题分布
```

---

## 一、样本总览

| 仓库 | star | 标称 skill | **真实 skill** | 定位 |
|---|---:|---:|---:|---|
| wshobson/agents | 40k | 184 | **184** | 多 harness 插件市场，覆盖面最广 |
| ComposioHQ/awesome-claude-skills | 77k | 864 | **94** | 770 个为自动生成的 MCP 包装 |
| mattpocock/skills | 282k | 38 | **38** | 资深工程师日常工作流 |
| addyosmani/agent-skills | 104k | 25 | **25** | 研发生命周期全覆盖 |
| anthropics/skills | 180k | 20 | **20** | 官方参考实现 |
| obra/superpowers | 297k | 15 | **15** | 完整开发方法论框架 |
| Nutlope/hallmark | 30k | 1 | **1** | 单点：反 AI 味设计 |
| multica-ai/andrej-karpathy-skills | 218k | 1 | **1** | 单文件行为约束 |
| VoltAgent/awesome-agent-skills | 35k | 0 | **0** | 纯索引目录（1,892 行 README） |
| **合计** | | 1,148 | **378** | |

**标称数字普遍不可信。** 剔除自动生成内容后，真实 skill 总量是标称的三分之一。

已删除：`affaan-m/ECC`（276k star，标称 1,027 个 SKILL.md，实际仅 296 个唯一名称——
71% 为多 harness 目录复制与西班牙语翻译重复计数，96MB）。
需要时 `git clone --depth 1 https://github.com/affaan-m/ECC` 取回。

---

## 二、体量分布

| 仓库 | body 中位 | body 最大 | 最大者 |
|---|---:|---:|---|
| mattpocock | 3,589 | 12,580 | |
| wshobson | 5,423 | 26,290 | |
| ComposioHQ | 6,221 | 25,533 | |
| obra | 7,729 | 32,358 | writing-skills |
| anthropics | 8,542 | **103,457** | claude-api |
| addyosmani | **13,497** | 20,956 | |
| Nutlope/hallmark | 66,585 | 66,585 | 单 skill |

两端都值得注意。mattpocock 中位仅 3,589 字符，与他"小、可组合、易改"的明确主张一致。
addyosmani 中位 13,497 是最大的，而它恰恰是渐进式披露用得最少的仓库（见下节）——
这个组合是 bloat 的典型信号。

---

## 三、跨仓库发现

### 3.1 frontmatter 的事实标准只有两个字段

| 仓库 | name | description | 其他 |
|---|---|---|---|
| 全部 8 个 | 100% | 100% | — |
| mattpocock | | | `disable-model-invocation` 23/38 |
| anthropics | | | `license` 17/20 |
| ComposioHQ | | | `requires` 62/94（MCP 依赖） |
| wshobson | | | `version` 14/184 |

`name` + `description` 在所有仓库 100% 覆盖，其余字段都是局部约定。

**唯一有行为意义的扩展是 mattpocock 的 `disable-model-invocation: true`**——
38 个 skill 里 23 个（61%）标了它，意思是只允许用户显式 `/xxx` 调用，模型不得自行触发。
这是整个样本里唯一被大规模使用的硬路由控制手段。其他仓库全部依赖 description 措辞这种软约束。

### 3.2 渐进式披露分化严重

| 仓库 | 带子目录比例 | 主要子目录 |
|---|---|---|
| wshobson | **152/184 (83%)** | `references/` ×152 |
| anthropics | 14/20 (70%) | `scripts/` ×8、`examples/` ×2 |
| obra | 6/15 (40%) | `scripts/`、`references/`、`templates/` |
| ComposioHQ | 12/94 (13%) | `scripts/` ×8 |
| addyosmani | **4/25 (16%)** | `references/` ×3 |

wshobson 把 `references/` 做成了近乎强制的约定，是最系统的一个。anthropics 的子目录
以 `scripts/` 为主——它的复杂 skill（docx/pdf/pptx/xlsx）靠真实可执行代码承载能力，
而不是靠更多散文。

mattpocock 看似 38/38 带子目录，但那个 `agents/` 里只有一个 `openai.yaml` 适配文件，
不是披露。他的真实披露方式是**同级兄弟文件**：`tdd/` 下并列 `SKILL.md`、`mocking.md`、
`tests.md`，`writing-for-agents/` 下并列 `SKILL-MECHANICS.md`。扁平、好改。

### 3.3 主题重合度揭示了共识区与前沿区

| 主题 | 覆盖仓库数 | 分布 |
|---|---:|---|
| TDD / 测试 | 6/8 | wshobson 8、addyosmani 2、其余各 1 |
| 前端 / 设计 | 6/8 | wshobson 19、anthropics 7、Composio 5 |
| 规划 / spec | 5/8 | mattpocock 4、obra 3、addyosmani 2 |
| 写 skill 本身 | 5/8 | 各 1 |
| 文档 | 5/8 | Composio 4、anthropics 2 |
| 代码审查 | 4/8 | wshobson 3、obra 2 |
| 调试 | 4/8 | obra 2、wshobson 2 |
| 安全 | 3/8 | wshobson 5 |
| **多 agent 编排** | 3/8 | wshobson 9、mattpocock 2、obra 2 |
| 部署 / CI | 2/8 | wshobson 5、addyosmani 2 |
| 反 AI 味写作 | 2/8 | Nutlope 1、wshobson 1 |

TDD 和前端设计是跨仓库共识最强的两块——**八个独立作者里有六个都认为值得单独写一个 skill**。

"写 skill 本身"出现在 5 个仓库，每个仓库恰好一个，说明这已经是公认的元能力。

多 agent 编排只在 3 个仓库出现但密度很高（wshobson 一家就 9 个），是正在成形的前沿区。

### 3.4 Composio 的"原创"部分有一大半是搬运

它那 94 个非自动生成 skill 里，**8 个与 anthropics/skills 完全同名**：

```
brand-guidelines  canvas-design  internal-comms  mcp-builder
skill-creator  slack-gif-creator  theme-factory  webapp-testing
```

加上 `artifacts-builder`、`document-skills`、`template-skill` 等变体，官方那套基本被整体
vendored 进去了。真正 Composio 原创的是 `competitive-ads-extractor`、`invoice-organizer`、
`lead-research-assistant`、`twitter-algorithm-optimizer` 这类业务向 skill。

---

## 四、四个值得精读的仓库

### anthropics/skills — 地基

20 个 skill 分创意设计、开发技术、企业沟通、文档处理四组。`docx`/`pdf`/`pptx`/`xlsx`
是 Claude 文档能力的生产级源码（source-available，非开源），复杂 skill 如何组织
`scripts/` + `references/` 看这几个最准。

`skill-creator` 最值得借鉴：自带 `agents/`（analyzer、comparator、grader 三个子 agent）、
`scripts/`（quick_validate、package_skill、improve_description、aggregate_benchmark）
和一套 eval viewer。官方把"写 skill"本身做成了**带评测闭环的工程流程**。

规范正文已迁至 agentskills.io，仓库 `spec/` 仅剩三行指路。

### obra/superpowers — 方法论最成体系

15 个 skill 串成强制流水线：

```
brainstorming → writing-plans → subagent-driven-development
  → requesting/receiving-code-review → verification-before-completion
  → finishing-a-development-branch
```

核心主张：**skill 要用 TDD 的方式写**。先跑 baseline 观察 agent 在没有 skill 时怎么违规、
记录它用了哪些"合理化借口"，再写 skill 专门堵这些洞，最后验证。
`writing-skills/SKILL.md` 有 32,358 字符，是这套思路的完整展开。

语气刻意强硬（"The Iron Law"、"Delete means delete"、"Violating the letter of the rules
is violating the spirit of the rules"），用绝对化措辞对抗模型找借口的倾向。

已适配十几种 harness（Codex、Cursor、Gemini CLI、Copilot CLI、Kimi、Qwen 等）。

### mattpocock/skills — 工程实践最克制

明确反对 BMAD/Spec-Kit 那种"接管整个流程"的做法，主张 skill 应当小、可组合、易改。
三个亮点：

1. **router skill**：`ask-matt` 专门负责在一堆 skill 里做路由分发
2. **invocation 控制**：61% 的 skill 标了 `disable-model-invocation: true`
3. **生命周期目录**：`skills/` 下分 `engineering/`、`productivity/`、`misc/`、
   `in-progress/`、`deprecated/`——skill 的成熟度直接体现在路径上

`productivity/writing-for-agents/SKILL.md` 是整个样本里写作质量最高的文档，
提出了几个可操作的概念：

- **context pointer**：description 是常驻上下文的指针，决定何时触发。
  每个分支只写一个触发词，同义词是"同一个分支写了两遍"，要合并。
- **两种负载**：context load（常驻上下文的 token 成本）vs cognitive load（人要记住哪些
  文档存在的成本）。后者不是越低越好，它是人保留判断权的代价。
- **信息层级三级**：in-file step → in-file reference → disclosed reference。
  分支是最干净的披露判据——所有分支都要的内联，只有部分分支到达的推到指针后面。
- **leading word**：用模型预训练里已有的紧凑概念（_lesson_、_tracer bullets_、_red_）
  做锚点，一个词顶一段话。自造词要额外花 token 定义，优先用已有词。
- **负向表述失效**：禁令会把被禁行为拉进上下文反而更可用（"别想大象"效应）。
  应直接陈述目标行为。

### addyosmani/agent-skills — 组织方式最好抄

25 个 skill 挂在 9 个 slash command 上，命令与研发生命周期一一对应：

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
/spec    /plan   /build   /test    /review  /ship
```

另有 `/constraints`、`/webperf`、`/code-simplify`。自带 `evals/` 和 `hooks/`。
`/build auto` 可在一次批准后自主跑完整个计划。

需要注意它的 body 中位 13,497 是全样本最大，而披露率只有 4/25——
抄它的组织方式，别抄它的篇幅。

---

## 五、可直接借鉴的五个模式

1. **router + 叶子 + 相对路径互指**。一个领域有多个子 skill 时，设一个 router 负责概念
   和跨面判断，叶子各管一个面，互相排除时给出**具体兄弟文件路径**而非空泛排除。

2. **`disable-model-invocation: true`**。凡是只应由人显式发起的 skill（有副作用的、
   需要人在场判断的），一律标上。这是样本里唯一被验证的硬路由手段。

3. **目录即生命周期**。`in-progress/` 和 `deprecated/` 让 skill 的成熟度可见，
   避免半成品和废弃品混在正式集合里影响路由。

4. **能力靠脚本而非散文**。anthropics 的复杂 skill 用 `scripts/` 承载确定性逻辑，
   SKILL.md 只讲何时用、怎么调。比写三千字描述同一件事更可靠。

5. **skill 的 TDD**。写之前先观察没有 skill 时 agent 怎么失败，记录具体的失败借口，
   针对性地写，再验证是否真的改变了行为。没见过失败就不知道自己在教什么。

---

## 六、目录现状

```
skill/
├── GITHUB-SKILLS-ANALYSIS.md     本文档
├── SKILL-INVENTORY.md            本机已装 skill 清单（另一主题，暂置）
├── di-skills-routing-audit.md    di-* 路由审计（另一主题，暂置）
├── tools/
│   ├── survey.py                 每仓库 skill 清单 + frontmatter
│   ├── crossrepo.py              规模、字段使用、渐进式披露
│   ├── topics.py                 主题分布
│   ├── inventory.py              本机已装 skill 盘点
│   └── desc.py                   description 体量分析
└── repos/                        9 个克隆仓库，合计约 84MB
```
