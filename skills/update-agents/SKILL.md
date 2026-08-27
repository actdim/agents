---
name: update-agents
description: Check and update agent protocol and skills to the latest version across the local repository, global installation, and GitHub. Use when the user asks to update agents, upgrade the repository protocol, or invokes /update-agents.
---

# Update Agents (`/update-agents`)

Automated one-liner update of repository agent context and global skills.

---

## 🎯 When to Use

1. The user asks to update or upgrade agent context/skills (e.g. *"обнови агентов"*, *"обнови контекст"*, *"upgrade agents"*, `/update-agents`).
2. Opening an existing project to ensure it is running the latest `ACTDIM-AGENTS-PROTOCOL` standard.
3. Synchronizing local global installations across Claude Code, Codex, Antigravity, and OpenCode with the latest remote GitHub releases.

---

## 🛠️ Execution Workflow

### Step 1: Run the Updater Engine
Execute the standalone updater engine on the current working directory:

```bash
python -c "
import os, sys, subprocess
# Try locating updater script in global or local skills
paths = [
    os.path.join(os.getcwd(), 'scripts', 'update_agents.py'),
    os.path.join(os.getcwd(), 'skills', 'update-agents', 'update_agents.py'),
    os.path.expanduser('~/.gemini/config/skills/update-agents/update_agents.py'),
    os.path.expanduser('~/.claude/skills/update-agents/update_agents.py'),
    os.path.expanduser('~/.codex/skills/update-agents/update_agents.py'),
]
for p in paths:
    if os.path.exists(p):
        sys.exit(subprocess.run([sys.executable, p, os.getcwd()]).returncode)
print('Updater script not found locally or globally; cloning latest from git...')
cache_dir = os.path.expanduser('~/.cache/actdim-agents/repo')
os.makedirs(cache_dir, exist_ok=True)
subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/actdim/agents.git', cache_dir], check=True)
sys.exit(subprocess.run([sys.executable, os.path.join(cache_dir, 'scripts', 'update_agents.py'), os.getcwd()]).returncode)
"
```

### Step 2: Report Results
Summarize for the user:
- Previous repository protocol version vs updated version.
- Global installation status (up-to-date or refreshed from GitHub).
- Status of entity structures, checklists, and migrations applied to the repository.

