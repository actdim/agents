# JavaScript Coding Standards & Best Practices

Modern ES2022+ ECMAScript conventions for clean, resilient JavaScript codebases.

---

## 1. Modern Syntax & Module Architecture
- **ES Modules (ESM)**: Always use `import` and `export` statements instead of CommonJS `require()` / `module.exports` (unless working with legacy tooling).
- **Const by Default**: Use `const` for all variable declarations. Use `let` only when variable reassignment is strictly required. Never use `var`.
- **Destructuring with Defaults**: Use object and array destructuring with fallback defaults to prevent `undefined` access.

```javascript
// Recommended: Destructuring with defaults
function handleUser({ id, name = "Anonymous", roles = [] } = {}) {
  // ...
}
```

---

## 2. Asynchronous Execution & Error Handling
- **Async / Await**: Prefer `async` / `await` over raw promise `.then()` chains.
- **Try-Catch Scope**: Keep `try / catch` blocks tightly scoped around operations that can actually throw (e.g. JSON parsing, network I/O).
- **Avoid Unhandled Rejections**: Always handle or re-throw rejected promises with contextual error messages.

---

## 3. Defensive Programming & Quality
- **Strict Equality**: Always use `===` and `!==` instead of loose equality (`==` / `!=`).
- **Defensive Object Operations**: Use `Object.freeze()` on static configuration dictionaries.
- **JSDoc Type Hints**: Use structured JSDoc comments (`@param`, `@returns`, `@typedef`) on public utility functions for editor autocompletion and type checking (`// @ts-check`).

