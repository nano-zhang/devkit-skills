# di-* Skill 路由审计与改写建议

审计时间：2026-10-09
审计对象：`~/.claude/skills/di-*`（18 个，均为指向 `di-cli-shopee` 安装包的软链接）

> **重要**：这些文件是 di-cli 的 bundled skills，每次 CLI 升级会自动 re-land 并检测 drift
> （见 di-shared `_notice.skills` 一节）。**不要就地编辑**，改动会在下次升级时被覆盖。
> 以下改写应提交到 di-cli 源码仓的 `di/_skills/` 目录。

---

## 一、路由是怎么发生的

只有 `description` 常驻上下文，body 要等 skill 被选中后才加载。所以：

- **选不中的 skill 等于不存在**，body 写得再好也没用。
- **description 的每个字每轮都在花钱**。当前 18 个 di-* 的 description 合计 **11,155 字符**，
  再加上 smc（5 个）、understand-anything（10 个）和内置 skill，常驻预算相当可观。
- 路由是**模型在读 description 列表后做的一次软判断**，不是规则匹配。所以歧义、重叠、
  悬空指针都会直接变成路由错误。

### 四个可用的控制手段，按强度排序

| 手段 | 强度 | 适用场景 |
|---|---|---|
| Hook（PreToolUse 等） | 硬 | 必须发生的前置动作，如"跑 di 命令前先读 di-shared" |
| `disable-model-invocation: true` | 硬 | 只允许用户显式 `/xxx` 调用，杜绝误触发 |
| Router skill（单一入口 + 分发表） | 中 | 一个领域有多个子 skill 时 |
| description 措辞 | 软 | 默认手段，但只是软约束 |

当前 di-* **只用了最弱的那一种**。

---

## 二、发现的具体问题

### P1 — di-bot 与 di-livy 触发词正面冲突

```
di-livy  TRIGGER: ... debug a failing Spark task ... "Spark 任务", "Spark 作业"
di-bot   TRIGGER: ... "分析失败", "诊断作业", "任务挂了", "diagnose Spark task"
```

"我的 Spark 任务挂了" 同时命中两者。真实分工应该是：

- **di-livy = 执行**：跑 SQL、提交 batch、开 interactive session
- **di-bot = 事后诊断**：针对已经跑过的任务（有 app id / task id）做失败归因和性能调优

`debug a failing Spark task` 出现在 di-livy 里是错的，应删除。

### P2 — 三个悬空指针（指向不存在的 skill）

| 位置 | 原文 | 问题 |
|---|---|---|
| di-scheduler-adhoc-submit | "broad Scheduler incident debugging should use a dedicated debug skill instead" | 该 skill 不存在 |
| di-datahub | DO NOT TRIGGER "…Scheduler/Flink/Spark diagnosis" | Scheduler diagnosis 无归属 |
| di-ram | "permission request / approval stays under the shared `di ram ...` flow" | 无 skill 覆盖该 flow |

指向空处比不指更糟：模型会去找，找不到后自由发挥。

### P3 — di-ram 名实不符

description 自己承认：读操作用 `di user` / `di team` / `di project`，**不是** `di ram`。
但 skill 叫 di-ram，用户问"当前用户是谁"时，`di-ram` 这个名字提供的是反向线索。
建议改名为 `di-identity` 或 `di-access-lookup`。

### P4 — di-shared 的强制前置是软约束

```
TRIGGER when: any di-cli command is about to be invoked; any di-* skill is being loaded
```

"任何 di 命令之前"是一个**必然条件**，用散文表达必然条件是不可靠的。应该用 hook 硬化。

### P5 — 普遍性措辞问题

1. **开头浪费**：`Use di-cli to inspect ClickHouse...` —— 第一个有效词 "ClickHouse"
   在第 24 个字符。description 的句首是触发力最强的位置，应前置领域词。
2. **DO NOT TRIGGER 是负向表述**：禁令会把被禁行为拉进上下文，反而提高其可用性
   （"别想大象"效应）。应改为**正向指路**：`X 类请求 → 用 Y skill`。
   Flink 四件套已经这么做了（`use ../di-flink-metrics-promql/SKILL.md`），是正确范例。
3. **body 细节上浮**：di-ticket（952 字符）把五项能力边界全写进了 description，
   这些属于 body。

---

## 三、做得对的地方（应推广）

**Flink 四件套是整个库里路由设计最好的部分**：

- `di-flink` 作为 router，负责概念和跨面诊断
- 三个叶子 skill 各管一个面（REST / PromQL / runtime logs）
- 彼此的 DO NOT TRIGGER **指向具体兄弟文件路径**，而不是空泛排除

这个"router + 叶子 + 相对路径互指"的模式应推广到 datahub 系和 OLAP 系。

---

## 四、改写版 description（可直接替换）

### di-livy

```yaml
description: >-
  Spark 任务执行 via Livy — interactive session 与 batch job。
  TRIGGER when: 跑 Spark SQL、提交 Spark batch、开 interactive session、
  指定 yarn 队列提交，或提到 Livy / Spark session / Spark batch / 提交任务 / 执行 sql。
  对已经跑完的任务做失败归因或性能调优，用 di-bot。
  纯 Spark 原理或 API 问题不需要本 skill。
```

### di-bot

```yaml
description: >-
  Spark 任务事后诊断与调优 — 针对已经运行过的任务（有 app id / task id）做失败归因、
  性能分析、参数优化。目前覆盖 Spark Bot。
  TRIGGER when: spark 诊断 / Spark 优化 / Spark 性能 / 分析失败 / 诊断作业 / 任务挂了 /
  task failed analysis / performance tuning / di bot spark。
  要提交或运行一个新任务，用 di-livy。
```

### di-scheduler-adhoc-submit

```yaml
description: >-
  Scheduler adhoc 任务提交与跟进 via `di scheduler adhoc-task submit`（支持 spark、presto 等类型）。
  TRIGGER when: 用户要跑一次性 adhoc 任务、查 adhoc 运行状态，或提到 adhoc。
  非 adhoc 的 Scheduler 流程、以及 Scheduler 故障排查目前没有专门 skill，
  按 di-shared 的命令发现流程直接探索 `di scheduler --help`。
```

### di-ram（建议同时改名 di-identity）

```yaml
description: >-
  身份与访问关系查询（只读）：当前 RAM 用户、team 列表与详情、project 列表与详情、
  成员列表、Hadoop 账号在 project 内的角色。
  实际命令是 `di user ...` / `di team ...` / `di project ...`。
  TRIGGER when: 当前用户是谁 / 我有哪些 team / project / 默认 team / project 是什么 /
  某 team 或 project 的详情和成员 / 某 Hadoop 账号的角色。
  本 skill 只做查询。登录登出用 `di auth`；权限申请与审批目前无 skill 覆盖，
  按 di-shared 的命令发现流程处理。
```

### di-clickhouse（示范前置领域词 + 正向指路）

```yaml
description: >-
  ClickHouse 集群、database、table、schema 查询与只读 SQL，through `di clickhouse`。
  TRIGGER when: ClickHouse 集群元数据、库表 schema 查询、运维诊断、只读 ClickHouse SQL。
  StarRocks 用 di-starrocks，Druid 用 di-druid。
  本 skill 只读：DDL / DML / kill query 不在范围内。
```

---

## 五、两个结构性建议

### 建议 1：用 hook 硬化 di-shared 前置

在 `~/.claude/settings.json` 加 PreToolUse hook，匹配 `^di\s` 的 Bash 命令，
注入一行提醒"先读 di-shared"。这把 P4 从软约束变成硬约束，
同时可以把 di-shared 的 description 从 718 字符压到 200 以内——
因为触发不再依赖措辞。

### 建议 2：给 di-shared 加一张路由表

di-shared 当前 24,823 字符的 body 里**没有任何 skill 索引**。
它既然是所有 di-* 的必读前置，天然就是放分发表的地方：

```markdown
## 选择 skill

| 你要做的事 | skill |
|---|---|
| Hive 表元数据 / 血缘 / 分区 | di-datamap |
| 跑 Spark SQL / 提交 batch | di-livy |
| 诊断跑过的 Spark 任务 | di-bot |
| DataHub 任务创建与生命周期 | di-datahub |
| DataHub Ingestion 健康度诊断 | di-datahub-ingestion |
| Flink 任何操作 | di-flink（会继续分发到三个叶子 skill）|
| ClickHouse / StarRocks / Druid | 对应同名 skill |
| 对象存储 | di-s3 |
| 身份 / team / project 查询 | di-ram |
| 提单 / 工单 | di-ticket |
| Langfuse trace | di-langfuse |
| Adhoc 任务提交 | di-scheduler-adhoc-submit |
```

有了这张表，各 skill 的 DO NOT TRIGGER 段落可以大幅精简——
不需要每个 skill 都重复排除另外 17 个，只要指回 di-shared 的表即可。
粗估能从 11,155 字符的常驻预算里省下 30%–40%。
