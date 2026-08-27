#!/usr/bin/env python3
"""
sanitize_emdash.py - Replace em-dash (U+2014) with standard ASCII hyphens (-) or colons across all files.
"""

import os
import glob

def sanitize_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    em_dash = '\u2014'
    if em_dash not in content:
        return False

    # Replace em-dashes
    # Context-aware replacement: " - " -> " - ", "-" -> "-"
    cleaned = content.replace(f' {em_dash} ', ' - ').replace(em_dash, '-')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    return True

def main():
    root = os.getcwd()
    modified = 0
    patterns = ['**/*.md', '**/*.py', '**/*.sh', '**/*.ps1', '**/*.bat']
    for p in patterns:
        for f in glob.glob(os.path.join(root, p), recursive=True):
            if '.git' in f.replace('\\', '/').split('/'):
                continue
            if sanitize_file(f):
                print(f"Sanitized: {os.path.relpath(f, root)}")
                modified += 1
    print(f"Total files sanitized: {modified}")

if __name__ == '__main__':
    main()

