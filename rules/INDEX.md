# Language Coding Standards & Rule Packs

Modular language-specific engineering standards for `actdim-agents`.

---

## 🎯 Overview

These rule packs provide strict, pragmatic coding standards based on modern industry conventions (Microsoft, Google, PEP 8, TypeScript strict guidelines). When running `/init-agents` in a repository, the agent automatically detects project files (`package.json`, `pyproject.toml`, `*.csproj`, etc.) and attaches the matching language conventions to `## Project specifics` in `AGENTS.md` and `.agents/KB/03-setup-and-workflow.md`.

---

## 📚 Available Language Rule Packs

| Language | Rule File | Primary Focus & Standards |
| :--- | :--- | :--- |
| **C# / .NET** | [`csharp.md`](file://rules/csharp.md) | Modern .NET 8+, Nullable reference types, Async/Await correctness, Pattern matching, Memory efficiency (`Span<T>`, records). |
| **TypeScript** | [`typescript.md`](file://rules/typescript.md) | Strict type safety, Zero `any`, Explicit function return types, Discriminated unions, Immutable structures. |
| **JavaScript** | [`javascript.md`](file://rules/javascript.md) | Modern ES2022+, ESM modules, Async/Await error handling, Defensive object manipulation. |
| **Python** | [`python.md`](file://rules/python.md) | Modern Python 3.11+, PEP 8, Type annotations (`mypy`/`pyright`), Dataclasses/Pydantic, Ruff linting. |

---

## 🛠️ Usage in Repositories

1. **Automatic Detection (`/init-agents`)**:
   - The agent inspects build descriptors (`*.csproj`, `tsconfig.json`, `pyproject.toml`) and imports relevant rules.
2. **Manual Reference**:
   - Reference in `AGENTS.md`: `See rules/typescript.md for coding guidelines.`
   - Or include as a Knowledge Base article in `.agents/KB/`.

