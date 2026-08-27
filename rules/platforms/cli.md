# CLI & Developer Tooling Guidelines & Best Practices

Strict standards for Command-Line Interfaces (CLI), developer tools, and automation scripts.

---

## 1. Stream Isolation & Pipeability

1. **Strict Stream Separation**:
   - `stdout`: Reserved strictly for primary command output / data (JSON, tables, requested content) that downstream tools may pipe or parse.
   - `stderr`: Reserved for status messages, progress bars, logs, and error outputs.

2. **Non-Interactive & Scripting Friendly**:
   - Detect non-interactive TTY environments (`isatty()`) or `--quiet` / `--json` flags to disable interactive prompts, animations, and spinners.
   - Respect the `NO_COLOR` environment variable (http://no-color.org) and disable ANSI escape codes when stdout is redirected or piped.

---

## 2. Exit Code Contracts

1. **Standard Exit Codes**:
   - Exit `0`: Success / clean execution.
   - Exit `1`: General application error or domain failure.
   - Exit `2`: Invalid CLI arguments, missing flags, or usage syntax error.
   - Exit `130`: Terminated by user interrupt (`Ctrl+C` / `SIGINT`).

---

## 3. Flag Parsing & Argument Standards

1. **POSIX / GNU Flag Conventions**:
   - Support standard short (`-f`) and long (`--flag`) options.
   - Always provide `--help` (`-h`) and `--version` (`-v`) flags.
   - Fail fast with informative usage messages if unknown flags are passed.

