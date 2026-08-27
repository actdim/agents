#!/usr/bin/env bash
# init-agents.sh - deterministic scaffolder for the ACTDIM-AGENTS agent-context structure.
#
# Runs under Git Bash on Windows (the shell Claude Code's Bash tool uses); also works on Linux/macOS.
# Uses only portable tools (awk / grep / date / mktemp) and computes relative paths + walks the tree
# with plain string ops (no `cd ..` subshells, no GNU-only `realpath --relative-to`).
#
# Usage: bash init-agents.sh [TARGET_DIR]
#   TARGET_DIR defaults to the git repo root of the current directory, else the current directory.
#
# Does the MECHANICAL parts only: pick FULL vs REF protocol block, create the .agents/ skeletons,
# ensure the CLAUDE.md pointer, move a folder-own VISION.md into .agents/ (source deleted).
# Intelligent migrations (relocating a legacy file's hand-written content) are left to the agent.
set -euo pipefail

MARK="ACTDIM-AGENTS-PROTOCOL"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROTOCOL_FILE="$SCRIPT_DIR/protocol.md"
if [ ! -f "$PROTOCOL_FILE" ]; then
  echo "ERROR: protocol.md not found next to the script ($PROTOCOL_FILE)" >&2
  exit 1
fi

# --- resolve target root ---
TARGET="${1:-}"
if [ -n "$TARGET" ]; then
  if [ ! -d "$TARGET" ]; then echo "ERROR: not a directory: $TARGET" >&2; exit 1; fi
  ROOT="$(cd "$TARGET" && pwd)"
else
  if ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then :; else ROOT="$(pwd)"; fi
  ROOT="$(cd "$ROOT" && pwd)"
fi
echo "Target root: $ROOT"

# --- detect FULL vs REF: nearest ANCESTOR whose AGENTS.md has a FULL block (string walk-up) ---
ANCESTOR=""
d="${ROOT%/*}"
hops=0
while [ -n "$d" ] && [ "$hops" -lt 64 ]; do
  hops=$((hops+1))
  if [ -f "$d/AGENTS.md" ] && grep -q "<!-- BEGIN $MARK root" "$d/AGENTS.md" 2>/dev/null; then
    ANCESTOR="$d"; break
  fi
  case "$d" in
    */*) d="${d%/*}" ;;
    *)   d="" ;;
  esac
done

BLOCK_FILE="$(mktemp)"
trap 'rm -f "$BLOCK_FILE" "$ROOT/AGENTS.md.new" "$ROOT/CLAUDE.md.new" 2>/dev/null || true' EXIT

if [ -z "$ANCESTOR" ]; then
  MODE="FULL (this folder is the architecture root)"
  {
    echo "<!-- BEGIN $MARK root (managed by init-agents - do not edit by hand) -->"
    cat "$PROTOCOL_FILE"
    echo "<!-- END $MARK -->"
  } > "$BLOCK_FILE"
else
  # relative path from ROOT to ANCESTOR/AGENTS.md, computed manually (portable)
  rem="${ROOT#"$ANCESTOR"/}"
  levels=0; tmp="$rem"
  while [ -n "$tmp" ]; do
    levels=$((levels+1))
    case "$tmp" in */*) tmp="${tmp#*/}" ;; *) tmp="" ;; esac
  done
  rel=""; i=0
  while [ "$i" -lt "$levels" ]; do rel="../$rel"; i=$((i+1)); done
  REL="${rel}AGENTS.md"
  MODE="REF -> $REL"
  {
    printf '%s\n' "<!-- BEGIN $MARK ref=$REL (managed by init-agents - do not edit by hand) -->"
    printf '%s\n' 'This folder belongs to a repository that uses the ACTDIM-AGENTS structure. The full working'
    printf '%s\n' "guidance + agent-context protocol live once in the nearest ancestor \`AGENTS.md\` (\`$REL\`) -"
    printf '%s\n' 'read it there. This folder keeps its OWN `.agents/` state; use the nearest one.'
    printf '%s\n' "Only this folder's specifics follow."
    printf '%s\n' "<!-- END $MARK -->"
  } > "$BLOCK_FILE"
fi
echo "Protocol block: $MODE"

# --- AGENTS.md ---
AG="$ROOT/AGENTS.md"
if [ ! -f "$AG" ]; then
  { cat "$BLOCK_FILE"; printf '\n## Project specifics\n\n<!-- Fill in: what this project is, how to build / test / run, architecture, conventions. -->\n'; } > "$AG"
  echo "AGENTS.md: created"
elif grep -q "<!-- BEGIN $MARK" "$AG"; then
  awk -v bf="$BLOCK_FILE" -v mark="$MARK" '
    BEGIN { while ((getline l < bf) > 0) blk = blk l "\n"; sub(/\n$/,"",blk) }
    index($0, "<!-- BEGIN " mark) { print blk; skip=1; next }
    skip && index($0, "<!-- END " mark " -->") { skip=0; next }
    skip { next }
    { print }
  ' "$AG" > "$AG.new" && mv "$AG.new" "$AG"
  echo "AGENTS.md: managed block refreshed"
else
  { cat "$BLOCK_FILE"; printf '\n\n'; cat "$AG"; } > "$AG.new" && mv "$AG.new" "$AG"
  echo "AGENTS.md: managed block prepended, existing content kept below"
fi

# --- CLAUDE.md ---
CL="$ROOT/CLAUDE.md"
PTR='See @AGENTS.md for project instructions and guidance.'
if [ ! -f "$CL" ]; then
  printf '%s\n' "$PTR" > "$CL"; echo "CLAUDE.md: created"
elif ! grep -q '@AGENTS.md' "$CL"; then
  { printf '%s\n\n' "$PTR"; cat "$CL"; } > "$CL.new" && mv "$CL.new" "$CL"; echo "CLAUDE.md: import line prepended"
else
  echo "CLAUDE.md: already imports @AGENTS.md (unchanged)"
fi

# --- .agents/ skeletons & migration (TASKS -> ISSUES) ---
A="$ROOT/.agents"
YEAR="$(date +%Y)"

if [ -d "$A" ]; then
  if [ -f "$A/TASKS.md" ] && [ ! -f "$A/ISSUES.md" ]; then
    mv "$A/TASKS.md" "$A/ISSUES.md"
    sed -i 's/# Tasks/# Issues/g; s/TASKS/ISSUES/g' "$A/ISSUES.md" 2>/dev/null || true
    echo "  migrated .agents/TASKS.md -> .agents/ISSUES.md"
  fi
  if [ -d "$A/TASKS" ] && [ ! -d "$A/ISSUES" ]; then
    mv "$A/TASKS" "$A/ISSUES"
    echo "  migrated .agents/TASKS/ -> .agents/ISSUES/"
  fi
  for folder in "$A/ISSUES" "$A/ISSUES/done"; do
    if [ -d "$folder" ]; then
      for f in "$folder"/*.md; do
        [ -f "$f" ] || continue
        fname="$(basename "$f")"
        if [[ "$fname" != *"--"* ]]; then
          tprefix="task"
          case "$fname" in
            *fix*|*bug*) tprefix="bug" ;;
            *add*|*feat*|*new*) tprefix="feat" ;;
            *refactor*|*clean*|*debt*) tprefix="debt" ;;
            *doc*|*readme*) tprefix="docs" ;;
          esac
          mv "$f" "$folder/${tprefix}--${fname}"
          echo "  renamed issue: $fname -> ${tprefix}--${fname}"
        fi
      done
    fi
  done
fi

mkdir -p "$A/ISSUES/done" "$A/SESSIONS/$YEAR" "$A/KB" "$A/MILESTONES" "$A/RISKS" "$A/SPIKES" "$A/CHECKLISTS"
for k in "$A/ISSUES/.gitkeep" "$A/ISSUES/done/.gitkeep" "$A/SESSIONS/$YEAR/.gitkeep" "$A/MILESTONES/.gitkeep" "$A/RISKS/.gitkeep" "$A/SPIKES/.gitkeep" "$A/CHECKLISTS/.gitkeep"; do
  if [ ! -f "$k" ]; then : > "$k"; fi
done

write_if_missing() {
  if [ -f "$1" ]; then cat > /dev/null; echo "  kept   ${1#"$ROOT"/}"; else cat > "$1"; echo "  create ${1#"$ROOT"/}"; fi
}

echo ".agents/ skeletons:"
write_if_missing "$A/CONTEXT.md" <<'EOF'
# Context

_Current-state snapshot. Keep SHORT; history goes to SESSIONS/._

- Status: initialized (no work recorded yet).
EOF

write_if_missing "$A/ISSUES.md" <<'EOF'
# Issues   (glyphs: [ ] open  [~] in-progress  [!] blocked  [x] done)

## Active

## Backlog

## Done (recent)
EOF

write_if_missing "$A/DECISIONS.md" <<'EOF'
# Decisions (ADR - append-only)

_One dated entry per architectural decision. Never edit past entries; mark a replaced one "Superseded by #N"._

<!-- Template:
## #001 - <title>
- Date: YYYY-MM-DD
- Status: accepted            (or: superseded by #NNN)
- Context: <why this came up>
- Decision: <what was decided>
- Consequences: <trade-offs / follow-ups>
-->
EOF

write_if_missing "$A/GLOSSARY.md" <<'EOF'
# Glossary

_Domain terms. Add a term when you introduce or clarify it._

<!-- - **Term** - definition. -->
EOF

write_if_missing "$A/HISTORY.md" <<'EOF'
# History

_Index of sessions (newest last). One line per session:_
_`<YYYY-MM-DD> - <slug> - <agent> - <summary> - <relative link>`_
EOF


# --- VISION: move a folder-own VISION.md into .agents/, else skeleton ---
if [ ! -f "$A/VISION.md" ]; then
  if [ -f "$ROOT/VISION.md" ]; then
    cp "$ROOT/VISION.md" "$A/VISION.md"
    rm -f "$ROOT/VISION.md"
    echo "  moved  VISION.md -> .agents/VISION.md (source deleted)"
  else
    cat > "$A/VISION.md" <<'EOF'
# Vision

_North star: scope, boundaries, non-goals, roadmap. Evolves slowly; slims as features ship._

## Scope

## Non-goals

## Roadmap
EOF
    echo "  create .agents/VISION.md"
  fi
else
  echo "  kept   .agents/VISION.md"
fi

# --- .code-review-graph-ignore ---
write_if_missing "$ROOT/.code-review-graph-ignore" <<'EOF'
# Code Review Graph Exclusions
node_modules/
dist/
build/
out/
.next/
.nuxt/
vendor/
tmp/
temp/
coverage/
.git/
.agents/SESSIONS/
*.min.js
*.bundle.js
*.map
*.pyc
__pycache__/
# --- Run versioned protocol migration for v1.5.0 compatibility ---
if command -v python3 >/dev/null 2>&1; then
  python3 "$SCRIPT_DIR/migrate_protocol.py" "$ROOT" || true
elif command -v python >/dev/null 2>&1; then
  python "$SCRIPT_DIR/migrate_protocol.py" "$ROOT" || true
fi

echo "Done: $ROOT ($MODE)"
