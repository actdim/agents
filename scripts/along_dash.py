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
Along Dashboard & Knowledge Base Engine Runner.

Runs the dynamic Along Dashboard, OpenAPI service, and Knowledge Base search engine:
- Terminal CLI Mode: Rich executive summary tables and active issues.
- Web Mode: FastAPI + Uvicorn service with OpenAPI Swagger docs and live UI.
- Static Export Mode: Standalone single-file snapshot only when explicitly requested via --export.
"""

import sys
from pathlib import Path

# Add repo root to sys.path to enable dashboard module imports
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from dashboard.app import main

if __name__ == "__main__":
    main()
