#!/usr/bin/env bash
# install.sh — install the ACTDIM-AGENTS skills into Claude Code, Codex, OpenCode and/or Antigravity.
# For Linux / macOS (and Git Bash on Windows).
#
# Claude, Codex & Antigravity use the same ~/.<tool>/skills/<name>/SKILL.md format -> the skill folders are copied verbatim.
# OpenCode uses flat ~/.config/opencode/commands/<name>.md commands -> generated from the same SKILL.md bodies;
#   init-agents' helper files (protocol.md, init-agents.sh) are placed in ~/.config/opencode/actdim-agents/.
# The ACTDIM-AGENTS-PROTOCOL itself is picked up by all four natively via each repo's AGENTS.md.
#
# Usage:
#   ./install.sh                        # all (default), copy
#   ./install.sh --target=claude        # claude | codex | opencode | antigravity | both (claude+codex) | all
#   ./install.sh --symlink              # symlink skill folders (claude/codex/antigravity); opencode commands are always generated
#   ./install.sh --claude-home=DIR --codex-home=DIR --opencode-home=DIR --antigravity-home=DIR
set -euo pipefail

TARGET=all
SYMLINK=0
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
OPENCODE_HOME="${OPENCODE_HOME:-$HOME/.config/opencode}"
ANTIGRAVITY_HOME="${ANTIGRAVITY_HOME:-$HOME/.gemini/config}"
for arg in "$@"; do
  case "$arg" in
    --target=*)           TARGET="${arg#*=}" ;;
    --symlink)            SYMLINK=1 ;;
    --claude-home=*)      CLAUDE_HOME="${arg#*=}" ;;
    --codex-home=*)       CODEX_HOME="${arg#*=}" ;;
    --opencode-home=*)    OPENCODE_HOME="${arg#*=}" ;;
    --antigravity-home=*) ANTIGRAVITY_HOME="${arg#*=}" ;;
    *) echo "unknown arg: $arg" >&2; exit 1 ;;
  esac
done

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

install_skillfolders() {  # $1 = tool home dir; installs SKILL.md folders verbatim
  local dst="$1/skills"
  mkdir -p "$dst"
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

install_opencode() {  # generate flat commands + place init-agents helper
  local cmddir="$OPENCODE_HOME/commands"
  local helper="$OPENCODE_HOME/actdim-agents"
  mkdir -p "$cmddir" "$helper"
  echo "-> $cmddir (commands) + $helper (helper)"
  cp -f "$src/init-agents/protocol.md"   "$helper/protocol.md"
  cp -f "$src/init-agents/init-agents.sh" "$helper/init-agents.sh"
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
      if [ "$name" = "init-agents" ]; then
        echo "> OpenCode: the helper script is at \`$helper/init-agents.sh\` and the protocol at \`$helper/protocol.md\`. Where the steps below say \"this skill's folder\", use \`$helper\`."
        echo
      fi
      awk 'c>=2{print} /^---[[:space:]]*$/{c++}' "$sk"
    } > "$out"
    echo "   command $name.md"
  done
}

if [ "$do_claude" -eq 1 ]; then install_skillfolders "$CLAUDE_HOME"; fi
if [ "$do_codex" -eq 1 ]; then install_skillfolders "$CODEX_HOME"; fi
if [ "$do_opencode" -eq 1 ]; then install_opencode; fi
if [ "$do_antigravity" -eq 1 ]; then install_skillfolders "$ANTIGRAVITY_HOME"; fi

echo "Done. Claude/Codex/Antigravity skills register next session as /init-agents etc.; OpenCode picks up /commands and all read AGENTS.md natively."

