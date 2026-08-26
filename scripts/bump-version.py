#!/usr/bin/env python3
"""
bump-version.py — Safely update version numbers across actdim-agents repo.
Usage:
    python scripts/bump-version.py 1.3.1
"""

import sys
import glob
import re
import os

if len(sys.argv) < 2:
    print("Usage: python scripts/bump-version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1].lstrip('v')
repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo_dir)

files_to_update = [
    'README.md',
    'AGENTS.md',
    'skills/init-agents/protocol.md',
    '.agents/CONTEXT.md',
] + glob.glob('skills/*/SKILL.md') + glob.glob('.agents/KB/*.md')

updated_count = 0
for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    
    # 1. Read cleanly
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 2. Perform safe replacements
    updated = re.sub(r'version:\s*"[^"]+"', f'version: "{new_version}"', content)
    updated = re.sub(r'\[v\d+\.\d+\.\d+\]', f'[v{new_version}]', updated)
    updated = re.sub(r'ACTDIM-AGENTS-PROTOCOL v\d+\.\d+\.\d+', f'ACTDIM-AGENTS-PROTOCOL v{new_version}', updated)
    updated = re.sub(r'actdim-agents \(v\d+\.\d+\.\d+\)', f'actdim-agents (v{new_version})', updated)
    updated = re.sub(r'Skills / commands \(v\d+\.\d+\.\d+\)', f'Skills / commands (v{new_version})', updated)
    
    # 3. Write cleanly only after read is complete
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)
    updated_count += 1

print(f"Successfully bumped version to v{new_version} across {updated_count} files!")
