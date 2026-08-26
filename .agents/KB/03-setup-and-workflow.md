# 03. Setup & Commands (`.agents/KB/03-setup-and-workflow.md`) [v1.2.0]

## Installation
- Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all`
- Linux/macOS: `bash install.sh --target=all`

## Slash Commands
- `/init-agents`: Scaffold agent context in any repository.
- `/init-kb`: Bootstrap structured Knowledge Base in `.agents/KB/`.
- `/search-kb <query>`: Hybrid search across project Knowledge Base.
- `/sync-kb`: Update Knowledge Base index and cross-links.
- `/check-graph`: Inspect code graph and blast radius.
- `/wrap-session`: Wrap up session and generate session log.

