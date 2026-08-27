---
name: along-bump-version
description: Increment project or protocol version (patch by default), sanitize typography, execute wrap-session reconciliation, and create a release git commit. Universal support for Node, Python, Rust, .NET, and custom .along/scripts/bump_version.py hooks.
---

# Along Bump Version (`/along-bump-version`) [v2.0.4]

Universal project version bumper and release pipeline engine for repositories adopting Along.

---

## When to Use
- Finalizing a milestone, stage, or version release (`/along-bump-version`, "bump version", "release new version").
- Incrementing `package.json`, `pyproject.toml`, `Cargo.toml`, or `.along/` state.
- Preparing clean ASCII typography and release git commit.

---

## Supported Stacks & Custom Hooks

1. **Custom Project Hook**:
   If `.along/scripts/bump_version.py` exists, it is executed directly to handle project-specific version files.
2. **Auto-Detected Stacks**:
   - **Node.js / TypeScript**: `package.json` & `package-lock.json`
   - **Python**: `pyproject.toml`, `setup.py`, `__init__.py`
   - **Rust**: `Cargo.toml`
   - **.NET / C#**: `Directory.Build.props`, `*.csproj`
   - **Along Development Repository**: `skills/along-*/SKILL.md`, `protocol.md`, `AGENTS.md`
   - Automatically synthesizes `.along/scripts/bump_version.py` for future transparent execution.
3. **Custom Stack Guidance**:
   If the project stack is non-standard, the engine outputs a template to scaffold `.along/scripts/bump_version.py`.

---

## Usage

```bash
python scripts/along_bump_version.py patch
python scripts/along_bump_version.py minor
python scripts/along_bump_version.py major
python scripts/along_bump_version.py 1.5.0
```

### Flags
- `-c`, `--commit`: Automatically create release `git commit` (`release: vX.Y.Z`).
- `-p`, `--push`: Automatically push release commit and tags to remote repository (`git push`).
- `-cp`, `-pc`: Combine commit and push in one command (`python scripts/along_bump_version.py patch -cp`).
- By default (without `-c`), files are updated on disk without creating a Git commit.
