---
protocol: along
date: 2026-09-01
slug: knowledge-base-and-skills-architecture-overhaul
agent: antigravity
branch: main
commit: pending
summary: Comprehensive overhaul of docs/ Knowledge Base, full 18-skill technical passports, multi-agent architectural rationale, and entity taxonomy.
milestone: v2.2.0-along
issues_advanced: [docs--comprehensive-knowledge-base-and-skills-architecture]
issues_completed: [docs--comprehensive-knowledge-base-and-skills-architecture]
decisions: []
risks_logged: []
spikes_conducted: []
---

# Session: Knowledge Base & Skills Architecture Overhaul

## Goal & Objectives
Transform all empty and hollow placeholder stubs in `docs/` into exhaustive, factually grounded, and rigorously structured technical documentation covering system architecture, multi-agent state machine rationale, domain entity ecosystems, LLM-Wiki retrieval mechanics, and detailed passports for all 18 Along automation skills.

## Historical Forensic Analysis (Root Cause)
- **Commit `5bab25d` Incident**: On 2026-08-30, an automated renaming routine replaced populated documentation files (`01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`) with 13-line placeholder templates.
- **Acceptance Criteria Omission**: Subsequent PRs updated internal skills and recorded ADRs, but closed issues without backfilling public `docs/` articles.

## Accomplishments
1. **`docs/topic--architecture.md` (15.4 KB)**:
   - System topology, provider compatibility (Claude Code, OpenAI Codex, OpenCode, Antigravity).
   - Multi-branch concurrency model (SSOT vs derived projections, `merge=union`).
   - End-to-end human and developer workflow.
   - Deep multi-agent state machine architectural rationale (trade-offs vs linear execution, S-size fast path vs L/XL state machine, 5 specialized role contracts, session blackboard lifecycle, AST blast radius).
2. **`docs/topic--domain-model.md` (11.2 KB)**:
   - Exhaustive taxonomy of all 9 entities: 5 issue types (`feat`, `bug`, `debt`, `task`, `docs`), Milestones, Risks, Spikes, Checklists, Sessions, History, Decisions.
   - Complete YAML front-matter schemas and canonical slug invariance rules.
   - Automated intent recognition heuristics table.
3. **`docs/topic--skills-reference.md` (20.3 KB)**:
   - Logical grouping of all 18 skills into 6 workflow phases.
   - Granular feature passports per skill: Value proposition, architectural rationale vs alternatives, invocation triggers (explicit CLI vs semantic context auto-trigger), entities touched, and chaining.
4. **`docs/topic--setup-and-workflow.md` & `docs/topic--llm-wiki-architecture.md`**:
   - Multi-platform setup, `.along/scripts/` runner hooks, and version bump workflow.
   - Karpathy LLM-Wiki paradigm, multi-tier search scoring (`Title: +10`, `Tags: +5`, `Body: +1`), and 95-98% token reduction mechanics.
5. **Compiler & Link Integrity Bugfix**:
   - Fixed `along_kb_sync.py` to skip Markdown code fences during inbound link rewriting and link validation, and prevented ISO dates from being misinterpreted as legacy numbered doc files.
   - 100% passing test suite (33/33 tests).

## Verification & Link Integrity
- `python scripts/along_kb_sync.py --strict`: Rebuilt `docs/INDEX.md`, 0 broken links across 51 relative links.
- `python .along/scripts/test.py`: 33/33 unit tests passed.
- `python scripts/along_kb_search.py`: Fast multi-scope snippet search verified.
