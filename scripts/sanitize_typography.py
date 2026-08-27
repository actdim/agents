#!/usr/bin/env python3
"""
sanitize_typography.py - Replace non-ASCII typographic and invisible characters
with standard ASCII equivalents across code, scripts, and markdown documentation.
"""

import os
import sys
import glob

# Comprehensive replacement map for non-ASCII typography & invisible characters
REPLACEMENTS = {
    # Dashes, hyphens & minuses
    '\u2014': '-',      # em-dash (-)
    '\u2013': '-',      # en-dash (-)
    '\u2212': '-',      # math minus (-)
    '\u2011': '-',      # non-breaking hyphen (-)
    '\u2012': '-',      # figure dash (-)
    '\u2015': '-',      # horizontal bar (-)

    # Quotes & apostrophes
    '\u201c': '"',      # left double quotation mark (")
    '\u201d': '"',      # right double quotation mark (")
    '\u2018': "'",      # left single quotation mark (')
    '\u2019': "'",      # right single quotation mark / apostrophe (')
    '\u201a': "'",      # single low-9 quotation mark (")
    '\u201e': '"',      # double low-9 quotation mark (")
    '\u00ab': '"',      # left-pointing double angle quotation mark (")
    '\u00bb': '"',      # right-pointing double angle quotation mark (")
    '\u2032': "'",      # prime (')
    '\u2033': '"',      # double prime (")
    '\u2035': "'",      # reversed prime (')

    # Ellipsis
    '\u2026': '...',    # horizontal ellipsis (...)

    # Bullets
    '\u2022': '-',      # bullet (-)
    '\u2023': '-',      # triangular bullet (-)
    '\u2043': '-',      # hyphen bullet (-)

    # Invisible & special whitespace
    '\u00a0': ' ',      # non-breaking space (NBSP)
    '\u2007': ' ',      # figure space
    '\u202f': ' ',      # narrow non-breaking space
    '\u3000': ' ',      # ideographic space
    '\u2002': ' ',      # en space
    '\u2003': ' ',      # em space
    '\u2009': ' ',      # thin space
    '\u200a': ' ',      # hair space
    '\u200b': '',       # zero-width space (ZWSP)
    '\u200c': '',       # zero-width non-joiner (ZWNJ)
    '\u200d': '',       # zero-width joiner (ZWJ)
    '\ufeff': '',       # zero-width no-break space / byte order mark (BOM)
}

def sanitize_content(content):
    modified = False
    cleaned = content

    # Contextual replacement for em-dash with surrounding spaces: " - " instead of " - "
    em_dash = '\u2014'
    if f' {em_dash} ' in cleaned:
        cleaned = cleaned.replace(f' {em_dash} ', ' - ')
        modified = True

    for char, replacement in REPLACEMENTS.items():
        if char in cleaned:
            cleaned = cleaned.replace(char, replacement)
            modified = True

    return cleaned, modified

def sanitize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return False

    cleaned, modified = sanitize_content(content)
    if not modified:
        return False

    try:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(cleaned)
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    modified_count = 0
    patterns = ['**/*.md', '**/*.py', '**/*.sh', '**/*.ps1', '**/*.bat', '**/*.json', '**/*.yaml', '**/*.yml', '**/*.toml']

    for p in patterns:
        for f in glob.glob(os.path.join(root, p), recursive=True):
            rel_parts = os.path.relpath(f, root).replace('\\', '/').split('/')
            if any(part in ('.git', 'node_modules', 'dist', 'build', '.venv', 'venv') for part in rel_parts):
                continue
            if sanitize_file(f):
                print(f"Sanitized: {os.path.relpath(f, root)}")
                modified_count += 1

    print(f"Total files sanitized: {modified_count}")

if __name__ == '__main__':
    main()
