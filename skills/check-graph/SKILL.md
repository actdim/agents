---
name: check-graph
version: "1.2.0"
description: Debug and inspect the code-review-graph status, impact radius (blast radius), call hierarchies, and architecture graph.
---

# Check Graph (`/check-graph`) [v1.2.0]

Use this skill to test, debug, and inspect the status of the **`code-review-graph`** MCP server.

## Usage
- `/check-graph`: Inspects overall graph statistics, community structure, and auto-detects uncommitted git changes to calculate their impact radius.
- `/check-graph <filepath>`: Calculates the impact radius (blast radius) for a specific file or list of files passed in the argument.

## Workflow

1. **Target Evaluation**:
   - If an explicit file or path argument is provided (e.g. `/check-graph install.ps1`), pass `changed_files: ["<filepath>"]` to `get_impact_radius_tool`.
   - If no argument is provided, auto-detect uncommitted changed files via `git status` / `git diff` and pass them to `get_impact_radius_tool`.

2. **Graph Statistics & Status**:
   - Call `list_graph_stats_tool` to display total files, nodes, edges, languages, and last update timestamp.

3. **Impact Radius (Blast Radius)**:
   - Call `get_impact_radius_tool` and present:
     - Direct changes (changed files and nodes)
     - Impacted nodes within 2 hops (functions/files calling or affected by the target)
     - Clear status if no target file or git changes were detected.
