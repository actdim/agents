# Rust Coding Standards & Best Practices

Modern Rust engineering conventions focusing on Cargo workspace inheritance, memory safety, zero-cost abstractions, idiomatic error handling, and performance.

---

## 1. Cargo Workspaces & Dependency Inheritance

- **Workspace Dependency Centralization**:
  - In multi-crate repositories, define external dependency versions centrally in the root `Cargo.toml` under `[workspace.dependencies]`.
  - Member crates must inherit dependencies via `{ workspace = true }` to eliminate version divergence across crates.

```toml
# Cargo.toml (root)
[workspace]
members = ["crates/*"]

[workspace.dependencies]
tokio = { version = "1.38", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"

# crates/core/Cargo.toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
```

---

## 2. Error Handling & Zero Panic Policy

- **Ban `.unwrap()` and `.expect()` in Production**: Never use `.unwrap()` or `.expect()` in library or application runtime logic. Use the `?` operator, pattern matching (`match`, `if let`), or combinators (`.ok_or()`, `.map_err()`).
- **Domain Errors with `thiserror`**: Use `thiserror` for typed library and domain error enums.
- **Application Errors with `anyhow`**: Use `anyhow::Result` strictly at top-level application boundaries (CLI, main entry points).

```rust
// Recommended: Typed domain error with thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("connection failed: {0}")]
    ConnectionFailed(String),
    #[error("record not found with id: {0}")]
    NotFound(u64),
}
```

---

## 3. Ownership, Borrowing & Allocation Efficiency

- **Borrow in Function Arguments**: Accept `&str` instead of `&String`, and `&[T]` instead of `&Vec<T>` to allow callers to pass slices without allocation.
- **Avoid Unnecessary `.clone()`**: Prefer borrowing or `std::borrow::Cow` (Clone-on-Write) when modifying data conditionally.
- **Minimize Lock Contention**: Keep `MutexGuard` and `RwLockReadGuard` lifetimes as short as possible (enclose within scoped `{ ... }` blocks).

---

## 4. Unsafe Code Guidelines

- **Avoid `unsafe`**: Do not use `unsafe` unless strictly interfacing with C FFI or implementing low-level performance primitives that cannot be verified by the borrow checker.
- **Mandatory `SAFETY:` Comments**: Every `unsafe` block must be immediately preceded by a `// SAFETY: <explanation>` comment explaining why the invariants are upheld.

---

## 5. Tooling & Linting Standards

- **Clippy**: Code must pass `cargo clippy -- -D warnings` without warnings.
- **Formatting**: Always format with `cargo fmt`.
- **Quiet Test Flag**: Run tests in agent loops using `cargo test -q`.

---

## 6. Crate Packaging & Cargo AI Documentation (LLM-Wiki)

- **Cargo Packaging with `include` Whitelist (Standard / Vanilla)**:
  - When publishing crates to `crates.io` or internal registries via `cargo publish`, explicitly specify the `include` field in `Cargo.toml` to ensure AI instructions and Knowledge Base articles are packaged into the `.crate` archive.

```toml
# Cargo.toml
[package]
name = "myorg-core"
version = "0.1.0"
edition = "2021"
readme = "README.md"
keywords = ["along", "ai-agent", "llms", "rules"]
include = [
    "src/**/*",
    "Cargo.toml",
    "README.md",
    "AGENTS.md",
    "llms.txt",
    "docs/**/*",
]

[package.metadata.ai]
agents = "AGENTS.md"
llms = "llms.txt"
wiki = "docs"
```

- **Consumer & Upward Discovery Protocol**:
  - Downstream crates inheriting or declaring the dependency download unpacked crate sources into `~/.cargo/registry/src/` or vendor directory.
  - The Along dependency scanner (`along-dep-scan`) inspects `Cargo.toml` dependencies, locates crate source directories in Cargo cache/vendor, and registers `AGENTS.md` and `docs/` in `docs/topic--dependencies.md`.


