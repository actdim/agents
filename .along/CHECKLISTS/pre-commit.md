---
protocol: along
slug: pre-commit
title: Pre-Commit Quality Gate
category: pre-commit
created: 2026-08-27
updated: 2026-08-27
---

# Pre-Commit Verification Checklist

1. [ ] Mandatory Automated Unit Tests pass: `python -m unittest tests/test_skills_and_scripts.py` (enforced automatically by `along-commit` and `along-bump-version`).
2. [ ] Mandatory Clean Typography: zero non-ASCII characters (em-dash, curly quotes, NBSP, ZWSP).
3. [ ] Mandatory git diff inspected for zero unintended deletions or file truncations.
4. [ ] No API keys, secrets, or sensitive credentials committed.
5. [ ] Filenames are Windows-safe (no colons, YYYY-MM-DD dates).

