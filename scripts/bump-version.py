#!/usr/bin/env python3
"""
bump-version.py - Safely update version numbers across actdim-agents repo.
Usage:
    python scripts/bump-version.py patch          # Auto-increments patch: 1.5.2 -> 1.5.3
    python scripts/bump-version.py minor          # Auto-increments minor: 1.5.2 -> 1.6.0
    python scripts/bump-version.py major          # Auto-increments major: 1.5.2 -> 2.0.0
    python scripts/bump-version.py 1.5.3          # Sets explicit version
"""

import sys
import glob
import re
import os

repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo_dir)

def get_current_version():
    with open('AGENTS.md', 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)', content)
    if m:
        return m.group(1)
    return "1.0.0"

def calculate_next_version(current, mode):
    parts = [int(x) for x in current.split('.')]
    if len(parts) != 3:
        parts = [1, 0, 0]
    major, minor, patch = parts
    if mode in ('patch', '--patch'):
        return f"{major}.{minor}.{patch + 1}"
    elif mode in ('minor', '--minor'):
        return f"{major}.{minor + 1}.0"
    elif mode in ('major', '--major'):
        return f"{major + 1}.0.0"
    else:
        return mode.lstrip('v')

if len(sys.argv) < 2:
    current = get_current_version()
    print(f"Current version: v{current}")
    print("Usage: python scripts/bump-version.py [patch|minor|major|<version>]")
    sys.exit(1)

mode = sys.argv[1].lower()
current_version = get_current_version()
new_version = calculate_next_version(current_version, mode)

files_to_update = [
    'README.md',
    'AGENTS.md',
    'skills/init-agents/protocol.md',
    'skills/init-agents/migrate_protocol.py',
    'scripts/migrate_protocol.py',
    'scripts/update_agents.py',
    'skills/update-agents/update_agents.py',
    '.agents/CONTEXT.md',
] + glob.glob('skills/*/SKILL.md') + glob.glob('.agents/KB/*.md')

updated_count = 0
for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = re.sub(r'version:\s*"[^"]+"', f'version: "{new_version}"', content)
    updated = re.sub(r'CURRENT_PROTOCOL_VERSION\s*=\s*"[^"]+"', f'CURRENT_PROTOCOL_VERSION = "{new_version}"', updated)
    updated = re.sub(r'\[v\d+\.\d+\.\d+\]', f'[v{new_version}]', updated)
    updated = re.sub(r'ACTDIM-AGENTS-PROTOCOL v\d+\.\d+\.\d+', f'ACTDIM-AGENTS-PROTOCOL v{new_version}', updated)
    updated = re.sub(r'actdim-agents \(v\d+\.\d+\.\d+\)', f'actdim-agents (v{new_version})', updated)
    updated = re.sub(r'Skills / commands \(v\d+\.\d+\.\d+\)', f'Skills / commands (v{new_version})', updated)
    
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(updated)
    updated_count += 1

print(f"Successfully bumped version: v{current_version} -> v{new_version} across {updated_count} files!")
