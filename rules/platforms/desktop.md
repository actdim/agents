# Desktop Application Engineering Guidelines & Best Practices

Strict architectural and security standards for Desktop applications (Tauri, Electron, .NET MAUI/WPF, Native).

---

## 1. IPC & Security Boundaries

1. **Principle of Least Privilege**:
   - Never expose raw Node.js or OS system calls directly to renderer processes (e.g. disable `nodeIntegration: true` and enable `contextIsolation: true` in Electron).
   - In Tauri, restrict `tauri.conf.json` permissions to strictly needed core plugins (`fs:allow-read`, `dialog:allow-open`).

2. **IPC Message Validation**:
   - Treat all IPC commands sent from renderer UI as untrusted input. Validate schemas on the backend / native host process before executing filesystem or shell operations.
   - Use typed command invocations (e.g. `invoke("plugin:name|command", payload)` with strict schema validation).

---

## 2. File System Access & Sandboxing

1. **Path Resolution & Traversal Prevention**:
   - Always resolve paths against standard OS application directories (`app_data_dir`, `app_config_dir`, `app_cache_dir`).
   - Validate and sanitize paths to prevent directory traversal (`../`) vulnerabilities when opening user files.

2. **Safe File Operations**:
   - Use atomic writes (`write to temp file -> rename`) for configuration and state files to prevent corruption during unexpected shutdowns.

---

## 3. Window & Process Lifecycle

1. **Graceful Shutdown & Background Tasks**:
   - Intercept window close events (`on_close_requested` / `window.onbeforeunload`) to persist unsaved state or prompt user confirmation.
   - Ensure child background processes and sidecars are cleanly killed when the main application exits.

2. **Multi-Window State Synchronization**:
   - Use a single source of truth (central background state / IPC bus) for synchronized data across multiple application windows.

---

## 4. Local Database & Offline-First Storage

1. **Embedded Databases**:
   - Prefer embedded ACID-compliant engines (SQLite via `rusqlite` / `better-sqlite3`, DuckDB) for local data caching and indexing.
   - Run database migrations deterministically at application startup before opening the UI.

