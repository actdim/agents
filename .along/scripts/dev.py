# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastapi>=0.110.0",
#     "uvicorn>=0.28.0",
#     "pydantic>=2.0.0",
#     "pyyaml>=6.0.0",
#     "rich>=13.0.0",
# ]
# ///

"""
Along Development Runner (.along/scripts/dev.py).
Launches the full dev environment with Vite HMR frontend (port 5173) and live FastAPI backend (port 8765).
"""

import sys
from pathlib import Path

# Add repo root to sys.path
repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from dashboard.app import main

if __name__ == "__main__":
    # Default to dev mode if no explicit mode arguments passed
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] not in ("-w", "--web", "-c", "--cli", "--export")):
        sys.argv.append("--dev")
    main()

