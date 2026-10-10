# devkit

从 0 开发一套软件系统用的 skill 集合。**每个阶段只有一个 skill**，
二十一个 skill 覆盖从第一个模糊想法到上线收尾的全过程。

内容全部来自四个上游仓库，不是重写，是**裁决后的收录**：同一个阶段有多个候选时，
按下面的标准逐项打分，只留一个，落选的记在案。裁决依据见「冲突裁决」一节，
对原文做过的每一次改动见 `CHANGES.md`，署名与许可证见 `ATTRIBUTION.md`。

---

## 一、评估标准

六条，按权重排序。前两条决定胜负的次数最多。

| # | 标准 | 怎么看 |
|---|---|---|
| 1 | **触发精确度** | description 是常驻上下文里的指针，决定 skill 何时被选中。只写触发条件，不写内容简介；每个分支只给一个触发词，同义词是同一分支写了两遍。**用更少字符说清同样的触发条件者胜。** |
| 2 | **堵口设计** | 是否预判并封堵 agent 的逃逸借口。有 Iron Law、Common Rationalizations、Red Flags 这类条款的，意味着作者观察过失败再针对性地写，而不是凭空列最佳实践。 |
| 3 | **确定性载体** | 能力放在脚本与模板里，还是只靠散文。可执行的东西比三千字描述同一件事更可靠。 |
| 4 | **渐进式披露** | 主文件只留所有分支都需要的内容，分支性内容推到参考文件后面。单文件超过一万字符又没有参考目录的，是 bloat 的典型信号。 |
| 5 | **耦合成本** | 是否依赖同仓库的其他 skill，或需要先跑一次性配置。耦合越深，单独收录后越容易出断链。 |
| 6 | **与内置重叠** | Claude Code 内置已覆盖的，一律不收。 |

---

## 二、冲突裁决

### TDD：三个同名候选

| 候选 | desc | body | 披露 | 反借口条款 |
|---|---:|---:|---|---|
| **obra/test-driven-development** | **79** | 9,648 | 有，writing-good-tests.md | Iron Law、Common Rationalizations、Red Flags、Verification Checklist |
| addyosmani/test-driven-development | 296 | 16,517 | 无 | Common Rationalizations、Red Flags |
| mattpocock/tdd | 171 | 3,629 | 有，tests.md、mocking.md | 无 |

**选 obra。** 它用 79 字符说清了触发条件，是三者的四分之一到三分之一，而内容覆盖最全。

**补齐落选者的不可替代部分。** mattpocock 有一个另外两家都没有的步骤：写第一个测试之前，
先把要测的 seam 写下来并和人确认。没有这一步，测试精力会均匀摊到所有边界而不是关键路径。
它的好测试与坏测试对照、以及"只在系统边界 mock"的规则也比 obra 具体。
这些原文收录为 `skills/test-driven-development/seams-and-mocking.md`，
并在主文件里加了指针。

### 调试：三个候选

| 候选 | desc | 结构 | 支撑文件 |
|---|---:|---|---|
| **obra/systematic-debugging** | **91** | 四阶段 + Iron Law + 反借口 | root-cause-tracing、defense-in-depth、condition-based-waiting、find-polluter.sh |
| addyosmani/debugging-and-error-recovery | 296 | 六步 triage，带命令 | 无 |
| mattpocock/diagnosing-bugs | 134 | 六阶段 | hitl-loop 模板 |

**选 obra。** 同样是触发最便宜、支撑文件最多、唯一带反借口条款的一个。

**补齐。** mattpocock 的 Phase 1 是三者里最强的一个洞见：先造一个能对这个 bug 变红的
紧凑信号，剩下的二分、假设、埋点都只是消费它；没有这个信号，再怎么读代码也找不到原因。
obra 要求先定位根因，但没说根因怎么被逼出来。该节原文收录为
`skills/systematic-debugging/building-a-feedback-loop.md`，连同它引用的脚本。

### 代码评审：四个候选，内置胜出

| 候选 | 体量 | 判定 |
|---|---:|---|
| **内置 `/code-review`** | 0 常驻 | **选它。** 自带验证轮、结构化输出、`--fix` 与 `--comment` |
| addyosmani/code-review-and-quality | 20,976 | 全样本最大的单文件。五轴与内置重合 |
| obra/requesting-code-review | 2,977 | 与内置重合 |
| mattpocock/code-review | 6,670 | 需要先配置 spec 源与 standards 文档 |

**另收 obra/receiving-code-review。** 它管的是收到意见之后怎么办，含禁止回应、
何时该反驳、实施顺序。四个候选里只有它覆盖这一面，与评审本身不重叠。

obra 的 reviewer 子 agent 提示词模板确实被派发流程需要，原文收进
`references/code-reviewer.md`，但它的 SKILL.md 不收。

### 计划：三个候选

obra/writing-plans 与 addyosmani/planning-and-task-breakdown 的 body 几乎同样大
（10,335 与 10,564），结构也近乎一致：都有任务模板、垂直切分、检查点。
分不出内容高下时，**按第一条标准判**：obra 的 description 是 84 字符，addyosmani 是 296。
选 obra。

mattpocock 的 to-spec 与 to-tickets 排除，不是因为差，是因为第五条：
两者都要求先跑 `/setup-matt-pocock-skills` 配好 issue tracker 与 triage 标签词表，
否则会直接让用户去跑配置。单独收录会把这个配置负担带进来。

### 需求与规格：不是替代，是顺序

四个候选里有两个该同时收，因为它们管的是前后两步：

- **obra/brainstorming** 管模糊想法到设计文档，产出 `docs/devkit/specs/`。
- **addyosmani/spec-driven-development** 管设计到项目契约，产出技术栈、命令、
  目录结构、代码风格、测试策略。从 0 开发时这份契约就是后面所有 skill 的共同前提，
  不可缺。

addyosmani 的 interview-me 与 idea-refine 排除：与 brainstorming 的
"Establish Shared Understanding" 正面重叠。interview-me 的"一次只问一个问题、
95% 置信度停止"是个好机制，但不值得为它承担一个重复槽位。

---

## 三、收录清单

二十一个。路由表在 `skills/devkit-router/SKILL.md`，开发时先调它。

| 阶段 | Skill | 来源 | desc |
|---|---|---|---:|
| 路由 | devkit-router | 本套件 | 178 |
| 想法到设计 | brainstorming | obra | 198 |
| 项目契约 | spec-driven-development | addyosmani | 431 |
| 领域词汇与 ADR | domain-modeling | mattpocock | 151 |
| 模块边界 | codebase-design | mattpocock | 265 |
| 接口设计 | api-and-interface-design | addyosmani | 251 |
| 实现计划 | writing-plans | obra | 84 |
| 隔离工作区 | using-git-worktrees | obra | 196 |
| 内联执行 | executing-plans | obra | 170 |
| 子 agent 执行 | subagent-driven-development | obra | 85 |
| 并行杂活 | dispatching-parallel-agents | obra | 106 |
| 写代码 | test-driven-development | obra | 79 |
| 查问题 | systematic-debugging | obra | 91 |
| 前端视觉 | frontend-design | anthropics | 204 |
| 浏览器验证 | webapp-testing | anthropics | 204 |
| 埋点 | observability-and-instrumentation | addyosmani | 307 |
| 流水线 | ci-cd-and-automation | addyosmani | 207 |
| 完工把关 | verification-before-completion | obra | 225 |
| 接受评审 | receiving-code-review | obra | 234 |
| 上线 | shipping-and-launch | addyosmani | 271 |
| 合并收尾 | finishing-a-development-branch | obra | 101 |

`references/` 下另有六份被上述 skill 引用的共享文档：完工定义、安全清单、
性能清单、可访问性清单、可观测性清单、reviewer 提示词模板。

---

## 四、成本

| 项 | 字符 | 约合 token |
|---|---:|---:|
| 本套件二十一个的常驻 description | 4,038 | 1,122 |
| 平均每个 | 192 | 53 |
| 全部正文与脚本，按需加载 | 385 KB | 不计入常驻 |

作为对照：上游 obra 十五个加 addyosmani 二十五个共 40 个，常驻 10,995 字符。
本套件用一半多一点的 skill 数量覆盖同样的生命周期，常驻只用其三分之一，
差额来自第一条标准，即同等内容下优先选 description 更省的那个。

---

## 五、按需启用

**不全局安装。** 全局启用会让这 1,122 token 出现在每一个会话里，包括与开发无关的会话。
本套件只在要开发系统的那个项目里打开。

```bash
/Users/jingzhong.zhang/jz/code/github/skill/devkit/enable.sh ~/path/to/project
```

这条命令只写 `<项目>/.claude/settings.json`，把本目录登记为该项目的 marketplace
并启用插件，不碰 `~/.claude/` 下的任何文件。已有配置会被合并而非覆盖，
改动前自动备份为同名 `.bak-<时间戳>` 文件。重启该项目的会话后生效。

| 命令 | 作用 |
|---|---|
| `enable.sh <项目>` | 在该项目启用，省略参数则用当前目录 |
| `enable.sh --off <项目>` | 关闭，并清掉空下来的配置键 |
| `enable.sh --status <项目>` | 查看该项目当前是否启用 |
| `verify.sh` | 结构自检：frontmatter、命名、断链、清单合法性、常驻开销 |

项目做完就 `--off`，常驻开销随即归零。同时开多个项目时各自独立，互不影响。

## 六、使用

会话里第一件事是调 `devkit-router`，它把当前阶段对应到唯一一个 skill。
阶段切换时回到路由表。阶段不可跳：没有设计不要进计划，没有验证不要说完成。

内置命令负责本套件刻意不收的四件事：`/code-review` 评审、`/security-review` 安全、
`/simplify` 清理、`/run` 跑起来。项目第一次成形后用 `/init` 把约定写进 `CLAUDE.md`。

## 七、维护

上游升级时不要就地改本目录。重新从上游复制选中的 skill，然后重放 `CHANGES.md`
里的五类改动。新增 skill 之前先按第一节的六条标准过一遍，尤其确认它不与
已有的二十一个抢同一个阶段。
