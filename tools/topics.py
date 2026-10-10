import os, re, sys, collections
root = sys.argv[1]
BUCKETS = {
 'TDD/测试': r'tdd|test-driven|testing|e2e|pytest|unit-test',
 '代码审查': r'code-review|review|multi-reviewer',
 '调试': r'debug|diagnos|error-recovery|troubleshoot',
 '规划/spec': r'spec|plan|brainstorm|task-breakdown|wayfinder|ticket',
 '写 skill 本身': r'skill-creator|writing-skills|skill-development|writing-for-agents|using-.*skills',
 '前端/设计': r'frontend|ui|design|canvas|theme|brand|landing|tailwind',
 '文档': r'doc|adr|changelog|openapi|readme',
 '安全': r'security|harden|auth|secrets|solidity',
 '多 agent 编排': r'parallel|subagent|dispatch|team-|orchestrat|coordination|handoff',
 '部署/CI': r'ci-cd|deploy|pipeline|github-actions|gitlab|ship|release',
 '反 AI 味写作': r'humaniz|avoid-ai|ai-writing|hallmark|slop',
}
rows = collections.defaultdict(lambda: collections.defaultdict(int))
for repo in sorted(os.listdir(root)):
    rp = os.path.join(root, repo)
    if not os.path.isdir(rp): continue
    for dirpath, dirnames, filenames in os.walk(rp):
        dirnames[:] = [d for d in dirnames if d != '.git']
        if 'SKILL.md' not in filenames: continue
        txt = open(os.path.join(dirpath,'SKILL.md'), encoding='utf-8', errors='replace').read(2000)
        if 'Rube MCP' in txt: continue
        nm = re.search(r'^name:\s*(.+)$', txt, re.M)
        name = (nm.group(1).strip() if nm else os.path.basename(dirpath)).lower()
        for b, pat in BUCKETS.items():
            if re.search(pat, name): rows[b][repo.split('_')[0]] += 1
print(f"{'主题':<16} {'仓库数':>5}  分布")
for b in BUCKETS:
    d = rows[b]
    if not d: continue
    print(f"{b:<16} {len(d):>5}  " + ', '.join(f"{k}:{v}" for k,v in sorted(d.items(), key=lambda kv:-kv[1])))
