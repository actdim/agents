---
slug: feat--bump-version-skill-and-typography-sanitizer
type: feat
status: done
priority: medium
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [skills, release, typography, versioning]
milestone: v1.5.0-dashboard-and-analytics
---

# Bump Version Skill & Comprehensive Typography Sanitizer

Implemented `/bump-version` release automation skill and expanded `sanitize_typography.py` to strip all non-ASCII typography and invisible characters.

## Changes Made
- Created `scripts/sanitize_typography.py` replacing `sanitize_emdash.py` with full support for em-dash, en-dash, math minus, curly quotes, guillemets, ellipsis, NBSP, and ZWSP.
- Upgraded `scripts/bump-version.py` with auto-increment calculation (`patch`, `minor`, `major`, or custom version).
- Created `skills/bump-version/SKILL.md` for one-command release automation.
- Expanded global Antigravity/Gemini and protocol formatting guidelines.
