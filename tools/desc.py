import os, re, sys
root = os.path.expanduser('~/.claude/skills')
rows = []
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, 'SKILL.md')
    if not os.path.exists(p): continue
    txt = open(p, encoding='utf-8', errors='replace').read()
    m = re.match(r'---\n(.*?)\n---', txt, re.S)
    fm = m.group(1) if m else ''
    dm = re.search(r'^description:\s*(.*?)(?=^\w+:|\Z)', fm, re.M | re.S)
    desc = ' '.join(dm.group(1).split()) if dm else '(none)'
    rows.append((d, len(desc), len(txt), desc))
tot = sum(r[1] for r in rows)
print(f"{len(rows)} skills, description chars total = {tot}\n")
for d, dl, bl, desc in sorted(rows, key=lambda r: -r[1]):
    print(f"--- {d}  [desc {dl} chars | body {bl} chars]")
    print(f"    {desc}\n")
