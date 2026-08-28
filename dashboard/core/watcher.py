"""Asynchronous filesystem watcher for Along repository events."""

import asyncio
import os
import time
from pathlib import Path
from typing import AsyncGenerator, Set


class RepoWatcher:
    """Watches .along/ and docs/ directories for file changes to stream SSE events."""

    def __init__(self, root_dir: Path, poll_interval: float = 1.0):
        self.root_dir = root_dir
        self.along_dir = root_dir / ".along"
        self.docs_dir = root_dir / "docs"
        self.poll_interval = poll_interval
        self._last_mtimes: dict[str, float] = {}

    def _scan_mtimes(self) -> dict[str, float]:
        mtimes = {}
        paths_to_watch = [self.along_dir, self.docs_dir]
        for base in paths_to_watch:
            if not base.exists():
                continue
            for root, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".md") or f.endswith(".yaml") or f.endswith(".yml"):
                        fp = os.path.join(root, f)
                        try:
                            mtimes[fp] = os.path.getmtime(fp)
                        except OSError:
                            pass
        return mtimes

    async def event_generator(self) -> AsyncGenerator[str, None]:
        """Yields Server-Sent Events when files are added, modified, or deleted."""
        self._last_mtimes = self._scan_mtimes()

        while True:
            await asyncio.sleep(self.poll_interval)
            current_mtimes = self._scan_mtimes()

            changed = False
            # Check for modified or new files
            for fp, mt in current_mtimes.items():
                if fp not in self._last_mtimes or mt > self._last_mtimes[fp]:
                    changed = True
                    break

            # Check for deleted files
            if not changed and len(current_mtimes) != len(self._last_mtimes):
                changed = True

            if changed:
                self._last_mtimes = current_mtimes
                yield f"event: reload\ndata: {{\"timestamp\": {time.time()}}}\n\n"
            else:
                # Keep-alive heartbeat every 15s
                yield f": heartbeat\n\n"

