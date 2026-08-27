---
name: check-graph
version: "1.5.6"
description: Debug and inspect code-review-graph status, blast radius, and enforce .code-review-graph-ignore filters to prevent node_modules ballooning.
---

# Check Graph (`/check-graph`) [v1.5.6]

Use this skill to test, debug, and inspect the status of the **`code-review-graph`** MCP server and enforce strict exclusion filters.

## Usage
- `/check-graph`: Inspects overall graph statistics, community structure, and auto-detects uncommitted git changes to calculate their impact radius.
- `/check-graph <filepath>`: Calculates the impact radius (blast radius) for a specific file or list of files passed in the argument.

## Workflow & Ignore Enforcement

1. **Verify Ignore Configuration (`.code-review-graph-ignore`)**:
   - Ensure `.code-review-graph-ignore` exists in the repo root to prevent indexing heavy dependencies (`node_modules/`, `dist/`, `build/`, `vendor/`, `tmp/`, `.git/`).
   - If missing, create `.code-review-graph-ignore` with standard exclusions before triggering graph commands:
     ```gitignore
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
     ```

2. **Target Evaluation**:
   - If an explicit file or path argument is provided (e.g. `/check-graph install.ps1`), pass `changed_files: ["<filepath>"]` to `get_impact_radius_tool`.
   - If no argument is provided, auto-detect uncommitted changed files via `git status` / `git diff` and pass them to `get_impact_radius_tool`.

3. **Graph Statistics & Status**:
   - Call `list_graph_stats_tool` to display total files, nodes, edges, languages, and last update timestamp.

4. **Impact Radius (Blast Radius)**:
   - Call `get_impact_radius_tool` and present:
     - Direct changes (changed files and nodes)
     - Impacted nodes within 2 hops (functions/files calling or affected by the target)
     - Clear status if no target file or git changes were detected.
