---
name: sync-history
version: "1.5.7"
description: Reconstruct and reconcile .agents/ project history (ISSUES, MILESTONES, SESSIONS) from Git commits, tags, and PRs. Use when bootstrapping agent context on an existing git repository (cold start), when commits exist in Git that were not tracked in .agents/ (sync drift), or when the user invokes /sync-history.
---

# Sync History (`/sync-history`) [v1.5.7]

Intelligently analyze Git history (commits, tags, diffs, PR merges) and synthesize missing `.agents/` entities (`ISSUES/done/`, `MILESTONES/`, `SESSIONS/`, `HISTORY.md`) to bring project tracking and visual dashboards into 100% sync with actual Git commits.

---

## 🎯 When to Use

1. **Pattern A: Bootstrapping a Legacy Repository (Cold Start)**:
   - Initializing `actdim-agents` on an existing codebase with dozens of Git commits, tags, and releases, but no `.agents/` tracking yet.
   - Synthesizes retroactive completed issues, milestones, and session history from past commits.
2. **Pattern B: Reconciling Sync Drift (Untracked Commits)**:
   - An agent or human made several Git commits without creating issues or logging sessions.
   - Identifies orphan commits not recorded in `.agents/SESSIONS/` or `HISTORY.md` and generates corresponding completed issues and session logs.

---

## 🛠️ Execution Workflow

### Step 1: Extract Git History & Detect Unmapped Commits
Run the deterministic helper script to extract structured commits, tags, and unmapped diffs without token waste:

```bash
python "<this skill's folder>/scripts/analyze_git_history.py" [REPO_ROOT]
```

The script outputs a JSON payload containing:
- `tags`: Git tags and release dates.
- `unmapped_commits`: Commits not yet linked to any `.agents/SESSIONS/` file.
- `inferred_type`: Auto-classified issue type (`feat`, `bug`, `debt`, `docs`, `task`).

---

### Step 2: Semantic Milestone Synthesis (From Git Tags & Releases)
For each major release tag or version epoch found in Git (e.g. `v1.0.0`, `v1.2.0`):
1. Check if a matching `.agents/MILESTONES/<slug>.md` already exists.
2. If missing, create `.agents/MILESTONES/<slug>.md`:
   ```markdown
   ---
   slug: v1.0.0-initial-release
   title: "v1.0.0: Initial Core Architecture & API"
   status: completed
   due_date: 2026-05-15
   created: 2026-05-01
   target_issues: [feat--core-api-routing, feat--database-migrations]
   progress_pct: 100
   ---

   # Milestone: v1.0.0 Initial Release

   Reconstructed from Git tag `v1.0.0`.
   ```

---

### Step 3: Semantic Issue Synthesis (From Commits into `ISSUES/done/`)
Group unmapped commits into logical features or bug fixes (filtering out micro-typos):
1. For each distinct unit of work, create `.agents/ISSUES/done/<type>--<slug>.md`:
   ```markdown
   ---
   slug: <kebab-case-slug>
   type: feat | bug | debt | docs | task
   status: done
   priority: medium
   created: <commit-date>
   updated: <commit-date>
   completed: <commit-date>
   agent: git-reconstructed
   tags: [git-sync]
   milestone: <nearest-milestone-slug>
   ---

   # <Commit Subject / Feature Title>

   Reconstructed from Git commit `<short_hash>` by `<author>`.

   ## Changes Made
   - <Summary of changes from commit message>
   ```

---

### Step 4: Session Log Synthesis (From Commit Clusters)
Group commits by date/author into historical session logs in `.agents/SESSIONS/<YYYY>/`:
- File: `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md`
- Include YAML front-matter:
  ```markdown
  ---
  date: YYYY-MM-DD
  slug: <slug>
  agent: git-reconstructed
  branch: main
  commit: <short_hash>
  summary: "<summary of work reconstructed from commits>"
  milestone: <milestone-slug>
  issues_advanced: []
  issues_completed: [<issue-slugs>]
  decisions: []
  risks_logged: []
  spikes_conducted: []
  ---

  # Work Session: <Summary>

  Historical session reconstructed from Git commits.
  ```

---

### Step 5: Update Boards & Historical Indices
1. **`ISSUES.md`**: Append newly reconstructed issues to `## Done (recent)`.
2. **`HISTORY.md`**: Append chronological entries:
   `<YYYY-MM-DD> - <slug> - git-reconstructed - <summary> - <relative-link>`.
3. **`CONTEXT.md`**: Refresh current snapshot to reflect total completed issues and active milestone status.
