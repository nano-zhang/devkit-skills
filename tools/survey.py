import os, sys, re

root = sys.argv[1]
for repo in sorted(os.listdir(root)):
    rp = os.path.join(root, repo)
    if not os.path.isdir(rp): continue
    skills = []
    for dirpath, dirnames, filenames in os.walk(rp):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for f in filenames:
            if f.upper() == 'SKILL.MD':
                skills.append(os.path.join(dirpath, f))
    # count other file types
    md = agents = cmds = 0
    for dirpath, dirnames, filenames in os.walk(rp):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for f in filenames:
            if f.endswith('.md'): md += 1
        if os.path.basename(dirpath) == 'agents': agents += len(filenames)
        if os.path.basename(dirpath) == 'commands': cmds += len(filenames)
    print(f"=== {repo}: SKILL.md={len(skills)}  all .md={md}  agents/={agents}  commands/={cmds}")
    for s in sorted(skills)[:400]:
        rel = os.path.relpath(s, rp)
        name = desc = ''
        try:
            txt = open(s, encoding='utf-8', errors='replace').read(4000)
        except Exception:
            continue
        m = re.match(r'---\n(.*?)\n---', txt, re.S)
        if m:
            fm = m.group(1)
            n = re.search(r'^name:\s*(.+)$', fm, re.M)
            d = re.search(r'^description:\s*(.+)$', fm, re.M | re.S)
            name = n.group(1).strip() if n else ''
            desc = d.group(1).strip().replace('\n', ' ')[:110] if d else ''
        print(f"   - {name or rel:<38} | {desc}")
    print()
