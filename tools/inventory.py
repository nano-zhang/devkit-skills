import os, re, sys

SOURCES = [
    ("personal  ~/.claude/skills", os.path.expanduser("~/.claude/skills")),
    ("plugin    smc@3.2.3", os.path.expanduser("~/.claude/plugins/cache/smc-marketplace/smc/3.2.3-smc.h0dc909885120/skills")),
    ("plugin    understand-anything@2.8.0", os.path.expanduser("~/.claude/plugins/cache/understand-anything-local/understand-anything/2.8.0/skills")),
]

grand_desc = grand_body = grand_n = 0
for label, root in SOURCES:
    if not os.path.isdir(root):
        print(f"### {label}: MISSING\n"); continue
    rows = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d, "SKILL.md")
        if not os.path.exists(p): continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        m = re.match(r"---\n(.*?)\n---", txt, re.S)
        fm = m.group(1) if m else ""
        dm = re.search(r"^description:\s*(.*?)(?=^\w+:|\Z)", fm, re.M | re.S)
        desc = " ".join(dm.group(1).split()) if dm else ""
        rows.append((d, len(desc), len(txt)))
    dsum = sum(r[1] for r in rows); bsum = sum(r[2] for r in rows)
    grand_desc += dsum; grand_body += bsum; grand_n += len(rows)
    print(f"### {label}  —  {len(rows)} skills | desc {dsum:,} chars | body {bsum:,} chars")
    for d, dl, bl in sorted(rows, key=lambda r: -r[2]):
        print(f"      {d:<30} desc {dl:>4}  body {bl:>6,}")
    print()

print(f"=== ACTIVE TOTAL: {grand_n} skills | always-on desc {grand_desc:,} chars | on-demand body {grand_body:,} chars")
print(f"    desc ≈ {grand_desc/3.5:,.0f}–{grand_desc/2.5:,.0f} tokens burned every turn")
