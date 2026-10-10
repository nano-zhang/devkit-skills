import os, re, sys, collections

root = sys.argv[1]
SKIP_DESC = 'Rube MCP'
repo_skills = {}   # repo -> list of (name, path, body_len, fields, subdirs)

for repo in sorted(os.listdir(root)):
    rp = os.path.join(root, repo)
    if not os.path.isdir(rp): continue
    items = []
    for dirpath, dirnames, filenames in os.walk(rp):
        dirnames[:] = [d for d in dirnames if d != '.git']
        if 'SKILL.md' not in filenames: continue
        p = os.path.join(dirpath, 'SKILL.md')
        txt = open(p, encoding='utf-8', errors='replace').read()
        m = re.match(r'---\n(.*?)\n---', txt, re.S)
        fm = m.group(1) if m else ''
        if SKIP_DESC in fm: continue          # drop Composio auto-generated
        fields = re.findall(r'^([a-zA-Z_-]+):', fm, re.M)
        nm = re.search(r'^name:\s*(.+)$', fm, re.M)
        name = nm.group(1).strip() if nm else os.path.basename(dirpath)
        subs = [d for d in dirnames]
        items.append((name, dirpath, len(txt), fields, subs))
    if items: repo_skills[repo] = items

print("## 每仓库规模（已剔除 Composio 自动生成）\n")
for r, items in repo_skills.items():
    bodies = sorted(x[2] for x in items)
    med = bodies[len(bodies)//2]
    print(f"{r:<36} {len(items):>4} skills | body 中位 {med:>6,} | 最大 {bodies[-1]:>7,}")

print("\n## frontmatter 字段使用频率\n")
for r, items in repo_skills.items():
    c = collections.Counter(f for x in items for f in set(x[3]))
    n = len(items)
    top = ', '.join(f"{k}={v}/{n}" for k, v in c.most_common(9))
    print(f"{r:<36} {top}")

print("\n## 渐进式披露（含子目录的 skill 占比）\n")
for r, items in repo_skills.items():
    withsub = [x for x in items if x[4]]
    subnames = collections.Counter(s for x in items for s in x[4])
    print(f"{r:<36} {len(withsub)}/{len(items)} 带子目录 | {dict(subnames.most_common(5))}")

print("\n## 跨仓库重复主题（出现在 >=3 个独立仓库）\n")
norm = lambda s: re.sub(r'[-_\s]+', '-', s.strip().lower())
topic = collections.defaultdict(set)
for r, items in repo_skills.items():
    for name, *_ in items:
        topic[norm(name)].add(r)
for t, rs in sorted(topic.items(), key=lambda kv: -len(kv[1])):
    if len(rs) >= 3:
        print(f"  {t:<34} {len(rs)} 个仓库: {', '.join(sorted(x.split('_')[0] for x in rs))}")
