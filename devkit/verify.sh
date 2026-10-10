#!/usr/bin/env bash
# 结构自检：frontmatter、命名、断链、清单合法性、常驻开销。
# 从上游同步或新增 skill 之后跑一次。
set -euo pipefail
DEVKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -I - "$DEVKIT_DIR" <<'PY'
import glob, json, os, re, sys

dk = sys.argv[1]
fail = []

rows = []
for f in sorted(glob.glob(os.path.join(dk, "skills", "*", "SKILL.md"))):
    d = os.path.basename(os.path.dirname(f))
    t = open(f, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        fail.append(f"{d}: 缺 frontmatter"); continue
    fm = m.group(1)
    nm = re.search(r"^name:\s*(.*)$", fm, re.M)
    de = re.search(r"^description:\s*(.*?)(?=\n[a-z-]+:|\Z)", fm, re.S | re.M)
    nm = nm.group(1).strip() if nm else ""
    dl = len(de.group(1).strip()) if de else 0
    if nm != d:  fail.append(f"{d}: name 为 {nm!r}，与目录不符")
    if dl == 0:  fail.append(f"{d}: description 为空")
    rows.append((d, dl))

names = [r[0] for r in rows]
for n in {x for x in names if names.count(x) > 1}:
    fail.append(f"{n}: name 重复")

# 收录的 skill 之间互相引用是否可达
for f in glob.glob(os.path.join(dk, "skills", "**", "*.md"), recursive=True):
    body = open(f, encoding="utf-8").read()
    rel = os.path.relpath(f, dk)
    for ref in sorted(set(re.findall(r"devkit:([a-z-]+)", body))):
        if not os.path.isdir(os.path.join(dk, "skills", ref)):
            fail.append(f"{rel}: 引用未收录的 devkit:{ref}")
    for _, link in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", body):
        if link.startswith(("http", "#", "mailto", "./src/")):
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(f), link.split("#")[0]))
        if not os.path.exists(tgt):
            fail.append(f"{rel}: 断链 {link}")

for p in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    full = os.path.join(dk, p)
    if not os.path.exists(full):
        fail.append(f"缺少 {p}")
    else:
        try: json.load(open(full, encoding="utf-8"))
        except json.JSONDecodeError as exc: fail.append(f"{p}: JSON 非法 {exc}")

total = sum(r[1] for r in rows)
print(f"skill {len(rows)} 个")
print(f"常驻 description {total} 字符，约 {round(total/3.6)} tokens，平均 {round(total/max(len(rows),1))} 字符")
if fail:
    print(f"\n发现 {len(fail)} 个问题：")
    for x in fail: print("  -", x)
    sys.exit(1)
print("\n全部检查通过")
PY
