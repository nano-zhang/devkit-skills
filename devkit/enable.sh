#!/usr/bin/env bash
# 在某个项目里按需启用 devkit，不碰全局配置。
#
#   ./enable.sh [项目目录]          启用，默认当前目录
#   ./enable.sh --off [项目目录]    关闭
#   ./enable.sh --status [项目目录] 查看
#
# 写入 <项目>/.claude/settings.json，合并而非覆盖，改动前自动备份。
set -euo pipefail

DEVKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE=on
case "${1:-}" in
  --off)    MODE=off;    shift ;;
  --status) MODE=status; shift ;;
  -h|--help) sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'; exit 0 ;;
esac
PROJECT="$(cd "${1:-$PWD}" && pwd)"

python3 -I - "$DEVKIT_DIR" "$PROJECT" "$MODE" <<'PY'
import json, os, shutil, sys, datetime

devkit, project, mode = sys.argv[1], sys.argv[2], sys.argv[3]
MARKET, PLUGIN = "devkit-local", "devkit@devkit-local"
path = os.path.join(project, ".claude", "settings.json")

cfg = {}
if os.path.exists(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    if text:
        try:
            cfg = json.loads(text)
        except json.JSONDecodeError as exc:
            sys.exit(f"{path} 不是合法 JSON，已中止：{exc}")

on = cfg.get("enabledPlugins", {}).get(PLUGIN) is True

if mode == "status":
    print(f"项目   {project}")
    print(f"配置   {path}{'' if os.path.exists(path) else '  (不存在)'}")
    print(f"devkit {'已启用' if on else '未启用'}")
    sys.exit(0)

if mode == "on" and on:
    print(f"已经是启用状态：{path}")
    sys.exit(0)
if mode == "off" and not on:
    print(f"本来就未启用：{path}")
    sys.exit(0)

if os.path.exists(path):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{path}.bak-{stamp}"
    shutil.copy2(path, backup)
    print(f"已备份 {backup}")

if mode == "on":
    cfg.setdefault("extraKnownMarketplaces", {})[MARKET] = {
        "source": {"source": "directory", "path": devkit}
    }
    cfg.setdefault("enabledPlugins", {})[PLUGIN] = True
    verb = "已启用"
else:
    cfg.get("extraKnownMarketplaces", {}).pop(MARKET, None)
    cfg.get("enabledPlugins", {}).pop(PLUGIN, None)
    for key in ("extraKnownMarketplaces", "enabledPlugins"):
        if key in cfg and not cfg[key]:
            del cfg[key]
    verb = "已关闭"

os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as fh:
    json.dump(cfg, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print(f"{verb} devkit")
print(f"  项目 {project}")
if mode == "on":
    print(f"  来源 {devkit}")
    print("  重启该项目下的 Claude Code 会话后生效。会话里先调 devkit-router。")
else:
    print("  重启该项目下的 Claude Code 会话后生效，常驻开销归零。")
PY
