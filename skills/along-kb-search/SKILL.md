---
name: along-kb-search
description: Query project Knowledge Base (docs/, README.md, DECISIONS.md) using targeted structured retrieval. Use when invoking /along-kb-search.
---

# Along KB Search (`/along-kb-search`) [v2.1.1]

Fast, targeted structured retrieval across `docs/` and project documentation to minimize agent context window and token usage.

## Usage
```bash
python skills/along-kb-search/along_kb_search.py "<query>" [--limit 5] [--tag <tag>]
```
