#!/usr/bin/env python3
"""
bump-version.py - Alias entrypoint for along_bump_version.py.
"""
import sys
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(script_dir, "along_bump_version.py")
    if os.path.exists(target):
        os.execv(sys.executable, [sys.executable, target] + sys.argv[1:])
    else:
        print("[Error] along_bump_version.py not found.", file=sys.stderr)
        sys.exit(1)
