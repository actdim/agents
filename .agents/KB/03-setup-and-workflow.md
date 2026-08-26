# 03. Setup & Commands (`.agents/KB/03-setup-and-workflow.md`) [v1.2.0]

## Installation Options

### Option A: Clone & Install (Recommended)
- **Windows (PowerShell)**:
  ```powershell
  git clone https://github.com/actdim/actdim-agents.git
  cd actdim-agents
  powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
  ```
- **Linux / macOS (Bash)**:
  ```bash
  git clone https://github.com/actdim/actdim-agents.git
  cd actdim-agents
  bash install.sh --target=all
  ```

### Option B: One-Liner Quick Install
- **Windows (PowerShell)**: `irm https://raw.githubusercontent.com/actdim/actdim-agents/main/install.ps1 | iex`
- **Linux / macOS (Bash)**: `curl -fsSL https://raw.githubusercontent.com/actdim/actdim-agents/main/install.sh | bash`

## Slash Commands
- `/init-agents`: Scaffold agent context in any repository.
- `/init-kb`: Bootstrap structured Knowledge Base in `.agents/KB/` from `README.md`, `AGENTS.md`, and `docs/`.
- `/search-kb <query>`: Hybrid search across project Knowledge Base.
- `/sync-kb`: Update Knowledge Base index and cross-links.
- `/check-graph`: Inspect code graph and blast radius.
- `/wrap-session`: Wrap up session and generate session log.
