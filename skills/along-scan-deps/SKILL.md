---
name: along-scan-deps
description: Scan direct declared project dependencies (Node/pnpm/npm, Python, Rust/Cargo), identify AI rules/instructions (AGENTS.md, llms.txt, package.json AI fields), and register them in .along/KB/dependencies.md. Use when invoking /along-scan-deps.
---

# Along Scan Dependencies (`/along-scan-deps`) [v2.0.10]

Discovers AI documentation and guidelines shipped inside declared project dependencies and registers them into the Knowledge Base (`.along/KB/dependencies.md`).

## What it does
1. **Manifest Inspection**: Detects top-level dependencies declared in:
   - Node: `package.json` (`dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies`).
   - Python: `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`.
   - Rust: `Cargo.toml` (`[dependencies]`, `[dev-dependencies]`, `[build-dependencies]`).
2. **On-Disk AI Rules Discovery**: Locates installed packages and inspects for:
   - `AGENTS.md`, `CLAUDE.md`, `llms.txt`, `llms-full.txt`, `LLMS.txt`, `LLMS.md`, `.along/`
   - Manifest metadata keys (`ai`, `llms`, `agents`, `along`).
3. **Idempotent KB Registry**: Builds or refreshes `.along/KB/dependencies.md` and links it in `.along/KB/INDEX.md`.

## Execution
Run the dependency scanner directly via Python:

```bash
python skills/along-scan-deps/along_scan_deps.py
```

### CLI Flags
- `--check`: Perform dry-run scan without modifying `.along/KB/`.
- `--json`: Output discovered dependencies in structured JSON format.
- `--quiet` / `-q`: Minimal console output.
- `--root <path>`: Specify custom repository root directory.

