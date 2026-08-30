#!/usr/bin/env bash
# install.sh - install the ALONG skills into Claude Code, Codex, OpenCode and/or Antigravity.
# For Linux / macOS (and Git Bash on Windows).
#
# Claude, Codex & Antigravity use the same ~/.<tool>/skills/<name>/SKILL.md format -> the skill folders are copied verbatim.
# OpenCode uses flat ~/.config/opencode/commands/<name>.md commands -> generated from the same SKILL.md bodies;
#   along-init's helper files (protocol.md, along_update.py, migrate_protocol.py) are placed in ~/.config/opencode/actdim-along/.
# The ALONG-PROTOCOL itself is picked up by all four natively via each repo's AGENTS.md.
#
# Usage:
#   ./install.sh                        # all (default), copy
#   ./install.sh --target=claude        # claude | codex | opencode | antigravity | both (claude+codex) | all
#   ./install.sh --symlink              # symlink skill folders (claude/codex/antigravity); opencode commands are always generated
#   ./install.sh --claude-home=DIR --codex-home=DIR --opencode-home=DIR --antigravity-home=DIR
set -euo pipefail

TARGET=all
SYMLINK=0
INSTALL_DEPS=0
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
OPENCODE_HOME="${OPENCODE_HOME:-$HOME/.config/opencode}"
ANTIGRAVITY_HOME="${ANTIGRAVITY_HOME:-$HOME/.gemini/config}"

LEGACY_SKILLS=(
  "init-agents" "update-agents" "dashboard" "repo-dashboard"
  "bump-version" "check-graph" "wrap-session" "wrap-stage"
  "sync-context" "sync-issues" "sync-tasks" "sync-decisions"
  "sync-history" "init-kb" "sync-kb" "sync-wiki" "search-kb" "search-wiki"
  "along-wrap-session" "along-wrap-stage"
  "along-sync-issues" "along-sync-context" "along-sync-decisions" "along-sync-history"
  "along-check-graph" "along-scan-deps" "along-bump-version"
  "along-init-kb" "along-sync-kb" "along-search-kb"
)

for arg in "$@"; do
  case "$arg" in
    --target=*)           TARGET="${arg#*=}" ;;
    --symlink)            SYMLINK=1 ;;
    --install-deps)       INSTALL_DEPS=1 ;;
    --claude-home=*)      CLAUDE_HOME="${arg#*=}" ;;
    --codex-home=*)       CODEX_HOME="${arg#*=}" ;;
    --opencode-home=*)    OPENCODE_HOME="${arg#*=}" ;;
    --antigravity-home=*) ANTIGRAVITY_HOME="${arg#*=}" ;;
    *) echo "unknown arg: $arg" >&2; exit 1 ;;
  esac
done

if ! command -v uv >/dev/null 2>&1; then
  if [ "$INSTALL_DEPS" -eq 1 ]; then
    echo "-> Installing 'uv' package & Python version manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
  else
    echo "-> [Note] 'uv' is recommended for automatic Python/MCP tool management."
    echo "   Install uv:  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   Or run with: ./install.sh --install-deps"
    echo "   Or use mise: mise install"
  fi
else
  echo "-> 'uv' detected: $(command -v uv)"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
src="$SCRIPT_DIR/skills"
[ -d "$src" ] || { echo "Source skills folder not found: $src" >&2; exit 1; }

do_claude=0; do_codex=0; do_opencode=0; do_antigravity=0
case "$TARGET" in
  claude)      do_claude=1 ;;
  codex)       do_codex=1 ;;
  opencode)    do_opencode=1 ;;
  antigravity) do_antigravity=1 ;;
  both)        do_claude=1; do_codex=1 ;;
  all)         do_claude=1; do_codex=1; do_opencode=1; do_antigravity=1 ;;
  *) echo "invalid --target: $TARGET (claude|codex|opencode|antigravity|both|all)" >&2; exit 1 ;;
esac

purge_legacy_skills() {
  local dst="$1/skills"
  if [ -d "$dst" ]; then
    for leg in "${LEGACY_SKILLS[@]}"; do
      rm -rf "$dst/$leg"
    done
  fi
}

install_skillfolders() {  # $1 = tool home dir; installs SKILL.md folders verbatim
  local dst="$1/skills"
  mkdir -p "$dst"
  purge_legacy_skills "$1"
  echo "-> $dst"
  local d name target
  for d in "$src"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"; target="$dst/$name"; rm -rf "$target"
    if [ "$SYMLINK" -eq 1 ]; then
      ln -s "$(cd "$d" && pwd)" "$target"; echo "   linked  $name"
    else
      cp -r "${d%/}" "$target"; echo "   copied  $name"
    fi
  done
}

install_opencode() {  # generate flat commands + place along-init helper
  local cmddir="$OPENCODE_HOME/commands"
  local helper="$OPENCODE_HOME/actdim-along"
  local old_helper="$OPENCODE_HOME/actdim-agents"
  mkdir -p "$cmddir" "$helper"
  rm -rf "$old_helper"

  # Clean legacy commands
  for leg in "${LEGACY_SKILLS[@]}"; do
    rm -f "$cmddir/$leg.md"
  done

  [ -f "$src/along-init/protocol.md" ] && cp -f "$src/along-init/protocol.md" "$helper/protocol.md"
  [ -f "$src/along-init/migrate_protocol.py" ] && cp -f "$src/along-init/migrate_protocol.py" "$helper/migrate_protocol.py"
  [ -f "$src/along-update/along_update.py" ] && cp -f "$src/along-update/along_update.py" "$helper/along_update.py"
  [ -f "$src/along-dash/along_dash.py" ] && cp -f "$src/along-dash/along_dash.py" "$helper/along_dash.py"
  [ -f "$src/along-dep-scan/along_dep_scan.py" ] && cp -f "$src/along-dep-scan/along_dep_scan.py" "$helper/along_dep_scan.py"
  [ -f "$src/along-version-bump/along_version_bump.py" ] && cp -f "$src/along-version-bump/along_version_bump.py" "$helper/along_version_bump.py"
  [ -f "$src/along-kb-sync/along_kb_sync.py" ] && cp -f "$src/along-kb-sync/along_kb_sync.py" "$helper/along_kb_sync.py"
  [ -f "$src/along-kb-search/along_kb_search.py" ] && cp -f "$src/along-kb-search/along_kb_search.py" "$helper/along_kb_search.py"

  local d name sk desc out
  for d in "$src"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"; sk="$d/SKILL.md"; out="$cmddir/$name.md"
    desc="$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^description:/{sub(/^description:[ ]*/,"");print;exit}' "$sk")"
    {
      echo '---'
      printf 'description: "%s"\n' "$desc"
      echo '---'
      echo
      if [ "$name" = "along-init" ]; then
        echo "> OpenCode: helper files live at \`$helper\`. Where the steps below say \"this skill's folder\", use \`$helper\`."
        echo
      fi
      awk 'c>=2{print} /^---[[:space:]]*$/{c++}' "$sk"
    } > "$out"
    echo "   command $name.md"

  done
}

configure_mcp_server() {  # $1 = target file path
  local file="$1"
  local dir="$(dirname "$file")"
  mkdir -p "$dir"
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json, os, sys
path = sys.argv[1]
data = {}
if os.path.exists(path) and os.path.getsize(path) > 0:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
if not isinstance(data, dict):
    data = {}
if 'mcpServers' not in data or not isinstance(data['mcpServers'], dict):
    data['mcpServers'] = {}
if 'code-review-graph' not in data['mcpServers']:
    data['mcpServers']['code-review-graph'] = {
        'command': 'uvx',
        'args': ['code-review-graph']
    }
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'   registered code-review-graph MCP in {path}')
    except Exception as e:
        print(f'   (note: could not write {path}: {e})')
else:
    print(f'   code-review-graph MCP already configured in {path}')
" "$file" 2>/dev/null || true
  fi
}

if [ "$do_claude" -eq 1 ]; then
  install_skillfolders "$CLAUDE_HOME"
  configure_mcp_server "$(dirname "$CLAUDE_HOME")/.claude.json"
  configure_mcp_server "$CLAUDE_HOME/mcp_config.json"
fi
if [ "$do_codex" -eq 1 ]; then
  install_skillfolders "$CODEX_HOME"
  configure_mcp_server "$CODEX_HOME/mcp_config.json"
fi
if [ "$do_opencode" -eq 1 ]; then
  install_opencode
  configure_mcp_server "$OPENCODE_HOME/mcp_config.json"
fi
if [ "$do_antigravity" -eq 1 ]; then
  install_skillfolders "$ANTIGRAVITY_HOME"
  configure_mcp_server "$ANTIGRAVITY_HOME/mcp_config.json"
fi

if command -v python3 >/dev/null 2>&1 && { [ -d "$SCRIPT_DIR/.along" ] || [ -d "$SCRIPT_DIR/.agents" ]; }; then
  echo "-> Running Along versioned protocol migration for v2.0.0 compatibility..."
  python3 "$SCRIPT_DIR/scripts/migrate_protocol.py" "$SCRIPT_DIR"
fi

echo "Done. Claude/Codex/Antigravity skills register next session as /along-* (/along-init, /along-update, /along-dash, etc.); OpenCode picks up /commands, code-review-graph MCP is configured, and all read AGENTS.md natively."
