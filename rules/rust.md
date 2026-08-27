# Rust Coding Standards & Best Practices

Modern Rust engineering conventions focusing on memory safety, zero-cost abstractions, idiomatic error handling, and performance.

---

## 1. Error Handling & Zero Panic Policy
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

## 2. Ownership, Borrowing & Allocation Efficiency
- **Borrow in Function Arguments**: Accept `&str` instead of `&String`, and `&[T]` instead of `&Vec<T>` to allow callers to pass slices without allocation.
- **Avoid Unnecessary `.clone()`**: Prefer borrowing or `std::borrow::Cow` (Clone-on-Write) when modifying data conditionally.
- **Minimize Lock Contention**: Keep `MutexGuard` and `RwLockReadGuard` lifetimes as short as possible (enclose within scoped `{ ... }` blocks).

```rust
// Recommended: Borrowing slices instead of owned collections
pub fn calculate_checksum(data: &[u8]) -> u32 {
    data.iter().fold(0u32, |acc, &byte| acc.wrapping_add(byte as u32))
}
```

---

## 3. Unsafe Code Guidelines
- **Avoid `unsafe`**: Do not use `unsafe` unless strictly interfacing with C FFI or implementing low-level performance primitives that cannot be verified by the borrow checker.
- **Mandatory `SAFETY:` Comments**: Every `unsafe` block must be immediately preceded by a `// SAFETY: <explanation>` comment explaining why the invariants are upheld.

---

## 4. Idiomatic Traits & Pattern Matching
- **Implement Standard Traits**: Implement `Debug`, `Clone`, `Default`, `PartialEq`, `From` / `Into` (or `TryFrom` / `TryInto`) instead of custom conversion functions.
- **Exhaustive Pattern Matching**: Prefer `match` expressions over nested `if / else` chains for state transitions and enums.

---

## 5. Tooling & Linting Standards
- **Clippy**: Code must pass `cargo clippy -- -D warnings` without warnings.
- **Formatting**: Always format with `cargo fmt`.
- **Quiet Test Flag**: Run tests in agent loops using `cargo test -q`.

