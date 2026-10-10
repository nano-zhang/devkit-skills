# 本机 Skill 清单

盘点时间：2026-10-09
盘点范围：`jingzhong.zhang` 用户下所有生效的 skill 来源
复现方式：`python3 -I tools/inventory.py`

---

## 总览

**生效 31 个**（三个来源）+ **Claude Code 内置 15 个** = 46 个可用。

| 来源 | 数量 | 常驻 desc | 占比 | body |
|---|---:|---:|---:|---:|
| 个人 `~/.claude/skills/`（di-cli 下发） | 18 | 11,155 | 73% | 236,096 |
| 插件 `smc@3.2.3-smc.h0dc909885120` | 5 | 2,897 | 19% | 56,282 |
| 插件 `understand-anything@2.8.0` | 8 | 1,175 | 8% | 79,493 |
| **合计** | **31** | **15,227** | 100% | **371,871** |
| Claude Code 内置 | 15 | — | — | — |

单位为字符。常驻 description **约 4,400–6,100 tokens，每轮对话都在消耗**；
body 为按需加载，只在 skill 被选中后计入。

安装来源配置在 `~/.claude/settings.json`：

```json
"enabledPlugins": {
  "smc@smc-marketplace": true,
  "understand-anything@understand-anything-local": true
}
```

---

## 一、个人 skill：di-* 十八个

全部为指向 `di-cli-shopee` 安装包的**软链接**，由 di-cli 在升级时自动 re-land
并检测 drift。**不可就地修改**，改动会被覆盖（详见 `di-skills-routing-audit.md`）。

真实路径：
`~/.local/share/uv/tools/di-cli-shopee/lib/python3.12/site-packages/di/_skills/`

### 按领域分组

| 组 | skill | 职责 |
|---|---|---|
| **协议底座** | di-shared | envelope 契约、exit code、exit 10 确认门、`_notice` 协议、身份模型。所有 di-* 的必读前置 |
| **计算** | di-livy | Spark 执行：interactive session / batch job / SQL |
| | di-bot | Spark 事后诊断：失败归因、性能调优 |
| | di-scheduler-adhoc-submit | Scheduler adhoc 任务提交与跟进 |
| **Flink** | di-flink | router：平台概念 + 跨面诊断，分发到下面三个 |
| | di-flink-tracking-url-rest | Web UI REST 端点检查 |
| | di-flink-metrics-promql | Prometheus 指标与 PromQL |
| | di-flink-runtime-logs-query | 运行日志检索与下载 |
| **数据平台** | di-datahub | DataHub 任务生命周期：创建、CSV 上传、trigger、freeze/kill/reset |
| | di-datahub-ingestion | 摄取链路健康度：RTI/DCS/Mirror/BTI、marker 延迟、数据质量 |
| | di-datamap | Hive 元数据、分区、血缘、影响分析 |
| **OLAP** | di-clickhouse | 集群元数据 + schema + 只读 SQL |
| | di-starrocks | 同上，另含 catalog 与 load job 状态 |
| | di-druid | 同上，另含 supervisor 与 task 状态 |
| **存储** | di-s3 | Ozone S3G：读写删 + tag 变更（唯一明确含写操作） |
| **平台周边** | di-ram | 身份 / team / project 查询（只读） |
| | di-ticket | Data Infra 工单：创建、查询、评论、状态变更 |
| | di-langfuse | LLM trace、observation、session、prompt、score 读取 |

### 体量明细

| skill | desc | body |
|---|---:|---:|
| di-shared | 718 | 24,823 |
| di-datahub-ingestion | 656 | 24,815 |
| di-langfuse | 601 | 20,068 |
| di-ticket | 952 | 16,023 |
| di-flink | 636 | 13,425 |
| di-datahub | 814 | 12,869 |
| di-s3 | 455 | 12,086 |
| di-flink-tracking-url-rest | 817 | 11,752 |
| di-ram | 763 | 11,530 |
| di-datamap | 458 | 11,500 |
| di-flink-metrics-promql | 668 | 11,405 |
| di-druid | 526 | 11,215 |
| di-starrocks | 601 | 11,181 |
| di-flink-runtime-logs-query | 653 | 10,773 |
| di-livy | 509 | 10,378 |
| di-clickhouse | 449 | 9,229 |
| di-bot | 525 | 8,846 |
| di-scheduler-adhoc-submit | 354 | 4,178 |

---

## 二、插件 smc：Shopee 基础设施接入

来源为本地目录 marketplace `/Users/jingzhong.zhang/.smc/ai_plugin`。

| skill | desc | body | 职责 |
|---|---:|---:|---|
| logcli | 461 | 17,480 | Space Log 平台应用日志查询（PQL）、ALB/NGINX 日志 |
| smc-service | 667 | 15,567 | Bromo/ECP 服务、任务、部署、Runonce 作业运维 |
| smc-pam | 817 | 9,149 | PAM 网关特权访问：SSH/SCP、MySQL、Redis、EKS、网络设备 |
| smc | 519 | 8,266 | SMC 插件自身的发现、安装、更新 |
| setup-remote-ssh-wrapper | 433 | 5,820 | 本地 SSH wrapper 配置，供 VSCode/Cursor Remote SSH 使用 |

---

## 三、插件 understand-anything：代码库理解

另附 9 个专用 subagent（project-scanner、file-analyzer、architecture-analyzer、
domain-analyzer、article-analyzer、graph-reviewer、assemble-reviewer、
tour-builder、knowledge-graph-guide）。

| skill | desc | body | 职责 |
|---|---:|---:|---|
| understand | 215 | 47,483 | 主入口：代码库 → 可查询知识图谱 |
| understand-domain | 213 | 7,589 | 抽取业务域与流程图 |
| understand-knowledge | 196 | 5,438 | 处理 wiki 式知识库 |
| understand-dashboard | 108 | 5,232 | 启动可视化面板 |
| understand-diff | 114 | 4,088 | 分析 git diff / PR |
| understand-explain | 124 | 3,347 | 深入讲解单个文件或模块 |
| understand-onboard | 88 | 3,326 | 生成新人 onboarding 指南 |
| understand-chat | 117 | 2,990 | 基于图谱的代码库问答 |

---

## 四、Claude Code 内置十五个

| 类别 | skill |
|---|---|
| 代码质量 | code-review、simplify、security-review、init |
| 可视化与 artifact | dataviz、artifact-design、artifact-diagramming |
| harness 配置 | update-config、keybindings-help、fewer-permission-prompts、plugin-authoring |
| 开发与运行 | claude-api、workflow-authoring、loop、run |

---

## 五、未生效的部分

**官方 marketplace 已知但零安装。** `claude-plugins-official` 在
`known_marketplaces.json` 里，缓存中有 **33 个 SKILL.md**，但
`installed_plugins.json` 中没有任何条目，因此**全部未加载**。涉及插件：

```
claude-code-setup  claude-md-management  claude-security  cwc-makers
discord  example-plugin  frontend-design  hookify  imessage
math-olympiad  math-proof  mcp-server-dev  playground  plugin-dev
project-artifact  receipts  session-report  skill-creator  telegram
```

其中 `skill-creator`（官方带评测闭环的 skill 编写工具）和 `plugin-dev`
全套，对维护 di-* 库有直接价值，建议安装。

**克隆的研究仓库不在搜索路径上。** `repos/` 下 9 个 GitHub 仓库仅为参考材料，
不会被 Claude Code 加载：

```
anthropics_skills            官方参考实现 + 规范
obra_superpowers             完整开发方法论框架
mattpocock_skills            工程工作流，router skill 范例
addyosmani_agent-skills      研发生命周期 + slash command 组织
wshobson_agents              多 harness 插件市场
ComposioHQ_awesome-claude-skills   目录（864 个多为自动生成）
VoltAgent_awesome-agent-skills     纯索引目录
Nutlope_hallmark             单点：反 AI 味设计
multica-ai_andrej-karpathy-skills  单文件行为约束
```

（`affaan-m_ECC` 已删除：1027 个 SKILL.md 仅 296 个唯一名称，71% 为多 harness
目录复制与西语翻译重复计数。）

---

## 六、观察

**di-* 吃掉 73% 的常驻预算，但只覆盖一个领域。** 18 个 skill 平均每个 620 字符
description；understand-anything 用平均 147 字符说清了同量级的分工，
`understand-onboard` 只花 88 字符。这说明 di-* 的 description 存在可观压缩空间，
且有现成参照——省掉三到四成之后仍比 understand-anything 详细。

**体量分布很不均。** `di-shared` 与 `di-datahub-ingestion` 各约 24.8k 字符，
加载一次约 7k tokens；`understand` 高达 47.5k 字符，约 13k tokens，是单个 skill 之最。
这些重型 skill 适合做 progressive disclosure——把分支性内容拆进 `references/`，
主文件只留所有分支都需要的部分。目前只有 `di-flink` 有 `references/` 目录。

**日志领域存在未声明的邻接。** `logcli`（应用日志）与
`di-flink-runtime-logs-query`（Flink 运行日志）职责相邻，但两者 description
都未提及对方，用户问"查日志"时路由结果不确定。

路由层面的完整问题清单与改写建议见 **`di-skills-routing-audit.md`**。
